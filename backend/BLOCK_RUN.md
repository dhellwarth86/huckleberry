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

## Phase 2: Phase D — storage activation + module wiring (D.1) (2026-04-29)

**Branch:** `phase2-v0.3-D1-storage-and-module-wiring` (from calibration head `2c56913`)
**Trigger:** Daniel directive 2026-04-29 — green-light Phase D after calibration soft-gate review; D scoped to storage activation + module wiring + Silverleaf hard gate; D.2 (job folder, multi-tenant, schema migration) deferred to its own future phase.
**Scope discipline:** Single session, auto-run, no CLAUDE.md touches (file retired by Daniel), PROJECT_CLAUDE.md is only canonical doc edited, frontend vault-treated.

### Files created
- `backend/scripts/d1_silverleaf_hardgate.py` — tracked hard-gate harness (`run_dispatch(storage="auto")` end-to-end + 7-criterion comparison vs calibration iter 2 baseline)
- `backend/D_HARD_GATE_silverleaf.md` — D.1 hard gate report (overall PASS)
- `MARCH_ORDERS_phase_D1.md` — phase D.1 march orders (root-level)

### Files modified
- `backend/core/dispatch_gate.py`
  - +159 / −2 lines, all D.1 additions line-tagged `# D.1:`
  - `_resolve_storage(storage)` helper + `_DEFAULT_STORAGE_INSTANCE` lazy singleton (sentinel `storage="auto"` triggers default `StorageEngine()` construction; `storage=None` preserves legacy no-op)
  - `_build_dispatch_only_input(ctx, page_idx, text_blocks, raw_tables)` helper (geometry-zeroed `TradeModuleInput`; matches C.2-established equivalent path)
  - `_run_trade_modules(engine, doc, ctx)` Stage 13 helper (RoofingModule + GlazingModule per page, errors caught + logged to `dispatch_warnings` without aborting; per-module error rate >25% surfaced as warning per orders §11 #6; pdfplumber re-used to extract per-page text_blocks + fall-back tables for non-schedule pages so module coverage matches calibration's all-pages reach)
  - `run_dispatch()` invokes `_run_trade_modules()` after `_extract_project_metadata()` when `storage is not None`; appends `"stage_13_trade_modules"` to `ctx.filters_completed`
- `backend/core/context.py`
  - +7 / −0 lines: single additive field on `PlanSetContext` (`trade_module_outputs: dict[int, dict[str, Any]] = field(default_factory=dict)`); default empty dict preserves all legacy behaviour
- `PROJECT_CLAUDE.md`
  - §1 — dropped retired-CLAUDE.md row; renumbered table (4 canonical docs → 3 + active march orders); added retirement note
  - §3 — added Calibration session paragraph + Phase D.1 paragraph + branch state addendum
  - §7 — phase table updated: Calibration → COMPLETE; D.1 → COMPLETE; D.2 → next-eligible; E → next-eligible / now UNBLOCKED; module tuning + C.4 → deferred
  - §8 — rewrote next-planning-conversation as Phase E vs D.2 decision
  - Sections §2, §4, §5, §6, §9, §10 untouched per orders §6
- `VALIDATION_LEDGER.md`
  - §A2 — appended four rows: D.1 dispatch_gate.py modifications, D.1 context.py modifications, retroactive calibration dispatch_gate.py / context.py / trade_input_builder.py rows
  - §D — appended three rows: Silverleaf calibration session, Silverleaf D.1 hard gate, plus matching headline-numbers subsections
- `backend/BLOCK_RUN.md`
  - this file — Phase 2 D.1 section populated

### Files deleted
None.

### Commits
- D.1 single commit on `phase2-v0.3-D1-storage-and-module-wiring` (SHA recorded after commit)

### Pushes
- D.1 branch pushed to origin (`https://github.com/dhellwarth86/huckleberry.git`) at session end

### Dependency / config changes
None. SQLite (already in `pyproject.toml` from B.4 via stdlib `sqlite3`) is what storage activates. No new deps. No `pyproject.toml` modification.

### Vault-ruled files touched
None. SHA-1 verification at session end (matches pre-session):
- `roofing_module.py`: `ae9e5b284191b45de419faacf11771da27a548f9`
- `glazing_module.py`: `52c014421915ec6a66b4a6860b71a0a3274920f2`
- `roofing_vocabulary.py`: `ec6c17f8955ef8e27c3ff1d552b299a6962c9d0b`
- `glazing_vocabulary.py`: `64249c8ef5f7d9db50added3c9a40836cba356ea`
- `debug_module.py`: `78f71d9030cde3b173389603f5f39bd6bedaac07`

### Frontend touched
None. SHA-1 verification at session end (matches pre-session):
- `Huckleberry_AI_6.3.1_Scope.html`: `a80463efe09a51e21c54635c34469fb64172f7b7`
- `Huckleberry_AI_6.3.2_Scope.html`: `09702119c7c299ae03c4b8f401c1a1a2c4db1626`
- `Huckleberry_AI_6.3.3_Scope.html`: `e8ba836c64df15277c9f8a36b7e28031f7b61f2a`
- `Huckleberry_AI_6.3.4_Scope.html`: `aaeddf686c8c74d79b2409d1b4fde1831b7f02c3`
- `Huckleberry_AI_6.3.5_Scope.html`: `cf3765d61fd6f17de46024a3a84c62f25b19b3c5`

### CLAUDE.md
Not opened, not edited, not referenced. File was retired by Daniel directive 2026-04-29 prior to this session; it is deleted in the working tree (moved to `previous handoff/CLAUDE.md` by Daniel before session start). The deletion is NOT staged in this D.1 commit — Daniel's archive movement is his to commit when ready. PROJECT_CLAUDE.md was the only canonical doc edited this session (per orders §0).

### Hard gate result
Silverleaf hard gate via `backend/scripts/d1_silverleaf_hardgate.py`: **PASS**, all 7 criteria. Module output exact parity with calibration iter 2 (338 roofing / 20-81-6 glazing). Wired-dispatch 139.8s under the 187.1s budget. 0 per-page module errors. See `backend/D_HARD_GATE_silverleaf.md`.

### §7 stops fired
None. Each §11 stop in MARCH_ORDERS_phase_D1.md verified non-firing at session end.

### Sacred floor at session end
Backend 216 passed, 19 skipped, 0 failed. Frontend 138/138 (verified at pre-flight against `Huckleberry_AI_6.3.5_Scope.html` per package.json default; not re-run at session end since frontend was vault-treated).

---

## Phase 2.5: Housekeeping — safe_for_removal sweep (2026-04-29)

**Branch:** `phase2-v0.3-housekeeping-safe-for-removal` (from D.1 head `b478456`)
**Trigger:** Daniel directive 2026-04-29 — clear retired files into `safe_for_removal/` folder before D.2 starts; manifest preserves recovery info; folder reviewed and deleted in future session, manifest preserved as wiki source.
**Scope discipline:** No production-code touches; no vault-ruled module touches; no frontend touches; no test suite touches; no canonical doc edits beyond a single PROJECT_CLAUDE.md §3 paragraph.

### Files created
- `safe_for_removal/` (new directory at workspace root)
- `safe_for_removal/README.md`
- `safe_for_removal/MANIFEST.md` — load-bearing artifact (survives folder deletion as wiki source)
- `safe_for_removal/march_orders/` — 3 retired completed-phase march orders
- `safe_for_removal/previous_handoff/contents/` — 5 archived handoff files (4 superseded handoffs + 1 archive copy of retired CLAUDE.md)
- `safe_for_removal/previous_orders/contents/` — 16 archived march orders + 2 STEP files
- `safe_for_removal/anomalous_nested_repo_huckleberry/repo_root` — embedded gitlink to anomalous nested repo found at workspace root
- `safe_for_removal/intake_diagnostic_outputs/` — 2 reports + 2 scripts + 2 summary JSONs + 19 per-bidset CSVs
- `safe_for_removal/pre_phase_B_validation/` — 5 markdown reports + 6 superseded scripts
- `safe_for_removal/superseded_scripts/` — 2 one-shot harnesses (c5_run_through.py, sweep_three_bidsets.py)
- `safe_for_removal/old_terminal_logs/` — 1 v0.2-era sweep log
- `backend/HOUSEKEEPING_GATE_REPORT.md` — final gate report

### Files moved
**Tracked moves (git rename, history preserved):** 25 files
- Workspace-root MARCH_ORDERS (3): `MARCH_ORDERS_calibration_silverleaf.md`, `MARCH_ORDERS_profile_and_housekeeping.md`, `MARCH_ORDERS_three_bidset_sweep.md` → `safe_for_removal/march_orders/`
- `previous handoff/` (4): `HANDOFF_2026-04-26.md`, `HANDOFF_FINAL_2026-04-27.md`, `HANDOFF_v3_2026-04-27.md`, `PHASE_2_HANDOFF.md` → `safe_for_removal/previous_handoff/contents/`
- `previous orders/` (12): all `MARCH_ORDERS_B_*.md`, `MARCH_ORDERS_C_*.md`, `MARCH_ORDERS_D8_FOLLOWUP.md`, `MARCH_ORDERS_page_type_verification.md`, `STEP_17_REVIEW_CHECKLIST.md`, `STEP_18_DECISION_BRIEF.md` → `safe_for_removal/previous_orders/contents/`
- `backend/INTAKE_DIAGNOSTIC*.md` (2) + `backend/scripts/intake_diagnostic*.py` (2) → `safe_for_removal/intake_diagnostic_outputs/`
- `backend/EXPERIMENT_*.md` (2) + `backend/PUBLIC_CORPUS_OBSERVATIONS.md` + `backend/TRACEPOINT_DISCOVERY.md` + `backend/V0_2_VALIDATION.md` (5) → `safe_for_removal/pre_phase_B_validation/`
- `backend/scripts/run_experiment.py` + `analyze_outputs.py` + `compare_v0.1_to_v0.2.py` + `verify_v02_outputs.py` + `run_dispatch_on_15_bidsets.py` + `run_dispatch_on_public_corpus.py` (6) → `safe_for_removal/pre_phase_B_validation/`
- `backend/scripts/c5_run_through.py` + `sweep_three_bidsets.py` (2) → `safe_for_removal/superseded_scripts/`

**Untracked moves (newly added under safe_for_removal/):** 28 items
- 1 archive copy of CLAUDE.md (Daniel's pre-session archive)
- 4 archive duplicates of MARCH_ORDERS already moved via the workspace-root path (calibration, profile/housekeeping, three-bidset sweep — Daniel had pre-staged these)
- 19 intake-diagnostic CSVs (previously untracked at `backend/test_fixtures/intake_diagnostic_outputs/`)
- 2 intake-diagnostic summary JSONs
- 1 anomalous nested repo (gitlink only)
- 1 v0.2_sweep.log

**Total: 53 file/path moves across 8 categories.** Soft observation per orders §11 #7: count between 50 and 100, surfaced for awareness but not a hard stop.

### Files modified
- `PROJECT_CLAUDE.md` — single new paragraph appended to §3 (housekeeping complete note); no other sections touched per orders §6
- `backend/BLOCK_RUN.md` — this section (Phase 2.5) added between Phase 2 and Phase 3 per orders §7

### Files deleted
None this session. (Files in `safe_for_removal/` pending Daniel review before deletion.) Note: an unstaged deletion of root `CLAUDE.md` exists in working tree from Daniel's pre-session retirement movement; that deletion is NOT staged in this commit per orders §0 instruction to leave CLAUDE.md untouched.

### Commits
- Single housekeeping commit on `phase2-v0.3-housekeeping-safe-for-removal` (SHA recorded after commit lands)

### Pushes
- Branch pushed to origin at session end

### Vault-ruled files touched
None. SHA-1 verification at session end (matches pre-session captured at HK.0):
- `roofing_module.py`: `ae9e5b284191b45de419faacf11771da27a548f9`
- `glazing_module.py`: `52c014421915ec6a66b4a6860b71a0a3274920f2`
- `roofing_vocabulary.py`: `ec6c17f8955ef8e27c3ff1d552b299a6962c9d0b`
- `glazing_vocabulary.py`: `64249c8ef5f7d9db50added3c9a40836cba356ea`
- `debug_module.py`: `78f71d9030cde3b173389603f5f39bd6bedaac07`

### Frontend touched
None. SHA-1 verification at session end (matches pre-session):
- `Huckleberry_AI_6.3.1_Scope.html`: `a80463efe09a51e21c54635c34469fb64172f7b7`
- `Huckleberry_AI_6.3.2_Scope.html`: `09702119c7c299ae03c4b8f401c1a1a2c4db1626`
- `Huckleberry_AI_6.3.3_Scope.html`: `e8ba836c64df15277c9f8a36b7e28031f7b61f2a`
- `Huckleberry_AI_6.3.4_Scope.html`: `aaeddf686c8c74d79b2409d1b4fde1831b7f02c3`
- `Huckleberry_AI_6.3.5_Scope.html`: `cf3765d61fd6f17de46024a3a84c62f25b19b3c5`

### Sacred floor at session end
Backend 216 passed, 19 skipped, 0 failed (verified pre-flight at HK.0 and post-moves before commit). Frontend at baseline (SHA-1 verified, suite not re-run since frontend was untouched).

### Ambiguous — left in place, surfacing for Daniel review
Three Phase 2 v0.1-era scripts in `backend/scripts/` were left in place because their forward use is plausibly relevant to D.2 (job folder structure):
- `local_manifest.py` — Phase 2 v0.1 local-mode manifest generator (no S3 dependency). Could inform D.2 job-folder design.
- `upload_fixtures.py` — S3-compatible object-storage upload utility. Could be relevant to a future production-storage decision.
- `verify_fixtures.py` — paired with upload_fixtures.py.
- `backend/test_fixtures/bidsets.json` — manifest file possibly consumed by the above; left in place for safety.

Daniel may want to retire any of the above in a follow-up housekeeping session if he confirms they're not needed for D.2.

---

## Phase 3: Phase E — backend API + frontend consumption (TBD)

(Populated by Phase E session.)

---
