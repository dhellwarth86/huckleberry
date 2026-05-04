# E.2.0 Strip Plan — Huckleberry_AI_6.3.5_Scope.html

**Date:** 2026-04-30
**Branch:** `phase2-v0.3-E2-0-strip-plan`
**Source:** `frontend/Huckleberry_AI_6.3.5_Scope.html` (SHA-1 `cf3765d61fd6f17de46024a3a84c62f25b19b3c5`, 8,694 lines)
**Companion docs:** `E2_0_NEW_FILE_DESIGN.md`, `E2_0_API_CLIENT_SPEC.md`, `E2_0_TEST_FLOOR_PROPOSAL.md`
**Phase:** E.2.0 (read-only diagnostic — this document plans the strip; E.2.1 executes it)

---

## §1 — Strip targets (line ranges)

Each entry below specifies: exact line range, function/block boundary, call sites in surviving code, and disposition of each call site.

### Target S1 — TP namespace (12-stage geometry pipeline JS port)

**Lines:** 1730–2561 (entire `<script>` block including open/close tags)
**Block boundary:** `<script>` at line 1730 through `</script>` at line 2561. Self-contained script block. No surviving code shares this `<script>` tag.
**Content:** `const TP = {};` namespace with 14 pipeline functions: `dispatch`, `zoneMask`, `weightFilter`, `lengthFilter`, `dashFilter`, `clusterUnionFind`, `determineScale`, `perimeterCleanup`, `confidenceScore`, `densityScore`, `rectilinearScore`, `selectFinal`, plus orchestrator `TP.run`, plus domain-type factories (`makePath`, `makeZone`, `makeText`, `makeContext`), plus helpers (`pathLengthInches`, `segIntersects`, `pointInPolygon`, `polygonArea`, `convexHull`, `shoelaceArea`).

**Call sites in surviving code:**

| Call site | Line(s) | In kept region? | Disposition |
|---|---|---|---|
| `TP.run(planSet, opts)` | 3561 | No — inside `runPipeline()` which strips (S7) | (a) delete with caller |
| `TP.run(planSet, opts)` | 4452 | No — inside `runWithOverrides` which strips (S7) | (a) delete with caller |
| `TP.dispatch(planSet)` | 2343 | No — inside `TP.run` itself | (a) deletes with S1 |
| `_TP_run_original` shimming | 4436–4513 | No — pipeline override layer, strips with S7 | (a) delete |
| `buildSyntheticPlan` calls into TP | 3338–3397 | No — inside INTEGRATION_TESTS which strip (S4) | (a) delete with tests |
| `TP.zoneMask` etc in UNIT_TESTS | 3066–3334 | No — strips (S3) | (a) delete with tests |
| `polygonArea` (shoelace) | multiple in TOOL_TESTS | **Yes — TOOL_TESTS survive** | **(c) stub or inline** — `polygonArea` is a pure math function used by annotation tools for SF calculation. E.2.1 must either inline this ~8-line function in the keeper region or preserve it as a standalone utility. |
| `makePath` in TOOL_TESTS | 4678, 4700 | **Yes — TOOL_TESTS survive** | **(c) stub or inline** — `makePath` is used to construct test fixtures. E.2.1 inlines the factory or rewrites the test fixture construction. |

**Net deletion:** ~832 lines.

---

### Target S2 — STAGE_META + pipeline UI functions

**Lines:** 2571–2643
**Block boundary:** Inside Script 2 (`<script>` at line 2566). Starts at `const STAGE_META = [` (line 2571), ends after `consoleLog()` (line 2643).
**Content:** `STAGE_META` array (13 entries), `renderStagesGrid()`, `setStageCardState()`, `formatStatVal()`, `setSidebarStage()`, `consoleLog()`.

**Call sites in surviving code:**

| Call site | Line(s) | In kept region? | Disposition |
|---|---|---|---|
| `renderStagesGrid()` | 4761, 8680 | **Yes — boot function** | (b) replace — boot function calls `renderStagesGrid()` which populates the Pipeline tab. After Pipeline tab strip (S9), this call is removed. |
| `consoleLog()` | 3523–3589, 3666, 3711, 4762 | Partially — 4762 is in boot | (a) delete calls in stripped regions; (b) replace boot call with status-bar init |

**Net deletion:** ~73 lines.

---

### Target S3 — UNIT_TESTS (pipeline unit tests)

**Lines:** 3066–3334
**Block boundary:** `const UNIT_TESTS = [` at line 3066 through `];` at line 3334. Preceded by `assert()` and `approx()` helper declarations (lines 3059–3064) which are **kept** (used by surviving TOOL_TESTS).
**Content:** 88 unit tests covering TP pipeline stages 1–12, helpers, and domain-type factories.

**Call sites in surviving code:**

| Call site | Line(s) | In kept region? | Disposition |
|---|---|---|---|
| `runTestBatch(UNIT_TESTS, ...)` | 3401, 3405 | Yes — `runUnitTests()` / `runAllTests()` | (b) replace — E.2.1 redefines `UNIT_TESTS` as the surviving TOOL_TESTS subset + new API client tests |
| `Array.prototype.push.apply(UNIT_TESTS, TOOL_TESTS)` | 4728 | Yes — test wiring | (b) replace — no longer needed if UNIT_TESTS starts as the combined array |
| `Array.prototype.push.apply(UNIT_TESTS, SCOPE_TESTS)` | 7322 | Strips with SCOPE_TESTS (S12) | (a) delete |

**Net deletion:** ~269 lines of test definitions. `assert()` and `approx()` helpers at 3059–3064 survive.

---

### Target S4 — INTEGRATION_TESTS (pipeline integration tests)

**Lines:** 3336–3398
**Block boundary:** `const INTEGRATION_TESTS = [` at line 3336 through `];` at line 3398.
**Content:** 5 integration tests exercising full `TP.run` pipeline against synthetic plans.

**Call sites in surviving code:**

| Call site | Line(s) | In kept region? | Disposition |
|---|---|---|---|
| `runTestBatch(INTEGRATION_TESTS, ...)` | 3406 | Yes — `runAllTests()` | (b) replace — E.2.1 redefines `INTEGRATION_TESTS` as the new API smoke tests |
| `Array.prototype.push.apply(INTEGRATION_TESTS, SCOPE_INTEGRATION_TESTS)` | 8637 | Strips with SCOPE_INTEGRATION_TESTS (S13) | (a) delete |

**Net deletion:** ~63 lines.

---

### Target S5 — ROOF_VOCAB (roofing vocabulary)

**Lines:** 5018–5143
**Block boundary:** `const ROOF_VOCAB = {` at line 5018 through `};` at line 5143. Inside Script 3 (`<script>` at line 4789).
**Content:** Regex-based vocabulary tables: `systemTypes` (9), `manufacturers` (7), `attachmentMethods` (7), `membraneThickness` (1), `insulationMaterials` (6), `coverBoards` (3), `penetrations` (18), `accessories` (8), `edgeTypes` (12), `systemLabelPatterns`, `roofPlanMarkers`, `detailMarkers`, `specMarkers`, `coverMarkers`.

**Call sites in surviving code:**

| Call site | Line(s) | In kept region? | Disposition |
|---|---|---|---|
| `ROOF_VOCAB.roofPlanMarkers` etc in `classifyPage()` | 5316–5319 | No — `classifyPage` strips (S8) | (a) delete with caller |
| `ROOF_VOCAB.systemLabelPatterns` in `splitBySystemLabels()` | 5171 | No — strips (S6) | (a) delete with caller |
| `findMatches(text, ROOF_VOCAB.systemTypes)` etc in `extractScope()` | 5215–5260 | No — strips (S7a) | (a) delete with caller |
| `ROOF_VOCAB` in `makeScopeSystem()` | ~5217 | No — strips (S7a) | (a) delete |
| `ROOF_VOCAB` in SCOPE_TESTS | 5559–6927 | No — strips (S12) | (a) delete |
| `ROOFING_CONSTANTS.wasteFactor` in `buildTakeoffModel()` | 7007 | **Yes — takeoff (keeper)** | **(c) stub** — `ROOFING_CONSTANTS.wasteFactor` (value `0.10`) is used by the takeoff model. E.2.1 inlines this as a local constant `const DEFAULT_WASTE_FACTOR = 0.10;` in the takeoff section. |

**Net deletion:** ~126 lines.

---

### Target S6 — Text helpers (collectPlanText, findMatches, splitBySystemLabels)

**Lines:** 5149–5191
**Block boundary:** Three standalone functions between ROOF_VOCAB end and extractScope start.
**Content:** `collectPlanText(planSet)`, `findMatches(text, vocabGroup)`, `splitBySystemLabels(allText)`.

**Call sites in surviving code:**

| Call site | Line(s) | In kept region? | Disposition |
|---|---|---|---|
| `collectPlanText(planSet)` | 5194 | No — inside `extractScope` (S7a) | (a) delete with caller |
| `findMatches(...)` | 5219+ | No — inside `extractScope` (S7a) | (a) delete |
| `splitBySystemLabels(...)` | 5208 | No — inside `extractScope` (S7a) | (a) delete |

No surviving code calls these functions. Clean delete.

**Net deletion:** ~43 lines.

---

### Target S7a — extractScope

**Lines:** 5193–5307
**Block boundary:** `function extractScope(planSet) {` at line 5193 through `}` at line 5307 (return + closing brace).
**Content:** Scope inference: walks planSet text, splits by system labels, runs findMatches per vocab group, computes confidence, merges unlabeled systems.

**Call sites in surviving code:**

| Call site | Line(s) | In kept region? | Disposition |
|---|---|---|---|
| `extractScope(App.planSet)` | 5438 | **Yes — `rescanScope()`** | **(b) replace with API call** — after E.2.2, scope comes from `GET /jobs/{id}` trade_outputs. `rescanScope()` becomes a fetch from the API. Until E.2.2 wires it: **(c) stub** returning empty `{ systems: [], rawText: '', lastScanAt: Date.now() }`. |
| `extractScope(App.planSet)` | 5521 | **Yes — `refreshAfterPdfLoad()`** | Same disposition as above — stub then API |
| `extractScope(App.planSet)` | 5544 | **Yes — `selectTrade('roofing')`** | Same disposition |
| `extractScope(planSet)` in SCOPE_TESTS | 5559–6927 | No — strips (S12) | (a) delete |
| `extractScope(planSet)` in SCOPE_INTEGRATION_TESTS | 8051–8635 | No — strips (S13) | (a) delete |

**Net deletion:** ~115 lines.

---

### Target S7b — classifyPage

**Lines:** 5313–5329
**Block boundary:** `function classifyPage(page) {` at line 5313 through `}` at line 5329.
**Content:** Page classifier using ROOF_VOCAB marker arrays.

**Call sites in surviving code:**

| Call site | Line(s) | In kept region? | Disposition |
|---|---|---|---|
| `classifyPage(pg)` | 5472 | **Yes — `renderPagesTab()`** | **(b) replace with API data** — after E.2.2, page_type comes from `dispatch_results.page_type` via API. Until E.2.2: **(c) stub** returning `{ kind: 'OTHER', scores: {}, confidence: 'low' }`. |
| `classifyPage(pg)` | 5524, 5547 | **Yes — `refreshAfterPdfLoad()` / `selectTrade()`** | Same disposition |

**Net deletion:** ~17 lines.

---

### Target S8 — PDF.js operator-list walker (extraction portion of B6)

**Lines:** 2768–2874 (within `extractPlanSetFromPdf`, lines 2757–2917)
**Block boundary:** The operator-list walker sits inside `extractPlanSetFromPdf()`. The function does **two things**: (1) path/text extraction via operator-list walking (lines 2768–2874) and (2) page rendering for the viewer (lines 2882–2917). **Only the walker strips; the rendering stays.**

**CRITICAL SEPARATION:** E.2.1 must rewrite `extractPlanSetFromPdf()` to:
- **KEEP:** PDF loading (lines 2757–2767), page viewport calculation (line 2772), thumbnail rendering (lines 2889–2900), page object construction (lines 2902–2911 minus `paths` and `texts` fields), `_pdfDoc` reference (line 2915).
- **STRIP:** The `FN = pdfjsLib.OPS` variable and the entire `for` loop body that walks `fnArray`/`argsArray` to build `paths[]` and `texts[]` (lines 2768–2874), plus the `zones` auto-detection (lines 2878–2880).
- After strip, each `planSet.pages[]` entry has: `idx`, `page_w_pts`, `page_h_pts`, `renderCanvas: null`, `thumbCanvas`, `renderDPI`, `_pdfPageRef`. No `paths`, no `texts`, no `zones`. Those come from the API.

**Call sites in surviving code:**

| Call site | Line(s) | In kept region? | Disposition |
|---|---|---|---|
| `extractPlanSetFromPdf(ab)` | 3702 | **Yes — `loadPdfFile()`** | **(b) rewrite** — the function is rewritten to do rendering only; paths/texts no longer extracted client-side |
| `getOrRenderPageCanvas(planSet, pageIdx)` | 3778, 2923 | **Yes — Viewer keeper** | **Keep as-is** — this function only renders page canvases, no path extraction |

**Net deletion:** ~107 lines (walker portion). ~55 lines restructured but kept (rendering).

---

### Target S9 — Pipeline tab (markup + handler + state)

**UI markup lines:** 1559–1601 (tab pane `#pane5` — "TRACEPOINT GEOMETRY PIPELINE")
**Tab bar entry:** 1298 (`<div class="tab" onclick="showTab(5)">...PIPELINE</div>`)
**Sidebar pipeline state:** 1251–1287 (sidebar sections "Pipeline State" + "12-Stage Pipeline" + "Karpathy Loop")
**Header stat:** 1224 (`<div class="header-stat" id="hdrStatusPipe">...PIPELINE READY</div>`)
**Status bar items:** 1234 ("ENGINE: TRACEPOINT 12-STAGE"), 1236 ("AI BACKEND: REMOVED"), 1238 ("MODE: 100% OFFLINE · CLIENT-SIDE")

**JS handler functions:**

| Function | Lines | Disposition |
|---|---|---|
| `runPipeline()` | 3516–3597 | (a) delete — pipeline execution UI |
| `resetPipelineUI()` | ~3598–3620 | (a) delete |
| `runPipelineWithOverrides()` | 4403–4460 | (a) delete — viewer sidebar "RUN WITH OVERRIDES" button handler |
| `_TP_run_original` shimming | 4436–4513 | (a) delete |
| `renderStagesGrid()` boot call | 4761, 8680 | (b) replace — remove call |

**Tab numbering impact:** Currently 8 tabs (0–7). Pipeline is tab 5. After removal, tabs renumber to 7 tabs (0–6). `showTab()` indices shift: TESTS becomes tab 5 (was 6), ABOUT becomes tab 6 (was 7). The `_showTab_orig_v62` hook at line 7314 references tab indices — must be updated.

**Viewer sidebar "RUN WITH OVERRIDES" button** (line 1508) and "Pipeline Inputs" section (lines 1503–1510): strips — these feed the pipeline, which is gone.

**CSS:** `.pipeline-stages` styles (lines 192–221), `.stages-grid` / `.stage-card` styles (lines 401–463) — strip. `.console` styles for the pipeline log — strip.

**Net deletion:** ~43 lines markup + ~37 lines sidebar + ~82 lines JS handlers + ~70 lines CSS = ~232 lines.

---

### Target S10 — buildSyntheticPlan + loadSyntheticPlan

**Lines:** 2651–2750 (`buildSyntheticPlan`), 3651–3680 (`loadSyntheticPlan`)
**Block boundary:** Standalone functions.
**Content:** Synthetic plan generator for tests/demos + the "LOAD SYNTHETIC PLAN" button handler.

**Call sites in surviving code:**

| Call site | Line(s) | In kept region? | Disposition |
|---|---|---|---|
| `loadSyntheticPlan()` | 1311 | **Yes — NEW SESSION tab button** | **(a) delete button** — synthetic plans only feed the pipeline. With pipeline gone, the button is meaningless. |
| `buildSyntheticPlan()` in INTEGRATION_TESTS | 3338+ | No — strips (S4) | (a) delete |
| `buildSyntheticPlan()` in TOOL_TESTS | 4678+ | **Yes — TOOL_TESTS** | **(c) stub or inline** — some TOOL_TESTS use `buildSyntheticPlan()` for fixture construction. E.2.1 inlines a minimal plan-object factory for those tests. |
| `_loadSynthetic_original` wrapper | 4770–4774 | Strips with viewer-auto-open patch | (a) delete |

**Net deletion:** ~130 lines.

---

### Target S11 — visualize (geometry canvas visualizer)

**Lines:** 2963–3055
**Block boundary:** `function visualize(planSet, runResult) {` through closing brace.
**Content:** Canvas drawing of all-paths, gate-filtered paths, candidate polygons, winning polygon.

**Call sites in surviving code:**

| Call site | Line(s) | In kept region? | Disposition |
|---|---|---|---|
| `visualize(planSet, result)` | 3592 | No — inside `runPipeline()` (S9) | (a) delete with caller |

Clean delete.

**Net deletion:** ~93 lines.

---

### Target S12 — SCOPE_TESTS

**Lines:** 5559–6927
**Block boundary:** `const SCOPE_TESTS = [` at line 5559 through `];` at line 6927. Plus the `Array.prototype.push.apply(UNIT_TESTS, SCOPE_TESTS)` wiring at line 7322.
**Content:** Tests exercising `extractScope()`, `ROOF_VOCAB`, `classifyPage()`, `makeScopeSystem()`, scope UI rendering, takeoff model — all against the local pipeline's scope output.

**Survival analysis:** Most SCOPE_TESTS test `extractScope` / `ROOF_VOCAB` / `classifyPage` which are all stripping. A small number test `buildTakeoffModel` — these are evaluated in Deliverable 4 (test floor proposal) for potential porting.

**Net deletion:** ~1,369 lines.

---

### Target S13 — SCOPE_INTEGRATION_TESTS

**Lines:** 8051–8637
**Block boundary:** `const SCOPE_INTEGRATION_TESTS = [` at line 8051 through `];` at line 8635. Plus the `Array.prototype.push.apply(INTEGRATION_TESTS, SCOPE_INTEGRATION_TESTS)` wiring at line 8637.
**Content:** End-to-end scope tests: load synthetic plan → extractScope → verify scope systems → verify annotations → verify takeoff model.

**Net deletion:** ~587 lines.

---

### Target S14 — Pipeline-related CSS

**Lines (approximate):**
- `.pipeline-stages` styles: 192–221 (~30 lines)
- `.stages-grid` / `.stage-card` styles: 401–463 (~63 lines)
- `.console` styles (if present): TBD by E.2.1 grep
- `@keyframes pulse`: 222–225 (~4 lines) — only used by pipeline stage animation

**Net deletion:** ~97 lines (estimate; E.2.1 confirms with grep).

---

## §2 — Confirmed strip column

Per Daniel directive 2026-04-30:

| ID | What | Lines | Approx size |
|---|---|---|---:|
| B1 | `TP` namespace (12-stage pipeline JS port) | 1730–2561 | 832 |
| B2 | `ROOF_VOCAB` | 5018–5143 | 126 |
| B3 | `extractScope` | 5193–5307 | 115 |
| B4 | `classifyPage` | 5313–5329 | 17 |
| B5 | Text helpers (`collectPlanText`, `findMatches`, `splitBySystemLabels`) | 5149–5191 | 43 |
| B6 | PDF.js path/text extraction (operator-list walker portion only) | 2768–2874 | 107 |
| Pipeline tab | Markup (1559–1601) + tab bar entry (1298) + sidebar (1251–1287) + header stat (1224) + JS handlers (3516–3620, 4403–4513) + CSS (~192–463 selectively) | scattered | ~232 |
| UNIT_TESTS | Pipeline unit tests | 3066–3334 | 269 |
| INTEGRATION_TESTS | Pipeline integration tests | 3336–3398 | 63 |
| SCOPE_TESTS | Scope/vocab/classifier tests | 5559–6927 | 1,369 |
| SCOPE_INTEGRATION_TESTS | Scope end-to-end tests | 8051–8637 | 587 |
| STAGE_META + pipeline UI | Stage metadata + rendering functions | 2571–2643 | 73 |
| buildSyntheticPlan + loadSyntheticPlan | Synthetic plan generator + handler | 2651–2750, 3651–3680 | 130 |
| visualize | Geometry canvas visualizer | 2963–3055 | 93 |
| runPipeline + overrides | Pipeline execution UI wiring | 3516–3620, 4403–4513 | 215 |
| Status bar copy | "AI BACKEND: REMOVED" / "100% OFFLINE" | 1234–1238 | (rewrite, not delete) |

---

## §3 — Confirmed keepers column

Per Daniel directive 2026-04-30:

| What | Lines (approx) | Notes |
|---|---|---|
| PDF.js page **rendering** (thumbnail + on-demand full-res) | 2757–2767 (setup), 2882–2917 (rendering), 2920–2956 (`getOrRenderPageCanvas`) | Kept portion of B6; rewritten to omit path/text extraction |
| OpenSeadragon viewer | 3725–3860 (Viewer object) | Unchanged |
| Konva annotation overlay | Part of Viewer + TOOL_HANDLERS | Unchanged |
| xlsx export (takeoff Excel) | 6993–7311 (`buildTakeoffModel`, `exportTakeoffToExcel`, `renderTakeoffTab`, `setTakeoffWaste`) | Minor edit: inline `ROOFING_CONSTANTS.wasteFactor` as local constant |
| Manual annotation tools — pin / line / polygon drawing | 4062–4560 (TOOL_HANDLERS + tool UI) | Unchanged |
| TOOL_TESTS | 4565–4723 | Survive; minor edits for inlined dependencies |
| 7 of 8 tabs | NEW SESSION / SCOPE / PAGES / VIEWER / TAKEOFF / TESTS / ABOUT | Pipeline tab struck; tab indices renumber |
| Scope UI rendering | 5335–5555 (`renderScopeTab`, `renderPagesTab`, `rescanScope`, etc.) | Call sites to `extractScope` / `classifyPage` stubbed in E.2.1, wired to API in E.2.2 |
| Viewer fullscreen | 8646–8691 | Unchanged |
| Boot function | 8676–8689 | Edited to remove `renderStagesGrid()` call |
| `assert()` / `approx()` helpers | 3059–3064 | Needed by surviving TOOL_TESTS |
| `escapeHTML()` | 3508–3510 | Used by surviving UI code |
| `withTestIsolation()` / `runTestBatch()` / `runUnitTests()` / `runAllTests()` | 3400–3506 | Test harness mechanics — kept, arrays redefined |
| App state object | 3725–3730 | Kept; `App.planSet` shape changes per §4 |
| `showTab()` hook | 7313–7319 | Edited to remove SCOPE_TESTS push; tab indices updated |
| `renderSyntheticCanvasForViewer()` | 4514–4560 | Stripped if `buildSyntheticPlan` is gone; **or** kept if we want synthetic demo to survive. E.2.1 decision: strip (synthetic demo is pipeline-only). |
| Vertex snap helper | 6929–6985 | Kept — used by corners pin tool |

---

## §4 — planSet shape dependency analysis (LOAD-BEARING)

### §4.1 — Current planSet shape (v6.3.5)

```
planSet = {
  pages: [
    {
      idx: number,              // page index (0-based)
      page_w_pts: number,       // page width in PDF points
      page_h_pts: number,       // page height in PDF points
      paths: Path[],            // STRIPPED — vector paths from operator-list walker
      texts: TextBlock[],       // STRIPPED — text fragments from operator-list walker
      zones: Zone[],            // STRIPPED — auto-detected zones (title_block)
      renderCanvas: Canvas|null,// KEPT — full-res canvas, built on demand
      thumbCanvas: Canvas|null, // KEPT — 40 DPI thumbnail
      renderDPI: number,        // KEPT — target DPI for full-res render (default 150)
      _pdfPageRef: PDFPage,     // KEPT — pdf.js page handle for lazy rendering
    },
    ...
  ],
  _pdfDoc: PDFDocument,         // KEPT — pdf.js document handle
  expected: { sqft: number },   // SYNTHETIC ONLY — not present on real PDFs; strips with synthetic plan
}
```

### §4.2 — Post-strip planSet shape (phase2.v1.0.0)

```
planSet = {
  pages: [
    {
      idx: number,
      page_w_pts: number,
      page_h_pts: number,
      renderCanvas: Canvas|null,
      thumbCanvas: Canvas|null,
      renderDPI: number,
      _pdfPageRef: PDFPage,
    },
    ...
  ],
  _pdfDoc: PDFDocument,
}
```

Fields `paths`, `texts`, `zones`, and `expected` are absent. No surviving code should reference them after E.2.1.

### §4.3 — Fields consumed by kept tools

| Consumer | Field consumed | Origin classification | Post-strip source |
|---|---|---|---|
| **Viewer.toPdfPt()** / **Viewer.toViewerPt()** | `planSet.pages[i].renderDPI` | **(b) Local pdf.js-rendering provided** | Set during `extractPlanSetFromPdf` page setup (kept portion) |
| **Viewer.init()** | `planSet.pages[pageIdx]` (existence, `.idx`) | **(b) Local** | Page object still constructed by kept rendering code |
| **Viewer.init()** | `planSet.pages[pageIdx].renderCanvas` or `thumbCanvas` | **(b) Local** | Built by `getOrRenderPageCanvas()` (kept) |
| **Viewer page picker** | `planSet.pages.length` | **(b) Local** | Array still populated by rendering loop |
| **getOrRenderPageCanvas()** | `page._pdfPageRef` | **(b) Local** | Set during rendering setup |
| **renderPagesTab()** | `App.planSet.pages[].thumbCanvas` | **(b) Local** | Thumbnails built at PDF load time |
| **renderPagesTab()** | `App.planSet.pages[].idx` | **(b) Local** | Set during page construction |
| **renderPagesTab()** | `classifyPage(pg)` → reads `pg.texts`, `pg.paths` | **(c) GAP** — `texts` and `paths` no longer exist locally | **Stub classifyPage** → returns `{ kind: 'OTHER' }` until E.2.2 fetches `page_type` from API |
| **rescanScope()** | `extractScope(App.planSet)` → reads `planSet.pages[].texts` | **(c) GAP** | **Stub extractScope** → returns empty scope until E.2.2 wires API |
| **refreshAfterPdfLoad()** | `App.planSet.pages.length` | **(b) Local** | Available |
| **refreshAfterPdfLoad()** | `extractScope(App.planSet)` | **(c) GAP** | Stub |
| **refreshAfterPdfLoad()** | `classifyPage(pg)` | **(c) GAP** | Stub |
| **buildTakeoffModel()** | `ROOFING_CONSTANTS.wasteFactor` | **(c) GAP** — currently in ROOF_VOCAB-adjacent constant block | **Inline** `0.10` as local constant |
| **Viewer sidebar — "Pipeline Inputs"** | reads `App.manualScale`, pipeline state | Strips with pipeline tab | Delete the section |

### §4.4 — Gap summary

| Gap | Consumed by | Current source (stripped) | Proposed resolution |
|---|---|---|---|
| `extractScope(planSet)` | `rescanScope()`, `refreshAfterPdfLoad()`, `selectTrade()` | `extractScope()` function (S7a) | **(E.2.1)** Stub returning `{ systems: [], rawText: '', lastScanAt: Date.now() }`. **(E.2.2)** Replace stub with `apiClient.getJob(jobId)` → populate scope from `trade_outputs`. |
| `classifyPage(pg)` | `renderPagesTab()`, `refreshAfterPdfLoad()` | `classifyPage()` function (S7b) | **(E.2.1)** Stub returning `{ kind: 'OTHER', scores: {}, confidence: 'low' }`. **(E.2.2)** Replace with API-provided `page_type` per page from `dispatch_results`. |
| `ROOFING_CONSTANTS.wasteFactor` | `buildTakeoffModel()` | `ROOFING_CONSTANTS` block near ROOF_VOCAB | **(E.2.1)** Inline as `const DEFAULT_WASTE_FACTOR = 0.10;` in the takeoff section. |
| `polygonArea()` | TOOL_TESTS, annotation area calculation | `TP` namespace (S1) | **(E.2.1)** Inline the ~8-line shoelace function as a standalone utility. |
| `makePath()` / `makeZone()` | TOOL_TESTS (fixture construction) | `TP` namespace (S1) | **(E.2.1)** Inline minimal factory functions in the test section, or rewrite test fixtures to construct plain objects directly. |

### §4.5 — planSet shape contract for the new file

After E.2.1, the new file's `planSet` is a **rendering-only** data structure:

1. **Local-only fields:** `idx`, `page_w_pts`, `page_h_pts`, `renderCanvas`, `thumbCanvas`, `renderDPI`, `_pdfPageRef`, `_pdfDoc`. All populated by the kept portion of `extractPlanSetFromPdf()`.
2. **No business data:** `paths`, `texts`, `zones` are absent. The new file does not extract or process PDF content — it only renders page images.
3. **Business data comes from the API** (E.2.2): scope systems come from `GET /jobs/{id}` → `trade_outputs`; page classification comes from `dispatch_results.page_type`; annotations round-trip via future `POST /jobs/{id}/annotations`.
4. **planSet is not the data model anymore.** In v6.3.5, `planSet` was the application's primary data store. In phase2.v1.0.0, `planSet` is the page-rendering cache. The application's data model is the API-provided job state.

---

## §5 — Risk areas

### Risk 1 — Annotation tools' planSet dependency (HIGHEST RISK)

**Description:** Annotation tools (pin, line, polygon) use `Viewer.toPdfPt()` and `Viewer.toViewerPt()` for coordinate conversion. These read `planSet.pages[currentPage].renderDPI`. If the page object is missing or `renderDPI` is absent, coordinate conversion breaks and all tools produce wrong positions.

**What could break:** Every annotation placement (pins at wrong coordinates, polygons with wrong vertex positions, measurements with wrong distances).

**Mitigation:** The rendering portion of `extractPlanSetFromPdf()` is kept; it sets `renderDPI` on every page object. `getOrRenderPageCanvas()` is unchanged. As long as the rewrite of `extractPlanSetFromPdf()` preserves the page object shape (minus `paths`/`texts`/`zones`), annotation tools work identically. **Test-before-strip preferred:** E.2.1 should load a real PDF in the new file, open the Viewer, drop a pin, and verify the pin lands where clicked. This is the E.2.debug hard-gate criterion.

### Risk 2 — extractScope stub leaves Scope tab empty

**Description:** After E.2.1, the Scope tab shows nothing because `extractScope` is stubbed. Users who load a PDF see an empty scope.

**What could break:** UX regression — the Scope tab was the primary value surface in v6.3.5.

**Mitigation:** Expected and acceptable. E.2.1's strip is destructive by design; E.2.2 restores Scope tab with API-fed data. The stub prevents JS errors. The status bar shows `UNREACHABLE` or `CONNECTED` to signal the transition state. Document in the About tab that scope is now backend-computed.

### Risk 3 — Tab index renumbering

**Description:** Pipeline tab removal shifts all subsequent tab indices. `showTab(5)` currently opens Pipeline; after removal, it opens Tests. Hardcoded `showTab()` calls scattered through the file will point to wrong tabs.

**What could break:** Button clicks navigate to wrong tabs; keyboard shortcuts if any.

**Mitigation:** E.2.1 must grep all `showTab(` calls and update indices. The `_showTab_orig_v62` hook at line 7314 must update its index checks (currently `if (idx === 1)` for Scope, `if (idx === 2)` for Pages, `if (idx === 4)` for Takeoff — these are all below Pipeline and stay correct, but any tab ≥5 shifts).

### Risk 4 — TOOL_TESTS depending on stripped TP functions

**Description:** Several TOOL_TESTS use `buildSyntheticPlan()`, `makePath()`, `polygonArea()` from stripped regions.

**What could break:** TOOL_TESTS fail at E.2.1 runtime because dependencies are gone.

**Mitigation:** E.2.1 inlines the needed functions (§4.4 gap resolution). These are small pure functions (~8–30 lines each). The test logic itself doesn't change.

### Risk 5 — Boot function calling stripped functions

**Description:** The boot IIFE at lines 8676–8689 calls `renderStagesGrid()` (stripped) and `selectTrade('roofing')` (kept) and `renderViewerSystemControls()` (kept).

**What could break:** JS error at page load if `renderStagesGrid` is undefined.

**Mitigation:** E.2.1 removes the `renderStagesGrid()` call from the boot function. Replace with status-bar initialization and API health check.

---

## §6 — Net line count summary

| Metric | Count |
|---|---:|
| **Pre-strip total** | **8,694** |
| TP namespace (S1) | −832 |
| STAGE_META + pipeline UI (S2) | −73 |
| UNIT_TESTS (S3) | −269 |
| INTEGRATION_TESTS (S4) | −63 |
| ROOF_VOCAB (S5) | −126 |
| Text helpers (S6) | −43 |
| extractScope (S7a) | −115 |
| classifyPage (S7b) | −17 |
| PDF.js walker (S8) | −107 |
| Pipeline tab markup/JS/CSS (S9) | −232 |
| buildSyntheticPlan + loadSyntheticPlan (S10) | −130 |
| visualize (S11) | −93 |
| SCOPE_TESTS (S12) | −1,369 |
| SCOPE_INTEGRATION_TESTS (S13) | −587 |
| Pipeline CSS (S14) | −97 |
| runPipeline + overrides handler (incl. in S9) | (counted in S9) |
| **Total lines deleted** | **~4,153** |
| **New lines added (API client + stubs + status bar)** | **~300–400** (estimated) |
| **Post-strip estimate** | **~4,841–4,941** |
| **Deletion percentage** | **~47.8%** |

This is within the audit's predicted ~3,800–4,100 line target (the difference is the test code — SCOPE_TESTS + SCOPE_INTEGRATION_TESTS alone are ~1,956 lines, which the audit bundled into its aggregate but is now counted separately here).

---

**End of E.2.0 Strip Plan. E.2.1 executes; this document is the specification.**
