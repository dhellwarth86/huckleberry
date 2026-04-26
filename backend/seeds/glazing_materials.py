"""
Glazing Materials Reference Database — SKELETON / STUB

Source: TRACEPOINT_PRODUCT_VISION.md, TRACEPOINT_CLAUDE_CODE_BRIEF.md
Extracted: April 23, 2026

STATUS: This file is mostly a skeleton. Unlike roofing_materials.py,
there was no equivalent material-intelligence spec written for glazing.
What exists in the TracePoint docs is:

  - A stated approach: "schedule-driven, not symbol-hunt" — glazing
    is counted from window/door schedules on the plans, not by looking
    for symbols on floor plans.
  - Pin categories for the UI (window, door, storefront, curtain_wall,
    louver, spandrel, entrance).
  - A planned file trades/glazing/fields.py that was never populated.

The SPEC_SECTIONS, MANUFACTURERS, and MATERIAL_PROPERTIES below are
placeholder scaffolds — CSI 08-series numbers and a partial manufacturer
list compiled from public industry sources. THIS DATA NEEDS REVIEW BY
A PERSON WHO ACTUALLY ESTIMATES GLAZING. Don't treat it as authoritative.

If you want to build this out properly, the right move is to hand it
to Sean, Jeremy, or another glazing estimator and let them correct
and expand it. This skeleton is a starting point, not a finished
reference.
"""


# ---------------------------------------------------------------------------
# A. CSI MasterFormat spec sections → glazing system type
#    SKELETON — verify against current CSI MasterFormat and your company's
#    actual usage. Section 08 covers openings (doors, windows, glazing).
# ---------------------------------------------------------------------------
SPEC_SECTIONS = {
    # --- Doors ---
    "08 11":    {"system": "hollow_metal_door",   "name": "Metal Doors and Frames"},
    "08 1113":  {"system": "hollow_metal_door",   "name": "Hollow Metal Doors and Frames"},
    "08 14":    {"system": "wood_door",           "name": "Wood Doors"},
    "08 1416":  {"system": "wood_door",           "name": "Flush Wood Doors"},
    "08 31":    {"system": "access_door",         "name": "Access Doors and Panels"},
    "08 33":    {"system": "overhead_door",       "name": "Coiling Doors and Grilles"},
    "08 34":    {"system": "special_door",        "name": "Special Function Doors"},
    "08 36":    {"system": "overhead_door",       "name": "Panel Doors"},
    "08 38":    {"system": "special_door",        "name": "Traffic Doors"},
    "08 42":    {"system": "entrance",            "name": "Entrances"},
    "08 4213":  {"system": "entrance",            "name": "Aluminum-Framed Entrances and Storefronts"},
    "08 4229":  {"system": "entrance",            "name": "Automatic Entrances"},

    # --- Windows ---
    "08 51":    {"system": "window",              "name": "Windows"},
    "08 5113":  {"system": "window",              "name": "Aluminum Windows"},
    "08 5123":  {"system": "window",              "name": "Steel Windows"},
    "08 5200":  {"system": "window",              "name": "Wood Windows"},
    "08 5300":  {"system": "window",              "name": "Plastic Windows"},

    # --- Storefront / Curtain Wall / Glazed Assemblies ---
    "08 43":    {"system": "storefront",          "name": "Storefronts"},
    "08 4313":  {"system": "storefront",          "name": "Aluminum-Framed Storefronts"},
    "08 44":    {"system": "curtain_wall",        "name": "Curtain Wall and Glazed Assemblies"},
    "08 4413":  {"system": "curtain_wall",        "name": "Glazed Aluminum Curtain Walls"},

    # --- Glazing (the glass itself) ---
    "08 80":    {"system": None, "name": "Glazing"},
    "08 8000":  {"system": None, "name": "Glazing"},
    "08 81":    {"system": None, "name": "Glass Glazing"},
    "08 83":    {"system": None, "name": "Mirrors"},
    "08 84":    {"system": None, "name": "Plastic Glazing"},
    "08 87":    {"system": None, "name": "Glazing Surface Films"},

    # --- Louvers and Vents (adjacent) ---
    "08 91":    {"system": "louver",              "name": "Louvers"},
    "08 9100":  {"system": "louver",              "name": "Louvers"},
    "08 95":    {"system": "louver",              "name": "Vents"},
}


# ---------------------------------------------------------------------------
# B. Manufacturer database — SKELETON
#    Needs expansion. Real glazing estimators will know the regional
#    players, which subs carry which brands, and which manufacturers
#    are actually on PRC's plans vs marketing noise.
# ---------------------------------------------------------------------------
MANUFACTURERS = {
    # --- Aluminum storefront / curtain wall ---
    "Kawneer": {
        "systems":  ["storefront", "curtain_wall", "entrance"],
        "products": {
            "Trifab":        "storefront",
            "1600 Wall":     "curtain_wall",
            "1630 SS":       "curtain_wall",
            "350":           "entrance",
            "500":           "entrance",
        },
        "aliases":  ["Kawneer Company", "Arconic"],
    },
    "YKK AP": {
        "systems":  ["storefront", "curtain_wall", "window", "entrance"],
        "products": {
            "YES 45":        "storefront",
            "YES SSG":       "curtain_wall",
            "YHS 50":        "storefront",
        },
        "aliases":  ["YKK AP America", "YKK"],
    },
    "EFCO": {
        "systems":  ["storefront", "curtain_wall", "window", "entrance"],
        "products": {
            "Series 403":    "storefront",
            "Series 5600":   "curtain_wall",
        },
        "aliases":  ["EFCO Corporation", "Apogee"],
    },
    "Oldcastle BuildingEnvelope": {
        "systems":  ["storefront", "curtain_wall", "window"],
        "products": {},
        "aliases":  ["Oldcastle BE", "OBE"],
    },
    "Tubelite": {
        "systems":  ["storefront", "curtain_wall", "entrance"],
        "products": {},
        "aliases":  ["Tubelite Inc"],
    },
    "Vistawall": {
        "systems":  ["storefront", "curtain_wall"],
        "products": {},
        "aliases":  ["Vistawall Architectural Products"],
    },

    # --- Glass ---
    "Guardian Glass": {
        "systems":  [],   # supplies glass, not framing
        "products": {
            "SunGuard":      "glass_coating",
            "ClimaGuard":    "glass_coating",
        },
        "aliases":  ["Guardian Industries"],
    },
    "Vitro": {
        "systems":  [],
        "products": {
            "Solarban":      "glass_coating",
            "Sungate":       "glass_coating",
        },
        "aliases":  ["Vitro Architectural Glass", "PPG Industries"],
    },
    "Cardinal": {
        "systems":  [],
        "products": {
            "LoE":           "glass_coating",
        },
        "aliases":  ["Cardinal Glass Industries"],
    },

    # --- Doors ---
    "Steelcraft": {
        "systems":  ["hollow_metal_door"],
        "products": {},
        "aliases":  [],
    },
    "Curries": {
        "systems":  ["hollow_metal_door"],
        "products": {},
        "aliases":  ["ASSA ABLOY Curries"],
    },
    "VT Industries": {
        "systems":  ["wood_door"],
        "products": {},
        "aliases":  [],
    },
}


# ---------------------------------------------------------------------------
# C. Material properties — SKELETON
# ---------------------------------------------------------------------------
MATERIAL_PROPERTIES = {
    # Glass thickness markers (IG units usually written as outer/air/inner)
    "glass_thickness_markers": {
        "1/4\"":        {"note": "monolithic, typical interior"},
        "1\" IGU":      {"note": "1-inch insulating glass unit — standard exterior"},
        "1-1/16\" IGU": {"note": "slightly thicker IGU for Low-E + argon"},
        "1/2\" lam":    {"note": "laminated safety glass"},
        "5/16\" lam":   {"note": "laminated — hurricane impact common"},
    },

    # Glass performance / coating markers
    "glass_coating_markers": {
        "Low-E":       {"note": "low-emissivity coating"},
        "Low-E2":      {"note": "dual silver Low-E"},
        "Low-E3":      {"note": "triple silver Low-E"},
        "argon":       {"note": "argon gas fill in IGU"},
        "krypton":     {"note": "krypton gas fill (higher performance, higher cost)"},
        "tempered":    {"note": "heat-strengthened safety glass"},
        "laminated":   {"note": "PVB interlayer — impact and security"},
        "spandrel":    {"note": "opaque backed glass, typically at slab edges"},
        "ceramic frit":{"note": "printed pattern for solar control"},
    },

    # Florida / hurricane signals
    "florida_signals": {
        "HVHZ":        {"note": "High Velocity Hurricane Zone — Miami-Dade/Broward"},
        "NOA":         {"note": "Notice of Acceptance — Miami-Dade product approval"},
        "large missile":{"note": "large missile impact test required"},
        "small missile":{"note": "small missile impact test required"},
        "TAS 201":     {"note": "Miami-Dade large missile impact test"},
        "TAS 202":     {"note": "Miami-Dade uniform static air pressure test"},
        "TAS 203":     {"note": "Miami-Dade cyclic wind pressure test"},
        "FBC":         {"note": "Florida Building Code"},
    },

    # Drawing conventions — how glazing tends to appear on plans
    # PLACEHOLDER — a glazing estimator should validate these
    "drawing_conventions": {
        "window": {
            "plan_view":       "Typically shown as a break in the wall with two parallel lines",
            "schedule":        "Window Schedule on architectural sheets (A-series)",
            "detail_callouts": "08 51, frame type, glass spec",
        },
        "storefront": {
            "plan_view":       "Multiple vertical mullions at regular spacing",
            "schedule":        "Storefront Schedule or noted in Door/Window Schedule",
            "elevation":       "Shown on exterior elevations with mullion pattern",
            "detail_callouts": "08 43, series number, finish, glass spec",
        },
        "curtain_wall": {
            "plan_view":       "Similar to storefront but typically full-height with more complex mullion patterns",
            "elevation":       "Major feature of exterior elevations",
            "detail_callouts": "08 44, series number, structural silicone or captured, glass spec",
        },
        "door": {
            "plan_view":       "Arc showing door swing",
            "schedule":        "Door Schedule on architectural sheets (A-series)",
            "detail_callouts": "08 11 / 08 14 / 08 42 depending on type, hardware set reference",
        },
    },
}


# ---------------------------------------------------------------------------
# Pin categories (from the TracePoint brief) — what the UI offers
# ---------------------------------------------------------------------------
GLAZING_PIN_TYPES = [
    "window",
    "door",
    "storefront",
    "entrance",
    "curtain_wall",
    "louver",
    "spandrel",
    "height",
]


# ---------------------------------------------------------------------------
# TODO — what this file is missing and should gain before trusting it
# ---------------------------------------------------------------------------
# - Review of spec sections by a practicing glazing estimator
# - Regional manufacturer coverage (Florida-specific distributors)
# - Hardware set conventions (how schedules map to hardware types)
# - Frame finish vocabulary (anodized, painted, kynar, etc.)
# - Impact-rated product line flags per manufacturer
# - Glass type shorthand actually used on PRC's reference plans
# - Real examples of how schedule entries are formatted on bid plans
