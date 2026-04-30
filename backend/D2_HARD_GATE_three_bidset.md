# D.2 Three-Bidset Hard Gate

**Date:** 2026-04-29
**Branch:** `phase2-v0.3-D2-job-folder-and-persistence`
**Bidsets:** Bearss Ave / Shoppes at Avalon / Vine Street
**Overall:** PASS

## Per-bidset summary

| Bidset | Pages | Dispatch wall-clock | Roofing fields | Glazing items | Total errors | Round-trip | Result |
|---|---:|---:|---:|---:|---:|---|---|
| Bearss Ave Distribution Center | 91 | 471.0s | 769 | 177/31/24 | 0 | PASS | PASS |
| Shoppes at Avalon | 97 | 721.8s | 833 | 43/22/22 | 0 | PASS | PASS |
| Vine Street | 138 | 1194.5s | 1201 | 100/12/23 | 0 | PASS | PASS |

## Bearss Ave Distribution Center — criteria detail

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | 1. run_dispatch completes without raising | PASS | 471.0s |
| 2 | 2. Module output >= sweep baseline (90%) | PASS | roofing 769 >= 692, glazing 177 >= 159, door 31 >= 27, storefront 24 >= 21 |
| 3 | 3. Per-page module error rate < 25% | PASS | 0/91 = 0.0% |
| 4 | 4. Tables populated on schedule_sheet pages | PASS | 24/24 |
| 5 | 5. Persistence round-trip exact match | PASS | live roofing=769 db=769, live glazing=177 db=177, live door=31 db=31, live storefront=24 db=24 |
| 6 | 6. Vault-ruled module SHA-1 matches pre-chain | PASS | verified externally |
| 7 | 7. Frontend HTML SHA-1 matches pre-chain | PASS | verified externally |

## Shoppes at Avalon — criteria detail

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | 1. run_dispatch completes without raising | PASS | 721.8s |
| 2 | 2. Module output >= sweep baseline (90%) | PASS | roofing 833 >= 750, glazing 43 >= 38, door 22 >= 20, storefront 22 >= 20 |
| 3 | 3. Per-page module error rate < 25% | PASS | 0/97 = 0.0% |
| 4 | 4. Tables populated on schedule_sheet pages | PASS | 13/13 |
| 5 | 5. Persistence round-trip exact match | PASS | live roofing=833 db=833, live glazing=43 db=43, live door=22 db=22, live storefront=22 db=22 |
| 6 | 6. Vault-ruled module SHA-1 matches pre-chain | PASS | verified externally |
| 7 | 7. Frontend HTML SHA-1 matches pre-chain | PASS | verified externally |

## Vine Street — criteria detail

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | 1. run_dispatch completes without raising | PASS | 1194.5s |
| 2 | 2. Module output >= sweep baseline (90%) | PASS | roofing 1201 >= 1080, glazing 100 >= 90, door 12 >= 11, storefront 23 >= 21 |
| 3 | 3. Per-page module error rate < 25% | PASS | 0/138 = 0.0% |
| 4 | 4. Tables populated on schedule_sheet pages | PASS | 41/41 |
| 5 | 5. Persistence round-trip exact match | PASS | live roofing=1201 db=1201, live glazing=100 db=100, live door=12 db=12, live storefront=23 db=23 |
| 6 | 6. Vault-ruled module SHA-1 matches pre-chain | PASS | verified externally |
| 7 | 7. Frontend HTML SHA-1 matches pre-chain | PASS | verified externally |

## Overall: PASS

