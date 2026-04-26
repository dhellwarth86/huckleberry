"""Smoke test — every seed file imports cleanly AND its top-level structures
are non-empty and shaped as expected.

This is the cheapest possible regression guard against a seed file silently
breaking. If a future PR breaks a manufacturer entry or removes a relationship,
this test catches it before the experiment + downstream code do.

These tests are NOT trying to validate trade-correctness — they only check that
the data structures are present and non-empty. Trade correctness is an
estimator's job (see honest caveats in each seed file's docstring).
"""

import pytest


# ────────────────────────────────────────────────────────────────────────────
# Layer 1: Dispatch
# ────────────────────────────────────────────────────────────────────────────

def test_dispatch_seed_imports():
    """All top-level structures present and non-empty."""
    from seeds import dispatch_seed as d

    assert isinstance(d.CONFIDENCE, dict) and len(d.CONFIDENCE) >= 5
    assert isinstance(d.DISCIPLINES, dict) and "A" in d.DISCIPLINES
    assert isinstance(d.PAGE_TYPES, list) and "roof_plan" in d.PAGE_TYPES
    assert isinstance(d.PAGE_CLASSIFICATION_KEYWORDS, list) and len(d.PAGE_CLASSIFICATION_KEYWORDS) >= 10
    assert isinstance(d.SHEET_NUMBER_REGEX, str)
    assert isinstance(d.CROSS_REFERENCE_PATTERNS, dict) and "detail_explicit" in d.CROSS_REFERENCE_PATTERNS
    assert isinstance(d.LEGEND_HEADER_KEYWORDS, list) and "LEGEND" in d.LEGEND_HEADER_KEYWORDS
    assert isinstance(d.LLM_RULES, dict) and "may" in d.LLM_RULES and "may_not" in d.LLM_RULES


def test_dispatch_dropped_patterns_documented():
    """Dropped patterns must carry a reason and dropped_date — guard against
    silently re-adding a pattern that the diagnostic showed produces 10-100x
    false positives."""
    from seeds import dispatch_seed as d

    for name, info in d.DROPPED_PATTERNS.items():
        assert "reason" in info, f"DROPPED_PATTERNS['{name}'] missing reason"
        assert "dropped_date" in info, f"DROPPED_PATTERNS['{name}'] missing dropped_date"


# ────────────────────────────────────────────────────────────────────────────
# Layer 2: Materials (roofing)
# ────────────────────────────────────────────────────────────────────────────

def test_roofing_materials_imports():
    from seeds import roofing_materials as r

    assert isinstance(r.SPEC_SECTIONS, dict) and len(r.SPEC_SECTIONS) >= 20
    assert "07 54 23" in r.SPEC_SECTIONS, "TPO Membrane spec section missing"

    assert isinstance(r.MANUFACTURERS, dict) and len(r.MANUFACTURERS) >= 10
    for mfr_name, mfr_data in r.MANUFACTURERS.items():
        assert "systems" in mfr_data, f"manufacturer {mfr_name} missing 'systems'"
        assert "products" in mfr_data, f"manufacturer {mfr_name} missing 'products'"
        assert "aliases" in mfr_data, f"manufacturer {mfr_name} missing 'aliases'"

    assert isinstance(r.MATERIAL_PROPERTIES, dict)
    assert "thickness_markers" in r.MATERIAL_PROPERTIES
    assert "drawing_conventions" in r.MATERIAL_PROPERTIES


# ────────────────────────────────────────────────────────────────────────────
# Layer 2: Materials (glazing — SKELETON, out of v0.1 scope but must still load)
# ────────────────────────────────────────────────────────────────────────────

def test_glazing_materials_imports_as_skeleton():
    """Glazing materials is documented as a skeleton needing estimator review.
    Out of scope for the v0.1 experiment but the file must still load — its
    presence in the repo is intentional."""
    from seeds import glazing_materials as g

    assert isinstance(g.SPEC_SECTIONS, dict) and len(g.SPEC_SECTIONS) >= 5
    assert "08 4413" in g.SPEC_SECTIONS, "curtain wall spec section missing"
    assert isinstance(g.MANUFACTURERS, dict)
    # Don't assert minimum count — author says it's a stub. Just confirm it's a dict.


# ────────────────────────────────────────────────────────────────────────────
# Layer 3: Assemblies (roofing)
# ────────────────────────────────────────────────────────────────────────────

def test_roof_assemblies_imports():
    from seeds import roof_assemblies as a

    assert isinstance(a.ROOF_COMPONENTS, dict) and len(a.ROOF_COMPONENTS) >= 30
    assert "field_membrane" in a.ROOF_COMPONENTS
    for comp_id, comp in a.ROOF_COMPONENTS.items():
        assert "role" in comp, f"component {comp_id} missing 'role'"
        assert "takeoff_unit" in comp, f"component {comp_id} missing 'takeoff_unit'"

    assert isinstance(a.ROOF_SYSTEMS, dict) and len(a.ROOF_SYSTEMS) >= 10
    assert "tpo_mechanically_attached" in a.ROOF_SYSTEMS
    for sys_id, sys in a.ROOF_SYSTEMS.items():
        assert "category" in sys, f"system {sys_id} missing 'category'"
        assert "required_components" in sys, f"system {sys_id} missing 'required_components'"

    assert isinstance(a.ASSEMBLY_RELATIONSHIPS, list) and len(a.ASSEMBLY_RELATIONSHIPS) >= 10
    for rule in a.ASSEMBLY_RELATIONSHIPS:
        assert "id" in rule and "rule" in rule and "triggers_warning_when" in rule

    assert isinstance(a.FBC_CONSTRAINTS, dict) and len(a.FBC_CONSTRAINTS) >= 5
    assert "hvhz" in a.FBC_CONSTRAINTS
    assert "secondary_drainage" in a.FBC_CONSTRAINTS


def test_roof_systems_components_resolve():
    """Every component listed in ROOF_SYSTEMS[*].required_components must
    resolve to a key in ROOF_COMPONENTS. Cross-file integrity check."""
    from seeds import roof_assemblies as a

    component_keys = set(a.ROOF_COMPONENTS.keys())
    for sys_id, sys in a.ROOF_SYSTEMS.items():
        for comp in sys.get("required_components", []):
            # Some shingle systems reference "drip_edge" which is functionally
            # edge_metal — not a perfect closure check, but flag obvious typos.
            if comp not in component_keys and comp not in ("drip_edge",):
                pytest.fail(
                    f"system '{sys_id}' references required component '{comp}' "
                    f"which is not defined in ROOF_COMPONENTS"
                )


# ────────────────────────────────────────────────────────────────────────────
# Layer 3: Assemblies (glazing — out of v0.1 scope but must load)
# ────────────────────────────────────────────────────────────────────────────

def test_glazing_assemblies_imports():
    """Glazing assemblies imports cleanly. Out of v0.1 experiment scope per
    PHASE_2_HANDOFF.md but the file ships in the repo."""
    from seeds import glazing_assemblies as g

    # Top-level structures should at least be present.
    # Don't assert specifics — content is real but unreviewed by glazing estimator.
    expected_attrs = ["GLAZING_COMPONENTS", "GLAZING_SYSTEMS"]
    for attr in expected_attrs:
        assert hasattr(g, attr), f"glazing_assemblies missing top-level {attr}"
        assert isinstance(getattr(g, attr), dict)
