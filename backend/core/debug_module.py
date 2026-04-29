"""
Debug Module — first trade_contexts plugin.

Developer diagnostic tool. Registers as trade_contexts["debug"].
Reads PlanSetContext and geometry results, produces a structured
diagnostic report. No mutations — read-only.

6 diagnostic sections:
  1. Dispatch Health — filter completion, warnings, timing
  2. Scale Comparison — dispatch scale vs geometry scale per page
  3. Page Intelligence — page classification table
  4. Cross-Reference Graph — resolution summary + unresolved list
  5. Geometry Diagnostics — polygon, area, perimeter, confidence
  6. Legend Contents — all legends with entry counts + quality flags

VAULT CONSTRAINT: This module must NOT be modified in the same session
that modifies core/ files. Debug enhancements require a separate session
with core/ frozen.

Usage:
    python -m modules.debug.debug_module path/to/plan.pdf [page_num]

---

Huckleberry Phase C.5 partial port (2026-04-28)
================================================

Sections 1 (dispatch health), 3 (page intelligence), 6 (legend contents +
quality flags) are ported VERBATIM from the TracePoint source — they read
public PlanSetContext fields that exist unchanged in Huckleberry's
`backend/core/context.py`.

Sections 2 (scale comparison), 4 (cross-reference graph), 5 (geometry
diagnostics) are STUBBED — they return a `{"stub_marker": ..., "reason":
...}` dict pending external state Huckleberry does not yet have:

  - Section 2: a scale-engine output route (Phase D/E)
  - Section 4: networkx + sheet-index parsing (deliberately not added as
              a dependency this session)
  - Section 5: geometry_results from the Stages 6-9 geometry route
              (Phase D/E)

The vault rule applies to all six sections, stubbed and ported alike.
Tuning of sections 1/3/6 happens in dedicated sessions with `core/`
frozen. Unstubbing of sections 2/4/5 is a future phase decision.

See `backend/DEBUG_MODULE_REPORT.md` for the full spec report and
`MARCH_ORDERS_C_5_debug_port.md` for the port's authoritative scope.

Source SHA-1 (TracePoint, verified at port time):
    b5a4cf93ca7c02116fc00f6dc5a1514da1b18b60
"""

DEBUG_MODULE_VERSION = "1.1.0"  # vault version after cleanup

import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# C.5 port: was "parent.parent.parent" in TracePoint source (TracePoint root
# = tracepoint_port/TracePoint/, three levels up from modules/debug/). In
# Huckleberry this file lives at backend/core/debug_module.py, so two levels
# up is the package root (backend/) which is what `from core.*` expects.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Optional library
try:
    import networkx as _nx
except ImportError:
    _nx = None

from core.context import (
    PlanSetContext, TradeContext, PageContext,
    Discipline, PageType,
    CONFIDENCE_EXPLICIT, CONFIDENCE_STRONG, CONFIDENCE_INFERRED,
    CONFIDENCE_WEAK, CONFIDENCE_UNKNOWN,
)


# ============================================================
# Debug Trade Context
# ============================================================

@dataclass
class DebugContext(TradeContext):
    """Debug diagnostic context. Extends TradeContext for registry."""
    dispatch_health: dict = field(default_factory=dict)
    scale_comparison: list = field(default_factory=list)
    page_intelligence: list = field(default_factory=list)
    crossref_summary: dict = field(default_factory=dict)
    geometry_diagnostics: dict = field(default_factory=dict)
    legend_contents: list = field(default_factory=list)
    legend_quality_flags: list = field(default_factory=list)


# ============================================================
# Legend Quality Flags
# ============================================================

def _check_legend_quality(ctx: PlanSetContext) -> list[str]:
    """Flag suspicious legend data. Returns list of warning strings."""
    flags = []
    total = len(ctx.all_legends)

    if total > 100:
        flags.append(
            f"WARNING: unusually high legend count ({total}) — "
            f"possible pdfplumber noise"
        )

    # Per-page check
    page_counts: dict[int, int] = {}
    for legend in ctx.all_legends:
        page_counts[legend.page_index] = page_counts.get(legend.page_index, 0) + 1
    for page_idx, count in sorted(page_counts.items()):
        if count > 10:
            flags.append(
                f"WARNING: page {page_idx} has {count} legends — "
                f"review for duplicates or noise"
            )

    # Source breakdown
    text_count = 0
    pdfplumber_count = 0
    for legend in ctx.all_legends:
        if legend.source_tag and "pdfplumber" in legend.source_tag.evidence:
            pdfplumber_count += 1
        else:
            text_count += 1
    if pdfplumber_count > 0:
        flags.append(
            f"Legend sources: {text_count} text-based, "
            f"{pdfplumber_count} pdfplumber"
        )

    return flags


# ============================================================
# Diagnostic Sections
# ============================================================

def _section_dispatch_health(ctx: PlanSetContext) -> dict:
    """Section 1: Dispatch health — filter completion, warnings, timing."""
    return {
        "dispatch_complete": ctx.dispatch_complete,
        "filters_completed": ctx.filters_completed,
        "filter_count": len(ctx.filters_completed),
        "warnings": ctx.dispatch_warnings,
        "warning_count": len(ctx.dispatch_warnings),
        "timestamp": ctx.dispatch_timestamp,
        "total_pages": ctx.total_pages,
        "sheet_map_source": ctx.sheet_map_source,
        "sheet_count": len(ctx.sheet_map),
        "mapped_pages": len(ctx.page_to_sheet),
    }


def _section_scale_comparison(ctx: PlanSetContext, geometry_results: dict = None) -> list:
    """Section 2: Scale comparison — dispatch scale vs geometry scale per page.

    C.5 STUB: pending the scale-engine output route. Deferred to Phase D/E
    per `backend/DEBUG_MODULE_REPORT.md`. The function name and signature
    are preserved so future-phase unstubbing is a body-only edit.
    """
    return {
        "stub_marker": "C.5_partial_port_pending_scale_engine_route",
        "reason": "Scale comparison requires the scale-engine output route; deferred to Phase D/E per DEBUG_MODULE_REPORT.md.",
    }


def _section_page_intelligence(ctx: PlanSetContext) -> list:
    """Section 3: Page intelligence — page classification table."""
    rows = []
    for page_idx in sorted(ctx.pages.keys()):
        pc = ctx.pages[page_idx]
        rows.append({
            "page": page_idx,
            "sheet": pc.sheet_number or "---",
            "title": pc.title or "---",
            "discipline": pc.discipline.value,
            "type": pc.page_type.value,
            "confidence": pc.confidence,
            "has_drawing": pc.has_drawing_area,
            "has_title_block": pc.has_title_block,
            "has_details": pc.has_details,
            "has_legend": pc.has_legend,
            "detail_count": pc.detail_count,
            "zone_count": len(pc.zones),
            "legend_count": len(pc.legends),
            "refs_out": len(pc.cross_refs_out),
            "refs_in": len(pc.cross_refs_in),
        })
    return rows


def _section_crossref_graph(ctx: PlanSetContext) -> dict:
    """Section 4: Cross-reference graph — resolution summary + unresolved list.

    C.5 STUB: pending networkx (deliberately NOT added as a dependency in
    this session) and sheet-index parsing decisions. Deferred per
    `backend/DEBUG_MODULE_REPORT.md`. The function name and signature are
    preserved so future-phase unstubbing is a body-only edit.
    """
    return {
        "stub_marker": "C.5_partial_port_pending_networkx_and_sheet_index",
        "reason": "Cross-reference graph requires networkx + sheet-index parsing; deferred per DEBUG_MODULE_REPORT.md.",
    }


def _section_geometry_diagnostics(ctx: PlanSetContext, geometry_results: dict = None) -> dict:
    """Section 5: Geometry diagnostics — polygon, area, perimeter, confidence.

    C.5 STUB: pending geometry_results from Stages 6-9. The optional
    `geometry_results` parameter on `run_debug()` is preserved; the stub
    ignores it. Deferred per `backend/DEBUG_MODULE_REPORT.md`. The
    function name and signature are preserved so future-phase unstubbing
    is a body-only edit.
    """
    return {
        "stub_marker": "C.5_partial_port_pending_geometry_results",
        "reason": "Geometry diagnostics requires geometry_results from Stages 6-9; deferred per DEBUG_MODULE_REPORT.md.",
    }


def _section_legend_contents(ctx: PlanSetContext) -> list:
    """Section 6: Legend contents — all legends with entry counts."""
    legends = []
    for legend in ctx.all_legends:
        entries = []
        for e in legend.entries[:10]:
            entries.append({"key": e.key, "desc": e.description[:80]})
        legends.append({
            "type": legend.legend_type,
            "title": legend.title,
            "page": legend.page_index,
            "entry_count": legend.entry_count,
            "confidence": legend.confidence,
            "source": legend.source_tag.evidence if legend.source_tag else "unknown",
            "entries_sample": entries,
        })
    return legends


# ============================================================
# Main entry point
# ============================================================

def run_debug(ctx: PlanSetContext, geometry_results: dict = None) -> DebugContext:
    """
    Run all 6 diagnostic sections and return a DebugContext.
    Registers itself in ctx.trade_contexts["debug"].

    Args:
        ctx: PlanSetContext from dispatch gate
        geometry_results: optional dict of {page_idx: geometry_result_dict}
    """
    debug = DebugContext(
        trade_id="debug",
        trade_name="Debug Diagnostics",
        scope_summary=f"Developer diagnostic module v{DEBUG_MODULE_VERSION} — 6 sections",
        relevant_pages=list(ctx.pages.keys()),
    )

    debug.dispatch_health = _section_dispatch_health(ctx)
    debug.scale_comparison = _section_scale_comparison(ctx, geometry_results)
    debug.page_intelligence = _section_page_intelligence(ctx)
    debug.crossref_summary = _section_crossref_graph(ctx)
    debug.geometry_diagnostics = _section_geometry_diagnostics(ctx, geometry_results)
    debug.legend_contents = _section_legend_contents(ctx)
    debug.legend_quality_flags = _check_legend_quality(ctx)

    # Register in trade_contexts
    ctx.trade_contexts["debug"] = debug
    return debug


# ============================================================
# CLI Report
# ============================================================

def _safe_print(text):
    """Print with Windows CP1252 fallback."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", "replace").decode("ascii"))


def print_report(debug: DebugContext):
    """Print formatted diagnostic report to stdout."""
    _safe_print(f"\n{'='*75}")
    _safe_print(f"  DEBUG DIAGNOSTIC REPORT  (v{DEBUG_MODULE_VERSION})")
    _safe_print(f"{'='*75}")

    # Section 1: Dispatch Health
    h = debug.dispatch_health
    _safe_print(f"\n  1. DISPATCH HEALTH")
    _safe_print(f"  {'-'*40}")
    _safe_print(f"  Complete:      {h['dispatch_complete']}")
    _safe_print(f"  Filters:       {h['filter_count']} ({', '.join(h['filters_completed'])})")
    _safe_print(f"  Warnings:      {h['warning_count']}")
    for w in h["warnings"]:
        _safe_print(f"    - {w}")
    _safe_print(f"  Total pages:   {h['total_pages']}")
    _safe_print(f"  Sheet source:  {h['sheet_map_source']}")
    _safe_print(f"  Sheets found:  {h['sheet_count']}")
    _safe_print(f"  Pages mapped:  {h['mapped_pages']}")

    # Section 2: Scale Comparison
    _safe_print(f"\n  2. SCALE COMPARISON")
    _safe_print(f"  {'-'*40}")
    if debug.scale_comparison:
        _safe_print(f"  {'Page':>4} {'Sheet':<8} {'Type':<14} {'D.fpi':>6} {'D.conf':>6} {'G.fpi':>6} {'G.meth':<12} {'Match'}")
        for r in debug.scale_comparison:
            d_fpi = f"{r['dispatch_fpi']:.1f}" if r['dispatch_fpi'] else "---"
            d_conf = f"{r['dispatch_conf']:.1f}" if r['dispatch_conf'] is not None else "---"
            g_fpi = f"{r['geo_fpi']:.1f}" if r['geo_fpi'] else "---"
            g_meth = r['geo_method'] or "---"
            match = "YES" if r['match'] is True else ("NO" if r['match'] is False else "---")
            _safe_print(f"  {r['page']:>4} {r['sheet']:<8} {r['type']:<14} {d_fpi:>6} {d_conf:>6} {g_fpi:>6} {g_meth:<12} {match}")
    else:
        _safe_print(f"  (no pages)")

    # Section 3: Page Intelligence
    _safe_print(f"\n  3. PAGE INTELLIGENCE")
    _safe_print(f"  {'-'*40}")
    if debug.page_intelligence:
        _safe_print(f"  {'Page':>4} {'Sheet':<8} {'Disc':>4} {'Type':<14} {'Conf':>5} {'Zones':>5} {'Legs':>4} {'Refs':>4} {'Title'}")
        for r in debug.page_intelligence:
            title = (r['title'][:30] + "..") if len(r['title']) > 32 else r['title']
            _safe_print(f"  {r['page']:>4} {r['sheet']:<8} {r['discipline']:>4} {r['type']:<14} {r['confidence']:>5.1f} {r['zone_count']:>5} {r['legend_count']:>4} {r['refs_out']:>4} {title}")
    else:
        _safe_print(f"  (no pages)")

    # Section 4: Cross-Reference Graph
    _safe_print(f"\n  4. CROSS-REFERENCE GRAPH")
    _safe_print(f"  {'-'*40}")
    cr = debug.crossref_summary
    _safe_print(f"  Total refs:    {cr['total_refs']}")
    _safe_print(f"  Resolved:      {cr['resolved']}")
    _safe_print(f"  Unresolved:    {cr['unresolved']}")
    _safe_print(f"  Resolution:    {cr['resolution_rate']:.0%}")
    if cr["by_type"]:
        _safe_print(f"  By type:")
        for t, counts in cr["by_type"].items():
            _safe_print(f"    {t:<15} {counts['resolved']}/{counts['total']}")
    if cr["unresolved_sample"]:
        _safe_print(f"  Unresolved sample:")
        for u in cr["unresolved_sample"][:10]:
            _safe_print(f"    [{u['type']}] p{u['source_page']} -> {u['target_sheet'] or '?'}: {u['text']}")
    if cr.get("graph"):
        g = cr["graph"]
        _safe_print(f"  Graph analysis (networkx):")
        _safe_print(f"    Nodes: {g.get('nodes', 0)}  Edges: {g.get('edges', 0)}")
        _safe_print(f"    Components: {g.get('connected_components', 0)}  Isolated: {g.get('isolated_pages', 0)}")
        if g.get("most_referenced"):
            top = ", ".join(f"p{p}({d})" for p, d in g["most_referenced"])
            _safe_print(f"    Most referenced: {top}")
        if g.get("most_referencing"):
            top = ", ".join(f"p{p}({d})" for p, d in g["most_referencing"])
            _safe_print(f"    Most referencing: {top}")

    # Section 5: Geometry Diagnostics
    _safe_print(f"\n  5. GEOMETRY DIAGNOSTICS")
    _safe_print(f"  {'-'*40}")
    gd = debug.geometry_diagnostics
    if not gd.get("available", False):
        _safe_print(f"  {gd.get('note', 'Not available')}")
    else:
        for page_idx, info in gd["pages"].items():
            _safe_print(f"  Page {page_idx}:")
            _safe_print(f"    Area:       {info['area_sqft']} SF")
            _safe_print(f"    Perimeter:  {info['perimeter_ft']} LF")
            _safe_print(f"    Scale:      {info['ft_per_inch']} fpi ({info['scale_method']})")
            _safe_print(f"    Source:     {info['source']}")
            _safe_print(f"    Confidence: {info['confidence']}")

    # Section 6: Legend Contents
    _safe_print(f"\n  6. LEGEND CONTENTS ({len(debug.legend_contents)} legends)")
    _safe_print(f"  {'-'*40}")

    # Quality flags first
    if debug.legend_quality_flags:
        for flag in debug.legend_quality_flags:
            _safe_print(f"  ** {flag}")
        _safe_print(f"")

    for leg in debug.legend_contents:
        source = leg.get("source", "unknown")
        _safe_print(f"  [{leg['type']}] {leg['title']} (p{leg['page']}, {leg['entry_count']} entries, conf={leg['confidence']:.1f}, src={source})")
        for e in leg["entries_sample"][:5]:
            _safe_print(f"    {e['key']}: {e['desc']}")
        if leg["entry_count"] > 5:
            _safe_print(f"    ... ({leg['entry_count'] - 5} more)")

    _safe_print(f"\n{'='*75}\n")


# ============================================================
# CLI — uses ONLY public interfaces (run_dispatch, run_debug)
# ============================================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m modules.debug.debug_module <pdf_path> [page_num]")
        sys.exit(1)

    pdf_path = Path(sys.argv[1])
    page_num = int(sys.argv[2]) if len(sys.argv) > 2 else None

    from core.dispatch_gate import run_dispatch

    _safe_print(f"  Debug Module v{DEBUG_MODULE_VERSION}")
    _safe_print(f"  Running dispatch on {pdf_path.name}...")
    t0 = time.time()
    ctx = run_dispatch(pdf_path)
    t_dispatch = time.time() - t0
    _safe_print(f"  Dispatch complete in {t_dispatch:.1f}s")

    # Geometry results are passed in by the caller (e.g. geometry route).
    # The CLI runs dispatch-only diagnostics. To include geometry,
    # use the debug module programmatically via run_debug(ctx, geo_results).
    geometry_results = {}

    debug = run_debug(ctx, geometry_results)
    print_report(debug)
