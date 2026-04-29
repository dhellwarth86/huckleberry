# MARCH ORDERS — Calibration Session: B2607 AEA Silverleaf

**Date issued:** 2026-04-29
**Issued by:** Daniel (via extended-thinking Claude planning session)
**Executed by:** Claude Code
**Phase shape:** Single session, autonomous, fix-allowed (dispatch-side only), iterative, hard iteration ceiling, single final gate report
**Read first:** PROJECT_CLAUDE.md, CLAUDE.md, VALIDATION_LEDGER.md, then this document

---

## §0 — What this phase is

**First calibration session of the program.** Iterative refinement of dispatch's output against a real bidset (B2607 AEA Silverleaf — smallest in workspace, chosen for tight iteration cycles), using the debug module as the diagnostic surface. This is the discipline established in CLAUDE.md §3 Decision 15 (vault rule: tuning sessions, `core/` frozen for vault-ruled modules, dispatch-side mutable) and the TracePoint paper §3.1 (diagnostic-first development).

This is **NOT another verification phase.** Code changes are explicitly authorized within scope. The job is to look at debug output, identify the worst single problem, fix it in dispatch, re-run, observe the delta, repeat.

The vault rule applies. The five vault-ruled modules — `roofing_module.py`, `glazing_module.py`, `roofing_vocabulary.py`, `glazing_vocabulary.py`, `debug_module.py` — are NOT touched this session. If a tuning impulse points at any of them, document it for a future module-tuning session and move on. Calibration this session is **dispatch-side only.**

This phase leads into Phase D (storage + job folder + module wiring), with Daniel's soft gate between them as the go/no-go decision. The calibration session's job is to produce a cleaner Silverleaf baseline that Phase D will then plumb through end-to-end.

**Open questions explicitly accepted as scope:** Bug 1 (page-type ordering), Bug 3 (trade_input_builder contract drift). The verification phase data supports both. This session is authorized to fix them dispatch-side. Bug 3's fix path is a real architectural choice — Path (a) cache to PlanSetContext, Path (c) extend `_parse_tables_on_page` — and the calibration session picks one and ships it, with the choice documented.

**Open questions explicitly OUT of scope:** trade module tuning of any kind, vault-ruled module changes, frontend changes, dependency additions, schema migration, storage activation.

---

## §1 — Pre-flight reads (Karpathy step 1)

Full reads, in this order:

1. **PROJECT_CLAUDE.md** — entry point. Note §3's coverage of the open path forward, §4's vault rule restatement, §6's misconceptions list.
2. **CLAUDE.md** — §3 Decision 15 (vault rule). §6 hard guardrails. §9 anti-patterns.
3. **VALIDATION_LEDGER.md** — sacred floor (216/19/0 backend), existing rows for sweep, profile, page-type verification.
4. **`backend/PAGE_TYPE_VERIFICATION_GATE_REPORT.md`** — the data that ordered this session.
5. **`backend/PAGE_TYPE_VERIFICATION_filter4_cache_audit.md`** — the Bug 3 architectural surface (Path a/b/c).
6. **`backend/PAGE_TYPE_VERIFICATION_bearss-ave.md`** — Block 5 evidence of what's at stake.
7. **`backend/core/dispatch_gate.py`** lines 100–135, 421–470, 733–878, 1440–1505. Architectural anchor.
8. **`backend/core/trade_input_builder.py`** — entire file (~150 lines).
9. **`backend/core/context.py`** — PlanSetContext + PageContext field lists.
10. **`backend/core/trade_module.py`** — `TradeModuleInput` definition with the C.3b `tables` field.
11. **`backend/scripts/sweep_three_bidsets.py`** — harness pattern reuse for the calibration runner.
12. **`backend/scripts/profile_diagnostic.py`** — for harness shape conventions.

**Do NOT read** the five vault-ruled modules. They are not in scope this session.

---

## §2 — Step Cal.0: Pre-flight verification

- Run the full backend suite. Floor: **216 passed, 19 skipped, 0 failed**. Hard stop if not met.
- Run the four frontend test suites at sacred floors: `run_tests.js` 107/107, spotchecks 7/4/8/14, mutations 8/8 caught.
- Verify branches:
  - `phase2-v0.3-page-type-verification` head = `06d46c5` (current; pushed)
- Locate **B2607 AEA Silverleaf** PDF at `C:/huck stage 2/full bid sets/` (or workspace equivalent path the prior phases used). Filename match should include "Silverleaf" — confirm before proceeding.
- Capture page count and file size. If the bidset is >50 pages, **§7 stop** — Daniel said this was the smallest set; if it isn't, the wrong file may have been picked.
- Confirm `git remote -v` shows `https://github.com/dhellwarth86/huckleberry.git`.

---

## §3 — Step Cal.1: Branch + create BLOCK_RUN.md

Branch from current head:

```
phase2-v0.3-calibration-silverleaf  (NEW; from 06d46c5)
```

**Create `backend/BLOCK_RUN.md` at session start.** This is the master ledger for the calibration → Phase D → Phase E chain. It is created in this session and persists/extends across the next two phases.

Initial structure:

```markdown
# Block Run — Master Ledger

**Purpose:** Single chronological log of every file created, modified, or deleted, every commit, every push, every config or schema change across the calibration → Phase D → Phase E chain. Updated at the end of each phase. Read top-to-bottom for "what's been touched" without re-reading march orders or gate reports.

**Started:** 2026-04-29 by calibration session on B2607 AEA Silverleaf.
**Phases this ledger spans:** calibration-silverleaf, phase-D-storage-and-wiring, phase-E-backend-api.

---

## Phase 1: Calibration — B2607 AEA Silverleaf (2026-04-29)

**Branch:** `phase2-v0.3-calibration-silverleaf` (from `06d46c5`)
**Trigger:** Daniel directive 2026-04-29 — first calibration session of program; dispatch-side only; iterative; vault rule active on five trade modules.

### Files created
(populate as work proceeds)

### Files modified
(populate as work proceeds)

### Files deleted
None expected.

### Commits
(populate as work proceeds)

### Pushes
(populate as work proceeds)

### Dependency / config changes
None expected. (No `pyproject.toml`, no schema, no new deps.)

### Vault-ruled files touched
None. (Vault rule active throughout — `roofing_module.py`, `glazing_module.py`, `roofing_vocabulary.py`, `glazing_vocabulary.py`, `debug_module.py` not modified, not opened.)

---

## Phase 2: Phase D — storage activation + job folder + module wiring (TBD)

(Populated by Phase D session.)

---

## Phase 3: Phase E — backend API + frontend consumption (TBD)

(Populated by Phase E session.)

---
```

Update BLOCK_RUN.md as work proceeds — Claude Code adds to the populated sections at end of session.

---

## §4 — Step Cal.2: Build the calibration runner harness

Create `backend/scripts/calibrate_silverleaf.py` (tracked — reusable template for future per-bidset calibration sessions).

The runner:

1. Loads B2607 AEA Silverleaf PDF.
2. Calls `run_dispatch(pdf_path, storage=None)` → PlanSetContext. Captures wall-clock.
3. For each page, builds a `TradeModuleInput` (using whatever the harness pattern is; reuse the sweep harness's approach for consistency). Note: this DOES call the existing trade_input_builder.py path post-Bug-3-fix; the entire point of this session is that that builder now populates `tables`.
4. Calls `RoofingModule().analyze(input)` per page; aggregates into `roofing_outputs`.
5. Calls `GlazingModule().analyze(input)` per page; aggregates into `glazing_outputs`.
6. Constructs `DebugContext`, calls `run_debug(ctx)` — captures the full debug output.
7. Writes the run output to `backend/CALIBRATION_RUN_silverleaf_iter_<N>.md` where `<N>` is the iteration number (0, 1, 2, ...).

**Iteration 0 is the BASELINE** — no fixes applied. Captures the starting state.

Each subsequent iteration runs with one targeted fix applied (see §5).

The harness has a hard cap: **maximum 4 iterations** (baseline + 3 fix iterations). If 3 fixes don't materially clean the output, stop and surface as a soft observation. Do not loop indefinitely.

Each iteration's report uses this skeleton:

```markdown
# Calibration Run — Silverleaf — Iteration <N>

**Date:** 2026-04-29
**Iteration:** <N> of max 4
**Fix applied this iteration:** <description, or "BASELINE — no fix" for iter 0>
**Wall-clock:** dispatch <s> / modules <s> / debug <s> / total <s>

## §1 — Dispatch output summary

- detected_system / confidence / scope_pages
- dispatch_complete / filters_completed / dispatch_warnings
- total_pages / sheet_count / mapped_pages
- page_type histogram

## §2 — Module output summary

- Roofing: per-page non-empty count, total fields, total warnings
- Glazing: per-page non-empty count, total glazing/door/storefront items

## §3 — Debug section 1 / 3 / 6 highlights

- Section 1 dispatch_health key fields
- Section 3 page_intelligence: count of pages with each type, count of has_legend pages
- Section 6 legend_count + quality_flags raised (full list)

## §4 — Delta from previous iteration (skip for iter 0)

- Page_type histogram delta
- Section 6 quality_flags delta (added / resolved)
- Total tables extracted (if Bug 3 fix landed: were any populated this iteration?)
- Wall-clock delta (sometimes fixes change runtime — record it)

## §5 — Worst single problem identified (for next iteration's fix)

(One paragraph: what's the next problem to fix? Quote the debug output that surfaces it. This becomes iter <N+1>'s target.)

## §6 — Iteration log
```

The harness should print to stdout AND save to file. Use a Tee pattern as the verification phase did.

---

## §5 — Step Cal.3: Iterative refinement loop

This is the meat of the session. The loop:

### Iteration 0: Baseline

- Run the harness with NO fixes applied.
- Save `CALIBRATION_RUN_silverleaf_iter_0.md`.
- Read debug section 1 / 3 / 6 output.
- Identify the **single worst problem** — the most-impactful issue visible in debug output. Likely candidates based on prior data:
  - Page-type misclassification (Bug 1 surface) — visible in section 3's page_type distribution
  - Empty `tables` field on TradeModuleInput (Bug 3 surface) — visible because glazing/roofing per-page output looks suspiciously sparse on schedule pages
  - Quality flags from section 6 emitted at high count
  - dispatch_warnings noise
- Document the worst problem in §5 of iter 0's report.

### Iteration 1: First fix (likely Bug 1)

Bug 1 is the most-likely first fix because:
- Verification confirmed it structurally
- Fix is small (~2-line change in `_PAGE_TYPE_RULES`)
- It's the upstream of Bug 2 (Filter 4 gate)
- Fixing it doesn't require an architectural decision

**Fix shape (suggested, not mandated):** Move the SCHEDULE rule to position 0 in `_PAGE_TYPE_RULES`. Make this change in `dispatch_gate.py` directly. Document the change in BLOCK_RUN.md and in the iter 1 report.

**Side effect to watch:** the verification phase data showed 57 NEW misclassifications under simple SCHEDULE-first ordering. Iter 1 should explicitly check whether those new misclassifications cause downstream noise (section 3 reports a bunch of false-positive schedule_sheet pages, section 6 quality flags spike, etc.). If they do, iter 1's "worst single problem identified" for iter 2 might be "SCHEDULE rule needs whole-word scoping or precedence refinement."

Run harness → save `iter_1.md` → §4 captures the delta → §5 identifies next problem.

### Iteration 2: Second fix (likely Bug 3 plumbing OR Bug 1 refinement)

Two paths depending on what iter 1 surfaced:

**Path A: Bug 3 plumbing.** If iter 1's output shows tables are still empty everywhere (because the C.3b contract field was never populated), iter 2 fixes Bug 3.

The verification phase produced three architectural fix-paths from the Filter 4 cache audit:
- (a) Cache field to PlanSetContext or PageContext
- (b) Per-page re-extraction in trade_input_builder
- (c) Extend `_parse_tables_on_page` to optionally cache raw tables

**Recommendation: Path (c).** Single-touch dispatch-side. Doesn't violate any verbatim-port relationships. Doesn't pay extract_tables cost twice. The change: `_parse_tables_on_page` already calls `page.extract_tables()` and discards the raw tables after wrapping in Legend objects. Modify it to also store raw tables on the relevant `page_ctx` (probably as `page_ctx.raw_tables: list[list[list]]` or similar). Then extend `trade_input_builder.py` to read `page_ctx.raw_tables` and populate `TradeModuleInput.tables`.

If Claude Code prefers Path (a) for some empirical reason, document the choice in BLOCK_RUN.md. Both are dispatch-side, both are vault-respecting. Path (b) is forbidden — it's the harness workaround we're getting rid of.

**Path B: Bug 1 refinement.** If iter 1's 57 new misclassifications caused real noise, iter 2 makes the ordering more surgical. Likely shape: whole-word match (`\bSCHEDULE\b` regex) instead of substring; or "if both SCHEDULE and another keyword match, prefer SCHEDULE" precedence rule.

Run harness → save `iter_2.md` → §4 captures the delta → §5 identifies next problem.

### Iteration 3: Final fix or stop

If iter 2 cleaned things meaningfully, iter 3 picks the new worst problem and fixes it.

If iter 2 didn't clean things, **stop** and document why. The hard cap is 3 fix iterations.

If by iter 3 the output looks clean — section 6 quality flags low or stabilized, page_type distribution looks right, tables populated — that's a successful calibration. Save iter 3, no further iterations.

### Stop conditions for the loop (any one ends iteration)

- **3 fix iterations completed.** Hard cap.
- **Section 6 quality_flags reach zero or stabilize across two consecutive iterations.** Diminishing returns.
- **No clearly identifiable "worst single problem" remains.** Surface as success — section 5 of the final report says "no further dispatch-side issue obvious; remaining surface is module tuning territory."
- **A fix attempt regresses sacred floor.** Hard stop. Revert the fix, do not continue.
- **A fix attempt would require touching a vault-ruled module.** Hard stop. Document the impulse, do not fix this session.

---

## §6 — Discipline reminders (Karpathy)

1. **Read first.** Full §1 docs before any code change. Especially `dispatch_gate.py` lines 100–135 and 733–878 — the Bug 1 + Bug 3 anchor zones.
2. **Sacred floor first.** 216/19/0 backend before, after each iteration, after final commit, after push.
3. **Minimum implementation per fix.** Each iteration fixes ONE thing. Not "while I'm in here also tune X." If iter 1 is the page-type ordering, that's the only change in iter 1. The next problem becomes iter 2's job.
4. **Vault rule held.** Five vault-ruled modules untouched and not opened.
5. **Calibration is fix-allowed but not tuning-allowed.** "Calibration" = adjust dispatch's structural output (classification, plumbing, gate behavior). "Tuning" = adjust trade module output quality (vocabulary thresholds, regex coverage, confidence calibration). Calibration: yes. Tuning: NO. The trade modules are vault-ruled; their output quality is locked until a future tuning session.
6. **Each iteration's report is observation + ONE fix description.** The iteration narrative isn't "this is broken because X." It's "iter N applied fix Y; debug shows Z changed; next problem is W."
7. **§5 in each iteration report names the SINGLE worst problem.** Don't list five things to fix. Pick one. The hard ceiling is 3 fixes; profligate problem-listing wastes iteration budget.

---

## §7 — §7 Stop Conditions

Stop, report, wait for Daniel if any fire:

1. **Sacred floor regresses.** Backend below 216/19/0 or frontend below baseline. Hard stop. Revert the iteration's fix.
2. **Silverleaf PDF cannot be located** or is >50 pages. Stop and ask.
3. **Dispatch raises** on Silverleaf. Hard stop. Revert the iteration's fix that caused the raise.
4. **A fix attempt would require touching a vault-ruled module.** Hard stop. Document the tuning impulse for a future session, do not proceed.
5. **A fix attempt would require modifying any non-dispatch `backend/core/` file** (`trade_module.py` itself, `architect_profile.py`, etc.). Hard stop. Calibration is dispatch-side only; the C.3b contract is already in place.
6. **A fix attempt would require adding a dependency.** Hard stop.
7. **An iteration regresses something previously working.** Soft observation if minor; hard stop if it's a regression on the calibration's own previous iteration's gains.
8. **3 fix iterations complete and output is no cleaner than baseline.** NOT a §7 stop in the strict sense, but a clear signal to stop and surface — the calibration approach didn't work for this bidset, and that's important data for the soft gate.
9. **Bug 3 Path (c) implementation reveals an unanticipated architectural concern** (e.g., `_parse_tables_on_page` is on a different ownership boundary than expected, or storing raw tables doubles memory in a way that breaks something). Hard stop. Document and surface.

---

## §8 — Done definition (gate report checklist)

The final gate report (`backend/CALIBRATION_GATE_REPORT_silverleaf.md`) must confirm:

- [ ] Pre-flight: 216/19/0 backend; frontend at baselines; Silverleaf located and ≤50 pages
- [ ] `backend/scripts/calibrate_silverleaf.py` written, tracked, runs cleanly
- [ ] `backend/BLOCK_RUN.md` created at session start; populated at session end with all touches
- [ ] Iteration 0 (baseline) report saved at `backend/CALIBRATION_RUN_silverleaf_iter_0.md`
- [ ] At least 1 fix iteration completed; iter reports saved up to last iteration
- [ ] Each fix iteration's report identifies ONE single worst problem and applies ONE fix
- [ ] Final iteration's report says either "calibration converged" or "ceiling reached at iter <N>"
- [ ] Bug 1 status: fixed in iter <N> (likely 1) — page-type ordering change documented
- [ ] Bug 3 status: addressed in iter <N> (likely 2) — Path (a)/(b)/(c) choice documented; OR explicitly deferred with reason
- [ ] No `roofing_module.py`, `glazing_module.py`, `roofing_vocabulary.py`, `glazing_vocabulary.py`, `debug_module.py` modification (verified by SHA-1 at session start AND end)
- [ ] No `pyproject.toml` change
- [ ] dispatch_gate.py changes: documented per-line in BLOCK_RUN.md, single-purpose per iteration
- [ ] trade_input_builder.py changes: only as required by chosen Bug 3 fix path
- [ ] Backend suite still 216/19/0 (zero new tests added)
- [ ] Frontend at baseline
- [ ] Single commit on `phase2-v0.3-calibration-silverleaf`; pushed to origin
- [ ] §7 stops: status of each enumerated explicitly
- [ ] Final gate report produced
- [ ] BLOCK_RUN.md fully populated with this phase's section

---

## §9 — Commit shape

**Single commit** on `phase2-v0.3-calibration-silverleaf`:

- `backend/scripts/calibrate_silverleaf.py` (NEW — tracked harness)
- `backend/CALIBRATION_RUN_silverleaf_iter_0.md` (NEW)
- `backend/CALIBRATION_RUN_silverleaf_iter_<1..N>.md` (NEW for each iteration that ran)
- `backend/CALIBRATION_GATE_REPORT_silverleaf.md` (NEW — gate report)
- `backend/BLOCK_RUN.md` (NEW)
- `backend/core/dispatch_gate.py` (MODIFIED — fixes)
- `backend/core/trade_input_builder.py` (MODIFIED — if Bug 3 Path c)
- `backend/core/context.py` (MODIFIED — if Bug 3 Path a; or to add a `raw_tables` field per Path c)

Commit message body: list each iteration's fix on its own line; final state of dispatch_gate.py / trade_input_builder.py / context.py changes summarized; SHA-1 confirmation that vault-ruled modules unchanged; backend test count.

Push at end of session. Authorized.

---

## §10 — Soft gate at session end

After the gate report lands and BLOCK_RUN.md is updated, **Daniel reviews and decides**:

- **If calibration looks good** → green-light Phase D march orders.
- **If calibration looks rough but salvageable** → discuss what's still off, possibly run a follow-up calibration session before Phase D.
- **If calibration uncovers something architectural we didn't expect** → reframe the path forward.

**This is a soft gate, not a hard gate.** Daniel's decision happens between sessions; Phase D's march orders get drafted by extended-thinking Claude based on the calibration outcome. Phase D doesn't auto-start.

The hard gate is the **Silverleaf re-run after Phase D ships** — Phase D's success criterion is that Silverleaf runs end-to-end through the wired pipeline (storage activated, modules wired, job folder structure in place) and produces output equivalent to or better than the calibration session's final iteration.

---

## §11 — Execution mode

**Single chunk, autonomous, soft gates only within the iteration loop.** Each iteration is a unit. Between iterations, the harness runs autonomously — no per-iteration confirmation needed from Daniel.

§7 stops are the only hard pauses. At the hard cap (3 fix iterations), the loop stops on its own.

Total wall-clock estimate: 4 iterations × (~2 min dispatch + ~4 min modules + ~30s debug + harness overhead) ≈ 30–45 minutes; plus harness write, fix coding, commit, push, BLOCK_RUN.md update — total session ≈ 1.5–2 hours.

---

## §12 — Closing

After this phase ships:

1. Daniel reviews `CALIBRATION_GATE_REPORT_silverleaf.md` first, then iteration deltas
2. Soft gate: green-light Phase D, or follow-up calibration, or reframe
3. **Phase D march orders drafted by extended-thinking Claude** — storage activation, job folder structure, module wiring in dispatch_gate, schema migration
4. Phase D ships
5. **Hard gate: re-run Silverleaf through Phase D's wiring** — verify end-to-end equivalent or better than calibration final iter
6. **Phase E march orders drafted** — backend API, frontend consumption, debug module integration in production wiring
7. Phase E ships
8. **PROJECT_CLAUDE.md updated** to reflect calibration + D + E complete
9. **BLOCK_RUN.md updated** with all of D and E's touches

This calibration session is the leadoff. Standing by for execution.

**End of MARCH_ORDERS_calibration_silverleaf.md.**
