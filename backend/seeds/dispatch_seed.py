"""
Dispatch Seed Data — Plan Document Classification

Source: CLAUDE_CODE_DISPATCH_ORDERS_FINAL.md (April 13, 2026)
Extracted: April 23, 2026

This is the vocabulary and pattern data the dispatch layer uses to
classify plan-set pages, extract cross-references, and parse legends.

Unlike the roofing/glazing material databases, the content here is
about plan-document STRUCTURE, not about construction materials.
These are industry conventions (CSI sheet numbering, title block
patterns, standard page-type labels) — not company-specific knowledge.

Note: The diagnostic behind this data was run on ~8 real bid sets
(CFA, Taco Bell, AEA, Panda, Vine Street, and others). Where a
pattern produced too many false positives in the diagnostic, it's
noted as dropped. Treat as a starting point; the classification
vocabulary is known to be thin — 52 of 60 roof pages in the 15-set
sweep fell back to universal items because keyword lists were too
narrow.
"""

# ---------------------------------------------------------------------------
# CONFIDENCE SCALE — use consistently across all filters
# ---------------------------------------------------------------------------
CONFIDENCE = {
    "explicit":   0.9,   # keyword found in title block
    "strong":     0.7,   # pattern match with good context
    "inferred":   0.5,   # reasonable assumption from partial data
    "weak":       0.3,   # discipline prefix only, no confirming text
    "unknown":    0.0,   # no data
}


# ---------------------------------------------------------------------------
# DISCIPLINE — single-letter sheet prefixes (CSI / industry standard)
# ---------------------------------------------------------------------------
DISCIPLINES = {
    "G":  "GENERAL",
    "A":  "ARCHITECTURAL",
    "S":  "STRUCTURAL",
    "M":  "MECHANICAL",
    "E":  "ELECTRICAL",
    "P":  "PLUMBING",
    "C":  "CIVIL",
    "L":  "LANDSCAPE",
    "FP": "FIRE_PROTECTION",
    "?":  "UNKNOWN",
}


# ---------------------------------------------------------------------------
# PAGE TYPES — what a single plan page can be
# ---------------------------------------------------------------------------
PAGE_TYPES = [
    "cover",
    "drawing_index",
    "symbol_legend",
    "general_notes",
    "site_plan",
    "floor_plan",
    "roof_plan",
    "ceiling_plan",
    "framing_plan",
    "elevation",
    "section",
    "detail_sheet",
    "schedule_sheet",
    "life_safety",
    "mep_plan",
    "shop_drawing",
    "unknown",
]


# ---------------------------------------------------------------------------
# CONSTRUCTION TYPE — LLM-interpreted, not parsed
# ---------------------------------------------------------------------------
CONSTRUCTION_TYPES = [
    "new",
    "reroof",
    "recover",
    "repair",
    "addition",
    "unknown",
]


# ---------------------------------------------------------------------------
# PAGE CLASSIFICATION KEYWORDS (Filter 2)
#
# For every page, the classifier checks title block text first, then
# full page text. Higher confidence when the match is in the title block.
#
# Case-insensitive substring match against page text.
# ---------------------------------------------------------------------------
PAGE_CLASSIFICATION_KEYWORDS = [
    # (keywords, page_type, title_conf, page_conf)
    (["ROOF PLAN"],                            "roof_plan",       0.9, 0.7),
    (["FLOOR PLAN", "SLAB PLAN"],              "floor_plan",      0.9, 0.7),
    (["FRAMING PLAN", "NOTED FRAMING"],        "framing_plan",    0.9, 0.7),
    (["CEILING PLAN", "RCP", "REFLECTED"],     "ceiling_plan",    0.9, 0.7),
    (["ELEVATION"],                            "elevation",       0.9, 0.7),
    (["DETAIL"],                               "detail_sheet",    0.9, 0.7),
    (["SCHEDULE"],                             "schedule_sheet",  0.9, 0.7),
    (["SECTION"],                              "section",         0.7, 0.5),
    (["GENERAL NOTE", "INDEX", "ABBREVIAT"],   "general_notes",   0.9, 0.7),
    (["SITE PLAN", "SITE PLOT"],               "site_plan",       0.9, 0.7),
    (["COVER"],                                "cover",           0.9, 0.9),
    (["LIFE SAFETY", "OCCUPANCY"],             "life_safety",     0.9, 0.7),
    (["SYMBOL", "LEGEND"],                     "symbol_legend",   0.7, 0.7),
]

# Fallback classification when no keywords match but a discipline letter
# gives a hint — e.g. a sheet labeled M-1.0 with no matching title keyword
# is probably MEP (but low confidence).
DISCIPLINE_FALLBACK = {
    "M":  ("mep_plan", 0.3),
    "E":  ("mep_plan", 0.3),
    "P":  ("mep_plan", 0.3),
    "FP": ("mep_plan", 0.3),
}


# ---------------------------------------------------------------------------
# SHEET NUMBER PATTERN
#
# Used to build the sheet map. Finds sheet numbers like A-1.3, G-0.0,
# S-1.0, A-1.4a, M2.01, etc. Detected in drawing index pages (10+
# sequential matches) or, as fallback, in bottom-right quadrant of
# each page's text (title block).
# ---------------------------------------------------------------------------
SHEET_NUMBER_REGEX = r"[A-Z]{1,2}-?\d+[\.\d]*[A-Za-z]?"


# ---------------------------------------------------------------------------
# CROSS-REFERENCE PATTERNS (Filter 3)
#
# Parsed from page text. Each match creates a CrossReference with a
# ref_type and source coordinates. Unresolved refs stay unresolved.
# ---------------------------------------------------------------------------
CROSS_REFERENCE_PATTERNS = {
    # "SEE DETAIL 5/A1.3" → identifier="5", target_sheet="A1.3"
    "detail_explicit": {
        "regex":    r"SEE\s+DETAIL\s+(\d+)\s*[/\\]\s*([A-Z]-?\d+[\.\d]*)",
        "ref_type": "detail",
        "notes":    "Explicit detail reference with SEE DETAIL prefix",
    },

    # "6 A1.2" in a small text block → identifier="6", target_sheet="A1.2"
    # Apply only when text block length < 50 chars to avoid body-text false positives.
    "detail_implicit": {
        "regex":    r"(\d+)\s+([A-Z]-?\d+[\.\d]*)",
        "ref_type": "detail",
        "notes":    "Number-over-sheet in small text block only (<50 chars)",
        "max_block_chars": 50,
    },

    # "SEE A-2.2" or "SEE SHEET A-2.2" → target_sheet="A-2.2"
    "see_ref": {
        "regex":    r"SEE\s+(?:SHEET\s+)?([A-Z]-?\d+[\.\d]*)",
        "ref_type": "see_ref",
        "notes":    "Generic SEE reference with optional SHEET keyword",
    },

    # Keynote: a 1-2 digit number in a small text block on a page that
    # also contains a keynote legend. Requires page-level context, not
    # just a regex match — handled in code, not pattern alone.
    "keynote": {
        "regex":    r"^\s*(\d{1,2})\s*$",
        "ref_type": "keynote",
        "notes":    "Single/double digit in text block <5 chars on page with keynote legend",
        "requires_keynote_legend_on_page": True,
        "max_block_chars": 5,
    },
}

# Patterns explicitly DROPPED from the dispatch pipeline because
# the April 13 diagnostic showed them producing 10-100x more false
# positives than true matches. Do not re-add without a regression test.
DROPPED_PATTERNS = {
    "section_ref": {
        "reason": "10-100x false positive rate in diagnostic on real plan sets",
        "dropped_date": "April 13, 2026",
    },
}


# ---------------------------------------------------------------------------
# LEGEND DETECTION AND CLASSIFICATION (Filter 4)
#
# Find numbered note lists (sequential integers or decimal patterns like
# 1.01, 1.02) with a qualifying header within 50pts above.
# ---------------------------------------------------------------------------
LEGEND_HEADER_KEYWORDS = [
    "NOTE",
    "LEGEND",
    "KEY",
    "MATERIAL",
    "SCHEDULE",
    "KEYNOTE",
]

LEGEND_MIN_ENTRIES = 3
LEGEND_HEADER_LOOKBACK_PTS = 50

# Legend type classification from header text (first match wins)
LEGEND_TYPE_FROM_HEADER = [
    # (substring_to_find, legend_type)
    ("KEYNOTE",       "keynote"),
    ("MATERIAL",      "material_notes"),
    ("ROOF",          "roof_notes"),
    ("GENERAL NOTE",  "general_notes"),
    ("DOOR",          "door_schedule"),
    ("WINDOW",        "window_schedule"),
    ("HARDWARE",      "hardware_schedule"),
    ("FINISH",        "finish_schedule"),
]

# If no classification hits, fall back to this
LEGEND_TYPE_DEFAULT = "notes"


# ---------------------------------------------------------------------------
# ZONE CLASSIFICATION (Filter 5)
#
# Beyond the zones detected by zone_filter.py, dispatch adds two more
# zone types identified from page structure.
# ---------------------------------------------------------------------------
ADDITIONAL_ZONE_TYPES = {
    "notes_area": {
        "definition": "Large text blocks in page margins",
        "heuristic":  "Top 20% or right 25% of page",
    },
    "legend_area": {
        "definition": "Bounding box around parsed legends from Filter 4",
        "heuristic":  "Computed from legend entry positions",
    },
}


# ---------------------------------------------------------------------------
# TEXT TAGGING BY ZONE (EXPERIMENTAL)
#
# Experimental tagging of text blocks by which zone they fall in.
# Marked EXPERIMENTAL because zone boundaries can be fuzzy and
# misclassification is common on first pass.
# ---------------------------------------------------------------------------
EXPERIMENTAL_ZONE_TAGS = {
    "main_drawing": "callout_texts",
    "notes_area":   "spec_note_texts",
}


# ---------------------------------------------------------------------------
# PROJECT METADATA EXTRACTION — what dispatch CAN vs CANNOT populate
# ---------------------------------------------------------------------------
PROJECT_METADATA_DETERMINISTIC = [
    # Populate these from regex + spatial analysis
    "project_name",
    "project_address",
    "project_number",
    "owner",
    "architect",
    "total_building_sf",  # only if a SF table exists on cover/index
]

PROJECT_METADATA_LLM_ONLY = [
    # Leave as None in dispatch — Filter 6 (LLM cage) may fill these later
    "building_type",
    "building_code",
    "construction_type",
    "occupancy_type",
    "wind_speed_mph",
    "system_classifications",
    "scope_summary",
]


# ---------------------------------------------------------------------------
# LLM BOUNDARIES — what the LLM may and may not do (Filter 6, future)
# ---------------------------------------------------------------------------
LLM_RULES = {
    "may": [
        "Relay numbers explicitly stated in source text",
        "Classify and interpret page content",
        "Cite the specific page and text block the answer came from",
    ],
    "may_not": [
        "Derive numbers from calculations",
        "Estimate quantities",
        "Count things itself",
        "Calculate area, perimeter, or any geometric value",
        "Infer numbers from context when not explicitly stated",
    ],
}
