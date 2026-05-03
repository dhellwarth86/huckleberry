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

## Phase 3: Phase D.2 — Job folder + persistence build (2026-04-29)

**Branch:** `phase2-v0.3-D2-job-folder-and-persistence` (from housekeeping head `870d555`)
**Trigger:** Daniel directive 2026-04-29 — long-run chain (D.2 build → soft gate → three-bidset hard gate → canon update + push). Single chain, auto-continue between phases unless a §7 stop fires.
**Scope discipline:** New file `backend/core/job_storage.py` preferred over modifying `core/storage.py` (B.4 verbatim port). `dispatch_gate.run_dispatch` extension capped at ≤20 lines (actual: 8). No vault-ruled module touches. No frontend touches. CLAUDE.md not opened. SQLAlchemy not introduced — stdlib `sqlite3` only.

### Files created
- `backend/core/job_storage.py` (336 lines) — three SQLite tables (`jobs`, `dispatch_results`, `trade_outputs`) sharing `~/.tracepoint/cache.db` via `core.storage.DB_PATH`; lifecycle API + persistence + loading. See VALIDATION_LEDGER.md §A2 row for verification details.
- `backend/scripts/d2_silverleaf_reference.py` — tracked harness creating Silverleaf job + running `run_dispatch(storage="auto", job_id=...)`.
- `backend/scripts/d2_persistence_soft_gate.py` — tracked harness for 10 round-trip assertions.
- `backend/scripts/d2_three_bidset_hardgate.py` — tracked harness for 3 bidsets × 7 criteria.
- `backend/D2_REFERENCE_silverleaf.md` — Silverleaf reference run report (job_id `45d58c49-2e78-41d7-91c4-759a7a8de0de`, dispatch 137.6s, 338 roofing / 20+81+6 glazing — exact D.1 parity).
- `MARCH_ORDERS_D2_long_run.md` — chain spec (root-level).

### Files modified
- `backend/core/dispatch_gate.py`
  - +8 / −1 lines, all D.2 additions line-tagged `# D.2:`
  - Signature: added optional `job_id: str | None = None` parameter to `run_dispatch`.
  - After Stage 13 completes and before leak check: `if job_id is not None:` block lazy-imports `core.job_storage` and calls `persist_dispatch_result(job_id, ctx)` + `persist_trade_outputs(job_id, ctx)` + `mark_dispatch_complete(job_id)` inside try/except (failures append to `ctx.dispatch_warnings` rather than raise).
  - `job_id=None` path is unchanged from D.1 — entire D.2 block is gated.

### Files deleted
None.

### Commits
- D.2 commit 1 of 2: `38f849d` — "D.2 job persistence layer + Silverleaf reference run" (job_storage.py + dispatch_gate.py extension + 3 harness scripts + MARCH_ORDERS_D2_long_run.md + D2_REFERENCE_silverleaf.md).

### Pushes
(D.2 branch pushed at chain end — see Phase 4 below.)

### Dependency / config changes
None. `pyproject.toml` not modified. SQLite (already in via stdlib) is what `job_storage.py` uses.

### Vault-ruled files touched
None. SHA-1 verification at Checkpoint 1 (post-build, pre-soft-gate):
- `roofing_module.py`: `ae9e5b284191b45de419faacf11771da27a548f9`
- `glazing_module.py`: `52c014421915ec6a66b4a6860b71a0a3274920f2`
- `roofing_vocabulary.py`: `ec6c17f8955ef8e27c3ff1d552b299a6962c9d0b`
- `glazing_vocabulary.py`: `64249c8ef5f7d9db50added3c9a40836cba356ea`
- `debug_module.py`: `78f71d9030cde3b173389603f5f39bd6bedaac07`

### Frontend touched
None. SHA-1 verification at Checkpoint 1 (matches pre-chain):
- `Huckleberry_AI_6.3.1_Scope.html`: `a80463efe09a51e21c54635c34469fb64172f7b7`
- `Huckleberry_AI_6.3.2_Scope.html`: `09702119c7c299ae03c4b8f401c1a1a2c4db1626`
- `Huckleberry_AI_6.3.3_Scope.html`: `e8ba836c64df15277c9f8a36b7e28031f7b61f2a`
- `Huckleberry_AI_6.3.4_Scope.html`: `aaeddf686c8c74d79b2409d1b4fde1831b7f02c3`
- `Huckleberry_AI_6.3.5_Scope.html`: `cf3765d61fd6f17de46024a3a84c62f25b19b3c5`

### Sacred floor at Checkpoint 1
Backend 216 passed, 19 skipped, 0 failed. Frontend at baseline (vault-treated, suite not re-run since untouched).

---

## Phase 3.5: Phase D.2 — Soft gate (Silverleaf round-trip) (2026-04-29)

**Branch:** same (`phase2-v0.3-D2-job-folder-and-persistence`)
**Trigger:** auto-continued from Phase 3 after Checkpoint 1 PASS.
**Scope discipline:** Read-only against the persisted Silverleaf job; zero new code paths exercised in production beyond `get_job` / `load_dispatch_results` / `load_trade_outputs`; one harness fix (Unicode `≥` → `>=` in console-print strings to avoid cp1252 encode error on Windows; report content unaffected).

### Files created
- `backend/D2_SOFT_GATE_silverleaf.md` — soft gate report (Overall PASS, 10/10 assertions).

### Files modified
- `backend/scripts/d2_persistence_soft_gate.py` — single-character fix (`≥` → `>=`) in print string (line 90); report-content string already correct.

### Commits
(Folded into D.2 commit 2 of 2 at chain end.)

### Soft gate result
**10/10 PASS** against Silverleaf job_id `45d58c49-2e78-41d7-91c4-759a7a8de0de`:
1. `get_job` returns non-None
2. `name == "B2607 AEA Silverleaf"`
3. `gc == "Accelerated Construction Services"`
4. `trade_scope` contains both roofing + glazing
5. `dispatch_results` has 40 page entries (every page persisted)
6. 18 pages classified `schedule_sheet` (matches calibration iter 2 baseline)
7. ≥18 pages with `raw_tables_json` populated
8. `trade_outputs` has 40 page keys
9. Roofing fields aggregate == 338 (exact parity with D.1 hard gate + calibration iter 2)
10. Glazing items aggregate == 107 (20g + 81d + 6s — exact parity)

See `backend/D2_SOFT_GATE_silverleaf.md` for full evidence table.

### §7 stops fired
None.

---

## Phase 4: Phase D.2 — Three-bidset hard gate (2026-04-29)

**Branch:** same (`phase2-v0.3-D2-job-folder-and-persistence`)
**Trigger:** auto-continued from Phase 3.5 after soft gate PASS.
**Bidsets:** Bearss Ave Distribution Center, Shoppes at Avalon, Vine Street Retail Center (the same three real bidsets used in the 2026-04-28 three-bidset sweep).
**Scope discipline:** Per-bidset: `create_job` → `run_dispatch(storage="auto", job_id=...)` → `update_job_status("dispatched")` → 7-criterion evaluation (criteria 6+7 verified externally per harness convention). Module output thresholds set at 90% of the 2026-04-28 sweep baseline. One harness threshold typo corrected mid-chain (Bearss `glazing_items` 200 → 159; sweep baseline is 177, 90% floor is 159 — typo, not module regression).

### Files created
- `backend/D2_HARD_GATE_bearss-ave.md` — Bearss per-bidset gate report (7/7 PASS, 471.0s dispatch).
- `backend/D2_HARD_GATE_shoppes-at-avalon.md` — Shoppes per-bidset gate report (7/7 PASS, 721.8s dispatch).
- `backend/D2_HARD_GATE_vine-street.md` — Vine Street per-bidset gate report (7/7 PASS, 1194.5s dispatch).
- `backend/D2_HARD_GATE_three_bidset.md` — master hard gate report (Overall PASS, 21/21 criteria).
- `backend/D2_MASTER_GATE_REPORT.md` — chain-end master report covering all three phases (Phase A build, Phase B soft gate, Phase C hard gate) + sacred floor verification + chain wall-clock + job IDs.

### Files modified
- `backend/scripts/d2_three_bidset_hardgate.py` — Bearss `glazing_items` threshold 200 → 159 (typo fix; sweep baseline is 177, 90% floor 159; corrected before re-run).
- `PROJECT_CLAUDE.md` — §3 (D.2 paragraph appended), §7 (D.2 row updated to COMPLETE; E row updated to NEXT-eligible), §8 (rewrote next-planning-conversation around Phase E now being the only remaining path before Phase F).
- `VALIDATION_LEDGER.md` — §A2 (two new rows: `job_storage.py` build row, `dispatch_gate.py` D.2 extension row), §D (three new diagnostic rows: D.2 reference + D.2 soft gate + D.2 three-bidset hard gate + new "D.2 long-run chain headline numbers" subsection).
- `backend/BLOCK_RUN.md` — this file; Phases 3 / 3.5 / 4 added.

### Per-bidset hard gate results
| Bidset | Pages | Dispatch | Roofing fields | Glazing/Door/SF | Errors | Round-trip | Result |
|---|---:|---:|---:|---:|---:|---|---|
| Bearss Ave | 91 | 471.0s | 769 (sweep 769) | 177/31/24 (sweep 177/31/24) | 0/91 | exact | **7/7 PASS** |
| Shoppes at Avalon | 97 | 721.8s | 833 (sweep 830, +0.36%) | 43/22/22 (sweep 43/22/22) | 0/97 | exact | **7/7 PASS** |
| Vine Street | 138 | 1194.5s | 1201 (sweep 1201) | 100/12/23 (sweep 100/12/23) | 0/138 | exact | **7/7 PASS** |

Module-output byte-exact reproducibility on Bearss + Vine Street (different days, different sessions, harness-direct vs wired-dispatch). Shoppes within +0.36% on roofing fields, all other metrics exact.

### Job IDs persisted across the chain
- Silverleaf reference: `45d58c49-2e78-41d7-91c4-759a7a8de0de`
- Bearss (first run, threshold typo): `dd1fe72a-9ba9-46e4-8450-af22f695addd`
- Bearss (re-run with corrected threshold): `1efc6ea4-8a94-4b4c-9128-262fd1a0e2ae`
- Shoppes at Avalon: `725c44b8-1493-4ab6-b4a8-abd8507ac8d8`
- Vine Street: `fa4868da-dd5b-4679-893f-3a44d5047f12`

### Commits
- D.2 commit 2 of 2: gate reports (5 files) + canon updates (PROJECT_CLAUDE.md, VALIDATION_LEDGER.md, BLOCK_RUN.md) + harness threshold + Unicode fix. SHA recorded after commit lands.

### Pushes
- Branch `phase2-v0.3-D2-job-folder-and-persistence` pushed to origin at chain end.

### Dependency / config changes
None.

### Vault-ruled files touched
None. SHA-1 verification at chain end (matches pre-chain captured at Chain.0):
- `roofing_module.py`: `ae9e5b284191b45de419faacf11771da27a548f9`
- `glazing_module.py`: `52c014421915ec6a66b4a6860b71a0a3274920f2`
- `roofing_vocabulary.py`: `ec6c17f8955ef8e27c3ff1d552b299a6962c9d0b`
- `glazing_vocabulary.py`: `64249c8ef5f7d9db50added3c9a40836cba356ea`
- `debug_module.py`: `78f71d9030cde3b173389603f5f39bd6bedaac07`

### Frontend touched
None. SHA-1 verification at chain end (matches pre-chain):
- `Huckleberry_AI_6.3.1_Scope.html`: `a80463efe09a51e21c54635c34469fb64172f7b7`
- `Huckleberry_AI_6.3.2_Scope.html`: `09702119c7c299ae03c4b8f401c1a1a2c4db1626`
- `Huckleberry_AI_6.3.3_Scope.html`: `e8ba836c64df15277c9f8a36b7e28031f7b61f2a`
- `Huckleberry_AI_6.3.4_Scope.html`: `aaeddf686c8c74d79b2409d1b4fde1831b7f02c3`
- `Huckleberry_AI_6.3.5_Scope.html`: `cf3765d61fd6f17de46024a3a84c62f25b19b3c5`

### CLAUDE.md
Not opened, not edited, not referenced. (File retired by Daniel directive 2026-04-29 prior to D.1 session; remained retired throughout D.2.)

### Hard gate result
**Overall PASS — 21/21 criteria across 3 bidsets.** See `backend/D2_HARD_GATE_three_bidset.md` and `backend/D2_MASTER_GATE_REPORT.md`.

### §7 stops fired
None. The chain-spec stop conditions (sacred-floor regression, vault SHA-1 change, frontend SHA-1 change, dispatch raises, persistence round-trip fail, hard gate criterion fail) were monitored at every transition. Zero trips. One transient FAIL during first hard-gate run was a harness threshold typo on Bearss `glazing_items` (200 set; correct 90% floor is 159 since sweep baseline is 177); module output was byte-exact with sweep baseline so the FAIL was harness-not-data; threshold corrected and re-run produced 7/7 Bearss PASS.

### Sacred floor at chain end
Backend 216 passed, 19 skipped, 0 failed (verified pre-chain, at Checkpoint 1, and post-chain). Frontend at baseline (SHA-1 verified pre-chain and post-chain; suite not re-run since vault-treated).

---

## Phase 5: E.0 — API Design + Frontend Audit (2026-04-30)

**Branch:** `phase2-v0.3-E0-api-design-and-frontend-audit` (from D.2 head `cd5608e`)
**Trigger:** Daniel directive 2026-04-29 — Phase E next-eligible after D.2 chain ship; E broken into 4 sub-phases (E.0 design + audit, E.1 FastAPI scaffold, E.2 frontend strip, E.3 render + edit surface); E.0 is read-only, no code changes.
**Scope discipline:** Single short session, audit + design + housekeeping only, no production code, vault rule active, frontend strip deferred to E.2. Three deliverables: frontend audit, API design, v6.3.x housekeeping moves.

### Files created
- `backend/E0_FRONTEND_AUDIT.md` — v6.3.5 structural audit (8,694 lines audited; ~1,320 lines of backend-shaped logic identified; ~3,800–4,100 lines projected to be stripped in E.2) + E.2 strip targets prioritized + E.3 render targets sketched
- `backend/E0_API_DESIGN.md` — FastAPI design contract for E.1: stack decisions (FastAPI / uvicorn / Pydantic v2 / stdlib sqlite3), two E.1 endpoints (`POST /jobs` + `GET /jobs/{id}`) + free `/health` probe, request/response schemas, error shapes, project structure under `backend/api/`, three new pyproject deps E.1 will add, test strategy (test_api_jobs.py, 216 → 219–222), reserved E.2/E.3 endpoint sketches, forward-compat commitments
- `backend/E0_GATE_REPORT.md` — final gate report

### Files moved (git mv, history preserved)
- `frontend/Huckleberry_AI_6.3.1_Scope.html` → `safe_for_removal/frontend_versions/`
- `frontend/Huckleberry_AI_6.3.2_Scope.html` → `safe_for_removal/frontend_versions/`
- `frontend/Huckleberry_AI_6.3.3_Scope.html` → `safe_for_removal/frontend_versions/`
- `frontend/Huckleberry_AI_6.3.4_Scope.html` → `safe_for_removal/frontend_versions/`
- `frontend/spotcheck_durolast.js` → `safe_for_removal/frontend_versions/` (targeted v6.3.1; hardcoded HTML_PATH)
- `frontend/spotcheck_manufacturer.js` → `safe_for_removal/frontend_versions/` (targeted v6.3.2)
- `frontend/spotcheck_cricket.js` → `safe_for_removal/frontend_versions/` (targeted v6.3.3)
- `frontend/spotcheck_10b.js` → `safe_for_removal/frontend_versions/` (targeted v6.3.4)

### Files modified
- `safe_for_removal/MANIFEST.md` — appended `frontend_versions/` row to category table + 8 entry blocks (4 HTMLs + 4 spotchecks) per orders §6.3
- `PROJECT_CLAUDE.md` — single §3 paragraph append per orders §7 (E.0 audit + design complete note)
- `backend/BLOCK_RUN.md` — this file; Phase 5 section populated

### Files deleted
None this session.

### Commits
- E.0 single commit on `phase2-v0.3-E0-api-design-and-frontend-audit` (SHA recorded after commit)

### Pushes
- Branch pushed to origin at session end

### Dependency / config changes
**None this session.** E.0 adds zero deps. E.1 will add `fastapi>=0.115`, `uvicorn[standard]>=0.30`, `pydantic>=2.7` per the API design doc.

### Vault-ruled files touched
None. SHA-1 verification at session end (matches pre-session captured at E0.0):
- `roofing_module.py`: `ae9e5b284191b45de419faacf11771da27a548f9`
- `glazing_module.py`: `52c014421915ec6a66b4a6860b71a0a3274920f2`
- `roofing_vocabulary.py`: `ec6c17f8955ef8e27c3ff1d552b299a6962c9d0b`
- `glazing_vocabulary.py`: `64249c8ef5f7d9db50added3c9a40836cba356ea`
- `debug_module.py`: `78f71d9030cde3b173389603f5f39bd6bedaac07`

### Frontend touched
- `frontend/Huckleberry_AI_6.3.5_Scope.html`: read-only audit; SHA-1 `cf3765d61fd6f17de46024a3a84c62f25b19b3c5` unchanged at session end (verified before commit)
- `frontend/Huckleberry_AI_6.3.{1,2,3,4}_Scope.html`: moved (git rename); file content unchanged
- `frontend/spotcheck_{durolast,manufacturer,cricket,10b}.js`: moved (git rename); file content unchanged
- `frontend/run_tests.js`, `frontend/mutation_test_step11.js`, `frontend/extracted/Huckleberry_AI_6.3.0_Scope.html`, `frontend/package.json`: untouched (still in `frontend/`; `npm test` continues to pass 138/138 against v6.3.5)

### Soft observation
`frontend/package.json` still contains a `test:spotchecks` script that references the four moved spotcheck files. Running it now will fail (target files no longer at the referenced paths). The script entry was deliberately left intact — modifying production frontend config is out of scope for E.0 per orders §9 #7. The next frontend-touching session (likely E.2) will remove or repoint the entry. `npm test` (the 138/138 floor) is unaffected.

### CLAUDE.md
Not opened, not edited, not referenced. (File retired by Daniel directive 2026-04-29 prior to D.1 session; remains retired through E.0.)

### Sacred floor at session end
- Backend: 216 passed, 19 skipped, 0 failed (verified pre-session at E0.0 and post-moves at E0.4)
- Frontend: 138/138 passed against v6.3.5 (verified pre-session at E0.0 and post-moves at E0.4)
- v6.3.5 SHA-1 unchanged: `cf3765d61fd6f17de46024a3a84c62f25b19b3c5`
- All 5 vault-ruled module SHA-1s unchanged

### §9 stops fired
None. Each enumerated stop verified non-firing in `backend/E0_GATE_REPORT.md`.

---

## Phase 6: E.1 — FastAPI Scaffold + First Endpoints (2026-04-30)

**Branch:** `phase2-v0.3-E1-fastapi-scaffold` (from E.0 head `b5c8d95`)
**Trigger:** Daniel directive 2026-04-29 — E.1 ships FastAPI server with 2 real endpoints + 1 exempt health probe + 6 new tests; single-bidset Silverleaf hard gate (3-bidset deferred to post-Phase-G); soft gate to E.2 after Daniel review.
**Scope discipline:** Three deps (fastapi / uvicorn[standard] / pydantic — already declared in `backend/pyproject.toml` from v0.2 era; first wired in E.1, no pyproject change needed); permissive CORS in dev with `# E.1:` deferral comment; auth deferred to Postgres/security phase; OpenAPI docs exposed in dev; data-leak guards in response schema (Pydantic `extra="forbid"`) and error messages (generic strings only); strict input validation (`JobStatus = Literal[...]`); vault rule active; frontend untouched.

### Files created
- `backend/api/__init__.py` — package marker
- `backend/api/main.py` — FastAPI app, permissive CORS, `/health` probe, jobs router include, uvicorn entry
- `backend/api/routes/__init__.py`
- `backend/api/routes/jobs.py` — `POST /jobs` + `GET /jobs/{id}` calling `core.job_storage.create_job` / `get_job`
- `backend/api/schemas/__init__.py`
- `backend/api/schemas/jobs.py` — `JobCreateRequest` + `JobResponse` Pydantic v2 models with `Literal` status + `extra="forbid"` data-leak guard
- `backend/tests/conftest.py` — shared fixtures; `silverleaf_path` fixture skips when PDF unavailable
- `backend/tests/test_api_jobs.py` — 6 new tests per `MARCH_ORDERS_E_1_fastapi_scaffold.md §6`
- `backend/scripts/e1_silverleaf_api_hardgate.py` — tracked harness; 8 hard-gate checks via TestClient
- `backend/E1_HARD_GATE_silverleaf_api.md` — Silverleaf API hard gate report (8/8 PASS)
- `backend/E1_GATE_REPORT.md` — final gate report

### Files modified
- `PROJECT_CLAUDE.md` — §3 single E.1 paragraph append + §7 phase table updated (E split into E.0 / E.1 / E.2 / E.3; Phase G inserted; Postgres/security phase row added)
- `backend/BLOCK_RUN.md` — this file; Phase 6 section added (Phase 7 placeholder reserved for E.2)

### Files deleted
None.

### Commits
- E.1 single commit on `phase2-v0.3-E1-fastapi-scaffold` (SHA recorded after commit lands)

### Pushes
- Branch pushed to origin at session end

### Dependency / config changes
**No `pyproject.toml` modification** in E.1. The three deps (`fastapi>=0.115`, `uvicorn[standard]>=0.32`, `pydantic>=2.9`) were already declared in `backend/pyproject.toml` from the v0.2 era (with the comment "Web framework — included now so v0.2 doesn't need to re-add"). E.1 is the first phase to actually import + wire them. Versions in current Python environment: fastapi 0.135.3, uvicorn 0.43.0, pydantic 2.12.5 — all satisfy the spec's `>=0.115` / `>=0.30` / `>=2.7` minimums.

### Vault-ruled files touched
None. SHA-1 verification at session end (matches pre-session captured at E1.0):
- `roofing_module.py`: `ae9e5b284191b45de419faacf11771da27a548f9`
- `glazing_module.py`: `52c014421915ec6a66b4a6860b71a0a3274920f2`
- `roofing_vocabulary.py`: `ec6c17f8955ef8e27c3ff1d552b299a6962c9d0b`
- `glazing_vocabulary.py`: `64249c8ef5f7d9db50added3c9a40836cba356ea`
- `debug_module.py`: `78f71d9030cde3b173389603f5f39bd6bedaac07`

### Frontend touched
None. v6.3.5 SHA-1 unchanged: `cf3765d61fd6f17de46024a3a84c62f25b19b3c5`.

### CLAUDE.md
Not opened, not edited, not referenced. Retired pre-D.1; remains retired through E.1.

### Hard gate result
Silverleaf single-bidset API hard gate via `backend/scripts/e1_silverleaf_api_hardgate.py`: **8/8 PASS**. TestClient init OK; POST /jobs 201 with 14-field JobResponse (33.7ms latency); GET /jobs/{id} 200 with id-match; direct `core.job_storage.get_job` round-trip confirms persistence (job id `c71dcdaa-b041-4cab-af41-337b9ce73448` written to `~/.tracepoint/cache.db`); `created_at` within 60s of now; `pdf_sha1` `76dc89072dae77c1b476b60da85870f3d799cd31` matches actual file SHA-1 exactly; invalid status returns 422 (Pydantic Literal enforced); non-existent id returns 404 with `{"detail": "Job not found"}` (data-leak guard — no SQL/path/traceback markers in error body). See `backend/E1_HARD_GATE_silverleaf_api.md`.

### §10 stops fired
None. Each enumerated stop verified non-firing in `backend/E1_GATE_REPORT.md`.

### Sacred floor at session end
- Backend: 222 passed, 19 skipped, 0 failed (verified pre-session at 216/19/0 and post-session at 222/19/0; the +6 are E.1's new tests)
- Frontend: 138/138 passed against v6.3.5 (vault-treated, untouched)
- v6.3.5 SHA-1 unchanged: `cf3765d61fd6f17de46024a3a84c62f25b19b3c5`
- All 5 vault-ruled module SHA-1s unchanged

---

## Phase 6.5: E.1 discipline patches — uvicorn smoke + spec corrigenda (2026-04-30)

**Branch:** `phase2-v0.3-E1-discipline-patches` (from E.1 head `6eb99fe`)
**Trigger:** Daniel directive 2026-04-30 — three small follow-ups before E.2 launches: (1) verify the production run-mode (real uvicorn over real HTTP, not just TestClient) actually works; (2) reconcile the `E0_API_DESIGN.md` 404 body with what shipped; (3) reconcile the `version=` string with what shipped. Single commit, single short session.
**Scope discipline:** No production code modified. No test changes. No new deps. Vault rule active. Frontend untouched. Three deliverables: a tracked uvicorn-smoke harness, a smoke report, two spec corrigenda inside the existing E0_API_DESIGN.md (no new top-level files for the corrigenda).

### Files created
- `backend/scripts/e1_uvicorn_smoke.py` — tracked harness; spawns uvicorn via `subprocess.Popen` against `api.main:app`, polls `/health` until ready, hits the four assertions over real HTTP via `requests`, terminates the subprocess in a `finally` block. ~250 lines.
- `backend/E1_UVICORN_SMOKE.md` — smoke report (4/4 PASS); per-assertion evidence + response-body excerpts + total wall-clock.

### Files modified
- `backend/E0_API_DESIGN.md` — two corrigenda landed:
  - §5.2 error-table row + implementation sketch: `{"detail": "job not found: <job_id>"}` → `{"detail": "Job not found"}` (no echo of user input)
  - §5.4 main.py skeleton: `version="0.1.0"` → `version="0.3.0-E.1"`
  - new §5.12 "Corrigenda — landed during E.1" section appended before doc close, documenting both patches with reasons + the version-string convention adopted (`<phase2-version>-<phase-stage>`)
- `backend/BLOCK_RUN.md` — this Phase 6.5 section appended; Phase 7 placeholder for E.2 retained below.

### Files deleted
None.

### Commits
- Single discipline-patches commit on `phase2-v0.3-E1-discipline-patches` (SHA recorded after commit lands).

### Pushes
- Branch pushed to origin at session end.

### Dependency / config changes
None. `requests` (used by the smoke harness) is a transitive dep already present (FastAPI's TestClient pulls in httpx; `requests` was already on PYTHONPATH from earlier setup — verified via `python -c "import requests"` returning 2.33.1). `pyproject.toml` unchanged this session.

### Vault-ruled files touched
None. SHA-1 verification at session end (matches pre-session captured before the patches):
- `roofing_module.py`: `ae9e5b284191b45de419faacf11771da27a548f9`
- `glazing_module.py`: `52c014421915ec6a66b4a6860b71a0a3274920f2`
- `roofing_vocabulary.py`: `ec6c17f8955ef8e27c3ff1d552b299a6962c9d0b`
- `glazing_vocabulary.py`: `64249c8ef5f7d9db50added3c9a40836cba356ea`
- `debug_module.py`: `78f71d9030cde3b173389603f5f39bd6bedaac07`

### Frontend touched
None. v6.3.5 SHA-1 unchanged: `cf3765d61fd6f17de46024a3a84c62f25b19b3c5`.

### CLAUDE.md
Not opened. Retired pre-D.1.

### Smoke gate result
**4/4 PASS over real HTTP.** uvicorn boot 1.1s; total smoke 1.2s.
1. `GET /health` → 200 + `{"status":"ok","version":"0.3.0-E.1"}`
2. `GET /docs` → 200 (Swagger UI HTML, 1013 bytes, contains "swagger" substring)
3. `POST /jobs` (Silverleaf payload) → 201 + 14-field JobResponse, id `98bd2e75-0458-41f8-865b-a4b8304c163b`
4. `GET /jobs/{id}` → 200, id-match + name-match

This is the production run-mode (uvicorn over a real socket) confirming what the in-process TestClient suite (E.1's 6 tests + the Silverleaf API hard gate's 8 checks) already proved at the in-process layer. Both layers now agree on the contract.

### Sacred floor at session end
- Backend: 222 passed, 19 skipped, 0 failed (no test changes this session — floor inherited from E.1 ship)
- Frontend: 138/138 passed against v6.3.5 (vault-treated, untouched)
- v6.3.5 SHA-1 unchanged
- All 5 vault-ruled module SHA-1s unchanged
- `pyproject.toml` unchanged

### §7 stops fired
None. Smoke 4/4 PASS; no other stop conditions triggered. (The single stop condition in this session's spec was "if any assertion fails, §7 stop with traceback + response body for diagnosis" — non-firing.)

---

## Phase 7: E.2.0 — Frontend strip-and-connect read-only diagnostic (2026-04-30)

**Branch:** `phase2-v0.3-E2-0-strip-plan` (from `29d2ef8`)
**Trigger:** Daniel directive 2026-04-30 — MARCH ORDERS Phase E.2.0: produce design deliverables specifying E.2.1 through E.2.hard-gate. Read-only: zero code changes, zero test changes, zero dependency changes.

### Files created
- `backend/E2_0_STRIP_PLAN.md` — D1: line-by-line strip plan for v6.3.5 (14 strip targets S1–S14, planSet shape analysis, 5 gaps, 5 risks)
- `backend/E2_0_NEW_FILE_DESIGN.md` — D2: structural skeleton of `frontend/src/Huckleberry_AI_phase2.v1.0.0.html` (7-tab layout, status bar spec, script ordering)
- `backend/E2_0_API_CLIENT_SPEC.md` — D3: `apiClient` wrapper spec (3 real methods, 3 stubs, `apiCall` helper, error matrix)
- `backend/E2_0_TEST_FLOOR_PROPOSAL.md` — D4: test floor proposal (138 → 25, with honest gap documentation)
- `backend/E2_0_GATE_REPORT.md` — gate report for E.2.0

### Files modified
- `PROJECT_CLAUDE.md` — §3 paragraph appended (E.2.0 summary), §7 phase table updated (E.2 row split into E.2.0/E.2.1/E.2.2/E.2.debug/E.2.hard-gate)
- `backend/BLOCK_RUN.md` — this Phase 7 section

### Files deleted
None.

### Config / dependency changes
None.

### Commits
Single commit on `phase2-v0.3-E2-0-strip-plan`.

### Vault-ruled modules
Unchanged. SHA-1s verified at pre-flight:
- `roofing_module.py`: `ae9e5b284191b45de419faacf11771da27a548f9`
- `roofing_vocabulary.py`: `ec6c17f8955ef8e27c3ff1d552b299a6962c9d0b`
- `glazing_module.py`: `52c014421915ec6a66b4a6860b71a0a3274920f2`
- `glazing_vocabulary.py`: `64249c8ef5f7d9db50added3c9a40836cba356ea`
- `debug_module.py`: `78f71d9030cde3b173389603f5f39bd6bedaac07`

### Frontend touched
None. v6.3.5 SHA-1 unchanged: `cf3765d61fd6f17de46024a3a84c62f25b19b3c5`. Read-only analysis only.

### Sacred floor at session end
- Backend: 222 passed, 19 skipped, 0 failed (no test changes — read-only phase)
- Frontend: 138/138 passed against v6.3.5 (untouched)
- v6.3.5 SHA-1 unchanged
- All 5 vault-ruled module SHA-1s unchanged
- `pyproject.toml` unchanged

### §7 stops fired
None. Read-only diagnostic — no stop conditions applicable.

### Key design decisions documented

1. **planSet is a rendering-only cache after E.2.1** — `paths`, `texts`, `zones` fields absent; business data comes from API (D1 §4)
2. **7-tab layout** — Pipeline tab removed, tabs renumber 0–6 (D2 §2.4)
3. **3-state status bar** — CHECKING/CONNECTED/UNREACHABLE with 30s polling interval (D2 §5)
4. **Browser-native `fetch()` API client** — no axios, no npm deps, `apiCall` helper with AbortController timeout (D3 §2)
5. **Frontend test floor drops from 138 → 25** — ~142 tests retire with stripped code; 11 survive + 14 new proposed (D4 §4)

---

## Phase 8: E.2.1 — Frontend strip + new file + v6.3.5 archival (2026-04-30)

**Branch:** `phase2-v0.3-E2-1-strip` (from `a1c804c`)
**Trigger:** MARCH ORDERS Phase E.2.1 — destructive sub-phase executing E.2.0 strip plan + new file design.

### Files created
- `frontend/src/Huckleberry_AI_phase2.v1.0.0.html` — 3,672 lines, built bottom-up from E.2.0 specs (D1 strip plan + D2 new file design + D3 apiClient spec + D4 test floor proposal)
- `backend/E2_1_GATE_REPORT.md` — gate report

### Files modified
- `frontend/package.json` — `test` script repointed to `src/Huckleberry_AI_phase2.v1.0.0.html`; obsolete `test:spotchecks` / `test:mutations` / `test:all-versions` entries removed (per E.2.1 §7.1); `version` bumped to `phase2.v1.0.0`; `dependencies` unchanged
- `backend/E0_API_DESIGN.md` — §5.12 corrigendum 3 (CHECKING vs DEGRADED) appended
- `PROJECT_CLAUDE.md` — §3 paragraph appended; §7 phase table E.2.1 row marked COMPLETE; E.2.2 row promoted to NEXT-eligible
- `backend/BLOCK_RUN.md` — this Phase 8 section
- `safe_for_removal/MANIFEST.md` — v6.3.5 row added

### Files renamed (via `git mv`, content unchanged)
- `frontend/Huckleberry_AI_6.3.5_Scope.html` → `safe_for_removal/frontend_versions/Huckleberry_AI_6.3.5_Scope.html` (content SHA-1 `cf3765d61fd6f17de46024a3a84c62f25b19b3c5` preserved)

### Files deleted
None. v6.3.5 moved, not deleted, per discipline rule.

### Config / dependency changes
None. `package.json` dependencies unchanged. `pyproject.toml` untouched. No new npm packages. No new Python packages.

### Commits
Single commit on `phase2-v0.3-E2-1-strip`.

### Vault-ruled modules
Unchanged. SHA-1 verification at session end (matches pre-session captured at E2.1.0):
- `roofing_module.py`: `ae9e5b284191b45de419faacf11771da27a548f9`
- `glazing_module.py`: `52c014421915ec6a66b4a6860b71a0a3274920f2`
- `roofing_vocabulary.py`: `ec6c17f8955ef8e27c3ff1d552b299a6962c9d0b`
- `glazing_vocabulary.py`: `64249c8ef5f7d9db50added3c9a40836cba356ea`
- `debug_module.py`: `78f71d9030cde3b173389603f5f39bd6bedaac07`

### E.1 production-code SHA-1s (per §3 stop #4)
Unchanged. SHA-1 verification at session end (matches pre-session):
- `backend/api/main.py`: `5572ebe5a41dabc6bd96a9819bb410dde7e5fc4b`
- `backend/api/routes/jobs.py`: `bfa86e9e5b23d0634ee54ae72f89f048345b2ef9`
- `backend/api/schemas/jobs.py`: `12ec441dc5935f06269b2e2df07eec5ec1fb7fc1`

### Frontend touched
- v6.3.5 moved (content unchanged): `cf3765d61fd6f17de46024a3a84c62f25b19b3c5` → same SHA-1 at archived path.
- New file created: `frontend/src/Huckleberry_AI_phase2.v1.0.0.html` (3,672 lines).

### CLAUDE.md
Not opened. Retired pre-D.1 — confirmed not touched in this session.

### Sacred floor at session end
- Backend: 222 passed, 19 skipped, 0 failed (no backend code touched — verified pre and post)
- Frontend: 20/20 passed, 0 failed against `frontend/src/Huckleberry_AI_phase2.v1.0.0.html` (138/138 floor against v6.3.5 retired permanently per §0)
- v6.3.5 SHA-1 unchanged through `git mv`
- All 5 vault-ruled module SHA-1s unchanged
- All 3 E.1 production-code SHA-1s unchanged
- `pyproject.toml` unchanged
- `package.json` `dependencies` unchanged (only `test` script field updated)

### §13 stops fired
None. All 17 stop conditions in MARCH_ORDERS_E_2_1_strip.md §13 confirmed non-firing at gate time.

### Test composition (20/20)
- 11 surviving TOOL_TESTS (parseFeetInches × 5, polygonAreaPt × 2, polygonPerimeterPt × 1, bboxOfPoints × 1, calibrate math × 1, measure math × 1)
- 3 status-bar tests (setHealthState DOM update, 3-state cycle, unreachable retry handler)
- 4 takeoff tests with hardcoded scope fixtures (empty annotations, areas-produce-derived-SF, default 10% waste, override waste)
- 2 stub correctness tests (extractScope and classifyPage return `_stub: true` markers)
- 0 integration tests (5 API smoke tests deferred to E.2.2)

### Key design decisions landed
1. **planSet as rendering cache, not data model** — architectural reframing per D1 §4.5; `paths`/`texts`/`zones`/`expected` fields absent from new planSet shape.
2. **Tab indices renumbered** — Pipeline tab removed; TESTS now tab 5 (was 6); ABOUT now tab 6 (was 7); all `showTab(N)` calls validated.
3. **CHECKING replaces DEGRADED** — corrigendum 3 to E0_API_DESIGN.md §5.12; canonical 3 states are CHECKING / CONNECTED / UNREACHABLE.
4. **healthCheck is the only real apiClient method in E.2.1** — createJob / getJob / listJobs / getResults / dispatchJob throw `not_implemented_in_e2_1` per D3 §4.
5. **Inlined per D1 §4.4 gap resolution** — `polygonArea` (shoelace), `DEFAULT_WASTE_FACTOR = 0.10` (was `ROOFING_CONSTANTS.wasteFactor` from stripped ROOF_VOCAB region).
6. **No `node_modules` / build step** — single-file HTML preserved; CDN imports only; vanilla `fetch()` for API client.

---

## Phase 9: E.2.2 — Frontend connect + hard gate (COMPLETE 2026-05-01)

**Backend changes:**
- Added `"dispatching"` to `_VALID_STATUSES` (`core/job_storage.py`) and `JobStatus` Literal (`api/schemas/jobs.py`)
- `POST /jobs/{id}/dispatch` — synchronous dispatch endpoint: `draft→dispatching→dispatched` lifecycle, idempotent on re-call, 400 if PDF deleted, 500 with rollback on failure
- `GET /jobs/{id}/results` — returns `JobResultsResponse` with string-keyed `dispatch_results` + `trade_outputs` dicts, 409 if not yet dispatched
- `JobResultsResponse` model (`extra="forbid"`)
- 8 new tests (tests 7–14): dispatch happy/404/idempotent/400-pdf-missing, results 200/404/409/string-keys
- `small_pdf_path` fixture in `conftest.py` (minimal 1-page PDF, dispatch <5s)

**Frontend changes:**
- 4 `apiClient` methods wired: `createJob`, `getJob`, `dispatchJob` (240s timeout), `getResults`
- `extractScope` + `classifyPage` stubs removed
- `populateScopeFromResults` + `populatePagesFromResults` consume API data for Scope/Pages tabs
- RUN DISPATCH button + `runDispatchFlow()` async orchestrator
- Step 1.5 "SERVER FILE PATH" input card
- Network-error → `probeHealth()` re-evaluation
- 5 API smoke tests added (SKIP convention), 2 stub tests retired → floor 20 → 23

**Debug verification:**
- `scripts/e2_2_debug_silverleaf.py` — in-process dispatch (no HTTP), writes `E2_2_DEBUG_silverleaf.md`
- Comparison vs D.2 calibration baseline: 5/5 checks PASS (page count 40==40, roofing 338 ±5%, glazing 107 ±5%, ROOF_PLAN present, no ERROR markers)
- Dispatch wall-clock: 147.7s

**Sacred floors:** backend 222 → 230/19/0; frontend 20 → 23/23; vault SHA-1s unchanged; no new deps.

---

## Phase 10: E.3 — Render API-fed data + edit surface (RESERVED, NOT STARTED)

(Populated by E.3 session. Per-page roofing/glazing display; debug summary; job list/dashboard; status transitions; annotation save/load via new annotations table.)

---

## Phase 11: G.2 — Corpus-wide classifier upgrade (2026-05-03)

**Branch:** `phase2-v0.3-G2-classifier-upgrade` (from `dec0af5`)
**Trigger:** MARCH ORDERS Phase G.2 — rescoped from discipline fallback after corpus scout invalidated the original premise.

### Files created
- `backend/scripts/g2_classifier_hardgate.py` — 4-bidset hard gate harness
- `backend/G_2_HARD_GATE_REPORT.md` — hard gate report (PASS)

### Files modified
- `backend/core/dispatch_gate.py` — `_classify_page_type` reads `pc.title`; `_PAGE_TYPE_RULES` extended (FLOOR_PLAN, SCHEDULE_SHEET, FRAMING_PLAN, DETAIL_SHEET, GENERAL_NOTES, MEP_PLAN)
- `backend/tests/test_dispatch.py` — 7 new classifier tests
- `CHECKLIST.md` — Phase G.2 row + handoff
- `ITINERARY.md` — Section 1 + 2 updated
- `PROJECT_CLAUDE.md` — sacred floor 230→237, active phase block updated

### Files deleted / renamed
None.

### Commits
- Code change: `170fcd7`
- Canon updates: (this commit)

### Vault-ruled files touched
None outside `dispatch_gate.py` (which is integration-frozen + allowed in dedicated tuning phases per PROJECT_CLAUDE.md vault rule). SHA-1 verification at session end:
- `roofing_module.py`: ae9e5b28... (unchanged)
- `glazing_module.py`: 52c01442... (unchanged)
- `roofing_vocabulary.py`: ec6c17f8... (unchanged)
- `glazing_vocabulary.py`: 64249c8e... (unchanged)
- `debug_module.py`: 78f71d90... (unchanged)
- `dispatch_gate.py`: 2a708d19 → 09bc0340 (expected change)

### Hard gate result
4/4 PASS per `backend/G_2_HARD_GATE_REPORT.md`. Bearss byte-equivalent (769/177/31/24). Hampshire 4→0. Chipotle Tarpon 3→0. Shoppes Avalon 2→0.

### Sacred floor at session end
Backend 237/19/0; frontend 23/23 (untouched).

---

## Phase 12: G.3 — Single-pass-per-page extraction (2026-05-03)

**Branch:** `phase2-v0.3-G3-single-pass-extraction` (from `e7a3884`, the G.2 canon-update head)
**Trigger:** MARCH ORDERS Phase G.3 — restore TracePoint paper §2.1 architecture (Layer 1 extracts once, Layers 2-4 consume cache). Absorbs F12 (Phase G.4) scope.

### Files created
- `backend/G_3_GATE_REPORT.md` — gate report

### Files modified
- `backend/core/pdf_engine.py` — `PDFEngine._extract_cache: dict` keyed `(id(doc), page_num, method_name)`; `extract_text` and `extract_text_blocks` consult cache before extracting; `engine.close(doc)` purges entries for that doc's id before closing fitz doc
- `backend/core/dispatch_gate.py` — `run_filter_4` opens pdfplumber once per dispatch in a `try`/`finally`; `_parse_tables_on_page` accepts an open `pdf` Document instead of a path; `_run_trade_modules` replaces `pdf_page.extract_words()` with cached `engine.extract_text_blocks(doc, page_idx)` for `TradeModuleInput.interior_text_blocks` (pdfplumber `extract_tables()` fallback for non-schedule pages preserved)
- `backend/tests/test_pdf_engine.py` — new `TestPDFEngineCache` class: 5 cache unit tests (`test_cache_returns_same_object_on_repeat_call`, `test_cache_separates_pages`, `test_cache_separates_text_and_blocks`, `test_cache_invalidates_on_doc_close`, `test_cache_separates_documents`) + `two_page_pdf` fixture
- `CHECKLIST.md` — F11 row signed (Developer, 2026-05-03); F12 marked absorbed; new Handoff entry
- `ITINERARY.md` — Section 1 (Last 1-2-3 promoted: G.3 → Last-1, G.2 → Last-2, recon-cascade-map → Last-3); Section 2 (G.5 promoted to Next-1; closing hard gate to Next-2; Silverleaf Filter 1 fix to Next-3; auto-notation to Next-4; TBD slots at Next-5 / Next-6); sacred-floor reminder 237 → 242
- `PROJECT_CLAUDE.md` — Phase G.3 session bullet added (Section 3); G.3 row added to Phases table (Section 7)

### Files deleted / renamed
None.

### Commits
- Code+tests+report: `e51c785`
- Canon updates: (this commit)

### Vault-ruled files touched
Only `dispatch_gate.py` and `pdf_engine.py` modified (the two files this phase scopes). SHA-1 verification at session end:
- `roofing_module.py`: ae9e5b28... (unchanged)
- `glazing_module.py`: 52c01442... (unchanged)
- `roofing_vocabulary.py`: ec6c17f8... (unchanged)
- `glazing_vocabulary.py`: 64249c8e... (unchanged)
- `debug_module.py`: 78f71d90... (unchanged)
- `dispatch_gate.py`: 09bc0340 → 8b39fd0e (expected change)
- `pdf_engine.py`: e872f69e → daf06dd2 (expected change)

### Hard gate result
PASS per `backend/G_3_GATE_REPORT.md`. Chipotle Tarpon dispatch completes successfully; page count 39 = 39 (pre- vs post-patch); single dispatch warning byte-identical (`Filter 4 quality gate: 21 of 53 legends removed (32 kept)`); zero new warnings, zero new errors, zero STOPs.

### Wall-clock (recorded but not a gate criterion — Daniel is the wall clock)
Chipotle Tarpon (39 pages): warm 58.72s → 50.05s (−14.8%). Cold 58.36s → 50.26s.

### Sacred floor at session end
Backend 242/19/0 (was 237 — +5 cache unit tests); frontend 23/23 (untouched).

---
