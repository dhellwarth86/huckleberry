"""C.5 bidset run-through verification (one-shot, not committed as a test).

Loads the chosen bidset PDF, runs dispatch + run_debug, writes a
structured markdown artifact to backend/C5_DEBUG_RUN_THROUGH_<bidset>.md.

Per MARCH_ORDERS_C_5_debug_port.md Section 5. Verification artifact only —
NOT a regression suite addition.
"""
from __future__ import annotations

import json
import sys
import time
import traceback
from dataclasses import asdict, fields, is_dataclass
from pathlib import Path

# Make the backend package importable when this script runs from repo root
HERE = Path(__file__).resolve()
BACKEND = HERE.parent.parent  # backend/
sys.path.insert(0, str(BACKEND))

from core.dispatch_gate import run_dispatch  # noqa: E402
from core.debug_module import run_debug  # noqa: E402


PDF_PATH = Path(r"C:\huck stage 2\full bid sets\Taco Bell - Weeki Wachee - Compass Construction Management (2).pdf")
BIDSET_NAME = "taco-bell-weeki-wachee-compass-construction-management-2"
OUTPUT_PATH = BACKEND / f"C5_DEBUG_RUN_THROUGH_{BIDSET_NAME}.md"


def _serialize_for_md(obj, max_items=50):
    """Pretty-serialize a debug-module section result for markdown embedding.

    Truncates long lists at max_items per section to keep the artifact
    readable without losing the shape.
    """
    if obj is None:
        return "null"
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            out[k] = _serialize_for_md(v, max_items)
        return out
    if isinstance(obj, list):
        if len(obj) > max_items:
            head = [_serialize_for_md(x, max_items) for x in obj[:max_items]]
            return head + [f"... ({len(obj) - max_items} more items truncated for artifact readability)"]
        return [_serialize_for_md(x, max_items) for x in obj]
    if hasattr(obj, "value") and hasattr(obj, "name"):
        # Enum
        return obj.value
    if is_dataclass(obj):
        try:
            return _serialize_for_md(asdict(obj), max_items)
        except Exception:
            return str(obj)
    return obj


def main():
    if not PDF_PATH.exists():
        print(f"ERROR: PDF not found at {PDF_PATH}", file=sys.stderr)
        sys.exit(2)

    print(f"Running dispatch on {PDF_PATH.name}...", flush=True)
    t0 = time.time()
    try:
        ctx = run_dispatch(str(PDF_PATH), storage=None)
    except Exception:
        print("Dispatch raised:")
        traceback.print_exc()
        sys.exit(3)
    t_dispatch = time.time() - t0
    print(f"Dispatch complete in {t_dispatch:.1f}s", flush=True)

    print("Running run_debug(ctx)...", flush=True)
    t1 = time.time()
    try:
        debug = run_debug(ctx)
    except Exception:
        print("run_debug raised:")
        traceback.print_exc()
        sys.exit(4)
    t_debug = time.time() - t1
    print(f"run_debug complete in {t_debug:.1f}s", flush=True)

    # Pull a few dispatch-side facts that orders Section 5 verification calls out
    # explicitly (some live on ctx.project_scope, not in debug section 1).
    ps = ctx.project_scope
    detected_system = ps.detected_system if ps else None
    system_confidence = ps.system_confidence if ps else None
    scope_pages = list(ps.scope_pages) if ps else []

    # Debug section results (six sections + quality flags)
    sections = {
        "1_dispatch_health": _serialize_for_md(debug.dispatch_health),
        "2_scale_comparison": _serialize_for_md(debug.scale_comparison),
        "3_page_intelligence": _serialize_for_md(debug.page_intelligence, max_items=200),
        "4_crossref_summary": _serialize_for_md(debug.crossref_summary),
        "5_geometry_diagnostics": _serialize_for_md(debug.geometry_diagnostics),
        "6_legend_contents": _serialize_for_md(debug.legend_contents, max_items=80),
        "6_legend_quality_flags": _serialize_for_md(debug.legend_quality_flags),
    }

    # Per-section verification status
    section_2_stub_ok = (
        isinstance(debug.scale_comparison, dict)
        and debug.scale_comparison.get("stub_marker") == "C.5_partial_port_pending_scale_engine_route"
    )
    section_4_stub_ok = (
        isinstance(debug.crossref_summary, dict)
        and debug.crossref_summary.get("stub_marker") == "C.5_partial_port_pending_networkx_and_sheet_index"
    )
    section_5_stub_ok = (
        isinstance(debug.geometry_diagnostics, dict)
        and debug.geometry_diagnostics.get("stub_marker") == "C.5_partial_port_pending_geometry_results"
    )
    section_1_real_content = (
        isinstance(debug.dispatch_health, dict)
        and "dispatch_complete" in debug.dispatch_health
        and "stub_marker" not in debug.dispatch_health
    )
    section_3_real_shape = isinstance(debug.page_intelligence, list)
    section_3_has_pages = section_3_real_shape and len(debug.page_intelligence) > 0
    section_6_real_shape = isinstance(debug.legend_contents, list)
    section_6_has_content = section_6_real_shape and len(debug.legend_contents) > 0
    section_6_quality_flags_emitted = isinstance(debug.legend_quality_flags, list)

    # scope_pages explicit Taco-Bell expectation (orders Section 5)
    scope_pages_includes_18_or_19 = bool(scope_pages and (18 in scope_pages or 19 in scope_pages))
    detected_system_present_in_planset = (ps is not None) and ("detected_system" in ps.__dataclass_fields__) if ps else (ps is not None)

    md_lines = []
    md_lines.append(f"# C.5 Debug Module — Bidset Run-Through Verification")
    md_lines.append("")
    md_lines.append(f"**Bidset:** Taco Bell — Weeki Wachee — Compass Construction Management (2)")
    md_lines.append(f"**PDF:** `{PDF_PATH}`")
    md_lines.append(f"**Bidset key:** `{BIDSET_NAME}`")
    md_lines.append(f"**Phase:** C.5 (debug module partial port)")
    md_lines.append(f"**Dispatch time:** {t_dispatch:.1f}s")
    md_lines.append(f"**run_debug time:** {t_debug:.1f}s")
    md_lines.append("")
    md_lines.append("**Type of artifact:** smoke verification that the partial port runs end-")
    md_lines.append("to-end against real input and produces real content for sections 1/3/6,")
    md_lines.append("and emits documented stub markers for sections 2/4/5.")
    md_lines.append("")
    md_lines.append("**NOT** calibration. **NOT** a sweep observation report. **NOT** an")
    md_lines.append("opportunity to tune sections 1/3/6 — vault rule active.")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")

    md_lines.append("## Verification status (per orders Section 5)")
    md_lines.append("")
    md_lines.append("| Item | Pass | Detail |")
    md_lines.append("|---|---|---|")
    md_lines.append(f"| Section 1 (dispatch_health): real content (not stub_marker) | {'YES' if section_1_real_content else 'NO'} | dispatch_complete = {debug.dispatch_health.get('dispatch_complete')}; filters_completed = {debug.dispatch_health.get('filters_completed')}; total_pages = {debug.dispatch_health.get('total_pages')}; sheet_count = {debug.dispatch_health.get('sheet_count')}; mapped_pages = {debug.dispatch_health.get('mapped_pages')} |")
    md_lines.append(f"| ctx.project_scope.detected_system field present | {'YES' if detected_system_present_in_planset else 'NO'} | value = {detected_system!r}; confidence = {system_confidence}; (orders Section 5: expected `\"tpo\"` with confidence ~0.95 for Taco Bell) |")
    md_lines.append(f"| ctx.project_scope.scope_pages includes 18 and/or 19 | {'YES' if scope_pages_includes_18_or_19 else 'NO'} | scope_pages = {scope_pages}; (orders Section 5: scope_pages should include page 18 and/or 19) |")
    md_lines.append(f"| Section 3 (page_intelligence): list shape | {'YES' if section_3_real_shape else 'NO'} | len = {len(debug.page_intelligence) if isinstance(debug.page_intelligence, list) else 'N/A'} |")
    md_lines.append(f"| Section 3: has at least one page entry | {'YES' if section_3_has_pages else 'NO'} | first page entry = {debug.page_intelligence[0] if section_3_has_pages else None} |")
    md_lines.append(f"| Section 6 (legend_contents): list shape | {'YES' if section_6_real_shape else 'NO'} | legend count = {len(debug.legend_contents) if isinstance(debug.legend_contents, list) else 'N/A'} |")
    md_lines.append(f"| Section 6: legend_quality_flags emitted (list type) | {'YES' if section_6_quality_flags_emitted else 'NO'} | flag count = {len(debug.legend_quality_flags) if isinstance(debug.legend_quality_flags, list) else 'N/A'} |")
    md_lines.append(f"| Section 2: stub_marker = C.5_partial_port_pending_scale_engine_route | {'YES' if section_2_stub_ok else 'NO'} | scale_comparison = {debug.scale_comparison} |")
    md_lines.append(f"| Section 4: stub_marker = C.5_partial_port_pending_networkx_and_sheet_index | {'YES' if section_4_stub_ok else 'NO'} | crossref_summary = {debug.crossref_summary} |")
    md_lines.append(f"| Section 5: stub_marker = C.5_partial_port_pending_geometry_results | {'YES' if section_5_stub_ok else 'NO'} | geometry_diagnostics = {debug.geometry_diagnostics} |")
    md_lines.append("")

    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## Section 1 — Dispatch Health (verbatim port)")
    md_lines.append("")
    md_lines.append("```json")
    md_lines.append(json.dumps(sections["1_dispatch_health"], indent=2, default=str))
    md_lines.append("```")
    md_lines.append("")

    md_lines.append("## Section 2 — Scale Comparison (C.5 stub)")
    md_lines.append("")
    md_lines.append("```json")
    md_lines.append(json.dumps(sections["2_scale_comparison"], indent=2, default=str))
    md_lines.append("```")
    md_lines.append("")

    md_lines.append("## Section 3 — Page Intelligence (verbatim port)")
    md_lines.append("")
    md_lines.append(f"Total page entries: {len(debug.page_intelligence) if isinstance(debug.page_intelligence, list) else 'N/A'}")
    md_lines.append("")
    md_lines.append("```json")
    md_lines.append(json.dumps(sections["3_page_intelligence"], indent=2, default=str))
    md_lines.append("```")
    md_lines.append("")

    md_lines.append("## Section 4 — Cross-Reference Graph (C.5 stub)")
    md_lines.append("")
    md_lines.append("```json")
    md_lines.append(json.dumps(sections["4_crossref_summary"], indent=2, default=str))
    md_lines.append("```")
    md_lines.append("")

    md_lines.append("## Section 5 — Geometry Diagnostics (C.5 stub)")
    md_lines.append("")
    md_lines.append("```json")
    md_lines.append(json.dumps(sections["5_geometry_diagnostics"], indent=2, default=str))
    md_lines.append("```")
    md_lines.append("")

    md_lines.append("## Section 6 — Legend Contents (verbatim port)")
    md_lines.append("")
    md_lines.append(f"Total legends: {len(debug.legend_contents) if isinstance(debug.legend_contents, list) else 'N/A'}")
    md_lines.append("")
    md_lines.append("### Legend quality flags")
    md_lines.append("")
    md_lines.append("```json")
    md_lines.append(json.dumps(sections["6_legend_quality_flags"], indent=2, default=str))
    md_lines.append("```")
    md_lines.append("")
    md_lines.append("### Legends sample")
    md_lines.append("")
    md_lines.append("```json")
    md_lines.append(json.dumps(sections["6_legend_contents"], indent=2, default=str))
    md_lines.append("```")
    md_lines.append("")

    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## Project-scope cross-check (dispatch output, not debug section)")
    md_lines.append("")
    md_lines.append("Reference for orders Section 5's `detected_system` and `scope_pages`")
    md_lines.append("expectations on Taco Bell. These fields live on `ctx.project_scope` —")
    md_lines.append("the debug module's section 1 reads dispatch-completion stats only and")
    md_lines.append("does NOT surface project_scope. Recorded here as a separate fact about")
    md_lines.append("the dispatch output for verification completeness.")
    md_lines.append("")
    if ps is None:
        md_lines.append("`ctx.project_scope` is None — no scope summary attached.")
    else:
        ps_dict = {
            "scope_pages": list(ps.scope_pages),
            "spec_sections": list(ps.spec_sections),
            "detected_system": ps.detected_system,
            "system_confidence": ps.system_confidence,
            "system_evidence": ps.system_evidence,
            "manufacturers": list(ps.manufacturers),
            "material_mentions": list(ps.material_mentions),
            "florida_signals": list(ps.florida_signals),
            "roof_shape_signal": ps.roof_shape_signal,
            "architect": ps.architect,
            "contractor": ps.contractor,
        }
        md_lines.append("```json")
        md_lines.append(json.dumps(ps_dict, indent=2, default=str))
        md_lines.append("```")
    md_lines.append("")

    md_lines.append("---")
    md_lines.append("")
    md_lines.append("**End of artifact.** This is a verification record, not a regression")
    md_lines.append("suite entry. Future tuning of sections 1/3/6 is gated by the vault rule")
    md_lines.append("(CLAUDE.md Section 3 Decision 15) and happens in dedicated sessions with")
    md_lines.append("`core/` frozen.")
    md_lines.append("")

    OUTPUT_PATH.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"\nWrote artifact: {OUTPUT_PATH}", flush=True)
    print(f"Size: {OUTPUT_PATH.stat().st_size} bytes")

    # Print short stdout verification summary
    print("\n=== Verification summary ===")
    print(f"  Section 1 real content:    {section_1_real_content}")
    print(f"  Section 3 list shape:      {section_3_real_shape} (entries={len(debug.page_intelligence) if isinstance(debug.page_intelligence, list) else 'N/A'})")
    print(f"  Section 6 list shape:      {section_6_real_shape} (legends={len(debug.legend_contents) if isinstance(debug.legend_contents, list) else 'N/A'})")
    print(f"  Section 2 stub_marker ok:  {section_2_stub_ok}")
    print(f"  Section 4 stub_marker ok:  {section_4_stub_ok}")
    print(f"  Section 5 stub_marker ok:  {section_5_stub_ok}")
    print(f"  detected_system:           {detected_system!r}")
    print(f"  system_confidence:         {system_confidence}")
    print(f"  scope_pages:               {scope_pages}")
    print(f"  scope_pages incl 18/19:    {scope_pages_includes_18_or_19}")


if __name__ == "__main__":
    main()
