# Calibration Run — Silverleaf — Iteration 0

**Date:** 2026-04-29
**Iteration:** 0 of max 4
**Fix applied this iteration:** BASELINE — no fix
**Wall-clock:** dispatch 30.7s / modules 83.8s / debug 0.0s / total 114.6s

## §1 — Dispatch output summary

- detected_system: `None` / confidence: `0.0` / scope_pages: `[]`
- dispatch_complete: `True` / filters_completed: `['filter_1', 'filter_2', 'filter_4', 'filter_3', 'filter_5']`
- dispatch_warnings: `['Filter 4 quality gate: 26 of 75 legends removed (49 kept)']`
- total_pages: `40` / sheet_count: `10` / mapped_pages: `4`

### Page-type histogram

- `elevation`: 8
- `detail_sheet`: 8
- `schedule_sheet`: 8
- `unknown`: 4
- `section`: 3
- `framing_plan`: 2
- `general_notes`: 2
- `roof_plan`: 2
- `cover`: 1
- `floor_plan`: 1
- `ceiling_plan`: 1

### Per-page type listing

| Page | Sheet | Title | Type | Conf | has_legend | has_schedule | legend_count |
|---:|---|---|---|---:|---|---|---:|
| 0 | --- | --- | elevation | 0.7 | True | False | 1 |
| 1 | --- | --- | framing_plan | 0.7 | True | True | 4 |
| 2 | --- | --- | detail_sheet | 0.7 | True | True | 1 |
| 3 | --- | --- | schedule_sheet | 0.7 | True | True | 4 |
| 4 | S502 | 6 | elevation | 0.7 | True | False | 2 |
| 5 | S101 | ROOF FRAMING PLAN | framing_plan | 0.9 | True | False | 2 |
| 6 | --- | --- | detail_sheet | 0.9 | True | True | 2 |
| 7 | --- | --- | elevation | 0.9 | True | True | 4 |
| 8 | --- | --- | detail_sheet | 0.9 | True | True | 4 |
| 9 | SW-3S | --- | schedule_sheet | 0.9 | True | True | 7 |
| 10 | --- | --- | general_notes | 0.9 | False | False | 0 |
| 11 | --- | --- | detail_sheet | 0.7 | False | False | 0 |
| 12 | --- | --- | unknown | 0.0 | False | False | 0 |
| 13 | --- | --- | unknown | 0.0 | False | False | 0 |
| 14 | --- | --- | cover | 0.9 | False | False | 0 |
| 15 | --- | --- | elevation | 0.7 | False | False | 0 |
| 16 | --- | --- | detail_sheet | 0.9 | False | False | 0 |
| 17 | --- | --- | detail_sheet | 0.9 | False | False | 0 |
| 18 | --- | --- | schedule_sheet | 0.9 | True | True | 2 |
| 19 | --- | --- | section | 0.7 | True | False | 1 |
| 20 | --- | --- | schedule_sheet | 0.9 | True | False | 1 |
| 21 | --- | --- | roof_plan | 0.7 | False | False | 0 |
| 22 | --- | --- | floor_plan | 0.9 | False | False | 0 |
| 23 | --- | --- | detail_sheet | 0.9 | True | True | 1 |
| 24 | --- | --- | ceiling_plan | 0.9 | False | False | 0 |
| 25 | WD1 | --- | schedule_sheet | 0.9 | True | False | 3 |
| 26 | --- | --- | schedule_sheet | 0.9 | True | False | 1 |
| 27 | --- | --- | roof_plan | 0.9 | True | False | 3 |
| 28 | --- | --- | elevation | 0.9 | False | False | 0 |
| 29 | --- | --- | elevation | 0.9 | False | False | 0 |
| 30 | --- | --- | section | 0.7 | False | False | 0 |
| 31 | --- | --- | elevation | 0.7 | False | False | 0 |
| 32 | --- | --- | elevation | 0.9 | False | False | 0 |
| 33 | --- | --- | schedule_sheet | 0.9 | True | True | 3 |
| 34 | --- | --- | schedule_sheet | 0.9 | True | False | 1 |
| 35 | --- | --- | section | 0.7 | True | True | 2 |
| 36 | --- | --- | general_notes | 0.9 | False | False | 0 |
| 37 | --- | --- | detail_sheet | 0.7 | False | False | 0 |
| 38 | --- | --- | unknown | 0.0 | False | False | 0 |
| 39 | --- | --- | unknown | 0.0 | False | False | 0 |

## §2 — Module output summary

- Roofing: 40 pages with content, 338 total fields, 0 total warnings
- Glazing: 16 pages with content, 20 glazing / 81 door / 6 storefront items
- Tables populated on TradeModuleInput: 40 of 40 pages
- Per-page errors: 0

## §3 — Debug section 1 / 3 / 6 highlights

### Section 1 — dispatch_health

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
    "Filter 4 quality gate: 26 of 75 legends removed (49 kept)"
  ],
  "warning_count": 1,
  "timestamp": "2026-04-29T18:59:09.482121+00:00",
  "total_pages": 40,
  "sheet_map_source": "drawing_index",
  "sheet_count": 10,
  "mapped_pages": 4
}
```

### Section 3 — page_intelligence (40 entries)

Type distribution:
- `elevation`: 8
- `detail_sheet`: 8
- `schedule_sheet`: 8
- `unknown`: 4
- `section`: 3
- `framing_plan`: 2
- `general_notes`: 2
- `roof_plan`: 2
- `cover`: 1
- `floor_plan`: 1
- `ceiling_plan`: 1
- has_legend pages: 20

### Section 6 — legends: 49, quality_flags: 0

## §4 — Delta from previous iteration

(Baseline — no previous iteration to compare against.)

## §5 — Worst single problem identified (for next iteration's fix)

**Bug 1 — page-type ordering.** 7 pages have `has_schedule=True` (Filter 4 found schedule-like content) but are classified as non-schedule types by Filter 2: pages 1 (framing_plan), 2 (detail_sheet), 6 (detail_sheet), 7 (elevation), 8 (detail_sheet), 23 (detail_sheet), 35 (section). This is because `_PAGE_TYPE_RULES` checks ELEVATION (position 4) and DETAIL (position 5) before SCHEDULE (position 6) — first-match-wins. Pages with mixed content (both DETAIL/ELEVATION and SCHEDULE keywords in page text) get classified as the earlier-matching type. Fix for iter 1: move SCHEDULE rule higher in `_PAGE_TYPE_RULES` to give schedule classification priority on pages that contain schedule content.

## §6 — Iteration log

- Iteration: 0
- Fix: BASELINE — no fix
- Wall-clock: dispatch 30.7s / modules 83.8s / debug 0.0s
- Backend test floor: (verified separately)
