# PROJECT_CLAUDE.md

**Read this first. Every session. No exceptions.**

This document exists so every Claude session — extended-thinking, Claude Code, any future model version — starts from the same page. The recurring failure mode in this project has been Claude sessions doubting work that has already been validated, asking Daniel to re-explain state he has explained many times before, and probing/re-running things that don't need to be re-run.

This document defeats that loop.

---

## 1. The canonical documents (read in this order)

| # | Document | What it is | When to read it |
|---|---|---|---|
| 1 | **PROJECT_CLAUDE.md** (this file) | Entry point and discipline | First, every session |
| 2 | **VALIDATION_LEDGER.md** | Empirical proof of what has been validated, with verification methods named | Second — quote it instead of re-litigating |
| 3 | **Latest handoff** (e.g., `HANDOFF_FINAL_*.md` if one exists, or the most recent gate report) | Narrative of recent state and where things stand right now | Third — bridges canon to current moment |
| 4 | **MARCH_ORDERS_*.md** (active phase orders) | Step-by-step execution plan for the current phase | Fourth — only when actually executing |

`CLAUDE.md` was retired by Daniel directive on 2026-04-29; substantive content has migrated to PROJECT_CLAUDE.md and VALIDATION_LEDGER.md. Older artifacts may still reference it as `CLAUDE.md §X` — treat such references as historical pointers and work from the canonical docs above.

If you (Claude session reading this) feel an urge to do something before reading those, stop and read them first. The urge is the failure mode.

---

## 2. The project, in three sentences

**Huckleberry AI is a commercial-construction-takeoff platform.** A general contractor uploads a bidset PDF; the Python backend ingests, dispatches, runs trade modules, extracts scope, detects polygons, identifies scale, produces auto-annotated structured data; the frontend pulls that data so the user can review, edit, approve, export to Excel, and ship corrections back as labeled training data.

**It is multi-trade by design.** Roofing is the first trade module to ship; glazing, siding, mechanical, plumbing, electrical, structural all use the same backend pipeline and the same trade module interface. The platform is NOT a roofing program with extensions.

**The architecture is TracePoint-derived.** A 12-stage pipeline ported from the TracePoint research artifact, with the dispatch gate (Layer 3), filter pipeline (Stages 2–5), geometry engine (Stages 6–9), post-clustering scorers (Stages 10–12), and architect-profile flywheel + storage + correction_store all verbatim-ported into the Huckleberry backend as of 2026-04-27. Phase B is sealed.

---

## 3. Where the project actually stands at end-of-day 2026-04-28

**Phases B, C.1, C.2, C.3b, C.3c-build, C.5, and the three-bidset sweep are complete.** Backend has TracePoint Stages 1–12 plus the architect-profile flywheel + storage + correction_store (Phase B), plus the trade module Protocol contract (Phase C.1: `TradeFieldValue` / `TradeModuleInput` / `TradeModuleOutput` / `TradeModule`), plus the first concrete trade module — roofing — implementing that Protocol (Phase C.2: `roofing_vocabulary.py` + `roofing_module.py` + `trade_input_builder.py`), plus the second trade module's vocabulary (Phase C.3b: `glazing_vocabulary.py` overlaying the parked glazing seeds), plus the second concrete trade module — glazing — built against the contract (Phase C.3c-build: `glazing_module.py`, first Huckleberry-original trade module, rough-ship per Daniel's 2026-04-28 spec), plus the partial debug-module port (Phase C.5: `debug_module.py`, sections 1/3/6 verbatim from TracePoint, sections 2/4/5 stubbed pending external state), plus the three-bidset sweep (descriptive observation reports against Shoppes-at-Avalon, Vine Street, Bearss Ave; modules vault-ruled and untouched throughout; reports under `backend/SWEEP_OBSERVATION_*.md`). C.1 also added `backend/CROSS_TRADE_INTEGRATION_NOTES.md` covering the four obvious cross-trade boundaries (RTU/roofing↔mechanical, storefront/glazing↔roofing, siding↔roofing transition, structural-deck↔roofing).

**Test floor:** **216 backend tests passing, 19 skipped, 0 failed** (215 baseline through D-8 follow-up + 1 C.3c-build smoke test for `GlazingModule` + 1 C.5 smoke test for `debug_module` partial port). Frontend at v6.3.1 baseline (107/107 + spotchecks + mutation tests, all sacred). No regressions across any sub-phase ship. C.1, C.2, C.3a, C.3b, D-8 follow-up all added zero tests; C.3c-build added 1 (`test_glazing_module_smoke.py`); C.5 added 1 (`test_debug_module_smoke.py`). Behavior-level verification for the trade modules is the C.3c-run sweep job, not advance tests.

**Branch state:** `phase2-v0.3-B2-geometry-engine` carries B.2 + B.3 + B.4. `phase2-v0.3-B1-filter-pipeline` carries B.1. `phase2-v0.3-C1-trade-module-interface` carries C.1 (one commit `23a459c` from `a8ee936`). `phase2-v0.3-C2-roofing-module` carries C.2 (one commit `74772b6` from `23a459c`). `phase2-v0.3-C3b-glazing-vocabulary` carries C.3b + D-8 follow-up (`7ea9abb`, `14f4f53`, `eb49a08`). `phase2-v0.3-C3c-glazing-module` carries C.3c-build from `eb49a08` (`c656ec6` contract extension, `6001042` module + smoke + vault rule). `phase2-v0.3-C5-debug-module-port` carries C.5 from `6001042` (`9025884` partial port + smoke + vault rule, plus the bidset run-through commit `b569312` landing in C.5 ship). `phase2-v0.3-sweep-three-bidsets` carries the sweep ship (single commit `cf107dd`: three observation reports + a prior PROJECT_CLAUDE.md update) from C.5 head `b569312`; pushed to remote 2026-04-29 at the start of the profile-and-housekeeping session. `phase2-v0.3-profile-and-housekeeping` from sweep head `cf107dd` carries the profile diagnostic + housekeeping bundle (commit 1: profile report + tracked harness; commit 2: housekeeping); pushed to remote 2026-04-29 at session end. All nine Phase 2 feature branches are now on remote.

**v0.2.1 (D-4 + D-5 + schema migration) is queued, not started.** Phase A (close v0.2 properly) was deprioritized in favor of Phase B by Daniel's explicit decision. Both are still on the board.

**Profile diagnostic complete (2026-04-29):** Receipts at `backend/PROFILE_DIAGNOSTIC_bearss-ave.md`. Times pdfplumber text/table extraction + RoofingModule.analyze + GlazingModule.analyze on two debug-section-3-driven Bearss Ave pages (page 15 high-content S-103 SPECIAL INSPECTIONS; page 82 low-content unknown). pdfplumber.extract_tables was the dominant per-page cost on both pages (2.91s median on page 15; 178ms median on page 82). Reusable harness committed at `backend/scripts/profile_diagnostic.py` (tracked, unlike the one-shot sweep harness). Full numerical receipts in VALIDATION_LEDGER.md §D.

**What's next:** Daniel reviews the three sweep observation reports (`backend/SWEEP_OBSERVATION_*.md`) plus the profile diagnostic (`backend/PROFILE_DIAGNOSTIC_bearss-ave.md`). The decision point is genuinely open: (a) module tuning sessions next, dedicated, with `core/` frozen, in the discipline established by CLAUDE.md §3 Decision 15; OR (b) proceed to C.4 cross-trade relationships layer design now and defer tuning; OR (c) a refined direction informed by what the profile data says about where per-page time actually went. Extended-thinking Claude drafts the next phase's march orders once Daniel chooses. The sweep + profile produced data, not a decision.

**C.3a complete (2026-04-28):** Read-only diagnostic comparing the parked Huckleberry glazing seeds (`backend/seeds/glazing_assemblies.py` 1,311 lines, `backend/seeds/glazing_materials.py` 264 lines) against the Shoppes-at-Avalon bidset's actual glazing scope (storefronts, window types, door schedules, hardware sets, exterior finish schedule). Verdict: **usable as a starting vocabulary, with documented gaps** — not "build from scratch." YKK manufacturer detection, FBC HVHZ vs non-HVHZ branches, tempered/Low-E/IGU vocabulary, and the schedule-driven workflow architecture all line up with the bidset. Real gaps surfaced: no `entrance_*_single` variants (only pairs), no hardware set for "single aluminum storefront entrance + panic," no standing-seam-metal-awning or pre-fab-flat-canopy entries (PAC-CLAD M-2 / MAPES M-4 — possible trade boundary), missing component slots for deadbolt/drip-cap/latch-guard/peep-hole, empty hardware-OEM manufacturer table. Receipts in `backend/C3_GLAZING_SEED_VALIDATION.md`. Explicit non-conclusion: one bidset, one building typology (single-story retail), Florida-only. Not calibration.

**C.3b complete (2026-04-28):** TradeModuleInput contract extended with optional `tables` field for schedule-driven trade modules (commit `7ea9abb`); `backend/core/glazing_vocabulary.py` built as overlay on the parked seeds with the C.3a-documented gaps (commit `14f4f53`). Vault-ruled retroactively in D-8 follow-up.

**D-8 follow-up complete (2026-04-28):** C.3a inventory miscounts corrected (60→64 components, 21→23 systems, 22→30 spec sections; SHA-1 of seeds unchanged). CLAUDE.md §3 Decision 15 extended to cover trade modules per Daniel's directive. Vault rule applied retroactively to RoofingModule, roofing_vocabulary, and glazing_vocabulary. Commit `eb49a08`.

**C.3c-build complete (2026-04-28):** First Huckleberry-original trade module. `backend/core/glazing_module.py` (757 lines) implements the C.1 `TradeModule` Protocol's `analyze(input)` method per Daniel's verbatim 2026-04-28 spec (`MARCH_ORDERS_C_3c_build.md` §1): schedule-first → elevation/plan reconciliation → title-page fallback → various-pages fallback; per-item field set for glazing/door/storefront with .0000 dimension precision; alias-aware vocabulary matching against `glazing_vocabulary`. Module ships ROUGH per CLAUDE.md §3 Decision 15; docstring lists 11 known limitations explicitly. Contract-extension commit `c656ec6` added three optional `list[dict]` fields to `TradeModuleOutput` (glazing_items, door_items, storefront_items) — additive, default None, RoofingModule unaffected. Module + smoke test + vault rule in commit `6001042`. Backend 214 → 215.

**Debug-module specification report complete (2026-04-28):** Read-only spec report on `tracepoint_port/TracePoint/modules/debug/debug_module.py` (470 lines, SHA-1 `b5a4cf93ca7c02116fc00f6dc5a1514da1b18b60`) plus its empty `__init__.py`. Recommendation: port partially, defer to a standalone C.5 sub-phase. Sections 1/3/6 immediately, sections 2/4/5 stubbed pending external state. Receipts in `backend/DEBUG_MODULE_REPORT.md`.

**C.5 complete (2026-04-28):** Partial debug-module port per the spec report's recommendation. `backend/core/debug_module.py` sealed at SHA-1 of the TracePoint source (`b5a4cf93ca7c02116fc00f6dc5a1514da1b18b60`, verified at port time) with **1 line** of import-path edit (line 65 `sys.path.insert` adjusted from TracePoint's `parent.parent.parent` to Huckleberry's `parent.parent` because `core/` lives one level closer to the package root) — well under the orders' 4-line budget. Sections 1 (dispatch health), 3 (page intelligence), 6 (legend contents + quality flags) ported verbatim. Sections 2 (scale comparison), 4 (cross-reference graph), 5 (geometry diagnostics) stubbed with documented `stub_marker` dicts pending external state (scale-engine route, networkx + sheet-index, geometry results respectively). No new dependencies (networkx deliberately not added). Vault-ruled at sealing per CLAUDE.md §3 Decision 15. Smoke test + bidset run-through verification both passed: smoke test asserts all six section attributes plus quality flags, asserts sections 1/3/6 produce real content, asserts sections 2/4/5 stub markers exact. Bidset run-through against Taco Bell — Weeki Wachee (`backend/C5_DEBUG_RUN_THROUGH_taco-bell-weeki-wachee-compass-construction-management-2.md`) produced: dispatch in 70.7s; section 1 dispatch_complete=True with all expected keys; section 3 with 88 page-intelligence rows; section 6 with 108 legends + quality flags emitted; sections 2/4/5 stub markers exact; `ctx.project_scope.detected_system="tpo"` confidence 0.95; `scope_pages=[18, 19]` — every orders §5 verification assertion passed. Branch `phase2-v0.3-C5-debug-module-port` from `6001042`; commits `9025884` (port + smoke + vault rule) + the bidset-run-through+canon-update commit `b569312`; pushed to remote 2026-04-28 at the start of the sweep session (after `phase2-v0.3-C3c-glazing-module` per push order so the parent commit was on remote first).

**Three-bidset sweep complete (2026-04-28).** Descriptive observation reports against three real bidsets per `MARCH_ORDERS_three_bidset_sweep.md`. Modules vault-ruled and untouched throughout — zero `backend/core/` modifications, zero new dependencies, zero new tests. Reports are descriptive only: no grading, no correctness comparison, no "needs ground truth" labels, no fix lists, no tuning recommendations, per Daniel's directive 2026-04-28. The three reports under `backend/`:

- `SWEEP_OBSERVATION_shoppes-at-avalon.md` — 97 pages; dispatch 60.2s; modules 653.6s; 0/97 errors on both modules; roofing module produced 830 `fields` entries across 97 non-empty-output pages with 0 warnings and 0 equipment_pins; glazing module produced 43 glazing_items / 22 door_items / 22 storefront_items across 22 pages with non-empty output; debug section 6 emitted 1 legend entry and 0 quality flags; sections 2/4/5 stub markers confirmed; `project_scope.detected_system = None` (consistent with C.3a's prior characterization of Shoppes as a STACK bidset where dispatch's manufacturer-scan path ran but produced no positive scope-page evidence within ±200 chars of a Division 7 reference).
- `SWEEP_OBSERVATION_vine-street.md` — 138 pages; dispatch 82.0s; modules 654.6s; 0/138 errors on both modules; roofing module produced 1,201 `fields` entries across 138 non-empty-output pages; glazing module produced 100 glazing_items / 12 door_items / 23 storefront_items across 47 pages with non-empty output; debug section 6 emitted 46 legend entries and 0 quality flags; sections 2/4/5 stub markers confirmed; `project_scope.detected_system = None`.
- `SWEEP_OBSERVATION_bearss-ave.md` — 91 pages; dispatch 95.0s; modules 824.9s; 0/91 errors on both modules; roofing module produced 769 `fields` entries across 91 non-empty-output pages; glazing module produced 177 glazing_items / 31 door_items / 24 storefront_items across 58 pages with non-empty output; debug section 6 emitted 145 legend entries and 1 quality flag; sections 2/4/5 stub markers confirmed; `project_scope.detected_system = None`.

Per-page module error rate was 0.00% across all three bidsets and both modules (652 module calls × 326 pages, no exceptions). The §7 stop threshold (>25% per-bidset per-module error rate) was never approached. Branch `phase2-v0.3-sweep-three-bidsets` from C.5 head `b569312`; one commit (the three reports + this PROJECT_CLAUDE.md update). Sweep branch is local-only at session end; push timing is Daniel's call. The sweep harness (`backend/scripts/sweep_three_bidsets.py`) is untracked, same convention as C.5's `c5_run_through.py`. Harness note: standard `build_trade_input()` requires `geometry_result` from Stages 6–9 which is ported but not wired to dispatch (Phase D/E concern); the sweep harness therefore constructed `TradeModuleInput` directly per page with dispatch-side state (page_legends, page_zones, page_type, project_scope) plus pdfplumber-extracted text and tables, with `polygon_*` fields zero/empty and `scale_source = "unwired"`. This is the "C.2-established equivalent" path explicitly permitted by the orders §6 when the standard builder's preconditions aren't met.

**Calibration session — B2607 AEA Silverleaf complete (2026-04-29):** First calibration session of program. Dispatch-side iterative refinement using the C.5 debug module as the diagnostic surface. Two structural fixes applied across two iterations on branch `phase2-v0.3-calibration-silverleaf` (single commit `2c56913` from `06d46c5`, pushed): Bug 1 (page-type ordering — SCHEDULE rule moved to position 0 in `_PAGE_TYPE_RULES`; iter 1 schedule_sheet 8→18, quality_flags held at 0) and Bug 3 (tables plumbing via Path c — `_parse_tables_on_page` returns `(legends, raw_tables)` tuple; raw_tables cached on `PageContext.raw_tables` for schedule pages; `build_trade_input` reads them into `TradeModuleInput.tables`). Iteration 3 skipped — diminishing returns. Vault rule held throughout (5 modules SHA-1-verified unchanged). Sacred floors held: backend 216/19/0, frontend at baseline. Receipts in `backend/CALIBRATION_GATE_REPORT_silverleaf.md` and `backend/CALIBRATION_RUN_silverleaf_iter_{0,1,2}.md`. Tracked harness at `backend/scripts/calibrate_silverleaf.py`. Master ledger at `backend/BLOCK_RUN.md` (continues across calibration → Phase D → Phase E).

**Phase D.1 complete (2026-04-29):** Storage activation + RoofingModule + GlazingModule wired into the production `run_dispatch` call path. Single session, autonomous, branch `phase2-v0.3-D1-storage-and-module-wiring` from calibration head `2c56913`. `dispatch_gate.run_dispatch(pdf, storage="auto")` now lazily constructs a default `StorageEngine` (SQLite, `~/.tracepoint/cache.db`); the `storage=None` path is unchanged so legacy harnesses (calibration, sweep, profile) continue to work. After Filter 5 / scope_scanner / project_metadata, a new "Stage 13" runs RoofingModule + GlazingModule per page using `core.trade_module.TradeModuleInput` (built dispatch-side with zeroed polygon fields — Stages 6–9 geometry wiring is deferred to D.2/E per the C.2-established equivalent path). Per-page `TradeModuleOutput` records land on the new `PlanSetContext.trade_module_outputs: dict[int, dict[str, Any]]` field (additive, default empty dict). Silverleaf hard gate passed all 7 criteria: roofing 338/338 fields, glazing 20/20 / door 81/81 / storefront 6/6 items (exact parity with calibration iter 2), schedule_sheet pages 18/18 with `raw_tables` populated, dispatch_warnings shape preserved, wired-dispatch wall-clock 139.8s under the 187.1s budget (+30% of calibration's combined dispatch+modules 143.9s — orders §7 criterion 2's intent), 0 per-page module errors, vault SHA-1s match pre-session, all 5 frontend HTML SHA-1s match pre-session, backend test floor 216/19/0 maintained (zero new tests). Hard gate report at `backend/D_HARD_GATE_silverleaf.md`; tracked harness at `backend/scripts/d1_silverleaf_hardgate.py`. CLAUDE.md retired by Daniel directive 2026-04-29 — frontend vault-treated for Phase D pending Phase E strip-and-connect. D.2 (job folder + multi-tenant identity + schema migration) and Phase E (backend API + frontend strip-and-connect) are now next-eligible.

**Branch state addendum (2026-04-29 end-of-day):** `phase2-v0.3-calibration-silverleaf` carries the 2-fix calibration commit `2c56913` from `06d46c5`; pushed. `phase2-v0.3-D1-storage-and-module-wiring` carries D.1 from `2c56913`; single commit at session end; pushed.

**Workspace housekeeping complete (2026-04-29):** Retired / no-longer-needed files moved to `safe_for_removal/` folder per `MARCH_ORDERS_housekeeping_safe_for_removal.md`. Manifest at `safe_for_removal/MANIFEST.md` documents what was moved, why, and what to look at if related issues surface. The folder will be removed in a future session after Daniel reviews; the MANIFEST.md is preserved as a wiki source. Tracked branch: `phase2-v0.3-housekeeping-safe-for-removal` from D.1 head.

For full state detail, read `HANDOFF_FINAL_2026-04-28.md`, then `backend/CALIBRATION_GATE_REPORT_silverleaf.md`, then `backend/D_HARD_GATE_silverleaf.md`.

For empirical verification of any claim above, read `VALIDATION_LEDGER.md`.

---

## 4. The discipline (non-negotiable)

### Karpathy procedure applies to discussions and code

1. **Read first.** Full reads, not partial. The TracePoint paper. CLAUDE.md. The validation ledger. The relevant march orders.
2. **Failing tests first** when writing code. `diff = 0` and SHA-1 match for verbatim ports.
3. **Minimum implementation.** No "while we're in there" expansion.
4. **Sacred floors held** at every verification point.
5. **§7 stops** when something is genuinely uncertain. Don't extrapolate; ask.

### Validation has been done — quote the ledger, don't re-litigate

The validation ledger names every empirical verification with method (SHA-1, `diff`, pytest count, file inspection, git log) and the date it was produced. If you find yourself doubting a claim, find the ledger row, name the method you don't trust, and ask Daniel before re-verifying. Re-verification of already-verified work is the failure mode this document exists to prevent.

If something is NOT in the ledger, it is genuinely unvalidated. Section F of the ledger lists what's unvalidated honestly. Don't pretend speculation is verification.

### Sacred files exist — they don't get touched

Sacred files at end of Phase C.5 (read CLAUDE.md §6 and the validation ledger Section G for the full list):

- Phase 1 frontend HTML
- All TracePoint source at `tracepoint_port/TracePoint/` (read-only reference)
- All v0.2 ported files (`config.py`, `pdf_engine.py`, `zone_filter.py`, `context.py`, `dispatch_gate.py`, `roofing_spec_database.py`, `test_pdf_engine.py`, `test_dispatch.py`)
- All B.1, B.2, B.3, B.4 ported files
- All C.1, C.2 ported files (`trade_module.py`, `roofing_vocabulary.py`, `roofing_module.py`, `trade_input_builder.py`)
- C.3b built file (`backend/core/glazing_vocabulary.py`) — vault-ruled
- C.3c-build files (`backend/core/glazing_module.py`, `backend/tests/test_glazing_module_smoke.py`) — vault-ruled at sealing
- C.5 files (`backend/core/debug_module.py`, `backend/tests/test_debug_module_smoke.py`) — vault-ruled at sealing per the original TracePoint paper §7.5 vault rule plus its trade-module extension
- `backend/core/__init__.py` (kept empty per TracePoint convention)
- `shared/bidset_record.py` (v0.1 schema; v0.2.1 ticket scope)
- All seed files (`roofing_materials.py`, `roofing_spec_database.py`, `roof_assemblies.py`, `glazing_assemblies.py`, `glazing_materials.py`)

**Vault rule** (CLAUDE.md §3 Decision 15, extended 2026-04-28): the following are vault-ruled and MUST NOT be modified in the same session that touches any other `backend/core/` file. Tuning happens in dedicated sessions with `core/` frozen.

- `backend/core/roofing_module.py` (C.2; vault-ruled retroactively D-8)
- `backend/core/roofing_vocabulary.py` (C.2; vault-ruled retroactively D-8)
- `backend/core/glazing_vocabulary.py` (C.3b; vault-ruled retroactively D-8)
- `backend/core/glazing_module.py` (C.3c-build; vault-ruled at sealing)
- `backend/core/debug_module.py` (C.5; vault-ruled at sealing — applies to all six sections, stubbed and ported alike)

Modifying a sacred or vault-ruled file requires explicit user approval at a phase gate. NOT in-session.

### The dispatch_gate storage activation gate stays at None

B.4 ported the storage layer but did NOT wire it. `run_dispatch()` calls still pass `storage=None`. Activation is a Phase D or Phase E decision when database/job-folder structure is finalized. Do not activate it before then.

### Anti-patterns to refuse

- **No "while we're in there" scope expansion.** Even if a fix is small, even if it's obvious. Ticket it; address in its phase.
- **No fabricated validation.** "Validated against X" requires X actually run through the pipeline. Quality scores without an evaluation set are not measurements.
- **No threshold tuning on STACK-only or public-archive-only corpora.** Tuning waits for supplier-sourced non-STACK bidsets that haven't arrived yet. Even when they arrive, tuning is a separate phase with its own march orders.
- **No schema "improvements" from outside sources.** Schema decisions are driven by TracePoint canonical structure (PlanSetContext) and Phase D's job-aware extensions. External proposals (e.g., the Grok-produced v3.5 BidsetRecord schema with fabricated Sanibel validation) are not imported.
- **No silent pivots.** When a march orders document is ambiguous, stop and ask. The §7 stop pattern is the model.
- **No speculation patches.** The B-16/17/18 anti-pattern (three consecutive patches without diagnostics) is named explicitly in CLAUDE.md §9. Diagnostic before production code.

---

## 5. The communication norms

Daniel is a non-developer, project owner, working under engineering-grade discipline. He runs sessions with extended-thinking Claude (planning/review) and Claude Code (execution).

**Discipline signals:**
- "Karpathy logic" → discipline is slipping. Stop. Re-read CLAUDE.md and authoritative documents. Restart from a measured position.
- "Continue" → resume signal between sessions.
- "Standing by" → the right closing for Claude.
- A blunt directive ("do X, no more Y") → take it at face value. Don't second-guess.

**Style:**
- Brutal honesty. No sugar-coating. No flattery. He says so explicitly.
- Push back when you disagree with reasoning. Agreement-with-everything is the failure mode.
- Match the conversational register. No bullet-points or emojis in casual replies.

**On Daniel's time:**
- He has explained the project state more times than he should have. Reduce that load.
- If something is in the validation ledger, it's validated. Don't make him re-explain.
- If something is genuinely unclear, ASK — don't probe with unauthorized diagnostics.

---

## 6. Things that are NOT what someone might think

A short list of common misconceptions a fresh Claude session might form, each corrected:

- **"The frontend has 138 tests."** No. The workspace file is `Huckleberry_AI_6_3_1_Scope.html` (v6.3.1, 107 tests). The 138 figure is from a v6.3.5 file that is NOT in the current workspace. Use the runner's actual output as the floor.
- **"v0.2 has the full TracePoint pipeline."** No. v0.2 ported only Layer 3 (dispatch gate / Filters 1–5). Phase B (B.1 through B.4) added Stages 2–12 plus architect-profile + storage + correction_store. Phase B is what completes the pipeline port.
- **"Huckleberry is a roofing program."** No. It's a multi-trade commercial-construction-takeoff platform. Roofing is the first trade module to ship. Glazing, siding, etc. are queued for Phase C.
- **"Pass 1 of the intake diagnostic showed the dispatch gate is broken."** No. Pass 1 surfaced an asymmetry that LOOKED actionable. Pass 2 (context inspection of 35 hits) found that 29 of 35 were manufacturer mentions in non-roofing contexts (sealants, drywall, etc.) — same brand names, different product lines. The asymmetry largely dissolved. The gate was doing approximately what it was designed to do.
- **"Auto-notation feasibility has been validated."** No. It is an explicitly UNVALIDATED hypothesis (Validation Ledger Section F). It cannot be measured without a ground-truth corpus that doesn't exist yet. Don't claim it's validated.
- **"SQLite in storage.py is a bug to fix."** No. SQLite is the deliberate, Daniel-approved decision (2026-04-27, reversed from earlier "Postgres adaptation" plan). Postgres is deferred to Phase D where multi-tenant job-folder data lives architecturally. Backend cache for dispatch/profile is a different concern.
- **"v0.2 should be re-validated."** No. v0.2 was validated with a 4-symptom STACK study. Receipts in `backend/V0_2_VALIDATION.md`, sealed at v0.2 ship 2026-04-25.
- **"The parked glazing seeds are validated."** No. The C.3a diagnostic (`backend/C3_GLAZING_SEED_VALIDATION.md`, 2026-04-28) is one-bidset preliminary evidence on a single-story Florida retail bidset (Shoppes-at-Avalon). The verdict is "usable as a starting vocabulary with documented gaps," not "validated." `glazing_materials.py` self-identifies as a SKELETON / STUB; `glazing_assemblies.py` has not been reviewed by a practicing glazing estimator. Treat C.3a as evidence, not calibration.
- **"The TracePoint debug module is part of the Phase B port and just hasn't shipped yet."** Updated 2026-04-28 (post-C.5): the debug module **was ported partially in C.5** as `backend/core/debug_module.py`. Sections 1 (dispatch health), 3 (page intelligence), 6 (legend contents + quality flags) are verbatim from the TracePoint source (SHA-1 `b5a4cf93ca7c02116fc00f6dc5a1514da1b18b60` at port time). Sections 2 (scale comparison), 4 (cross-reference graph), 5 (geometry diagnostics) are stubbed with documented `stub_marker` dicts pending external state Huckleberry doesn't yet have (scale-engine route, networkx + sheet-index, geometry results respectively). Vault-ruled at sealing per CLAUDE.md §3 Decision 15 and the original TracePoint paper §7.5. Smoke test + Taco-Bell bidset run-through both passed; receipts in `backend/C5_DEBUG_RUN_THROUGH_taco-bell-weeki-wachee-compass-construction-management-2.md`. Unstubbing of sections 2/4/5 is a future phase decision (D/E).
- **"The three-bidset sweep is when the modules get tuned."** No, and the sweep is now complete (2026-04-28). The sweep ran dispatch + RoofingModule + GlazingModule + run_debug against Shoppes-at-Avalon (97 pp), Vine Street (138 pp), and Bearss Ave (91 pp), and produced three descriptive observation reports under `backend/SWEEP_OBSERVATION_*.md`. Modules were vault-ruled and untouched throughout: zero `backend/core/` modifications, zero new dependencies, zero new tests. The reports are descriptive only — no grading, no correctness comparison, no "needs ground truth" labels, no fix lists, no tuning recommendations. Per-page module error rate was 0.00% across all three bidsets and both modules. Tuning, if any, happens in dedicated future sessions with `core/` frozen, per CLAUDE.md §3 Decision 15. Whether tuning is the next phase or whether C.4 (cross-trade relationships) goes first is Daniel's call after he reviews the three reports — see §8 below.

If you're tempted to act on a misconception in this list, find the row in the validation ledger that contradicts it. The verification is named there.

---

## 7. The phased recovery path (high-level)

Just so every session knows the trajectory. Detail is in `CLAUDE.md` §5.

| Phase | What | Status |
|---|---|---|
| A | Close v0.2 properly (push, ship v0.2.1, schema migration) | Pre-scoped, NOT started |
| **B** | **Port rest of TracePoint to backend (B.1, B.2, B.3, B.4)** | **COMPLETE 2026-04-27** |
| **C.1** | **Trade module Protocol port + cross-trade integration notes** | **COMPLETE 2026-04-27** (commit `23a459c`) |
| **C.2** | **First concrete trade module: roofing (vocabulary + roofing_module + build_trade_input)** | **COMPLETE 2026-04-27** (commit `74772b6`) |
| C.3a | Glazing seed validation diagnostic (one-bidset preliminary evidence) | COMPLETE 2026-04-28 — verdict: usable as starting vocabulary with documented gaps; receipts in `backend/C3_GLAZING_SEED_VALIDATION.md` |
| **C.3b** | **TradeModuleInput contract extension + glazing_vocabulary build (overlay on parked seeds)** | **COMPLETE 2026-04-28** (commits `7ea9abb`, `14f4f53`) |
| **D-8 follow-up** | **C.3a inventory count corrections + vault rule extension to cover trade modules** | **COMPLETE 2026-04-28** (commit `eb49a08`) |
| **C.3c-build** | **Second concrete trade module: glazing (build-against-contract per Daniel's verbatim spec; first Huckleberry-original module)** | **COMPLETE 2026-04-28** (commits `c656ec6`, `6001042`) — vault-ruled at sealing; ships rough; behavior validation deferred to the three-bidset sweep |
| Debug-module spec | Read-only specification report on TracePoint debug module + port-to-Huckleberry assessment | COMPLETE 2026-04-28 — recommendation: partial port at standalone C.5 sub-phase; receipts in `backend/DEBUG_MODULE_REPORT.md` |
| **C.5** | **Debug-module partial port (sections 1/3/6 verbatim from TracePoint, sections 2/4/5 stubbed pending external state) + Taco Bell bidset run-through verification** | **COMPLETE 2026-04-28** (commits `9025884` + bidset-run-through commit `b569312`) — vault-ruled at sealing; no new dependencies; pushed to remote 2026-04-28; run-through receipts in `backend/C5_DEBUG_RUN_THROUGH_taco-bell-weeki-wachee-compass-construction-management-2.md` |
| **Three-bidset sweep** | **Dispatch + RoofingModule + GlazingModule + debug module run against Shoppes-at-Avalon, Vine Street, Bearss Ave; three descriptive observation reports produced; modules vault-ruled and untouched throughout** | **COMPLETE 2026-04-28** — single commit on local branch `phase2-v0.3-sweep-three-bidsets` from `b569312`; reports at `backend/SWEEP_OBSERVATION_shoppes-at-avalon.md`, `backend/SWEEP_OBSERVATION_vine-street.md`, `backend/SWEEP_OBSERVATION_bearss-ave.md`; per-page module error rate 0.00% across all three bidsets and both modules; sections 2/4/5 stub markers confirmed in all three debug outputs |
| Module tuning sessions | Dedicated sessions with `core/` frozen, vault rule observed (Decision 15) | Available; deferred until tuning data justifies it |
| C.4 | Cross-trade relationships layer (reads `CROSS_TRADE_INTEGRATION_NOTES.md` as starting map; resolves awning/canopy boundary surfaced in C.3b plus anything surfaced in the sweep) | Available; deferred |
| **Calibration — B2607 AEA Silverleaf** | **Dispatch-side iterative refinement; Bug 1 + Bug 3 fixes; tracked harness; vault rule held; receipts in `backend/CALIBRATION_GATE_REPORT_silverleaf.md`** | **COMPLETE 2026-04-29** (commit `2c56913` on `phase2-v0.3-calibration-silverleaf`; pushed) |
| **D.1** | **Storage activation in `run_dispatch` (lazy SQLite via `storage="auto"`) + RoofingModule + GlazingModule wired into production path (Stage 13) + `PlanSetContext.trade_module_outputs` field + Silverleaf hard gate end-to-end** | **COMPLETE 2026-04-29** (single commit on `phase2-v0.3-D1-storage-and-module-wiring` from `2c56913`; pushed) — Silverleaf hard gate PASS all 7 criteria; module output exact parity with calibration iter 2 |
| D.2 | Job folder + multi-tenant identity + schema migration (BidsetRecord → PlanSetContext; D-4 + D-5 v0.2.1 fixes fold here); GC as primary identity | **NEXT-eligible** — Daniel's decision (this OR Phase E below) |
| E | Backend API + frontend strip-and-connect (frontend stops parsing in browser; pulls structured data from backend; Phase 1 v6.3.x HTML preserved as offline fallback) | **NEXT-eligible** — now UNBLOCKED by D.1 |
| F | Auto-notation product (three-state annotations, provenance, training data loop) | NOT started |

Phases are gated. Each gets its own march-orders document drafted by extended-thinking Claude and reviewed by Daniel before Claude Code executes. No phase starts without explicit approval.

---

## 8. The next planning conversation

**Daniel reviews the D.1 hard gate report (`backend/D_HARD_GATE_silverleaf.md`), the calibration gate report (`backend/CALIBRATION_GATE_REPORT_silverleaf.md`), and the new BLOCK_RUN.md Phase 2 section. The next phase is genuinely open — Phase E (backend API + frontend strip-and-connect) OR Phase D.2 (job folder + multi-tenant identity + schema migration) — and is Daniel's call.**

D.1 wired the production call path end-to-end on Silverleaf. `run_dispatch(pdf, storage="auto")` now produces a populated `PlanSetContext` whose `trade_module_outputs` carry per-page `TradeModuleOutput` records from RoofingModule + GlazingModule. Module output is byte-equivalent to calibration iter 2 (338 roofing fields, 20/81/6 glazing). Bidsets remain in-memory + ephemeral SQLite cache; persistent job folders, GC-as-primary-identity, and the multi-tenant data model are explicitly D.2 scope, not D.1.

The decision Daniel is now making:

- **Path (a) — Phase E next.** Backend API surfaces. FastAPI routes that consume `run_dispatch(storage="auto")` and serve `PlanSetContext` + `trade_module_outputs` to the frontend. Frontend strip-and-connect: ROOF_VOCAB, dispatch filters, geometry engine, scope extractors all stop running in the browser; Phase 1 v6.3.x HTML preserved as offline fallback per the Section-6 sacred constraint. Frontend visibility of module output unblocks meaningful tuning iteration. Module tuning, C.4 cross-trade, and D.2 persistence all stay deferred.
- **Path (b) — Phase D.2 next.** Job folder structure (one folder per job, GC as primary identity), multi-tenant Postgres decision (per the long-deferred Decision Q2 reversal — backend cache stays SQLite; Phase D job-folder data is a separate concern), schema migration (BidsetRecord → PlanSetContext extended with job-level entities; D-4 + D-5 v0.2.1 fixes fold here). Persistent state before API. Phase E follows D.2.

Either path ends at the same downstream Phase F (auto-notation product). The order of (a) vs (b) is what the next planning conversation chooses.

Extended-thinking Claude drafts the chosen next phase's march orders once Daniel decides. The march orders document is the gate; Claude Code does not start either path without it.

Module tuning sessions, C.4 cross-trade relationships layer, and (eventually) v0.2.1 schema-migration follow-on items remain on the board but are not in front of E or D.2.

---

## 9. If you are a future Claude session reading this

You have permission to do any of the following:

- Skip ahead to CLAUDE.md, the validation ledger, and the latest handoff
- Push back on Daniel when you have reasoned disagreement
- Stop and ask when something genuinely doesn't fit (§7 stop)
- Refuse to do unauthorized work (anti-patterns above)
- Match gate density to actual work risk (verbatim ports = autonomous; design work = gated; novel code = heaviest gating)

You do NOT have permission to:

- Re-validate things in the ledger without first quoting the row and naming the method you don't trust
- Speculate about state that isn't in the canonical documents
- Probe with unauthorized diagnostics
- Run the intake diagnostic again (it's been run twice; conclusions are documented)
- Tune any TracePoint-ported file's calibrated thresholds
- Propose new schemas from outside sources
- Start a phase without a march-orders document and Daniel's approval
- Make Daniel re-explain validated facts

If you read this and ALL FOUR canonical documents and still doubt something, ask Daniel directly with the specific concern named. That's the right move. Probing the codebase or re-running diagnostics to "verify for yourself" is not.

---

## 10. The single rule

**The validation ledger says what's been done. The handoff says what's happening now. CLAUDE.md says what the project is and what the discipline is. This document tells you to read all three before doing anything else.**

That's it. The whole rule.

If every session starts here and reads in order, the loop breaks.

---

**End of PROJECT_CLAUDE.md.**
