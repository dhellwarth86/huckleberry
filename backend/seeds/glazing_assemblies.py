"""
Glazing Assemblies Reference Database
(Windows, Doors, Storefronts, Curtain Walls, Entrances, Louvers, Spandrels)

Source: Synthesized from April 14, 2026 TracePoint brief (schedule-driven
glazing approach), SMACNA Architectural Sheet Metal Manual, AAMA glazing
standards, GANA Glazing Manual, Florida Building Code Chapter 24 (Glass
and Glazing), IBC Chapter 10 (Means of Egress), IBC Chapter 24, ADA
Standards, and manufacturer installation guides (Kawneer, YKK AP, EFCO,
Vistawall, Oldcastle).

Extracted / compiled: April 23, 2026

PURPOSE
-------
Same role as roof_assemblies.py but for openings (glazing trade):
given "this plan shows a medium-stile aluminum storefront entrance,"
the module produces the takeoff checklist — what components belong
in that assembly, how quantities are driven, and what code constraints
apply.

APPROACH
--------
The TracePoint brief calls this "schedule-driven, not symbol-hunt."
For glazing, the workflow is:

    1. Table extractor finds Window/Door/Storefront schedules on plans
    2. OCR reads schedule cells (mark, type, dimensions, glass, hardware)
    3. Cross-reference marks (W-1, D-101, SF-A) on floor plans to count
    4. Each mark maps to an assembly defined in this file
    5. Assembly produces the takeoff line items

WHAT IT CONTAINS
----------------
1. GLAZING_COMPONENTS — universal component vocabulary
2. GLAZING_SYSTEMS — each window/door/storefront type → components
3. HARDWARE_SETS — common door hardware set patterns
4. ASSEMBLY_RELATIONSHIPS — cross-component rules
5. FBC_CONSTRAINTS — Florida code requirements for glazing

WHAT IT DOES NOT CONTAIN
------------------------
- Pricing (no dollar amounts)
- Unit labor hours (estimator judgment)
- Product-specific wind design tables (manufacturer-specific)
- Specific NOA numbers (jurisdiction and job-specific)
- Safety glazing locations on a specific plan (plan-specific)

HONEST CAVEAT
-------------
Daniel is not a glazing estimator. The content here was compiled with
AI assistance from public industry references. A practicing glazing
estimator (Sean, Jeremy, or a glazing specialty sub) should review
before using on a live bid. Treat as a starting point.

Florida-specific context: the constraints section is weighted toward
FBC / HVHZ / ASCE 7 because the TracePoint reference jobs are in
Florida. Non-Florida jobs would swap in their local code.
"""


# ===========================================================================
# 1. GLAZING_COMPONENTS — universal component vocabulary
# ===========================================================================
GLAZING_COMPONENTS = {
    # -------- Frame systems (the aluminum/steel perimeter) --------
    "storefront_frame": {
        "role": "Aluminum framing for ground-level glazed walls, typical 1-3/4\" x 4-1/2\" profile",
        "takeoff_unit": "LF",
        "takeoff_driver": "sum of vertical mullions + horizontal rails + perimeter",
        "typical_products": ["Kawneer Trifab", "YKK YES 45", "EFCO 403", "Tubelite T14000"],
        "source": "Manufacturer catalogs; AAMA",
    },
    "curtain_wall_frame": {
        "role": "Aluminum framing for multi-story glazed walls, typical 2-1/2\" x 6-7.5\" profile",
        "takeoff_unit": "LF",
        "takeoff_driver": "sum of vertical mullions + horizontal rails",
        "typical_products": ["Kawneer 1600/1630", "YKK YHC 300", "EFCO 5600", "Vistawall CW-250"],
        "source": "Manufacturer; AAMA",
    },
    "window_frame_aluminum": {
        "role": "Aluminum frame for punched window opening",
        "takeoff_unit": "LF or EA (per mark)",
        "takeoff_driver": "window_mark_count × perimeter_per_mark",
        "source": "Manufacturer; AAMA",
    },
    "window_frame_hollow_metal": {
        "role": "Steel frame for industrial/utility windows",
        "takeoff_unit": "EA",
        "takeoff_driver": "window_mark_count",
        "source": "SDI; industry",
    },
    "window_frame_vinyl": {
        "role": "PVC/vinyl window frame (residential mostly)",
        "takeoff_unit": "EA",
        "takeoff_driver": "window_mark_count",
        "source": "AAMA",
    },
    "window_frame_wood": {
        "role": "Wood window frame (residential / historic)",
        "takeoff_unit": "EA",
        "takeoff_driver": "window_mark_count",
        "source": "WDMA",
    },
    "door_frame_hollow_metal": {
        "role": "Steel door frame (welded or knock-down)",
        "takeoff_unit": "EA",
        "takeoff_driver": "door_mark_count",
        "source": "SDI; ANSI A250.8",
    },
    "door_frame_wood": {
        "role": "Wood door frame (interior typically)",
        "takeoff_unit": "EA",
        "takeoff_driver": "door_mark_count",
        "source": "WDMA",
    },
    "door_frame_aluminum": {
        "role": "Aluminum entrance door frame (typically part of storefront/curtain wall)",
        "takeoff_unit": "EA",
        "takeoff_driver": "entrance_count",
        "source": "Manufacturer",
    },

    # -------- Doors --------
    "door_hollow_metal": {
        "role": "Steel door slab",
        "takeoff_unit": "EA",
        "takeoff_driver": "door_mark_count (where type = HM)",
        "typical_gauges": "16 ga, 18 ga",
        "source": "SDI; ANSI A250.8",
    },
    "door_wood": {
        "role": "Solid-core wood door slab",
        "takeoff_unit": "EA",
        "takeoff_driver": "door_mark_count (where type = W)",
        "source": "WDMA; AWI",
    },
    "door_aluminum_entrance_medium_stile": {
        "role": "Aluminum entrance door, 3-1/2\" stile (most common commercial)",
        "takeoff_unit": "EA",
        "takeoff_driver": "entrance_count",
        "source": "Manufacturer",
    },
    "door_aluminum_entrance_narrow_stile": {
        "role": "Aluminum entrance door, 2-1/2\" stile (retail, max glass)",
        "takeoff_unit": "EA",
        "takeoff_driver": "entrance_count",
        "source": "Manufacturer",
    },
    "door_aluminum_entrance_wide_stile": {
        "role": "Aluminum entrance door, 5\" stile (schools, heavy traffic)",
        "takeoff_unit": "EA",
        "takeoff_driver": "entrance_count",
        "source": "Manufacturer",
    },
    "door_glass_all_glass": {
        "role": "Frameless tempered glass entrance door",
        "takeoff_unit": "EA",
        "takeoff_driver": "entrance_count (where type = GL)",
        "source": "GANA; manufacturer",
    },
    "door_overhead_coiling": {
        "role": "Rolling steel service door",
        "takeoff_unit": "EA",
        "takeoff_driver": "overhead_door_mark_count",
        "source": "DASMA",
    },
    "door_overhead_sectional": {
        "role": "Garage-style sectional door (warehouse, loading)",
        "takeoff_unit": "EA",
        "takeoff_driver": "overhead_door_mark_count",
        "source": "DASMA",
    },
    "door_access_panel": {
        "role": "Small access door in wall or ceiling",
        "takeoff_unit": "EA",
        "takeoff_driver": "access_panel_count from plan",
        "source": "Manufacturer",
    },

    # -------- Glass (infill material) --------
    "glass_monolithic": {
        "role": "Single-lite glass (interior use, non-code-required locations)",
        "takeoff_unit": "SF",
        "takeoff_driver": "glazed_area_where_monolithic_allowed",
        "source": "GANA",
    },
    "glass_tempered": {
        "role": "Heat-strengthened safety glass (IBC 2406 locations)",
        "takeoff_unit": "SF",
        "takeoff_driver": "safety_glazing_locations per IBC 2406",
        "source": "ASTM C1048; IBC 2406",
    },
    "glass_laminated": {
        "role": "Two glass lites with PVB interlayer (safety + impact)",
        "takeoff_unit": "SF",
        "takeoff_driver": "impact_or_security_locations; often required in HVHZ",
        "source": "ASTM C1172",
    },
    "glass_insulated_unit": {
        "role": "Dual-pane IGU with airspace (thermal performance)",
        "takeoff_unit": "SF",
        "takeoff_driver": "exterior_glazed_area",
        "typical_makeup": "1\" overall: 1/4\" outer + 1/2\" airspace + 1/4\" inner",
        "source": "IGCC; FBC Energy Conservation",
    },
    "glass_insulated_laminated": {
        "role": "IGU with laminated lite(s) — HVHZ impact rating",
        "takeoff_unit": "SF",
        "takeoff_driver": "hvhz_exterior_glazing_area",
        "source": "Miami-Dade NOA; TAS 201/202/203",
    },
    "glass_spandrel": {
        "role": "Opaque backed glass at slab edge or non-vision area",
        "takeoff_unit": "SF",
        "takeoff_driver": "spandrel_area",
        "typical_backing": "Silicone ceramic frit, paint, opacifier film",
        "source": "GANA",
    },
    "glass_wired": {
        "role": "Fire-rated glazing (legacy; polished wire or ceramic alternatives now preferred)",
        "takeoff_unit": "SF",
        "takeoff_driver": "fire_rated_assembly_area",
        "source": "IBC 716; UL",
    },
    "glass_fire_rated_ceramic": {
        "role": "Modern fire-rated glazing (Pyran, FireLite)",
        "takeoff_unit": "SF",
        "takeoff_driver": "fire_rated_assembly_area",
        "source": "UL 9; UL 10C; IBC 716",
    },

    # -------- Glass coatings / performance --------
    "coating_low_e": {
        "role": "Low-emissivity coating on IGU surface (energy performance)",
        "takeoff_unit": "SF (applied to IGU area)",
        "takeoff_driver": "IGU_area",
        "typical_products": ["Solarban 60/70/90", "LoE²-272", "SunGuard SN"],
        "source": "FBC Energy Conservation; NFRC",
    },
    "coating_reflective": {
        "role": "Reflective coating for solar control (typically replaced by Low-E)",
        "takeoff_unit": "SF",
        "takeoff_driver": "IGU_area_where_specified",
        "source": "GANA",
    },
    "tint_body": {
        "role": "Bulk-tinted glass (bronze, gray, blue, green)",
        "takeoff_unit": "SF",
        "takeoff_driver": "glazed_area_where_tinted",
        "source": "Manufacturer",
    },
    "ceramic_frit_pattern": {
        "role": "Printed ceramic pattern on glass (solar control, privacy, bird-friendly)",
        "takeoff_unit": "SF",
        "takeoff_driver": "patterned_area",
        "source": "GANA",
    },

    # -------- Perimeter and installation --------
    "glazing_gasket": {
        "role": "Dry gasket between glass and frame",
        "takeoff_unit": "LF",
        "takeoff_driver": "glazing_perimeter",
        "source": "Manufacturer",
    },
    "structural_silicone": {
        "role": "Wet glazing for structural silicone glazed (SSG) curtain wall",
        "takeoff_unit": "GAL or TUBE",
        "takeoff_driver": "ssg_joint_length",
        "source": "ASTM C1184",
    },
    "weatherseal_sealant": {
        "role": "Exterior perimeter sealant between frame and building",
        "takeoff_unit": "LF or TUBE",
        "takeoff_driver": "frame_perimeter_exterior",
        "source": "ASTM C920",
    },
    "backer_rod": {
        "role": "Closed-cell foam behind sealant joint",
        "takeoff_unit": "LF",
        "takeoff_driver": "frame_perimeter_exterior",
        "source": "ASTM C1330",
    },
    "anchor": {
        "role": "Mechanical attachment of frame to structure",
        "takeoff_unit": "EA",
        "takeoff_driver": "frame_perimeter ÷ anchor_spacing (wind-zone dependent)",
        "note": "Spacing determined by wind design — not populated here",
        "source": "AAMA; manufacturer",
    },
    "shim": {
        "role": "Plumb/level frame during install",
        "takeoff_unit": "LB or LF",
        "takeoff_driver": "frame_perimeter",
        "source": "Install standard",
    },
    "sill_flashing": {
        "role": "Waterproof flashing at sill, directs water out",
        "takeoff_unit": "LF",
        "takeoff_driver": "sill_length",
        "source": "AAMA 714; SMACNA",
    },
    "head_flashing": {
        "role": "Waterproof flashing at head",
        "takeoff_unit": "LF",
        "takeoff_driver": "head_length",
        "source": "AAMA 714",
    },
    "sill_receptor": {
        "role": "Track component at bottom of storefront for water management",
        "takeoff_unit": "LF",
        "takeoff_driver": "storefront_sill_length",
        "source": "Manufacturer",
    },
    "snap_cover": {
        "role": "Aesthetic cover over pressure plate on curtain wall",
        "takeoff_unit": "LF",
        "takeoff_driver": "curtain_wall_frame_lf",
        "source": "Manufacturer",
    },
    "threshold": {
        "role": "Metal threshold at door sill",
        "takeoff_unit": "LF or EA",
        "takeoff_driver": "door_count (exterior and floor-transition)",
        "source": "BHMA",
    },

    # -------- Door hardware components --------
    "hinge": {
        "role": "Door pivot (butt, continuous, or pivot)",
        "takeoff_unit": "EA (pairs typical)",
        "takeoff_driver": "door_count × hinge_per_door (typically 3 for commercial)",
        "source": "BHMA A156.1",
    },
    "continuous_hinge": {
        "role": "Full-length door hinge (high-traffic)",
        "takeoff_unit": "EA",
        "takeoff_driver": "high_traffic_door_count",
        "source": "BHMA",
    },
    "pivot_hinge": {
        "role": "Top and bottom pivot sets for heavy doors (entrance)",
        "takeoff_unit": "SET",
        "takeoff_driver": "entrance_door_count",
        "source": "BHMA",
    },
    "lockset": {
        "role": "Door lock / passage / privacy mechanism",
        "takeoff_unit": "EA",
        "takeoff_driver": "door_count requiring lock function",
        "function_types": ["passage", "privacy", "entrance", "storeroom", "classroom"],
        "source": "BHMA A156.2 / A156.13",
    },
    "panic_hardware": {
        "role": "Exit device (panic bar) required on egress doors in certain occupancies",
        "takeoff_unit": "EA",
        "takeoff_driver": "egress_door_count per IBC 1010.1.10",
        "source": "IBC 1010; BHMA A156.3",
    },
    "door_closer": {
        "role": "Hydraulic closer returning door to closed position",
        "takeoff_unit": "EA",
        "takeoff_driver": "door_count requiring closer (exterior, fire-rated, ADA)",
        "source": "BHMA A156.4",
    },
    "automatic_operator": {
        "role": "Power operator for ADA-compliant automatic doors",
        "takeoff_unit": "EA",
        "takeoff_driver": "ada_automatic_door_count",
        "source": "BHMA A156.10; ADA",
    },
    "door_push_pull": {
        "role": "Pull handle and push plate",
        "takeoff_unit": "SET",
        "takeoff_driver": "entrance_door_count",
        "source": "BHMA",
    },
    "door_stop": {
        "role": "Floor or wall stop preventing door overswing",
        "takeoff_unit": "EA",
        "takeoff_driver": "door_count",
        "source": "BHMA",
    },
    "weatherstripping": {
        "role": "Head and jamb weather seal",
        "takeoff_unit": "LF",
        "takeoff_driver": "exterior_door_perimeter (head + jambs)",
        "source": "BHMA",
    },
    "door_sweep": {
        "role": "Bottom sweep sealing door to threshold",
        "takeoff_unit": "EA",
        "takeoff_driver": "exterior_door_count",
        "source": "BHMA",
    },
    "kickplate": {
        "role": "Protective plate at base of door",
        "takeoff_unit": "EA",
        "takeoff_driver": "high_traffic_door_count",
        "source": "BHMA",
    },
    "silencer": {
        "role": "Rubber bumper in door frame stop",
        "takeoff_unit": "EA (typically 3 per frame)",
        "takeoff_driver": "door_frame_count × 3",
        "source": "BHMA",
    },

    # -------- Louvers and screens --------
    "louver_frame": {
        "role": "Frame of exterior louver for mechanical ventilation",
        "takeoff_unit": "EA or SF",
        "takeoff_driver": "louver_mark_count",
        "source": "AMCA",
    },
    "louver_blades": {
        "role": "Horizontal drainable blades",
        "takeoff_unit": "SF (with frame)",
        "takeoff_driver": "louver_area",
        "source": "AMCA",
    },
    "bird_screen": {
        "role": "Mesh screen preventing bird entry",
        "takeoff_unit": "SF",
        "takeoff_driver": "louver_area (exterior)",
        "source": "Manufacturer",
    },
    "insect_screen": {
        "role": "Finer mesh preventing insect entry",
        "takeoff_unit": "SF",
        "takeoff_driver": "operable_window_area where specified",
        "source": "Manufacturer",
    },
    "blank_off_panel": {
        "role": "Opaque panel behind louver for non-vented area",
        "takeoff_unit": "SF",
        "takeoff_driver": "inactive_louver_area",
        "source": "AMCA",
    },

    # -------- Spandrel specifics --------
    "spandrel_back_pan": {
        "role": "Metal back pan behind spandrel glass",
        "takeoff_unit": "SF",
        "takeoff_driver": "spandrel_area",
        "source": "Manufacturer",
    },
    "spandrel_insulation": {
        "role": "Mineral wool or rigid insulation in spandrel cavity",
        "takeoff_unit": "SF",
        "takeoff_driver": "spandrel_area",
        "source": "ASHRAE 90.1; FBC Energy",
    },
    "shadow_box": {
        "role": "Enclosed cavity creating depth appearance behind spandrel glass",
        "takeoff_unit": "SF",
        "takeoff_driver": "shadow_box_specified_area",
        "source": "Architectural",
    },

    # -------- Interior trim / finish --------
    "interior_trim": {
        "role": "Applied trim around interior window/door opening",
        "takeoff_unit": "LF",
        "takeoff_driver": "interior_opening_perimeter",
        "source": "Architectural",
    },
    "stool_and_apron": {
        "role": "Interior window sill and trim",
        "takeoff_unit": "LF or EA",
        "takeoff_driver": "window_mark_count (interior trim scope)",
        "source": "Architectural",
    },
}


# ===========================================================================
# 2. GLAZING_SYSTEMS — each system → components
# ===========================================================================
GLAZING_SYSTEMS = {
    # ----------------------------------------------------------------------
    # STOREFRONT
    # ----------------------------------------------------------------------
    "storefront_captured": {
        "category": "storefront",
        "description": "Aluminum storefront framing (1-3/4\" profile) with captured (pressure-plate) glazing. Ground-level glazed wall.",
        "spec_sections": ["08 43 13"],
        "typical_height": "up to ~10 feet",
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
            "glass_insulated_laminated": "HVHZ / impact-rated locations",
            "glass_tempered": "IBC 2406 safety glazing locations",
            "coating_low_e": "exterior (code-driven)",
            "tint_body": "when specified",
            "threshold": "at door openings in the wall",
            "head_flashing": "when substrate requires",
        },
        "notes": [
            "Most common ground-floor commercial glazed system",
            "Typical frame depth 4-1/2\" — integrates with 6\" stud wall",
            "HVHZ requires laminated impact glass per TAS 201/202/203",
        ],
    },

    "storefront_ssg": {
        "category": "storefront",
        "description": "Structural silicone glazed (SSG) storefront — glass bonded to frame with silicone, no outside pressure plate.",
        "spec_sections": ["08 43 13"],
        "required_components": [
            "storefront_frame",
            "glass_insulated_unit",
            "structural_silicone",
            "glazing_gasket",
            "anchor",
            "weatherseal_sealant",
            "backer_rod",
            "sill_receptor",
            "sill_flashing",
        ],
        "conditional_components": "See storefront_captured",
        "notes": [
            "Cleaner exterior appearance (no pressure plate visible)",
            "Higher cost; requires factory or careful field SSG application",
        ],
    },

    # ----------------------------------------------------------------------
    # CURTAIN WALL
    # ----------------------------------------------------------------------
    "curtain_wall_captured": {
        "category": "curtain_wall",
        "description": "Multi-story aluminum curtain wall with captured glazing (pressure plate + snap cover).",
        "spec_sections": ["08 44 13"],
        "typical_height": "multi-story, hung from floor slabs",
        "required_components": [
            "curtain_wall_frame",
            "glass_insulated_unit",
            "glazing_gasket",
            "snap_cover",
            "anchor",
            "shim",
            "weatherseal_sealant",
            "backer_rod",
        ],
        "conditional_components": {
            "glass_insulated_laminated": "HVHZ / impact locations",
            "glass_spandrel": "at slab edge (non-vision)",
            "spandrel_back_pan": "behind spandrel glass",
            "spandrel_insulation": "per energy code",
            "shadow_box": "when specified architecturally",
            "glass_tempered": "IBC 2406 safety locations",
            "coating_low_e": "per energy code",
            "sill_flashing": "at grade or slab transitions",
        },
        "notes": [
            "Stick-built on site (most common) or unitized (factory-assembled panels)",
            "Spandrel areas at each floor slab — need back pan + insulation",
            "Typical frame depth 6\"-7.5\"",
        ],
    },

    "curtain_wall_ssg_two_side": {
        "category": "curtain_wall",
        "description": "Two-side structural silicone glazed curtain wall — horizontals captured, verticals SSG.",
        "spec_sections": ["08 44 13"],
        "required_components": [
            "curtain_wall_frame",
            "glass_insulated_unit",
            "structural_silicone",
            "glazing_gasket",
            "snap_cover",
            "anchor",
            "weatherseal_sealant",
            "backer_rod",
        ],
        "conditional_components": "See curtain_wall_captured",
        "notes": [
            "Cleaner vertical appearance (no visible mullions on glass edges)",
            "Mixed capture/SSG is common compromise for appearance vs cost",
        ],
    },

    "curtain_wall_ssg_four_side": {
        "category": "curtain_wall",
        "description": "Four-side structural silicone glazed curtain wall — flush glass appearance.",
        "spec_sections": ["08 44 13"],
        "required_components": [
            "curtain_wall_frame",
            "glass_insulated_unit",
            "structural_silicone",
            "glazing_gasket",
            "anchor",
            "weatherseal_sealant",
            "backer_rod",
        ],
        "conditional_components": "See curtain_wall_captured",
        "notes": [
            "Highest-cost curtain wall appearance; silicone bond is structural",
            "Requires manufacturer approval / qualified applicator",
        ],
    },

    # ----------------------------------------------------------------------
    # WINDOWS (PUNCHED OPENINGS)
    # ----------------------------------------------------------------------
    "window_aluminum_fixed": {
        "category": "window",
        "description": "Fixed aluminum window in punched opening.",
        "spec_sections": ["08 51 13"],
        "required_components": [
            "window_frame_aluminum",
            "glass_insulated_unit",
            "glazing_gasket",
            "anchor",
            "weatherseal_sealant",
            "backer_rod",
            "sill_flashing",
            "head_flashing",
        ],
        "conditional_components": {
            "glass_insulated_laminated": "HVHZ",
            "glass_tempered": "safety glazing locations",
            "coating_low_e": "per energy code",
            "interior_trim": "per spec",
        },
    },

    "window_aluminum_operable": {
        "category": "window",
        "description": "Operable aluminum window (casement, awning, horizontal slide, single-hung, project-out).",
        "spec_sections": ["08 51 13"],
        "required_components": [
            "window_frame_aluminum",
            "glass_insulated_unit",
            "glazing_gasket",
            "anchor",
            "weatherseal_sealant",
            "backer_rod",
            "sill_flashing",
            "head_flashing",
            "weatherstripping",
        ],
        "conditional_components": {
            "glass_insulated_laminated": "HVHZ",
            "insect_screen": "on operable portions",
            "coating_low_e": "per energy code",
        },
        "notes": [
            "Operable types include: casement, awning, horizontal slider, single/double-hung, project-out",
            "HVHZ operable windows must pass impact + cyclic pressure tests",
        ],
    },

    "window_hollow_metal": {
        "category": "window",
        "description": "Steel window (industrial / utility / prison / specialty).",
        "spec_sections": ["08 51 23"],
        "required_components": [
            "window_frame_hollow_metal",
            "glass_monolithic",  # often wired or laminated; varies
            "glazing_gasket",
            "anchor",
            "weatherseal_sealant",
        ],
        "conditional_components": {
            "glass_laminated": "security applications",
            "glass_fire_rated_ceramic": "fire-rated openings",
        },
    },

    "window_vinyl": {
        "category": "window",
        "description": "Vinyl window (residential; light commercial multifamily).",
        "spec_sections": ["08 53"],
        "required_components": [
            "window_frame_vinyl",
            "glass_insulated_unit",
            "anchor",
            "weatherseal_sealant",
            "backer_rod",
            "sill_flashing",
        ],
        "conditional_components": {
            "glass_insulated_laminated": "HVHZ",
            "insect_screen": "on operable",
        },
    },

    # ----------------------------------------------------------------------
    # ENTRANCES
    # ----------------------------------------------------------------------
    "entrance_medium_stile_pair": {
        "category": "entrance",
        "description": "Pair of aluminum medium-stile entrance doors with glass infill — most common commercial entrance.",
        "spec_sections": ["08 42 13"],
        "required_components": [
            "door_aluminum_entrance_medium_stile",
            "door_frame_aluminum",
            "glass_tempered",  # safety glazing always in entrance doors
            "pivot_hinge",  # OR continuous_hinge, see note
            "lockset",
            "door_closer",
            "door_push_pull",
            "threshold",
            "weatherstripping",
            "door_sweep",
        ],
        "conditional_components": {
            "panic_hardware": "required in egress doors per IBC 1010.1.10",
            "automatic_operator": "ADA automatic entrance",
            "continuous_hinge": "alternative to pivot hinge",
            "kickplate": "high-traffic",
            "glass_laminated": "HVHZ impact-rated",
        },
        "notes": [
            "Medium stile is the workhorse — balance of strength and glass area",
            "Pair typically 6' (3' + 3') or 7' (3'-6\" + 3'-6\") overall opening",
            "Entrance doors almost always require tempered or laminated safety glass",
        ],
    },

    "entrance_narrow_stile_pair": {
        "category": "entrance",
        "description": "Pair of narrow-stile aluminum entrance doors — maximum glass, retail applications.",
        "spec_sections": ["08 42 13"],
        "required_components": "See entrance_medium_stile_pair (swap narrow_stile door)",
        "conditional_components": "See entrance_medium_stile_pair",
        "notes": [
            "Minimum hardware clearance — limits some hardware options",
            "Less durable in high-traffic applications",
        ],
    },

    "entrance_wide_stile_pair": {
        "category": "entrance",
        "description": "Pair of wide-stile aluminum entrance doors — schools, institutions, heavy traffic.",
        "spec_sections": ["08 42 13"],
        "required_components": "See entrance_medium_stile_pair (swap wide_stile door)",
        "conditional_components": "See entrance_medium_stile_pair",
        "notes": [
            "Accommodates panic hardware easily",
            "Higher cost; more durable",
        ],
    },

    "entrance_automatic_sliding": {
        "category": "entrance",
        "description": "Automatic sliding entrance doors (retail, healthcare, hospitality).",
        "spec_sections": ["08 42 29"],
        "required_components": [
            "door_aluminum_entrance_medium_stile",  # sliding panels
            "door_frame_aluminum",
            "glass_tempered",
            "automatic_operator",
            "threshold",
            "weatherstripping",
            "lockset",  # for after-hours
        ],
        "conditional_components": {
            "glass_laminated": "HVHZ",
            "panic_hardware": "when backup egress required",
        },
        "notes": [
            "Requires backup egress (typically paired with adjacent swing door per IBC)",
            "Safety sensors required on all automatic doors",
        ],
    },

    "entrance_automatic_swing": {
        "category": "entrance",
        "description": "Automatic swinging entrance door with ADA-compliant power operator.",
        "spec_sections": ["08 42 29"],
        "required_components": [
            "door_aluminum_entrance_medium_stile",
            "door_frame_aluminum",
            "glass_tempered",
            "automatic_operator",
            "pivot_hinge",
            "lockset",
            "threshold",
            "weatherstripping",
        ],
        "conditional_components": "See entrance_automatic_sliding",
    },

    # ----------------------------------------------------------------------
    # DOORS (NON-ENTRANCE)
    # ----------------------------------------------------------------------
    "door_hollow_metal_single": {
        "category": "door",
        "description": "Single hollow metal (steel) door in hollow metal frame — utility, back-of-house, mechanical.",
        "spec_sections": ["08 11 13"],
        "required_components": [
            "door_hollow_metal",
            "door_frame_hollow_metal",
            "hinge",
            "lockset",
            "silencer",
        ],
        "conditional_components": {
            "door_closer": "exterior, fire-rated, ADA",
            "panic_hardware": "egress in required occupancies",
            "weatherstripping": "exterior",
            "door_sweep": "exterior",
            "threshold": "exterior or transition",
            "kickplate": "high-traffic",
            "glass_fire_rated_ceramic": "if vision lite and fire-rated",
            "glass_tempered": "if vision lite",
        },
    },

    "door_hollow_metal_pair": {
        "category": "door",
        "description": "Pair of hollow metal doors (double egress).",
        "spec_sections": ["08 11 13"],
        "required_components": "See door_hollow_metal_single (x2, one frame)",
        "conditional_components": {
            "panic_hardware": "typical in egress pairs",
            "coordinator": "for fire-rated pairs (sequencing closers)",
            "astragal": "at meeting edges",
        },
    },

    "door_wood_interior": {
        "category": "door",
        "description": "Solid-core wood door, interior.",
        "spec_sections": ["08 14 16"],
        "required_components": [
            "door_wood",
            "door_frame_wood",  # OR door_frame_hollow_metal
            "hinge",
            "lockset",
            "silencer",
        ],
        "conditional_components": {
            "door_closer": "fire-rated, ADA",
            "kickplate": "high-traffic",
            "door_stop": "typical",
        },
    },

    "door_overhead_coiling": {
        "category": "door",
        "description": "Rolling steel overhead door — service, loading, security.",
        "spec_sections": ["08 33"],
        "required_components": [
            "door_overhead_coiling",
            # hardware and operator typically packaged with door
        ],
        "conditional_components": {
            "automatic_operator": "motorized",
            "weatherstripping": "exterior applications",
        },
        "notes": [
            "Fire-rated coiling doors (FSD) are common at corridors and rated walls",
            "Typical opening sizes: 8x8, 10x10, 12x12, custom",
        ],
    },

    "door_overhead_sectional": {
        "category": "door",
        "description": "Sectional overhead door — loading dock, warehouse, garage.",
        "spec_sections": ["08 36"],
        "required_components": [
            "door_overhead_sectional",
            # track, springs, hardware packaged
        ],
        "conditional_components": {
            "automatic_operator": "motorized",
            "weatherstripping": "exterior",
        },
    },

    # ----------------------------------------------------------------------
    # LOUVERS
    # ----------------------------------------------------------------------
    "louver_drainable": {
        "category": "louver",
        "description": "Exterior drainable-head louver for mechanical intake/exhaust.",
        "spec_sections": ["08 91 00"],
        "required_components": [
            "louver_frame",
            "louver_blades",
            "bird_screen",
            "anchor",
            "weatherseal_sealant",
            "backer_rod",
        ],
        "conditional_components": {
            "blank_off_panel": "portion not active (inactive louver area)",
            "insect_screen": "when specified (rare on large louvers)",
        },
        "notes": [
            "Common on penthouses and mechanical rooms",
            "Free area percentage determines CFM capacity",
        ],
    },

    # ----------------------------------------------------------------------
    # SPANDREL
    # ----------------------------------------------------------------------
    "spandrel_panel": {
        "category": "spandrel",
        "description": "Opaque infill panel at slab edge in curtain wall.",
        "spec_sections": ["08 44"],
        "required_components": [
            "glass_spandrel",
            "spandrel_back_pan",
            "spandrel_insulation",
            "glazing_gasket",
            "structural_silicone",  # OR captured
        ],
        "conditional_components": {
            "shadow_box": "when architecturally specified",
        },
        "notes": [
            "Part of curtain wall system — not a standalone assembly",
            "Back pan and insulation fill cavity between glass and interior wall",
        ],
    },

    # ----------------------------------------------------------------------
    # INTERIOR GLAZING
    # ----------------------------------------------------------------------
    "interior_office_front": {
        "category": "interior_glazing",
        "description": "Interior aluminum-framed office front (sidelite + door).",
        "spec_sections": ["08 42 13"],
        "required_components": [
            "storefront_frame",  # interior profile
            "glass_tempered",
            "glazing_gasket",
            "anchor",
            "door_aluminum_entrance_medium_stile",  # if includes door
            "door_frame_aluminum",
            "hinge",
            "lockset",
        ],
        "conditional_components": {
            "door_closer": "ADA, fire-rated",
            "ceramic_frit_pattern": "privacy or wayfinding",
        },
        "notes": [
            "Interior use — typically no weatherseal, no flashing",
            "Tempered glass in door and adjacent sidelite per IBC 2406",
        ],
    },

    "interior_sidelite": {
        "category": "interior_glazing",
        "description": "Narrow glazed panel beside an interior door.",
        "spec_sections": ["08 81"],
        "required_components": [
            "glass_tempered",
            "window_frame_aluminum",  # OR integral to adjacent door frame
            "glazing_gasket",
        ],
        "conditional_components": {
            "glass_fire_rated_ceramic": "fire-rated wall assembly",
        },
        "notes": [
            "Within 24\" of door edge and less than 60\" above floor = safety glazing (IBC 2406)",
        ],
    },
}


# ===========================================================================
# 3. HARDWARE_SETS — common door hardware patterns
#
# On real plans, doors are assigned hardware sets like HW-1, HW-2 in
# the Door Schedule, and the hardware set is defined in Section 08 71 00.
# These are typical component groupings — actual sets on a live project
# should be read from that spec section.
# ===========================================================================
HARDWARE_SETS = {
    "hw_interior_office_passage": {
        "description": "Typical interior office/passage door",
        "components": ["hinge", "lockset (passage)", "silencer", "door_stop"],
    },
    "hw_interior_office_privacy": {
        "description": "Interior office with lock (privacy or storeroom)",
        "components": ["hinge", "lockset (entrance or storeroom)", "door_closer", "silencer", "door_stop"],
    },
    "hw_exterior_single_non_egress": {
        "description": "Exterior single door, non-egress",
        "components": [
            "hinge", "lockset (entrance)", "door_closer", "threshold",
            "weatherstripping", "door_sweep", "silencer", "door_stop",
        ],
    },
    "hw_exterior_single_egress": {
        "description": "Exterior single egress door with panic hardware",
        "components": [
            "hinge", "panic_hardware", "door_closer", "threshold",
            "weatherstripping", "door_sweep", "kickplate", "silencer",
        ],
    },
    "hw_exterior_pair_egress": {
        "description": "Exterior egress pair with panic hardware both leaves",
        "components": [
            "hinge (x2 sets)", "panic_hardware (x2)", "door_closer (x2)",
            "threshold", "weatherstripping", "door_sweep (x2)",
            "astragal", "kickplate (x2)", "silencer",
        ],
    },
    "hw_entrance_pair_medium_stile": {
        "description": "Commercial aluminum entrance pair",
        "components": [
            "pivot_hinge (x2 sets)", "lockset (entrance)", "door_closer (x2)",
            "door_push_pull (x2)", "threshold", "weatherstripping",
            "door_sweep (x2)",
        ],
    },
    "hw_ada_automatic_entrance": {
        "description": "ADA-compliant automatic swing entrance",
        "components": [
            "pivot_hinge", "automatic_operator", "lockset", "threshold",
            "weatherstripping", "door_sweep", "push_plate_actuator",
        ],
    },
}


# ===========================================================================
# 4. ASSEMBLY_RELATIONSHIPS — cross-component glazing rules
# ===========================================================================
ASSEMBLY_RELATIONSHIPS = [
    {
        "id": "door_frame_pairing",
        "rule": "Every door requires one frame",
        "triggers_warning_when": "door_count != door_frame_count",
        "why": "Door and frame are separate line items; mismatch usually means the schedule was partially read",
        "source": "Industry convention",
    },
    {
        "id": "door_hardware_pairing",
        "rule": "Every door requires a hardware set",
        "triggers_warning_when": "door_count > 0 AND no hardware_set assigned",
        "why": "Door Schedule always references a hardware set (HW-1, HW-2, etc.)",
        "source": "Industry convention; Section 08 71 00",
    },
    {
        "id": "safety_glazing_required",
        "rule": "Glass in doors and within 24\" of door edge must be safety glazing (tempered or laminated)",
        "triggers_warning_when": "glazed_door OR sidelite present AND glass_monolithic selected",
        "why": "IBC 2406.4 defines hazardous locations; monolithic glass not allowed",
        "source": "IBC 2406",
    },
    {
        "id": "egress_panic_hardware",
        "rule": "Egress doors in A, E, H, I (and certain M) occupancies with 50+ occupants require panic hardware",
        "triggers_warning_when": "egress_door in applicable occupancy AND no panic_hardware",
        "why": "Code requires exit devices to allow quick egress under duress",
        "source": "IBC 1010.1.10",
    },
    {
        "id": "automatic_door_backup_egress",
        "rule": "Automatic entrance doors require backup manual egress",
        "triggers_warning_when": "automatic_entrance AND no adjacent manual swing door",
        "why": "Code requires egress if automatic operator fails",
        "source": "IBC; BHMA A156.10",
    },
    {
        "id": "storefront_sill_receptor",
        "rule": "Storefront at floor level should have a sill receptor for water management",
        "triggers_warning_when": "storefront_lf > 0 AND sill_receptor absent",
        "why": "Water that penetrates frame must drain out through sill receptor weeps",
        "source": "Manufacturer install guides; AAMA",
    },
    {
        "id": "hvhz_impact_glazing",
        "rule": "In HVHZ, exterior glazing must be impact-rated (laminated IGU or impact-approved product)",
        "triggers_warning_when": "project_location == HVHZ AND glass_insulated_unit without laminated",
        "why": "Miami-Dade / Broward code requires NOA-approved impact-rated products",
        "source": "Miami-Dade HVHZ; TAS 201/202/203",
    },
    {
        "id": "spandrel_back_pan_and_insulation",
        "rule": "Spandrel glass areas require back pan + insulation",
        "triggers_warning_when": "glass_spandrel present AND (spandrel_back_pan OR spandrel_insulation absent)",
        "why": "Energy code requires insulation at slab edge; back pan hides interior space",
        "source": "ASHRAE 90.1; FBC Energy",
    },
    {
        "id": "anchor_spacing_wind_zone",
        "rule": "Frame anchor spacing is wind-zone dependent; verify against product data",
        "triggers_warning_when": "anchor count not verified against manufacturer tables",
        "why": "Generic anchor spacing (24\" o.c. traditional) may not meet code in high-wind zones",
        "source": "Manufacturer wind design tables; AAMA",
    },
    {
        "id": "schedule_mark_count_balance",
        "rule": "Total storefront LF from plan should reconcile with storefront openings in schedule",
        "triggers_warning_when": "scheduled_sf_area × perimeter_estimate disagrees with plan_measured_sf by >15%",
        "why": "Schedule and plan should agree; large discrepancy usually means schedule was partial",
        "source": "Plan reading convention",
    },
    {
        "id": "louver_needs_screen",
        "rule": "Exterior louvers require bird screen",
        "triggers_warning_when": "louver AND bird_screen absent",
        "why": "Prevents bird nesting in equipment areas; code and insurance requirement",
        "source": "Manufacturer; typical spec",
    },
    {
        "id": "fire_rated_assembly_rating_match",
        "rule": "Fire-rated door + frame + hardware + glazing must all match the required rating",
        "triggers_warning_when": "fire_rated_opening with mismatched component ratings",
        "why": "A 90-minute door in a 60-minute frame defaults to the lower rating",
        "source": "IBC 716; NFPA 80; UL listings",
    },
    {
        "id": "ada_clear_opening",
        "rule": "ADA-compliant door must provide 32\" minimum clear opening (36\" door typical)",
        "triggers_warning_when": "ada_accessible AND door_width < 36\"",
        "why": "Clear opening measured from door face to stop at 90 degrees open",
        "source": "ADA Standards 404.2.3",
    },
    {
        "id": "perimeter_sealant_coverage",
        "rule": "Exterior frames require continuous perimeter sealant + backer rod",
        "triggers_warning_when": "exterior_frame_perimeter_lf > 0 AND sealant or backer_rod absent",
        "why": "Water infiltration path — must be fully sealed",
        "source": "AAMA installation standards",
    },
    {
        "id": "threshold_at_exterior_doors",
        "rule": "Every exterior door needs a threshold",
        "triggers_warning_when": "exterior_door AND threshold absent",
        "why": "Water stop and ADA transition requirement",
        "source": "BHMA; ADA",
    },
]


# ===========================================================================
# 5. FBC_CONSTRAINTS — Florida code / standards for glazing
# ===========================================================================
FBC_CONSTRAINTS = {
    "hvhz_impact": {
        "name": "HVHZ impact testing",
        "applies_to": ["Miami-Dade County", "Broward County"],
        "tests_required": {
            "TAS 201": "Large missile impact (9 lb 2x4 @ 50 fps)",
            "TAS 202": "Static air pressure (design pressures)",
            "TAS 203": "Cyclic wind pressure (9,000 cycles)",
        },
        "impacts": [
            "All exterior glazing must carry Miami-Dade NOA",
            "Laminated or approved impact IGUs required",
            "Shutters NOT allowed as alternative in most occupancies",
            "Significant cost premium vs non-HVHZ glazing",
        ],
        "source": "Miami-Dade HVHZ; FBC HVHZ chapter",
    },
    "non_hvhz_impact": {
        "name": "Non-HVHZ wind-borne debris regions",
        "applies_to": "Coastal counties outside HVHZ (most of FL coast)",
        "requirements": [
            "ASTM E1886/E1996 impact testing, OR",
            "Code-approved shutters, OR",
            "Structural panels meeting specified wind speed",
        ],
        "impacts": [
            "Impact glazing OR shutters (owner choice)",
            "Shutters allowed in non-HVHZ — more flexibility",
        ],
        "source": "FBC 1609; ASCE 7",
    },
    "wind_loads": {
        "name": "Design wind pressure",
        "source": "ASCE 7 wind maps; FBC",
        "florida_range_mph": "140-200 (ultimate design wind speed)",
        "impacts": [
            "Frame profile selection (deeper for higher wind)",
            "Anchor spacing (tighter for higher wind)",
            "Glass thickness and makeup",
            "Structural silicone width (if SSG)",
        ],
    },
    "safety_glazing": {
        "name": "Hazardous locations requiring safety glazing",
        "requirement": "Tempered or laminated glass required",
        "locations": [
            "In any door",
            "Within 24\" of door edge AND lower than 60\" above floor",
            "Panels larger than 9 SF with bottom edge < 18\" above floor",
            "Adjacent to stairs (within 36\" horizontal, lower than 36\" above landing)",
            "In walls/fences around swimming pools",
            "In bathtub/shower enclosures",
        ],
        "source": "IBC 2406",
    },
    "energy_code": {
        "name": "Fenestration thermal performance",
        "florida_climate_zones": "1A Miami, 2A most of FL, 2B panhandle",
        "metrics": {
            "U-factor": "Maximum allowable for fenestration assembly",
            "SHGC": "Solar Heat Gain Coefficient maximum",
            "VT": "Visible Transmittance (daylighting)",
        },
        "impacts": [
            "IGU required (vs monolithic)",
            "Low-E coating typically required",
            "Tinted or reflective glass may be used",
            "NFRC-certified product ratings required",
        ],
        "source": "FBC Energy Conservation; ASHRAE 90.1; NFRC",
    },
    "egress_hardware": {
        "name": "Egress hardware requirements",
        "requirement": "Exit devices (panic hardware) on egress doors in certain occupancies",
        "applies_when": "Occupancy A/E/H/I with 50+ occupants; some M occupancies",
        "impacts": [
            "Panic hardware required on egress doors",
            "Fire-exit hardware required on egress fire-rated doors",
            "Delayed-egress or controlled-egress requires specific listed hardware",
        ],
        "source": "IBC 1010.1.10; NFPA 101",
    },
    "fire_rated_openings": {
        "name": "Fire-rated door / frame / glazing assemblies",
        "requirement": "Rated assembly (frame + door + hardware + glazing) must be listed and labeled",
        "common_ratings": ["20 min", "45 min", "60 min", "90 min", "3 hour"],
        "impacts": [
            "Fire-rated hardware (closer, lockset rated for rating)",
            "Fire-rated glazing (Pyran, FireLite) limited to listed areas",
            "Self-closing and self-latching required",
            "Astragal at pairs",
        ],
        "source": "IBC 716; NFPA 80; UL listings",
    },
    "accessibility": {
        "name": "ADA / accessibility requirements",
        "requirements": [
            "32\" minimum clear opening (36\" door typical)",
            "Max 5 lb opening force (exterior), 5 lb (interior swinging), or auto operator",
            "Hardware: lever, push plate, or loop (no grasping/twisting)",
            "Hardware mounting: 34-48\" above floor",
            "Maneuvering clearances per ADA 404.2.4",
        ],
        "source": "ADA Standards 404; FBC Accessibility",
    },
    "hurricane_shutters": {
        "name": "Hurricane protection alternatives",
        "applies_to": "Wind-borne debris regions outside HVHZ",
        "allowed_alternatives": [
            "Accordion shutters",
            "Roll-down shutters",
            "Bahama / colonial shutters",
            "Structural panels (plywood per FBC; metal shutters)",
            "Impact-rated glazing (eliminates need for shutters)",
        ],
        "impacts": [
            "May reduce glazing cost (non-impact glass allowed)",
            "Maintenance and deployment labor over life of building",
            "HVHZ typically prohibits shutter-only alternative",
        ],
        "source": "FBC 1609",
    },
}


# ===========================================================================
# USAGE SKETCH
#
# # Step 1: Table extractor finds Door Schedule
# schedule = extract_door_schedule(plan_pdf)
#
# # Step 2: OCR reads schedule rows
# rows = ocr_schedule(schedule)  # [{mark: "101", type: "HM-A", hw_set: "HW-1", ...}]
#
# # Step 3: Each row → assembly lookup
# for row in rows:
#     system = map_door_type_to_system(row["type"])  # → "door_hollow_metal_single"
#     assembly = GLAZING_SYSTEMS[system]
#     hardware = HARDWARE_SETS.get(row["hw_set"])
#
#     takeoff.add_row(
#         mark=row["mark"],
#         system=system,
#         components=[ROOF_COMPONENTS[c] for c in assembly["required_components"]],
#         hardware=hardware,
#     )
#
# # Step 4: Cross-reference marks on floor plan
# mark_counts = count_marks_on_plans(rows, floor_plan_pages)
# takeoff.apply_counts(mark_counts)
#
# # Step 5: Apply relationship rules
# for rule in ASSEMBLY_RELATIONSHIPS:
#     if rule_triggers(takeoff, rule):
#         takeoff.add_warning(rule["id"], rule["rule"])
#
# # Step 6: Apply FBC constraints
# for constraint in FBC_CONSTRAINTS.values():
#     if constraint_applies(project, constraint):
#         takeoff.add_code_note(constraint["name"])
# ===========================================================================
