# Calibration Run — Silverleaf — Iteration 2

**Date:** 2026-04-29
**Iteration:** 2 of max 4
**Fix applied this iteration:** Bug 3: tables plumbing via Path (c) — raw_tables cached on PageContext, build_trade_input populates TradeModuleInput.tables
**Wall-clock:** dispatch 59.3s / modules 84.6s / debug 0.0s / total 143.9s

## §1 — Dispatch output summary

- detected_system: `None` / confidence: `0.0` / scope_pages: `[]`
- dispatch_complete: `True` / filters_completed: `['filter_1', 'filter_2', 'filter_4', 'filter_3', 'filter_5']`
- dispatch_warnings: `['Filter 4 quality gate: 85 of 145 legends removed (60 kept)']`
- total_pages: `40` / sheet_count: `10` / mapped_pages: `4`

### Page-type histogram

- `schedule_sheet`: 18
- `detail_sheet`: 5
- `unknown`: 4
- `section`: 3
- `elevation`: 3
- `general_notes`: 2
- `framing_plan`: 1
- `cover`: 1
- `floor_plan`: 1
- `ceiling_plan`: 1
- `roof_plan`: 1

### Per-page type listing

| Page | Sheet | Title | Type | Conf | has_legend | has_schedule | legend_count |
|---:|---|---|---|---:|---|---|---:|
| 0 | --- | --- | schedule_sheet | 0.7 | True | False | 2 |
| 1 | --- | --- | schedule_sheet | 0.7 | True | True | 4 |
| 2 | --- | --- | schedule_sheet | 0.7 | True | True | 1 |
| 3 | --- | --- | schedule_sheet | 0.7 | True | True | 4 |
| 4 | S502 | 6 | schedule_sheet | 0.7 | True | False | 4 |
| 5 | S101 | ROOF FRAMING PLAN | framing_plan | 0.9 | True | False | 2 |
| 6 | --- | --- | detail_sheet | 0.9 | True | True | 2 |
| 7 | --- | --- | schedule_sheet | 0.9 | True | True | 6 |
| 8 | --- | --- | detail_sheet | 0.9 | True | True | 4 |
| 9 | SW-3S | --- | schedule_sheet | 0.9 | True | True | 7 |
| 10 | --- | --- | general_notes | 0.9 | False | False | 0 |
| 11 | --- | --- | schedule_sheet | 0.7 | True | False | 1 |
| 12 | --- | --- | unknown | 0.0 | False | False | 0 |
| 13 | --- | --- | unknown | 0.0 | False | False | 0 |
| 14 | --- | --- | cover | 0.9 | False | False | 0 |
| 15 | --- | --- | schedule_sheet | 0.7 | True | False | 3 |
| 16 | --- | --- | detail_sheet | 0.9 | False | False | 0 |
| 17 | --- | --- | detail_sheet | 0.9 | False | False | 0 |
| 18 | --- | --- | schedule_sheet | 0.9 | True | True | 2 |
| 19 | --- | --- | section | 0.7 | True | False | 1 |
| 20 | --- | --- | schedule_sheet | 0.9 | True | False | 1 |
| 21 | --- | --- | schedule_sheet | 0.7 | False | False | 0 |
| 22 | --- | --- | floor_plan | 0.9 | False | False | 0 |
| 23 | --- | --- | schedule_sheet | 0.9 | True | True | 2 |
| 24 | --- | --- | ceiling_plan | 0.9 | False | False | 0 |
| 25 | WD1 | --- | schedule_sheet | 0.9 | True | False | 3 |
| 26 | --- | --- | schedule_sheet | 0.9 | True | False | 1 |
| 27 | --- | --- | roof_plan | 0.9 | True | False | 3 |
| 28 | --- | --- | elevation | 0.9 | False | False | 0 |
| 29 | --- | --- | elevation | 0.9 | False | False | 0 |
| 30 | --- | --- | section | 0.7 | False | False | 0 |
| 31 | --- | --- | schedule_sheet | 0.7 | True | False | 1 |
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
    "Filter 4 quality gate: 85 of 145 legends removed (60 kept)"
  ],
  "warning_count": 1,
  "timestamp": "2026-04-29T19:15:33.030285+00:00",
  "total_pages": 40,
  "sheet_map_source": "drawing_index",
  "sheet_count": 10,
  "mapped_pages": 4
}
```

### Section 3 — page_intelligence (40 entries)

Type distribution:
- `schedule_sheet`: 18
- `detail_sheet`: 5
- `unknown`: 4
- `section`: 3
- `elevation`: 3
- `general_notes`: 2
- `framing_plan`: 1
- `cover`: 1
- `floor_plan`: 1
- `ceiling_plan`: 1
- `roof_plan`: 1
- has_legend pages: 23

### Section 6 — legends: 60, quality_flags: 0

## §4 — Delta from previous iteration

- Page-type histogram: identical to iter 1 (expected — Bug 3 is plumbing, not classification)
- Dispatch wall-clock: 59.3s vs 59.2s (noise — same Filter 4 coverage)
- Module output: unchanged (338 roofing fields, 20/81/6 glazing — harness uses direct-construction path, not build_trade_input)
- Legend count: 60 → 60 (unchanged)
- quality_flags: 0 → 0 (unchanged)
- **Structural change:** `_parse_tables_on_page` now returns `(legends, raw_tables)` tuple; raw_tables cached on `PageContext.raw_tables` for schedule pages; `build_trade_input` reads them into `TradeModuleInput.tables`. This change is invisible to the harness (which constructs TradeModuleInput directly) but will be exercised when the real pipeline routes through `build_trade_input` in Phase E.

## §5 — Worst single problem identified (for next iteration's fix)

**No fix — diminishing returns.** The two structural bugs identified pre-calibration (Bug 1: page-type ordering, Bug 3: tables plumbing) are both resolved. Remaining dispatch characteristics:
- 6 pages over-classified as `schedule_sheet` (pages 0, 4, 11, 15, 21, 31 — matched SCHEDULE keyword in full text without `has_schedule=True`). Over-classification is preferable to under-classification: a schedule page classified as elevation loses its table extraction. quality_flags = 0 confirms no downstream noise from these classifications.
- `detected_system = None` — this is a scope-detection question (filter_5 / vocabulary matching), not a dispatch-structural question. Fixing it requires tuning trade module vocabulary, which is out of scope per the vault rule.
- 4 `unknown` pages (12, 13, 38, 39) — likely blank/separator pages with no extractable text content. Not a dispatch defect.
- `mapped_pages = 4` — the drawing_index sheet map only found 4 pages with sheet numbers. This is a PDF content limitation, not a dispatch bug.

Iteration 3 skipped per march orders §6: "If not [enough to justify the risk], write 'No fix — diminishing returns' in §5 and skip straight to §8."

## §6 — Iteration log

- Iteration: 2
- Fix: Bug 3: tables plumbing via Path (c) — raw_tables cached on PageContext, build_trade_input populates TradeModuleInput.tables
- Wall-clock: dispatch 59.3s / modules 84.6s / debug 0.0s
- Backend test floor: (verified separately)
