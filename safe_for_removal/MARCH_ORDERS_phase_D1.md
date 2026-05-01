# MARCH ORDERS — Phase D: Storage Activation + Module Wiring + Silverleaf Hard Gate

**Date issued:** 2026-04-29
**Issued by:** Daniel (via extended-thinking Claude planning session)
**Executed by:** Claude Code
**Phase shape:** Single session, autonomous, soft-gates-only, single final gate report
**Phase scope (compressed):** D.1 — storage activation + RoofingModule + GlazingModule wired into dispatch + Silverleaf hard gate end-to-end through `build_trade_input`. Job folder structure, multi-tenant identity, schema migration, and v0.2.1 are NOT in this phase — they are deferred to a future D.2 phase.
**Read first:** PROJECT_CLAUDE.md, VALIDATION_LEDGER.md, BLOCK_RUN.md, then this document

---

## §0 — Scope and explicit non-scope

### What this phase is

Wire what was rough-built in C.2 / C.3c-build / C.5 / calibration into dispatch's actual production path. End-to-end Silverleaf flow validated as the hard gate.

Specifically:

1. **Activate storage** — `dispatch_gate.run_dispatch(pdf_path, storage=None)` currently takes None. Wire it to a real SQLite-backed storage implementation per CLAUDE.md (retired) Decision Q2 (2026-04-27): "SQLite stays verbatim in storage.py. Postgres deferred to Phase D." That decision lives in `VALIDATION_LEDGER.md §H` and is honored here.
2. **Wire RoofingModule + GlazingModule into dispatch's flow** — currently both modules are called manually by harnesses (sweep, profile, calibration). This phase wires the production call path: when `run_dispatch` completes, modules run automatically per page using `build_trade_input` (now Bug 3-fixed) and produce real `TradeModuleOutput` per page on the PlanSetContext.
3. **Hard gate: re-run Silverleaf end-to-end through the wired pipeline** — the success criterion is that Silverleaf produces output equivalent to or better than the calibration session's iter 2 final state. Equivalence measured against the calibration baseline.

### What this phase is NOT

- **NOT job folder structure.** Bidsets remain in-memory + ephemeral SQLite cache for now. Persistent job-folder identity, GC-as-primary-identity, and the multi-tenant data model are deferred to D.2 with their own march orders.
- **NOT schema migration.** v0.2.1 schema work (D-4 + D-5 fixes) folds into D.2.
- **NOT Postgres.** SQLite stays.
- **NOT trade module tuning.** Vault rule active on all five vault-ruled modules. The wiring exposes module output to the production path; it does not modify what modules produce.
- **NOT a Phase E preview.** No FastAPI work. No frontend wiring. No HTTP endpoints. Phase E is its own phase.
- **NOT auto-notation.** Phase F.

### What this phase is allowed to touch (in priority order)

- `backend/core/dispatch_gate.py` — wire storage; wire module call path
- `backend/core/storage.py` — confirm port, light edits if needed (currently sealed B.4 verbatim port; vault-ruled? **No** — storage.py is NOT in the vault-ruled list per VALIDATION_LEDGER.md §G; modifications allowed but minimal)
- `backend/core/context.py` — extend PlanSetContext with optional fields for per-page TradeModuleOutput results IF needed
- `backend/core/trade_input_builder.py` — already Bug 3-fixed in calibration; possibly minor hardening this phase
- `backend/scripts/calibrate_silverleaf.py` — re-run for hard gate (or new equivalent harness; see §7)
- `backend/PROJECT_CLAUDE.md` — single canonical doc edit at end of session
- `backend/BLOCK_RUN.md` — populate Phase 2 section
- `backend/D_HARD_GATE_silverleaf.md` — new gate report
- `backend/scripts/d1_silverleaf_hardgate.py` — new harness if needed

### What this phase MUST NOT touch (vault-ruled, sacred, or Daniel-retired)

| File | Why | Verification |
|---|---|---|
| `backend/core/roofing_module.py` | Vault-ruled (CLAUDE.md retired §3 Decision 15) | SHA-1 must match pre-session at session end |
| `backend/core/glazing_module.py` | Vault-ruled at C.3c-build sealing | SHA-1 must match |
| `backend/core/roofing_vocabulary.py` | Vault-ruled | SHA-1 must match |
| `backend/core/glazing_vocabulary.py` | Vault-ruled | SHA-1 must match |
| `backend/core/debug_module.py` | Vault-ruled at C.5 sealing | SHA-1 must match |
| `frontend/Huckleberry_AI_6_3_1_Scope.html` (or whatever the workspace canonical is) | **TREATED AS VAULTED for Phase D** — Daniel directive 2026-04-29: frontend is sacred until Phase E does the strip-and-connect work | SHA-1 must match pre-session at session end |
| `CLAUDE.md` (if it still exists in workspace) | **Daniel retired this file** — moved into "old orders" archive 2026-04-29. Do not open, do not edit, do not reference. | If file exists in workspace, leave it untouched; do not even open it for reading |
| All TracePoint sources at `tracepoint_port/TracePoint/` | Read-only reference | n/a |
| All seed files in `backend/seeds/` | Sacred | SHA-1 must match |
| `backend/tests/` directory contents | Sacred per the no-new-tests floor in this phase | Test file count must match pre-session |

### Canonical doc ground rule

**PROJECT_CLAUDE.md is the only canonical document edited in this phase.** Daniel directive 2026-04-29: CLAUDE.md retired (moved to old-orders archive). Do not open, do not edit, do not reference CLAUDE.md. If you encounter "see CLAUDE.md §X" in a doc, treat it as a historical pointer; the substantive content of those decisions has been migrated to PROJECT_CLAUDE.md and VALIDATION_LEDGER.md.

If a march orders or older artifact references CLAUDE.md, do not chase the reference — work from what's in PROJECT_CLAUDE.md, VALIDATION_LEDGER.md, and the calibration gate report. If a substantive question can ONLY be answered by CLAUDE.md, that is a §7 stop, not a "let me just take a peek" exception.

### Frontend ground rule

The frontend HTML file (`Huckleberry_AI_6_3_1_Scope.html` or whatever the actual workspace canonical filename resolves to) is **vault-treated for Phase D.** Daniel directive 2026-04-29: frontend is treated as sacred and untouched until Phase E does the strip-and-connect work.

This means:

- Do not modify the frontend HTML for any reason.
- Do not run the frontend test suite at the end if the frontend file isn't touched (but DO run it at pre-flight, to verify the baseline is at start of session).
- Do not "while we're in there" any frontend cleanup.
- Frontend SHA-1 captured at session start, verified at session end, committed to BLOCK_RUN.md.

The frontend version question (107 vs 138) flagged in calibration's gate-report review remains open for Phase E to resolve. Do not resolve it here. Do not investigate it here. Just verify whatever file is at the start-of-session SHA-1 is at the end-of-session SHA-1.

---

## §1 — Pre-flight reads (Karpathy step 1)

Full reads, in this order:

1. **PROJECT_CLAUDE.md** — entry point. Note §3's calibration completion. Note the discipline rules in §4.
2. **VALIDATION_LEDGER.md** — sacred floors (216/19/0 backend, frontend baselines whatever they are). §G vault-ruled list. §H Q2 (SQLite stays). §D existing rows.
3. **BLOCK_RUN.md** — Phase 1 (calibration) entries. You are extending this file in the same shape, not restructuring it.
4. **`backend/CALIBRATION_GATE_REPORT_silverleaf.md`** — what calibration produced. The hard gate compares against this baseline.
5. **`backend/CALIBRATION_RUN_silverleaf_iter_2.md`** — final calibration iteration's output. The numerical baseline for hard gate comparison.
6. **`backend/core/dispatch_gate.py`** — full read this time, all 1,726 lines or thereabouts. You are wiring storage and modules into `run_dispatch`; you need to know the whole flow.
7. **`backend/core/storage.py`** — read entirely. Understand its API. This is what `run_dispatch` activates against. Ported B.4 verbatim per VALIDATION_LEDGER §A. Dataclass: `Storage` (or whatever the class name resolves to in the actual file).
8. **`backend/core/context.py`** — full read. PlanSetContext, PageContext, related dataclasses. You may extend with new optional fields; you will not redefine existing ones.
9. **`backend/core/trade_input_builder.py`** — confirm post-calibration shape (Bug 3 fix landed: reads `page_ctx.raw_tables`, populates `TradeModuleInput.tables`).
10. **`backend/core/trade_module.py`** — confirm `TradeModule` Protocol, `TradeModuleOutput` shape (with C.3b additive fields glazing_items / door_items / storefront_items).
11. **`backend/scripts/calibrate_silverleaf.py`** — read for harness pattern reuse.

Read-only inspection of the five vault-ruled modules is **NOT NEEDED** for this phase. Do not open them. The modules are consumed via their public Protocol surface; you don't need to read implementation.

---

## §2 — Step D.0: Pre-flight verification

- Run the full backend suite. Floor: **216 passed, 19 skipped, 0 failed**. Hard stop if not met.
- Run the frontend test suite at sacred baseline (whatever the workspace v6.3.1 file produces). Capture the count. Recording baseline before any work.
- Capture frontend file SHA-1 at session start. (You will verify at session end.)
- Capture pre-session SHA-1 of all five vault-ruled modules. (You will verify at session end.)
- Verify branch `phase2-v0.3-calibration-silverleaf` is at expected head (calibration commit `2c56913` or whatever the actual final calibration SHA is; read BLOCK_RUN.md to confirm).
- Locate **B2607 AEA Silverleaf** PDF at the workspace path the calibration session used. Same path, same file.
- `git remote -v` confirms `https://github.com/dhellwarth86/huckleberry.git`.
- Confirm CLAUDE.md is NOT opened during pre-flight reads. If it's in the workspace file tree, do not click into it. (PROJECT_CLAUDE.md is the canonical replacement.)

---

## §3 — Step D.1: Branch + BLOCK_RUN.md preparation

Branch from calibration head:

```
phase2-v0.3-D1-storage-and-module-wiring  (NEW; from calibration head)
```

Open `backend/BLOCK_RUN.md`. Locate the "Phase 2: Phase D" section that's a stub. Replace the `(Populated by Phase D session.)` placeholder with the populated section header — but leave the actual file/commit lines empty until session end. The header looks like:

```markdown
## Phase 2: Phase D — storage activation + module wiring (D.1) (2026-04-29)

**Branch:** `phase2-v0.3-D1-storage-and-module-wiring` (from calibration head)
**Trigger:** Daniel directive 2026-04-29 — green-light Phase D after calibration soft-gate review; D scoped to storage activation + module wiring + Silverleaf hard gate; D.2 (job folder, multi-tenant, schema migration) deferred to its own future phase.
**Scope discipline:** Single session, auto-run, no CLAUDE.md touches (file retired by Daniel), PROJECT_CLAUDE.md is only canonical doc edited, frontend vault-treated.

### Files created
(populate at session end)

### Files modified
(populate at session end)

### Files deleted
None expected.

### Commits
(populate at session end)

### Pushes
(populate at session end)

### Dependency / config changes
None expected. SQLite (already in pyproject.toml from B.4) is what storage activates.

### Vault-ruled files touched
None. (Vault rule active. SHA-1 verification at session end.)

### Frontend touched
None. (Frontend vault-treated for Phase D per Daniel directive. SHA-1 verification at session end.)
```

This populates as work proceeds; final cleanup at session end.

---

## §4 — Step D.2: Activate storage in dispatch

Open `backend/core/dispatch_gate.py` and locate the `run_dispatch(pdf_path, storage=None)` function.

The current call site (calibration ran with `storage=None`) means the architect-profile detection block at lines ~1483–1489 short-circuits. We are activating storage.

**Activation pattern:** within `run_dispatch`, if the caller passes `storage=None`, lazily construct a default `Storage` instance (using the SQLite implementation already in `storage.py`). The activation should:

- Use a default cache path under `backend/cache/dispatch.sqlite` (or wherever the storage layer's convention puts it; read `storage.py` to find out).
- Be idempotent — multiple `run_dispatch` calls in the same session should reuse one storage instance.
- Not break existing tests. Current `test_dispatch.py` tests that pass `storage=None` should continue to pass — meaning either the new default storage activation is silent (creates a tmp file, doesn't pollute test fixtures) OR the test signature accommodates the new default.

If existing tests would fail under the new default, prefer this shape: keep `storage=None` as the no-op signature for tests AND add a new `storage="default"` (string sentinel) or `storage="auto"` parameter that triggers lazy SQLite construction. The production call from D's wiring uses `storage="auto"`.

**Documentation:** for every line modified, add an inline comment `# D.1: <reason>`. Ex: `# D.1: lazy default SQLite storage activation per Phase D march orders §4`.

Confirm `dispatch_gate.run_dispatch(pdf_path, storage="auto")` runs against Silverleaf without raising. (This is a §6 sanity check, not the hard gate.)

---

## §5 — Step D.3: Wire RoofingModule and GlazingModule into the production call path

Currently RoofingModule and GlazingModule are called by harnesses (sweep, profile, calibration). We are wiring them as part of dispatch's standard completion path.

**Wiring pattern (proposed; adjust to fit existing dispatch_gate.py shape):**

After all five filters complete and before `run_dispatch` returns, add a "Stage 13" block that:

1. For each page in `PlanSetContext.pages`:
   - Build a `TradeModuleInput` via `trade_input_builder.build_trade_input(...)`. This is the production path — it now reads `page_ctx.raw_tables` (Bug 3 fix from calibration) and populates `TradeModuleInput.tables`.
   - Call `RoofingModule().analyze(input)` — store result.
   - Call `GlazingModule().analyze(input)` — store result.
2. Aggregate per-page module outputs onto a new field on `PlanSetContext`. **Add a new optional field**: `trade_module_outputs: dict[int, dict[str, TradeModuleOutput]] = field(default_factory=dict)` — mapping page_idx → trade_name → TradeModuleOutput. (`context.py` modification, additive only, default empty dict, existing tests untouched.)
3. Run `RoofingModule` and `GlazingModule` instances are constructed once per `run_dispatch` call (not per-page) for efficiency.

**Failure handling:**

- If `build_trade_input` raises on a page: skip that page's trade modules, log to `ctx.dispatch_warnings`, continue with the next page.
- If `RoofingModule.analyze` raises on a page: skip roofing for that page only, log to dispatch_warnings, continue with glazing.
- If `GlazingModule.analyze` raises on a page: skip glazing for that page only, log, continue.
- If error rate >25% across all pages × either module: §7 stop. (Same threshold as the sweep had, applied to the wired path.)

**Constraint:** module output is appended to context but NOT yet exposed via API or persisted to a job folder. That's D.2's work. Phase D's job is just to make the wired call path produce correct in-memory output that the Silverleaf hard gate can verify.

**Documentation:** every wiring line gets an inline `# D.1: <reason>` comment.

---

## §6 — Step D.4: Sanity check before hard gate

Before running the Silverleaf hard gate, do a quick sanity check:

- Run `backend/scripts/calibrate_silverleaf.py` (the calibration harness from Phase 1) — does it still run cleanly under the new storage-activated, module-wired dispatch?
- The calibration harness's iter 2 output should be reproducible. If it isn't (e.g., wiring changed something the calibration didn't expect), back up and investigate before proceeding to hard gate.
- Run the full backend test suite. Floor: 216/19/0. Hard stop if regressed.
- Capture vault-ruled module SHA-1s — verify still match pre-session.
- Capture frontend SHA-1 — verify still matches pre-session.

This sanity check is not a §7 stop in itself — it's a checkpoint. If it surfaces a problem, address it in the wiring before hard gate; don't push a known-broken state to the hard gate.

---

## §7 — Step D.5: Silverleaf hard gate — end-to-end through wired pipeline

Build (or extend) a harness: `backend/scripts/d1_silverleaf_hardgate.py`. Tracked, reusable.

The harness runs Silverleaf through the **wired** production path:

```python
from core.dispatch_gate import run_dispatch
from core.debug_module import run_debug, DebugContext

ctx = run_dispatch(silverleaf_path, storage="auto")
# Modules already ran during run_dispatch via D.3 wiring.
# Aggregate from ctx.trade_module_outputs (no manual per-page loop).

debug_ctx = DebugContext(plan_set_context=ctx, trade_contexts={...from ctx.trade_module_outputs...})
debug_output = run_debug(debug_ctx)
```

Capture:
- Wall-clock for `run_dispatch` (now includes module wiring time)
- Aggregate module output: total roofing fields, total glazing/door/storefront items, per-page error counts
- Debug section 1, 3, 6 output
- `ctx.dispatch_warnings`

Save the result to `backend/D_HARD_GATE_silverleaf.md` using a structure modeled on the calibration iter 2 report.

**Hard gate criteria** — Silverleaf via wired pipeline must produce:

1. **Equivalent or better module output** vs calibration iter 2:
   - Calibration iter 2 produced 338 roofing fields, 20 glazing / 81 door / 6 storefront items.
   - Hard gate: should produce at least 90% of those numbers (allowing for small wiring-induced variance) AND no new exceptions.
2. **Equivalent or better dispatch wall-clock**: should not regress more than 30% vs calibration iter 2's 59.3s. (Wiring adds module call time, which is expected; the budget accommodates that.)
3. **Tables populated correctly**: at least the 18 schedule_sheet pages should have non-empty `TradeModuleInput.tables`. Verify by inspecting `ctx.pages[idx].raw_tables` directly on schedule_sheet pages.
4. **dispatch_warnings**: same shape as calibration iter 2 (one Filter 4 quality gate warning is expected; new warnings about module wiring are acceptable if they're informational).
5. **No vault-ruled module modification**: SHA-1 verification.
6. **Sacred floor**: backend 216/19/0 still passing.
7. **Frontend untouched**: SHA-1 verification.

If any criterion fails, **§7 stop with full traceback**. Do not paper over.

---

## §8 — Step D.6: Update PROJECT_CLAUDE.md

After hard gate passes, update PROJECT_CLAUDE.md to reflect Phase D.1 complete.

**Specific edits, surgical:**

- **§1 (canonical documents table):** drop the row referencing CLAUDE.md (Daniel retired the file 2026-04-29). Renumber subsequent rows. Update entry-point note to read: "PROJECT_CLAUDE.md, VALIDATION_LEDGER.md, latest handoff, active march orders." That's three canonical docs now, not four.
- **§3 (where the project stands):** add a paragraph for "Phase D.1 complete (2026-04-29):" — storage activated, RoofingModule + GlazingModule wired into `run_dispatch`, Silverleaf hard gate passed, `ctx.trade_module_outputs` field on PlanSetContext now populated by production path. Reference the gate report by filename.
- **§3 update test floor** if backend count changed (it should NOT — D.1 is wiring not new tests; if it changed, surface as soft observation).
- **§3 update branch state**: D.1 branch added.
- **§7 (phase table):** D.1 → COMPLETE; D.2 (job folder + schema + multi-tenant) → NEXT; E → NOT YET DRAFTED but unblocked by D.1.
- **§8 (next planning conversation):** rewrite to reflect "Phase E — backend API (now unblocked); OR Phase D.2 — job folder structure and schema migration. Daniel chooses; extended-thinking Claude drafts next phase's march orders."

Do NOT modify §2, §4, §5, §6, §9, §10. Do NOT touch CLAUDE.md (file retired). VALIDATION_LEDGER.md gets minor updates per §10 below; that's allowed because it's empirical receipts, not "canonical doc work."

---

## §9 — Step D.7: Update VALIDATION_LEDGER.md (minor)

Append two rows:

- **§D row** — "Silverleaf hard gate end-to-end (D.1, measured 2026-04-29)" with headline numbers from the hard gate report.
- **§A row** — `dispatch_gate.py` D.1 modifications documented (lazy storage activation, module wiring, +N lines, all comment-tagged `# D.1:`). Same row format as B.1/B.2/B.3/B.4 entries.

These are additive ledger updates, not restructuring.

---

## §10 — Step D.8: Populate BLOCK_RUN.md Phase 2 section

At session end, fill in the Phase 2 section of BLOCK_RUN.md with all touches:

- Files created
- Files modified
- Files deleted (none)
- Commits (commit SHA + message)
- Pushes
- Dependency / config changes (none expected)
- Vault-ruled files touched: confirm none, with SHA-1s
- Frontend touched: confirm none, with SHA-1

---

## §11 — §7 Stop Conditions

Stop, report, wait for Daniel if any fire:

1. **Sacred floor regresses.** Backend below 216/19/0. Frontend SHA-1 changes. Either is a hard stop.
2. **Vault-ruled module SHA-1 changes** during the session. Hard stop. Investigate the regression source.
3. **CLAUDE.md gets opened or edited.** Should not happen — file is retired. If it does, hard stop.
4. **PROJECT_CLAUDE.md edits exceed §6 surgical scope.** §1, §3, §7, §8 are allowed targets. Other sections require §7 stop.
5. **Silverleaf hard gate fails any criterion in §7 of these orders.** Specifically:
   - Module output drops below 90% of calibration iter 2 numbers
   - Dispatch wall-clock regresses more than 30%
   - Tables not populated on schedule_sheet pages
   - Backend tests regress
6. **Per-page module error rate >25%** during hard gate. (Same threshold as sweep.) Hard stop.
7. **`storage.py` requires substantial modification** to activate — i.e., the B.4 port has a real bug that surfaces only when storage is exercised. Hard stop. Document and surface. Don't speculate-fix.
8. **`run_dispatch` raises** during D.2 (storage activation) or D.3 (module wiring) on Silverleaf. Hard stop with traceback.
9. **A test added in D.1** — D.1 is wiring + verification, not new test coverage. If you find yourself wanting to add a test, that signals scope creep; document the impulse for D.2 and move on.
10. **A new dependency is needed.** SQLite is already there from B.4. No other dep should be needed for D.1. Hard stop if otherwise.
11. **Frontend file is opened for any reason.** Even read-only inspection. Vault-treated means untouched; SHA-1 verification at session end is the only frontend interaction this phase.

---

## §12 — Discipline reminders (Karpathy)

1. **Read first.** All §1 docs in full. PROJECT_CLAUDE.md, VALIDATION_LEDGER.md, BLOCK_RUN.md, calibration gate report, calibration iter 2 report, dispatch_gate.py, storage.py, context.py, trade_input_builder.py, trade_module.py, calibrate_silverleaf.py.
2. **Sacred floor first.** 216/19/0 backend before pre-flight, after each step, after final commit.
3. **Minimum implementation.** Activate storage. Wire two modules. Hard-gate Silverleaf. Don't add features. Don't add tests. Don't refactor "while I'm in here."
4. **Vault rule held.** Five vault-ruled modules untouched and not opened. Frontend untouched and not opened.
5. **CLAUDE.md retired.** Do not open. Do not reference. PROJECT_CLAUDE.md is the canonical entry point now.
6. **PROJECT_CLAUDE.md is the only canonical doc you edit.** VALIDATION_LEDGER.md gets additive ledger rows; that's not "doc editing" in the canonical-state sense — it's receipt logging.
7. **D scope is COMPRESSED to D.1.** Job folder structure, multi-tenant identity, schema migration are D.2's job, not D.1. If you find yourself thinking "I should also add X for the multi-tenant case" — stop. That's D.2.
8. **Hard gate is empirical.** The calibration iter 2 numbers are the baseline. If the wired pipeline can't reproduce or improve those numbers, the wiring has a bug. Don't hand-wave; verify.

---

## §13 — Done definition (gate report checklist)

The final gate report (`backend/D_HARD_GATE_silverleaf.md`) must confirm:

- [ ] Pre-flight: 216/19/0 backend; frontend at baseline; vault-ruled SHA-1s captured; frontend SHA-1 captured
- [ ] Branch `phase2-v0.3-D1-storage-and-module-wiring` from calibration head
- [ ] Storage activated in `run_dispatch` with documented `# D.1:` line tags
- [ ] RoofingModule + GlazingModule wired into `run_dispatch` post-Filter-5
- [ ] `PlanSetContext.trade_module_outputs` field added (additive, default empty dict)
- [ ] Silverleaf runs end-to-end through wired pipeline without exception
- [ ] Silverleaf hard gate passes all 7 criteria in §7 of orders
- [ ] No vault-ruled module modification (5 SHA-1s match pre-session)
- [ ] Frontend SHA-1 matches pre-session (vault-treated)
- [ ] CLAUDE.md not opened, not edited
- [ ] No new dependencies (`pyproject.toml` unchanged)
- [ ] No new tests added (test file count unchanged; backend 216/19/0 unchanged)
- [ ] PROJECT_CLAUDE.md updated per §6 (sections §1, §3, §7, §8 only)
- [ ] VALIDATION_LEDGER.md additive updates per §7 (ledger rows in §A and §D)
- [ ] BLOCK_RUN.md Phase 2 section populated per §8
- [ ] `backend/D_HARD_GATE_silverleaf.md` saved with hard gate empirical comparison vs calibration iter 2
- [ ] Single commit on `phase2-v0.3-D1-storage-and-module-wiring`; pushed to origin
- [ ] §7 stops: status of each enumerated explicitly
- [ ] Final gate report produced

---

## §14 — Commit shape

**Single commit** on `phase2-v0.3-D1-storage-and-module-wiring`:

- `backend/core/dispatch_gate.py` (MODIFIED — storage activation + module wiring; line-tagged `# D.1:`)
- `backend/core/context.py` (MODIFIED — `trade_module_outputs` field added; additive)
- `backend/core/storage.py` (MODIFIED only if §11 #7 didn't fire — likely no change or trivial only)
- `backend/scripts/d1_silverleaf_hardgate.py` (NEW — tracked harness)
- `backend/D_HARD_GATE_silverleaf.md` (NEW — gate report)
- `backend/PROJECT_CLAUDE.md` (MODIFIED — §1, §3, §7, §8)
- `backend/VALIDATION_LEDGER.md` (MODIFIED — additive rows in §A and §D)
- `backend/BLOCK_RUN.md` (MODIFIED — Phase 2 section populated)

Commit message body:
- D.1 scope (one line)
- Storage activation lines added (count)
- Module wiring lines added (count)
- Hard gate result (PASS/FAIL with key numbers)
- Vault-ruled SHA-1 confirmation
- Frontend SHA-1 confirmation
- §7 stops fired (none expected)

Push at end of session. Authorized.

---

## §15 — Execution mode

**Single chunk, autonomous, soft gates within steps.** Run D.0 through D.8 without per-step confirmation. Single final gate report at end.

§7 stops are the only hard pauses. The §6 sanity-check checkpoint is not a stop; it's a course correction opportunity.

Total wall-clock estimate: ~30 minutes pre-flight + reads, ~30 minutes wiring code, ~10 minutes hard gate run on Silverleaf (40 pages), ~15 minutes doc updates + commit + push, ~15 minutes buffer = **~100 minutes total session.**

---

## §16 — Closing

After D.1 ships and PROJECT_CLAUDE.md is updated, **Daniel reviews**:

1. The hard gate report empirical comparison vs calibration iter 2
2. PROJECT_CLAUDE.md §3's new Phase D.1 paragraph
3. BLOCK_RUN.md Phase 2 section

The next planning conversation chooses:
- **Phase E** (backend API + frontend strip-and-connect) — NOW UNBLOCKED by D.1
- **Phase D.2** (job folder + schema migration + multi-tenant identity) — also next-eligible
- **Trade module tuning sessions** — also next-eligible (independent path)

Extended-thinking Claude drafts the chosen next phase's march orders.

D.1 is the wiring. D.2 is the persistence. E is the API. F is the product. One step at a time, single session each, with discipline.

Standing by for execution.

**End of MARCH_ORDERS_phase_D1.md.**
