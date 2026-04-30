# D.2 Hard Gate — Vine Street

**Date:** 2026-04-29
**Job ID:** `fa4868da-dd5b-4679-893f-3a44d5047f12`
**Dispatch wall-clock:** 1194.5s
**Overall:** PASS

## Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | 1. run_dispatch completes without raising | PASS | 1194.5s |
| 2 | 2. Module output >= sweep baseline (90%) | PASS | roofing 1201 >= 1080, glazing 100 >= 90, door 12 >= 11, storefront 23 >= 21 |
| 3 | 3. Per-page module error rate < 25% | PASS | 0/138 = 0.0% |
| 4 | 4. Tables populated on schedule_sheet pages | PASS | 41/41 |
| 5 | 5. Persistence round-trip exact match | PASS | live roofing=1201 db=1201, live glazing=100 db=100, live door=12 db=12, live storefront=23 db=23 |
| 6 | 6. Vault-ruled module SHA-1 matches pre-chain | PASS | verified externally |
| 7 | 7. Frontend HTML SHA-1 matches pre-chain | PASS | verified externally |

## Module output (live)

- roofing_fields: 1201
- glazing_items: 100
- door_items: 12
- storefront_items: 23
- errors: 0
- pages_attempted: 138

## Module output (from DB round-trip)

- roofing_fields: 1201
- glazing_items: 100
- door_items: 12
- storefront_items: 23
- page_keys: 138

