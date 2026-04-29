# Page-Type Verification — Shoppes at Avalon — Spring Hill — MEC

**Date:** 2026-04-29
**Phase:** Page-type verification + coupling diagnostic
**Bidset file:** `C:\huck stage 2\full bid sets\Shoppes at Avalon - Spring Hill - MEC.pdf`
**Page count:** 97
**Dispatch wall-clock:** 59.27s

**Type of artifact:** read-only verification, no fixes. Tests three coupled bugs hypothesized by extended-thinking Claude on 2026-04-29. dispatch_gate.py and trade_input_builder.py read-only this phase per orders §0; vault rule active on the five vault-ruled modules (none opened). The gate report (`backend/PAGE_TYPE_VERIFICATION_GATE_REPORT.md`) summarizes hypothesis status across all three bidsets.

---

## §1 — Block 1: Page-Type Histogram

##DIAG_START:page_type_histogram:shoppes-at-avalon##
{
  "total_pages": 97,
  "total_mapped_pages": 19,
  "total_pages_has_legend": 1,
  "total_pages_has_schedule": 1,
  "histogram": {
    "unknown": 34,
    "detail_sheet": 31,
    "elevation": 14,
    "roof_plan": 4,
    "ceiling_plan": 4,
    "floor_plan": 4,
    "section": 4,
    "general_notes": 1,
    "framing_plan": 1
  },
  "per_page": [
    {
      "page_idx": 0,
      "sheet_num": "LS-101",
      "sheet_title": "LIFE SAFETY PLAN",
      "page_type": "roof_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 1,
      "sheet_num": "A-601",
      "sheet_title": "DOOR TYPES, SCHEDULES, AND DETAILS",
      "page_type": "elevation",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 2,
      "sheet_num": "G-003",
      "sheet_title": "WALL TYPES",
      "page_type": "elevation",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 3,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "ceiling_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 4,
      "sheet_num": "A-402",
      "sheet_title": "DUMPSTER ENCLOSURE PLANS AND DETAILS",
      "page_type": "general_notes",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 5,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "roof_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 6,
      "sheet_num": "A-102",
      "sheet_title": "DIMENSIONED BUILDING PLAN",
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 7,
      "sheet_num": "A-111",
      "sheet_title": "REFLECTED CEILING PLAN",
      "page_type": "ceiling_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 8,
      "sheet_num": "A-101",
      "sheet_title": "OVERALL BUILDING PLAN",
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 9,
      "sheet_num": "A-306",
      "sheet_title": "BUILDING SECTIONS AND ROOF ACCESS LADDER DETAILS",
      "page_type": "elevation",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 10,
      "sheet_num": "A-301",
      "sheet_title": "WALL SECTIONS",
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 11,
      "sheet_num": "A-302",
      "sheet_title": "WALL SECTIONS",
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 12,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 13,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 14,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
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
      "sheet_num": "A-401",
      "sheet_title": "PLAN DETAILS",
      "page_type": "detail_sheet",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 17,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 18,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 19,
      "sheet_num": "A-602",
      "sheet_title": "WINDOW TYPES",
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 20,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 21,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 22,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 23,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 24,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 25,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 26,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 27,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 28,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 29,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 30,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 31,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "roof_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 32,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 33,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 34,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 35,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 36,
      "sheet_num": "A-100",
      "sheet_title": "ARCHITECTURAL SITE PLAN",
      "page_type": "elevation",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 37,
      "sheet_num": "A-201",
      "sheet_title": "EXTERIOR ELEVATIONS",
      "page_type": "floor_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 38,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "floor_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 39,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "ceiling_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 40,
      "sheet_num": "A-121",
      "sheet_title": "ROOF PLAN",
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 41,
      "sheet_num": "A-303",
      "sheet_title": "WALL SECTIONS",
      "page_type": "elevation",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 42,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 43,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 44,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 45,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "section",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 46,
      "sheet_num": "A-304",
      "sheet_title": "WALL SECTIONS",
      "page_type": "section",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 47,
      "sheet_num": "A-305",
      "sheet_title": "WALL SECTIONS",
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 48,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 49,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 50,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 51,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 52,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
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
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 64,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "roof_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 65,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 66,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 67,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 68,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 69,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 70,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "floor_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 71,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "floor_plan",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 72,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "ceiling_plan",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 73,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 74,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "elevation",
      "confidence": 0.7,
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
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 77,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 78,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "section",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 79,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "section",
      "confidence": 0.7,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 80,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
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
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 84,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 85,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "detail_sheet",
      "confidence": 0.9,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 86,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 87,
      "sheet_num": "S-401",
      "sheet_title": "FRAMING DETAILS",
      "page_type": "framing_plan",
      "confidence": 0.9,
      "has_legend": true,
      "has_schedule": true,
      "legend_count": 1
    },
    {
      "page_idx": 88,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 89,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 90,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 91,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 92,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 93,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 94,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 95,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    },
    {
      "page_idx": 96,
      "sheet_num": null,
      "sheet_title": null,
      "page_type": "unknown",
      "confidence": 0.0,
      "has_legend": false,
      "has_schedule": false,
      "legend_count": 0
    }
  ]
}
##DIAG_END:page_type_histogram:shoppes-at-avalon##

## §2 — Block 2: Schedule-Bearing Audit

Heuristic: `is_schedule_bearing = 'SCHEDULE' in (sheet_title or '').upper()`. Not real ground truth — tests whether the sheet's title self-identifies as schedule-bearing.

##DIAG_START:schedule_bearing_audit:shoppes-at-avalon##
{
  "total_schedule_bearing": 1,
  "classified_as_schedule_sheet": 0,
  "classified_as_other_count": 1,
  "other_classification_breakdown": {
    "elevation": 1
  },
  "schedule_bearing_pages": [
    {
      "page_idx": 1,
      "sheet_num": "A-601",
      "sheet_title": "DOOR TYPES, SCHEDULES, AND DETAILS",
      "current_type": "elevation"
    }
  ],
  "other_classified_pages": [
    {
      "page_idx": 1,
      "sheet_num": "A-601",
      "sheet_title": "DOOR TYPES, SCHEDULES, AND DETAILS",
      "current_type": "elevation"
    }
  ]
}
##DIAG_END:schedule_bearing_audit:shoppes-at-avalon##

## §3 — Block 4: Reclassification Simulation (SCHEDULE rule moved to position 0)

##DIAG_START:reclassification_simulation:shoppes-at-avalon##
{
  "total_pages": 97,
  "total_changed": 13,
  "transition_histogram": {
    "elevation -> schedule_sheet": 9,
    "roof_plan -> schedule_sheet": 2,
    "ceiling_plan -> schedule_sheet": 1,
    "framing_plan -> schedule_sheet": 1
  },
  "schedule_bearing_pages_not_currently_sched": 1,
  "schedule_bearing_pages_flipped_to_sched": 1,
  "schedule_bearing_flip_coverage": 1.0,
  "new_misclassifications_count": 12,
  "new_misclassifications_sample": [
    {
      "page_idx": 0,
      "sheet_num": "LS-101",
      "sheet_title": "LIFE SAFETY PLAN",
      "current_type": "roof_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 3,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "ceiling_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 5,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "roof_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 18,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 32,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 33,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 41,
      "sheet_num": "A-303",
      "sheet_title": "WALL SECTIONS",
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 42,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 65,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 66,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 74,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 87,
      "sheet_num": "S-401",
      "sheet_title": "FRAMING DETAILS",
      "current_type": "framing_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 1
    }
  ],
  "changed_pages": [
    {
      "page_idx": 0,
      "sheet_num": "LS-101",
      "sheet_title": "LIFE SAFETY PLAN",
      "current_type": "roof_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 1,
      "sheet_num": "A-601",
      "sheet_title": "DOOR TYPES, SCHEDULES, AND DETAILS",
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 3,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "ceiling_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 5,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "roof_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 18,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 32,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 33,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 41,
      "sheet_num": "A-303",
      "sheet_title": "WALL SECTIONS",
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 42,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 65,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 66,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 74,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    },
    {
      "page_idx": 87,
      "sheet_num": "S-401",
      "sheet_title": "FRAMING DETAILS",
      "current_type": "framing_plan",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.9,
      "changed": true,
      "legend_count": 1
    }
  ],
  "schedule_bearing_flip_pages": [
    {
      "page_idx": 1,
      "sheet_num": "A-601",
      "sheet_title": "DOOR TYPES, SCHEDULES, AND DETAILS",
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "simulated_confidence": 0.7,
      "changed": true,
      "legend_count": 0
    }
  ]
}
##DIAG_END:reclassification_simulation:shoppes-at-avalon##

## §4 — Block 5: Table Extraction Validation

For pages that flipped from non-SCHEDULE_SHEET to SCHEDULE_SHEET under Block 4's simulation, run `extract_tables` and measure. Hard cap: 20 pages per bidset, ranked by `legend_count` descending. Wall-clock soft cap recorded; hard cap 360s aborts further pages.

##DIAG_START:table_extraction_validation:shoppes-at-avalon##
{
  "total_changed_to_sched": 13,
  "page_cap_applied": false,
  "page_cap": 20,
  "pages_validated": 13,
  "total_tables_extracted": 558,
  "total_rows_extracted": 2236,
  "wallclock_seconds": 61.5466,
  "pages_with_tables": 13,
  "extraction_errors": [],
  "per_page": [
    {
      "page_idx": 87,
      "sheet_num": "S-401",
      "sheet_title": "FRAMING DETAILS",
      "current_type": "framing_plan",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 10,
      "total_rows": 48,
      "headers_first5": [
        "5\" lc:f'-c::fll\n(1",
        "I\nl\nt I\nI\nI ' '\n22KC-54 '\n6AR JOI :>T5 I\nI\nI I\nI\nI\nI\nI\nI\nL_\n-- '\nI-- ---\nf- --- ",
        ".\" \\\nC)\nI\nC)\n,I)\n/\n..v",
        "\u2022",
        "PRINT RECORD"
      ],
      "wallclock_seconds": 0.6999,
      "legend_count": 1
    },
    {
      "page_idx": 0,
      "sheet_num": "LS-101",
      "sheet_title": "LIFE SAFETY PLAN",
      "current_type": "roof_plan",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 33,
      "total_rows": 124,
      "headers_first5": [
        "DRAWING INDEX\nGENERAL\nSHEET TITLE\nG-001 COVER SHEET\nG-002 GENERAL NOTES AND ABBR",
        "GENERAL",
        "G-001 COVER SHEET",
        "Tel: 770 -910- 9740",
        "ARCHITECTURAL"
      ],
      "wallclock_seconds": 7.565,
      "legend_count": 0
    },
    {
      "page_idx": 1,
      "sheet_num": "A-601",
      "sheet_title": "DOOR TYPES, SCHEDULES, AND DETAILS",
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 98,
      "total_rows": 385,
      "headers_first5": [
        "FIRE MARSHAL CONDITIONS OF APPROVA L-APPLICABLE CODES: NFPA 101 LIF",
        "SPRINKLER SYSTEM NOTES:",
        "FIREWALL OUTLET",
        "DOORS AND ACCESSIBILITY",
        "BASE BUILDING INSULATION MUST BE LOCATED AT THE ROOF, NOT THE CEILING,"
      ],
      "wallclock_seconds": 4.9916,
      "legend_count": 0
    },
    {
      "page_idx": 3,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "ceiling_plan",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 6,
      "total_rows": 27,
      "headers_first5": [
        "Tel: 770 - 910- 9740",
        "LEGEND AND GENERAL NOTES:",
        "THIS DRAWING IS THE PROPERTY OF MAXDESIGN GROUP,",
        "OFFICE BUILDING\nFE\nTOTAL LEASABLE SQUARE\nFOOTAGE = 4,351 SF\n30 PEOPLE\nS\n9'\n7\n36\"",
        ""
      ],
      "wallclock_seconds": 1.1415,
      "legend_count": 0
    },
    {
      "page_idx": 5,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "roof_plan",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 14,
      "total_rows": 47,
      "headers_first5": [
        "KEY NOTE LEGEND",
        "1 CONCRETE SIDEWALK, BROOM FINISH W/ JOINTS AT 6'-0\" MAX - REFER TO CIVIL DWGS F",
        "1",
        "Tel: 770 - 910- 9740",
        "6"
      ],
      "wallclock_seconds": 1.8377,
      "legend_count": 0
    },
    {
      "page_idx": 18,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 21,
      "total_rows": 89,
      "headers_first5": [
        "DOOR SCHEDULE",
        "DOOR HARDWARE",
        "100 LOBBY ENTRY DOOR ALUM/GLASS STOREFRONT DOOR TYPE-B REFER TO ELEVATION 3' - 0",
        "Tel: 770 - 910- 9740",
        "1."
      ],
      "wallclock_seconds": 1.1752,
      "legend_count": 0
    },
    {
      "page_idx": 32,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 106,
      "total_rows": 414,
      "headers_first5": [
        "FIRE MARSHAL CONDITIONS OF APPROVA L-APPLICABLE CODES: NFPA 101 LIF",
        "SPRINKLER SYSTEM NOTES:",
        "FIREWALL OUTLET",
        "DOORS AND ACCESSIBILITY",
        "BASE BUILDING INSULATION MUST BE LOCATED AT THE ROOF, NOT THE CEILING,"
      ],
      "wallclock_seconds": 5.6411,
      "legend_count": 0
    },
    {
      "page_idx": 33,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 64,
      "total_rows": 222,
      "headers_first5": [
        "WALL SCHEDULE",
        "Tel: 770 - 910 - 9740",
        "NOT TO BE USED ON ANOTHER PROJECT AND SHALL BE",
        "DIETRICH FTC -",
        "BELOW - 8\" (NOM.) CONCRETE BLOCK W/ REINFORCING AND FOAM INSULATION FILLED CELLS"
      ],
      "wallclock_seconds": 2.951,
      "legend_count": 0
    },
    {
      "page_idx": 41,
      "sheet_num": "A-303",
      "sheet_title": "WALL SECTIONS",
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 22,
      "total_rows": 104,
      "headers_first5": [
        "",
        "",
        "5\nM-3\nEF-4\n19 19\nP-1 P-1\nEF-1\nST-1 M-3\n18 18\n20\n4\nEF-4\n4\nEF-4\n14\n19 19\n13\nP-1 P-",
        "19' -",
        "NOT TO BE USED ON ANOTHER PROJECT AND SHALL BE"
      ],
      "wallclock_seconds": 7.6558,
      "legend_count": 0
    },
    {
      "page_idx": 42,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 24,
      "total_rows": 118,
      "headers_first5": [
        "T.O. HIGH PARAPET",
        "",
        "",
        "Tel: 770 - 910 - 9740",
        "T.O. MID PARAPET"
      ],
      "wallclock_seconds": 8.071,
      "legend_count": 0
    },
    {
      "page_idx": 65,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 98,
      "total_rows": 387,
      "headers_first5": [
        "FIRE MARSHAL CONDITIONS OF APPROVA L-APPLICABLE CODES: NFPA 101 LIF",
        "SPRINKLER SYSTEM NOTES:",
        "FIREWALL OUTLET",
        "DOORS AND ACCESSIBILITY",
        "BASE BUILDING INSULATION MUST BE LOCATED AT THE ROOF, NOT THE CEILING,"
      ],
      "wallclock_seconds": 5.6972,
      "legend_count": 0
    },
    {
      "page_idx": 66,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 45,
      "total_rows": 173,
      "headers_first5": [
        "WALL SCHEDULE",
        "MIN.",
        "Tel: 770 - 910 - 9740",
        "THIS DRAWING IS THE PROPERTY OF MAXDESIGN GROUP,",
        "DIETRICH FTC - 500 WITH"
      ],
      "wallclock_seconds": 2.5787,
      "legend_count": 0
    },
    {
      "page_idx": 74,
      "sheet_num": null,
      "sheet_title": null,
      "current_type": "elevation",
      "simulated_type": "schedule_sheet",
      "tables_extracted": 17,
      "total_rows": 98,
      "headers_first5": [
        "",
        "T.O. HIGH PARAPET",
        "",
        "Tel: 770 - 910 - 9740",
        ""
      ],
      "wallclock_seconds": 11.5409,
      "legend_count": 0
    }
  ],
  "aborted_due_to_hard_cap": false,
  "hard_cap_seconds": 360.0
}
##DIAG_END:table_extraction_validation:shoppes-at-avalon##

## §5 — Cross-Reference With Sweep Section 3

For each page in §4 that produced ≥2 tables under validation, the page's section-3 entry from `SWEEP_OBSERVATION_<bidset>.md` carried these signals at sweep ship time (`legend_count`, `has_legend`, `page_type`). Same `legend_count` is replicated below from this run's Block 1.

| Page | Sheet | Title | Current type | Tables | Legend count |
|---:|---|---|---|---:|---:|
| 87 | `S-401` | FRAMING DETAILS | `framing_plan` | 10 | 1 |
| 0 | `LS-101` | LIFE SAFETY PLAN | `roof_plan` | 33 | 0 |
| 1 | `A-601` | DOOR TYPES, SCHEDULES, AND DETAILS | `elevation` | 98 | 0 |
| 3 | `None` |  | `ceiling_plan` | 6 | 0 |
| 5 | `None` |  | `roof_plan` | 14 | 0 |
| 18 | `None` |  | `elevation` | 21 | 0 |
| 32 | `None` |  | `elevation` | 106 | 0 |
| 33 | `None` |  | `elevation` | 64 | 0 |
| 41 | `A-303` | WALL SECTIONS | `elevation` | 22 | 0 |
| 42 | `None` |  | `elevation` | 24 | 0 |
| 65 | `None` |  | `elevation` | 98 | 0 |
| 66 | `None` |  | `elevation` | 45 | 0 |
| 74 | `None` |  | `elevation` | 17 | 0 |

## §6 — Observations (no fixes, no recommendations)

- Observed: bidset has 97 pages total, 19 mapped to sheets, 1 pages with `has_legend=True` after Filter 4, 1 with `has_schedule=True`.
- Observed: page-type histogram shows 0 pages classified as `schedule_sheet` by current dispatch ordering.
- Observed: 1 pages have 'SCHEDULE' in sheet title (heuristic). Of those, 0 currently classify as `schedule_sheet`; 1 classify as something else. Other-classification breakdown: {'elevation': 1}.
- Observed: under SCHEDULE-first simulation, 13 of 97 pages would change classification. Of the 1 schedule-bearing pages NOT currently classified as `schedule_sheet`, 1 would flip to `schedule_sheet` under simulation.
- Observed: simulation produced 12 pages newly classified as `schedule_sheet` whose sheet title does NOT contain 'SCHEDULE'. Documented per orders §7 stop #9 as soft observation; sample of up to 20 in the Block 4 payload.
- Observed: of 13 flipped pages validated in Block 5, 13 produced ≥1 table. Total 558 tables / 2236 rows extracted in 61.55s. Cap applied: False.

## §7 — Closing

Diagnostic only. Three coupled bugs hypothesized by extended-thinking Claude 2026-04-29 are tested by this report's data. The gate report (separate file) summarizes hypothesis status across all three bidsets. No fixes were attempted. dispatch_gate.py and trade_input_builder.py NOT modified. Vault rule held — five vault-ruled modules untouched.
