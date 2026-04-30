"""
Dispatch Gate — Layer 3 plan set intake engine.

Runs once when a plan set is loaded, BEFORE the geometry engine.
Produces PlanSetContext: the platform's structured understanding
of the entire plan set.

Seven-filter pipeline (Filters 1-5 built, 6-7 future):
  1. Document Structure — sheet map from drawing index or title blocks
  2. Page Classification — page type from title block keywords
  3. Cross-Reference Extraction — detail refs, sheet refs, see refs
  4. Legend/Schedule Parsing — numbered note lists with headers
  5. Zone Classification — wraps zone_filter.py + notes/legend zones

Usage:
    python -m core.dispatch_gate path/to/plan.pdf
"""

import hashlib
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from core.pdf_engine import PDFEngine, TextBlock, parse_scale_to_ft_per_inch, find_roof_plan_scale
from core.zone_filter import detect_detail_zones, detect_title_block
from core.context import (
    PlanSetContext, PageContext, SheetEntry, CrossReference,
    Legend, LegendEntry, PageZone, ScaleInfo, ProjectMetadata,
    ScopePage, ProjectScope,
    SourceTag, Discipline, PageType,
    CONFIDENCE_EXPLICIT, CONFIDENCE_STRONG, CONFIDENCE_INFERRED,
    CONFIDENCE_WEAK, CONFIDENCE_UNKNOWN,
    check_for_leaks,
)

# Optional libraries — dispatch works without them
try:
    from rapidfuzz import fuzz as _fuzz
except ImportError:
    _fuzz = None

try:
    import pdfplumber as _pdfplumber
except ImportError:
    _pdfplumber = None


# ============================================================
# REGEX PATTERNS
# ============================================================

# Sheet number: A-1.3, G-0.0, S-1.0, A1.2, FP-1.0, A101, etc.
_SHEET_NUM_RE = re.compile(r'\b([A-Z]{1,2})-?(\d+[\.\d]*[A-Za-z]?)\b')

# Detail ref: "SEE DETAIL 5/A1.3"
_DETAIL_REF_RE = re.compile(
    r'SEE\s+DETAIL\s+(\d+)\s*[/\\]\s*([A-Z]-?\d+[\.\d]*)',
    re.IGNORECASE
)

# Sheet ref (compact): "6 A1.2" — small text block, number + sheet
_SHEET_REF_RE = re.compile(
    r'^(\d{1,2})\s+([A-Z]-?\d+[\.\d]*)$'
)

# See ref: "SEE A-2.2" or "SEE SHEET A-2.2"
_SEE_REF_RE = re.compile(
    r'SEE\s+(?:SHEET\s+)?([A-Z]-?\d+[\.\d]*)',
    re.IGNORECASE
)

# Legend header keywords
_LEGEND_HEADERS = re.compile(
    r'\b(NOTES?|LEGEND|KEY|MATERIAL|SCHEDULE|KEYNOTE)\b',
    re.IGNORECASE
)

# Numbered entry in a legend: "1. description" or "1 description"
_LEGEND_ENTRY_RE = re.compile(r'^\s*(\d+\.?\d*)\s*[.\s]\s*(.+)')

# Scale pattern (matches pdf_engine's internal pattern)
_SCALE_PATTERN = re.compile(r'(\d+)\s*/\s*(\d+)\s*["\u201d]\s*=\s*1\s*[\'\u2019]-?\s*0\s*["\u201d]?')

# Square footage on cover/index
_SF_PATTERN = re.compile(r'([\d,]+)\s*(?:SQ\.?\s*F\.?T\.?|SF)\b', re.IGNORECASE)

# Discipline prefix map
_DISCIPLINE_MAP = {
    "A": Discipline.ARCHITECTURAL,
    "S": Discipline.STRUCTURAL,
    "M": Discipline.MECHANICAL,
    "E": Discipline.ELECTRICAL,
    "P": Discipline.PLUMBING,
    "G": Discipline.GENERAL,
    "C": Discipline.CIVIL,
    "L": Discipline.LANDSCAPE,
    "FP": Discipline.FIRE_PROTECTION,
}

# Page type keywords: (keywords, PageType, title_conf, page_conf)
_PAGE_TYPE_RULES = [
    (["SCHEDULE"], PageType.SCHEDULE_SHEET, CONFIDENCE_EXPLICIT, CONFIDENCE_STRONG),
    (["ROOF PLAN"], PageType.ROOF_PLAN, CONFIDENCE_EXPLICIT, CONFIDENCE_STRONG),
    (["FLOOR PLAN", "SLAB PLAN"], PageType.FLOOR_PLAN, CONFIDENCE_EXPLICIT, CONFIDENCE_STRONG),
    (["FRAMING PLAN", "NOTED FRAMING"], PageType.FRAMING_PLAN, CONFIDENCE_EXPLICIT, CONFIDENCE_STRONG),
    (["CEILING PLAN", "RCP", "REFLECTED"], PageType.CEILING_PLAN, CONFIDENCE_EXPLICIT, CONFIDENCE_STRONG),
    (["ELEVATION"], PageType.ELEVATION, CONFIDENCE_EXPLICIT, CONFIDENCE_STRONG),
    (["DETAIL"], PageType.DETAIL_SHEET, CONFIDENCE_EXPLICIT, CONFIDENCE_STRONG),
    (["SECTION"], PageType.SECTION, CONFIDENCE_STRONG, CONFIDENCE_INFERRED),
    (["GENERAL NOTE", "INDEX", "ABBREVIAT"], PageType.GENERAL_NOTES, CONFIDENCE_EXPLICIT, CONFIDENCE_STRONG),
    (["SITE PLAN", "SITE PLOT"], PageType.SITE_PLAN, CONFIDENCE_EXPLICIT, CONFIDENCE_STRONG),
    (["COVER"], PageType.COVER, CONFIDENCE_EXPLICIT, CONFIDENCE_EXPLICIT),
    (["LIFE SAFETY", "OCCUPANCY"], PageType.LIFE_SAFETY, CONFIDENCE_EXPLICIT, CONFIDENCE_STRONG),
    (["SYMBOL", "LEGEND"], PageType.SYMBOL_LEGEND, CONFIDENCE_STRONG, CONFIDENCE_STRONG),
]


# ============================================================
# HELPERS
# ============================================================

def _file_hash(path: Path) -> str:
    """SHA-256 of first 64KB of file (fast, sufficient for identity)."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read(65536))
    return h.hexdigest()[:16]


def _discipline_from_prefix(sheet_num: str) -> Discipline:
    """Parse discipline from sheet number prefix."""
    upper = sheet_num.upper().lstrip()
    # Check two-char prefixes first (FP)
    if len(upper) >= 2 and upper[:2] in _DISCIPLINE_MAP:
        return _DISCIPLINE_MAP[upper[:2]]
    if upper[0] in _DISCIPLINE_MAP:
        return _DISCIPLINE_MAP[upper[0]]
    return Discipline.UNKNOWN


def _normalize_sheet(raw: str) -> str:
    """Normalize sheet number: strip whitespace, collapse spaces around dashes, uppercase.
    Keeps dashes as-is — use _sheet_key() for lookup matching.
    Handles 'A - 500' -> 'A-500'."""
    s = raw.strip().upper()
    # Collapse spaces around dashes: "A - 500" -> "A-500"
    s = re.sub(r'\s*-\s*', '-', s)
    return s


def _sheet_key(sheet_num: str) -> str:
    """Canonical key for sheet lookup: uppercase, dashes removed.
    'A-1.3' and 'A1.3' both become 'A1.3'."""
    return sheet_num.strip().upper().replace("-", "")


def _get_title_block_text(text_blocks, page_meta) -> str:
    """Get concatenated text from bottom-right quadrant (title block area)."""
    pw = page_meta.width_pts
    ph = page_meta.height_pts
    qx = pw * 0.6
    qy = ph * 0.6
    parts = []
    for b in text_blocks:
        if b.x0 >= qx and b.y0 >= qy:
            parts.append(b.text.strip())
    return " ".join(parts)


def _get_title_block_blocks(text_blocks, page_meta):
    """Get text blocks in bottom-right quadrant."""
    pw = page_meta.width_pts
    ph = page_meta.height_pts
    qx = pw * 0.6
    qy = ph * 0.6
    return [b for b in text_blocks if b.x0 >= qx and b.y0 >= qy]


# ============================================================
# FILTER 1: DOCUMENT STRUCTURE
# ============================================================

def _find_drawing_index_page(engine: PDFEngine, doc, max_pages: int = 10) -> Optional[tuple[int, list[dict]]]:
    """
    Scan first N pages for a drawing index page (10+ sheet number patterns).
    Returns (page_index, list of {sheet_number, title_text}) or None.

    Handles two formats:
      1. Same-line: "A-1.3  BUILDING B - ROOF PLAN"
      2. Split-line: "A-1.3\\nBUILDING B - ROOF PLAN" (sheet number alone, title on next line)
    """
    scan_range = min(doc.page_count, max_pages)
    for page_idx in range(scan_range):
        text = engine.extract_text(doc, page_idx)
        lines = text.split("\n")

        entries = []
        i = 0
        while i < len(lines):
            line_stripped = lines[i].strip()
            i += 1
            if not line_stripped:
                continue

            # Normalize spaces around dashes: "A - 500" -> "A-500"
            line_norm = re.sub(r'([A-Z])\s*-\s*(\d)', r'\1-\2', line_stripped)

            # Check if line starts with (or is) a sheet number
            m = _SHEET_NUM_RE.match(line_norm)
            if not m:
                continue

            sheet_num = _normalize_sheet(m.group(0))
            remainder = line_norm[m.end():].strip().lstrip("-").strip()

            if remainder:
                # Same-line format: "A-1.3  BUILDING B - ROOF PLAN"
                # Skip short remainders that are just noise (e.g., discipline headers)
                if len(remainder) > 3:
                    entries.append({"sheet_number": sheet_num, "title_text": remainder})
            else:
                # Split-line format: sheet number alone, title on next non-empty line
                while i < len(lines):
                    next_line = lines[i].strip()
                    i += 1
                    if not next_line:
                        continue
                    # Skip if next line is also a sheet number (no title found)
                    next_norm = re.sub(r'([A-Z])\s*-\s*(\d)', r'\1-\2', next_line)
                    if _SHEET_NUM_RE.match(next_norm):
                        # Put it back for next iteration
                        i -= 1
                        entries.append({"sheet_number": sheet_num, "title_text": ""})
                        break
                    # Skip discipline headers and boilerplate
                    if next_line.upper() in ("GENERAL", "ARCHITECTURAL", "STRUCTURAL",
                                             "MECHANICAL", "ELECTRICAL", "PLUMBING",
                                             "CIVIL", "LANDSCAPE", "FIRE PROTECTION",
                                             "SHEET INDEX", "SHEET NAME", "CURRENT",
                                             "REVISION DATE", "NO"):
                        continue
                    entries.append({"sheet_number": sheet_num, "title_text": next_line})
                    break

        # Require 10+ unique sheet numbers
        unique_sheets = {e["sheet_number"] for e in entries}
        if len(unique_sheets) >= 10:
            # Deduplicate: keep first occurrence of each sheet number
            seen = set()
            deduped = []
            for e in entries:
                if e["sheet_number"] not in seen:
                    seen.add(e["sheet_number"])
                    deduped.append(e)
            return (page_idx, deduped)

    return None


def _find_sheet_on_page(engine: PDFEngine, doc, page_idx: int,
                        known_keys: Optional[set] = None) -> Optional[str]:
    """Find sheet number from title block text on a single page.

    Strategies (in order — known-key match always preferred):
      1. Short text block in title block with known index key match
      2. Full page text scan for known index key match
      3. Short text block in title block with any sheet pattern
      4. Last 10 lines of page text for short sheet patterns
      5. (rapidfuzz) fuzzy match title block text against known keys
    """
    meta = engine.get_page_meta(doc, page_idx)
    blocks = engine.extract_text_blocks(doc, page_idx)
    tb_blocks = _get_title_block_blocks(blocks, meta)

    if known_keys:
        # Strategy 1: Short title block text that matches a known key
        for b in tb_blocks:
            text = b.text.strip()
            if len(text) < 20:
                m = _SHEET_NUM_RE.search(text)
                if m:
                    candidate = _normalize_sheet(m.group(0))
                    if _sheet_key(candidate) in known_keys:
                        return candidate

        # Strategy 2: Full text scan for known key match
        full_text = engine.extract_text(doc, page_idx)
        for m in _SHEET_NUM_RE.finditer(full_text):
            candidate = _normalize_sheet(m.group(0))
            if _sheet_key(candidate) in known_keys:
                return candidate

    # Strategy 3: Short text block in title block (any sheet pattern)
    for b in tb_blocks:
        text = b.text.strip()
        if len(text) < 20:
            m = _SHEET_NUM_RE.search(text)
            if m:
                return _normalize_sheet(m.group(0))

    # Strategy 4: Last 10 lines of page text
    full_text = engine.extract_text(doc, page_idx) if not known_keys else full_text
    lines = full_text.strip().split("\n")
    for line in reversed(lines[-10:]):
        line_stripped = line.strip()
        if len(line_stripped) < 15:
            m = _SHEET_NUM_RE.match(line_stripped)
            if m:
                return _normalize_sheet(m.group(0))

    # Strategy 5: rapidfuzz — fuzzy match title block sheets against known keys
    if known_keys and _fuzz:
        for b in tb_blocks:
            text = b.text.strip()
            if len(text) < 20:
                m = _SHEET_NUM_RE.search(text)
                if m:
                    candidate = _normalize_sheet(m.group(0))
                    ckey = _sheet_key(candidate)
                    # Check if candidate is a prefix of any known key
                    for kk in known_keys:
                        if kk.startswith(ckey) and len(kk) > len(ckey):
                            # e.g. "A1" is prefix of "A141" — ambiguous, skip
                            continue
                        score = _fuzz.ratio(ckey, kk)
                        if score >= 80:
                            return candidate

    return None


def _build_sheet_map_from_index(engine: PDFEngine, doc, index_entries: list[dict]) -> dict[str, int]:
    """Map sheet numbers to page indices by scanning title blocks on every page.
    Uses _sheet_key() for dash-agnostic matching (A-1.3 == A1.3)."""
    sheet_to_page = {}

    # Build canonical key lookup from index entries
    index_keys = {_sheet_key(e["sheet_number"]): e["sheet_number"] for e in index_entries}
    known_keys = set(index_keys.keys())

    # Scan all pages to find their sheet numbers
    for page_idx in range(doc.page_count):
        found_sn = _find_sheet_on_page(engine, doc, page_idx, known_keys=known_keys)
        if found_sn:
            key = _sheet_key(found_sn)
            # Match to index entry by canonical key
            if key in index_keys:
                original_sn = index_keys[key]
                if original_sn not in sheet_to_page:
                    sheet_to_page[original_sn] = page_idx

    return sheet_to_page


def run_filter_1(engine: PDFEngine, doc, ctx: PlanSetContext):
    """Filter 1: Document Structure — build sheet map."""

    # Try drawing index first
    index_result = _find_drawing_index_page(engine, doc)

    if index_result:
        idx_page, entries = index_result
        ctx.sheet_map_source = "drawing_index"

        # Build page mapping
        sheet_to_page = _build_sheet_map_from_index(engine, doc, entries)

        for entry in entries:
            sn = entry["sheet_number"]
            page_idx = sheet_to_page.get(sn, -1)
            disc = _discipline_from_prefix(sn)

            ctx.sheet_map[sn] = SheetEntry(
                sheet_number=sn,
                title=entry["title_text"],
                page_index=page_idx,
                discipline=disc,
                page_type=PageType.UNKNOWN,  # Filter 2 fills this
                confidence=CONFIDENCE_EXPLICIT if page_idx >= 0 else CONFIDENCE_WEAK,
                source_tag=SourceTag("filter_1", CONFIDENCE_EXPLICIT, f"drawing_index_page_{idx_page}"),
            )
            if page_idx >= 0:
                ctx.page_to_sheet[page_idx] = sn
    else:
        # Fallback: title block scanning
        ctx.sheet_map_source = "title_blocks"
        for page_idx in range(doc.page_count):
            sheet_num = _find_sheet_on_page(engine, doc, page_idx)
            if sheet_num:
                disc = _discipline_from_prefix(sheet_num)
                # Get title from title block text
                meta = engine.get_page_meta(doc, page_idx)
                blocks = engine.extract_text_blocks(doc, page_idx)
                tb_text = _get_title_block_text(blocks, meta)
                # Use first line-ish of title block as title
                title = tb_text[:60].strip() if tb_text else ""

                ctx.sheet_map[sheet_num] = SheetEntry(
                    sheet_number=sheet_num,
                    title=title,
                    page_index=page_idx,
                    discipline=disc,
                    page_type=PageType.UNKNOWN,
                    confidence=CONFIDENCE_STRONG,
                    source_tag=SourceTag("filter_1", CONFIDENCE_STRONG, f"title_block_page_{page_idx}"),
                )
                ctx.page_to_sheet[page_idx] = sheet_num

    ctx.project.total_pages = doc.page_count
    ctx.filters_completed.append("filter_1")


# ============================================================
# FILTER 2: PAGE CLASSIFICATION
# ============================================================

def _classify_page_type(title_text: str, full_text: str) -> tuple[PageType, float]:
    """Classify page type from title block and full page text."""
    title_upper = title_text.upper()
    full_upper = full_text.upper()

    for keywords, ptype, title_conf, page_conf in _PAGE_TYPE_RULES:
        for kw in keywords:
            if kw in title_upper:
                return (ptype, title_conf)

    for keywords, ptype, title_conf, page_conf in _PAGE_TYPE_RULES:
        for kw in keywords:
            if kw in full_upper:
                return (ptype, page_conf)

    return (PageType.UNKNOWN, CONFIDENCE_UNKNOWN)


def run_filter_2(engine: PDFEngine, doc, ctx: PlanSetContext):
    """Filter 2: Page Classification — determine page type for every page."""

    for page_idx in range(doc.page_count):
        meta = engine.get_page_meta(doc, page_idx)
        blocks = engine.extract_text_blocks(doc, page_idx)
        tb_text = _get_title_block_text(blocks, meta)
        full_text = engine.extract_text(doc, page_idx)

        page_type, confidence = _classify_page_type(tb_text, full_text)

        # Get sheet entry if exists
        sheet_num = ctx.page_to_sheet.get(page_idx)
        disc = Discipline.UNKNOWN
        title = ""
        if sheet_num and sheet_num in ctx.sheet_map:
            entry = ctx.sheet_map[sheet_num]
            disc = entry.discipline
            title = entry.title
            # Update sheet entry page type
            entry.page_type = page_type
        else:
            disc = _discipline_from_prefix(sheet_num) if sheet_num else Discipline.UNKNOWN

        # MEP fallback: if discipline is M/E/P and no specific match
        if page_type == PageType.UNKNOWN and disc in (Discipline.MECHANICAL, Discipline.ELECTRICAL, Discipline.PLUMBING):
            page_type = PageType.MEP_PLAN
            confidence = CONFIDENCE_WEAK

        # Scale detection
        scale_info = None
        roof_plan_fpi = find_roof_plan_scale(blocks)
        if roof_plan_fpi:
            scale_info = ScaleInfo(
                scale_string=f"{roof_plan_fpi} fpi",
                ft_per_inch=roof_plan_fpi,
                source="zone_label",
                source_page=page_idx,
                confidence=CONFIDENCE_EXPLICIT,
            )
        else:
            text_fpi = parse_scale_to_ft_per_inch(full_text)
            if text_fpi:
                scale_info = ScaleInfo(
                    scale_string=f"{text_fpi} fpi",
                    ft_per_inch=text_fpi,
                    source="text_near_title",
                    source_page=page_idx,
                    confidence=CONFIDENCE_STRONG,
                )

        page_ctx = PageContext(
            page_index=page_idx,
            sheet_number=sheet_num,
            title=title,
            discipline=disc,
            page_type=page_type,
            scale=scale_info,
            confidence=confidence,
            source_tag=SourceTag("filter_2", confidence, f"keywords_page_{page_idx}"),
        )
        ctx.pages[page_idx] = page_ctx

    ctx.filters_completed.append("filter_2")


# ============================================================
# FILTER 3: CROSS-REFERENCE EXTRACTION
# ============================================================

def _extract_cross_refs_on_page(text_blocks, page_idx: int,
                                 has_keynote_legend: bool) -> list[CrossReference]:
    """Extract cross-references from text blocks on a single page."""
    refs = []

    for block in text_blocks:
        text = block.text.strip()
        cx = (block.x0 + block.x1) / 2
        cy = (block.y0 + block.y1) / 2

        # Pattern 1: "SEE DETAIL N/sheet"
        for m in _DETAIL_REF_RE.finditer(text):
            refs.append(CrossReference(
                ref_type="detail",
                identifier=m.group(1),
                text=m.group(0),
                source_page=page_idx,
                source_x=cx, source_y=cy,
                target_sheet=_normalize_sheet(m.group(2)),
                target_detail=m.group(1),
                confidence=CONFIDENCE_EXPLICIT,
                source_tag=SourceTag("filter_3", CONFIDENCE_EXPLICIT, f"detail_ref: {m.group(0)}"),
            ))

        # Pattern 2: Compact sheet ref "N sheet_number" — short text blocks only
        if len(text) < 50:
            m = _SHEET_REF_RE.match(text)
            if m:
                refs.append(CrossReference(
                    ref_type="detail",
                    identifier=m.group(1),
                    text=text,
                    source_page=page_idx,
                    source_x=cx, source_y=cy,
                    target_sheet=_normalize_sheet(m.group(2)),
                    target_detail=m.group(1),
                    confidence=CONFIDENCE_STRONG,
                    source_tag=SourceTag("filter_3", CONFIDENCE_STRONG, f"sheet_ref: {text}"),
                ))

        # Pattern 3: "SEE sheet" / "SEE SHEET sheet"
        for m in _SEE_REF_RE.finditer(text):
            # Avoid matching if already matched as detail ref
            full_match = m.group(0)
            if "DETAIL" in full_match.upper():
                continue
            refs.append(CrossReference(
                ref_type="see_ref",
                identifier=m.group(1),
                text=full_match,
                source_page=page_idx,
                source_x=cx, source_y=cy,
                target_sheet=_normalize_sheet(m.group(1)),
                confidence=CONFIDENCE_STRONG,
                source_tag=SourceTag("filter_3", CONFIDENCE_STRONG, f"see_ref: {full_match}"),
            ))

        # Pattern 4: Keynote ref — single/double digit in tiny text block, if page has keynote legend
        if has_keynote_legend and len(text) < 5:
            try:
                num = int(text.strip())
                if 1 <= num <= 99:
                    refs.append(CrossReference(
                        ref_type="keynote",
                        identifier=str(num),
                        text=text,
                        source_page=page_idx,
                        source_x=cx, source_y=cy,
                        confidence=CONFIDENCE_INFERRED,
                        source_tag=SourceTag("filter_3", CONFIDENCE_INFERRED, f"keynote: {text}"),
                    ))
            except ValueError:
                pass

    return refs


def run_filter_3(engine: PDFEngine, doc, ctx: PlanSetContext):
    """Filter 3: Cross-Reference Extraction — parse and resolve text refs."""

    # Determine which pages have keynote legends (from filter 4 if already run,
    # otherwise we'll do a quick scan)
    pages_with_keynotes = set()
    for legend in ctx.all_legends:
        if legend.legend_type in ("keynote", "material_notes", "roof_notes"):
            pages_with_keynotes.add(legend.page_index)

    for page_idx in range(doc.page_count):
        blocks = engine.extract_text_blocks(doc, page_idx)
        has_keynotes = page_idx in pages_with_keynotes
        refs = _extract_cross_refs_on_page(blocks, page_idx, has_keynotes)

        # Resolve against sheet map (dash-agnostic lookup)
        for ref in refs:
            if ref.target_sheet:
                # Try exact match first, then canonical key
                entry = ctx.sheet_map.get(ref.target_sheet)
                if not entry:
                    key = _sheet_key(ref.target_sheet)
                    for sn, se in ctx.sheet_map.items():
                        if _sheet_key(sn) == key:
                            entry = se
                            break
                if entry and entry.page_index >= 0:
                    ref.target_page = entry.page_index
                    ref.resolved = True

        ctx.all_cross_refs.extend(refs)

        if page_idx in ctx.pages:
            ctx.pages[page_idx].cross_refs_out = refs
            if refs:
                ctx.pages[page_idx].has_details = True
                ctx.pages[page_idx].detail_count = len([r for r in refs if r.ref_type == "detail"])

    # Populate cross_refs_in (incoming references to each page)
    for ref in ctx.all_cross_refs:
        if ref.resolved and ref.target_page is not None:
            if ref.target_page in ctx.pages:
                ctx.pages[ref.target_page].cross_refs_in.append(ref)

    ctx.resolved_count = sum(1 for r in ctx.all_cross_refs if r.resolved)
    ctx.unresolved_count = len(ctx.all_cross_refs) - ctx.resolved_count
    ctx.filters_completed.append("filter_3")


# ============================================================
# FILTER 4: LEGEND AND SCHEDULE PARSING
# ============================================================

def _classify_legend_type(header: str) -> str:
    """Classify legend type from its header text."""
    h = header.upper()
    if "KEYNOTE" in h:
        return "keynote"
    if "MATERIAL" in h:
        return "material_notes"
    if "ROOF" in h and "NOTE" in h:
        return "roof_notes"
    if "GENERAL NOTE" in h:
        return "general_notes"
    if "DOOR" in h:
        return "door_schedule"
    if "WINDOW" in h:
        return "window_schedule"
    if "HARDWARE" in h:
        return "hardware_schedule"
    if "FINISH" in h:
        return "finish_schedule"
    if "SCHEDULE" in h:
        return "schedule"
    if "LEGEND" in h:
        return "legend"
    return "notes"


def _find_legends_on_page(text_blocks, page_idx: int) -> list[Legend]:
    """Find numbered note/legend lists on a page."""
    legends = []

    # Sort blocks by vertical position
    sorted_blocks = sorted(text_blocks, key=lambda b: (b.y0, b.x0))

    for i, block in enumerate(sorted_blocks):
        text = block.text.strip()
        if not text:
            continue

        # Check if this block is a legend header
        if not _LEGEND_HEADERS.search(text):
            continue

        # Look at subsequent blocks for numbered entries
        entries = []
        bbox_x0 = block.x0
        bbox_y0 = block.y0
        bbox_x1 = block.x1
        bbox_y1 = block.y1

        # Check blocks near this header (within 500pts below)
        for j in range(i + 1, len(sorted_blocks)):
            candidate = sorted_blocks[j]
            if candidate.y0 > block.y0 + 500:
                break
            # Must be in roughly the same horizontal region
            if abs(candidate.x0 - block.x0) > 200:
                continue

            # Parse numbered entries from this block
            for line in candidate.text.split("\n"):
                m = _LEGEND_ENTRY_RE.match(line.strip())
                if m:
                    entries.append(LegendEntry(
                        key=m.group(1).rstrip("."),
                        description=m.group(2).strip()[:100],
                    ))
                    bbox_x1 = max(bbox_x1, candidate.x1)
                    bbox_y1 = max(bbox_y1, candidate.y1)

        # Also parse entries from the header block itself (multi-line)
        for line in text.split("\n"):
            m = _LEGEND_ENTRY_RE.match(line.strip())
            if m:
                key = m.group(1).rstrip(".")
                desc = m.group(2).strip()[:100]
                if not any(e.key == key for e in entries):
                    entries.append(LegendEntry(key=key, description=desc))

        if len(entries) >= 3:
            legend_type = _classify_legend_type(text)
            legends.append(Legend(
                legend_type=legend_type,
                title=text[:80],
                page_index=page_idx,
                entries=entries,
                entry_count=len(entries),
                bbox=(bbox_x0, bbox_y0, bbox_x1, bbox_y1),
                confidence=CONFIDENCE_STRONG,
                source_tag=SourceTag("filter_4", CONFIDENCE_STRONG, f"legend: {text[:40]}"),
            ))

    return legends


def _parse_tables_on_page(pdf_path: str, page_idx: int) -> tuple[list[Legend], list]:
    """Use pdfplumber to extract table data from a page.
    Returns (Legend objects, raw_tables). Falls back to ([], []) on failure."""
    if not _pdfplumber:
        return [], []
    try:
        pdf = _pdfplumber.open(pdf_path)
        if page_idx >= len(pdf.pages):
            pdf.close()
            return [], []
        page = pdf.pages[page_idx]
        tables = page.extract_tables()
        pdf.close()

        raw_tables = list(tables) if tables else []

        legends = []
        for table in tables:
            if not table or len(table) < 2:
                continue
            # Use first row as header
            header_row = table[0]
            header_text = " ".join(str(c) for c in header_row if c)
            if len(header_text) < 3:
                continue

            entries = []
            for row in table[1:]:
                if not row or not any(row):
                    continue
                key = str(row[0]) if row[0] else ""
                desc = " ".join(str(c) for c in row[1:] if c)
                if key or desc:
                    entries.append(LegendEntry(key=key[:20], description=desc[:200]))

            if entries:
                legend_type = _classify_legend_type(header_text)
                legends.append(Legend(
                    legend_type=legend_type,
                    title=header_text[:80],
                    page_index=page_idx,
                    entries=entries[:50],
                    entry_count=len(entries),
                    confidence=CONFIDENCE_INFERRED,
                    source_tag=SourceTag("filter_4_pdfplumber", CONFIDENCE_INFERRED, "table extraction"),
                ))
        return legends, raw_tables
    except Exception:
        return [], []


def _quality_check_legends(legends: list[Legend]) -> list[Legend]:
    """Remove low-quality legends. Run after all parsing completes.
    Returns filtered list. Logs removal count via dispatch warnings."""
    _VALID_HEADERS = [
        "schedule", "note", "legend", "key",
        "material", "finish", "door", "window",
        "hardware", "fixture", "equipment",
        "keynote", "abbreviat",
    ]

    clean = []
    for legend in legends:
        # Rule 1: Must have at least 2 entries
        if legend.entry_count < 2:
            continue

        # Rule 2: Must have a title (header keyword matched)
        if not legend.title or legend.title.strip() == "":
            continue

        # Rule 3: pdfplumber legends need stricter validation
        if legend.source_tag and "pdfplumber" in legend.source_tag.evidence:
            if legend.entry_count < 3:
                continue
            has_valid_header = any(
                h in legend.title.lower() for h in _VALID_HEADERS
            )
            if not has_valid_header:
                continue

        # Rule 4: Deduplicate — if text-based and pdfplumber found
        # the same legend (same page, similar type), keep text-based
        is_duplicate = False
        for existing in clean:
            if (existing.page_index == legend.page_index and
                    existing.legend_type == legend.legend_type and
                    abs(existing.entry_count - legend.entry_count) < 3):
                is_duplicate = True
                break
        if is_duplicate:
            continue

        clean.append(legend)

    return clean


def run_filter_4(engine: PDFEngine, doc, ctx: PlanSetContext):
    """Filter 4: Legend and Schedule Parsing."""
    raw_legends = []

    for page_idx in range(doc.page_count):
        blocks = engine.extract_text_blocks(doc, page_idx)
        legends = _find_legends_on_page(blocks, page_idx)

        # Supplement: pdfplumber table extraction on schedule pages
        page_ctx = ctx.pages.get(page_idx)
        if page_ctx and page_ctx.page_type == PageType.SCHEDULE_SHEET:
            table_legends, raw_tables = _parse_tables_on_page(ctx.pdf_path, page_idx)
            legends.extend(table_legends)
            if raw_tables:
                page_ctx.raw_tables = raw_tables

        raw_legends.extend(legends)

    # Quality gate — remove noise before storing
    total_raw = len(raw_legends)
    clean_legends = _quality_check_legends(raw_legends)
    removed = total_raw - len(clean_legends)
    if removed > 0:
        ctx.dispatch_warnings.append(
            f"Filter 4 quality gate: {removed} of {total_raw} legends removed "
            f"({len(clean_legends)} kept)"
        )

    ctx.all_legends = clean_legends

    # Re-associate legends with page contexts
    page_legends: dict[int, list[Legend]] = {}
    for legend in clean_legends:
        page_legends.setdefault(legend.page_index, []).append(legend)

    for page_idx in range(doc.page_count):
        if page_idx in ctx.pages:
            legends = page_legends.get(page_idx, [])
            ctx.pages[page_idx].legends = legends
            if legends:
                ctx.pages[page_idx].has_legend = True
                if any(l.legend_type.endswith("_schedule") or l.legend_type == "schedule"
                       for l in legends):
                    ctx.pages[page_idx].has_schedule = True

    # Build legends_by_type index
    for legend in ctx.all_legends:
        if legend.legend_type not in ctx.legends_by_type:
            ctx.legends_by_type[legend.legend_type] = []
        ctx.legends_by_type[legend.legend_type].append(legend)

    ctx.filters_completed.append("filter_4")


# ============================================================
# FILTER 5: ZONE CLASSIFICATION
# ============================================================

def run_filter_5(engine: PDFEngine, doc, ctx: PlanSetContext):
    """Filter 5: Zone Classification — wraps zone_filter.py + additional zones."""

    for page_idx in range(doc.page_count):
        meta = engine.get_page_meta(doc, page_idx)
        blocks = engine.extract_text_blocks(doc, page_idx)
        page_ctx = ctx.pages.get(page_idx)
        if not page_ctx:
            continue

        pw = meta.width_pts
        ph = meta.height_pts
        zones = []

        # Use existing zone_filter.py for detail zones
        detail_zones = detect_detail_zones(blocks, meta)
        for dz in detail_zones:
            zones.append(PageZone(
                zone_type="detail_view",
                bbox=(dz["x0"], dz["y0"], dz["x1"], dz["y1"]),
                label=dz.get("name"),
                confidence=CONFIDENCE_STRONG,
            ))

        # Title block zone
        tb_zone = detect_title_block(blocks, meta)
        if tb_zone:
            zones.append(PageZone(
                zone_type="title_block",
                bbox=(tb_zone["x0"], tb_zone["y0"], tb_zone["x1"], tb_zone["y1"]),
                confidence=CONFIDENCE_EXPLICIT,
            ))
            page_ctx.has_title_block = True

        # Notes area: large text blocks in top 20% or right 25% of page
        notes_blocks = [b for b in blocks
                        if (b.y0 < ph * 0.20 or b.x0 > pw * 0.75)
                        and len(b.text) > 100]
        if notes_blocks:
            nx0 = min(b.x0 for b in notes_blocks)
            ny0 = min(b.y0 for b in notes_blocks)
            nx1 = max(b.x1 for b in notes_blocks)
            ny1 = max(b.y1 for b in notes_blocks)
            zones.append(PageZone(
                zone_type="notes_area",
                bbox=(nx0, ny0, nx1, ny1),
                confidence=CONFIDENCE_INFERRED,
            ))

        # Legend area: bounding box around parsed legends
        for legend in page_ctx.legends:
            if legend.bbox:
                zones.append(PageZone(
                    zone_type="legend_area",
                    bbox=legend.bbox,
                    label=legend.title[:40],
                    confidence=CONFIDENCE_STRONG,
                ))

        # Main drawing zone: page area minus title block and detail zones
        # Estimate as largest remaining rectangular region
        if tb_zone:
            # Main drawing is everything left of / above the title block
            main_x1 = pw
            main_y1 = tb_zone["y0"] if tb_zone["y0"] < ph * 0.8 else ph
            main_zone = PageZone(
                zone_type="main_drawing",
                bbox=(0, 0, main_x1, main_y1),
                confidence=CONFIDENCE_INFERRED,
            )
            zones.append(main_zone)
            page_ctx.primary_zone = main_zone
            page_ctx.has_drawing_area = True
        elif blocks:
            # No title block — whole page is drawing area
            main_zone = PageZone(
                zone_type="main_drawing",
                bbox=(0, 0, pw, ph),
                confidence=CONFIDENCE_WEAK,
            )
            zones.append(main_zone)
            page_ctx.primary_zone = main_zone
            page_ctx.has_drawing_area = True

        page_ctx.zones = zones

        # EXPERIMENTAL: Text classification by zone
        for b in blocks:
            bx = (b.x0 + b.x1) / 2
            by = (b.y0 + b.y1) / 2
            entry = {"text": b.text.strip()[:200], "x": b.x0, "y": b.y0}

            in_notes = False
            for z in zones:
                if z.zone_type == "notes_area":
                    if z.bbox[0] <= bx <= z.bbox[2] and z.bbox[1] <= by <= z.bbox[3]:
                        page_ctx.spec_note_texts.append(entry)
                        in_notes = True
                        break

            if not in_notes and page_ctx.primary_zone:
                pz = page_ctx.primary_zone
                if pz.bbox[0] <= bx <= pz.bbox[2] and pz.bbox[1] <= by <= pz.bbox[3]:
                    # Short text in main drawing → likely callout
                    if len(b.text.strip()) < 100:
                        page_ctx.callout_texts.append(entry)

    ctx.filters_completed.append("filter_5")


# ============================================================
# PROJECT METADATA (deterministic extraction)
# ============================================================

def _extract_project_metadata(engine: PDFEngine, doc, ctx: PlanSetContext):
    """Extract project metadata from cover page and title blocks."""

    # Try cover page (page 0, then page 1)
    for cover_idx in range(min(2, doc.page_count)):
        text = engine.extract_text(doc, cover_idx)
        text_upper = text.upper()

        # Check if this looks like a cover page
        if any(kw in text_upper for kw in ["COVER", "PROJECT", "PREPARED FOR", "BUILDING"]):
            # Project name: look for large/prominent text near top
            blocks = engine.extract_text_blocks(doc, cover_idx)
            meta = engine.get_page_meta(doc, cover_idx)

            # Find prominent text blocks in upper portion
            top_blocks = sorted(
                [b for b in blocks if b.y0 < meta.height_pts * 0.5 and len(b.text.strip()) > 5],
                key=lambda b: b.y0
            )

            # First substantial non-boilerplate text is often project name
            for b in top_blocks:
                t = b.text.strip()
                if len(t) > 10 and not any(skip in t.upper() for skip in ["SHEET", "DATE", "REV", "DESCRIPTION"]):
                    if not ctx.project.project_name:
                        ctx.project.project_name = t[:80]
                        ctx.project.field_sources["project_name"] = SourceTag(
                            "filter_1", CONFIDENCE_INFERRED, f"cover_page_{cover_idx}")
                    break

            # Address: look for pattern with state abbreviation + zip
            addr_re = re.compile(r'(\d+[^,\n]{5,50},?\s*[A-Z]{2}\.?\s*\d{5})', re.IGNORECASE)
            m = addr_re.search(text)
            if m and not ctx.project.project_address:
                ctx.project.project_address = m.group(1).strip()
                ctx.project.field_sources["project_address"] = SourceTag(
                    "filter_1", CONFIDENCE_STRONG, f"address_regex_page_{cover_idx}")

            # Square footage
            for sf_m in _SF_PATTERN.finditer(text):
                raw = (sf_m.group(1) or "").replace(",", "").strip()
                if not raw:
                    continue
                try:
                    sf_val = float(raw)
                except ValueError:
                    continue
                if 500 < sf_val < 500000:  # reasonable building size
                    if not ctx.project.total_building_sf:
                        ctx.project.total_building_sf = sf_val
                        ctx.project.field_sources["total_building_sf"] = SourceTag(
                            "filter_1", CONFIDENCE_STRONG, f"sf_regex: {sf_m.group(0)}")
                    break

            break  # Only process first cover-like page

    # Cross-check project name from title blocks
    if not ctx.project.project_name:
        # Try extracting from the most common text in title blocks across pages
        sample_pages = list(range(min(5, doc.page_count)))
        for page_idx in sample_pages:
            meta = engine.get_page_meta(doc, page_idx)
            blocks = engine.extract_text_blocks(doc, page_idx)
            tb_blocks = _get_title_block_blocks(blocks, meta)
            for b in tb_blocks:
                t = b.text.strip()
                if 10 < len(t) < 60 and not any(skip in t.upper() for skip in ["SHEET", "DATE", "REV", "SCALE", "DRAWN"]):
                    ctx.project.project_name = t[:80]
                    ctx.project.field_sources["project_name"] = SourceTag(
                        "filter_1", CONFIDENCE_WEAK, f"title_block_page_{page_idx}")
                    break
            if ctx.project.project_name:
                break


# ============================================================
# MAIN DISPATCH
# ============================================================

def _collect_title_block_text(engine: PDFEngine, doc, ctx: PlanSetContext) -> list:
    """Gather text blocks that fall inside any title_block zone."""
    out = []
    for page_idx, page_ctx in ctx.pages.items():
        tb_zones = [z for z in page_ctx.zones if z.zone_type == "title_block"]
        if not tb_zones:
            continue
        blocks = engine.extract_text_blocks(doc, page_idx)
        for b in blocks:
            cx = (b.x0 + b.x1) / 2
            cy = (b.y0 + b.y1) / 2
            for z in tb_zones:
                if z.bbox[0] <= cx <= z.bbox[2] and z.bbox[1] <= cy <= z.bbox[3]:
                    out.append(b)
                    break
    return out


# ============================================================
# SCOPE PAGE SCANNER (Step 75)
# ============================================================

# Keywords signaling a scope/cover/separator page.
# Compound phrases only — single words like "PROJECT"/"SECTION" fire on
# drawing title blocks and detail references and add noise without signal.
_SCOPE_KEYWORDS = [
    "TABLE OF CONTENTS",
    "DRAWING INDEX",
    "SHEET INDEX",
    "PROJECT DIRECTORY",
    "SCOPE OF WORK",
    "WORK INCLUDED",
    "WORK EXCLUDED",
    "GENERAL CONDITIONS",
    "DIVISION 07",
    "DIVISION 7",
    "THERMAL AND MOISTURE",
    "THERMAL & MOISTURE",
    "ROOFING SCOPE",
    "ROOFING NOTES",
]

# "07 54 00" / "07 5400" / "07-54-00" — Division 07 tagger.
_SPEC_SECTION_RX = re.compile(r'\b(\d{2})[\s\-]?(\d{2})(?:[\s\-]?(\d{2}))?\b')

# Thickness / insulation / metal markers (searched whole-word, case-insensitive).
_MATERIAL_MARKERS_RX = re.compile(
    r'\b('
    r'\d{2,3}\s?mil|'
    r'\d{2}\s?(?:ga|gauge)|'
    r'polyiso(?:cyanurate)?|polyisocynurate|'
    r'[RrEe][Pp][Ss]|XPS|EPS|'
    r'R[\s\-]?\d{2}|'
    r'cover\s?board|dens[\w]*|securshield|'
    r'galvalume|kynar|pvdf'
    r')\b',
    re.IGNORECASE,
)

_FLORIDA_TOKENS = {
    "HVHZ", "NOA", "FBC", "TAS", "FRSA", "NRCA", "SMACNA", "SPRI",
    "FM 1-60", "FM 1-90", "FM 1-120", "FM 1-150", "FM GLOBAL",
    "UL 580", "UL 790",
}

# Architect / contractor extraction heuristics.
_ARCHITECT_LINE_RX = re.compile(
    r'(architect(?:\s+of\s+record)?|architect/engineer)[:\s\-]+(.{3,80})',
    re.IGNORECASE,
)
_CONTRACTOR_LINE_RX = re.compile(
    r'(general\s+contractor|contractor|gc)[:\s\-]+(.{3,80})',
    re.IGNORECASE,
)


def _find_spec_sections(text: str) -> list[str]:
    """Return Division 07 spec section strings found in text."""
    out = []
    for m in _SPEC_SECTION_RX.finditer(text):
        a, b, c = m.group(1), m.group(2), m.group(3)
        if a != "07":
            continue
        if c:
            out.append(f"{a} {b} {c}")
        else:
            out.append(f"{a} {b}")
    return out


def _find_manufacturers_in_text(text: str) -> list[str]:
    """Return canonical manufacturer names mentioned in text (dedup)."""
    from seeds.roofing_spec_database import all_manufacturer_names
    up = text.upper()
    found: list[str] = []
    seen: set[str] = set()
    for search_name, canonical in all_manufacturer_names():
        if canonical in seen:
            continue
        if re.search(rf'\b{re.escape(search_name.upper())}\b', up):
            found.append(canonical)
            seen.add(canonical)
    return found


def _find_material_markers(text: str) -> list[str]:
    """Return membrane-thickness / insulation / metal markers in text."""
    out: list[str] = []
    for m in _MATERIAL_MARKERS_RX.finditer(text):
        val = m.group(1).strip()
        # Normalize whitespace
        val = re.sub(r'\s+', ' ', val)
        out.append(val)
    return out


def _find_florida_signals(text: str) -> list[str]:
    up = text.upper()
    return [t for t in _FLORIDA_TOKENS if re.search(rf'\b{re.escape(t)}\b', up)]


def _find_architect_name(text: str) -> Optional[str]:
    m = _ARCHITECT_LINE_RX.search(text)
    if not m:
        return None
    candidate = m.group(2).strip().splitlines()[0].strip(" -:,")
    if len(candidate) < 4 or len(candidate) > 80:
        return None
    return candidate


def _find_contractor_name(text: str) -> Optional[str]:
    m = _CONTRACTOR_LINE_RX.search(text)
    if not m:
        return None
    candidate = m.group(2).strip().splitlines()[0].strip(" -:,")
    if len(candidate) < 4 or len(candidate) > 80:
        return None
    return candidate


def _classify_scope_pages(engine, doc, ctx: PlanSetContext) -> list[ScopePage]:
    """Score every page for scope-page probability. Returns all hits."""
    scope_pages: list[ScopePage] = []

    for page_num in range(doc.page_count):
        try:
            text_blocks = engine.extract_text_blocks(doc, page_num)
        except Exception:
            continue
        try:
            vector_count = len(engine.extract_vectors(doc, page_num))
        except Exception:
            vector_count = 0

        page_text = " ".join(getattr(tb, "text", "") or getattr(tb, "content", "") or "" for tb in text_blocks)
        text_block_count = len(text_blocks)

        # HARD GATE — structural check. A scope page is a text document,
        # not a drawing. Drawing pages are rejected no matter what words
        # appear in their annotations.
        if vector_count > 500:
            continue
        if text_block_count < 15:
            continue

        score = 0
        evidence: list[str] = []

        evidence.append(f"text/vector ratio (tb={text_block_count}, v={vector_count})")

        page_upper = page_text.upper()

        for kw in _SCOPE_KEYWORDS:
            if kw in page_upper:
                score += 1
                evidence.append(f"keyword '{kw}'")

        div07 = _find_spec_sections(page_text)
        if div07:
            score += 3
            evidence.append(f"{len(div07)} Division 07 spec section(s)")

        mfrs = _find_manufacturers_in_text(page_text)
        if mfrs:
            score += 2
            evidence.append("manufacturer(s): " + ", ".join(mfrs[:3]))

        # Higher bar now that noise keywords are gone and structural gate
        # already removed drawing pages.
        if score >= 3:
            scope_pages.append(ScopePage(
                page_number=page_num,
                score=score,
                evidence=evidence,
                text=page_text,
            ))

    scope_pages.sort(key=lambda p: p.score, reverse=True)
    return scope_pages


def _resolve_scope_system(spec_sections: list[str],
                          manufacturers: list[str],
                          material_markers: list[str]) -> tuple[Optional[str], float, str]:
    """Decide the system from accumulated scope signals.

    Priority:
      1. Div 07 spec section unambiguously naming a system (0.9)
      2. Manufacturer + product match (0.85)
      3. Manufacturer alone mapping to single system (0.7)
      4. Thickness marker in roof context (0.7)
    Reinforcement: multiple independent signals → bump 0.05 (cap 0.95).
    """
    from seeds.roofing_spec_database import (
        spec_section_to_system, MANUFACTURERS, MATERIAL_PROPERTIES,
    )

    votes: dict[str, list[str]] = {}

    def _vote(system: str, ev: str):
        if system is None:
            return
        votes.setdefault(system, []).append(ev)

    best_evidence: list[str] = []

    for sec in spec_sections:
        sys_, name = spec_section_to_system(sec)
        if sys_:
            _vote(sys_, f"spec {sec} → {name}")
            best_evidence.append(f"spec {sec}")

    for mfr in manufacturers:
        data = MANUFACTURERS.get(mfr, {})
        systems = data.get("systems", [])
        if len(systems) == 1:
            _vote(systems[0], f"{mfr} manufacturer")
            best_evidence.append(f"{mfr}")
        elif len(systems) > 1:
            # Narrowing vote — split 0.4 across systems
            for s in systems:
                votes.setdefault(s, []).append(f"{mfr} (multi-system)")

    # Membrane thickness hints
    thickness_mp = MATERIAL_PROPERTIES.get("thickness_markers", {})
    for marker in material_markers:
        norm = marker.lower().replace(" ", " ")
        for key, info in thickness_mp.items():
            if norm == key.lower() or norm.replace(" ", "") == key.lower().replace(" ", ""):
                for s in info.get("systems", []):
                    votes.setdefault(s, []).append(f"{marker}")

    # Metal gauge / galvalume signals
    metal_mp = MATERIAL_PROPERTIES.get("metal_markers", {})
    for marker in material_markers:
        norm = marker.lower()
        for key, info in metal_mp.items():
            if norm == key.lower() or norm.replace(" ", "") == key.lower().replace(" ", ""):
                for s in info.get("systems", []):
                    votes.setdefault(s, []).append(f"{marker}")

    if not votes:
        return None, 0.0, ""

    # Winner: most unique evidence sources
    winner = max(votes.items(), key=lambda kv: len(kv[1]))
    system, evidences = winner
    base = 0.7 if len(evidences) == 1 else min(0.95, 0.85 + 0.05 * (len(evidences) - 1))

    # Bump to 0.9 when a spec section unambiguously maps
    if any(e.startswith("spec ") for e in evidences):
        base = max(base, 0.9)

    return system, base, "; ".join(evidences[:5])


def _determine_roof_shape(spec_sections: list[str],
                          material_markers: list[str],
                          system: Optional[str]) -> Optional[str]:
    """Return 'flat_roof' / 'steep_roof' when we have signal."""
    from seeds.roofing_spec_database import SPEC_SECTIONS, MATERIAL_PROPERTIES

    flat_systems = {"tpo", "pvc", "epdm", "modified_bitumen", "built_up"}
    steep_systems = {"shingle"}

    if system in flat_systems:
        return "flat_roof"
    if system in steep_systems:
        return "steep_roof"

    # Insulation marker → flat
    insul = MATERIAL_PROPERTIES.get("insulation_markers", {})
    for marker in material_markers:
        if marker.lower() in {k.lower() for k in insul.keys()}:
            return "flat_roof"

    for sec in spec_sections:
        entry = SPEC_SECTIONS.get(sec) or SPEC_SECTIONS.get(sec.replace(" ", ""))
        if entry and entry.get("signal") == "flat_roof":
            return "flat_roof"

    return None


def run_scope_scanner(engine, doc, ctx: PlanSetContext) -> None:
    """Scan every page, build ProjectScope, attach to ctx."""
    pages = _classify_scope_pages(engine, doc, ctx)
    if not pages:
        ctx.project_scope = ProjectScope()
        return

    all_specs: list[str] = []
    all_mfrs: list[str] = []
    all_mats: list[str] = []
    all_fl: list[str] = []
    architect: Optional[str] = None
    contractor: Optional[str] = None

    for sp in pages:
        for s in _find_spec_sections(sp.text):
            if s not in all_specs:
                all_specs.append(s)
        for m in _find_manufacturers_in_text(sp.text):
            if m not in all_mfrs:
                all_mfrs.append(m)
        for mat in _find_material_markers(sp.text):
            if mat not in all_mats:
                all_mats.append(mat)
        for fl in _find_florida_signals(sp.text):
            if fl not in all_fl:
                all_fl.append(fl)
        if not architect:
            architect = _find_architect_name(sp.text)
        if not contractor:
            contractor = _find_contractor_name(sp.text)

    system, conf, evidence = _resolve_scope_system(all_specs, all_mfrs, all_mats)
    shape = _determine_roof_shape(all_specs, all_mats, system)

    page_list = [sp.page_number for sp in pages]
    if evidence:
        evidence_prefix = f"from {len(pages)} scope page(s) {page_list[:3]}: "
        full_evidence = evidence_prefix + evidence
    else:
        full_evidence = f"{len(pages)} scope page(s) scanned, no system signal"

    ctx.project_scope = ProjectScope(
        scope_pages=page_list,
        spec_sections=all_specs,
        detected_system=system,
        system_confidence=conf,
        system_evidence=full_evidence,
        manufacturers=all_mfrs,
        material_mentions=all_mats,
        florida_signals=all_fl,
        roof_shape_signal=shape,
        architect=architect,
        contractor=contractor,
    )


# D.1: Stage 13 — trade module wiring helpers.
#
# Approach: when storage is activated, run_dispatch invokes Roofing + Glazing
# modules per page after Filter 5 / scope_scanner / project_metadata complete.
# Inputs are built via core.trade_input_builder.build_trade_input(), which now
# (post-calibration Bug 3 fix) reads page_ctx.raw_tables and populates
# TradeModuleInput.tables. Geometry-derived polygon fields are zeroed because
# Stages 6–9 are not yet wired into run_dispatch (deferred to D.2/E); this
# matches the C.2-established equivalent path used by sweep / calibration
# harnesses. Module outputs land on ctx.trade_module_outputs.

def _build_dispatch_only_input(ctx: PlanSetContext, page_idx: int,
                               text_blocks: list, raw_tables):
    """D.1: build a TradeModuleInput without geometry results.

    Geometry isn't wired into dispatch yet (Phase D.2/E), so polygon-derived
    fields are zeroed, mirroring the C.2-established direct-construction
    pattern used by the calibration / sweep harnesses. The dispatch-side
    state (page_type, page_legends, page_zones, raw_tables, project_scope)
    is wired through correctly.
    """
    from core.trade_module import TradeModuleInput

    page_ctx = ctx.pages.get(page_idx)
    page_type = "UNKNOWN"
    page_legends: list = []
    page_zones: list = []
    if page_ctx is not None:
        pt = getattr(page_ctx, "page_type", None)
        page_type = getattr(pt, "value", str(pt)) if pt is not None else "UNKNOWN"
        page_legends = list(page_ctx.legends or [])
        page_zones = list(page_ctx.zones or [])

    return TradeModuleInput(
        polygon_area_sqin=0.0,
        polygon_area_sf=0.0,
        polygon_perimeter_in=0.0,
        polygon_perimeter_lf=0.0,
        polygon_bbox=(0.0, 0.0, 0.0, 0.0),
        polygon_vertices=0,
        scale_fpi=0.0,
        scale_source="unwired",
        scale_confidence=0.0,
        detection_source="none",
        interior_text_blocks=text_blocks,
        equipment_callouts=[],
        dimension_strings=[],
        page_type=page_type,
        page_legends=page_legends,
        page_zones=page_zones,
        tables=raw_tables if raw_tables else None,
        project_scope=getattr(ctx, "project_scope", None),
        page_number=page_idx,
    )


def _run_trade_modules(engine: PDFEngine, doc, ctx: PlanSetContext) -> None:
    """D.1: Stage 13 — run RoofingModule + GlazingModule for every page.

    Per-page errors are caught and logged to ctx.dispatch_warnings without
    aborting the loop. If the per-module error rate exceeds 25% of pages
    attempted, a single summary warning is appended (the §11 #6 stop is
    triggered by the gate harness reading dispatch_warnings, not by this
    helper raising — keeps run_dispatch's contract simple).
    """
    from core.roofing_module import RoofingModule
    from core.glazing_module import GlazingModule

    roofing_mod = RoofingModule()
    glazing_mod = GlazingModule()

    pages_attempted = 0
    roofing_errors = 0
    glazing_errors = 0

    use_pdfplumber = _pdfplumber is not None
    pdf = None
    if use_pdfplumber:
        try:
            pdf = _pdfplumber.open(ctx.pdf_path)
        except Exception as exc:
            ctx.dispatch_warnings.append(
                f"trade module wiring: pdfplumber.open failed ({type(exc).__name__}); "
                "trade modules skipped"
            )
            return

    try:
        for page_idx in sorted(ctx.pages.keys()):
            page_ctx = ctx.pages[page_idx]
            text_blocks: list = []
            raw_tables = page_ctx.raw_tables  # cached by Filter 4 for SCHEDULE pages

            # Pull per-page text blocks via pdfplumber (cheap; Filter 4 already
            # paid extract_tables() for schedule pages so raw_tables is reused).
            # Also fall back to extract_tables() for non-schedule pages so
            # door/glazing schedules on non-SCHEDULE_SHEET-classified pages
            # land on TradeModuleInput.tables — matches the calibration
            # harness's all-pages table coverage and avoids module output
            # regression.
            if pdf is not None and page_idx < len(pdf.pages):
                try:
                    pdf_page = pdf.pages[page_idx]
                    words = pdf_page.extract_words() or []
                    for w in words:
                        try:
                            text_blocks.append(TextBlock(
                                text=str(w.get("text", "")),
                                x0=float(w.get("x0", 0.0)),
                                y0=float(w.get("top", 0.0)),
                                x1=float(w.get("x1", 0.0)),
                                y1=float(w.get("bottom", 0.0)),
                                page=page_idx,
                            ))
                        except Exception:
                            continue
                    if not raw_tables:
                        try:
                            ext = pdf_page.extract_tables() or []
                            if ext:
                                raw_tables = [t for t in ext if t]
                        except Exception:
                            pass
                except Exception:
                    text_blocks = []

            tinput = _build_dispatch_only_input(ctx, page_idx, text_blocks, raw_tables)
            pages_attempted += 1
            per_page: dict = {}

            try:
                per_page["roofing"] = roofing_mod.analyze(tinput)
            except Exception as exc:
                roofing_errors += 1
                ctx.dispatch_warnings.append(
                    f"trade module page {page_idx} roofing.analyze raised "
                    f"{type(exc).__name__}: {str(exc)[:120]}"
                )

            try:
                per_page["glazing"] = glazing_mod.analyze(tinput)
            except Exception as exc:
                glazing_errors += 1
                ctx.dispatch_warnings.append(
                    f"trade module page {page_idx} glazing.analyze raised "
                    f"{type(exc).__name__}: {str(exc)[:120]}"
                )

            if per_page:
                ctx.trade_module_outputs[page_idx] = per_page
    finally:
        if pdf is not None:
            try:
                pdf.close()
            except Exception:
                pass

    # §11 #6: surface error-rate threshold. Hard stop is the harness's job.
    if pages_attempted > 0:
        r_rate = roofing_errors / pages_attempted
        g_rate = glazing_errors / pages_attempted
        if r_rate > 0.25:
            ctx.dispatch_warnings.append(
                f"trade module wiring: roofing error rate {r_rate:.0%} "
                f"({roofing_errors}/{pages_attempted}) exceeds 25% threshold"
            )
        if g_rate > 0.25:
            ctx.dispatch_warnings.append(
                f"trade module wiring: glazing error rate {g_rate:.0%} "
                f"({glazing_errors}/{pages_attempted}) exceeds 25% threshold"
            )

    ctx.filters_completed.append("stage_13_trade_modules")  # D.1


_DEFAULT_STORAGE_INSTANCE = None  # D.1: lazy singleton for storage="auto"


def _resolve_storage(storage):
    """D.1: resolve the storage argument per Phase D.1 march orders §4.

    - storage=None: legacy no-op (preserves test_dispatch.py expectations)
    - storage="auto": lazily construct a default SQLite-backed StorageEngine,
      cached as a module-level singleton for the process lifetime
    - any other value: assumed to be a pre-constructed storage instance
    """
    if storage is None:
        return None
    if storage == "auto":
        global _DEFAULT_STORAGE_INSTANCE
        if _DEFAULT_STORAGE_INSTANCE is None:
            from core.storage import StorageEngine
            _DEFAULT_STORAGE_INSTANCE = StorageEngine()
        return _DEFAULT_STORAGE_INSTANCE
    return storage


def run_dispatch(pdf_path: str | Path, storage=None, job_id: str | None = None) -> PlanSetContext:
    """
    Run the full dispatch gate on a PDF plan set.
    Returns a populated PlanSetContext.

    If storage is provided (instance or "auto" sentinel — D.1), also runs
    architect-firm detection after Filter 5 and attaches the profile (or a
    stub) to ctx.architect_profile, and wires RoofingModule + GlazingModule
    into the production call path so per-page TradeModuleOutput records land
    on ctx.trade_module_outputs.

    If job_id is provided (D.2), persists dispatch results and trade module
    outputs to the jobs database after Stage 13 completes.
    """
    pdf_path = Path(pdf_path)
    engine = PDFEngine()
    doc = engine.open(pdf_path)

    storage = _resolve_storage(storage)  # D.1: lazy default storage activation

    ctx = PlanSetContext(
        pdf_path=str(pdf_path),
        pdf_hash=_file_hash(pdf_path),
        total_pages=doc.page_count,
    )

    try:
        # Filter 1: Document Structure (sheet map)
        run_filter_1(engine, doc, ctx)

        # Filter 2: Page Classification
        run_filter_2(engine, doc, ctx)

        # Filter 4: Legend/Schedule Parsing (run before Filter 3 so keynote
        # detection knows which pages have keynote legends)
        run_filter_4(engine, doc, ctx)

        # Filter 3: Cross-Reference Extraction
        run_filter_3(engine, doc, ctx)

        # Filter 5: Zone Classification
        run_filter_5(engine, doc, ctx)

        # Scope page scanner (Step 75) — reads every page for cover/separator
        # content and builds PlanSetContext.project_scope.
        try:
            run_scope_scanner(engine, doc, ctx)
        except Exception as e:
            ctx.dispatch_warnings.append(f"scope scanner failed: {e}")

        # Architect profile detection (optional — needs storage)
        if storage is not None:
            try:
                from core.architect_profile import detect_firm
                tb_text = _collect_title_block_text(engine, doc, ctx)
                ctx.architect_profile = detect_firm(tb_text, storage)
            except Exception as e:
                ctx.dispatch_warnings.append(f"architect_profile detection failed: {e}")

        # Project Metadata
        _extract_project_metadata(engine, doc, ctx)

        # D.1: Stage 13 — wire trade modules into the production path. Only
        # runs when storage is activated (storage=None preserves legacy
        # test path that expects no module side-effects). Errors per page
        # are logged to dispatch_warnings; >25% per-module error rate is
        # surfaced as a single warning per the §11 #6 stop threshold.
        if storage is not None:
            try:
                _run_trade_modules(engine, doc, ctx)
            except Exception as e:
                ctx.dispatch_warnings.append(f"trade module wiring failed: {e}")

        # D.2: persist dispatch results + trade outputs to job database
        if job_id is not None:
            try:
                from core.job_storage import persist_dispatch_result, persist_trade_outputs, mark_dispatch_complete  # D.2:
                persist_dispatch_result(job_id, ctx)  # D.2:
                persist_trade_outputs(job_id, ctx)  # D.2:
                mark_dispatch_complete(job_id)  # D.2:
            except Exception as e:  # D.2:
                ctx.dispatch_warnings.append(f"D.2 job persistence failed: {e}")  # D.2:

        # Leak check
        ctx.dispatch_warnings.extend(check_for_leaks(ctx))

        ctx.dispatch_complete = True
        ctx.dispatch_timestamp = datetime.now(timezone.utc).isoformat()

    finally:
        engine.close(doc)

    return ctx


# ============================================================
# JSON SERIALIZATION
# ============================================================

def _ctx_to_dict(ctx: PlanSetContext) -> dict:
    """Convert PlanSetContext to a JSON-serializable dict."""

    def _source_tag(tag):
        if tag is None:
            return None
        return {"origin": tag.origin, "confidence": tag.confidence, "evidence": tag.evidence}

    def _scale_info(si):
        if si is None:
            return None
        return {
            "scale_string": si.scale_string,
            "ft_per_inch": si.ft_per_inch,
            "source": si.source,
            "source_page": si.source_page,
            "confidence": si.confidence,
        }

    sheet_map = {}
    for sn, entry in ctx.sheet_map.items():
        sheet_map[sn] = {
            "sheet_number": entry.sheet_number,
            "title": entry.title,
            "page_index": entry.page_index,
            "discipline": entry.discipline.value,
            "page_type": entry.page_type.value,
            "scale": _scale_info(entry.scale),
            "confidence": entry.confidence,
        }

    pages = {}
    for idx, pc in ctx.pages.items():
        pages[str(idx)] = {
            "page_index": pc.page_index,
            "sheet_number": pc.sheet_number,
            "title": pc.title,
            "discipline": pc.discipline.value,
            "page_type": pc.page_type.value,
            "scale": _scale_info(pc.scale),
            "confidence": pc.confidence,
            "zone_count": len(pc.zones),
            "legend_count": len(pc.legends),
            "cross_refs_out": len(pc.cross_refs_out),
            "cross_refs_in": len(pc.cross_refs_in),
            "has_drawing_area": pc.has_drawing_area,
            "has_title_block": pc.has_title_block,
            "has_details": pc.has_details,
            "has_schedule": pc.has_schedule,
            "has_legend": pc.has_legend,
            "detail_count": pc.detail_count,
        }

    cross_refs = []
    for ref in ctx.all_cross_refs:
        cross_refs.append({
            "ref_type": ref.ref_type,
            "identifier": ref.identifier,
            "text": ref.text[:60],
            "source_page": ref.source_page,
            "target_sheet": ref.target_sheet,
            "target_page": ref.target_page,
            "resolved": ref.resolved,
            "confidence": ref.confidence,
        })

    legends = []
    for leg in ctx.all_legends:
        legends.append({
            "legend_type": leg.legend_type,
            "title": leg.title[:60],
            "page_index": leg.page_index,
            "entry_count": leg.entry_count,
            "confidence": leg.confidence,
        })

    project = {
        "project_name": ctx.project.project_name,
        "project_address": ctx.project.project_address,
        "project_number": ctx.project.project_number,
        "total_pages": ctx.project.total_pages,
        "total_building_sf": ctx.project.total_building_sf,
    }

    return {
        "pdf_path": ctx.pdf_path,
        "pdf_hash": ctx.pdf_hash,
        "total_pages": ctx.total_pages,
        "sheet_map_source": ctx.sheet_map_source,
        "sheet_map": sheet_map,
        "page_to_sheet": {str(k): v for k, v in ctx.page_to_sheet.items()},
        "pages": pages,
        "cross_refs_total": len(ctx.all_cross_refs),
        "cross_refs_resolved": ctx.resolved_count,
        "cross_refs_unresolved": ctx.unresolved_count,
        "cross_refs": cross_refs,
        "legends_total": len(ctx.all_legends),
        "legends_by_type": {k: len(v) for k, v in ctx.legends_by_type.items()},
        "legends": legends,
        "project": project,
        "filters_completed": ctx.filters_completed,
        "dispatch_complete": ctx.dispatch_complete,
        "dispatch_timestamp": ctx.dispatch_timestamp,
        "dispatch_warnings": ctx.dispatch_warnings,
    }


# ============================================================
# CLI
# ============================================================

def _safe_print(text: str):
    """Print with fallback for non-encodable characters on Windows."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode("ascii"))


def _print_report(ctx: PlanSetContext):
    """Print human-readable dispatch report."""
    _safe_print(f"\n{'='*60}")
    _safe_print(f"DISPATCH GATE -- {Path(ctx.pdf_path).name}")
    _safe_print(f"{'='*60}")

    # Sheet Map
    _safe_print(f"\nSHEET MAP: {len(ctx.sheet_map)} sheets (source: {ctx.sheet_map_source})")
    for sn, entry in sorted(ctx.sheet_map.items()):
        page_str = f"page {entry.page_index}" if entry.page_index >= 0 else "UNMAPPED"
        _safe_print(f"  {sn:<10} -> {page_str:<10} | {entry.page_type.value:<18} | "
                    f"{entry.discipline.value:<3} | conf {entry.confidence:.1f}")

    # Page Classification
    _safe_print(f"\nPAGE CLASSIFICATION:")
    type_counts = {}
    for pc in ctx.pages.values():
        t = pc.page_type.value
        type_counts[t] = type_counts.get(t, 0) + 1
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        _safe_print(f"  {t:<20}: {c} pages")

    # Cross-References
    total_refs = len(ctx.all_cross_refs)
    if total_refs > 0:
        rate = ctx.resolved_count / total_refs * 100
        _safe_print(f"\nCROSS-REFERENCES: {total_refs} found, {ctx.resolved_count} resolved ({rate:.0f}%)")
        target_counts = {}
        for ref in ctx.all_cross_refs:
            if ref.target_sheet:
                target_counts[ref.target_sheet] = target_counts.get(ref.target_sheet, 0) + 1
        top = sorted(target_counts.items(), key=lambda x: -x[1])[:10]
        if top:
            _safe_print(f"  Top targets: " + ", ".join(f"{s} ({c} refs)" for s, c in top))
    else:
        _safe_print(f"\nCROSS-REFERENCES: 0 found")

    # Legends
    _safe_print(f"\nLEGENDS: {len(ctx.all_legends)} found")
    for leg in ctx.all_legends:
        _safe_print(f"  \"{leg.title[:50]}\" ({leg.entry_count} entries, page {leg.page_index}, type: {leg.legend_type})")

    # Scale Sources
    _safe_print(f"\nSCALE SOURCES:")
    pages_with_scale = [(idx, pc) for idx, pc in sorted(ctx.pages.items()) if pc.scale]
    if pages_with_scale:
        for idx, pc in pages_with_scale[:20]:
            _safe_print(f"  Page {idx}: {pc.scale.source} \"{pc.scale.scale_string}\" (conf {pc.scale.confidence:.1f})")
        if len(pages_with_scale) > 20:
            _safe_print(f"  ... and {len(pages_with_scale) - 20} more")
    else:
        _safe_print(f"  No scales detected")

    # Project
    _safe_print(f"\nPROJECT:")
    if ctx.project.project_name:
        _safe_print(f"  Name: {ctx.project.project_name}")
    if ctx.project.project_address:
        _safe_print(f"  Address: {ctx.project.project_address}")
    if ctx.project.total_building_sf:
        _safe_print(f"  Building SF: {ctx.project.total_building_sf:,.0f}")

    # Status
    _safe_print(f"\nFILTERS COMPLETED: {ctx.filters_completed}")
    if ctx.dispatch_warnings:
        _safe_print(f"WARNINGS:")
        for w in ctx.dispatch_warnings:
            _safe_print(f"  {w}")
    _safe_print(f"{'='*60}\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m core.dispatch_gate <path/to/plan.pdf>")
        sys.exit(1)

    pdf_path = Path(sys.argv[1])
    if not pdf_path.exists():
        print(f"File not found: {pdf_path}")
        sys.exit(1)

    t0 = time.time()
    ctx = run_dispatch(pdf_path)
    elapsed = time.time() - t0

    _print_report(ctx)
    print(f"Time: {elapsed:.1f}s")

    # Save JSON
    out_path = Path("scripts/dispatch_results.json")
    out_path.parent.mkdir(exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(_ctx_to_dict(ctx), f, indent=2)
    print(f"Results saved to {out_path}")


if __name__ == "__main__":
    main()
