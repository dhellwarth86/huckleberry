# D.2 Soft Gate — Silverleaf Persistence Round-Trip

**Date:** 2026-04-29
**Branch:** `phase2-v0.3-D2-job-folder-and-persistence`
**Job ID:** `45d58c49-2e78-41d7-91c4-759a7a8de0de`
**Database:** ~/.tracepoint/cache.db
**Overall:** PASS

## Round-trip assertions

| # | Assertion | Result | Evidence |
|---|---|---|---|
| 1 | get_job returns non-None | PASS | returned dict with id=45d58c49-2e78-41d7-91c4-759a7a8de0de |
| 2 | name == "B2607 AEA Silverleaf" | PASS | actual: 'B2607 AEA Silverleaf' |
| 3 | gc == "Accelerated Construction Services" | PASS | actual: 'Accelerated Construction Services' |
| 4 | trade_scope contains both trades | PASS | actual: 'roofing,glazing' |
| 5 | dispatch_results has 40 page entries | PASS | actual: 40 |
| 6 | 18 pages classified schedule_sheet | PASS | actual: 18 |
| 7 | ≥ 18 pages with raw_tables_json | PASS | actual: 18 |
| 8 | trade_outputs has 40 page keys | PASS | actual: 40 |
| 9 | Roofing fields aggregate == 338 | PASS | actual: 338 |
| 10 | Glazing items aggregate == 107 | PASS | actual: 107 (20g + 81d + 6s) |

**Overall:** PASS — all 10 assertions PASS

