"""Profile diagnostic harness — times the existing extraction + module stack.

Phase: profile-and-housekeeping (2026-04-29)
Orders: MARCH_ORDERS_profile_and_housekeeping.md §5

Times these four operations per target page, with three repeats each, on
the Bearss Ave bidset:

    1. pdfplumber text extraction (extract_words on the page)
    2. pdfplumber table extraction (extract_tables on the page)
    3. RoofingModule().analyze on a TradeModuleInput built from that page
    4. GlazingModule().analyze on the same input

Captures full TradeModuleOutput from each module call. Cross-references
debug section 1 / 3 / 6 entries that correspond to the two target pages.

Reusable diagnostic template (tracked, unlike sweep_three_bidsets.py
which is a one-shot). Future profile diagnostics can import or copy
shape; future tuning sessions can re-run this on new bidsets.

§7 stops:
    - Dispatch raises (orders §10 #4)
    - Trade module raises on either target page (orders §10 #5 — single-
      page targeted run, no soft-recover)
    - Need to modify any backend/core/ file (orders §10 #6 — hard stop)
    - Need to add a dependency (orders §10 #7 — time.perf_counter only)

NOT included (orders §0, §5):
    - OCR libraries (Tesseract, PaddleOCR, Surya, Marker)
    - Benchmarking frameworks (cProfile, py-spy, snakeviz, etc.)
    - Memory profiling
    - Extractor alternatives evaluation
"""
from __future__ import annotations

import json
import statistics
import sys
import time
import traceback
from dataclasses import asdict, is_dataclass
from pathlib import Path

# Make the backend package importable when this script runs from repo root
HERE = Path(__file__).resolve()
BACKEND = HERE.parent.parent  # backend/
sys.path.insert(0, str(BACKEND))

import pdfplumber  # noqa: E402

from core.dispatch_gate import run_dispatch  # noqa: E402
from core.debug_module import run_debug  # noqa: E402
from core.roofing_module import RoofingModule  # noqa: E402
from core.glazing_module import GlazingModule  # noqa: E402
from core.trade_module import TradeModuleInput, TradeModuleOutput  # noqa: E402


PDF_PATH = Path(r"C:\huck stage 2\full bid sets\Bearss Ave Distribution Center - University - Marcobay Construction (3).pdf")
BIDSET_NAME = "bearss-ave"
SWEEP_REFERENCE_DISPATCH_S = 95.0   # per SWEEP_OBSERVATION_bearss-ave.md
SWEEP_REFERENCE_MODULES_S = 824.9   # per SWEEP_OBSERVATION_bearss-ave.md
SWEEP_REFERENCE_PAGES = 91

# Page selection driven by debug section 3 (page_intelligence) signal density
# from SWEEP_OBSERVATION_bearss-ave.md. Selection rationale documented in
# both the report (§1) and PAGE_SELECTION below.
HIGH_PAGE = 15      # S-103 SPECIAL INSPECTIONS — section-3 score 60 (top)
LOW_PAGE = 82       # unknown — section-3 score 3, type=unknown, conf=0.0

PAGE_SELECTION = {
    HIGH_PAGE: {
        "label": "high-content",
        "rationale": (
            "Top section-3 signal score (60), tied with page 61 which has "
            "unmapped sheet/title; page 15 chosen for clearer identity. "
            "Sheet S-103 'SPECIAL INSPECTIONS', type=section, 8 legends, "
            "11 zones, 41 refs_out, confidence 0.7. Section-typed = notes-"
            "heavy spec/inspections page; exercises pdfplumber text + "
            "module text-scanning paths."
        ),
    },
    LOW_PAGE: {
        "label": "low-content",
        "rationale": (
            "Section-3 signal score 3 (legends 0, zones 3, refs in/out 0). "
            "type=unknown, confidence 0.0, sheet '---', title '---'. The "
            "page debug section 3 has no opinion about — module behavior "
            "on a page with no dispatch-side classification signal."
        ),
    },
}

REPEATS = 3
OUTPUT_PATH = BACKEND / f"PROFILE_DIAGNOSTIC_{BIDSET_NAME}.md"


# ---------------------------------------------------------------------------
# Reusable helpers (shape mirrors sweep_three_bidsets.py)
# ---------------------------------------------------------------------------

class _TextBlock:
    __slots__ = ("text", "x0", "y0", "x1", "y1")

    def __init__(self, text, x0, y0, x1, y1):
        self.text = text
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1


def _extract_text_blocks(pdf_page) -> list:
    """pdfplumber.extract_words wrapped to module-friendly shape. Used by
    both the timed text-extraction measurement AND as input to the modules.
    """
    blocks: list = []
    words = pdf_page.extract_words() or []
    for w in words:
        try:
            blocks.append(
                _TextBlock(
                    text=str(w.get("text", "")),
                    x0=float(w.get("x0", 0.0)),
                    y0=float(w.get("top", 0.0)),
                    x1=float(w.get("x1", 0.0)),
                    y1=float(w.get("bottom", 0.0)),
                )
            )
        except Exception:
            continue
    return blocks


def _extract_tables(pdf_page) -> list:
    ext = pdf_page.extract_tables() or []
    return [t for t in ext if t]


def _build_input_for_page(ctx, page_idx, text_blocks, tables) -> TradeModuleInput:
    """Same C.2-established equivalent path as the sweep harness."""
    page_ctx = ctx.pages.get(page_idx)
    page_type = "UNKNOWN"
    page_legends: list = []
    page_zones: list = []
    if page_ctx is not None:
        pt = getattr(page_ctx, "page_type", None)
        page_type = getattr(pt, "value", str(pt)) if pt is not None else "UNKNOWN"
        page_legends = list(page_ctx.legends or [])
        page_zones = list(page_ctx.zones or [])
    project_scope = getattr(ctx, "project_scope", None)

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
        tables=tables if tables else None,
        project_scope=project_scope,
        page_number=page_idx,
    )


def _output_to_dict(out: TradeModuleOutput) -> dict:
    fields_dict = {}
    for k, v in (out.fields or {}).items():
        if is_dataclass(v):
            fields_dict[k] = asdict(v)
        else:
            fields_dict[k] = v
    return {
        "fields": fields_dict,
        "warnings": list(out.warnings or []),
        "equipment_pins": list(out.equipment_pins or []),
        "glazing_items": list(out.glazing_items) if out.glazing_items is not None else None,
        "door_items": list(out.door_items) if out.door_items is not None else None,
        "storefront_items": list(out.storefront_items) if out.storefront_items is not None else None,
    }


# ---------------------------------------------------------------------------
# Timing
# ---------------------------------------------------------------------------

def _time_n(label: str, fn, repeats: int = REPEATS) -> dict:
    """Run `fn` N times, return min/median/max + the last result's value.
    Uses time.perf_counter (orders §5: not time.time()).
    """
    times: list[float] = []
    last_result = None
    for _ in range(repeats):
        t0 = time.perf_counter()
        last_result = fn()
        t1 = time.perf_counter()
        times.append(t1 - t0)
    return {
        "label": label,
        "min": min(times),
        "median": statistics.median(times),
        "max": max(times),
        "all": list(times),
        "last_result": last_result,
    }


# ---------------------------------------------------------------------------
# Per-page profiling
# ---------------------------------------------------------------------------

def profile_page(pdf, ctx, page_idx: int) -> dict:
    """Time the four operations on a single page. Returns a dict with
    timings + the last module outputs (for §4 of the report).
    """
    pdf_page = pdf.pages[page_idx]

    # Operation 1: pdfplumber text extraction
    text_t = _time_n(
        "pdfplumber_text_extraction",
        lambda: _extract_text_blocks(pdf_page),
    )

    # Operation 2: pdfplumber table extraction
    table_t = _time_n(
        "pdfplumber_table_extraction",
        lambda: _extract_tables(pdf_page),
    )

    # Build the TradeModuleInput once (use the last text/table results)
    last_text = text_t["last_result"]
    last_tables = table_t["last_result"]
    tinput = _build_input_for_page(ctx, page_idx, last_text, last_tables)

    # Operation 3: RoofingModule.analyze
    roof_mod = RoofingModule()
    roof_t = _time_n(
        "roofing_module_analyze",
        lambda: roof_mod.analyze(tinput),
    )

    # Operation 4: GlazingModule.analyze
    glaz_mod = GlazingModule()
    glaz_t = _time_n(
        "glazing_module_analyze",
        lambda: glaz_mod.analyze(tinput),
    )

    return {
        "page_idx": page_idx,
        "text_blocks_count": len(last_text) if last_text else 0,
        "tables_count": len(last_tables) if last_tables else 0,
        "timings": {
            "text": text_t,
            "table": table_t,
            "roofing": roof_t,
            "glazing": glaz_t,
        },
        "roofing_output": _output_to_dict(roof_t["last_result"]),
        "glazing_output": _output_to_dict(glaz_t["last_result"]),
    }


# ---------------------------------------------------------------------------
# Debug cross-reference
# ---------------------------------------------------------------------------

def debug_xref(debug, page_idx: int) -> dict:
    """Pull section 1 (overall, not per-page; included for context) plus
    section 3's per-page entry plus section 6's legends attributed to this
    page. Returns a dict ready for serialization.
    """
    # Section 3: page_intelligence is a list of per-page dicts; find ours.
    sec3 = None
    if isinstance(debug.page_intelligence, list):
        for entry in debug.page_intelligence:
            if entry.get("page") == page_idx:
                sec3 = entry
                break

    # Section 6: legend_contents is list[dict] with "page" field per legend.
    sec6_legends = []
    if isinstance(debug.legend_contents, list):
        sec6_legends = [
            leg for leg in debug.legend_contents
            if leg.get("page") == page_idx
        ]

    # Section 6: quality_flags is bidset-wide list of strings; we attach
    # the full list per page (it's not page-attributed in the C.5 port).
    sec6_flags = list(debug.legend_quality_flags or [])

    return {
        "section_1_dispatch_health_overall": dict(debug.dispatch_health or {}),
        "section_3_page_intelligence_entry": sec3,
        "section_6_legends_for_this_page": sec6_legends,
        "section_6_quality_flags_bidset_wide": sec6_flags,
    }


# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------

def _fmt_seconds(s: float) -> str:
    if s >= 1.0:
        return f"{s:.3f}s"
    if s >= 0.001:
        return f"{s * 1000:.2f}ms"
    return f"{s * 1_000_000:.0f}µs"


def _safe_ratio(a: float, b: float) -> str:
    if b <= 0:
        return "n/a"
    return f"{a / b:.2f}×"


def format_report(*, dispatch_time_s: float, ctx, debug,
                  high_profile: dict, low_profile: dict,
                  high_xref: dict, low_xref: dict) -> str:
    h = high_profile
    l = low_profile

    def med(p, op):
        return p["timings"][op]["median"]

    def rng(p, op):
        return f"{_fmt_seconds(p['timings'][op]['min'])}–{_fmt_seconds(p['timings'][op]['max'])}"

    high_total = med(h, "text") + med(h, "table") + med(h, "roofing") + med(h, "glazing")
    low_total = med(l, "text") + med(l, "table") + med(l, "roofing") + med(l, "glazing")

    lines: list[str] = []
    a = lines.append

    a("# Profile Diagnostic — Bearss Ave")
    a("")
    a("**Date:** 2026-04-29")
    a("**Phase:** Profile diagnostic + housekeeping")
    a(f"**Bidset:** Bearss Ave Distribution Center — University — Marcobay Construction (3)")
    a(f"**PDF:** `{PDF_PATH}`")
    a(f"**Page count:** {SWEEP_REFERENCE_PAGES}")
    a(f"**Sweep wall-clock reference:** {SWEEP_REFERENCE_MODULES_S}s modules / "
      f"{SWEEP_REFERENCE_DISPATCH_S}s dispatch (per `SWEEP_OBSERVATION_bearss-ave.md`)")
    a("")
    a("**Type of artifact:** observation only. No grading, no fix lists, no "
      "tuning recommendations, no extractor-alternative benchmarks. Times the "
      "existing stack (pdfplumber + RoofingModule + GlazingModule + "
      "debug_module sections 1/3/6) on two debug-driven target pages. The "
      "vault rule is active on all five vault-ruled modules per CLAUDE.md §3 "
      "Decision 15; this run modified zero `backend/core/` files.")
    a("")
    a("---")
    a("")

    # ----- §1 page selection rationale -----
    a("## §1 — Page Selection Rationale")
    a("")
    a(f"**High-content page:** {HIGH_PAGE}")
    a("")
    a(PAGE_SELECTION[HIGH_PAGE]["rationale"])
    a("")
    a(f"**Low-content page:** {LOW_PAGE}")
    a("")
    a(PAGE_SELECTION[LOW_PAGE]["rationale"])
    a("")
    a("Page selection was driven by debug section 3 (page_intelligence) "
      "signal density per `SWEEP_OBSERVATION_bearss-ave.md`. Combined "
      "signal proxy = `legend_count + zone_count + refs_in + refs_out`. "
      "Page 15 ranked highest among pages with mapped sheet identity "
      "(score 60); page 82 ranked among the lowest (score 3) and was "
      "selected as the section-3-unclassified counterpoint.")
    a("")

    # ----- §2 dispatch -----
    a("## §2 — Dispatch Timing (whole bidset)")
    a("")
    a(f"- run_dispatch wall-clock: `{dispatch_time_s:.2f}s`")
    a(f"- Reference from sweep (2026-04-28): `{SWEEP_REFERENCE_DISPATCH_S}s`")
    delta = dispatch_time_s - SWEEP_REFERENCE_DISPATCH_S
    delta_pct = (delta / SWEEP_REFERENCE_DISPATCH_S * 100.0) if SWEEP_REFERENCE_DISPATCH_S else 0.0
    a(f"- Delta vs sweep: `{delta:+.2f}s` (`{delta_pct:+.1f}%`)")
    a("")

    # ----- §3 per-page timing table -----
    a(f"## §3 — Per-Page Timing ({REPEATS} repeats; median in headline; range below)")
    a("")
    a(f"| Operation | Page {HIGH_PAGE} (high) | Page {LOW_PAGE} (low) | Ratio (high/low) |")
    a(f"|---|---:|---:|---:|")
    a(f"| pdfplumber text extraction | {_fmt_seconds(med(h, 'text'))} | {_fmt_seconds(med(l, 'text'))} | "
      f"{_safe_ratio(med(h, 'text'), med(l, 'text'))} |")
    a(f"| pdfplumber table extraction | {_fmt_seconds(med(h, 'table'))} | {_fmt_seconds(med(l, 'table'))} | "
      f"{_safe_ratio(med(h, 'table'), med(l, 'table'))} |")
    a(f"| RoofingModule.analyze | {_fmt_seconds(med(h, 'roofing'))} | {_fmt_seconds(med(l, 'roofing'))} | "
      f"{_safe_ratio(med(h, 'roofing'), med(l, 'roofing'))} |")
    a(f"| GlazingModule.analyze | {_fmt_seconds(med(h, 'glazing'))} | {_fmt_seconds(med(l, 'glazing'))} | "
      f"{_safe_ratio(med(h, 'glazing'), med(l, 'glazing'))} |")
    a(f"| **Total per-page (sum of medians)** | **{_fmt_seconds(high_total)}** | "
      f"**{_fmt_seconds(low_total)}** | **{_safe_ratio(high_total, low_total)}** |")
    a("")
    a("**Ranges (min–max across 3 repeats) for sanity-check:**")
    a("")
    a(f"- Page {HIGH_PAGE} text: {rng(h, 'text')}; table: {rng(h, 'table')}; "
      f"roofing: {rng(h, 'roofing')}; glazing: {rng(h, 'glazing')}.")
    a(f"- Page {LOW_PAGE} text: {rng(l, 'text')}; table: {rng(l, 'table')}; "
      f"roofing: {rng(l, 'roofing')}; glazing: {rng(l, 'glazing')}.")
    a("")
    a(f"**Per-page wall-clock budget vs sweep average:** sweep modules averaged "
      f"`{SWEEP_REFERENCE_MODULES_S / SWEEP_REFERENCE_PAGES:.2f}s/page` "
      f"across {SWEEP_REFERENCE_PAGES} pages × 2 modules + per-page text/table extraction. "
      f"This profile breaks that down on two specific pages.")
    a("")

    # ----- §4 module output -----
    a("## §4 — Module Output Summary")
    a("")
    for label, p in [("high-content", h), ("low-content", l)]:
        page_idx = p["page_idx"]
        a(f"### Page {page_idx} ({label})")
        a("")
        a(f"- pdfplumber text blocks extracted: `{p['text_blocks_count']}`")
        a(f"- pdfplumber tables extracted: `{p['tables_count']}`")
        ro = p["roofing_output"]
        a(f"- Roofing fields: `{len(ro.get('fields') or {})}`; "
          f"warnings: `{len(ro.get('warnings') or [])}`; "
          f"equipment_pins: `{len(ro.get('equipment_pins') or [])}`")
        go = p["glazing_output"]
        gi = go.get("glazing_items") or []
        di = go.get("door_items") or []
        si = go.get("storefront_items") or []
        a(f"- Glazing items: `{len(gi)} glazing` / `{len(di)} door` / "
          f"`{len(si)} storefront`")
        a("")

    # ----- §5 debug cross-reference -----
    a("## §5 — Debug Cross-Reference")
    a("")
    for label, p, xref in [
        ("high-content", h, high_xref),
        ("low-content", l, low_xref),
    ]:
        page_idx = p["page_idx"]
        a(f"### Page {page_idx} ({label})")
        a("")
        sec3 = xref.get("section_3_page_intelligence_entry")
        legs = xref.get("section_6_legends_for_this_page", [])
        flags = xref.get("section_6_quality_flags_bidset_wide", [])
        a("**Section 3 (page_intelligence) entry for this page:**")
        a("")
        a("```json")
        a(json.dumps(sec3, indent=2, default=str))
        a("```")
        a("")
        a(f"**Section 6 legends attributed to this page:** {len(legs)}")
        a("")
        if legs:
            a("```json")
            a(json.dumps(legs[:10], indent=2, default=str))
            if len(legs) > 10:
                a(f"// {len(legs) - 10} more legends truncated")
            a("```")
        else:
            a("(none)")
        a("")
        a(f"**Section 6 quality flags (bidset-wide; not page-attributed):** "
          f"{len(flags)} flags")
        if flags:
            a("")
            a("```json")
            a(json.dumps(flags, indent=2, default=str))
            a("```")
        a("")
    a("**Section 1 (dispatch_health, bidset-wide) for context:**")
    a("")
    a("```json")
    a(json.dumps(high_xref.get("section_1_dispatch_health_overall"), indent=2, default=str))
    a("```")
    a("")

    # ----- §6 observations -----
    a("## §6 — Observations (no fixes, no recommendations)")
    a("")

    text_ratio = _safe_ratio(med(h, "text"), med(l, "text"))
    table_ratio = _safe_ratio(med(h, "table"), med(l, "table"))
    roof_ratio = _safe_ratio(med(h, "roofing"), med(l, "roofing"))
    glaz_ratio = _safe_ratio(med(h, "glazing"), med(l, "glazing"))

    # Build mechanical observations from the data — no interpretation.
    a(f"- Observed: pdfplumber text extraction medians were `{_fmt_seconds(med(h, 'text'))}` "
      f"on page {HIGH_PAGE} (high-content) and `{_fmt_seconds(med(l, 'text'))}` on "
      f"page {LOW_PAGE} (low-content); ratio {text_ratio}.")
    a(f"- Observed: pdfplumber table extraction medians were `{_fmt_seconds(med(h, 'table'))}` "
      f"on page {HIGH_PAGE} and `{_fmt_seconds(med(l, 'table'))}` on page {LOW_PAGE}; "
      f"ratio {table_ratio}.")
    a(f"- Observed: RoofingModule.analyze medians were `{_fmt_seconds(med(h, 'roofing'))}` on page "
      f"{HIGH_PAGE} and `{_fmt_seconds(med(l, 'roofing'))}` on page {LOW_PAGE}; ratio {roof_ratio}.")
    a(f"- Observed: GlazingModule.analyze medians were `{_fmt_seconds(med(h, 'glazing'))}` on page "
      f"{HIGH_PAGE} and `{_fmt_seconds(med(l, 'glazing'))}` on page {LOW_PAGE}; ratio {glaz_ratio}.")
    a(f"- Observed: per-page total (sum of four operation medians) was "
      f"`{_fmt_seconds(high_total)}` on page {HIGH_PAGE} and `{_fmt_seconds(low_total)}` "
      f"on page {LOW_PAGE}; per-page ratio "
      f"{_safe_ratio(high_total, low_total)}. Sweep-average per-page was "
      f"`{SWEEP_REFERENCE_MODULES_S / SWEEP_REFERENCE_PAGES:.2f}s` (modules only across "
      f"{SWEEP_REFERENCE_PAGES} pages; this profile additionally captures pdfplumber).")

    # Per-operation dominance per page (mechanical: which op had largest median)
    def dominant_op(p):
        ts = p["timings"]
        ranked = sorted(
            [(op, ts[op]["median"]) for op in ("text", "table", "roofing", "glazing")],
            key=lambda x: x[1], reverse=True,
        )
        return ranked

    h_dom = dominant_op(h)
    l_dom = dominant_op(l)
    a(f"- Observed: on page {HIGH_PAGE} (high), the largest-median operation was "
      f"`{h_dom[0][0]}` at `{_fmt_seconds(h_dom[0][1])}`; second was `{h_dom[1][0]}` "
      f"at `{_fmt_seconds(h_dom[1][1])}`. On page {LOW_PAGE} (low), the largest-median "
      f"operation was `{l_dom[0][0]}` at `{_fmt_seconds(l_dom[0][1])}`; second was "
      f"`{l_dom[1][0]}` at `{_fmt_seconds(l_dom[1][1])}`.")

    # Cross-reference observation: how informative was section 3?
    high_sec3 = high_xref.get("section_3_page_intelligence_entry") or {}
    low_sec3 = low_xref.get("section_3_page_intelligence_entry") or {}
    a(f"- Observed: debug section 3's per-page entry for page {HIGH_PAGE} reported "
      f"type=`{high_sec3.get('type')}`, confidence=`{high_sec3.get('confidence')}`, "
      f"legend_count=`{high_sec3.get('legend_count')}`, "
      f"zone_count=`{high_sec3.get('zone_count')}`, "
      f"refs_out=`{high_sec3.get('refs_out')}`, refs_in=`{high_sec3.get('refs_in')}`. "
      f"For page {LOW_PAGE} it reported type=`{low_sec3.get('type')}`, "
      f"confidence=`{low_sec3.get('confidence')}`, "
      f"legend_count=`{low_sec3.get('legend_count')}`, "
      f"zone_count=`{low_sec3.get('zone_count')}`, "
      f"refs_out=`{low_sec3.get('refs_out')}`, refs_in=`{low_sec3.get('refs_in')}`.")

    a("")
    # Closing one-sentence on debug-section-3 utility for page picking.
    a("Closing observation on page-selection utility of debug section 3: "
      "the per-page combined signal proxy "
      "(`legend_count + zone_count + refs_in + refs_out`) ordered the bidset's pages "
      "from a 60-point top to a 1-point bottom, with `confidence=0.0` distinguishing "
      "the unclassified low-end pages from low-but-confidently-classified pages — "
      f"sufficient to drive this run's high (page {HIGH_PAGE}) / low (page {LOW_PAGE}) "
      f"selection without guessing.")
    a("")

    # ----- §7 closing -----
    a("## §7 — Closing")
    a("")
    a("Diagnostic only. Profile data feeds the future planning conversation "
      "about Path (a) module tuning vs (b) C.4 design vs other directions. "
      "No tuning was performed. No fixes were attempted. The roofing "
      "module, glazing module, and debug module are vault-ruled per "
      "CLAUDE.md §3 Decision 15. The `backend/scripts/profile_diagnostic.py` "
      "harness is tracked (commit 1 of this phase) and reusable for future "
      "profile diagnostics on other bidsets.")
    a("")
    a("---")
    a("")
    a("**End of report.**")
    a("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not PDF_PATH.exists():
        print(f"ERROR: PDF not found at {PDF_PATH}", file=sys.stderr)
        sys.exit(3)

    print(f"PDF: {PDF_PATH}", flush=True)
    print(f"High-content target page: {HIGH_PAGE}", flush=True)
    print(f"Low-content target page:  {LOW_PAGE}", flush=True)
    print(f"Repeats per measurement:  {REPEATS}", flush=True)
    print("", flush=True)

    # Dispatch
    print("Running run_dispatch...", flush=True)
    t0 = time.perf_counter()
    try:
        ctx = run_dispatch(str(PDF_PATH), storage=None)
    except Exception:
        print("DISPATCH RAISED — §7 stop:", file=sys.stderr)
        traceback.print_exc()
        sys.exit(4)
    dispatch_time = time.perf_counter() - t0
    print(f"Dispatch complete in {dispatch_time:.2f}s", flush=True)

    # Profile both pages with a single pdfplumber session
    print("Profiling pages...", flush=True)
    with pdfplumber.open(str(PDF_PATH)) as pdf:
        # Bound-check page indexes
        for p in (HIGH_PAGE, LOW_PAGE):
            if p < 0 or p >= len(pdf.pages):
                print(f"§7 stop: page {p} out of bounds (PDF has {len(pdf.pages)} pages)",
                      file=sys.stderr)
                sys.exit(5)

        try:
            high_profile = profile_page(pdf, ctx, HIGH_PAGE)
        except Exception:
            print(f"Module raised on high-content page {HIGH_PAGE} — §7 stop:", file=sys.stderr)
            traceback.print_exc()
            sys.exit(5)

        try:
            low_profile = profile_page(pdf, ctx, LOW_PAGE)
        except Exception:
            print(f"Module raised on low-content page {LOW_PAGE} — §7 stop:", file=sys.stderr)
            traceback.print_exc()
            sys.exit(5)

    print(f"Page {HIGH_PAGE} (high) text_blocks={high_profile['text_blocks_count']}, "
          f"tables={high_profile['tables_count']}", flush=True)
    print(f"Page {LOW_PAGE} (low)  text_blocks={low_profile['text_blocks_count']}, "
          f"tables={low_profile['tables_count']}", flush=True)

    # Run debug for cross-reference
    print("Running run_debug for cross-reference...", flush=True)
    try:
        debug = run_debug(ctx)
    except Exception:
        print("run_debug RAISED — §7 stop:", file=sys.stderr)
        traceback.print_exc()
        sys.exit(6)

    high_xref = debug_xref(debug, HIGH_PAGE)
    low_xref = debug_xref(debug, LOW_PAGE)

    # Format and write report
    print(f"Writing report to {OUTPUT_PATH}...", flush=True)
    report = format_report(
        dispatch_time_s=dispatch_time,
        ctx=ctx,
        debug=debug,
        high_profile=high_profile,
        low_profile=low_profile,
        high_xref=high_xref,
        low_xref=low_xref,
    )
    OUTPUT_PATH.write_text(report, encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH} ({OUTPUT_PATH.stat().st_size} bytes)", flush=True)

    # Console summary
    print("", flush=True)
    print("=== Profile summary ===", flush=True)
    for label, p in [("high", high_profile), ("low", low_profile)]:
        ts = p["timings"]
        print(f"  page {p['page_idx']} ({label}):", flush=True)
        for op in ("text", "table", "roofing", "glazing"):
            d = ts[op]
            print(f"    {op:10s} median={d['median']*1000:8.2f}ms  "
                  f"min={d['min']*1000:8.2f}ms  max={d['max']*1000:8.2f}ms", flush=True)


if __name__ == "__main__":
    main()
