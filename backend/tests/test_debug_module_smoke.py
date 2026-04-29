"""Smoke test for debug_module (C.5 partial port).

NOT a behavior test. Verifies the partial port imports cleanly, runs
end-to-end on a minimal stub PlanSetContext, produces real content for
sections 1/3/6 (the verbatim ports), and emits the documented stub
markers for sections 2/4/5 (the deferred sections).

Real-bidset verification of section 1/3/6 content lives in the run-
through artifact `backend/C5_DEBUG_RUN_THROUGH_<bidset>.md`, not in
this test. Behavior validation comes from the three-bidset sweep, not
from advance tests, per CLAUDE.md Section 3 Decision 15.

ONE test per the orders' "215 -> 216 suite count" expectation
(MARCH_ORDERS_C_5_debug_port.md Section 4).
"""
from __future__ import annotations

from core.context import PlanSetContext
from core.debug_module import run_debug, DebugContext


def test_debug_module_partial_port_imports_runs_and_stubs_sections_2_4_5():
    """Single smoke test: partial port reaches the contract on a stub."""
    # Minimum PlanSetContext — only the three required identity fields.
    # All other fields default (empty pages dict, empty legends, etc.),
    # which is enough to exercise the verbatim-port code paths in
    # sections 1, 3, 6 and confirm they do not return a stub marker.
    ctx = PlanSetContext(pdf_path="<stub>", pdf_hash="<stub>", total_pages=0)

    debug = run_debug(ctx)

    # The contract returns a DebugContext (TradeContext subclass) and
    # registers it in ctx.trade_contexts under the "debug" key.
    assert isinstance(debug, DebugContext)
    assert ctx.trade_contexts.get("debug") is debug
    assert debug.trade_id == "debug"

    # The six diagnostic-section attributes plus the quality-flags list
    # all exist on the DebugContext (TracePoint key shape preserved).
    assert hasattr(debug, "dispatch_health")
    assert hasattr(debug, "scale_comparison")
    assert hasattr(debug, "page_intelligence")
    assert hasattr(debug, "crossref_summary")
    assert hasattr(debug, "geometry_diagnostics")
    assert hasattr(debug, "legend_contents")
    assert hasattr(debug, "legend_quality_flags")

    # Sections 1, 3, 6 are the verbatim ports. They produce real content
    # shapes (not the stub_marker dict) on the stub input. With an empty
    # pages dict and no legends, section 3 and section 6 yield empty
    # lists, but the type/shape distinguishes them from a stub.
    assert isinstance(debug.dispatch_health, dict)
    assert "dispatch_complete" in debug.dispatch_health
    assert "stub_marker" not in debug.dispatch_health

    assert isinstance(debug.page_intelligence, list)  # empty list is acceptable

    assert isinstance(debug.legend_contents, list)  # empty list is acceptable
    assert isinstance(debug.legend_quality_flags, list)

    # Sections 2, 4, 5 are stubbed pending external state. Each returns a
    # documented stub_marker dict (per MARCH_ORDERS_C_5_debug_port.md Section 3).
    assert isinstance(debug.scale_comparison, dict)
    assert debug.scale_comparison.get("stub_marker") == "C.5_partial_port_pending_scale_engine_route"

    assert isinstance(debug.crossref_summary, dict)
    assert debug.crossref_summary.get("stub_marker") == "C.5_partial_port_pending_networkx_and_sheet_index"

    assert isinstance(debug.geometry_diagnostics, dict)
    assert debug.geometry_diagnostics.get("stub_marker") == "C.5_partial_port_pending_geometry_results"
