# Block Run — Master Ledger

**Purpose:** Single chronological log of every file created, modified, or deleted, every commit, every push, every config or schema change across the calibration → Phase D → Phase E chain. Updated at the end of each phase. Read top-to-bottom for "what's been touched" without re-reading march orders or gate reports.

**Started:** 2026-04-29 by calibration session on B2607 AEA Silverleaf.
**Phases this ledger spans:** calibration-silverleaf, phase-D-storage-and-wiring, phase-E-backend-api.

---

## Phase 1: Calibration — B2607 AEA Silverleaf (2026-04-29)

**Branch:** `phase2-v0.3-calibration-silverleaf` (from `06d46c5`)
**Trigger:** Daniel directive 2026-04-29 — first calibration session of program; dispatch-side only; iterative; vault rule active on five trade modules.

### Files created
- `backend/scripts/calibrate_silverleaf.py` — calibration runner harness for Silverleaf bidset
- `backend/CALIBRATION_RUN_silverleaf_iter_0.md` — baseline iteration report
- `backend/CALIBRATION_RUN_silverleaf_iter_1.md` — Bug 1 fix iteration report
- `backend/CALIBRATION_RUN_silverleaf_iter_2.md` — Bug 3 fix iteration report
- `backend/CALIBRATION_GATE_REPORT_silverleaf.md` — final gate report
- `backend/BLOCK_RUN.md` — this file (master ledger)

### Files modified
- `backend/core/dispatch_gate.py`
  - Line 105: moved SCHEDULE rule from position 6 to position 0 in `_PAGE_TYPE_RULES` (Bug 1 fix, iter 1)
  - Lines 733-779: `_parse_tables_on_page` return type changed from `list[Legend]` to `tuple[list[Legend], list]`; raw tables preserved alongside legends (Bug 3 fix, iter 2)
  - Lines 839-842: `run_filter_4` unpacks `(table_legends, raw_tables)` tuple; stores `raw_tables` on `page_ctx.raw_tables` (Bug 3 fix, iter 2)
- `backend/core/context.py`
  - Line 204: added `raw_tables: Optional[list] = None` field to `PageContext` dataclass (Bug 3 fix, iter 2)
- `backend/core/trade_input_builder.py`
  - Lines 130-162: `build_trade_input` reads `page_ctx.raw_tables` and passes to `TradeModuleInput(tables=...)` (Bug 3 fix, iter 2)

### Files deleted
None.

### Commits
(single commit at session end — see gate report)

### Pushes
(single push at session end — see gate report)

### Dependency / config changes
None. No `pyproject.toml` change. No schema change. No new deps.

### Vault-ruled files touched
None. Vault rule held throughout. SHA-1 verification at session end:
- `roofing_module.py`: `ae9e5b284191b45de419faacf11771da27a548f9`
- `glazing_module.py`: `52c014421915ec6a66b4a6860b71a0a3274920f2`
- `roofing_vocabulary.py`: `ec6c17f8955ef8e27c3ff1d552b299a6962c9d0b`
- `glazing_vocabulary.py`: `64249c8ef5f7d9db50added3c9a40836cba356ea`
- `debug_module.py`: `78f71d9030cde3b173389603f5f39bd6bedaac07`

---

## Phase 2: Phase D — storage activation + job folder + module wiring (TBD)

(Populated by Phase D session.)

---

## Phase 3: Phase E — backend API + frontend consumption (TBD)

(Populated by Phase E session.)

---
