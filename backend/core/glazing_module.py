"""
GlazingModule — rough first-pass trade module for glazing scope.

Phase:        C.3c-build (2026-04-28)
Source spec:  MARCH_ORDERS_C_3c_build.md §1 (Daniel's verbatim 2026-04-28 spec)
Vault rule:   applied at sealing per CLAUDE.md §3 Decision 15.

The module ships ROUGH. Output may be incomplete, over-pull, under-pull, or
misclassify. That is acceptable at this phase. Tuning happens in dedicated
sessions with `core/` frozen, after the C.3c-run sweep produces real-bidset
output. The vagueness of the search heuristics is intentional per spec
("most architects do not do things uniformly"); tightening them in advance
bakes in assumptions about uniformity that don't hold.

Search strategy (per spec, applied to a single TradeModuleInput page):

    1. Schedule-first.        Look at input.tables and input.interior_text_blocks
                              for door / window / storefront / glazing schedule
                              shapes. Pull mark + size + system + glass + finish
                              + manufacturer from schedule rows when found.
    2. Elevation reconciliation. Scan interior text for glazing-verbiage mark
                              callouts (W-1, SF-1, etc.). Count occurrences.
                              Reconcile counts against schedule rows.
    3. Title-page fallback.   If no schedule shape found in tables, scan the
                              page text for sheet-index entries that name
                              glazing schedules (e.g., "A-601 DOOR SCHEDULE").
    4. Various-pages fallback. If neither schedule nor title-page reveals
                              schedule content, scan all interior text for
                              row-shaped patterns matching schedule headers.

Field set (per spec). Three list[dict] outputs on TradeModuleOutput, with
keys defined here. Dimensions are decimal feet to .0000 precision.

    glazing_items   — mark, count, system, glass_type, manufacturer,
                      color_finish, width_ft, height_ft, sqft, location,
                      source_page, confidence
    door_items      — mark, count, door_type, frame_type, manufacturer,
                      door_kind, material, glass_door, finish, location,
                      width_ft, height_ft, source_page, confidence
    storefront_items — mark, count, system_type, manufacturer,
                      sqft_per_segment, door_in_segment,
                      double_door_in_segment, location, finish, width_ft,
                      height_ft, source_page, confidence

Confidence is a simple vocabulary-match score (1.0 direct, 0.7 alias / fuzzy,
0.4 fallback inference, 0.2 various-pages fallback). NOT calibrated — the
sweep tells us whether the scale is meaningful.

Known limitations (rough-ship, deliberately not addressed in this phase):

  - Schedule parsing assumes pdfplumber-style nested rows (`list[list[list[str]]]`)
    or a flat list-of-rows (`list[list[str]]`). Other table shapes will not
    parse.
  - Rasterized schedule pages have no text layer and will not be parsed
    (OCR is a separate, future workstream).
  - Mark extraction uses a simple regex (W-/D-/SF-/WIN-/DOOR- prefixes plus
    the bare numeric door-number convention). Architect-specific naming
    schemes outside that pattern will be missed.
  - Reconciliation is per-page only; cross-page reconciliation (e.g., a
    schedule on A-601 against elevation marks on A-201) happens at the
    dispatch / aggregation layer, which is NOT activated this phase.
  - Manufacturer matching is alias-aware whole-word; brand names that
    appear only inside a longer string ("YKK-AP-XYZ") may not match.
  - Dimension parsing handles X'-Y", X'-Y, X' Y", X ft Y in, decimal feet,
    and bare X'. Fractional inches like 1/2 or 1-1/2 are accepted; mixed
    notations within one cell may not parse cleanly.
  - Single-leaf vs pair classification for doors uses keyword inference
    only ("DOUBLE", "PAIR" → pair; otherwise single). Wrong on bidsets that
    indicate pair status by other means (visual symbol, schedule column
    not parsed, etc.).
  - The various-pages fallback is intentionally vague per spec; over-pull
    is expected and acceptable.
  - No HVHZ vs non-HVHZ branch selection. The vocabulary distinguishes
    them; the module does not yet use the distinction.
  - No CSI section number extraction. Spec sections live in the spec book,
    not the drawing sheets, per C.3a §4.5.
  - Confidence scores are rough vocabulary-match-quality numbers, not
    domain-validated.

These limitations are surfaced in this docstring per CLAUDE.md §3 Decision
15: rough modules are diagnostic surfaces; the docstring tells the future
tuning session where to start.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Optional

from core.trade_module import (
    TradeModule,
    TradeModuleInput,
    TradeModuleOutput,
    TradeFieldValue,
)
from core.glazing_vocabulary import (
    COMPONENTS,
    SYSTEMS,
    HARDWARE_SETS,
    MANUFACTURERS,
    GLAZING_VOCABULARY,
)


# ===========================================================================
# Dimension parsing
# ===========================================================================
# Converts architect dimension notations to decimal feet at .0000 precision.
# Per spec: width / height to .0000 precision (e.g., "4'-1\"" → 4.0833).
# ===========================================================================

# X'-Y" or X'-Y or X' Y" — feet-and-inches, optional fractional inches.
# Captures: feet, inches integer, fractional inches (optional).
_FT_IN_RE = re.compile(
    r"""(?xi)
    (?P<ft>\d+)              # feet
    \s*['′]\s*           # foot tick (' or unicode prime)
    -?\s*
    (?:(?P<in>\d+)            # whole inches (optional)
       (?:\s+(?P<num>\d+)/(?P<den>\d+))?  # fractional inches (optional)
       |(?P<frac_only>\d+)/(?P<den2>\d+)  # fraction-only inches
    )?
    \s*[\"″]?            # inch tick (optional)
    """
)

# "X ft Y in" — words form
_FT_IN_WORDS_RE = re.compile(
    r"(?i)(?P<ft>\d+)\s*(?:ft|feet|foot)\s*"
    r"(?:(?P<in>\d+(?:\.\d+)?)\s*(?:in|inch|inches|\"))?"
)

# Bare decimal feet, e.g. "4.0833" or "4.5"
_DECIMAL_RE = re.compile(r"(?P<dec>\d+\.\d+)")


def _parse_dimension(text: Any) -> Optional[float]:
    """Parse architect dimension text → decimal feet at .0000 precision.

    Handles common patterns:
        4'-1"       → 4.0833
        4'-1 1/2"   → 4.1250
        4'-0"       → 4.0000
        4'          → 4.0000
        4 ft 1 in   → 4.0833
        4.0833      → 4.0833 (already decimal)
        18'-9"      → 18.7500

    Returns None for cases not handled. Per §4.5, fancy edge cases are NOT
    invented — limitation surfaced in module docstring.
    """
    if text is None:
        return None
    s = str(text).strip()
    if not s:
        return None

    # Try X'-Y" pattern first (most common architect notation).
    m = _FT_IN_RE.search(s)
    if m:
        ft = int(m.group("ft"))
        inches = 0.0
        if m.group("in"):
            inches = float(m.group("in"))
            if m.group("num") and m.group("den"):
                num = int(m.group("num"))
                den = int(m.group("den"))
                if den:
                    inches += num / den
        elif m.group("frac_only") and m.group("den2"):
            num = int(m.group("frac_only"))
            den = int(m.group("den2"))
            if den:
                inches = num / den
        return round(ft + inches / 12.0, 4)

    # Try "X ft Y in" word form.
    m = _FT_IN_WORDS_RE.search(s)
    if m:
        ft = int(m.group("ft"))
        inches = float(m.group("in")) if m.group("in") else 0.0
        return round(ft + inches / 12.0, 4)

    # Try bare decimal feet.
    m = _DECIMAL_RE.search(s)
    if m:
        return round(float(m.group("dec")), 4)

    # Bare integer feet.
    m = re.match(r"^\s*(\d+)\s*$", s)
    if m:
        return round(float(m.group(1)), 4)

    return None


# ===========================================================================
# Mark extraction
# ===========================================================================
# Mark patterns per spec — vague by design. Architects vary widely; over-pull
# acceptable.
# ===========================================================================

_MARK_RE = re.compile(
    r"""(?xi)
    \b(?P<mark>
        (?:W|WIN|WINDOW|D|DR|DOOR|SF|STOREFRONT|HW|HM|FR)
        [\s\-_]
        [A-Z0-9]{1,4}
    )\b
    """
)

_NUMERIC_DOOR_RE = re.compile(r"\b(?P<mark>1\d{2})\b")  # 100-199 typical retail


def _extract_marks(text: str, kinds: tuple[str, ...] = ("W", "WIN", "D", "DR", "DOOR", "SF")) -> list[str]:
    """Extract mark callouts from text. Rough; over-pull expected."""
    found: list[str] = []
    for m in _MARK_RE.finditer(text or ""):
        token = m.group("mark").upper().replace(" ", "-").replace("_", "-")
        prefix = token.split("-", 1)[0]
        if prefix in kinds:
            found.append(token)
    return found


# ===========================================================================
# Vocabulary matchers
# ===========================================================================

_GLASS_KEYS: tuple[str, ...] = tuple(
    k for k in COMPONENTS.keys() if k.startswith("glass_") or k.startswith("coating_")
)


def _whole_word(needle: str, haystack: str) -> bool:
    if not needle:
        return False
    return bool(re.search(rf"\b{re.escape(needle)}\b", haystack, re.IGNORECASE))


def _match_manufacturer(text: str) -> tuple[Optional[str], float]:
    """Alias-aware whole-word manufacturer match.

    Returns (canonical_name, confidence). 1.0 for canonical name, 0.7 for
    alias hit. None / 0.0 if no match.
    """
    blob = (text or "").upper()
    if not blob:
        return None, 0.0
    for name, entry in MANUFACTURERS.items():
        if _whole_word(name, blob):
            return name, 1.0
        for alias in entry.get("aliases", []) or []:
            if _whole_word(alias, blob):
                return name, 0.7
    return None, 0.0


def _match_system(text: str) -> tuple[Optional[str], float]:
    """Match the closest GLAZING_SYSTEMS key by keyword presence in text.

    Rough: looks for system-name tokens (split on '_') as whole words. The
    first system whose tokens are all present wins.
    """
    blob = (text or "").upper()
    if not blob:
        return None, 0.0
    best_name: Optional[str] = None
    best_hits = 0
    for name in SYSTEMS.keys():
        tokens = [t for t in name.split("_") if len(t) >= 3 and t.isalpha()]
        if not tokens:
            continue
        hits = sum(1 for t in tokens if _whole_word(t, blob))
        if hits > best_hits:
            best_hits = hits
            best_name = name
    if best_name and best_hits >= max(1, len(best_name.split("_")) // 2):
        return best_name, 0.7 if best_hits == len(best_name.split("_")) else 0.4
    return None, 0.0


def _match_glass_type(text: str) -> Optional[str]:
    blob = (text or "").upper()
    if not blob:
        return None
    for key in _GLASS_KEYS:
        token = key.split("_", 1)[-1].replace("_", " ")
        if _whole_word(token, blob):
            return key
        if _whole_word(key, blob):
            return key
    if _whole_word("LOW-E", blob) or _whole_word("LOW E", blob):
        return "coating_low_e"
    if _whole_word("IGU", blob):
        return "glass_insulated_unit"
    return None


def _has_glass_in_door(text: str) -> bool:
    blob = (text or "").upper()
    return any(
        _whole_word(t, blob)
        for t in ("GLASS", "GLAZING", "VISION", "LITE", "TEMPERED", "LAMINATED")
    )


def _classify_door_kind(text: str) -> str:
    blob = (text or "").upper()
    if _whole_word("PAIR", blob) or _whole_word("DOUBLE", blob):
        return "pair"
    if _whole_word("OVERHEAD", blob) or _whole_word("COILING", blob) or _whole_word("SECTIONAL", blob):
        return "overhead"
    if _whole_word("SLIDING", blob):
        return "sliding"
    if _whole_word("REVOLVING", blob):
        return "revolving"
    return "single"


def _classify_door_type(text: str) -> Optional[str]:
    blob = (text or "").upper()
    if _whole_word("HM", blob) or _whole_word("HOLLOW", blob):
        return "HM"
    if _whole_word("ALUMINUM", blob) or _whole_word("ALUM", blob) or _whole_word("STOREFRONT", blob):
        return "aluminum_storefront"
    if _whole_word("WOOD", blob):
        return "wood"
    if _whole_word("FIBERGLASS", blob):
        return "fiberglass"
    return None


# ===========================================================================
# Helpers — text/table flattening
# ===========================================================================


def _tb_text(tb: Any) -> str:
    for attr in ("content", "text"):
        v = getattr(tb, attr, None)
        if v:
            return str(v)
    if isinstance(tb, dict):
        return str(tb.get("content") or tb.get("text") or "")
    return ""


def _interior_blob(blocks: list) -> str:
    return " | ".join(_tb_text(b) for b in (blocks or []) if _tb_text(b))


def _iter_table_rows(tables: Any) -> list[list[str]]:
    """Flatten input.tables to a list of rows-of-strings.

    Accepts pdfplumber's nested form (list[list[list[str|None]]]) or a flat
    form (list[list[str]]). Other shapes return empty per the docstring's
    documented limitation.
    """
    rows: list[list[str]] = []
    if not tables:
        return rows
    for tbl in tables:
        if not isinstance(tbl, list) or not tbl:
            continue
        # Heuristic: nested if first row is a list of cells (list of str-like).
        first = tbl[0]
        if isinstance(first, list):
            for row in tbl:
                if isinstance(row, list):
                    rows.append([("" if c is None else str(c)) for c in row])
        else:
            rows.append([("" if c is None else str(c)) for c in tbl])
    return rows


# ===========================================================================
# The module
# ===========================================================================


@dataclass
class GlazingModule:
    """Rough glazing trade module. See module docstring."""

    TRADE_NAME: str = "glazing"

    @property
    def FIELDS(self) -> list[str]:
        # Informational — list of every per-item field the module *can* produce.
        return [
            "mark", "count", "system", "glass_type", "manufacturer", "color_finish",
            "width_ft", "height_ft", "sqft", "location", "source_page", "confidence",
            "door_type", "frame_type", "door_kind", "material", "glass_door", "finish",
            "system_type", "sqft_per_segment", "door_in_segment", "double_door_in_segment",
        ]

    # ---- Public entry point -------------------------------------------------

    def analyze(self, input: TradeModuleInput) -> TradeModuleOutput:
        """Per-page glazing analysis. Returns TradeModuleOutput with three
        per-item lists (glazing_items, door_items, storefront_items). Empty
        lists are returned (rather than None) when the page was inspected
        but no items were found, so consumers can distinguish "looked, found
        nothing" from "did not look" (None default on the contract).
        """
        # 1. Schedule-first
        schedules = self._find_schedules(input)

        # 2. Elevation reconciliation
        elevation_counts = self._reconcile_elevations(input, schedules)

        # 3. Title-page fallback
        if not schedules:
            schedules = self._title_page_fallback(input)

        # 4. Various-pages fallback
        if not schedules:
            schedules = self._various_pages_fallback(input)

        # 5. Synthesize items from whatever was found
        glazing_items = self._build_glazing_items(input, schedules, elevation_counts)
        door_items = self._build_door_items(input, schedules, elevation_counts)
        storefront_items = self._build_storefront_items(input, schedules, elevation_counts)

        # 6. Lightweight scope summary in the legacy `fields` dict for the
        #    Trade Panel (mirrors RoofingModule's _scope pseudo-field shape).
        fields: dict[str, TradeFieldValue] = {}
        total = len(glazing_items) + len(door_items) + len(storefront_items)
        fields["_scope"] = TradeFieldValue(
            value=f"Glazing scope: {len(glazing_items)} window / {len(door_items)} door / {len(storefront_items)} storefront items",
            confidence=0.5 if total else 0.0,
            source="auto_text" if schedules else "manual_needed",
            evidence=(
                f"{len(schedules)} schedule rows parsed; "
                f"{sum(elevation_counts.values()) if elevation_counts else 0} elevation marks counted"
            ),
            display_name="Glazing Scope",
            unit="",
        )

        return TradeModuleOutput(
            fields=fields,
            warnings=[],
            equipment_pins=[],
            glazing_items=glazing_items,
            door_items=door_items,
            storefront_items=storefront_items,
        )

    # ---- Step 1: schedule discovery ---------------------------------------

    def _find_schedules(self, input: TradeModuleInput) -> list[dict]:
        """Look at input.tables for schedule-shaped rows.

        A schedule-shaped row has at least 3 cells and at least one cell that
        looks like a mark token (W-1, SF-A, 100, etc.). Vague by design; over-
        pull acceptable per spec.

        Returns a list of dicts, one per detected schedule row, with the raw
        cell values plus a category guess (`window` / `door` / `storefront`).
        """
        rows = _iter_table_rows(getattr(input, "tables", None))
        out: list[dict] = []
        if not rows:
            return out

        # Detect a category for the table from the first non-empty row's cells
        # (header-ish heuristic). Vague.
        category = self._infer_table_category(rows)

        for r in rows:
            if not r or len(r) < 3:
                continue
            joined = " ".join(c for c in r if c).strip()
            if not joined:
                continue
            marks = _extract_marks(joined)
            if not marks and not _NUMERIC_DOOR_RE.search(joined):
                # Skip header rows / blank rows / footer rows
                continue
            mark = marks[0] if marks else (
                _NUMERIC_DOOR_RE.search(joined).group("mark") if _NUMERIC_DOOR_RE.search(joined) else ""
            )
            out.append({
                "category": category or self._infer_row_category(joined),
                "mark": mark,
                "cells": list(r),
                "joined": joined,
            })
        return out

    def _infer_table_category(self, rows: list[list[str]]) -> Optional[str]:
        head = " ".join(c for r in rows[:3] for c in r if c).upper()
        if not head:
            return None
        if "DOOR" in head and "SCHEDULE" in head:
            return "door"
        if "WINDOW" in head and ("SCHEDULE" in head or "TYPE" in head):
            return "window"
        if "STOREFRONT" in head:
            return "storefront"
        if "GLAZING" in head and "SCHEDULE" in head:
            return "window"
        return None

    def _infer_row_category(self, joined: str) -> str:
        blob = joined.upper()
        if _whole_word("STOREFRONT", blob) or _whole_word("SF", blob):
            return "storefront"
        if _whole_word("DOOR", blob) or any(_whole_word(p, blob) for p in ("D-", "DR-", "HM")):
            return "door"
        return "window"

    # ---- Step 2: elevation reconciliation ---------------------------------

    def _reconcile_elevations(
        self, input: TradeModuleInput, schedules: list[dict]
    ) -> dict[str, int]:
        """Count mark callouts in interior text. Returns mark → count.

        Per spec: scan elevation/plan text for glazing-verbiage marks; reconcile
        against schedule. Reconciliation here is a count map that builders use
        to set the `count` field on each item.
        """
        blob = _interior_blob(input.interior_text_blocks).upper()
        if not blob:
            return {}
        # Collect mark candidates: schedule marks + freshly-extracted callouts.
        scheduled = {s.get("mark", "") for s in schedules if s.get("mark")}
        callouts = _extract_marks(blob)
        counts: dict[str, int] = {}
        for mk in callouts:
            counts[mk] = counts.get(mk, 0) + 1
        for mk in scheduled:
            counts.setdefault(mk, 0)
        return counts

    # ---- Step 3: title-page fallback --------------------------------------

    def _title_page_fallback(self, input: TradeModuleInput) -> list[dict]:
        """Look for sheet-index entries naming glazing schedules.

        Vague per spec — matches lines like "A-601 DOOR SCHEDULE" or
        "A-602 WINDOW TYPES". Returns a synthetic schedules list with one
        entry per matched sheet reference (no row data, just a marker that
        a schedule sheet is referenced from this page).
        """
        blob = _interior_blob(input.interior_text_blocks)
        if not blob:
            return []
        out: list[dict] = []
        for m in re.finditer(
            r"(?im)\b(A[-\s]?\d{3}\w?)\s+([A-Z][A-Z\s/&\-]{4,40})",
            blob,
        ):
            sheet = m.group(1).upper().replace(" ", "-")
            title = m.group(2).strip().upper()
            cat: Optional[str] = None
            if "DOOR" in title and "SCHEDULE" in title:
                cat = "door"
            elif "WINDOW" in title:
                cat = "window"
            elif "STOREFRONT" in title:
                cat = "storefront"
            if cat:
                out.append({
                    "category": cat,
                    "mark": "",
                    "cells": [],
                    "joined": f"{sheet} {title} (title-page reference)",
                    "_source": "title_page_fallback",
                })
        return out

    # ---- Step 4: various-pages fallback -----------------------------------

    def _various_pages_fallback(self, input: TradeModuleInput) -> list[dict]:
        """Last-resort scan for row-shaped content in interior text.

        Intentionally vague per spec ("most architects do not do things
        uniformly"). Looks for any text block that contains a mark token
        and synthesizes a schedules-like entry. Confidence is low; over-pull
        acceptable.
        """
        out: list[dict] = []
        for tb in input.interior_text_blocks or []:
            text = _tb_text(tb)
            if not text or len(text) > 200:
                continue
            marks = _extract_marks(text)
            if not marks:
                continue
            out.append({
                "category": self._infer_row_category(text),
                "mark": marks[0],
                "cells": [text],
                "joined": text,
                "_source": "various_pages_fallback",
            })
        return out

    # ---- Step 5: per-category item builders -------------------------------

    def _confidence_for_source(self, source: Optional[str]) -> float:
        if source == "title_page_fallback":
            return 0.4
        if source == "various_pages_fallback":
            return 0.2
        return 0.7

    def _row_dimensions(self, joined: str) -> tuple[Optional[float], Optional[float]]:
        """Try to pull width and height from a joined cell string.

        Strategy: find all dimension matches, take the first two as
        (width, height). Order is bidset-dependent; this is rough.
        """
        dims: list[float] = []
        for m in _FT_IN_RE.finditer(joined):
            v = _parse_dimension(m.group(0))
            if v is not None and v > 0:
                dims.append(v)
            if len(dims) >= 2:
                break
        if not dims:
            for m in _FT_IN_WORDS_RE.finditer(joined):
                v = _parse_dimension(m.group(0))
                if v is not None and v > 0:
                    dims.append(v)
                if len(dims) >= 2:
                    break
        width = dims[0] if dims else None
        height = dims[1] if len(dims) >= 2 else None
        return width, height

    def _build_glazing_items(
        self,
        input: TradeModuleInput,
        schedules: list[dict],
        elevation_counts: dict[str, int],
    ) -> list[dict]:
        items: list[dict] = []
        for s in schedules:
            if s.get("category") not in ("window", None):
                continue
            joined = s.get("joined", "")
            mark = s.get("mark", "")
            mfr, mfr_conf = _match_manufacturer(joined)
            sys_name, sys_conf = _match_system(joined)
            glass = _match_glass_type(joined)
            width, height = self._row_dimensions(joined)
            sqft = round(width * height, 4) if (width and height) else None
            base_conf = self._confidence_for_source(s.get("_source"))
            items.append({
                "mark": mark,
                "count": elevation_counts.get(mark, 1) if mark else 1,
                "system": sys_name,
                "glass_type": glass,
                "manufacturer": mfr,
                "color_finish": self._extract_color_finish(joined),
                "width_ft": width,
                "height_ft": height,
                "sqft": sqft,
                "location": "",  # populated by future cross-page reconciliation; rough-ship blank
                "source_page": getattr(input, "page_number", None),
                "confidence": round(min(base_conf, max(mfr_conf, sys_conf, 0.4 if glass else 0.2)), 4),
            })
        return items

    def _build_door_items(
        self,
        input: TradeModuleInput,
        schedules: list[dict],
        elevation_counts: dict[str, int],
    ) -> list[dict]:
        items: list[dict] = []
        for s in schedules:
            if s.get("category") not in ("door", None):
                continue
            joined = s.get("joined", "")
            mark = s.get("mark", "")
            mfr, mfr_conf = _match_manufacturer(joined)
            door_type = _classify_door_type(joined)
            frame_type = _classify_door_type(joined)  # rough: same heuristic
            kind = _classify_door_kind(joined)
            material = door_type or "unknown"
            glass_door = _has_glass_in_door(joined)
            width, height = self._row_dimensions(joined)
            base_conf = self._confidence_for_source(s.get("_source"))
            items.append({
                "mark": mark,
                "count": elevation_counts.get(mark, 1) if mark else 1,
                "door_type": door_type,
                "frame_type": frame_type,
                "manufacturer": mfr,
                "door_kind": kind,
                "material": material,
                "glass_door": glass_door,
                "finish": self._extract_color_finish(joined),
                "location": "",
                "width_ft": width,
                "height_ft": height,
                "source_page": getattr(input, "page_number", None),
                "confidence": round(min(base_conf, max(mfr_conf, 0.5 if door_type else 0.2)), 4),
            })
        return items

    def _build_storefront_items(
        self,
        input: TradeModuleInput,
        schedules: list[dict],
        elevation_counts: dict[str, int],
    ) -> list[dict]:
        items: list[dict] = []
        for s in schedules:
            if s.get("category") not in ("storefront", None):
                continue
            joined = s.get("joined", "")
            mark = s.get("mark", "")
            mfr, mfr_conf = _match_manufacturer(joined)
            sys_name, sys_conf = _match_system(joined)
            width, height = self._row_dimensions(joined)
            sqft = round(width * height, 4) if (width and height) else None
            blob = joined.upper()
            door_in = _whole_word("DOOR", blob)
            double_door = _whole_word("PAIR", blob) or _whole_word("DOUBLE", blob)
            base_conf = self._confidence_for_source(s.get("_source"))
            items.append({
                "mark": mark,
                "count": elevation_counts.get(mark, 1) if mark else 1,
                "system_type": sys_name,
                "manufacturer": mfr,
                "sqft_per_segment": sqft,
                "door_in_segment": bool(door_in),
                "double_door_in_segment": bool(double_door),
                "location": "",
                "finish": self._extract_color_finish(joined),
                "width_ft": width,
                "height_ft": height,
                "source_page": getattr(input, "page_number", None),
                "confidence": round(min(base_conf, max(mfr_conf, sys_conf, 0.3)), 4),
            })
        return items

    def _extract_color_finish(self, joined: str) -> Optional[str]:
        blob = joined.upper()
        for token in (
            "DARK BRONZE", "MEDIUM BRONZE", "LIGHT BRONZE",
            "CLEAR ANODIZED", "BLACK ANODIZED", "BRONZE ANODIZED",
            "PAINTED", "MILL FINISH", "KYNAR", "PVDF", "POWDER COAT",
            "ANODIZED", "BRONZE", "BLACK", "WHITE", "CLEAR",
        ):
            if _whole_word(token, blob):
                return token.title()
        return None
