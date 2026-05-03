"""
Tests for the dispatch gate (Layer 3).

Covers:
  1. Schema tests — dataclass instantiation, defaults, enums
  2. Confidence scale constants
  3. Single-page test — CFA roof plan
  4. Multi-page test — Vine Street 138-page bid set
  5. LLM validation tests
  6. Leak check tests
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.context import (
    PlanSetContext, PageContext, SheetEntry, CrossReference,
    Legend, LegendEntry, PageZone, ScaleInfo, ProjectMetadata,
    TradeContext, BidContext, SourceTag, LLMInput, LLMOutput,
    Discipline, PageType, ConstructionType,
    CONFIDENCE_EXPLICIT, CONFIDENCE_STRONG, CONFIDENCE_INFERRED,
    CONFIDENCE_WEAK, CONFIDENCE_UNKNOWN,
    validate_llm_output, check_for_leaks,
)
from core.dispatch_gate import run_dispatch, _classify_page_type


# ============================================================
# TEST DATA PATHS
# ============================================================

CFA_PDF = Path("test_plans/cfa_roof_A230.pdf")
VINE_PDF = Path("test_plans/Vine_Street_Retail_Center_-_Kissimmee_-_Great_Southern_Constructors.pdf")
TACO_BELL_PDF = Path("test_plans/tacobell_roof_A12.pdf")
AEA_PDF = Path("test_plans/aeasilverleaf_roof_A106.pdf")


# ============================================================
# 1. SCHEMA TESTS
# ============================================================

class TestSchema:
    """Verify all dataclasses can be instantiated with defaults."""

    def test_source_tag(self):
        tag = SourceTag(origin="filter_1", confidence=0.9, evidence="test")
        assert tag.origin == "filter_1"
        assert tag.confidence == 0.9

    def test_scale_info(self):
        si = ScaleInfo(scale_string='1/4" = 1\'-0"', ft_per_inch=4.0, source="zone_label")
        assert si.ft_per_inch == 4.0
        assert si.source_page is None
        assert si.confidence == CONFIDENCE_UNKNOWN

    def test_sheet_entry(self):
        entry = SheetEntry(
            sheet_number="A-1.3", title="ROOF PLAN", page_index=12,
            discipline=Discipline.ARCHITECTURAL, page_type=PageType.ROOF_PLAN)
        assert entry.scale is None
        assert entry.confidence == CONFIDENCE_UNKNOWN

    def test_cross_reference(self):
        ref = CrossReference(
            ref_type="detail", identifier="5", text="SEE DETAIL 5/A1.3",
            source_page=12, source_x=100.0, source_y=200.0,
            target_sheet="A1.3")
        assert ref.resolved is False
        assert ref.target_page is None

    def test_legend(self):
        leg = Legend(legend_type="keynote", title="ROOF KEYNOTES", page_index=12)
        assert leg.entries == []
        assert leg.entry_count == 0

    def test_legend_entry(self):
        entry = LegendEntry(key="1", description="SINGLE PLY MEMBRANE")
        assert entry.key == "1"

    def test_page_zone(self):
        zone = PageZone(zone_type="main_drawing", bbox=(0, 0, 600, 800))
        assert zone.label is None
        assert zone.scale is None

    def test_page_context(self):
        pc = PageContext(page_index=0)
        assert pc.page_type == PageType.UNKNOWN
        assert pc.discipline == Discipline.UNKNOWN
        assert pc.zones == []
        assert pc.legends == []
        assert pc.cross_refs_out == []
        assert pc.cross_refs_in == []
        assert pc.callout_texts == []
        assert pc.spec_note_texts == []
        assert not pc.has_drawing_area
        assert not pc.has_title_block

    def test_project_metadata(self):
        pm = ProjectMetadata()
        assert pm.project_name is None
        assert pm.total_pages == 0
        assert pm.construction_type is None
        assert pm.system_classifications == {}
        assert pm.field_sources == {}

    def test_trade_context(self):
        tc = TradeContext(trade_id="roofing", trade_name="Commercial Roofing")
        assert tc.relevant_pages == []
        assert tc.code_requirements == {}

    def test_bid_context(self):
        bc = BidContext()
        assert bc.bid_status == "open"
        assert bc.trades_solicited == []
        assert not bc.pre_bid_required

    def test_llm_input(self):
        li = LLMInput()
        assert li.cover_page_text == ""
        assert li.legend_texts == {}

    def test_llm_output(self):
        lo = LLMOutput()
        assert lo.project_name is None
        assert lo.system_classifications == {}

    def test_plan_set_context_defaults(self):
        ctx = PlanSetContext(pdf_path="test.pdf", pdf_hash="abc123", total_pages=1)
        assert ctx.sheet_map == {}
        assert ctx.pages == {}
        assert ctx.all_cross_refs == []
        assert ctx.all_legends == []
        assert ctx.legends_by_type == {}
        assert ctx.trade_contexts == {}
        assert ctx.dispatch_complete is False
        assert ctx.sheet_map_source == "none"

    def test_plan_set_context_methods(self):
        ctx = PlanSetContext(pdf_path="test.pdf", pdf_hash="abc123", total_pages=5)
        ctx.pages[0] = PageContext(page_index=0, page_type=PageType.ROOF_PLAN,
                                   discipline=Discipline.ARCHITECTURAL)
        ctx.pages[1] = PageContext(page_index=1, page_type=PageType.DETAIL_SHEET,
                                   discipline=Discipline.ARCHITECTURAL)
        ctx.pages[2] = PageContext(page_index=2, page_type=PageType.FLOOR_PLAN,
                                   discipline=Discipline.STRUCTURAL)

        roof_pages = ctx.get_pages_by_type(PageType.ROOF_PLAN)
        assert len(roof_pages) == 1
        assert roof_pages[0].page_index == 0

        arch_pages = ctx.get_pages_by_discipline(Discipline.ARCHITECTURAL)
        assert len(arch_pages) == 2

    def test_resolve_sheet(self):
        ctx = PlanSetContext(pdf_path="test.pdf", pdf_hash="abc123", total_pages=5)
        ctx.sheet_map["A-1.3"] = SheetEntry(
            sheet_number="A-1.3", title="ROOF PLAN", page_index=12,
            discipline=Discipline.ARCHITECTURAL, page_type=PageType.ROOF_PLAN)
        assert ctx.resolve_sheet("A-1.3") == 12
        assert ctx.resolve_sheet("X-99") is None

    def test_lookup_keynote(self):
        ctx = PlanSetContext(pdf_path="test.pdf", pdf_hash="abc123", total_pages=1)
        legend = Legend(legend_type="keynote", title="KEYNOTES", page_index=0,
                       entries=[LegendEntry(key="1", description="MEMBRANE"),
                                LegendEntry(key="2", description="INSULATION")])
        ctx.legends_by_type["keynote"] = [legend]
        assert ctx.lookup_keynote("1") == "MEMBRANE"
        assert ctx.lookup_keynote("99") is None

    def test_discipline_enum(self):
        assert Discipline.ARCHITECTURAL.value == "A"
        assert Discipline.FIRE_PROTECTION.value == "FP"
        assert Discipline.UNKNOWN.value == "?"

    def test_page_type_enum(self):
        assert PageType.ROOF_PLAN.value == "roof_plan"
        assert PageType.DRAWING_INDEX.value == "drawing_index"
        assert PageType.UNKNOWN.value == "unknown"

    def test_construction_type_enum(self):
        assert ConstructionType.REROOF.value == "reroof"
        assert ConstructionType.UNKNOWN.value == "unknown"


# ============================================================
# 2. CONFIDENCE SCALE
# ============================================================

class TestConfidence:
    def test_confidence_constants_exist(self):
        assert CONFIDENCE_EXPLICIT == 0.9
        assert CONFIDENCE_STRONG == 0.7
        assert CONFIDENCE_INFERRED == 0.5
        assert CONFIDENCE_WEAK == 0.3
        assert CONFIDENCE_UNKNOWN == 0.0

    def test_confidence_ordering(self):
        assert CONFIDENCE_EXPLICIT > CONFIDENCE_STRONG > CONFIDENCE_INFERRED > CONFIDENCE_WEAK > CONFIDENCE_UNKNOWN


# ============================================================
# 3. SINGLE-PAGE TEST — CFA
# ============================================================

@pytest.mark.skipif(not CFA_PDF.exists(), reason="CFA test PDF not available")
class TestSinglePageCFA:
    @pytest.fixture(scope="class")
    def ctx(self):
        return run_dispatch(CFA_PDF)

    def test_dispatch_completes(self, ctx):
        assert ctx.dispatch_complete is True
        assert len(ctx.filters_completed) == 5

    def test_page_classified_as_roof_plan(self, ctx):
        assert 0 in ctx.pages
        assert ctx.pages[0].page_type == PageType.ROOF_PLAN

    def test_scale_found(self, ctx):
        assert ctx.pages[0].scale is not None
        assert ctx.pages[0].scale.ft_per_inch == 4.0

    def test_total_pages(self, ctx):
        assert ctx.total_pages == 1


# ============================================================
# 4. MULTI-PAGE TEST — VINE STREET
# ============================================================

@pytest.mark.skipif(not VINE_PDF.exists(), reason="Vine Street test PDF not available")
class TestMultiPageVineStreet:
    @pytest.fixture(scope="class")
    def ctx(self):
        return run_dispatch(VINE_PDF)

    def test_dispatch_completes(self, ctx):
        assert ctx.dispatch_complete is True

    def test_sheet_map_populated(self, ctx):
        assert len(ctx.sheet_map) >= 25

    def test_sheet_map_source_is_drawing_index(self, ctx):
        assert ctx.sheet_map_source == "drawing_index"

    def test_roof_plan_classified(self, ctx):
        # Page 11 (A-1.3) should be ROOF_PLAN
        roof_pages = ctx.get_pages_by_type(PageType.ROOF_PLAN)
        assert len(roof_pages) >= 1

    def test_cross_references_resolved(self, ctx):
        total = len(ctx.all_cross_refs)
        assert total > 0
        if total > 0:
            rate = ctx.resolved_count / total
            assert rate > 0.40, f"Resolution rate {rate:.0%} below 40% threshold"

    def test_legend_count(self, ctx):
        assert len(ctx.all_legends) >= 5

    def test_multiple_disciplines(self, ctx):
        disciplines = {pc.discipline for pc in ctx.pages.values()
                       if pc.discipline != Discipline.UNKNOWN}
        assert len(disciplines) >= 3  # Should have A, S, E, P, G, M at minimum


# ============================================================
# 5. LLM VALIDATION TESTS
# ============================================================

class TestLLMValidation:
    def test_valid_output_passes(self):
        source = "The building is 7280 SF retail. Wind speed 150 MPH."
        output = LLMOutput(
            building_type="retail",
            total_building_sf=7280.0,
            wind_speed_mph=150,
        )
        valid, errors = validate_llm_output(output, source)
        assert valid is True
        assert errors == []

    def test_invented_wind_speed_rejected(self):
        source = "The building is a retail store."
        output = LLMOutput(wind_speed_mph=185)
        valid, errors = validate_llm_output(output, source)
        assert valid is False
        assert any("wind_speed_mph" in e for e in errors)

    def test_invented_sf_rejected(self):
        source = "General notes for the project."
        output = LLMOutput(total_building_sf=99999.0)
        valid, errors = validate_llm_output(output, source)
        assert valid is False
        assert any("total_building_sf" in e for e in errors)

    def test_relayed_sf_accepted(self):
        source = "Total building area: 5,746 SF."
        output = LLMOutput(total_building_sf=5746.0)
        valid, errors = validate_llm_output(output, source)
        assert valid is True

    def test_invalid_building_type_rejected(self):
        source = "Some text."
        output = LLMOutput(building_type="spaceship")
        valid, errors = validate_llm_output(output, source)
        assert valid is False
        assert any("building_type" in e for e in errors)

    def test_invalid_construction_type_rejected(self):
        source = "Some text."
        output = LLMOutput(construction_type="demolition")
        valid, errors = validate_llm_output(output, source)
        assert valid is False

    def test_long_scope_summary_rejected(self):
        source = "Some text."
        output = LLMOutput(scope_summary="x" * 501)
        valid, errors = validate_llm_output(output, source)
        assert valid is False
        assert any("scope_summary" in e for e in errors)


# ============================================================
# 6. LEAK CHECK TESTS
# ============================================================

class TestLeakCheck:
    def test_llm_writing_deterministic_field_detected(self):
        ctx = PlanSetContext(pdf_path="test.pdf", pdf_hash="abc", total_pages=1)
        # Simulate LLM writing to a deterministic field
        ctx.project.field_sources["sheet_map"] = SourceTag(
            origin="filter_6_llm", confidence=0.9, evidence="LLM said so")
        warnings = check_for_leaks(ctx)
        assert any("LEAK" in w for w in warnings)

    def test_unscored_page_type_detected(self):
        ctx = PlanSetContext(pdf_path="test.pdf", pdf_hash="abc", total_pages=1)
        ctx.pages[0] = PageContext(
            page_index=0, page_type=PageType.ROOF_PLAN, confidence=0.0)
        warnings = check_for_leaks(ctx)
        assert any("UNSCORED" in w for w in warnings)

    def test_low_resolution_rate_detected(self):
        ctx = PlanSetContext(pdf_path="test.pdf", pdf_hash="abc", total_pages=1)
        ctx.resolved_count = 2
        ctx.unresolved_count = 100
        warnings = check_for_leaks(ctx)
        assert any("LOW RESOLUTION" in w for w in warnings)

    def test_clean_context_no_warnings(self):
        ctx = PlanSetContext(pdf_path="test.pdf", pdf_hash="abc", total_pages=1)
        ctx.pages[0] = PageContext(
            page_index=0, page_type=PageType.UNKNOWN, confidence=0.0)
        warnings = check_for_leaks(ctx)
        assert len(warnings) == 0

    def test_deterministic_field_from_filter_1_ok(self):
        ctx = PlanSetContext(pdf_path="test.pdf", pdf_hash="abc", total_pages=1)
        ctx.project.field_sources["sheet_map"] = SourceTag(
            origin="filter_1", confidence=0.9, evidence="drawing index")
        warnings = check_for_leaks(ctx)
        assert not any("LEAK" in w for w in warnings)


# ============================================================
# ADDITIONAL SINGLE-PAGE TESTS
# ============================================================

@pytest.mark.skipif(not TACO_BELL_PDF.exists(), reason="Taco Bell PDF not available")
class TestTacoBell:
    @pytest.fixture(scope="class")
    def ctx(self):
        return run_dispatch(TACO_BELL_PDF)

    def test_page_classified_roof_plan(self, ctx):
        assert ctx.pages[0].page_type == PageType.ROOF_PLAN

    def test_cross_refs_found(self, ctx):
        assert len(ctx.all_cross_refs) > 0

    def test_has_legend(self, ctx):
        assert len(ctx.all_legends) >= 1

    def test_scale_found(self, ctx):
        assert ctx.pages[0].scale is not None
        assert ctx.pages[0].scale.ft_per_inch == 4.0


@pytest.mark.skipif(not AEA_PDF.exists(), reason="AEA PDF not available")
class TestAEA:
    @pytest.fixture(scope="class")
    def ctx(self):
        return run_dispatch(AEA_PDF)

    def test_page_classified_roof_plan(self, ctx):
        assert ctx.pages[0].page_type == PageType.ROOF_PLAN

    def test_scale_detected(self, ctx):
        assert ctx.pages[0].scale is not None
        assert ctx.pages[0].scale.ft_per_inch == 8.0

    def test_building_sf_found(self, ctx):
        assert ctx.project.total_building_sf == 5746.0

    def test_has_legends(self, ctx):
        assert len(ctx.all_legends) >= 2


class TestClassifierUpgrade:
    """Tests for G.2 classifier upgrade: pc.title read + new keywords."""

    def test_classify_reads_pc_title_framing_plan(self):
        page_type, _ = _classify_page_type("", "", title="ROOF FRAMING PLAN")
        assert page_type == PageType.FRAMING_PLAN

    def test_classify_reads_pc_title_general_notes(self):
        page_type, _ = _classify_page_type("", "", title="STRUCTURAL NOTES")
        assert page_type == PageType.GENERAL_NOTES

    def test_classify_dimensioned_building_plan(self):
        page_type, _ = _classify_page_type("", "DIMENSIONED BUILDING PLAN")
        assert page_type == PageType.FLOOR_PLAN

    def test_classify_window_types_schedule(self):
        page_type, _ = _classify_page_type("", "WINDOW TYPES")
        assert page_type == PageType.SCHEDULE_SHEET

    def test_classify_fire_sprinkler_plan(self):
        page_type, _ = _classify_page_type("", "FIRST FLOOR FIRE SPRINKLER PLAN")
        assert page_type == PageType.MEP_PLAN

    def test_classify_steel_elevations_details(self):
        page_type, _ = _classify_page_type("", "", title="STEEL ELEVATIONS AND DETAILS")
        assert page_type == PageType.DETAIL_SHEET

    def test_classify_utility_notes(self):
        page_type, _ = _classify_page_type("", "UTILITY NOTES")
        assert page_type == PageType.GENERAL_NOTES
