"""
Roof Assemblies Reference Database

Source: Synthesized from the April 14, 2026 four-layer module
discussion, NRCA Roofing Manual, SMACNA Architectural Sheet Metal
Manual, Florida Building Code Chapter 15, and manufacturer
installation guides.

Extracted / compiled: April 23, 2026

PURPOSE
-------
This file is the "assembly map" for commercial roofing systems.
For each system type, it lists the components that make up the
assembly, how those components relate, and what takeoff items
the assembly produces. It is a SHOPPING LIST generator, not a
pricing or quantities generator.

Given: "this plan shows a TPO mechanically attached system."
Produces: "takeoff should include these items, driven by these
measurements, subject to these code constraints."

WHAT IT CONTAINS
----------------
1. ROOF_COMPONENTS — universal vocabulary of roofing parts
   (membrane, insulation, cover board, fasteners, flashings, etc.)
2. ROOF_SYSTEMS — each roofing system mapped to its components
3. ASSEMBLY_RELATIONSHIPS — cross-component rules that apply
   across systems (drain XOR scupper, RTU drives curb count, etc.)
4. FBC_CONSTRAINTS — Florida Building Code constraints that
   affect assembly selection or variant requirements

WHAT IT DOES NOT CONTAIN
------------------------
- Pricing (no dollar amounts anywhere)
- Coverage rates (SF per roll — product-specific, left to estimator)
- Waste factors (company-specific, left to estimator)
- Fastener density numbers (wind-zone and deck-dependent — flagged
  as code-driven, not populated)
- Labor hours (estimator judgment)

HONEST CAVEAT
-------------
The roofing-trade knowledge here was compiled with AI assistance
from public industry references. Daniel is not an estimator and
did not author the relationships. A practicing commercial roofing
estimator should review this file before trusting it on a live
bid. Treat as a starting point for Sean, Jeremy, or another
estimator to correct and extend.

Cross-references to siblings:
- roofing_materials.py: spec sections, manufacturer lists, thickness markers
- dispatch_seed.py: page classification, cross-reference patterns
- This file: assembly structure, takeoff drivers, code constraints
"""


# ===========================================================================
# 1. ROOF_COMPONENTS — universal component vocabulary
#
# Every component used by any roofing system is defined here once.
# Systems reference components by key. This avoids duplication and
# makes it possible to add new systems without duplicating component
# definitions.
# ===========================================================================
ROOF_COMPONENTS = {
    # -------- Field materials (cover the main roof area) --------
    "field_membrane": {
        "role": "Primary waterproofing layer over roof field",
        "takeoff_unit": "SF",
        "takeoff_driver": "roof_area",
        "source": "NRCA Roofing Manual",
    },
    "base_sheet": {
        "role": "First ply in multi-ply systems; provides substrate for cap sheet",
        "takeoff_unit": "SF",
        "takeoff_driver": "roof_area",
        "source": "NRCA; ASTM D4601 / D4897",
    },
    "cap_sheet": {
        "role": "Final ply in multi-ply modified bitumen or BUR systems",
        "takeoff_unit": "SF",
        "takeoff_driver": "roof_area",
        "source": "NRCA; ASTM D6163 / D6164 / D6222",
    },
    "interply_felt": {
        "role": "Intermediate ply in BUR systems (3-ply, 4-ply)",
        "takeoff_unit": "SF",
        "takeoff_driver": "roof_area × ply_count",
        "source": "NRCA",
    },

    # -------- Substrate layers --------
    "insulation": {
        "role": "Thermal resistance (R-value)",
        "takeoff_unit": "SF (per layer) or BF for tapered",
        "takeoff_driver": "roof_area; thickness per FBC-E energy code",
        "source": "NRCA; FBC Energy Conservation; ASHRAE 90.1",
    },
    "tapered_insulation": {
        "role": "Slope for positive drainage to drains/scuppers",
        "takeoff_unit": "SF or BF",
        "takeoff_driver": "roof_area where slope is required; min 1/4\" per foot per code",
        "source": "FBC 1507; IBC 1507.10",
    },
    "cover_board": {
        "role": "Protects insulation from wind uplift and mechanical damage",
        "takeoff_unit": "SF",
        "takeoff_driver": "roof_area",
        "typical_products": ["DensDeck", "SecurShield HD", "gypsum board", "high-density polyiso"],
        "source": "NRCA; FM 4470",
    },
    "vapor_retarder": {
        "role": "Limits moisture migration into insulation (cold-climate or high-humidity)",
        "takeoff_unit": "SF",
        "takeoff_driver": "roof_area (when required)",
        "required_when_note": "Plan / spec driven; not always present in FL",
        "source": "NRCA; ASHRAE",
    },

    # -------- Attachment --------
    "fasteners": {
        "role": "Mechanically anchor insulation and/or membrane to deck",
        "takeoff_unit": "EA",
        "takeoff_driver": "density varies by wind zone, edge/corner vs field, deck type",
        "density_source": "FBC 1504 / TAS 105 / FM 4470; manufacturer wind design tables",
        "note": "Density NOT populated here — code- and job-specific. Left to estimator or wind calc.",
    },
    "fastener_plates": {
        "role": "Load-distribution washers paired 1:1 with fasteners",
        "takeoff_unit": "EA",
        "takeoff_driver": "matches fastener count",
        "typical_products": ["3\" barbed plate", "OMG AccuSeam"],
        "source": "FM 4470; manufacturer",
    },
    "membrane_adhesive": {
        "role": "Bonds fully-adhered membrane to substrate",
        "takeoff_unit": "GAL",
        "takeoff_driver": "roof_area × spread_rate (product-specific)",
        "note": "Spread rate is product-specific — manufacturer install guide required",
        "source": "Manufacturer install guides",
    },
    "ballast": {
        "role": "Holds loose-laid membrane in place (EPDM ballasted systems)",
        "takeoff_unit": "TON or CY",
        "takeoff_driver": "roof_area × ballast_weight_per_sf (code- and zone-dependent)",
        "source": "NRCA; FBC wind tables",
    },

    # -------- Perimeter and edge --------
    "coping": {
        "role": "Caps the top of parapet walls",
        "takeoff_unit": "LF",
        "takeoff_driver": "parapet_perimeter (from roof_perimeter)",
        "source": "SMACNA Architectural Sheet Metal Manual",
    },
    "edge_metal": {
        "role": "Drip edge / gravel stop at roof perimeter where no parapet",
        "takeoff_unit": "LF",
        "takeoff_driver": "portion of roof_perimeter without parapet",
        "source": "SMACNA; ANSI/SPRI ES-1",
    },
    "gutter": {
        "role": "Collects runoff at eave (pitched roofs)",
        "takeoff_unit": "LF",
        "takeoff_driver": "eave_length",
        "source": "SMACNA",
    },
    "gravel_stop": {
        "role": "Raised metal edge retaining gravel/ballast on built-up roofs",
        "takeoff_unit": "LF",
        "takeoff_driver": "roof_perimeter (built-up systems)",
        "source": "SMACNA",
    },
    "termination_bar": {
        "role": "Mechanical termination of single-ply membrane at walls or curbs",
        "takeoff_unit": "LF",
        "takeoff_driver": "vertical_terminations (wall bases, curb tops)",
        "source": "Manufacturer install guides",
    },
    "counterflashing": {
        "role": "Metal flashing over base flashing at walls",
        "takeoff_unit": "LF",
        "takeoff_driver": "wall_base_length",
        "source": "SMACNA; NRCA",
    },
    "base_flashing": {
        "role": "Turn-up of membrane at vertical surfaces (walls, curbs)",
        "takeoff_unit": "LF",
        "takeoff_driver": "wall_base_length + curb_perimeters",
        "source": "NRCA",
    },
    "reglet": {
        "role": "Embedded channel in wall that receives counterflashing",
        "takeoff_unit": "LF",
        "takeoff_driver": "masonry_wall_counterflashing_length",
        "source": "SMACNA",
    },

    # -------- Drainage --------
    "roof_drain": {
        "role": "Primary roof drainage through internal downspouts",
        "takeoff_unit": "EA",
        "takeoff_driver": "count from plan; one per drainage zone per code",
        "source": "FBC Plumbing (FPC) Chapter 11; IPC",
    },
    "overflow_drain": {
        "role": "Secondary drain in case primary is blocked (code-required)",
        "takeoff_unit": "EA",
        "takeoff_driver": "one per drainage zone, typically paired with roof_drain",
        "source": "FBC Plumbing; IPC 1108",
    },
    "scupper": {
        "role": "Through-wall drainage at parapet",
        "takeoff_unit": "EA",
        "takeoff_driver": "count from plan",
        "source": "FBC 1502; SMACNA",
    },
    "overflow_scupper": {
        "role": "Secondary through-wall drain above primary scupper",
        "takeoff_unit": "EA",
        "takeoff_driver": "typically paired with each scupper per code",
        "source": "FBC Plumbing; IPC 1108",
    },
    "downspout": {
        "role": "External drainage from scupper or gutter to grade",
        "takeoff_unit": "LF",
        "takeoff_driver": "roof_height × scupper_or_gutter_outlet_count",
        "source": "SMACNA",
    },
    "drain_flashing": {
        "role": "Waterproof transition at each drain; membrane-specific lead or TPO/PVC target",
        "takeoff_unit": "EA",
        "takeoff_driver": "drain_count + overflow_drain_count",
        "source": "Manufacturer install guides",
    },
    "sump_receiver": {
        "role": "Recessed area around drain for positive drainage",
        "takeoff_unit": "EA",
        "takeoff_driver": "drain_count (where specified)",
        "source": "NRCA",
    },

    # -------- Penetrations --------
    "pipe_boot": {
        "role": "Membrane transition around single pipe penetration",
        "takeoff_unit": "EA",
        "takeoff_driver": "single_pipe_penetration_count (vents, conduits, supports)",
        "source": "Manufacturer install guides",
    },
    "split_pipe_boot": {
        "role": "Membrane transition around paired refrigerant lines from RTU",
        "takeoff_unit": "EA",
        "takeoff_driver": "RTU_count × typical_2.0_to_2.4 (refrigerant + control pair)",
        "source": "Manufacturer; NRCA",
        "note": "Exact multiplier depends on unit config — estimator verifies",
    },
    "mechanical_curb": {
        "role": "Raised curb supporting RTUs, exhaust fans, or hatches",
        "takeoff_unit": "EA",
        "takeoff_driver": "equipment_count_requiring_curb",
        "source": "NRCA; SMACNA",
    },
    "curb_flashing": {
        "role": "Membrane wrap around equipment curb perimeter",
        "takeoff_unit": "LF",
        "takeoff_driver": "sum_of_curb_perimeters",
        "source": "NRCA",
    },
    "hatch": {
        "role": "Roof access hatch for maintenance",
        "takeoff_unit": "EA",
        "takeoff_driver": "count from plan",
        "source": "NRCA",
    },
    "hatch_flashing": {
        "role": "Membrane flashing around hatch curb",
        "takeoff_unit": "LF",
        "takeoff_driver": "hatch_count × hatch_perimeter",
        "source": "NRCA",
    },
    "skylight": {
        "role": "Translucent roof opening",
        "takeoff_unit": "EA",
        "takeoff_driver": "count from plan",
        "source": "NRCA",
    },
    "skylight_flashing": {
        "role": "Membrane flashing around skylight curb",
        "takeoff_unit": "LF",
        "takeoff_driver": "skylight_count × skylight_perimeter",
        "source": "NRCA",
    },

    # -------- Accessories --------
    "walkway_pad": {
        "role": "Protects membrane in service paths and equipment areas",
        "takeoff_unit": "EA or SF",
        "takeoff_driver": "per plan / designer spec",
        "typical_placement": "Hatch to each RTU, around service access zones",
        "source": "NRCA",
    },
    "lightning_protection_tie_in": {
        "role": "Membrane transitions at lightning protection base plates",
        "takeoff_unit": "EA",
        "takeoff_driver": "lightning_protection_base_count (if LP system present)",
        "source": "NFPA 780",
    },
    "expansion_joint_cover": {
        "role": "Bridges building expansion joints at roof",
        "takeoff_unit": "LF",
        "takeoff_driver": "expansion_joint_length",
        "source": "NRCA",
    },
    "cricket": {
        "role": "Tapered triangular insulation diverting water around high-side of curbs",
        "takeoff_unit": "EA or SF",
        "takeoff_driver": "high_side_equipment_count (RTUs, curbs > 30\" wide)",
        "source": "NRCA; IBC 1503.4",
        "note": "Code typically requires crickets on high side of curbs wider than 30\"",
    },
    "saddle": {
        "role": "Tapered insulation between adjacent curbs to route water",
        "takeoff_unit": "EA",
        "takeoff_driver": "between_curb_gap_count",
        "source": "NRCA",
    },
    "sealant": {
        "role": "Joint and termination sealing",
        "takeoff_unit": "TUBE or LF",
        "takeoff_driver": "termination_lf + penetration_count (product-specific)",
        "source": "Manufacturer",
    },

    # -------- Metal roofing specific --------
    "metal_panel": {
        "role": "Primary metal roof covering",
        "takeoff_unit": "SF or SQ",
        "takeoff_driver": "roof_area ÷ panel_coverage",
        "source": "MBCI; MCA metal construction manual",
    },
    "panel_clip": {
        "role": "Attaches standing-seam panels to substrate",
        "takeoff_unit": "EA",
        "takeoff_driver": "panel_count × clips_per_panel (wind-zone dependent)",
        "source": "Manufacturer; FM tables",
    },
    "panel_closure": {
        "role": "Foam or metal closures at panel ends",
        "takeoff_unit": "LF",
        "takeoff_driver": "ridge_length + eave_length",
        "source": "Manufacturer",
    },
    "ridge_cap": {
        "role": "Metal cap over ridge of sloped metal roof",
        "takeoff_unit": "LF",
        "takeoff_driver": "ridge_length",
        "source": "SMACNA",
    },
    "valley_flashing": {
        "role": "Valley waterproofing on pitched roofs",
        "takeoff_unit": "LF",
        "takeoff_driver": "valley_length",
        "source": "SMACNA",
    },

    # -------- Shingle/tile specific --------
    "starter_strip": {
        "role": "Starter course at eaves for shingle/tile roofs",
        "takeoff_unit": "LF",
        "takeoff_driver": "eave_length",
        "source": "NRCA; manufacturer",
    },
    "underlayment": {
        "role": "Secondary waterproofing layer beneath shingles/tile",
        "takeoff_unit": "SF",
        "takeoff_driver": "roof_area",
        "source": "FBC 1507; manufacturer",
    },
    "ice_and_water_shield": {
        "role": "Self-adhered membrane at eaves/valleys (cold climates; some FL zones)",
        "takeoff_unit": "SF",
        "takeoff_driver": "eave_area + valley_area (per code / spec)",
        "source": "FBC 1507; ASTM D1970",
    },
    "step_flashing": {
        "role": "Sidewall flashing stepped up slope on shingle/tile roofs",
        "takeoff_unit": "EA or LF",
        "takeoff_driver": "sidewall_length",
        "source": "SMACNA",
    },
    "hip_cap": {
        "role": "Caps hip lines on shingle/tile roofs",
        "takeoff_unit": "LF",
        "takeoff_driver": "hip_length",
        "source": "Manufacturer",
    },
}


# ===========================================================================
# 2. ROOF_SYSTEMS — each system mapped to its components
#
# Each system entry lists:
#   - category: single_ply / multi_ply / metal / steep_slope / other
#   - attachment: how it's secured (mechanically_attached, fully_adhered, etc.)
#   - required_components: always present in this assembly
#   - conditional_components: present when conditions are met
#   - notes: anything specific to this system
#
# "Required" and "conditional" component keys must match ROOF_COMPONENTS above.
# ===========================================================================
ROOF_SYSTEMS = {
    # ----------------------------------------------------------------------
    # SINGLE-PLY SYSTEMS
    # ----------------------------------------------------------------------
    "tpo_mechanically_attached": {
        "category": "single_ply",
        "membrane_type": "tpo",
        "attachment": "mechanically_attached",
        "description": "TPO single-ply membrane mechanically fastened with plates, over rigid insulation on deck.",
        "spec_sections": ["07 54", "07 54 23"],
        "required_components": [
            "field_membrane",
            "insulation",
            "cover_board",
            "fasteners",
            "fastener_plates",
            "base_flashing",
            "termination_bar",
        ],
        "conditional_components": {
            "tapered_insulation": "when positive drainage required",
            "vapor_retarder": "when specified (rare in FL)",
            "coping": "when parapet present",
            "edge_metal": "when no parapet",
            "roof_drain": "when internal drainage",
            "overflow_drain": "paired with roof_drain per code",
            "scupper": "when parapet drainage",
            "overflow_scupper": "paired with scupper per code",
            "drain_flashing": "per drain",
            "pipe_boot": "per single pipe penetration",
            "split_pipe_boot": "per RTU refrigerant line pair",
            "mechanical_curb": "per RTU/EF/hatch",
            "curb_flashing": "per curb",
            "hatch": "per plan",
            "hatch_flashing": "per hatch",
            "skylight": "per plan",
            "skylight_flashing": "per skylight",
            "walkway_pad": "per plan",
            "cricket": "required on high side of curbs >30\" wide per IBC 1503.4",
            "saddle": "between adjacent curbs",
            "counterflashing": "at wall terminations",
            "sealant": "always",
        },
        "notes": [
            "Most common commercial flat-roof system in Florida",
            "Cover board required for wind uplift performance",
            "Fastener density critical — scales with wind zone",
        ],
    },

    "tpo_fully_adhered": {
        "category": "single_ply",
        "membrane_type": "tpo",
        "attachment": "fully_adhered",
        "description": "TPO single-ply membrane fully adhered to cover board / insulation with bonding adhesive.",
        "spec_sections": ["07 54", "07 54 23"],
        "required_components": [
            "field_membrane",
            "insulation",
            "cover_board",
            "membrane_adhesive",
            "fasteners",
            "fastener_plates",
            "base_flashing",
            "termination_bar",
        ],
        "conditional_components": {
            "tapered_insulation": "when positive drainage required",
            "coping": "when parapet present",
            "edge_metal": "when no parapet",
            "roof_drain": "when internal drainage",
            "overflow_drain": "paired per code",
            "scupper": "when parapet drainage",
            "overflow_scupper": "paired per code",
            "drain_flashing": "per drain",
            "pipe_boot": "per single pipe",
            "split_pipe_boot": "per RTU",
            "mechanical_curb": "per equipment",
            "curb_flashing": "per curb",
            "hatch": "per plan",
            "hatch_flashing": "per hatch",
            "walkway_pad": "per plan",
            "cricket": "per code (curbs >30\")",
            "sealant": "always",
        },
        "notes": [
            "Insulation below is still mechanically attached; membrane is adhered",
            "Higher initial cost, smoother appearance, better for high-wind zones",
        ],
    },

    "pvc_mechanically_attached": {
        "category": "single_ply",
        "membrane_type": "pvc",
        "attachment": "mechanically_attached",
        "description": "PVC single-ply membrane, mechanically fastened, over rigid insulation.",
        "spec_sections": ["07 54 19"],
        "required_components": [
            "field_membrane",
            "insulation",
            "cover_board",
            "fasteners",
            "fastener_plates",
            "base_flashing",
            "termination_bar",
        ],
        "conditional_components": "See tpo_mechanically_attached — same component map",
        "notes": [
            "Chemical-resistant alternative to TPO (restaurants, kitchens)",
            "Typically Sika Sarnafil on commercial; higher cost than TPO",
        ],
    },

    "pvc_fully_adhered": {
        "category": "single_ply",
        "membrane_type": "pvc",
        "attachment": "fully_adhered",
        "description": "PVC single-ply membrane fully adhered to cover board.",
        "spec_sections": ["07 54 19"],
        "required_components": [
            "field_membrane",
            "insulation",
            "cover_board",
            "membrane_adhesive",
            "fasteners",
            "fastener_plates",
            "base_flashing",
            "termination_bar",
        ],
        "conditional_components": "See tpo_fully_adhered — same component map",
    },

    "epdm_mechanically_attached": {
        "category": "single_ply",
        "membrane_type": "epdm",
        "attachment": "mechanically_attached",
        "description": "EPDM rubber single-ply, mechanically fastened with batten bars or plates.",
        "spec_sections": ["07 53"],
        "required_components": [
            "field_membrane",
            "insulation",
            "cover_board",
            "fasteners",
            "fastener_plates",
            "base_flashing",
        ],
        "conditional_components": "See tpo_mechanically_attached — same component map",
        "notes": [
            "Less common in FL commercial; more common in northern climates",
            "EPDM seams require seam tape or adhesive",
        ],
    },

    "epdm_fully_adhered": {
        "category": "single_ply",
        "membrane_type": "epdm",
        "attachment": "fully_adhered",
        "description": "EPDM rubber single-ply fully adhered to substrate.",
        "spec_sections": ["07 53"],
        "required_components": [
            "field_membrane",
            "insulation",
            "cover_board",
            "membrane_adhesive",
            "base_flashing",
        ],
        "conditional_components": "See tpo_fully_adhered — same component map",
    },

    "epdm_ballasted": {
        "category": "single_ply",
        "membrane_type": "epdm",
        "attachment": "ballasted",
        "description": "Loose-laid EPDM held down by stone ballast.",
        "spec_sections": ["07 53"],
        "required_components": [
            "field_membrane",
            "insulation",
            "ballast",
            "base_flashing",
        ],
        "conditional_components": {
            "gravel_stop": "at perimeter to retain ballast",
            "roof_drain": "when internal drainage",
            "walkway_pad": "per plan",
        },
        "notes": [
            "Rare in FL — ballast prohibited in HVHZ and most coastal wind zones",
            "Requires structural capacity for ballast weight (typically 10+ PSF)",
        ],
    },

    # ----------------------------------------------------------------------
    # MULTI-PLY SYSTEMS
    # ----------------------------------------------------------------------
    "modified_bitumen_torched": {
        "category": "multi_ply",
        "membrane_type": "modified_bitumen",
        "attachment": "torch_applied",
        "description": "Two-ply modified bitumen (base + cap) applied by torching to heat-activate adhesive.",
        "spec_sections": ["07 55"],
        "required_components": [
            "base_sheet",
            "cap_sheet",
            "insulation",
            "cover_board",
            "fasteners",
            "fastener_plates",
            "base_flashing",
        ],
        "conditional_components": {
            "tapered_insulation": "when positive drainage required",
            "coping": "when parapet present",
            "edge_metal": "when no parapet",
            "roof_drain": "when internal drainage",
            "drain_flashing": "per drain",
            "pipe_boot": "per single pipe",
            "mechanical_curb": "per equipment",
            "curb_flashing": "per curb",
            "gravel_stop": "optional on granulated cap",
            "sealant": "always",
        },
        "notes": [
            "Open flame — fire watch and insurance requirements apply",
            "Granulated cap sheet provides UV protection and walkability",
        ],
    },

    "modified_bitumen_cold_applied": {
        "category": "multi_ply",
        "membrane_type": "modified_bitumen",
        "attachment": "cold_applied_adhesive",
        "description": "Two-ply modified bitumen installed with cold-applied adhesive (no open flame).",
        "spec_sections": ["07 55"],
        "required_components": [
            "base_sheet",
            "cap_sheet",
            "insulation",
            "cover_board",
            "membrane_adhesive",
            "base_flashing",
        ],
        "conditional_components": "See modified_bitumen_torched — same component map",
        "notes": [
            "Preferred where open flame is prohibited (occupied buildings, sensitive areas)",
        ],
    },

    "modified_bitumen_hot_mopped": {
        "category": "multi_ply",
        "membrane_type": "modified_bitumen",
        "attachment": "hot_mopped_asphalt",
        "description": "Modified bitumen applied in hot asphalt.",
        "spec_sections": ["07 55"],
        "required_components": [
            "base_sheet",
            "cap_sheet",
            "insulation",
            "cover_board",
            "base_flashing",
        ],
        "conditional_components": "See modified_bitumen_torched — same component map",
    },

    "built_up_roofing": {
        "category": "multi_ply",
        "membrane_type": "built_up",
        "attachment": "hot_asphalt_mopped",
        "description": "Traditional BUR: base + 2-3 plies of felt + flood coat and gravel, all hot mopped.",
        "spec_sections": ["07 52"],
        "required_components": [
            "base_sheet",
            "interply_felt",
            "insulation",
            "cover_board",
            "fasteners",
            "base_flashing",
            "gravel_stop",
        ],
        "conditional_components": {
            "tapered_insulation": "when positive drainage required",
            "cap_sheet": "when smooth-surface BUR",
            "coping": "when parapet present",
            "roof_drain": "when internal drainage",
            "drain_flashing": "per drain",
            "pipe_boot": "per single pipe",
            "mechanical_curb": "per equipment",
            "curb_flashing": "per curb",
        },
        "notes": [
            "Declining in new construction; still common in reroof over existing BUR",
            "Ply count (3-ply, 4-ply) drives interply_felt quantity",
        ],
    },

    # ----------------------------------------------------------------------
    # METAL SYSTEMS
    # ----------------------------------------------------------------------
    "metal_panel_standing_seam": {
        "category": "metal",
        "membrane_type": "metal_panel",
        "attachment": "concealed_clip",
        "description": "Standing-seam metal panels attached by concealed clips (no panel penetrations).",
        "spec_sections": ["07 61", "07 61 13", "07 41"],
        "required_components": [
            "metal_panel",
            "panel_clip",
            "underlayment",
            "ridge_cap",
            "panel_closure",
            "valley_flashing",
        ],
        "conditional_components": {
            "insulation": "when thermal performance required (typically yes)",
            "coping": "rare — typically ridge cap instead",
            "gutter": "at eaves",
            "downspout": "paired with gutter",
            "step_flashing": "at sidewalls",
            "skylight": "per plan",
            "skylight_flashing": "per skylight",
            "pipe_boot": "per penetration",
            "sealant": "at panel ends and penetrations",
        },
        "notes": [
            "High wind performance when properly clipped",
            "Gauge: typically 24 or 22 ga for commercial",
            "Finish: Kynar/PVDF for 20+ year warranty",
        ],
    },

    "metal_panel_screw_down": {
        "category": "metal",
        "membrane_type": "metal_panel",
        "attachment": "exposed_fastener",
        "description": "R-panel or similar ribbed metal with exposed fasteners through the panel.",
        "spec_sections": ["07 41"],
        "required_components": [
            "metal_panel",
            "fasteners",
            "underlayment",
            "ridge_cap",
            "panel_closure",
        ],
        "conditional_components": "See metal_panel_standing_seam",
        "notes": [
            "Lower cost than standing seam; shorter warranty (exposed fastener gaskets degrade)",
            "Common in agricultural, industrial, back-of-house applications",
        ],
    },

    # ----------------------------------------------------------------------
    # STEEP-SLOPE SYSTEMS
    # ----------------------------------------------------------------------
    "asphalt_shingles": {
        "category": "steep_slope",
        "membrane_type": "shingle",
        "attachment": "nailed",
        "description": "Asphalt composition shingles over underlayment on pitched roof.",
        "spec_sections": ["07 31", "07 31 13"],
        "required_components": [
            "field_membrane",  # shingles
            "underlayment",
            "starter_strip",
            "fasteners",
            "ridge_cap",
            "valley_flashing",
            "step_flashing",
            "drip_edge",  # functionally edge_metal
        ],
        "conditional_components": {
            "ice_and_water_shield": "at eaves and valleys per code",
            "hip_cap": "on hip roofs",
            "pipe_boot": "per penetration",
            "skylight": "per plan",
            "skylight_flashing": "per skylight",
        },
        "notes": [
            "Steep slope only (pitch >= 2:12 per most manufacturer warranties)",
            "Florida: architectural (dimensional) shingles standard; 3-tab rare",
            "HVHZ: requires impact rating and enhanced nailing pattern",
        ],
    },

    "tile_concrete": {
        "category": "steep_slope",
        "membrane_type": "tile",
        "attachment": "mortar_or_foam_or_mechanical",
        "description": "Concrete tile on battens or adhesive, common in Florida.",
        "spec_sections": ["07 32"],
        "required_components": [
            "field_membrane",  # tile
            "underlayment",
            "starter_strip",
            "ridge_cap",
            "valley_flashing",
        ],
        "conditional_components": {
            "ice_and_water_shield": "full coverage common in FL",
            "fasteners": "mechanical attachment",
            "membrane_adhesive": "foam-adhesive installations",
            "hip_cap": "on hip roofs",
            "pipe_boot": "per penetration",
        },
        "notes": [
            "Common Florida residential / light commercial",
            "HVHZ: Miami-Dade NOA product approval required",
            "Heavy — requires structural capacity (15+ PSF)",
        ],
    },

    # ----------------------------------------------------------------------
    # OTHER
    # ----------------------------------------------------------------------
    "spray_polyurethane_foam": {
        "category": "other",
        "membrane_type": "spf",
        "attachment": "spray_applied",
        "description": "Sprayed polyurethane foam with elastomeric coating; monolithic system.",
        "spec_sections": ["07 57"],
        "required_components": [
            "field_membrane",  # SPF acts as both insulation and membrane
            "sealant",
        ],
        "conditional_components": {
            "cover_board": "rare — SPF typically sprayed direct to deck",
            "coping": "when parapet present",
            "edge_metal": "when no parapet",
            "roof_drain": "when internal drainage",
            "drain_flashing": "per drain",
            "pipe_boot": "per penetration (foam-embedded)",
        },
        "notes": [
            "Reroof-friendly — can spray over existing roof if sound",
            "Coating is wear layer — recoat typically every 10-15 years",
            "Sensitive to weather during application (humidity, wind)",
        ],
    },
}


# ===========================================================================
# 3. ASSEMBLY_RELATIONSHIPS — cross-component rules
#
# These are universal rules that apply across roofing systems. They
# catch common takeoff errors and inconsistencies regardless of which
# system is on the plan.
# ===========================================================================
ASSEMBLY_RELATIONSHIPS = [
    {
        "id": "drainage_exclusivity",
        "rule": "A given drainage zone uses drains OR scuppers, not both",
        "triggers_warning_when": "drain_count > 0 AND scupper_count > 0 on same drainage zone",
        "why": "Drains and scuppers serve the same function; simultaneous presence usually indicates miscounted or mixed-zone plan",
        "exceptions": ["Large roofs with multiple drainage zones (each zone one or the other)"],
        "source": "Commercial roofing convention; NRCA",
    },
    {
        "id": "overflow_pairing",
        "rule": "Every primary drain or scupper must have a paired overflow",
        "triggers_warning_when": "drain_count != overflow_drain_count OR scupper_count != overflow_scupper_count",
        "why": "Code requires secondary drainage in case primary is blocked",
        "source": "FBC Plumbing / IPC 1108",
    },
    {
        "id": "rtu_drives_curb",
        "rule": "Each RTU requires a mechanical curb",
        "triggers_warning_when": "rtu_count > 0 AND mechanical_curb_count < rtu_count",
        "why": "RTUs sit on curbs; curb count should match RTU count plus other curbed equipment",
        "source": "NRCA",
    },
    {
        "id": "rtu_drives_split_boots",
        "rule": "Each RTU typically requires 2.0-2.4 split pipe boots",
        "triggers_warning_when": "split_pipe_boot_count not in [2.0×rtu, 2.4×rtu]",
        "why": "Refrigerant + suction line pair, occasionally plus control conduit",
        "exceptions": ["Electric units without refrigerant lines", "Hydronic units"],
        "source": "NRCA; HVAC industry convention",
    },
    {
        "id": "curb_requires_flashing",
        "rule": "Every curb needs curb flashing",
        "triggers_warning_when": "mechanical_curb_count > 0 AND curb_flashing_lf == 0",
        "why": "Curb flashing is the membrane transition around the curb perimeter",
        "source": "NRCA",
    },
    {
        "id": "curb_high_side_cricket",
        "rule": "Curbs wider than 30\" require a cricket on their high (uphill) side",
        "triggers_warning_when": "wide_curb_count > 0 AND cricket_count < wide_curb_count",
        "why": "Without cricket, water ponds against high side of curb",
        "source": "IBC 1503.4; NRCA",
    },
    {
        "id": "perimeter_coverage_balance",
        "rule": "coping_lf + edge_metal_lf + gutter_lf should ≈ roof_perimeter",
        "triggers_warning_when": "sum of those three LF values differs from perimeter by more than ~10%",
        "why": "Building perimeter must be closed by some edge treatment everywhere",
        "exceptions": ["Tie-in to adjacent higher structure (counterflashing covers that segment)"],
        "source": "SMACNA",
    },
    {
        "id": "fasteners_pair_plates_1to1",
        "rule": "fastener_count == fastener_plate_count",
        "triggers_warning_when": "mismatch",
        "why": "Every mechanical fastener through membrane/insulation pairs with one plate",
        "source": "Manufacturer install standard",
    },
    {
        "id": "adhesive_requires_cover_board",
        "rule": "Fully-adhered single-ply systems require a cover board to bond to",
        "triggers_warning_when": "attachment == 'fully_adhered' AND cover_board absent",
        "why": "Adhesive bond to raw polyiso insulation is unreliable; cover board provides bondable substrate",
        "source": "Manufacturer install guides",
    },
    {
        "id": "penetration_needs_flashing",
        "rule": "Every penetration needs a flashing component",
        "triggers_warning_when": "single_pipe_penetrations > 0 AND pipe_boot_count == 0",
        "why": "Unflashed penetrations leak; obvious but commonly missed line on takeoff",
        "source": "NRCA",
    },
    {
        "id": "tapered_insulation_for_drainage",
        "rule": "Flat roofs drained to interior drains typically require tapered insulation",
        "triggers_warning_when": "flat_roof AND interior_drains AND tapered_insulation absent",
        "why": "Code requires positive drainage (min 1/4\" per foot slope)",
        "source": "FBC 1507; IBC 1507.10",
    },
    {
        "id": "walkway_pad_coverage",
        "rule": "Expected: walkway pad path from hatch to each RTU and around service zones",
        "triggers_warning_when": "rtu_count > 0 AND walkway_pad_sf == 0 AND hatch_present",
        "why": "Protects membrane from foot traffic; typical spec requirement",
        "exceptions": ["Ballasted systems", "Systems with integral walkway spec"],
        "source": "NRCA; spec convention",
    },
]


# ===========================================================================
# 4. FBC_CONSTRAINTS — Florida Building Code considerations
#
# FBC is the governing code for Florida commercial roofing. These
# constraints modify assembly selection, component requirements, or
# approval process. They are NOT pricing — they are code-driven
# requirements that must be reflected in the takeoff.
# ===========================================================================
FBC_CONSTRAINTS = {
    "hvhz": {
        "name": "High Velocity Hurricane Zone",
        "applies_to": ["Miami-Dade County", "Broward County"],
        "requirements": [
            "All roofing products must carry a Miami-Dade Notice of Acceptance (NOA)",
            "Ballasted systems prohibited",
            "Enhanced fastener density at perimeter and corners",
            "Impact-rated skylights and hatches required",
        ],
        "source": "FBC HVHZ sections; Miami-Dade Building Code Compliance Office",
    },
    "wind_zones": {
        "name": "Wind speed design zones",
        "note": "FBC uses ASCE 7 wind speed maps. Design wind speed affects fastener density, edge securement, and ballast eligibility.",
        "typical_florida_range_mph": "140 - 200",
        "impacts": [
            "Fastener density (wind uplift design)",
            "Edge securement per ANSI/SPRI ES-1",
            "Ballast prohibited above certain wind speeds",
            "Membrane thickness and manufacturer wind approval ratings",
        ],
        "source": "FBC; ASCE 7; FM 4474 / FM 4470",
    },
    "positive_drainage": {
        "name": "Positive drainage requirement",
        "requirement": "Flat roofs must have minimum 1/4\" per foot slope to drainage points",
        "impacts": [
            "Tapered insulation typically required on flat roofs",
            "Affects drain count and placement",
            "Drives cricket/saddle requirements at equipment",
        ],
        "source": "FBC 1507; IBC 1507.10",
    },
    "secondary_drainage": {
        "name": "Overflow drainage required",
        "requirement": "Every drainage zone must have secondary (overflow) drainage",
        "impacts": [
            "Overflow drain paired with each primary drain",
            "Overflow scupper paired with each primary scupper",
            "Overflow typically 2\" above primary",
        ],
        "source": "FBC Plumbing; IPC 1108",
    },
    "edge_securement": {
        "name": "Perimeter edge securement",
        "requirement": "Metal edge must be tested and approved per ANSI/SPRI ES-1",
        "impacts": [
            "Edge metal gauge and fastener spacing driven by wind zone",
            "Coping wind rating required",
            "SMACNA standards applied",
        ],
        "source": "ANSI/SPRI ES-1; FBC",
    },
    "reroof_specific": {
        "name": "Reroof constraints",
        "requirement": "Reroof (tear-off vs recover) governed by FBC Existing Building chapter",
        "impacts": [
            "Recover allowed only once; second recover requires tear-off",
            "Deck inspection required after tear-off",
            "Existing insulation evaluation required for recover",
        ],
        "source": "Florida Existing Building Code Chapter 15; FBC 706",
    },
    "energy_code": {
        "name": "Insulation R-value",
        "requirement": "Minimum R-value per FBC Energy Conservation / ASHRAE 90.1 climate zone",
        "florida_climate_zones": "1A (Miami area), 2A (most of peninsula), 2B (panhandle)",
        "impacts": [
            "Minimum insulation thickness on re-insulation",
            "Recover systems: existing + new must meet current R-value",
        ],
        "source": "FBC Energy Conservation; ASHRAE 90.1",
    },
    "fire_rating": {
        "name": "Roof fire classification",
        "requirement": "Class A, B, or C assembly per occupancy and code",
        "impacts": [
            "Affects cover board requirement (gypsum cover for Class A)",
            "Limits eligible insulation types",
            "Ballasted rock typically achieves Class A by default",
        ],
        "source": "FBC Chapter 15; UL 790; ASTM E108",
    },
    "impact_rating": {
        "name": "Hail / debris impact rating",
        "requirement": "UL 2218 Class 1-4 impact rating may be specified",
        "impacts": [
            "Modified bitumen cap sheets and metal panels carry impact ratings",
            "Skylights and translucent roof elements need impact approval in HVHZ",
        ],
        "source": "UL 2218; FBC HVHZ",
    },
}


# ===========================================================================
# USAGE SKETCH
#
# module = identify_roof_system(plan_text)  # returns "tpo_mechanically_attached"
# assembly = ROOF_SYSTEMS[module]
# required = [ROOF_COMPONENTS[c] for c in assembly["required_components"]]
# for component in required:
#     takeoff.add_item(
#         name=component_name,
#         unit=component["takeoff_unit"],
#         driver=component["takeoff_driver"],
#         quantity=None,  # estimator fills this in, possibly assisted by geometry
#     )
#
# for rule in ASSEMBLY_RELATIONSHIPS:
#     if rule_triggers_on(takeoff, rule):
#         takeoff.add_warning(rule["id"], rule["rule"])
#
# for constraint in FBC_CONSTRAINTS.values():
#     if constraint_applies_to(project, constraint):
#         takeoff.add_code_note(constraint["name"])
# ===========================================================================
