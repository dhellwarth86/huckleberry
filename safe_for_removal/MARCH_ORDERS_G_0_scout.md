# MARCH ORDERS — Phase G.0: Scout Mission (read-only fact-finding for Phase G)

**Date issued:** 2026-05-01
**Issued by:** Daniel (via extended-thinking Claude General planning session)
**Executed by:** Claude Code
**Phase shape:** Single autonomous read-only session. **No code changes. No new tests. No new deps. No vault touches.** Output is one markdown deliverable: `backend/G_0_SCOUT_REPORT.md`. Mirror the E.2.0 read-only diagnostic pattern.
**Phase scope:** Inventory the current pdfplumber render path. Audit PyMuPDF + Pandas as proposed dep additions. Compute tiling math against the actual codebase. Root-cause the Silverleaf classification weakness (internal title-page separators triggered multi-bidset path). Re-baseline 3-bidset wall-clock with timing receipts. Propose `core/render/` module structure with line counts. Surface open design questions for Daniel decision.
**Read first:** PROJECT_CLAUDE.md, ITINERARY.md, then this document, then the receipts called out in §2.

---

## §0 — What this phase is

G.0 is a scout mission. Read-only diagnostic; mirror of E.2.0's discipline shape. Claude Code reads, measures, surveys, and writes a single report. Daniel reads the report, locks design decisions, then G.0.1 drafts G.1 build march orders from the scout intel + locked decisions.

Seven concrete deliverables, all rolled into `backend/G_0_SCOUT_REPORT.md` as numbered sections:

1. **Render path inventory.** Where pdfplumber is currently called, what it produces, what consumes its output, what would break if the render path changes.
2. **Dependency audit.** PyMuPDF (`pymupdf` package, imports as `fitz`) + Pandas — install footprint, license, Python version compatibility against current `backend/pyproject.toml`, transitive deps, cost-of-adoption ledger.
3. **Tiling math.** What 200/250/300 DPI tiling means in this codebase — page size in points, tile dimensions in pixels, memory profile per tile, tiles per Silverleaf page, expected wall-clock per page vs current pdfplumber path.
4. **Silverleaf classification root-cause.** Why did the Silverleaf bidset's internal title-page separators trip the multi-bidset classification path? Which dispatch_gate stage made the call, on what signal, against what threshold? Concrete bug name, not a vague description.
5. **3-bidset baseline numbers.** Re-run dispatch on Shoppes-at-Avalon / Vine Street / Bearss-Ave with timing receipts. Wall-clock per stage, total wall-clock per bidset, total memory profile if measurable. Phase G's eventual hard gate compares quadrant-scan vs this baseline; the numbers exist piecemeal in BLOCK_RUN — scout produces a fresh, unified A/B baseline.
6. **Module structure proposal.** Where tiling code belongs in the codebase — new `core/render/` module? Extension to existing geometry stages? Separate utility imported by dispatch? Line count estimates for each option, vault rule implications, dispatch_gate.py line-budget impact.
7. **Open design questions for Daniel.** The decisions scout cannot make alone — DPI choice (200 vs 250 vs 300), tile overlap strategy, when (if ever) to fall back to full-page render, whether tiling applies to all pages or only roof_plan/detail/elevation classifications, etc. Numbered questions with scout's read on each, ending in "Your call:" — Daniel decides at G.0.1 design phase.

After G.0 ships, soft-gate to G.0.1 design phase (extended-thinking Claude drafts G.1 march orders). After G.0.1, soft-gate to G.1 build phase. After G.1 build + soft gates, hard gate against 3-bidset baseline AND deferred E.2.2 Silverleaf visual hard gate in Chrome.

**Why scout-first and not straight to design:**

E.2.0 was effectively a scout mission and produced the cleanest E.2 sub-phase chain in project history. E.2.1 and E.2.2 both shipped first-run-clean against E.2.0's specs because the design phase had real intel under it. Skipping scout for G means drafting design from recall — same trap E.2.0 was created to avoid. PyMuPDF + Pandas are the first real Python deps since FastAPI in E.1; tiling at 200-300 DPI is a render-path change with consequences for memory, accuracy, and downstream consumers. Drafting design without scout intel is the prelude to a drift loop.

**Architectural commitments NOT being made in G.0:**

Scout proposes; Daniel disposes. G.0 ships **proposals, not decisions**. The DPI choice, tile overlap, module structure, and rollout sequencing are all G.0.1 decisions made from G.0 intel. Scout writes "my read: 250 DPI for the right cost/accuracy balance — see §3 numbers; your call" and stops.

---

## §1 — What this phase is NOT

**OUT OF SCOPE for G.0:**

- **Any code change anywhere.** No new files in `backend/api/`, `backend/core/`, `backend/tests/`, `backend/scripts/`, or `frontend/`. No edits to existing files except the single deliverable `backend/G_0_SCOUT_REPORT.md`. Vault rule remains active.
- **New dependencies.** No `pip install`, no `pyproject.toml` edits, no `package.json` edits. The dep audit (§2 deliverable) is paper research — read PyMuPDF and Pandas docs, check PyPI, verify Python version compat — but does NOT install them. PyMuPDF and Pandas can be referenced in the scout report as "proposed addition for G.1" without being added in G.0.
- **New tests.** Backend stays at 230/19/0; frontend stays at 23/23. Verified at session start AND end.
- **Running anything that mutates state.** The 3-bidset baseline runs (§2 deliverable 5) are read-only dispatches that write to `~/.tracepoint/cache.db` per existing D.2 persistence — that's normal dispatch behavior, not a scout-introduced mutation. Use `job_id=None` for the baseline runs so persistence is skipped (matches E.2.2 debug script pattern). Or use new job_ids and accept the DB rows. Either way, no schema changes, no migration, no DB resets.
- **Vault-ruled module changes.** All 5 trade modules + `debug_module.py` read-only.
- **Touching `dispatch_gate.py`, `api/main.py`, or any production code.** Scout opens these files for reading only.
- **CLAUDE.md.** Retired, do not open.
- **`safe_for_removal/`.** Pending Daniel cleanout; scout does not touch.
- **Speculative bug-patches on the Silverleaf classification weakness.** Scout's job is to NAME the bug concretely (which stage, which signal, which threshold). Fixing it is G.1's job. Do not propose patches; do not test patches; do not write "this could be fixed by…" — write "this is caused by [specific code path]" and stop.
- **Recommendations beyond what scout intel supports.** If the dep audit reveals PyMuPDF has a license issue or Python version conflict, surface it; do NOT propose alternatives unless the question was asked. Stay in lane.
- **Multi-trade scope expansion.** Scout looks at roofing + glazing as currently shipped. No siding, no other trades. They're parked deliberately.

---

## §2 — Pre-flight reads (Karpathy step 1)

Full reads, in this order:

1. **PROJECT_CLAUDE.md** — entry point. §3 paragraphs through E.2.2 (most recent); §7 phase table for G's current row description; §4 discipline; §6 misconceptions.
2. **ITINERARY.md** — current state, deferred Silverleaf hard gate note, Phase G as Next-1.
3. **VALIDATION_LEDGER.md** — sacred floors, vault list, especially §D (profile diagnostic) which has the existing pdfplumber profiling numbers from 2026-04-29.
4. **`backend/PROFILE_DIAGNOSTIC_bearss-ave.md`** — the single existing profiling receipt. Cost numbers: pdfplumber.extract_tables 2.91s median on Bearss page 15 (high-content), 178ms median on Bearss page 82 (low-content). This is the cost ceiling Phase G is trying to lower.
5. **`backend/scripts/profile_diagnostic.py`** — the tracked harness from 2026-04-29. Phase G.0 may extend its pattern for the 3-bidset baseline runs, but does NOT modify it.
6. **`backend/E2_2_DEBUG_silverleaf.md`** — fresh Silverleaf calibration: 40 pages, 338 roofing, 107 glazing, 147.7s wall-clock dispatch. The "ROOF_PLAN: 1" line is suspicious in light of the multi-bidset classification observation — investigate whether this is the same root cause.
7. **`backend/CALIBRATION_GATE_REPORT_silverleaf.md`** — original calibration with bug fixes (Bug 1: SCHEDULE rule moved from position 6 to position 0; Bug 3: raw tables preserved alongside legends). Read for context on what page-classification logic looks like inside dispatch_gate.
8. **`backend/SWEEP_OBSERVATION_shoppes-at-avalon.md`** + **`backend/SWEEP_OBSERVATION_vine-street.md`** + **`backend/SWEEP_OBSERVATION_bearss-ave.md`** — descriptive observation reports from 2026-04-28 sweep. Page counts, page-type distributions, item counts per bidset. Reference for the §2 deliverable 5 baseline numbers.
9. **`backend/D2_MASTER_GATE_REPORT.md`** — 3-bidset hard gate from 2026-04-29. Total wall-clock numbers (Vine Street ~1195s, Bearss ~XXXs, Shoppes ~XXXs; verify exact). Phase G's hard gate compares against this.
10. **`backend/E0_FRONTEND_AUDIT.md`** — for context on what the frontend expects from the render path. The audit predates E.2.1's strip; the strip removed all client-side pipeline JS, so the frontend now consumes only `dispatch_results` + `trade_outputs` from the API. Render path changes are server-side only — confirm.
11. **`backend/core/dispatch_gate.py`** — full read. Map every pdfplumber call site; map every `doc.pages[i]` access; map every text/table extraction. The render path inventory (deliverable 1) lives here.
12. **`backend/core/job_storage.py`** — full read. Confirm scout's baseline runs don't accidentally collide with E.2.2 job persistence (use `job_id=None` per §1).
13. **`backend/scripts/d2_silverleaf_reference.py`** + **`backend/scripts/sweep_three_bidsets.py`** (if tracked; sweep harness was untracked at C.5 — verify) — pattern reference for the 3-bidset baseline runs.
14. **`backend/pyproject.toml`** — current Python version pin, current deps, project layout. PyMuPDF + Pandas compatibility check against this.
15. **PyMuPDF docs (PyPI page + project README)** — license (AGPL with commercial-use clarifications), API surface for tiled rendering (`page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=fitz.Rect(x0, y0, x1, y1))`), Python version support.
16. **Pandas docs (PyPI page)** — version, install footprint, transitive deps.
17. **`backend/core/debug_module.py`** — read-only walkthrough. Look for any debug-section output that might surface page-classification confidence scores or alternate-classification candidates. The Silverleaf classification root-cause may have a debug-side trace already.

**Do NOT open:**
- 5 vault-ruled trade modules (roofing/glazing modules + vocabularies). Read for understanding only via gate reports + sweep observations + calibration receipts.
- `debug_module.py` (vault-ruled — same restriction; read-only walkthrough only via existing receipts where possible).
- `CLAUDE.md` (retired).
- v6.3.5 archive (retired).
- Any file in `safe_for_removal/`.
- Frontend HTML beyond confirming via existing E.2.2 receipts that scout doesn't need it.

---

## §3 — Step G0.0: Pre-flight verification

Establish the floor before scout work begins. Read-only phase has the same discipline as build phases.

- Run full backend suite. Floor: **230 passed, 19 skipped, 0 failed**. Hard stop if not met (something drifted post-E.2.2; investigate before scout).
- Run frontend suite against `frontend/src/Huckleberry_AI_phase2.v1.0.0.html`. Floor: **23/23 passed**. Hard stop if not met.
- Capture pre-session SHA-1s for all 5 vault-ruled trade modules + `debug_module.py`. Verify match post-E.2.2 expected values per BLOCK_RUN Phase 9.
- Capture pre-session SHA-1s for `backend/core/dispatch_gate.py`, `backend/api/main.py`, `backend/api/routes/jobs.py`, `backend/api/schemas/jobs.py`, `backend/core/job_storage.py`. **None of these change in G.0.** Verified at session end.
- Capture pre-session SHA-1 for `frontend/src/Huckleberry_AI_phase2.v1.0.0.html`. Does not change in G.0.
- Capture pre-session SHA-1 for `backend/pyproject.toml`. Does not change in G.0.
- Capture pre-session SHA-1 for `frontend/package.json`. Does not change in G.0.
- Verify branch state: head matches commit `0ddd5a5` per BLOCK_RUN Phase 9.
- Confirm `git remote -v` shows `https://github.com/dhellwarth86/huckleberry.git`.
- `git status` snapshot at start. `git status` snapshot at end. The diff between them must contain only `backend/G_0_SCOUT_REPORT.md` (new file).

Pre-flight failure → §13 stop, no scout work begins.

---

## §4 — Step G0.1: Branch

```
phase2-v0.3-G0-scout-mission  (NEW; from E.2.2 head 0ddd5a5)
```

Single commit at end of session. Pushed.

---

## §5 — Step G0.2: Render path inventory (deliverable 1)

Output: §1 of `backend/G_0_SCOUT_REPORT.md`.

Map the current pdfplumber render path end-to-end. Read `backend/core/dispatch_gate.py` and any helper modules it calls. Produce:

1. **Every pdfplumber import or call site.** File + line number + what it produces.
2. **Every `doc.pages[i]` or page-index access.** Tracks who reads pages, in what order, with what side effects.
3. **Every text extraction call.** `page.extract_text()`, `page.extract_words()`, `page.extract_tables()` — call sites, frequency (per-page, per-bidset, per-stage), output type and shape.
4. **Every table extraction call.** Same as above, separated because tables are the dominant cost per profile diagnostic.
5. **Every consumer of pdfplumber output.** Who reads what, what would break if the output shape or precision changed. Scope_scanner? Trade modules? Stage filters? List each consumer with the field they depend on.
6. **Stage-by-stage cost map.** For each of the 12 dispatch stages, what render operations run inside it, what cost they impose. Best-available numbers from the profile diagnostic (Bearss pages 15 + 82 are the only profiled pages; extrapolate cautiously and label as estimates).
7. **What's already cached.** Are page text blocks cached after first extraction? Are tables cached? Look for `page_ctx` storage of these outputs in dispatch_gate.

Format: a table per item where applicable, prose where not. Aim for ~100 lines of inventory in this section.

---

## §6 — Step G0.3: Dependency audit (deliverable 2)

Output: §2 of `backend/G_0_SCOUT_REPORT.md`.

Paper research. Do NOT install anything.

For each of PyMuPDF + Pandas:

1. **Package name and PyPI version.** PyMuPDF imports as `fitz`; latest stable version on PyPI. Pandas latest stable.
2. **License.** PyMuPDF is AGPL-3.0 with a separate commercial license available (Artifex). Pandas is BSD-3-Clause. Surface any commercial-use implications for Huckleberry's eventual deployment posture.
3. **Python version compatibility.** Check current `pyproject.toml` Python pin. Verify both packages support that range.
4. **Install footprint.** Approximate disk size, transitive deps. PyMuPDF bundles MuPDF C library (large). Pandas pulls NumPy.
5. **Transitive dep conflicts.** Any clash with existing pinned deps (FastAPI, uvicorn, pydantic, fastapi, sqlite3-stdlib, pdfplumber)?
6. **API surface for tiled rendering (PyMuPDF).** What's the call shape for "render this rectangular region of this page at N DPI to a PNG/numpy array"? Does it produce in-memory bytes or write to disk by default? Any thread-safety constraints?
7. **API surface for tabular processing (Pandas).** What's the value-add over stdlib + pdfplumber's existing table output? Where in the pipeline would Pandas land — replacing pdfplumber's table extraction, or processing pdfplumber's table output? Be concrete; vague "Pandas helps" is not scout intel.
8. **Cost-of-adoption ledger.** Pyproject diff (proposed lines). Test floor impact estimate. Documentation surface impact (does Phase G need a new VALIDATION_LEDGER section?). Bus-factor risk (both packages are well-maintained — note for completeness).

Format: a sub-section per package, ~30-50 lines each.

---

## §7 — Step G0.4: Tiling math (deliverable 3)

Output: §3 of `backend/G_0_SCOUT_REPORT.md`.

Numbers, not adjectives.

Given:
- Construction-document page sizes: standard ARCH D (24"×36"), ARCH E (36"×48"). Letter (8.5"×11") for spec sheets.
- DPI options to evaluate: 200, 250, 300.

Produce, per DPI option:

1. **Page size in pixels.** ARCH D at 200 DPI = 4800×7200 px. ARCH D at 300 DPI = 7200×10800 px. Etc.
2. **Memory per full-page render in RGB.** width × height × 3 bytes. ARCH D at 300 DPI ≈ 233 MB raw. PyMuPDF's `pixmap.samples` is RGB by default; verify.
3. **Tiling proposal.** Quadrants (2×2)? Sextants (2×3)? More? For each, tile dimensions and memory per tile.
4. **Tile overlap strategy.** Why overlap matters: continuous lines, polygons, and text crossing a tile boundary need to be reassembled. Propose overlap percentage (e.g., 5% per edge) and the call-site implications.
5. **Wall-clock estimate per page.** Based on PyMuPDF benchmarks where available; if no public benchmark, label as estimate with reasoning.
6. **Comparison vs current pdfplumber path.** Bearss page 15 is the existing data point: 2.91s median for table extraction on a high-content page. The proposal should produce a per-page wall-clock estimate that's lower than 2.91s on the same page, OR explain why the cost shifts.
7. **Memory aggregate per bidset.** ARCH D at 250 DPI × 40 pages × 4 tiles per page = how much peak memory if all tiles are held? How much if tiles are processed serially and freed? Phase G is making this decision; scout produces the numbers.
8. **Tiling-vs-no-tiling decision boundary.** Is there a page-type or page-size threshold where tiling pays off but full-page render is still cheaper? E.g., letter-size spec sheets at 200 DPI are 1700×2200 = 3.7 MB raw; tiling those is overhead, not savings. Surface the boundary.

Format: a sub-section per DPI option, plus a concluding sub-section with the comparison table. ~80-120 lines.

---

## §8 — Step G0.5: Silverleaf classification root-cause (deliverable 4)

Output: §4 of `backend/G_0_SCOUT_REPORT.md`.

This is the bug that triggered the E.2.2 hard-gate deferral. Concrete diagnostic, not vague description.

Investigate:

1. **Silverleaf bidset structure.** 40 pages total per E.2.2 calibration. Per-page sheet numbers (where present) per `E2_2_DEBUG_silverleaf.md` per-page table. Note pages where `sheet_num` is `—` — those are likely the internal title-page separators.
2. **Page-classification logic in dispatch_gate.py.** Stage where page_type is decided. What signals feed the decision? Sheet number presence? Drawing index lookup? Text content patterns? Filter rules?
3. **Multi-bidset detection logic.** Where in dispatch_gate.py is the "is this multiple bidsets concatenated" decision made (if any explicit decision exists at all)? Or is it implicit — title-page-like content triggers a state machine reset somewhere?
4. **The specific path Silverleaf took.** Trace through the actual classification decisions for a Silverleaf page that has a separator, and the page that follows it. Show what signal the dispatcher saw, what threshold it compared against, and why it resulted in (whatever the misclassification was — pages 38/39 came back as `UNKNOWN` per E2_2_DEBUG_silverleaf.md; investigate whether this is the same bug or a different one).
5. **Classification confidence.** Does the classifier produce a confidence score? Is the "UNKNOWN" classification a low-confidence default, or a deliberate state? Different fix paths.
6. **Concrete bug name.** End the section with a one-sentence statement: "The Silverleaf classification weakness is caused by [specific code path] in [specific file:line] when [specific condition]." Not "the classifier sometimes gets confused." Specific.
7. **Whether this bug is in the render path or the classification path.** Phase G is primarily a render-path optimization. If the Silverleaf bug is in classification logic and unrelated to rendering, scout flags this — G may need to expand scope, or the bug may need its own phase.

Format: prose narrative with code snippets where helpful. ~80-100 lines.

---

## §9 — Step G0.6: 3-bidset baseline (deliverable 5)

Output: §5 of `backend/G_0_SCOUT_REPORT.md`.

Re-run dispatch on Shoppes-at-Avalon, Vine Street, and Bearss-Ave with timing receipts. **`job_id=None` for all three runs — these are baseline measurements, not persisted dispatches.**

Procedure:

1. Locate the 3 bidset PDFs. Paths should be in the existing sweep observation reports or `backend/scripts/sweep_three_bidsets.py` if tracked. If sweep harness is untracked, replicate its pattern in a one-shot scout-only script that writes results into the scout report and is NOT committed (scout produces no scripts). Use `subprocess` from a Python REPL or a notebook-style sequence — whatever lets you run the dispatches without creating new tracked files.
2. For each bidset, capture:
   - Total wall-clock from `run_dispatch` start to return.
   - Page count.
   - Per-stage wall-clock if surfaceable (dispatch_gate logs may already provide this; check).
   - Total pdfplumber call count (roughly — count from logging output if available).
   - Item counts: roofing fields total, glazing total (matching E2_2_DEBUG numbers).
   - Memory peak if measurable via `tracemalloc` snapshot or `resource.getrusage()` on Linux/Mac, `psutil` on Windows. Memory measurement is best-effort; if it requires installing psutil, skip it and note "memory peak not measured — psutil not available."
3. Cross-check against existing receipts (`SWEEP_OBSERVATION_*.md`, `D2_MASTER_GATE_REPORT.md`). Numbers should match within ±5% of recorded baselines. If not, scout flags the drift — that's a separate bug, not a Phase G concern.
4. Run all three sequentially (parallel runs may share pdfplumber state inappropriately; sequential is the conservative choice).

Format: a table with bidset name, page count, wall-clock, item counts, memory if measured. Plus per-bidset notes for any anomalies. ~50-70 lines.

**Wall-clock for this step:** ~42 minutes per existing 3-bidset hard gate receipts. Vine Street alone is ~1195s. Plan accordingly.

---

## §10 — Step G0.7: Module structure proposal (deliverable 6)

Output: §6 of `backend/G_0_SCOUT_REPORT.md`.

Three options. Trade-offs. Scout's read. Daniel's call at G.0.1.

1. **Option A: New `backend/core/render/` module.** Top-level subdir under core/. Tiling logic + PyMuPDF wrapper land there. dispatch_gate.py calls into render module. Estimated ~300-500 lines new code in render module; dispatch_gate.py change ~30-50 lines (replace pdfplumber calls with render module calls). Vault rule implications: render module is NOT vault-ruled at creation; opens for tuning until ship. Pros: clean separation, easy to test, easy to vault later. Cons: new module surface to maintain.
2. **Option B: Extend existing geometry stages.** Stages 6-9 already do geometry. Tiling fits into the geometry path. Estimated ~200-300 lines added to existing files. Pros: no new module; tiling colocated with consumers. Cons: stages 6-9 are inside dispatch_gate.py — line budget tight; would push dispatch_gate.py over reasonable size.
3. **Option C: Standalone utility imported by dispatch.** Single file `backend/core/render_utils.py`. Estimated ~200-400 lines. Pros: simplest. Cons: not a clean architectural slot — utility files tend to grow into module-shaped messes.

Per option, address:

- **Vault rule implications.** When does the new code seal? Does Phase G's hard gate seal it, or does it stay open through Phase F?
- **dispatch_gate.py line budget impact.** D.2 added 8 lines; E.2.2 added zero. G.1 budget for dispatch_gate.py changes: ≤30 lines is the soft target.
- **Test surface impact.** New tests probably ~10-20. Does this fit cleanly under existing `backend/tests/` structure, or need a new test file?
- **Frontend impact.** None expected (render path is server-side per E.2 strip). Confirm.
- **Migration path.** How does the existing pdfplumber path get retired — all-at-once on G.1 ship, or phase-by-phase?

Format: option-by-option sub-sections, ending with scout's read on the strongest option and the trade-off Daniel is choosing between. ~80-100 lines.

---

## §11 — Step G0.8: Open design questions (deliverable 7)

Output: §7 of `backend/G_0_SCOUT_REPORT.md`.

Numbered list. Scout's read on each. Daniel's call at G.0.1.

Expected questions (scout may add or remove based on what §5-§10 surface):

1. **DPI choice.** 200 vs 250 vs 300?
2. **Tile overlap percentage.** 0% / 2% / 5% / 10%?
3. **Tile geometry.** 2×2 quadrants / 2×3 sextants / dynamic per page size?
4. **Render module structure.** Option A / B / C from §10?
5. **Page-type-driven tiling.** Tile all pages, or only ROOF_PLAN / DETAIL_SHEET / FRAMING_PLAN classifications? Spec-sheet pages may not need tiling.
6. **Pandas integration depth.** Replace pdfplumber's table extraction wholesale, or process pdfplumber's table output? Or skip Pandas in G entirely and revisit later?
7. **Migration timing.** All-at-once cutover from pdfplumber to PyMuPDF on G.1 ship? Or shadow-mode (run both, compare, then cut)?
8. **Silverleaf classification fix scope.** Inside Phase G or split to its own phase? §8 root-cause determines this.
9. **Hard gate composition.** G's hard gate runs the 3-bidset baseline rerun comparison. Should it also include the deferred E.2.2 Silverleaf visual hard gate (single-bidset upload-to-display in Chrome)? Scout's read: yes, bundle them.
10. **Test floor target.** Backend 230 + ~10-20 new render tests = ~240-250. Is the floor a window or a target?

Each question gets:

- One-paragraph context (what's the trade-off?).
- Scout's read with reasoning (one sentence).
- "Your call:" tag.

Format: numbered list, ~60-80 lines.

---

## §12 — Step G0.9: Gate report

Final deliverable: `backend/G_0_SCOUT_REPORT.md`. Single document, structured per §5-§11 above with §0 framing (what scout did, what scout didn't do, sacred floors held throughout) at the top.

Plus appendices:

- **Appendix A:** Pre-flight + post-flight SHA-1 captures.
- **Appendix B:** Sacred floors at session start + session end (backend / frontend / vault / E.1+E.2 production-code SHA-1s).
- **Appendix C:** Wall-clock per scout step.
- **Appendix D:** §13 stop conditions — explicit non-firing status with evidence per stop.

Estimated total length: 600-900 lines of markdown. Honest count over compressed-for-impressiveness.

---

## §13 — Stop conditions (any → halt + report, do not proceed)

1. Sacred floor regresses (backend < 230 OR frontend < 23 at any verification point).
2. Any vault-ruled module SHA-1 changes (5 trade modules + `debug_module.py`).
3. `backend/core/dispatch_gate.py` SHA-1 changes (read-only this phase).
4. Any of the 4 E.1/E.2 production-code SHA-1s changes (`api/main.py`, `routes/jobs.py`, `schemas/jobs.py`, `core/job_storage.py`).
5. CLAUDE.md gets opened or edited.
6. ANY code change in `backend/` source files, including utility scripts. Scout produces zero scripts. The 3-bidset baseline runs (§9) use existing tracked harnesses (`profile_diagnostic.py`, `d2_silverleaf_reference.py`, etc.) or one-shot REPL/notebook execution that does NOT land in a tracked file.
7. `pyproject.toml` modified.
8. `package.json` modified.
9. Any new dependency added (Python or npm). Even a `pip install` to verify a PyMuPDF API call is OUT OF SCOPE — paper research only.
10. Any test added or removed.
11. Frontend HTML modified.
12. `safe_for_removal/` files modified.
13. PROJECT_CLAUDE.md edits exceed surgical updates (G.0 should make zero edits to PROJECT_CLAUDE.md — that's General work post-debrief).
14. `backend/G_0_SCOUT_REPORT.md` is missing or doesn't contain the 7 deliverable sections.
15. Scout report contains code patches, fix proposals, or recommendations not asked for in §5-§11. Scout names problems; does not propose fixes.
16. Push to origin fails.
17. Wall-clock exceeds 5 hours total. The 3-bidset baseline alone is ~42 min; reading + writing the report is ~2-3 hours; total estimate is ~3-4 hours. 5 hours is the soft ceiling; if exceeded with deliverables incomplete, STOP and document.

---

## §14 — Karpathy procedure conformance

G.0 is read-only. Karpathy compliance:

1. **Read first.** All §2 reads in full before any deliverable section is written. The temptation in scout work is to dive into §5 inventory before reading §2; resist. Reading the receipts changes what the inventory should emphasize.
2. **Failing tests first.** Not applicable in this phase — no code changes, no new tests. The "test" of G.0 is whether the scout report enables clean G.0.1 design without further rounds of fact-finding. That's a Daniel-judges measurement, not a code-driven one.
3. **Minimum implementation.** Scout produces only what §5-§11 specify. No "while we're in there" additions. No proposing fixes (§13 #15). If scout finds a bug, scout names it; G.1 fixes it.
4. **Sacred floors held** at every verification point: pre-flight (230/19/0 + 23/23), post-3-bidset-baseline (230/19/0 + 23/23 — running dispatches on existing harnesses doesn't change tests), end-of-session (same).
5. **Stops fire** when something is genuinely uncertain. Don't extrapolate; document and stop.
6. **Diagnostic before action.** Especially at §8 Silverleaf classification root-cause: NAME the bug, do not propose the fix.

The B-16/17/18 anti-pattern (speculation patches without diagnostics) is the explicit thing-to-avoid. G.0 is the diagnostic phase by design — no actions taken, no patches written. If scout's instinct says "I see the fix, let me just…" — STOP. That's G.1 territory.

---

## §15 — Vault rule enforcement

5 trade modules + `debug_module.py` are vault-ruled. SHA-1s captured at pre-flight, verified at session end. G.0 reads these via existing receipts (gate reports, sweep observations, calibration reports) where possible; if direct file read is unavoidable for the inventory, read but do not edit.

`backend/core/dispatch_gate.py` is NOT vault-ruled but is read-only this phase. Same with `api/` and `core/job_storage.py`. SHA-1s captured + verified.

---

## §16 — Done-definition checklist

| # | Item | Verified by |
|---|------|-------------|
| 1 | Pre-flight: 230/19/0 backend, 23/23 frontend, all SHA-1s captured, git status documented | G0.0 |
| 2 | Branch `phase2-v0.3-G0-scout-mission` from `0ddd5a5` | G0.1 |
| 3 | Render path inventory shipped per §5 (every pdfplumber call site mapped, every consumer named) | §1 of report |
| 4 | Dependency audit shipped per §6 (PyMuPDF + Pandas — license, version, footprint, API surface, cost-of-adoption) | §2 of report |
| 5 | Tiling math shipped per §7 (3 DPI options, page sizes, memory profiles, wall-clock estimates, comparison vs pdfplumber) | §3 of report |
| 6 | Silverleaf classification root-cause shipped per §8 (concrete bug name, file:line, condition) | §4 of report |
| 7 | 3-bidset baseline shipped per §9 (Shoppes + Vine Street + Bearss with wall-clock + item counts; cross-check vs existing receipts) | §5 of report |
| 8 | Module structure proposal shipped per §10 (3 options, trade-offs, scout's read) | §6 of report |
| 9 | Open design questions shipped per §11 (numbered list, scout's read on each, "your call" per question) | §7 of report |
| 10 | Sacred floors at session end (backend 230/19/0; frontend 23/23; vault SHA-1s + 4 E.1/E.2 prod-code SHA-1s + dispatch_gate SHA-1 all match pre-session) | G0.2-G0.8 |
| 11 | `git diff` against everything except `backend/G_0_SCOUT_REPORT.md` is empty | G0.9 |
| 12 | `pyproject.toml`, `package.json`, all source files unchanged | G0.9 |
| 13 | CLAUDE.md not opened during session | G0.9 |
| 14 | `safe_for_removal/` files not modified during session | G0.9 |
| 15 | `backend/G_0_SCOUT_REPORT.md` produced; all 17 §13 stop conditions explicitly confirmed non-firing in Appendix D | G0.9 |
| 16 | Scout report contains zero code patches, zero fix proposals not in scope | G0.9 |
| 17 | Single commit on branch with one new file: `backend/G_0_SCOUT_REPORT.md` | G0.10 |
| 18 | Commit pushed to origin | G0.10 |

---

## §17 — Estimated wall-clock

| Step | Estimated |
|------|-----------|
| G0.0 pre-flight (backend tests, frontend tests, SHA-1s, git status) | ~5 min |
| G0.1 branch | <1 min |
| G0.2 render path inventory (read dispatch_gate fully + write §1) | ~30-40 min |
| G0.3 dependency audit (paper research + write §2) | ~30-40 min |
| G0.4 tiling math (numbers + write §3) | ~30-40 min |
| G0.5 Silverleaf classification root-cause (read + investigate + write §4) | ~40-60 min |
| G0.6 3-bidset baseline (sequential dispatch runs) | ~45 min wall-clock (mostly waiting for Vine Street) |
| G0.7 module structure proposal (write §6) | ~20-30 min |
| G0.8 open design questions (write §7) | ~15-20 min |
| G0.9 report finalization (assemble, appendices, verify done-definition) | ~15-20 min |
| G0.10 commit + push | ~3 min |
| **Total** | **~3.5 to 4.5 hours** |

Soft ceiling is 5 hours. Hard ceiling is "the deliverables listed in §16, fully shipped" — if we hit 5 hours and §5-§7 are still incomplete, STOP and report. Don't push past the timeline; deferred deliverables are better than rushed ones.

---

## §18 — What ships at end of G.0

A single markdown file: `backend/G_0_SCOUT_REPORT.md`, ~600-900 lines, covering 7 deliverable sections + 4 appendices. Zero code changes. Sacred floors held. Single commit on `phase2-v0.3-G0-scout-mission`. Pushed.

After Daniel reviews:

- **If scout report enables design without further fact-finding:** Daniel green-lights G.0.1 design phase. Extended-thinking Claude drafts G.1 march orders from scout intel + Daniel's locked answers to §11 questions.
- **If scout report has gaps:** Daniel flags them; G.0 follow-up session to fill the gaps before G.0.1.
- **If scout report surfaces something major (Silverleaf bug is bigger than Phase G; PyMuPDF has a license blocker; etc.):** Daniel decides the next phase shape. G may need to expand, contract, or reshuffle.

Phase G hard gate (when G.1 ships) bundles two things per §11 question 9 default: (a) 3-bidset wall-clock + accuracy A/B vs the §9 baseline; (b) deferred E.2.2 Silverleaf single-bidset visual hard gate in Chrome.

---

## §19 — Reminder: Daniel's locked decisions feeding G.0

| Decision | Locked answer | Where it lives in this phase |
|----------|--------------|-------------------------------|
| Phase G shape | Scout-first (G.0), then design (G.0.1), then build (G.1), then hard gate | §0 + §18 |
| New artifacts mandate (2026-05-01) | Claude does not create downloadable files without explicit Daniel permission. The single G.0 deliverable is permitted because this march orders document explicitly directs its creation. | §1 + §13 #6 (no scripts) |
| Vault rule still active | 5 trade modules + debug_module.py read-only; SHA-1 verified | §15 |
| safe_for_removal/ pending Daniel cleanout | Scout does not touch | §1 + §13 #12 |
| Deferred E.2.2 Silverleaf visual hard gate | Bundled into Phase G's hard gate per directive 2026-05-01 | §11 #9 |
| Karpathy applied | Read first; diagnose, don't fix; STOP when uncertain | §14 |

---

**End of MARCH ORDERS — Phase G.0 Scout Mission.**

Daniel green-lights → Claude Code executes. Single autonomous read-only session. Scout produces intel; design phase happens in a separate G.0.1 session.
