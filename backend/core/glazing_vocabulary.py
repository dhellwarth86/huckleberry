"""
Glazing vocabulary for the GlazingModule (Phase C.3c, not yet built).

Imports the parked seed content from `backend/seeds/glazing_assemblies.py`
and `backend/seeds/glazing_materials.py` verbatim and overlays the
C.3a-documented gaps. The parked seeds remain authoritative for what's
already in them; this file extends them. The seed files are NOT modified
by C.3b.

Source of truth for additions:
    `backend/C3_GLAZING_SEED_VALIDATION.md` (2026-04-28, C.3a diagnostic
    against Shoppes-at-Avalon)

Bounded additions per `MARCH_ORDERS_C_3b.md` §1:

    Components (4 new entries on `GLAZING_COMPONENTS`):
        - hw_deadbolt        — auxiliary lock supplementing the primary
                                lockset (Shoppes SET-2 "MATCHING DEAD
                                BOLT LOCK")
        - hw_latch_guard     — exterior latch-area metal guard (Shoppes
                                SET-2 "LATCH GUARD")
        - hw_door_viewer     — peep-hole / 200° door viewer (Shoppes OP5
                                SET-2 "ONE (1) PEEP HOLE MOUNTED AT
                                58\" A.F.F. CAL ROYAL OR EQUAL 200°
                                DOOR VIEWER")
        - flashing_drip_cap  — head flashing cap that sheds water from
                                above an opening (Shoppes SET-2 "DRIP
                                CAP")

    Systems (4 new entries on `GLAZING_SYSTEMS`):
        - entrance_medium_stile_single  — single-leaf medium-stile
                                aluminum entrance (Shoppes Type-B
                                3'-0"×7'-0" doors at lobby and rears)
        - entrance_narrow_stile_single  — single-leaf narrow-stile
                                aluminum entrance (retail, max-glass)
        - entrance_wide_stile_single    — single-leaf wide-stile
                                aluminum entrance (institutional)
        - window_storefront_panel       — storefront-framing wall panel
                                as named on Shoppes A-602 "WINDOW
                                TYPES" (distinct from a punched
                                aluminum window)

    Hardware sets (1 new entry on `HARDWARE_SETS`):
        - hw_entrance_single_medium_stile_egress  — single aluminum
                                entrance + panic hardware (Shoppes
                                SET-1A pattern at OP4 east/west rear
                                doors)

    Manufacturers (5 new entries on `MANUFACTURERS`):
        - Cal Royal     — locksets / closers / viewers (Shoppes OP4 +
                          OP5 explicit "CAL ROYAL OR EQUAL")
        - Yale Security — locksets (Shoppes OP5 SET-2 "YALE SECURITY
                          INC. KEYED LOCK SET")
        - Sargent       — locksets / exit devices (industry-standard
                          commercial OEM, ASSA ABLOY)
        - Schlage       — locksets (industry-standard commercial OEM,
                          Allegion)
        - Von Duprin    — exit devices / panic hardware (industry-
                          standard commercial OEM, Allegion)

Structural addition (named here, not in the parked seed): the five new
manufacturer entries use `"door_hardware"` as their `systems` value.
The parked `MANUFACTURERS` table uses system-type strings like
`"storefront"`, `"hollow_metal_door"`, etc. — categories of glazing
*systems*. Hardware OEMs make hardware that goes onto multiple system
types, so a new value `"door_hardware"` is introduced as the natural
slot. No change to the parked seed; the new value is local to the
overlay additions.

Public surface (analogous to `roofing_vocabulary.py`'s shape):
    - `COMPONENTS`           — dict of all components (parked + 4 added)
    - `SYSTEMS`              — dict of all systems (parked + 4 added)
    - `HARDWARE_SETS`        — dict of all hardware sets (parked + 1 added)
    - `RELATIONSHIPS`        — list of assembly relationships (parked,
                                unchanged; alias of ASSEMBLY_RELATIONSHIPS)
    - `FBC_CONSTRAINTS`      — dict of Florida Building Code constraints
                                (parked, unchanged)
    - `SPEC_SECTIONS`        — dict of CSI spec sections (parked,
                                unchanged)
    - `MANUFACTURERS`        — dict of manufacturers (parked + 5 added)
    - `MATERIAL_PROPERTIES`  — dict of material property markers (parked,
                                unchanged)
    - `GLAZING_PIN_TYPES`    — list of pin types (parked, unchanged)
    - `GLAZING_VOCABULARY`   — top-level aggregate dict

Roofing-vocabulary analogy: where roofing has SYSTEMS / ITEMS /
UNIVERSAL_ITEMS / RULES, glazing has the parked seeds' richer shape
(COMPONENTS / SYSTEMS / HARDWARE_SETS / RELATIONSHIPS / FBC_CONSTRAINTS /
SPEC_SECTIONS / MANUFACTURERS / MATERIAL_PROPERTIES / GLAZING_PIN_TYPES).
Both fit the C.1-ported `TradeModule` Protocol contract; the
GlazingModule (C.3c) will choose how to traverse this richer structure.
"""

from __future__ import annotations

from typing import Any

from seeds.glazing_assemblies import (
    GLAZING_COMPONENTS as _SEED_COMPONENTS,
    GLAZING_SYSTEMS as _SEED_SYSTEMS,
    HARDWARE_SETS as _SEED_HARDWARE_SETS,
    ASSEMBLY_RELATIONSHIPS as _SEED_RELATIONSHIPS,
    FBC_CONSTRAINTS as _SEED_FBC,
)
from seeds.glazing_materials import (
    SPEC_SECTIONS as _SEED_SPEC_SECTIONS,
    MANUFACTURERS as _SEED_MANUFACTURERS,
    MATERIAL_PROPERTIES as _SEED_MATERIAL_PROPS,
    GLAZING_PIN_TYPES as _SEED_PIN_TYPES,
)


# ===========================================================================
# C.3a-documented additions — components
# ===========================================================================
# Each entry mirrors the parked-seed component shape:
#   role / takeoff_unit / takeoff_driver / source (+ optional notes).
# ===========================================================================

_C3A_COMPONENT_ADDITIONS: dict[str, Any] = {
    "hw_deadbolt": {
        "role": "Auxiliary deadbolt lock supplementing the primary lockset on exterior or security doors",
        "takeoff_unit": "EA",
        "takeoff_driver": "exterior_door_count requiring deadbolt (typically rear and back-of-house doors)",
        "function_types": ["single_cylinder", "double_cylinder", "thumb_turn"],
        "source": "BHMA A156.5; industry convention",
    },
    "hw_latch_guard": {
        "role": "Metal plate covering the latch area on the strike side of an outswing exterior door, prevents pry attacks",
        "takeoff_unit": "EA",
        "takeoff_driver": "exterior_outswing_door_count",
        "source": "BHMA; industry security convention",
    },
    "hw_door_viewer": {
        "role": "Wide-angle peep-hole (typically 200°) mounted in exterior doors for occupant identification of approachers",
        "takeoff_unit": "EA",
        "takeoff_driver": "exterior_door_count where viewer specified (typically back-of-house or single-occupant entries)",
        "note": "Mounting height 58\"-66\" A.F.F. typical; ADA accessibility may require lower secondary viewer at 43\"",
        "source": "BHMA; ADA Standards 309",
    },
    "flashing_drip_cap": {
        "role": "Head flashing cap above door or window opening that diverts water away from the head condition",
        "takeoff_unit": "LF or EA",
        "takeoff_driver": "exterior_opening_head_length (or door/window mark count when sized per opening)",
        "note": "Adjacent to head_flashing in the seed vocabulary; drip cap is the visible exterior cap, head_flashing is the concealed waterproofing",
        "source": "AAMA 714; SMACNA; industry convention",
    },
}


# ===========================================================================
# C.3a-documented additions — systems
# ===========================================================================
# Each entry mirrors the parked-seed system shape:
#   category / description / spec_sections / required_components /
#   conditional_components / notes (+ optional typical_height).
# Single-leaf entrance variants mirror their pair counterparts with the
# component list adjusted to one leaf (one pivot set, one closer, one
# threshold, etc.).
# ===========================================================================

_C3A_SYSTEM_ADDITIONS: dict[str, Any] = {
    "entrance_medium_stile_single": {
        "category": "entrance",
        "description": (
            "Single aluminum medium-stile entrance door with glass infill — common "
            "back-of-house or single-occupant commercial entrance. Mirrors "
            "entrance_medium_stile_pair with one leaf rather than two."
        ),
        "spec_sections": ["08 42 13"],
        "required_components": [
            "door_aluminum_entrance_medium_stile",
            "door_frame_aluminum",
            "glass_tempered",  # safety glazing always in entrance doors
            "pivot_hinge",     # one set
            "lockset",
            "door_closer",
            "door_push_pull",
            "threshold",
            "weatherstripping",
            "door_sweep",
        ],
        "conditional_components": {
            "panic_hardware": "required in egress doors per IBC 1010.1.10 — see hw_entrance_single_medium_stile_egress",
            "automatic_operator": "ADA automatic entrance",
            "continuous_hinge": "alternative to pivot hinge",
            "kickplate": "high-traffic",
            "glass_laminated": "HVHZ impact-rated",
            "hw_deadbolt": "back-of-house single-leaf doors typically require deadbolt for after-hours security",
        },
        "notes": [
            "Most common single-leaf storefront entrance pattern — Shoppes-at-Avalon Outparcel 4 lobby (Door 100) and rear doors (101, 102) are this type",
            "Single leaf typically 3'-0\" × 7'-0\" × 1¾\" (Shoppes Type-B)",
            "When egress is required, see hw_entrance_single_medium_stile_egress (SET-1A pattern)",
        ],
    },

    "entrance_narrow_stile_single": {
        "category": "entrance",
        "description": (
            "Single narrow-stile aluminum entrance door — retail applications "
            "favouring maximum glass area over hardware durability. Mirrors "
            "entrance_narrow_stile_pair with one leaf."
        ),
        "spec_sections": ["08 42 13"],
        "required_components": "See entrance_medium_stile_single (swap narrow_stile door)",
        "conditional_components": "See entrance_medium_stile_single",
        "notes": [
            "Minimum hardware clearance — limits some hardware options",
            "Less durable in high-traffic applications",
        ],
    },

    "entrance_wide_stile_single": {
        "category": "entrance",
        "description": (
            "Single wide-stile aluminum entrance door — schools, institutions, "
            "heavy traffic single-leaf entries. Mirrors entrance_wide_stile_pair "
            "with one leaf."
        ),
        "spec_sections": ["08 42 13"],
        "required_components": "See entrance_medium_stile_single (swap wide_stile door)",
        "conditional_components": "See entrance_medium_stile_single",
        "notes": [
            "Accommodates panic hardware easily on a single leaf",
            "Higher cost; more durable than medium-stile",
        ],
    },

    "window_storefront_panel": {
        "category": "window",
        "description": (
            "Storefront-framing wall panel — a section of the storefront system "
            "tagged as a 'window type' on the architectural drawings (e.g., "
            "Shoppes A-602 'WINDOW TYPES A through G'). Distinct from "
            "window_aluminum_fixed (which is a punched window in CMU): a "
            "storefront panel is a region of the continuous storefront wall "
            "system delimited by mullion-spacing for takeoff/labeling purposes."
        ),
        "spec_sections": ["08 43 13"],
        "required_components": [
            "storefront_frame",
            "glass_insulated_unit",
            "glazing_gasket",
            "anchor",
            "shim",
            "sill_receptor",
            "weatherseal_sealant",
            "backer_rod",
            "sill_flashing",
        ],
        "conditional_components": {
            "glass_insulated_laminated": "HVHZ / non-HVHZ wind-borne debris (impact-rated tempered + laminated)",
            "glass_tempered": "IBC 2406 safety glazing locations adjacent to door openings",
            "coating_low_e": "exterior (FBC Energy Conservation)",
            "tint_body": "when specified",
            "head_flashing": "when substrate requires",
            "flashing_drip_cap": "exterior head condition above panel",
            "door_aluminum_entrance_medium_stile": "panel may include a door opening (Shoppes Window Type 'C' / 'D' patterns include 3'-0\" door openings)",
        },
        "notes": [
            "Takeoff unit is panel area (SF) — same driver as storefront_captured but bounded by mullion-marked panel extents",
            "Distinct from window_aluminum_fixed in that the surrounding wall is itself a storefront framing system, not CMU/EIFS punched opening",
            "Shoppes-at-Avalon A-602 marks 7 window types (A-G) at 9'-4\" to 9'-6\" tall × 4'-0\" to ~18'-9\" wide",
        ],
    },
}


# ===========================================================================
# C.3a-documented additions — hardware sets
# ===========================================================================
# Mirrors the parked-seed hardware-set shape: description / components.
# ===========================================================================

_C3A_HARDWARE_SET_ADDITIONS: dict[str, Any] = {
    "hw_entrance_single_medium_stile_egress": {
        "description": (
            "Single aluminum medium-stile entrance with panic hardware for egress "
            "(Shoppes-at-Avalon SET-1A pattern: SET-1 storefront-entrance hardware "
            "plus a panic device on a single leaf rather than a pair). Used at "
            "rear egress doors of single-tenant retail outparcels."
        ),
        "components": [
            "pivot_hinge",
            "lockset (entrance, after-hours)",
            "panic_hardware",
            "door_closer",
            "door_push_pull",
            "threshold",
            "weatherstripping",
            "door_sweep",
        ],
    },
}


# ===========================================================================
# C.3a-documented additions — manufacturers (hardware OEMs)
# ===========================================================================
# Each entry mirrors the parked-seed manufacturer shape:
#   systems / products / aliases.
# All five entries use the new "door_hardware" systems value (see file
# docstring for the structural-addition note).
# Product lines listed below are representative of each OEM's commercial-
# door catalog as of 2026; they are not Shoppes-bidset-specific (the
# bidset references generic "OR EQUAL" hardware, naming Cal Royal and Yale
# Security only).
# ===========================================================================

_C3A_MANUFACTURER_ADDITIONS: dict[str, dict[str, Any]] = {
    "Cal Royal": {
        "systems": ["door_hardware"],
        "products": {
            "Lockset (lever)":  "lockset",
            "Door closer":      "door_closer",
            "Door viewer (200°)": "hw_door_viewer",
            "Panic device":     "panic_hardware",
        },
        "aliases": ["Cal Royal Products", "Cal-Royal"],
    },
    "Yale Security": {
        "systems": ["door_hardware"],
        "products": {
            "8800 Series mortise lockset": "lockset",
            "5400 Series cylindrical lockset": "lockset",
            "7100 Series exit device":     "panic_hardware",
            "1100 Series closer":          "door_closer",
        },
        "aliases": ["Yale Security Inc.", "Yale", "ASSA ABLOY Yale"],
    },
    "Sargent": {
        "systems": ["door_hardware"],
        "products": {
            "8200 Series mortise lockset": "lockset",
            "10X Series cylindrical lockset": "lockset",
            "80 Series exit device":       "panic_hardware",
            "351 Series closer":           "door_closer",
        },
        "aliases": ["Sargent Manufacturing", "ASSA ABLOY Sargent"],
    },
    "Schlage": {
        "systems": ["door_hardware"],
        "products": {
            "L9000 Series mortise lockset":   "lockset",
            "ND Series cylindrical lockset":  "lockset",
            "AL Series cylindrical lockset":  "lockset",
        },
        "aliases": ["Schlage Lock Company", "Allegion Schlage"],
    },
    "Von Duprin": {
        "systems": ["door_hardware"],
        "products": {
            "98/99 Series exit device": "panic_hardware",
            "33A/35A Series exit device": "panic_hardware",
        },
        "aliases": ["Allegion Von Duprin"],
    },
}


# ===========================================================================
# Public surface — overlay additions on parked content
# ===========================================================================
# Dicts are merged with parked entries first (preserving parked authority
# for any name collision; there should be none given the bounded scope).
# Lists/dicts that have no additions are aliased through unchanged.
# ===========================================================================

COMPONENTS: dict[str, Any] = {**_SEED_COMPONENTS, **_C3A_COMPONENT_ADDITIONS}
SYSTEMS: dict[str, Any] = {**_SEED_SYSTEMS, **_C3A_SYSTEM_ADDITIONS}
HARDWARE_SETS: dict[str, Any] = {**_SEED_HARDWARE_SETS, **_C3A_HARDWARE_SET_ADDITIONS}
RELATIONSHIPS: list[Any] = list(_SEED_RELATIONSHIPS)
FBC_CONSTRAINTS: dict[str, Any] = dict(_SEED_FBC)

SPEC_SECTIONS: dict[str, Any] = dict(_SEED_SPEC_SECTIONS)
MANUFACTURERS: dict[str, dict[str, Any]] = {
    **_SEED_MANUFACTURERS,
    **_C3A_MANUFACTURER_ADDITIONS,
}
MATERIAL_PROPERTIES: dict[str, Any] = dict(_SEED_MATERIAL_PROPS)
GLAZING_PIN_TYPES: list[str] = list(_SEED_PIN_TYPES)


# G.5a CP4: GLAZING_PIN_PALETTE_COLORS — placeholder color map symmetric
# to roofing_vocabulary.PIN_PALETTE_COLORS. Glazing's vocabulary is richer
# than roofing's (COMPONENTS/SYSTEMS/HARDWARE_SETS), and the trade module's
# `analyze` impl is partial pre-C.3c; this color map is a starter set so
# GlazingModule.get_palette_seed() can return a coherent skeletal palette
# today. Items not listed here fall back to GlazingModule._color_for's
# hash-derived default. Will be tightened when C.3c lands real per-item
# vocab.
GLAZING_PIN_PALETTE_COLORS: dict[str, str] = {
    # Common glazing pin types (seed)
    "window":            "#5DADE2",
    "door":              "#48C9B0",
    "storefront":        "#F5B041",
    "curtain_wall":      "#AF7AC5",
    "skylight":          "#85C1E9",
    "operable_window":   "#5499C7",
    "fixed_window":      "#7FB3D5",
    "entrance_door":     "#52BE80",
    "interior_door":     "#76D7C4",
    "exterior_door":     "#28B463",
    "transom":           "#F8C471",
    "sidelite":          "#F0B27A",
}


# Alias for callers that may prefer the parked seed's longer name —
# preserves discoverability without changing semantics.
ASSEMBLY_RELATIONSHIPS: list[Any] = RELATIONSHIPS


# ---------------------------------------------------------------------------
# Module-level aggregate (matches roofing_vocabulary.py's public-surface
# convention of a single top-level dict that callers may walk in one pass)
# ---------------------------------------------------------------------------

GLAZING_VOCABULARY: dict[str, Any] = {
    "components": COMPONENTS,
    "systems": SYSTEMS,
    "hardware_sets": HARDWARE_SETS,
    "relationships": RELATIONSHIPS,
    "fbc_constraints": FBC_CONSTRAINTS,
    "spec_sections": SPEC_SECTIONS,
    "manufacturers": MANUFACTURERS,
    "material_properties": MATERIAL_PROPERTIES,
    "pin_types": GLAZING_PIN_TYPES,
}
