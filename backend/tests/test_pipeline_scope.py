"""Tiny unit tests for Layer 2 (scope) extraction primitives."""

from scripts._pipeline.scope import (
    find_spec_sections,
    find_manufacturers,
    find_attachments,
    find_thicknesses,
    find_florida_signals,
    find_system_type_keywords,
)


def test_spec_section_07_54_23_finds_tpo():
    hits = find_spec_sections("SECTION 07 54 23 - THERMOPLASTIC MEMBRANE")
    assert any(h["system"] == "tpo" for h in hits)


def test_spec_section_07_54_19_finds_pvc():
    hits = find_spec_sections("Refer to 07 54 19 PVC membrane")
    assert any(h["system"] == "pvc" for h in hits)


def test_spec_section_no_match_outside_div7():
    # 09 51 is acoustical ceilings — not in our SPEC_SECTIONS
    hits = find_spec_sections("Refer to 09 51 23 Acoustical")
    assert not hits


def test_manufacturer_carlisle_canonical():
    hits = find_manufacturers("MANUFACTURER: CARLISLE SYNTEC SYSTEMS")
    assert any(h["manufacturer"] == "Carlisle" for h in hits)


def test_manufacturer_via_product_name():
    hits = find_manufacturers("Sure-Weld 60 mil membrane by Carlisle")
    # Either name-match or product-match should fire
    assert any(h["manufacturer"] == "Carlisle" for h in hits)


def test_manufacturer_sika_sarnafil():
    hits = find_manufacturers("Provide Sarnafil G410 60mil PVC")
    assert any(h["manufacturer"] == "Sika Sarnafil" for h in hits)


def test_attachment_mechanically_attached():
    out = find_attachments("MECHANICALLY ATTACHED TPO MEMBRANE")
    assert "mechanically_attached" in out


def test_attachment_fully_adhered():
    out = find_attachments("Fully adhered TPO over cover board")
    assert "fully_adhered" in out


def test_thickness_60_mil():
    out = find_thicknesses("Provide 60 mil TPO membrane")
    assert "60 mil" in out


def test_florida_signals():
    out = find_florida_signals("Comply with FBC and HVHZ requirements; NOA required.")
    assert "FBC" in out
    assert "HVHZ" in out
    assert "NOA" in out


def test_system_type_keywords_tpo_and_modbit():
    out = find_system_type_keywords("Two-ply MODIFIED BITUMEN cap sheet over base")
    assert "modified_bitumen" in out


def test_system_type_keyword_pvc_requires_roof_or_membrane_word():
    # Bare "PVC pipe" should NOT be flagged as a roof system
    out = find_system_type_keywords("Provide 4 inch PVC pipe to floor drain")
    assert "pvc" not in out

    out2 = find_system_type_keywords("Install PVC roof membrane per spec")
    assert "pvc" in out2
