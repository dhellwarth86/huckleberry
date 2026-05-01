# safe_for_removal/ MANIFEST

**Generated:** 2026-04-29 by housekeeping session per `MARCH_ORDERS_housekeeping_safe_for_removal.md`
**Branch when generated:** `phase2-v0.3-housekeeping-safe-for-removal` (from D.1 head `b478456`)

**How to read this file:** each entry below describes one file or directory that was moved into `safe_for_removal/` at the date above. Each entry names what the artifact was, when it was active, why it's being retired, what (if anything) replaced it, and what to look at if you encounter related issues. After Daniel reviews `safe_for_removal/` and confirms nothing critical lives in it, the folder gets deleted in a future session — but **this MANIFEST.md is preserved** (copied out before deletion, probably to `backend/RETIRED_FILES_WIKI.md`) and converted into a wiki. **Write entries for someone debugging in 2027 who has only this file as context.**

---

## Categories

The folder is organized into one subdirectory per category:

| Subdirectory | What it holds |
|---|---|
| `march_orders/` | Completed march orders for shipped phases (calibration, profile/housekeeping, three-bidset sweep). One copy per phase, git-history-preserved via `git mv`. |
| `previous_handoff/contents/` | Daniel's pre-session archive of older handoff documents and the retired CLAUDE.md. |
| `previous_orders/contents/` | Daniel's pre-session archive of every completed phase's march orders (B.1, B.2/B.3, B.4, C.1, C.2, C.3b, C.3c-build, C.5, D8 follow-up, calibration, page-type-verification, profile-and-housekeeping, three-bidset sweep, STEP_17/STEP_18). |
| `anomalous_nested_repo_huckleberry/repo_root` | The empty nested git repo found at workspace root in the profile-and-housekeeping session. Has its own `.git/` directory. Contents: just a `.gitattributes`. Tracked here as a gitlink (embedded git repo), not as content. |
| `intake_diagnostic_outputs/` | All Pass 1 + Pass 2 intake-diagnostic outputs (CSVs + summary JSONs) plus the two scripts (`intake_diagnostic.py`, `intake_diagnostic_pass2.py`) plus the two markdown reports (`INTAKE_DIAGNOSTIC.md`, `INTAKE_DIAGNOSTIC_PASS2.md`). VALIDATION_LEDGER.md §I forbids re-running these. |
| `pre_phase_B_validation/` | Pre-Phase-B experiment infrastructure: `EXPERIMENT_*.md` reports, the v0.1 experiment runner + analyzer + helpers, the v0.2-era sweep scripts, the v0.2 validation report, the public-corpus observations, the TracePoint discovery doc. All superseded by VALIDATION_LEDGER.md and the per-phase gate reports. |
| `superseded_scripts/` | One-shot harnesses superseded by tracked reusable harnesses: `c5_run_through.py` (replaced by sweep + calibration patterns), `sweep_three_bidsets.py` (was intentionally untracked but did get committed; superseded by `calibrate_silverleaf.py` and `d1_silverleaf_hardgate.py` patterns). |
| `old_terminal_logs/` | Old captured terminal output: `v0.2_sweep.log` from the v0.2 ship sweep session. |
| `frontend_versions/` | Retired frontend HTML iterations (v6.3.1, v6.3.2, v6.3.3, v6.3.4) plus their version-specific spotcheck scripts (`spotcheck_durolast.js` → 6.3.1, `spotcheck_manufacturer.js` → 6.3.2, `spotcheck_cricket.js` → 6.3.3, `spotcheck_10b.js` → 6.3.4). Retired by E.0 2026-04-30; v6.3.5 confirmed canonical. |

---

## Entries

### MARCH_ORDERS_calibration_silverleaf.md

**Original path:** `MARCH_ORDERS_calibration_silverleaf.md` (workspace root)
**New path:** `safe_for_removal/march_orders/MARCH_ORDERS_calibration_silverleaf.md`
**Category:** completed_march_orders
**When active:** 2026-04-29 (calibration session)
**Purpose when active:** Drove the iterative dispatch-side calibration of B2607 AEA Silverleaf — Bug 1 (page-type ordering) + Bug 3 (tables plumbing) fixes across two iterations on `phase2-v0.3-calibration-silverleaf` branch.
**Why retired:** Phase shipped (commit `2c56913`). Gate report `backend/CALIBRATION_GATE_REPORT_silverleaf.md` is the persistent receipt; the orders themselves are historical.
**What replaced it (if anything):** Nothing — orders are write-once-and-ship; the gate report supersedes them as the active artifact.
**What to look at if related issues surface:** `backend/CALIBRATION_GATE_REPORT_silverleaf.md` (final gate report), `backend/CALIBRATION_RUN_silverleaf_iter_{0,1,2}.md` (per-iteration reports), `backend/scripts/calibrate_silverleaf.py` (tracked harness — still active for any future per-bidset calibration work).

---

### MARCH_ORDERS_profile_and_housekeeping.md

**Original path:** `MARCH_ORDERS_profile_and_housekeeping.md` (workspace root)
**New path:** `safe_for_removal/march_orders/MARCH_ORDERS_profile_and_housekeeping.md`
**Category:** completed_march_orders
**When active:** 2026-04-29 (profile-and-housekeeping session)
**Purpose when active:** Drove the Bearss Ave profile diagnostic + branch push housekeeping bundle on `phase2-v0.3-profile-and-housekeeping` branch.
**Why retired:** Phase shipped (commits `112bca7` profile + `963f0c5` housekeeping). The receipts persist; the orders are historical.
**What replaced it (if anything):** Nothing.
**What to look at if related issues surface:** `backend/PROFILE_DIAGNOSTIC_bearss-ave.md` (profile receipts), `backend/scripts/profile_diagnostic.py` (tracked reusable harness), VALIDATION_LEDGER.md §D (Bearss Ave profile headline numbers).

---

### MARCH_ORDERS_three_bidset_sweep.md

**Original path:** `MARCH_ORDERS_three_bidset_sweep.md` (workspace root)
**New path:** `safe_for_removal/march_orders/MARCH_ORDERS_three_bidset_sweep.md`
**Category:** completed_march_orders
**When active:** 2026-04-28 (three-bidset sweep session)
**Purpose when active:** Drove the descriptive observation sweep against Shoppes-at-Avalon, Vine Street, Bearss Ave on `phase2-v0.3-sweep-three-bidsets` branch. Modules vault-ruled and untouched throughout.
**Why retired:** Phase shipped (commit `cf107dd`). Three observation reports persist; orders are historical.
**What replaced it (if anything):** Nothing.
**What to look at if related issues surface:** `backend/SWEEP_OBSERVATION_shoppes-at-avalon.md`, `backend/SWEEP_OBSERVATION_vine-street.md`, `backend/SWEEP_OBSERVATION_bearss-ave.md` (active reports). VALIDATION_LEDGER.md §D documents headline numbers. The sweep harness `sweep_three_bidsets.py` is in `safe_for_removal/superseded_scripts/`.

---

### previous_handoff/contents/CLAUDE.md (Daniel's archive copy)

**Original path:** `previous handoff/CLAUDE.md` (Daniel's pre-session archive directory, untracked)
**New path:** `safe_for_removal/previous_handoff/contents/CLAUDE.md`
**Category:** archived_canon
**When active:** Through 2026-04-28 (multiple sessions). Retired by Daniel directive 2026-04-29.
**Purpose when active:** Single source of truth for Phase 2 canon: project identity, canonical workflow, 18 ratified Phase 2 architectural decisions (including Decision 15 vault rule), phased recovery path A–F, hard guardrails. Sessions through 2026-04-28 read this first; D.1 onwards do not open it (substantive content has migrated to PROJECT_CLAUDE.md and VALIDATION_LEDGER.md).
**Why retired:** Daniel directive 2026-04-29 — replaced as canonical entry point by PROJECT_CLAUDE.md (which references VALIDATION_LEDGER.md as the empirical receipts). The retirement avoids the canonical-doc-confusion failure mode where two large docs partially repeat each other.
**What replaced it (if anything):** PROJECT_CLAUDE.md (entry point + section-by-section canonical state) and VALIDATION_LEDGER.md (empirical receipts and decisions).
**What to look at if related issues surface:** PROJECT_CLAUDE.md §3 (where the project stands), §4 (discipline), §6 (common misconceptions), §7 (phased recovery table). VALIDATION_LEDGER.md §G (vault-ruled list — the original Decision 15 content), §H (decisions including the SQLite-stays-Postgres-deferred call). NOTE: an additional unstaged deletion of `CLAUDE.md` at workspace root is Daniel's separate retirement movement; that's not part of this housekeeping session and is not staged in this commit.

---

### previous_handoff/contents/HANDOFF_2026-04-26.md

**Original path:** `previous handoff/HANDOFF_2026-04-26.md` (Daniel's pre-session archive, was tracked there)
**New path:** `safe_for_removal/previous_handoff/contents/HANDOFF_2026-04-26.md`
**Category:** completed_handoffs
**When active:** 2026-04-26 (architectural realignment session)
**Purpose when active:** Narrative state of the project at the end of the architectural-realignment session (the session that produced CLAUDE.md §4).
**Why retired:** Superseded by `HANDOFF_FINAL_2026-04-28.md` (the latest handoff, kept active in workspace root).
**What replaced it:** `HANDOFF_FINAL_2026-04-28.md`.
**What to look at if related issues surface:** Active `HANDOFF_FINAL_2026-04-28.md` and PROJECT_CLAUDE.md §3.

---

### previous_handoff/contents/HANDOFF_FINAL_2026-04-27.md

**Original path:** `previous handoff/HANDOFF_FINAL_2026-04-27.md` (Daniel's pre-session archive, was tracked there)
**New path:** `safe_for_removal/previous_handoff/contents/HANDOFF_FINAL_2026-04-27.md`
**Category:** completed_handoffs
**When active:** 2026-04-27 (Phase B ship day)
**Purpose when active:** State narrative at the end of the day Phase B (B.1–B.4) shipped — the day the full TracePoint pipeline port completed.
**Why retired:** Superseded by `HANDOFF_FINAL_2026-04-28.md`.
**What replaced it:** `HANDOFF_FINAL_2026-04-28.md`.
**What to look at if related issues surface:** Active `HANDOFF_FINAL_2026-04-28.md`. For Phase B-specific receipts, VALIDATION_LEDGER.md §A.

---

### previous_handoff/contents/HANDOFF_v3_2026-04-27.md

**Original path:** `previous handoff/HANDOFF_v3_2026-04-27.md` (Daniel's pre-session archive, was tracked there)
**New path:** `safe_for_removal/previous_handoff/contents/HANDOFF_v3_2026-04-27.md`
**Category:** completed_handoffs
**When active:** 2026-04-27 (revision of same-day handoff)
**Purpose when active:** Updated narrative at the end of the same Phase B day, capturing late-day decisions.
**Why retired:** Superseded by `HANDOFF_FINAL_2026-04-28.md`.
**What replaced it:** `HANDOFF_FINAL_2026-04-28.md`.
**What to look at if related issues surface:** Active `HANDOFF_FINAL_2026-04-28.md`.

---

### previous_handoff/contents/PHASE_2_HANDOFF.md

**Original path:** `previous handoff/PHASE_2_HANDOFF.md` (Daniel's pre-session archive, was tracked there)
**New path:** `safe_for_removal/previous_handoff/contents/PHASE_2_HANDOFF.md`
**Category:** completed_handoffs
**When active:** Phase 2 v0.1 era (pre-realignment, before 2026-04-26)
**Purpose when active:** Original Phase 2 handoff document covering the v0.1 schema-experiment work. Pre-dates the full TracePoint port.
**Why retired:** Phase 2 architecture has been realigned (per PROJECT_CLAUDE.md §3); the v0.1 schema is queued for migration in v0.2.1 / D.2. The original handoff is no longer load-bearing.
**What replaced it:** `HANDOFF_FINAL_2026-04-28.md` (current narrative). VALIDATION_LEDGER.md §B for v0.1 baseline test counts.
**What to look at if related issues surface:** `shared/bidset_record.py` for the v0.1 schema still in workspace; PROJECT_CLAUDE.md §6's "v0.2.1 ticket scope" note.

---

### previous_orders/contents/MARCH_ORDERS_B_1.md

**Original path:** `previous orders/MARCH_ORDERS_B_1.md` (Daniel's pre-session archive, was tracked there)
**New path:** `safe_for_removal/previous_orders/contents/MARCH_ORDERS_B_1.md`
**Category:** completed_march_orders
**When active:** 2026-04-27 (Phase B.1 ship)
**Purpose when active:** Drove the verbatim port of TracePoint Stages 2–5 (filter pipeline) onto `phase2-v0.3-B1-filter-pipeline` (commit `1c3fde4`).
**Why retired:** Phase B.1 shipped; verbatim port verified per VALIDATION_LEDGER.md §A (`filter_pipeline.py` SHA-1 `62390dbb…`, `test_filter_pipeline.py` `6dd43c1c…`). 27/27 tests still passing.
**What replaced it:** Nothing.
**What to look at if related issues surface:** `backend/core/filter_pipeline.py`, `backend/tests/test_filter_pipeline.py`, VALIDATION_LEDGER.md §A row.

---

### previous_orders/contents/MARCH_ORDERS_B_2_AND_B_3.md

**Original path:** `previous orders/MARCH_ORDERS_B_2_AND_B_3.md` (Daniel's pre-session archive, was tracked there)
**New path:** `safe_for_removal/previous_orders/contents/MARCH_ORDERS_B_2_AND_B_3.md`
**Category:** completed_march_orders
**When active:** 2026-04-27 (Phase B.2 + B.3 ship)
**Purpose when active:** Drove the verbatim port of TracePoint Stages 6–9 (geometry engine) and 10–12 (post-clustering scorers) onto `phase2-v0.3-B2-geometry-engine` (commits `4af872e` + `70c1835`). Added 4 new dependencies (`opencv-python`, `numpy`, `shapely`, `Pillow`).
**Why retired:** B.2 + B.3 shipped; verbatim port verified per VALIDATION_LEDGER.md §A (`geometry_matrix.py` SHA-1 `e0884449…`, `polygon_scorers.py` `c60d1419…`). 36/36 + 16/16 tests passing.
**What replaced it:** Nothing.
**What to look at if related issues surface:** `backend/core/geometry_matrix.py`, `backend/core/polygon_scorers.py`, VALIDATION_LEDGER.md §A.

---

### previous_orders/contents/MARCH_ORDERS_B_4.md

**Original path:** `previous orders/MARCH_ORDERS_B_4.md` (Daniel's pre-session archive, was tracked there)
**New path:** `safe_for_removal/previous_orders/contents/MARCH_ORDERS_B_4.md`
**Category:** completed_march_orders
**When active:** 2026-04-27 (Phase B.4 ship)
**Purpose when active:** Drove the verbatim port of TracePoint architect-profile flywheel + storage layer + correction_store onto `phase2-v0.3-B2-geometry-engine` (commit `a8ee936`). Storage layer ported but NOT activated in `run_dispatch` (deferred to D.1).
**Why retired:** B.4 shipped. Storage activation finally landed in D.1 per `backend/D_HARD_GATE_silverleaf.md`.
**What replaced it:** Nothing for B.4 itself; `MARCH_ORDERS_phase_D1.md` did the storage activation that B.4 deliberately left at `storage=None`.
**What to look at if related issues surface:** `backend/core/architect_profile.py`, `backend/core/storage.py`, `backend/core/correction_store.py`, `backend/tests/test_architect_profile.py`, VALIDATION_LEDGER.md §A.

---

### previous_orders/contents/MARCH_ORDERS_C_1.md

**Original path:** `previous orders/MARCH_ORDERS_C_1.md` (Daniel's pre-session archive, was tracked there)
**New path:** `safe_for_removal/previous_orders/contents/MARCH_ORDERS_C_1.md`
**Category:** completed_march_orders
**When active:** 2026-04-27 (Phase C.1 ship)
**Purpose when active:** Drove the verbatim port of TracePoint's `core/trade_module.py` (Protocol + 3 dataclasses) and authored `backend/CROSS_TRADE_INTEGRATION_NOTES.md` on `phase2-v0.3-C1-trade-module-interface` (commit `23a459c`).
**Why retired:** C.1 shipped; Protocol verbatim per VALIDATION_LEDGER.md §A (`trade_module.py` SHA-1 `d272f47d…`).
**What replaced it:** Nothing.
**What to look at if related issues surface:** `backend/core/trade_module.py`, `backend/CROSS_TRADE_INTEGRATION_NOTES.md`.

---

### previous_orders/contents/MARCH_ORDERS_C_2.md

**Original path:** `previous orders/MARCH_ORDERS_C_2.md` (Daniel's pre-session archive, was tracked there)
**New path:** `safe_for_removal/previous_orders/contents/MARCH_ORDERS_C_2.md`
**Category:** completed_march_orders
**When active:** 2026-04-27 (Phase C.2 ship)
**Purpose when active:** Drove the C.2 split-port: roofing vocabulary verbatim from TracePoint, roofing module with one same-character import edit, `build_trade_input` extracted from FastAPI route file into `trade_input_builder.py`. On `phase2-v0.3-C2-roofing-module` (commit `74772b6`).
**Why retired:** C.2 shipped. Module is vault-ruled per Decision 15 (extended D-8 follow-up). The "C.2-established equivalent path" referenced in calibration / sweep / D.1 wiring (zeroed-polygon TradeModuleInput) traces back to this orders document.
**What replaced it:** Nothing.
**What to look at if related issues surface:** `backend/core/roofing_module.py` (vault-ruled), `backend/core/roofing_vocabulary.py` (vault-ruled), `backend/core/trade_input_builder.py`, VALIDATION_LEDGER.md §A.

---

### previous_orders/contents/MARCH_ORDERS_C_3b.md

**Original path:** `previous orders/MARCH_ORDERS_C_3b.md` (Daniel's pre-session archive, was tracked there)
**New path:** `safe_for_removal/previous_orders/contents/MARCH_ORDERS_C_3b.md`
**Category:** completed_march_orders
**When active:** 2026-04-28 (Phase C.3b ship)
**Purpose when active:** Drove the additive `tables` field extension on `TradeModuleInput` (commit `7ea9abb`) and the `glazing_vocabulary.py` overlay build (commit `14f4f53`) on `phase2-v0.3-C3b-glazing-vocabulary` branch.
**Why retired:** C.3b shipped. `glazing_vocabulary.py` is vault-ruled retroactively per D-8.
**What replaced it:** Nothing.
**What to look at if related issues surface:** `backend/core/glazing_vocabulary.py` (vault-ruled), `backend/core/trade_module.py` (`tables` field), `backend/CROSS_TRADE_INTEGRATION_NOTES.md` (awning/canopy boundary added during this phase).

---

### previous_orders/contents/MARCH_ORDERS_C_3c_build.md

**Original path:** `previous orders/MARCH_ORDERS_C_3c_build.md` (Daniel's pre-session archive, was tracked there)
**New path:** `safe_for_removal/previous_orders/contents/MARCH_ORDERS_C_3c_build.md`
**Category:** completed_march_orders
**When active:** 2026-04-28 (Phase C.3c-build ship)
**Purpose when active:** Drove the build of `glazing_module.py` (first Huckleberry-original trade module) per Daniel's verbatim 2026-04-28 spec (schedule-first → elevation/plan reconciliation → title-page fallback → various-pages fallback). On `phase2-v0.3-C3c-glazing-module` (commits `c656ec6` contract-extension + `6001042` module + smoke + vault).
**Why retired:** C.3c-build shipped. Module is vault-ruled at sealing per Decision 15.
**What replaced it:** Nothing.
**What to look at if related issues surface:** `backend/core/glazing_module.py` (vault-ruled), `backend/tests/test_glazing_module_smoke.py`, VALIDATION_LEDGER.md §A2 row.

---

### previous_orders/contents/MARCH_ORDERS_C_5_debug_port.md

**Original path:** `previous orders/MARCH_ORDERS_C_5_debug_port.md` (Daniel's pre-session archive, was tracked there)
**New path:** `safe_for_removal/previous_orders/contents/MARCH_ORDERS_C_5_debug_port.md`
**Category:** completed_march_orders
**When active:** 2026-04-28 (Phase C.5 ship)
**Purpose when active:** Drove the partial-port of TracePoint's debug module: sections 1 (dispatch health), 3 (page intelligence), 6 (legend contents + quality flags) verbatim; sections 2/4/5 stubbed pending external state. On `phase2-v0.3-C5-debug-module-port` (commits `9025884` port + `b569312` Taco Bell run-through verification).
**Why retired:** C.5 shipped. `debug_module.py` is vault-ruled at sealing per Decision 15.
**What replaced it:** Nothing.
**What to look at if related issues surface:** `backend/core/debug_module.py` (vault-ruled), `backend/tests/test_debug_module_smoke.py`, `backend/DEBUG_MODULE_REPORT.md` (active spec/recommendation report), `backend/C5_DEBUG_RUN_THROUGH_taco-bell-weeki-wachee-compass-construction-management-2.md` (active run-through receipt).

---

### previous_orders/contents/MARCH_ORDERS_D8_FOLLOWUP.md

**Original path:** `previous orders/MARCH_ORDERS_D8_FOLLOWUP.md` (Daniel's pre-session archive, was tracked there)
**New path:** `safe_for_removal/previous_orders/contents/MARCH_ORDERS_D8_FOLLOWUP.md`
**Category:** completed_march_orders
**When active:** 2026-04-28 (D-8 follow-up session)
**Purpose when active:** Drove three corrections: C.3a inventory miscounts (60→64 components, 21→23 systems, 22→30 spec sections); CLAUDE.md §3 Decision 15 vault rule extension to cover trade modules; retroactive vault-rule application to RoofingModule, roofing_vocabulary, glazing_vocabulary. Single commit `eb49a08`.
**Why retired:** D-8 shipped.
**What replaced it:** Nothing.
**What to look at if related issues surface:** `backend/C3_GLAZING_SEED_VALIDATION.md` (active diagnostic with corrected counts), VALIDATION_LEDGER.md §A2 (count-correction row), §G (vault-ruled list).

---

### previous_orders/contents/MARCH_ORDERS_calibration_silverleaf.md (Daniel's archive copy)

**Original path:** `previous orders/MARCH_ORDERS_calibration_silverleaf.md` (Daniel's archive — duplicate of the root copy that's now in `safe_for_removal/march_orders/`)
**New path:** `safe_for_removal/previous_orders/contents/MARCH_ORDERS_calibration_silverleaf.md`
**Category:** completed_march_orders (duplicate)
**When active:** 2026-04-29 (calibration session)
**Purpose when active:** Same as the workspace-root copy — drove calibration. Daniel's archive movement created this second copy.
**Why retired:** Same reason. Two copies are in `safe_for_removal/` (one in `march_orders/` with git-history-preserved rename, one here in `previous_orders/contents/` from Daniel's pre-session archive).
**What replaced it:** Same as primary entry above.
**What to look at if related issues surface:** Same as primary entry above. The `march_orders/` copy is the one with full git history.

---

### previous_orders/contents/MARCH_ORDERS_page_type_verification.md

**Original path:** `previous orders/MARCH_ORDERS_page_type_verification.md` (Daniel's pre-session archive, was tracked there)
**New path:** `safe_for_removal/previous_orders/contents/MARCH_ORDERS_page_type_verification.md`
**Category:** completed_march_orders
**When active:** 2026-04-29 (page-type-verification session)
**Purpose when active:** Drove the page-type verification across 3 bidsets that PARTIALLY confirmed Bug 1 (page-type ordering) and CONFIRMED Bug 3 (tables plumbing) without shipping fixes. Single commit `06d46c5`.
**Why retired:** Verification phase shipped. Bugs were subsequently fixed in calibration session (commit `2c56913`).
**What replaced it:** `MARCH_ORDERS_calibration_silverleaf.md` (now in `safe_for_removal/march_orders/`) drove the actual fixes.
**What to look at if related issues surface:** `backend/PAGE_TYPE_VERIFICATION_GATE_REPORT.md` (active gate report), `backend/PAGE_TYPE_VERIFICATION_*.md` per-bidset reports (active), `backend/PAGE_TYPE_VERIFICATION_filter4_cache_audit.md` (active context-shape inspection), `backend/scripts/page_type_verification.py` (active tracked harness).

---

### previous_orders/contents/MARCH_ORDERS_profile_and_housekeeping.md (Daniel's archive copy)

**Original path:** `previous orders/MARCH_ORDERS_profile_and_housekeeping.md` (Daniel's archive — duplicate)
**New path:** `safe_for_removal/previous_orders/contents/MARCH_ORDERS_profile_and_housekeeping.md`
**Category:** completed_march_orders (duplicate)
**When active:** 2026-04-29 (profile-and-housekeeping session)
**Purpose when active:** Same as the workspace-root copy.
**Why retired:** Same reason. Two copies in `safe_for_removal/` (one in `march_orders/` with git-history-preserved rename, one here from Daniel's pre-session archive).
**What replaced it:** Same as primary entry above.
**What to look at if related issues surface:** Same as primary entry above.

---

### previous_orders/contents/MARCH_ORDERS_three_bidset_sweep.md (Daniel's archive copy)

**Original path:** `previous orders/MARCH_ORDERS_three_bidset_sweep.md` (Daniel's archive — duplicate)
**New path:** `safe_for_removal/previous_orders/contents/MARCH_ORDERS_three_bidset_sweep.md`
**Category:** completed_march_orders (duplicate)
**When active:** 2026-04-28 (three-bidset sweep session)
**Purpose when active:** Same as the workspace-root copy.
**Why retired:** Same reason.
**What replaced it:** Same as primary entry above.
**What to look at if related issues surface:** Same as primary entry above.

---

### previous_orders/contents/STEP_17_REVIEW_CHECKLIST.md

**Original path:** `previous orders/STEP_17_REVIEW_CHECKLIST.md` (Daniel's pre-session archive, was tracked there)
**New path:** `safe_for_removal/previous_orders/contents/STEP_17_REVIEW_CHECKLIST.md`
**Category:** step_by_step_orders
**When active:** v0.2 ship era (2026-04-25)
**Purpose when active:** Step-17 review checklist for v0.2 dispatch port. Daniel placed it in repo tree per D-3 (`DISCOVERED_ISSUES.md`).
**Why retired:** v0.2 shipped (commit `441896a`); Step 17 review completed.
**What replaced it:** Nothing — v0.2 gate-report-style checklists are now embedded in per-phase gate reports.
**What to look at if related issues surface:** `backend/DISCOVERED_ISSUES.md` (active register, contains D-3 row), `backend/V0_2_VALIDATION.md` (now in `safe_for_removal/pre_phase_B_validation/`).

---

### previous_orders/contents/STEP_18_DECISION_BRIEF.md

**Original path:** `previous orders/STEP_18_DECISION_BRIEF.md` (Daniel's pre-session archive, was tracked there)
**New path:** `safe_for_removal/previous_orders/contents/STEP_18_DECISION_BRIEF.md`
**Category:** step_by_step_orders
**When active:** v0.2 ship era (2026-04-25)
**Purpose when active:** Step-18 decision brief that pre-scoped v0.2.1 (D-4 + D-5 + schema migration).
**Why retired:** v0.2.1 work itself is queued, not started; the decision brief content is captured in PROJECT_CLAUDE.md §6 "v0.2.1 ticket scope" misconception entry.
**What replaced it:** PROJECT_CLAUDE.md §6 carries the decision; D-4 and D-5 rows persist in `backend/DISCOVERED_ISSUES.md`.
**What to look at if related issues surface:** PROJECT_CLAUDE.md §6, `backend/DISCOVERED_ISSUES.md` (D-4 + D-5 rows).

---

### anomalous_nested_repo_huckleberry/repo_root

**Original path:** `huckleberry/` (workspace root, untracked)
**New path:** `safe_for_removal/anomalous_nested_repo_huckleberry/repo_root` (tracked as embedded git repo / gitlink)
**Category:** anomalous_nested_repo
**When active:** Unknown. First flagged as a soft observation in the profile-and-housekeeping session (2026-04-29).
**Purpose when active:** Unknown. The directory contains its own `.git/` directory and a single `.gitattributes` file — no source files, no docs. Likely an accidental nested-repo init from an earlier session.
**Why retired:** Anomalous and unused. The workspace's primary git repo lives at the root; a nested repo here serves no purpose.
**What replaced it:** Nothing.
**What to look at if related issues surface:** **NOTE FOR DANIEL:** this directory has its own `.git/` subdirectory. If you want to inspect it, `cd safe_for_removal/anomalous_nested_repo_huckleberry/repo_root && git log` will show that repo's history (if any). When the time comes to delete `safe_for_removal/`, this nested `.git/` will be deleted along with it. Git tracks it here as a single embedded-repo gitlink (one SHA reference, not the contents).

---

### intake_diagnostic_outputs/INTAKE_DIAGNOSTIC.md

**Original path:** `backend/INTAKE_DIAGNOSTIC.md`
**New path:** `safe_for_removal/intake_diagnostic_outputs/INTAKE_DIAGNOSTIC.md`
**Category:** intake_diagnostic_outputs
**When active:** 2026-04-26 (intake diagnostic Pass 1 session)
**Purpose when active:** Pass 1 markdown report — surfaced an asymmetry between manufacturer evidence and detected_system across 19 bidsets. Looked actionable but turned out (per Pass 2) to largely dissolve.
**Why retired:** Diagnostic complete; conclusions are in VALIDATION_LEDGER.md §D + §I. Re-running it is forbidden per VALIDATION_LEDGER.md §I.
**What replaced it:** VALIDATION_LEDGER.md §D headline numbers; PROJECT_CLAUDE.md §6's "Pass 1 ... showed the dispatch gate is broken" misconception entry.
**What to look at if related issues surface:** VALIDATION_LEDGER.md §D ("Pass 1 headline numbers"), PROJECT_CLAUDE.md §6 (the "no — read the ledger" frame for this exact claim).

---

### intake_diagnostic_outputs/INTAKE_DIAGNOSTIC_PASS2.md

**Original path:** `backend/INTAKE_DIAGNOSTIC_PASS2.md`
**New path:** `safe_for_removal/intake_diagnostic_outputs/INTAKE_DIAGNOSTIC_PASS2.md`
**Category:** intake_diagnostic_outputs
**When active:** 2026-04-26 (Pass 2 session)
**Purpose when active:** Pass 2 markdown report — context-inspection of 35 manufacturer hits. Found 29/35 were manufacturers in non-roofing contexts; 0/35 had Division 7 spec proximity; 1/35 in negation context. Largely dissolved Pass 1's apparent asymmetry.
**Why retired:** Diagnostic complete; conclusions in VALIDATION_LEDGER.md §D.
**What replaced it:** VALIDATION_LEDGER.md §D ("Pass 2 headline numbers").
**What to look at if related issues surface:** VALIDATION_LEDGER.md §D, PROJECT_CLAUDE.md §6.

---

### intake_diagnostic_outputs/intake_diagnostic.py

**Original path:** `backend/scripts/intake_diagnostic.py`
**New path:** `safe_for_removal/intake_diagnostic_outputs/intake_diagnostic.py`
**Category:** intake_diagnostic_outputs
**When active:** 2026-04-26 (Pass 1)
**Purpose when active:** The script that produced Pass 1's per-page CSVs and summary JSON.
**Why retired:** Re-running forbidden per VALIDATION_LEDGER.md §I. Conclusions are in the ledger.
**What replaced it:** Nothing — diagnostic was one-shot.
**What to look at if related issues surface:** VALIDATION_LEDGER.md §D + §I.

---

### intake_diagnostic_outputs/intake_diagnostic_pass2.py

**Original path:** `backend/scripts/intake_diagnostic_pass2.py`
**New path:** `safe_for_removal/intake_diagnostic_outputs/intake_diagnostic_pass2.py`
**Category:** intake_diagnostic_outputs
**When active:** 2026-04-26 (Pass 2)
**Purpose when active:** Same shape as Pass 1 script, focused on context inspection.
**Why retired:** Same.
**What replaced it:** Nothing.
**What to look at if related issues surface:** Same.

---

### intake_diagnostic_outputs/intake_diagnostic_summary.json + intake_diagnostic_pass2_summary.json

**Original path:** `backend/test_fixtures/intake_diagnostic_summary.json`, `backend/test_fixtures/intake_diagnostic_pass2_summary.json` (both untracked)
**New path:** `safe_for_removal/intake_diagnostic_outputs/intake_diagnostic_{summary,pass2_summary}.json`
**Category:** intake_diagnostic_outputs
**When active:** 2026-04-26
**Purpose when active:** Aggregate JSON summaries produced by the two intake-diagnostic scripts.
**Why retired:** Diagnostics complete; ledger has the headline numbers.
**What replaced it:** Nothing.
**What to look at if related issues surface:** VALIDATION_LEDGER.md §D.

---

### intake_diagnostic_outputs/csvs/ (19 per-bidset CSVs)

**Original path:** `backend/test_fixtures/intake_diagnostic_outputs/*.csv` (untracked directory)
**New path:** `safe_for_removal/intake_diagnostic_outputs/csvs/*.csv` (now tracked)
**Category:** intake_diagnostic_outputs
**When active:** 2026-04-26
**Purpose when active:** One CSV per bidset (15 STACK + 4 public corpus = 19) capturing per-page evidence rows for Pass 1.
**Why retired:** Pass 1 conclusions sealed; CSVs not consumed elsewhere. VALIDATION_LEDGER.md §H lists them as "gitignored" but they were never actually gitignored — they sat untracked. Now tracked under `safe_for_removal/` for recoverability.
**What replaced it:** Nothing.
**What to look at if related issues surface:** Pass 1 conclusions in VALIDATION_LEDGER.md §D; the CSV per-page numbers are no longer load-bearing.

---

### pre_phase_B_validation/EXPERIMENT_FINDINGS.md

**Original path:** `backend/EXPERIMENT_FINDINGS.md`
**New path:** `safe_for_removal/pre_phase_B_validation/EXPERIMENT_FINDINGS.md`
**Category:** pre_phase_B_validation
**When active:** Pre-realignment Phase 2 v0.1 era
**Purpose when active:** Findings document from the v0.1 schema experiment that produced `BidsetRecord` and the original 15-bidset processed JSONs in `backend/test_fixtures/experiment_outputs/`.
**Why retired:** Phase 2 was architecturally realigned 2026-04-26 (PROJECT_CLAUDE.md §3 + retired CLAUDE.md §4); v0.1 schema is queued for migration in v0.2.1 / D.2; the findings document is no longer load-bearing.
**What replaced it:** PROJECT_CLAUDE.md §3 narrative + per-phase gate reports.
**What to look at if related issues surface:** `shared/bidset_record.py` (v0.1 schema still in workspace), `backend/test_fixtures/experiment_outputs/` (v0.1 outputs still in test_fixtures, consumed by `backend/tests/test_schema_round_trip.py`), PROJECT_CLAUDE.md §6 v0.2.1 entry.

---

### pre_phase_B_validation/EXPERIMENT_PROMPT.md

**Original path:** `backend/EXPERIMENT_PROMPT.md`
**New path:** `safe_for_removal/pre_phase_B_validation/EXPERIMENT_PROMPT.md`
**Category:** pre_phase_B_validation
**When active:** Pre-realignment Phase 2 v0.1 era
**Purpose when active:** The prompt / brief that drove the v0.1 experiment session.
**Why retired:** Same as `EXPERIMENT_FINDINGS.md` above.
**What replaced it:** Nothing.
**What to look at if related issues surface:** Same.

---

### pre_phase_B_validation/PUBLIC_CORPUS_OBSERVATIONS.md

**Original path:** `backend/PUBLIC_CORPUS_OBSERVATIONS.md`
**New path:** `safe_for_removal/pre_phase_B_validation/PUBLIC_CORPUS_OBSERVATIONS.md`
**Category:** pre_phase_B_validation
**When active:** 2026-04-26 (between v0.2 ship and Phase B start)
**Purpose when active:** Sweep observations across 4 non-STACK public-corpus bidsets — confirmed v0.2 verbatim port held end-to-end against PDFs from different producers.
**Why retired:** Headline numbers preserved in VALIDATION_LEDGER.md §C; the markdown observations are superseded by per-phase sweep reports (e.g., `backend/SWEEP_OBSERVATION_*.md` for the three-bidset sweep).
**What replaced it:** VALIDATION_LEDGER.md §C; subsequent per-phase observation reports.
**What to look at if related issues surface:** VALIDATION_LEDGER.md §C ("Public corpus" subsection).

---

### pre_phase_B_validation/TRACEPOINT_DISCOVERY.md

**Original path:** `backend/TRACEPOINT_DISCOVERY.md`
**New path:** `safe_for_removal/pre_phase_B_validation/TRACEPOINT_DISCOVERY.md`
**Category:** pre_phase_B_validation
**When active:** 2026-04-27 (Phase B port preparation)
**Purpose when active:** Discovery doc from when Daniel placed the TracePoint folder in the project tree — measured the Phase B port surface (2,854 lines across B.1–B.4), identified the 5 v0.2 ported files for SHA-1 verification, listed new dependencies needed.
**Why retired:** Phase B shipped; the discovery's findings are now in VALIDATION_LEDGER.md §A (port verification) and §D (TracePoint folder discovery numbers).
**What replaced it:** VALIDATION_LEDGER.md §A + §D.
**What to look at if related issues surface:** VALIDATION_LEDGER.md §D ("TracePoint folder discovery numbers").

---

### pre_phase_B_validation/V0_2_VALIDATION.md

**Original path:** `backend/V0_2_VALIDATION.md`
**New path:** `safe_for_removal/pre_phase_B_validation/V0_2_VALIDATION.md`
**Category:** pre_phase_B_validation
**When active:** v0.2 ship era (2026-04-25)
**Purpose when active:** v0.2 4-symptom STACK validation report. The artifact PROJECT_CLAUDE.md §6 cited as "v0.2 was validated with a 4-symptom STACK study. Receipts in `backend/V0_2_VALIDATION.md`."
**Why retired:** Per orders §4 #8 explicit listing. Findings persist as PROJECT_CLAUDE.md §6 "v0.2 should be re-validated" misconception entry. v0.2 is sealed; the 4-symptom report is no longer load-bearing.
**What replaced it:** PROJECT_CLAUDE.md §6.
**What to look at if related issues surface:** PROJECT_CLAUDE.md §6 (the "v0.2 should be re-validated" entry says "no — receipts in V0_2_VALIDATION.md sealed at v0.2 ship 2026-04-25"; that pointer now points here).

---

### pre_phase_B_validation/run_experiment.py

**Original path:** `backend/scripts/run_experiment.py`
**New path:** `safe_for_removal/pre_phase_B_validation/run_experiment.py`
**Category:** pre_phase_B_validation
**When active:** Pre-realignment v0.1 era
**Purpose when active:** v0.1 experiment runner that consumed `backend/scripts/_pipeline/*.py` (which is KEPT — `_pipeline/` is consumed by `backend/tests/test_pipeline_*.py` in the 216 sacred suite). Produced the per-bidset JSONs in `backend/test_fixtures/experiment_outputs/`.
**Why retired:** Realigned out by Phase B port. The actual pipeline now lives in `backend/core/`; `_pipeline/` is the v0.1 implementation kept solely so the v0.1 schema-roundtrip tests still pass.
**What replaced it:** Phase B port of TracePoint Stages 1–12 in `backend/core/`.
**What to look at if related issues surface:** `backend/scripts/_pipeline/` (still in workspace — consumed by tests), `backend/tests/test_pipeline_dispatch.py` + `test_pipeline_scope.py`, PROJECT_CLAUDE.md §3 Phase B paragraph.

---

### pre_phase_B_validation/analyze_outputs.py

**Original path:** `backend/scripts/analyze_outputs.py`
**New path:** `safe_for_removal/pre_phase_B_validation/analyze_outputs.py`
**Category:** pre_phase_B_validation
**When active:** Pre-realignment v0.1 era
**Purpose when active:** Read the 15 per-PDF JSONs and produced the coverage matrix / dispatch-accuracy ratio / observed-fields inventory used to populate `EXPERIMENT_FINDINGS.md`.
**Why retired:** EXPERIMENT_FINDINGS.md retired (above); analysis script no longer load-bearing.
**What replaced it:** Nothing.
**What to look at if related issues surface:** N/A — outputs not load-bearing post-realignment.

---

### pre_phase_B_validation/run_dispatch_on_15_bidsets.py

**Original path:** `backend/scripts/run_dispatch_on_15_bidsets.py`
**New path:** `safe_for_removal/pre_phase_B_validation/run_dispatch_on_15_bidsets.py`
**Category:** pre_phase_B_validation
**When active:** v0.2 ship era
**Purpose when active:** The 15-bidset STACK sweep that produced `backend/test_fixtures/v0.2_outputs/*.json` during v0.2 ship.
**Why retired:** v0.2 sealed. The output JSONs ARE KEPT (`backend/test_fixtures/v0.2_outputs/` per VALIDATION_LEDGER.md §C). The script that produced them is no longer load-bearing — re-running would produce the same outputs.
**What replaced it:** Nothing — receipts persist; producer script retired.
**What to look at if related issues surface:** `backend/test_fixtures/v0.2_outputs/*.json` (still in workspace; sacred per ledger), VALIDATION_LEDGER.md §C ("STACK corpus").

---

### pre_phase_B_validation/run_dispatch_on_public_corpus.py

**Original path:** `backend/scripts/run_dispatch_on_public_corpus.py`
**New path:** `safe_for_removal/pre_phase_B_validation/run_dispatch_on_public_corpus.py`
**Category:** pre_phase_B_validation
**When active:** 2026-04-26 (post-v0.2 public-corpus sweep)
**Purpose when active:** 4-bidset non-STACK sweep that produced `backend/test_fixtures/public_corpus_outputs/*.json` (gitignored) and `PUBLIC_CORPUS_OBSERVATIONS.md`.
**Why retired:** Sweep complete; observations sealed.
**What replaced it:** Nothing.
**What to look at if related issues surface:** VALIDATION_LEDGER.md §C ("Public corpus").

---

### pre_phase_B_validation/compare_v0.1_to_v0.2.py

**Original path:** `backend/scripts/compare_v0.1_to_v0.2.py`
**New path:** `safe_for_removal/pre_phase_B_validation/compare_v0.1_to_v0.2.py`
**Category:** pre_phase_B_validation
**When active:** v0.2 ship era
**Purpose when active:** Compare v0.1 schema-experiment outputs against v0.2 dispatch outputs. Used during v0.2 validation.
**Why retired:** v0.2 validation sealed.
**What replaced it:** Nothing.
**What to look at if related issues surface:** `backend/V0_2_VALIDATION.md` (now in `safe_for_removal/pre_phase_B_validation/`).

---

### pre_phase_B_validation/verify_v02_outputs.py

**Original path:** `backend/scripts/verify_v02_outputs.py`
**New path:** `safe_for_removal/pre_phase_B_validation/verify_v02_outputs.py`
**Category:** pre_phase_B_validation
**When active:** v0.2 ship era
**Purpose when active:** Verify v0.2 output JSONs after the 15-bidset sweep.
**Why retired:** v0.2 sealed; verification complete.
**What replaced it:** Nothing.
**What to look at if related issues surface:** Same as above.

---

### superseded_scripts/c5_run_through.py

**Original path:** `backend/scripts/c5_run_through.py`
**New path:** `safe_for_removal/superseded_scripts/c5_run_through.py`
**Category:** superseded_scripts
**When active:** 2026-04-28 (Phase C.5 ship — Taco Bell bidset run-through)
**Purpose when active:** One-shot harness that ran dispatch + debug module against Taco Bell to verify C.5 partial-port. Produced `backend/C5_DEBUG_RUN_THROUGH_taco-bell-weeki-wachee-compass-construction-management-2.md`.
**Why retired:** Superseded by reusable harnesses (`calibrate_silverleaf.py`, `d1_silverleaf_hardgate.py`) that follow the same pattern. Per orders §4 #10 explicit listing. The Taco Bell run-through report itself is KEPT (active receipt).
**What replaced it:** `backend/scripts/calibrate_silverleaf.py` and `backend/scripts/d1_silverleaf_hardgate.py` follow this script's pattern but are tracked, parameterized, and reusable.
**What to look at if related issues surface:** `backend/C5_DEBUG_RUN_THROUGH_taco-bell-weeki-wachee-compass-construction-management-2.md` (active report).

---

### superseded_scripts/sweep_three_bidsets.py

**Original path:** `backend/scripts/sweep_three_bidsets.py`
**New path:** `safe_for_removal/superseded_scripts/sweep_three_bidsets.py`
**Category:** superseded_scripts
**When active:** 2026-04-28 (three-bidset sweep session)
**Purpose when active:** One-shot harness that ran dispatch + RoofingModule + GlazingModule + debug module against Shoppes-at-Avalon, Vine Street, Bearss Ave. Produced the three `backend/SWEEP_OBSERVATION_*.md` reports.
**Why retired:** Per orders §4 #10 explicit listing — was intentionally untracked but did get committed; superseded by `calibrate_silverleaf.py` / `d1_silverleaf_hardgate.py` patterns. The three observation reports themselves are KEPT (active receipts).
**What replaced it:** Pattern lives on in active tracked harnesses.
**What to look at if related issues surface:** `backend/SWEEP_OBSERVATION_*.md` reports (active), VALIDATION_LEDGER.md §D ("Three-bidset sweep headline numbers").

---

### old_terminal_logs/v0.2_sweep.log

**Original path:** `backend/scripts/v0.2_sweep.log` (untracked)
**New path:** `safe_for_removal/old_terminal_logs/v0.2_sweep.log`
**Category:** old_terminal_logs
**When active:** v0.2 ship era
**Purpose when active:** Captured terminal output of the 15-bidset STACK sweep.
**Why retired:** v0.2 shipped; terminal log is not load-bearing.
**What replaced it:** Nothing.
**What to look at if related issues surface:** `backend/test_fixtures/v0.2_outputs/*.json` (the actual sweep outputs are still in workspace).

---

## Frontend versions retired by E.0 (2026-04-30)

Per Daniel directive 2026-04-29 / executed 2026-04-30: v6.3.5 confirmed canonical going forward; v6.3.1 through v6.3.4 retired. The four version-specific spotcheck scripts that hardcode older versions in their `HTML_PATH` constants are moved alongside the HTML files they target — they are historical regression tests for behavior that landed in those specific versions.

The currently-active frontend test artifacts stay in `frontend/`:
- `frontend/Huckleberry_AI_6.3.5_Scope.html` (canonical, 138/138 tests pass)
- `frontend/run_tests.js` (jsdom harness; defaults to v6.3.5 via `npm test` CLI argument)
- `frontend/mutation_test_step11.js` (targets v6.3.5 explicitly; not part of the 138 floor)
- `frontend/extracted/Huckleberry_AI_6.3.0_Scope.html` (older still; left in place — not in scope for E.0)

`npm test` still passes 138/138 against v6.3.5 after these moves (verified 2026-04-30 at E0.4 post-move floor check). `npm run test:spotchecks` is now broken because the four spotcheck scripts moved with their target HTMLs; the script entry in `frontend/package.json` is left as-is so a future archaeologist sees what was there. The next frontend-touching session can clean up that `package.json` entry; doing so in E.0 would require modifying production frontend config and is out of scope per orders §9 #7.

### Huckleberry_AI_6.3.1_Scope.html

**Original path:** `frontend/Huckleberry_AI_6.3.1_Scope.html`
**New path:** `safe_for_removal/frontend_versions/Huckleberry_AI_6.3.1_Scope.html`
**Category:** retired_frontend_versions
**When active:** before 2026-04-30 (v6.3.1 ship era, ~107 tests historically per PROJECT_CLAUDE.md reference)
**Purpose when active:** Phase 1 frontend HTML iteration; superseded by the v6.3.2 → v6.3.5 chain.
**Why retired:** Superseded by v6.3.5 (138 tests, more complete). E.0 audit confirmed v6.3.5 is the canonical surface going into Phase E.
**What replaced it:** `frontend/Huckleberry_AI_6.3.5_Scope.html`
**What to look at if related issues surface:** v6.3.5 audit at `backend/E0_FRONTEND_AUDIT.md`; sacred-files list in `VALIDATION_LEDGER.md §A2`; `frontend/package.json` test scripts.

---

### Huckleberry_AI_6.3.2_Scope.html

**Original path:** `frontend/Huckleberry_AI_6.3.2_Scope.html`
**New path:** `safe_for_removal/frontend_versions/Huckleberry_AI_6.3.2_Scope.html`
**Category:** retired_frontend_versions
**When active:** before 2026-04-30 (v6.3.2 ship era)
**Purpose when active:** Phase 1 frontend HTML iteration; intermediate between 6.3.1 and 6.3.5.
**Why retired:** Same as 6.3.1.
**What replaced it:** `frontend/Huckleberry_AI_6.3.5_Scope.html`
**What to look at if related issues surface:** Same as 6.3.1.

---

### Huckleberry_AI_6.3.3_Scope.html

**Original path:** `frontend/Huckleberry_AI_6.3.3_Scope.html`
**New path:** `safe_for_removal/frontend_versions/Huckleberry_AI_6.3.3_Scope.html`
**Category:** retired_frontend_versions
**When active:** before 2026-04-30 (v6.3.3 ship era)
**Purpose when active:** Phase 1 frontend HTML iteration.
**Why retired:** Same as 6.3.1.
**What replaced it:** `frontend/Huckleberry_AI_6.3.5_Scope.html`
**What to look at if related issues surface:** Same as 6.3.1.

---

### Huckleberry_AI_6.3.4_Scope.html

**Original path:** `frontend/Huckleberry_AI_6.3.4_Scope.html`
**New path:** `safe_for_removal/frontend_versions/Huckleberry_AI_6.3.4_Scope.html`
**Category:** retired_frontend_versions
**When active:** before 2026-04-30 (v6.3.4 ship era)
**Purpose when active:** Phase 1 frontend HTML iteration; immediate predecessor of 6.3.5.
**Why retired:** Same as 6.3.1.
**What replaced it:** `frontend/Huckleberry_AI_6.3.5_Scope.html`
**What to look at if related issues surface:** Same as 6.3.1.

---

### spotcheck_durolast.js

**Original path:** `frontend/spotcheck_durolast.js`
**New path:** `safe_for_removal/frontend_versions/spotcheck_durolast.js`
**Category:** retired_frontend_versions (version-specific test)
**When active:** before 2026-04-30
**Purpose when active:** Exercised the Duro-Last + TPO + PVC vocab against real CLAUDE.md bidset strings at v6.3.1; targeted `Huckleberry_AI_6.3.1_Scope.html` directly via hardcoded `HTML_PATH` constant.
**Why retired:** The HTML it targets is retired. Was reachable only via `npm run test:spotchecks` (not part of the 138/138 floor). Coverage of Duro-Last + TPO + PVC has since rolled into the 138-test suite against v6.3.5.
**What replaced it:** SCOPE_TESTS embedded in v6.3.5 (line 5559+); backend `roofing_vocabulary.py` (vault-ruled).
**What to look at if related issues surface:** Backend `roofing_vocabulary.py`; v6.3.5 SCOPE_TESTS; `backend/SWEEP_OBSERVATION_*.md` for real-bidset behavior.

---

### spotcheck_manufacturer.js

**Original path:** `frontend/spotcheck_manufacturer.js`
**New path:** `safe_for_removal/frontend_versions/spotcheck_manufacturer.js`
**Category:** retired_frontend_versions (version-specific test)
**When active:** before 2026-04-30
**Purpose when active:** Exercised manufacturer-detection vocab at v6.3.2; targeted `Huckleberry_AI_6.3.2_Scope.html` directly.
**Why retired:** Same as `spotcheck_durolast.js`.
**What replaced it:** Same as `spotcheck_durolast.js`.

---

### spotcheck_cricket.js

**Original path:** `frontend/spotcheck_cricket.js`
**New path:** `safe_for_removal/frontend_versions/spotcheck_cricket.js`
**Category:** retired_frontend_versions (version-specific test)
**When active:** before 2026-04-30
**Purpose when active:** Exercised cricket/saddle vocab + tool-routing logic at v6.3.3; targeted `Huckleberry_AI_6.3.3_Scope.html` directly.
**Why retired:** Same as `spotcheck_durolast.js`.
**What replaced it:** Same as `spotcheck_durolast.js`.

---

### spotcheck_10b.js

**Original path:** `frontend/spotcheck_10b.js`
**New path:** `safe_for_removal/frontend_versions/spotcheck_10b.js`
**Category:** retired_frontend_versions (version-specific test)
**When active:** before 2026-04-30
**Purpose when active:** Exercised Step 10b interior-density scoring at v6.3.4; targeted `Huckleberry_AI_6.3.4_Scope.html` directly.
**Why retired:** Same as `spotcheck_durolast.js`.
**What replaced it:** Same as `spotcheck_durolast.js`.

---

### Huckleberry_AI_6.3.5_Scope.html

**Original path:** `frontend/Huckleberry_AI_6.3.5_Scope.html`
**New path:** `safe_for_removal/frontend_versions/Huckleberry_AI_6.3.5_Scope.html`
**Category:** retired_frontend_versions
**When active:** ship era through 2026-04-30 (138/138 frontend test floor; canonical surface for E.0 audit + E.2.0 strip plan)
**Purpose when active:** Phase 1 single-file HTML viewer with the full TracePoint 12-stage geometry pipeline JS port, ROOF_VOCAB scope extractor, classifyPage classifier, PDF.js operator-list walker, and 138 jsdom-driven tests. Was the canonical frontend surface entering Phase E.
**Why retired:** Phase E.2.1 destructive sub-phase shipped (2026-04-30). v6.3.5 was the explicit strip target — pipeline + scope + walker code stripped per `backend/E2_0_STRIP_PLAN.md`; the surviving keeper code (Viewer + tools + takeoff Excel) was rebuilt bottom-up into `frontend/src/Huckleberry_AI_phase2.v1.0.0.html`. v6.3.5's content SHA-1 (`cf3765d61fd6f17de46024a3a84c62f25b19b3c5`) is preserved through the `git mv` to the archived path — the file content is byte-identical, only the path changed.
**What replaced it:** `frontend/src/Huckleberry_AI_phase2.v1.0.0.html` (3,672 lines; 20/20 test floor; API-connected viewer with apiClient skeleton).
**What to look at if related issues surface:** `backend/E2_0_STRIP_PLAN.md` (line-by-line strip plan that targeted v6.3.5), `backend/E2_1_GATE_REPORT.md` (gate report for the strip sub-phase), `frontend/src/Huckleberry_AI_phase2.v1.0.0.html` (the new file), `backend/E0_FRONTEND_AUDIT.md` (the audit that catalogued v6.3.5's structure before strip). v6.3.5 stays accessible at the archived path as an offline-fallback reference until Daniel's eventual review-and-empty session for `safe_for_removal/`.

---

## End of MANIFEST

If you're reading this in 2027 from the wiki conversion: the `safe_for_removal/` folder is gone, but every file mentioned above existed at the path under "Original path:" before this session. Use git history (`git log --all --follow -- <original-path>`) to retrieve full content if needed.
