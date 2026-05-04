# C.5 Debug Module — Bidset Run-Through Verification

**Bidset:** Taco Bell — Weeki Wachee — Compass Construction Management (2)
**PDF:** `C:\huck stage 2\full bid sets\Taco Bell - Weeki Wachee - Compass Construction Management (2).pdf`
**Bidset key:** `taco-bell-weeki-wachee-compass-construction-management-2`
**Phase:** C.5 (debug module partial port)
**Dispatch time:** 70.7s
**run_debug time:** 0.0s

**Type of artifact:** smoke verification that the partial port runs end-
to-end against real input and produces real content for sections 1/3/6,
and emits documented stub markers for sections 2/4/5.

**NOT** calibration. **NOT** a sweep observation report. **NOT** an
opportunity to tune sections 1/3/6 — vault rule active.

---

## Verification status (per orders Section 5)

| Item | Pass | Detail |
|---|---|---|
| Section 1 (dispatch_health): real content (not stub_marker) | YES | dispatch_complete = True; filters_completed = ['filter_1', 'filter_2', 'filter_4', 'filter_3', 'filter_5']; total_pages = 88; sheet_count = 92; mapped_pages = 65 |
| ctx.project_scope.detected_system field present | YES | value = 'tpo'; confidence = 0.95; (orders Section 5: expected `"tpo"` with confidence ~0.95 for Taco Bell) |
| ctx.project_scope.scope_pages includes 18 and/or 19 | YES | scope_pages = [18, 19]; (orders Section 5: scope_pages should include page 18 and/or 19) |
| Section 3 (page_intelligence): list shape | YES | len = 88 |
| Section 3: has at least one page entry | YES | first page entry = {'page': 0, 'sheet': 'AD1', 'title': 'AUG. 20, 2025', 'discipline': 'A', 'type': 'roof_plan', 'confidence': 0.9, 'has_drawing': True, 'has_title_block': True, 'has_details': False, 'has_legend': False, 'detail_count': 0, 'zone_count': 2, 'legend_count': 0, 'refs_out': 0, 'refs_in': 0} |
| Section 6 (legend_contents): list shape | YES | legend count = 108 |
| Section 6: legend_quality_flags emitted (list type) | YES | flag count = 1 |
| Section 2: stub_marker = C.5_partial_port_pending_scale_engine_route | YES | scale_comparison = {'stub_marker': 'C.5_partial_port_pending_scale_engine_route', 'reason': 'Scale comparison requires the scale-engine output route; deferred to Phase D/E per DEBUG_MODULE_REPORT.md.'} |
| Section 4: stub_marker = C.5_partial_port_pending_networkx_and_sheet_index | YES | crossref_summary = {'stub_marker': 'C.5_partial_port_pending_networkx_and_sheet_index', 'reason': 'Cross-reference graph requires networkx + sheet-index parsing; deferred per DEBUG_MODULE_REPORT.md.'} |
| Section 5: stub_marker = C.5_partial_port_pending_geometry_results | YES | geometry_diagnostics = {'stub_marker': 'C.5_partial_port_pending_geometry_results', 'reason': 'Geometry diagnostics requires geometry_results from Stages 6-9; deferred per DEBUG_MODULE_REPORT.md.'} |

---

## Section 1 — Dispatch Health (verbatim port)

```json
{
  "dispatch_complete": true,
  "filters_completed": [
    "filter_1",
    "filter_2",
    "filter_4",
    "filter_3",
    "filter_5"
  ],
  "filter_count": 5,
  "warnings": [
    "Filter 4 quality gate: 128 of 236 legends removed (108 kept)"
  ],
  "warning_count": 1,
  "timestamp": "2026-04-29T01:59:14.210509+00:00",
  "total_pages": 88,
  "sheet_map_source": "drawing_index",
  "sheet_count": 92,
  "mapped_pages": 65
}
```

## Section 2 — Scale Comparison (C.5 stub)

```json
{
  "stub_marker": "C.5_partial_port_pending_scale_engine_route",
  "reason": "Scale comparison requires the scale-engine output route; deferred to Phase D/E per DEBUG_MODULE_REPORT.md."
}
```

## Section 3 — Page Intelligence (verbatim port)

Total page entries: 88

```json
[
  {
    "page": 0,
    "sheet": "AD1",
    "title": "AUG. 20, 2025",
    "discipline": "A",
    "type": "roof_plan",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 1,
    "sheet": "T1.1",
    "title": "PROJECT INFORMATION",
    "discipline": "?",
    "type": "section",
    "confidence": 0.5,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 2,
    "sheet": "T1.2",
    "title": "INTERIOR SIGNAGE SCHEDULE AND NOTES",
    "discipline": "?",
    "type": "schedule_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 2,
    "legend_count": 2,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 3,
    "sheet": "C0.1",
    "title": "COVER SHEET",
    "discipline": "C",
    "type": "cover",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 6,
    "legend_count": 3,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 4,
    "sheet": "C0.2",
    "title": "SPECIFICATIONS",
    "discipline": "C",
    "type": "schedule_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 6,
    "legend_count": 3,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 5,
    "sheet": "C1.0",
    "title": "EXISTING SITE AND DEMOLITION PLAN",
    "discipline": "C",
    "type": "general_notes",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 6,
    "sheet": "C1.1",
    "title": "SITE PLAN",
    "discipline": "C",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 1,
    "refs_out": 0,
    "refs_in": 1
  },
  {
    "page": 7,
    "sheet": "C1.2",
    "title": "GRADING AND EROSION CONTROL PLAN",
    "discipline": "C",
    "type": "elevation",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 8,
    "sheet": "C3.1",
    "title": "SITE PHOTOMETRIC PLAN & DETAILS",
    "discipline": "C",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 4,
    "refs_in": 4
  },
  {
    "page": 9,
    "sheet": "C2.0",
    "title": "DETAILS",
    "discipline": "C",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 8,
    "legend_count": 0,
    "refs_out": 1,
    "refs_in": 0
  },
  {
    "page": 10,
    "sheet": "C2.1",
    "title": "DETAILS",
    "discipline": "C",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 1,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 11,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "schedule_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 1,
    "legend_count": 2,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 12,
    "sheet": "C3.2",
    "title": "GREASE INTERCEPTOR DETAIL & SCHEDULE",
    "discipline": "C",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 5,
    "legend_count": 1,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 13,
    "sheet": "LP-1",
    "title": "PLANTING PLAN (BY OTHERS)",
    "discipline": "L",
    "type": "site_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 1,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 14,
    "sheet": "LP-2",
    "title": "PLANTING DETAILS (BY OTHERS)",
    "discipline": "L",
    "type": "detail_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 1,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 15,
    "sheet": "IR-01",
    "title": "IRRIGATION PLAN (BY OTHERS)",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 6,
    "legend_count": 3,
    "refs_out": 10,
    "refs_in": 0
  },
  {
    "page": 16,
    "sheet": "IR-02",
    "title": "IRRIGATION DETAILS (BY OTHERS)",
    "discipline": "?",
    "type": "schedule_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 1,
    "refs_out": 139,
    "refs_in": 0
  },
  {
    "page": 17,
    "sheet": "IR-03",
    "title": "IRRIGATION NOTES (BY OTHERS)",
    "discipline": "?",
    "type": "cover",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 9,
    "legend_count": 6,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 18,
    "sheet": "A0.1",
    "title": "SPECIFICATIONS",
    "discipline": "A",
    "type": "cover",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 8,
    "legend_count": 5,
    "refs_out": 0,
    "refs_in": 1
  },
  {
    "page": 19,
    "sheet": "A0.2",
    "title": "SPECIFICATIONS",
    "discipline": "A",
    "type": "detail_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 8,
    "legend_count": 5,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 20,
    "sheet": "A0.3",
    "title": "SPECIFICATIONS",
    "discipline": "A",
    "type": "detail_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 5,
    "legend_count": 2,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 21,
    "sheet": "A6.1",
    "title": "DOOR SCHEDULE",
    "discipline": "A",
    "type": "floor_plan",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 12,
    "zone_count": 5,
    "legend_count": 1,
    "refs_out": 14,
    "refs_in": 6
  },
  {
    "page": 22,
    "sheet": "A1.3",
    "title": "ROOF DETAILS",
    "discipline": "A",
    "type": "roof_plan",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 16,
    "zone_count": 4,
    "legend_count": 1,
    "refs_out": 36,
    "refs_in": 16
  },
  {
    "page": 23,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 7,
    "legend_count": 2,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 24,
    "sheet": "A1.4",
    "title": "DUMPSTER ENCLOSURE PLAN AND DETAILS",
    "discipline": "A",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 8,
    "zone_count": 7,
    "legend_count": 0,
    "refs_out": 8,
    "refs_in": 5
  },
  {
    "page": 25,
    "sheet": "A1.5",
    "title": "DUMPSTER ENCLOSURE PLAN ELEVATIONS",
    "discipline": "A",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 3
  },
  {
    "page": 26,
    "sheet": "A3.0",
    "title": "BUILDING SECTIONS",
    "discipline": "A",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 7,
    "zone_count": 6,
    "legend_count": 3,
    "refs_out": 7,
    "refs_in": 16
  },
  {
    "page": 27,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 6,
    "zone_count": 6,
    "legend_count": 3,
    "refs_out": 6,
    "refs_in": 0
  },
  {
    "page": 28,
    "sheet": "A4.1",
    "title": "WALL SECTIONS & DETAILS",
    "discipline": "A",
    "type": "section",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 4,
    "zone_count": 5,
    "legend_count": 0,
    "refs_out": 4,
    "refs_in": 0
  },
  {
    "page": 29,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "section",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 3,
    "zone_count": 5,
    "legend_count": 0,
    "refs_out": 3,
    "refs_in": 0
  },
  {
    "page": 30,
    "sheet": "A4.0",
    "title": "INTERIOR WALL TYPES",
    "discipline": "A",
    "type": "elevation",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 31,
    "sheet": "A4.2",
    "title": "WALL SECTIONS & DETAILS",
    "discipline": "A",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 2,
    "zone_count": 12,
    "legend_count": 0,
    "refs_out": 2,
    "refs_in": 0
  },
  {
    "page": 32,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 2,
    "zone_count": 11,
    "legend_count": 0,
    "refs_out": 5,
    "refs_in": 0
  },
  {
    "page": 33,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 1,
    "zone_count": 7,
    "legend_count": 0,
    "refs_out": 4,
    "refs_in": 0
  },
  {
    "page": 34,
    "sheet": "A4.4",
    "title": "DETAILS",
    "discipline": "A",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 5,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 13
  },
  {
    "page": 35,
    "sheet": "A1.1",
    "title": "FIRST FLOOR PLAN",
    "discipline": "A",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 4,
    "zone_count": 5,
    "legend_count": 0,
    "refs_out": 4,
    "refs_in": 7
  },
  {
    "page": 36,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 6,
    "zone_count": 5,
    "legend_count": 2,
    "refs_out": 6,
    "refs_in": 0
  },
  {
    "page": 37,
    "sheet": "A5.2",
    "title": "ENLARGED PLANS AND INTERIOR ELEVATIONS",
    "discipline": "A",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 2,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 38,
    "sheet": "A7.1",
    "title": "FIRST FLOOR REFLECTED CEILING PLAN",
    "discipline": "A",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 8
  },
  {
    "page": 39,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "schedule_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 5,
    "legend_count": 7,
    "refs_out": 1,
    "refs_in": 0
  },
  {
    "page": 40,
    "sheet": "A2.0",
    "title": "EXTERIOR ELEVATIONS",
    "discipline": "A",
    "type": "ceiling_plan",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 18,
    "zone_count": 7,
    "legend_count": 2,
    "refs_out": 18,
    "refs_in": 3
  },
  {
    "page": 41,
    "sheet": "A8.1",
    "title": "FIRST FLOOR FINISH PLAN",
    "discipline": "A",
    "type": "detail_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 3,
    "zone_count": 6,
    "legend_count": 3,
    "refs_out": 17,
    "refs_in": 3
  },
  {
    "page": 42,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "schedule_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 2,
    "refs_out": 8,
    "refs_in": 0
  },
  {
    "page": 43,
    "sheet": "A9.2",
    "title": "FIRST FLOOR EQUIPMENT SCHEDULE",
    "discipline": "A",
    "type": "schedule_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 3,
    "refs_out": 2,
    "refs_in": 0
  },
  {
    "page": 44,
    "sheet": "A9.3",
    "title": "EQUIPMENT DETAILS",
    "discipline": "A",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 1
  },
  {
    "page": 45,
    "sheet": "S0.1",
    "title": "SPECIFICATIONS & DESIGN CRITERIA",
    "discipline": "S",
    "type": "framing_plan",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 9,
    "legend_count": 6,
    "refs_out": 8,
    "refs_in": 0
  },
  {
    "page": 46,
    "sheet": "S2.0",
    "title": "FOUNDATION SCHEDULES",
    "discipline": "S",
    "type": "floor_plan",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 10,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 15,
    "refs_in": 10
  },
  {
    "page": 47,
    "sheet": "S3.1",
    "title": "FRAMING DETAILS",
    "discipline": "S",
    "type": "framing_plan",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 13,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 19,
    "refs_in": 11
  },
  {
    "page": 48,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 11,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 49,
    "sheet": "S3.0",
    "title": "FRAMING SCHEDULES",
    "discipline": "S",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 9,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 2
  },
  {
    "page": 50,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 1,
    "zone_count": 10,
    "legend_count": 0,
    "refs_out": 1,
    "refs_in": 0
  },
  {
    "page": 51,
    "sheet": "S5.0",
    "title": "MASONRY ELEVATIONS",
    "discipline": "S",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 52,
    "sheet": "S5.1",
    "title": "MASONRY SCHEDULES",
    "discipline": "S",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 7,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 53,
    "sheet": "S5.3",
    "title": "MASONRY CONTROL JOINT DETAILS",
    "discipline": "S",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 1,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 54,
    "sheet": "P3.0",
    "title": "DETAILS",
    "discipline": "P",
    "type": "floor_plan",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 55,
    "sheet": "P0.2",
    "title": "SPECIFICATIONS",
    "discipline": "P",
    "type": "elevation",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 1,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 56,
    "sheet": "P3.2",
    "title": "DETAILS",
    "discipline": "P",
    "type": "floor_plan",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 1,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 1,
    "refs_in": 0
  },
  {
    "page": 57,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 1,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 1,
    "refs_in": 0
  },
  {
    "page": 58,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "schedule_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 3,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 59,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 12,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 60,
    "sheet": "P1.1",
    "title": "FIRST FLOOR PLAN",
    "discipline": "P",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 9,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 61,
    "sheet": "E3.0",
    "title": "ELECTRICAL POWER PLAN",
    "discipline": "E",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 5,
    "legend_count": 1,
    "refs_out": 1,
    "refs_in": 2
  },
  {
    "page": 62,
    "sheet": "P4.0",
    "title": "SCHEDULES",
    "discipline": "P",
    "type": "schedule_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 8,
    "legend_count": 7,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 63,
    "sheet": "H0.1",
    "title": "LEGEND AND SPECIFICATIONS",
    "discipline": "?",
    "type": "roof_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 1,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 64,
    "sheet": "H0.2",
    "title": "SPECIFICATIONS AND VENTILATION CALCULATIONS",
    "discipline": "?",
    "type": "life_safety",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 1,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 65,
    "sheet": "H1.1",
    "title": "FIRST FLOOR PLAN",
    "discipline": "?",
    "type": "floor_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 1,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 66,
    "sheet": "H3.0",
    "title": "DETAILS",
    "discipline": "?",
    "type": "roof_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": true,
    "has_legend": false,
    "detail_count": 1,
    "zone_count": 1,
    "legend_count": 0,
    "refs_out": 1,
    "refs_in": 1
  },
  {
    "page": 67,
    "sheet": "H5.1",
    "title": "CAPTIVEAIRE DRAWINGS",
    "discipline": "?",
    "type": "schedule_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 9,
    "legend_count": 2,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 68,
    "sheet": "H1.2",
    "title": "ROOF PLAN",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 8,
    "legend_count": 0,
    "refs_out": 1,
    "refs_in": 1
  },
  {
    "page": 69,
    "sheet": "H4.0",
    "title": "SCHEDULES",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 9,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 70,
    "sheet": "H3.3",
    "title": "HOOD DETAILS",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 7,
    "legend_count": 2,
    "refs_out": 1,
    "refs_in": 0
  },
  {
    "page": 71,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "schedule_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 7,
    "legend_count": 8,
    "refs_out": 2,
    "refs_in": 0
  },
  {
    "page": 72,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 73,
    "sheet": "H5.2",
    "title": "CAPTIVEAIRE DRAWINGS",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 1,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 74,
    "sheet": "H5.3",
    "title": "CAPTIVEAIRE DRAWINGS",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 1,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 75,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": true,
    "has_legend": false,
    "detail_count": 1,
    "zone_count": 1,
    "legend_count": 0,
    "refs_out": 1,
    "refs_in": 0
  },
  {
    "page": 76,
    "sheet": "E2.1",
    "title": "ELECTRICAL SCHEDULES",
    "discipline": "E",
    "type": "detail_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 1,
    "refs_in": 1
  },
  {
    "page": 77,
    "sheet": "E7.0",
    "title": "ELECTRICAL DETAILS",
    "discipline": "E",
    "type": "schedule_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 2,
    "legend_count": 5,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 78,
    "sheet": "E2.2",
    "title": "ELECTRICAL SCHEDULES",
    "discipline": "E",
    "type": "schedule_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 4,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 79,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "roof_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 1,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 3,
    "refs_in": 0
  },
  {
    "page": 80,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 81,
    "sheet": "E2.0",
    "title": "ELECTRICAL ONE LINE DIAGRAMS AND LEGEND",
    "discipline": "E",
    "type": "roof_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": true,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 1,
    "legend_count": 0,
    "refs_out": 2,
    "refs_in": 0
  },
  {
    "page": 82,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": true,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 1,
    "legend_count": 0,
    "refs_out": 3,
    "refs_in": 0
  },
  {
    "page": 83,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 7,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 7,
    "refs_in": 0
  },
  {
    "page": 84,
    "sheet": "E7.1",
    "title": "ELECTRICAL DETAILS",
    "discipline": "E",
    "type": "detail_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 1,
    "refs_in": 1
  },
  {
    "page": 85,
    "sheet": "E6.1",
    "title": "ELECTRICAL DETAILS - TBCCB",
    "discipline": "E",
    "type": "detail_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": true,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 1,
    "refs_in": 2
  },
  {
    "page": 86,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 2,
    "refs_in": 0
  },
  {
    "page": 87,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": true,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 1,
    "legend_count": 0,
    "refs_out": 1,
    "refs_in": 0
  }
]
```

## Section 4 — Cross-Reference Graph (C.5 stub)

```json
{
  "stub_marker": "C.5_partial_port_pending_networkx_and_sheet_index",
  "reason": "Cross-reference graph requires networkx + sheet-index parsing; deferred per DEBUG_MODULE_REPORT.md."
}
```

## Section 5 — Geometry Diagnostics (C.5 stub)

```json
{
  "stub_marker": "C.5_partial_port_pending_geometry_results",
  "reason": "Geometry diagnostics requires geometry_results from Stages 6-9; deferred per DEBUG_MODULE_REPORT.md."
}
```

## Section 6 — Legend Contents (verbatim port)

Total legends: 108

### Legend quality flags

```json
[
  "WARNING: unusually high legend count (108) \u2014 possible pdfplumber noise"
]
```

### Legends sample

```json
[
  {
    "type": "notes",
    "title": "WOMEN'S RESTROOM CIRCLE\nL208 MEN'S RESTROOM TRIANGLE\nL206 6\"\n\"6\nEXIT BRAILLE SIG",
    "page": 2,
    "entry_count": 3,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "",
        "desc": "6\" 6\"\n\"9 \"\"99\nWOMEN'S RESTROOM WITH BRAILLE\nL209 6\" 6\"\n\"9 \"\"99\nMEN'S RESTROOM WI"
      },
      {
        "key": "",
        "desc": "6\"\n\"6\nCLEAN RESTROOM SIGN\nL202"
      },
      {
        "key": "",
        "desc": "SIGNAGE SCHEDULE\nTAG VERBIAGE SIZE MOUNTING HEIGHT QUANTITY LOCATION\nL201 NO SMO"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "SIGNAGE SCHEDULE",
    "page": 2,
    "entry_count": 11,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "TAG",
        "desc": "VERBIAGE SIZE MOUNTING HEIGHT QUANTITY LOCATION"
      },
      {
        "key": "L201",
        "desc": "NO SMOKING OR ELECTRONIC CIGARETTE USE. THIS IS A SMOKE FREE\nESTABLISHMENT 1/16 "
      },
      {
        "key": "L202",
        "desc": "CLEAN RESTROOM 1/16 x 6 x 6 60\" A.F.F. 2 1 INSIDE RESTROOM (BACK OF DOOR)"
      },
      {
        "key": "L203",
        "desc": "EMPLOYEES MUST WASH HANDS BEFORE RETURNING TO WORK 1/16 x 6 x 6 60\" A.F.F. 4 1 I"
      },
      {
        "key": "L204",
        "desc": "EXIT 1/16 x 6 x 6 60\" A.F.F. 3 1 AT EACH EXIT, MOUNTED ON WALL, ACCORDING TO ADA"
      },
      {
        "key": "L205",
        "desc": "OCCUPANCY 1/16 x 6 x 6 60\" A.F.F. 1 1 AT CUSTOMER EXIT"
      },
      {
        "key": "L206",
        "desc": "MEN'S RESTROOM TRIANGLE (W/B) 1/4 x 12 x 12 60\" A.F.F. 1 MOUNTED ON MEN'S RESTRO"
      },
      {
        "key": "L207",
        "desc": "MEN'S RESTROOM (w/ BRAILLE) 1/4 x 9 x 6 60\" A.F.F. 1 MOUNTED ON WALL NEXT TO RES"
      },
      {
        "key": "L208",
        "desc": "WOMEN'S RESTROOM CIRCLE (W/B) 1/4 x 12 x 12 60\" A.F.F. 1 MOUNTED ON WOMEN'S REST"
      },
      {
        "key": "L209",
        "desc": "WOMEN'S RESTROOM (w/ BRAILLE) 1/4 x 9 x 6 60\" A.F.F. 1 MOUNTED ON WALL NEXT TO R"
      }
    ]
  },
  {
    "type": "legend",
    "title": "IDENTIFICATION\nSYM.\nEXCEL LEGEND",
    "page": 3,
    "entry_count": 4,
    "confidence": 0.7,
    "source": "legend: IDENTIFICATION\nSYM.\nEXCEL LEGEND",
    "entries_sample": [
      {
        "key": "000",
        "desc": "00"
      },
      {
        "key": "000.00",
        "desc": "CL"
      },
      {
        "key": "000.00",
        "desc": "FG"
      },
      {
        "key": "000.00",
        "desc": "BG"
      }
    ]
  },
  {
    "type": "notes",
    "title": "NOTE:  ALL SYMBOLS SHOWN MAY NOT APPEAR ON DRAWINGS.",
    "page": 3,
    "entry_count": 4,
    "confidence": 0.7,
    "source": "legend: NOTE:  ALL SYMBOLS SHOWN MAY NOT APPEAR ",
    "entries_sample": [
      {
        "key": "000",
        "desc": "00"
      },
      {
        "key": "000.00",
        "desc": "CL"
      },
      {
        "key": "000.00",
        "desc": "FG"
      },
      {
        "key": "000.00",
        "desc": "BG"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "C3.2\nGREASE INTERCEPTOR DETAIL & SCHEDULE",
    "page": 3,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: C3.2\nGREASE INTERCEPTOR DETAIL & SCHEDUL",
    "entries_sample": [
      {
        "key": "1",
        "desc": "PRE-CONSTRUCTION"
      },
      {
        "key": "2",
        "desc": "CONSTRUCTION"
      },
      {
        "key": "3",
        "desc": "POST CONSTRUCTION"
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "THE GUIDELINES AND REQUIREMENTS SET FORTH IN SWFWMD PERFORMANCE STANDARDS.  THE ",
    "page": 4,
    "entry_count": 9,
    "confidence": 0.7,
    "source": "legend: THE GUIDELINES AND REQUIREMENTS SET FORT",
    "entries_sample": [
      {
        "key": "1",
        "desc": "SILT FENCE SHALL BE PLACED ON SITE AT LOCATIONS SHOWN ON THE EROSION CONTROL PLA"
      },
      {
        "key": "2",
        "desc": "DITCH CHECKS SHALL BE PROVIDED TO REDUCE THE VELOCITY OF WATER FLOWING IN DITCH "
      },
      {
        "key": "3",
        "desc": "STONE TRACKING PADS AND TRACKOUT CONTROL PRACTICES SHALL BE PLACED AT ALL CONSTR"
      },
      {
        "key": "4",
        "desc": "STORM DRAIN INLET PROTECTION SHALL BE PROVIDED FOR ALL NEW AND DOWNSTREAM STORM "
      },
      {
        "key": "5",
        "desc": "DUST CONTROL MEASURES SHALL BE PROVIDED TO REDUCE OR PREVENT THE SURFACE AND AIR"
      },
      {
        "key": "6",
        "desc": "THE USE, STORAGE, AND DISPOSAL OF CHEMICALS, CEMENT, AND OTHER COMPOUNDS AND MAT"
      },
      {
        "key": "7",
        "desc": "CONTRACTOR SHALL PROVIDE AN OPEN AGGREGATE CONCRETE TRUCK WASHOUT AREA ON SITE."
      },
      {
        "key": "8",
        "desc": "TEMPORARY SITE RESTORATION SHALL TAKE PLACE IN DISTURBED AREAS THAT WILL NOT BE "
      },
      {
        "key": "9",
        "desc": "IF SITE DEWATERING IS REQUIRED FOR PROPOSED CONSTRUCTION ACTIVITIES, ALL SEDIMEN"
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "REMOVED.  PROOF ROLL SUBGRADES BEFORE PLACING FILL WITH HEAVY PNEUMATIC-TIRED EQ",
    "page": 4,
    "entry_count": 6,
    "confidence": 0.7,
    "source": "legend: REMOVED.  PROOF ROLL SUBGRADES BEFORE PL",
    "entries_sample": [
      {
        "key": "1",
        "desc": "UNDER FOUNDATIONS - SUBGRADE, AND EACH LAYER OF BACKFILL OR FILL MATERIAL, TO NO"
      },
      {
        "key": "2",
        "desc": "UNDER INTERIOR SLAB-ON-GRADE WHERE GROUNDWATER IS MORE THAN 3 FEET BELOW THE SLA"
      },
      {
        "key": "3",
        "desc": "UNDER INTERIOR SLAB-ON-GRADE WHERE GROUNDWATER IS WITHIN 3 FEET OF THE SLAB SURF"
      },
      {
        "key": "4",
        "desc": "UNDER EXTERIOR CONCRETE AND ASPHALT PAVEMENTS - COMPACT THE SUBGRADE AND EACH LA"
      },
      {
        "key": "5",
        "desc": "UNDER WALKWAYS - COMPACT SUBGRADE AND EACH LAYER OF BACKFILL OR FILL MATERIAL TO"
      },
      {
        "key": "6",
        "desc": "UNDER LAWN OR UNPAVED AREAS - COMPACT SUBGRADE AND EACH LAYER OF BACKFILL OR FIL"
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "MATERIAL / INFORMATION",
    "page": 4,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: MATERIAL / INFORMATION",
    "entries_sample": [
      {
        "key": "32.10",
        "desc": "00 (A) - AGGREGATE BASE & ASPHALT PAVEMENT"
      },
      {
        "key": "32.20",
        "desc": "00-CONCRETE AND AGGREGATE BASE"
      },
      {
        "key": "33.10",
        "desc": "00 - SITE UTILITIES"
      }
    ]
  },
  {
    "type": "notes",
    "title": "EXISTING PARCEL KEY: 948005",
    "page": 6,
    "entry_count": 20,
    "confidence": 0.7,
    "source": "legend: EXISTING PARCEL KEY: 948005",
    "entries_sample": [
      {
        "key": "0",
        "desc": "00"
      },
      {
        "key": "0",
        "desc": "0%"
      },
      {
        "key": "0",
        "desc": "00"
      },
      {
        "key": "0",
        "desc": "0%"
      },
      {
        "key": "0",
        "desc": "00"
      },
      {
        "key": "0",
        "desc": "0%"
      },
      {
        "key": "2",
        "desc": "26"
      },
      {
        "key": "100",
        "desc": "0%"
      },
      {
        "key": "2",
        "desc": "26"
      },
      {
        "key": "100",
        "desc": "0%"
      }
    ]
  },
  {
    "type": "notes",
    "title": "NOTES\n1. FOUNDATION SHOWN IS A TYP.\nDESIGN. WIND LOADS OF MORE THAN\n100 MPH & UN",
    "page": 10,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: NOTES\n1. FOUNDATION SHOWN IS A TYP.\nDESI",
    "entries_sample": [
      {
        "key": "2",
        "desc": "FOUNDATIONS SHALL EXTEND BELOW"
      },
      {
        "key": "1",
        "desc": "FOUNDATION SHOWN IS A TYP."
      },
      {
        "key": "100",
        "desc": "MPH & UNSTABLE SOIL CONDITIONS"
      }
    ]
  },
  {
    "type": "notes",
    "title": "Statistics",
    "page": 11,
    "entry_count": 3,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "Description",
        "desc": "Symbol Avg Max Min Max/Min Avg/Min"
      },
      {
        "key": "Calc Zone #1",
        "desc": "0.3 fc 13.9 fc 0.0 fc N/A N/A"
      },
      {
        "key": "PARKING LOT",
        "desc": "1.2 fc 5.0 fc 0.1 fc 50.0:1 12.0:1"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "Schedule",
    "page": 11,
    "entry_count": 6,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "Symbol",
        "desc": "Label Quantity Manufacturer Catalog Number Description Number\nLamps Lumens\nPer\nL"
      },
      {
        "key": "",
        "desc": "L12H 1 LSI\nINDUSTRIES,\nINC. MRM-LED-09L-SIL-2-40-\n-70CRI-IL 1 5990 0.9 62"
      },
      {
        "key": "",
        "desc": "L14 3 LSI\nINDUSTRIES,\nINC. MRM-LED-09L-SIL-4-40-\n-70CRI-IH 1 7600 0.9 62"
      },
      {
        "key": "",
        "desc": "D2 6 TROY B2772 1 963 0.9 100"
      },
      {
        "key": "",
        "desc": "WP1 1 COOPER\nLIGHTING\nSOLUTIONS -\nLUMARK\n(FORMERLY\nEATON) LDWP-FC-3B-ED-7040 LUM"
      },
      {
        "key": "",
        "desc": "C1 2 ACCUSERV CR6 1 1516 0.9 14"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "1\nHDPE\n113\n60\n39\n1250\n4\"\n(1)\n10.5' (2)\n1250 GALLON\nKSI\n(INCHES)\nSIZE\nDEPTH\nNO.\nM",
    "page": 12,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: 1\nHDPE\n113\n60\n39\n1250\n4\"\n(1)\n10.5' (2)\n1",
    "entries_sample": [
      {
        "key": "0.75",
        "desc": "x"
      },
      {
        "key": "10",
        "desc": "5' (2)"
      },
      {
        "key": "1250",
        "desc": "GALLON"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "IRRIGATION SCHEDULE",
    "page": 15,
    "entry_count": 4,
    "confidence": 0.7,
    "source": "legend: IRRIGATION SCHEDULE",
    "entries_sample": [
      {
        "key": "0",
        "desc": "22"
      },
      {
        "key": "0",
        "desc": "44"
      },
      {
        "key": "1",
        "desc": "48"
      },
      {
        "key": "0",
        "desc": "5"
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "PIPE SLEEVE: PVC SCHEDULE 40\nTYPICAL PIPE SLEEVE FOR IRRIGATION PIPE. PIPE SLEEV",
    "page": 15,
    "entry_count": 18,
    "confidence": 0.7,
    "source": "legend: PIPE SLEEVE: PVC SCHEDULE 40\nTYPICAL PIP",
    "entries_sample": [
      {
        "key": "12",
        "desc": "61"
      },
      {
        "key": "44",
        "desc": "5"
      },
      {
        "key": "0.31",
        "desc": "in/h"
      },
      {
        "key": "14",
        "desc": "01"
      },
      {
        "key": "33",
        "desc": "5"
      },
      {
        "key": "1.16",
        "desc": "in/h"
      },
      {
        "key": "15",
        "desc": "18"
      },
      {
        "key": "46",
        "desc": "3"
      },
      {
        "key": "0.27",
        "desc": "in/h"
      },
      {
        "key": "13",
        "desc": "28"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "VALVE SCHEDULE",
    "page": 15,
    "entry_count": 18,
    "confidence": 0.7,
    "source": "legend: VALVE SCHEDULE",
    "entries_sample": [
      {
        "key": "12",
        "desc": "61"
      },
      {
        "key": "44",
        "desc": "5"
      },
      {
        "key": "0.31",
        "desc": "in/h"
      },
      {
        "key": "14",
        "desc": "01"
      },
      {
        "key": "33",
        "desc": "5"
      },
      {
        "key": "1.16",
        "desc": "in/h"
      },
      {
        "key": "15",
        "desc": "18"
      },
      {
        "key": "46",
        "desc": "3"
      },
      {
        "key": "0.27",
        "desc": "in/h"
      },
      {
        "key": "13",
        "desc": "28"
      }
    ]
  },
  {
    "type": "roof_notes",
    "title": "FINISH GRADE/TOP OF MULCH\n8\n6\n3 POP-UP SPRAY SPRINKLER\n6\nWITH NOZZLE PER SPECS 2",
    "page": 16,
    "entry_count": 6,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "",
        "desc": "NALP\nNOITAGIRRI SLLEB\nADIROLF\nTTEJ-LLEB\nOCAT"
      },
      {
        "key": "",
        "desc": "25014 M SB"
      },
      {
        "key": "",
        "desc": "10/28/2025 M SB"
      },
      {
        "key": "",
        "desc": "AS SHOWN M SB"
      },
      {
        "key": "",
        "desc": "IR-02"
      },
      {
        "key": "",
        "desc": "LANDSCAPE\nD\nE A\nE R STEFAN BO R C\nI S T A R C R T A H IT\nG MLA 6667430K E\nE C\nR "
      }
    ]
  },
  {
    "type": "notes",
    "title": "IRRIGATION NOTES",
    "page": 17,
    "entry_count": 12,
    "confidence": 0.7,
    "source": "legend: IRRIGATION NOTES",
    "entries_sample": [
      {
        "key": "1",
        "desc": "1."
      },
      {
        "key": "1",
        "desc": "2."
      },
      {
        "key": "1",
        "desc": "3."
      },
      {
        "key": "1",
        "desc": "4."
      },
      {
        "key": "1",
        "desc": "5."
      },
      {
        "key": "1",
        "desc": "6."
      },
      {
        "key": "2",
        "desc": "1."
      },
      {
        "key": "2",
        "desc": "2."
      },
      {
        "key": "2",
        "desc": "3."
      },
      {
        "key": "2",
        "desc": "4."
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "ALL CONNECTION POINTS, #6 BARE COPPER WIRE, AND EARTH CONTACT MATERIAL. INSTALL ",
    "page": 17,
    "entry_count": 15,
    "confidence": 0.7,
    "source": "legend: ALL CONNECTION POINTS, #6 BARE COPPER WI",
    "entries_sample": [
      {
        "key": "13",
        "desc": "1."
      },
      {
        "key": "13",
        "desc": "2."
      },
      {
        "key": "13",
        "desc": "3."
      },
      {
        "key": "14",
        "desc": "EQUIPMENT"
      },
      {
        "key": "14",
        "desc": "1."
      },
      {
        "key": "14",
        "desc": "2."
      },
      {
        "key": "14",
        "desc": "3."
      },
      {
        "key": "15",
        "desc": "1."
      },
      {
        "key": "15",
        "desc": "2."
      },
      {
        "key": "16",
        "desc": "INSTALLATION"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "14.1.\nINSTALL BUBBLERS USING PVC SCHEDULE 80 NIPPLES AND PLACE AT THE BASE OF TR",
    "page": 17,
    "entry_count": 13,
    "confidence": 0.7,
    "source": "legend: 14.1.\nINSTALL BUBBLERS USING PVC SCHEDUL",
    "entries_sample": [
      {
        "key": "14",
        "desc": "2."
      },
      {
        "key": "14",
        "desc": "3."
      },
      {
        "key": "15",
        "desc": "1."
      },
      {
        "key": "15",
        "desc": "2."
      },
      {
        "key": "16",
        "desc": "INSTALLATION"
      },
      {
        "key": "16",
        "desc": "1."
      },
      {
        "key": "16",
        "desc": "2."
      },
      {
        "key": "17",
        "desc": "BACKFILLING"
      },
      {
        "key": "17",
        "desc": "1."
      },
      {
        "key": "17",
        "desc": "2."
      }
    ]
  },
  {
    "type": "schedule",
    "title": "4.1.2.\nPROVIDE SYSTEM OPERATION MANUALS, MAINTENANCE SCHEDULES, RECOMMENDED SCHE",
    "page": 17,
    "entry_count": 17,
    "confidence": 0.7,
    "source": "legend: 4.1.2.\nPROVIDE SYSTEM OPERATION MANUALS,",
    "entries_sample": [
      {
        "key": "4.1",
        "desc": "3."
      },
      {
        "key": "4",
        "desc": "2."
      },
      {
        "key": "4",
        "desc": "3."
      },
      {
        "key": "5",
        "desc": "1."
      },
      {
        "key": "5.1",
        "desc": "1."
      },
      {
        "key": "5.1",
        "desc": "2."
      },
      {
        "key": "5.1",
        "desc": "3."
      },
      {
        "key": "6",
        "desc": "1."
      },
      {
        "key": "6",
        "desc": "2."
      },
      {
        "key": "6",
        "desc": "3."
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "MATERIAL BUT SHALL NOT CONTAIN ANYTHING LARGER THAN 2\" IN DIAMETER.",
    "page": 17,
    "entry_count": 12,
    "confidence": 0.7,
    "source": "legend: MATERIAL BUT SHALL NOT CONTAIN ANYTHING ",
    "entries_sample": [
      {
        "key": "17",
        "desc": "2."
      },
      {
        "key": "18",
        "desc": "1."
      },
      {
        "key": "18.1",
        "desc": "1."
      },
      {
        "key": "18.1",
        "desc": "2."
      },
      {
        "key": "18.1",
        "desc": "3."
      },
      {
        "key": "18.1",
        "desc": "4."
      },
      {
        "key": "18",
        "desc": "2."
      },
      {
        "key": "18.2",
        "desc": "1."
      },
      {
        "key": "18.2",
        "desc": "2."
      },
      {
        "key": "18",
        "desc": "3."
      }
    ]
  },
  {
    "type": "schedule",
    "title": "ROADS, WALKS, AND PATIOS, THE PIPES MUST BE SLEEVED USING PVC SCHEDULE 40 WITH T",
    "page": 17,
    "entry_count": 9,
    "confidence": 0.7,
    "source": "legend: ROADS, WALKS, AND PATIOS, THE PIPES MUST",
    "entries_sample": [
      {
        "key": "8",
        "desc": "6."
      },
      {
        "key": "8",
        "desc": "7."
      },
      {
        "key": "8",
        "desc": "8."
      },
      {
        "key": "8",
        "desc": "9."
      },
      {
        "key": "8",
        "desc": "10."
      },
      {
        "key": "9",
        "desc": "1."
      },
      {
        "key": "9",
        "desc": "2."
      },
      {
        "key": "9",
        "desc": "3."
      },
      {
        "key": "9",
        "desc": "4."
      }
    ]
  },
  {
    "type": "schedule",
    "title": "K. BUILDING COMPONENTS REQUIRING SUBMISSION \u201cFOR RECORD\u201d TO THE AUTHORITY HAVING",
    "page": 18,
    "entry_count": 28,
    "confidence": 0.7,
    "source": "legend: K. BUILDING COMPONENTS REQUIRING SUBMISS",
    "entries_sample": [
      {
        "key": "1",
        "desc": "UNIT MASONRY"
      },
      {
        "key": "2",
        "desc": "ROUGH CARPENTRY MATERIALS"
      },
      {
        "key": "3",
        "desc": "EXTERIOR FINISH CARPENTRY MATERIALS"
      },
      {
        "key": "4",
        "desc": "INTERIOR FINISH CARPENTRY MATERIALS"
      },
      {
        "key": "5",
        "desc": "WATERPROOFING"
      },
      {
        "key": "6",
        "desc": "INSULATION"
      },
      {
        "key": "7",
        "desc": "WEATHER BARRIER"
      },
      {
        "key": "8",
        "desc": "AIR AND MOISTURE BARRIERS"
      },
      {
        "key": "9",
        "desc": "MEMBRANE ROOFING SYSTEMS"
      },
      {
        "key": "10",
        "desc": "ROOFING ACCESSORIES"
      }
    ]
  },
  {
    "type": "door_schedule",
    "title": "H. PERIMETER FOUNDATION INSULATION\n1. MANUFACTURER: DOW STYROFOAM SQUARE EDGE EX",
    "page": 18,
    "entry_count": 10,
    "confidence": 0.7,
    "source": "legend: H. PERIMETER FOUNDATION INSULATION\n1. MA",
    "entries_sample": [
      {
        "key": "1",
        "desc": "MANUFACTURER: DOW STYROFOAM SQUARE EDGE EXTRUDED POLYSTYRENE (XPS) INSULATION PA"
      },
      {
        "key": "2",
        "desc": "MANUFACTURER: PLYMOUTH FOAM GOLD-GUARD FOUNDATION PERIMETER INSULATION EXPANDED"
      },
      {
        "key": "3",
        "desc": "THICKNESS AS INDICATED ON PLANS."
      },
      {
        "key": "4",
        "desc": "CLOSED CELL CONTENT: >90%"
      },
      {
        "key": "5",
        "desc": "R-VALUE PER INCH: 6.9 AT 1\u201d, 25 @ 3.5\u201d"
      },
      {
        "key": "6",
        "desc": "VAPOR PERMEANCE: 1.09-1.28 @ 1\u201d THICKNESS"
      },
      {
        "key": "7",
        "desc": "FLAME SPREAD INDEX: LESS THAN OR EQUAL TO 25"
      },
      {
        "key": "8",
        "desc": "SMOKE DEVELOPED INDEX: LESS THAN OR EQUAL TO 450"
      },
      {
        "key": "9",
        "desc": "AIR LEAKAGE: <0.005 L / S*M2 @ 75 PA"
      },
      {
        "key": "10",
        "desc": "THERMAX WALL SYSEM GOLD WARRANTY:  CONTRACTOR SHALL COORDINATE AND COMPLETE APPI"
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "A. INSTALL EXTERIOR FINISH CARPENTRY LEVEL, PLUMB, TRUE, AND ALIGNED WITH ADJACE",
    "page": 18,
    "entry_count": 7,
    "confidence": 0.7,
    "source": "legend: A. INSTALL EXTERIOR FINISH CARPENTRY LEV",
    "entries_sample": [
      {
        "key": "06",
        "desc": "20 23 INTERIOR FINISH CARPENTRY"
      },
      {
        "key": "06",
        "desc": "40 23 INTERIOR ARCHITECTURAL WOODWORK"
      },
      {
        "key": "07",
        "desc": "14 16 WATERPROOFING"
      },
      {
        "key": "1",
        "desc": "PRODUCT DATA: MANUFACTURER\u2019S TECHNICAL BULLETINS."
      },
      {
        "key": "1",
        "desc": "ACCEPTABLE PRODUCT: SIKA MASTERSEAL HLM 5000."
      },
      {
        "key": "1",
        "desc": "ON VERTICAL APPLICATIONS, SPRAY APPLY AT A RATE OF 25 SQUARE FEET PER GALLON."
      },
      {
        "key": "2",
        "desc": "VERIFY APPLIED THICKNESS WITH MIL GAUGE AS WORK PROGRESSES."
      }
    ]
  },
  {
    "type": "schedule",
    "title": "A. NOTIFY ARCHITECT ONE WEEK IN ADVANCE TO SCHEDULE FINAL COMPLIANCE WALK-THRU. ",
    "page": 18,
    "entry_count": 7,
    "confidence": 0.7,
    "source": "legend: A. NOTIFY ARCHITECT ONE WEEK IN ADVANCE ",
    "entries_sample": [
      {
        "key": "01",
        "desc": "52 00 CONSTRUCTION FACILITIES"
      },
      {
        "key": "01",
        "desc": "53 00 TEMPORARY CONSTRUCTION"
      },
      {
        "key": "01",
        "desc": "71 00 FIELD ENGINEERING"
      },
      {
        "key": "01",
        "desc": "78 00 CLOSEOUT SUBMITTALS"
      },
      {
        "key": "01",
        "desc": "78 36 WARRANTIES"
      },
      {
        "key": "03",
        "desc": "30 00 CAST-IN-PLACE CONCRETE"
      },
      {
        "key": "03",
        "desc": "60 00 GROUT"
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "A. BEFORE INSTALLATION, CONDITION WOODWORK TO AVERAGE PREVAILING HUMIDITY CONDIT",
    "page": 18,
    "entry_count": 20,
    "confidence": 0.7,
    "source": "legend: A. BEFORE INSTALLATION, CONDITION WOODWO",
    "entries_sample": [
      {
        "key": "07",
        "desc": "14 16 WATERPROOFING"
      },
      {
        "key": "1",
        "desc": "PRODUCT DATA: MANUFACTURER\u2019S TECHNICAL BULLETINS."
      },
      {
        "key": "1",
        "desc": "ACCEPTABLE PRODUCT: SIKA MASTERSEAL HLM 5000."
      },
      {
        "key": "1",
        "desc": "ON VERTICAL APPLICATIONS, SPRAY APPLY AT A RATE OF 25 SQUARE FEET PER GALLON."
      },
      {
        "key": "2",
        "desc": "VERIFY APPLIED THICKNESS WITH MIL GAUGE AS WORK PROGRESSES."
      },
      {
        "key": "07",
        "desc": "21 00 INSULATION"
      },
      {
        "key": "1",
        "desc": "MANUFACTURER: CERTAINTEED OR OWENS CORNING."
      },
      {
        "key": "2",
        "desc": "UNFACED FIBERGLASS BATT OR ROLL COMPLYING WITH ASTM C665 AND NONCOMBUSTIBLE PER "
      },
      {
        "key": "3",
        "desc": "THICKNESS OR R VALUE AS INDICATED ON PLANS. IF THICKNESS IS NOT SHOWN ON PLANS, "
      },
      {
        "key": "4",
        "desc": "STRAP TO PREVENT SLUMPING IF GYPSUM BOARD NOT BEING INSTALLED."
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "B. EXTRA MATERIAL:\n1. PROVIDE NEW, EXTRA MATERIAL OF EACH FINISH TYPE AND COLOR ",
    "page": 19,
    "entry_count": 27,
    "confidence": 0.7,
    "source": "legend: B. EXTRA MATERIAL:\n1. PROVIDE NEW, EXTRA",
    "entries_sample": [
      {
        "key": "09",
        "desc": "22 16 DRYWALL STUDS (INTERIOR NON-BEARING)"
      },
      {
        "key": "1",
        "desc": "STUDS SHALL BE SECURED TO TOP AND BOTTOM TRACK WITH (1) #8ML SCREW IN EACH FLANG"
      },
      {
        "key": "2",
        "desc": "PROVIDE SLIP TRACK AT TOP OF FULL HEIGHT PARTITIONS."
      },
      {
        "key": "3",
        "desc": "STUDS SHALL BE INSTALLED PER \"GYPSUM CONSTRUCTION HANDBOOK\" AS PUBLISHED BY UNIT"
      },
      {
        "key": "4",
        "desc": "DRYWALL STUDS SHALL BE ACCORDING TO THE LIST BELOW OR AS INDICATED ON THE PLANS "
      },
      {
        "key": "5",
        "desc": "STUD SIZE \u2014 GAUGE \u2014 LIMITING HEIGHT WITH STUD SPACING"
      },
      {
        "key": "3",
        "desc": "5/8\u201d \u2014 25 GA. \u2014 13\u2019-6\u201d AT 16\u201d O.C. \u2014 11\u2019-9\u201d AT 24\u201d O.C."
      },
      {
        "key": "3",
        "desc": "5/8\u201d \u2014 20 GA. \u2014 15\u2019-11\u201d AT 16\u201d O.C. \u2014 13\u2019-11\u201d AT 24\u201d O.C."
      },
      {
        "key": "09",
        "desc": "29 00 GYPSUM BOARD (GYP)"
      },
      {
        "key": "1",
        "desc": "PROVIDE CONTROL JOINTS PER THESE REQUIREMENTS."
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "A. PROVIDE MANUFACTURES STANDARD VINYL BASE AS SPECIFIED THAT COMPLIES WITH ASTM",
    "page": 19,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: A. PROVIDE MANUFACTURES STANDARD VINYL B",
    "entries_sample": [
      {
        "key": "09",
        "desc": "66 31 RESINOUS FLOORING \u2014 EPOXY (EPX)"
      },
      {
        "key": "1",
        "desc": "MATCH PREPARATION, MATERIALS, AND CONSTRUCTION OF FLOOR SYSTEM."
      },
      {
        "key": "09",
        "desc": "72 00  VINYL WALL COVERING (VWC)"
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "A. GENERAL: \n1. IT IS THE INTENTION OF THIS SPECIFICATION THAT ALL JOINTS ARE TO",
    "page": 19,
    "entry_count": 17,
    "confidence": 0.7,
    "source": "legend: A. GENERAL: \n1. IT IS THE INTENTION OF T",
    "entries_sample": [
      {
        "key": "08",
        "desc": "11 13 HOLLOW METAL DOORS AND FRAMES"
      },
      {
        "key": "1",
        "desc": "SET FRAMES ACCURATELY IN POSITION, PLUMBED, ALIGNED, AND BRACED SECURELY UNTIL P"
      },
      {
        "key": "2",
        "desc": "AT FIRE-PROTECTION-RATED OPENINGS, INSTALL FRAMES ACCORDING TO NFPA 80."
      },
      {
        "key": "1",
        "desc": "FIRE-RATED DOORS:  INSTALL DOORS WITH CLEARANCES ACCORDING TO NFPA 80."
      },
      {
        "key": "2",
        "desc": "SMOKE-CONTROL DOORS:  INSTALL DOORS ACCORDING TO NFPA 105."
      },
      {
        "key": "08",
        "desc": "15 10 PLASTIC LAMINATE FACED DOORS"
      },
      {
        "key": "1",
        "desc": "SET FRAMES ACCURATELY IN POSITION, PLUMBED, ALIGNED, AND BRACED SECURELY UNTIL P"
      },
      {
        "key": "2",
        "desc": "AT FIRE-PROTECTION-RATED OPENINGS, INSTALL FRAMES ACCORDING TO NFPA 80."
      },
      {
        "key": "1",
        "desc": "FIRE-RATED DOORS:  INSTALL DOORS WITH CLEARANCES ACCORDING TO NFPA 80."
      },
      {
        "key": "2",
        "desc": "SMOKE-CONTROL DOORS:  INSTALL DOORS ACCORDING TO NFPA 105."
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "A. 1/4\" EPOXY FLOORING.\nB. PREPARE CONCRETE FLOOR BY MECHANICAL MEANS BY USE OF ",
    "page": 19,
    "entry_count": 9,
    "confidence": 0.7,
    "source": "legend: A. 1/4\" EPOXY FLOORING.\nB. PREPARE CONCR",
    "entries_sample": [
      {
        "key": "09",
        "desc": "72 00  VINYL WALL COVERING (VWC)"
      },
      {
        "key": "09",
        "desc": "91 00 PAINTING"
      },
      {
        "key": "2",
        "desc": "THE CONTRACTOR SHALL BE RESPONSIBLE FOR THE PROPER PREPARATION OF ALL SURFACES P"
      },
      {
        "key": "3",
        "desc": "REVIEW CLEANING SOLVENTS AND PROTOCOLS WITH COATING MANUFACTURER TO DETERMINE TE"
      },
      {
        "key": "4",
        "desc": "MILD STEEL"
      },
      {
        "key": "5",
        "desc": "GALVANIZED METAL"
      },
      {
        "key": "6",
        "desc": "CONCRETE BLOCK (CMU)"
      },
      {
        "key": "7",
        "desc": "PRECAST CONCRETE"
      },
      {
        "key": "1",
        "desc": "UPON CONCLUSION OF THE PROJECT, THE CONTRACTOR OR PAINT MANUFACTURER/SUPPLIER SH"
      }
    ]
  },
  {
    "type": "door_schedule",
    "title": "A. REQUIREMENTS:\n1. ALL LOCKSETS SHALL BE LEVER TYPE AS REQUIRED TO MEET REQUIRE",
    "page": 19,
    "entry_count": 7,
    "confidence": 0.7,
    "source": "legend: A. REQUIREMENTS:\n1. ALL LOCKSETS SHALL B",
    "entries_sample": [
      {
        "key": "08",
        "desc": "80 00 GLAZING"
      },
      {
        "key": "1",
        "desc": "WHERE REQUIRED BY FEDERAL, STATE AND LOCAL CODES."
      },
      {
        "key": "1",
        "desc": "SAFETY GLASS SHALL BE, BUT NOT LIMITED TO"
      },
      {
        "key": "2",
        "desc": "ALL SAFETY GLAZING MATERIAL SHALL BE LABELED PER LOCAL, STATE, AND FEDERAL REQUI"
      },
      {
        "key": "09",
        "desc": "01 00 FINISHES"
      },
      {
        "key": "3",
        "desc": "ALL EXIT DOORS SHALL BE EQUIPPED WITH LEVER TYPE OR PANIC TYPE EXIT HARDWARE OPE"
      },
      {
        "key": "4",
        "desc": "CONTRACTOR TO COORDINATE KEYING SCHEDULE WITH OWNER."
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "M. PAINT VENT THRU ROOFS ON PITCHED ROOF SAME COLOR AS ROOFING MATERIAL.\nN. PAIN",
    "page": 20,
    "entry_count": 18,
    "confidence": 0.7,
    "source": "legend: M. PAINT VENT THRU ROOFS ON PITCHED ROOF",
    "entries_sample": [
      {
        "key": "1",
        "desc": "GYPSUM DRYWALL (PA):"
      },
      {
        "key": "1",
        "desc": "COAT S-W PROMAR 200 ZERO VOC INTERIOR LATEX PRIMER B28W2600 @ 1.0 MILS DFT."
      },
      {
        "key": "2",
        "desc": "COATS S-W PROMAR 200 ZERO VOC INTERIOR LATEX EG-SHEL B20-2600 @ 1.7 MILS DFT/COA"
      },
      {
        "key": "1",
        "desc": "COAT S-W PROMAR 200 ZERO VOC INTERIOR LATEX PRIMER B28W2600 @ 1.2-1.5 MILS DFT."
      },
      {
        "key": "2",
        "desc": "COATS S-W PROMAR 200 ZERO VOC INTERIOR LATEX FLAT B30-2600 @ 1.4 MILS DFT/COAT."
      },
      {
        "key": "1",
        "desc": "COAT S-W PROMAR 200 ZERO VOC INTERIOR LATEX PRIMER B28W2600 @ 1.2-1.5 MILS DFT."
      },
      {
        "key": "2",
        "desc": "COATS S-W PROMAR 200 ZERO VOC INTERIOR LATEX SEMI-GLOSS B31-2600 @ 1.5 MILS DFT/"
      },
      {
        "key": "2",
        "desc": "WOOD:"
      },
      {
        "key": "1",
        "desc": "COAT S-W PREMIUM WALL AND WOOD PRIMER B28W8111 @ 1.8-2.1 MILS DFT."
      },
      {
        "key": "2",
        "desc": "COATS S-W PRO INDUSTRIAL ACRYLIC SEMI GLOSS B66-660 @ 2.5-4.0 MILS DFT/COAT."
      }
    ]
  },
  {
    "type": "schedule",
    "title": "T. INTERIOR ITEMS:\n1. GYPSUM DRYWALL (PA):\na. \nACRYLIC EG-SHEL\ni. \n1 COAT S-W PR",
    "page": 20,
    "entry_count": 5,
    "confidence": 0.7,
    "source": "legend: T. INTERIOR ITEMS:\n1. GYPSUM DRYWALL (PA",
    "entries_sample": [
      {
        "key": "1",
        "desc": "GYPSUM DRYWALL (PA):"
      },
      {
        "key": "2",
        "desc": "COATS S-W PROMAR 200 ZERO VOC INTERIOR LATEX EG-SHEL B20-2600 @ 1.7 MILS DFT/COA"
      },
      {
        "key": "3",
        "desc": "FERROUS METAL"
      },
      {
        "key": "4",
        "desc": "ALUMINUM, ZINC-COATED AND NON FERROUS METALS: (NON MOISTURE, NON WASHDOWN AREAS)"
      },
      {
        "key": "5",
        "desc": "CONCRETE MASONRY UNITS (PA):"
      }
    ]
  },
  {
    "type": "door_schedule",
    "title": "\u2022 SEE SHEET A6.1 FOR DOOR SCHEDULE AND WINDOW SCHEDULE.",
    "page": 21,
    "entry_count": 4,
    "confidence": 0.7,
    "source": "legend: \u2022 SEE SHEET A6.1 FOR DOOR SCHEDULE AND W",
    "entries_sample": [
      {
        "key": "1",
        "desc": "REFER TO SHEET A9.1 FOR FURNITURE AND EQUIPMENT INFORMATION."
      },
      {
        "key": "2",
        "desc": "S.S. CORNER GUARD / WALL CAP TYP. ALL CORNERS IN BACK-OF-HOUSE"
      },
      {
        "key": "3",
        "desc": "FIRE EXTINGUISHER, TYP. OF (3)."
      },
      {
        "key": "4",
        "desc": "OIL COLLECTION PORT."
      }
    ]
  },
  {
    "type": "roof_notes",
    "title": "ROOF PLAN GENERAL NOTES",
    "page": 22,
    "entry_count": 4,
    "confidence": 0.7,
    "source": "legend: ROOF PLAN GENERAL NOTES",
    "entries_sample": [
      {
        "key": "1",
        "desc": "PAINT UNDERSIDE OF PARAPET CAP FLASHING w/ FACTORY BONDED"
      },
      {
        "key": "2",
        "desc": "TOP NAILING AT PARAPET CAP FLASHING WILL NOT BE ACCEPTED."
      },
      {
        "key": "3",
        "desc": "PENETRATIONS IN ROOFING MEMBRANE AND FLASHING SHALL ONLY"
      },
      {
        "key": "4",
        "desc": "ALL SHEET METAL FLASHING SHALL BE 22 GA. MINIMUM."
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "HATCH MATERIAL:",
    "page": 23,
    "entry_count": 4,
    "confidence": 0.7,
    "source": "legend: HATCH MATERIAL:",
    "entries_sample": [
      {
        "key": "1",
        "desc": "COVER - 14 GA. GALV STEEL"
      },
      {
        "key": "2",
        "desc": "FRAME COVER - 14 GA. GALV STEEL"
      },
      {
        "key": "3",
        "desc": "FRAME CURB - 14 GA. GALV STEEL"
      },
      {
        "key": "4",
        "desc": "COVER LINER - 14 GA. GALV STEEL"
      }
    ]
  },
  {
    "type": "hardware_schedule",
    "title": "NOTES: \n1. ALL MOUNTING HARDWARE TO BE SUPPLIED BY OTHERS.\n2. FOR OPERATING EFFI",
    "page": 23,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: NOTES: \n1. ALL MOUNTING HARDWARE TO BE S",
    "entries_sample": [
      {
        "key": "1",
        "desc": "ALL MOUNTING HARDWARE TO BE SUPPLIED BY OTHERS."
      },
      {
        "key": "2",
        "desc": "FOR OPERATING EFFICIENCY, HATCH HARDWARE VARIES BY SIZE."
      },
      {
        "key": "3",
        "desc": "EXAMPLE MODEL#: PH-A/G OPENING SIZE IN FEET-INCHES (PH-G2630)."
      }
    ]
  },
  {
    "type": "general_notes",
    "title": "GENERAL NOTES",
    "page": 26,
    "entry_count": 7,
    "confidence": 0.7,
    "source": "legend: GENERAL NOTES",
    "entries_sample": [
      {
        "key": "1",
        "desc": "DECORATIVE WALL SCONCE/WALL PACK/ OR EMERGENCY LIGHT FIXTURE."
      },
      {
        "key": "2",
        "desc": "BUILDING SIGNAGE PROVIDED BY SIGNAGE VENDOR."
      },
      {
        "key": "3",
        "desc": "HVAC, ELECTRICAL, OR PLUMBING SERVICE EQUIPMENT."
      },
      {
        "key": "4",
        "desc": "OIL COLLECTION PORT. SEE MANUFACTURER INSTALLATION INSTRUCTIONS."
      },
      {
        "key": "5",
        "desc": "BOH SERVICE DOOR."
      },
      {
        "key": "6",
        "desc": "PROVIDE LOCK BOX PER CITY STANDARDS."
      },
      {
        "key": "7",
        "desc": "ARTWORK. VERIFY SIZES IN FIELD."
      }
    ]
  },
  {
    "type": "schedule",
    "title": "\u2022 REFER TO THE ELECTRICAL DRAWINGS.\n\u2022 REFER TO THE SIGNAGE SCHEDULE.\n\u2022 PROVIDE B",
    "page": 26,
    "entry_count": 12,
    "confidence": 0.7,
    "source": "legend: \u2022 REFER TO THE ELECTRICAL DRAWINGS.\n\u2022 RE",
    "entries_sample": [
      {
        "key": "3",
        "desc": "HVAC, ELECTRICAL, OR PLUMBING SERVICE EQUIPMENT."
      },
      {
        "key": "4",
        "desc": "OIL COLLECTION PORT. SEE MANUFACTURER INSTALLATION INSTRUCTIONS."
      },
      {
        "key": "5",
        "desc": "BOH SERVICE DOOR."
      },
      {
        "key": "6",
        "desc": "PROVIDE LOCK BOX PER CITY STANDARDS."
      },
      {
        "key": "7",
        "desc": "ARTWORK. VERIFY SIZES IN FIELD."
      },
      {
        "key": "8",
        "desc": "CANOPY DESIGNED BY SIGNAGE VENDOR."
      },
      {
        "key": "9",
        "desc": "12\" HIGH ADDRESS NUMBERS IN BLACK. ADDRESS SHALL BE VISIBLE FROM"
      },
      {
        "key": "10",
        "desc": "ROOF LINE BEHIND PARAPET."
      },
      {
        "key": "11",
        "desc": "HOSE BIBB."
      },
      {
        "key": "12",
        "desc": "LED WALL WASHER LIGHTING."
      }
    ]
  },
  {
    "type": "schedule",
    "title": "\u2022 REFER TO THE ARTWORK SCHEDULE ON SHEET A9.1.",
    "page": 26,
    "entry_count": 7,
    "confidence": 0.7,
    "source": "legend: \u2022 REFER TO THE ARTWORK SCHEDULE ON SHEET",
    "entries_sample": [
      {
        "key": "8",
        "desc": "CANOPY DESIGNED BY SIGNAGE VENDOR."
      },
      {
        "key": "9",
        "desc": "12\" HIGH ADDRESS NUMBERS IN BLACK. ADDRESS SHALL BE VISIBLE FROM"
      },
      {
        "key": "10",
        "desc": "ROOF LINE BEHIND PARAPET."
      },
      {
        "key": "11",
        "desc": "HOSE BIBB."
      },
      {
        "key": "12",
        "desc": "LED WALL WASHER LIGHTING."
      },
      {
        "key": "13",
        "desc": "CO2 FILLER VALVE AND COVER."
      },
      {
        "key": "14",
        "desc": "PIPE BOLLARD."
      }
    ]
  },
  {
    "type": "general_notes",
    "title": "GENERAL NOTES",
    "page": 27,
    "entry_count": 7,
    "confidence": 0.7,
    "source": "legend: GENERAL NOTES",
    "entries_sample": [
      {
        "key": "1",
        "desc": "DECORATIVE WALL SCONCE/WALL PACK/ OR EMERGENCY LIGHT FIXTURE."
      },
      {
        "key": "2",
        "desc": "BUILDING SIGNAGE PROVIDED BY SIGNAGE VENDOR."
      },
      {
        "key": "3",
        "desc": "HVAC, ELECTRICAL, OR PLUMBING SERVICE EQUIPMENT."
      },
      {
        "key": "4",
        "desc": "OIL COLLECTION PORT. SEE MANUFACTURER INSTALLATION INSTRUCTIONS."
      },
      {
        "key": "5",
        "desc": "BOH SERVICE DOOR."
      },
      {
        "key": "6",
        "desc": "PROVIDE LOCK BOX PER CITY STANDARDS."
      },
      {
        "key": "7",
        "desc": "ARTWORK. VERIFY SIZES IN FIELD."
      }
    ]
  },
  {
    "type": "schedule",
    "title": "\u2022 REFER TO THE ELECTRICAL DRAWINGS.\n\u2022 REFER TO THE SIGNAGE SCHEDULE.\n\u2022 PROVIDE B",
    "page": 27,
    "entry_count": 12,
    "confidence": 0.7,
    "source": "legend: \u2022 REFER TO THE ELECTRICAL DRAWINGS.\n\u2022 RE",
    "entries_sample": [
      {
        "key": "3",
        "desc": "HVAC, ELECTRICAL, OR PLUMBING SERVICE EQUIPMENT."
      },
      {
        "key": "4",
        "desc": "OIL COLLECTION PORT. SEE MANUFACTURER INSTALLATION INSTRUCTIONS."
      },
      {
        "key": "5",
        "desc": "BOH SERVICE DOOR."
      },
      {
        "key": "6",
        "desc": "PROVIDE LOCK BOX PER CITY STANDARDS."
      },
      {
        "key": "7",
        "desc": "ARTWORK. VERIFY SIZES IN FIELD."
      },
      {
        "key": "8",
        "desc": "CANOPY DESIGNED BY SIGNAGE VENDOR."
      },
      {
        "key": "9",
        "desc": "12\" HIGH ADDRESS NUMBERS IN BLACK. ADDRESS SHALL BE VISIBLE FROM"
      },
      {
        "key": "10",
        "desc": "ROOF LINE BEHIND PARAPET."
      },
      {
        "key": "11",
        "desc": "HOSE BIBB."
      },
      {
        "key": "12",
        "desc": "LED WALL WASHER LIGHTING."
      }
    ]
  },
  {
    "type": "schedule",
    "title": "\u2022 REFER TO THE ARTWORK SCHEDULE ON SHEET A9.1.",
    "page": 27,
    "entry_count": 7,
    "confidence": 0.7,
    "source": "legend: \u2022 REFER TO THE ARTWORK SCHEDULE ON SHEET",
    "entries_sample": [
      {
        "key": "8",
        "desc": "CANOPY DESIGNED BY SIGNAGE VENDOR."
      },
      {
        "key": "9",
        "desc": "12\" HIGH ADDRESS NUMBERS IN BLACK. ADDRESS SHALL BE VISIBLE FROM"
      },
      {
        "key": "10",
        "desc": "ROOF LINE BEHIND PARAPET."
      },
      {
        "key": "11",
        "desc": "HOSE BIBB."
      },
      {
        "key": "12",
        "desc": "LED WALL WASHER LIGHTING."
      },
      {
        "key": "13",
        "desc": "CO2 FILLER VALVE AND COVER."
      },
      {
        "key": "14",
        "desc": "PIPE BOLLARD."
      }
    ]
  },
  {
    "type": "general_notes",
    "title": "GENERAL NOTES",
    "page": 36,
    "entry_count": 10,
    "confidence": 0.7,
    "source": "legend: GENERAL NOTES",
    "entries_sample": [
      {
        "key": "1",
        "desc": "STAINLESS STEEL CHASE FOR SYRUP LINES & ICE MACHINE REFRIGERANT"
      },
      {
        "key": "2",
        "desc": "ANSUL CABINET."
      },
      {
        "key": "3",
        "desc": "SS CORNER/END WALL CHANNEL GUARD, FULL HEIGHT."
      },
      {
        "key": "4",
        "desc": "HOLD-UP BUTTON."
      },
      {
        "key": "5",
        "desc": "SS CORNER GUARDS AT PERIMETER OF D/T WINDOW."
      },
      {
        "key": "6",
        "desc": "SPLASHGUARD."
      },
      {
        "key": "7",
        "desc": "ANSUL PULL STATION."
      },
      {
        "key": "8",
        "desc": "20 GA. STAINLESS STEEL PANEL BEHIND HOOD."
      },
      {
        "key": "9",
        "desc": "OPENING FINISHED WITH FRP FOR SYRUP TUBES."
      },
      {
        "key": "10",
        "desc": "CUP DISPENSERS MOUNTED ON PEPSI MACHINE. PROVIDED BY PEPSI."
      }
    ]
  },
  {
    "type": "finish_schedule",
    "title": "\u2022 REFER TO THE FINISH SCHEDULE ON SHEET A6.0 FOR FINISHES.",
    "page": 36,
    "entry_count": 11,
    "confidence": 0.7,
    "source": "legend: \u2022 REFER TO THE FINISH SCHEDULE ON SHEET ",
    "entries_sample": [
      {
        "key": "1",
        "desc": "STAINLESS STEEL CHASE FOR SYRUP LINES & ICE MACHINE REFRIGERANT"
      },
      {
        "key": "2",
        "desc": "ANSUL CABINET."
      },
      {
        "key": "3",
        "desc": "SS CORNER/END WALL CHANNEL GUARD, FULL HEIGHT."
      },
      {
        "key": "4",
        "desc": "HOLD-UP BUTTON."
      },
      {
        "key": "5",
        "desc": "SS CORNER GUARDS AT PERIMETER OF D/T WINDOW."
      },
      {
        "key": "6",
        "desc": "SPLASHGUARD."
      },
      {
        "key": "7",
        "desc": "ANSUL PULL STATION."
      },
      {
        "key": "8",
        "desc": "20 GA. STAINLESS STEEL PANEL BEHIND HOOD."
      },
      {
        "key": "9",
        "desc": "OPENING FINISHED WITH FRP FOR SYRUP TUBES."
      },
      {
        "key": "10",
        "desc": "CUP DISPENSERS MOUNTED ON PEPSI MACHINE. PROVIDED BY PEPSI."
      }
    ]
  },
  {
    "type": "finish_schedule",
    "title": "\u2022 REFER TO THE FINISH SCHEDULE ON SHEET A6.0.",
    "page": 37,
    "entry_count": 6,
    "confidence": 0.7,
    "source": "legend: \u2022 REFER TO THE FINISH SCHEDULE ON SHEET ",
    "entries_sample": [
      {
        "key": "5",
        "desc": "EXTERIOR LIGHTING CONTROL BOX."
      },
      {
        "key": "6",
        "desc": "TECH-IN-A-BOX - WALL MOUNT I.T. RACK ENCLOSURE CABINETS."
      },
      {
        "key": "7",
        "desc": "SHELF BY G.C.- FINISH WITH PLASTIC LAMINATE L-1."
      },
      {
        "key": "8",
        "desc": "ELECTRIC PANELS."
      },
      {
        "key": "9",
        "desc": "SEE ELECTRICAL DRAWINGS FOR EQUIPMENT NOT SHOWN."
      },
      {
        "key": "10",
        "desc": "FAN AND LIGHT CONTROL BOX."
      }
    ]
  },
  {
    "type": "finish_schedule",
    "title": "\u2022 REFER TO THE FINISH SCHEDULE ON SHEET A6.0.",
    "page": 37,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: \u2022 REFER TO THE FINISH SCHEDULE ON SHEET ",
    "entries_sample": [
      {
        "key": "8",
        "desc": "ELECTRIC PANELS."
      },
      {
        "key": "9",
        "desc": "SEE ELECTRICAL DRAWINGS FOR EQUIPMENT NOT SHOWN."
      },
      {
        "key": "10",
        "desc": "FAN AND LIGHT CONTROL BOX."
      }
    ]
  },
  {
    "type": "door_schedule",
    "title": "DOOR HARDWARE KEY",
    "page": 39,
    "entry_count": 7,
    "confidence": 0.7,
    "source": "legend: DOOR HARDWARE KEY",
    "entries_sample": [
      {
        "key": "351",
        "desc": "P10"
      },
      {
        "key": "351",
        "desc": "O"
      },
      {
        "key": "1",
        "desc": "1/2 PR #TA2731, 4-1/2\" x 4-1/2\""
      },
      {
        "key": "1690",
        "desc": "CONCEAL VERTICAL PANIC HARDWARE"
      },
      {
        "key": "441",
        "desc": "CU FLOOR STOP"
      },
      {
        "key": "532",
        "desc": "NP HINGE STOP"
      },
      {
        "key": "404",
        "desc": "WALL STOP"
      }
    ]
  },
  {
    "type": "door_schedule",
    "title": "1. MOUNT KICKPLATE ON BOTH SIDES OF DOOR.\n2. RESTROOM SIGN REQUIRED.\n3. COAT HOO",
    "page": 39,
    "entry_count": 20,
    "confidence": 0.7,
    "source": "legend: 1. MOUNT KICKPLATE ON BOTH SIDES OF DOOR",
    "entries_sample": [
      {
        "key": "1",
        "desc": "MOUNT KICKPLATE ON BOTH SIDES OF DOOR."
      },
      {
        "key": "2",
        "desc": "RESTROOM SIGN REQUIRED."
      },
      {
        "key": "3",
        "desc": "COAT HOOK (BACK OF DOOR) BOBRICK #B-670."
      },
      {
        "key": "4",
        "desc": "MOUNT DOOR CLOSERS ON RESTROOM OR KITCHEN SIDE ONLY."
      },
      {
        "key": "5",
        "desc": "MAXIMUM DOOR OPERATING PRESSURE: 5 LBS INTERIOR : 8 LBS EXTERIOR."
      },
      {
        "key": "6",
        "desc": "ADA COMPLIANT ACCESSIBILITY SIGNAGE, INCLUDE BRAILLE AS REQUIRED BY LOCAL JURISD"
      },
      {
        "key": "7",
        "desc": "ALL HARDWARE SHALL BE US32D U.N.O."
      },
      {
        "key": "8",
        "desc": "ALL HM FRAMES SHALL BE 16 GA STEEL U.N.O."
      },
      {
        "key": "9",
        "desc": "LAMINATE DOORS AND PAINTED FRAMES. SEE FINISH SCHEDULE."
      },
      {
        "key": "10",
        "desc": "BARRIER FREE DOOR SIGN."
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "GLAZING SCHEDULE\nGLAZING SHALL MEET THE FOLLOWING STANDARDS AND GUIDELINES AS AP",
    "page": 39,
    "entry_count": 2,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "",
        "desc": "GENERAL DOOR AND FRAME NOTES: SOLID CORE WOOD DOOR SPECIFICATIONS: EXTERIOR ALUM"
      },
      {
        "key": "",
        "desc": "2\" SEE 2\" 3 1/2\" 3 1/2\" EQ 1'-0\" EQ\n8\" 8\"\nSCHED. \"2/1\n\"2 \"8\n3 STOREFRONT SYSTEM "
      }
    ]
  },
  {
    "type": "schedule",
    "title": "GLAZING SCHEDULE",
    "page": 39,
    "entry_count": 2,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "",
        "desc": "GLAZING SCHEDULE"
      },
      {
        "key": "",
        "desc": "GLAZING SHALL MEET THE FOLLOWING STANDARDS AND GUIDELINES AS APPLICABLE FOR EACH"
      }
    ]
  },
  {
    "type": "door_schedule",
    "title": "DOOR SCHEDULE",
    "page": 39,
    "entry_count": 10,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "OOR\nNUMBER",
        "desc": "DOOR SIZE\nWIDTH HEIGHT THICKNESS DOO R TYPE FRAME TYPE UNDERCUT\nOR GRILLE\n(W x H"
      },
      {
        "key": "",
        "desc": "WIDTH HEIGHT HINGE LO CKSET STOPS CLOSER KICKPLATE SWEEP,\nTHRESHOLD"
      },
      {
        "key": "00A",
        "desc": "3'-0\" 7'-0\" 1 3/4\" AD5 AL-1 -- - - L2, L4 S4 C1 -- T1, SW2 5,10,11,12,13,14,15,1"
      },
      {
        "key": "00B",
        "desc": "3'-0\" 7'-0\" 1 3/4\" AD5 AL-1 -- - - L2, L4 S4 C1 -- T1, SW2 5,10,11,12,13,14,15,1"
      },
      {
        "key": "00C",
        "desc": "3'-0\" 7'-0\" 1 3/4\" AD5 AL-3 -- - - L2, L4 S4 C1 -- T1, SW2 5,10,11,12,13,14,15,1"
      },
      {
        "key": "02",
        "desc": "2'-0\" 7'-0\" 1 3/4\" WD1 HM1 1\" UC H 1 L1 S2 OR S3 -- K1 -- 5,7,8,9"
      },
      {
        "key": "03",
        "desc": "3'-0\" 7'-0\" 1 3/4\" WD1 HM1 1\" UC H 1 L3, L5, L6 S2 OR S3 C2 K1 -- 1,2,3,4,5,6,7,"
      },
      {
        "key": "04",
        "desc": "3'-0\" 7'-0\" 1 3/4\" WD1 HM1 1\" UC H 1 L3, L5, L6 S2 OR S3 C2 K1 -- 1,2,3,4,5,6,7,"
      },
      {
        "key": "08",
        "desc": "3'-0\" 7'-0\" 1 3/4\" WD3 HM1 1\" UC H 1 L1 S2 -- K1 -- 1,5,7,8,9"
      },
      {
        "key": "11",
        "desc": "3'-6\" 7'-0\" 1 3/4\" MD7 HM1 -- - - -- -- -- -- SW1 4,5,12,14,17,18"
      }
    ]
  },
  {
    "type": "notes",
    "title": "X MANUFACTURER MODEL",
    "page": 39,
    "entry_count": 2,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "C1",
        "desc": "SARGENT 351 P10"
      },
      {
        "key": "C2",
        "desc": "SARGENT 351 O"
      }
    ]
  },
  {
    "type": "notes",
    "title": "X MANUFACTURER MODEL",
    "page": 39,
    "entry_count": 6,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "L1",
        "desc": "YALE B-PB5407LNIC"
      },
      {
        "key": "L2",
        "desc": "FALCON C953-7 OR C987-7 AS REQ."
      },
      {
        "key": "L3",
        "desc": "FALCON D271 DEADBOLT WITH OCCUPANCY INDICATOR"
      },
      {
        "key": "L4",
        "desc": "FALCON 1690 CONCEAL VERTICAL PANIC HARDWARE"
      },
      {
        "key": "L5",
        "desc": "TRIMCO PUSH PLATE - 1001-3 - 4\" x 16\""
      },
      {
        "key": "L6",
        "desc": "TRIMCO PULL PLATE - 1017-3B - 4\" x 16\""
      }
    ]
  },
  {
    "type": "finish_schedule",
    "title": "\u2022 REFER TO THE FINISH SCHEDULE (SHEET A6.0) FOR CEILING FINISHES.",
    "page": 40,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: \u2022 REFER TO THE FINISH SCHEDULE (SHEET A6",
    "entries_sample": [
      {
        "key": "1",
        "desc": "CEILING GRID STARTING POINT."
      },
      {
        "key": "2",
        "desc": "HOOD. SUPPLIED AND INSTALLED BY H.C."
      },
      {
        "key": "3",
        "desc": "ROUGH FRAMING OPENINGS."
      }
    ]
  },
  {
    "type": "schedule",
    "title": "ELECTRICAL:\n\u2022 REFER TO THE ELECTRICAL DRAWINGS FOR LIGHTING FIXTURES AND \nSCHEDU",
    "page": 40,
    "entry_count": 9,
    "confidence": 0.7,
    "source": "legend: ELECTRICAL:\n\u2022 REFER TO THE ELECTRICAL DR",
    "entries_sample": [
      {
        "key": "1",
        "desc": "CEILING GRID STARTING POINT."
      },
      {
        "key": "2",
        "desc": "HOOD. SUPPLIED AND INSTALLED BY H.C."
      },
      {
        "key": "3",
        "desc": "ROUGH FRAMING OPENINGS."
      },
      {
        "key": "4",
        "desc": "EXTERIOR CANOPY BY SIGNAGE VENDOR."
      },
      {
        "key": "5",
        "desc": "(2) POLE MOUNTED 43\" DIGITAL SCREENS."
      },
      {
        "key": "6",
        "desc": "BULKHEAD - BOTTOM OF SOFFIT AT 7'-0\" A.F.F."
      },
      {
        "key": "7",
        "desc": "STAINLESS STEEL SYRUP CHASE ON WALL."
      },
      {
        "key": "8",
        "desc": "PENDANT LIGHT - CENTER ON TABLE BELOW. BOTTOM OF PENDANT @ 80\"."
      },
      {
        "key": "9",
        "desc": "EXTERIOR LIGHT FIXTURES."
      }
    ]
  },
  {
    "type": "finish_schedule",
    "title": "ROOM FINISH NOTES",
    "page": 41,
    "entry_count": 4,
    "confidence": 0.7,
    "source": "legend: ROOM FINISH NOTES",
    "entries_sample": [
      {
        "key": "1",
        "desc": "QUARRY FLOOR TILE: 1/4\""
      },
      {
        "key": "2",
        "desc": "PORCELAIN FLOOR TILE: 3/16\""
      },
      {
        "key": "3",
        "desc": "GLAZED WALL TILE: 1/8\""
      },
      {
        "key": "4",
        "desc": "BASE, TRIM AND ACCESSORIES: MATCH ADJOINING TILE"
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "\u2022 FLOORING CONTRACTOR SHALL PREPARE FLOOR SURFACES RECEIVING \nNEW FINISHES AS RE",
    "page": 41,
    "entry_count": 7,
    "confidence": 0.7,
    "source": "legend: \u2022 FLOORING CONTRACTOR SHALL PREPARE FLOO",
    "entries_sample": [
      {
        "key": "1",
        "desc": "QUARRY FLOOR TILE: 1/4\""
      },
      {
        "key": "2",
        "desc": "PORCELAIN FLOOR TILE: 3/16\""
      },
      {
        "key": "3",
        "desc": "GLAZED WALL TILE: 1/8\""
      },
      {
        "key": "4",
        "desc": "BASE, TRIM AND ACCESSORIES: MATCH ADJOINING TILE"
      },
      {
        "key": "1",
        "desc": "NEW FLOOR TILE AND BASE."
      },
      {
        "key": "2",
        "desc": "NEW EPOXY FLOORING AND BASE."
      },
      {
        "key": "3",
        "desc": "PROVIDE KITCHEN FLOOR FINISH INSIDE WALK-IN COOLER.  FLOAT FLOOR IN"
      }
    ]
  },
  {
    "type": "finish_schedule",
    "title": "\u2022 \n\u2022 REFER TO THE FLOORING LEGEND THIS SHEET.\n\u2022 REFER TO THE FINISH SCHEDULE ON ",
    "page": 41,
    "entry_count": 8,
    "confidence": 0.7,
    "source": "legend: \u2022 \n\u2022 REFER TO THE FLOORING LEGEND THIS S",
    "entries_sample": [
      {
        "key": "2",
        "desc": "NEW EPOXY FLOORING AND BASE."
      },
      {
        "key": "3",
        "desc": "PROVIDE KITCHEN FLOOR FINISH INSIDE WALK-IN COOLER.  FLOAT FLOOR IN"
      },
      {
        "key": "4",
        "desc": "ALIGN FLOORING TRANSITION WITH FACE OF WALL. PROVIDE FLUSH"
      },
      {
        "key": "5",
        "desc": "FACTORY FLOOR FINISH (GALVANIZED STEEL) W/ INTEGRAL COVE BASE. NO"
      },
      {
        "key": "6",
        "desc": "FLOOR TILE START POINT."
      },
      {
        "key": "7",
        "desc": "FLOOR DRAIN/FLOOR CLEAN OUT/TRENCH DRAIN/FLOOR SINK, TYP."
      },
      {
        "key": "8",
        "desc": "MOP SINK WITH STAINLESS STEEL PANELS, PROVIDED AND INSTALLED BY"
      },
      {
        "key": "9",
        "desc": "NO BASE BEHIND WALK-IN COOLER/FREEZER."
      }
    ]
  },
  {
    "type": "schedule",
    "title": "\u2022 REFER TO THE ARTWORK SCHEDULE THIS SHEET.",
    "page": 42,
    "entry_count": 4,
    "confidence": 0.7,
    "source": "legend: \u2022 REFER TO THE ARTWORK SCHEDULE THIS SHE",
    "entries_sample": [
      {
        "key": "3",
        "desc": "ACCESSIBLE TABLE AS INDICATED BY CLEARANCE MARKER LABEL ON TABLE"
      },
      {
        "key": "4",
        "desc": "KITCHEN EQUIPMENT."
      },
      {
        "key": "5",
        "desc": "FURNITURE BY VENDOR."
      },
      {
        "key": "50",
        "desc": "5"
      }
    ]
  },
  {
    "type": "notes",
    "title": "HELVING",
    "page": 42,
    "entry_count": 3,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "x 33.5''",
        "desc": ""
      },
      {
        "key": "P",
        "desc": ""
      },
      {
        "key": "4 TOP",
        "desc": ""
      }
    ]
  },
  {
    "type": "notes",
    "title": "NO.\nQTY\nITEM DESCRIPTION\nMFR & MODEL NUMBER\nINSTALLED BY\nNOTES",
    "page": 43,
    "entry_count": 4,
    "confidence": 0.7,
    "source": "legend: NO.\nQTY\nITEM DESCRIPTION\nMFR & MODEL NUM",
    "entries_sample": [
      {
        "key": "10",
        "desc": "81\"x14.0625\" Surface Mounted Manual Stainless Steel Finish"
      },
      {
        "key": "32",
        "desc": "Gallon Round Brute Gray"
      },
      {
        "key": "15.8",
        "desc": "Gallon Gray"
      },
      {
        "key": "12",
        "desc": "1/2L x 5 1/4W x 10 3/4H White"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "EQUIPMENT SCHEDULE",
    "page": 43,
    "entry_count": 63,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "NO.",
        "desc": "QTY ITEM DESCRIPTION MFR & MODEL NUMBER INSTALLED BY NOTES"
      },
      {
        "key": "B BUILDING MISCELLAN",
        "desc": ""
      },
      {
        "key": "B-049",
        "desc": "1 ROOF LADDER PRECISION LADDER #FL-184 G.C. Roof Ladder 16'0\" Overall Dimension "
      },
      {
        "key": "B-050",
        "desc": "1 ROOF HATCH PRECISION LADDER #PLHG G.C. Roof Hatch 2'6\" x 3' Clear Opening Galv"
      },
      {
        "key": "B-140",
        "desc": "1 SELF CLOSING DRIVE-THRU WINDOW QUICKSERV #SC-4030-IP G.C. G.C. TO PROVIDE EXTR"
      },
      {
        "key": "B-220",
        "desc": "1 USED COOKING OIL RECYCLING SYSTEM CLEARVIEW 1500 G.C. ROUGH PLUMBING BY PLUMBE"
      },
      {
        "key": "B-223",
        "desc": "3 WATER HEATER - G.C. SEE PLUMBING DRAWINGS"
      },
      {
        "key": "B-241",
        "desc": "4 SOAP DISPENSER (WALL MOUNT) KAY #3741 G.C. --"
      },
      {
        "key": "B-251",
        "desc": "2 SANITIZER DISPENSER (WALL MOUNT) KAY #3741 G.C. --"
      },
      {
        "key": "B-265",
        "desc": "1 MIRROR, 18 x 36 BOBRICK #B-165-1836 G.C. SURFACE MOUNTED, STAINLESS STEEL FINI"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "EQUIPMENT SCHEDULE",
    "page": 43,
    "entry_count": 70,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "NO.",
        "desc": "QTY ITEM DESCRIPTION MFR & MODEL NUMBER INSTALLED BY NOTES"
      },
      {
        "key": "N SINKS",
        "desc": ""
      },
      {
        "key": "N-043",
        "desc": "1 3-COMP SINK POWERSOAK #PS6750 G.C. Power Soak Sink, 31\"x102\"x44-1/2\", Gen 4, 2"
      },
      {
        "key": "N-062",
        "desc": "2 STAINLESS STEEL WALL MOUNTED SINK WITH FAUCET AERO #HSKSKV G.C. Hand Sink, 15-"
      },
      {
        "key": "N-071",
        "desc": "1 MOP SINK FAUCET T&S #B-2465 P.C. SEE PLUMBING DRAWINGS"
      },
      {
        "key": "N-130",
        "desc": "1 1 COMP SINK FAUCET T&S #B-2463 G.C."
      },
      {
        "key": "N-141",
        "desc": "2 WALL MOUNTED LAVATORY - P.C. SEE PLUMBING DRAWINGS"
      },
      {
        "key": "N-171",
        "desc": "1 LEVER WASTE DRAIN S-20 G.C. --"
      },
      {
        "key": "N-202",
        "desc": "1 MOP SINK AERO #3MP-2121-6/1P P.C. Mop Sink 24\"x24\"x10\" Floor Mount 16 Ga 304 S"
      },
      {
        "key": "N-698",
        "desc": "1 1 COMP SINK AERO #2F1, 2116-17LR G.C. 1-Compartment Sink, 27\"x53-1/4\"x42-1/2\","
      }
    ]
  },
  {
    "type": "schedule",
    "title": "H. CONTROL JOINTS SHALL BE SPACED PER NCMA 10-2B: CONTROL JOINTS FOR CONCRETE MA",
    "page": 45,
    "entry_count": 12,
    "confidence": 0.7,
    "source": "legend: H. CONTROL JOINTS SHALL BE SPACED PER NC",
    "entries_sample": [
      {
        "key": "05",
        "desc": "21 00 STEEL JOIST FRAMING"
      },
      {
        "key": "1",
        "desc": "STANDARD: SHOP PREPARE STEEL TO SSPC-SP-2 OR 3 (HAND OR POWER TOOL CLEANING).  O"
      },
      {
        "key": "2",
        "desc": "GALVANIZED: MINIMUM G60 HOT-DIP GALVANIZED COATING MEETING THE REQUIREMENTS OF A"
      },
      {
        "key": "05",
        "desc": "31 00 STEEL DECKING"
      },
      {
        "key": "1",
        "desc": "1.5B, 1.5BI, 1.5PLB, 1.5BA, 1.5BIA, 1.5PLBA:  MIN. 50 KSI YIELD."
      },
      {
        "key": "2",
        "desc": "3NL-32, 3NI-32, 3PLN-32, 3NLA-32, 3NIA-32, 3PLNA-32:  MIN. 50 KSI YIELD."
      },
      {
        "key": "3",
        "desc": "3N-24, 3NI-24, 3NA-24, 3NIA-24:  MIN. 40 KSI YIELD."
      },
      {
        "key": "4",
        "desc": "0.6C, 1.0C, 1.3C, 1.5C:  MIN. 80 KSI YIELD."
      },
      {
        "key": "5",
        "desc": "2C, 3C:  MIN. 50 KSI YIELD."
      },
      {
        "key": "6",
        "desc": "1.5VL, 1.5VLI, 1.5VLR, 1.5PLVLI, 2VL, 2VLI, 2PLVLI, 3VL, 3VLI, 3PLVLI:  MIN. 50 "
      }
    ]
  },
  {
    "type": "roof_notes",
    "title": "A. SEE DIVISION 00 PROCUREMENT AND CONTRACTING AND DIVISION 01 GENERAL REQUIREME",
    "page": 45,
    "entry_count": 9,
    "confidence": 0.7,
    "source": "legend: A. SEE DIVISION 00 PROCUREMENT AND CONTR",
    "entries_sample": [
      {
        "key": "1",
        "desc": "SEE DIVISION 01 25 13 PRODUCT SUBSTITUTION PROCEDURES FOR ADDITIONAL REQUIREMENT"
      },
      {
        "key": "2",
        "desc": "CONTRACTOR SHALL PROVIDE ALL SUPPORTING DATA AND ASSUME THE BURDEN OF PROOF THAT"
      },
      {
        "key": "7",
        "desc": "CONSTRUCTION ADMINISTRATION SUBMITTAL LIST:"
      },
      {
        "key": "3",
        "desc": "THE FOLLOWING ITEMS ARE DESIGNATED AS DELEGATED DESIGN SUBMITTALS. DELEGATED DES"
      },
      {
        "key": "4",
        "desc": "WHERE DETAILS ARE CALLED FOR IN ONE AREA OF THE BUILDING THEY SHALL BE DUPLICATE"
      },
      {
        "key": "5",
        "desc": "IN THE EVENT OF ANY CONFLICT BETWEEN PLANS, DETAILS, STRUCTURAL NOTES, STRUCTURA"
      },
      {
        "key": "6",
        "desc": "THESE STRUCTURAL PLANS DEPICT A STRUCTURAL FRAMING SYSTEM AND THE MAJOR COMPONEN"
      },
      {
        "key": "8",
        "desc": "BOTTOM OF FOOTING ELEVATION SHALL BE A MINIMUM OF 1\u2019-6\u201d BELOW ADJACENT EXTERIOR "
      },
      {
        "key": "9",
        "desc": "FOUNDATION SHORING AND/OR UNDERPINNING SHALL BE DESIGNED BY THE CONTRACTOR TO LI"
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "1. TOP OF FLOOR ELEVATION SHALL BE WITHIN 3/4\" OF DESIGN ELEVATION IN ACCORDANCE",
    "page": 45,
    "entry_count": 8,
    "confidence": 0.7,
    "source": "legend: 1. TOP OF FLOOR ELEVATION SHALL BE WITHI",
    "entries_sample": [
      {
        "key": "1",
        "desc": "TOP OF FLOOR ELEVATION SHALL BE WITHIN 3/4\" OF DESIGN ELEVATION IN ACCORDANCE TO"
      },
      {
        "key": "2",
        "desc": "CONTRACTOR SHALL REPLACE AREAS THAT DO NOT MEET THESE CRITERIA."
      },
      {
        "key": "3",
        "desc": "NON-SLIP LIGHT BROOM FINISH: SEE ARCHITECTURAL ROOM FINISH SCHEDULE FOR LOCATION"
      },
      {
        "key": "4",
        "desc": "POLISHED CONCRETE:  HARD-STEEL TROWELED (3 PASSES) CONCRETE, NO BURNISHING MARKS"
      },
      {
        "key": "302",
        "desc": "1R, CLASS 5 FLOOR).  SEE ARCHITECTURAL ROOM FINISH SCHEDULE FOR LOCATIONS."
      },
      {
        "key": "1.5",
        "desc": "LBS/CU. YD. AND 6 X 6-W1.4 X W1.4 WELDED WIRE MESH UNLESS NOTED OTHERWISE."
      },
      {
        "key": "24",
        "desc": "HOURS AFTER TESTS.  REPORTS OF COMPRESSIVE STRENGTH TESTS SHALL CONTAIN THE PROJ"
      },
      {
        "key": "28",
        "desc": "DAYS, CONCRETE MIX PROPORTIONS AND MATERIALS, COMPRESSIVE BREAKING STRENGTH, AND"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "A. INSTALLATION/CONSTRUCTION OF ALL STEEL DECK SYSTEMS WORK SHALL CONFORM TO THE",
    "page": 45,
    "entry_count": 7,
    "confidence": 0.7,
    "source": "legend: A. INSTALLATION/CONSTRUCTION OF ALL STEE",
    "entries_sample": [
      {
        "key": "05",
        "desc": "50 00 MISCELLANEOUS STEEL FABRICATIONS (INCLUDING STAIRS AND RAILINGS)"
      },
      {
        "key": "1",
        "desc": "STEEL GRADES SHALL BE AS LISTED BELOW UNLESS INDICATED OTHERWISE:"
      },
      {
        "key": "2",
        "desc": "SHOP APPLIED COATINGS (SEE SHOP APPLIED COATING AND AESS REQUIREMENT SCHEDULE ON"
      },
      {
        "key": "3",
        "desc": "3N-24, 3NI-24, 3NA-24, 3NIA-24:  MIN. 40 KSI YIELD."
      },
      {
        "key": "4",
        "desc": "0.6C, 1.0C, 1.3C, 1.5C:  MIN. 80 KSI YIELD."
      },
      {
        "key": "5",
        "desc": "2C, 3C:  MIN. 50 KSI YIELD."
      },
      {
        "key": "6",
        "desc": "1.5VL, 1.5VLI, 1.5VLR, 1.5PLVLI, 2VL, 2VLI, 2PLVLI, 3VL, 3VLI, 3PLVLI:  MIN. 50 "
      }
    ]
  },
  {
    "type": "legend",
    "title": "NET WIND UPLIFT LEGEND",
    "page": 45,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: NET WIND UPLIFT LEGEND",
    "entries_sample": [
      {
        "key": "26.0",
        "desc": "PSF"
      },
      {
        "key": "31.8",
        "desc": "PSF"
      },
      {
        "key": "31.8",
        "desc": "PSF"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "A. SCOPE \u2014 THIS SECTION IS APPLICABLE TO ALL DIVISION 05 STEEL EXPOSED TO VIEW (",
    "page": 45,
    "entry_count": 4,
    "confidence": 0.7,
    "source": "legend: A. SCOPE \u2014 THIS SECTION IS APPLICABLE TO",
    "entries_sample": [
      {
        "key": "1",
        "desc": "AESS 1: STEEL DESIGNATED AS AESS 1 ARE BASIC ELEMENTS WITH WORKMANSHIP REQUIREME"
      },
      {
        "key": "2",
        "desc": "AESS 2: STEEL DESIGNATED AS AESS 2 ARE FEATURE ELEMENTS VIEWED AT A DISTANCE GRE"
      },
      {
        "key": "3",
        "desc": "AESS 3: STEEL DESIGNATED AS AESS 3 ARE FEATURE ELEMENTS VIEWED AT A DISTANCE LES"
      },
      {
        "key": "4",
        "desc": "AESS 4: STEEL DESIGNATED AS AESS 4 ARE SHOWCASE ELEMENTS WITH SPECIAL SURFACE AN"
      }
    ]
  },
  {
    "type": "notes",
    "title": "NOTES:\n1. SEE MASONRY PLANS/ELEVATIONS",
    "page": 53,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: NOTES:\n1. SEE MASONRY PLANS/ELEVATIONS",
    "entries_sample": [
      {
        "key": "2",
        "desc": "LINTEL AND JAMB REINFORCING NOT"
      },
      {
        "key": "3",
        "desc": "SEE ARCHITECTURAL PLANS FOR"
      },
      {
        "key": "1",
        "desc": "SEE MASONRY PLANS/ELEVATIONS"
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "A. \nPIPING\n1. \nSEE PIPE SCHEDULE ON PLANS FOR ADDITIONAL INFORMATION.\nB. \nPIPING",
    "page": 55,
    "entry_count": 6,
    "confidence": 0.7,
    "source": "legend: A. \nPIPING\n1. \nSEE PIPE SCHEDULE ON PLAN",
    "entries_sample": [
      {
        "key": "10",
        "desc": "PREPARE EXPOSED UNFINISHED PIPE, FITTINGS, SUPPORTS, AND ACCESSORIES, READY FOR "
      },
      {
        "key": "11",
        "desc": "SLOPE PIPING AND ARRANGE SYSTEMS TO DRAIN AT LOW POINTS.  USE TOP CONNECTIONS FO"
      },
      {
        "key": "12",
        "desc": "USE LONG RADIUS ELBOWS FOR ALL 90 DEGREE ELBOWS."
      },
      {
        "key": "13",
        "desc": "INSTALL VALVE STEM BETWEEN THE VERTICAL (UPRIGHT) OR HORIZONTAL POSITION."
      },
      {
        "key": "14",
        "desc": "DO NOT SUPPORT WEIGHT OF PIPING ON VALVE."
      },
      {
        "key": "61",
        "desc": "LISTED."
      }
    ]
  },
  {
    "type": "notes",
    "title": "SEE WATER",
    "page": 58,
    "entry_count": 2,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "FILTER DETAILS",
        "desc": ""
      },
      {
        "key": "ON SHEET P3.2",
        "desc": ""
      }
    ]
  },
  {
    "type": "notes",
    "title": "METER\nWSFU\nCOPPER CPVC PEX\nPIPE FLUSH FLUSH FLUSH FLUSH FLUSH FLUSH\nCE MAKER SIZ",
    "page": 58,
    "entry_count": 12,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "",
        "desc": "WSFU"
      },
      {
        "key": "",
        "desc": "COPPER\nPE FLUSH FLUSH F\nZE TANK VALVE T CPVC PEX COPPER CPVC PEX"
      },
      {
        "key": "",
        "desc": "LUSH\nANK FLUSH\nVALVE FLUSH\nTANK FLUSH\nVALVE FLUSH\nTANK FLUSH\nVALVE FLUSH\nTANK FL"
      },
      {
        "key": "DRIVE THRU 106 1",
        "desc": "/2 5.0 NP 3.0 NP 3.0 NP KITCHEN 107 1/2 5 NP 3 NP 3 NP"
      },
      {
        "key": "25 PSIG 3\n2 FEET 1",
        "desc": "/4 16.5 4.0 12.5 4.0 6.0 NP 8 PSIG\n3 FEET 3/4 16.5 4 12.5 4 6 NP"
      },
      {
        "key": "",
        "desc": "31.0 6.5 24.0 5.5 20.5 4.5 1 31 6.5 24 5.5 20.5 4.5"
      },
      {
        "key": "10 PSIG 1 1\n0 PSIG 1",
        "desc": "/4 58.0 15.0 41.0 8.0 34.0 7.0 10 PSIG\n0 PSIG 1 1/4 58 15 41 8 34 7"
      },
      {
        "key": "",
        "desc": "/2 107.0 37.0 68.0 19.0 55.0 13.5 1 1/2 107 37 68 19 55 13.5"
      },
      {
        "key": "31.6 PSIG 2\n105 FEET",
        "desc": "260.0 136.0 171.0 73.0 135.0 53.0 48.2 PSIG\n115 FEET 2 260 136 171 73 135 53"
      },
      {
        "key": "",
        "desc": "/2 469.0 356.0 385.0 255.0 2 1/2 469 356 385 255"
      }
    ]
  },
  {
    "type": "notes",
    "title": "WASTE COLD WATER HOT WATER TOTAL WATER",
    "page": 58,
    "entry_count": 16,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "ITS TOTAL TRAP\nSIZE",
        "desc": "UNITS TOTAL BRAN\nSIZE CH UNITS TOTAL BRANCH\nSIZE UNITS TOTAL"
      },
      {
        "key": "- - -",
        "desc": "2 2 1/2\" - - - 2 2"
      },
      {
        "key": "- - -",
        "desc": "2 2 1/2\" - - - 2 2"
      },
      {
        "key": "- - -",
        "desc": "0.5 1.5 1/2\" - - - 0.5 1.5"
      },
      {
        "key": "- - -",
        "desc": "1 1 1/2\" 1 1 1/2\" 1.5 1.5"
      },
      {
        "key": "- - -",
        "desc": "4 8 3/4\" - - - 4 8"
      },
      {
        "key": "- - -",
        "desc": "0.5 2 1/2\" - - - 0.5 2"
      },
      {
        "key": "- - -",
        "desc": "0.5 1 1/2\" - - - 0.5 1"
      },
      {
        "key": "5 60 3\"",
        "desc": "- - - - - - - -"
      },
      {
        "key": "6 6 4\"",
        "desc": "- - - - - - - -"
      }
    ]
  },
  {
    "type": "notes",
    "title": "KEY NOTES:",
    "page": 61,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: KEY NOTES:",
    "entries_sample": [
      {
        "key": "1",
        "desc": "DRIVE THRU DRINK STATION"
      },
      {
        "key": "2",
        "desc": "SELF SERVE DRINK STATION"
      },
      {
        "key": "1",
        "desc": "ICE MACHINES"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "COPPER\nPEX\nPVC\nCPVC\nCAST IRON\nSTEEL\nPIPE SCHEDULE",
    "page": 62,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: COPPER\nPEX\nPVC\nCPVC\nCAST IRON\nSTEEL\nPIPE",
    "entries_sample": [
      {
        "key": "2",
        "desc": "1/2\" - 8\""
      },
      {
        "key": "10",
        "desc": "YEAR WARRANTY IN MATERIAL AND WORKMANSHIP. INSTALL PER MFR INSTALLATION INSTRUCT"
      },
      {
        "key": "0",
        "desc": "5"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "INFR WTR CONTROL (L-1)\nSEE SCHED\n-\nFRAC.\n-\n-\n-\n120\n1\n-\nINTEGRAL\nEM\n-\nNR\n-\n(1)\nPB",
    "page": 62,
    "entry_count": 17,
    "confidence": 0.7,
    "source": "legend: INFR WTR CONTROL (L-1)\nSEE SCHED\n-\nFRAC.",
    "entries_sample": [
      {
        "key": "96",
        "desc": "0"
      },
      {
        "key": "5",
        "desc": "6"
      },
      {
        "key": "67",
        "desc": "0"
      },
      {
        "key": "6",
        "desc": "PSIG"
      },
      {
        "key": "150",
        "desc": "PSIG"
      },
      {
        "key": "96",
        "desc": "0"
      },
      {
        "key": "5",
        "desc": "6"
      },
      {
        "key": "67",
        "desc": "0"
      },
      {
        "key": "6",
        "desc": "PSIG"
      },
      {
        "key": "150",
        "desc": "PSIG"
      }
    ]
  },
  "... (28 more items truncated for artifact readability)"
]
```

---

## Project-scope cross-check (dispatch output, not debug section)

Reference for orders Section 5's `detected_system` and `scope_pages`
expectations on Taco Bell. These fields live on `ctx.project_scope` —
the debug module's section 1 reads dispatch-completion stats only and
does NOT surface project_scope. Recorded here as a separate fact about
the dispatch output for verification completeness.

```json
{
  "scope_pages": [
    18,
    19
  ],
  "spec_sections": [
    "07 14 16",
    "07 21 00",
    "07 26 00",
    "07 27 26",
    "07 53 23",
    "07 54 23",
    "07 54 19",
    "07 84 13",
    "07 92 00"
  ],
  "detected_system": "tpo",
  "system_confidence": 0.95,
  "system_evidence": "from 2 scope page(s) [18, 19]: spec 07 54 23 \u2192 TPO Membrane Roofing; Johns Manville (multi-system); Tremco (multi-system)",
  "manufacturers": [
    "CertainTeed",
    "Sika Sarnafil",
    "Johns Manville",
    "Tremco"
  ],
  "material_mentions": [
    "DENSGLASS",
    "DENSDECK",
    "DENSITY",
    "COVERBOARD",
    "XPS",
    "EPS",
    "POLYISOCYANURATE",
    "25 MIL",
    "15 MIL",
    "25 GA",
    "22 GA",
    "20 GA"
  ],
  "florida_signals": [
    "UL 790"
  ],
  "roof_shape_signal": "flat_roof",
  "architect": "APPROVED FORM, NUMBER SEQUENCE AND INCLUDE THE FOLLOWING INFORMATION",
  "contractor": "SHALL SUBMIT TO THE OWNER CERTIFICATE OF INSURANCE"
}
```

---

**End of artifact.** This is a verification record, not a regression
suite entry. Future tuning of sections 1/3/6 is gated by the vault rule
(CLAUDE.md Section 3 Decision 15) and happens in dedicated sessions with
`core/` frozen.
