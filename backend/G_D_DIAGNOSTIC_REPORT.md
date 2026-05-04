# Phase G.D — End-to-End Diagnostic — Final Report

**Branch:** `phase2-v0.3-GD-diagnostic`
**Date:** 2026-05-04
**Author:** Claude Code (Developer role)
**Bidsets exercised:** Chipotle Tarpon Springs (Cycles 1+2, automated), B2607 AEA Silverleaf (Cycle 3, Daniel-driven)

---

## 1. Honest summary

The system runs end-to-end. Backend starts, dispatches, persists, and serves results. Frontend connects, polls health, drives a real dispatch, and reaches "DISPATCH COMPLETE" without errors. SQLite persistence round-trips losslessly. Sacred floors held throughout (242/19/0 backend, 23/23 frontend). Vault SHA-1s held for all five trade modules and the two integration files (`dispatch_gate.py`, `pdf_engine.py`). Zero unblocking fixes were needed for the system to come up — the gates the prior phases shipped against still hold.

What does *not* work end-to-end is **the rendering layer for trade-module output**. The frontend's `populateScopeFromResults(results)` reads `output.systems` from each trade output, but the API's actual trade-output shape has no `systems` key (only `fields / warnings / equipment_pins / glazing_items / door_items / storefront_items`). Result: the Scope tab renders empty after a successful dispatch, and the entire downstream chain that depends on a selected system — the viewer's PIN palette, the gating message on the Pin tool, the polygon/rectangle save destination — all stay broken. The frontend's hard-coded "(E.2.1: stub returns empty)" alert is still on screen even after the API returns real data, so the user sees no signal that dispatch actually produced anything.

The Pages tab works *only* when the user drops the PDF into the upload dropzone (which runs PDF.js client-side for thumbnails) and runs dispatch (which provides classifications). Either alone leaves the tab empty. The classifications themselves are partially right and partially wrong — Silverleaf's structural framing pages (S100/S101) classify correctly as `framing_plan`, the section sheet A301 classifies correctly as `section`, but A603 (a door schedule) misclassifies as `section`, and a separate finding revealed that `sheet_title` extraction in Filter 1 is grabbing the architect-firm imprint line instead of the actual drawing title (PAGE 28 = ROOF PLAN sheet A106 has `sheet_title="CED Architecture, Inc. Colliers Engineering & Design TAMPA"`). The 4 known UNKNOWN pages on Silverleaf (display PAGE 13/14/39/40, page_idx 12/13/38/39) match the ITINERARY's standing parking item — Filter 1 sheet-detection gap, not a regression.

The diagnostic also found a quieter problem: **the diagnostic's own observation channels can't see most of what users do.** All viewer tools (Pan/Zoom/Calibrate/Measure/Line/Polygon/Rect/Pin/Exclude) run 100% client-side. Tab navigation, chip filtering, polygon drawing — none of it generates events the backend or static-file server can observe. With a user-driven real browser there is no live telemetry channel; the only evidence of any tool-use comes from screenshots the user volunteers. This is itself a finding for any future user-test phase.

The G.3 gate report's claim that Chipotle produces "0 entries in `ctx.trade_module_outputs`" is contradicted by what the API path actually persists — Cycle 1's API dispatch on Chipotle produced **349 roofing fields, 40 glazing items, 24 door items, 0 storefront items** across the 39 pages. The gate report was apparently looking at a different runtime path or different field. This is a real gap between gate claim and on-the-ground reality.

The Silverleaf trade-output aggregate this run is `338/20/81/7` — `+1 storefront` vs. the D.1/D.2 canonical `338/20/81/6`. Minor drift, possibly non-deterministic.

---

## 2. Cycle 1 findings — Backend in isolation (Chipotle, curl)

| # | Finding | Verdict |
|---|---------|---------|
| 1.1 | `/health` returns 200 with `{"status":"ok","version":"0.3.0-E.1"}` | CLEAN |
| 1.2 | `POST /jobs` with valid JSON body returns 201 with full JobResponse including computed `pdf_sha1` | CLEAN |
| 1.3 | `POST /jobs/{id}/dispatch` returns 200 after wall-clock 172.06s with status transition `draft → dispatching → dispatched` and `dispatch_complete=true` | CLEAN (functional); DRIFT (wall-clock 3.4× G.3 in-process baseline of 50s — likely API + persistence overhead, not pipeline regression) |
| 1.4 | `GET /jobs/{id}/results` returns 200 with `{job_id, dispatch_results, trade_outputs}` shape; both subdicts string-keyed by page_idx | CLEAN |
| 1.5 | Chipotle dispatch produces 39 pages, page-type distribution: `general_notes:5, detail_sheet:13, schedule_sheet:10, section:3, roof_plan:3, elevation:1, framing_plan:1, symbol_legend:1, floor_plan:1, site_plan:1`. Zero UNKNOWN. | CLEAN |
| 1.6 | Trade modules **DO** fire on Chipotle through the API path: 349 roofing fields, 40 glazing items, 24 door items, 0 storefront items across 39 pages | **CONTRADICTS G.3 gate report claim** ("Pre-patch and post-patch dispatch on Chipotle both produce 0 entries in `ctx.trade_module_outputs`"). DRIFT — gate report described different code path or different field than what the API persists |
| 1.7 | Backend warnings during dispatch: identical to G.3's recorded `Filter 4 quality gate: 21 of 53 legends removed (32 kept)` — single dispatch warning, byte-identical | CLEAN |
| 1.8 | SQLite state after dispatch: 1 row in `jobs`, 39 rows in `dispatch_results`, 78 rows in `trade_outputs` (39 pages × 2 trades). `pdf_sha1` correctly computed. | CLEAN |
| 1.9 | `POST /jobs` with raw Windows backslash path produces JSON parse error (422). Forward-slash path works. | DRIFT — minor; clients have to pre-normalize Windows paths. Not a defect of the API; backslash is JSON-illegal escape. |
| 1.10 | **Shape mismatch between API trade_outputs and frontend `populateScopeFromResults`:** frontend reads `output.systems` (array of system names), but actual trade-output shape has no `systems` key. Top-level keys are `fields, warnings, equipment_pins, glazing_items, door_items, storefront_items`. | **BROKEN** — cascades to all of Cycle 2's BROKEN findings on Scope tab + Pin tool + polygon save |

**Cycle 1 unblocking fixes:** none required.

---

## 3. Cycle 2 findings — Headless browser through frontend (Chipotle)

Driven by the Claude Preview MCP. Headless Chromium against `http://127.0.0.1:8080/Huckleberry_AI_phase2.v1.0.0.html`. Server file path field made visible by direct DOM manipulation (the dropzone's "drop PDF" handler doesn't fire in headless without a real file event), then RUN DISPATCH clicked via element selector.

| # | Finding | Verdict |
|---|---------|---------|
| 2.1 | Status bar reaches CONNECTED on initial load. Backend version `0.3.0-E.1` displayed in header and sidebar. | CLEAN |
| 2.2 | Health polling fires every 30s as designed; backend logs confirm. | CLEAN |
| 2.3 | RUN DISPATCH flow proceeds through state transitions: button text `▸ RUN DISPATCH` → `CREATING JOB...` → `DISPATCHING — this may take several minutes...` → `LOADING RESULTS...` → `DISPATCH COMPLETE`. Status text `Dispatch complete. Scope and page classifications populated.` | CLEAN |
| 2.4 | Network sequence: `OPTIONS /jobs` (CORS preflight 200) → `POST /jobs` (201) → `POST /jobs/{id}/dispatch` (200 after ~3 min) → `GET /jobs/{id}/results` (200). Zero 4xx/5xx. | CLEAN |
| 2.5 | Cycle 2 results JSON byte-identical to Cycle 1 results JSON (39 pages, identical page_type assignments, identical trade aggregates `349/40/24/0`). API path is deterministic. | CLEAN |
| 2.6 | Browser console: zero errors, zero warnings, zero info messages throughout the session. | CLEAN |
| 2.7 | After dispatch: `App.currentJobId` is set, `App.currentResults` is set, `App.project.pageClasses` has 39 entries, `App.project.scope.systems = []`. | Mixed — pageClasses CLEAN; scope.systems BROKEN (cascades from 1.10) |
| 2.8 | **Scope tab renders empty** with hardcoded alert "Upload a bidset on the NEW SESSION tab to populate scope. Scope data comes from the backend API (wired in E.2.2). Until then, empty." Even with successful dispatch and 78 persisted trade_outputs, the alert stays. The renderer doesn't check that scope was populated; it shows the "stub" copy unconditionally. | **BROKEN** |
| 2.9 | **Pages tab renders empty** in Cycle 2 (no PDF dropped client-side). Tab requires both client-side `planSet` (for thumbnails) AND backend `pageClasses` (for labels). Backend data alone produces no rendering path. | DRIFT (by-design coupling to client-side PDF; revisit in Cycle 3 with real PDF dropped) |
| 2.10 | **Sidebar Job indicator stays "Job: none"** after dispatch. `App.currentJobId` is set but the sidebar text is never re-bound. | BROKEN (cosmetic) |

**Cycle 2 unblocking fixes:** none required.

**Cycle 2 wall-clock:** ~3 min for full UI dispatch flow on Chipotle.

---

## 4. Cycle 3 findings — Daniel-driven (Silverleaf, real browser)

Daniel drove a real Microsoft Edge browser session against the same backend + frontend. Job ID `8b2020a2-5bab-4ad1-a4f0-406082d86a7f`. Bidset: B2607 AEA Silverleaf (40 pages).

### 4.0 Daniel's reports — chronological, verbatim, with backend/frontend correlations

| Time | Daniel report | Backend timeline | Frontend timeline | Correlation |
|------|---------------|------------------|-------------------|-------------|
| 10:05 | (loaded the page) | health 200 | GET HTML 200 | Page loaded clean |
| 10:07 | (reload) | continued health 200 | GET HTML 200 | Reload clean |
| ~10:10 | "ran the in browser test navigated pages. still testing just note" — screenshot showed Tests tab 23/23 PASS in 263ms including 5 API smoke tests | health 200, no 4xx/5xx | API smoke tests fired against live backend, all clean | Frontend test floor 23/23 holds against live backend |
| ~10:13 | "running dispatch on silverleaf put pdf in front end upload and v1.5 backend upload" | OPTIONS /jobs 200, POST /jobs 201, POST /jobs/{id}/dispatch (in flight) | DISPATCHING state captured | Dispatch initiated cleanly; client-side planSet populated by drop, server path filled, both paths active |
| ~10:15 | (dispatch in flight) | dispatch still running | (browser waiting) | ~2 min wait, normal |
| ~10:17 | (dispatch completed) | POST .../dispatch 200, GET .../results 200 | DISPATCH COMPLETE captured | E2E successful |
| ~10:18 | "here is these im goin to go to viewer on page an play with the tools on print" — screenshots of Pages tab full render (40 pages with classifications), Scope tab still empty, NEW SESSION tab showing DISPATCH COMPLETE | nothing (tab nav is client-side) | nothing | Pages tab DOES render with backend classifications when client-side PDF is also present (revises Cycle 2 finding 2.9 — coupling is by-design, not a bug) |
| ~10:23 | "played with tools this is an answer key ignore the tools markings as this is a key only talk about the tools i used that you should have caught did you catch tool usage or should i do it again" — screenshots of viewer with MEASURE (39.8 ft line), AREA polygon, CALIBRATE (scale switched from MANUAL to auto), EXCLUDE zone (1) | nothing | nothing | **FINDING — no live observability for client-side tool actions.** Backend stdout has no entries for tool clicks; frontend HTTP server only sees static GETs. With a real user-driven browser there is no diagnostic channel. |
| ~10:34 | "im in Microsoft edge im goin to click pin tool then try to close polygon which currently has no place to save to once closed so it disappears pin tools are supposed to be popluated from trade modules so no pins to place" | nothing | nothing | Daniel's prediction confirmed by 10:36 screenshots |
| ~10:36 | "played with poly clicked pin tool captured what it said then played with rect tool did you catch any of that" — screenshots: RECT tool drew dashed-green rect (areas: 0 — silently discarded), PIN tool showed "No system selected. Pick a trade and upload a bidset." overlay (gating copy is wrong — Roofing IS picked, bidset IS uploaded; real condition is empty `App.project.scope.systems`), POLYGON tool drew 4-pt polygon (areas: 0 — silently discarded) | nothing | nothing | **BROKEN — asymmetric tool gating:** PIN shows explicit user-facing message; RECT/POLYGON/LINE/MEASURE silently fail to persist. **BROKEN — gating-copy precondition mismatch:** PIN message describes a precondition the user already satisfied. |
| ~10:39 | "interesting played with the sorted files interesting finds" — screenshots filtering by chip: framing_plan(2), section(3), ROOF_PLAN(0) uppercase chip empty, roof_plan(1), detail_sheet(6) | nothing | nothing | DRIFT — UPPERCASE chips are dead UI (don't match lowercase backend page_type keys); page-classifier accuracy mixed (see §4.5) |
| ~10:45 | "interesting finds is dispatch related so frontend does its own dispatch or is this from backend?" | nothing | nothing | Daniel's question answered: classifications are 100% backend (frontend was stripped of `classifyPage` in E.2.1). Confirmed by reading post-strip HTML. |
| 10:48 | "im done unless you have anything you want me to try on my end" | (final cleanup begins) | (final cleanup begins) | End of Cycle 3 |

### 4.1 Silverleaf SQLite final state (job `8b2020a2-...`)

- 40 dispatch_results rows ✓
- 80 trade_outputs rows (40 × 2 trades) ✓
- Aggregate: **338 roofing fields / 20 glazing items / 81 door items / 7 storefront items**
- Page type distribution: `general_notes:5, schedule_sheet:14, framing_plan:2, detail_sheet:6, unknown:4, cover:1, section:3, floor_plan:1, ceiling_plan:1, roof_plan:1, elevation:2`
- Wall-clock (UI): ~2 min from "DISPATCHING" to "DISPATCH COMPLETE"

### 4.2 Drift from D.1/D.2 baseline

PROJECT_CLAUDE.md records D.1+D.2 Silverleaf canonical aggregate as `338/20/81/6` (storefront=6). Cycle 3 produced `338/20/81/7` (+1 storefront). **DRIFT — minor, +1 storefront item.** Possible causes: non-determinism in storefront detection, post-D.2 storefront drift, or a benign threshold-edge case. Logged.

### 4.3 UNKNOWN pages — known parking item

Pages 13, 14, 39, 40 (display) = page_idx 12, 13, 38, 39. All have `sheet_num=None` and `sheet_title=""`. Matches ITINERARY's standing parking item: "Silverleaf pages 12/13/38/39 — Filter 1 sheet-detection gap". **Not a new finding, not a regression.**

### 4.4 sheet_title extraction is wrong (NEW finding)

PAGE 28 of Silverleaf is the building's roof plan (sheet A106). The `dispatch_results.sheet_title` value is:

```
"CED Architecture, Inc. Colliers Engineering / & Design TAMPA / 5"
```

That's the architect/engineer firm imprint from the title-block boilerplate, not "ROOF PLAN". The pattern repeats on multiple pages — Filter 1's title extraction is grabbing the wrong line in the title block. **BROKEN — Filter 1 sheet_title extraction.** Doesn't affect classification (which uses keyword matching against `tb_text` + `pc.title` + `full_text`), but does affect any UI surface or downstream consumer that displays sheet_title to humans.

### 4.5 Page-classifier accuracy on Silverleaf

| Frontend chip | DB classification | Sheet code | Visual | Verdict |
|---------------|-------------------|------------|--------|---------|
| framing_plan(2) | pp 5, 6 | S100, S101 | small drawing + heavy notes | **Likely correct** — S-series = structural, S100/S101 are framing plans |
| section(3) PAGE 31 | section | A301 | building/wall section | **Likely correct** — A301 is conventionally a section sheet |
| section(3) PAGE 36 | section | A603 | schedule grid | **Likely misclassified** — A603 is conventionally a door/window schedule, should be `schedule_sheet` |
| section(3) PAGE 20 | section | G101.1 | mostly text/notes | Ambiguous — G-series is general; could legitimately be a code-section page |
| roof_plan(1) PAGE 28 | roof_plan | A106 | building roof plan | **Likely correct** — single roof plan on single-building project |
| detail_sheet(6) | pp 7, 9, 17, 18, 33, 38 | mixed | mixed | All look reasonable as detail sheets |
| ROOF_PLAN(0) UPPERCASE | n/a | n/a | n/a | **BROKEN UI** — dead chip; doesn't match any backend `page_type` key (which are all lowercase) |

### 4.6 Cycle 3 unblocking fixes

None required.

---

## 5. Unblocking fixes log

**Zero unblocking fixes were applied in this phase.** The system came up clean on its own:

- Backend started cleanly via `uvicorn api.main:app --host 127.0.0.1 --port 8000`
- Frontend served cleanly via `python -m http.server 8080 --directory frontend/src`
- All API endpoints returned expected status codes on first call
- All 7 vault SHA-1s held byte-identical from start to end of phase
- All 242 backend tests passed at start and end
- All 23 frontend tests passed (verified via Tests tab in Cycle 3)

The only minor non-fix annoyance: the Cycle 1 curl POST /jobs first attempt 422'd because Windows backslashes in the path produced JSON-illegal escapes. Re-issuing with forward slashes worked. Not a system fix; client-side curl invocation issue.

---

## 6. Coupling map

Markdown table form per orders. Read-only — gathered from reading source files, not from running.

### Frontend → API

| Frontend call | API endpoint | Frontend file location |
|---------------|--------------|------------------------|
| `apiClient.healthCheck()` | `GET /health` | `Huckleberry_AI_phase2.v1.0.0.html` script block 1 |
| `apiClient.createJob({...})` | `POST /jobs` | script block 1; called by `runDispatchFlow()` ~line 1984 |
| `apiClient.getJob(id)` | `GET /jobs/{id}` | script block 1 |
| `apiClient.dispatchJob(id)` | `POST /jobs/{id}/dispatch` | script block 1; called by `runDispatchFlow()` ~line 1992 |
| `apiClient.getResults(id)` | `GET /jobs/{id}/results` | script block 1; called by `runDispatchFlow()` ~line 1994 |
| `apiClient.listJobs()` | (stub — not implemented) | script block 1 |

### API → core / server functions

| API endpoint | Handler | Calls into core |
|--------------|---------|-----------------|
| `GET /health` | `api/main.py::health` | none |
| `POST /jobs` | `api/routes/jobs.py::create_job_endpoint` | `core.job_storage.create_job`, `core.job_storage.get_job` |
| `GET /jobs/{id}` | `api/routes/jobs.py::get_job_endpoint` | `core.job_storage.get_job` |
| `POST /jobs/{id}/dispatch` | `api/routes/jobs.py::dispatch_job_endpoint` | `core.job_storage.get_job` + `update_job_status`; `core.dispatch_gate.run_dispatch(pdf_path, storage="auto", job_id=job_id)` |
| `GET /jobs/{id}/results` | `api/routes/jobs.py::get_job_results_endpoint` | `core.job_storage.get_job`, `core.job_storage.load_dispatch_results`, `core.job_storage.load_trade_outputs` |

### `core/dispatch_gate.run_dispatch` — major call sites

| Stage / Filter | core function | Reads from | Writes to |
|----------------|---------------|------------|-----------|
| 1 — Document Structure | `run_filter_1` | `engine.extract_text_blocks` (cached) | `ctx.sheet_map`, `ctx.page_to_sheet`, per-page `pc.sheet_number`, `pc.title` |
| 2 — Page Classification | `run_filter_2`, `_classify_page_type_for_filter_2` | `engine.extract_text` (cached), `engine.extract_text_blocks` (cached), `pc.title` (G.2 add) | per-page `pc.page_type` |
| 4 — Legend/Schedule | `run_filter_4`, `_parse_tables_on_page` | `engine.extract_text_blocks` (cached); `pdfplumber.open` (G.3: hoisted to once per dispatch) | per-page `pc.legends`, `pc.raw_tables` |
| 3 — Cross-References | `run_filter_3` | `engine.extract_text_blocks` (cached); `engine.extract_text` (cached) | `ctx.cross_references`, per-trade `trade_score` |
| 5 — Zone Classification | `run_filter_5` | `engine.extract_text_blocks` (cached); `zone_filter.detect_*` | per-page `pc.zones` |
| Stage 13 — Trade modules | `_run_trade_modules` | `engine.extract_text_blocks` (cached); `pdf_page.extract_tables()` (non-schedule fallback) | `ctx.trade_module_outputs[page_idx][trade_name]` |

### Trade module input read fields

`backend/core/trade_module.py::TradeModuleInput`. Trade modules read these fields read-only.

| Field | Read by RoofingModule | Read by GlazingModule | Read by DebugModule |
|-------|-----------------------|------------------------|----------------------|
| `page_index` | yes | yes | yes (via PlanSetContext direct) |
| `page_type` | yes | yes | yes |
| `page_legends` | yes | yes | yes (Section 6) |
| `page_zones` | yes | yes | no |
| `interior_text_blocks` | yes (G.3: now PyMuPDF blocks; was pdfplumber words) | yes | no |
| `tables` (C.3b add) | no | yes | no |
| `project_scope` | yes (5 read sites) | **no** (per recon-cascade-map) | yes (Section 1) |
| `polygon_*` | zero/empty in current dispatch (Stages 6–9 not wired) | not read | not read |

**Note:** DebugModule does NOT follow TradeModule Protocol; it receives `PlanSetContext` directly per recon-cascade-map.

### Storage / cache layer

| Path | Layer | Lifecycle |
|------|-------|-----------|
| `~/.tracepoint/cache.db` | shared SQLite for storage + job_storage | persistent across sessions |
| Table `dispatch_cache` | StorageEngine (B.4 ported) | keyed by `pdf_hash` |
| Table `geometry_cache` | StorageEngine | keyed by `(pdf_hash, page_number)` |
| Table `architect_profiles` | StorageEngine | keyed by `firm_name` |
| Table `jobs` | D.2 job_storage | keyed by job UUID |
| Table `dispatch_results` | D.2 job_storage | keyed by `(job_id, page_idx)` |
| Table `trade_outputs` | D.2 job_storage | keyed by `(job_id, page_idx, trade_name)` |
| `PDFEngine._extract_cache` (G.3) | in-memory dict | per `id(pdf_doc)`; purged on `engine.close(pdf_doc)` |

---

## 7. Vault SHA-1 verification

| File | Pre-phase | Post-phase | Status |
|------|-----------|------------|--------|
| `backend/core/roofing_module.py` | `ae9e5b284191b45de419faacf11771da27a548f9` | `ae9e5b284191b45de419faacf11771da27a548f9` | ✓ HELD |
| `backend/core/roofing_vocabulary.py` | `ec6c17f8955ef8e27c3ff1d552b299a6962c9d0b` | `ec6c17f8955ef8e27c3ff1d552b299a6962c9d0b` | ✓ HELD |
| `backend/core/glazing_module.py` | `52c014421915ec6a66b4a6860b71a0a3274920f2` | `52c014421915ec6a66b4a6860b71a0a3274920f2` | ✓ HELD |
| `backend/core/glazing_vocabulary.py` | `64249c8ef5f7d9db50added3c9a40836cba356ea` | `64249c8ef5f7d9db50added3c9a40836cba356ea` | ✓ HELD |
| `backend/core/debug_module.py` | `78f71d9030cde3b173389603f5f39bd6bedaac07` | `78f71d9030cde3b173389603f5f39bd6bedaac07` | ✓ HELD |
| `backend/core/dispatch_gate.py` (reference; not vault) | `8b39fd0eb4fa6e5a3a61f8da7f9a095be7bd091a` | `8b39fd0eb4fa6e5a3a61f8da7f9a095be7bd091a` | ✓ unchanged |
| `backend/core/pdf_engine.py` (reference; not vault) | `daf06dd266d52983a0c761669f8af1ed825088a7` | `daf06dd266d52983a0c761669f8af1ed825088a7` | ✓ unchanged |

**All five vault-ruled trade modules held SHA-1-identical for the entire phase. No edits. No exceptions.**

---

## 8. Sacred floor verification

| Stage | Backend | Frontend |
|-------|---------|----------|
| Pre-phase (start of GD) | 242 passed, 19 skipped, 0 failed | 23/23 (verified via Tests tab in Cycle 3) |
| Post-phase (end of GD) | **242 passed, 19 skipped, 0 failed** | **23/23** |
| Delta | 0 | 0 |

**Floors held.** Zero new tests added, zero existing tests modified (per orders).

---

## 9. Helper logs index

All under `backend/`:

- `G_D_BACKEND_TIMELINE.log` — Helper 1 stdout (uvicorn). 56 lines. Captures startup + all incoming request lines.
- `G_D_FRONTEND_TIMELINE.log` — Helper 2 (HTTP server) stdout. 13 lines. Captures static GETs from automated browser (Cycle 2) and Daniel's real browser (Cycle 3).
- `G_D_chipotle_results.json` — Cycle 1 raw API results (`GET /jobs/{id}/results` body) for Chipotle.
- `G_D_chipotle_cycle2_results.json` — Cycle 2 same shape, Chipotle.
- `G_D_chipotle_db.json` — Cycle 1 SQLite dump (jobs row, dispatch_results, trade_outputs summary) for Chipotle.
- `G_D_silverleaf_db.json` — Cycle 3 SQLite full dump for Silverleaf job `8b2020a2-...`.

**Helper 2 Playwright/Selenium script:** none was created. The Claude Preview MCP was used in lieu of Playwright for Cycle 2; the MCP holds no script that needs deletion. Cycle 3 used a real Daniel-driven browser, with the Python `http.server` as the only "Helper 2" component (already terminated).

**Cycle 2 screenshots:** captured inline in the conversation transcript, not saved to disk by the Preview MCP. The Preview MCP's `screenshot` tool returns JPEG bytes inline only. This is a documentation gap — for future user-test phases, screenshots should be captured by a tool that writes to disk.

**Cycle 3 screenshots:** all provided by Daniel in conversation. Multiple PNGs covering NEW SESSION, SCOPE, PAGES (multiple chip filters), VIEWER (multiple tools), TESTS, ABOUT.

---

## 10. Findings index — verdict by category

### CLEAN
- Backend startup, /health, all four /jobs endpoints
- API ↔ SQLite round-trip
- Cycle 1 ↔ Cycle 2 byte-identical results (deterministic API)
- Frontend health polling, status bar 3-state machine
- RUN DISPATCH end-to-end flow
- Pages tab rendering when both client-side PDF + backend classifications present
- Sacred floors (backend 242/19/0, frontend 23/23)
- Vault SHA-1s on all five trade modules

### DRIFT
- Cycle 1 wall-clock 172s vs G.3's 50s (3.4× — API + persistence overhead)
- Silverleaf storefront `+1` from D.1/D.2 baseline (`338/20/81/7` vs `338/20/81/6`)
- UPPERCASE filter chips (`ROOF_PLAN`, `DETAIL`, `SPEC`, `COVER`, `OTHER`) all show 0 — dead UI, don't match lowercase backend keys
- Diagnostic infrastructure has no live observability for client-side action telemetry — by-design gap, not a defect

### BROKEN
- Scope tab renders empty even after successful dispatch (shape mismatch: frontend reads `output.systems`, API has none)
- Sidebar "Job: none" never updates after dispatch
- Pin tool gating message describes wrong precondition ("Pick a trade and upload a bidset" — already done; real condition is empty `App.project.scope.systems`)
- Asymmetric tool gating: PIN warns; RECT/POLYGON/LINE/MEASURE silently fail to persist
- Filter 1 `sheet_title` extraction grabs firm imprint instead of drawing title (Silverleaf PAGE 28 sheet A106 has `sheet_title="CED Architecture, Inc. Colliers Engineering & Design TAMPA"`)
- G.3 gate report claim ("0 entries in `ctx.trade_module_outputs`" on Chipotle) **contradicted** by API path producing 349/40/24/0
- Likely-misclassified Silverleaf PAGE 36 (sheet A603, schedule grid) classified as `section`

### KNOWN PARKED (per ITINERARY)
- Silverleaf UNKNOWN pages 12/13/38/39 — Filter 1 sheet-detection gap

---

## 11. What was NOT done in this phase

Per orders §10 ("Hard guardrails"):

- No edits to any of the 5 vault trade modules
- No edits to `dispatch_gate.py` or `pdf_engine.py`
- No new pytest tests
- No canon updates (CHECKLIST / ITINERARY / PROJECT_CLAUDE / BLOCK_RUN unchanged)
- No follow-up phase drafts
- No fixes to scope-level findings (page-classifier accuracy, trade-module output values, sheet_title extraction, frontend Scope tab, Pin tool gating copy — all logged as findings, not fixed)

This phase produced data, not code.

---

**End of report.**

Daniel reads this, decides what's next.
