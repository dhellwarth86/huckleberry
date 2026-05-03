# ITINERARY.md — Huckleberry Working Memory

**Purpose:** Compressed working memory. The 120-150 line doc that catches a fresh Claude up without reading every gate report. Mutates each handoff. If this file is current, the project state is recoverable in under 5 minutes.

**Update discipline:** Every session that ships work updates this file. The General updates it after ratifying / debriefing. The Developer updates it after a hands-on ship. Canon updates are produced by Claude in chat as complete drop-in files at sign-out — Daniel does not paste snippets.

---

## Section 1 — Last 3 Completed

Most recent ships, 7 lines each. Each entry: phase name, date, branch, what shipped, sacred floor delta, receipt path, key learning.

### Last-1 — Phase G.2 (corpus-wide classifier upgrade) — 2026-05-03

- **Branch:** `phase2-v0.3-G2-classifier-upgrade` head `170fcd7`, pushed
- **Shipped:** Classifier reads `pc.title` alongside `tb_text` + `full_text`; `_PAGE_TYPE_RULES` extended with corpus-validated keywords from G.2 scout. 7 new unit tests + 4-bidset hard gate.
- **Floor delta:** Backend 230 → 237/19/0 (+7 new classifier tests); frontend 23/23 unchanged
- **Receipts:** `backend/G_2_HARD_GATE_REPORT.md` · commit `170fcd7` · hard-gate proof on Bearss/Hampshire/Chipotle/Shoppes
- **Learning:** Filter 1's `pc.title` write was load-bearing input the classifier never read. The corpus scout's discipline-fallback approach was wrong; the keyword-and-title approach was the corpus-validated path. Two full-chain scout cycles (G.0.5-G.1 regex; G.2 fallback) finally located classification's actual lever — `_classify_page_type`'s string corpus.
- **Lesson banked:** Corpus scout text samples are inferred, not verbatim. Always verify keyword presence via `engine.extract_text()` on actual PDFs before committing keywords to rules.

### Last-2 — Recon cascade map + Phase G.1 ratification — 2026-05-03

- **Branch:** `phase2-v0.3-recon-cascade-map` head `cef1ca7`, pushed (built from G.1 head `7318d8b`)
- **Shipped:** (1) G.1 verbally ratified. (2) Recon cascade map — 445-line read-only inventory of every read/write site for major PlanSetContext fields; filter chain trace (1→2→4→3→5 actual execution order). (3) Phase G.2 march orders drafted.
- **Floor delta:** Backend 230/19/0 unchanged; frontend 23/23 unchanged; vault SHA-1s held throughout.
- **Receipts:** `backend/RECON_CASCADE_MAP.md` · commit `cef1ca7`
- **Learning:** The MEP fallback at `dispatch_gate.py:463-466` is the only sheet_map → page_type cascade in code. Phase G.2 scope shrunk from "build new system" to "extend existing fallback."
- **Lesson banked:** Build the map before the patch, every time the fix depends on data flow across files.

### Last-3 — Phase G.1 — 2026-05-01

- **Branch:** `phase2-v0.3-G1-audit-and-regex` head `7318d8b`, pushed
- **Shipped:** Test-floor audit (230/19/0 honest count) · hybrid regex patch at `dispatch_gate.py:57` · Bearss byte-equivalence verified (769/177/31/24) · Silverleaf sheet_map jumped 4→32 mapped pages
- **Floor delta:** Backend 230/19/0 unchanged · frontend 23/23 unchanged
- **Receipts:** `backend/G_1_GATE_REPORT.md` · commit `7318d8b`
- **Learning:** Cascade hypothesis was wrong. Filter 2 reads keywords directly from page text, not sheet_map (except narrow MEP discipline fallback).
- **Lesson banked:** "If A causes B, find the line where A causes B. If you can't find that line, the cascade doesn't exist."

---

## Section 2 — Next 6 Pipeline Steps

Each entry: phase name, dependency, scope summary, sacred-floor target, soft/hard gate, key risk, who-runs-it.

### Next-1 — Phase G.3 (cache layer)

- **Depends on:** G.2 ratified (this phase)
- **Scope:** Cache `extract_text` and `extract_text_blocks` per page in PDFEngine. Consolidate pdfplumber to single open-per-dispatch lifecycle (Filter 4 + Stage 13 share). Reuse PyMuPDF blocks in Stage 13 instead of `pdfplumber.extract_words()`.
- **Floor target:** Backend 237/19/0; cache tests likely add 5-10 (target 242-247)
- **Gate:** Hard gate vs Bearss byte-equivalence (cache must not change behavior) + wall-clock target (meaningful reduction vs current ~8 min)
- **Risk:** Cache invalidation timing. Single open-per-dispatch changes pdfplumber lifecycle — must verify Filter 4 and Stage 13 still see the same data.
- **Run:** General drafts march orders after G.2 ships clean

### Next-2 — Phase G.4 (Filter 4 hoist + Stage 13 retire)

- **Depends on:** G.3
- **Scope:** Two-part. (1) Filter 4 hoist: `pdfplumber.open()` once per dispatch, reused across all SCHEDULE_SHEET pages. Per G.0.8 recon, Filter 4 is 78.7% of dispatch wall-clock on Bearss (240+ pages). (2) Stage 13 retire: replace `pdfplumber.extract_words()` with PyMuPDF equivalent — recon confirmed 5/5 word fields available from PyMuPDF.
- **Floor target:** Backend ≥237; vault SHA-1s held except `dispatch_gate.py` (Filter 4 implementation lives there)
- **Gate:** Hard gate vs Bearss baseline timing — substantial Filter 4 reduction
- **Risk:** pdfplumber and PyMuPDF have different word-coordinate conventions (origin top-left vs bottom-left, units). Pre-scout micro-benchmark needed first to verify equivalent outputs at the field level.
- **Run:** General drafts march orders after G.3 ships clean

### Next-3 — Phase G.5 (render optimization — original Phase G/F1 scope)

- **Depends on:** G.4
- **Scope:** PyMuPDF replacing pdfplumber for rendering; tiling at 200-300 DPI to reduce compute and improve drawing detection. The original Phase G headline. Now last in the chain because page classification (G.2), cache (G.3), and Filter 4 hoist (G.4) must precede — render work is meaningless until we know which pages to tile.
- **Floor target:** Backend ≥240 (new tiling tests); vault SHA-1s held except `pdf_engine.py` and `dispatch_gate.py` (render path lives there)
- **Gate:** Hard gate against re-running 3-bidset benchmark with quadrant scan vs without (compare wall-clock + accuracy)
- **Risk:** New dependencies (PyMuPDF, Pandas if not already present) — first real dep additions since FastAPI in E.1
- **Run:** General drafts G.5.0 design phase first; Claude Code executes G.5.1 build

### Next-4 — Closing hard gate (3-bidset + deferred E.2.2 visual)

- **Depends on:** G.5
- **Scope:** Bundles two deferred hard gates. (1) 3-bidset hard gate (Bearss + Silverleaf + Vine Street) re-run end-to-end against the full Phase F/G chain. (2) Deferred E.2.2 visual hard gate that was rolled into E.2.2 but not exercised on multiple bidsets. Closes Phase F/G chain permanently.
- **Floor target:** All previous floors held + hard gate report PASS
- **Gate:** **Hard gate** — completes the entire Phase F/G chain
- **Risk:** Single-bidset Silverleaf testing throughout the chain may have masked bidset-specific quirks.
- **Run:** Developer session with Daniel manually verifying browser; General writes gate report

### Next-5 — Silverleaf Filter 1 sheet-detection fix

- **Depends on:** G.2 shipped (this phase confirms the classifier lever works; Silverleaf 12/13/38/39 need Filter 1 to detect their sheet numbers first)
- **Scope:** Fix `_find_sheet_on_page` for pages where sheet numbers exist in page text but current strategies (3-5) miss them. Silverleaf pages 12/13/38/39 have sheet numbers (P201, P301, M101, M102) in full text but empty title-block quadrants. Once Filter 1 populates `sheet_number`, existing MEP fallback + new classifier keywords catch them.
- **Floor target:** Backend ≥237 + new tests for sheet detection edge cases
- **Gate:** Soft gate — Silverleaf UNKNOWN count drops from 4 to 0
- **Risk:** Broadening sheet-number detection may false-positive on pages where number-like strings appear in non-title contexts.
- **Run:** General scopes and drafts march orders after G.3/G.4 performance work stabilizes

### Next-6 — Phase G auto-notation product (post-optimization)

- **Depends on:** All G.3-G.5 performance work + closing hard gate
- **Scope:** Three-state annotations + provenance + training loop. The user-facing product phase that builds on the dispatch infrastructure.
- **Floor target:** TBD at design time
- **Gate:** TBD
- **Risk:** This is the product phase — architecture risk is bounded by the preceding infrastructure chain.
- **Run:** General designs; Developer builds

---

## Section 3 — Schedule Pusher / Blocker Tracking

What's blocking what. What's parked. What needs Daniel decision before it can move.

### Active blockers — none

### Parked items (deliberately deferred)

- **Login screen** — security cluster (post-user-testing)
- **Postgres migration** — security cluster
- **CORS lockdown** — security cluster
- **OpenAPI docs hidden in production** — security cluster
- **File upload via API** — security cluster (string path until then)
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

- None active. G.2 shipped; G.3 march orders await General draft after Daniel reviews G.2 ship.

### Discipline reminders standing

- New sessions ALWAYS announce role at start (General or Developer)
- New sessions ALWAYS read PROJECT_CLAUDE.md + PROJECT_ETIQUETTE.md + ITINERARY.md + 3 most recent CHECKLIST handoffs
- Vault rule: 5 trade modules (roofing_module, roofing_vocabulary, glazing_module, glazing_vocabulary, debug_module) — SHA-1 verified at session boundaries. `dispatch_gate.py` is *integration-frozen* but allowed to change in dedicated tuning phases (G.1 and G.2 were such phases).
- Backend sacred floor: 237 passed / 19 skipped / 0 failed
- Frontend sacred floor: 23/23 against `Huckleberry_AI_phase2.v1.0.0.html` (v6.3.5 retired and archived to safe_for_removal at E.2.1)
- Soft gate between every G sub-phase — Daniel reviews before next phase drafts
- Single-bidset Silverleaf only until Phase G.5 ships (3-bidset hard gate is Next-4)
- No CLAUDE.md (retired by Daniel directive 2026-04-29)
- **Mandate 2026-05-01 (cascade discipline):** When a proposed fix depends on cascade behavior, the first scout traces the cascade — not the bug, not the theory, not the corpus. "If A causes B, find the line where A causes B. If you can't find that line, the cascade doesn't exist."
- **Mandate 2026-05-01 (no artifacts without permission):** Claude does not produce downloadable files without explicit Daniel direction. Inline edits to canon files when shipped through normal sign-out flow are produced as complete drop-in files per the chat-handles-canon protocol.
- **Mandate 2026-05-03 (canon protocol):** Claude in chat produces complete updated CHECKLIST.md, ITINERARY.md, PROJECT_CLAUDE.md as deliverable files at sign-out. Daniel does not paste snippets, does not merge text, does not maintain canon.
- **Mandate 2026-05-03 (lane discipline):** When work crosses lanes mid-session, the active role flags it and asks for explicit role switch before proceeding.
- **Mandate 2026-05-03 (keyword verification):** Corpus scout text samples are inferred, not verbatim. Always verify keyword presence via `engine.extract_text()` on actual PDFs before committing keywords to `_PAGE_TYPE_RULES`.
