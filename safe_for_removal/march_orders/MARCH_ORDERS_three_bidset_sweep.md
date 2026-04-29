# MARCH ORDERS — Three-Bidset Sweep (Shoppes-at-Avalon / Vine Street / Bearss Ave)

**Date issued:** 2026-04-28
**Issued by:** Daniel (via extended-thinking Claude planning session)
**Executed by:** Claude Code
**Phase shape:** Single session, autonomous, soft-gates-only, single final gate report
**Read first:** PROJECT_CLAUDE.md, CLAUDE.md, VALIDATION_LEDGER.md, HANDOFF_FINAL_2026-04-28.md, then this document

---

## §0 — What this phase is

Three things, in order:

1. **Push the local-only branch stack to remote.** C.3c-build (`phase2-v0.3-C3c-glazing-module`, commits `c656ec6` + `6001042`) and C.5 (`phase2-v0.3-C5-debug-module-port`, commits `9025884` + `b569312`) are sealed, vault-ruled, and proven on bench. Push order matters: C.3c-build first (so C.5 references are valid on remote), then C.5. Both push to `https://github.com/dhellwarth86/huckleberry.git`.

2. **Run the three-bidset sweep.** For each of three bidsets — Shoppes-at-Avalon, Vine Street, Bearss Ave — run `run_dispatch()` to produce a PlanSetContext, then iterate over its pages and call `RoofingModule().analyze(input)` + `GlazingModule().analyze(input)` per page, then call `run_debug(ctx)` once with all per-page outputs aggregated into the DebugContext's `trade_contexts`. Save the entire output as a structured markdown observation report per bidset.

3. **Update PROJECT_CLAUDE.md** to reflect both the push and the sweep ship.

This phase produces **descriptive observation reports**. Not grades. Not correctness comparisons. Not "needs ground truth" labels. Not fix lists. Not tuning recommendations. Pure observation. The sweep is the input to a future planning conversation about what comes next (module tuning vs. C.4 cross-trade design); it is NOT itself any of those.

---

## §1 — The observation-only norm (read this twice)

**This is the load-bearing discipline for this phase.** Read it slowly.

While running this sweep, you WILL see output that looks wrong. Roofing fields will be sparse on bidsets where the trade is barely present. Glazing items will over-pull on pages where door schedules collide with glazing callouts. Debug section 6 quality flags will fire on real bidsets in ways that look noisy. Manufacturer matching will miss obvious brands; mark extraction will catch tokens that aren't really marks; confidence scores will look uncalibrated; section 1's dispatch_health may flag "low scope confidence" for trades that actually exist in the bidset.

**That is the entire point of the sweep.** The modules are vault-ruled. They were shipped rough on purpose. The sweep is the diagnostic surface that informs the future tuning session — which is its own phase, with its own march orders, with `core/` frozen, in a dedicated session.

**Your reports are observation, not analysis.** Every closing per-bidset note is an "observed:" statement. Never "should be:" or "recommend:" or "this looks like a bug in:" or "the next session should fix:". If you find yourself writing one of those, delete it and rewrite as observation.

**Examples of correct observation language:**

- "Page 18 produced 3 roofing fields with confidence 0.92, 0.84, 0.76. No equipment pins emitted on this page despite presence of 'TPO MEMBRANE' in adjacent text."
- "Glazing module produced 47 door items across 12 pages. 31 of the 47 carry mark 'D-100' through 'D-199'. No door items emitted on pages 1–7 (title pages and code summaries)."
- "Debug section 6 emitted 14 quality flags. 9 are LegendSourceTagFlag, 3 are PageIntelligenceFlag, 2 are CrossReferenceFlag (the latter consistent with section 4 stub state)."

**Examples of forbidden language:**

- "The roofing module is missing material X. The vocabulary needs Y."
- "Confidence calibration is off — 0.92 here is overconfident."
- "Section 6 over-flags. Threshold should be raised."
- "This looks like a bug in `_extract_marks`."

If your gut says "this is broken," the report says "observed:" and describes what you saw. That's the entire job. The future tuning session reads these reports; the future tuning session decides what to fix. You do not.

The only exception is a literal traceback. A traceback during dispatch or module call is a §7 stop, not an observation.

---

## §2 — Pre-flight reads (Karpathy step 1)

Full reads, in this order, before any execution:

1. **PROJECT_CLAUDE.md** — entry point. Note §3's existing language about the sweep ("descriptive observation reports; no grading, no correctness comparison, no 'needs ground truth' labels per Daniel's 2026-04-28 directive"). Note §6's misconceptions list including "the sweep is when modules get tuned" (no — observation only).
2. **CLAUDE.md** — §3 Decision 15 (vault rule, current vault list including `roofing_vocabulary.py`, `glazing_vocabulary.py`, `roofing_module.py`, `glazing_module.py`, `debug_module.py`). §6 hard guardrails. §9 anti-patterns.
3. **VALIDATION_LEDGER.md** — sacred floors (216/19/0 backend, all frontend baselines).
4. **HANDOFF_FINAL_2026-04-28.md** — recent state.
5. **`backend/C3_GLAZING_SEED_VALIDATION.md`** — the C.3a diagnostic on Shoppes-at-Avalon. This is the only existing observation artifact for any of the sweep bidsets. Do not "validate against" it; just note that Shoppes has prior characterization.
6. **`backend/C5_DEBUG_RUN_THROUGH_taco-bell-weeki-wachee-compass-construction-management-2.md`** — the C.5 verification artifact. The shape of this artifact is the closest existing template for what this sweep's reports look like, but they include trade module output too. Use it as a structural reference, not a content template.
7. **`backend/core/trade_input_builder.py`** — to learn the contract for building TradeModuleInput per page.
8. **`backend/core/roofing_module.py`** (read-only) — to confirm the public surface (`RoofingModule().analyze(input) → TradeModuleOutput`).
9. **`backend/core/glazing_module.py`** (read-only) — to confirm the public surface (`GlazingModule().analyze(input) → TradeModuleOutput` with `glazing_items` / `door_items` / `storefront_items`).
10. **`backend/core/debug_module.py`** (read-only) — confirm `DebugContext` shape and what `run_debug(ctx)` reads from `ctx.trade_contexts`.

**Reading these read-only files for shape confirmation does NOT violate the vault rule.** The vault rule prohibits modification, not inspection. The sweep script needs to know the contracts to call them correctly.

---

## §3 — Step Sweep.0: Pre-flight verification

- Run the full backend suite. Floor: **216 passed, 19 skipped, 0 failed**. If not met, stop and report.
- Run the four frontend test suites at sacred floors: `run_tests.js` 107/107, `spotcheck_10b.js` 7/7, `spotcheck_cricket.js` 4/4, `spotcheck_durolast.js` 8/8, `spotcheck_manufacturer.js` 14/14, `mutation_test_step11.js` 8/8 caught.
- Verify both C.3c-build and C.5 branches exist locally with expected commit hashes:
  - `phase2-v0.3-C3c-glazing-module` head = `6001042`
  - `phase2-v0.3-C5-debug-module-port` head = `b569312`
- Locate all three bidsets in the workspace. Conventions established by C.3a and C.5: bidsets live under `backend/data/bidsets/` or equivalent path. Names to look for:
  - **Shoppes-at-Avalon** — characterized in `backend/C3_GLAZING_SEED_VALIDATION.md`; filename is whatever C.3a referenced
  - **Vine Street** — uncharacterized; locate by name match
  - **Bearss Ave** — uncharacterized; locate by name match
- If any bidset cannot be located, **§7 stop**. Do not substitute another bidset; ask Daniel.
- Confirm `git remote -v` shows `https://github.com/dhellwarth86/huckleberry.git` and that auth is intact (the previous push 2026-04-28 worked).

---

## §4 — Step Sweep.1: Push C.3c-build and C.5 to remote

Two pushes, in order:

```
git push origin phase2-v0.3-C3c-glazing-module
git push origin phase2-v0.3-C5-debug-module-port
```

Order matters: C.5 was branched from C.3c-build's head (`6001042`); pushing C.3c-build first ensures C.5's parent commit exists on remote when C.5 pushes.

Confirm both branches appear on `origin` after push. Capture push output (commit ranges, branch tracking confirmation) for the gate report.

If either push fails (auth, conflict, anything), **§7 stop**. Do not retry with `--force`. Do not modify any commit. Stop and report.

---

## §5 — Step Sweep.2: Branch for sweep work

Branch from C.5 head (`b569312`) on `phase2-v0.3-C5-debug-module-port`:

```
phase2-v0.3-sweep-three-bidsets  (NEW; from b569312)
```

The sweep itself produces no production-code commits. The only commit on this branch is the three observation reports + the PROJECT_CLAUDE.md update at end of session (single commit; see §10).

The sweep script (see §6) is a one-shot verification artifact, NOT committed — same pattern as C.5's run-through script. If you want a permanent sweep tool, that's a separate phase with proper test coverage. This phase keeps the script untracked.

---

## §6 — Step Sweep.3: Write the sweep script

Create `backend/scripts/sweep_three_bidsets.py` (working tree only, NOT committed). The script:

### Imports

```python
from core.dispatch_gate import run_dispatch
from core.trade_input_builder import build_trade_input  # or whatever the actual name is
from core.roofing_module import RoofingModule
from core.glazing_module import GlazingModule
from core.debug_module import run_debug, DebugContext
```

If `trade_input_builder.py` exposes a different function name or shape, adapt accordingly. The contract is: build a TradeModuleInput per page from the PlanSetContext. Read `trade_input_builder.py` once before writing the script to learn the actual interface.

### Per-bidset run procedure

For each bidset:

1. Call `run_dispatch(pdf_path, storage=None)` → `PlanSetContext`. Capture wall-clock time.
2. Initialize empty lists: `roofing_outputs_per_page = []`, `glazing_outputs_per_page = []`.
3. For each page in `PlanSetContext.pages`:
   - Build a `TradeModuleInput` for this page using `build_trade_input` (or the C.2-established equivalent).
   - Call `RoofingModule().analyze(input)` → store result in `roofing_outputs_per_page` keyed by page number.
   - Call `GlazingModule().analyze(input)` → store result in `glazing_outputs_per_page` keyed by page number.
4. Construct `DebugContext`:
   - `plan_set_context = pc`
   - `trade_contexts = {"roofing": <aggregated roofing per-page outputs>, "glazing": <aggregated glazing per-page outputs>}` — exact aggregation shape per whatever `debug_module.py` section 6 reads. If unsure of shape, store the per-page lists as-is and let section 6 emit whatever it emits; the sweep is observation, not optimization.
5. Call `run_debug(ctx)` → debug output dict.
6. Hand all four outputs (PlanSetContext, roofing per-page, glazing per-page, debug dict) to a report-formatting function.
7. Write the formatted report to `backend/SWEEP_OBSERVATION_<bidset_short_name>.md`.

### Failure handling

If dispatch raises during any bidset, **§7 stop**. Do not skip the bidset. Do not catch-and-continue. Stop, report the traceback, wait for Daniel.

If a trade module raises on a specific page, soft-recover for that page only: log "trade module raised on page N: <exception type>: <first 200 chars of message>" into the report's per-page section, and continue with remaining pages. **This is NOT a §7 stop** because trade modules running on per-page input can hit edge cases that aren't whole-bidset failures; the observation report should record where they hit. But: if a trade module raises on more than 25% of pages in any single bidset, that becomes a §7 stop — that signals a contract-shape issue, not an edge case.

### What the script does NOT do

- Does not modify any backend/core/ file.
- Does not add any dependency to pyproject.toml.
- Does not create any pytest tests (the sweep produces artifacts, not regression coverage).
- Does not call `_scope` pseudo-field handling differently than the modules emit it; just passes through.
- Does not "fix" any output that looks wrong.
- Does not make any judgment about correctness.

---

## §7 — Step Sweep.4/5/6: Run the sweep on all three bidsets

Run the script three times (or once with all three bidsets — your choice; both are valid). Bidset order:

1. **Shoppes-at-Avalon** (has prior C.3a characterization; sanity-check baseline)
2. **Vine Street** (uncharacterized)
3. **Bearss Ave** (uncharacterized)

Each run produces one report at `backend/SWEEP_OBSERVATION_<short_name>.md`. Suggested filenames (use whatever `<short_name>` cleanly maps to the actual bidset filename):

- `backend/SWEEP_OBSERVATION_shoppes-at-avalon.md`
- `backend/SWEEP_OBSERVATION_vine-street.md`
- `backend/SWEEP_OBSERVATION_bearss-ave.md`

### Report structure (use this skeleton for each)

```markdown
# Sweep Observation Report — <Bidset Display Name>

**Date:** 2026-04-28
**Phase:** Three-bidset sweep
**Bidset file:** <full path or filename>
**Page count:** <N>
**File size:** <KB or MB>
**Wall-clock dispatch time:** <seconds>

## §1 — Bidset Metadata

(Filename, page count, file size, source/contractor if known from filename or C.3a-style prior characterization, note "uncharacterized" for Vine Street / Bearss Ave.)

## §2 — Dispatch Output (PlanSetContext)

### project_scope
- detected_system: <value or null>
- confidence: <value or null>
- scope_pages: <list>

### dispatch_complete: <True/False>
### filters_completed: <list>
### dispatch_warnings: <list, full content>
### total_pages: <N>
### sheet_count: <N>
### mapped_pages: <N>

## §3 — Roofing Module Output

### Per-page summary table

| Page | Fields produced | Warnings | Equipment pins |
|------|-----------------|----------|----------------|
| 1    | 0               | 0        | 0              |
| ...  | ...             | ...      | ...            |

### Aggregated
- Total fields produced across all pages: <N>
- Total warnings: <N>
- Total equipment pins: <N>
- Pages with non-empty output: <N>
- Pages with empty output: <N>

### Per-page detail (only pages with non-empty output)

#### Page <N>

```json
{
  "fields": { ... },
  "warnings": [ ... ],
  "equipment_pins": [ ... ]
}
```

(Repeat for each page with content.)

## §4 — Glazing Module Output

### Per-page summary table

| Page | glazing_items | door_items | storefront_items |
|------|---------------|------------|------------------|
| ...  | ...           | ...        | ...              |

### Aggregated
- Total glazing_items across all pages: <N>
- Total door_items: <N>
- Total storefront_items: <N>
- Pages with any glazing module content: <N>
- Pages with empty output: <N>

### Per-page detail (only pages with non-empty output)

(Same format as §3 — JSON-like dumps for pages with content. Skip empty pages.)

## §5 — Debug Module Output

### Section 1 — dispatch_health
```json
{ ... full dump ... }
```

### Section 2 — scale_comparison (STUB)
- stub_marker confirmed: `C.5_partial_port_pending_scale_engine_route`

### Section 3 — page_intelligence
- Page entry count: <N>
- (Sample of first 3 entries shown below; full dump omitted for size if >50 pages)

```json
[ <first 3 entries or all if ≤50 pages> ]
```

### Section 4 — cross_reference_graph (STUB)
- stub_marker confirmed: `C.5_partial_port_pending_networkx_and_sheet_index`

### Section 5 — geometry_diagnostics (STUB)
- stub_marker confirmed: `C.5_partial_port_pending_geometry_results`

### Section 6 — legend_and_quality_flags
- Legend count: <N>
- Quality flag count: <N>
- Quality flags raised:

```json
[ <full list> ]
```

## §6 — Per-Page Errors (if any)

(List any pages where a trade module raised during analyze(). Format: page N, module name, exception type, first 200 chars of message. Empty section if no errors.)

## §7 — Closing

Observation only. No grades. No fixes proposed. No tuning recommendations. The roofing module and glazing module are vault-ruled per CLAUDE.md §3 Decision 15. The debug module is vault-ruled per the same. Tuning is a future phase with `core/` frozen.

(Optional: 3–5 plain "observed:" statements describing what stood out. NEVER "should be:", "recommend:", or "looks like a bug:". If you can't write a statement in pure observation language, omit it.)
```

### What the reports are and aren't

- **Are:** the diagnostic surface for the future tuning planning conversation.
- **Are:** the input to whether C.4 (cross-trade relationships) design proceeds or whether tuning sessions come first.
- **Are not:** correctness scores.
- **Are not:** ground-truth comparisons (no ground truth exists for these bidsets at the trade-module-output level).
- **Are not:** fix lists.
- **Are not:** "needs ground truth" labels (per Daniel's 2026-04-28 directive in PROJECT_CLAUDE.md §3).

---

## §8 — Step Sweep.7: Update PROJECT_CLAUDE.md

After all three observation reports are saved, update `PROJECT_CLAUDE.md` to reflect both the push and the sweep ship.

Specific edits:

- **§3** — Update branch state: C.3c-build and C.5 are now pushed. Move them from "local-only" to "pushed 2026-04-28." Note the sweep observation reports by filename (3 of them). Add the sweep itself to the completed-phases narrative — descriptive observation only, modules vault-ruled and untouched, three reports saved as raw input for the future tuning planning conversation.
- **§4** — Sacred files list: the three sweep observation reports are reference artifacts (not sacred), so do NOT add them to the sacred list. Vault rule subsection unchanged (no new vault-ruled files; the sweep modified zero modules).
- **§6** — The misconception "the three-bidset sweep is when modules get tuned" can be sharpened: the sweep IS COMPLETE and produced descriptive reports; no tuning happened. Update phrasing to past tense where appropriate.
- **§7** — Phase table: "Three-bidset sweep" → COMPLETE with date and report filenames. The next entry depends on Daniel's decision after reviewing reports — leave both options open: "Module tuning sessions" and "C.4 cross-trade relationships layer" both move to "NEXT — Daniel's decision after reviewing observation reports."
- **§8** — Rewrite to reflect the genuinely open choice: "Next planning conversation: Daniel reviews the three observation reports. Decision: (a) module tuning sessions next, with `core/` frozen and dedicated sessions per module, OR (b) proceed to C.4 cross-trade relationships layer design now and defer tuning. The sweep reports inform that decision; extended-thinking Claude drafts the next phase's march orders once Daniel chooses."

Do NOT modify §1, §2, §5, §9, §10. Surface-level wording tweaks elsewhere are acceptable; do not restructure.

If anything about how the sweep actually shipped (a §7 stop fired, a bidset wasn't located, a per-page error rate was unusually high) makes a §3 or §7 line awkward to update, **state the awkwardness in the gate report rather than glossing it.**

---

## §9 — Step Sweep.8: Commit and final gate report

**Single commit** on `phase2-v0.3-sweep-three-bidsets`:

- `backend/SWEEP_OBSERVATION_shoppes-at-avalon.md` (NEW)
- `backend/SWEEP_OBSERVATION_vine-street.md` (NEW)
- `backend/SWEEP_OBSERVATION_bearss-ave.md` (NEW)
- `PROJECT_CLAUDE.md` (MODIFIED)

Commit message body: name the three bidsets, summarize for each (page count, dispatch time, dispatch_complete, total roofing/glazing/door/storefront item counts, debug section 6 quality flag count). Note any per-page errors that surfaced. Confirm all three sections 2/4/5 stub markers present in all three debug outputs. State which §7 stops fired (none expected) or close observations.

Branch is local-only at session end. Push timing for the sweep branch is Daniel's call.

---

## §10 — §7 Stop Conditions

Stop, report, and wait for Daniel before continuing if any fire:

1. **Sacred floor regresses.** Backend below 216/19/0. Frontend below baseline. Hard stop.
2. **Push fails** for either C.3c-build or C.5. Hard stop. Do not retry with `--force`.
3. **A bidset cannot be located** in the workspace. Do NOT substitute. Stop and ask.
4. **Dispatch raises** on any bidset (whole-bidset failure, not per-page). Stop and report traceback.
5. **A trade module raises on >25% of pages** in any single bidset. Signals a contract-shape issue, not an edge case. Stop.
6. **Need to modify any backend/core/ file** for any reason. Vault rule active on all five vault-ruled modules; only the sweep script (untracked) is created. Hard stop.
7. **Need to add a dependency.** Hard stop. networkx is still NOT to be added in this session.
8. **Per-page error rate is between 5% and 25%** on any bidset. NOT a hard stop, but record the rate explicitly in the report's §6 (Per-Page Errors) and call it out as a soft observation in the gate report. The future tuning session decides whether the rate matters.
9. **PROJECT_CLAUDE.md update creates ambiguity.** State the ambiguity in the gate report; do not paper over.

§7 stops are how this phase distinguishes "running the sweep cleanly" from "discovering the modules can't run on real bidsets." Surface the discovery. Do not absorb it.

The §1 observation-only norm is **not** a §7 stop — it's an in-line discipline. If you find yourself writing "should be:" or "recommend:" in a report, delete it and rewrite. That's correction, not a stop.

---

## §11 — Discipline reminders (Karpathy)

1. **Read first.** All §2 docs in full. Especially the C.3a Shoppes characterization and the C.5 Taco Bell run-through artifact — they're the closest existing templates.
2. **Sacred floor first.** 216/19/0 backend before pre-flight, after sweep, after commit. Frontend baselines unchanged throughout.
3. **Minimum implementation.** The sweep script does exactly what §6 says. No bonus diagnostics. No "while we're in there" expansion. No auxiliary analysis.
4. **Vault rule held throughout.** Zero `backend/core/` modifications. Read-only inspection of `roofing_module.py`, `glazing_module.py`, `debug_module.py`, `trade_input_builder.py` is allowed and necessary; modification of any of them is a §7 stop.
5. **Observation discipline.** Re-read §1 of these orders before writing each closing per-bidset note. The temptation to slip into analysis language increases as you see imperfect output stack up. Resist.
6. **No tuning, no fix lists, no recommendations.** This is the most-counterintuitive constraint of this phase, the same way §4.5 was for C.3c-build. The sweep produces raw observation. The future tuning session decides what to do with it.

---

## §12 — Done definition (gate report checklist)

The final gate report must confirm:

- [ ] Pre-flight: 216/19/0 backend; frontend at baselines; both branches at expected commits; all three bidsets located
- [ ] C.3c-build branch pushed to `origin`
- [ ] C.5 branch pushed to `origin`
- [ ] Sweep script written at `backend/scripts/sweep_three_bidsets.py` (NOT committed)
- [ ] Shoppes-at-Avalon report saved at `backend/SWEEP_OBSERVATION_shoppes-at-avalon.md`
- [ ] Vine Street report saved at `backend/SWEEP_OBSERVATION_vine-street.md`
- [ ] Bearss Ave report saved at `backend/SWEEP_OBSERVATION_bearss-ave.md`
- [ ] All three reports follow the §7 skeleton structure
- [ ] All three reports contain only observation language in their closing sections (no "should be:", "recommend:", "looks like a bug:")
- [ ] All three reports confirm sections 2/4/5 stub markers present
- [ ] PROJECT_CLAUDE.md updated per §8 (§3, §4, §6, §7, §8; §1, §2, §5, §9, §10 untouched)
- [ ] No `backend/core/` file modified
- [ ] No `pyproject.toml` change
- [ ] Backend suite still 216/19/0 (sweep adds zero tests)
- [ ] Frontend at baseline
- [ ] Single commit on local branch `phase2-v0.3-sweep-three-bidsets`; not pushed
- [ ] §7 stops: status of each enumerated explicitly
- [ ] Per-bidset wall-clock dispatch time recorded
- [ ] Per-bidset trade module per-page error rate recorded (zero expected)
- [ ] Final gate report produced

---

## §13 — Execution mode

**Single chunk, autonomous, soft gates only.** If pre-flight reads complete cleanly, push succeeds, and no §7 stop fires, execute Steps Sweep.0 through Sweep.8 without pausing for confirmation between steps. Single final gate report at the end.

Soft observations (per-page error rates 0–5%, large but valid quality flag counts, sparse trade module output on pages where the trade isn't present) go in the gate report and the per-bidset reports. Do not pause for those.

§7 stops are the only hard pauses. Those genuinely stop and wait.

---

## §14 — Closing

After the gate report lands and PROJECT_CLAUDE.md is updated, **Daniel reviews the three observation reports**. The next planning conversation depends on what he sees:

- If output reveals the modules need tuning before cross-trade work makes sense → next phase is module tuning sessions, dedicated, with `core/` frozen, in the discipline established by CLAUDE.md §3 Decision 15.
- If output is clean enough to proceed to architecture → next phase is C.4 cross-trade relationships layer design.
- If output reveals a structural issue not anticipated by either path → Daniel and extended-thinking Claude redraft from there.

The sweep is the input to that decision, not a constraint on it.

Standing by for execution.

**End of MARCH_ORDERS_three_bidset_sweep.md.**
