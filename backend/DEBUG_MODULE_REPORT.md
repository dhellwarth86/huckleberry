# Debug Module Specification Report

**Status:** Read-only observation. No production code touched. No port executed. No march orders.
**Author:** Claude Code session, 2026-04-28
**Branch:** `phase2-v0.3-C2-roofing-module` (current; no new branch — observation task only)
**Companion:** `backend/C3_GLAZING_SEED_VALIDATION.md` (Task 1 of this same session)

---

## 1. Files inspected

### 1.1 Source files (TracePoint port reference tree)

| File | Lines | SHA-1 |
|---|---:|---|
| `tracepoint_port/TracePoint/modules/debug/__init__.py` | 0 (empty file) | `da39a3ee5e6b4b0d3255bfef95601890afd80709` |
| `tracepoint_port/TracePoint/modules/debug/debug_module.py` | 470 | `b5a4cf93ca7c02116fc00f6dc5a1514da1b18b60` |

### 1.2 Imports

```
sys, time
dataclasses (dataclass, field)
pathlib (Path)
typing (Optional)
networkx as _nx          # OPTIONAL — try/except ImportError, _nx=None on failure
core.context             # PlanSetContext, TradeContext, PageContext,
                         # Discipline, PageType, CONFIDENCE_EXPLICIT,
                         # CONFIDENCE_STRONG, CONFIDENCE_INFERRED,
                         # CONFIDENCE_WEAK, CONFIDENCE_UNKNOWN
core.dispatch_gate       # run_dispatch — only inside CLI __main__ block
```

The module also performs `sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))` at import time (line 32) so that the `core.context` and `core.dispatch_gate` imports resolve when the module is run as `python -m modules.debug.debug_module`.

### 1.3 Public surface

| Symbol | Kind | Notes |
|---|---|---|
| `DEBUG_MODULE_VERSION = "1.1.0"` | module constant | printed in the report header |
| `class DebugContext(TradeContext)` | dataclass | extends `core.context.TradeContext`; carries 7 result fields (`dispatch_health`, `scale_comparison`, `page_intelligence`, `crossref_summary`, `geometry_diagnostics`, `legend_contents`, `legend_quality_flags`) |
| `def run_debug(ctx, geometry_results=None) -> DebugContext` | entry point | the only function any caller is expected to use; populates a DebugContext and registers it as `ctx.trade_contexts["debug"]` |
| `def print_report(debug)` | CLI helper | text formatter for `run_debug` output; called only by the `__main__` block |
| `if __name__ == "__main__":` | CLI | parses argv, runs dispatch, calls `run_debug(ctx, {})` (no geometry results), prints |

Six private helpers (one per diagnostic section, plus `_check_legend_quality` and `_safe_print`) are not part of the public surface — they are stable internals of `run_debug`.

### 1.4 Caller / consumer surface in TracePoint

`grep run_debug | DebugContext | trade_contexts["debug"]` across `tracepoint_port/TracePoint/` returns hits only inside `debug_module.py` itself plus the README-style mention in `tracepoint_port/TracePoint/CLAUDE.md`. There is **no** caller in the dispatch pipeline, the geometry route, the trade module, the FastAPI server, or the test suite. The debug module is a self-contained CLI and, per its architecture note, an optional Layer 4 plugin that other code MAY invoke programmatically by passing a PlanSetContext and a `{page_idx: geometry_dict}` dict.

### 1.5 Test surface

`tracepoint_port/TracePoint/tests/` enumerated:
- `test_pdf_engine.py`
- `test_dispatch.py`
- `test_filter_pipeline.py`
- `test_geometry_matrix.py`
- `test_polygon_scorers.py`
- `test_architect_profile.py`
- `test_integration.py`
- `test_wendys_integration.py`
- `fixtures/` directory

No `test_debug_module.py`. `grep -r debug` across `tests/` returns no matches. The debug module ships with **zero** tests in TracePoint. Verification floor is "imports resolve and CLI runs without crashing on a real PDF" — same shape as Discovered Issue D-7 from the C.2 ship (TracePoint had no roofing-module tests either).

---

## 2. What the debug module does (functional description in plain language)

The debug module is a developer-facing diagnostic that, given a PlanSetContext (the dispatch-gate output) and an optional dict of geometry-engine results, produces a six-section structured snapshot of what the platform thinks about a plan set. It does not modify the input. It does not call any internal pipeline function. It only reads public dataclass fields off the input objects.

The six sections are:

1. **Dispatch Health.** Did dispatch complete? Which filters ran? How many warnings did it raise? How many sheets in the sheet map? How many pages got mapped to sheet numbers? Plus the timestamp and total page count.

2. **Scale Comparison.** For every page: dispatch's scale (ft-per-inch + confidence + source) versus the geometry engine's scale (ft-per-inch + scale_method) when geometry results are supplied. Reports a per-page boolean "match" when both sides have a number. Surfaces disagreement between Layer 3 and Layer 2 directly.

3. **Page Intelligence.** Per-page table of: sheet number, title, discipline, page_type, classification confidence, has_drawing/has_title_block/has_details/has_legend booleans, detail count, zone count, legend count, outgoing cross-ref count, incoming cross-ref count.

4. **Cross-Reference Graph.** Total / resolved / unresolved counts across the whole plan set, resolution rate, by-type breakdown (detail-ref vs sheet-ref etc.), a 20-entry sample of unresolved refs (type, source page, target sheet, snippet of the matching text), and — if `networkx` is installed — a directed-graph analysis: nodes/edges, connected-component count, isolated-page count, top-5 most-referenced pages by in-degree, top-5 most-referencing pages by out-degree. The networkx block is optional; the rest of section 4 works without it.

5. **Geometry Diagnostics.** Only populated when `geometry_results` was passed in. Per-page area_sqft, perimeter_ft, ft_per_inch, area_sqin, source (`vector_heavy` / `vector_all` / `dimension_calc` / `stated_area`), scale_method (`dispatch` / `roof_plan_text` / `dimension_validation` / `multi_page` / `scoring`), confidence, polygon count.

6. **Legend Contents.** Every legend the dispatch parsed: legend_type, title, page, entry_count, confidence, source ("text-based" vs "pdfplumber"), and a 10-entry sample of `{key, description}` pairs. **Plus quality flags** (the `_check_legend_quality` helper): warning if total legends > 100 (likely pdfplumber noise), warning if any single page has > 10 legends (likely duplicates), and a count breakdown of text-based versus pdfplumber-sourced legends.

The module is purely a read view. Every output is derivable from the inputs by a deterministic function. Re-running it produces identical results given the same inputs.

---

## 3. How it's used in TracePoint

Three integration points exist:

1. **CLI**, the actual production usage shape: `python -m modules.debug.debug_module path/to/plan.pdf [page_num]`. The CLI imports `run_dispatch` from `core.dispatch_gate`, runs it, prints "Dispatch complete in Xs", calls `run_debug(ctx, geometry_results={})`, and pipes the result through `print_report` to stdout. The `[page_num]` argv position is parsed but never used inside the file — the CLI runs full-bidset diagnostics, not per-page.

2. **Programmatic**, named in the docstring but not wired in TracePoint source: a caller may construct a `geometry_results` dict (`{page_idx: {"area_sqft": ..., "perimeter_ft": ..., "ft_per_inch": ..., "scale_method": ..., "confidence": ..., "n_polygons": ..., "source": ..., "area_sqin": ...}}`) and pass it as the second argument to `run_debug`. Section 5 (Geometry Diagnostics) and the per-page rows in section 2 (Scale Comparison) become populated when this is done. The geometry route in `tracepoint_port/TracePoint/server/routes/geometry.py` is the obvious caller — but TracePoint does not currently invoke the debug module from the route. Section 5's docstring confirms the intent: "Geometry results are passed in by the caller (e.g. geometry route). The CLI runs dispatch-only diagnostics."

3. **Trade context registration.** `run_debug` writes its output to `ctx.trade_contexts["debug"]` so that anything traversing `PlanSetContext.trade_contexts` (a registry pattern) sees the debug result alongside any roofing/glazing/etc. trade contexts. No TracePoint code currently iterates `trade_contexts` looking for "debug" specifically. The registration is for a hypothetical UI or tooling layer that might want to render the diagnostic alongside trade panels. As of TracePoint's current state per its `CLAUDE.md`, this registration is unconsumed.

In short: in TracePoint today the debug module is exercised by a developer typing the CLI command. Its programmatic path is wired correctly but unused. Its trade_contexts registration is wired correctly but unconsumed.

---

## 4. The vault rule (TracePoint paper §7.5)

The user's prompt names the TracePoint paper §7.5 as the canonical statement of the vault rule. The TracePoint paper text itself is not in this Claude session's reading scope, but the rule is paraphrased and named in two authoritative documents that ARE in scope:

- **Huckleberry `CLAUDE.md` §3 Decision 15:** "The vault rule. From TracePoint paper §7.5: the debug module must not be modified in the same session that modifies core pipeline files. Adopted as Huckleberry-wide for any diagnostic instrumentation."
- **TracePoint `CLAUDE.md`, Constraints section:** "The debug module (modules/debug/) is diagnostic infrastructure. It must NOT be modified in the same session that modifies core/ files. Debug enhancements require a separate session with core/ frozen."
- **TracePoint `CLAUDE.md`, Debug Module section:** "Vault rule: Must NOT be modified in the same session that modifies core/ files."

The discipline the rule enforces:

- **Diagnostic instrumentation must be independent of the system it observes.** If a session is in the middle of changing how `dispatch_gate.py` produces text, and in the same session "improves" the legend-quality check in the debug module to handle the new output, the diagnostic now reflects the new code regardless of whether the new code is correct. The diagnostic loses its ability to flag the regression. The vault rule preserves the diagnostic as a stable third-party observer.
- **Debug-module changes cannot smuggle in core-pipeline behavior changes.** The author is forbidden from "while we're in there" edits to core code while the debug module is the editing target. This is the architectural-level expression of the same anti-pattern Huckleberry's `CLAUDE.md` §6 names ("No 'while we're in there' scope expansion").
- **The debug module reads only public interfaces.** TracePoint's `CLAUDE.md` Debug Module section reinforces: "Public interface only: The debug module reads from PlanSetContext and geometry result dicts. It does NOT import dispatch_gate functions, zone_filter, or pdf_engine." This is verifiable in the source — the only `core.*` imports the file makes are `core.context` (for the dataclasses) and a `core.dispatch_gate` import that lives ONLY inside the `if __name__ == "__main__":` block, not at module top level. It does not call any private function from any pipeline file.

How the debug module fits the rule:

The module's structure makes the rule holdable without active enforcement. It reads dataclass attributes (PageContext.scale.ft_per_inch, ctx.all_legends, etc.) — public schema — and writes only to its own DebugContext + the `trade_contexts["debug"]` slot. There is no path from a debug-module change to a behavior change in the dispatch or geometry pipelines. The only file a debug-module edit could affect at runtime is the diagnostic report itself.

The vault rule's existence is an explicit statement that this property is load-bearing — it must remain true forever, not coincidentally true at a snapshot.

---

## 5. What would be required to port it to Huckleberry

### 5.1 Code

- **Source:** 470-line `tracepoint_port/TracePoint/modules/debug/debug_module.py` (SHA-1 `b5a4cf93ca7c02116fc00f6dc5a1514da1b18b60`) plus the empty `__init__.py`.
- **Target placement, two options:**
  - **(a) Flat in `backend/core/`**, matching the C.2 pattern where `roofing_module.py`, `roofing_vocabulary.py`, and `trade_input_builder.py` were placed flat under `backend/core/` rather than under a `backend/modules/roofing/` subtree. This minimises new directory creation and keeps Huckleberry's `core` flat.
  - **(b) Under `backend/modules/debug/`** matching TracePoint's directory layout. This requires creating `backend/modules/__init__.py` and `backend/modules/debug/__init__.py`, and updating `pyproject.toml`'s `[tool.setuptools.packages.find].include` (currently `["app*", "seeds*", "scripts*"]` — note `core*` is itself absent from this list, suggesting the package finder for `core` is satisfied by another mechanism that I have not traced) to include `modules*`.
- **Edit budget for verbatim port:** the only required edits are import-path adjustments. The source already does `from core.context import ...` and `from core.dispatch_gate import run_dispatch`. Under Huckleberry's layout, depending on where the file lands, these may resolve unchanged, may need to become `from backend.core.context` / `from backend.core.dispatch_gate`, or may need a `sys.path` adjustment matching the existing one at line 32. In the worst case the port is at most 4 lines: line 32 (`sys.path` insert), line 40 (`from core.context import`), line 455 (`from core.dispatch_gate import run_dispatch`), and the absolute-import shape of any future caller. By the C.2 budget that is comfortably "verbatim with same-character import-path edits."

### 5.2 Dependencies

- **Already in Huckleberry `pyproject.toml`:** `pdfplumber>=0.11`, `rapidfuzz>=3.0.0`, plus all of the geometry/dispatch deps. Neither pdfplumber nor rapidfuzz is used by the debug module itself, but TracePoint uses them in dispatch/legend parsing — Huckleberry already inherits them via the dispatch port.
- **NOT in Huckleberry `pyproject.toml`:** `networkx`. The debug module's section 4 graph analysis is wrapped in `try: import networkx as _nx / except ImportError: _nx = None`, so the rest of the module functions without it. Adding networkx is a Huckleberry pyproject.toml change and would be the only new dependency the port introduces. Downgrading section 4 to "no graph analysis" is also a valid choice — the unresolved-list and resolution-rate parts of section 4 work without networkx.

### 5.3 Tests

Zero tests in TracePoint (verified by enumeration of `tracepoint_port/TracePoint/tests/` and `grep -r debug` returning no matches). A verbatim port would add zero tests, matching the C.1 / C.2 precedent ("no tests in C.1 because TracePoint has no `test_trade_module.py`; the Protocol is exercised by concrete modules" — Discovered Issue D-7). The verification floor for a verbatim debug-module port would be: (a) `diff = 0` against the TracePoint source modulo same-character import edits, (b) imports resolve, (c) `python -m <path> <a-real-bidset-pdf>` runs end-to-end and emits a report.

### 5.4 Total port surface

- 1 file, 470 lines (production)
- 1 empty `__init__.py`
- 0 tests
- 1 new dependency (`networkx`, optional in source — downgrade path exists)
- 0 modifications to existing core files
- 0 new FastAPI routes (TracePoint hasn't wired one either; it's not part of the port)
- 0 frontend touches

This is the smallest possible port shape in this codebase. By point of comparison, C.1 ported 90 lines + 0 tests; C.2 ported 1,099 lines + 0 tests + 1 cross-trade integration notes file. The debug module alone would be a smaller ship than C.2 was.

---

## 6. What value would it add to Huckleberry specifically?

This section is the genuinely undecided one. TracePoint and Huckleberry are different products, and what the debug module does for TracePoint may not transfer 1:1 to Huckleberry.

**TracePoint is a research artifact** producing 7/10 building-polygon detection on a 10-plan calibration corpus, with developer-facing diagnostics for clustering / scoring / scale-determination work. The debug module's six sections map directly to questions a TracePoint developer asks every day: did dispatch fire all 5 filters? Does dispatch's scale agree with geometry's? Which pages are unclassified? Are cross-references resolving? Does the geometry engine have results for this page? Are the legends pdfplumber-noise or real?

**Huckleberry is a commercial-construction-takeoff platform** whose product loop is: GC uploads bidset → backend extracts trade-aware structured scope → estimator reviews on a screen → estimator approves or corrects → corrections become labeled training data. The user is an estimator, not a TracePoint researcher. The "value" of the debug module is filtered through that lens.

### 6.1 Where the value transfers

- **During Phase B and C development sessions, Huckleberry IS doing TracePoint-developer work.** Every Phase B sub-phase ports a piece of the dispatch / filter / geometry / scoring pipeline. Every Phase C sub-phase exercises that pipeline against new corpora. The debug module's six sections are exactly the questions a Huckleberry session would otherwise have to answer ad-hoc. Right now, in this session, Task 1 (the C.3a glazing seed validation) had to write its own keyword-scan script and its own PDF text-extraction loop because there was no diagnostic harness sitting on top of dispatch outputs. Section 1 (dispatch health), Section 3 (page intelligence), Section 6 (legend contents with quality flags) of the debug module would have collapsed several of the bash scripts I wrote in Task 1 to a single command. That is real value during the Phase B/C/D build years. It is developer value, not estimator value.
- **The legend quality flags** (`_check_legend_quality`) were specifically calibrated against TracePoint's 15-bidset sweep — Chewy's 823 legends down to ~172 after the Filter 4 quality gate, the >100 / >10 thresholds, the text-based-vs-pdfplumber breakdown — and that calibration is corpus-overlap-relevant to Huckleberry. Huckleberry's 15 bidsets are the same Florida-FL retail corpus TracePoint calibrated against (per `CLAUDE.md` §2 lineage). The numbers should transfer with no re-tuning.
- **The vault-rule discipline** is already an established Huckleberry rule (Decision 15, repeated in §6 hard guardrails). The debug module is the canonical example the rule names. Importing the rule without ever importing the example may be acceptable; importing the example reinforces the rule with a tangible artifact.

### 6.2 Where the value diverges

- **The debug module's audience is a developer at a CLI.** Huckleberry's audience is an estimator inside a browser. The debug module produces ASCII text reports with `_safe_print` Windows CP1252 fallback — it has no UI surface, no JSON serialization beyond the dataclass shape, no integration with the v6.3.5 frontend or any post-realignment Phase E API. Whatever value it adds to Huckleberry, it does NOT add product value visible to the GC user.
- **Section 5 (Geometry Diagnostics) is keyed to TracePoint's geometry-route response shape** (`area_sqft`, `perimeter_ft`, `ft_per_inch`, `area_sqin`, `source`, `scale_method`, `confidence`, `n_polygons`). Huckleberry's geometry engine is ported (B.2) but the wrapping endpoint that produces this dict shape lives in TracePoint's `server/routes/geometry.py`, which is not in the Phase B port plan. To populate section 5 on Huckleberry, either Phase E builds a parallel endpoint or a developer constructs the dict by hand from `geometry_matrix` calls. Until then, section 5 returns `{"available": False, "note": "No geometry results provided"}` — the section runs but is empty.
- **Section 4 (Cross-Reference Graph) depends on networkx** for the graph block. Huckleberry has no `networkx` dependency today, and the dispatch port does not need it. Adding it just for section 4 is a real-but-small dependency-surface decision.
- **The auto-notation product** (Phase F) is Huckleberry-specific — three-state annotations, provenance, training-data loop. The debug module's sections do not produce any of that data. It's orthogonal to the auto-notation goal.

### 6.3 Where the value is unclear

- **Whether Huckleberry sessions need a stable diagnostic harness right now versus continuing to write per-session diagnostic scripts.** Both Pass 1 and Pass 2 of the intake diagnostic were per-session scripts (`scripts/intake_diagnostic.py`, `scripts/intake_diagnostic_pass2.py`); the C.3a diagnostic in this session was another per-session script (`scan_glazing.py`, scratch). Each of those answered a specific question. The debug module answers a fixed set of six questions in a fixed format. If Huckleberry's diagnostic needs are heterogeneous (each session wants different data), the debug module saves a small amount of plumbing per session. If they are homogeneous (the same six questions, asked over and over), the debug module is the right tool. We do not yet know which regime Huckleberry is in. We have three diagnostic scripts so far; that is not enough data to call it.
- **Whether Phase D's job-folder structure changes the natural shape of a debug report.** Phase D introduces multi-bidset jobs, GC primary identity, and possibly per-job storage. A debug module that takes one PDF and one PlanSetContext is the right shape for current Phase B/C work; whether it stays the right shape across job folders is unknown until Phase D is scoped.

---

## 7. Recommendation

**Port partially, deferred. Don't port now. Don't port at C.3.**

The thinking, in plain language:

The debug module is small, low-risk, dependency-light, and well-isolated. The cost of porting it is the smallest cost of any TracePoint artifact still on the table. That argues for porting it.

But it is also a developer-facing tool whose audience overlaps "Huckleberry sessions doing Phase B/C verbatim ports and Phase D/E architecture" rather than "the GC user." Phases B is sealed and C is in progress; the moments it would have most helped are mostly behind us. The moments where it would help most going forward are the C.3 / C.4 / Phase D bring-up sessions — but those sessions are also the highest-friction sessions, where a "while we're in there" port carries the most risk of vault-rule violation in the wrong direction (a session that's editing core/ files for legitimate Phase B/C reasons should NOT also be porting the debug module).

A clean phasing path would be:

1. **NOT C.3.** C.3 is the second-trade-module ship. The vault rule says debug-module work and core-pipeline work do not share a session. C.3 is core-pipeline-adjacent work (it builds against the trade contract, may surface contract refinements, may surface vocabulary-loading bugs). Pairing the debug-module port with C.3 violates the rule's spirit even if not its letter.
2. **NOT C.4.** Same reasoning. C.4 (cross-trade relationships) is the most architecturally novel piece of Phase C and demands the developer's full attention.
3. **A standalone "C.x debug-module port" sub-phase**, scheduled between C.4 and Phase D, with its own march-orders document. Sacred files frozen across all of Phase B + all of Phase C + new C.4 outputs. Same shape as C.1 (small, verbatim, zero-test, byte-identical-modulo-imports).
4. **Optional partial port:** if `networkx` is unwanted, ship sections 1, 2 (without geometry), 3, 6 immediately and stub sections 4 (graph block) and 5 (geometry diagnostics) with `{"available": False, "note": "..."}` placeholders that match what TracePoint already does when `geometry_results=None` or `_nx is None`. The source is already structured to support partial-availability — both gating points (`if geometry_results:` line 138, `if _nx and total > 0:` line 218) are already present. A "partial port" in this sense is just a verbatim port with two specific runtime branches always taking the "unavailable" path until the relevant Huckleberry pieces are in place.

The honest **non-conclusion** here is that this is a judgment call that benefits from Daniel's decision rather than a Claude decision. The code is small enough that the port could happen any time. The discipline cost (vault-rule observance) means the port should NOT happen as a side-task during C.3 or C.4. Whether it happens between C.4 and Phase D, in parallel with Phase D, or never (because Phase E's auto-notation API surfaces the same data in a more product-aligned way) is the question the C.x planning conversation should answer.

If forced to pick one number: **port at a standalone C.5 sub-phase between C.4 and Phase D, partially (sections 1/3/6 immediately, sections 2/4/5 stubbed pending geometry-route + networkx decisions).** Receipts to support a different choice are entirely valid; this is not a high-confidence recommendation, just a reasoned one.

---

## 8. Explicit non-conclusions

This is a specification report, not a port plan. Specific non-conclusions:

1. **No code was written, ported, or modified.** No new files in `backend/`. No edits to `pyproject.toml`. No new tests.
2. **No port shape was selected.** Sections 5.1(a) vs 5.1(b), networkx-included vs networkx-excluded, full-port vs partial-port — all options were named, none were chosen.
3. **No phase placement was decided.** Section 7's "C.5 sub-phase between C.4 and Phase D, partial port" is a recommendation, not a phase plan. The actual placement is Daniel's call after this report is read.
4. **The TracePoint paper text was not re-read.** Section 4's account of the vault rule is built from the two authoritative paraphrases in `huckleberry/CLAUDE.md` §3 Decision 15 and `tracepoint_port/TracePoint/CLAUDE.md`. The paper itself (§7.5 specifically) is named by the user as load-bearing for the project's discipline; this report does not contest or extend that account, only summarises and applies it.
5. **The "value to Huckleberry" claim in section 6 is reasoned, not measured.** No telemetry on how often Huckleberry sessions write per-session diagnostic scripts versus needing structured diagnostics. The three observed cases (intake-diagnostic Pass 1, Pass 2, this session's `scan_glazing.py`) are too few to call a regime. The judgment is plausible but not validated.
6. **The "would-have-saved-plumbing-in-Task-1" observation is honest but partial.** Section 1 of the debug module would have produced the dispatch_complete=True / 4 filters / 0 warnings / 30 sheets / 19 mapped-pages numbers I quoted in `C3_GLAZING_SEED_VALIDATION.md` §3. But the actual Task 1 work needed page-level *text content*, which the debug module does not surface (it surfaces classification, zones, legend metadata — not the raw text bodies). So the debug module would have saved minutes of plumbing on Task 1, not hours.
7. **Section 6.1's "the same Florida-FL retail corpus" claim** is reasonably supported by the bidset list in `tracepoint_port/TracePoint/CLAUDE.md` "15 Bid Set Sweep (Step 56)" matching the bidsets in `backend/test_fixtures/v0.2_outputs/`. But "calibration transfers" is a hypothesis, not a measurement — actually running the debug module's legend-quality flags on a Huckleberry dispatch output would be the test. That test was not run for this report.
8. **No comparison to alternative diagnostic tools** (e.g. running dispatch with `--verbose`, pretty-printing PlanSetContext, custom session scripts). Section 7's recommendation assumes the debug module is the right shape for Huckleberry's diagnostic needs; that assumption is not benchmarked.

---

**End of DEBUG_MODULE_REPORT.md.**
