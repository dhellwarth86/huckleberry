# D.2 Hard Gate — Shoppes at Avalon

**Date:** 2026-04-29
**Job ID:** `725c44b8-1493-4ab6-b4a8-abd8507ac8d8`
**Dispatch wall-clock:** 721.8s
**Overall:** PASS

## Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | 1. run_dispatch completes without raising | PASS | 721.8s |
| 2 | 2. Module output >= sweep baseline (90%) | PASS | roofing 833 >= 750, glazing 43 >= 38, door 22 >= 20, storefront 22 >= 20 |
| 3 | 3. Per-page module error rate < 25% | PASS | 0/97 = 0.0% |
| 4 | 4. Tables populated on schedule_sheet pages | PASS | 13/13 |
| 5 | 5. Persistence round-trip exact match | PASS | live roofing=833 db=833, live glazing=43 db=43, live door=22 db=22, live storefront=22 db=22 |
| 6 | 6. Vault-ruled module SHA-1 matches pre-chain | PASS | verified externally |
| 7 | 7. Frontend HTML SHA-1 matches pre-chain | PASS | verified externally |

## Module output (live)

- roofing_fields: 833
- glazing_items: 43
- door_items: 22
- storefront_items: 22
- errors: 0
- pages_attempted: 97

## Module output (from DB round-trip)

- roofing_fields: 833
- glazing_items: 43
- door_items: 22
- storefront_items: 22
- page_keys: 97

