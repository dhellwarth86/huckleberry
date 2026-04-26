"""
Roofing Materials Reference Database

Source: CLAUDE_CODE_MATERIAL_INTEL_ORDERS.md (April 14, 2026)
Extracted: April 23, 2026

This is reference data, not business logic. It maps what materials
and systems look like in construction documents — spec sections,
manufacturer names, thickness markers, drawing conventions.

No pricing. No supplier data. No mutable state. Read-only reference.

Note: this data was compiled during the TracePoint build with AI
assistance (CSI MasterFormat numbers, published manufacturer lists,
industry-standard thickness markers). Verify against current CSI
MasterFormat and manufacturer product lines before using on a live
bid. Treat as a starting point, not a finished authority.
"""


# ---------------------------------------------------------------------------
# A. CSI MasterFormat spec sections → roofing system type
# ---------------------------------------------------------------------------
SPEC_SECTIONS = {
    # Section number → system type + description
    "07 52":    {"system": "built_up",         "name": "Built-Up Bituminous Roofing"},
    "07 5200":  {"system": "built_up",         "name": "Built-Up Bituminous Roofing"},
    "07 54":    {"system": "tpo",              "name": "Thermoplastic Membrane Roofing"},
    "07 5400":  {"system": "tpo",              "name": "Thermoplastic Membrane Roofing"},
    "07 54 23": {"system": "tpo",              "name": "TPO Membrane Roofing"},
    "07 54 19": {"system": "pvc",              "name": "PVC Membrane Roofing"},
    "07 55":    {"system": "modified_bitumen", "name": "Modified Bituminous Membrane"},
    "07 5500":  {"system": "modified_bitumen", "name": "Modified Bituminous Membrane"},
    "07 61":    {"system": "metal_panel",      "name": "Sheet Metal Roofing"},
    "07 6100":  {"system": "metal_panel",      "name": "Sheet Metal Roofing"},
    "07 61 13": {"system": "metal_panel",      "name": "Standing Seam Metal Roofing"},
    "07 61 14": {"system": "metal_panel",      "name": "Formed Metal Roofing"},
    "07 31":    {"system": "shingle",          "name": "Asphalt Shingles"},
    "07 3100":  {"system": "shingle",          "name": "Asphalt Shingles"},
    "07 31 13": {"system": "shingle",          "name": "Asphalt Shingles"},
    "07 41":    {"system": "metal_panel",      "name": "Metal Roof Panels"},
    "07 42":    {"system": "metal_panel",      "name": "Metal Wall Panels"},   # adjacent trade signal
    "07 46":    {"system": "metal_panel",      "name": "Siding"},
    "07 62":    {"system": "metal_panel",      "name": "Flashing and Sheet Metal"},
    "07 71":    {"system": None,               "name": "Roof Specialties"},    # accessories
    "07 72":    {"system": None,               "name": "Roof Accessories"},
    "07 84":    {"system": None,               "name": "Firestopping"},
    "07 92":    {"system": None,               "name": "Joint Sealants"},

    # Insulation sections (not systems, but confirm flat-roof scope)
    "07 21":    {"system": None, "name": "Thermal Insulation",         "signal": "flat_roof"},
    "07 22":    {"system": None, "name": "Roof and Deck Insulation",   "signal": "flat_roof"},
}


# ---------------------------------------------------------------------------
# B. Manufacturer database
# ---------------------------------------------------------------------------
MANUFACTURERS = {
    # --- TPO / PVC / Single Ply ---
    "Carlisle": {
        "systems":  ["tpo", "pvc", "epdm"],
        "products": {
            "Sure-Weld":    "tpo",
            "FleeceBACK":   "tpo",
            "Sure-Flex":    "pvc",
        },
        "aliases": ["Carlisle SynTec", "Carlisle Coatings", "CSM"],
    },
    "Firestone": {
        "systems":  ["epdm", "tpo"],
        "products": {
            "RubberGard":   "epdm",
            "UltraPly":     "tpo",
        },
        "aliases": ["Firestone Building Products", "FSBP"],
    },
    "GAF": {
        "systems":  ["tpo", "modified_bitumen", "shingle", "built_up"],
        "products": {
            "EverGuard":          "tpo",
            "EverGuard Extreme":  "tpo",
            "Timberline":         "shingle",
            "Liberty":            "modified_bitumen",
            "Ruberoid":           "modified_bitumen",
        },
        "aliases": ["GAF Materials", "GAF Commercial"],
    },
    "Johns Manville": {
        "systems":  ["tpo", "epdm", "modified_bitumen"],
        "products": {
            "JM TPO":       "tpo",
            "JM PVC":       "pvc",
            "DynaFlex":     "modified_bitumen",
        },
        "aliases": ["JM", "J-M", "Johns-Manville"],
    },
    "Sika Sarnafil": {
        "systems":  ["pvc"],
        "products": {
            "Sarnafil":     "pvc",
            "Sikaplan":     "pvc",
        },
        "aliases": ["Sika", "Sarnafil"],
    },
    "Tremco": {
        "systems":  ["tpo", "modified_bitumen", "built_up"],
        "products": {
            "TremPly":      "tpo",
            "POWERply":     "modified_bitumen",
        },
        "aliases": ["Tremco Roofing", "Tremco Inc"],
    },
    "Versico": {
        "systems":  ["tpo", "pvc", "epdm"],
        "products": {
            "VersiFlex":    "tpo",
            "VersiWeld":    "tpo",
        },
        "aliases": ["Versico Roofing"],
    },
    "IKO": {
        "systems":  ["modified_bitumen", "shingle"],
        "products": {
            "Torchflex":    "modified_bitumen",
            "Dynasty":      "shingle",
            "Cambridge":    "shingle",
        },
        "aliases": ["IKO Industries", "IKO Commercial"],
    },
    "CertainTeed": {
        "systems":  ["shingle", "modified_bitumen"],
        "products": {
            "Landmark":     "shingle",
            "Flintlastic":  "modified_bitumen",
        },
        "aliases": ["CertainTeed Roofing", "Saint-Gobain"],
    },
    "ATAS International": {
        "systems":  ["metal_panel"],
        "products": {
            "Field-Lok":    "metal_panel",
        },
        "aliases": ["ATAS"],
    },
    "MBCI": {
        "systems":  ["metal_panel"],
        "products": {
            "BattenLok":    "metal_panel",
            "SuperLok":     "metal_panel",
        },
        "aliases": ["Metal Building Components"],
    },
    "Berridge": {
        "systems":  ["metal_panel"],
        "products": {},
        "aliases": ["Berridge Manufacturing"],
    },
}


# ---------------------------------------------------------------------------
# C. Material properties — physical signals, not pricing
# ---------------------------------------------------------------------------
MATERIAL_PROPERTIES = {
    # Membrane thickness markers → system signals
    "thickness_markers": {
        "45 mil":  {"systems": ["tpo", "epdm"],       "note": "light-duty single ply"},
        "60 mil":  {"systems": ["tpo", "pvc"],        "note": "standard commercial single ply"},
        "80 mil":  {"systems": ["tpo", "pvc"],        "note": "heavy-duty / warranted single ply"},
        "90 mil":  {"systems": ["epdm"],              "note": "thick EPDM"},
        "115 mil": {"systems": ["epdm"],              "note": "extra-thick EPDM"},
    },

    # Insulation types → confirm flat roof
    "insulation_markers": {
        "polyiso":          {"signal": "flat_roof", "note": "most common commercial insulation"},
        "polyisocyanurate": {"signal": "flat_roof"},
        "EPS":              {"signal": "flat_roof", "note": "expanded polystyrene"},
        "XPS":              {"signal": "flat_roof", "note": "extruded polystyrene"},
        "R-20":             {"signal": "flat_roof"},
        "R-25":             {"signal": "flat_roof"},
        "R-30":             {"signal": "flat_roof"},
        "R-38":             {"signal": "flat_roof"},
        "cover board":      {"signal": "flat_roof", "note": "goes over insulation under membrane"},
        "DensDeck":         {"signal": "flat_roof", "note": "GP gypsum cover board"},
        "SecurShield":      {"signal": "flat_roof", "note": "GP HD insulation"},
    },

    # Metal panel markers
    "metal_markers": {
        "24 gauge": {"systems": ["metal_panel"]},
        "24 ga":    {"systems": ["metal_panel"]},
        "22 gauge": {"systems": ["metal_panel"]},
        "22 ga":    {"systems": ["metal_panel"]},
        "26 gauge": {"systems": ["metal_panel"]},
        "Galvalume":{"systems": ["metal_panel"]},
        "Kynar":    {"systems": ["metal_panel"], "note": "PVDF fluoropolymer finish"},
        "PVDF":     {"systems": ["metal_panel"]},
    },

    # Florida-specific signals (scope context, not system types)
    "florida_signals": {
        "HVHZ":      {"note": "High Velocity Hurricane Zone — Miami-Dade/Broward"},
        "NOA":       {"note": "Notice of Acceptance — Miami-Dade product approval"},
        "FBC":       {"note": "Florida Building Code"},
        "TAS":       {"note": "Testing Application Standard — Miami-Dade"},
        "FM 1-60":   {"note": "Factory Mutual wind uplift rating"},
        "FM 1-90":   {"note": "Factory Mutual wind uplift rating"},
        "FM 1-120":  {"note": "Factory Mutual wind uplift rating"},
        "FM 1-150":  {"note": "Factory Mutual wind uplift rating"},
        "FM Global": {"note": "Factory Mutual approval"},
        "UL 580":    {"note": "Wind uplift test standard"},
        "UL 790":    {"note": "Fire test standard"},
        "FRSA":      {"note": "Florida Roofing & Sheet Metal Association"},
        "NRCA":      {"note": "National Roofing Contractors Association"},
        "SMACNA":    {"note": "Sheet Metal and Air Conditioning Contractors"},
        "SPRI":      {"note": "Single Ply Roofing Industry association"},
    },

    # Drawing conventions — how each system tends to appear on plans
    "drawing_conventions": {
        "tpo": {
            "outline":          "Single heavy line at roof edge",
            "membrane_fill":    "Usually no fill or light stipple",
            "detail_callouts":  "07 54, membrane thickness, manufacturer",
        },
        "metal_panel": {
            "outline":          'Parallel lines at panel width (12", 16", 18")',
            "seam_lines":       "Regularly spaced parallel lines across roof area",
            "detail_callouts":  "07 61, gauge, finish, panel profile name",
        },
        "shingle": {
            "outline":          "Often shown on elevation views, not plan view",
            "pattern_fill":     "Scalloped or staggered pattern fill",
            "detail_callouts":  "07 31, manufacturer, style name",
        },
        "modified_bitumen": {
            "outline":          "Similar to single ply",
            "detail_callouts":  "07 55, base sheet + cap sheet specification",
        },
    },
}
