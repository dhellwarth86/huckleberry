# MARCH ORDERS — Phase C.5: Debug Module Port (Partial) + Bidset Run-Through Verification

**Date issued:** 2026-04-28
**Issued by:** Daniel (via extended-thinking Claude planning session)
**Executed by:** Claude Code
**Phase shape:** Single session, autonomous, soft-gates-only, single final gate report
**Read first:** PROJECT_CLAUDE.md, CLAUDE.md, VALIDATION_LEDGER.md, HANDOFF_FINAL_2026-04-28.md, then this document

---

## §0 — What this phase is

Port the TracePoint debug module to Huckleberry as `backend/core/debug_module.py`, **partially**, per the recommendation in `backend/DEBUG_MODULE_REPORT.md`. Sections 1 (dispatch health), 3 (page intelligence), and 6 (legend + quality flags) port immediately and produce real diagnostic output. Sections 2 (scale comparison), 4 (cross-reference graph), and 5 (geometry diagnostics) stub gracefully — they emit a documented placeholder marker pending the external state they need (scale-engine route, networkx + sheet-index parsing, geometry_results from Stages 6–9 respectively).

Then run one real bidset through `run_dispatch()` + `run_debug(ctx)` to verify sections 1/3/6 produce content and 2/4/5 stub cleanly. Capture the output as a saved artifact in `backend/`. Update PROJECT_CLAUDE.md to mark C.5 COMPLETE.

This phase is a **port**, not a build-against-contract. Verification standard is byte-clean port + minimal documented import-path edits + smoke test + bidset run-through producing expected content.

The debug module is **vault-ruled by definition** — it is the original vault-rule subject from TracePoint paper §7.5, codified in Huckleberry CLAUDE.md §3 Decision 15. It must NEVER be modified in the same session that modifies any `backend/core/` non-vault file. Vault rule applies the moment the module is sealed in this phase. Future tuning sessions only.

This phase is the prerequisite to the three-bidset sweep that follows. The sweep will use the debug module as one of its observation surfaces.

---

## §1 — Pre-flight reads (Karpathy step 1)

Full reads, in this order, before writing any code:

1. **PROJECT_CLAUDE.md** — entry point and discipline; the §8 "next planning conversation" subsection explicitly names this phase.
2. **CLAUDE.md** — full read of §3 Decision 15 (vault rule), §6 hard guardrails, §9 anti-patterns. Note that Decision 15 was extended 2026-04-28 to cover trade modules; the same vault rule covers the debug module by definition (TracePoint §7.5 origin).
3. **backend/DEBUG_MODULE_REPORT.md** — the spec report you produced 2026-04-28. The recommendation in that report IS the recommendation Daniel approved. Re-reading it ensures execution matches the spec.
4. **VALIDATION_LEDGER.md** — confirm the 215/19/0 backend floor + frontend baselines that must hold.
5. **HANDOFF_FINAL_2026-04-28.md** — narrative state.
6. **tracepoint_port/TracePoint/modules/debug/debug_module.py** — source file, 470 lines, SHA-1 `b5a4cf93ca7c02116fc00f6dc5a1514da1b18b60`. Re-verify SHA-1 before reading.
7. **tracepoint_port/TracePoint/modules/debug/__init__.py** — confirm empty.
8. **backend/core/context.py** — PlanSetContext definition. The debug module consumes this; you need to know its shape to know what sections 1/3/6 can read without modification.
9. **backend/core/dispatch_gate.py** — `run_dispatch()` signature; you'll call it for the bidset run-through.
10. **backend/core/__init__.py** — confirm still empty (TracePoint convention; should not change in this phase).

**Do not** read or open `roofing_module.py`, `glazing_module.py`, `roofing_vocabulary.py`, `glazing_vocabulary.py`, or any other `backend/core/` file beyond `context.py` and `dispatch_gate.py`. The vault rule keeps those out of scope this session.

---

## §2 — Branch and pre-flight verification (Step C.5.0)

**Branch from C.3c-build head, NOT from `eb49a08`.** C.3c-build is sealed locally at commit `6001042` on `phase2-v0.3-C3c-glazing-module`. Branch C.5 from there:

```
phase2-v0.3-C5-debug-module-port  (NEW; from 6001042)
```

C.5 stacks on C.3c-build because the module the debug port will run alongside (GlazingModule) lives on C.3c-build's branch. Push timing for both branches is Daniel's call after this phase ships — neither push is authorized in this session.

**Pre-flight verification:**

- Run the full backend suite. Floor: **215 passed, 19 skipped, 0 failed**. If the floor is not met before C.5 begins, stop and report; do not begin work on a non-clean baseline.
- Run the four frontend test suites at their sacred floors: `run_tests.js` 107/107, `spotcheck_10b.js` 7/7, `spotcheck_cricket.js` 4/4, `spotcheck_durolast.js` 8/8, `spotcheck_manufacturer.js` 14/14, `mutation_test_step11.js` 8/8 caught.
- Verify SHA-1 of `tracepoint_port/TracePoint/modules/debug/debug_module.py` matches `b5a4cf93ca7c02116fc00f6dc5a1514da1b18b60`.
- Verify `tracepoint_port/TracePoint/modules/debug/__init__.py` is empty (size 0 or whitespace-only).
- Confirm the bidset target (see §5) is accessible.

---

## §3 — Port the debug module (Step C.5.1)

Create `backend/core/debug_module.py` as a faithful port of the TracePoint source with the following constraints:

### What ports verbatim

- Module docstring (extend with a Huckleberry-specific note: "Partial port per Phase C.5 — sections 2, 4, 5 stubbed pending external state. See `backend/DEBUG_MODULE_REPORT.md` for full spec." Do not delete the original docstring; append.)
- `DebugContext` dataclass — verbatim
- `run_debug(ctx, geometry_results=None)` public function signature — verbatim
- Section 1 (`_section_dispatch_health`) — verbatim, reading from `ctx.plan_set_context` exactly as TracePoint does
- Section 3 (`_section_page_intelligence`) — verbatim, reading from `ctx.plan_set_context.pages`
- Section 6 (`_section_legend_and_quality_flags`) — verbatim
- `print_report` helper — verbatim
- CLI `__main__` block — verbatim (it'll be functional under the same shape; even if you don't exercise it this session, leaving it intact preserves the option for future sessions)

### What stubs

- Section 2 (`_section_scale_comparison`) — replace function body with a stub that returns:
  ```python
  return {
      "stub_marker": "C.5_partial_port_pending_scale_engine_route",
      "reason": "Scale comparison requires the scale-engine output route; deferred to Phase D/E per DEBUG_MODULE_REPORT.md.",
  }
  ```
  Keep the original function name and signature intact.

- Section 4 (`_section_cross_reference_graph`) — replace function body with a stub that returns:
  ```python
  return {
      "stub_marker": "C.5_partial_port_pending_networkx_and_sheet_index",
      "reason": "Cross-reference graph requires networkx + sheet-index parsing; deferred per DEBUG_MODULE_REPORT.md.",
  }
  ```
  Keep the original function name and signature intact. **Do NOT add networkx as a dependency this session** — the stub doesn't need it. networkx becomes a real dependency only when section 4 is unstubbed in a future phase.

- Section 5 (`_section_geometry_diagnostics`) — replace function body with a stub that returns:
  ```python
  return {
      "stub_marker": "C.5_partial_port_pending_geometry_results",
      "reason": "Geometry diagnostics requires geometry_results from Stages 6–9; deferred per DEBUG_MODULE_REPORT.md.",
  }
  ```
  Keep the original function name and signature intact. The optional `geometry_results=None` parameter on `run_debug` stays — the stub just ignores it.

### Import-path edits

TracePoint's debug module imports from `data.*` and similar TracePoint-internal paths. Port-time edits change these to Huckleberry paths (`from core.context import ...`, etc.). **Budget: ≤4 lines of import-path edits.** If more are needed, that's a §7 stop.

Document each edited import line with an inline comment: `# C.5 port: was "from data.context import" in TracePoint source`.

### What does NOT change

- No correctness optimization on sections 1/3/6 — port them as-is. If they produce sparse output on a real bidset, that's data observation for the future tuning session, not something to fix now.
- No new sections, helpers, or bonus features.
- No changes to `pyproject.toml` (no networkx, no other deps).
- No changes to `backend/core/__init__.py` (stays empty per TracePoint convention).
- No changes to any other `backend/core/` file. Vault rule active on `roofing_module.py`, `glazing_module.py`, `roofing_vocabulary.py`, `glazing_vocabulary.py` — none of those open this session.

---

## §4 — Smoke test (Step C.5.2)

Per Discovered Issue D-7 precedent (and the C.3c-build precedent of "ONE test file with ONE test"), create `backend/tests/test_debug_module_smoke.py` with **ONE test function** containing multiple assertions:

- Module imports cleanly (`from core.debug_module import run_debug, DebugContext`)
- `DebugContext` instantiates with a minimal stub PlanSetContext (use whatever minimum shape `context.py` requires)
- `run_debug(ctx)` returns a dict
- Returned dict has the six expected section keys (whatever the TracePoint module names them — preserve TracePoint's keys exactly)
- Sections 1, 3, 6 produce content (non-empty / non-stub-marker — exact assertion shape depends on what minimum stub PlanSetContext can yield, but the assertion should distinguish "produced something" from "stub marker")
- Sections 2, 4, 5 contain the `stub_marker` key from §3

**Suite count expectation: 215 → 216.** If the smoke test runs and the total is anything other than 216 passed / 19 skipped / 0 failed, that's a §7 stop — investigate before continuing.

---

## §5 — Bidset run-through verification (Step C.5.3)

This is the verification step that distinguishes "ported and smoke-tested" from "actually working."

### Bidset selection

**Primary:** Taco Bell bidset (the one that has `detected_system="tpo"` confidence 0.95, scope_pages [18, 19] per the C.3a / debug report context). If Daniel did not specify the path, locate it under `backend/data/bidsets/` or equivalent path. Prefer the file path Daniel uses elsewhere in the repo — check `MARCH_ORDERS_C_3c_build.md` or `C3_GLAZING_SEED_VALIDATION.md` for established convention.

**Fallback 1:** Shoppes-at-Avalon (the C.3a diagnostic bidset; well-documented, single-story Florida retail).

**Fallback 2:** Any bidset Daniel specifies in chat. If none specified and neither primary nor Fallback 1 is locatable, **stop and ask** rather than guessing.

### Run procedure

Write a small one-shot script (do not commit it as a test; this is a verification artifact, not a regression suite addition). The script:

1. Loads the chosen bidset PDF.
2. Calls `run_dispatch(pdf_path, storage=None)` to produce a `PlanSetContext`. Storage stays None — RoofingModule and GlazingModule are NOT activated in `dispatch_gate.py`, and that's correct for this phase.
3. Constructs a `DebugContext` from the PlanSetContext.
4. Calls `run_debug(ctx)`.
5. Pretty-prints the resulting dict to a file: `backend/C5_DEBUG_RUN_THROUGH_<bidset_name>.md`. Format as a structured report with one section per debug module section, named per the TracePoint section names, with the dict contents pretty-printed beneath.

### Verification assertions (in the report, not as pytest)

Confirm and explicitly state in the saved report:

- **Section 1 (dispatch health):** has `detected_system` field present (value may be `None` if dispatch found nothing — that's fine, the assertion is "field present"). For Taco Bell specifically: should be `"tpo"` with confidence ~0.95.
- **Section 3 (page intelligence):** dict has at least one page entry. For Taco Bell: scope_pages should include page 18 and/or 19.
- **Section 6 (legend + quality flags):** is a populated dict with at least one quality flag emitted (or explicit "no flags raised" marker if TracePoint's section 6 returns that on clean input).
- **Section 2:** contains `"stub_marker": "C.5_partial_port_pending_scale_engine_route"`.
- **Section 4:** contains `"stub_marker": "C.5_partial_port_pending_networkx_and_sheet_index"`.
- **Section 5:** contains `"stub_marker": "C.5_partial_port_pending_geometry_results"`.

If any of the above fails, that's a §7 stop — investigate, don't paper over.

### What the run-through is and is not

- **Is:** smoke verification that the partial port runs end-to-end against real input and produces real content for sections 1/3/6.
- **Is not:** a calibration of the debug module against ground truth (no ground truth exists yet for these bidsets at the trade-module-output level).
- **Is not:** a sweep observation report (the three-bidset sweep is a separate phase with its own march orders).
- **Is not:** an opportunity to tune sections 1/3/6 if they look "off" — vault rule active. If section 3 is sparse, that's data; it's not a fix list.

---

## §6 — Vault rule application (Step C.5.4)

Edit `CLAUDE.md` §3 Decision 15 to add `debug_module.py` to the vault-ruled list. Mirror the pattern used at C.3c-build sealing (single-section edit, "Vault-ruled at sealing (2026-04-28)" subsection):

- Add `backend/core/debug_module.py` to the vault-ruled-at-sealing list with note: "C.5 partial port; vault rule applies to all six sections, stubbed and ported alike. Tuning of sections 1/3/6 happens in dedicated sessions with `core/` frozen. Unstubbing of sections 2/4/5 is a future phase decision (D/E)."

Single-section edit. Do not modify any other CLAUDE.md section. Do not edit any other doc beyond CLAUDE.md and (per §8 below) PROJECT_CLAUDE.md.

---

## §7 — Stop conditions

Stop, report, and wait for Daniel before continuing if any of these fire:

1. **Sacred floor regresses.** Backend below 216/19/0 after smoke test lands. Frontend below baseline anywhere. Either is a hard stop.
2. **SHA-1 mismatch on TracePoint source.** If `debug_module.py` SHA-1 ≠ `b5a4cf93ca7c02116fc00f6dc5a1514da1b18b60`, do not port — investigate the discrepancy first.
3. **More than 4 lines of import-path edits required.** The spec report estimated ≤4. If reality demands more, stop and surface — there may be a deeper deviation between TracePoint and Huckleberry shape than the spec report captured.
4. **A section beyond 1/3/6 needs to "produce content" in the smoke test or run-through.** If the spec report's "stub gracefully" doesn't actually work — i.e., calling `run_debug` blows up because section 2/4/5's stub returns something the rest of the function can't handle — that's a §7 stop. The fix is more careful stubbing, not removing sections from the partial port.
5. **Section 1 / 3 / 6 cannot produce content from a real bidset's PlanSetContext** — even though they read shapes that should exist. This signals either a PlanSetContext shape divergence between TracePoint and Huckleberry, or a real bug in the port. Stop, investigate before claiming success.
6. **Bidset run-through traceback.** Not "produces sparse output" — actually crashes. Stop and report with the traceback.
7. **A change is needed to any `backend/core/` file beyond the new `debug_module.py`.** Vault rule active on every other module. If the port reveals that `context.py` or `dispatch_gate.py` needs a tweak to make the port work, stop — that becomes a separate vault-respecting phase.
8. **A new dependency is needed beyond what's in `pyproject.toml` today.** Specifically: networkx is NOT to be added in this session. If section 4 stubbing somehow demands it, that's a stop.
9. **PROJECT_CLAUDE.md update creates ambiguity.** If something about the C.5 outcome doesn't fit cleanly into the §3 / §7 / §8 update slots in PROJECT_CLAUDE.md, stop and surface — don't paper over with vague language.

§7 stops are how this phase distinguishes "executing a clean port" from "discovering the port has hidden complexity." Surface the complexity. Do not absorb it.

---

## §8 — PROJECT_CLAUDE.md update at end of session (Step C.5.5)

After Steps C.5.0 through C.5.4 land cleanly, update `PROJECT_CLAUDE.md` to reflect C.5 COMPLETE. The version Daniel handed off at the start of this session is the input.

Specific edits:

- **§3** — Add C.5 to the completed-phases narrative. Update test floor: 215 → 216 backend (or whatever the actual final number is post-smoke-test). Note `debug_module.py` as vault-ruled at sealing. Branch state: `phase2-v0.3-C5-debug-module-port` carries C.5; local-only; push timing Daniel's call. Reference the saved bidset run-through report by filename.
- **§4** — Sacred files list extended with `backend/core/debug_module.py` and `backend/tests/test_debug_module_smoke.py`. Vault rule subsection extended to list `debug_module.py`.
- **§6** — Update the misconception about the debug module: change from "needs porting (C.5)" to "ported partially in C.5; sections 2/4/5 stubbed pending external state."
- **§7** — Phase table: C.5 → COMPLETE with commits and date. Three-bidset sweep → NEXT.
- **§8** — Rewrite to point at the three-bidset sweep as the next planning artifact. Inline the sweep constraints from §3 narrative: descriptive observation only; no grading; no "needs ground truth" labels; modules vault-ruled; tuning is a later phase.

Do NOT modify §1, §2, §5, §9, §10. Surface-level wording tweaks elsewhere are acceptable; don't restructure.

If anything about how C.5 actually shipped (the bidset that got chosen, the section-output shapes, the import-edit count) makes a §3 or §7 line awkward to update, **state the awkwardness in the gate report rather than glossing it.**

---

## §9 — Commit shape

**Two commits on `phase2-v0.3-C5-debug-module-port`:**

**Commit 1 of 2:** Port + smoke test + vault rule
- `backend/core/debug_module.py` (NEW)
- `backend/tests/test_debug_module_smoke.py` (NEW)
- `CLAUDE.md` (vault rule extension, single section)
- Commit message body: list edited import lines, note section-stub markers, confirm SHA-1 of TracePoint source

**Commit 2 of 2:** Bidset run-through + canon update
- `backend/C5_DEBUG_RUN_THROUGH_<bidset_name>.md` (NEW)
- `PROJECT_CLAUDE.md` (MODIFIED)
- Commit message body: name the bidset chosen, summarize section 1/3/6 content presence, confirm sections 2/4/5 stub markers present, note any §7 stops that fired (none expected) or close observations worth recording

Branch is local-only at end of session. Do not push.

---

## §10 — Discipline reminders (Karpathy)

1. **Read first.** All §1 docs in full. The TracePoint debug module source from line 1 to line 470. The PlanSetContext shape in `context.py`. Don't skim.
2. **Smoke-test floor first.** Scaffold the smoke test before the module body. Confirm it fails (import error). Then write the module. Confirm it passes.
3. **Minimum implementation.** Sections 1/3/6 verbatim from TracePoint. Sections 2/4/5 stubbed exactly per §3. No bonus features. No "while we're in there" expansions.
4. **100% green floor.** All 13 sacred suites unchanged. Backend +1 (smoke test). 216/19/0 final.
5. **Vault rule applied at sealing.** `debug_module.py` lands in CLAUDE.md §3 Decision 15's vault-ruled-at-sealing list before commit 1 of 2 closes.
6. **Tuning impulses surfaced and refused.** §4.5-style discipline applies here too. If sections 1/3/6 look "off" on the bidset run-through, that's data — not a fix list. Tuning is a future session with `core/` frozen. Document the impression in the run-through report as observation, not as a fix to make.

---

## §11 — Done definition (gate report checklist)

The final gate report must confirm:

- [ ] `backend/core/debug_module.py` exists, ports TracePoint sections 1/3/6 verbatim, stubs sections 2/4/5 with documented markers
- [ ] Import-path edits ≤ 4 lines, each with inline comment naming the original TracePoint import
- [ ] `backend/tests/test_debug_module_smoke.py` exists with ONE test function passing
- [ ] Backend suite: 216 / 19 sk / 0 fail
- [ ] Frontend suites at sacred baselines (no change)
- [ ] CLAUDE.md §3 Decision 15 updated with `debug_module.py` vault-ruled at sealing (single-section edit)
- [ ] Bidset run-through report saved as `backend/C5_DEBUG_RUN_THROUGH_<bidset_name>.md` with explicit section-by-section verification
- [ ] Section 1/3/6 produced content on the run-through (named in the report)
- [ ] Section 2/4/5 stub markers present in the run-through output (named in the report)
- [ ] PROJECT_CLAUDE.md updated per §8
- [ ] No new dependencies added to `pyproject.toml`
- [ ] No `backend/core/` file other than the new `debug_module.py` modified
- [ ] Two commits on local branch `phase2-v0.3-C5-debug-module-port`; neither pushed
- [ ] §7 stops: status of each enumerated explicitly (fired or did not fire)
- [ ] Final gate report produced

---

## §12 — Execution mode

**Single chunk, autonomous, soft gates only.** If pre-flight reads complete cleanly and no §7 stop fires, execute Steps C.5.0 through C.5.5 without pausing for confirmation between steps. Single final gate report at the end.

Soft gates: surface observations and minor decisions in the gate report. Do not pause for those.

§7 stops are the only hard pauses. Those genuinely stop and wait.

---

## §13 — Closing

After the gate report lands and PROJECT_CLAUDE.md is updated, the next planning artifact is the three-bidset sweep march orders — drafted by extended-thinking Claude in a separate session. C.4 (cross-trade relationships layer) follows the sweep observations, not before.

C.5 is the last port-shaped phase before the sweep. Get it clean.

Standing by for execution.

**End of MARCH_ORDERS_C_5_debug_port.md.**
