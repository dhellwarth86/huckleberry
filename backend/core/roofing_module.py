"""
Scope-driven RoofingModule — vocabulary + scope detection + quantity engine.

Replaces the previous hardcoded 19-field module. The module now:

  1. Reads ROOFING_VOCABULARY (modules/roofing/vocabulary.py) — the
     "semi-training" knowledge base that names every roof-system type
     (TPO, EPDM, mod-bit, metal, shingle, ...) and every takeoff item
     (drains, edge metal, flashing, ...).
  2. `detect_scope(input)` scans legends + interior text for system
     keywords, identifies the roof system, and assembles the list of
     active takeoff items for THIS plan.
  3. `derive_quantities(input, scope)` computes a value for each
     active item based on its `derive_from` rule (polygon_area,
     polygon_perimeter, callout_count, polygon_area_div_100, manual).
  4. Relationship rules run at the end; warnings are returned with the
     output.

The module never touches raw paths or PlanSetContext. All filtering
is done by `server.routes.trade.build_trade_input()` above.
"""

from __future__ import annotations

import re
from typing import Optional

from core.trade_module import (
    TradeModuleInput,
    TradeModuleOutput,
    TradeFieldValue,
)

from core.roofing_vocabulary import (
    SYSTEMS,
    ITEMS,
    UNIVERSAL_ITEMS,
    RULES,
    ROOFING_VOCABULARY,
    PIN_PALETTE_COLORS,  # G.5a CP4
)


# --- Helpers --------------------------------------------------------------

# Callouts at the same position within this tolerance collapse to one item.
DEDUP_TOLERANCE_PTS = 72.0  # 1 inch


def _tb_text(tb) -> str:
    for attr in ("content", "text"):
        v = getattr(tb, attr, None)
        if v:
            return str(v)
    if isinstance(tb, dict):
        return str(tb.get("content") or tb.get("text") or "")
    return ""


def _tb_center(tb):
    if hasattr(tb, "x0") and hasattr(tb, "y0"):
        return ((tb.x0 + tb.x1) / 2, (tb.y0 + tb.y1) / 2)
    b = getattr(tb, "bbox", None)
    if b is None and isinstance(tb, dict):
        b = tb.get("bbox")
    if b and len(b) >= 4:
        return ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
    return None


def _legend_blob(legends: list) -> str:
    """Flatten legend titles + entries into one UPPER-CASE search blob."""
    pieces: list[str] = []
    for leg in legends or []:
        title = getattr(leg, "title", "") or (
            leg.get("title", "") if isinstance(leg, dict) else ""
        )
        pieces.append(title or "")
        entries = getattr(leg, "entries", None)
        if entries is None and isinstance(leg, dict):
            entries = leg.get("entries", []) or []
        for e in entries or []:
            key = getattr(e, "key", "") or (
                e.get("key", "") if isinstance(e, dict) else ""
            )
            desc = (
                getattr(e, "description", None)
                or getattr(e, "desc", None)
                or (e.get("description", "") if isinstance(e, dict) else "")
                or (e.get("desc", "") if isinstance(e, dict) else "")
                or ""
            )
            pieces.append(f"{key} {desc}")
    return " | ".join(p for p in pieces if p).upper()


def _callout_blob(blocks: list) -> str:
    """Flatten interior text blocks into one UPPER-CASE search blob."""
    return " | ".join(_tb_text(tb).strip() for tb in (blocks or []) if _tb_text(tb)).upper()


def _whole_word(keyword: str, text: str) -> bool:
    return bool(re.search(rf"\b{re.escape(keyword)}\b", text))


def _scale_label(fpi: float) -> str:
    if fpi is None or fpi == 0:
        return "unknown scale"
    lookup = {
        1.0: '1" = 1\'-0"', 1.333: '3/4" = 1\'-0"', 2.0: '1/2" = 1\'-0"',
        2.667: '3/8" = 1\'-0"', 4.0: '1/4" = 1\'-0"',
        5.333: '3/16" = 1\'-0"', 8.0: '1/8" = 1\'-0"',
        10.667: '3/32" = 1\'-0"',
    }
    for k, v in lookup.items():
        if abs(fpi - k) < 0.05:
            return v
    return f'1" = {fpi:.1f}\' (fpi={fpi:.2f})'


# --- Module ---------------------------------------------------------------


class RoofingModule:
    """Scope-driven roofing takeoff module.

    Discovers what system is on the plan (TPO, mod-bit, shingle, ...) and
    only reports the takeoff items relevant to that system.
    """

    TRADE_NAME = "roofing"

    # FIELDS is now informational — a list of every item the module
    # *could* report. The actual fields returned depend on scope.
    FIELDS = list(ITEMS.keys())

    # ---- Scope detection ------------------------------------------------

    def detect_scope(self, inp: TradeModuleInput) -> dict:
        """Identify roof system + list of active takeoff items for this page.

        Priority: project_scope (weight 3) > page_legends (weight 2) >
        interior callouts (weight 1).
        """
        legend_blob = _legend_blob(inp.page_legends)
        callout_blob = _callout_blob(inp.interior_text_blocks or inp.equipment_callouts)
        full_blob = legend_blob + " || " + callout_blob

        best_system: Optional[str] = None
        best_hits = 0
        best_evidence = ""

        # --- Project scope takes precedence (weight 3) ---
        ps = getattr(inp, "project_scope", None)
        if ps is not None and getattr(ps, "detected_system", None) \
                and getattr(ps, "system_confidence", 0.0) >= 0.7:
            best_system = ps.detected_system
            best_hits = 3
            best_evidence = f"project scope: {ps.system_evidence}"

        # --- Identify the system by per-page keyword match ---
        for sys_name, sys_def in SYSTEMS.items():
            for kw in sys_def["keywords"]:
                if _whole_word(kw, legend_blob):
                    hits = 2
                    source = f"legend match '{kw}'"
                elif _whole_word(kw, callout_blob):
                    hits = 1
                    source = f"interior callout '{kw}'"
                else:
                    continue
                if hits > best_hits:
                    best_system = sys_name
                    best_hits = hits
                    best_evidence = source
                    break

        if best_system:
            if best_hits >= 3:
                system_confidence = float(getattr(ps, "system_confidence", 0.9))
            elif best_hits >= 2:
                system_confidence = 0.9
            else:
                system_confidence = 0.7
            typical_items = list(SYSTEMS[best_system]["typical_items"])
            system_display = SYSTEMS[best_system]["display_name"]
        else:
            # No specific system — try roof-shape classification from scope
            shape = getattr(ps, "roof_shape_signal", None) if ps else None
            if shape == "flat_roof":
                system_confidence = 0.5
                system_display = "Flat roof (system TBD)"
                typical_items = list(UNIVERSAL_ITEMS)
                best_evidence = f"scope flat-roof signal: {ps.system_evidence}"
            elif shape == "steep_roof":
                system_confidence = 0.5
                system_display = "Steep roof (system TBD)"
                typical_items = list(UNIVERSAL_ITEMS)
                best_evidence = f"scope steep-roof signal: {ps.system_evidence}"
            else:
                system_confidence = 0.0
                typical_items = list(UNIVERSAL_ITEMS)
                system_display = "Unknown — universal items only"

        # active_items = typical_items baseline + any item whose keywords
        # appear in the text. Typical items are "expected" even without a
        # text signal; extras are "text-activated" (only shown if keyword hit).
        active_items = list(typical_items)
        for item_name, item_def in ITEMS.items():
            if item_name in active_items:
                continue
            for kw in item_def.get("keywords", []) or []:
                if _whole_word(kw, full_blob):
                    active_items.append(item_name)
                    break

        return {
            "system": best_system,
            "system_display": system_display,
            "system_confidence": system_confidence,
            "system_evidence": best_evidence or "no system keyword match",
            "active_items": list(dict.fromkeys(active_items)),  # dedup, keep order
            "typical_items": list(dict.fromkeys(typical_items)),
        }

    # ---- Quantity derivation --------------------------------------------

    def derive_quantities(self, inp: TradeModuleInput, scope: dict) -> dict:
        """Return field_name -> TradeFieldValue for every active item.

        Items with `derive_from="callout_count"` that match zero callouts
        are OMITTED (no empty "0 count" rows). Items with
        `derive_from="manual"` are RETURNED with value=None so the
        estimator sees an empty slot to fill.
        """
        fields: dict[str, TradeFieldValue] = {}
        scale_str = _scale_label(inp.scale_fpi)
        geom_confidence = inp.scale_confidence or 0.5
        typical = set(scope.get("typical_items") or [])
        system_display = scope.get("system_display", "")
        # Collected pin positions — returned from analyze() via equipment_pins.
        self._last_pins = []

        for item_name in scope["active_items"]:
            item_def = ITEMS.get(item_name)
            if not item_def:
                continue
            derive = item_def["derive_from"]
            base_conf = float(item_def.get("confidence", 0.5))
            display = item_def["display_name"]
            unit = item_def["unit"]

            if derive == "polygon_area":
                if inp.polygon_area_sf <= 0:
                    continue
                fields[item_name] = TradeFieldValue(
                    value=round(inp.polygon_area_sf),
                    confidence=min(base_conf, geom_confidence),
                    source="auto_geometry",
                    evidence=f"polygon area at {scale_str}",
                    display_name=display, unit=unit,
                )

            elif derive == "polygon_area_div_100":
                if inp.polygon_area_sf <= 0:
                    continue
                fields[item_name] = TradeFieldValue(
                    value=round(inp.polygon_area_sf / 100, 1),
                    confidence=min(base_conf, geom_confidence),
                    source="auto_geometry",
                    evidence=f"polygon area / 100 at {scale_str}",
                    display_name=display, unit=unit,
                )

            elif derive == "polygon_perimeter":
                if inp.polygon_perimeter_lf <= 0:
                    continue
                fields[item_name] = TradeFieldValue(
                    value=round(inp.polygon_perimeter_lf),
                    confidence=min(base_conf, geom_confidence),
                    source="auto_geometry",
                    evidence=f"polygon perimeter at {scale_str}",
                    display_name=display, unit=unit,
                )

            elif derive == "callout_count":
                count, hit_kw, positions = self._count_callouts(
                    item_def["keywords"], inp.equipment_callouts
                )
                if count == 0:
                    # Zero matches: show as "expected" ONLY if this item
                    # is in the active system's typical_items. Otherwise
                    # omit (text-activated items that didn't hit).
                    if item_name in typical:
                        fields[item_name] = TradeFieldValue(
                            value=None,
                            confidence=0.0,
                            source="assembly_expected",
                            evidence=(
                                f"expected for {system_display} — "
                                f"no callouts found, enter manually"
                            ),
                            display_name=display, unit=unit,
                        )
                    continue
                # Record one pin per matched position for the overlay.
                for (cx, cy, kw) in positions:
                    self._last_pins.append({
                        "type": item_name,
                        "bbox": (cx - 6, cy - 6, cx + 6, cy + 6),
                        "keyword": kw,
                        "page": getattr(inp, "page_number", None),
                    })
                fields[item_name] = TradeFieldValue(
                    value=count,
                    confidence=base_conf,
                    source="auto_text",
                    evidence=(
                        f"{count} '{hit_kw}' label(s) inside building"
                        if hit_kw else f"{count} matching label(s)"
                    ),
                    display_name=display, unit=unit,
                )

            elif derive == "manual":
                # Items requiring manual entry. If the item is in
                # typical_items, flag as "expected" for visual distinction
                # from text-activated manual items.
                is_expected = item_name in typical
                fields[item_name] = TradeFieldValue(
                    value=None,
                    confidence=0.0,
                    source="assembly_expected" if is_expected else "manual_needed",
                    evidence=(
                        f"expected for {system_display} — enter manually"
                        if is_expected
                        else "detected in scope — enter quantity manually"
                    ),
                    display_name=display, unit=unit,
                )

        return fields

    # ---- Public entry point ---------------------------------------------

    def analyze(self, inp: TradeModuleInput) -> TradeModuleOutput:
        scope = self.detect_scope(inp)
        fields = self.derive_quantities(inp, scope)
        warnings = self._check_rules(fields, inp.polygon_area_sf)

        # Attach scope info as a pseudo-field so the panel can show the
        # system header. Uses a stable key "_scope" that the frontend
        # knows to render as a header, not a row.
        ps = getattr(inp, "project_scope", None)
        scope_field = TradeFieldValue(
            value=scope["system_display"],
            confidence=scope["system_confidence"],
            source="auto_legend" if scope["system"] else "auto_text",
            evidence=scope["system_evidence"],
            display_name="Roof System",
            unit="",
        )
        # Enrich the scope pseudo-field with material context (Step 78).
        if ps is not None:
            # dataclass → dict for the frontend
            scope_field.evidence = scope["system_evidence"]
            # Attach as attributes the serializer reads (trade.py reads display_name/unit,
            # route serializer will also pull scope_materials below).
            scope_field.scope_materials = {
                "spec_sections": list(getattr(ps, "spec_sections", []) or []),
                "manufacturers": list(getattr(ps, "manufacturers", []) or []),
                "material_mentions": list(getattr(ps, "material_mentions", []) or []),
                "florida_signals": list(getattr(ps, "florida_signals", []) or []),
                "roof_shape_signal": getattr(ps, "roof_shape_signal", None),
                "scope_pages": list(getattr(ps, "scope_pages", []) or []),
                "architect": getattr(ps, "architect", None),
                "contractor": getattr(ps, "contractor", None),
            }
        fields["_scope"] = scope_field

        return TradeModuleOutput(
            fields=fields,
            warnings=warnings,
            equipment_pins=list(getattr(self, "_last_pins", []) or []),
        )

    # ---- Internals ------------------------------------------------------

    def _count_callouts(self, keywords: list, callouts: list) -> tuple[int, str, list]:
        """Whole-word keyword match against short interior callouts, deduped by position.

        Returns (count, first_matched_keyword, positions) where positions is a
        list of (x, y, matched_keyword) tuples in PDF point coordinates.
        """
        matched_positions: list[tuple[float, float]] = []
        matched_details: list[tuple[float, float, str]] = []
        matched_keyword = ""
        for cb in callouts or []:
            text = _tb_text(cb).upper().strip()
            if not text or len(text) > 30:
                continue
            hit = None
            for kw in keywords:
                if _whole_word(kw, text):
                    hit = kw
                    break
            if not hit:
                continue
            center = _tb_center(cb)
            if center is None:
                continue
            is_dup = False
            for (px, py) in matched_positions:
                if (abs(center[0] - px) < DEDUP_TOLERANCE_PTS and
                        abs(center[1] - py) < DEDUP_TOLERANCE_PTS):
                    is_dup = True
                    break
            if is_dup:
                continue
            matched_positions.append(center)
            matched_details.append((center[0], center[1], hit))
            if not matched_keyword:
                matched_keyword = hit
        return (len(matched_positions), matched_keyword, matched_details)

    def _check_rules(self, fields: dict, roof_area_sf: float) -> list[str]:
        """Apply the vocabulary's relationship rules."""
        warnings: list[str] = []
        for rule in RULES:
            try:
                if rule["check"](fields, roof_area_sf):
                    warnings.append(rule["message"](fields, roof_area_sf))
            except Exception:
                continue
        return warnings

    # ----------------------------------------------------------------
    # G.5a CP4 — TradeModule Protocol vocabulary classmethods.
    # The platform layer (core/job_storage.py, api/) calls these to seed
    # scope-system palettes + EXPECTS checklists + system pickers WITHOUT
    # importing roofing-specific constants. Per Daniel 2026-05-08:
    # "hardcoding roofing verbiage and systems outside of module is forbidden."
    # ----------------------------------------------------------------

    @staticmethod
    def _color_for(item_name: str) -> str:
        """Deterministic display color per item.

        Uses the curated PIN_PALETTE_COLORS dict from roofing_vocabulary
        first; falls back to a hash-derived HSL hex for unknown items so
        new items added to ITEMS still get a stable color without a
        vocabulary edit.
        """
        if item_name in PIN_PALETTE_COLORS:
            return PIN_PALETTE_COLORS[item_name]
        # Fallback: deterministic HSL from name hash. Hue spread across
        # 360°; saturation/lightness fixed so colors stay distinguishable
        # on the dark canvas background.
        h = 0
        for ch in item_name:
            h = (h * 31 + ord(ch)) & 0xFFFFFFFF
        hue = h % 360
        # Convert HSL(hue, 60%, 60%) to hex.
        import colorsys
        r, g, b = colorsys.hls_to_rgb(hue / 360.0, 0.60, 0.60)
        return "#{:02x}{:02x}{:02x}".format(int(r * 255), int(g * 255), int(b * 255))

    @classmethod
    def _resolve_typical_items(cls, system_code: Optional[str]) -> list[str]:
        """Return the item-name list for `system_code`, falling back to all
        ITEMS when system_code is None or unknown. Helper for the three
        Protocol methods below."""
        if system_code:
            sys_def = SYSTEMS.get(system_code)
            if sys_def and "typical_items" in sys_def:
                return list(sys_def["typical_items"])
        # Fallback: every known item (manual ADD SYSTEM with no code picked,
        # or unknown system_code — give the user a useful starter palette).
        return list(ITEMS.keys())

    @classmethod
    def get_palette_seed(cls, system_code: Optional[str]) -> dict:
        """G.5a CP4 — return scope-system palette seed payload.

        Routes ITEMS by `derive_from`:
          - callout_count       -> pinPalette
          - polygon_perimeter   -> edgeTypes
          - polygon_area        -> polygonTypes
          - polygon_area_div_100 / manual / other -> skipped (derived rows
            are auto-computed; manual-only items don't belong in palettes)

        Each entry: {id, name, color, source: 'auto', seedId}. The frontend
        consumes the same shape it would get from user-added entries.
        """
        typical = cls._resolve_typical_items(system_code)
        pin_palette: list[dict] = []
        edge_types: list[dict] = []
        polygon_types: list[dict] = []
        for item_name in typical:
            item = ITEMS.get(item_name)
            if not item:
                continue
            derive = item.get("derive_from")
            entry = {
                "id": "pt-" + item_name,
                "name": item.get("display_name", item_name),
                "color": cls._color_for(item_name),
                "source": "auto",
                "seedId": item_name,
            }
            if derive == "callout_count":
                pin_palette.append(entry)
            elif derive == "polygon_perimeter":
                edge_types.append(entry)
            elif derive == "polygon_area":
                # membrane / insulation / cover_board are visually placed as
                # area polygons; insulation/cover_board are also auto-derived
                # rows in the takeoff (frontend handles dedup).
                polygon_types.append(entry)
            # polygon_area_div_100 / manual / other -> skip
        return {
            "pinPalette": pin_palette,
            "edgeTypes": edge_types,
            "polygonTypes": polygon_types,
        }

    @classmethod
    def get_expected_items(cls, system_code: Optional[str]) -> list[dict]:
        """G.5a CP4 — return the EXPECTS-checklist payload.

        One dict per item the system typically includes, with the metadata
        the estimator needs to confirm presence on the bidset. Frontend
        renders one checkbox per row.
        """
        typical = cls._resolve_typical_items(system_code)
        out: list[dict] = []
        for item_name in typical:
            item = ITEMS.get(item_name)
            if not item:
                continue
            out.append({
                "name": item_name,
                "display_name": item.get("display_name", item_name),
                "unit": item.get("unit", ""),
                "derive_from": item.get("derive_from", ""),
                "confidence": item.get("confidence", 0.0),
            })
        return out

    @classmethod
    def get_systems_catalog(cls) -> dict[str, dict]:
        """G.5a CP4 — return the system-picker catalog.

        Shape mirrors the SYSTEMS dict but excludes the heavy `keywords`
        list (frontend doesn't need it; keeps the payload small). Each
        entry preserves display_name + typical_items so the UI can show
        a system picker AND preview which items it will seed.
        """
        out: dict[str, dict] = {}
        for code, sys_def in SYSTEMS.items():
            out[code] = {
                "display_name": sys_def.get("display_name", code),
                "typical_items": list(sys_def.get("typical_items", [])),
            }
        return out
