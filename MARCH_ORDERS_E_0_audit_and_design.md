# MARCH ORDERS — Phase E.0: API Design + Frontend Audit (READ-ONLY DIAGNOSTIC)

**Date issued:** 2026-04-29
**Issued by:** Daniel (via extended-thinking Claude planning session)
**Executed by:** Claude Code
**Phase shape:** Single short session, autonomous, soft-gates-only, design + audit + housekeeping only — NO production code changes. Single final gate report.
**Read first:** PROJECT_CLAUDE.md, BLOCK_RUN.md, VALIDATION_LEDGER.md, then this document

---

## §0 — What this phase is and is not

### Is

A read-only diagnostic and design phase for Phase E (backend API + frontend strip-and-connect). Three deliverables:

1. **Frontend audit** — what does the current frontend HTML actually do? What ROOF_VOCAB / dispatch logic / business rules live in the browser today? What stays in the browser vs what moves to the backend? Output: structured audit doc.

2. **API design document** — the FastAPI surface for E.1: endpoints, payloads, request/response schemas, error shapes, no-auth-yet stance documented. Output: design doc Daniel reads and approves before E.1 builds.

3. **Frontend version housekeeping** — confirm v6.3.5 is the most complete version. Move v6.3.1, v6.3.2, v6.3.3, v6.3.4 HTML files (and their associated tests / package.json variants) into `safe_for_removal/frontend_versions/`. Manifest entry per the housekeeping pattern.

### Is NOT

- A code-change phase. Zero production code modifications. Even small "while we're in here" edits — no.
- An API build. E.1 builds. E.0 designs.
- A frontend strip. E.2 strips. E.0 surveys.
- A test suite extension. No new tests.
- A vault-ruled module touch.
- A canonical doc edit beyond PROJECT_CLAUDE.md §3 single paragraph note about E.0 audit complete.

---

## §1 — Pre-flight reads (Karpathy step 1)

Full reads, in this order:

1. **PROJECT_CLAUDE.md** — entry point. §3 D.2 paragraph; §7 phase table; §8 Phase E next-eligible.
2. **BLOCK_RUN.md** — Phase 1 / 2 / 2.5 / 3 / 3.5 / 4 entries.
3. **VALIDATION_LEDGER.md** — sacred floors, vault list, Phase E references in §H.
4. **`backend/D2_MASTER_GATE_REPORT.md`** — D.2 chain final state.
5. **`backend/D_HARD_GATE_silverleaf.md`** — D.1 baseline, what dispatch returns end-to-end.
6. **`backend/core/job_storage.py`** — the persistence layer the API will surface.
7. **`backend/core/dispatch_gate.py`** — current `run_dispatch` shape (especially the `job_id` parameter from D.2).
8. **`backend/core/context.py`** — `PlanSetContext` / `PageContext` / `trade_module_outputs` shapes (these are what API responses will serialize).
9. **`backend/core/trade_module.py`** — `TradeModuleOutput` shape.
10. **`Huckleberry_AI_6.3.5_Scope.html`** — read this entire file. It's the audit target. (Vault-treated through Phase D, but E.0 needs to AUDIT it; reading is allowed, modification is NOT.)

That's 10 docs. The frontend HTML is the largest — likely 20K+ lines. Skim in passes:
- First pass: structure (sections, modules, top-level objects)
- Second pass: ROOF_VOCAB and dispatch-shaped logic (anything that looks like business rules)
- Third pass: rendering / annotation / event handlers (what stays in browser)

**Do NOT open:** the four other frontend HTMLs (v6.3.1 through v6.3.4 — they're getting moved to safe_for_removal/, audit only the canonical 6.3.5). Five vault-ruled modules. Anything in `safe_for_removal/`. CLAUDE.md (retired).

---

## §2 — Step E0.0: Pre-flight verification

- Run the full backend suite. Floor: **216 passed, 19 skipped, 0 failed**. Hard stop if not met.
- Run frontend test suite. Capture baseline (likely 138/138 against v6.3.5 per package.json default).
- Capture pre-session SHA-1s for all five vault-ruled modules.
- Capture pre-session SHA-1s for all five frontend HTML files. (v6.3.5 is being audited but NOT modified; v6.3.1–6.3.4 are being moved but NOT modified.)
- Verify branch state: `phase2-v0.3-D2-job-folder-and-persistence` head per BLOCK_RUN.md (D.2 chain end commit).
- Locate workspace root for `safe_for_removal/` directory (created by housekeeping phase 2026-04-29).
- Confirm `git remote -v` shows `https://github.com/dhellwarth86/huckleberry.git`.

---

## §3 — Step E0.1: Branch

```
phase2-v0.3-E0-api-design-and-frontend-audit  (NEW; from D.2 head)
```

Single commit at end of session. Pushed.

---

## §4 — Step E0.2: Frontend audit

Audit `Huckleberry_AI_6.3.5_Scope.html`. Read the entire file. Produce `backend/E0_FRONTEND_AUDIT.md` documenting:

### §4.1 — Structure overview

- Total line count
- Top-level sections / modules (script tags, major component boundaries)
- External dependencies (CDN imports, library references)
- Storage usage (localStorage, sessionStorage, IndexedDB usage if any)
- Test count per package.json (138 expected)

### §4.2 — Backend-shaped logic in the browser

This is the heart of the audit. Identify code that duplicates or pre-runs what backend dispatch / modules already do. Likely candidates:

- ROOF_VOCAB or similar vocabulary tables
- Page classification logic (does the frontend run its own version of `_classify_page_type`?)
- Scope detection (does the frontend run its own scope inference?)
- Annotation tools (manual vs auto)
- PDF rendering / text extraction (any in-browser pdfjs work)
- Geometry / measurement calculations
- Material / quantity computation

For each instance found, document:
- Function/section name
- Approximate line count
- What it does
- Whether backend already does this (yes/no/partial)
- Recommendation: STAY in browser, MOVE to backend (E.2 strip target), or KEEP both (rendering layer that needs to know shape)

### §4.3 — Frontend-only surface that stays

- Annotation tools (pin placement, polygon drawing, line measurement) — manual user actions
- Rendering (PDF display, overlay, zoom/pan)
- Editing UI (form fields, dropdowns, validation that doesn't duplicate backend rules)
- Local UI state (which page is active, which tool is selected, undo/redo)

These are real frontend concerns. They stay even after E.2 strips backend-shaped logic.

### §4.4 — The seam

Where does the frontend currently get its data? Currently: nowhere — it's manual annotation only. After E.2: it gets data from FastAPI endpoints. Document the proposed seam:

- What data does the frontend need to display from backend? (PlanSetContext per-page details, TradeModuleOutput per page, debug section 1/3/6)
- What user actions need to round-trip to backend? (job creation, annotation save, status updates, exports)
- What stays local to the browser? (current view state, draft annotations before save, UI preferences)

### §4.5 — E.2 strip targets

A prioritized list of what E.2 will remove from the frontend:

| Priority | Section/Function | Lines | Why removed | What replaces it |
|---|---|---|---|---|
| 1 | (top item) | ~N | (reason) | (backend endpoint or "shown directly from API response") |
| 2 | ... | ... | ... | ... |

Top-priority items are the ones with biggest line-count savings AND least complexity to replace. Lowest-priority items are the ones that might be hard to fully strip until later phases.

### §4.6 — E.3 render targets

What new rendering does the frontend need to do for backend-supplied data?

- Per-page roofing field display
- Per-page glazing/door/storefront items display
- Debug summary (section 1/3/6) for "is this dispatch healthy?"
- Job sortable list (E.3+ when listing API exists)

For each: rough UX sketch in markdown. Not a wireframe — a description of "this section appears here, shows this data, allows this action."

---

## §5 — Step E0.3: API design document

Produce `backend/E0_API_DESIGN.md`. The contract Phase E.1 builds against.

### §5.1 — Stack decisions

- **Framework:** FastAPI (chosen over Django Ninja per Daniel directive 2026-04-29 — keeps stack lean, preserves stdlib `sqlite3` storage port, Django freebies arrive when needed in same window as Postgres migration)
- **ASGI server:** uvicorn (FastAPI standard)
- **Auth:** none in E.1 (per Daniel directive — auth + security come at user-testing time, separate later phase)
- **Validation:** Pydantic v2 (FastAPI native)
- **DB:** stdlib `sqlite3` via D.2's `job_storage.py` — no ORM
- **CORS:** permissive in dev, locked down later
- **Error format:** standard FastAPI HTTPException with consistent JSON shape

### §5.2 — Endpoints (E.1 scope)

E.1 ships exactly 2 endpoints. Don't pre-build E.2/E.3 endpoints in E.1.

**`POST /jobs`** — create a job
- Request body: `JobCreateRequest` Pydantic schema
  - `name: str` (required)
  - `pdf_path: str` (required — for E.1 this is a file path; later phases handle upload)
  - `gc: str | None`
  - `location_city: str | None`
  - `location_state: str | None`
  - `trade_scope: str = "roofing"`
  - `bid_due_date: str | None` (ISO 8601)
  - `notes: str | None`
- Response: `JobResponse`
  - `id: str` (UUID)
  - `name: str`
  - All other fields from `jobs` row
  - `created_at: str`
  - `updated_at: str`
  - `status: str` ("draft")
- HTTP status: 201 Created
- Errors: 400 if name missing or pdf_path invalid, 500 on storage failure

**`GET /jobs/{job_id}`** — load a job
- Response: `JobResponse` (same as POST response)
- HTTP status: 200 OK
- Errors: 404 if job_id not found

### §5.3 — Endpoints reserved for E.2/E.3 (NOT built in E.1)

Document but don't build:

- `POST /jobs/{job_id}/dispatch` — trigger run_dispatch on a job
- `GET /jobs/{job_id}/results` — fetch dispatch_results + trade_outputs
- `GET /jobs` — list jobs with sort/filter
- `PUT /jobs/{job_id}` — update job metadata
- `PATCH /jobs/{job_id}/status` — status transition
- `POST /jobs/{job_id}/annotations` — save user annotations (E.3)
- `GET /jobs/{job_id}/debug` — fetch debug module output

These get drafted into E.2 or E.3 march orders, not E.1. Their request/response shapes can be sketched in this design doc as forward-compat reference.

### §5.4 — Project structure

Where the API code lives:

```
backend/
├── api/
│   ├── __init__.py        # NEW — package marker
│   ├── main.py            # NEW — FastAPI app + uvicorn entry
│   ├── routes/
│   │   ├── __init__.py    # NEW
│   │   └── jobs.py        # NEW — /jobs endpoints
│   └── schemas/
│       ├── __init__.py    # NEW
│       └── jobs.py        # NEW — Pydantic models
├── core/                  # UNCHANGED — vault-ruled + others
└── tests/                 # UNCHANGED in E.1; E.2 may add API tests
```

The `api/` directory is new top-level. No existing files moved. No existing tests broken.

### §5.5 — Dependencies

E.1 adds three new pyproject.toml dependencies:

- `fastapi>=0.115`
- `uvicorn[standard]>=0.30`
- `pydantic>=2.7`

That's it. No SQLAlchemy. No JWT. No CORS middleware libs (FastAPI built-in).

E.0 itself adds NO dependencies. It just documents what E.1 will add.

### §5.6 — Run instructions

For E.1 deliverable. Document the command:

```
cd backend
uvicorn api.main:app --reload --port 8000
```

OpenAPI docs auto-generated at `http://localhost:8000/docs`.

### §5.7 — Test strategy for E.1

- Create a new file `backend/tests/test_api_jobs.py` (E.1 adds this — E.0 just designs)
- Use FastAPI's `TestClient` for in-process requests
- Round-trip test: POST a job, GET the job, assert fields match
- Error test: GET non-existent job, assert 404
- Integration with D.2 storage: verify job persists to SQLite, can be loaded by `job_storage.get_job` directly
- Test count after E.1: 216 → 220 (or thereabouts, depending on actual test breakdown)

### §5.8 — What E.0 does NOT decide

- Auth implementation (deferred)
- Frontend → backend connection mechanism (E.2)
- File upload handling (later phase)
- Pagination strategy for list endpoints (E.2 or E.3)
- Webhook / event system (much later)
- Rate limiting (later)
- Multi-tenant isolation (later)

These get decided when their phase arrives. Documenting absences.

---

## §6 — Step E0.4: Frontend version housekeeping

Move retired frontend HTML files into `safe_for_removal/`.

### §6.1 — Identify files to move

Likely retire candidates:
- `Huckleberry_AI_6.3.1_Scope.html` (107 tests per PROJECT_CLAUDE.md historical reference)
- `Huckleberry_AI_6.3.2_Scope.html`
- `Huckleberry_AI_6.3.3_Scope.html`
- `Huckleberry_AI_6.3.4_Scope.html`

Keep: `Huckleberry_AI_6.3.5_Scope.html` (canonical going forward)

Also check:
- Any `package.json` variants tied to specific versions (likely 1 file)
- Any `node_modules` / test fixture files specific to old versions
- Any `*.test.js` / `*.spec.js` files specific to old versions

If a test file references v6.3.5 and the test passes, it stays. If a test file references v6.3.1 and is no longer relevant, move it.

### §6.2 — Move pattern

Same as housekeeping phase 2026-04-29:

```bash
git mv Huckleberry_AI_6.3.1_Scope.html safe_for_removal/frontend_versions/
# repeat for 6.3.2, 6.3.3, 6.3.4
```

### §6.3 — Update MANIFEST.md

Append a new section in `safe_for_removal/MANIFEST.md`:

```markdown
## Frontend versions retired by E.0 (2026-04-29)

Per Daniel directive 2026-04-29: v6.3.5 confirmed canonical going forward; v6.3.1 through v6.3.4 retired.

### Huckleberry_AI_6.3.1_Scope.html
**Original path:** `Huckleberry_AI_6.3.1_Scope.html`
**New path:** `safe_for_removal/frontend_versions/Huckleberry_AI_6.3.1_Scope.html`
**Category:** retired_frontend_versions
**When active:** before 2026-04-29
**Purpose when active:** Phase 1 frontend HTML, ~107 tests
**Why retired:** Superseded by v6.3.5 (138 tests, more complete)
**What replaced it:** Huckleberry_AI_6.3.5_Scope.html
**What to look at if related issues surface:** v6.3.5 audit at backend/E0_FRONTEND_AUDIT.md; sacred-files list in VALIDATION_LEDGER.md §A

---

(Repeat for v6.3.2, v6.3.3, v6.3.4)
```

### §6.4 — Sacred floor check after moves

After moves:
- Run backend tests: 216/19/0 still passing.
- Run frontend test suite: 138/138 still passing against v6.3.5 (the only HTML left in workspace root).
- Confirm v6.3.5 SHA-1 unchanged (the move only touched 6.3.1–6.3.4, not 6.3.5).

If anything regresses, the test runner is referencing a moved file — restore it and surface as soft observation.

---

## §7 — Step E0.5: PROJECT_CLAUDE.md update

Single surgical edit. §3 only.

Append one paragraph to §3 (before the "For full state detail" closer):

```
**Phase E.0 audit + design complete (2026-04-29):** Frontend audit at `backend/E0_FRONTEND_AUDIT.md` documents v6.3.5 structure, backend-shaped logic in browser (E.2 strip targets), frontend-only surface that stays, and the API seam. API design at `backend/E0_API_DESIGN.md` specifies FastAPI stack, two E.1 endpoints (POST /jobs and GET /jobs/{id}), no-auth-in-E.1 stance, project structure under `backend/api/`, and the three new dependencies E.1 adds. v6.3.1 through v6.3.4 frontend HTMLs moved to `safe_for_removal/frontend_versions/`; v6.3.5 confirmed canonical. Branch: `phase2-v0.3-E0-api-design-and-frontend-audit`. E.1 (FastAPI scaffold + first endpoints) ready to draft after Daniel reviews E.0 deliverables.
```

Do NOT modify §1, §2, §4, §5, §6, §7, §8, §9, §10. §7 phase table update happens in E.1's run, not E.0.

---

## §8 — Step E0.6: BLOCK_RUN.md update

Append Phase 5 section to BLOCK_RUN.md:

```markdown
## Phase 5: E.0 — API Design + Frontend Audit (2026-04-29)

**Branch:** `phase2-v0.3-E0-api-design-and-frontend-audit` (from D.2 head)
**Trigger:** Daniel directive 2026-04-29 — Phase E next-eligible after D.2 chain ship; E broken into 4 sub-phases (E.0 design + audit, E.1 FastAPI scaffold, E.2 frontend strip, E.3 render + edit surface); E.0 is read-only, no code changes.
**Scope discipline:** Single short session, audit + design + housekeeping only, no production code, vault rule active, frontend strip deferred to E.2.

### Files created
- `backend/E0_FRONTEND_AUDIT.md` — 6.3.5 structural audit + E.2 strip targets + E.3 render targets
- `backend/E0_API_DESIGN.md` — FastAPI design contract for E.1
- `backend/E0_GATE_REPORT.md` — E.0 gate report

### Files moved
- `Huckleberry_AI_6.3.1_Scope.html` → `safe_for_removal/frontend_versions/`
- `Huckleberry_AI_6.3.2_Scope.html` → `safe_for_removal/frontend_versions/`
- `Huckleberry_AI_6.3.3_Scope.html` → `safe_for_removal/frontend_versions/`
- `Huckleberry_AI_6.3.4_Scope.html` → `safe_for_removal/frontend_versions/`

### Files modified
- `safe_for_removal/MANIFEST.md` — appended frontend versions section
- `PROJECT_CLAUDE.md` — single §3 paragraph append (E.0 complete note)

### Files deleted
None this session.

### Commits
(populate at session end)

### Pushes
(populate at session end)

### Dependency / config changes
None. (E.1 will add fastapi, uvicorn, pydantic. E.0 only documents.)

### Vault-ruled files touched
None. SHA-1 verification at session end.

### Frontend touched
- v6.3.5: read-only audit (SHA-1 unchanged at session end)
- v6.3.1, 6.3.2, 6.3.3, 6.3.4: moved (`git mv`); SHA-1 of file content unchanged

### Sacred floor at session end
Backend 216/19/0; frontend 138/138 against v6.3.5.
```

---

## §9 — Stop conditions

Stop, report, wait for Daniel if any fire:

1. **Sacred floor regresses.** Backend below 216/19/0 or frontend below 138/138. Hard stop.
2. **v6.3.5 frontend SHA-1 changes.** It's audit-only; modification is a stop.
3. **Vault-ruled module SHA-1 changes.** Should be impossible — not opened this session.
4. **Frontend test suite breaks** after the v6.3.1–6.3.4 moves. Means a test was referencing one of the moved files. Restore and investigate.
5. **CLAUDE.md gets opened or edited.** Retired.
6. **PROJECT_CLAUDE.md edits exceed §7 single-paragraph append to §3.** Hard stop.
7. **Production code modified.** ANY backend/core/ file change is a stop. ANY existing backend/scripts/ file change is a stop. (New files in backend/ are fine — that's the audit + design + gate report writes.)
8. **A new dependency is needed for E.0.** Should not happen — E.0 is read-only design.
9. **Audit reveals something architecturally surprising** that changes the E.1 design materially. Soft observation in gate report; document the surprise; do NOT redesign mid-session. The redesign is Daniel's call after he reads E.0.

---

## §10 — Discipline reminders (Karpathy)

1. **Read first.** All §1 docs in full before any audit writing. Especially the v6.3.5 HTML.
2. **Sacred floor first.** 216/19/0 before, after, after commit.
3. **Minimum implementation.** No code. No deps. No prod-file modifications. Audit + design docs + housekeeping moves only.
4. **Vault rule held.** Five trade modules untouched, not opened. v6.3.5 read-only.
5. **Audit honesty.** If the v6.3.5 HTML has surprising structure or duplicates a lot of backend logic, document it factually. Don't soften. The audit is the input to E.2's strip planning; soft audits cause E.2 to under-strip and ship a bloated frontend.
6. **Design conservatism.** E.1 ships 2 endpoints. Not 5. The API design doc lists future endpoints but E.0 is for E.1 design only. Don't pre-build later phases' contracts in detail; the shape will shift as E.1 ships and E.2 reveals what the frontend actually needs.
7. **Housekeeping discipline.** v6.3.5 stays put. v6.3.1–6.3.4 move with `git mv` (history preserved). MANIFEST.md entries for each. Same pattern as 2026-04-29 housekeeping.

---

## §11 — Done definition (gate report checklist)

The final gate report `backend/E0_GATE_REPORT.md` confirms:

- [ ] Pre-flight: 216/19/0 backend; 138/138 frontend; vault SHA-1s captured; 5 frontend SHA-1s captured; branch from D.2 head
- [ ] Branch `phase2-v0.3-E0-api-design-and-frontend-audit` created
- [ ] `backend/E0_FRONTEND_AUDIT.md` written per §4 structure
- [ ] `backend/E0_API_DESIGN.md` written per §5 structure
- [ ] v6.3.1, 6.3.2, 6.3.3, 6.3.4 HTMLs moved to `safe_for_removal/frontend_versions/` via `git mv`
- [ ] `safe_for_removal/MANIFEST.md` updated per §6.3
- [ ] v6.3.5 SHA-1 unchanged (audit was read-only)
- [ ] All 5 vault-ruled module SHA-1s unchanged
- [ ] Backend tests 216/19/0; frontend tests 138/138 against v6.3.5
- [ ] No production code modified (`git diff --stat backend/core/` empty; `git diff --stat backend/scripts/` empty)
- [ ] No `pyproject.toml` change
- [ ] PROJECT_CLAUDE.md updated per §7 (single §3 paragraph; nothing else)
- [ ] BLOCK_RUN.md Phase 5 section populated per §8
- [ ] Single commit on `phase2-v0.3-E0-api-design-and-frontend-audit`; pushed to origin
- [ ] §9 stops: status of each enumerated explicitly (none expected)
- [ ] Final gate report produced

---

## §12 — Commit shape

**Single commit** on `phase2-v0.3-E0-api-design-and-frontend-audit`:

- `backend/E0_FRONTEND_AUDIT.md` (NEW)
- `backend/E0_API_DESIGN.md` (NEW)
- `backend/E0_GATE_REPORT.md` (NEW)
- `Huckleberry_AI_6.3.1_Scope.html` → `safe_for_removal/frontend_versions/...` (git rename)
- `Huckleberry_AI_6.3.2_Scope.html` → ... (git rename)
- `Huckleberry_AI_6.3.3_Scope.html` → ... (git rename)
- `Huckleberry_AI_6.3.4_Scope.html` → ... (git rename)
- `safe_for_removal/MANIFEST.md` (MODIFIED — appended frontend versions section)
- `PROJECT_CLAUDE.md` (MODIFIED — §3 single paragraph append)
- `backend/BLOCK_RUN.md` (MODIFIED — Phase 5 section added)

Commit message body:
- "E.0: frontend audit + API design + v6.3.x housekeeping"
- One line per deliverable
- "v6.3.5 SHA-1 unchanged; vault SHA-1s unchanged; backend 216/19/0; frontend 138/138"

Push at end. Authorized.

---

## §13 — Execution mode

**Single chunk, autonomous, soft gates only.** Run E0.0 through E0.6 without per-step confirmation. Single final gate report.

§9 stops are the only hard pauses.

Total wall-clock estimate: ~30-60 minutes. Pre-flight reads dominate (especially the v6.3.5 HTML at presumably 20K+ lines). Audit + design writing ~15-20 min. Housekeeping moves ~5 min. Doc updates + commit + push ~10 min.

---

## §14 — Closing

After E.0 ships:

1. **Daniel reviews** `backend/E0_FRONTEND_AUDIT.md` and `backend/E0_API_DESIGN.md`. These are the design docs E.1 builds against. If anything in either doc is wrong, Daniel flags it; we patch the docs before E.1 starts.
2. **Daniel reviews** the v6.3.x housekeeping (4 files moved, manifest updated).
3. **Daniel decides** any patches to the API design.
4. **E.1 march orders drafted** by extended-thinking Claude — FastAPI scaffold, two endpoints, test coverage, hard gate via TestClient.

E.0 is a read-only design phase. E.1 is when novel code starts shipping. Standing by for execution.

**End of MARCH_ORDERS_E_0_audit_and_design.md.**
