# ITINERARY.md — Huckleberry Working Memory

**Purpose:** Compressed working memory. The 120-150 line doc that catches a fresh Claude up without reading every gate report. Mutates each handoff. If this file is current, the project state is recoverable in under 5 minutes.

**Update discipline:** Every session that ships work updates this file. The General updates it after ratifying / debriefing. The Developer updates it after a hands-on ship. Canon updates are produced by Claude in chat as complete drop-in files at sign-out — Daniel does not paste snippets.

---

## Section 1 — Last 3 Completed

Most recent ships, 7 lines each. Each entry: phase name, date, branch, what shipped, sacred floor delta, receipt path, key learning.

### Last-1 — Phase G.4 (scope tab as backend-DB-frontend cycle + backend file storage + dropzone retire) — 2026-05-07

- **Branch:** `phase2-v0.3-G4-scope-fix-and-backend-storage` HEAD `a1d8ded` + canon commit pending; 7 commits when canon lands; awaiting push approval
- **Shipped:** Scope tab as full backend-DB-frontend cycle (CP1 + CP1.1 polish + CP1.2 flatten bridge), backend file upload + storage + GET /pdf endpoint (CP2), single upload point with JSON path-string + client-only dropzone render path both retired (CP3), PROJECT_CLAUDE.md cleanup with 4 edits including new misconception entry on `ctx.project_scope` as canonical scope source (CP4). Two new SQLite tables: `job_project_scope`, `scope_systems`. Six new endpoints under `/jobs/{id}/scope/*` + multipart `POST /jobs/upload` + `GET /jobs/{id}/pdf`. Frontend rewired for render+relay with localStorage rehydrate of `currentJobId` for refresh-survival of scope state. Baseline items 1/2/3 moved from NOT MET to MET.
- **Floor delta:** Backend 242 → 255/19/0 (+13 net: +9 G.4 scope + 7 multipart − 3 retired JSON-path); frontend 23 → 28 (+5 SCOPE_API_TESTS net after CP3 migration). Vault SHA-1s held identical to Step 0c capture across all 7 vault/integration-frozen files.
- **Receipts:** `backend/G_4_GATE_REPORT.md` · commits `8f1de64` → `a1d8ded` · empirical hard gate 11/11 CP MET via Daniel-driven Silverleaf (manual-entry path; `system_confidence=0.0`) + Taco Bell (auto-detect path; `tpo @ 0.95`, evidence "spec 07 54 23 → TPO Membrane Roofing; Johns Manville (multi-system); Tremco (multi-system)")
- **Learning:** The original chat-Claude G.4 march orders prescribed a frontend-only literal fix that surfaced per-page `_scope` noise. Daniel rejected mid-execution and locked the architectural rule that drives everything since: **frontend = window only, backend = source of truth, every user edit is a database mutation, refresh-the-browser rehydrates everything from the database, "migrate later" is the failure mode.** The plan was rewritten to the architecturally-correct backend-DB-driven approach before any code shipped. Future planning conversations run new orders through this rule before approval.
- **Lesson banked:** `_resolve_scope_system` confidence is binary, not continuous — emits 0.0 or 0.7+, no values in 0.0–0.7 band. Lowering `_AUTO_PREPOPULATE_THRESHOLD` is not a useful knob; the real lever is widening the evidence sources the function votes on (vault-locked, future tuning phase). RoofingModule output is fully persisted + shipped via API but unrendered by the frontend — matches baseline items 5+6 deferral; the `scope_systems` CRUD pattern shipped in CP1 is the template the future annotation-persistence phase reuses.

### Last-2 — Phase G.3 (single-pass-per-page extraction) — 2026-05-03

- **Branch:** `phase2-v0.3-G3-single-pass-extraction` head `e51c785` (code+tests+report), canon commit + push pending
- **Shipped:** PDFEngine cache + Filter 4 pdfplumber hoist + Stage 13 PyMuPDF reuse. `extract_text` and `extract_text_blocks` now keyed `(id(doc), page_num, method)`; cache purged on `engine.close(doc)`. Filter 4 opens pdfplumber once per dispatch (was: per SCHEDULE page). Stage 13 trade-module wiring replaces `pdf_page.extract_words()` with cached PyMuPDF blocks. F12 (Phase G.4 scope) absorbed into G.3 — same branch, same commit. 5 new cache unit tests.
- **Floor delta:** Backend 237 → 242/19/0 (+5 cache tests); frontend 23/23 unchanged
- **Receipts:** `backend/G_3_GATE_REPORT.md` · commit `e51c785` · Chipotle Tarpon wall-clock 58.72s → 50.05s warm (−14.8%)
- **Learning:** TracePoint paper §2.1 architecture restored — Layer 1 (PyMuPDF) extracts once per page, Layers 2-4 consume cache. Was: 5 sites × extract_text + 10 sites × extract_text_blocks per page (up to 195 + 390 calls per dispatch on 39-page Chipotle); now: 39 + 39 max. Filter 4 pdfplumber lifecycle hoisted from per-SCHEDULE-page to per-dispatch. Stage 13's `pdf_page.extract_words()` retired in favor of cached PyMuPDF blocks (free reuse — Filters 1/2/4 already extracted).
- **Lesson banked:** A test that passes for the wrong reason is worse than a test that fails. Cache separation tests passed pre-implementation because un-cached calls naturally return new objects each time — accidental property, unproven spec. Each separation test must also assert repeat-call identity on at least one side, so absence of cache fails the test. The ported pipeline accumulated an "extract again to be safe" pattern that the original TracePoint architecture explicitly forbade. Look for similar shapes elsewhere — anywhere the same source data is fetched twice in one logical pass is a candidate for cache.

### Last-3 — Phase G.2 (corpus-wide classifier upgrade) — 2026-05-03

- **Branch:** `phase2-v0.3-G2-classifier-upgrade` head `170fcd7`, pushed
- **Shipped:** Classifier reads `pc.title` alongside `tb_text` + `full_text`; `_PAGE_TYPE_RULES` extended with corpus-validated keywords from G.2 scout. 7 new unit tests + 4-bidset hard gate.
- **Floor delta:** Backend 230 → 237/19/0 (+7 new classifier tests); frontend 23/23 unchanged
- **Receipts:** `backend/G_2_HARD_GATE_REPORT.md` · commit `170fcd7` · hard-gate proof on Bearss/Hampshire/Chipotle/Shoppes
- **Learning:** Filter 1's `pc.title` write was load-bearing input the classifier never read. The corpus scout's discipline-fallback approach was wrong; the keyword-and-title approach was the corpus-validated path. Two full-chain scout cycles (G.0.5-G.1 regex; G.2 fallback) finally located classification's actual lever — `_classify_page_type`'s string corpus.
- **Lesson banked:** Corpus scout text samples are inferred, not verbatim. Always verify keyword presence via `engine.extract_text()` on actual PDFs before committing keywords to rules.

---

## Section 2 — Next 6 Pipeline Steps

Each entry: phase name, dependency, scope summary, sacred-floor target, soft/hard gate, key risk, who-runs-it.

### Next-1 — G.5 priority pick (Daniel's call) — annotation persistence OR render optimization

After G.4 ships, **next-eligible work is awaiting Daniel's priority call between two candidates.** Order doesn't bind; both are queued.

**Candidate A — Annotation persistence (baseline items 5+6, c.2-territory).** Viewer tools (calibrate / measure / line / polygon / rectangle / pin / exclude) save to a new `annotations` table; takeoff tab reads from `annotations` + `scope_systems` instead of in-memory state; RoofingModule's per-page output (currently fully persisted but unrendered — see banked observation in §3) finally becomes visible. Reuses the `scope_systems` CRUD pattern from G.4 verbatim: new SQLite table + GET/POST/PATCH/DELETE endpoints + frontend renders from API + frontend POSTs every mutation + refresh re-fetches. Architecturally the natural follow-on to G.4 — closes baseline items 5+6 and unblocks items 7+8. Floor target: backend ≥255 + new annotation CRUD tests.

**Candidate B — Render optimization (original Phase G/F1 scope).** PyMuPDF replacing pdfplumber for rendering; tiling at 200-300 DPI to reduce compute and improve drawing detection. Independent of A — targets the render path (image generation for downstream auto-notation), separate from the data-flow path A addresses. Floor target: backend ≥255 + new tiling tests; vault SHA-1s held except `pdf_engine.py` and `dispatch_gate.py` (render path lives there). New deps (PyMuPDF was already added in G.3; Pandas TBD).

**Recommendation:** A first — closes the architectural loop opened by G.4 (data is in the DB but invisible to the user) and continues the pattern Daniel already validated. B is the original Phase G headline but is performance work that doesn't unblock new user-facing baseline items. Daniel's pick.

### Next-2 — Closing hard gate (3-bidset + deferred E.2.2 visual)

- **Depends on:** G.5
- **Scope:** Bundles two deferred hard gates. (1) 3-bidset hard gate (Bearss + Silverleaf + Vine Street) re-run end-to-end against the full Phase F/G chain. (2) Deferred E.2.2 visual hard gate that was rolled into E.2.2 but not exercised on multiple bidsets. Closes Phase F/G chain permanently.
- **Floor target:** All previous floors held + hard gate report PASS
- **Gate:** **Hard gate** — completes the entire Phase F/G chain
- **Risk:** Single-bidset Silverleaf testing throughout the chain may have masked bidset-specific quirks.
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

### Next-5 — TBD pending Phase F design

### Next-6 — TBD pending Phase F design

---

## Section 3 — Schedule Pusher / Blocker Tracking

What's blocking what. What's parked. What needs Daniel decision before it can move.

### Active blockers — none

### Baseline status (from PROJECT_CLAUDE.md "Architectural truth" section)

- **Item 1 (single upload point — backend stores file):** **MET** — G.4 CP2/CP3. Multipart `POST /jobs/upload` writes to `~/.tracepoint/uploads/{job_id}/source.pdf`; JSON path-string variant retired.
- **Item 2 (dispatch fires on backend-stored copy):** **MET** — side effect of item 1.
- **Item 3 (scope tab populates + system pick + retry):** **MET** — G.4 CP1. `scope_systems` table + 5 CRUD endpoints + frontend render+relay; auto-populated when `system_confidence ≥ 0.7`, manual-entry fallback otherwise; PATCH-on-blur edits; refresh-survival via localStorage rehydrate of `currentJobId`.
- **Item 4 (page reclassify writes to DB):** parked — G.5/c.2.
- **Item 5 (viewer tools save to DB):** parked — G.5/c.2 (Candidate A above). RoofingModule's per-page output is fully persisted in `trade_outputs` table + shipped via API but unrendered by the frontend; unblocking item 5 also unblocks the render of that data.
- **Item 6 (takeoff reads from DB):** parked — G.5/c.2 (Candidate A above).
- **Item 7 (Excel export reads from DB):** parked — G.5/c.2.
- **Item 8 (browser refresh persists everything):** **PARTIAL** — G.4 ships scope-tab survival via localStorage `currentJobId` + boot-time `loadScopeFromApi`. Pages tab, viewer state, and annotations rehydration deferred to G.5/c.2. Will be fully MET once item 5+6 land.

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

- None active. G.3 shipped; G.5 march orders (or whichever phase Daniel chooses) await General draft after Daniel reviews G.3 ship.

### Discipline reminders standing

- New sessions ALWAYS announce role at start (General or Developer)
- New sessions ALWAYS read PROJECT_CLAUDE.md + PROJECT_ETIQUETTE.md + ITINERARY.md + 3 most recent CHECKLIST handoffs
- Vault rule: 5 trade modules (roofing_module, roofing_vocabulary, glazing_module, glazing_vocabulary, debug_module) — SHA-1 verified at session boundaries. `dispatch_gate.py` is *integration-frozen* but allowed to change in dedicated tuning phases (G.1 and G.2 were such phases).
- Backend sacred floor: 242 passed / 19 skipped / 0 failed
- Frontend sacred floor: 23/23 against `Huckleberry_AI_phase2.v1.0.0.html` (v6.3.5 retired and archived to safe_for_removal at E.2.1)
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
