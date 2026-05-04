# E.0 Frontend Audit — Huckleberry_AI_6.3.5_Scope.html

**Date:** 2026-04-30
**Branch:** `phase2-v0.3-E0-api-design-and-frontend-audit`
**Audit target:** `frontend/Huckleberry_AI_6.3.5_Scope.html` (pre-session SHA-1 `cf3765d61fd6f17de46024a3a84c62f25b19b3c5`)
**Audit method:** Read-only; grep + targeted reads; modification = §9 stop (file SHA-1 must match pre-session at session end)
**Companion:** `backend/E0_API_DESIGN.md` (FastAPI surface E.1 builds against)

---

## §4.1 — Structure overview

**Total file size:** 8,694 lines, single self-contained HTML file. Page subtitle: "TracePoint Geometry Engine." Status-bar copy explicitly advertises **`AI BACKEND: REMOVED`** and **`MODE: 100% OFFLINE · CLIENT-SIDE`** — the file was deliberately built as a complete browser-resident takeoff app with no backend dependency.

**Layout (line ranges):**

| Section | Lines | Bytes (approx) | Purpose |
|---|---:|---:|---|
| `<!DOCTYPE>` + `<head>` (CDN imports, `<style>`) | 1–1210 | ~38KB CSS | Layout, theme, components |
| `<body>` markup (header, sidebar, tabs, panes) | 1211–1729 | ~26KB HTML | UI shell; 8 tabs (NEW SESSION / SCOPE / PAGES / VIEWER / TAKEOFF / PIPELINE / TESTS / ABOUT) |
| **Script 1 — TracePoint pipeline** | 1730–2560 | ~830 lines | `TP` namespace: 12-stage geometry pipeline JS port |
| **Script 2 — UI + PDF.js + tests** | 2566–4780 | ~2,215 lines | App state, viewer, tools, PDF.js parsing, UNIT_TESTS, INTEGRATION_TESTS |
| **Script 3 — Scope + viewer integrations + roofing** | 4789–8691 | ~3,902 lines | ROOF_VOCAB, scope extractor, page classifier, takeoff, viewer extensions, scope tests |

**External dependencies (CDN, lines 7–10):**

- `pdf.js@3.11.174` — PDF parsing (text + paths)
- `openseadragon@4.1.0` — pan/zoom for rendered pages
- `konva@9.3.0` — annotation overlay (pin/line/polygon drawing)
- `xlsx@0.18.5` — Excel export

No npm runtime deps for the browser HTML. Test harness uses `jsdom@^29.0.2` (one dependency in `package.json`).

**Storage usage:** None. No localStorage / sessionStorage / IndexedDB references. State lives entirely in JS objects (`App`, `Viewer`, planSet) for the session; nothing persists across reload. (This is the key gap E.1+ closes — D.2 added the SQLite persistence layer, but nothing in v6.3.5 talks to it.)

**Test count per `package.json`:**
- `npm test` → `node run_tests.js Huckleberry_AI_6.3.5_Scope.html`
- Harness output: **`UNIT_TESTS: 118 | INTEGRATION_TESTS: 20 | total: 138`** (verified at E0.0 pre-flight 2026-04-30)
- Collections inside the file:
  - `UNIT_TESTS` (line 3066) — 12-stage pipeline unit coverage
  - `INTEGRATION_TESTS` (line 3336) — pipeline end-to-end scenarios
  - `TOOL_TESTS` (line 4565) — annotation tool behavior (rolled into the 138 count via the same harness)
  - `SCOPE_TESTS` (line 5559) — ROOF_VOCAB and `extractScope` regression coverage
  - `SCOPE_INTEGRATION_TESTS` (line 8051) — scope end-to-end scenarios
- The `npm test:spotchecks` and `npm test:mutations` scripts are separate (not part of the 138 floor); see §6.

---

## §4.2 — Backend-shaped logic in the browser (the heart of the audit)

This is the load-bearing finding. **v6.3.5 is not a thin renderer that displays backend results — it is a complete browser port of the dispatch + roofing-trade pipeline.** It runs in offline mode, ingests the PDF, and produces a roofing scope independently of the Python backend. Every numbered item below is logic that the backend (Phase B + C.2 + dispatch_gate + scope_scanner) already does — duplicated, in JavaScript, executing in the user's browser.

The audit is honest: there is **a lot** of backend-shaped logic here. Approximately **1,170 lines of business logic** out of ~7,000 script lines duplicate backend functions. E.2 cannot be a small surgical strip; it is a re-architecture from "browser app" to "browser viewer."

### Item B1 — TracePoint 12-stage geometry pipeline (`TP` namespace)

- **Lines:** 1730–2560 (~830 lines)
- **What it does:** Pure-function port of the 12 stages: `dispatch`, `zoneMask`, `weightFilter`, `lengthFilter`, `dashFilter`, `clusterUnionFind`, `determineScale`, `perimeterCleanup`, `confidenceScore`, `densityScore`, `rectilinearScore`, `selectFinal`, plus the orchestrator `TP.run`. Includes domain-type factories (`makePath`, `makeZone`, `makeText`, `makeContext`).
- **Comment block at line 1731:** *"TRACEPOINT 12-STAGE GEOMETRY PIPELINE / Faithful JavaScript port of the architecture from the 'TracePoint AI — Technical Report' (April 2026). Every stage is a pure function: input in, { output, log } out. No global state. No I/O. Easy to test in isolation."* — explicitly identified as a port, not a coincidental implementation.
- **Backend equivalent:** `backend/core/dispatch_gate.py` (Stages 1–5 filter pipeline), `backend/core/geometry/*` (Stages 6–9 union-find + scale + perimeter + confidence), `backend/core/scoring/*` (Stages 10–12 density + rectilinear + selection). All fully ported in Phase B.
- **Backend already does this?** **YES — completely.** The Python pipeline is the canonical implementation (216 backend tests pass against it). The JS port was Phase 1's offline-only bet that has now been overtaken by the wired backend.
- **Recommendation:** **MOVE TO BACKEND** — strip in E.2. Frontend stops running the pipeline; instead, frontend POSTs the PDF (or job_id of an already-uploaded PDF) and reads back the resulting `PlanSetContext` shape from the API.

### Item B2 — `ROOF_VOCAB` (roofing vocabulary)

- **Lines:** 5018–5143 (~125 lines)
- **What it does:** Regex-based vocabulary tables for `systemTypes` (9 entries: TPO/PVC/EPDM/Modified Bit/Built-Up/Metal SS/Metal Corr/Shingle/Spray Foam), `manufacturers` (7: Duro-Last, Sika Sarnafil, Carlisle, Firestone, GAF, Johns Manville, Versico), `attachmentMethods` (7), `membraneThickness` (1 regex), `insulationMaterials` (6), `coverBoards` (3), `penetrations` (18), `accessories` (8), `edgeTypes` (12), plus `systemLabelPatterns` and four page-classification marker arrays (`roofPlanMarkers`, `detailMarkers`, `specMarkers`, `coverMarkers`).
- **Comment at line 5034:** *"Mirrors the Python `roofing_materials.py` MANUFACTURERS model"* — explicit acknowledgement that this is a JS mirror of the Python vocabulary.
- **Backend equivalent:** `backend/core/roofing_vocabulary.py` (vault-ruled, SHA-1 `ec6c17f8…`) plus `backend/seeds/roofing_materials.py`.
- **Backend already does this?** **YES.** The Python vocabulary is canonical (Phase C.2 ship; vault-ruled in D-8 follow-up). Drift between the two is a real risk — any backend tuning post-D.2 won't propagate to the browser.
- **Recommendation:** **MOVE TO BACKEND.** Frontend should never touch this. After E.2, vocabulary lives only in the vault-ruled Python file; the API serves matched results, not raw patterns.

### Item B3 — `extractScope` (scope inference / project metadata)

- **Lines:** 5193–5306 (~115 lines)
- **What it does:** Walks the planSet text, splits by `systemLabelPatterns`, runs `findMatches` for every ROOF_VOCAB group per system chunk, computes a confidence score (high/medium/low) based on which fields filled, falls back to a single merged "Inline / unlabeled" system if no labels found.
- **Backend equivalent:** `backend/core/dispatch_gate.py` `_extract_project_metadata()` + scope_scanner + Stage 13 `RoofingModule.analyze` (fields populated per-page via D.1 wiring).
- **Backend already does this?** **YES.** D.1 wires RoofingModule into `run_dispatch`; D.2 persists per-page roofing fields to `trade_outputs.output_json`. The persistence layer's `load_trade_outputs(job_id)` returns exactly what `extractScope` produces in the browser, only authoritative.
- **Recommendation:** **MOVE TO BACKEND.** Browser reads `trade_outputs` via API.

### Item B4 — `classifyPage` (page classification)

- **Lines:** 5313–5329 (~17 lines)
- **What it does:** Scores each page across {ROOF_PLAN, DETAIL, SPEC, COVER, OTHER} via marker matches plus heuristics on long-block count and short-text density; returns kind + scores + confidence.
- **Backend equivalent:** `backend/core/dispatch_gate.py` `_PAGE_TYPE_RULES` + `_classify_page_type()` (calibrated 2026-04-29 per Silverleaf calibration Bug 1).
- **Backend already does this?** **YES.** Stored in `dispatch_results.page_type` per D.2; loadable via `load_dispatch_results(job_id)`.
- **Recommendation:** **MOVE TO BACKEND.** Browser reads `page_type` per page from the API.

### Item B5 — Text-processing helpers (`collectPlanText`, `findMatches`, `splitBySystemLabels`)

- **Lines:** 5149–5191 (~43 lines)
- **What it does:** String concatenation across pages, regex iteration over vocab groups, label-driven chunking.
- **Backend equivalent:** Built into `RoofingModule` and dispatch's text scanners.
- **Recommendation:** **MOVE TO BACKEND** (folds in with B3).

### Item B6 — PDF.js path/text extraction (`buildPlanSetFromPDF` area)

- **Lines:** ~2768–2960 (the operator-list walker that turns pdf.js `getOperatorList()` output into `paths[]` + `texts[]`)
- **What it does:** Walks pdf.js operator list, maintains a save/restore graphics-state stack, emits line segments with stroke width and dash flag, builds a `planSet.pages[]` array.
- **Backend equivalent:** `backend/core/PDFEngine` + pdfplumber integration (B.1 / D.1).
- **Backend already does this?** **YES.** Backend's `PDFEngine` and pdfplumber together produce the same paths + texts the browser walker produces. Backend has already run this path on 4 jobs in D.2 (Silverleaf + Bearss + Shoppes + Vine Street, byte-exact reproducibility on the latter two).
- **Recommendation:** **MOVE TO BACKEND** — the browser shouldn't be running pdf.js operator walks. Backend produces the canonical path/text data and serves it via API or, more economically, never exposes paths to the browser at all (the browser only needs the rendered image + the polygon overlays, not the raw vector paths).

### Item B7 — Roofing seed items + constants + scope merging

- **Lines:** 4805–5017 (~213 lines: ROOFING_SEED_ITEMS + ROOFING_CONSTANTS + `seedSystem` + `mergeScopeProposal` + `_seedVocabNameFor` + helpers)
- **What it does:** Seeds the scope with always-on takeoff items (drain/scupper/coping/edge metal/membrane/insulation/cover board) and merges parser proposals with user edits, enforcing precedence (`seed < parsed < user`).
- **Backend equivalent:** Partially — backend has `roofing_vocabulary.py` and the persistence pieces; the seed-item table itself (with its `unit`/`tool`/`priority`/`vocabRef` shape) doesn't have a clean backend equivalent yet. **This is a frontend takeoff-tooling concern more than a parser concern.**
- **Recommendation:** **KEEP BOTH (rendering layer that needs to know shape).** The seed-item *table* should move to backend (so it can be served to the frontend, possibly per-trade, in E.3+). The merge precedence logic stays in the browser because it deals with live user edits. The frontend will need to know the `unit`/`tool`/`priority` shape to render the takeoff sidebar correctly.

### Item B8 — Test suites (UNIT_TESTS / INTEGRATION_TESTS / TOOL_TESTS / SCOPE_TESTS / SCOPE_INTEGRATION_TESTS)

- **Lines:** 3066–3508 (UNIT_TESTS + INTEGRATION_TESTS), 4565–4768 (TOOL_TESTS), 5559–7416 (SCOPE_TESTS, embedded), 8051–8645 (SCOPE_INTEGRATION_TESTS)
- **What it does:** 138 jsdom-driven tests against the in-browser pipeline + scope extractor.
- **Backend equivalent:** Backend pytest suite (216 tests) covers the same ground from the Python side.
- **Recommendation:** **STAY in the browser file for now**, but they will shrink dramatically in E.2 because most assertions are about the pipeline + extractScope code that's leaving. Keep the harness; replace pipeline tests with API contract tests (E.1 will add ~4 backend tests for the two endpoints; E.2 will likely remove most of the 138 frontend tests as the code they cover gets stripped). Phase E.2 march orders should explicitly account for the test-count change.

### Aggregate

| Category | Approx lines | Recommendation |
|---|---:|---|
| TP pipeline (B1) | 830 | MOVE |
| ROOF_VOCAB (B2) | 125 | MOVE |
| extractScope (B3) | 115 | MOVE |
| classifyPage (B4) | 17 | MOVE |
| Text helpers (B5) | 43 | MOVE |
| PDF.js path walker (B6) | ~190 | MOVE (or eliminate — see §4.5) |
| Seed items + merge (B7) | ~213 | SPLIT (table moves; merge logic stays) |
| Test suites (B8) | ~2,500 | SHRINK in E.2 to match what stays |
| **Total business logic identifiable as backend-shaped** | **~1,320 (excluding tests)** | |

That is roughly 15% of total file lines (1,320 / 8,694) and a much higher fraction of the script-tag content (~22% of the ~6,000 lines of script).

---

## §4.3 — Frontend-only surface that stays

These are the legitimate browser concerns. They survive E.2 and form the spine of the post-strip frontend.

### F1 — UI shell + tabs (lines 1211–1729)

- 8-tab layout (NEW SESSION / SCOPE / PAGES / VIEWER / TAKEOFF / PIPELINE / TESTS / ABOUT)
- Header, sidebar with pipeline state, status bar, footer
- Tab switching (`showTab`)
- **Stays.** Replace tab content with API-fed data; tab structure unchanged.

### F2 — Viewer (OpenSeadragon + Konva, lines 3725–4050)

- PDF page rendering (canvas → tile)
- Pan/zoom (OpenSeadragon)
- Annotation overlay layer (Konva stage + layer)
- Coordinate-system math (PDF points ↔ render canvas px ↔ screen px)
- **Stays.** This is the actual user surface. Backend produces page images (or the frontend renders them client-side); annotations live in the browser until saved.

### F3 — TOOL_HANDLERS (pin/line/polygon/rectangle drawing) (lines 4062–4296 + later integrations)

- Pin placement (count items)
- Line drawing (LF measurements with feet/inches parsing)
- Polygon drawing (SF areas)
- Rectangle drawing (zone selection)
- Vertex snapping (corners pin, lines 8472–8500 the test cases)
- **Stays.** These are real user-interaction surfaces. The drawing math is local; only the *resulting annotation* needs to round-trip to the backend (E.3 endpoint).

### F4 — Takeoff (Excel export, lines 6993–7311)

- `buildTakeoffModel(system, annotations)` — combines scope + annotations into rows
- `exportTakeoffToExcel()` — XLSX generation via the xlsx CDN library
- Per-row waste-factor editing (`setTakeoffWaste`)
- **Stays mostly.** The Excel export library + sheet-construction stays browser-side (no need for a backend Excel route). The *inputs* to the takeoff model (scope + annotations) come from the API.

### F5 — Local UI state (App.\* and Viewer.\* objects)

- `App.project.scope.systems` (current scope)
- `App.project.annotations` (current annotations)
- `Viewer.tool`, `Viewer.currentPage`, `Viewer.tempState` (drawing state)
- `App._pagesFilter` (page-list filter)
- **Stays.** Browser-local view state.

### F6 — Editing UI (form fields, dropdowns, inline edit)

- `updateSystemField`, `updateMembraneField`, `addEmptySystem`, `removeSystem`
- `addPinTypeFromInput`, `removePinType`, `addEdgeTypeFromInput`, etc.
- **Stays.** UI-driven mutations; the *resulting state* round-trips to backend on save (E.3).

### F7 — Test harness (jsdom-driven, run_tests.js + the test arrays)

- **Stays in shape**, shrinks in content. The harness mechanics are sound; what they test changes.

---

## §4.4 — The seam (where frontend gets data after E.2)

**Today (v6.3.5):** the browser parses the PDF, runs the pipeline, runs the scope extractor, and shows everything from local in-memory state. There is no network seam — the status bar literally reads "AI BACKEND: REMOVED."

**After E.1 (FastAPI scaffold + 2 endpoints):** the seam exists but is not yet plumbed into the frontend. The frontend continues working as it does today; backend has `POST /jobs` and `GET /jobs/{id}` available for CLI/test usage.

**After E.2 (frontend strip-and-connect):** browser fetches data from API instead of computing it locally.

### Data the frontend will need to FETCH from backend

| Need | Backend source | API surface |
|---|---|---|
| Job metadata (name, gc, location, status, dates) | `jobs` table via `get_job` | `GET /jobs/{id}` (E.1) |
| Per-page page_type, sheet_num, sheet_title, has_legend, has_schedule | `dispatch_results` via `load_dispatch_results` | `GET /jobs/{id}/results` (E.2) |
| Per-page raw_tables (for schedule pages) | `dispatch_results.raw_tables_json` | included in same endpoint |
| Per-page roofing fields | `trade_outputs` via `load_trade_outputs` | `GET /jobs/{id}/results` (E.2) |
| Per-page glazing/door/storefront items | same | same |
| Debug summary (sections 1/3/6) | new helper that wraps `debug_module.run_debug` | `GET /jobs/{id}/debug` (E.2 or E.3) |
| Job list (sortable) | `list_jobs` | `GET /jobs` (E.2) |

### User actions that need to ROUND-TRIP to backend

| Action | API surface | Phase |
|---|---|---|
| Create a job from a PDF | `POST /jobs` (E.1) — creates row, dispatch happens in E.2's `POST /jobs/{id}/dispatch` | E.1 / E.2 |
| Trigger dispatch for a created job | `POST /jobs/{id}/dispatch` | E.2 |
| Save user-edited scope (manual overrides on roofing fields) | `PUT /jobs/{id}/scope` or `PATCH /jobs/{id}` | E.3 |
| Save annotations (pins/lines/polygons) | `POST /jobs/{id}/annotations` | E.3 |
| Update job status (draft → in_review → exported) | `PATCH /jobs/{id}/status` | E.2 |
| Update job metadata (gc, due date, notes) | `PUT /jobs/{id}` | E.2 |

### What stays local to the browser

- Current view state (which tab, which page, current tool)
- Draft annotations before save (to allow undo without server round-trip)
- UI preferences (zoom level, sidebar collapse state)
- Excel export composition (sheet rows assembled in browser, then download)

---

## §4.5 — E.2 strip targets (prioritized)

E.2 is the strip-and-connect phase. Below is the prioritized removal list, in order of biggest-line-savings × lowest-replacement-complexity.

| Priority | Section/Function | Approx lines | Why removed | What replaces it |
|---:|---|---:|---|---|
| **1** | `TP` namespace + `TP.run` orchestrator (B1) | ~830 | Backend pipeline canonical; D.2 already runs and persists this end-to-end | API response carries finished pipeline output. Frontend never re-runs stages. |
| **2** | Test suites that exercise the pipeline (UNIT_TESTS + INTEGRATION_TESTS for stages 1–12) | ~1,800 of the ~2,500 test lines | Tests cover code that's leaving | E.1 adds 3–4 backend pytest tests via FastAPI TestClient; pipeline coverage stays in backend's 216-test suite |
| **3** | `ROOF_VOCAB` (B2) | ~125 | Vault-ruled Python is canonical | API response carries matched results, not raw patterns |
| **4** | `extractScope` + `collectPlanText` + `findMatches` + `splitBySystemLabels` (B3 + B5) | ~158 | Backend's RoofingModule (vault-ruled) + scope_scanner is canonical | API carries `trade_outputs` per page |
| **5** | `classifyPage` (B4) | ~17 | Backend's `_classify_page_type` is canonical | API carries `dispatch_results.page_type` per page |
| **6** | PDF.js operator-list walker (B6) | ~190 | Backend's `PDFEngine` + pdfplumber is canonical | Either: (a) backend serves rendered page images and the polygon overlays directly — no paths in browser; or (b) backend serves a smaller "render hint" structure. **Decision deferred to E.2 design**, but the operator walker leaves either way. |
| **7** | `STAGE_META` constant + Pipeline tab card rendering | ~14 (constant) + ~130 (rendering) | The Pipeline tab is a debugging surface for in-browser pipeline state; once the pipeline lives in backend, this becomes a separate Debug/Health tab with backend-supplied data | Replace with debug summary panel pulling `GET /jobs/{id}/debug` |
| **8** | `STAGE_META` reverse stub Pipeline-tab visualizations (`renderStagesGrid`, `setStageCardState`, `formatStatVal`, `setSidebarStage`, `consoleLog`, `visualize`) | ~330 | Same reason as #7 | Same |
| **9** | `buildSyntheticPlan` + `loadSyntheticPlan` (synthetic plan generators for tests/demos) | ~310 | Tied to local pipeline; once pipeline is gone, no in-browser need | If retained, becomes a backend test fixture (probably not retained — backend already has 4 real bidsets persisted in cache.db) |
| **10** | Roofing seed-item *table* (the data, not the merge logic) | ~30 | Should be a backend-served per-trade resource | `GET /trades/roofing/seed-items` (post-E.3) |

**Rough strip total:** ~2,000–2,300 lines of business logic + ~1,800 lines of associated tests = approximately **3,800–4,100 lines deleted from v6.3.5** in E.2. That is ~45% of the current file.

The post-E.2 file is plausibly in the 4,500–5,000 line range, dominated by:
- HTML markup (~520 lines, unchanged)
- CSS (~38KB, unchanged)
- Viewer + tools (~1,100 lines, retained)
- Takeoff (~400 lines, retained)
- App state + UI render functions (~600 lines, retained, partly rewritten to consume API)
- API client glue (NEW, ~200–300 lines)
- A small test suite focused on UI behavior + API client (NEW shape, ~500 lines)

**E.2 will not be a small patch.** Plan the orders accordingly.

### Soft observation — "AI BACKEND: REMOVED" is a status-bar lie after E.2

Line 1236: `<div class="sb-item"><span class="sb-label">AI BACKEND:</span> <span class="sb-value" style="color:var(--green);">REMOVED</span></div>`

This is a Phase 1 design statement that becomes incorrect the moment E.2 ships. The string + the "100% OFFLINE · CLIENT-SIDE" mode label below it both need to flip. Trivially handled in E.2's HTML edit pass. Not a stop, not a regression — just a copy update to schedule.

---

## §4.6 — E.3 render targets (what the frontend renders FROM backend data)

These are the new rendering surfaces that backend-fed data unlocks. E.3 is the proper "render the API response" phase; some pieces sneak into E.2 inevitably.

### R1 — Per-page roofing field display (Scope tab + Pages tab)

- **Data source:** `GET /jobs/{id}/results` → `trade_outputs[page_idx]['roofing']['fields']`
- **What renders:** the per-page roofing fields dict (system type, manufacturer, attachment, insulation, cover board, edge types, penetrations) shown grouped by page.
- **UX sketch:** Pages tab gets a per-page expandable "scope detected here" panel listing ROOF_VOCAB hits; Scope tab aggregates these into the existing system-card view. The structure of the existing scope tab (`renderSystemCard`) carries over almost intact — only the *data source* changes from `extractScope(planSet)` to fetched JSON.

### R2 — Per-page glazing items display (when trade_scope includes glazing)

- **Data source:** same endpoint → `trade_outputs[page_idx]['glazing']['glazing_items']` + `door_items` + `storefront_items`
- **What renders:** schedule-page-driven glazing/door/storefront tables. Each item row shows mark, size, type, alias-matched vocabulary entry.
- **UX sketch:** Scope tab gains a Glazing accordion alongside Roofing; per-page detail is in Pages tab.

### R3 — Debug summary panel ("is this dispatch healthy?")

- **Data source:** `GET /jobs/{id}/debug` → debug_module sections 1 (dispatch health), 3 (page intelligence), 6 (legends + quality flags)
- **What renders:** Top-of-screen banner summarizing dispatch_complete + filters_completed + warning count; Pages tab includes per-page legend count and quality-flag indicator; sidebar shows dispatch wall-clock and total error rate.
- **UX sketch:** Replaces the existing Pipeline tab, which currently shows stage-by-stage in-browser pipeline progress. The new tab shows backend dispatch health in the same shape but populated from the debug module output.

### R4 — Job list (Dashboard / sortable)

- **Data source:** `GET /jobs` (E.2 endpoint)
- **What renders:** A new top-level Jobs / Dashboard view (currently absent from v6.3.5 because there's no persistence).
- **UX sketch:** Sortable table — columns: Name, GC, Location, Trade Scope, Bid Due, Status, Created. Click a row to load that job. Per the D.2 jobs-table sortable columns spec.

### R5 — Status transitions (draft → dispatched → in_review → exported)

- **Data source:** `PATCH /jobs/{id}/status`
- **What renders:** A status pill in the header, clickable to transition. Validation: only valid next-states shown (FSM enforced server-side per `_VALID_STATUSES` in `job_storage.py`).

---

## §4.7 — Cross-cutting observations (not graded, surface-only per orders §10 #5)

1. **The status bar's "AI BACKEND: REMOVED" copy is load-bearing** for the v6.3.5 design philosophy and needs deliberate revision in E.2. Not just a string — the Phase 1 design committed to offline-first and the JS pipeline port is the proof of that commitment. Phase E reverses that commitment with Daniel's approval per the §8 next-planning-conversation; the E.2 march orders should call this out as a deliberate policy reversal, not a stealth change.

2. **The frontend's TP.run uses `_TP_run_original` shimming pattern** (lines 4436–4513 and 7985–8021). Two override layers exist (manual-scale override + short-circuit-stage-6 for tests). This pattern is brittle — three different versions of `TP.run` in the same file. After E.2 strips the pipeline, this complexity vanishes with it.

3. **No `node_modules` or build step.** The HTML is self-contained: CDN imports + inline JS + inline CSS. Test harness uses jsdom + Node only. After E.2, the frontend file will likely still be self-contained (CDN + inline) — the frontend doesn't gain a build pipeline just because it gains an API client. This preserves the no-build-step constraint Phase 1 valued.

4. **138 tests is high coverage for a single-file app** but the coverage is concentrated in the pipeline + scope extractor — exactly the code that's leaving. Plan the test re-baseline carefully in E.2.

5. **Memory bug fixes (B-11, B-13, B-15, B-19, B-20) are scattered through the viewer code** — see comments at lines 2882, 3775, 3832, 3863, 3923, 4102, 4119, 4128, 4488, 7417. These are real-bidset learnings (e.g., "Measurements were piling up forever (we saw 196 of them"). They stay; they're viewer concerns, not pipeline concerns.

6. **PDF.js, OpenSeadragon, Konva, and xlsx all stay** — they are the actual frontend stack. No reason to move any of them server-side.

---

## §4.8 — Audit summary

**v6.3.5 is approximately 15% backend-shaped logic by line count, 22% by script-tag content, and approximately 45% by what E.2 will plausibly remove (counting tests).** It was built as a complete offline app and now needs to become a viewer + editor against a backend API. The transition is a re-architecture, not a refactor.

E.2 should be planned with that scale in mind. E.1 builds the API E.2 will consume; the API is small (2 endpoints) but the frontend strip is large.

The frontend audit is honest because soft audits would cause E.2 to under-strip. The recommendations above are graded by replacement clarity:

- **Move with high confidence (vault-backed equivalent exists):** B1, B2, B3, B4, B5, B6 — backend has them all, well-tested, vault-ruled where applicable.
- **Move with deliberation (no clean backend equivalent yet):** B7 seed-item table, R3 debug panel — backend exists but the API shape needs design (E.2/E.3).
- **Stay (legitimate frontend concerns):** F1–F7, R1 rendering, R2 rendering, viewer + tools + takeoff + UI state.

End of audit. Companion: `backend/E0_API_DESIGN.md`.
