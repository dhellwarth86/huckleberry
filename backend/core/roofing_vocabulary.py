"""
Roofing vocabulary — the semi-training knowledge base.

This is DATA, not code. Adding a new roof system = one `systems` entry.
Adding a new takeoff item = one `items` entry. Adding a relationship
rule = one `rules` entry. No code changes needed.

Organised into three sections:
  1. `systems`  — roof system types (TPO, PVC, EPDM, mod-bit, metal, shingle).
                  Each system has keywords (how we detect it from legends /
                  notes) and `typical_items` (what usually appears in a
                  takeoff for that system).
  2. `items`    — every takeoff line item the module knows about. Each
                  item declares its display_name, unit, how to derive its
                  quantity (`derive_from`), the keywords to search for in
                  text, and a base confidence.
  3. `rules`    — relationship warnings applied after scope is built
                  (drain density, cricket vs AC units, etc.).

The roofing module reads this dict; it is otherwise agnostic to what
items exist.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# SYSTEMS — how we recognise a roof assembly and what typically ships with it
# ---------------------------------------------------------------------------

SYSTEMS: dict[str, dict] = {
    "tpo": {
        "display_name": "TPO Single Ply",
        "keywords": [
            # Direct
            "TPO", "THERMOPLASTIC", "SINGLE PLY", "SINGLE-PLY",
            "THERMOPLASTIC POLYOLEFIN",
            # Spec sections
            "07 54", "07 54 00", "07 54 23", "075400", "075423",
            # Manufacturers + product lines
            "CARLISLE", "CARLISLE SYNTEC", "SURE-WELD", "SUREWELD",
            "FLEECEBACK", "FLEECE BACK",
            "FIRESTONE", "ULTRAPLY",
            "GAF", "EVERGUARD",
            "JOHNS MANVILLE", "JM TPO",
            "VERSICO", "VERSIFLEX", "VERSIWELD",
            "TREMCO", "TREMPLY",
            # Thickness markers (TPO is the usual single-ply when unqualified)
            "60 MIL", "80 MIL", "45 MIL",
            # Standards / associations
            "SPRI",
        ],
        "typical_items": [
            "membrane_area", "edge_metal", "coping", "drains", "scuppers",
            "insulation", "cover_board", "walkway_pads", "curbs", "hatches",
            "pipe_boots", "exhaust_fans", "rtus", "cricket",
        ],
    },
    "pvc": {
        "display_name": "PVC Single Ply",
        "keywords": [
            # Direct
            "PVC", "POLYVINYL", "POLYVINYL CHLORIDE",
            # Spec sections
            "07 54 19", "075419",
            # Manufacturers + products
            "SIKA SARNAFIL", "SARNAFIL", "SIKA", "SIKAPLAN",
            "SURE-FLEX", "SUREFLEX",
            "JM PVC",
        ],
        "typical_items": [
            "membrane_area", "edge_metal", "coping", "drains", "scuppers",
            "insulation", "cover_board", "walkway_pads", "curbs", "hatches",
            "pipe_boots", "exhaust_fans", "rtus", "cricket",
        ],
    },
    "epdm": {
        "display_name": "EPDM Rubber",
        "keywords": [
            "EPDM", "RUBBER ROOF", "ETHYLENE PROPYLENE",
            # Manufacturers + products
            "RUBBERGARD",
            # Thick EPDM
            "90 MIL", "115 MIL",
        ],
        "typical_items": [
            "membrane_area", "edge_metal", "drains", "insulation",
            "cover_board", "curbs", "hatches", "pipe_boots", "cricket",
        ],
    },
    "modified_bitumen": {
        "display_name": "Modified Bitumen",
        "keywords": [
            # Direct
            "MODIFIED BITUMEN", "MOD BIT", "MOD-BIT", "SBS", "APP",
            "TORCH APPLIED", "TORCH-APPLIED",
            # Spec sections
            "07 55", "07 55 00", "075500",
            "07 52", "07 52 00", "075200",  # Built-up — treated as mod-bit family
            # Manufacturers + products
            "LIBERTY", "RUBEROID",      # GAF
            "POWERPLY",                  # Tremco
            "DYNAFLEX",                  # JM
            "TORCHFLEX",                 # IKO
            "FLINTLASTIC",               # CertainTeed
            # Legacy BUR keywords (merge into mod-bit family scope)
            "BUILT-UP", "BUR", "BUILT UP ROOF",
        ],
        "typical_items": [
            "base_sheet_area", "cap_sheet_area", "flashing", "cant_strip",
            "drains", "scuppers", "pitch_pans", "insulation", "curbs",
            "hatches", "pipe_boots", "cricket",
        ],
    },
    "built_up": {
        "display_name": "Built-Up Roofing",
        "keywords": [
            "BUILT-UP BITUMINOUS", "BUILT UP BITUMINOUS",
            "07 52", "07 52 00", "075200",
        ],
        "typical_items": [
            "base_sheet_area", "cap_sheet_area", "flashing", "cant_strip",
            "drains", "scuppers", "pitch_pans", "insulation", "curbs",
            "hatches", "pipe_boots", "cricket",
        ],
    },
    "metal_panel": {
        "display_name": "Standing Seam Metal",
        "keywords": [
            # Direct
            "STANDING SEAM", "METAL PANEL", "METAL ROOF",
            "CONCEALED FASTENER", "EXPOSED FASTENER",
            # Spec sections
            "07 61", "07 61 13", "07 61 14", "07 61 00",
            "076113", "076100",
            "07 41", "07 41 00", "074100",
            "07 62", "07 62 00", "076200",
            # Manufacturers + products
            "MBCI", "BATTENLOK", "SUPERLOK",
            "BERRIDGE", "ATAS", "FIELD-LOK",
            # Finishes / substrate (gauge markers removed — coping and
            # edge metal on any roof system are specified in gauge)
            "GALVALUME", "KYNAR", "PVDF",
            "CONCEALED FASTENER", "EXPOSED FASTENER",
        ],
        "typical_items": [
            "panel_area", "ridge_cap", "hip_cap", "valley", "gutter",
            "downspout", "clips", "flashing", "trim",
        ],
    },
    "shingle": {
        "display_name": "Asphalt Shingle",
        "keywords": [
            # Direct
            "SHINGLE", "ASPHALT SHINGLE", "ARCHITECTURAL SHINGLE",
            "3-TAB", "LAMINATED SHINGLE",
            # Spec sections
            "07 31", "07 31 00", "07 31 13", "073100", "073113",
            # Manufacturers + products
            "TIMBERLINE", "LANDMARK", "DYNASTY", "CAMBRIDGE",
            "CERTAINTEED", "GAF TIMBERLINE",
        ],
        "typical_items": [
            "shingle_squares", "ridge_cap", "hip_cap", "valley",
            "starter_strip", "drip_edge", "ice_water_shield",
            "felt_underlayment", "gutter", "downspout",
        ],
    },
}


# ---------------------------------------------------------------------------
# Cross-system signals — narrow scope to flat vs steep even when a specific
# system isn't identified. Used when no SYSTEMS keyword hits.
# ---------------------------------------------------------------------------

FLAT_ROOF_SIGNALS: list[str] = [
    "POLYISO", "POLYISOCYANURATE", "COVER BOARD", "DENSDECK",
    "DENS DECK", "SECURSHIELD",
    "ROOF DRAIN", "SCUPPER", "WALKWAY PAD", "ROOF HATCH",
    "TAPERED INSULATION", "CRICKETS", "CRICKET",
    "07 21", "07 22", "072100", "072200",
]

STEEP_ROOF_SIGNALS: list[str] = [
    "RIDGE CAP", "HIP CAP", "VALLEY", "STARTER STRIP",
    "DRIP EDGE", "ICE AND WATER", "ICE & WATER",
    "FELT UNDERLAYMENT",
    "GUTTER", "DOWNSPOUT",
]


# ---------------------------------------------------------------------------
# ITEMS — every known takeoff line item
# ---------------------------------------------------------------------------

# derive_from values:
#   "polygon_area"           → value = polygon SF
#   "polygon_area_div_100"   → value = polygon SF / 100 (roofing squares)
#   "polygon_perimeter"      → value = polygon LF
#   "callout_count"          → value = count of keyword matches inside polygon
#   "manual"                 → value = None (estimator fills in)

ITEMS: dict[str, dict] = {
    # --- Universal flat-roof items ---
    "membrane_area": {
        "display_name": "Roof Membrane",
        "unit": "SF",
        "derive_from": "polygon_area",
        "confidence": 0.9,
        "keywords": [],  # derived from geometry, not text
    },
    "edge_metal": {
        "display_name": "Edge Metal",
        "unit": "LF",
        "derive_from": "polygon_perimeter",
        "confidence": 0.7,
        "keywords": [
            "EDGE METAL", "DRIP EDGE", "GRAVEL STOP", "FASCIA",
        ],
    },
    "coping": {
        "display_name": "Coping",
        "unit": "LF",
        "derive_from": "polygon_perimeter",
        "confidence": 0.6,
        "keywords": ["COPING", "METAL COPING", "PREFINISHED COPING"],
    },
    "drains": {
        "display_name": "Roof Drains",
        "unit": "EA",
        "derive_from": "callout_count",
        "confidence": 0.5,
        "keywords": ["ROOF DRAIN", "OVERFLOW DRAIN", "DRAIN", "RD"],
    },
    "scuppers": {
        "display_name": "Scuppers",
        "unit": "EA",
        "derive_from": "callout_count",
        "confidence": 0.5,
        "keywords": [
            "OVERFLOW SCUPPER", "SCUPPER", "THRU-WALL SCUPPER",
            "THRU WALL SCUPPER",
        ],
    },
    "rtus": {
        "display_name": "Rooftop Units / RTUs",
        "unit": "EA",
        "derive_from": "callout_count",
        "confidence": 0.5,
        "keywords": ["ROOFTOP UNIT", "RTU", "AHU", "AIR HANDLING"],
    },
    "curbs": {
        # G.5a CP4.1 (Daniel 2026-05-08): curbs are unspecified-size
        # equipment enclosures that need polygon-traced area, not pin
        # counts. unit changed EA -> SF + derive_from changed
        # callout_count -> manual. Frontend palette routing now sends
        # curbs to polygonTypes (SF). Estimator still places one polygon
        # per curb on the canvas.
        "display_name": "Equipment Curbs",
        "unit": "SF",
        "derive_from": "manual",
        "confidence": 0.5,
        "keywords": [
            "EQUIPMENT CURB", "MECH CURB", "MECHANICAL CURB", "CURB",
        ],
    },
    "walkway_pads": {
        "display_name": "Walkway Pads",
        "unit": "LF",
        "derive_from": "manual",      # LF auto from counting is unreliable
        "confidence": 0.0,
        "keywords": ["WALKWAY", "WALK PAD", "ROOF WALKWAY"],
    },
    "insulation": {
        "display_name": "Insulation",
        "unit": "SF",
        "derive_from": "polygon_area",
        "confidence": 0.6,
        "keywords": [
            "POLYISO", "INSULATION", "ISO BOARD", "EPS", "XPS",
            "RIGID INSULATION", "TAPERED INSULATION", "R-VALUE",
        ],
    },
    "cover_board": {
        "display_name": "Cover Board",
        "unit": "SF",
        "derive_from": "polygon_area",
        "confidence": 0.5,
        "keywords": ["COVER BOARD", "COVERBOARD", "GYPSUM BOARD", "DENSDECK"],
    },
    "hatches": {
        "display_name": "Roof Hatches",
        "unit": "EA",
        "derive_from": "callout_count",
        "confidence": 0.5,
        "keywords": ["ROOF HATCH", "HATCH", "ACCESS HATCH"],
    },
    "pipe_boots": {
        "display_name": "Pipe Boots / Vents",
        "unit": "EA",
        "derive_from": "callout_count",
        "confidence": 0.4,
        "keywords": [
            "PIPE BOOT", "PLUMBING VENT", "VENT THROUGH ROOF",
            "VTR", "VENT",
        ],
    },
    "exhaust_fans": {
        "display_name": "Exhaust Fans",
        "unit": "EA",
        "derive_from": "callout_count",
        "confidence": 0.5,
        "keywords": ["EXHAUST FAN", "EF-", "EF"],
    },
    "skylights": {
        "display_name": "Skylights",
        "unit": "EA",
        "derive_from": "callout_count",
        "confidence": 0.5,
        "keywords": ["SKYLIGHT", "SKY LIGHT"],
    },

    # --- Modified bitumen / built-up specific ---
    "base_sheet_area": {
        "display_name": "Base Sheet",
        "unit": "SF",
        "derive_from": "polygon_area",
        "confidence": 0.8,
        "keywords": ["BASE SHEET", "BASE PLY"],
    },
    "cap_sheet_area": {
        "display_name": "Cap Sheet",
        "unit": "SF",
        "derive_from": "polygon_area",
        "confidence": 0.8,
        "keywords": ["CAP SHEET", "CAP PLY"],
    },
    "flashing": {
        "display_name": "Flashing",
        "unit": "LF",
        "derive_from": "manual",
        "confidence": 0.0,
        "keywords": [
            "FLASHING", "BASE FLASHING", "COUNTERFLASHING",
            "COUNTER FLASHING", "STEP FLASHING",
        ],
    },
    "cant_strip": {
        "display_name": "Cant Strip",
        "unit": "LF",
        "derive_from": "polygon_perimeter",
        "confidence": 0.5,
        "keywords": ["CANT STRIP", "CANT"],
    },
    "pitch_pans": {
        "display_name": "Pitch Pans",
        "unit": "EA",
        "derive_from": "callout_count",
        "confidence": 0.4,
        "keywords": ["PITCH PAN", "PITCH POCKET"],
    },

    # --- Metal panel specific ---
    "panel_area": {
        "display_name": "Metal Panels",
        "unit": "SF",
        "derive_from": "polygon_area",
        "confidence": 0.8,
        "keywords": ["STANDING SEAM", "METAL PANEL"],
    },
    "ridge_cap": {
        "display_name": "Ridge Cap",
        "unit": "LF",
        "derive_from": "manual",
        "confidence": 0.0,
        "keywords": ["RIDGE CAP", "RIDGE"],
    },
    "hip_cap": {
        "display_name": "Hip Cap",
        "unit": "LF",
        "derive_from": "manual",
        "confidence": 0.0,
        "keywords": ["HIP CAP", "HIP"],
    },
    "valley": {
        "display_name": "Valley",
        "unit": "LF",
        "derive_from": "manual",
        "confidence": 0.0,
        "keywords": ["VALLEY"],
    },
    "gutter": {
        "display_name": "Gutters",
        "unit": "LF",
        "derive_from": "manual",
        "confidence": 0.0,
        "keywords": ["GUTTER", "BOX GUTTER"],
    },
    "downspout": {
        "display_name": "Downspouts",
        "unit": "EA",
        "derive_from": "callout_count",
        "confidence": 0.5,
        "keywords": ["DOWNSPOUT", "LEADER", "DS-"],
    },
    "clips": {
        "display_name": "Panel Clips",
        "unit": "EA",
        "derive_from": "manual",
        "confidence": 0.0,
        "keywords": ["CLIP", "PANEL CLIP"],
    },
    "trim": {
        "display_name": "Trim",
        "unit": "LF",
        "derive_from": "manual",
        "confidence": 0.0,
        "keywords": ["TRIM", "METAL TRIM"],
    },

    # --- Shingle specific ---
    "shingle_squares": {
        "display_name": "Shingles",
        "unit": "SQ",
        "derive_from": "polygon_area_div_100",
        "confidence": 0.8,
        "keywords": ["SHINGLE"],
    },
    "starter_strip": {
        "display_name": "Starter Strip",
        "unit": "LF",
        "derive_from": "polygon_perimeter",
        "confidence": 0.5,
        "keywords": ["STARTER STRIP", "STARTER"],
    },
    "drip_edge": {
        "display_name": "Drip Edge",
        "unit": "LF",
        "derive_from": "polygon_perimeter",
        "confidence": 0.6,
        "keywords": ["DRIP EDGE"],
    },
    "ice_water_shield": {
        "display_name": "Ice & Water Shield",
        "unit": "SF",
        "derive_from": "manual",
        "confidence": 0.0,
        "keywords": ["ICE AND WATER", "ICE & WATER", "ICE WATER SHIELD"],
    },
    "felt_underlayment": {
        "display_name": "Felt Underlayment",
        "unit": "SF",
        "derive_from": "polygon_area",
        "confidence": 0.6,
        "keywords": ["FELT", "UNDERLAYMENT", "15 LB", "30 LB"],
    },

    # --- Cross-system extras ---
    "cricket": {
        "display_name": "Crickets",
        "unit": "SF",
        "derive_from": "manual",
        "confidence": 0.0,
        "keywords": ["CRICKET"],
    },
    "parapet": {
        "display_name": "Parapet",
        "unit": "LF",
        "derive_from": "polygon_perimeter",
        "confidence": 0.5,
        "keywords": ["PARAPET", "PARAPET WALL"],
    },
}


# Items active for an "unknown" system — the universal baseline that
# survives any roofing scope.
UNIVERSAL_ITEMS: list[str] = [
    "membrane_area", "edge_metal", "drains", "scuppers", "insulation",
    "hatches", "rtus", "curbs", "pipe_boots", "exhaust_fans",
]


# ---------------------------------------------------------------------------
# RULES — post-scope relationship warnings
# ---------------------------------------------------------------------------
#
# Each rule has:
#   name:      stable id
#   check:     callable(fields_dict, roof_area) -> bool (True = trigger)
#              where fields_dict maps item_name -> numeric value (None skips)
#   message:   callable(fields_dict, roof_area) -> str
#   severity:  "info" | "warning"

def _v(fields: dict, key: str):
    """Read numeric value from fields dict — returns None if missing/null."""
    fv = fields.get(key)
    if fv is None:
        return None
    v = getattr(fv, "value", fv) if not isinstance(fv, dict) else fv.get("value")
    try:
        return float(v) if v is not None else None
    except (TypeError, ValueError):
        return None


RULES: list[dict] = [
    {
        "name": "drain_or_scupper",
        "severity": "info",
        "check": lambda f, a: (
            (_v(f, "scuppers") or 0) > 0 and (_v(f, "drains") or 0) > 0
        ),
        "message": lambda f, a: (
            "Plans rarely have both scuppers AND drains on the same roof — verify."
        ),
    },
    {
        "name": "low_drain_density",
        "severity": "warning",
        "check": lambda f, a: (
            a > 0 and (_v(f, "drains") or 0) > 0
            and a / (_v(f, "drains") or 1) > 10000
        ),
        "message": lambda f, a: (
            f"Low drain density: {int(_v(f, 'drains') or 0)} drains for "
            f"{int(a)} SF "
            f"({int(a / (_v(f, 'drains') or 1))} SF per drain, "
            f"typical max ~10,000)."
        ),
    },
    {
        "name": "no_drains_on_flat_roof",
        "severity": "warning",
        "check": lambda f, a: (
            a > 0 and (_v(f, "drains") is not None)
            and (_v(f, "drains") or 0) == 0
            and (_v(f, "scuppers") or 0) == 0
        ),
        "message": lambda f, a: (
            f"No drains or scuppers found on a {int(a)} SF roof — "
            f"verify drainage callouts exist inside the outline."
        ),
    },
    {
        "name": "insulation_matches_area",
        "severity": "info",
        "check": lambda f, a: (
            a > 0 and (_v(f, "insulation") or 0) > 0
            and abs((_v(f, "insulation") or 0) - a) / a > 0.10
        ),
        "message": lambda f, a: (
            f"Insulation area ({int(_v(f, 'insulation') or 0)} SF) differs "
            f"from roof area ({int(a)} SF) by >10% — usually they match."
        ),
    },
    {
        "name": "walkway_with_hatch",
        "severity": "warning",
        "check": lambda f, a: (
            (_v(f, "hatches") or 0) > 0 and (_v(f, "walkway_pads") or 0) == 0
        ),
        "message": lambda f, a: (
            "Roof hatch found but no walkway pads — code typically requires "
            "an access walkway from the hatch to equipment."
        ),
    },
]


# ---------------------------------------------------------------------------
# G.5a CP4: PIN_PALETTE_COLORS — deterministic per-item display colors used
# by the scope-system palette UI. Keys are item names from ITEMS; values are
# hex strings consumed by the frontend's pin/edge/polygon overlay rendering.
# Items not listed here fall back to a hash-derived default color in
# RoofingModule.get_palette_seed (single source of truth for color logic).
# Colors chosen to be distinguishable on dark + light canvases.
# ---------------------------------------------------------------------------

PIN_PALETTE_COLORS: dict[str, str] = {
    # callout_count items → pinPalette
    "drains":         "#4FC3F7",   # blue
    "scuppers":       "#5DADE2",   # blue-2
    "rtus":           "#F39C12",   # amber
    "curbs":          "#D68910",   # amber-2
    "hatches":        "#2ECC71",   # green
    "pipe_boots":     "#9B59B6",   # purple
    "exhaust_fans":   "#E74C3C",   # red
    # polygon_perimeter items → edgeTypes
    "edge_metal":     "#FFB300",   # gold
    "coping":         "#FFA000",   # gold-2
    "walkway_pads":   "#7F8C8D",   # grey
    # polygon_area items → polygonTypes / derived
    "membrane_area":  "#1ABC9C",   # teal
    "insulation":     "#16A085",   # teal-2
    "cover_board":    "#138D75",   # teal-3
}


# ---------------------------------------------------------------------------
# Public dict (matches the structure in the spec)
# ---------------------------------------------------------------------------

ROOFING_VOCABULARY = {
    "systems": SYSTEMS,
    "items": ITEMS,
    "universal_items": UNIVERSAL_ITEMS,
    "rules": RULES,
}
