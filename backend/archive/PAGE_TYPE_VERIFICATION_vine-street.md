# Page-Type Verification — Vine Street Retail Center — Kissimmee — Great Southern Constructors

**Date:** 2026-04-29
**Phase:** Page-type verification + coupling diagnostic
**Bidset file:** `C:\huck stage 2\full bid sets\Vine Street Retail Center - Kissimmee - Great Southern Constructors.pdf`
**Page count:** 138
**Dispatch wall-clock:** 82.40s

**Type of artifact:** read-only verification, no fixes. Tests three coupled bugs hypothesized by extended-thinking Claude on 2026-04-29. dispatch_gate.py and trade_input_builder.py read-only this phase per orders §0; vault rule active on the five vault-ruled modules (none opened). The gate report (`backend/PAGE_TYPE_VERIFICATION_GATE_REPORT.md`) summarizes hypothesis status across all three bidsets.

---

## §1 — Block 1: Page-Type Histogram

##DIAG_START:page_type_histogram:vine-street##
{
  "total_pages": 138,
  "total_mapped_pages": 35,
  "total_pages_has_legend": 34,
  "total_pages_has_schedule": 25,
  "histogram": {
    "detail_sheet": 33,
    "unknown": 32,
    "section": 13,
    "schedule_sheet": 11,
    "roof_plan": 9,
    "floor_plan": 9,
    "elevation": 9,
    "site_plan": 6,
    "ceiling_plan": 6,
    "framing_plan": 6,
    "general_notes": 2,
    "mep_plan": 2
  },
  "per_page": [
    {
      "page_idx": 0,
      "sheet_num": "G-0.0",
      "sheet_title": "COVER SHEET",
      "page_type": "section",
      "confidence": 0.5,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 1,
      "sheet_num": "G-0.1",
      "sheet_title": "SITE PLOT PLAN",
      "page_type": "site_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 2,
      "sheet_num": "G-2.0",
      "sheet_title": "CODE ANALYSIS",
      "page_type": "roof_plan",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 3,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "section",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 4,
      "sheet_num": "A-2.4",
      "sheet_title": "EXTERIOR DETAILS AND SECTIONS",
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 1
    },
    {
      "page_idx": 5,
      "sheet_num": "G-4.0",
      "sheet_title": "WALL TYPES",
      "page_type": "detail_sheet",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 6,
      "sheet_num": "G-5.0",
      "sheet_title": "UL RATINGS - 1 HOUR FIRE WALL",
      "page_type": "general_notes",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 1
    },
    {
      "page_idx": 7,
      "sheet_num": "A-0.1",
      "sheet_title": "BUILDING B SLAB PLAN",
      "page_type": "floor_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 8,
      "sheet_num": "A-1.0",
      "sheet_title": "BUILDING B - NOTED FRAMING PLAN",
      "page_type": "floor_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 9,
      "sheet_num": "A-1.1",
      "sheet_title": "BUILDING B - LIFESAFETY PLAN/ OCCUPANCY",
      "page_type": "schedule_sheet",
      "confidence": 0.7,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 1
    },
    {
      "page_idx": 10,
      "sheet_num": "A-1.2",
      "sheet_title": "BUILDING B - WALL SECTIONS",
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 11,
      "sheet_num": "A-1.3",
      "sheet_title": "BUILDING B - ROOF PLAN",
      "page_type": "roof_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 12,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 13,
      "sheet_num": "A-2.2",
      "sheet_title": "EXTERIOR DETAILS AND SECTIONS",
      "page_type": "detail_sheet",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 14,
      "sheet_num": "A-2.3",
      "sheet_title": "EXTERIOR DETAILS AND SECTIONS",
      "page_type": "section",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 15,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 16,
      "sheet_num": "A-3.0",
      "sheet_title": "PLUMBING FIXTURES AND  ACCESSORIES",
      "page_type": "schedule_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 2
    },
    {
      "page_idx": 17,
      "sheet_num": "A-4.0",
      "sheet_title": "BUILDING B - REFLECTIVE CEILING PLAN",
      "page_type": "ceiling_plan",
      "confidence": 0.7,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 1
    },
    {
      "page_idx": 18,
      "sheet_num": "S-0.1",
      "sheet_title": "GENERAL NOTES",
      "page_type": "section",
      "confidence": 0.7,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 19,
      "sheet_num": "S-0.2",
      "sheet_title": "GENERAL NOTES",
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 20,
      "sheet_num": "S-0.3",
      "sheet_title": "GENERAL NOTES",
      "page_type": "framing_plan",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 2
    },
    {
      "page_idx": 21,
      "sheet_num": "A1",
      "sheet_title": "",
      "page_type": "elevation",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 22,
      "sheet_num": "S-2.0",
      "sheet_title": "BLOCK AND LINTEL PLAN",
      "page_type": "detail_sheet",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 23,
      "sheet_num": "S-3.0",
      "sheet_title": "ROOF FRAMING PLAN",
      "page_type": "framing_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 24,
      "sheet_num": "S-4.0",
      "sheet_title": "WALL SECTIONS AND STRUCTURAL DETAILS",
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 25,
      "sheet_num": "E-0.0",
      "sheet_title": "ELECTRICAL GENERAL NOTES",
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 2
    },
    {
      "page_idx": 26,
      "sheet_num": "E-1.0",
      "sheet_title": "BUILDING B ELECTRICAL POWER PLAN",
      "page_type": "schedule_sheet",
      "confidence": 0.7,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 1
    },
    {
      "page_idx": 27,
      "sheet_num": "E-2.0",
      "sheet_title": "BUILDING B ELECTRICAL LIGHTING PLAN",
      "page_type": "schedule_sheet",
      "confidence": 0.7,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 2
    },
    {
      "page_idx": 28,
      "sheet_num": "E-3.0",
      "sheet_title": "ELECTRICAL RISER AND SUB-PANELS",
      "page_type": "ceiling_plan",
      "confidence": 0.7,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 29,
      "sheet_num": "P-0.1",
      "sheet_title": "PLUMBING SITE PLAN",
      "page_type": "site_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 30,
      "sheet_num": "P-0.2",
      "sheet_title": "PLUMBING GENERAL NOTES",
      "page_type": "floor_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 31,
      "sheet_num": "P-1.0",
      "sheet_title": "BUILDING B - WATER - PLUMBING PLAN",
      "page_type": "mep_plan",
      "confidence": 0.3,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 32,
      "sheet_num": "P-2.0",
      "sheet_title": "BUILDING B - SANITARY - PLUMBING PLAN",
      "page_type": "mep_plan",
      "confidence": 0.3,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 33,
      "sheet_num": "P-3.0",
      "sheet_title": "BUILDING B - ROOF PLAN",
      "page_type": "roof_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 34,
      "sheet_num": "P-4.0",
      "sheet_title": "PLUMBING DETAILS",
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 35,
      "sheet_num": "M-1.0",
      "sheet_title": "MECHANICAL LAYOUT",
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 36,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 37,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 38,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 39,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 40,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 41,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 42,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 43,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 44,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 45,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 46,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 47,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 48,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 49,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 50,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 51,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 52,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 53,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 54,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 55,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 56,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 57,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 58,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 59,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 60,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 61,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 62,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 63,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 64,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 65,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 66,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 67,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 68,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "section",
      "confidence": 0.5,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 69,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "site_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 70,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "roof_plan",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 71,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "section",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 72,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 1
    },
    {
      "page_idx": 73,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 74,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "floor_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 75,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "floor_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 76,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "schedule_sheet",
      "confidence": 0.7,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 1
    },
    {
      "page_idx": 77,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 78,
      "sheet_num": "A-1.4",
      "sheet_title": "BUILDING A - ROOF PLAN",
      "page_type": "roof_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 79,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 80,
      "sheet_num": "A-2.1",
      "sheet_title": "BUILDING B - EXTERIOR ELEVATIONS",
      "page_type": "detail_sheet",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 81,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "section",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 82,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 83,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "ceiling_plan",
      "confidence": 0.7,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 1
    },
    {
      "page_idx": 84,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "section",
      "confidence": 0.7,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 85,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 86,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "framing_plan",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 2
    },
    {
      "page_idx": 87,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 88,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "section",
      "confidence": 0.5,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 89,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 90,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "framing_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 91,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 2
    },
    {
      "page_idx": 92,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "schedule_sheet",
      "confidence": 0.7,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 1
    },
    {
      "page_idx": 93,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "schedule_sheet",
      "confidence": 0.7,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 2
    },
    {
      "page_idx": 94,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "ceiling_plan",
      "confidence": 0.7,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 2
    },
    {
      "page_idx": 95,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "site_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 96,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "floor_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 97,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 98,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 99,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "roof_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 100,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 101,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 102,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "section",
      "confidence": 0.5,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 103,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "site_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 104,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "roof_plan",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 105,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "section",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 106,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 1
    },
    {
      "page_idx": 107,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 108,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "general_notes",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 1
    },
    {
      "page_idx": 109,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "floor_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 110,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "floor_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 111,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "schedule_sheet",
      "confidence": 0.7,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 1
    },
    {
      "page_idx": 112,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 113,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "roof_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 114,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 115,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 116,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "section",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 117,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 118,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "schedule_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 2
    },
    {
      "page_idx": 119,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "ceiling_plan",
      "confidence": 0.7,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 1
    },
    {
      "page_idx": 120,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "section",
      "confidence": 0.7,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 121,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 122,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "framing_plan",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 2
    },
    {
      "page_idx": 123,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 124,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 125,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "framing_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 126,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 127,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 2
    },
    {
      "page_idx": 128,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "schedule_sheet",
      "confidence": 0.7,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 1
    },
    {
      "page_idx": 129,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "schedule_sheet",
      "confidence": 0.7,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 2
    },
    {
      "page_idx": 130,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "ceiling_plan",
      "confidence": 0.7,
      "has_legend": true,
      "has_schedule": false,
      "legend_count": 1
    },
    {
      "page_idx": 131,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "site_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 132,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "floor_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 133,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 134,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 135,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "roof_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 136,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 137,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    }
  ]
}
##DIAG_END:page_type_histogram:vine-street##

## §2 — Block 2: Schedule-Bearing Audit

Heuristic: `is_schedule_bearing = 'SCHEDULE' in (sheet_title or '').upper()`. Not real ground truth — tests whether the sheet's title self-identifies as schedule-bearing.

##DIAG_START:schedule_bearing_audit:vine-street##
{
  "total_schedule_bearing": 0,
  "classified_as_schedule_sheet": 0,
  "classified_as_other_count": 0,
  "other_classification_breakdown": {},
  "schedule_bearing_pages": [],
  "other_classified_pages": []
}
##DIAG_END:schedule_bearing_audit:vine-street##

## §3 — Block 4: Reclassification Simulation (SCHEDULE rule moved to position 0)

##DIAG_START:reclassification_simulation:vine-street##
{
  "total_pages": 138,
  "total_changed": 32,
  "transition_histogram": {
    "detail_sheet -> schedule_sheet": 9,
    "floor_plan -> schedule_sheet": 6,
    "ceiling_plan -> schedule_sheet": 6,
    "roof_plan -> schedule_sheet": 3,
    "elevation -> schedule_sheet": 3,
    "framing_plan -> schedule_sheet": 3,
    "mep_plan -> unknown": 2
  },
  "schedule_bearing_pages_not_currently_sched": 0,
  "schedule_bearing_pages_flipped_to_sched": 0,
  "schedule_bearing_flip_coverage": null,
  "new_misclassifications_count": 30,
  "new_misclassifications_sample": [
    {
      "page_idx": 2,
      "sheet_num": "G-2.0",
      "sheet_title": "CODE ANALYSIS",
      "current_type": "roof_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 8,
      "sheet_num": "A-1.0",
      "sheet_title": "BUILDING B - NOTED FRAMING PLAN",
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 13,
      "sheet_num": "A-2.2",
      "sheet_title": "EXTERIOR DETAILS AND SECTIONS",
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 17,
      "sheet_num": "A-4.0",
      "sheet_title": "BUILDING B - REFLECTIVE CEILING PLAN",
      "current_type": "ceiling_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 1
    },
    {
      "page_idx": 19,
      "sheet_num": "S-0.2",
      "sheet_title": "GENERAL NOTES",
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 1
    },
    {
      "page_idx": 21,
      "sheet_num": "A1",
      "sheet_title": "",
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 23,
      "sheet_num": "S-3.0",
      "sheet_title": "ROOF FRAMING PLAN",
      "current_type": "framing_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 28,
      "sheet_num": "E-3.0",
      "sheet_title": "ELECTRICAL RISER AND SUB-PANELS",
      "current_type": "ceiling_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 1
    },
    {
      "page_idx": 30,
      "sheet_num": "P-0.2",
      "sheet_title": "PLUMBING GENERAL NOTES",
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 35,
      "sheet_num": "M-1.0",
      "sheet_title": "MECHANICAL LAYOUT",
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 70,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "roof_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 75,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 80,
      "sheet_num": "A-2.1",
      "sheet_title": "BUILDING B - EXTERIOR ELEVATIONS",
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 83,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "ceiling_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 1
    },
    {
      "page_idx": 85,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 1
    },
    {
      "page_idx": 87,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 90,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "framing_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 94,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "ceiling_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 2
    },
    {
      "page_idx": 96,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 101,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    }
  ],
  "changed_pages": [
    {
      "page_idx": 2,
      "sheet_num": "G-2.0",
      "sheet_title": "CODE ANALYSIS",
      "current_type": "roof_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 8,
      "sheet_num": "A-1.0",
      "sheet_title": "BUILDING B - NOTED FRAMING PLAN",
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 13,
      "sheet_num": "A-2.2",
      "sheet_title": "EXTERIOR DETAILS AND SECTIONS",
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 17,
      "sheet_num": "A-4.0",
      "sheet_title": "BUILDING B - REFLECTIVE CEILING PLAN",
      "current_type": "ceiling_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 1
    },
    {
      "page_idx": 19,
      "sheet_num": "S-0.2",
      "sheet_title": "GENERAL NOTES",
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 1
    },
    {
      "page_idx": 21,
      "sheet_num": "A1",
      "sheet_title": "",
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 23,
      "sheet_num": "S-3.0",
      "sheet_title": "ROOF FRAMING PLAN",
      "current_type": "framing_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 28,
      "sheet_num": "E-3.0",
      "sheet_title": "ELECTRICAL RISER AND SUB-PANELS",
      "current_type": "ceiling_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 1
    },
    {
      "page_idx": 30,
      "sheet_num": "P-0.2",
      "sheet_title": "PLUMBING GENERAL NOTES",
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 31,
      "sheet_num": "P-1.0",
      "sheet_title": "BUILDING B - WATER - PLUMBING PLAN",
      "current_type": "mep_plan",
      "simulated_type": "unknown",
      "simulated_confidence": 0.0,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 32,
      "sheet_num": "P-2.0",
      "sheet_title": "BUILDING B - SANITARY - PLUMBING PLAN",
      "current_type": "mep_plan",
      "simulated_type": "unknown",
      "simulated_confidence": 0.0,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 35,
      "sheet_num": "M-1.0",
      "sheet_title": "MECHANICAL LAYOUT",
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 70,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "roof_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 75,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 80,
      "sheet_num": "A-2.1",
      "sheet_title": "BUILDING B - EXTERIOR ELEVATIONS",
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 83,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "ceiling_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 1
    },
    {
      "page_idx": 85,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 1
    },
    {
      "page_idx": 87,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 90,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "framing_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 94,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "ceiling_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 2
    },
    {
      "page_idx": 96,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 101,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 104,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "roof_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 110,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 115,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 119,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "ceiling_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 1
    },
    {
      "page_idx": 121,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 1
    },
    {
      "page_idx": 123,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 125,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "framing_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 130,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "ceiling_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 1
    },
    {
      "page_idx": 132,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 137,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 0
    }
  ],
  "schedule_bearing_flip_pages": []
}
##DIAG_END:reclassification_simulation:vine-street##

## §4 — Block 5: Table Extraction Validation

For pages that flipped from non-SCHEDULE_SHEET to SCHEDULE_SHEET under Block 4's simulation, run `extract_tables` and measure. Hard cap: 20 pages per bidset, ranked by `legend_count` descending. Wall-clock soft cap recorded; hard cap 360s aborts further pages.

##DIAG_START:table_extraction_validation:vine-street##
{
  "total_changed_to_sched": 30,
  "page_cap_applied": true,
  "page_cap": 20,
  "pages_validated": 20,
  "total_tables_extracted": 172,
  "total_rows_extracted": 980,
  "wallclock_seconds": 126.687,
  "pages_with_tables": 20,
  "extraction_errors": [],
  "per_page": [
    {
      "page_idx": 94,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "ceiling_plan",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 5,
      "total_rows": 12,
      "headers_first5": [
        "GENERAL NOTES NOTE:\nELECTRIC SERVICE AND METER\nLOCATED ON BUILDING B",
        "1440 EXT WALL LIGHT\n840 EXT WALL LIGHT\n1320 EXT WALL LIGHT\n- SPARE S - B 20/1 5 ",
        "C G\nD H\nEL\nE I",
        "ECTRICAL CONTRACTOR\nTO VERIFY LOCATION",
        ""
      ],
      "wallclock_seconds": 37.6804,
      "legend_count": 2
    },
    {
      "page_idx": 17,
      "sheet_num": "A-4.0",
      "sheet_title": "BUILDING B - REFLECTIVE CEILING PLAN",
      "current_type": "ceiling_plan",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 5,
      "total_rows": 25,
      "headers_first5": [
        "LIGHTING FIXTURE SCHEDULE",
        "",
        "",
        "",
        "REV DATE"
      ],
      "wallclock_seconds": 1.4284,
      "legend_count": 1
    },
    {
      "page_idx": 19,
      "sheet_num": "S-0.2",
      "sheet_title": "GENERAL NOTES",
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 13,
      "total_rows": 51,
      "headers_first5": [
        "",
        "",
        "",
        "",
        ""
      ],
      "wallclock_seconds": 1.5713,
      "legend_count": 1
    },
    {
      "page_idx": 28,
      "sheet_num": "E-3.0",
      "sheet_title": "ELECTRICAL RISER AND SUB-PANELS",
      "current_type": "ceiling_plan",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 9,
      "total_rows": 95,
      "headers_first5": [
        "GENERAL NOTES",
        "SUBPANEL: \"U\" = UNITS: C,D,E,F,G,H,I",
        "SUBPANEL: \"HP\"",
        "",
        "CONDUIT AND CONDUCTOR SCHEDULE"
      ],
      "wallclock_seconds": 2.2004,
      "legend_count": 1
    },
    {
      "page_idx": 83,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "ceiling_plan",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 3,
      "total_rows": 24,
      "headers_first5": [
        "LIGHTING FIXTURE SCHEDULE",
        "",
        "REV DATE"
      ],
      "wallclock_seconds": 0.9199,
      "legend_count": 1
    },
    {
      "page_idx": 85,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 12,
      "total_rows": 66,
      "headers_first5": [
        "",
        "",
        "",
        "",
        ""
      ],
      "wallclock_seconds": 1.4895,
      "legend_count": 1
    },
    {
      "page_idx": 119,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "ceiling_plan",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 5,
      "total_rows": 26,
      "headers_first5": [
        "LIGHTING FIXTURE SCHEDULE",
        "",
        "",
        "",
        "REV DATE"
      ],
      "wallclock_seconds": 1.4752,
      "legend_count": 1
    },
    {
      "page_idx": 121,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 13,
      "total_rows": 63,
      "headers_first5": [
        "",
        "",
        "",
        "",
        ""
      ],
      "wallclock_seconds": 1.4401,
      "legend_count": 1
    },
    {
      "page_idx": 130,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "ceiling_plan",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 2,
      "total_rows": 4,
      "headers_first5": [
        "WEEKS ARCHITECTURE AND DESI",
        "CEPT/ TIMER 20/1\nCEPT/ TIMER 20/1 1 A\n3 B 2 20/1 SHEL\n4 20/1 REST L LIGHTS 960\n."
      ],
      "wallclock_seconds": 45.4503,
      "legend_count": 1
    },
    {
      "page_idx": 2,
      "sheet_num": "G-2.0",
      "sheet_title": "CODE ANALYSIS",
      "current_type": "roof_plan",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 12,
      "total_rows": 104,
      "headers_first5": [
        "",
        "ARCH. GENERAL NOTES",
        "ARCH. SYMBOLS LEGEND",
        "CODE SUMMARY INFORMATION",
        "SHEET INDEX"
      ],
      "wallclock_seconds": 3.1973,
      "legend_count": 0
    },
    {
      "page_idx": 8,
      "sheet_num": "A-1.0",
      "sheet_title": "BUILDING B - NOTED FRAMING PLAN",
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 11,
      "total_rows": 58,
      "headers_first5": [
        "",
        "",
        "",
        "AREA CALCS PER UNIT",
        "18'-10\" 45'-2\" 18'-10\" 20'-1\" 21'-4\""
      ],
      "wallclock_seconds": 1.812,
      "legend_count": 0
    },
    {
      "page_idx": 13,
      "sheet_num": "A-2.2",
      "sheet_title": "EXTERIOR DETAILS AND SECTIONS",
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 5,
      "total_rows": 46,
      "headers_first5": [
        "",
        "NIM\n\"4\n3\" MIN",
        "",
        "",
        "REV DATE"
      ],
      "wallclock_seconds": 2.593,
      "legend_count": 0
    },
    {
      "page_idx": 21,
      "sheet_num": "A1",
      "sheet_title": "",
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 19,
      "total_rows": 74,
      "headers_first5": [
        "STEM WALL - CHART",
        "",
        "",
        "",
        "BLOCK WALL FILL CELLS"
      ],
      "wallclock_seconds": 1.8882,
      "legend_count": 0
    },
    {
      "page_idx": 23,
      "sheet_num": "S-3.0",
      "sheet_title": "ROOF FRAMING PLAN",
      "current_type": "framing_plan",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 11,
      "total_rows": 51,
      "headers_first5": [
        "",
        "",
        "",
        "*",
        "ANGLE SIZE\n\"D\""
      ],
      "wallclock_seconds": 2.6374,
      "legend_count": 0
    },
    {
      "page_idx": 30,
      "sheet_num": "P-0.2",
      "sheet_title": "PLUMBING GENERAL NOTES",
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 5,
      "total_rows": 24,
      "headers_first5": [
        "PLUMBING SPECIFICATIONS",
        "PLUMBING FIXTURE SCHEDULE",
        "",
        "BASIC PLUMBING MATERIAL\nREQUIREMENTS:",
        "REV DATE"
      ],
      "wallclock_seconds": 1.1749,
      "legend_count": 0
    },
    {
      "page_idx": 35,
      "sheet_num": "M-1.0",
      "sheet_title": "MECHANICAL LAYOUT",
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 5,
      "total_rows": 27,
      "headers_first5": [
        "UNIT SCHEDULE",
        "TYPE DESCRIPTION\nSURFACE MOUNTED LIGHT FIXTURE/ FAN COMBO,\n800 LUMEN LED, BLACK ",
        "",
        "FAN SCHEDULE",
        "REV DATE"
      ],
      "wallclock_seconds": 7.311,
      "legend_count": 0
    },
    {
      "page_idx": 70,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "roof_plan",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 11,
      "total_rows": 96,
      "headers_first5": [
        "ARCH. GENERAL NOTES",
        "ARCH. SYMBOLS LEGEND",
        "CODE SUMMARY INFORMATION",
        "SHEET INDEX",
        ""
      ],
      "wallclock_seconds": 3.7366,
      "legend_count": 0
    },
    {
      "page_idx": 75,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "floor_plan",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 7,
      "total_rows": 23,
      "headers_first5": [
        "BLOCK WALL FILL CE",
        "",
        "AREA CALCS PER UNIT",
        "",
        ""
      ],
      "wallclock_seconds": 3.7749,
      "legend_count": 0
    },
    {
      "page_idx": 80,
      "sheet_num": "A-2.1",
      "sheet_title": "BUILDING B - EXTERIOR ELEVATIONS",
      "current_type": "detail_sheet",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 3,
      "total_rows": 39,
      "headers_first5": [
        "WEEKS ARCHITECTURE AND DESIGN",
        "",
        "REV DATE"
      ],
      "wallclock_seconds": 2.6893,
      "legend_count": 0
    },
    {
      "page_idx": 87,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 16,
      "total_rows": 72,
      "headers_first5": [
        "",
        "STEM WALL - CHART",
        "",
        "7\n6'-4\" 4'-0\" 6'-4\" 1 1\n\" 5'-4 \"\n2 3'-0\" 2 9'-0\" 1'-4\" 8'-7\" 11'-10\" 8'-7\"",
        "F1"
      ],
      "wallclock_seconds": 2.217,
      "legend_count": 0
    }
  ],
  "aborted_due_to_hard_cap": false,
  "hard_cap_seconds": 360.0
}
##DIAG_END:table_extraction_validation:vine-street##

## §5 — Cross-Reference With Sweep Section 3

For each page in §4 that produced ≥2 tables under validation, the page's section-3 entry from `SWEEP_OBSERVATION_<bidset>.md` carried these signals at sweep ship time (`legend_count`, `has_legend`, `page_type`). Same `legend_count` is replicated below from this run's Block 1.

| Page | Sheet | Title | Current type | Tables | Legend count |
|---:|---|---|---|---:|---:|
| 94 | `None` |  | `ceiling_plan` | 5 | 2 |
| 17 | `A-4.0` | BUILDING B - REFLECTIVE CEILING PLAN | `ceiling_plan` | 5 | 1 |
| 19 | `S-0.2` | GENERAL NOTES | `detail_sheet` | 13 | 1 |
| 28 | `E-3.0` | ELECTRICAL RISER AND SUB-PANELS | `ceiling_plan` | 9 | 1 |
| 83 | `None` |  | `ceiling_plan` | 3 | 1 |
| 85 | `None` |  | `detail_sheet` | 12 | 1 |
| 119 | `None` |  | `ceiling_plan` | 5 | 1 |
| 121 | `None` |  | `detail_sheet` | 13 | 1 |
| 130 | `None` |  | `ceiling_plan` | 2 | 1 |
| 2 | `G-2.0` | CODE ANALYSIS | `roof_plan` | 12 | 0 |
| 8 | `A-1.0` | BUILDING B - NOTED FRAMING PLAN | `floor_plan` | 11 | 0 |
| 13 | `A-2.2` | EXTERIOR DETAILS AND SECTIONS | `detail_sheet` | 5 | 0 |
| 21 | `A1` |  | `elevation` | 19 | 0 |
| 23 | `S-3.0` | ROOF FRAMING PLAN | `framing_plan` | 11 | 0 |
| 30 | `P-0.2` | PLUMBING GENERAL NOTES | `floor_plan` | 5 | 0 |
| 35 | `M-1.0` | MECHANICAL LAYOUT | `detail_sheet` | 5 | 0 |
| 70 | `None` |  | `roof_plan` | 11 | 0 |
| 75 | `None` |  | `floor_plan` | 7 | 0 |
| 80 | `A-2.1` | BUILDING B - EXTERIOR ELEVATIONS | `detail_sheet` | 3 | 0 |
| 87 | `None` |  | `elevation` | 16 | 0 |

## §6 — Observations (no fixes, no recommendations)

- Observed: bidset has 138 pages total, 35 mapped to sheets, 34 pages with `has_legend=True` after Filter 4, 25 with `has_schedule=True`.
- Observed: page-type histogram shows 11 pages classified as `schedule_sheet` by current dispatch ordering.
- Observed: 0 pages have 'SCHEDULE' in sheet title (heuristic). Of those, 0 currently classify as `schedule_sheet`; 0 classify as something else. Other-classification breakdown: {}.
- Observed: under SCHEDULE-first simulation, 32 of 138 pages would change classification. Of the 0 schedule-bearing pages NOT currently classified as `schedule_sheet`, 0 would flip to `schedule_sheet` under simulation.
- Observed: simulation produced 30 pages newly classified as `schedule_sheet` whose sheet title does NOT contain 'SCHEDULE'. Documented per orders §7 stop #9 as soft observation; sample of up to 20 in the Block 4 payload.
- Observed: of 20 flipped pages validated in Block 5, 20 produced ≥1 table. Total 172 tables / 980 rows extracted in 126.69s. Cap applied: True.

## §7 — Closing

Diagnostic only. Three coupled bugs hypothesized by extended-thinking Claude 2026-04-29 are tested by this report's data. The gate report (separate file) summarizes hypothesis status across all three bidsets. No fixes were attempted. dispatch_gate.py and trade_input_builder.py NOT modified. Vault rule held — five vault-ruled modules untouched.
