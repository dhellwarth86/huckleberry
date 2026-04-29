"""intake_diagnostic_pass2.py — second-pass diagnostic over the 10 STACK
bidsets that had positive manufacturer hits AND empty scope_pages in
pass 1.

For each manufacturer hit on each page, capture:
  - bidset_id, page_number, sheet_number, page_type
  - manufacturer canonical + matched_name
  - 80 chars of surrounding context (40 before + 40 after the match)
  - is_in_title_block_zone (heuristic: bbox center in bottom-right quadrant)
  - is_in_drawing_index (page is the bidset's drawing-index page)
  - is_repeating_text (same canonical appears on >5 pages of same bidset)
  - nearby_spec_section_ref (Division 7 reference within ±200 chars)

DOES NOT modify any ported file. DOES NOT extend vocabulary. DOES NOT
propose fixes. Read-only.
"""

from __future__ import annotations

import json
import re
import sys
import time
import traceback
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

import fitz  # PyMuPDF — same library dispatch + pass 1 used

from seeds.roofing_spec_database import all_manufacturer_names  # noqa: E402

STACK_MANIFEST = BACKEND_DIR / "test_fixtures" / "bidsets.json"
STACK_OUTPUTS_DIR = BACKEND_DIR / "test_fixtures" / "v0.2_outputs"
PASS1_SUMMARY = BACKEND_DIR / "test_fixtures" / "intake_diagnostic_summary.json"
PASS2_SUMMARY = BACKEND_DIR / "test_fixtures" / "intake_diagnostic_pass2_summary.json"

# Title-block zone heuristic: bottom-right quadrant.
# Same fractions used in dispatch_gate._get_title_block_text() (qx = 0.6w,
# qy = 0.6h). Verbatim from there.
TITLE_BLOCK_X_FRAC = 0.6
TITLE_BLOCK_Y_FRAC = 0.6

# Repeating-text threshold from Daniel's brief: >5 pages
REPEATING_THRESHOLD = 5

# Nearby-spec radius from brief: ±200 chars
NEARBY_SPEC_RADIUS = 200

# Drawing-index gate: same as Filter 1's _find_drawing_index_page (10+
# unique sheet numbers in early pages, scan first 10 pages).
DRAWING_INDEX_MIN_SHEETS = 10
DRAWING_INDEX_SCAN_PAGES = 10
_SHEET_NUM_RE = re.compile(r"\b([A-Z]{1,2})-?(\d+[\.\d]*[A-Za-z]?)\b")
_SPEC_SECTION_RX = re.compile(r"\b(0?7)[\s\-]?(\d{2})(?:[\s\-]?(\d{2,4}))?\b")

# Manufacturer patterns (verbatim from pass 1)
_MFR_PAIRS = all_manufacturer_names()
_MFR_PATTERNS = [
    (canonical, search_name, re.compile(rf"\b{re.escape(search_name)}\b", re.IGNORECASE))
    for search_name, canonical in _MFR_PAIRS
]

# Negation patterns (verbatim from pass 1)
_NEGATION_RX = re.compile(r"\b(NOT\s+(?:ACCEPTABLE|PERMITTED|APPROVED))\b", re.IGNORECASE)
NEGATION_RADIUS_CHARS = 50


# ─── Targets: STACK bidsets with mfr_pos>0 AND scope_pages=0 from pass 1 ─

def load_targets() -> list[dict[str, Any]]:
    summary = json.loads(PASS1_SUMMARY.read_text(encoding="utf-8"))
    targets = [
        a for a in summary["aggregates"]
        if a["corpus"] == "stack"
        and a["manufacturer_hits_positive_total"] > 0
        and not a["scope_pages_indices"]
    ]
    targets.sort(key=lambda a: -a["manufacturer_hits_positive_total"])

    manifest = json.loads(STACK_MANIFEST.read_text(encoding="utf-8"))
    by_id = {b["id"]: b for b in manifest["bidsets"]}

    out = []
    for t in targets:
        m = by_id.get(t["bidset_id"])
        if not m:
            continue
        out.append({
            "id": t["bidset_id"],
            "local_path": m["local_path"],
            "json_path": str(STACK_OUTPUTS_DIR / f"{t['bidset_id']}.json"),
            "pass1_mfr_pos": t["manufacturer_hits_positive_total"],
        })
    return out


# ─── Drawing-index page detection (replicates Filter 1's gate) ──────────

def detect_drawing_index_page(doc: fitz.Document, sheet_map_source: str) -> int | None:
    """Replicate Filter 1's gate: if sheet_map_source is 'drawing_index',
    find the page that has 10+ unique sheet-number patterns within the
    first DRAWING_INDEX_SCAN_PAGES pages. Returns the page index or None.

    This is read-only (does not modify the JSON or any code). It re-runs
    the same heuristic so the 'is_in_drawing_index' classification is
    accurate per-page."""
    if sheet_map_source != "drawing_index":
        return None
    scan_range = min(doc.page_count, DRAWING_INDEX_SCAN_PAGES)
    for idx in range(scan_range):
        try:
            text = doc.load_page(idx).get_text("text") or ""
        except Exception:
            continue
        unique_sheets = {m.group(0) for m in _SHEET_NUM_RE.finditer(text)}
        if len(unique_sheets) >= DRAWING_INDEX_MIN_SHEETS:
            return idx
    return None


# ─── Per-page processing ────────────────────────────────────────────────

def find_match_bbox(page: fitz.Page, search_text: str) -> tuple[float, float, float, float] | None:
    """Use PyMuPDF's search_for to locate search_text on the page.
    Returns the first bbox or None."""
    try:
        rects = page.search_for(search_text)
    except Exception:
        rects = []
    if rects:
        r = rects[0]
        # PyMuPDF Rect is (x0, y0, x1, y1)
        return (float(r.x0), float(r.y0), float(r.x1), float(r.y1))
    return None


def is_in_title_block(bbox: tuple[float, float, float, float] | None,
                     page_w: float, page_h: float) -> bool:
    if bbox is None or page_w <= 0 or page_h <= 0:
        return False
    cx = (bbox[0] + bbox[2]) / 2.0
    cy = (bbox[1] + bbox[3]) / 2.0
    return cx >= page_w * TITLE_BLOCK_X_FRAC and cy >= page_h * TITLE_BLOCK_Y_FRAC


def context_window(text: str, match_start: int, match_end: int, before: int = 40, after: int = 40) -> str:
    """Return text[match_start-before : match_end+after] with whitespace
    collapsed to single spaces for compact display."""
    s = max(0, match_start - before)
    e = min(len(text), match_end + after)
    snip = text[s:e]
    return re.sub(r"\s+", " ", snip).strip()


def nearby_spec_section(text: str, match_start: int, match_end: int,
                        radius: int = NEARBY_SPEC_RADIUS) -> str | None:
    """Find any Division 7 spec-section reference within ±radius chars of
    the match. Returns the first match string, or None."""
    s = max(0, match_start - radius)
    e = min(len(text), match_end + radius)
    window = text[s:e]
    for m in _SPEC_SECTION_RX.finditer(window):
        a, b, c = m.group(1), m.group(2), m.group(3)
        if a.lstrip("0") == "7":  # Division 07 only
            return m.group(0)
    return None


def scan_page_manufacturers(text: str) -> list[dict[str, Any]]:
    """Return list of {canonical, matched_name, match_start, match_end}.
    Per-canonical dedup within page (one position per canonical, the
    first match) — same shape as pass 1's per-page scan."""
    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    for canonical, search_name, pat in _MFR_PATTERNS:
        if canonical in seen:
            continue
        m = pat.search(text)
        if not m:
            continue
        seen.add(canonical)
        out.append({
            "canonical": canonical,
            "matched_name": search_name,
            "match_start": m.start(),
            "match_end": m.end(),
        })
    return out


# ─── Main per-bidset processing ─────────────────────────────────────────

def process_bidset(target: dict[str, Any]) -> dict[str, Any]:
    bidset_id = target["id"]
    pdf_path = Path(target["local_path"])
    json_data = json.loads(Path(target["json_path"]).read_text(encoding="utf-8"))
    sheet_map_source = json_data.get("sheet_map_source", "none")
    pages_meta = json_data.get("pages", {})

    doc = fitz.open(str(pdf_path))
    try:
        di_page = detect_drawing_index_page(doc, sheet_map_source)

        # First pass: gather all hits with raw context (no repetition flag yet).
        # Then second pass: tag is_repeating_text per (canonical, count of pages).
        raw_hits: list[dict[str, Any]] = []
        canonical_pages: dict[str, set[int]] = defaultdict(set)

        for idx in range(doc.page_count):
            try:
                page = doc.load_page(idx)
                text = page.get_text("text") or ""
            except Exception:
                continue
            if not text:
                continue

            page_w = float(page.rect.width)
            page_h = float(page.rect.height)
            pc = pages_meta.get(str(idx), {})
            sheet_num = pc.get("sheet_number") or ""
            page_type = pc.get("page_type", "unknown")

            mfr_hits = scan_page_manufacturers(text)
            if not mfr_hits:
                continue

            for h in mfr_hits:
                canonical_pages[h["canonical"]].add(idx)
                bbox = find_match_bbox(page, h["matched_name"])
                tb_zone = is_in_title_block(bbox, page_w, page_h)
                ctx = context_window(text, h["match_start"], h["match_end"], before=40, after=40)
                neg_window = text[max(0, h["match_start"] - NEGATION_RADIUS_CHARS): h["match_end"] + NEGATION_RADIUS_CHARS]
                negated = bool(_NEGATION_RX.search(neg_window))
                spec_ref = nearby_spec_section(text, h["match_start"], h["match_end"])
                raw_hits.append({
                    "bidset_id": bidset_id,
                    "page_index": idx,
                    "sheet_number": sheet_num,
                    "page_type": page_type,
                    "canonical": h["canonical"],
                    "matched_name": h["matched_name"],
                    "context_80": ctx,
                    "match_bbox": bbox,
                    "page_w": page_w,
                    "page_h": page_h,
                    "is_in_title_block_zone": tb_zone,
                    "is_in_drawing_index": (di_page is not None and idx == di_page),
                    "negated": negated,
                    "nearby_spec_section_ref": spec_ref,
                })

        # Apply repetition flag: a canonical seen on >REPEATING_THRESHOLD
        # pages of this bidset → all its hits flagged as repeating
        repeating_canonicals = {
            c for c, pages in canonical_pages.items()
            if len(pages) > REPEATING_THRESHOLD
        }
        for h in raw_hits:
            h["is_repeating_text"] = h["canonical"] in repeating_canonicals
            h["repeating_page_count"] = len(canonical_pages[h["canonical"]])

    finally:
        doc.close()

    return {
        "bidset_id": bidset_id,
        "sheet_map_source": sheet_map_source,
        "drawing_index_page": di_page,
        "n_hits": len(raw_hits),
        "hits": raw_hits,
        "canonical_page_counts": {c: len(p) for c, p in canonical_pages.items()},
        "repeating_canonicals": sorted(repeating_canonicals),
    }


# ─── Aggregate roll-up ──────────────────────────────────────────────────

def classify_location(hit: dict[str, Any]) -> str:
    """Single-label location classification for the aggregate roll-up.
    Priority: drawing_index > title_block > repeating_text >
    has_nearby_spec_section > body_text_other."""
    if hit["is_in_drawing_index"]:
        return "drawing_index_page"
    if hit["is_in_title_block_zone"]:
        return "title_block_zone"
    if hit["is_repeating_text"]:
        return "repeating_text_boilerplate"
    if hit["nearby_spec_section_ref"]:
        return "near_spec_section"
    if hit["negated"]:
        return "negation_window"
    return "body_text_other"


def aggregate_locations(all_hits: list[dict[str, Any]]) -> dict[str, int]:
    return dict(Counter(classify_location(h) for h in all_hits))


# ─── Main ───────────────────────────────────────────────────────────────

def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", action="append", help="Process only these bidset ids")
    args = parser.parse_args()

    targets = load_targets()
    if args.only:
        wanted = set(args.only)
        targets = [t for t in targets if t["id"] in wanted]

    print(f"Pass 2 — processing {len(targets)} bidset(s)")
    print()

    all_results: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    t0_corpus = time.time()
    for target in targets:
        bid = target["id"]
        print(f"  [run] {bid}  (pass1 mfr_pos={target['pass1_mfr_pos']})")
        t0 = time.time()
        try:
            res = process_bidset(target)
            elapsed = time.time() - t0
            res["elapsed_s"] = round(elapsed, 1)
            all_results.append(res)
            print(f"        n_hits={res['n_hits']}  drawing_index_page={res['drawing_index_page']}  repeating={res['repeating_canonicals']}  elapsed={elapsed:.1f}s")
        except Exception as e:
            tb = traceback.format_exc()
            print(f"  [FAIL] {bid}  {type(e).__name__}: {e}")
            print(tb)
            failures.append({"id": bid, "error_type": type(e).__name__, "error_msg": str(e), "traceback": tb})

    total = time.time() - t0_corpus

    # Aggregate roll-up
    all_hits = [h for r in all_results for h in r["hits"]]
    agg = aggregate_locations(all_hits)
    n_total = len(all_hits)

    print()
    print("=" * 72)
    print(f"PASS 2 SUMMARY — {n_total} per-page-unique manufacturer hits across {len(all_results)} bidsets")
    print("=" * 72)
    print()
    print("Where do manufacturer hits live (single-label classification)?")
    for k, v in sorted(agg.items(), key=lambda kv: -kv[1]):
        pct = (100.0 * v / n_total) if n_total else 0.0
        print(f"  {k:<30}  {v:>3}  ({pct:.1f}%)")
    print()
    print(f"Total wall-clock: {total:.1f}s")

    summary = {
        "n_bidsets": len(all_results),
        "n_failures": len(failures),
        "n_hits_total": n_total,
        "elapsed_s": round(total, 1),
        "vocabulary_source": "seeds/roofing_spec_database.py (verbatim, not extended)",
        "title_block_x_frac": TITLE_BLOCK_X_FRAC,
        "title_block_y_frac": TITLE_BLOCK_Y_FRAC,
        "repeating_threshold": REPEATING_THRESHOLD,
        "nearby_spec_radius": NEARBY_SPEC_RADIUS,
        "drawing_index_min_sheets": DRAWING_INDEX_MIN_SHEETS,
        "drawing_index_scan_pages": DRAWING_INDEX_SCAN_PAGES,
        "location_aggregate": agg,
        "results": all_results,
        "failures": failures,
    }
    PASS2_SUMMARY.write_text(json.dumps(summary, indent=2, default=str))
    print(f"Pass 2 summary JSON: {PASS2_SUMMARY.relative_to(BACKEND_DIR)}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
