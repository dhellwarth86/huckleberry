"""Layer 3 — Assembly: components-list and relationship warnings per system.

Consumes seeds/roof_assemblies.py. For each scope-identified system, walks
ROOF_SYSTEMS to pick the best-matching assembly (by membrane_type +
attachment), enumerates required + conditional components, and tries to
support each component with text evidence from the bidset. Then runs
ASSEMBLY_RELATIONSHIPS against the available evidence and reports which
warnings *would have triggered* if pin counts were present.
"""

from __future__ import annotations

import re
from typing import Any

from seeds import roof_assemblies as RA


def pick_assembly_key(system_type: str | None, attachment: str | None) -> str | None:
    """Pick the most-specific ROOF_SYSTEMS key matching the (system_type,
    attachment) pair. Falls back to the first system whose membrane_type
    matches when attachment is missing."""
    if not system_type:
        return None
    candidates: list[tuple[str, dict[str, Any]]] = []
    for key, sys in RA.ROOF_SYSTEMS.items():
        if sys.get("membrane_type") == system_type:
            candidates.append((key, sys))

    if not candidates:
        return None

    if attachment:
        for key, sys in candidates:
            if sys.get("attachment") == attachment:
                return key

    # Default to the most-common attachment we know — mechanically_attached
    # for single-ply, then fully_adhered, else first match.
    for prefer in ("mechanically_attached", "fully_adhered", "torch_applied",
                   "concealed_clip", "nailed", "spray_applied"):
        for key, sys in candidates:
            if sys.get("attachment") == prefer:
                return key

    return candidates[0][0]


# ─────────────────────────────────────────────────────────────────────────────
# Component evidence detection
# ─────────────────────────────────────────────────────────────────────────────

# Component keyword bank — maps a component key to text patterns that count
# as evidence of that component being present in the spec/legend text.
# Drawn from the takeoff_driver descriptions and known industry vocab.
COMPONENT_KEYWORDS: dict[str, list[str]] = {
    "field_membrane":          ["MEMBRANE", "ROOF MEMBRANE"],
    "base_sheet":              ["BASE SHEET", "BASE PLY"],
    "cap_sheet":               ["CAP SHEET", "GRANULATED CAP"],
    "interply_felt":           ["INTERPLY", "PLY FELT"],
    "insulation":              ["INSULATION", "POLYISO", "POLYISOCYANURATE", "EPS", "XPS"],
    "tapered_insulation":      ["TAPERED", "TAPERED INSULATION", "POSITIVE DRAINAGE"],
    "cover_board":             ["COVER BOARD", "DENSDECK", "DENS-DECK", "SECURSHIELD"],
    "vapor_retarder":          ["VAPOR RETARDER", "VAPOR BARRIER"],
    "fasteners":               ["FASTENER", "MECHANICAL FASTENER", "SCREW"],
    "fastener_plates":         ["FASTENER PLATE", "BARBED PLATE", "STRESS PLATE"],
    "membrane_adhesive":       ["BONDING ADHESIVE", "MEMBRANE ADHESIVE", "ADHERED"],
    "ballast":                 ["BALLAST", "STONE BALLAST"],
    "coping":                  ["COPING"],
    "edge_metal":              ["EDGE METAL", "DRIP EDGE", "GRAVEL STOP"],
    "gutter":                  ["GUTTER"],
    "gravel_stop":             ["GRAVEL STOP"],
    "termination_bar":         ["TERMINATION BAR", "TERM BAR"],
    "counterflashing":         ["COUNTERFLASHING", "COUNTER FLASHING"],
    "base_flashing":           ["BASE FLASHING", "FLASHING AT WALL"],
    "reglet":                  ["REGLET"],
    "roof_drain":              ["ROOF DRAIN", "PRIMARY DRAIN"],
    "overflow_drain":          ["OVERFLOW DRAIN", "SECONDARY DRAIN"],
    "scupper":                 ["SCUPPER"],
    "overflow_scupper":        ["OVERFLOW SCUPPER"],
    "downspout":               ["DOWNSPOUT", "LEADER"],
    "drain_flashing":          ["DRAIN FLASHING", "DRAIN BOOT"],
    "sump_receiver":           ["SUMP", "DRAIN SUMP"],
    "pipe_boot":               ["PIPE BOOT", "VENT BOOT", "VTR BOOT"],
    "split_pipe_boot":         ["SPLIT PIPE BOOT", "SPLIT BOOT"],
    "mechanical_curb":         ["MECH CURB", "MECHANICAL CURB", "EQUIPMENT CURB", "RTU CURB"],
    "curb_flashing":           ["CURB FLASHING"],
    "hatch":                   ["ROOF HATCH", "HATCH"],
    "hatch_flashing":          ["HATCH FLASHING"],
    "skylight":                ["SKYLIGHT"],
    "skylight_flashing":       ["SKYLIGHT FLASHING"],
    "walkway_pad":             ["WALK PAD", "WALKWAY PAD", "WALKWAY"],
    "lightning_protection_tie_in": ["LIGHTNING PROTECTION", "LIGHTNING ARRESTER"],
    "expansion_joint_cover":   ["EXPANSION JOINT"],
    "cricket":                 ["CRICKET"],
    "saddle":                  ["SADDLE"],
    "sealant":                 ["SEALANT", "CAULK"],
    "metal_panel":             ["METAL PANEL", "STANDING SEAM"],
    "panel_clip":               ["PANEL CLIP", "CONCEALED CLIP"],
    "panel_closure":           ["PANEL CLOSURE", "CLOSURE STRIP"],
    "ridge_cap":               ["RIDGE CAP"],
    "valley_flashing":         ["VALLEY FLASHING", "VALLEY"],
    "starter_strip":           ["STARTER STRIP", "STARTER COURSE"],
    "underlayment":            ["UNDERLAYMENT", "FELT"],
    "ice_and_water_shield":    ["ICE AND WATER", "SELF-ADHERED MEMBRANE"],
    "step_flashing":           ["STEP FLASHING"],
    "hip_cap":                 ["HIP CAP"],
    "drip_edge":               ["DRIP EDGE"],
}


def find_component_evidence(component_key: str, texts_by_page: dict[int, str]) -> list[dict[str, Any]]:
    """Return per-page evidence pages where this component's keywords appear."""
    keywords = COMPONENT_KEYWORDS.get(component_key, [])
    if not keywords:
        return []
    out: list[dict[str, Any]] = []
    for page_idx, text in texts_by_page.items():
        upper = text.upper()
        for kw in keywords:
            if kw in upper:
                out.append({"page_index": page_idx, "matched_keyword": kw})
                break
    return out


def evaluate_relationships(component_evidence: dict[str, list[dict[str, Any]]],
                           system_attachment: str | None,
                           florida_signals: list[str]) -> list[dict[str, Any]]:
    """Run ASSEMBLY_RELATIONSHIPS rules over what the parser found.

    v0.1 caveat: pin counts aren't available (annotations are user-entered).
    We can only trigger warnings about TEXT-LEVEL evidence (e.g., 'spec
    mentions drains but never overflow drains'). Most rules are
    informational-only at this layer; we report which would FIRE if
    pin counts existed."""
    warnings: list[dict[str, Any]] = []

    has = lambda k: bool(component_evidence.get(k))

    # drainage_exclusivity (text-level)
    if has("roof_drain") and has("scupper"):
        warnings.append({
            "id": "drainage_exclusivity",
            "rule": "A given drainage zone uses drains OR scuppers, not both",
            "trigger_kind": "text_evidence",
            "would_fire_when": "drain_count > 0 AND scupper_count > 0 on same zone",
            "note": "Spec mentions both drains AND scuppers — distinct drainage zones expected; verify on plans",
        })

    # overflow_pairing
    if has("roof_drain") and not has("overflow_drain"):
        warnings.append({
            "id": "overflow_pairing",
            "rule": "Every primary drain must have a paired overflow",
            "trigger_kind": "text_evidence_missing",
            "note": "Spec mentions roof drains but no overflow drains found in text",
        })
    if has("scupper") and not has("overflow_scupper"):
        warnings.append({
            "id": "overflow_pairing",
            "rule": "Every primary scupper must have a paired overflow",
            "trigger_kind": "text_evidence_missing",
            "note": "Spec mentions scuppers but no overflow scuppers found in text",
        })

    # adhesive_requires_cover_board
    if system_attachment == "fully_adhered" and not has("cover_board"):
        warnings.append({
            "id": "adhesive_requires_cover_board",
            "rule": "Fully-adhered single-ply systems require a cover board",
            "trigger_kind": "text_evidence_missing",
            "note": "Attachment is fully_adhered but no cover board mentioned in spec",
        })

    # tapered_insulation_for_drainage
    if (has("roof_drain") or has("scupper")) and not has("tapered_insulation"):
        warnings.append({
            "id": "tapered_insulation_for_drainage",
            "rule": "Flat roofs with drains typically require tapered insulation",
            "trigger_kind": "text_evidence_missing",
            "note": "Drainage present but tapered insulation not mentioned in text",
        })

    # curb_high_side_cricket — pure pin/measurement rule, can't evaluate from text alone.
    # But we can flag it as 'would fire on pin data':
    if has("mechanical_curb"):
        warnings.append({
            "id": "curb_high_side_cricket",
            "rule": "Curbs > 30\" require cricket on high side (IBC 1503.4)",
            "trigger_kind": "would_fire_on_pin_data",
            "note": "Curbs identified — cricket-required check awaits user pin data",
        })

    # rtu_drives_curb
    if has("mechanical_curb") or "RTU" in str(component_evidence):
        warnings.append({
            "id": "rtu_drives_curb",
            "rule": "Each RTU requires a mechanical curb",
            "trigger_kind": "would_fire_on_pin_data",
            "note": "Awaits user pin data for RTUs and curbs",
        })

    # FBC HVHZ surfacing (florida_signals) — turn into informational warnings
    if "HVHZ" in florida_signals or "NOA" in florida_signals:
        warnings.append({
            "id": "fbc_hvhz_applies",
            "rule": "HVHZ/NOA mentioned — Miami-Dade NOA approval required",
            "trigger_kind": "code_constraint",
            "note": "Project references HVHZ or Miami-Dade NOA",
        })

    return warnings


def build_assembly_layer(scope_layer: dict[str, Any],
                         pages: list[Any],
                         classifications: list[dict[str, Any]]) -> dict[str, Any]:
    """For each identified system in scope_layer.systems, build the assembly
    output: matched ROOF_SYSTEMS key, components with evidence, warnings."""
    classmap = {c["page_index"]: c for c in classifications}

    # Build a per-page text map limited to roof-relevant pages so component
    # evidence isn't polluted by unrelated trade specs.
    from scripts._pipeline.scope import ROOF_RELEVANT_PAGE_TYPES
    texts_by_page: dict[int, str] = {}
    for p in pages:
        cls = classmap.get(p.page_index)
        if cls and cls["page_type"] in ROOF_RELEVANT_PAGE_TYPES:
            texts_by_page[p.page_index] = p.full_text or ""

    florida_signals = sorted({
        h["marker"] for h in scope_layer.get("evidence", {}).get("florida_signals", [])
    })

    systems_out: list[dict[str, Any]] = []
    for sys in scope_layer.get("systems", []):
        sys_t = sys.get("system_type")
        attach = sys.get("attachment")
        key = pick_assembly_key(sys_t, attach)
        if not key:
            systems_out.append({
                "system_type": sys_t,
                "attachment": attach,
                "matched_assembly_key": None,
                "supported_components": [],
                "missing_components": [],
                "warnings": [],
                "note": f"No matching ROOF_SYSTEMS entry for system_type={sys_t}",
            })
            continue

        assembly = RA.ROOF_SYSTEMS[key]
        required = list(assembly.get("required_components", []))
        conditional_raw = assembly.get("conditional_components", {})
        conditional = list(conditional_raw.keys()) if isinstance(conditional_raw, dict) else []

        component_evidence: dict[str, list[dict[str, Any]]] = {}
        for comp in required + conditional:
            evidence = find_component_evidence(comp, texts_by_page)
            if evidence:
                component_evidence[comp] = evidence

        supported = [c for c in required if c in component_evidence]
        missing = [c for c in required if c not in component_evidence]
        conditional_supported = [c for c in conditional if c in component_evidence]

        warnings = evaluate_relationships(component_evidence, attach, florida_signals)

        systems_out.append({
            "system_type": sys_t,
            "attachment": attach,
            "manufacturer": sys.get("manufacturer"),
            "matched_assembly_key": key,
            "assembly_category": assembly.get("category"),
            "required_total": len(required),
            "required_supported": len(supported),
            "required_supported_components": supported,
            "required_missing_components": missing,
            "conditional_supported_components": conditional_supported,
            "component_evidence": component_evidence,
            "warnings": warnings,
        })

    return {
        "systems": systems_out,
        "florida_signals": florida_signals,
    }
