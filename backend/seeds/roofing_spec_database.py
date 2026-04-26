"""
Roofing Material Intelligence — reference database.

READ-ONLY reference data consumed by `modules/roofing/vocabulary.py` and
`core/dispatch_gate.py`. No pricing, no supplier info, no business logic.
Facts only: what materials are, how they appear in construction documents,
and what system they belong to.

Adding a new manufacturer or spec section is a dict entry here — never a
code change.
"""

from __future__ import annotations


# --- CSI MasterFormat Division 07 -----------------------------------------

SPEC_SECTIONS: dict[str, dict] = {
    # Section number (with/without spaces) → system type + description.
    # Use the shortest normalized form as the key; matcher normalizes before lookup.
    "07 52": {"system": "built_up", "name": "Built-Up Bituminous Roofing"},
    "07 5200": {"system": "built_up", "name": "Built-Up Bituminous Roofing"},
    "07 52 00": {"system": "built_up", "name": "Built-Up Bituminous Roofing"},

    "07 54": {"system": "tpo", "name": "Thermoplastic Membrane Roofing"},
    "07 5400": {"system": "tpo", "name": "Thermoplastic Membrane Roofing"},
    "07 54 00": {"system": "tpo", "name": "Thermoplastic Membrane Roofing"},
    "07 54 23": {"system": "tpo", "name": "TPO Membrane Roofing"},
    "07 54 19": {"system": "pvc", "name": "PVC Membrane Roofing"},

    "07 55": {"system": "modified_bitumen", "name": "Modified Bituminous Membrane"},
    "07 5500": {"system": "modified_bitumen", "name": "Modified Bituminous Membrane"},
    "07 55 00": {"system": "modified_bitumen", "name": "Modified Bituminous Membrane"},

    "07 61": {"system": "metal_panel", "name": "Sheet Metal Roofing"},
    "07 6100": {"system": "metal_panel", "name": "Sheet Metal Roofing"},
    "07 61 00": {"system": "metal_panel", "name": "Sheet Metal Roofing"},
    "07 61 13": {"system": "metal_panel", "name": "Standing Seam Metal Roofing"},
    "07 61 14": {"system": "metal_panel", "name": "Formed Metal Roofing"},

    "07 31": {"system": "shingle", "name": "Asphalt Shingles"},
    "07 3100": {"system": "shingle", "name": "Asphalt Shingles"},
    "07 31 00": {"system": "shingle", "name": "Asphalt Shingles"},
    "07 31 13": {"system": "shingle", "name": "Asphalt Shingles"},

    "07 41": {"system": "metal_panel", "name": "Metal Roof Panels"},
    "07 4100": {"system": "metal_panel", "name": "Metal Roof Panels"},
    "07 42": {"system": "metal_panel", "name": "Metal Wall Panels"},
    "07 46": {"system": "metal_panel", "name": "Siding"},
    "07 62": {"system": "metal_panel", "name": "Flashing and Sheet Metal"},
    "07 6200": {"system": "metal_panel", "name": "Flashing and Sheet Metal"},

    # Accessory / context-only sections (no system, but confirm roofing scope)
    "07 71": {"system": None, "name": "Roof Specialties"},
    "07 72": {"system": None, "name": "Roof Accessories"},
    "07 84": {"system": None, "name": "Firestopping"},
    "07 92": {"system": None, "name": "Joint Sealants"},

    # Insulation — not a system by itself, but signals flat-roof assembly
    "07 21": {"system": None, "name": "Thermal Insulation", "signal": "flat_roof"},
    "07 2100": {"system": None, "name": "Thermal Insulation", "signal": "flat_roof"},
    "07 22": {"system": None, "name": "Roof and Deck Insulation", "signal": "flat_roof"},
    "07 2200": {"system": None, "name": "Roof and Deck Insulation", "signal": "flat_roof"},
}


# --- Manufacturer database ------------------------------------------------

MANUFACTURERS: dict[str, dict] = {
    "Carlisle": {
        "systems": ["tpo", "pvc", "epdm"],
        "products": {
            "Sure-Weld": "tpo",
            "FleeceBACK": "tpo",
            "Sure-Flex": "pvc",
        },
        "aliases": ["Carlisle SynTec", "Carlisle Coatings", "CSM"],
    },
    "Firestone": {
        "systems": ["epdm", "tpo"],
        "products": {
            "RubberGard": "epdm",
            "UltraPly": "tpo",
        },
        "aliases": ["Firestone Building Products", "FSBP"],
    },
    "GAF": {
        "systems": ["tpo", "modified_bitumen", "shingle", "built_up"],
        "products": {
            "EverGuard": "tpo",
            "EverGuard Extreme": "tpo",
            "Timberline": "shingle",
            "Liberty": "modified_bitumen",
            "Ruberoid": "modified_bitumen",
        },
        "aliases": ["GAF Materials", "GAF Commercial"],
    },
    "Johns Manville": {
        "systems": ["tpo", "epdm", "modified_bitumen", "pvc"],
        "products": {
            "JM TPO": "tpo",
            "JM PVC": "pvc",
            "DynaFlex": "modified_bitumen",
        },
        "aliases": ["JM", "J-M", "Johns-Manville"],
    },
    "Sika Sarnafil": {
        "systems": ["pvc"],
        "products": {
            "Sarnafil": "pvc",
            "Sikaplan": "pvc",
        },
        "aliases": ["Sika", "Sarnafil"],
    },
    "Tremco": {
        "systems": ["tpo", "modified_bitumen", "built_up"],
        "products": {
            "TremPly": "tpo",
            "POWERply": "modified_bitumen",
        },
        "aliases": ["Tremco Roofing", "Tremco Inc"],
    },
    "Versico": {
        "systems": ["tpo", "pvc", "epdm"],
        "products": {
            "VersiFlex": "tpo",
            "VersiWeld": "tpo",
        },
        "aliases": ["Versico Roofing"],
    },
    "IKO": {
        "systems": ["modified_bitumen", "shingle"],
        "products": {
            "Torchflex": "modified_bitumen",
            "Dynasty": "shingle",
            "Cambridge": "shingle",
        },
        "aliases": ["IKO Industries", "IKO Commercial"],
    },
    "CertainTeed": {
        "systems": ["shingle", "modified_bitumen"],
        "products": {
            "Landmark": "shingle",
            "Flintlastic": "modified_bitumen",
        },
        "aliases": ["CertainTeed Roofing", "Saint-Gobain"],
    },
    "ATAS International": {
        "systems": ["metal_panel"],
        "products": {
            "Field-Lok": "metal_panel",
        },
        "aliases": ["ATAS"],
    },
    "MBCI": {
        "systems": ["metal_panel"],
        "products": {
            "BattenLok": "metal_panel",
            "SuperLok": "metal_panel",
        },
        "aliases": ["Metal Building Components"],
    },
    "Berridge": {
        "systems": ["metal_panel"],
        "products": {},
        "aliases": ["Berridge Manufacturing"],
    },
}


# --- Material properties (physical facts only — no pricing) ---------------

MATERIAL_PROPERTIES: dict[str, dict] = {
    "thickness_markers": {
        "45 mil": {"systems": ["tpo", "epdm"], "note": "light-duty single ply"},
        "60 mil": {"systems": ["tpo", "pvc"], "note": "standard commercial single ply"},
        "80 mil": {"systems": ["tpo", "pvc"], "note": "heavy-duty / warranted single ply"},
        "90 mil": {"systems": ["epdm"], "note": "thick EPDM"},
        "115 mil": {"systems": ["epdm"], "note": "extra-thick EPDM"},
    },

    "insulation_markers": {
        "polyiso": {"signal": "flat_roof", "note": "most common commercial insulation"},
        "polyisocyanurate": {"signal": "flat_roof"},
        "EPS": {"signal": "flat_roof", "note": "expanded polystyrene"},
        "XPS": {"signal": "flat_roof", "note": "extruded polystyrene"},
        "R-20": {"signal": "flat_roof"},
        "R-25": {"signal": "flat_roof"},
        "R-30": {"signal": "flat_roof"},
        "R-38": {"signal": "flat_roof"},
        "cover board": {"signal": "flat_roof", "note": "goes over insulation under membrane"},
        "DensDeck": {"signal": "flat_roof", "note": "GP gypsum cover board"},
        "SecurShield": {"signal": "flat_roof", "note": "GP HD insulation"},
    },

    "metal_markers": {
        # Gauge markers removed — coping and edge metal on ANY roof
        # system (TPO, PVC, EPDM, etc.) are specified in gauge, so they
        # are not a system signal.
        "Galvalume": {"systems": ["metal_panel"]},
        "Kynar": {"systems": ["metal_panel"], "note": "PVDF fluoropolymer finish"},
        "PVDF": {"systems": ["metal_panel"]},
    },

    "florida_signals": {
        "HVHZ": {"note": "High Velocity Hurricane Zone — Miami-Dade/Broward"},
        "NOA": {"note": "Notice of Acceptance — Miami-Dade product approval"},
        "FBC": {"note": "Florida Building Code"},
        "TAS": {"note": "Testing Application Standard — Miami-Dade"},
        "FM 1-60": {"note": "Factory Mutual wind uplift rating"},
        "FM 1-90": {"note": "Factory Mutual wind uplift rating"},
        "FM 1-120": {"note": "Factory Mutual wind uplift rating"},
        "FM 1-150": {"note": "Factory Mutual wind uplift rating"},
        "FM Global": {"note": "Factory Mutual approval"},
        "UL 580": {"note": "Wind uplift test standard"},
        "UL 790": {"note": "Fire test standard"},
        "FRSA": {"note": "Florida Roofing & Sheet Metal Association"},
        "NRCA": {"note": "National Roofing Contractors Association"},
        "SMACNA": {"note": "Sheet Metal and Air Conditioning Contractors"},
        "SPRI": {"note": "Single Ply Roofing Industry association"},
    },

    "drawing_conventions": {
        "tpo": {
            "outline": "Single heavy line at roof edge",
            "membrane_fill": "Usually no fill or light stipple",
            "detail_callouts": "07 54, membrane thickness, manufacturer",
        },
        "metal_panel": {
            "outline": "Parallel lines at panel width (12\", 16\", 18\")",
            "seam_lines": "Regularly spaced parallel lines across roof area",
            "detail_callouts": "07 61, gauge, finish, panel profile name",
        },
        "shingle": {
            "outline": "Often shown on elevation views, not plan view",
            "pattern_fill": "Scalloped or staggered pattern fill",
            "detail_callouts": "07 31, manufacturer, style name",
        },
        "modified_bitumen": {
            "outline": "Similar to single ply",
            "detail_callouts": "07 55, base sheet + cap sheet specification",
        },
    },
}


# --- Derived helpers ------------------------------------------------------

def all_manufacturer_names() -> list[tuple[str, str]]:
    """Returns [(search_name, canonical_name), ...] — aliases expanded."""
    pairs: list[tuple[str, str]] = []
    for canonical, data in MANUFACTURERS.items():
        pairs.append((canonical, canonical))
        for alias in data.get("aliases", []):
            pairs.append((alias, canonical))
        for product in data.get("products", {}).keys():
            pairs.append((product, canonical))
    # Sort by length descending so longer (more specific) names match first.
    return sorted(pairs, key=lambda p: -len(p[0]))


def manufacturer_to_systems(canonical: str) -> list[str]:
    return MANUFACTURERS.get(canonical, {}).get("systems", [])


def product_to_system(product: str) -> str | None:
    for data in MANUFACTURERS.values():
        sys = data.get("products", {}).get(product)
        if sys:
            return sys
    return None


def normalize_spec_section(raw: str) -> str:
    """Collapse '07 54 00', '075400', '07-54-00' → '07 54 00'."""
    digits = "".join(c for c in raw if c.isdigit())
    if len(digits) == 6:
        return f"{digits[0:2]} {digits[2:4]} {digits[4:6]}"
    if len(digits) == 4:
        return f"{digits[0:2]} {digits[2:4]}"
    return raw.strip()


def spec_section_to_system(raw: str) -> tuple[str | None, str | None]:
    """Return (system, section_name) for a raw spec section string.

    Tries normalized form, then progressively shorter prefixes.
    """
    norm = normalize_spec_section(raw)
    for key in (norm, norm.replace(" ", ""), norm[:5], norm[:5].replace(" ", "")):
        entry = SPEC_SECTIONS.get(key)
        if entry:
            return entry.get("system"), entry.get("name")
    return None, None
