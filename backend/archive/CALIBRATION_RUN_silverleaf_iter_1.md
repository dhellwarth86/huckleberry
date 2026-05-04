# Calibration Run — Silverleaf — Iteration 1

**Date:** 2026-04-29
**Iteration:** 1 of max 4
**Fix applied this iteration:** Bug 1: moved SCHEDULE rule to position 0 in _PAGE_TYPE_RULES (dispatch_gate.py line 105)
**Wall-clock:** dispatch 59.2s / modules 85.0s / debug 0.0s / total 144.1s

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
  "timestamp": "2026-04-29T19:05:27.501857+00:00",
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

- Page-type histogram delta: `schedule_sheet` 8 → 18 (+10); `elevation` 8 → 3 (-5); `detail_sheet` 8 → 5 (-3); `framing_plan` 2 → 1 (-1); `roof_plan` 2 → 1 (-1)
- Of 10 new schedule_sheet pages: 4 correctly flipped (pages 1, 2, 7, 23 — all had `has_schedule=True` in baseline), 6 are new classifications from full-text SCHEDULE keyword match (pages 0, 4, 11, 15, 21, 31)
- Section 6 quality_flags: 0 → 0 (no spike — new classifications not causing noise)
- Legend count: 49 → 60 (+11 — more pages running table extraction produces more legends)
- has_legend pages: 20 → 23 (+3)
- Dispatch wall-clock: 30.7s → 59.2s (+28.5s — Filter 4 table extraction on 10 more pages)
- Module output: unchanged (338 roofing fields, 20/81/6 glazing — harness uses direct-construction path)

## §5 — Worst single problem identified (for next iteration's fix)

**Bug 3 — tables plumbing via Path (c).** TradeModuleInput has a `tables: Optional[list[Any]] = None` field (added in C.3b), but `build_trade_input()` in trade_input_builder.py never populates it. Meanwhile `_parse_tables_on_page()` in dispatch_gate.py already calls `page.extract_tables()` but discards the raw table data after wrapping rows in Legend objects. Fix for iter 2: (1) add `raw_tables: Optional[list] = None` to PageContext in context.py, (2) modify `_parse_tables_on_page` to return raw tables alongside legends, (3) store raw_tables on page_ctx in run_filter_4, (4) extend `build_trade_input` to read page_ctx.raw_tables → TradeModuleInput.tables. This is Path (c) — single-touch dispatch-side, no vault violation, no double extraction cost.

## §6 — Iteration log

- Iteration: 1
- Fix: Bug 1: moved SCHEDULE rule to position 0 in _PAGE_TYPE_RULES (dispatch_gate.py line 105)
- Wall-clock: dispatch 59.2s / modules 85.0s / debug 0.0s
- Backend test floor: (verified separately)
