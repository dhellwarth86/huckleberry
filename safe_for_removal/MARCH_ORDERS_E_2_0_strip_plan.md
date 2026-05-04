# MARCH ORDERS — Phase E.2.0: Frontend Strip Plan + New-File Design + API Client Spec (Read-Only Diagnostic)

**Date issued:** 2026-04-30
**Issued by:** Daniel (via extended-thinking Claude planning session)
**Executed by:** Claude Code
**Phase shape:** Single short session, autonomous, soft-gates-only, **read-only diagnostic** — no code changes, no test changes, no dependency changes
**Phase scope:** Produce four design deliverables that fully spec E.2.1 (strip), E.2.2 (connect), E.2.debug (smoke), and E.2.hard-gate. After E.2.0 ships and Daniel reviews, E.2.1 march orders draft based on what E.2.0 produced.
**Read first:** PROJECT_CLAUDE.md, backend/BLOCK_RUN.md, then this document

---

## §0 — What this phase is

E.2 is a re-architecture, not a refactor. ~3,800–4,100 lines of `Huckleberry_AI_6.3.5_Scope.html` are slated for deletion (per `backend/E0_FRONTEND_AUDIT.md`); the surviving portions wire to the FastAPI surface E.1 shipped (`backend/E1_GATE_REPORT.md`); a fresh single-file HTML named `Huckleberry_AI_phase2.v1.0.0.html` lands at `frontend/src/`.

E.2.0 is the **planning-only** sub-phase of E.2. It produces the line-by-line strip plan, the new-file structural design, the API client wrapper signature spec, and the new frontend test floor proposal. **No code is modified, anywhere.** E.2.0's deliverables become the input to E.2.1's march orders.

**Why E.2.0 exists as its own sub-phase:** the audit (`backend/E0_FRONTEND_AUDIT.md`) identified ~1,170 lines of business logic to delete but did not draw the cut lines. Cut lines are load-bearing — strip 5 lines too many and a manual annotation tool stops working; strip 5 lines too few and dead JS keeps trying to call the deleted pipeline. E.2.0 draws the cut lines on paper before E.2.1 makes the cuts.

**Five-sub-phase E.2 shape (Daniel directive 2026-04-30):**

| Sub-phase | Type | What it produces | Gate |
|---|---|---|---|
| **E.2.0 (this)** | Read-only diagnostic | Strip plan + new-file design + API client spec + test floor proposal | Soft gate to Daniel review |
| E.2.1 | Destructive | New file built; v6.3.5 archived to safe_for_removal/; old test floor retired | Soft gate |
| E.2.2 | Constructive | API client wired; endpoints called from new file | Soft gate |
| E.2.debug | Diagnostic | Browser console + network glitches + UI bugs shaken out; API contract frozen | Soft gate |
| E.2.hard-gate | Empirical | Silverleaf upload-to-display end-to-end via real uvicorn | Hard gate |

If E.2.debug surfaces an API issue rather than a frontend issue, that issue **kicks back to a separate E.1-territory session** rather than getting fixed in E.2.debug. API contract frozen during E.2 means the same shape v6.3.5's tests can be ported against, and means E.2.hard-gate is testing connection, not API design.

---

## §1 — What this phase is NOT

**OUT OF SCOPE for E.2.0:**

- **Any code modification anywhere.** E.2.0 is read-only. The v6.3.5 SHA-1 must match pre-session at session end; the five vault-ruled module SHA-1s must match; `backend/api/` and `backend/core/` are not opened.
- **Adding any test.** Test floor stays 222 backend / 138 frontend.
- **Adding any dependency.** `pyproject.toml` and `package.json` unchanged.
- **Building the new HTML.** E.2.0 designs it on paper; E.2.1 builds it.
- **Stripping anything from v6.3.5.** E.2.0 plans the strip; E.2.1 executes.
- **Wiring API calls.** E.2.0 specs the wrapper; E.2.2 implements.
- **Login screen.** Goes to post-user-testing security cluster (Daniel directive 2026-04-30).
- **Build step / npm bundling / module split.** Single-file HTML through E.2; split deferred.
- **PROJECT_CLAUDE.md edits beyond §3 paragraph append + §7 phase table update.** Other sections require explicit authorization.
- **Vault-ruled module changes.** Vault rule active.

---

## §2 — Pre-flight reads (Karpathy step 1)

Full reads, in this order:

1. **PROJECT_CLAUDE.md** — entry point. §3 most-recent paragraph (E.1 complete + discipline patches); §7 phase table.
2. **`backend/BLOCK_RUN.md`** — Phases 5 (E.0), 6 (E.1), 6.5 (E.1 discipline patches). You extend with Phase 7 (E.2.0).
3. **`VALIDATION_LEDGER.md`** — sacred floors, vault list.
4. **`backend/E0_FRONTEND_AUDIT.md`** — the audit E.2.0 acts on. Read in full. Items B1–B6 are the strip targets.
5. **`backend/E0_API_DESIGN.md`** — the API contract E.2 connects to. §5.2 (endpoints) and §5.9 (forward-compat shape) are load-bearing for the API client spec deliverable.
6. **`backend/E1_GATE_REPORT.md`** — what actually shipped (versus what was specced).
7. **`backend/E1_HARD_GATE_silverleaf_api.md`** — the empirical evidence the API works.
8. **`backend/E1_UVICORN_SMOKE.md`** — production run-mode validation; informs the status-bar polling spec.
9. **`frontend/Huckleberry_AI_6.3.5_Scope.html`** — **READ-ONLY**, full file. SHA-1 captured at pre-flight, verified at session end. This is the strip target; E.2.0 reads every line range identified in the audit and writes the strip plan against it.

**Do NOT open:**
- Five vault-ruled modules (`backend/core/roofing_module.py`, `glazing_module.py`, `roofing_vocabulary.py`, `glazing_vocabulary.py`, `debug_module.py`).
- `backend/api/` (E.1's production code; not modified in E.2.0).
- `backend/core/` (D.2's production code; not modified).
- Anything in `safe_for_removal/` (housekeeping reference only).
- `CLAUDE.md` (retired pre-D.1).

---

## §3 — Step E2.0.0: Pre-flight verification

Establish the read-only floor before any audit work begins.

- Run full backend suite. Floor: **222 passed, 19 skipped, 0 failed**. Hard stop if not met.
- Run frontend suite. Floor: **138/138 against v6.3.5**. Hard stop if not met.
- Capture pre-session SHA-1s for all five vault-ruled modules.
- Capture pre-session SHA-1 for `frontend/Huckleberry_AI_6.3.5_Scope.html`.
- Capture pre-session SHA-1s for `backend/api/main.py`, `backend/api/routes/jobs.py`, `backend/api/schemas/jobs.py` (E.1 production code; must not change).
- Verify branch state: `phase2-v0.3-E1-discipline-patches` head matches commit `29d2ef8` per BLOCK_RUN.md Phase 6.5.
- Confirm `git remote -v` shows `https://github.com/dhellwarth86/huckleberry.git`.

Pre-flight failure → §10 stop, no audit work begins.

---

## §4 — Step E2.0.1: Branch

```
phase2-v0.3-E2-0-strip-plan  (NEW; from E.1 discipline patches head 29d2ef8)
```

Single commit at end of session. Pushed.

---

## §5 — Step E2.0.2: Produce the four deliverables

E.2.0 produces exactly four design documents under `backend/`. All four are markdown. None contain code modifications — they specify modifications that E.2.1 / E.2.2 will execute.

### Deliverable 1 — `backend/E2_0_STRIP_PLAN.md`

**Purpose:** Line-by-line plan for what E.2.1 deletes from v6.3.5, what it preserves, and what it minimally restructures.

**Required sections:**

§1 — **Strip targets (line ranges).** For each audit item B1–B6 plus the pipeline tab, specify:
- Exact line range to delete (start line / end line, inclusive).
- The function or block boundary the deletion respects (don't delete from mid-function).
- What references in surviving code currently call into the deleted region (grep results — actual call sites by line number).
- What to do about each call site: (a) delete the call (deletion cascade), (b) replace with API call (E.2.2), (c) replace with stub that throws clearly until E.2.2 wires it.

§2 — **Confirmed strip column** (per Daniel directive 2026-04-30):
- B1 — `TP` namespace (12-stage pipeline JS port), lines 1730–2560
- B2 — `ROOF_VOCAB`, lines 5018–5143
- B3 — `extractScope`, lines 5193–5306
- B4 — `classifyPage`, lines 5313–5329
- B5 — text helpers (`collectPlanText`, `findMatches`, `splitBySystemLabels`), lines 5149–5191
- B6 — pdf.js path/text *extraction* (operator-list walker), lines ~2768–2960 — **carefully separate** from pdf.js *page rendering*, which is preserved
- Pipeline tab — UI markup + tab handler + state (line ranges TBD by audit; this section identifies them)
- Any test code under `UNIT_TESTS` / `INTEGRATION_TESTS` / `SCOPE_TESTS` / `SCOPE_INTEGRATION_TESTS` that exercises the above (test-floor implications go to Deliverable 4)

§3 — **Confirmed keepers column** (per Daniel directive 2026-04-30):
- pdf.js page **rendering** (the part of B6 that produces page images for OpenSeadragon)
- OpenSeadragon viewer
- Konva annotation overlay
- xlsx export (takeoff Excel)
- Manual annotation tools — pin / line / polygon drawing
- 7 of 8 tabs (NEW SESSION / SCOPE / PAGES / VIEWER / TAKEOFF / TESTS / ABOUT) — pipeline tab struck per §2

§4 — **planSet shape dependency analysis (LOAD-BEARING).** This is the highest-risk strip surface. The manual annotation tools (preserved) currently read fields from a `planSet` object that the JS pipeline (being stripped) builds. After E.2.1:
- Identify every field of `planSet` (and `planSet.pages[]`) that the kept tools actually read. Grep `planSet.` and `\.pages\[` against the kept regions.
- For each consumed field, classify origin:
  - **(a) API-provided** — comes from `GET /jobs/{id}` or future endpoints; document expected shape mismatch with current planSet field
  - **(b) Local pdf.js-rendering provided** — the kept pdf.js code can populate this from `getPage(n)` directly without the operator-list walker
  - **(c) Currently-pipeline-derived, not-yet-API-provided** — field is consumed by kept tools, currently built by stripped pipeline, no E.1 endpoint provides it. **These are the gaps.** For each gap, propose: defer-via-stub-empty-array, surface-in-E.3-endpoint-design, or local-pdf.js-derive-without-pipeline.
- Output: a planSet shape contract for the new file. What fields exist; where each comes from; what the kept tools can rely on after strip.

§5 — **Risk areas.** The 5–10 specific cut decisions where a wrong call breaks something. Manual annotation tools' planSet dependency is the headliner; others may surface during the line-by-line walk. Each risk area gets: description, what could break, mitigation (test-before-strip is preferred; defer-to-E.2.debug is acceptable; ship-and-pray is not).

§6 — **Net line count summary.** Pre-strip total (8,694), post-strip estimate, deletion percentage. Sanity-check against audit's ~3,800–4,100 line target.

### Deliverable 2 — `backend/E2_0_NEW_FILE_DESIGN.md`

**Purpose:** Structural skeleton of `frontend/src/Huckleberry_AI_phase2.v1.0.0.html`. Defines the file's top-to-bottom organization so E.2.1's strip-and-rebuild produces a coherent file rather than a v6.3.5 with deletions.

**Required sections:**

§1 — **File header.**
- DOCTYPE, lang, meta charset/viewport
- `<title>` — exact string TBD; "Huckleberry AI · Phase 2" as default unless Daniel directs otherwise
- CDN script imports (`pdf.js@3.11.174`, `openseadragon@4.1.0`, `konva@9.3.0`, `xlsx@0.18.5`) — verify versions match v6.3.5 keepers exactly; document any drift
- `<style>` block — preserved from v6.3.5 minus pipeline-tab CSS; new status-bar state CSS added for `connected` / `degraded` / `unreachable`

§2 — **Body markup (UI shell).**
- Header
- Sidebar
- 7-tab structure (pipeline tab struck): `NEW SESSION / SCOPE / PAGES / VIEWER / TAKEOFF / TESTS / ABOUT`
- Per-tab pane skeleton — what's in each tab, what's deleted from each, what's new
- Status bar — three states (`CONNECTED · v0.3.0-E.2` / `DEGRADED` / `UNREACHABLE`); CSS class names; DOM hook

§3 — **Top-level constants and configuration.**
```javascript
const API_BASE = "http://localhost:8000"; // E.2: hardcoded for dev; runtime config at security/Postgres phase
const HEALTH_POLL_INTERVAL_MS = 30000;     // E.2: every 30s
const HEALTH_PROBE_TIMEOUT_MS = 5000;      // E.2: per-request timeout
```
Document additional constants surfaced during the audit.

§4 — **Script section ordering.**
After v6.3.5's three big script blocks (TP / UI+tests / scope+roofing), the new file's script section should be reorganized to:
1. Constants and configuration
2. API client wrapper (per Deliverable 3)
3. Status bar polling logic
4. PDF.js page rendering (kept portion of B6)
5. Viewer (OpenSeadragon)
6. Annotation tools (Konva-driven pin / line / polygon)
7. Per-tab handlers
8. xlsx export
9. New test suite (per Deliverable 4)

Document why this order and what scope-load implications it has (e.g., the wrapper must be defined before any tab handler that calls it).

§5 — **Status-bar dynamic polling spec.**
- Three states with copy: `AI BACKEND: CONNECTED · v0.3.0-E.2`, `AI BACKEND: DEGRADED`, `AI BACKEND: UNREACHABLE`
- Three triggers (per planning Q6 + clarification 2026-04-30):
  - On page load (immediate)
  - Every `HEALTH_POLL_INTERVAL_MS` thereafter
  - On any failed user-initiated request (i.e., immediate re-poll if `createJob`/`getJob` fails network)
- State transition rules: success → CONNECTED; non-200 → DEGRADED; fetch throws → UNREACHABLE
- Visual: include CSS color/icon spec so the state is glanceable

§6 — **What v6.3.5 elements do NOT carry forward.**
Explicit list (cross-references Deliverable 1):
- Pipeline tab + handler + state
- TP namespace
- ROOF_VOCAB and matchers
- extractScope
- classifyPage
- Pipeline-related test categories
- Status-bar copy `AI BACKEND: REMOVED / 100% OFFLINE · CLIENT-SIDE`

### Deliverable 3 — `backend/E2_0_API_CLIENT_SPEC.md`

**Purpose:** Full signature spec for the API client wrapper that lives in `phase2.v1.0.0.html`. Includes stubs for E.3 endpoints (signatures committed now to prevent drift).

**Required sections:**

§1 — **Wrapper structure.**
Single namespace object (preferred) or module-pattern IIFE; living in the new file's script block per Deliverable 2 §4 ordering.

§2 — **`apiCall(method, path, body)` helper.**
The single point through which every wrapper function flows. Spec: signature, return shape, error normalization, timeout handling, AbortController integration, JSON parse safety. Output for callers should be a single discriminated-union shape (e.g., `{ ok: true, status, data }` or `{ ok: false, status, error, detail }`) so call-site error handling is uniform.

§3 — **Real implementations (E.1 endpoints).**
- `createJob(payload)` — `POST /jobs`. Document expected payload shape (matches `JobCreateRequest` per `E0_API_DESIGN.md` §5.2) and response shape (matches `JobResponse`).
- `getJob(jobId)` — `GET /jobs/{job_id}`. 404 handling — wrapper returns the error shape; UI decides what to render.
- `health()` — `GET /health`. Used by status-bar polling. Returns version string for status-bar display.

§4 — **Stub slots (E.3 forward-compat).**
Each stub returns immediately with `{ ok: false, error: "not_implemented_in_e2", detail: "<endpoint> ships in E.3" }`. Signatures committed:
- `dispatch(jobId)` — `POST /jobs/{id}/dispatch` (reserved per `E0_API_DESIGN.md` §5.3)
- `loadResults(jobId)` — `GET /jobs/{id}/results` (reserved)
- `listJobs(params)` — `GET /jobs` with sort+filter (reserved; matches `job_storage.list_jobs`)
- `updateJobStatus(jobId, status)` — `PATCH /jobs/{id}` or similar (reserved)
- Annotation save/load — deferred; signatures sketched as comments only since shape isn't decided

The signatures are *commitments* — E.3 fills in the body, doesn't redesign the wrapper.

§5 — **Error handling matrix.**
For each of the four error classes the API can return (404, 422, 500, network failure), specify:
- Wrapper return shape
- UI-side default behavior (e.g., 404 on getJob → show "job not found" empty state; network failure → flip status bar to UNREACHABLE)
- Whether the failure should immediately re-poll `/health` (per Deliverable 2 §5 trigger 3)

§6 — **Status-bar integration.**
The wrapper exposes a hook for status-bar polling to subscribe. When `apiCall` detects network failure, the status bar's polling logic fires its own `/health` immediately rather than waiting 30s.

### Deliverable 4 — `backend/E2_0_TEST_FLOOR_PROPOSAL.md`

**Purpose:** Spec the new frontend test floor for `phase2.v1.0.0.html`. The 138/138 floor against v6.3.5 retires entirely (per Daniel directive 2026-04-30); new floor is fresh and smaller.

**Required sections:**

§1 — **What retires.**
The 138 test enumeration from v6.3.5. Document which of the five test collections (`UNIT_TESTS`, `INTEGRATION_TESTS`, `TOOL_TESTS`, `SCOPE_TESTS`, `SCOPE_INTEGRATION_TESTS`) retire entirely vs. which contribute survivors.

§2 — **What survives (ported as-is or with minor edits).**
Annotation tool tests (`TOOL_TESTS` collection, per audit line 4565) — these test pin/line/polygon drawing behavior that's preserved. Identify exact test names that survive.

§3 — **What's new.**
- API client smoke tests (mocked `fetch`, confirm `createJob` / `getJob` / `health` shape correctness, confirm error normalization)
- Status-bar state transition tests (mocked `health()` responses, assert correct state class and copy)
- Stub-slot tests (assert each stub returns the canonical not-implemented shape)
- Status-bar event-driven re-poll trigger test

§4 — **Proposed new floor count.**
Sum the survivors + new tests. Daniel sets the actual floor when E.2.1 ships; E.2.0 proposes a number and a rationale.

§5 — **Test harness changes.**
`run_tests.js` currently runs against `Huckleberry_AI_6.3.5_Scope.html`. After E.2.1 ships:
- Old harness retires (or moves to safe_for_removal/) per the v6.3.5 archival decision
- New harness runs against `frontend/src/Huckleberry_AI_phase2.v1.0.0.html`
- `package.json` `test` script update (one-line; happens in E.2.1, but spec'd here)
- Spotcheck and mutation-test scripts: confirm they retire alongside v6.3.5 archival (matches the existing `npm run test:spotchecks` failure noted in the housekeeping debt section of `HANDOFF_2026-04-29_end_of_E_0.md`)

§6 — **What the new floor does NOT cover.**
The new floor is a smoke suite for the *thin viewer*. The deep correctness coverage migrated to backend with Phase B / C / D — `RoofingModule.analyze`, `GlazingModule.analyze`, `dispatch_gate.run_dispatch`, etc. all carry test coverage in the 222 backend floor. E.2.0's test proposal explicitly notes this re-distribution; the new frontend floor isn't *smaller* than v6.3.5's because the tests vanished, it's smaller because they migrated.

---

## §6 — Step E2.0.3: Update canon

Surgical edits only.

### `PROJECT_CLAUDE.md`

**§3 (state paragraphs, chronological order):** append a new paragraph after the E.1 discipline patches paragraph documenting E.2.0 completion. Pattern matches prior phase entries: what shipped, key receipts, sacred floor status, branch.

**§7 (phase table):** update the E.2 row from "NEXT-eligible" to a sub-table or note documenting the 5-sub-phase structure (E.2.0 through E.2.hard-gate). E.2.0 row gets `COMPLETE 2026-04-30`. E.2.1 through E.2.hard-gate stay as scheduled-but-unstarted entries with the soft-gate dependency on Daniel review of E.2.0 deliverables called out.

**No other section is touched.** §1, §2, §4, §5, §6, §8, §9, §10 stay verbatim.

### `backend/BLOCK_RUN.md`

Append **Phase 7 — E.2.0 strip plan diagnostic** section. Contents per the section's own template (matches Phase 6 / 6.5 structure). Phase 8 placeholder reserved for E.2.1.

---

## §7 — Step E2.0.4: Gate report

Final deliverable: `backend/E2_0_GATE_REPORT.md`. Contents:

§1 — Pre-flight results (test floors, SHA-1 captures, branch verification).
§2 — Done-definition checklist (§13 of this doc) — every item PASS / FAIL / N/A with evidence.
§3 — §10 stop conditions — explicit non-firing status with evidence per stop.
§4 — Sacred floors at session end (matches pre-flight; no drift).
§5 — Wall-clock summary per E2.0.X step.
§6 — Deliverables produced (file paths + brief description of each).
§7 — Open items for Daniel review before E.2.1 march orders draft.

---

## §8 — Step E2.0.5: Commit and push

Single commit. Files in commit:

- `backend/E2_0_STRIP_PLAN.md` (NEW)
- `backend/E2_0_NEW_FILE_DESIGN.md` (NEW)
- `backend/E2_0_API_CLIENT_SPEC.md` (NEW)
- `backend/E2_0_TEST_FLOOR_PROPOSAL.md` (NEW)
- `backend/E2_0_GATE_REPORT.md` (NEW)
- `PROJECT_CLAUDE.md` (MODIFIED — §3 paragraph + §7 phase table only)
- `backend/BLOCK_RUN.md` (MODIFIED — Phase 7 section appended)

Commit message: `E.2.0 strip plan: read-only diagnostic — strip + new-file design + API client spec + test floor proposal`

Push to origin.

---

## §9 — Sacred floors to hold

| Check | Pre-session value | Post-session expectation |
|---|---|---|
| Backend tests | `222 passed, 19 skipped, 0 failed` | unchanged |
| Frontend tests | `138/138 against v6.3.5` | unchanged |
| Vault SHA-1: `roofing_module.py` | `ae9e5b28…` | unchanged |
| Vault SHA-1: `glazing_module.py` | `52c01442…` | unchanged |
| Vault SHA-1: `roofing_vocabulary.py` | `ec6c17f8…` | unchanged |
| Vault SHA-1: `glazing_vocabulary.py` | `64249c8e…` | unchanged |
| Vault SHA-1: `debug_module.py` | `78f71d90…` | unchanged |
| v6.3.5 SHA-1 | `cf3765d6…` | unchanged |
| `backend/api/main.py` SHA-1 | (capture pre-session) | unchanged |
| `backend/api/routes/jobs.py` SHA-1 | (capture pre-session) | unchanged |
| `backend/api/schemas/jobs.py` SHA-1 | (capture pre-session) | unchanged |
| `git diff backend/core/` | empty | empty |
| `git diff backend/api/` | empty | empty |
| `git diff backend/tests/` | empty | empty |
| `pyproject.toml` | unchanged | unchanged |
| `package.json` | unchanged | unchanged |
| CLAUDE.md opened | no | no |

Any drift on any row → §10 stop.

---

## §10 — Stop conditions (any → halt + report, do not proceed)

1. Sacred floor regresses (backend < 222/19/0 or frontend < 138/138).
2. Any vault-ruled module SHA-1 changes.
3. v6.3.5 SHA-1 changes (E.2.0 is read-only against this file).
4. Any of the three E.1 production-code SHA-1s change (`backend/api/main.py`, `routes/jobs.py`, `schemas/jobs.py`).
5. CLAUDE.md gets opened or edited.
6. Any code change in `backend/` source files (E.2.0 is read-only against backend production code).
7. Any test added, modified, or deleted.
8. `pyproject.toml` or `package.json` modified.
9. Any new dependency added (Python or npm).
10. Deliverables 1–4 don't all four address every required section in §5.
11. Daniel's stated keepers-vs-strip boundary (per planning Q4) gets violated by Deliverable 1 — proposing to strip a confirmed keeper or keep a confirmed strip is a §10 stop, not a design choice E.2.0 may make.
12. PROJECT_CLAUDE.md edits exceed the §3 paragraph + §7 phase table scope.
13. Push to origin fails.

---

## §11 — Karpathy procedure conformance

E.2.0 is unusual — read-only diagnostic, no failing-tests-first because nothing is implemented. Karpathy compliance shape:

1. **Read existing code first.** v6.3.5 read in full per §2. Audit re-read. API design re-read. Done.
2. **No failing tests required.** This is a planning phase; the design *is* the deliverable. Tests come in E.2.1 (strip session — old tests retire) and E.2.2 (connect session — new tests added per Deliverable 4).
3. **No implementation.** E.2.0 produces specifications, not code.
4. **No 100% pass verification needed beyond the unchanged test floor.** Sacred floor (222/19/0 + 138/138) confirms no accidental damage.
5. **Ship after all four deliverables produced + canon updated + gate report PASS.**

The Karpathy "diagnostic before production code" rule is honored in spirit — E.2.0 *is* the diagnostic for E.2.1 / E.2.2.

---

## §12 — Vault rule enforcement

Same as every prior phase. Five trade modules + v6.3.5 frontend HTML have SHA-1s captured at pre-flight, verified at session end. Plus three E.1 production-code files (`main.py`, `routes/jobs.py`, `schemas/jobs.py`) — these aren't formally vaulted but E.2.0 is read-only against them, so SHA-1 lock applies for this session.

E.2.0 doesn't open any vault-ruled file. It only opens v6.3.5 (read-only) for the strip plan walk.

---

## §13 — Done-definition checklist

| # | Item | Verified by |
|---|---|---|
| 1 | Pre-flight: 222/19/0 backend; 138/138 frontend; vault SHA-1s + v6.3.5 SHA-1 + 3 E.1 file SHA-1s captured | E2.0.0 |
| 2 | Branch `phase2-v0.3-E2-0-strip-plan` from `29d2ef8` | E2.0.1 |
| 3 | `backend/E2_0_STRIP_PLAN.md` written, all 6 §sections present, planSet shape dependency analysis included | E2.0.2 D1 |
| 4 | `backend/E2_0_NEW_FILE_DESIGN.md` written, all 6 §sections present, status bar polling triggers spec'd | E2.0.2 D2 |
| 5 | `backend/E2_0_API_CLIENT_SPEC.md` written, all 6 §sections present, stub signatures committed | E2.0.2 D3 |
| 6 | `backend/E2_0_TEST_FLOOR_PROPOSAL.md` written, all 6 §sections present, harness changes spec'd | E2.0.2 D4 |
| 7 | Each deliverable cross-references Daniel's locked decisions from planning Q1–Q6 (audit verifies the right inputs were used) | E2.0.4 |
| 8 | `PROJECT_CLAUDE.md` §3 paragraph + §7 phase table updated; no other sections touched | E2.0.3 |
| 9 | `backend/BLOCK_RUN.md` Phase 7 section appended; Phase 8 placeholder reserved | E2.0.3 |
| 10 | Sacred floors all unchanged at session end | E2.0.4 |
| 11 | All vault SHA-1s + v6.3.5 SHA-1 + 3 E.1 file SHA-1s match pre-session | E2.0.4 |
| 12 | `git diff` against `backend/core/`, `backend/api/`, `backend/tests/`, `pyproject.toml`, `package.json` all empty | E2.0.4 |
| 13 | CLAUDE.md not opened during session (verified by absence in any tool call log) | E2.0.4 |
| 14 | Single commit on branch with the 7 files listed in §8 | E2.0.5 |
| 15 | Commit pushed to origin | E2.0.5 |
| 16 | `backend/E2_0_GATE_REPORT.md` produced; all §10 stop conditions explicitly confirmed non-firing | E2.0.4 |
| 17 | No 5th-deliverable scope creep — only the four specified design docs + gate report ship | session end |

---

## §14 — Estimated wall-clock

| Step | Estimated |
|---|---|
| E2.0.0 pre-flight | ~1 min |
| E2.0.1 branch | <30 sec |
| E2.0.2 D1 strip plan (heaviest — full v6.3.5 walk + planSet dep analysis) | ~25–35 min |
| E2.0.2 D2 new-file design | ~10–15 min |
| E2.0.2 D3 API client spec | ~10–15 min |
| E2.0.2 D4 test floor proposal | ~10–15 min |
| E2.0.3 canon updates (PROJECT_CLAUDE.md + BLOCK_RUN.md) | ~5 min |
| E2.0.4 gate report | ~5 min |
| E2.0.5 commit + push | ~2 min |
| **Total** | **~70–95 min** |

D1 is by far the heaviest deliverable — it requires the full v6.3.5 read plus the planSet shape dependency grep walk. Budget accordingly. If D1 hits a snag (e.g., a planSet field consumed in a place the audit didn't catch), do not attempt to design a fix; document the snag in D1 §5 (risk areas) and let E.2.1 march orders address it.

---

## §15 — What ships at end of E.2.0

A complete-on-paper plan for the rest of E.2. After Daniel reviews:

- **If E.2.0 looks clean:** Daniel green-lights E.2.1. Extended-thinking Claude drafts E.2.1 march orders using the strip plan + new-file design as inputs. E.2.1 builds the new file and archives v6.3.5.
- **If something needs adjustment:** Daniel flags it; small follow-up commit on the same E.2.0 branch (or a sibling fix branch) before E.2.1 starts. Common adjustments expected: scope of an individual strip range, a planSet-field origin classification, an API client signature naming convention.

E.2.1 cannot start without E.2.0's deliverables in hand. E.2.0's deliverables cannot ship without Daniel's green light. Soft-gate-with-Daniel-review is the discipline rule for every E sub-phase (per HANDOFF_2026-04-29 §6 rule 6).

---

## §16 — Reminder: Daniel's locked decisions feeding this phase

Pulled forward from the 2026-04-30 planning conversation so they're in the executor's context without requiring a re-read:

| Q | Locked answer | Where it lives in this phase |
|---|---|---|
| Q1 | v6.3.5 → safe_for_removal/frontend_versions/ in E.2.1; 138/138 floor retires; new floor TBD by E.2.0's plan | Deliverable 4 |
| Q2 | New file: `frontend/src/Huckleberry_AI_phase2.v1.0.0.html`; single-file HTML; no build step | Deliverable 2 |
| Q3 | Five-sub-phase E.2 (E.2.0 → E.2.1 → E.2.2 → E.2.debug → E.2.hard-gate); E.2.0 ships standalone first | This document |
| Q4 | Confirmed keepers + strips per §5 D1 §2/§3; pipeline tab strips; manual annotation tools preserved; login screen → security cluster | Deliverable 1 |
| Q5 | Vanilla fetch; hardcoded API_BASE; no auth; thin wrapper with stub slots; apiCall() helper | Deliverable 3 |
| Q6 | Dynamic status bar; 30s polling + page-load + on-failure triggers; three states (CONNECTED/DEGRADED/UNREACHABLE) | Deliverable 2 §5 |

---

**End of MARCH ORDERS — Phase E.2.0.**

Daniel green-lights → Claude Code executes. Single short session. Soft gate to E.2.1 march orders draft after.
