# CHECKLIST.md — Huckleberry Project Audit Trail

**Purpose:** Signed checklist of every phase / sub-phase / patch shipped on Huckleberry. Future Claude reading this knows what's done, who shipped it, when, and how it was verified. If something breaks, this is where investigation starts.

**Discipline:** Every row signed by the role that shipped the work, dated, with validation method and evidence link. No exceptions. Unsigned rows = unverified.

**Format per row:**
- **What** — short description of the work shipped
- **Who** — which role signed off (General / Developer)
- **Date** — YYYY-MM-DD
- **Validation** — pytest count / SHA-1 match / git log / file inspection / manual smoke / hard gate report
- **Evidence** — receipt path (gate report, commit SHA, etc.)

---

## Phase A — TracePoint Pipeline Port

| # | What | Who | Date | Validation | Evidence |
|---|---|---|---|---|---|
| A1 | Phase B — TracePoint pipeline ported (Stages 1-12, dispatch, filters, geometry, scoring, architect-profile flywheel, storage layer, correction store) | (historical) | 2026-04-XX | pytest + SHA-1 verbatim port | (canon) |
| A2 | Phase C.1 — trade module Protocol contract | (historical) | 2026-04-XX | pytest | (canon) |
| A3 | Phase C.2 — Roofing module verbatim port | (historical) | 2026-04-XX | SHA-1 + pytest | (canon) |
| A4 | Phase C.3a/b — Glazing seed validation + vocabulary | (historical) | 2026-04-XX | pytest | (canon) |
| A5 | Phase C.3c-build — Glazing module shipped | (historical) | 2026-04-28 | pytest + smoke | commit `c656ec6` |
| A6 | Phase C.5 — Debug module ported (sections 1/3/6 working) | (historical) | 2026-04-28 | smoke + bidset run-through | commit `9025884` |

## Phase B — Real Bidset Validation

| # | What | Who | Date | Validation | Evidence |
|---|---|---|---|---|---|
| B1 | Three-bidset sweep (Shoppes / Vine / Bearss) | (historical) | 2026-04-28 | descriptive observation reports | `backend/SWEEP_OBSERVATION_*.md` |
| B2 | Profile diagnostic + page-type verification | (historical) | 2026-04-29 | hypothesis verification | (canon) |
| B3 | Calibration session on Silverleaf (Bug 1 + Bug 3 fixed) | (historical) | 2026-04-29 | hard gate | `backend/CALIBRATION_GATE_REPORT_silverleaf.md` |

## Phase C — Backend Infrastructure

| # | What | Who | Date | Validation | Evidence |
|---|---|---|---|---|---|
| C1 | Phase D.1 — storage activation + RoofingModule + GlazingModule wired into run_dispatch | (historical) | 2026-04-29 | Silverleaf hard gate 7/7 PASS | `backend/D_HARD_GATE_silverleaf.md` |
| C2 | Housekeeping — 53 files moved to safe_for_removal | (historical) | 2026-04-29 | manifest | `safe_for_removal/MANIFEST.md` |
| C3 | Phase D.2 — job persistence layer + 3-bidset hard gate (21/21 PASS) | (historical) | 2026-04-29 | hard gate | `backend/D2_MASTER_GATE_REPORT.md` |

## Phase D — API Surface

| # | What | Who | Date | Validation | Evidence |
|---|---|---|---|---|---|
| D1 | Phase E.0 — frontend audit + API design + v6.3.x housekeeping | (historical) | 2026-04-30 | gate report | `backend/E0_GATE_REPORT.md` |
| D2 | Phase E.1 — FastAPI scaffold + 2 endpoints + 6 new tests | (historical) | 2026-04-30 | hard gate 8/8 PASS | `backend/E1_HARD_GATE_silverleaf_api.md` |
| D3 | E.1 discipline patches (uvicorn smoke + corrigenda) | (historical) | 2026-04-30 | smoke 4/4 PASS | `backend/E1_UVICORN_SMOKE.md` |
| D4 | Phase E.2.0 — strip plan + new file design + API client spec + test floor proposal | (historical) | 2026-04-30 | gate report 10/10 PASS | `backend/E2_0_GATE_REPORT.md` |

## Phase E — Frontend Strip + Connect

| # | What | Who | Date | Validation | Evidence |
|---|---|---|---|---|---|
| E1 | Phase E.2.1 — frontend strip + new file (Huckleberry_AI_phase2.v1.0.0.html) + v6.3.5 archival (frontend floor 138 → 20) | General | 2026-04-30 | sacred floor delta verified | commit `4f7c90f` |
| E2 | Phase E.2.2 — frontend connect + 2 new API endpoints + Silverleaf upload-to-display hard gate (backend 222 → 230, frontend 20 → 23) | General | 2026-04-30 | end-to-end Silverleaf hard gate PASS | commit `0ddd5a5` |
| E3 | (folded into E2 — Phase E.2.2 absorbed bug shake-out as part of hard gate) | — | — | — | — |
| E4 | (folded into E2 — Phase E.2.2 included the Silverleaf upload-to-display hard gate) | — | — | — | — |

## Phase F — Pre-Multi-Bidset Optimization (Phase G chain — restructured 2026-05-01)

Original scope (single phase: render optimization via PyMuPDF tiling) was restructured across multiple sub-phases after G.0 scout chain surfaced a sequence of upstream bugs and architectural debt that block render optimization from being meaningful.

| # | What | Who | Date | Validation | Evidence |
|---|---|---|---|---|---|
| F1 | Phase G.0 — scout mission: render path inventory + dep audit + tiling math + Silverleaf root-cause + Bearss baseline + module structure proposal + 10 design questions | General | 2026-05-01 | Read-only; sacred floors held; backend 230/19/0; all SHA-1s unchanged; Bearss baseline byte-exact (769/177/31/24, 466.1s) | `backend/G_0_SCOUT_REPORT.md` · commit `52fadd5` |
| F2 | Phase G.0.5 — parser scout: 3 bugs named (drawing-index regex too permissive · 7-9× redundant text extraction · Filter 4 pdfplumber open/close per page); zero rogue parsers; cache-key shape verified trivial | General | 2026-05-01 | Read-only; 230/19/0; SHA-1s unchanged | `backend/G_0_5_PARSER_SCOUT_REPORT.md` · commit `9cdcec5` |
| F3 | Phase G.0.6 — regex theory validation: Alt C (\\d{3,} digit floor) cleanly rejects Silverleaf p5 bogus index AND accepts Bearss p0 real index on 2 control points | General | 2026-05-01 | Read-only paper experiment; 3 alternatives tested; decision matrix unambiguous | `backend/G_0_6_REGEX_VALIDATION_REPORT.md` · commit `2514457` |
| F4 | Phase G.0.7 — corpus validation: Alt C breaks on 4 of 15 bidsets; hybrid pattern derived as alternation of `\\d{3,}` OR `\\d+\\.\\d+`; corpus-clean across all 15 bidsets | General | 2026-05-01 | Read-only; 15-bidset sweep; hybrid validated against Silverleaf p5 + Bearss p0 control points | `backend/G_0_7_REGEX_CORPUS_REPORT.md` · commit `cfdb806` |
| F5 | Phase G.0.8 — pre-implementation recon (4 scouts): cache call-site map (21 sites); regex blast radius (zero impact on green build); Filter 4 cost (78.7% of dispatch wall-clock on Bearss); Stage 13 pdfplumber retire feasibility (5/5 word fields available from PyMuPDF) | General | 2026-05-01 | Read-only; instrumented Bearss timing; ship-order recommended | `backend/G_0_8_PRE_IMPLEMENTATION_RECON_REPORT.md` · commit `7155286` |
| F6 | Phase G.0.9 — real-bidset verification: 5-scout team validated hybrid byte-equivalence on full Bearss against current regex (3 dispatches, all 769/177/31/24 exact); determinism confirmed | General | 2026-05-01 | Read-only; monkey-patch only, dispatch_gate.py SHA-1 unchanged; vault SHA-1s held | `backend/G_0_9_REAL_BIDSET_VERIFICATION_REPORT.md` · commit `af67825` |
| F7 | Phase G.1 — test-floor audit + hybrid regex patch: floor honest (X=230 genuine pass, Y=0 silent-skip, Z=19 explicit-skipif on missing test_plans/ PDFs); regex patch shipped (one-line `dispatch_gate.py:57`); Bearss byte-equivalent 769/177/31/24; Silverleaf sheet_map 4→32 mapped pages (8x improvement); Guardrail #6 fired — page-classification cascade did NOT shift; housekeeping Track 3 halted per guardrail. **Ratified 2026-05-03**: LOW RESOLUTION warning explained (cross-ref resolution rate 22% < hardcoded 30% threshold at `core/context.py:413` — not 50% as G.1 report stated; threshold value corrigendum banked). Patch ships clean on its own merits. | General (ship) / Developer (ratify) | 2026-05-01 / 2026-05-03 | Sacred floors held; vault SHA-1s unchanged except `dispatch_gate.py` (line 57 only); leak-check threshold confirmed via direct read of `check_for_leaks` source | `backend/G_1_GATE_REPORT.md` · commit `7318d8b` |
| F8 | Recon cascade map — read-only inventory of every read/write site for major `PlanSetContext` fields (`sheet_map`, `page_to_sheet`, `pages`, `project`, `project_scope`, `dispatch_warnings`, `trade_module_outputs`, `scope_pages`); filter chain trace for run_filter_1 through run_filter_5; trade module Protocol contract documented end-to-end. Confirmed cascade gap that broke G.1 hypothesis: MEP fallback at `dispatch_gate.py:463-466` reads sheet_map discipline and assigns MEP_PLAN; no equivalent cascade for S/A/C/L/G/FP disciplines. | Developer | 2026-05-03 | Sacred floor 230/19/0 held start and end; vault SHA-1s unchanged (dispatch_gate.py at 2a708d… post-G.1, others as recorded); single-file diff (445 lines added, no other modifications) | `backend/RECON_CASCADE_MAP.md` · commit `cef1ca7` |
| F9 | Phase G.2 Track 1 — corpus survey scout (invalidated discipline-fallback premise; found keyword-rule gaps + pc.title not read) | Developer | 2026-05-03 | sacred floor 230/19/0 held; read-only | `backend/G_2_CORPUS_SCOUT_REPORT.md` · commit `dec0af5` |
| F10 | Phase G.2 — corpus-wide classifier upgrade (pc.title read + _PAGE_TYPE_RULES extended; rescoped from discipline fallback per Track 1 findings) | Developer | 2026-05-03 | hard gate 4/4 PASS; sacred floor 237/19/0 | `backend/G_2_HARD_GATE_REPORT.md` · commit `170fcd7` |
| F11 | Phase G.3 — single-pass-per-page extraction (PDFEngine cache + Filter 4 pdfplumber hoist + Stage 13 PyMuPDF reuse, replacing pdfplumber.extract_words). Absorbed scope previously held by F12. | Developer | 2026-05-03 | hard gate PASS (Chipotle Tarpon dispatch completes, 39 = 39 pages); sacred floor 237 → 242/19/0; vault SHA-1s held except `dispatch_gate.py` and `pdf_engine.py` | `backend/G_3_GATE_REPORT.md` · commit `e51c785` |
| F12 | (the original F12 — "Phase G.4's scope of Filter 4 hoist + Stage 13 pdfplumber retire shipped as part of G.3" — was absorbed into F11. The G.4 phase that actually shipped is the scope-tab + backend-storage phase below at F13.) | — | — | — | — |
| F13 | Phase G.4 — scope tab as full backend-DB-frontend cycle + backend file storage + dropzone retire + PROJECT_CLAUDE cleanup. Baseline items 1/2/3 → MET. New tables: `job_project_scope`, `scope_systems`. New endpoints: GET/POST/PATCH/DELETE/rescan on `/jobs/{id}/scope/*`, multipart `POST /jobs/upload`, `GET /jobs/{id}/pdf`. Killed: JSON path-string `POST /jobs`, `JobCreateRequest`, `#dropZone`, `#serverPdfPath`, `populateScopeFromResults`, `mergeScopeProposal`. | Developer | 2026-05-07 | hard gate 11/11 PASS · sacred floor 242 → 255/19/0 · vault SHA-1s held (all 7) · empirical Daniel-driven verification on Silverleaf (manual-entry path) + Taco Bell (auto-detect path, `tpo @ 0.95`) | `backend/G_4_GATE_REPORT.md` · commits `8f1de64` → `a1d8ded` |
| F14 | Phase G.5a — annotation persistence (baseline items 5+6 → MET; item 8 → MET). New `annotations` SQLite table (type discriminator + JSON data_json blob); 5 CRUD endpoints under `/jobs/{id}/annotations`; viewer tools (line/pin/polygon) rewired to API relay (optimistic-push + async POST + refetch); `Viewer.rebuildOverlayFromState()`; cascade-delete on `scope_systems` removal; takeoff page-number labels per row; auto-pin extractor wired (idle until Stages 6-9 land). **Mid-phase architectural correction (CP4):** TradeModule Protocol extended with 3 vocabulary classmethods (`get_palette_seed`/`get_expected_items`/`get_systems_catalog`); per-trade vocabulary stays inside trade modules; `_resolve_trade_module(trade)` lazy-LOCAL-imports inside `job_storage.py`; grep-assertion test enforces no `roofing_*`/`glazing_*` imports leak. **Vault unfreeze ceremony:** 4 trade-knowledge files unfrozen for this CP per Daniel's contract ("1 then test if we have to change anything when test clears this gate vault rule goes back into effect"); re-locked at NEW SHA-1 baseline at gate close. CP4.1 fixes: route palette by `unit` not `derive_from`; cricket added to typical_items; Equipment Curbs EA→SF. CP4.2 fix: viewer DELETE race (pre-refetch + local-id fallback). | Developer | 2026-05-08 | soft gate 12/12 PASS · sacred floor 255 → 273/19/0 (+18 net) · vault re-locked at new SHA-1s for 4 trade files (`roofing_module 9a6085d4…`, `roofing_vocabulary 863ffb01…`, `glazing_module 1b449e97…`, `glazing_vocabulary 008ed191…`); `debug_module`/`dispatch_gate`/`pdf_engine` HELD · Daniel-driven empirical run on Taco Bell verbatim "all clean good to go" | `backend/G_5a_GATE_REPORT.md` · commits `dd65940` → `364e6d0` |
| F15 | Phase G.5b — PyMuPDF tile rendering API in `pdf_engine.py` (CP1: `render_page_tiled()` + `_estimate_render_memory_mb()` + `_compute_tile_rects()` + 4 module constants — plumbing for G.6 Stage 6 contour detection on ARCH-D pages at 250 DPI, 50 MB threshold, 5% overlap, 2x2 grid per G.0 scout math) + surgical theater cut of `detect_firm`/`architect_profile` dispatch invocation (no downstream consumer; ~20-50ms saved per dispatch when storage active). **CP2 (Filter 4 tile consumer) RETIRED** during fact-find when scout work confirmed `pdfplumber.extract_tables()` is vector-bound algorithmic work, not rasterization-bound — tiling does not help. Pipeline-wide theater audit shipped as the real deliverable: pandas/OCR claim resolved FALSE (zero hits across `tracepoint_port/`); pipeline order verified correct (TracePoint = Huckleberry strict subset); 10-item theater inventory with cascade analysis; algorithmic Filter 4 replacement parked as Phase 10 (post-hard-gate, Daniel directive 2026-05-09: Taco Bell <400s, no current pain). | Developer | 2026-05-09 | soft gate 5/5 CP MET · sacred floor 273 → 278/19/0 (+5 tile API tests) · vault re-locked at new SHA-1s for 2 integration-frozen files (`pdf_engine eb5b8372…`, `dispatch_gate 71e409a2…`); 4 trade-knowledge files + `debug_module` HELD · backend-only cuts, no live dispatch needed | `backend/G_5b_GATE_REPORT.md` · commits `36017fb` (CP1) → canon |
| F16 | Phase G.6 — Stages 6-9 geometry/scale/callout extraction wiring (deferred since D.1; auto-pin INSTANCES wait on this — extractor already wired in G.5a CP1 and starts producing rows immediately once Stages 6-9 land; G.5b tile API ready as Stage 6 consumer). | _____ | _____ | _____ | _____ |
| F17 | 3-bidset hard gate + deferred E.2.2 visual hard gate (closes Phase F/G chain permanently) | _____ | _____ | _____ | _____ |
| F18 | Phase 10 — algorithmic Filter 4 replacement (parked Daniel 2026-05-09; post-hard-gate). Replace `pdfplumber.extract_tables()` (vector-bound 2.91s/page on Bearss p15 per G.0 scout) with a faster algorithm (PyMuPDF `Page.find_tables()` native to current dep, custom vector-direct grid finder, or hybrid). Requires parity gate (legends + raw_tables shape match) and bidset-wide wall-clock measurement on Bearss/Silverleaf/Vine. | _____ | _____ | _____ | _____ |

## Phase G — Auto-Notation Product

| # | What | Who | Date | Validation | Evidence |
|---|---|---|---|---|---|
| G1 | Phase F — three-state annotations + provenance + training loop | _____ | _____ | _____ | _____ |

## Phase H — Security Cluster (post-user-testing)

| # | What | Who | Date | Validation | Evidence |
|---|---|---|---|---|---|
| H1 | USERS table + auth (JWT or sessions) | _____ | _____ | _____ | _____ |
| H2 | CORS lockdown | _____ | _____ | _____ | _____ |
| H3 | OpenAPI docs hidden in production | _____ | _____ | _____ | _____ |
| H4 | Postgres migration from SQLite | _____ | _____ | _____ | _____ |
| H5 | File upload via API (local disk → cloud when data demands) | _____ | _____ | _____ | _____ |
| H6 | SETTINGS table | _____ | _____ | _____ | _____ |
| H7 | DEVELOPER table | _____ | _____ | _____ | _____ |
| H8 | PROJECT_SCOPE_BY_TRADE rollup table | _____ | _____ | _____ | _____ |
| H9 | Login screen | _____ | _____ | _____ | _____ |

---

## Rules for working in this project

1. **Every row gets signed when shipped.** Unsigned = unverified.
2. **Validation method is specific.** "tested" is not validation. "pytest 230/19/0" is. "SHA-1 ae9e5b28… match" is. "Silverleaf hard gate 8/8 PASS" is.
3. **Evidence link points to the receipt.** Gate report path, commit SHA, file path. Not "see commit history."
4. **One row per ship, not per attempt.** If a phase needs three patches, that's three rows on the same row's sub-numbering, not one row claiming success.
5. **Don't backfill historical work without evidence.** If you can't link the evidence, the row stays "(historical)" — don't fabricate signatures.
6. **The General signs march-orders-style work.** Phases, sub-phases, sweeps, gate reports.
7. **The Developer signs hands-on technical work.** Calibration, debugging sessions, surgical patches, infrastructure maintenance.
8. **If a row is signed but the evidence link is broken, the row is invalid until restored.**
9. **Canon updates happen in chat.** Claude in chat produces complete updated CHECKLIST.md, ITINERARY.md, PROJECT_CLAUDE.md as deliverable files at sign-out. Daniel does not paste snippets or merge text. Files arrive ready to drop in.

---

## Handoff Template (bottom of file — fill in at sign-out)

When a session ends, the role copies this template, fills it in, and appends below the most recent handoff. Future Claude reading this section knows what just happened and what's next.

```markdown
### Handoff — [DATE] — [ROLE]

**Session length:** ~X minutes
**Branch state:** branch name + commit SHA + push status
**What shipped:** one sentence
**Sacred floors at session end:** backend X/Y/Z, frontend X/Y, vault SHA-1s status
**Stops fired:** (list, or "none")
**What's pending for next role:** one sentence + which file to read first
**Open questions for Daniel:** (list, or "none — Daniel has all needed info")

**Next-eligible work:** (phase / sub-phase / patch name)
```

---

### Handoff — 2026-04-30 — Innovator (extended-thinking Claude in current chat)

**Session length:** Multi-session conversation across calibration → D.1 → D.2 → E.0 → E.1 → E.1 patches → E.2.0 → E.2.1 march orders draft → meta-orchestration design
**Branch state:** Most recent shipped: `phase2-v0.3-E2-0-strip-plan` head `a1c804c`. E.2.1 march orders drafted but NOT yet executed — awaits Claude Code launch in new chat.
**What shipped:** All phases through E.2.0 ratified; E.2.1 march orders drafted and approved; orchestration design (Huckleberry Dispatch project) settled on 5 files with 2 roles
**Sacred floors at session end:** Backend 222/19/0; frontend 138/138 against v6.3.5; all 5 vault SHA-1s + v6.3.5 SHA-1 unchanged
**Stops fired:** None this session — but other-Claude session caused multi-day drift loop on E.2.0 review (lesson: stop using fresh Claudes for mid-phase review)
**What's pending for next role:** Launch E.2.1 in Claude Code per `MARCH_ORDERS_phase_E_2_1_strip.md`. Read PROJECT_CLAUDE.md → BLOCK_RUN.md → march orders → E.2.0 design deliverables.
**Open questions for Daniel:** None — six locked decisions (Q1-Q6) + DEGRADED→CHECKING corrigendum + sub-bullet calls (stub createJob/getJob, inline makePath, delete test:spotchecks) all settled.

**Next-eligible work:** Phase E.2.1 — frontend strip + new file + v6.3.5 archival

---

### Handoff — 2026-05-01 — General (prior chat — handoff drafted but sign-off was incomplete)

**Session length:** Multi-session conversation across G.0 → G.0.5 → G.0.6 → G.0.7 → G.0.8 → G.0.9 → G.1 march orders → G.1 execution → G.1 debrief
**Branch state:** Most recent shipped: `phase2-v0.3-G1-audit-and-regex` head `7318d8b`, pushed. G.1 patch shipped but NOT YET ratified at session end.
**What shipped:** Phase E.2.1 → E.2.2 cleared; G.0 scout mission and full G.0.5–G.0.9 scout chain shipped; G.1 hybrid regex patch shipped (one-line at dispatch_gate.py:57); recon-cascade-map deferred to next session
**Sacred floors at session end:** Backend 230/19/0 (E.2.2 added 8 tests for new endpoints, 222 → 230); frontend 23/23 against new file (E.2.2 added 3 tests, 20 → 23); vault SHA-1s held throughout (only `dispatch_gate.py` changed during G.1 patch as authorized)
**Stops fired:** Guardrail #6 fired during G.1 Track 2c — page-classification cascade did not shift on Silverleaf as predicted; Track 3 housekeeping halted as required
**What's pending for next role:** G.1 ratification (small scout on LOW RESOLUTION warning before final CHECKLIST signature); cascade-discipline-recon to identify why Filter 2 didn't move; page-classification phase scoping
**Open questions for Daniel:** New "LOW RESOLUTION: 22% cross-references resolved" warning surfaced post-G.1 — needs investigation before final ratification

**Next-eligible work:** Phase G.1 ratification + cascade recon

**Banked discipline lesson (2026-05-01):** When a proposed fix depends on cascade behavior, the first scout traces the cascade itself — not the bug, not the theory, not the corpus. "If A causes B, find the line where A causes B. If you can't find that line, the cascade doesn't exist." The G.1 chain ran 5 scouts on a cascade hypothesis nobody verified. Drift was bounded to ~3 hours scout time by sacred-floor discipline; previous projects have lost weeks. Discipline kept it bounded; it didn't prevent it. Question-discipline ("are we asking the right question?") is the General's job and was lacking.

---

### Handoff — 2026-05-03 — Developer

**Session length:** ~3 hours conversation across G.1 ratification scout → recon-cascade-map march snippet draft + Claude Code execution + review → G.2 march orders draft → canon sign-out
**Branch state:** Most recent shipped: `phase2-v0.3-recon-cascade-map` head `cef1ca7`, pushed. G.1 verbally ratified this session; recon shipped via Claude Code execution; G.2 march orders drafted but not yet executed (awaits next chat).
**What shipped:**
1. G.1 ratification — `check_for_leaks` source read at `core/context.py:403-415` confirmed LOW RESOLUTION threshold is hardcoded at 30% (not 50% as G.1 report stated); 22% Silverleaf rate fires legitimately; warning is system correctly surfacing increased visibility post-patch, not a regression. G.1 ships clean.
2. Recon cascade map — drafted march snippet, ratified Claude Code's 445-line deliverable. Confirmed: MEP fallback at `dispatch_gate.py:463-466` is the only sheet_map → page_type cascade in code; filter execution order is 1-2-4-3-5 (Filter 4 reordered before 3 for keynote legend availability); DebugModule does NOT follow TradeModule Protocol (receives PlanSetContext directly); GlazingModule does NOT read project_scope (RoofingModule is sole consumer at 5 sites).
3. Phase G.2 march orders drafted — discipline-based page-type fallback. Two-track structure: corpus survey scout (Track 1, read-only) → patch (Track 2, single function modification). Track 2 gated behind Daniel go-ahead between tracks to prevent cascade-hypothesis-loop repeat.

**Sacred floors at session end:** Backend 230/19/0; frontend 23/23; vault SHA-1s held (post-G.1 dispatch_gate.py at `2a708d…`, roofing/glazing/debug unchanged)
**Stops fired:** None this session
**What's pending for next role:** Launch G.2 Track 1 in Claude Code per `MARCH_ORDERS_phase_G_2_discipline_fallback.md`. Track 2 explicitly gated — STOP after Track 1 ships and await Daniel go-ahead.
**Open questions for Daniel:** None settled this session — corpus scout will surface the discipline-to-page-type matrix and Daniel will lock it before Track 2 patch.

**Next-eligible work:** Phase G.2 Track 1 (corpus survey scout)

**Banked discipline lessons (2026-05-03):**
1. **Lane discipline drift acknowledged.** Daniel announced this session as Developer; some work crossed into General territory (drafting G.2 march orders, debriefing G.1 gate report and recon as primary activity). Daniel did not call a role switch but accepted the hybrid mode for this session. Future sessions: if planning/march-orders work is needed, Daniel calls "switch to General" first per ROLES.md §2 cross-role rule 2.
2. **Karpathy step-0 mandate retained.** When proposing a fix that depends on cascade behavior, the first scout traces the cascade itself. The recon delivery proves the discipline pays — full ctx field cascade map produced in one read-only Claude Code session, would have prevented the entire G.1 five-scout chain.
3. **Test fixture filename specificity.** Daniel populated `backend/test_plans/` with full bidsets, but the 19 SKIPPED tests in `test_dispatch.py` look for specific extracted slice filenames (`cfa_roof_A230.pdf`, `Vine_Street_*.pdf`, `tacobell_roof_A12.pdf`, `aeasilverleaf_roof_A106.pdf`). Floor remained 230/19/0. Parking item: either generate the 4 trimmed slice PDFs or rewrite fixtures to use full-bidset fallback pattern. Not a current-phase blocker.
4. **G.1 LOW RESOLUTION threshold corrigendum banked.** G.1 report claimed 50% threshold; actual code at `core/context.py:413` is `if rate < 0.3`. Hardcoded literal, no config variable. Corrigendum noted in F7 row.

---

### Handoff — 2026-05-03 — Developer

**Session length:** ~90 minutes (Claude Code execution of G.2 classifier upgrade march orders)
**Branch state:** `phase2-v0.3-G2-classifier-upgrade` head `170fcd7` (code commit) + canon commit pending, pushed after canon.
**What shipped:** Phase G.2 corpus-wide classifier upgrade — `_classify_page_type` reads `pc.title` alongside `tb_text` and `full_text`; `_PAGE_TYPE_RULES` extended with corpus-validated keywords. 7 new unit tests. 4-bidset hard gate PASS. Bearss byte-equivalent (769/177/31/24). Hampshire 4→0, Chipotle Tarpon 3→0, Shoppes Avalon 2→0.
**Sacred floors at session end:** Backend 237/19/0; frontend 23/23 (untouched); vault SHA-1s held except `dispatch_gate.py` (expected: 2a708d19 → 09bc0340)
**Stops fired:** None. Hampshire initially failed (corpus scout's stated keywords didn't match actual page text — "FIRE SPRINKLER PLAN" split across lines; solved by adding "FIRE SPRINKLER" standalone keyword).
**What's pending for next role:** Phase G.3 (cache layer) march orders. General drafts after Daniel reviews G.2 ship.
**Open questions for Daniel:** None — hard gate 4/4 PASS, all criteria met.

**Next-eligible work:** Phase G.3 — single-pass-per-page extraction (caching layer + pdfplumber consolidation)

**Banked lesson (2026-05-03):** Corpus scout text samples are not always verbatim quotes of what `extract_text()` returns. The scout inferred page content from visual inspection; actual PyMuPDF extraction splits multi-line title blocks into separate lines. Always verify keyword presence via `engine.extract_text()` on the actual PDF before committing keywords to rules.

---

### Handoff — 2026-05-03 — Developer

**Session length:** ~75 minutes (Claude Code execution of G.3 single-pass-per-page extraction march orders)
**Branch state:** `phase2-v0.3-G3-single-pass-extraction` head `e51c785` (code+tests+report) + canon commit pending, push after canon.
**What shipped:** Phase G.3 single-pass-per-page extraction. PDFEngine now caches `extract_text` and `extract_text_blocks` per `(id(doc), page_num, method)`. Filter 4 opens pdfplumber once per dispatch in `run_filter_4` (was: once per SCHEDULE_SHEET page in `_parse_tables_on_page`). Stage 13 trade-module wiring (`_run_trade_modules`) replaces `pdf_page.extract_words()` with cached `engine.extract_text_blocks(doc, page_idx)`. F12 (Phase G.4) absorbed into F11 — same branch, same commit. 5 new cache unit tests (`TestPDFEngineCache` in `test_pdf_engine.py`).
**Sacred floors at session end:** Backend 237 → **242/19/0** (+5 cache tests); frontend 23/23 (untouched); vault SHA-1s held except `dispatch_gate.py` (`09bc0340…` → `8b39fd0e…`) and `pdf_engine.py` (`e872f69e…` → `daf06dd2…`)
**Stops fired:** None. One observation surfaced during failing-test step: 4 of 5 cache separation tests passed accidentally pre-implementation (because un-cached implementations naturally return new objects each call); strengthened each test to require cache-hit identity on repeat call so all 5 fail until caching exists. Tests then all passed post-implementation.
**What's pending for next role:** Phase G.5 (render optimization) march orders, or whichever phase Daniel chooses next.
**Open questions for Daniel:** None — hard gate PASS (Chipotle Tarpon, 39 = 39 pages, byte-identical dispatch warning).

**Next-eligible work:** Phase G.5 — render optimization (PyMuPDF tiling 200-300 DPI), or new phase pending Daniel's call.

**Banked lessons (2026-05-03):**
1. **Pre-flight clean tree blocker handled correctly.** Working tree had ~40 deleted files paired with untracked moves to `safe_for_removal/` and `backend/archive/` — uncommitted G.2-era housekeeping. Stashed under explicit message before branching from `e7a3884`. Did NOT commit drift onto G.3 branch (would have violated two-commit guardrail). Stash entry remains for restoration after G.3 ships.
2. **Karpathy step needs strengthening for separation tests.** Initial cache tests for "separates pages / separates methods / separates documents" all *passed* pre-implementation because each non-cached call returns a fresh object naturally. The separation property held by accident; the cache property was unproven. Fix: each separation test must also assert repeat-call identity on at least one side, so absence of cache fails the test. The lesson: a test that passes for the wrong reason is worse than a test that fails — it doesn't enforce the spec it claims to enforce.
3. **Wall-clock improvement on Chipotle: 58.72s → 50.05s warm (−14.8%).** Recorded but not a gate criterion per orders. Per-page extraction call count dropped from up to 9-15 (text + blocks combined) to 1 each, plus Filter 4's pdfplumber.open went from per-SCHEDULE-page to once per dispatch (Chipotle had 0 SCHEDULE_SHEET pages so this didn't show on the wall-clock here, but the change still ships).
4. **Trade modules quiet on Chipotle pre- and post-patch (0 entries in `trade_module_outputs`).** This is pre-existing behavior, not a G.3 regression. Confirmed by stashing G.3 changes, re-running dispatch, observing same 0-entry result. Granularity change (pdfplumber word-level → PyMuPDF paragraph-level `TextBlock`s) had no observable effect here because modules weren't firing on this bidset regardless.

---

### Handoff — 2026-05-07 — Developer

**Session length:** Multi-day, multi-session conversation across G.D2 review → G.4 plan rewrite (Daniel locked architectural rule mid-phase: "frontend = window only, backend = source of truth, every edit is a DB mutation, refresh proves it") → 6-CP execution → live empirical hard gate
**Branch state:** `phase2-v0.3-G4-scope-fix-and-backend-storage` HEAD `a1d8ded` + canon commit pending; total 7 commits when canon lands; not yet pushed (awaiting Daniel's go on push).
**What shipped:** Phase G.4 — scope tab as full backend-DB-frontend cycle (CP1 + CP1.1 polish + CP1.2 flatten bridge), backend file upload + storage + GET /pdf endpoint (CP2), single upload point (CP3 — kill JSON path-string, kill dropzone-only render path, kill Step 1.5), PROJECT_CLAUDE.md cleanup (CP4 — 4 edits including new misconception entry on `ctx.project_scope` as canonical scope source). Two new SQLite tables: `job_project_scope`, `scope_systems`. Five new API endpoints under `/jobs/{id}/scope/*` plus multipart upload + file-serving endpoints. Frontend rewired for render+relay with localStorage rehydrate of `currentJobId` for refresh-survival.
**Sacred floors at session end:** Backend 255/19/0 (was 242 at Step 0c, +13 net: +9 G.4 scope tests, +7 multipart tests, −3 retired JSON-path tests). Frontend 28 (was 23, +5 SCOPE_API_TESTS net after CP3 migration). All 7 vault SHA-1s held identical to Step 0c capture: `roofing_module ae9e5b28…`, `roofing_vocabulary ec6c17f8…`, `glazing_module 52c01442…`, `glazing_vocabulary 64249c8e…`, `debug_module 78f71d90…`, `dispatch_gate 8b39fd0e…`, `pdf_engine daf06dd2…`.
**Stops fired:** None functionally. One mid-phase architectural correction: original chat-Claude G.4 march orders prescribed a frontend-only literal fix that surfaced per-page `_scope` noise; Daniel rejected, plan was rewritten to the architecturally-correct backend-DB-driven approach before any code shipped. Original CP1 commit `0ccfbae` was reverted/rewritten on a fresh branch.
**What's pending for next role:** Hard gate ship paperwork is done with this commit. Branch push awaits Daniel's go. After push, next planning conversation is G.5 priority pick — annotation persistence (baseline items 5+6) vs render optimization (original Phase G/F1 scope).
**Open questions for Daniel:** None on G.4. Two pending for next planning conversation: which G.5 candidate goes first; whether to add a tuning phase for `_resolve_scope_system` evidence widening (would require dispatch_gate edit, own phase).

**Next-eligible work:** Daniel-picked between G.5 candidates (annotation persistence vs render optimization).

**Banked discipline lessons (2026-05-07):**
1. **`_resolve_scope_system` confidence is binary, not continuous.** Function emits 0.0 or 0.7+. No values in the 0.0–0.7 band. Lowering `_AUTO_PREPOPULATE_THRESHOLD` is not a useful knob — the real lever is widening the evidence sources the function votes on (vault-locked, future phase). Banked so future tuning conversations don't waste cycles on threshold tweaking.
2. **The `scope_systems` CRUD pattern is the template for baseline items 5+6.** When G.5/c.2 ships annotation persistence, the right shape is: new SQLite table + GET/POST/PATCH/DELETE endpoints + frontend renders from API + frontend POSTs every mutation + refresh re-fetches. Same architecture as G.4. The viewer tools' in-memory `App.project.annotations` becomes a transient render cache only.
3. **RoofingModule output is fully persisted but unrendered.** All 8 per-page roofing fields (drains, scuppers, hatches, RTUs, curbs, pipe boots, exhaust fans, _scope) plus equipment_pins + warnings ship to the frontend in `JobResultsResponse.trade_outputs` but no frontend code reads them. Confirmed by recon (full chain trace + grep). Not a G.4 regression — matches the original baseline-items-5+6 deferral. Naming it explicitly so the next phase doesn't have to re-discover it.
4. **Architectural-rule check on every CP draft.** Daniel's rule "frontend = window only, backend = source of truth, every edit is a DB mutation, no migrate-later" caught the original G.4 march orders' drift. Future planning conversations should run new orders through the same check before approval.

---

### Handoff — 2026-05-08 — Developer

**Session length:** Multi-session conversation across G.5a planning → CP1-CP4 execution → CP4 architectural correction (Daniel forbade `roofing_vocabulary` import in `job_storage.py` mid-CP) → vault unfreeze ceremony → CP4.1 routing+vocabulary fixes → CP4.2 viewer DELETE race fix → Daniel-driven empirical soft gate on Taco Bell
**Branch state:** `phase2-v0.3-G5a-annotation-persistence` HEAD `364e6d0` + canon commit pending; total 7 commits when canon lands; not yet pushed (awaiting Daniel's go on push).
**What shipped:** Phase G.5a — annotation persistence (baseline items 5+6 → MET; item 8 → MET). New `annotations` SQLite table + 5 CRUD endpoints + viewer tools rewired to API relay. **Mid-phase architectural correction:** TradeModule Protocol extended with 3 vocabulary classmethods so `core/job_storage.py` stays trade-agnostic ("hardcoding roofing verbiage and systems outside of module is forbidden"). Vault unfreeze ceremony executed on 4 trade-knowledge files per Daniel's contract; re-locked at NEW SHA-1 baseline at gate close. CP4.1: routing dispatch by `unit` (not `derive_from`) + cricket added to typical_items + Equipment Curbs EA→SF. CP4.2: viewer DELETE race-condition fix (pre-refetch + local-id fallback for optimistic-pushed entries).
**Sacred floors at session end:** Backend **273/19/0** (was 255 at G.4 close, +18 net: +6 annotations CRUD/cascade, +1 auto-pin extractor, +3 roofing Protocol classmethods, +1 glazing skeletal, +2 `_seed_palette_via_protocol` (incl. grep-assert), +1 create_scope_system auto-seed, +1 dispatch auto-seed, +1 cricket polygon, +1 equipment curbs SF, +1 grep-assert no per-trade imports). Frontend **28/28** held (viewer rewire validated by Daniel-driven empirical run, not new automated tests). Vault re-locked at NEW SHA-1s for 4 trade files: `roofing_module 9a6085d4a3fbe7bbafa4b920c75868261f3c3a60`, `roofing_vocabulary 863ffb01de05ed8a55b1975268c3ff3a9c1d4252`, `glazing_module 1b449e9716ef2fe83ee0f2546ad2281deef5ac55`, `glazing_vocabulary 008ed1914422e7f63a8fe90833bcda9e0cb3b44a`. UNCHANGED: `debug_module 78f71d90…`, `dispatch_gate 8b39fd0e…`, `pdf_engine daf06dd2…`.
**Stops fired:** Two mid-phase architectural corrections from Daniel: (1) original CP4 plan would have imported `roofing_vocabulary.SYSTEMS/ITEMS` from `job_storage.py` — Daniel forbade ("hardcoding roofing verbiage and systems outside of module is forbidden"; "roofing module unlock vault is my command to make"); plan rewritten to TradeModule Protocol vocabulary methods with vault unfreeze authorization ("1 then test if we have to change anything when test clears this gate vault rule goes back into effect"). (2) Cricket missing from polygon palette + Equipment Curbs wrong unit surfaced during Daniel's first live run — fixed in CP4.1. (3) DELETE button race-condition surfaced during Daniel's second live run — fixed in CP4.2. Final receipt verbatim: "all clean good to go".
**What's pending for next role:** Hard gate ship paperwork done with this commit. Branch push awaits Daniel's go. After push, next planning conversation is Daniel's pick between **G.5b (render optimization)** and **G.6 (Stages 6-9 geometry wiring — unlocks auto-pin INSTANCES, extractor already wired)**.
**Open questions for Daniel:** None on G.5a. Two pending for next planning conversation: G.5b vs G.6 priority pick; whether to schedule Phase C.3c follow-on (real glazing palette implementation) before either.

**Next-eligible work:** Daniel-picked between G.5b (render optimization) and G.6 (Stages 6-9 geometry wiring).

**Banked discipline lessons (2026-05-08):**
1. **TradeModule Protocol vocabulary pattern.** Trade-specific knowledge (item names, system types, expected items, units, vocabulary) lives INSIDE the trade module. `core/job_storage.py` and `api/` are trade-agnostic; they call Protocol methods, never import per-trade constants. New trades implement the Protocol; everything else works without code changes. Enforced at the test floor by `test_no_per_trade_imports_in_job_storage` (greps the file for `roofing_*`/`glazing_*` imports). Lazy LOCAL imports inside `_resolve_trade_module(trade)` are the only path.
2. **Vault unfreeze ceremony (re-applied).** Same protocol as G.3 used for `dispatch_gate.py` + `pdf_engine.py`: pre-capture SHA-1s → unfreeze for the work → soft-gate → re-capture SHA-1s → vault re-locks at new values. Daniel's contract is the load-bearing piece: "1 then test if we have to change anything when test clears this gate vault rule goes back into effect" — temporary unfreeze for the phase, vault re-engages at the new baseline once stable.
3. **Optimistic-push race window is real.** Frontend optimistic-push patterns have a 100-300ms window where entries exist on the overlay before the POST returns and assigns the server ID. Destructive operations (DELETE, update, recategorize) must pre-refetch annotations OR carry a local-id fallback. Banked as a recipe: when adding any future mutation UI to the viewer, audit the optimistic-push pattern.
4. **Auto-pin TYPES vs INSTANCES distinction.** G.5a CP4 ships palette TYPES (vocabulary-based, no geometry needed — item names + units + colors). Auto-pin INSTANCES (the actual drain/scupper/RTU rows from PDF callouts) wait on Stages 6-9 wiring. The extractor (`_extract_auto_pins_from_trade_output`) is already wired in CP1 and currently produces 0 rows because `RoofingModule.equipment_pins=[]`; once Stages 6-9 land, rows start appearing immediately.

---

### Handoff — 2026-05-09 — Developer

**Session length:** Multi-session conversation across G.5b plan approval → CP1 tile API ship (RED→GREEN tests, vault unfreeze) → CP2 fact-find on Filter 4 (discovered tiling doesn't help vector-bound work) → §7 stop → 3-Explore-agent pipeline-wide theater audit → cascaded report → Daniel-locked Path A + Phase 10 parking → surgical theater cut of `detect_firm` invocation
**Branch state:** `phase2-v0.3-G5b-render-tile-and-filter4` HEAD `<canon commit pending>`; total 2 code commits + canon when this lands; not yet pushed (awaiting Daniel's go on push).
**What shipped:** Phase G.5b — PyMuPDF tile rendering API in `pdf_engine.py` (CP1, plumbing for G.6 Stage 6 contour detection on ARCH-D pages at 250 DPI, 50 MB threshold, 5% overlap, 2x2 grid per G.0 scout math) + surgical theater cut of `detect_firm`/`architect_profile` dispatch invocation (no downstream consumer; ~20-50ms saved per dispatch when storage is active). **CP2 (Filter 4 tile consumer) RETIRED** during fact-find when scout work confirmed `pdfplumber.extract_tables()` is vector-bound algorithmic work, not rasterization-bound — tiling does not help. Pipeline-wide theater audit shipped as the real deliverable (see backend/G_5b_GATE_REPORT.md §3). Algorithmic Filter 4 replacement parked as Phase 10 (post-hard-gate, Daniel directive 2026-05-09: Taco Bell <400s, no current pain).
**Sacred floors at session end:** Backend **278/19/0** (was 273 at G.5a close, +5 net: tile API tests). Frontend **28/28** held. Vault re-locked at NEW SHA-1s for 2 integration-frozen files: `pdf_engine eb5b8372f6f0c52de5a81b452399035c2b720551` (was `daf06dd266d52983a0c761669f8af1ed825088a7` post-G.3); `dispatch_gate 71e409a27caf78525d663fa6ca11d0e7a0c9b7ca` (was `8b39fd0eb4fa6e5a3a61f8da7f9a095be7bd091a` post-G.3). HELD: 4 trade-knowledge files at G.5a baseline; `debug_module 78f71d9030cde3b173389603f5f39bd6bedaac07`.
**Stops fired:** Two §7 stops mid-phase: (1) vault SHA-1 method discrepancy at session start — `git hash-object` returned non-canon values; investigation confirmed canonical method is `sha1sum` of raw file content on disk (CRLF preserved on Windows), `git hash-object` normalizes to LF and gives different values. (2) CP2 fact-find revealed `pdfplumber.extract_tables()` is vector-bound, not rasterization-bound — substituting tiles via `pdfplumber.Page.crop()` would be slower per-page and risk losing tables that span tile boundaries. Daniel chose pipeline-wide scout instead of speculation-patching CP2; theater audit produced; Path A locked (ship CP1 + surgical theater cut + park algorithmic work as Phase 10).
**What's pending for next role:** G.5b ship paperwork done with this commit. Branch push awaits Daniel's go. After push, next phase is **G.6 (Stages 6-9 geometry/scale/callout extraction wiring)** — auto-pin INSTANCES finally appear in viewer + takeoff; G.5b tile API ready as Stage 6 consumer; G.5a CP1 auto-pin extractor activates the moment `RoofingModule.equipment_pins` is non-empty.
**Open questions for Daniel:** None on G.5b. Pending for next planning conversation: G.6 plan + soft-gate bidset (likely Taco Bell again for Karpathy single-bidset discipline).

**Next-eligible work:** Phase G.6 — Stages 6-9 geometry/scale/callout extraction wiring.

**Banked discipline lessons (2026-05-09):**
1. **Vault SHA-1 canonical method is `sha1sum` of raw file content on disk, NOT `git hash-object`.** On Windows with `core.autocrlf=true`, `git hash-object` normalizes to LF and computes a different SHA-1 than the file as it exists on disk. Canon SHA-1s are computed from disk bytes (CRLF preserved). Future sessions: verify with `sha1sum backend/core/{vault_file}.py` (also matches Python `hashlib.sha1(open(f,'rb').read()).hexdigest()`).
2. **The G.0 scout report connected two independent findings that don't actually intersect.** "pdfplumber.extract_tables() is the cost ceiling at 2.91s/page" + "PyMuPDF tiling is ready" got read as "tile pdfplumber to win wall-clock." Tiling helps **rasterization-bound** work; Filter 4 is **vector-bound** (PDF text stream + grid-line detection in vector space). pdfplumber doesn't take images; substituting tiles would be slower not faster. Future scout reports: explicitly state which findings can be bridged and which are independent.
3. **Pandas / OCR claim about TracePoint resolved FALSE.** Grep across `tracepoint_port/TracePoint/`: zero pandas imports, zero OCR imports (tesseract/pytesseract/easyocr/paddleocr). The render-to-image path in TracePoint exists only in the geometry engine for scanned-PDF fallback (OpenCV contours), never in dispatch. Memory was conflating pdfplumber's vector table extraction with image-based table extraction. Future planning: don't trust memory of "TracePoint did X" without grep verification.
4. **Pipeline-wide theater audit produces more value than narrow per-CP fact-finds.** Three Explore agents in parallel (pipeline trace, TracePoint comparison, output consumer trace) produced a 10-item theater inventory + cascade analysis that rewrote G.5b/G.6 phase shape. Future phases: when a per-CP fact-find surfaces a fundamental mismatch between plan and reality, expand to pipeline-wide audit before re-planning. Cheaper than a wrong patch.
5. **Theater cuts must include test cascade analysis.** `_extract_project_metadata` cut was BANKED (not shipped) because `test_dispatch.py:408-409 test_building_sf_found` asserts `ctx.project.total_building_sf == 5746.0` after dispatch (currently SKIPPED on missing AEA fixture — but the assertion is the spec). Cutting the implementation while keeping the test silently turns a SKIPPED test into a future-fail. Honest cut requires retiring the test too — separate decision. `detect_firm` cut shipped because cascade was zero (`test_architect_profile.py` tests function directly, not via dispatch).
