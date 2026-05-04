# D.1 Silverleaf Hard Gate Report

**Date:** 2026-04-29
**Branch:** `phase2-v0.3-D1-storage-and-module-wiring`
**Bidset:** B2607 AEA Silverleaf — St Augustine — Accelerated Construction Services
**Pipeline:** wired (`run_dispatch(storage='auto')` — D.1 storage activation + Stage 13 trade module wiring)
**Overall: PASS**

---

## §1 — Wall-clock

- run_dispatch (wired): **139.8s** vs calibration baseline 59.3s (budget 187.1s)
- run_debug: 0.0s

## §2 — Dispatch summary

- detected_system: `None` / confidence: `0.0` / scope_pages: `[]`
- dispatch_complete: `True` / filters_completed: `['filter_1', 'filter_2', 'filter_4', 'filter_3', 'filter_5', 'stage_13_trade_modules']`
- dispatch_warnings: 1 total
  - `Filter 4 quality gate: 85 of 145 legends removed (60 kept)`
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

## §3 — Module output (from ctx.trade_module_outputs, populated by Stage 13)

- Roofing: 40 pages with content, **338 total fields**, 0 total warnings
- Glazing: 16 pages with content, **20 glazing / 81 door / 6 storefront items**
- Tables populated on schedule_sheet pages: **18/18**
- Per-page module errors: **0** (error rate 0.0%)

## §4 — Comparison vs calibration iter 2 baseline

| Metric | Calibration iter 2 | D.1 wired | Δ |
|---|---:|---:|---:|
| Roofing fields | 338 | 338 | +0 |
| Glazing items | 20 | 20 | +0 |
| Door items | 81 | 81 | +0 |
| Storefront items | 6 | 6 | +0 |
| Dispatch wall-clock | 59.3s | 139.8s | +80.5s |
| Schedule-sheet pages | 18 | 18 | +0 |
| Legends (debug §6) | 60 | 60 | +0 |
| Quality flags (debug §6) | 0 | 0 | +0 |

## §5 — Hard gate criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | 1. Module output ≥ 90% baseline AND no new exceptions | PASS | roofing 338 ≥ 304=True; glazing 20 ≥ 18=True; door 81 ≥ 73=True; storefront 6 ≥ 5=True; errors=0 |
| 2 | 2. Wired-dispatch wall-clock ≤ 187.1s (+30% of calibration iter 2's combined 143.9s = dispatch 59.3s + modules 84.6s) | PASS | actual 139.8s |
| 3 | 3. Tables populated on ≥ 16 schedule_sheet pages | PASS | 18/18 schedule_sheet pages have raw_tables |
| 4 | 4. dispatch_warnings shape: exactly one Filter 4 quality gate warning | PASS | 1 total warnings, 1 Filter 4 quality gate |
| 5 | No vault-ruled module modification | verified externally | SHA-1s captured separately at session end |
| 6 | Backend test floor 216/19/0 | verified externally | `pytest backend/tests/` |
| 7 | Frontend SHA-1 unchanged | verified externally | SHA-1s captured pre/post-session |

**Overall: PASS**

## §6 — Debug section 1 / 3 / 6 highlights

### Section 1 — dispatch_health

```json
{
  "dispatch_complete": true,
  "filters_completed": [
    "filter_1",
    "filter_2",
    "filter_4",
    "filter_3",
    "filter_5",
    "stage_13_trade_modules"
  ],
  "filter_count": 6,
  "warnings": [
    "Filter 4 quality gate: 85 of 145 legends removed (60 kept)"
  ],
  "warning_count": 1,
  "timestamp": "2026-04-29T20:46:35.695122+00:00",
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

## §7 — Schedule pages with raw_tables (pages where Stage 13 wired tables through)

- page 0 (sheet `---`): 2 table(s) cached
- page 1 (sheet `---`): 2 table(s) cached
- page 2 (sheet `---`): 2 table(s) cached
- page 3 (sheet `---`): 6 table(s) cached
- page 4 (sheet `S502`): 14 table(s) cached
- page 7 (sheet `---`): 19 table(s) cached
- page 9 (sheet `SW-3S`): 8 table(s) cached
- page 11 (sheet `---`): 1 table(s) cached
- page 15 (sheet `---`): 51 table(s) cached
- page 18 (sheet `---`): 8 table(s) cached
- page 20 (sheet `---`): 18 table(s) cached
- page 21 (sheet `---`): 5 table(s) cached
- page 23 (sheet `---`): 14 table(s) cached
- page 25 (sheet `WD1`): 6 table(s) cached
- page 26 (sheet `---`): 4 table(s) cached
- page 31 (sheet `---`): 23 table(s) cached
- page 33 (sheet `---`): 9 table(s) cached
- page 34 (sheet `---`): 14 table(s) cached
