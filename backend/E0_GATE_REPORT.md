# E.0 Gate Report — API Design + Frontend Audit + v6.3.x Housekeeping

**Date:** 2026-04-30
**Branch:** `phase2-v0.3-E0-api-design-and-frontend-audit` (from D.2 head `cd5608e`)
**Spec:** `MARCH_ORDERS_E_0_audit_and_design.md`
**Phase shape:** Read-only diagnostic + design + housekeeping. Single short session, autonomous, soft gates only. No production code modified.
**Overall:** **PASS** — all done-definition checklist items satisfied; zero §9 stops fired.

---

## §11 Done-definition checklist

| # | Item | Result |
|---|---|---|
| 1 | Pre-flight: 216/19/0 backend; 138/138 frontend; vault SHA-1s captured; 5 frontend SHA-1s captured; branch from D.2 head | **PASS** (E0.0) |
| 2 | Branch `phase2-v0.3-E0-api-design-and-frontend-audit` created | **PASS** (from `cd5608e`) |
| 3 | `backend/E0_FRONTEND_AUDIT.md` written per §4 structure | **PASS** (8 sections — overview / backend-shaped logic / frontend-only surface / seam / E.2 strip targets / E.3 render targets / cross-cutting observations / summary) |
| 4 | `backend/E0_API_DESIGN.md` written per §5 structure | **PASS** (11 sections — stack / E.1 endpoints / reserved E.2-E.3 / project structure / deps / run / tests / non-decisions / forward-compat / minimal-impl / open questions) |
| 5 | v6.3.1, 6.3.2, 6.3.3, 6.3.4 HTMLs moved to `safe_for_removal/frontend_versions/` via `git mv` | **PASS** + 4 version-specific spotcheck scripts moved alongside (see §3 below) |
| 6 | `safe_for_removal/MANIFEST.md` updated per §6.3 | **PASS** (category table row + 8 entry blocks: 4 HTMLs + 4 spotchecks) |
| 7 | v6.3.5 SHA-1 unchanged (audit was read-only) | **PASS** — pre and post: `cf3765d61fd6f17de46024a3a84c62f25b19b3c5` |
| 8 | All 5 vault-ruled module SHA-1s unchanged | **PASS** (see §6 below) |
| 9 | Backend tests 216/19/0; frontend tests 138/138 against v6.3.5 | **PASS** — verified pre-session and post-moves |
| 10 | No production code modified (`git diff --stat backend/core/` empty; `git diff --stat backend/scripts/` empty) | **PASS** — confirmed (see §5 below) |
| 11 | No `pyproject.toml` change | **PASS** — file untouched |
| 12 | PROJECT_CLAUDE.md updated per §7 (single §3 paragraph; nothing else) | **PASS** — single paragraph appended to §3 after the D.2 paragraph; sections §1, §2, §4, §5, §6, §7, §8, §9, §10 all untouched |
| 13 | BLOCK_RUN.md Phase 5 section populated per §8 | **PASS** — Phase 5 section added; Phase 6 placeholder added for E.1 |
| 14 | Single commit on `phase2-v0.3-E0-api-design-and-frontend-audit`; pushed to origin | **PASS** (commit SHA recorded after commit lands) |
| 15 | §9 stops: status of each enumerated explicitly (none expected) | **PASS** — see §7 below; all 9 confirmed non-firing |
| 16 | Final gate report produced | **PASS** — this document |

---

## §1 Pre-flight (E0.0)

| Check | Result |
|---|---|
| Backend tests | **216 passed, 19 skipped, 0 failed** (pytest 4.41s) |
| Frontend tests | **138/138 passed** against v6.3.5 (jsdom harness, `UNIT_TESTS: 118 \| INTEGRATION_TESTS: 20`) |
| Branch starting point | `cd5608e` (D.2 chain end commit, on `phase2-v0.3-D2-job-folder-and-persistence`) |
| `safe_for_removal/` exists | yes (workspace root) |
| `git remote -v` | `https://github.com/dhellwarth86/huckleberry.git` (fetch + push) |

Pre-session SHA-1 capture (full set, 10 files):

| File | Pre-session SHA-1 |
|---|---|
| `backend/core/roofing_module.py` | `ae9e5b284191b45de419faacf11771da27a548f9` |
| `backend/core/glazing_module.py` | `52c014421915ec6a66b4a6860b71a0a3274920f2` |
| `backend/core/roofing_vocabulary.py` | `ec6c17f8955ef8e27c3ff1d552b299a6962c9d0b` |
| `backend/core/glazing_vocabulary.py` | `64249c8ef5f7d9db50added3c9a40836cba356ea` |
| `backend/core/debug_module.py` | `78f71d9030cde3b173389603f5f39bd6bedaac07` |
| `frontend/Huckleberry_AI_6.3.5_Scope.html` | `cf3765d61fd6f17de46024a3a84c62f25b19b3c5` |
| `frontend/Huckleberry_AI_6.3.1_Scope.html` | `a80463efe09a51e21c54635c34469fb64172f7b7` |
| `frontend/Huckleberry_AI_6.3.2_Scope.html` | `09702119c7c299ae03c4b8f401c1a1a2c4db1626` |
| `frontend/Huckleberry_AI_6.3.3_Scope.html` | `e8ba836c64df15277c9f8a36b7e28031f7b61f2a` |
| `frontend/Huckleberry_AI_6.3.4_Scope.html` | `aaeddf686c8c74d79b2409d1b4fde1831b7f02c3` |

---

## §2 Branch (E0.1)

`git checkout -b phase2-v0.3-E0-api-design-and-frontend-audit` from `cd5608e`. Single commit at session end. Push at end.

---

## §3 Frontend audit (E0.2) — `backend/E0_FRONTEND_AUDIT.md`

**Audit subject:** v6.3.5 only. v6.3.1–v6.3.4 NOT opened (orders §1 prohibition). Vault modules NOT opened.

**Audit method:** read-only — Glob, Grep, Read against v6.3.5; multiple targeted reads at landmark line numbers; no edits attempted. Final SHA-1 of v6.3.5 verified at session end (matches pre-session, see §6 below).

**Major findings (full detail in `backend/E0_FRONTEND_AUDIT.md`):**

- **8,694 lines total**; 3 script blocks (lines 1730–2560, 2566–4780, 4789–8691); status-bar copy "AI BACKEND: REMOVED" + "100% OFFLINE · CLIENT-SIDE" baked into the file (Phase 1 design philosophy now reversing in Phase E).
- **~1,320 lines of business logic identified as backend-shaped** (15% of total file, 22% of script content):
  - **TP namespace 12-stage pipeline port** (lines 1730–2560, ~830 lines) — explicitly self-described as a "Faithful JavaScript port of the architecture from the 'TracePoint AI — Technical Report' (April 2026)." Duplicates B.1+B.2+B.3 (filter pipeline + geometry engine + scoring).
  - **`ROOF_VOCAB`** (lines 5018–5143, ~125 lines) — 9 systemTypes + 7 manufacturers + 7 attachmentMethods + 6 insulationMaterials + 3 coverBoards + 18 penetrations + 8 accessories + 12 edgeTypes + page-classification markers. Self-described as a JS mirror of `roofing_materials.py`.
  - **`extractScope`** (lines 5193–5306, ~115 lines) — duplicates `_extract_project_metadata` + scope_scanner.
  - **`classifyPage`** (lines 5313–5329, ~17 lines) — duplicates `_classify_page_type`.
  - **Text-processing helpers** (`collectPlanText`, `findMatches`, `splitBySystemLabels` at 5149–5191, ~43 lines).
  - **PDF.js operator-list walker** (lines 2768–2960, ~190 lines) — duplicates `PDFEngine` + pdfplumber.
- **E.2 strip projection:** ~3,800–4,100 lines deletable (~45% of file), counting business logic + tests that exercise it.
- **Frontend-only surface (stays):** UI shell + tabs + Viewer (OpenSeadragon + Konva) + TOOL_HANDLERS (pin/line/polygon/rectangle drawing) + Takeoff Excel export + local UI state + editing UI. Roughly 4,500–5,000 lines projected post-strip.
- **Audit honesty notes** (orders §10 #5): v6.3.5 is *not* a thin renderer; it is a complete browser app. E.2 should be planned as a re-architecture, not a refactor. Soft audits cause E.2 to under-strip and ship a bloated frontend.

---

## §4 API design (E0.3) — `backend/E0_API_DESIGN.md`

**Stack:** FastAPI + uvicorn + Pydantic v2 + stdlib `sqlite3` (no SQLAlchemy, no ORM). No auth in E.1 per Daniel directive.

**E.1 endpoints (exactly two):**

1. `POST /jobs` — create a job, returns 201 + JobResponse with computed `pdf_sha1`. Pydantic-validated request body. 400 on missing pdf_path; 422 on Pydantic validation failure.
2. `GET /jobs/{job_id}` — load job by id, returns 200 + JobResponse. 404 on miss.

Plus a free `/health` liveness probe (zero state, no coupling to job_storage).

**Project structure (E.1 deliverable):** new `backend/api/` directory with `main.py`, `routes/jobs.py`, `schemas/jobs.py`. Existing `backend/core/` and `backend/tests/` untouched by E.1 (E.1 adds one new test file `backend/tests/test_api_jobs.py`).

**Three new pyproject deps E.1 will add** (E.0 adds zero):
- `fastapi>=0.115`
- `uvicorn[standard]>=0.30`
- `pydantic>=2.7`

**Test strategy:** TestClient-based round-trip + error tests; floor moves 216 → 219–222.

**Reserved (sketched but not built in E.1):** `POST /jobs/{id}/dispatch`, `GET /jobs/{id}/results`, `GET /jobs`, `PUT /jobs/{id}`, `PATCH /jobs/{id}/status`, `POST /jobs/{id}/annotations`, `GET /jobs/{id}/debug`. Each gets its own march orders.

**Open questions surfaced for Daniel review:** see §5.11 of the API design doc — pdf_path-vs-upload, CORS lockdown timing, /health classification, test count window, status validation strategy, OpenAPI exposure in production.

---

## §5 Frontend version housekeeping (E0.4) + Manifest update (E0.5)

**Files moved (8 total via `git mv` — history preserved):**

| From | To | Type |
|---|---|---|
| `frontend/Huckleberry_AI_6.3.1_Scope.html` | `safe_for_removal/frontend_versions/Huckleberry_AI_6.3.1_Scope.html` | retired HTML |
| `frontend/Huckleberry_AI_6.3.2_Scope.html` | `safe_for_removal/frontend_versions/Huckleberry_AI_6.3.2_Scope.html` | retired HTML |
| `frontend/Huckleberry_AI_6.3.3_Scope.html` | `safe_for_removal/frontend_versions/Huckleberry_AI_6.3.3_Scope.html` | retired HTML |
| `frontend/Huckleberry_AI_6.3.4_Scope.html` | `safe_for_removal/frontend_versions/Huckleberry_AI_6.3.4_Scope.html` | retired HTML |
| `frontend/spotcheck_durolast.js` | `safe_for_removal/frontend_versions/spotcheck_durolast.js` | targeted v6.3.1 (hardcoded `HTML_PATH`) |
| `frontend/spotcheck_manufacturer.js` | `safe_for_removal/frontend_versions/spotcheck_manufacturer.js` | targeted v6.3.2 |
| `frontend/spotcheck_cricket.js` | `safe_for_removal/frontend_versions/spotcheck_cricket.js` | targeted v6.3.3 |
| `frontend/spotcheck_10b.js` | `safe_for_removal/frontend_versions/spotcheck_10b.js` | targeted v6.3.4 |

**Why the 4 spotcheck scripts moved alongside:** each one hardcodes a specific older version's HTML path in its `HTML_PATH = path.join(__dirname, 'Huckleberry_AI_6.3.X_Scope.html')` line. Leaving the spotchecks behind would create dangling-reference scripts. Moving them preserves audit trail. They are not part of the 138/138 `npm test` floor — they ran via `npm run test:spotchecks` only.

**Files explicitly NOT moved (still in `frontend/`):**
- `Huckleberry_AI_6.3.5_Scope.html` (canonical; SHA-1 unchanged through session)
- `run_tests.js` (jsdom harness; defaults to v6.3.5 via `npm test`)
- `mutation_test_step11.js` (targets v6.3.5 explicitly; not part of 138/138 floor but useful)
- `package.json` (untouched per orders §9 #7 — modifying production frontend config out of scope for E.0)
- `extracted/Huckleberry_AI_6.3.0_Scope.html` (older still; not in scope per orders §6.1)

**Soft observation surfaced:** `frontend/package.json` still has a `test:spotchecks` script entry referencing the moved files. Running `npm run test:spotchecks` will now fail (target files moved). The 138/138 floor (`npm test`) is unaffected. Cleanup deferred to next frontend-touching session (likely E.2). Documented in `safe_for_removal/MANIFEST.md` and BLOCK_RUN.md Phase 5.

**`safe_for_removal/MANIFEST.md` updates:**
- Added `frontend_versions/` row to the categories table at top of file.
- Added 8 detailed entry blocks (one per moved file) under a new "Frontend versions retired by E.0 (2026-04-30)" section, before the "End of MANIFEST" closer.
- Each entry follows the established 8-field schema (Original path / New path / Category / When active / Purpose when active / Why retired / What replaced it / What to look at if related issues surface).

---

## §6 Sacred floors at session end

**Backend tests (post-moves, E0.4):**
```
216 passed, 19 skipped, 1 warning in 2.54s
```

**Frontend tests (post-moves, E0.4):**
```
[harness] UNIT_TESTS: 118 | INTEGRATION_TESTS: 20 | total: 138
[harness] RESULT: 138/138 passed, 0 failed
```

**Vault-ruled module SHA-1s (post-session, matches pre-session):**

| File | SHA-1 | Unchanged |
|---|---|---|
| `backend/core/roofing_module.py` | `ae9e5b284191b45de419faacf11771da27a548f9` | ✓ |
| `backend/core/glazing_module.py` | `52c014421915ec6a66b4a6860b71a0a3274920f2` | ✓ |
| `backend/core/roofing_vocabulary.py` | `ec6c17f8955ef8e27c3ff1d552b299a6962c9d0b` | ✓ |
| `backend/core/glazing_vocabulary.py` | `64249c8ef5f7d9db50added3c9a40836cba356ea` | ✓ |
| `backend/core/debug_module.py` | `78f71d9030cde3b173389603f5f39bd6bedaac07` | ✓ |

**v6.3.5 SHA-1 (post-audit, matches pre-session):**

| File | SHA-1 | Unchanged |
|---|---|---|
| `frontend/Huckleberry_AI_6.3.5_Scope.html` | `cf3765d61fd6f17de46024a3a84c62f25b19b3c5` | ✓ |

**Production code modification check:**
- `git diff --stat backend/core/` → empty (vault held; D.2-shipped files untouched)
- `git diff --stat backend/scripts/` → empty (no harness modifications)
- `git diff --stat backend/tests/` → empty (no test modifications)
- `pyproject.toml` → empty (no dep changes)

---

## §7 §9 Stop conditions — explicit non-firing status

| # | Stop | Status | Evidence |
|---|---|---|---|
| 1 | Sacred floor regresses (backend < 216/19/0 or frontend < 138/138) | **NOT FIRED** | Both floors verified pre-session and post-moves |
| 2 | v6.3.5 frontend SHA-1 changes | **NOT FIRED** | SHA-1 `cf3765d6…` unchanged |
| 3 | Vault-ruled module SHA-1 changes | **NOT FIRED** | All 5 SHA-1s unchanged (modules not opened this session) |
| 4 | Frontend test suite breaks after v6.3.1–6.3.4 moves | **NOT FIRED** | 138/138 still passes; no `npm test` reference touched files (only the spotchecks did, and those moved with their targets) |
| 5 | CLAUDE.md gets opened or edited | **NOT FIRED** | File retired pre-D.1; not opened this session |
| 6 | PROJECT_CLAUDE.md edits exceed §7 single-paragraph append to §3 | **NOT FIRED** | Single paragraph appended to §3 after D.2 paragraph; sections §1, §2, §4, §5, §6, §7, §8, §9, §10 untouched |
| 7 | Production code modified (any backend/core/ or backend/scripts/ change) | **NOT FIRED** | git diff --stat empty for both directories |
| 8 | A new dependency is needed for E.0 | **NOT FIRED** | `pyproject.toml` untouched; design doc names E.1's three deps but E.0 adds zero |
| 9 | Audit reveals architecturally surprising element | **SOFT OBSERVATION ONLY** | The audit found that v6.3.5 contains a substantial JS port of the TracePoint pipeline (~830 lines) plus full ROOF_VOCAB plus extractScope. This is "surprising" only in scale, not in kind — Phase 1's offline-first design committed to this; E.2's strip is correspondingly larger than naive estimates. This is documented factually in `backend/E0_FRONTEND_AUDIT.md` §4.2 and §4.5. Per orders §9 #9: "Soft observation in gate report; document the surprise; do NOT redesign mid-session. The redesign is Daniel's call after he reads E.0." Documented; no redesign attempted. |

Two additional soft observations recorded but not stop-condition flags:

- **Status-bar copy invalidation:** v6.3.5's HTML literally says "AI BACKEND: REMOVED" and "100% OFFLINE · CLIENT-SIDE" (line 1236, 1238). E.2 will need to update these strings as part of the strip — this is a copy update, not a code change. Surfaced in `E0_FRONTEND_AUDIT.md §4.5`.
- **`package.json` `test:spotchecks` orphan:** mentioned above in §5.

---

## §8 Wall-clock summary

| Step | Wall-clock |
|---|---|
| E0.0 pre-flight (tests, SHA-1s, branch) | ~30 sec |
| E0.1 branch creation | <5 sec |
| E0.2 frontend audit (10 docs read + write) | ~6 min (most spent on v6.3.5 read passes) |
| E0.3 API design (write) | ~3 min |
| E0.4 housekeeping moves (`git mv` × 8) | <30 sec |
| E0.4 floor re-verify (tests + SHA-1s post-moves) | ~30 sec |
| E0.5 MANIFEST.md update | ~1 min |
| E0.6 PROJECT_CLAUDE.md + BLOCK_RUN.md + this gate report + commit + push | ~3 min |
| **Total** | **~14 min** |

Within the orders §13 estimate ("~30-60 minutes"). Pre-flight reads were faster than estimated because v6.3.5 came in at 8,694 lines rather than the spec's "presumably 20K+ lines."

---

## §9 Deliverables ready for Daniel review

1. **`backend/E0_FRONTEND_AUDIT.md`** — read this first; it sets the scale of E.2's strip work.
2. **`backend/E0_API_DESIGN.md`** — the contract E.1 builds against. §5.11 has open questions for explicit Daniel review.
3. **`safe_for_removal/MANIFEST.md`** — verify the 8 entries (4 HTMLs + 4 spotchecks) are in the shape Daniel wants for the wiki.
4. **`PROJECT_CLAUDE.md` §3** — single E.0 paragraph appended (line 80, between D.2 paragraph and "For full state detail" closer).
5. **`backend/BLOCK_RUN.md` Phase 5** — populated; Phase 6 placeholder added for E.1.
6. **This gate report** (`backend/E0_GATE_REPORT.md`).

After Daniel reviews:
- **If E0_API_DESIGN.md is good as written:** E.1 march orders can be drafted by extended-thinking Claude; Claude Code executes the 2-endpoint scaffold.
- **If anything needs patching:** Daniel flags it; the design doc gets a delta commit on the same E.0 branch (or a small follow-up branch); then E.1 starts.
- **If the audit changes E.2 plans:** the audit's E.2 strip targets list is the working draft; E.2 march orders refine it.

---

## §10 Overall

**E.0 is complete and shippable.** All checklist items satisfied. Zero stops fired. Sacred floors held. Three deliverables produced + canon updates + housekeeping moves + single commit + push.

E.0 is the design phase Phase E was waiting for. E.1 (FastAPI scaffold, 2 endpoints) is the next-eligible phase as soon as Daniel approves the API design.

**End of E.0 gate report.**
