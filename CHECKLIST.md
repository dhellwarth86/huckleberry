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
| F11 | Phase G.3 — cache layer (21 call sites of extract_text_blocks/extract_text wrapped with `dict[(pdf_path, page_idx), result]` memoization) | _____ | _____ | _____ | _____ |
| F12 | Phase G.4 — Filter 4 hoist (pdfplumber.open() once per dispatch, reused across SCHEDULE_SHEET pages) + Stage 13 pdfplumber retire (replaced with PyMuPDF equivalent) | _____ | _____ | _____ | _____ |
| F13 | Phase G.5 — render optimization (PyMuPDF + Pandas + tiling 200-300 DPI — original Phase G/F1 scope, now last in chain because page classification, cache, and Filter 4 hoist must precede) | _____ | _____ | _____ | _____ |
| F14 | 3-bidset hard gate + deferred E.2.2 visual hard gate (closes Phase F/G chain permanently) | _____ | _____ | _____ | _____ |

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
