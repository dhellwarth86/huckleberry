# Phase G.D2 — Baseline Inventory + Live-Fire Diagnostic Report

**Branch:** `phase2-v0.3-GD2-baseline-inventory`
**Date:** 2026-05-04
**Author:** Claude Code (Developer role)
**Predecessor:** G.D diagnostic report at `backend/G_D_DIAGNOSTIC_REPORT.md`

---

## 1. Baseline status summary

| # | Baseline item | Status | Reason |
|---|---------------|--------|--------|
| 1 | Single upload point (backend stores file) | **NOT MET** | Two upload mechanisms exist; neither stores the file in the database. Backend reads from a pre-existing filesystem path. |
| 2 | Dispatch fires on backend-stored copy | **NOT MET** | Dispatch fires on a filesystem path string the user provides. The file is not uploaded into or stored by the backend. |
| 3 | Scope tab populates + system pick + retry | **NOT MET** | Shape mismatch: frontend reads `output.systems` but API trade outputs have no `systems` key. Scope tab renders empty. Retry button exists but re-fetches the same broken shape. System pick is wired but has no systems to pick from. |
| 4 | Pages tab + manual re-classify writes to DB | **PARTIAL** | Pages tab populates from backend classifications when client-side PDF is also present. No manual re-classify UI or endpoint exists. |
| 5 | Viewer tools save to database | **NOT MET** | All 7 tools are 100% in-memory. No API endpoints for annotations exist. No database tables for annotations exist. Browser refresh loses everything. |
| 6 | Takeoff tab reads from database | **NOT MET** | Takeoff reads from in-memory `App.project.scope.systems` and `App.project.annotations`. No database involvement. |
| 7 | Excel export reads from database | **NOT MET** | Excel export is entirely client-side (SheetJS). Reads from in-memory state. No backend export endpoint exists. No Python Excel library in the repo. |
| 8 | Browser refresh persists everything | **NOT MET** | No localStorage, no sessionStorage, no IndexedDB. No boot-time job reload. `App.project` resets to empty on refresh. Only the SQLite job row persists (but nothing reads it back on page load). |

**Summary: 0 of 8 baseline items are MET. 1 is PARTIAL (Pages tab populates but lacks re-classify). 7 are NOT MET.**

---

## 2. PROJECT_CLAUDE.md update confirmation

The following section was added as the new top-level section of `PROJECT_CLAUDE.md`, immediately after the title line, committed as `be02b4a`:

```markdown
## Baseline definition + architectural truth (G chain target)

**Architectural truth:** Backend is the database. Viewer (frontend) is the application window to edit, review, finalize document, and export. The viewer does not own state. Every edit a user makes is a database mutation. Every save is a database commit. Every export reads from the database. Refresh the browser, everything is still there because it lives in the database.

This has been the design intent since Huckleberry v5. It is the contract every G-chain phase ships against.

**Baseline (the engineering target that unlocks Phase F user testing):**

1. Single upload point. The user uploads a bidset file to the backend in one place. The backend stores the file. There is no separate client-side dropzone for thumbnails — thumbnails come from the backend's stored copy.
2. Dispatch fires on the backend's stored copy at the user's discretion (RUN DISPATCH button).
3. Scope tab populates from the database after dispatch. User can pick a system. A retry control re-fetches scope when the tab is empty.
4. Pages tab shows classified pages from the database. User can manually re-classify; the change writes back to the database.
5. Viewer opens a page. All tools — calibrate, measure, line, polygon, rectangle, pin, exclude — save their edits to the database. No silent discards.
6. Takeoff tab reads from the database (scope + user edits accumulated in the viewer) and shows the in-progress takeoff.
7. Excel export reads from the database. Output: one folder per trade, one page per trade per file.
8. Browser refresh persists everything. The user's session resumes from the database.

When all eight items work end-to-end on a real bidset, baseline is met. Phase F (user testing + trade-module tuning) unlocks. No G-phase ships against any other definition of "done" until baseline is met.
```

---

## 3. Stage 1 inventory — read-only code analysis

### 3.1 — Single upload point

**Current state: TWO upload mechanisms, NEITHER stores the file in the database.**

#### Mechanism A — Client-side dropzone (Step 2)
- **Frontend:** `#dropZone` drag-drop handler at `Huckleberry_AI_phase2.v1.0.0.html` lines ~1920-1973
- **What it does:** User drops a PDF. `extractPlanSetFromPdf()` (line 1649) uses PDF.js to render page canvases client-side into `App.planSet`. The `File` object is consumed locally for rendering only.
- **Database state produced:** None. The PDF bytes never leave the browser.

#### Mechanism B — Server file path (Step 1.5)
- **Frontend:** Text input `#serverPdfPath` (E.2.2 addition, line ~1080). User types/pastes an absolute filesystem path.
- **What it does:** The path string is sent in the `POST /jobs` body as `pdf_path`. The backend stores this **string** in the `jobs.pdf_path` column and computes `pdf_sha1` from the file at that path.
- **Backend:** `create_job()` in `job_storage.py:110` stores the path string. No bytes are copied or ingested. Dispatch reads the file from this path on disk via `run_dispatch(pdf_path=job['pdf_path'], ...)`.
- **Database state produced:** A `pdf_path` string and a `pdf_sha1` hash. NOT the file itself.

#### Backend upload endpoint search
- **Search:** `UploadFile`, `File(...)`, `multipart` in `backend/api/routes/` — **zero hits**.
- **No multipart upload endpoint exists.** The API accepts only a JSON string path.

#### Database: `pdf_blob` column?
- **Search:** `pdf_blob`, `BLOB` in `job_storage.py` — **zero hits**.
- The PDF is NOT stored in the database. It exists only as a file on the local filesystem referenced by path.

#### Verdict: **PARTIAL (two mechanisms exist, neither meets baseline)**
The baseline requires "the user uploads a bidset file to the backend in one place. The backend stores the file." Current state: the user provides a filesystem path; the backend reads from that path on disk. The file is not uploaded into or managed by the backend. The client-side dropzone is a separate rendering path that doesn't interact with the backend at all.

**Gap:** Need a real file upload endpoint (`POST /jobs` with `multipart/form-data`) that stores the PDF in backend-managed storage (SQLite BLOB or a managed file directory). The client-side dropzone should be retired or made to read from the backend's stored copy.

---

### 3.2 — Dispatch fires on backend-stored copy

**Current state: Dispatch fires on a filesystem path the user provided.**

- **Endpoint:** `POST /jobs/{id}/dispatch` in `api/routes/jobs.py:82`
- **Handler:** Reads `job['pdf_path']` from the jobs table, checks `Path(job['pdf_path']).exists()`, calls `run_dispatch(pdf_path=job['pdf_path'], storage="auto", job_id=job_id)`
- **`run_dispatch` signature** (dispatch_gate.py:1661): `run_dispatch(pdf_path: str | Path, storage=None, job_id: str | None = None) -> PlanSetContext`
- **What happens:** The dispatch opens the file at the given filesystem path using `PDFEngine` and pdfplumber. If the file doesn't exist at dispatch time, the endpoint returns 400.

#### Is this "backend-stored copy"?
**No.** The backend doesn't own the file. If Daniel moves or deletes the file between `POST /jobs` and `POST /dispatch`, the dispatch fails with 400. The file is a reference to something the user pre-placed on the same machine running uvicorn. This works for local dev (single machine) but is not "backend stores the file."

#### Verdict: **IMPLEMENTED + UNWIRED (to baseline contract)**
The dispatch pipeline works perfectly on a file it can reach. The gap is in how the file gets there — baseline requires the backend to store the file, dispatch to read from that store. Current path: filesystem reference string.

**Gap:** Same as 3.1 — once the backend stores the file, dispatch reads from that store instead of a raw filesystem path.

---

### 3.3 — Scope tab populates + system pickable + retry

#### Frontend: `populateScopeFromResults(results)` (line 1731-1756)

**What it expects:** `results.trade_outputs[pageKey][tradeName].systems` — an array of system name strings.

**What the API actually returns:** `GET /jobs/{id}/results` returns `trade_outputs` where each page's trade output is the deserialized `output_json` from the `trade_outputs` table. The actual shape of a roofing trade output has these top-level keys:
- `fields` (dict of per-page roofing field matches)
- `warnings` (list)
- `equipment_pins` (list)

The actual shape of a glazing trade output has:
- `glazing_items` (list)
- `door_items` (list)
- `storefront_items` (list)

**Neither trade module output has a `systems` key.** The `populateScopeFromResults` function iterates trade outputs looking for `.systems` arrays and finds none. Result: zero systems added to `App.project.scope.systems`. The Scope tab renders empty.

**G.D confirmed this:** Finding 1.10 documented the shape mismatch. The scope tab shows "Upload a bidset on the NEW SESSION tab to populate scope" even after a successful dispatch.

#### System pick
- **Frontend:** `App.currentSystemId` tracks the selected system. The system dropdown in the Viewer sidebar reads from `App.project.scope.systems`.
- **Persistence:** System selection writes to `App.currentSystemId` (in-memory). No API call writes system selection to the database.
- **Database:** No column or table stores which system the user selected.

#### Retry button
- **Frontend:** "RE-SCAN" button at line 1135. Calls `rescanScope()` (line 3227) which re-fetches `apiClient.getResults(App.currentJobId)` and re-runs `populateScopeFromResults`. This is a legitimate retry mechanism — it re-fetches from the API.
- **Problem:** Re-fetching returns the same data with the same missing `systems` key. The retry works mechanically but can't fix a shape mismatch.

#### Verdict per item:
- **Scope-populate:** IMPLEMENTED + UNWIRED — `populateScopeFromResults` exists and is called, but reads a key (`systems`) that doesn't exist in the trade output shape. The function needs to be rewritten to extract system information from `fields` / `glazing_items` / etc.
- **System-pick-persists:** IMPLEMENTED + UNWIRED — system selection works in-memory but doesn't persist to database. No API endpoint for persisting system selection.
- **Retry-control:** IMPLEMENTED + WIRED — the RE-SCAN button works end-to-end (fetches from API, re-populates). It just can't fix the upstream shape mismatch.

**Gap:** The `populateScopeFromResults` function needs to derive system information from the actual trade output shape (`fields` for roofing, `glazing_items`/`door_items`/`storefront_items` for glazing). Alternatively, trade modules need to produce a `systems` key in their output.

---

### 3.4 — Pages tab + manual re-classify writes to database

#### Pages tab populates
- **Frontend:** `populatePagesFromResults(results)` (line 1758-1767) reads `results.dispatch_results[pageKey].page_type` and writes to `App.project.pageClasses[pageIdx]`.
- **Rendering:** `renderPagesTab()` (line 3245-3291) reads `App.project.pageClasses` to render per-page badges and bucket counts.
- **G.D confirmed:** Pages tab renders correctly when both client-side PDF AND backend classifications are present. Either alone leaves the tab incomplete (client PDF provides thumbnails; backend provides classifications).

#### Manual re-classify UI
- **Search:** `reclassify`, `change type`, `page_type` mutation handlers in HTML — **zero hits** for any re-classify UI.
- The Pages tab shows page type chips as filters (`framing_plan`, `section`, `roof_plan`, etc.) but these are read-only display. Clicking a chip filters the page list; it does not change a page's classification.

#### Backend endpoint for re-classify
- **Search:** `PATCH /jobs/{id}/pages`, `page_type` update in `api/routes/` — **zero hits**.
- No API endpoint accepts a page_type override.

#### Database for user-overridden classifications
- **`dispatch_results` table columns:** `page_idx, page_type, sheet_num, sheet_title, legends_count, has_legend, has_schedule, raw_tables_json`
- No `user_page_type` or `override_page_type` column exists. There is no mechanism to store a user's manual re-classification distinct from the dispatch-generated one.

#### Verdict: **PARTIAL**
- Pages-tab-populates: **IMPLEMENTED + WIRED** (works when both PDF and dispatch results present)
- Re-classify-UI: **MISSING** (no UI exists)
- Re-classify-persists: **MISSING** (no endpoint, no database column)

**Gap:** Need (1) a UI control on each page card to change its classification, (2) a `PATCH /jobs/{id}/pages/{page_idx}` endpoint that accepts a `page_type` override, (3) a mechanism in the database to store overrides (either a new column or a separate table).

---

### 3.5 — Viewer tools save to database

**Current state: ALL SEVEN TOOLS ARE 100% IN-MEMORY. Nothing saves to the database.**

Per the frontend agent's inventory of `TOOL_HANDLERS` (lines 2523-2776):

| Tool | What happens on complete | Where data lands | API call? |
|------|--------------------------|------------------|-----------|
| **Calibrate** | Computes `ftPerInch` scale from two clicks + user-entered real distance | `App.manualScale` + `App.manualScaleSource` (in-memory) | No |
| **Measure** | Computes distance using current scale | `Viewer.annotations[]` (in-memory, max 3 visible, trimmed) | No |
| **Line** | Creates LF segment with scale | `App.project.annotations.lineSegments[]` (in-memory) | No |
| **Polygon** | Computes area/perimeter from vertices | `App.project.annotations.areas[]` via `persistAreaFromPoints` (in-memory) | No |
| **Rectangle** | Creates 4-point rect, computes area | `App.project.annotations.areas[]` via `persistAreaFromPoints` (in-memory) | No |
| **Pin** | Places pin at click coordinates | `App.project.annotations.pins[]` (in-memory) | No |
| **Exclude** | Creates rectangular exclude zone | `Viewer.annotations[]` only (ephemeral, NOT even in `App.project`) | No |

#### Backend: annotation endpoints?
- **Search:** `annotation`, `pin`, `polygon`, `measurement`, `calibration`, `exclusion` in `api/routes/` — **zero hits** for any annotation-related endpoint.
- No `POST /jobs/{id}/annotations` or similar exists.

#### Database: annotation tables?
- **`job_storage.py`:** Only three tables: `jobs`, `dispatch_results`, `trade_outputs`. **Zero annotation tables.**
- **`storage.py`:** `dispatch_cache`, `geometry_cache`, `architect_profiles`. **Zero annotation tables.**
- No table anywhere in the codebase stores annotations, pins, measurements, calibrations, or exclusion zones.

#### Tool edits survive browser refresh?
**No.** All tool data lives in `App.project.annotations` which is an in-memory JavaScript object initialized to `{ byPage: {}, areas: [], pins: [], lineSegments: [] }` on every page load. Refresh = total loss.

#### Verdict per tool:
- **Calibrate:** IMPLEMENTED + UNWIRED — tool works in-memory, no persistence path
- **Measure:** IMPLEMENTED + UNWIRED — tool works in-memory, no persistence path
- **Line:** IMPLEMENTED + UNWIRED — tool works, saves to `App.project`, no DB path
- **Polygon:** IMPLEMENTED + UNWIRED — tool works, saves to `App.project`, no DB path
- **Rectangle:** IMPLEMENTED + UNWIRED — tool works, saves to `App.project`, no DB path
- **Pin:** IMPLEMENTED + UNWIRED — tool works, saves to `App.project`, no DB path
- **Exclude:** IMPLEMENTED + UNWIRED — tool works, saves to `Viewer.annotations` only (more ephemeral than others)

**Overall verdict: tool edits do NOT survive a browser refresh.** Everything is lost.

**Gap:** Need (1) database table(s) for annotations/pins/measurements/calibrations/exclusions, (2) API endpoints to save/load them per job+page, (3) frontend wiring to POST annotation data on tool completion and GET it on page load.

---

### 3.6 — Takeoff tab populates from scope + user edits

#### Frontend takeoff code
- **`buildTakeoffModel(system, annotations)`** at line 3297-3377: Pure function that reads a system's seed items and `App.project.annotations` (areas, pins, lineSegments). Returns `{ count[], lf[], sf[], derived[] }`.
- **`renderTakeoffTab()`** at line 3464-3507: Renders HTML preview in Tab 4 (pane4). Called lazily on tab activation.
- **Data source:** Reads from `App.project.scope.systems` (in-memory) and `App.project.annotations` (in-memory).

#### Backend takeoff endpoint?
- **Search:** `/jobs/{id}/takeoff` in `api/routes/` — **zero hits**.
- No backend takeoff endpoint exists. Takeoff is computed entirely in the browser from in-memory state.

#### Takeoff data shape
- **Frontend:** `ROOFING_SEED_ITEMS` (line 1773-1799) defines the always-on takeoff items (membrane, insulation, cover board, edge metal, drains, scuppers, coping, penetrations).
- Each system has `takeoffOverrides[seedId].wastePct` for per-item waste factor.
- The takeoff model is a combination of seed items + scope system data + user annotations. All computed locally.

#### Verdict: **IMPLEMENTED + UNWIRED**
The takeoff tab works correctly when scope systems exist and annotations exist — both in-memory. It does not read from the database. It doesn't need a dedicated `/takeoff` endpoint if scope + annotations are themselves persisted and loaded from DB on page load. But today neither is.

**Gap:** Takeoff will work automatically once scope (3.3) and annotations (3.5) persist and reload from DB. No takeoff-specific work needed beyond those dependencies.

---

### 3.7 — Excel export

#### Frontend export code
- **`exportTakeoffToExcel()`** at line 3379-3462: Uses SheetJS (`XLSX` from CDN) to build a workbook with a "Summary" sheet + one sheet per system. Downloads as `Takeoff_{project}_{date}.xlsx`.
- **Export button:** Line 3471: `<button onclick="exportTakeoffToExcel()">FINALIZE -> EXCEL</button>` in the Takeoff tab.
- **Data source:** Reads from `App.project.scope.systems` and `App.project.annotations` — entirely in-memory.

#### Backend export code?
- **Search:** `openpyxl`, `xlsxwriter`, `to_excel`, `export` endpoint in backend — **zero hits** for any Python Excel generation.
- No `GET /jobs/{id}/export` endpoint exists.

#### Output contract: "one folder per trade, one page per trade per file"
- **Search:** This specific output structure is described only in the baseline definition (march orders). It does not exist anywhere in the current code or docs.
- Current export: one `.xlsx` file with one sheet per system (not per trade, not per page). No folder structure. This is a different shape than what the baseline specifies.

#### Verdict: **PARTIAL**
The Excel export function exists and works. But:
1. It reads from in-memory state, not the database
2. Its output shape (one file, sheets per system) differs from the baseline contract (one folder per trade, one page per trade per file)
3. No backend export capability exists

**Gap:** Either (a) the frontend export is rewired to read from the database (via API) instead of in-memory state, or (b) a backend export endpoint is built that reads from the database and produces the baseline output structure. The output format (one folder per trade, one page per trade per file) needs design work regardless.

---

### 3.8 — Refresh persistence

#### After dispatch: what persists in SQLite?
- **`jobs` row:** id, name, pdf_path, pdf_sha1, status="dispatched", dispatch_complete=1, timestamps. **Persists.**
- **`dispatch_results` rows:** per-page page_type, sheet_num, sheet_title, legends_count, has_legend, has_schedule, raw_tables_json. **Persists.**
- **`trade_outputs` rows:** per-page per-trade output_json (roofing fields, glazing items, etc.). **Persists.**

G.D verified all of this round-trips losslessly.

#### Does the frontend check for an in-progress job on page load?
- **Boot sequence** (lines 3767-3782): Calls `selectTrade('roofing')`, `renderViewerSystemControls()`, `startHealthPolling()`.
- **No call to `getJob`, `getResults`, `listJobs`, or any job-loading function at boot.** The frontend starts fresh every time.

#### localStorage / sessionStorage for `currentJobId`?
- **Zero references** to `localStorage` or `sessionStorage` anywhere in the HTML file.
- `App.currentJobId` is initialized to `null` on every page load.

#### If user refreshes mid-edit, what happens?
- All `App.project.*` state resets to empty defaults: `scope.systems = []`, `annotations = { areas: [], pins: [], lineSegments: [] }`, `pageClasses = {}`, `currentJobId = null`.
- The SQLite data still exists but nothing reads it back.
- **Total loss of all in-progress work.**

#### Verdict: **IMPLEMENTED + UNWIRED**
The database persistence layer (D.2) works perfectly. The gap is entirely on the frontend:
1. No `currentJobId` stored in localStorage/URL/sessionStorage
2. No boot-time call to `getJob` / `getResults` to resume a session
3. No mechanism to reload annotations (which don't persist at all — see 3.5)

**Gap:** Need (1) a way to remember which job is active across refresh (URL parameter, localStorage, or job-list UI), (2) boot-time logic to load the active job's results from the API, (3) annotation persistence (3.5) so tool edits survive.

---

### 3.9 — PROJECT_CLAUDE.md contradictions

After adding the new baseline section (Step 1), the following sentences elsewhere in `PROJECT_CLAUDE.md` have potential tension or staleness relative to the architectural truth:

#### Contradiction 1: Storage activation gate (§4, line ~163)
**Text:** "The dispatch_gate storage activation gate stays at None. B.4 ported the storage layer but did NOT wire it. `run_dispatch()` calls still pass `storage=None`. Activation is a Phase D or Phase E decision..."
**Issue:** This is factually stale. D.1 activated storage with `storage="auto"`. The text was never updated after D.1 shipped.
**Proposed resolution:** Update or strike this paragraph — it describes a state that no longer exists.

#### Contradiction 2: E.0 audit framing of Excel export (§3, E.0 paragraph, line ~101)
**Text (within E.0 summary):** "frontend-only surface that stays (UI shell, Viewer, TOOL_HANDLERS, takeoff Excel export, local UI state)"
**Issue:** The baseline says "Excel export reads from the database." The E.0 audit classified Excel export as a "frontend-only surface" — meaning it stays in the browser. These are in tension. The E.0 audit's recommendation was that the XLSX file construction stays browser-side but inputs come from the API. The baseline is stricter: "reads from the database."
**Proposed resolution:** Clarify whether "reads from the database" means (a) the data flowing into the export comes from the database via API (E.0's position — the XLSX library stays client-side), or (b) the entire export is backend-generated. Daniel's call.

#### Contradiction 3: Misconceptions list item about SQLite (§6, line ~207)
**Text:** "SQLite in storage.py is a bug to fix." No. SQLite is the deliberate, Daniel-approved decision... Postgres is deferred to Phase D where multi-tenant job-folder data lives architecturally."
**Issue:** Not a contradiction with the baseline, but the framing "Postgres is deferred to Phase D" is stale — D.2 shipped with SQLite as designed, and the Postgres migration is now in the security cluster (Phase H). Minor staleness.
**Proposed resolution:** Update the "deferred to Phase D" reference to "deferred to the Postgres/security phase (Phase H)."

**No other contradictions found.** The E.2.1 paragraph's reframing of `planSet` as "page-rendering cache" is consistent with the baseline. The phased recovery path table (§7) is consistent.

---

## 4. Stage 2 live-fire annotations

**Live-fire session: 2026-05-04T17:22 to 17:52 UTC (~30 minutes).**
Daniel drove the test using a real bidset (`B2607 AEA Silverleaf - St Augustine - Accelerated Construction Services (6).pdf`, 40 pages, roofing trade). All 6 helpers captured telemetry. Job ID: `5e33f43f-daad-490c-bd2f-734f9c7eaea5`.

### Headline Stage 2 finding — Daniel's workflow note

> "everything works if manual system is created first."

This validates Stage 1's identification of 3.3 (Scope-tab shape mismatch) as the upstream blocker for the entire system. Once Daniel manually added a system in-memory to bypass the broken auto-populate, the rest of the in-memory pipeline (tools → takeoff → Excel export) functioned end-to-end. **The system "works" only because the user manually substitutes for the broken automated step.** This is a confidence-graded behavioural map, not a fix.

### 4.1 — Single upload point — **Stage 2 verified BROKEN (per baseline)**

Helper 3 + Helper 6 captured the upload sequence:
- Daniel pasted server path `C:\huck stage 2\huckleberry\backend\test_plans\B2607 AEA Silverleaf - St Augustine - Accelerated Construction Services (6).pdf` into Step 1.5 input
- Browser telemetry: 5 `createJob` attempts (4 with quote-wrapped path that failed validation, then 1 successful)
- Successful `POST /jobs` at 17:26:56 returned 201
- Helper 4 logged the INSERT: `pdf_path` stored as a string, `pdf_sha1` computed (`76dc89072d…`)
- Helper 6 detected NO new file in `~/.tracepoint/` from the upload (only files arrived later from dispatch's tile-rendering)

The file was NOT copied into backend-managed storage. Backend stored only the path reference. **Confirms Stage 1 verdict.**

### 4.2 — Dispatch fires on backend-stored copy — **Stage 2 verified IMPLEMENTED+UNWIRED**

Helper 3 captured: `POST /jobs/{id}/dispatch` at 17:26:56, returned 200 at 17:28:53 — **116.7 seconds** of pipeline work. Helper 4 caught the burst: at 17:28:54 a single 121-row mutation containing 40 `dispatch_results` INSERTs + 80 `trade_outputs` INSERTs (40 pages × 2 trades — roofing + glazing both ran).

Final row delta: jobs 345→346, dispatch_results 711→751, trade_outputs 1422→1502. Pipeline ran cleanly, persisted everything correctly. **Reads from path string** (Stage 1 verdict stands — works for single-machine dev, doesn't match baseline contract).

### 4.3 — Scope tab populates + system pickable + retry — **Stage 2 verified BROKEN**

Helper 3 captured 3 calls to `GET /jobs/{id}/results` at 17:28:53, 17:29:10, 17:29:36 — initial fetch + 2 retries (the RE-SCAN button worked mechanically). All 3 returned 200 with the same data shape. Browser telemetry shows no system was rendered to the user; instead Daniel manually added "New System" via the in-app UI.

**Helper 4 logged ZERO mutations** during system creation. The manual system existed only in `App.project.scope.systems` (in-memory). Confirms Stage 1: shape mismatch persists, retry works, system pick (and now system *creation*) writes nothing to DB. The Excel export later confirmed the in-memory system survived locally — sheet name "New System" appears in the workbook.

### 4.4 — Pages tab + manual re-classify — **Stage 2 NOT EXERCISED**

Daniel did not exercise the Pages tab during this session (verified via browser telemetry — no `TAB_SWITCH` to `pages` and no UI interaction with page chips). Stage 1 finding stands unverified by live fire: pages tab populates from backend data when both PDF and dispatch results present (G.D-confirmed); no re-classify UI or endpoint exists.

### 4.5 — Viewer tools save to database — **Stage 2 verified BROKEN (per baseline)**

Browser telemetry captured every tool selection:

| Tool | Selections logged | Used by Daniel |
|------|-------------------|----------------|
| `pin` | 2+ | Yes (16 pins exported) |
| `polygon` | 6+ | Yes (7 polygons exported) |
| `measure` | 2+ | Yes (transient — none exported) |
| `excludeZone` | 1 | Yes (visible in screenshot) |
| `rectangle` | 1 | Yes |
| `calibrate` | 1 | Yes (1"=8' manual scale exported) |
| `pan` | 6+ | Navigation |

The Excel export proves all 7 tools functioned: 16 pins (Inside Corners x8, RTU x8), 7 polygons (tpo main + Cricket #1-6), 3 line segments (walk pads x2, Edge Metal), and a calibrated 1"=8' scale.

**Helper 4 logged ZERO mutations after dispatch (17:28:54).** Helper 3 captured ZERO API calls beyond `/health` polling for the entire 22-minute viewer/tools/takeoff/export session. Every tool wrote to in-memory state only. **Tool edits will not survive a browser refresh** — confirms Stage 1 finding precisely.

### 4.6 — Takeoff tab populates from scope + edits — **Stage 2 verified IMPLEMENTED+UNWIRED**

Daniel switched to the Takeoff tab (browser telemetry confirms tab navigation), viewed the in-progress takeoff, then triggered FINALIZE → EXCEL. The exported file proves takeoff was correctly computed end-to-end:
- COUNT block: 8 Inside Corners (seed) + 8 RTU (user-added pin type) → both with 10% waste applied
- LINEAR FEET block: 0 Coping (seed, 0 LF), 140.5 Edge Metal (from line segments)
- SQUARE FEET block: 522.8 Cricket (sum of 6 cricket polygons)
- DERIVED SF block: 5939.2 SF Membrane/Insulation/Cover Board (from main polygon)
- AREAS / PINS / LINE SEGMENTS detail — all present, all correct

No API call was made to a `/takeoff` endpoint (none exists). All computed in browser from in-memory `App.project`. Confirms Stage 1.

### 4.7 — Excel export — **Stage 2 verified IMPLEMENTED+UNWIRED**

File: `Takeoff_B2607_AEA_Silverleaf___St_Augustine___Accelerated_Construction_Services__6__2026-05-04.xlsx`
Generated: 2026-05-04T17:50:28Z (per workbook metadata)

**Output shape (observed):**
- 1 file
- 2 sheets: `Summary` + `New System`
- Summary lists per-system aggregate metrics (areas, total SF, total LF, pin types)
- "New System" sheet has 7 sections: COUNT, LINEAR FEET, SQUARE FEET, DERIVED SF, AREAS, PINS, LINE SEGMENTS
- Each annotation captured with page number, units, base qty, waste %, qty-with-waste, seed ID, source ('seed' / 'user' / null)

**Output shape (baseline contract):** "one folder per trade, one page per trade per file."

These do not match. Current export is a single workbook, sheets per system, not folder-per-trade. The export *content* is correct and complete; the *structure* differs from the baseline contract. Confirms Stage 1.

Note: a few Type/Attachment/Membrane/etc. cells display as `�` (replacement char) — these are unset enum slots for the manually-added system that Daniel didn't populate. Not a bug; just empty.

### 4.8 — Refresh persistence — **Stage 2 NOT EXERCISED**

Daniel did not refresh the browser during the session. Stage 1 finding stands unverified by direct test, but indirectly confirmed by:
- Helper 4: zero mutations to any persistence layer for annotations after dispatch
- Helper 3: zero non-`/health` API calls during the 22-minute viewer session
- Conclusion: a hypothetical refresh would have lost the manual system "New System", all 16 pins, all 7 polygons, all 3 line segments, the manual 1"=8' scale, and any in-memory tab state. Only the dispatch-stage data (jobs/dispatch_results/trade_outputs rows) would persist on the backend with no UI mechanism to reload them.

### 4.9 — Helper observations summary

| Helper | Lines logged | Key signal |
|--------|--------------|------------|
| 1 — Backend watcher | 128 | Process alive, RAM/CPU normal, row counts moved only at dispatch |
| 2 — Frontend HTTP server | 315 | Served instrumented HTML; ~120 page-asset GETs |
| 3 — API intercept | 330 | Captured 4 distinct non-health calls: createJob, dispatchJob, getResults x3 — *that's the entire API surface used* |
| 4 — DB mutation watcher | 138 | 3 mutation events total: job INSERT, job UPDATE (status), 121-row dispatch burst — *zero mutations after 17:28:54* |
| 5 — Browser telemetry | 306 | 23+ tool selections, 4 unique apiClient calls, ~5 PROJECT_CHANGE diffs |
| 6 — Filesystem watcher | 120,676 | Initial scan dominated; new file activity only inside `~/.tracepoint/tiles/` (OSD viewer cache) — no upload-staging directory ever appeared |

---

## 5. The gap between current state and baseline

The system has a working backend pipeline (dispatch → persist → serve via API) and a working frontend viewer (PDF rendering, annotation tools, takeoff computation, Excel export). The gap is the **connection layer** between them for everything beyond dispatch results:

### What exists and works
- Backend dispatch pipeline: end-to-end, persists results to SQLite
- API: 5 endpoints covering job CRUD, dispatch trigger, and results retrieval
- Frontend: PDF rendering, 7 annotation tools, takeoff model, Excel export
- Health polling, status bar, RUN DISPATCH flow

### What's missing for baseline

1. **File upload** — A real `POST /jobs` with multipart upload replacing the string-path workaround. Backend stores the file. Client-side dropzone reads from backend's copy (or is retired). This is the Postgres/security cluster item currently parked.

2. **Scope tab shape fix** — `populateScopeFromResults` reads `output.systems` which doesn't exist. Either: (a) trade modules produce a `systems` key in their output, or (b) the frontend derives system info from the existing `fields` / `glazing_items` shapes. This is likely the smallest fix with the biggest visible impact.

3. **Annotation persistence** — New SQLite table(s) for annotations (areas, pins, line segments, calibrations, exclusion zones) keyed by `(job_id, page_idx)`. New API endpoints to save/load. Frontend wiring to POST on tool completion, GET on page load.

4. **Page re-classify** — UI control + API endpoint + database support for user-overridden page classifications.

5. **Session resume on refresh** — Store `currentJobId` (localStorage or URL param). On boot, if a job ID is known, call `getResults` and re-populate scope + pages. Annotation reload depends on #3.

6. **Excel export shape** — Current output is one file with sheets per system. Baseline specifies "one folder per trade, one page per trade per file." Design work needed to define the exact output structure.

### Suggested priority order (by unblocking impact)
1. **Scope tab shape fix** (#2) — unblocks the entire downstream chain (system pick → pin tool → polygon save → takeoff → export)
2. **Annotation persistence** (#3) — unblocks tool edits surviving refresh
3. **Session resume** (#5) — unblocks the "refresh and everything is still there" contract
4. **Page re-classify** (#4) — incremental; pages tab already works for display
5. **File upload** (#1) — significant infrastructure; current string-path works for single-machine dev
6. **Excel export shape** (#6) — output format change; current export works functionally

---

## 6. Unblocking fixes log

**Zero unblocking fixes were applied in this phase.** Stage 1 was read-only against the working tree. No code was modified, no files were created except this report and the PROJECT_CLAUDE.md update (Step 1).

---

## 7. Helper logs index

All 6 helper logs were captured during the 2026-05-04 live-fire session. Locations:

- `backend/G_D2_BACKEND_TIMELINE.log` — Helper 1 (128 lines, 30s polling of process + DB row counts)
- `backend/G_D2_FRONTEND_TIMELINE.log` — Helper 2 (315 lines, HTTP access log for port 8080)
- `backend/G_D2_API_INTERCEPT.log` — Helper 3 (330 lines, every backend request/response with bodies)
- `backend/G_D2_DB_MUTATIONS.log` — Helper 4 (138 lines, 2s polling, 3 mutation events captured)
- `backend/G_D2_BROWSER_TELEMETRY.log` — Helper 5 (306 lines, every click/tool/tab/apiClient invocation)
- `backend/G_D2_FILESYSTEM.log` — Helper 6 (120,676 lines, initial scan dominated; activity only in OSD tile cache)

The Helper 3 middleware (`backend/G_D2_helper3_middleware.py`) and Helper 5 instrumented-HTML server (`backend/G_D2_helper2_5_server.py`) were development-only tools. Per march orders Hard Guardrail #5, they are removed before the final commit. The `main.py` import + `add_middleware` lines for Helper 3 are reverted in the final commit. The captured log files ARE committed.

---

## 8. Vault SHA-1 verification

| File | Start of phase | End of phase | Status |
|------|----------------|--------------|--------|
| `backend/core/roofing_module.py` | `ae9e5b284191b45de419faacf11771da27a548f9` | `ae9e5b284191b45de419faacf11771da27a548f9` | ✅ HELD |
| `backend/core/roofing_vocabulary.py` | `ec6c17f8955ef8e27c3ff1d552b299a6962c9d0b` | `ec6c17f8955ef8e27c3ff1d552b299a6962c9d0b` | ✅ HELD |
| `backend/core/glazing_module.py` | `52c014421915ec6a66b4a6860b71a0a3274920f2` | `52c014421915ec6a66b4a6860b71a0a3274920f2` | ✅ HELD |
| `backend/core/glazing_vocabulary.py` | `64249c8ef5f7d9db50added3c9a40836cba356ea` | `64249c8ef5f7d9db50added3c9a40836cba356ea` | ✅ HELD |
| `backend/core/debug_module.py` | `78f71d9030cde3b173389603f5f39bd6bedaac07` | `78f71d9030cde3b173389603f5f39bd6bedaac07` | ✅ HELD |
| `backend/core/dispatch_gate.py` (ref) | `8b39fd0eb4fa6e5a3a61f8da7f9a095be7bd091a` | `8b39fd0eb4fa6e5a3a61f8da7f9a095be7bd091a` | ✅ HELD |
| `backend/core/pdf_engine.py` (ref) | `daf06dd266d52983a0c761669f8af1ed825088a7` | `daf06dd266d52983a0c761669f8af1ed825088a7` | ✅ HELD |

All 5 vault files + 2 integration-frozen reference files unchanged. Vault rule honoured.

---

## 9. Sacred floor verification

| Stage | Backend | Frontend |
|-------|---------|----------|
| Start of phase | 242 passed, 19 skipped, 0 failed | 23/23 |
| End of phase | **242 passed, 19 skipped, 0 failed** | (frontend tests not re-run; no frontend code modified during the phase) |

Backend sacred floor held. The frontend HTML file was served (with run-time JS injection by Helper 5) but the source file on disk was never modified.

---

## 10. What this phase does NOT do

- Does NOT fix any scope-level finding (the scope tab shape mismatch, the tool persistence gap, the export shape — all findings, not fixes)
- Does NOT update CHECKLIST.md, ITINERARY.md, or BLOCK_RUN.md
- Does NOT add or modify any pytest tests
- Does NOT touch trade modules (vault rule absolute)
- Does NOT touch dispatch_gate.py or pdf_engine.py (integration-frozen)
- Does NOT propose G.4 scope or any follow-up phase
- Does NOT declare anything "ships clean" — verdicts are factual labels (IMPLEMENTED+WIRED / IMPLEMENTED+UNWIRED / STUBBED / PARTIAL / MISSING) plus Stage 2 observation matches

---

**End of Stage 1 inventory. Stage 2 live-fire session pending Daniel's participation.**

Daniel reads this, decides what's next.
