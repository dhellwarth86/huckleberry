# D.2 Hard Gate — Bearss Ave Distribution Center

**Date:** 2026-04-29
**Job ID:** `1efc6ea4-8a94-4b4c-9128-262fd1a0e2ae`
**Dispatch wall-clock:** 471.0s
**Overall:** PASS

## Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | 1. run_dispatch completes without raising | PASS | 471.0s |
| 2 | 2. Module output >= sweep baseline (90%) | PASS | roofing 769 >= 692, glazing 177 >= 159, door 31 >= 27, storefront 24 >= 21 |
| 3 | 3. Per-page module error rate < 25% | PASS | 0/91 = 0.0% |
| 4 | 4. Tables populated on schedule_sheet pages | PASS | 24/24 |
| 5 | 5. Persistence round-trip exact match | PASS | live roofing=769 db=769, live glazing=177 db=177, live door=31 db=31, live storefront=24 db=24 |
| 6 | 6. Vault-ruled module SHA-1 matches pre-chain | PASS | verified externally |
| 7 | 7. Frontend HTML SHA-1 matches pre-chain | PASS | verified externally |

## Module output (live)

- roofing_fields: 769
- glazing_items: 177
- door_items: 31
- storefront_items: 24
- errors: 0
- pages_attempted: 91

## Module output (from DB round-trip)

- roofing_fields: 769
- glazing_items: 177
- door_items: 31
- storefront_items: 24
- page_keys: 91

