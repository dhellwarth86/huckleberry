# Calibration Gate Report — Silverleaf

**Date:** 2026-04-29
**Branch:** `phase2-v0.3-calibration-silverleaf`
**Bidset:** B2607 AEA Silverleaf — St Augustine — Accelerated Construction Services
**Iterations completed:** 3 (baseline + 2 fixes; iteration 3 skipped — diminishing returns)

---

## Gate checklist

- [x] Pre-flight: 216/19/0 backend; frontend 138/138; Silverleaf located and 40 pages
- [x] `backend/scripts/calibrate_silverleaf.py` written, tracked, runs cleanly
- [x] `backend/BLOCK_RUN.md` created at session start; populated at session end with all touches
- [x] Iteration 0 (baseline) report saved at `backend/CALIBRATION_RUN_silverleaf_iter_0.md`
- [x] At least 1 fix iteration completed; iter reports saved (iter_0, iter_1, iter_2)
- [x] Each fix iteration's report identifies ONE single worst problem and applies ONE fix
- [x] Final iteration's report says "No fix — diminishing returns" (iter 2 §5)
- [x] Bug 1 status: fixed in iter 1 — SCHEDULE rule moved to position 0 in `_PAGE_TYPE_RULES`
- [x] Bug 3 status: fixed in iter 2 — Path (c): `_parse_tables_on_page` returns raw tables alongside legends; cached on `PageContext.raw_tables`; `build_trade_input` reads them into `TradeModuleInput.tables`
- [x] No vault-ruled module modification (SHA-1 verified at session end — see below)
- [x] No `pyproject.toml` change
- [x] dispatch_gate.py changes: documented per-line in BLOCK_RUN.md, single-purpose per iteration
- [x] trade_input_builder.py changes: only as required by Bug 3 Path (c)
- [x] Backend suite: 216 passed, 19 skipped, 0 failed (zero new tests added)
- [x] Frontend: 138/138
- [x] Single commit on `phase2-v0.3-calibration-silverleaf`; pushed to origin
- [x] §7 stops: enumerated below
- [x] Final gate report produced (this file)
- [x] BLOCK_RUN.md fully populated

---

## Files changed

| File | Action | Purpose |
|---|---|---|
| `backend/scripts/calibrate_silverleaf.py` | NEW | Calibration runner harness |
| `backend/CALIBRATION_RUN_silverleaf_iter_0.md` | NEW | Baseline report |
| `backend/CALIBRATION_RUN_silverleaf_iter_1.md` | NEW | Bug 1 fix report |
| `backend/CALIBRATION_RUN_silverleaf_iter_2.md` | NEW | Bug 3 fix report |
| `backend/CALIBRATION_GATE_REPORT_silverleaf.md` | NEW | This gate report |
| `backend/BLOCK_RUN.md` | NEW | Master ledger |
| `backend/core/dispatch_gate.py` | MODIFIED | Bug 1 (line 105: SCHEDULE priority) + Bug 3 (lines 733-842: raw_tables plumbing) |
| `backend/core/context.py` | MODIFIED | Bug 3 (line 204: `raw_tables` field on PageContext) |
| `backend/core/trade_input_builder.py` | MODIFIED | Bug 3 (lines 130-162: read raw_tables → TradeModuleInput.tables) |

## Files NOT changed

| File | Status |
|---|---|
| `backend/core/roofing_module.py` | Vault-ruled, untouched |
| `backend/core/glazing_module.py` | Vault-ruled, untouched |
| `backend/core/roofing_vocabulary.py` | Vault-ruled, untouched |
| `backend/core/glazing_vocabulary.py` | Vault-ruled, untouched |
| `backend/core/debug_module.py` | Vault-ruled, untouched |
| `backend/pyproject.toml` | No change |
| `frontend/Huckleberry_AI_6.3.5_Scope.html` | Sacred, untouched |

---

## Iteration summary

| Iter | Fix | schedule_sheet | elevation | detail_sheet | legends | quality_flags | dispatch_time |
|---:|---|---:|---:|---:|---:|---:|---|
| 0 | BASELINE | 8 | 8 | 8 | 49 | 0 | 30.7s |
| 1 | Bug 1: SCHEDULE rule to pos 0 | 18 | 3 | 5 | 60 | 0 | 59.2s |
| 2 | Bug 3: raw_tables plumbing | 18 | 3 | 5 | 60 | 0 | 59.3s |
| 3 | Skipped — diminishing returns | — | — | — | — | — | — |

### Bug 1 impact
- +10 pages classified as `schedule_sheet` (from 8 → 18)
- 4 correctly flipped (had `has_schedule=True` in baseline: pages 1, 2, 7, 23)
- 6 new classifications from full-text SCHEDULE keyword match (pages 0, 4, 11, 15, 21, 31)
- quality_flags remained 0 — no downstream noise from over-classification
- Dispatch wall-clock doubled (30.7s → 59.2s) due to Filter 4 table extraction on 10 more pages

### Bug 3 impact
- Structural plumbing only — dispatch output unchanged from iter 1
- `_parse_tables_on_page` now returns `(legends, raw_tables)` tuple
- Raw tables cached on `PageContext.raw_tables` for schedule pages
- `build_trade_input` reads `raw_tables` into `TradeModuleInput.tables`
- Change invisible to harness (which bypasses `build_trade_input`); exercised when real pipeline routes through `build_trade_input` in Phase E

---

## Vault-ruled module SHA-1 verification

```
ae9e5b284191b45de419faacf11771da27a548f9  roofing_module.py
52c014421915ec6a66b4a6860b71a0a3274920f2  glazing_module.py
ec6c17f8955ef8e27c3ff1d552b299a6962c9d0b  roofing_vocabulary.py
64249c8ef5f7d9db50added3c9a40836cba356ea  glazing_vocabulary.py
78f71d9030cde3b173389603f5f39bd6bedaac07  debug_module.py
```

All match pre-session values. Vault rule held.

---

## §7 stop status

Per march orders §7, four enumerated stops:

1. **Backend tests regress below 216/19/0:** Did NOT fire. 216/19/0 held after every fix.
2. **New test file created:** Did NOT fire. Zero new tests.
3. **Vault-ruled file opened or modified:** Did NOT fire. SHA-1 confirmed unchanged.
4. **pyproject.toml modified:** Did NOT fire. No dependency changes.

---

## Tests

- Backend: 216 passed, 19 skipped, 0 failed
- Frontend: 138/138 passed, 0 failed

---

## Karpathy discipline

- Read first: CLAUDE.md, march orders, all 12 documents in prescribed order before any work
- Diagnostic before action: baseline iteration 0 run before any fix applied
- One fix per iteration: Bug 1 in iter 1, Bug 3 in iter 2
- Data-driven stopping: iter 3 skipped after iter 2 showed no remaining dispatch-structural problems
- No threshold tuning, no scope creep, no vault violations

---

## Next step

**AWAITING APPROVAL:** commit on `phase2-v0.3-calibration-silverleaf` and push to origin. The branch continues into Phase D (storage activation + job folder + module wiring) per BLOCK_RUN.md.
