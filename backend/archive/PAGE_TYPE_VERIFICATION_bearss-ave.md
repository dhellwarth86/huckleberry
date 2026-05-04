# Page-Type Verification — Bearss Ave Distribution Center — University — Marcobay Construction (3)

**Date:** 2026-04-29
**Phase:** Page-type verification + coupling diagnostic
**Bidset file:** `C:\huck stage 2\full bid sets\Bearss Ave Distribution Center - University - Marcobay Construction (3).pdf`
**Page count:** 91
**Dispatch wall-clock:** 85.43s

**Type of artifact:** read-only verification, no fixes. Tests three coupled bugs hypothesized by extended-thinking Claude on 2026-04-29. dispatch_gate.py and trade_input_builder.py read-only this phase per orders §0; vault rule active on the five vault-ruled modules (none opened). The gate report (`backend/PAGE_TYPE_VERIFICATION_GATE_REPORT.md`) summarizes hypothesis status across all three bidsets.

---

## §1 — Block 1: Page-Type Histogram

##DIAG_START:page_type_histogram:bearss-ave##
{
  "total_pages": 91,
  "total_mapped_pages": 44,
  "total_pages_has_legend": 53,
  "total_pages_has_schedule": 23,
  "histogram": {
    "elevation": 27,
    "detail_sheet": 27,
    "floor_plan": 15,
    "schedule_sheet": 7,
    "cover": 4,
    "site_plan": 3,
    "life_safety": 2,
    "roof_plan": 2,
    "section": 2,
    "mep_plan": 1,
    "unknown": 1
  },
  "per_page": [
    {
      "page_idx": 0,
      "sheet_num": "A-001",
      "sheet_title": "COVER SHEET  SHEET NUMBER: A-001  PROJECT NAME: BEARSS AVENUE DISTRIBUTION CENTER - BUILDING 1",
      "page_type": "cover",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 1,
      "sheet_num": "A-002",
      "sheet_title": "CODE & LIFE SAFETY",
      "page_type": "life_safety",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 2,
      "sheet_num": "A-003",
      "sheet_title": "ARCHITECTURAL SITE PLAN",
      "page_type": "site_plan",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 3,
      "sheet_num": "A-202",
      "sheet_title": "PANEL ELEVATIONS, WALL SECTIONS, & DETAILS",
      "page_type": "roof_plan",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 4,
      "sheet_num": "A-402",
      "sheet_title": "MISC. DETAILS",
      "page_type": "floor_plan",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 5,
      "sheet_num": "A-201",
      "sheet_title": "EXTERIOR ELEVATIONS",
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 6,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 7,
      "sheet_num": "A-401",
      "sheet_title": "ROOF MISC. DETAILS",
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 8,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 9,
      "sheet_num": "A-501",
      "sheet_title": "UL DETAILS",
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 10,
      "sheet_num": "A-601",
      "sheet_title": "DOOR & WINDOW SCHEDULES, FRAMES & DETAILS",
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 1
    },
    {
      "page_idx": 11,
      "sheet_num": "S-000",
      "sheet_title": "COVER",
      "page_type": "cover",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 12,
      "sheet_num": "S-100",
      "sheet_title": "GENERAL NOTES",
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 8
    },
    {
      "page_idx": 13,
      "sheet_num": "S-101",
      "sheet_title": "GRAVITY & LATERAL LOADING",
      "page_type": "detail_sheet",
      "confidence": 0.7,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 2
    },
    {
      "page_idx": 14,
      "sheet_num": "S-102",
      "sheet_title": "BUILDING CLEAR HEIGHT ELEVATIONS",
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 15,
      "sheet_num": "S-103",
      "sheet_title": "SPECIAL INSPECTIONS",
      "page_type": "section",
      "confidence": 0.7,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 8
    },
    {
      "page_idx": 16,
      "sheet_num": "S-200",
      "sheet_title": "OVERALL FOUNDATION PLAN",
      "page_type": "schedule_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 5
    },
    {
      "page_idx": 17,
      "sheet_num": "S-210",
      "sheet_title": "OVERALL ROOF  FRAMING PLAN",
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 2
    },
    {
      "page_idx": 18,
      "sheet_num": "S-300",
      "sheet_title": "OVERALL TILT PANEL PLAN",
      "page_type": "elevation",
      "confidence": 0.7,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 19,
      "sheet_num": "S-301",
      "sheet_title": "TILT PANEL EMBED/REINF SECTIONS & DETAILS",
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 20,
      "sheet_num": "S-310",
      "sheet_title": "NORTH TILT PANEL ELEVATIONS",
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 21,
      "sheet_num": "S-311",
      "sheet_title": "EAST TILT PANEL ELEVATIONS",
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 22,
      "sheet_num": "S-312",
      "sheet_title": "SOUTH TILT PANEL ELEVATIONS",
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 23,
      "sheet_num": "S-313",
      "sheet_title": "WEST TILT PANEL ELEVATIONS",
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 24,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 25,
      "sheet_num": "S-321",
      "sheet_title": "TILT REBAR ELEVATION",
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 26,
      "sheet_num": "S-322",
      "sheet_title": "TILT REBAR ELEVATION",
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 27,
      "sheet_num": "S-323",
      "sheet_title": "TILT REBAR ELEVATION",
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 28,
      "sheet_num": "S-400",
      "sheet_title": "CMU SECTIONS AND DETAILS",
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 29,
      "sheet_num": "S-500",
      "sheet_title": "FOUNDATION SECTIONS AND DETAILS",
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 30,
      "sheet_num": "S-501",
      "sheet_title": "FOUNDATION SECTIONS AND DETAILS",
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 3
    },
    {
      "page_idx": 31,
      "sheet_num": "S-510",
      "sheet_title": "SLAB ON GRADE SECTIONS AND DETAILS",
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 32,
      "sheet_num": "S-520",
      "sheet_title": "STEEL FRAMING SECTIONS AND DETAILS",
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 33,
      "sheet_num": "S-530",
      "sheet_title": "BRACE FRAMING SECTIONS & DETAILS",
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 34,
      "sheet_num": "M-001",
      "sheet_title": "MECHANICAL GENERAL",
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 1
    },
    {
      "page_idx": 35,
      "sheet_num": "M-002",
      "sheet_title": "MECHANICAL SCHEDULES & DETAILS",
      "page_type": "detail_sheet",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 36,
      "sheet_num": "M-100",
      "sheet_title": "MECHANICAL PLANS",
      "page_type": "mep_plan",
      "confidence": 0.3,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 37,
      "sheet_num": "P-001",
      "sheet_title": "PLUMBING GENERAL",
      "page_type": "floor_plan",
      "confidence": 0.7,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 3
    },
    {
      "page_idx": 38,
      "sheet_num": "P-002",
      "sheet_title": "PLUMBING SPECIFICATIONS",
      "page_type": "schedule_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 7
    },
    {
      "page_idx": 39,
      "sheet_num": "P-100",
      "sheet_title": "PLUMBING FLOOR PLAN",
      "page_type": "floor_plan",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 40,
      "sheet_num": "E-001",
      "sheet_title": "ELECTRICAL GENERAL",
      "page_type": "floor_plan",
      "confidence": 0.7,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 6
    },
    {
      "page_idx": 41,
      "sheet_num": "E-002",
      "sheet_title": "LIGHTING GENERAL",
      "page_type": "floor_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 42,
      "sheet_num": "E-101",
      "sheet_title": "ELECTRICAL SITE PLAN",
      "page_type": "site_plan",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 43,
      "sheet_num": "E-201",
      "sheet_title": "ELECTRICAL PLAN - LIGHTING",
      "page_type": "floor_plan",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 2
    },
    {
      "page_idx": 44,
      "sheet_num": "E-301",
      "sheet_title": "FLOOR PLAN - POWER",
      "page_type": "floor_plan",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 45,
      "sheet_num": "E-401",
      "sheet_title": "ELECTRICAL RISER & SCHEDULES",
      "page_type": "schedule_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 9
    },
    {
      "page_idx": 46,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "cover",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 47,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "life_safety",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 48,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "site_plan",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 49,
      "sheet_num": "A-101",
      "sheet_title": "OVERALL FLOOR PLAN & ROOF PLANS",
      "page_type": "roof_plan",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 50,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "floor_plan",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 51,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 52,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 53,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 54,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 55,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 56,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 1
    },
    {
      "page_idx": 57,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "cover",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 58,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 7
    },
    {
      "page_idx": 59,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.7,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 2
    },
    {
      "page_idx": 60,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 61,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "section",
      "confidence": 0.7,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 8
    },
    {
      "page_idx": 62,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "schedule_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 5
    },
    {
      "page_idx": 63,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 2
    },
    {
      "page_idx": 64,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "schedule_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 6
    },
    {
      "page_idx": 65,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 66,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 67,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 68,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 69,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 70,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 71,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 72,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 73,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 74,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 75,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 76,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 3
    },
    {
      "page_idx": 77,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 78,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 79,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 80,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "floor_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 81,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 82,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 83,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "floor_plan",
      "confidence": 0.7,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 3
    },
    {
      "page_idx": 84,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "schedule_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 7
    },
    {
      "page_idx": 85,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "floor_plan",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 86,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "floor_plan",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 6
    },
    {
      "page_idx": 87,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "floor_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 88,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "floor_plan",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 2
    },
    {
      "page_idx": 89,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "floor_plan",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 2
    },
    {
      "page_idx": 90,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "schedule_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 8
    }
  ]
}
##DIAG_END:page_type_histogram:bearss-ave##

## §2 — Block 2: Schedule-Bearing Audit

Heuristic: `is_schedule_bearing = 'SCHEDULE' in (sheet_title or '').upper()`. Not real ground truth — tests whether the sheet's title self-identifies as schedule-bearing.

##DIAG_START:schedule_bearing_audit:bearss-ave##
{
  "total_schedule_bearing": 3,
  "classified_as_schedule_sheet": 1,
  "classified_as_other_count": 2,
  "other_classification_breakdown": {
    "elevation": 1,
    "detail_sheet": 1
  },
  "schedule_bearing_pages": [
    {
      "page_idx": 10,
      "sheet_num": "A-601",
      "sheet_title": "DOOR & WINDOW SCHEDULES, FRAMES & DETAILS",
      "current_type": "elevation"
    },
    {
      "page_idx": 35,
      "sheet_num": "M-002",
      "sheet_title": "MECHANICAL SCHEDULES & DETAILS",
      "current_type": "detail_sheet"
    },
    {
      "page_idx": 45,
      "sheet_num": "E-401",
      "sheet_title": "ELECTRICAL RISER & SCHEDULES",
      "current_type": "schedule_sheet"
    }
  ],
  "other_classified_pages": [
    {
      "page_idx": 10,
      "sheet_num": "A-601",
      "sheet_title": "DOOR & WINDOW SCHEDULES, FRAMES & DETAILS",
      "current_type": "elevation"
    },
    {
      "page_idx": 35,
      "sheet_num": "M-002",
      "sheet_title": "MECHANICAL SCHEDULES & DETAILS",
      "current_type": "detail_sheet"
    }
  ]
}
##DIAG_END:schedule_bearing_audit:bearss-ave##

## §3 — Block 4: Reclassification Simulation (SCHEDULE rule moved to position 0)

##DIAG_START:reclassification_simulation:bearss-ave##
{
  "total_pages": 91,
  "total_changed": 18,
  "transition_histogram": {
    "elevation -> schedule_sheet": 7,
    "floor_plan -> schedule_sheet": 7,
    "detail_sheet -> schedule_sheet": 3,
    "mep_plan -> unknown": 1
  },
  "schedule_bearing_pages_not_currently_sched": 2,
  "schedule_bearing_pages_flipped_to_sched": 2,
  "schedule_bearing_flip_coverage": 1.0,
  "new_misclassifications_count": 15,
  "new_misclassifications_sample": [
    {
      "page_idx": 5,
      "sheet_num": "A-201",
      "sheet_title": "EXTERIOR ELEVATIONS",
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 12,
      "sheet_num": "S-100",
      "sheet_title": "GENERAL NOTES",
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 8
    },
    {
      "page_idx": 18,
      "sheet_num": "S-300",
      "sheet_title": "OVERALL TILT PANEL PLAN",
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 1
    },
    {
      "page_idx": 34,
      "sheet_num": "M-001",
      "sheet_title": "MECHANICAL GENERAL",
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 1
    },
    {
      "page_idx": 37,
      "sheet_num": "P-001",
      "sheet_title": "PLUMBING GENERAL",
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 3
    },
    {
      "page_idx": 40,
      "sheet_num": "E-001",
      "sheet_title": "ELECTRICAL GENERAL",
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 6
    },
    {
      "page_idx": 41,
      "sheet_num": "E-002",
      "sheet_title": "LIGHTING GENERAL",
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 51,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 56,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 1
    },
    {
      "page_idx": 58,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 7
    },
    {
      "page_idx": 80,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 81,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 1
    },
    {
      "page_idx": 83,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 3
    },
    {
      "page_idx": 86,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 6
    },
    {
      "page_idx": 87,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    }
  ],
  "changed_pages": [
    {
      "page_idx": 5,
      "sheet_num": "A-201",
      "sheet_title": "EXTERIOR ELEVATIONS",
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 10,
      "sheet_num": "A-601",
      "sheet_title": "DOOR & WINDOW SCHEDULES, FRAMES & DETAILS",
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 1
    },
    {
      "page_idx": 12,
      "sheet_num": "S-100",
      "sheet_title": "GENERAL NOTES",
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 8
    },
    {
      "page_idx": 18,
      "sheet_num": "S-300",
      "sheet_title": "OVERALL TILT PANEL PLAN",
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 1
    },
    {
      "page_idx": 34,
      "sheet_num": "M-001",
      "sheet_title": "MECHANICAL GENERAL",
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 1
    },
    {
      "page_idx": 35,
      "sheet_num": "M-002",
      "sheet_title": "MECHANICAL SCHEDULES & DETAILS",
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 36,
      "sheet_num": "M-100",
      "sheet_title": "MECHANICAL PLANS",
      "current_type": "mep_plan",
      "simulated_type": "unknown",
      "simulated_confidence": 0.0,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 37,
      "sheet_num": "P-001",
      "sheet_title": "PLUMBING GENERAL",
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 3
    },
    {
      "page_idx": 40,
      "sheet_num": "E-001",
      "sheet_title": "ELECTRICAL GENERAL",
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 6
    },
    {
      "page_idx": 41,
      "sheet_num": "E-002",
      "sheet_title": "LIGHTING GENERAL",
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 51,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 56,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 1
    },
    {
      "page_idx": 58,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 7
    },
    {
      "page_idx": 80,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 81,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 1
    },
    {
      "page_idx": 83,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 3
    },
    {
      "page_idx": 86,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 6
    },
    {
      "page_idx": 87,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    }
  ],
  "schedule_bearing_flip_pages": [
    {
      "page_idx": 10,
      "sheet_num": "A-601",
      "sheet_title": "DOOR & WINDOW SCHEDULES, FRAMES & DETAILS",
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 1
    },
    {
      "page_idx": 35,
      "sheet_num": "M-002",
      "sheet_title": "MECHANICAL SCHEDULES & DETAILS",
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    }
  ]
}
##DIAG_END:reclassification_simulation:bearss-ave##

## §4 — Block 5: Table Extraction Validation

For pages that flipped from non-SCHEDULE_SHEET to SCHEDULE_SHEET under Block 4's simulation, run `extract_tables` and measure. Hard cap: 20 pages per bidset, ranked by `legend_count` descending. Wall-clock soft cap recorded; hard cap 360s aborts further pages.

##DIAG_START:table_extraction_validation:bearss-ave##
{
  "total_changed_to_sched": 17,
  "page_cap_applied": false,
  "page_cap": 20,
  "pages_validated": 17,
  "total_tables_extracted": 832,
  "total_rows_extracted": 4685,
  "wallclock_seconds": 102.6578,
  "pages_with_tables": 17,
  "extraction_errors": [],
  "per_page": [
    {
      "page_idx": 12,
      "sheet_num": "S-100",
      "sheet_title": "GENERAL NOTES",
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 101,
      "total_rows": 715,
      "headers_first5": [
        "STRUCTURAL STEEL, STEEL JOISTS, STEEL DECK :",
        "ABBREVIATIONS SCHEDULE",
        "ABBREVIATIONS SCHEDULE",
        "STRUCTURE DESIGNED IN ACCORDANCE WITH THE FLORIDA BUILDING CODE",
        "STRUCTURAL STEEL"
      ],
      "wallclock_seconds": 19.7184,
      "legend_count": 8
    },
    {
      "page_idx": 58,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 106,
      "total_rows": 689,
      "headers_first5": [
        "ABBREVIATIONS SCHEDULE",
        "ABBREVIATIONS SCHEDULE",
        "STRUCTURAL STEEL, STEEL JOISTS, STEEL DECK :",
        "POST INSTALLED ANCHOR",
        "STRUCTURE DESIGNED IN ACCORDANCE WITH THE FLORIDA BUILDING CODE,"
      ],
      "wallclock_seconds": 17.0703,
      "legend_count": 7
    },
    {
      "page_idx": 40,
      "sheet_num": "E-001",
      "sheet_title": "ELECTRICAL GENERAL",
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 102,
      "total_rows": 397,
      "headers_first5": [
        "\"3",
        "ELECTRICAL SPECIFICATIONS ELECTRICAL GENERAL NOTES ELECTRICAL GENERAL SYMBOLS LE",
        "ELECTRICAL SPECIFICATIONS",
        "ELECTRICAL GENERAL NOTES",
        "ELECTRICAL GENERAL SYMBOLS LEGEND"
      ],
      "wallclock_seconds": 6.7454,
      "legend_count": 6
    },
    {
      "page_idx": 86,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 107,
      "total_rows": 413,
      "headers_first5": [
        "\"3",
        "ELECTRICAL SPECIFICATIONS ELECTRICAL GENERAL NOTES\nELECTRICAL GENERAL SYMBOLS LE",
        "ELECTRICAL SPECIFICATIONS",
        "ELECTRICAL GENERAL NOTES",
        "ELECTRICAL GENERAL SYMBOLS LEGEND"
      ],
      "wallclock_seconds": 6.9821,
      "legend_count": 6
    },
    {
      "page_idx": 37,
      "sheet_num": "P-001",
      "sheet_title": "PLUMBING GENERAL",
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 22,
      "total_rows": 190,
      "headers_first5": [
        "PLUMBING GENERAL NOTES FIRE PROTECTION GENERAL NOTES PLUMBING ABBREVIATIONS PLUM",
        "PLUMBING ABBREVIATIONS",
        "PLUMBING LEGEND",
        "ADA COMPLIANCE",
        "Atlanta"
      ],
      "wallclock_seconds": 1.8832,
      "legend_count": 3
    },
    {
      "page_idx": 83,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 21,
      "total_rows": 196,
      "headers_first5": [
        "PLUMBING GENERAL NOTES FIRE PROTECTION GENERAL NOTES PLUMBING ABBREVIATIONS PLUM",
        "PLUMBING ABBREVIATIONS",
        "PLUMBING LEGEND",
        "ADA COMPLIANCE",
        "Atlanta"
      ],
      "wallclock_seconds": 1.9251,
      "legend_count": 3
    },
    {
      "page_idx": 10,
      "sheet_num": "A-601",
      "sheet_title": "DOOR & WINDOW SCHEDULES, FRAMES & DETAILS",
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 46,
      "total_rows": 188,
      "headers_first5": [
        "DOOR SCHEDULE\nFire Under Frame Frame Frame Hea\nType Mark Rating Width Height Thi",
        "DOOR SCHEDULE",
        "OVERHEAD AND PERSONNEL DOORS AND FRAMES TO",
        "ALL OVERHEAD DOORS LOCATED AT DOCK LEVELER",
        "ALL HARDWARE TO BE DULL CHROME FINISH (626D)"
      ],
      "wallclock_seconds": 3.076,
      "legend_count": 1
    },
    {
      "page_idx": 18,
      "sheet_num": "S-300",
      "sheet_title": "OVERALL TILT PANEL PLAN",
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 35,
      "total_rows": 160,
      "headers_first5": [
        "55' - 0\" 52' - 0\" 52' - 0\" 52' - 0\" 52' - 0\" 52' - 0\" 52' - 0\" 52' - 0\" 52' - 0\"",
        "(N101",
        "N110)",
        "(N122",
        "TH = 8\""
      ],
      "wallclock_seconds": 3.0806,
      "legend_count": 1
    },
    {
      "page_idx": 34,
      "sheet_num": "M-001",
      "sheet_title": "MECHANICAL GENERAL",
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 69,
      "total_rows": 573,
      "headers_first5": [
        "\"3",
        "MECHANICAL ABBREVIATIONS DUCTWORK SYMBOLS MECHANICAL SPECIFICATIONS\nABBREVIATION",
        "MECHANICAL ABBREVIATIONS",
        "DUCTWORK SYMBOLS",
        "MECHANICAL SPECIFICATIONS"
      ],
      "wallclock_seconds": 13.0631,
      "legend_count": 1
    },
    {
      "page_idx": 56,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 45,
      "total_rows": 183,
      "headers_first5": [
        "DOOR SCHEDULE\nFire Under Frame Frame Frame\nType Mark Rating Width Height Thickne",
        "DOOR SCHEDULE",
        "OVERHEAD AND PERSONNEL DOORS AND FRAMES TO",
        "ALL OVERHEAD DOORS LOCATED AT DOCK LEVELER",
        "ALL HARDWARE TO BE DULL CHROME FINISH (626D)"
      ],
      "wallclock_seconds": 3.0904,
      "legend_count": 1
    },
    {
      "page_idx": 81,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 20,
      "total_rows": 77,
      "headers_first5": [
        "\"3",
        "SPLIT SYSTEM AIR CONDITIONING UNIT SCHEDULE\nFAN COIL UNIT AIR COOLED CONDENSING ",
        "404 -881 -5300",
        "Atlanta",
        "SPLIT SYSTEM AIR CONDITIONING UNIT SCHEDULE"
      ],
      "wallclock_seconds": 0.9389,
      "legend_count": 1
    },
    {
      "page_idx": 5,
      "sheet_num": "A-201",
      "sheet_title": "EXTERIOR ELEVATIONS",
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 12,
      "total_rows": 38,
      "headers_first5": [
        "",
        "CENTER -",
        "RETNEC\nNOITUBIRTSID\nEUNEVA\nSSRAEB\n:EMAN\nTCEJORP\n102",
        "",
        "LL GLASS WITHIN 2' OF DOOR SWING TO BE TEMPERED."
      ],
      "wallclock_seconds": 5.3359,
      "legend_count": 0
    },
    {
      "page_idx": 35,
      "sheet_num": "M-002",
      "sheet_title": "MECHANICAL SCHEDULES & DETAILS",
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 20,
      "total_rows": 84,
      "headers_first5": [
        "\"3",
        "SPLIT SYSTEM AIR CONDITIONING UNIT SCHEDULE\nFAN COIL UNIT AIR COOLED CONDENSING ",
        "404 -881 -5300",
        "Atlanta",
        "SPLIT SYSTEM AIR CONDITIONING UNIT SCHEDULE"
      ],
      "wallclock_seconds": 1.2384,
      "legend_count": 0
    },
    {
      "page_idx": 41,
      "sheet_num": "E-002",
      "sheet_title": "LIGHTING GENERAL",
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 21,
      "total_rows": 87,
      "headers_first5": [
        "\"3",
        "LIGHT FIXTURE SCHEDULE LIGHTING CONTROL LEGEND - WIRED\nITEM DESCRIPTION MANUFACT",
        "LIGHT FIXTURE SCHEDULE",
        "LIGHTING CONTROL LEGEND - WIRED",
        "LIGHTING CONTROL LEGEND -"
      ],
      "wallclock_seconds": 0.3578,
      "legend_count": 0
    },
    {
      "page_idx": 51,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 14,
      "total_rows": 37,
      "headers_first5": [
        "38' -0",
        "",
        "",
        "",
        "CENTER -"
      ],
      "wallclock_seconds": 4.8135,
      "legend_count": 0
    },
    {
      "page_idx": 80,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 70,
      "total_rows": 572,
      "headers_first5": [
        "\"3",
        "MECHANICAL ABBREVIATIONS DUCTWORK SYMBOLS MECHANICAL SPECIFICATIONS\nABBREVIATION",
        "MECHANICAL ABBREVIATIONS",
        "DUCTWORK SYMBOLS",
        "MECHANICAL SPECIFICATIONS"
      ],
      "wallclock_seconds": 12.9885,
      "legend_count": 0
    },
    {
      "page_idx": 87,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 21,
      "total_rows": 86,
      "headers_first5": [
        "\"3",
        "LIGHTING CONTROL LEGEND - WIRED\nLIGHT FIXTURE SCHEDULE\nITEM DESCRIPTION MANUFACT",
        "LIGHTING CONTROL LEGEND - WIRED",
        "LIGHT FIXTURE SCHEDULE",
        "LIGHTING CONTROL LEGEND -"
      ],
      "wallclock_seconds": 0.3502,
      "legend_count": 0
    }
  ],
  "aborted_due_to_hard_cap": false,
  "hard_cap_seconds": 360.0
}
##DIAG_END:table_extraction_validation:bearss-ave##

## §5 — Cross-Reference With Sweep Section 3

For each page in §4 that produced ≥2 tables under validation, the page's section-3 entry from `SWEEP_OBSERVATION_<bidset>.md` carried these signals at sweep ship time (`legend_count`, `has_legend`, `page_type`). Same `legend_count` is replicated below from this run's Block 1.

| Page | Sheet | Title | Current type | Tables | Legend count |
|---:|---|---|---|---:|---:|
| 12 | `S-100` | GENERAL NOTES | `elevation` | 101 | 8 |
| 58 | `None` |  | `elevation` | 106 | 7 |
| 40 | `E-001` | ELECTRICAL GENERAL | `floor_plan` | 102 | 6 |
| 86 | `None` |  | `floor_plan` | 107 | 6 |
| 37 | `P-001` | PLUMBING GENERAL | `floor_plan` | 22 | 3 |
| 83 | `None` |  | `floor_plan` | 21 | 3 |
| 10 | `A-601` | DOOR & WINDOW SCHEDULES, FRAMES & DETAILS | `elevation` | 46 | 1 |
| 18 | `S-300` | OVERALL TILT PANEL PLAN | `elevation` | 35 | 1 |
| 34 | `M-001` | MECHANICAL GENERAL | `detail_sheet` | 69 | 1 |
| 56 | `None` |  | `elevation` | 45 | 1 |
| 81 | `None` |  | `detail_sheet` | 20 | 1 |
| 5 | `A-201` | EXTERIOR ELEVATIONS | `elevation` | 12 | 0 |
| 35 | `M-002` | MECHANICAL SCHEDULES & DETAILS | `detail_sheet` | 20 | 0 |
| 41 | `E-002` | LIGHTING GENERAL | `floor_plan` | 21 | 0 |
| 51 | `None` |  | `elevation` | 14 | 0 |
| 80 | `None` |  | `floor_plan` | 70 | 0 |
| 87 | `None` |  | `floor_plan` | 21 | 0 |

## §6 — Observations (no fixes, no recommendations)

- Observed: bidset has 91 pages total, 44 mapped to sheets, 53 pages with `has_legend=True` after Filter 4, 23 with `has_schedule=True`.
- Observed: page-type histogram shows 7 pages classified as `schedule_sheet` by current dispatch ordering.
- Observed: 3 pages have 'SCHEDULE' in sheet title (heuristic). Of those, 1 currently classify as `schedule_sheet`; 2 classify as something else. Other-classification breakdown: {'elevation': 1, 'detail_sheet': 1}.
- Observed: under SCHEDULE-first simulation, 18 of 91 pages would change classification. Of the 2 schedule-bearing pages NOT currently classified as `schedule_sheet`, 2 would flip to `schedule_sheet` under simulation.
- Observed: simulation produced 15 pages newly classified as `schedule_sheet` whose sheet title does NOT contain 'SCHEDULE'. Documented per orders §7 stop #9 as soft observation; sample of up to 20 in the Block 4 payload.
- Observed: of 17 flipped pages validated in Block 5, 17 produced ≥1 table. Total 832 tables / 4685 rows extracted in 102.66s. Cap applied: False.

## §7 — Closing

Diagnostic only. Three coupled bugs hypothesized by extended-thinking Claude 2026-04-29 are tested by this report's data. The gate report (separate file) summarizes hypothesis status across all three bidsets. No fixes were attempted. dispatch_gate.py and trade_input_builder.py NOT modified. Vault rule held — five vault-ruled modules untouched.
