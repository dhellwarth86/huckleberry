"""Smoke test for GlazingModule (C.3c-build).

NOT a behavior test. Verifies the module imports, instantiates, and runs
on a stub TradeModuleInput without raising. Behavior validation comes
from the C.3c-run sweep, not from advance tests; tests are written from
sweep observations per CLAUDE.md Section 3 Decision 15 and
MARCH_ORDERS_C_3c_build.md Section 4.4.

ONE test per the orders' "214 -> 215 suite count" expectation.
"""
from __future__ import annotations

from core.glazing_module import GlazingModule
from core.trade_module import TradeModuleInput, TradeModuleOutput


def test_glazing_module_imports_instantiates_and_runs_on_stub():
    """Single smoke test: module reaches the contract on a minimal stub."""
    module = GlazingModule()
    assert module.TRADE_NAME == "glazing"
    assert isinstance(module.FIELDS, list) and module.FIELDS
    assert callable(getattr(module, "analyze", None))

    stub = TradeModuleInput(
        polygon_area_sqin=0.0,
        polygon_area_sf=0.0,
        polygon_perimeter_in=0.0,
        polygon_perimeter_lf=0.0,
        polygon_bbox=(0.0, 0.0, 100.0, 100.0),
        polygon_vertices=4,
        scale_fpi=8.0,
        scale_source="dispatch",
        scale_confidence=0.9,
        detection_source="vector_heavy",
    )

    output = module.analyze(stub)
    assert isinstance(output, TradeModuleOutput)
    assert isinstance(output.glazing_items, list)
    assert isinstance(output.door_items, list)
    assert isinstance(output.storefront_items, list)
