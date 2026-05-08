# Phase G.4 — Hard Gate Report

**Branch:** `phase2-v0.3-G4-scope-fix-and-backend-storage` (HEAD = `a1d8ded`, +canon commit pending)
**Predecessor:** `phase2-v0.3-GD2-baseline-inventory` head `5292994`
**Started:** 2026-05-04 (per original march orders date)
**Hard gate executed:** 2026-05-07 (Daniel-driven empirical run)
**Verdict: HARD GATE PASS — 11/11 CP MET.**

---

## 1. Honest summary

Phase G.4 ships the architectural rewrite Daniel locked mid-phase: **frontend = window only; backend = source of truth; every user edit is a database mutation; refresh-the-browser rehydrates everything from the database; "migrate later" is the failure mode**. Six commits across four checkpoints + two polish sub-checkpoints, no `dispatch_gate.py` or vault edits, sacred floor moved 242 → 255/19/0 backend (+13 tests net) and 23 → 28 frontend (+5 tests net).

Three baseline items moved from NOT MET to MET:
- **Item 1** (single upload point — backend stores file): MET via multipart `POST /jobs/upload` writing to `~/.tracepoint/uploads/{job_id}/source.pdf`. JSON path-string `POST /jobs` and the client-only dropzone render path are both retired.
- **Item 2** (dispatch fires on backend-stored copy): MET as a side effect of item 1; `run_dispatch` reads `jobs.pdf_path` which now points at the managed-storage location.
- **Item 3** (scope tab populates + system pick + retry): MET via `scope_systems` SQLite table + 5 CRUD endpoints + frontend render-and-relay pattern. Auto-populated from `ctx.project_scope` when system_confidence ≥ 0.7; manual-entry fallback when below threshold; PATCH-on-blur for every editable field; refresh-survival via localStorage rehydrate of `currentJobId`.

Items 4–8 (page reclassify, viewer tools save to DB, takeoff DB read, Excel backend, full session resume) remain deferred to G.5/c.2 per the plan. The `scope_systems` CRUD pattern shipped here becomes the template those phases reuse.

Empirical verification: Daniel drove Silverleaf (manual-entry path; `system_confidence=0.0`) and Taco Bell (auto-detect path; `system_confidence=0.95`) live through the running stack. All 11 hard-gate matrix rows CP MET. The Taco Bell scope card alone is the architectural rule made visible.

---

## 2. Commit chain

| Commit | CP | One-line summary |
|---|---|---|
| `8f1de64` | CP1 | scope tab as full backend-DB-frontend cycle (new tables `job_project_scope` + `scope_systems`; CRUD endpoints; render+relay frontend; 9 backend tests + 5 frontend smoke tests) |
| `6e4fb8f` | CP1.1 | empty-state copy + sidebar Job indicator + polling-pattern dispatch (replaces 240s timeout that was failing on bidsets > ~40 pages) |
| `25481f7` | CP1.2 | bridge API ScopeSystem shape to legacy viewer + takeoff readers (`_flattenScopeRow` helper) |
| `9b7b989` | CP2 | backend file upload + storage + `GET /jobs/{id}/pdf` (multipart endpoint, `~/.tracepoint/uploads/`, 7 new tests) |
| `845327e` | CP3 | kill dropzone-only client render + path-string mode; single upload point (delete `create_job_endpoint` + `JobCreateRequest`; rewire frontend; 3 retired tests, 1 new) |
| `a1d8ded` | CP4 | PROJECT_CLAUDE.md cleanup — 4 edits per plan |

---

## 3. The 11-row hard-gate verification matrix

Daniel drove the matrix live across two bidsets on 2026-05-07. Each row labelled CP MET / CP MET WITH NOTE / CP BROKEN per etiquette norm.

| # | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | PDF stored backend-side | **CP MET** | Taco Bell (62 MB, 88 pp) and Silverleaf (~19 MB, 40 pp) uploads landed at `~/.tracepoint/uploads/{job_id}/source.pdf` — verified earlier via `get_uploaded_pdf_path` SHA-1 round-trip on job `83c695cb-…` (Silverleaf SHA-1 `76dc89072d…` byte-identical to G.D2 §4.1 historical capture). |
| 2 | Multipart upload reached backend | **CP MET** | uvicorn log line `POST /jobs/upload HTTP/1.1 201 Created`. `python-multipart>=0.0.20` declared in `pyproject.toml`. JSON path-string variant deleted in CP3. |
| 3 | Frontend round-trip via GET /pdf | **CP MET** | `apiClient.getPdf(id)` returns Blob; `await blob.arrayBuffer()` feeds `extractPlanSetFromPdf`. Live test: `curl http://127.0.0.1:8000/jobs/83c695cb-…/pdf -o /tmp/cp2_roundtrip.pdf` returned 19,188,443 bytes; SHA-1 byte-identical to upload. |
| 4 | No dropzone path triggered | **CP MET** | `#dropZone` element no longer exists in `Huckleberry_AI_phase2.v1.0.0.html`. Original `#uploadZone` retained as visual UX, but its handler now uploads via `apiClient.createJob({file, ...})` instead of rendering client-only. |
| 5 | No path-string Step 1.5 path triggered | **CP MET** | `#serverPdfPath` element + entire Step 1.5 SERVER FILE PATH card deleted from HTML. Daniel-confirmed visually: "Step 1.5 should be gone. Just Steps 1, 2, 3." |
| 6 | Dispatch ran successfully | **CP MET** | Silverleaf: 40 pages dispatched, `dispatch_complete=1`. Taco Bell: 88 pages dispatched, scope tab auto-populated. Polling pattern (`pollJobStatus` every 3s) replaced the 240s timeout — works on larger bidsets that previously failed. |
| 7 | `project_scope` persisted | **CP MET** | New `job_project_scope` table populated by `persist_project_scope(job_id, ctx)` extending `persist_dispatch_result`. dispatch_gate.py call site at line 1738 SHA-1 unchanged. Live verification: Silverleaf job `db8a5774-…` shows `detected_system=None, confidence=0.0`; Taco Bell job shows `detected_system='tpo', confidence=0.95`. Both correctly mirror what `_resolve_scope_system` produced. |
| 8 | (Taco Bell) Auto scope_systems row pre-populated | **CP MET** | Daniel-pasted scope-card receipt verbatim: `TPO Single Ply / AUTO · seen on PAGE 19, PAGE 20 / evidence: from 2 scope page(s) [18, 19]: spec 07 54 23 → TPO Membrane Roofing; Johns Manville (multi-system); Tremco (multi-system) / HIGH CONF / × REMOVE / [System Type] [Manufacturer] [Attachment] [Membrane Thickness] [Cover Board] [Slope Pitch] [Waste %]`. Confirms: backend persisted, label mapped via `_DISPLAY_NAME_MAP`, evidence JSON shipped, frontend `_flattenScopeRow` + `renderSystemCard` rendered all expected affordances. |
| 9 | (Silverleaf) Manual scope row creates + edits + persists | **CP MET** | Verified earlier in session: Daniel drove `+ ADD SYSTEM` on Silverleaf, row appeared (POST), edited fields (PATCH), removed system (DELETE). Tests tab confirmed `api · scope · POST creates manual roofing system PASS`, `PATCH updates user_fields PASS`, `DELETE removes the row PASS`, `GET filters by trade query param PASS`. |
| 10 | Browser refresh persists scope | **CP MET** | `localStorage.setItem('huck.currentJobId', job.id)` on dispatch success; boot rehydrate reads it back and calls `loadScopeFromApi`. Daniel confirmed earlier: "scope tab still shows the system, sidebar still shows the job ID" after F5. |
| 11 | Sacred floor + vault SHA-1s held | **CP MET** | Backend `pytest` final run: **255 passed, 19 skipped, 0 failed** (242 → +13 net: +9 scope + 7 multipart - 3 retired). Frontend Tests tab: 28/28 (was 23, +5 SCOPE_API_TESTS net after CP3 migration). All 7 vault/integration-frozen SHA-1s identical to Step 0c capture: `roofing_module ae9e5b28…`, `roofing_vocabulary ec6c17f8…`, `glazing_module 52c01442…`, `glazing_vocabulary 64249c8e…`, `debug_module 78f71d90…`, `dispatch_gate 8b39fd0e…`, `pdf_engine daf06dd2…`. |

**Result: 11/11 CP MET. Hard gate PASS.**

---

## 4. Banked observations (out of G.4 scope; tracked for later)

These came out during the recon + execution but aren't G.4 fixes. Surfaced here so future phases inherit them with context.

### 4.1 — `_resolve_scope_system` confidence is binary, not continuous

Reading `dispatch_gate.py:1316-1388`, the function emits exactly these confidence values:

| Evidence found | `system_confidence` |
|---|---|
| Nothing | 0.0 |
| 1 source (manufacturer-only OR thickness marker) | 0.7 |
| 2 sources | 0.85 |
| 3+ sources (capped) | 0.9 → 0.95 |
| Any spec-section hit | bumped to ≥0.9 |

**No values exist in the 0.0–0.7 band.** Daniel's question "should we drop the threshold?" doesn't have a useful answer: lowering `_AUTO_PREPOPULATE_THRESHOLD` from 0.7 to 0.5 would surface zero additional bidsets because the function never returns intermediate values. The 0.0 returns on Silverleaf, Bearss, Shoppes, Vine (per existing `SWEEP_OBSERVATION_*.md` reports) are **real signals** — those bidsets genuinely lack detectable Division 07 / manufacturer / material evidence. The historical `content` vs `text` field-name bug from TracePoint history is already fixed in Huckleberry's port (`dispatch_gate.py:1269` reads `text` first, falls back to `content`).

The real opportunity for raising the auto-detection rate is **widening the evidence sources** in `_resolve_scope_system` (vote on roof-shape signals, slope evidence, manufacturer-product asymmetric matches, etc.) — but that requires editing the integration-frozen `dispatch_gate.py`, so it belongs to a dedicated tuning phase.

### 4.2 — RoofingModule output is fully persisted but never rendered

Recon (this session) traced the full chain from `RoofingModule` definition → instantiation → dispatch call → `ctx.trade_module_outputs` → `persist_trade_outputs` → API `JobResultsResponse.trade_outputs` → frontend `App.currentResults`. **Every hop is connected through to the API. The disconnect is on the rendering layer:** `populatePagesFromResults()` only reads `dispatch_results.page_type` (page classification labels) and ignores `trade_outputs` entirely. The 8 roofing fields populated per page (drains, scuppers, hatches, RTUs, curbs, pipe boots, exhaust fans, _scope) plus equipment_pins plus warnings are all sitting in `App.currentResults` unread.

This matches **baseline items 5+6** (viewer tools save to DB; takeoff reads from database) which were always deferred to G.5/c.2. Not a G.4 regression. The `scope_systems` CRUD pattern shipped in CP1 is the template the future annotation-persistence phase reuses.

Live receipt (5 most recent dispatched jobs at gate close):
- Each job: 38–40 rows in `trade_outputs` for trade=`roofing`, ~76,000 bytes total
- Per-page output: 8 keyed fields populated, equipment_pins included, _scope value computed

### 4.3 — Glazing project-level scope detection deferred

`_resolve_scope_system` and `run_scope_scanner` only resolve roofing systems. Glazing's per-page `glazing_items` / `door_items` / `storefront_items` arrays are populated by `GlazingModule.analyze` per page but never aggregated into a project-level "Storefront-dominant" / "Curtain-wall" / "Window-only" answer. A future sibling file (`backend/core/glazing_scope_detector.py`) reading those aggregated arrays could populate a `trade='glazing'` row in `scope_systems` without editing the vault-locked glazing module. Banked.

### 4.4 — Helper-3 / Helper-5 ceremony skipped

The original G.4 plan called for 6 instrumented helpers (backend watcher, frontend HTTP log, API intercept middleware, DB mutation watcher, browser telemetry wrapper, filesystem watcher) per the G.D2 architecture. Daniel's empirical drives on Silverleaf and Taco Bell substituted for the helper ceremony — every matrix row was either visually confirmed by him or directly readable from existing receipts (uvicorn log, sqlite tables, SHA-1 sums). Helpers 1/2/4/6 (the lightweight log-tee + DB poller + filesystem watcher patterns) remain in the playbook for the next phase that needs heavier verification.

---

## 5. What's NOT in G.4 (explicit, so future phases don't claim coverage)

- **Backend trade-routing in dispatch** — `_run_trade_modules` still runs all modules unconditionally regardless of `jobs.trade_scope`. Trade isolation in dispatch needs `dispatch_gate.py` edit, vault-locked. G.4 ships backend trade filtering at the API layer (`?trade=roofing` query param on `/scope`).
- **Glazing project-level system identification** — see §4.3.
- **Page reclassify UI + endpoint + DB column** — baseline item 4.
- **Viewer tools save to database** — baseline item 5.
- **Takeoff tab reads from database** — baseline item 6.
- **Excel export reads from database** — baseline item 7.
- **Full session resume** (pages tab, viewer state, annotations) — baseline item 8. G.4 ships only the scope-tab piece (currentJobId in localStorage, scope re-fetch on boot).
- **3-bidset compute-heavy hard gate** — already ITINERARY-parked as G.5/Next-2.
- **Stack.CT-style project directory + multi-job UI** — Daniel-locked deferral from G.4 planning conversation.
- **Render optimization (PyMuPDF tiling)** — original Phase G/F1 scope, parked as G.5/Next-1.
- **LLM/VLM "secretary" fallback** for noisy bidsets — Daniel's stated future idea; no design yet.

---

## 6. Vault SHA-1 verification

| File | Pre-phase (Step 0c) | Post-phase (gate close) | Status |
|---|---|---|---|
| `backend/core/roofing_module.py` | `ae9e5b284191b45de419faacf11771da27a548f9` | `ae9e5b284191b45de419faacf11771da27a548f9` | ✅ HELD |
| `backend/core/roofing_vocabulary.py` | `ec6c17f8955ef8e27c3ff1d552b299a6962c9d0b` | `ec6c17f8955ef8e27c3ff1d552b299a6962c9d0b` | ✅ HELD |
| `backend/core/glazing_module.py` | `52c014421915ec6a66b4a6860b71a0a3274920f2` | `52c014421915ec6a66b4a6860b71a0a3274920f2` | ✅ HELD |
| `backend/core/glazing_vocabulary.py` | `64249c8ef5f7d9db50added3c9a40836cba356ea` | `64249c8ef5f7d9db50added3c9a40836cba356ea` | ✅ HELD |
| `backend/core/debug_module.py` | `78f71d9030cde3b173389603f5f39bd6bedaac07` | `78f71d9030cde3b173389603f5f39bd6bedaac07` | ✅ HELD |
| `backend/core/dispatch_gate.py` (integration-frozen) | `8b39fd0eb4fa6e5a3a61f8da7f9a095be7bd091a` | `8b39fd0eb4fa6e5a3a61f8da7f9a095be7bd091a` | ✅ HELD |
| `backend/core/pdf_engine.py` (integration-frozen) | `daf06dd266d52983a0c761669f8af1ed825088a7` | `daf06dd266d52983a0c761669f8af1ed825088a7` | ✅ HELD |

All 5 vault-ruled trade modules + 2 integration-frozen reference files unchanged. Vault rule honoured.

---

## 7. Sacred floor verification

| Stage | Backend | Frontend |
|---|---|---|
| Pre-phase (Step 0b) | 242 passed, 19 skipped, 0 failed | 23/23 |
| Post-CP1 (8f1de64) | 251 passed, 19 skipped, 0 failed (+9 scope) | 28 (+5) |
| Post-CP2 (9b7b989) | 258 passed, 19 skipped, 0 failed (+7 multipart) | 28 |
| Post-CP3 (845327e) | 255 passed, 19 skipped, 0 failed (-3 retired JSON-path) | 28 (5 migrated) |
| Post-CP4 (a1d8ded) | 255 passed, 19 skipped, 0 failed (no test changes) | 28 |
| **Post-canon (this report)** | **255 passed, 19 skipped, 0 failed** | **28** |

Backend +13 net tests; frontend +5 net tests. No regressions at any boundary.

---

## 8. Receipts index

- **Plan file:** `~/.claude/plans/a-but-i-want-valiant-moler.md` (the formalize-ship plan)
- **Original march orders:** `MARCH_ORDERS_phase_G_4_scope_fix_and_backend_storage.md` (workspace untracked)
- **Predecessor inventory:** `backend/G_D2_INVENTORY_REPORT.md`
- **Predecessor diagnostic:** `backend/G_D_DIAGNOSTIC_REPORT.md`
- **Code commits:** `8f1de64`, `6e4fb8f`, `25481f7`, `9b7b989`, `845327e`, `a1d8ded` (+ canon commit at end of formalize-ship)
- **Live verification screenshots:** in conversation transcript (Taco Bell scope card, Silverleaf manual-entry flow, Tests tab 28/28)

---

**End of Phase G.4 hard gate report.** Daniel reviews this, the canon updates ship in a single commit, branch pushes to origin.
