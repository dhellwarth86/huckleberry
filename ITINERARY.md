# ITINERARY.md — Huckleberry Working Memory

**Purpose:** Compressed working memory. The 120-150 line doc that catches a fresh Claude up without reading every gate report. Mutates each handoff. If this file is current, the project state is recoverable in under 5 minutes.

**Update discipline:** Every session that ships work updates this file. The General updates it after ratifying / debriefing. The Developer updates it after a hands-on ship. Canon updates are produced by Claude in chat as complete drop-in files at sign-out — Daniel does not paste snippets.

---

## Section 1 — Last 3 Completed

Most recent ships, 7 lines each. Each entry: phase name, date, branch, what shipped, sacred floor delta, receipt path, key learning.

### Last-1 — Phase G.5b (PyMuPDF tile rendering API + surgical theater cut + pipeline-wide theater audit) — 2026-05-09

- **Branch:** `phase2-v0.3-G5b-render-tile-and-filter4` HEAD `<canon commit pending>`; 2 code commits + canon when this lands; awaiting push approval
- **Shipped:** PyMuPDF tile rendering API in `pdf_engine.py` (CP1: `render_page_tiled()` + `_estimate_render_memory_mb()` + `_compute_tile_rects()` + 4 module constants — plumbing for G.6 Stage 6 contour detection on ARCH-D pages at 250 DPI, 50 MB threshold, 5% overlap, 2x2 grid per G.0 scout math); surgical theater cut of `detect_firm`/`architect_profile` dispatch invocation in `dispatch_gate.py:1711-1718` (no downstream consumer; `ctx.architect_profile` field declaration in `context.py` stays defined as None; `core/architect_profile.py` itself unchanged + unit-tested in `test_architect_profile.py`; ~20-50ms saved per dispatch when storage is active). **CP2 (Filter 4 tile consumer) RETIRED** during fact-find when scout work confirmed `pdfplumber.extract_tables()` is vector-bound algorithmic work (PDF text stream + grid-line detection in vector space), NOT rasterization-bound — tiling does not help; substituting tiles via `pdfplumber.Page.crop()` would be slower per-page and risk losing tables that span tile boundaries. **Pipeline-wide theater audit** shipped as the real deliverable (3 parallel Explore agents): pandas/OCR claim about TracePoint resolved FALSE (zero hits across `tracepoint_port/`); pipeline order verified correct (TracePoint and Huckleberry both run F1→F2→F4→F3→F5→scope_scanner→metadata→Stage 13→persist; Filter 4 before Filter 3 is intentional for keynote detection); 10-item theater inventory with cascade analysis (#1 `_extract_project_metadata` BANKED — has skipped-test cascade; #2 `detect_firm` CUT this CP; #3-#10 either banked, "wire don't cut", or "don't cut — load-bearing for in-flight phases"). Algorithmic Filter 4 replacement parked as Phase 10 (post-hard-gate, Daniel directive 2026-05-09: Taco Bell Weeki Wachee currently <400s, no current pain).
- **Floor delta:** Backend 273 → 278/19/0 (+5 net: tile API tests). Frontend 28/28 held (backend-only changes, no frontend impact, no live dispatch needed for soft gate). **Vault re-locked at NEW SHA-1s for 2 integration-frozen files:** `pdf_engine eb5b8372f6f0c52de5a81b452399035c2b720551`, `dispatch_gate 71e409a27caf78525d663fa6ca11d0e7a0c9b7ca`. HELD: 4 trade-knowledge files at G.5a baseline (`roofing_module 9a6085d4…`, `roofing_vocabulary 863ffb01…`, `glazing_module 1b449e97…`, `glazing_vocabulary 008ed191…`); `debug_module 78f71d90…`.
- **Receipts:** `backend/G_5b_GATE_REPORT.md` · commits `36017fb` (CP1) → canon · soft gate 5/5 CP MET · pipeline theater audit preserved in session transcript (3 Explore agent reports)
- **Learning:** The original CP2 plan ("Filter 4 tile consumer") presupposed Filter 4 had an "image-extraction path" that could be replaced with tile rendering — fact-find showed Filter 4 has zero rendering operations of any kind. The G.0 scout report had connected two independent findings ("pdfplumber.extract_tables() is the cost ceiling" + "PyMuPDF tiling is ready") that don't actually intersect. Tiling helps **rasterization-bound** work; Filter 4 is **vector-bound**. Karpathy procedure step 5 (§7 stop on uncertainty) fired correctly; pipeline-wide audit (not narrow patch-and-pray) produced the right next-phase shape.
- **Lesson banked:** (a) Vault SHA-1 canonical method is `sha1sum` of raw file content on disk (CRLF preserved on Windows), NOT `git hash-object` (which normalizes to LF). (b) Pandas/OCR claim about TracePoint resolved FALSE via grep — memory was conflating pdfplumber vector table extraction with image-based extraction; future planning must grep-verify before trusting "TracePoint did X." (c) Pipeline-wide theater audit produces more value than narrow per-CP fact-finds when a fundamental mismatch surfaces. (d) Theater cuts must include test cascade analysis — `_extract_project_metadata` was banked (not shipped) because a SKIPPED test asserts on its side effect; cutting the implementation while keeping the test silently turns SKIPPED into future-fail.

### Last-2 — Phase G.5a (annotation persistence + TradeModule Protocol vocabulary unfreeze) — 2026-05-08

- **Branch:** `phase2-v0.3-G5a-annotation-persistence` HEAD `364e6d0` + canon commit pending; 7 commits when canon lands; awaiting push approval
- **Shipped:** Annotation persistence end-to-end (baseline items 5+6 → MET; item 8 → MET). New `annotations` SQLite table (type discriminator + JSON `data_json` blob); 5 CRUD endpoints under `/jobs/{id}/annotations` (CP1); viewer tools (line/pin/polygon) rewired to API relay via optimistic-push + async POST + refetch (CP2); `Viewer.rebuildOverlayFromState()`; cascade-delete on `scope_systems` removal; takeoff page-number labels per row (CP3); auto-pin extractor `_extract_auto_pins_from_trade_output` wired (currently idle — produces 0 rows until Stages 6-9 ship). **Mid-phase architectural correction (CP4):** TradeModule Protocol extended with 3 vocabulary classmethods (`get_palette_seed`/`get_expected_items`/`get_systems_catalog`); per-trade vocabulary stays inside trade modules; `_resolve_trade_module(trade)` does lazy LOCAL imports inside `job_storage.py`; grep-assertion test `test_no_per_trade_imports_in_job_storage` enforces no `roofing_*`/`glazing_*` imports leak across the module boundary. `_seed_palette_via_protocol(sys_id, trade, system_code)` wired into `_pre_populate_auto_scope_systems` + `create_scope_system`. EXPECTS checklist + line tool draft fix shipped same CP. **Vault unfreeze ceremony:** 4 trade-knowledge files unfrozen (`roofing_module.py`, `roofing_vocabulary.py`, `glazing_module.py`, `glazing_vocabulary.py`) per Daniel's contract ("1 then test if we have to change anything when test clears this gate vault rule goes back into effect"); re-locked at NEW SHA-1 baseline at gate close. CP4.1: routing dispatch by `unit` (was `derive_from`) + cricket added to typical_items for tpo/pvc/epdm/modified_bitumen/built_up + Equipment Curbs EA→SF (Daniel-surfaced: "crickets are a polygon tool that doesnt show up in auto or manual" + "equipment curbs should be a sqft too not a count"). CP4.2: viewer DELETE race-condition fix — pre-refetch + local-id fallback for optimistic-pushed entries that lack `_annId` until POST completes ~100-300ms (Daniel-surfaced: "would have to keep hitting delete in viewer window until item gets deleted").
- **Floor delta:** Backend 255 → 273/19/0 (+18 net: annotations CRUD/cascade/auto-pin extractor + Protocol classmethods + auto-seed wiring + cricket polygon + equipment curbs SF + grep-assert no per-trade imports). Frontend 28/28 held (viewer rewire validated by Daniel-driven empirical run, not new automated tests). **Vault re-locked at NEW SHA-1s for 4 trade files:** `roofing_module 9a6085d4a3fbe7bbafa4b920c75868261f3c3a60`, `roofing_vocabulary 863ffb01de05ed8a55b1975268c3ff3a9c1d4252`, `glazing_module 1b449e9716ef2fe83ee0f2546ad2281deef5ac55`, `glazing_vocabulary 008ed1914422e7f63a8fe90833bcda9e0cb3b44a`. UNCHANGED: `debug_module 78f71d90…`, `dispatch_gate 8b39fd0e…`, `pdf_engine daf06dd2…`.
- **Receipts:** `backend/G_5a_GATE_REPORT.md` · commits `dd65940` (CP1) → `cebb58b` (CP2) → `19783ca` (CP3) → `e6a2ef5` (CP4) → `d8def62` (CP4.1) → `364e6d0` (CP4.2) · soft gate 12/12 CP MET via Daniel-driven empirical run on Taco Bell across CP4.1+CP4.2 iterations; final receipt verbatim "all clean good to go".
- **Learning:** The chat-Claude draft of CP4 would have imported `roofing_vocabulary.SYSTEMS/ITEMS` from `core/job_storage.py`. Daniel forbade mid-CP ("hardcoding roofing verbiage and systems outside of module is forbidden") and authorized vault unfreeze ("roofing module unlock vault is my command to make"). Plan rewritten to the architecturally-correct TradeModule Protocol vocabulary methods. **The architectural rule extends G.4's:** *trade-specific knowledge — item names, system types, expected items, units, vocabulary — lives INSIDE the trade module; `core/job_storage.py` and `api/` are trade-agnostic; they call Protocol methods, never import per-trade constants.* New trades implement the Protocol; everything else works without code changes. Enforced at the test floor.
- **Lesson banked:** (a) Vault unfreeze ceremony works the same as G.3's `dispatch_gate.py`/`pdf_engine.py` precedent — pre-capture SHA-1s → unfreeze → soft-gate → re-capture → re-lock at new baseline. The contract is load-bearing: "when test clears this gate vault rule goes back into effect." (b) Frontend optimistic-push patterns have a real 100-300ms race window. Destructive operations must pre-refetch OR carry a local-id fallback. When a future phase adds annotation editing UI, audit all mutation paths. (c) Auto-pin TYPES (palette seeding from vocabulary — no geometry needed) ship distinct from auto-pin INSTANCES (drain/scupper rows from PDF callouts — wait on Stages 6-9 wiring). The extractor is wired and idle; once Stages 6-9 land, rows start appearing immediately.

### Last-3 — Phase G.4 (scope tab as backend-DB-frontend cycle + backend file storage + dropzone retire) — 2026-05-07

- **Branch:** `phase2-v0.3-G4-scope-fix-and-backend-storage` HEAD `a1d8ded`, canon commit shipped, push status TBD per G.4 handoff
- **Shipped:** Scope tab as full backend-DB-frontend cycle (CP1 + CP1.1 polish + CP1.2 flatten bridge), backend file upload + storage + GET /pdf endpoint (CP2), single upload point with JSON path-string + client-only dropzone render path both retired (CP3), PROJECT_CLAUDE.md cleanup with 4 edits including new misconception entry on `ctx.project_scope` as canonical scope source (CP4). Two new SQLite tables: `job_project_scope`, `scope_systems`. Six new endpoints under `/jobs/{id}/scope/*` + multipart `POST /jobs/upload` + `GET /jobs/{id}/pdf`. Frontend rewired for render+relay with localStorage rehydrate of `currentJobId` for refresh-survival of scope state. Baseline items 1/2/3 moved from NOT MET to MET.
- **Floor delta:** Backend 242 → 255/19/0 (+13 net: +9 G.4 scope + 7 multipart − 3 retired JSON-path); frontend 23 → 28 (+5 SCOPE_API_TESTS net after CP3 migration). Vault SHA-1s held identical to Step 0c capture across all 7 vault/integration-frozen files.
- **Receipts:** `backend/G_4_GATE_REPORT.md` · commits `8f1de64` → `a1d8ded` · empirical hard gate 11/11 CP MET via Daniel-driven Silverleaf (manual-entry path; `system_confidence=0.0`) + Taco Bell (auto-detect path; `tpo @ 0.95`)
- **Learning:** The original chat-Claude G.4 march orders prescribed a frontend-only literal fix that surfaced per-page `_scope` noise. Daniel rejected mid-execution and locked the architectural rule that drives everything since: **frontend = window only, backend = source of truth, every user edit is a database mutation, refresh-the-browser rehydrates everything from the database, "migrate later" is the failure mode.** Plan rewritten before any code shipped. (G.5a CP4 extended this rule to per-trade vocabulary boundaries — see Last-1.)
- **Lesson banked:** `_resolve_scope_system` confidence is binary, not continuous — emits 0.0 or 0.7+. RoofingModule output is fully persisted + shipped via API; G.5a CP2 reused the `scope_systems` CRUD pattern verbatim for the new `annotations` table.

---

## Section 2 — Next 6 Pipeline Steps

Each entry: phase name, dependency, scope summary, sacred-floor target, soft/hard gate, key risk, who-runs-it.

### Next-1 — G.6 Stages 6-9 geometry/scale/callout extraction wiring

After G.5b ships, G.6 is unambiguously next. Wires the deferred Stages 6-9 (deferred D.1 → "D.2/E", never picked back up; G.5b confirmed pipeline order is correct + Stages 6-9 ports already exist in `geometry_matrix.py` / `pdf_engine.py` / `trade_input_builder.py` waiting for the dispatch call site to invoke them).

- **Scope:** Replace `_build_dispatch_only_input()` in `dispatch_gate.py:1487-1529` with a new `_run_stages_6_9(ctx, page_idx, doc, page)` helper that runs contour detection (Stage 6, consuming G.5b's `render_page_tiled` for ARCH-D pages at 250 DPI), scale resolution (Stage 7, already-ported `find_roof_plan_scale`), area/perimeter/bbox computation (Stage 8, already-ported `geometry_matrix`), then call `build_trade_input(geometry_result, ...)` (already supports populated `geometry_result` per `trade_input_builder.py:71-165`). Stage 9 (callout extraction inside polygon bbox + 30% margin) already lives in `build_trade_input:105-128`. Once landed: RoofingModule's `equipment_pins` and `fields[name].value` populate from PDF callouts; the G.5a CP1 auto-pin extractor (currently idle) starts producing annotation rows immediately; auto-detected pin INSTANCES appear in the viewer overlay + takeoff with PAGE labels.
- **Floor target:** backend ≥278 + ~5 new geometry/wiring tests
- **Vault:** likely unfreeze `dispatch_gate.py` (G.5b's new SHA-1 baseline) only; trade modules expected to stay locked; `trade_input_builder.py` and `geometry_matrix.py` are not vault-ruled
- **Soft gate:** Daniel-driven Taco Bell live verification — auto-pins (drains/scuppers/RTUs/hatches/etc.) appear on roof-plan pages 18/19 with dotted-ring + 🤖 prefix; takeoff rows populated; manual pins coexist; DELETE works first-click
- **Risk:** Stage 6 contour detection on synthetic data may not match real bidset behavior; Daniel-driven empirical verification is the gate
- **Run:** Developer; same Karpathy single-bidset discipline as G.4/G.5a/G.5b

**Also queued (lower priority):** Phase C.3c follow-on — real glazing palette implementation replacing G.5a skeletal stubs. Independent of G.6.

### Next-2 — Closing hard gate (3-bidset + deferred E.2.2 visual)

- **Depends on:** G.6 shipped
- **Scope:** Bundles two deferred hard gates. (1) 3-bidset hard gate (Bearss + Silverleaf + Vine Street) re-run end-to-end against the full Phase F/G chain. (2) Deferred E.2.2 visual hard gate that was rolled into E.2.2 but not exercised on multiple bidsets. Closes Phase F/G chain permanently.
- **Floor target:** All previous floors held + hard gate report PASS
- **Gate:** **Hard gate** — completes the entire Phase F/G chain
- **Risk:** Single-bidset Silverleaf/Taco Bell testing throughout the chain may have masked bidset-specific quirks.
- **Run:** Developer session with Daniel manually verifying browser; General writes gate report

### Next-3 — Silverleaf Filter 1 sheet-detection fix

- **Depends on:** G.2 shipped (G.2 confirmed the classifier lever works; Silverleaf 12/13/38/39 need Filter 1 to detect their sheet numbers first)
- **Scope:** Fix `_find_sheet_on_page` for pages where sheet numbers exist in page text but current strategies (3-5) miss them. Silverleaf pages 12/13/38/39 have sheet numbers (P201, P301, M101, M102) in full text but empty title-block quadrants. Once Filter 1 populates `sheet_number`, existing MEP fallback + new classifier keywords catch them.
- **Floor target:** Backend ≥242 + new tests for sheet detection edge cases
- **Gate:** Soft gate — Silverleaf UNKNOWN count drops from 4 to 0
- **Risk:** Broadening sheet-number detection may false-positive on pages where number-like strings appear in non-title contexts.
- **Run:** General scopes and drafts march orders after G.5 ships

### Next-4 — Phase G auto-notation product (post-optimization)

- **Depends on:** All G.3-G.5 performance work + closing hard gate
- **Scope:** Three-state annotations + provenance + training loop. The user-facing product phase that builds on the dispatch infrastructure.
- **Floor target:** TBD at design time
- **Gate:** TBD
- **Risk:** This is the product phase — architecture risk is bounded by the preceding infrastructure chain.
- **Run:** General designs; Developer builds

### Next-5 — Phase 10 — algorithmic Filter 4 replacement (parked Daniel 2026-05-09)

- **Depends on:** closing hard gate (3-bidset) shipped
- **Scope:** Replace `pdfplumber.extract_tables()` (vector-bound 2.91s/page on Bearss p15 per G.0 scout) with a faster algorithm. Candidates: PyMuPDF `Page.find_tables()` (native to current `PyMuPDF>=1.24.0` dep, added in 1.23+), custom vector-direct grid finder, or hybrid (PyMuPDF fast path + pdfplumber fallback when quality check fails). Requires parity gate (legends + raw_tables shape match across libraries) and bidset-wide wall-clock measurement on Bearss/Silverleaf/Vine.
- **Floor target:** TBD at scout-phase entry
- **Gate:** Soft gate (algorithmic + measurement); likely 2-3 sub-phases (scout-and-measure → design pick → ship) per cascade-discipline mandate
- **Risk:** PyMuPDF `find_tables()` may not match pdfplumber's quality on dense schedule pages; parity gate may force hybrid; algorithm switch likely vault-unfreeze on `dispatch_gate.py`
- **Run:** Developer + Daniel-driven measurement gate
- **Why parked:** Daniel directive 2026-05-09 — Taco Bell Weeki Wachee currently dispatches in <400s; algorithmic compute cost is not a current user pain point. Phase 10 returns after gate 9 closes the F/G chain.

### Next-6 — TBD pending Phase G/post-hard-gate design

---

## Section 3 — Schedule Pusher / Blocker Tracking

What's blocking what. What's parked. What needs Daniel decision before it can move.

### Active blockers — none

### Baseline status (from PROJECT_CLAUDE.md "Architectural truth" section)

- **Item 1 (single upload point — backend stores file):** **MET** — G.4 CP2/CP3. Multipart `POST /jobs/upload` writes to `~/.tracepoint/uploads/{job_id}/source.pdf`; JSON path-string variant retired.
- **Item 2 (dispatch fires on backend-stored copy):** **MET** — side effect of item 1.
- **Item 3 (scope tab populates + system pick + retry):** **MET** — G.4 CP1. `scope_systems` table + 5 CRUD endpoints + frontend render+relay; auto-populated when `system_confidence ≥ 0.7`, manual-entry fallback otherwise; PATCH-on-blur edits; refresh-survival via localStorage rehydrate of `currentJobId`.
- **Item 4 (page reclassify writes to DB):** parked.
- **Item 5 (viewer tools save to DB):** **MET** — G.5a CP1+CP2. New `annotations` SQLite table + 5 CRUD endpoints under `/jobs/{id}/annotations`; viewer tools (line/pin/polygon) rewired to API relay (optimistic-push + async POST + refetch); cascade-delete on `scope_systems` removal. Auto-pin extractor wired and idle (waits on Stages 6-9 for INSTANCES — see banked observations).
- **Item 6 (takeoff reads from DB):** **MET** — G.5a CP3. Takeoff reads `App.currentResults.annotations` + `scope_systems` (rehydrated through `loadAnnotationsFromApi`) instead of in-memory state; page-number labels per row.
- **Item 7 (Excel export reads from DB):** parked. Annotations are now in the DB but Excel still client-side.
- **Item 8 (browser refresh persists everything):** **MET** — G.5a CP2. `loadAnnotationsFromApi` runs at boot alongside `loadScopeFromApi`; `Viewer.rebuildOverlayFromState()` rebuilds overlays from API state. Was PARTIAL after G.4 (scope-only); now full.

### Parked items (deliberately deferred)

- **Login screen** — security cluster (post-user-testing)
- **Postgres migration** — security cluster (Phase H)
- **CORS lockdown** — security cluster
- **OpenAPI docs hidden in production** — security cluster
- **Auth (USERS table + JWT)** — security cluster
- **3-bidset hard gates** — Phase G.5 / Next-4
- **Sweep + multi-bidset compute-heavy testing** — Phase G.5 / Next-4
- **Build step / module split for frontend** — deferred, matches POC architecture; revisit when Phase G (auto-notation) demands it
- **Local LLM scope parsing** — much later, read-only enhancement on top of rule-based parser
- **Phase C.4 (cross-trade relationships)** — available, deferred until tuning data justifies
- **Wiki / Project Memory Vault** — much later
- **Color palette work for crickets / brand identification** — deferred
- **Glazing as separate trade module path forward** — deferred
- **`sheet_map_source` shift on Silverleaf (drawing_index → title_blocks)** — fall-out of G.1 patch; banked for future visit
- **19 SKIPPED tests in `test_dispatch.py`** — fixtures look for specific extracted slice PDFs; not a current-phase blocker
- **`ctx.trade_contexts["debug"]` field** — surfaced during recon; banked observation for future trade module work
- **Silverleaf pages 12/13/38/39** — Filter 1 sheet-detection gap (see Next-5); classifier upgrade cannot reach them because `pc.title=""` and `sheet_number=None`

### Awaiting Daniel decision

- G.5b shipped soft gate. Next is **G.6 (Stages 6-9 geometry wiring — unlocks auto-pin INSTANCES)** unambiguously per the post-G.5b plan. Phase C.3c follow-on (real glazing palette) and Phase 10 (algorithmic Filter 4 replacement, parked) remain queued at lower priority. Branch push approval pending.

### Discipline reminders standing

- New sessions ALWAYS announce role at start (General or Developer)
- New sessions ALWAYS read PROJECT_CLAUDE.md + PROJECT_ETIQUETTE.md + ITINERARY.md + 3 most recent CHECKLIST handoffs
- Vault rule: 5 trade modules (roofing_module, roofing_vocabulary, glazing_module, glazing_vocabulary, debug_module) — SHA-1 verified at session boundaries. `dispatch_gate.py` and `pdf_engine.py` are *integration-frozen* but allowed to change in dedicated phases via the unfreeze ceremony (G.1, G.2, G.3 were such phases for `dispatch_gate.py`; G.3 + G.5b for `pdf_engine.py`; G.5a for the 4 trade-knowledge files; G.5b again for `dispatch_gate.py`). **Vault SHA-1 baseline (post-G.5b re-lock 2026-05-09):** `roofing_module 9a6085d4…`, `roofing_vocabulary 863ffb01…`, `glazing_module 1b449e97…`, `glazing_vocabulary 008ed191…`, `debug_module 78f71d90…`, `dispatch_gate 71e409a2…`, `pdf_engine eb5b8372…`. **CANONICAL HASH METHOD: `sha1sum` of raw file content on disk (CRLF preserved on Windows), NOT `git hash-object`.**
- Backend sacred floor: 278 passed / 19 skipped / 0 failed
- Frontend sacred floor: 28/28 against `Huckleberry_AI_phase2.v1.0.0.html` (v6.3.5 retired and archived to safe_for_removal at E.2.1)
- Soft gate between every G sub-phase — Daniel reviews before next phase drafts
- Single-bidset Silverleaf only until Phase G.5 ships (3-bidset hard gate is Next-4)
- No CLAUDE.md (retired by Daniel directive 2026-04-29)
- **Mandate 2026-05-01 (cascade discipline):** When a proposed fix depends on cascade behavior, the first scout traces the cascade — not the bug, not the theory, not the corpus. "If A causes B, find the line where A causes B. If you can't find that line, the cascade doesn't exist."
- **Mandate 2026-05-01 (no artifacts without permission):** Claude does not produce downloadable files without explicit Daniel direction. Inline edits to canon files when shipped through normal sign-out flow are produced as complete drop-in files per the chat-handles-canon protocol.
- **Mandate 2026-05-03 (canon protocol):** Claude in chat produces complete updated CHECKLIST.md, ITINERARY.md, PROJECT_CLAUDE.md as deliverable files at sign-out. Daniel does not paste snippets, does not merge text, does not maintain canon.
- **Mandate 2026-05-03 (lane discipline):** When work crosses lanes mid-session, the active role flags it and asks for explicit role switch before proceeding.
- **Mandate 2026-05-03 (keyword verification):** Corpus scout text samples are inferred, not verbatim. Always verify keyword presence via `engine.extract_text()` on actual PDFs before committing keywords to `_PAGE_TYPE_RULES`.
- **Mandate 2026-05-07 (architectural-rule check on every CP draft):** Daniel's rule "frontend = window only, backend = source of truth, every user edit is a database mutation, refresh-the-browser rehydrates everything from the database, no migrate-later" caught chat-Claude's original G.4 march orders' drift mid-execution. Future planning conversations run new orders through this rule before approval. If a draft puts state on the frontend that the backend could own, the draft is wrong.
- **Mandate 2026-05-07 (`_resolve_scope_system` confidence is binary):** The function emits 0.0 or 0.7+, never values in 0.0–0.7. Lowering `_AUTO_PREPOPULATE_THRESHOLD` is not a useful knob — the real lever is widening evidence sources (vault-locked, future tuning phase). Don't waste cycles on threshold tweaking; the manual-entry fallback IS the spec'd path for bidsets without detectable Division 07 evidence.
- **Mandate 2026-05-08 (TradeModule Protocol vocabulary boundary):** Trade-specific knowledge — item names, system types, expected items, units, vocabulary, palette colors — lives INSIDE the trade module. `core/job_storage.py` and `api/` are trade-agnostic; they call Protocol methods (`get_palette_seed` / `get_expected_items` / `get_systems_catalog`), never import per-trade constants. New trades implement the Protocol; everything else works without code changes. Enforced at the test floor by `test_no_per_trade_imports_in_job_storage`. Lazy LOCAL imports inside `_resolve_trade_module(trade)` are the only path; top-level imports of `roofing_*` or `glazing_*` are forbidden in `job_storage.py`.
- **Mandate 2026-05-08 (vault unfreeze ceremony):** When trade-knowledge or integration-frozen files need to change, the ceremony is: (1) pre-capture SHA-1s; (2) Daniel explicitly authorizes unfreeze for the phase; (3) work + tests + soft gate; (4) re-capture SHA-1s; (5) vault rule re-engages at NEW SHA-1 baseline; (6) PROJECT_CLAUDE.md §4 + ITINERARY.md updated. Daniel's contract: "when test clears this gate vault rule goes back into effect." Same protocol used for G.1/G.2/G.3 (`dispatch_gate.py`), G.3 (`pdf_engine.py`), G.5a (4 trade-knowledge files).
- **Mandate 2026-05-08 (optimistic-push race window):** Frontend optimistic-push patterns have a real 100-300ms window where entries exist on the overlay before the POST returns and assigns the server ID (`_annId === undefined`). Destructive operations (DELETE, etc.) must pre-refetch annotations OR carry a local-id fallback. When future phases add annotation editing UI, audit all mutation paths — the recipe is the same.
- **Mandate 2026-05-09 (vault SHA-1 canonical method):** Vault SHA-1s are computed via `sha1sum` of the raw file content on disk (CRLF preserved on Windows), NOT `git hash-object` (which normalizes line endings to LF and produces different values). When verifying vault SHA-1s, use `sha1sum backend/core/{file}.py` (or Python `hashlib.sha1(open(f,'rb').read()).hexdigest()`). The canonical SHA-1s in PROJECT_CLAUDE.md §4 + ITINERARY.md were computed this way; any vault audit using `git hash-object` will return mismatched values that look like regressions but aren't.
- **Mandate 2026-05-09 (independent-findings audit):** When a scout report connects two findings ("X is the cost ceiling" + "Y is ready to deploy") into a recommendation ("use Y to fix X"), explicitly state whether the bridge is verified or assumed. The G.0 scout's "tile pdfplumber to win wall-clock" was a false bridge — pdfplumber is vector-bound, tiling helps rasterization-bound work; they don't intersect. Future scouts: name the unverified assumption, or run the empirical verification before recommending.
- **Mandate 2026-05-09 (theater cuts require test cascade analysis):** Before cutting code identified as theater, grep for tests that assert on its behavior — even SKIPPED tests (which don't run today but document the spec). A cut that silently turns a SKIPPED test into a future-fail is dishonest. Either retire the test alongside the implementation in the same commit, OR bank the cut and ship only cuts with zero test cascade. Example: G.5b cut `detect_firm` invocation (zero test cascade) but BANKED `_extract_project_metadata` cut (SKIPPED test asserts on its side effect).
- **Mandate 2026-05-09 (pipeline-wide audit beats narrow patches):** When a per-CP fact-find surfaces a fundamental mismatch between plan and reality (G.5b CP2: tiling can't help vector-bound work), expand to a pipeline-wide audit (3 parallel Explore agents) before re-planning. Cheaper than a wrong patch. The G.5b audit produced a 10-item theater inventory with cascade analysis that rewrote the next 2 phases' shape (G.6 = real wins, Phase 10 = parked). Future phases: when ambiguity surfaces, audit the system not the symptom.
