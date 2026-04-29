# MARCH ORDERS — Profile Diagnostic + Housekeeping

**Date issued:** 2026-04-29
**Issued by:** Daniel (via extended-thinking Claude planning session)
**Executed by:** Claude Code
**Phase shape:** Single session, autonomous, soft-gates-only, single final gate report
**Read first:** PROJECT_CLAUDE.md, CLAUDE.md, VALIDATION_LEDGER.md, HANDOFF_FINAL_2026-04-28.md, then this document

---

## §0 — What this phase is

Two things, in the same session:

1. **Profile diagnostic.** On the Bearss Ave bidset (highest content density, slowest sweep wall-clock at 824.9s for 91 pages = 9.1s/page modules), pick two pages — one high-content, one low-content — and time pdfplumber text extraction, pdfplumber table extraction, `RoofingModule.analyze`, and `GlazingModule.analyze` separately on each. Cross-reference timing data against what `debug_module` sections 1, 3, and 6 say about those same pages. Produce one structured diagnostic report.

2. **Housekeeping.** Four bookkeeping items that have accumulated and are now overdue: push the sweep branch to remote, commit the pre-existing untracked working-tree dirt to a clean state, add a validation ledger row for the sweep's detected_system=None finding, and log D-9 (glazing_module.py docstring drift identified by extended-thinking Claude on 2026-04-28) in DISCOVERED_ISSUES.md.

The profile diagnostic is **observation only** — same discipline as the sweep. No tuning, no fix lists, no recommendations. The output tells the next planning conversation where sweep time actually went, so the (a) tuning / (b) C.4 / (c) something-else decision is made on data, not intuition. Vault rule active on all five vault-ruled modules throughout — only the diagnostic script (working-tree only or `backend/scripts/`) and the report file are created.

This phase is **NOT** an upgrade evaluation, **NOT** a benchmark of pdfplumber vs Marker vs Surya vs PaddleOCR, and **NOT** a recommendation about extractor swaps. It produces timing data on the existing stack. Period. If timing data later motivates an extractor evaluation, that's its own future phase with its own march orders.

---

## §1 — Pre-flight reads (Karpathy step 1)

Full reads, in this order:

1. **PROJECT_CLAUDE.md** — current state. Note §3's coverage of the sweep ship and the open Path (a)/(b) decision in §8.
2. **CLAUDE.md** — §3 Decision 15 (vault rule, current vault list of 5 modules). §6 hard guardrails. §9 anti-patterns.
3. **VALIDATION_LEDGER.md** — sacred floor (216/19/0); structure of §C / §D / §F so the new row is appended in the right section.
4. **HANDOFF_FINAL_2026-04-28.md** — recent state.
5. **`backend/SWEEP_OBSERVATION_bearss-ave.md`** — to identify candidate pages (highest legend count, schedule-classified pages, etc.) for the high-content profile target.
6. **`backend/C5_DEBUG_RUN_THROUGH_taco-bell-weeki-wachee-compass-construction-management-2.md`** — structural template for cross-referencing debug output with profile findings.
7. **`backend/scripts/sweep_three_bidsets.py`** (if accessible from working tree) — the sweep harness; the profile diagnostic harness shares its dispatch + per-page-input setup, so reuse the pattern rather than reinventing.
8. **`backend/core/debug_module.py`** (read-only) — confirm what sections 1, 3, 6 read; needed to know what cross-reference data the report can pull.
9. **`backend/DISCOVERED_ISSUES.md`** — to confirm the next D-N number and the row format.

Read-only inspection of `roofing_module.py`, `glazing_module.py`, `debug_module.py` is allowed and necessary. Modification of any of them is a §7 stop.

---

## §2 — Step Profile.0: Pre-flight verification

- Run the full backend suite. Floor: **216 passed, 19 skipped, 0 failed**. Hard stop if not met.
- Run the four frontend test suites at sacred floors: `run_tests.js` 107/107, spotchecks 7/4/8/14, mutations 8/8.
- Verify branches:
  - `phase2-v0.3-C3c-glazing-module` head = `6001042` (already pushed)
  - `phase2-v0.3-C5-debug-module-port` head = `b569312` (already pushed)
  - `phase2-v0.3-sweep-three-bidsets` head = `cf107dd` (currently local-only — will be pushed in §7 housekeeping)
- Locate Bearss Ave PDF at the C.3a-established path (`C:/huck stage 2/full bid sets/` per the sweep gate report) or the equivalent `backend/data/bidsets/` convention.
- Confirm `git remote -v` shows `https://github.com/dhellwarth86/huckleberry.git`.

---

## §3 — Step Profile.1: Branch

Branch from sweep head:

```
phase2-v0.3-profile-and-housekeeping  (NEW; from cf107dd)
```

Two commits expected on this branch (one for the diagnostic, one for housekeeping). Branch will be pushed at end of session. Push timing for the sweep branch is part of §7 housekeeping.

---

## §4 — Step Profile.2: Identify target pages using debug section 3

The page selection is **driven by debug output**, not by guessing.

Run `run_dispatch()` + `run_debug(ctx)` on Bearss Ave (this is essentially the C.5 run-through pattern, restricted to Bearss Ave). Read debug section 3 (page_intelligence) and pick:

- **High-content page.** The page with the most signal in section 3. Reasonable proxies: highest legend count attribution to that page (cross-reference section 6's `legend_contents` if it carries page indices), schedule-bearing classification, highest path-operator count, or whatever section 3 surfaces as "rich." Document why this page was picked.
- **Low-content page.** The opposite — minimal section 3 signal, ideally a clean cover page or a sparse detail page. Document why.

If section 3 doesn't surface obvious distinctions (Bearss is uniform-content), fall back to extreme page numbers — the first non-cover page with content vs. a clearly thin spec or detail page. Document the fallback choice if used.

This page-selection step is also a soft observation in itself: how informative is debug section 3 for "tell me which page to look at"? Note that as a closing observation in the report (one sentence, not analysis).

---

## §5 — Step Profile.3: Write the diagnostic harness

Create `backend/scripts/profile_diagnostic.py` (working tree; commit it this time as a tracked diagnostic harness — see §9 commit shape).

The script:

1. Loads the Bearss Ave PDF.
2. Calls `run_dispatch(pdf_path, storage=None)` once → `PlanSetContext`. Record dispatch wall-clock time.
3. For each of the two target pages (high-content, low-content):
   - Time **pdfplumber text extraction** on that page in isolation. Repeat 3 times; report min, median, max.
   - Time **pdfplumber table extraction** on that page in isolation. Repeat 3 times.
   - Time **RoofingModule().analyze(input)** on a TradeModuleInput built from that page. Repeat 3 times.
   - Time **GlazingModule().analyze(input)** on the same input. Repeat 3 times.
4. Capture the full `TradeModuleOutput` from each module call (don't just count fields — the report will summarize what came back).
5. Build a `DebugContext`, call `run_debug(ctx)`, and pull the per-page entries from sections 1 / 3 / 6 that correspond to the two target pages.
6. Write the formatted report to `backend/PROFILE_DIAGNOSTIC_bearss-ave.md`.

Use `time.perf_counter()` for timing, not `time.time()`. Three repeats per measurement to filter cold-start effects; report median as the headline number, range as a sanity check.

**What the harness does NOT do:**

- Does not modify any `backend/core/` file.
- Does not call OCR libraries (Tesseract, PaddleOCR, Surya, Marker — none of these belong in this phase).
- Does not benchmark alternatives. It times the existing stack as it is.
- Does not test anything (no pytest additions).
- Does not optimize or "improve" anything that runs slow.

---

## §6 — Step Profile.4: The report

Save as `backend/PROFILE_DIAGNOSTIC_bearss-ave.md`. Use this skeleton:

```markdown
# Profile Diagnostic — Bearss Ave

**Date:** 2026-04-29
**Phase:** Profile diagnostic + housekeeping
**Bidset:** Bearss Ave (full filename and path)
**Page count:** 91
**Sweep wall-clock reference:** 824.9s modules / 95.0s dispatch (per SWEEP_OBSERVATION_bearss-ave.md)

## §1 — Page Selection Rationale

**High-content page:** N. Reason: <debug section 3 / 6 signal that drove selection>.
**Low-content page:** M. Reason: <debug section 3 / 6 signal that drove selection>.

## §2 — Dispatch Timing (whole bidset)

- run_dispatch wall-clock: <s>
- (Reference from sweep: 95.0s — confirm match or note delta)

## §3 — Per-Page Timing (3 repeats, median in seconds)

| Operation                          | Page <N> (high) | Page <M> (low) | Ratio (high/low) |
|------------------------------------|-----------------|----------------|------------------|
| pdfplumber text extraction         |                 |                |                  |
| pdfplumber table extraction        |                 |                |                  |
| RoofingModule.analyze              |                 |                |                  |
| GlazingModule.analyze              |                 |                |                  |
| **Total per-page**                 |                 |                |                  |

(Ranges below the table for sanity-check; e.g., "table extraction range 0.42s–0.51s" — not in the headline table.)

## §4 — Module Output Summary

### Page <N> (high-content)
- Roofing fields produced: <N>
- Glazing items produced: <N glazing> / <N door> / <N storefront>

### Page <M> (low-content)
- Roofing fields produced: <N>
- Glazing items produced: <N glazing> / <N door> / <N storefront>

## §5 — Debug Cross-Reference

### Page <N> (high-content)

**Section 1 (dispatch_health):** <relevant per-page stats if exposed>

**Section 3 (page_intelligence) entry for page <N>:**
```json
{ ... full per-page entry ... }
```

**Section 6 (legend + quality flags) attribution to page <N>:**
- Legends attributed: <N>
- Quality flags: <list>

### Page <M> (low-content)

(Same shape.)

## §6 — Observations (no fixes, no recommendations)

(3-5 plain "Observed:" statements describing the timing pattern, the high/low ratio, and any cross-reference between debug signal and timing. NEVER "should be:", "recommend:", "looks like a bug:". If the data shows table extraction dominates on the high-content page, the observation says exactly that — "Observed: pdfplumber table extraction was N×  the time of text extraction on page X" — and stops.)

(One closing sentence on whether debug section 3's signal proved useful for picking the target pages — was the page selection guided by debug, or did debug not differentiate enough?)

## §7 — Closing

Diagnostic only. Profile data feeds the future planning conversation about Path (a) module tuning vs (b) C.4 design vs other directions. No tuning was performed. No fixes were attempted. The roofing module, glazing module, and debug module are vault-ruled per CLAUDE.md §3 Decision 15.
```

The §6 observation language is the same load-bearing discipline as the sweep. If the data says "table extraction is 8× text extraction on the dense page," the observation says exactly that. It does NOT say "table extraction is too slow" or "pdfplumber should be replaced" or "this needs fixing." The future planning conversation makes those calls; the report produces data.

---

## §7 — Step Housekeeping.0–3: Four bookkeeping items

These run after the profile diagnostic completes and before the final gate report. Each is small.

### §7.1 — Push the sweep branch

```
git push origin phase2-v0.3-sweep-three-bidsets
```

The sweep branch (commit `cf107dd`) was authorized as Daniel's-call at sweep ship time. Pushing now. If push fails (auth, conflict), §7 stop.

### §7.2 — Commit pre-existing untracked working-tree dirt

The sweep gate report named this explicitly: "All pre-existing uncommitted documentation and scripts in working tree (HANDOFF_FINAL, MARCH_ORDERS, VALIDATION_LEDGER, prior diagnostics, etc.) — pre-existing dirt not related to this phase, future bookkeeping commit."

Run `git status --porcelain | head -40` first to inventory what's actually there. Then commit the documentation/canon files (`MARCH_ORDERS_*.md`, `HANDOFF_FINAL_*.md`, `VALIDATION_LEDGER.md`, `DEBUG_MODULE_REPORT.md`, `C3_GLAZING_SEED_VALIDATION.md`, prior observation reports, the C.5 run-through script `backend/scripts/c5_run_through.py`, the sweep harness `backend/scripts/sweep_three_bidsets.py`) into the housekeeping commit.

**Do NOT commit:**
- Any `backend/core/` file (vault rule active; nothing should be uncommitted there anyway)
- Any temporary diagnostic output files (one-shot debug dumps, scratch JSON, etc.)
- Any file that looks like uncommitted in-progress work that might confuse future sessions

If the inventory surfaces anything ambiguous, list it in the gate report and **leave it untracked** rather than committing it. Soft observation, not §7 stop.

The diagnostic harness `backend/scripts/profile_diagnostic.py` from Step Profile.3 is committed in **commit 1** (the diagnostic commit), not here.

### §7.3 — Validation ledger row for sweep finding

In `VALIDATION_LEDGER.md`, append a new row to whichever section is most appropriate (likely §C or §D — Claude Code reads the ledger structure and decides) capturing this finding from the sweep:

> **Three-bidset sweep, 2026-04-28:** `project_scope.detected_system = None` on 3/3 real bidsets (Shoppes-at-Avalon, Vine Street, Bearss Ave) despite presence of roofing scope. Consistent with intake-diagnostic Pass 2 finding (manufacturer mentions in negation contexts; sealants/drywall manufacturer mentions colliding with roofing detection). NOT graded. NOT adjudicated as bug or feature. Surfaces dispatch detection rate on real bidsets vs. Taco Bell's clean `tpo` 0.95 hit. Receipts: `backend/SWEEP_OBSERVATION_*.md`. Method: dispatch + module call observation, no ground truth.

Format the row to match the ledger's existing row conventions (Claude Code reads them and matches).

### §7.4 — D-9 in DISCOVERED_ISSUES.md

Add a new row D-9 (or whatever the next number is) capturing the docstring drift in `glazing_module.py` flagged by extended-thinking Claude on 2026-04-28:

> **D-9 — glazing_module.py docstring limitations list undersells actual code in four places** (filed 2026-04-29, surfaced in extended-thinking review of C.3c-build ship 2026-04-28):
>
> 1. Lines 686-688: `door_type`, `frame_type`, and `material` fields all derive from `_classify_door_type(joined)`. Three fields, one classifier, one heuristic. Docstring limitation #7 covers single/pair classification, NOT type/frame/material collapse.
> 2. Line 214: `_NUMERIC_DOOR_RE` hardcoded to 100-199 numbering ("typical retail"). Multi-story bidsets with 200/300/400-series doors will miss. Not flagged in docstring.
> 3. Line 280: `_match_system` half-token threshold (`best_hits >= max(1, len(best_name.split("_")) // 2)`). For two-token system names, any one token in any row hits. Not flagged in docstring.
> 4. Line 207: `_MARK_RE` includes more prefixes than docstring limitation #3 enumerates (HW, HM, FR, bare D in addition to W-/D-/SF-/WIN-/DOOR-).
>
> **Status:** observation only. NOT a fix list. NOT scheduled. Belongs to future glazing tuning session (vault rule active per CLAUDE.md §3 Decision 15). The docstring update is itself a tuning action and goes in a vault-respecting session.

Match the existing DISCOVERED_ISSUES.md format. If the file structure differs from this layout, adapt.

---

## §8 — Step Housekeeping.4: PROJECT_CLAUDE.md minor update

Two small edits:

- **§3** — Move the sweep branch from "local-only" to "pushed 2026-04-29" in the branch state narrative.
- **§3** — One sentence added: profile diagnostic complete; receipts at `backend/PROFILE_DIAGNOSTIC_bearss-ave.md`. Sweep observations + profile data together inform the open Path (a)/(b) decision.

Do NOT modify §1, §2, §4, §5, §6, §7, §8 (the next-planning-conversation section), §9, §10. Surface-level wording changes only where strictly required.

---

## §9 — Commit shape

**Two commits on `phase2-v0.3-profile-and-housekeeping`:**

**Commit 1 of 2:** Profile diagnostic
- `backend/PROFILE_DIAGNOSTIC_bearss-ave.md` (NEW)
- `backend/scripts/profile_diagnostic.py` (NEW — tracked this time, unlike sweep_three_bidsets.py; this is now a reusable diagnostic template for future sessions)
- Commit message body: high/low page numbers chosen, rationale (1-2 sentences), median timings for the 8 measurements, headline cross-reference observation

**Commit 2 of 2:** Housekeeping
- `VALIDATION_LEDGER.md` (MODIFIED — sweep row added)
- `DISCOVERED_ISSUES.md` (MODIFIED — D-9 row added)
- `PROJECT_CLAUDE.md` (MODIFIED — §3 push state + profile diagnostic mention)
- Plus any pre-existing untracked docs that pass the §7.2 filter
- Commit message body: list of files committed for §7.2 inventory, sweep branch push confirmation, ledger row summary, D-9 summary

**Pushes from this session:**
- `phase2-v0.3-sweep-three-bidsets` → origin (during §7.1)
- `phase2-v0.3-profile-and-housekeeping` → origin (after both commits land)

Both pushes authorized. If either fails, §7 stop.

---

## §10 — §7 Stop Conditions

Stop, report, wait for Daniel if any fire:

1. **Sacred floor regresses.** 216/19/0 backend or any frontend baseline. Hard stop.
2. **Sweep branch push fails.** Stop. Do not retry with `--force`.
3. **Bearss Ave PDF cannot be located.** Stop and ask. Do not substitute.
4. **Dispatch raises** on Bearss Ave. (Did not raise during sweep on 2026-04-28; if it raises now, something changed — investigate.)
5. **A trade module raises** on either of the two target pages during profiling. Stop, capture traceback, do not "soft-recover" — this is a single-page targeted run, not the wide sweep.
6. **Need to modify any `backend/core/` file** for any reason. Hard stop.
7. **Need to add a dependency.** Hard stop. No OCR libs, no profilers, no benchmarking frameworks. `time.perf_counter()` is in stdlib.
8. **Inventory of pre-existing untracked dirt is unexpectedly large or contains anything that looks like in-progress work** (>50 files, or any file whose name suggests scratch/temp/debug-N work that wasn't intentionally preserved). Stop, list, ask.
9. **PROJECT_CLAUDE.md edit creates ambiguity** beyond the small §3 changes specified.

§7 stops are how this phase distinguishes "clean diagnostic + tidy housekeeping" from "discovering something architectural." Surface, don't absorb.

---

## §11 — Discipline reminders (Karpathy)

1. **Read first.** All §1 docs in full. Especially the Bearss Ave sweep observation report and the C.5 run-through artifact for cross-reference template.
2. **Sacred floor first.** 216/19/0 before, after diagnostic, after both commits, after both pushes.
3. **Minimum implementation.** The profiling harness times four operations on two pages. No bonus measurements. No CPU profiler integration. No memory profiling. No flamegraphs. Just `time.perf_counter()` × 24 measurements (4 ops × 2 pages × 3 repeats).
4. **Vault rule held.** Five vault-ruled modules read-only. Modification of any is §7 stop.
5. **Observation discipline.** §6 of the report uses "Observed:" prefix only. Same load-bearing rule as the sweep. If you find yourself writing analysis or a fix list in the report, delete and rewrite as observation.
6. **Housekeeping is housekeeping.** Don't expand the §7 scope. The four items listed are the four items. If you find another bookkeeping issue, add it to the gate report as a soft observation; do not fix it in this session unless it's blocking commit/push.

---

## §12 — Done definition (gate report checklist)

The final gate report must confirm:

- [ ] Pre-flight: 216/19/0 backend; frontend at baselines; all three pre-existing branches at expected commits; Bearss Ave PDF located
- [ ] Two target pages selected with documented rationale based on debug section 3 / 6 signal
- [ ] `backend/scripts/profile_diagnostic.py` written and runs cleanly
- [ ] Eight median timings captured (4 ops × 2 pages); ranges in report sanity-check
- [ ] Module output summarized for both pages
- [ ] Debug section 1 / 3 / 6 cross-reference attached to both pages
- [ ] `backend/PROFILE_DIAGNOSTIC_bearss-ave.md` saved per §6 skeleton
- [ ] Report §6 observations follow "Observed:" discipline (no "should be:", "recommend:", "looks like a bug:")
- [ ] Sweep branch pushed to `origin`
- [ ] Pre-existing untracked dirt inventoried and committed (or explicitly left untracked with reason in gate report)
- [ ] VALIDATION_LEDGER.md row added for sweep detected_system=None finding
- [ ] DISCOVERED_ISSUES.md D-9 row added per §7.4
- [ ] PROJECT_CLAUDE.md §3 minor update (push state + profile diagnostic mention) — §1, §2, §4, §5, §6, §7, §8, §9, §10 untouched
- [ ] No `backend/core/` modification
- [ ] No `pyproject.toml` change
- [ ] Backend suite still 216/19/0 (zero new tests)
- [ ] Frontend at baseline
- [ ] Two commits on `phase2-v0.3-profile-and-housekeeping`; both pushed
- [ ] §7 stops: status of each enumerated explicitly
- [ ] Final gate report produced

---

## §13 — Execution mode

**Single chunk, autonomous, soft gates only.** If pre-flight reads complete cleanly and no §7 stop fires, execute Profile.0 through Housekeeping.4 without pausing for confirmation. Single final gate report at the end.

Soft observations (timing variance, page-selection ambiguity, untracked-dirt edge cases) go in the gate report and the diagnostic report. Do not pause.

§7 stops are the only hard pauses.

---

## §14 — Closing

After the gate report lands, Daniel reviews:

1. The profile diagnostic timings — to see whether pdfplumber tables, module regex work, or something else dominates per-page time.
2. The cross-reference between debug signal and timing — to see whether debug section 3 already knows which pages will be slow.
3. The housekeeping outcomes — to confirm the working tree is clean for the next phase.

The next planning conversation chooses Path (a) module tuning, Path (b) C.4 cross-trade, or a refined direction informed by what the profile data says. The diagnostic is input to that decision, not a constraint on it.

Standing by for execution.

**End of MARCH_ORDERS_profile_and_housekeeping.md.**
