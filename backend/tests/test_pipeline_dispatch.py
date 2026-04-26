"""Tiny unit tests for Layer 1 (dispatch) extraction primitives.

Karpathy red-phase: each test asserts a specific contract. Failures point at
which classification rule broke. These tests run against synthetic page-text
fixtures, not real PDFs, so they're fast and deterministic.
"""

from scripts._pipeline.dispatch import (
    PageText,
    classify_page,
    extract_sheet_number,
    extract_discipline,
    find_cross_references,
    find_legends,
    extract_project_metadata,
)


def _page(idx: int, full_text: str, title_block: str = "") -> PageText:
    return PageText(
        page_index=idx,
        full_text=full_text,
        title_block_text=title_block or full_text[-200:],
        text_blocks=[],
        width=2592.0,
        height=1728.0,
    )


def test_extract_sheet_number_typical():
    assert extract_sheet_number("DRAWING TITLE A-1.3") == "A-1.3"
    assert extract_sheet_number("ROOF PLAN A-2.0") == "A-2.0"
    assert extract_sheet_number("M-1.0  HVAC PLAN") == "M-1.0"


def test_extract_sheet_number_no_match():
    assert extract_sheet_number("just some text 123") is None
    assert extract_sheet_number("") is None


def test_extract_discipline_basic():
    assert extract_discipline("A-1.3") == "ARCHITECTURAL"
    assert extract_discipline("M-2.0") == "MECHANICAL"
    assert extract_discipline("S-1.0") == "STRUCTURAL"
    assert extract_discipline("FP-1") == "FIRE_PROTECTION"
    assert extract_discipline(None) is None


def test_classify_page_roof_plan_title():
    p = _page(0, "Some body text", title_block="ROOF PLAN  A-2.0")
    c = classify_page(p)
    assert c.page_type == "roof_plan"
    assert c.confidence == 0.9
    assert c.matched_in == "title_block"
    assert c.sheet_number == "A-2.0"
    assert c.discipline == "ARCHITECTURAL"


def test_classify_page_roof_plan_in_body():
    p = _page(1, "Some text containing ROOF PLAN somewhere", title_block="A-2.0")
    c = classify_page(p)
    assert c.page_type == "roof_plan"
    # Body match -> page_conf, lower than title_conf
    assert c.confidence == 0.7
    assert c.matched_in == "page_text"


def test_classify_page_unknown_when_no_match():
    p = _page(2, "Random text with no classification keywords", title_block="X-1")
    c = classify_page(p)
    assert c.page_type == "unknown"
    assert c.confidence == 0.0


def test_classify_page_mep_fallback():
    # No keyword match BUT sheet number M-1.0 -> mep_plan low-conf fallback
    p = _page(3, "Some random body", title_block="HVAC SOMETHING M-1.0")
    c = classify_page(p)
    # "HVAC" doesn't match a keyword; M-1 sheet number drives fallback
    # BUT note that "SCHEDULE" or other keywords in HVAC sheets often hit first.
    # This page has none, so fallback fires:
    assert c.page_type == "mep_plan"
    assert c.matched_in == "fallback"
    assert c.confidence == 0.3


def test_classify_page_cover_high_confidence():
    p = _page(0, "Some text", title_block="COVER SHEET  G-0.0")
    c = classify_page(p)
    assert c.page_type == "cover"
    assert c.confidence == 0.9


def test_find_cross_references_explicit():
    refs = find_cross_references([], "PLEASE SEE DETAIL 5/A-1.3 FOR MORE")
    assert any(r["pattern"] == "detail_explicit" and r["target_sheet"] == "A-1.3" for r in refs)


def test_find_cross_references_see_ref():
    refs = find_cross_references([], "ALSO SEE A-2.2 FOR REFERENCE")
    assert any(r["pattern"] == "see_ref" and r["target_sheet"] == "A-2.2" for r in refs)


def test_find_cross_references_implicit_short_block():
    blocks = [{"text": "6 A1.2"}]
    refs = find_cross_references(blocks, "6 A1.2")
    assert any(r["pattern"] == "detail_implicit" and r["target_sheet"] == "A1.2" for r in refs)


def test_find_cross_references_implicit_skips_long_block():
    long_block = "This is a long body of text 6 A1.2 that should not be classified as a callout because it's clearly body text far longer than the block-char gate."
    refs = find_cross_references([{"text": long_block}], long_block)
    # The detail_implicit matcher should NOT fire on this block
    assert not any(r["pattern"] == "detail_implicit" for r in refs)


def test_find_legends_basic():
    text = """
    KEYNOTES:
    1. Notes one
    2. Notes two
    3. Notes three
    """
    legs = find_legends(text)
    assert len(legs) == 1
    assert legs[0]["legend_type"] == "keynote"


def test_extract_project_metadata_address():
    text = "PROJECT: PANDA EXPRESS\nADDRESS: 123 MAIN STREET\nNAPLES, FL"
    meta = extract_project_metadata(text)
    assert meta["project_address"] == "123 MAIN STREET"
    # LLM-only fields stay None
    assert meta["wind_speed_mph"] is None
    assert meta["construction_type"] is None
