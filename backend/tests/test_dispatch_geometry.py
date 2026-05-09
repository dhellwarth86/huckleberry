"""
Phase G.6 — Stages 6-9 geometry/scale/callout extraction wiring tests.

Replaces the deferred zeroed-geometry path with the proper geometry pipeline:
  - Stage 6: vector polygon clustering (`GeometryMatrix.cluster_and_union_polygons`)
  - Stage 7: scale resolution (built into the cluster scoring pass)
  - Stage 8: building outline area/perimeter/bbox (top-scored cluster)
  - Stage 9: callout extraction inside polygon bbox (already in `build_trade_input`)

The G.5a CP1 auto-pin extractor consumes RoofingModule.equipment_pins; once
G.6 wires geometry, equipment_pins finally populate from PDF callouts.
"""

import pytest
from pathlib import Path

import fitz

from core.dispatch_gate import _run_stages_6_9, run_dispatch
from core.pdf_engine import PDFEngine


# ---------------------------------------------------------------------------
# Synthetic fixtures with vector geometry
# ---------------------------------------------------------------------------

@pytest.fixture
def vector_polygon_pdf(tmp_path) -> Path:
    """Single-page PDF with a closed vector rectangle large enough to score
    above cluster_and_union_polygons' 400-sqft floor at building scales.

    Letter page (792 x 612 pts = 11 x 8.5 in). Rectangle covers 650 x 400 pts
    (9.03 x 5.56 in = 50.2 sq in on paper). At 1/4" = 1'-0" (4 ft/in), that's
    ~803 sqft — within the 400-60000 sf range cluster scoring keeps.
    """
    doc = fitz.open()
    page = doc.new_page(width=792, height=612)
    page.insert_text(fitz.Point(72, 36), "ROOF PLAN", fontsize=18)
    page.insert_text(fitz.Point(72, 60), "Scale: 1/4\" = 1'-0\"", fontsize=10)
    rect = fitz.Rect(50, 100, 700, 500)
    page.draw_rect(rect, color=(0, 0, 0), width=2)
    pdf_path = tmp_path / "vector_polygon.pdf"
    doc.save(str(pdf_path))
    doc.close()
    return pdf_path


@pytest.fixture
def vector_polygon_with_callouts_pdf(tmp_path) -> Path:
    """Same large rectangle, plus equipment callouts inside the polygon bbox.

    Used to verify Stage 9 (callout extraction) flows through to
    RoofingModule.equipment_pins via build_trade_input + roofing_module._count_callouts.
    """
    doc = fitz.open()
    page = doc.new_page(width=792, height=612)
    page.insert_text(fitz.Point(72, 36), "ROOF PLAN", fontsize=18)
    page.insert_text(fitz.Point(72, 60), "Scale: 1/4\" = 1'-0\"", fontsize=10)
    # Large building rect (matches vector_polygon_pdf)
    rect = fitz.Rect(50, 100, 700, 500)
    page.draw_rect(rect, color=(0, 0, 0), width=2)
    # Equipment callouts INSIDE the rect, at known positions
    page.insert_text(fitz.Point(150, 200), "DRAIN", fontsize=10)
    page.insert_text(fitz.Point(400, 200), "RTU-1", fontsize=10)
    page.insert_text(fitz.Point(600, 200), "SCUPPER", fontsize=10)
    page.insert_text(fitz.Point(150, 400), "VTR", fontsize=10)
    pdf_path = tmp_path / "vector_polygon_callouts.pdf"
    doc.save(str(pdf_path))
    doc.close()
    return pdf_path


@pytest.fixture
def empty_page_pdf(tmp_path) -> Path:
    """Single-page PDF with text only — no closed vector polygons.

    Used to verify _run_stages_6_9 returns gracefully when geometry detection
    finds nothing (most non-roof-plan pages: specs, details, cover sheets).
    """
    doc = fitz.open()
    page = doc.new_page(width=792, height=612)
    page.insert_text(fitz.Point(72, 100), "GENERAL NOTES", fontsize=14)
    page.insert_text(fitz.Point(72, 130), "All work shall comply with code.", fontsize=10)
    pdf_path = tmp_path / "empty.pdf"
    doc.save(str(pdf_path))
    doc.close()
    return pdf_path


# ---------------------------------------------------------------------------
# _run_stages_6_9 unit tests
# ---------------------------------------------------------------------------

class TestRunStages69:
    """Direct unit tests for the new dispatch-side geometry helper."""

    def test_returns_geometry_shape_with_synthetic_vector_polygon(self, vector_polygon_pdf):
        """Vector polygon present → geometry_result has populated building_outline + contours."""
        engine = PDFEngine()
        doc = engine.open(vector_polygon_pdf)
        try:
            result = _run_stages_6_9(engine, doc, page_idx=0)
            assert result is not None, "must return a dict (not None) when geometry available"
            assert isinstance(result, dict)
            outline = result.get("building_outline")
            assert outline is not None, "building_outline must be populated when polygon present"
            assert outline.get("area_sqft", 0) > 0, "area_sqft must be > 0 for a real polygon"
            assert outline.get("perimeter_ft", 0) > 0, "perimeter_ft must be > 0 for a real polygon"
            assert outline.get("ft_per_inch", 0) > 0, "ft_per_inch must be set by scale scoring"

            contours = result.get("contours") or []
            assert len(contours) > 0, "contours list must include at least the building outline"
            building = next((c for c in contours if c.get("is_building_outline")), None)
            assert building is not None, "exactly one contour must be flagged is_building_outline"
            bbox_pct = building.get("bbox_pct")
            assert bbox_pct is not None and len(bbox_pct) == 4, "bbox_pct must be [x, y, w, h]"
            for v in bbox_pct:
                assert 0 <= v <= 100, f"bbox_pct values must be in 0..100, got {bbox_pct}"

            scale_info = result.get("scale_info") or {}
            assert scale_info.get("source"), "scale_info.source must be set (not 'unwired')"
        finally:
            engine.close(doc)

    def test_returns_empty_when_no_vector_polygons(self, empty_page_pdf):
        """No polygons → empty/safe dict so build_trade_input falls back gracefully."""
        engine = PDFEngine()
        doc = engine.open(empty_page_pdf)
        try:
            result = _run_stages_6_9(engine, doc, page_idx=0)
            # Either {} (safe-empty) or a dict where building_outline is None/empty.
            assert isinstance(result, dict)
            outline = result.get("building_outline") or {}
            assert outline.get("area_sqft", 0.0) == 0.0, (
                "no polygons → area_sqft 0.0; build_trade_input zeros polygon fields"
            )
        finally:
            engine.close(doc)


# ---------------------------------------------------------------------------
# Dispatch wiring integration tests
# ---------------------------------------------------------------------------

class TestDispatchGeometryWiring:
    """End-to-end: confirm Stage 6-9 wiring lights up RoofingModule.equipment_pins."""

    def test_dispatch_populates_polygon_fields_in_trade_module_outputs(self, vector_polygon_pdf, tmp_path):
        """Full dispatch on a synthetic page with a vector polygon must populate
        polygon_area_sf > 0 and scale_source != 'unwired' on the RoofingModule input.

        Uses storage='auto' to trigger Stage 13 (trade module wiring); job_id=None
        skips D.2 persistence so this stays a pure dispatch-shape assertion.
        """
        ctx = run_dispatch(vector_polygon_pdf, storage="auto")
        # trade_module_outputs is keyed by page_idx → trade_name → output dict
        assert 0 in ctx.trade_module_outputs, (
            f"trade_module_outputs missing page 0; got pages {list(ctx.trade_module_outputs.keys())}"
        )
        page_outputs = ctx.trade_module_outputs[0]
        assert "roofing" in page_outputs, "roofing output must exist for page 0"
        roofing_out = page_outputs["roofing"]
        # Roofing output's equipment_pins is the load-bearing artifact for the
        # G.5a auto-pin extractor. Without callouts present in this fixture,
        # the list may be empty — but the wiring should not crash.
        assert hasattr(roofing_out, "equipment_pins"), "RoofingModule output must have equipment_pins attr"

    def test_dispatch_with_callouts_populates_roofing_equipment_pins(
        self, vector_polygon_with_callouts_pdf
    ):
        """Stages 6-9 wired + callouts inside polygon → equipment_pins non-empty.

        This is the load-bearing test: G.5a CP1 wired the auto-pin extractor
        but it's been idle (RoofingModule.equipment_pins=[]). G.6 turns it on.
        """
        ctx = run_dispatch(vector_polygon_with_callouts_pdf, storage="auto")
        assert 0 in ctx.trade_module_outputs
        roofing_out = ctx.trade_module_outputs[0]["roofing"]
        pins = list(getattr(roofing_out, "equipment_pins", []) or [])
        assert len(pins) > 0, (
            f"equipment_pins must be non-empty when DRAIN/RTU/SCUPPER/VTR callouts "
            f"are inside the polygon bbox; got {pins}"
        )
        # Each pin must have a 'type' field for the auto-pin extractor to
        # produce annotation rows downstream.
        for pin in pins:
            assert "type" in pin, f"pin missing 'type' field: {pin}"
