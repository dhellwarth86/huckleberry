# MARCH ORDERS — Phase E.2.1: Frontend Strip + New File + v6.3.5 Archival

**Date issued:** 2026-04-30
**Issued by:** Daniel (via extended-thinking Claude planning session)
**Executed by:** Claude Code
**Phase shape:** Single autonomous session, soft-gates-only, **destructive sub-phase** — frontend re-architecture per E.2.0's four design deliverables
**Phase scope:** Create `frontend/src/Huckleberry_AI_phase2.v1.0.0.html` per E.2.0 design specs. Strip ~4,153 lines of pipeline + scope JS per `E2_0_STRIP_PLAN.md`. Archive v6.3.5 to safe_for_removal/. Re-baseline frontend test floor 138 → **20**. Add one E0_API_DESIGN.md corrigendum (CHECKING vs DEGRADED). No backend changes.
**Read first:** PROJECT_CLAUDE.md, backend/BLOCK_RUN.md, then this document, then the four E.2.0 design deliverables in full

---

## §0 — What this phase is

E.2.1 executes the strip plan. Three concrete things happen:

1. **`Huckleberry_AI_6.3.5_Scope.html` moves** to `safe_for_removal/frontend_versions/` alongside v6.3.1–v6.3.4. The 138/138 floor against v6.3.5 retires permanently.
2. **`frontend/src/Huckleberry_AI_phase2.v1.0.0.html` is created** per `E2_0_NEW_FILE_DESIGN.md`. ~4,841–4,941 lines. Contains: 7 tabs (Pipeline tab struck), rewritten status bar with 3-state health polling, apiClient skeleton with `healthCheck()` real and other methods stubbed, kept Viewer + annotation tools + takeoff Excel export, stubbed `extractScope` + `classifyPage`.
3. **Frontend test floor re-baselines to 20/20.** Per `E2_0_TEST_FLOOR_PROPOSAL.md`: 11 surviving TOOL_TESTS + 3 new status-bar tests + 4 takeoff tests ported from SCOPE_TESTS + 2 new stub tests = 20. The 5 API smoke tests are E.2.2's deliverable, not E.2.1's.

After E.2.1 ships and Daniel green-lights, **soft-gate continuation** to E.2.2 (API client wiring + 5 API smoke tests added). Not auto-continue.

**Why these three things and not more:** E.2.0 produced four deliverables that fully specify five sub-phases of E.2. E.2.1 executes only what E.2.0's strip plan and new-file design specify. Wiring `createJob` / `getJob` to real implementations is E.2.2's work — keeping it out of E.2.1 isolates the strip risk from the connection risk.

**Architectural reframing landed in canon (per `E2_0_STRIP_PLAN.md` §4.5):** After E.2.1, `planSet` is no longer the application's data model. It is a page-rendering cache. The application's data model becomes the API-provided job state. This is the single most consequential change E.2.1 makes, and it is the change every subsequent design choice flows from.

---

## §1 — What this phase is NOT

**OUT OF SCOPE for E.2.1:**

- **Wiring `createJob` / `getJob` / `listJobs` / `getResults` / `dispatchJob` to real backend calls.** E.2.2 territory. In E.2.1, these methods exist as stubs that throw `Error("not_implemented_in_e2_1")` (or throw the not-yet-implemented signal per D3 §4). **Exception:** `healthCheck()` is implemented in E.2.1 because the status-bar polling cannot function without it.
- **Adding the 5 API smoke tests.** E.2.2. Floor at end of E.2.1 = 20/20. Floor at end of E.2.2 = 25/25.
- **Manual verification of viewer + annotations + takeoff with real PDF.** E.2.debug. E.2.1 verifies the new file *loads* in a browser without JS errors and the test harness reports 20/20 — but does not run a Silverleaf bidset through it end-to-end.
- **Backend code changes anywhere.** `backend/api/`, `backend/core/`, `backend/tests/`, `backend/scripts/` all read-only.
- **`pyproject.toml` changes.** No new Python deps.
- **`package.json` dep changes.** The browser uses native `fetch()` — no axios, no http library. Only the `package.json` `test` script field updates (path repointing).
- **Login screen.** Post-user-testing security cluster.
- **Build step / module split / npm bundling.** Single-file HTML through E.2.
- **PROJECT_CLAUDE.md edits beyond §3 paragraph append + §7 phase table update.**
- **Vault-ruled module changes.**
- **Restoring DEGRADED state.** Per Daniel directive 2026-04-30: ship CHECKING/CONNECTED/UNREACHABLE; DEGRADED re-evaluated when auth/CORS lockdown creates real 503-style "reachable-but-rejecting" scenarios in the security phase.
- **Scope creep beyond the 14 strip targets in `E2_0_STRIP_PLAN.md` §1.** If E.2.1 finds additional pipeline-related code that wasn't in the strip plan, **STOP** (§7 stop) and document the finding. Do not creatively expand the strip.

---

## §2 — Pre-flight reads (Karpathy step 1)

Full reads, in this order:

1. **PROJECT_CLAUDE.md** — entry point. §3 paragraphs through E.2.0 (most recent); §7 phase table; §4 discipline; §6 misconceptions.
2. **`backend/BLOCK_RUN.md`** — Phase 7 (E.2.0). You extend with Phase 8 (E.2.1).
3. **`VALIDATION_LEDGER.md`** — sacred floors, vault list.
4. **`backend/E2_0_STRIP_PLAN.md`** — D1. Read in full. The 14 strip targets (S1–S14), planSet shape dependency analysis (§4), risk areas (§5), net line count (§6) are load-bearing for execution.
5. **`backend/E2_0_NEW_FILE_DESIGN.md`** — D2. Read in full. File header (§1), 7-tab markup (§2), top-level constants (§3), 9-section script ordering (§4), status-bar polling (§5), what doesn't carry forward (§6).
6. **`backend/E2_0_API_CLIENT_SPEC.md`** — D3. Read in full. apiClient skeleton (§1), apiCall helper (§2), real vs stub methods (§3 + §4), error matrix (§5), status-bar integration (§6).
7. **`backend/E2_0_TEST_FLOOR_PROPOSAL.md`** — D4. Read in full. Retiring (§1), surviving (§2), new (§3), proposed floor 25/25 (§4) — but **E.2.1 floor is 20/20** (§4.4 progression: E.2.1 = 20, E.2.2 = 25 after API smoke tests added).
8. **`backend/E2_0_GATE_REPORT.md`** — what E.2.0 actually shipped.
9. **`frontend/Huckleberry_AI_6.3.5_Scope.html`** — **READ-ONLY SOURCE** for the strip. Pre-session SHA-1 captured, verified at session end before move (post-move it lives at `safe_for_removal/frontend_versions/Huckleberry_AI_6.3.5_Scope.html` with the same content; SHA-1 of file content unchanged, only path changes).
10. **`backend/E0_API_DESIGN.md`** — the contract `apiClient` is built against. §5.2 endpoint shapes (E.1 endpoints), §5.12 corrigenda section (E.1 patches landed there; E.2.1 appends a third corrigendum).
11. **`backend/E0_FRONTEND_AUDIT.md`** — original audit; useful for cross-reference if a strip target's call site is unclear.
12. **`backend/E1_GATE_REPORT.md`** + **`backend/E1_HARD_GATE_silverleaf_api.md`** + **`backend/E1_UVICORN_SMOKE.md`** — what the API actually does on the wire (so the apiClient implementation matches reality, not just the spec).

**Do NOT open:**
- Five vault-ruled modules.
- `backend/api/` (read for understanding only via gate reports — do not modify).
- `backend/core/` (do not open).
- `CLAUDE.md` (retired).
- v6.3.1–v6.3.4 in `safe_for_removal/frontend_versions/` (already archived).

---

## §3 — Step E2.1.0: Pre-flight verification

Establish the floor before destructive work begins.

- Run full backend suite. Floor: **222 passed, 19 skipped, 0 failed**. Hard stop if not met.
- Run frontend suite against v6.3.5. Floor: **138/138 passed**. **This is the last time this floor is verified — it retires today.** Hard stop if not met (don't ship a strip on top of a regressed baseline).
- Capture pre-session SHA-1s for all five vault-ruled modules.
- Capture pre-session SHA-1 for `frontend/Huckleberry_AI_6.3.5_Scope.html` (`cf3765d61fd6f17de46024a3a84c62f25b19b3c5` per E.2.0 ship). This SHA-1 is verified at session end **after** the file is moved — content unchanged, only path changes via `git mv`.
- Capture pre-session SHA-1s for `backend/api/main.py`, `backend/api/routes/jobs.py`, `backend/api/schemas/jobs.py` (E.1 production code; must not change in E.2.1).
- Verify branch state: `phase2-v0.3-E2-0-strip-plan` head matches commit `a1c804c` per BLOCK_RUN.md Phase 7.
- Confirm `git remote -v` shows `https://github.com/dhellwarth86/huckleberry.git`.

Pre-flight failure → §10 stop, no destructive work begins.

---

## §4 — Step E2.1.1: Branch

```
phase2-v0.3-E2-1-strip  (NEW; from E.2.0 head a1c804c)
```

Single commit at end of session. Pushed.

---

## §5 — Step E2.1.2: Move v6.3.5 to safe_for_removal/

Per locked decision Q1 (planning conversation 2026-04-30):

```
git mv frontend/Huckleberry_AI_6.3.5_Scope.html safe_for_removal/frontend_versions/Huckleberry_AI_6.3.5_Scope.html
```

After the move:
- The file content is unchanged (SHA-1 of content matches pre-session capture).
- `npm test` against the original path will fail (file no longer at `frontend/Huckleberry_AI_6.3.5_Scope.html`). This is expected and correct — the 138/138 floor retires.
- The `safe_for_removal/MANIFEST.md` is updated with one row noting v6.3.5's move per E.2.1 strip.

**Do not delete v6.3.5 outright.** The discipline rule is: things move to safe_for_removal/ pending Daniel's eventual review-and-empty session. Outright deletion is reserved for that session.

---

## §6 — Step E2.1.3: Create new file scaffold

Create `frontend/src/Huckleberry_AI_phase2.v1.0.0.html` per `E2_0_NEW_FILE_DESIGN.md`.

The new file is built **bottom-up from spec**, not top-down by copying v6.3.5 and deleting. This is intentional: copy-and-delete invites accidental retention of pipeline-coupled code; spec-driven build forces every line to justify its presence.

**Build order (per D2 §4 dependency graph):**

1. **File header** (D2 §1):
   - `<!DOCTYPE html>`, lang, meta, `<title>` "Huckleberry AI — Phase 2"
   - 4 CDN imports: pdf.js@3.11.174, openseadragon@4.1.0, konva@9.3.0, xlsx@0.18.5
   - Google Fonts link (unchanged from v6.3.5)
   - `<style>` block: ported from v6.3.5 minus the ~96 lines of pipeline-related CSS (D2 §1.2); adds ~15 lines of `.sb-health-dot` styles for the 3 states
2. **Body markup** (D2 §2):
   - Header with `phase2.v1.0.0` version badge, `TRACEPOINT VIEWER` logo
   - 3-state status bar with `#sbHealthDot` + `#sbApiStatus` + `#sbBackendVersion` (D2 §2.2)
   - Sidebar with "Connection" section + "Architecture" section (D2 §2.3) — pipeline sections gone
   - 7-tab structure (D2 §2.4); tab indices 0–6; Pipeline tab struck
   - 7 tab panes per D2 §2.5 (NEW SESSION / SCOPE / PAGES / VIEWER / TAKEOFF / TESTS / ABOUT — Pipeline pane removed)
   - Fullscreen exit button (kept)
3. **Script block 1** — API client + UI utils (D2 §4 sections 1–2):
   - Top-level constants: `API_BASE = 'http://127.0.0.1:8000'`, `HEALTH_POLL_INTERVAL_MS = 30000`, `HEALTH_PROBE_TIMEOUT_MS = 5000`
   - `apiCall(method, path, opts)` helper per D3 §2 (fetch + AbortController + JSON parse + error normalization)
   - `apiClient` object per D3 §1: `healthCheck` real (per D3 §3.1), `createJob` / `getJob` stubs throwing `Error("not_implemented_in_e2_1: createJob ships in E.2.2")` and similar (per D3 §4 stub pattern, but extended to also stub createJob/getJob in E.2.1)
   - `showTab(idx)`, `escapeHTML()` / `esc()`
4. **Script block 2** — everything else, in dependency order (D2 §4 sections 3–9):
   - Section 3: PDF loader. `extractPlanSetFromPdf()` rewritten per S8 to do rendering only (no operator-list walker). `getOrRenderPageCanvas()` unchanged.
   - Section 4: Test harness. `assert()`, `approx()`, `withTestIsolation()`, `runTestBatch()`, `runUnitTests()`, `runAllTests()`. Plus the SKIP convention in `runTestBatch` per D4 §5.2.
   - Section 5: App state + file handling. `App` object, `handleFileSelect`, `handleDrop`, `loadPdfFile`, `refreshAfterPdfLoad`. Pipeline-specific calls removed.
   - Section 6: Viewer. Unchanged keeper region per D1 §3 (lines 3725–4560 of v6.3.5).
   - Section 7: Scope UI + seed data. `ROOFING_SEED_ITEMS` kept. `extractScope()` and `classifyPage()` are stubs (see §6.1 below). `renderScopeTab` etc. unchanged in structure but read from stubs.
   - Section 8: Takeoff + Excel export. `DEFAULT_WASTE_FACTOR = 0.10` inlined (replacing `ROOFING_CONSTANTS.wasteFactor`). `buildTakeoffModel`, `exportTakeoffToExcel`, `renderTakeoffTab`, `setTakeoffWaste`. Vertex snap helper kept.
   - Section 9: Viewer extensions + hooks + tests + boot. `showTab` hook with **updated tab indices** per Risk 3. Surviving 11 TOOL_TESTS. New 3 status-bar tests + 4 takeoff tests + 2 stub tests. Boot IIFE.

### §6.1 — Stubs land in E.2.1, real implementations land in E.2.2

The stub strategy per D1 §4.4:

```javascript
// E.2.1: stub. Real impl ships in E.2.2 fetching from GET /jobs/{id}/results.
function extractScope(planSet) {
  return {
    systems: [],
    rawText: '',
    lastScanAt: Date.now(),
    _stub: true  // marker for stub correctness test
  };
}

// E.2.1: stub. Real impl ships in E.2.2 reading dispatch_results.page_type per page.
function classifyPage(page) {
  return {
    kind: 'OTHER',
    scores: {},
    confidence: 'low',
    _stub: true
  };
}
```

The `_stub: true` marker is what the 2 new stub correctness tests assert against (D4 §3.4). It also makes a stub call grep-able in the file for E.2.2 to find and replace.

### §6.2 — Inlined functions from stripped TP namespace

Per D1 §4.4 gap resolution:

- `polygonArea(points)` — shoelace formula, ~8 lines, inlined as a standalone utility in Section 6 (Viewer) where annotation area calculation needs it
- `makePath(spec)` — minimal factory for TOOL_TESTS fixture construction; inlined in Section 9 (test section) only
- `DEFAULT_WASTE_FACTOR = 0.10` — inlined as a `const` at the top of Section 8 (Takeoff)

Choice for `makePath`: per Daniel directive (E.2.1 may resolve the D1 §4.4 alternate "or rewrite test fixtures to construct plain objects directly" decision in-session): **inline the factory.** Lower risk than rewriting fixtures; preserves the test logic exactly.

### §6.3 — Status bar polling implementation

Per D2 §5.5:

- `_healthState`, `_healthProbeInFlight`, `_healthIntervalId` module-level vars in Script block 1
- `probeHealth()` async — guards against in-flight; calls `apiClient.healthCheck()`; on success sets state to `connected` + updates version; on throw sets state to `unreachable`
- `setHealthState(state)` — pure DOM update of `#sbHealthDot`, `#sbApiStatus`, `#sbApiState`
- `startHealthPolling()` — initial probe + `setInterval(probeHealth, HEALTH_POLL_INTERVAL_MS)`
- Boot IIFE calls `startHealthPolling()` after DOM ready

**Manual retry trigger** (D2 §5.2): on UNREACHABLE, the status bar's text becomes a clickable retry. Clicking calls `probeHealth()` directly. Implementation: add `onclick="probeHealth()"` to the `#sbApiStatus` span when state is `unreachable`; remove when state changes.

**API call failure cascade** (D2 §5.2 trigger 3): in E.2.1 only `healthCheck` is wired, so the cascade is trivially satisfied — `healthCheck` failures already trigger the state change. E.2.2 extends this to `createJob` / `getJob` failures triggering an immediate `probeHealth()` re-check.

### §6.4 — Tab index renumbering (Risk 3 mitigation)

Pipeline was tab 5 in v6.3.5 (8 tabs total, 0–7). After removal, tabs 6 (TESTS) and 7 (ABOUT) shift to 5 and 6. Implementation:

- Update tab markup `onclick="showTab(N)"` per D2 §2.4 table
- Update pane IDs: `#pane6` → `#pane5` (TESTS), `#pane7` → `#pane6` (ABOUT)
- Update the `_showTab_orig_v62` hook (v6.3.5 line 7314) — its existing `if (idx === 1)` / `if (idx === 2)` / `if (idx === 4)` checks for SCOPE / PAGES / TAKEOFF stay correct (those are below the removed Pipeline tab). Any check for `idx === 5` / `6` / `7` must update to the new indices.
- Grep all `showTab(` calls in the new file and confirm targets are correct.

---

## §7 — Step E2.1.4: Re-baseline frontend test floor 138 → 20

Per `E2_0_TEST_FLOOR_PROPOSAL.md` §4.4:

| Category | Source | Count |
|---|---|---:|
| Surviving TOOL_TESTS | Ported from v6.3.5 lines 4565–4723 (11 of 15 — minus 4 pipeline-dependent tests) | 11 |
| New status-bar tests | D4 §3.2 — 3 unit tests on `setHealthState` state transitions | 3 |
| Ported takeoff tests | D4 §3.3 — 4 tests on `buildTakeoffModel` with hardcoded scope fixtures replacing the stripped `extractScope` dependency | 4 |
| New stub tests | D4 §3.4 — 2 tests asserting stub `extractScope` and stub `classifyPage` return correct shapes | 2 |
| **Total E.2.1 floor** | | **20** |

**Karpathy procedure for tests in this phase:**

1. Define the 20 tests in the new file as you build it. The 11 ported TOOL_TESTS should pass immediately (their dependencies are inlined per §6.2). The 3 status-bar tests should pass once §6.3 is wired. The 4 takeoff tests should pass once Section 8 is built. The 2 stub tests should pass once §6.1 stubs are in place.
2. After the new file is complete, run `npm test` against the new path. Floor: **20 / 20 passed, 0 failed**.
3. Hard stop if any test fails. The strip is destructive; debugging mid-strip is faster than discovering a broken test at gate-report time.

### §7.1 — `package.json` test script update

Single change to `frontend/package.json`:

```json
"test": "node run_tests.js src/Huckleberry_AI_phase2.v1.0.0.html"
```

(was `"node run_tests.js Huckleberry_AI_6.3.5_Scope.html"`)

The runner itself (`frontend/run_tests.js`) needs no structural change — it hoists `UNIT_TESTS` and `INTEGRATION_TESTS` via `window.__TESTS__`, and the new file defines those same global arrays.

The `test:spotchecks` and `test:mutations` scripts in `package.json` are noted as "soft observation" debt in BLOCK_RUN.md Phase 5 (E.0). E.2.1 deals with them: **either remove the entries from package.json or update them to point at the new file.** Recommended: remove. The mutation tests targeted v6.3.5 specifically and are stale architecture; spotchecks targeted moved-to-archive HTMLs and are obsolete. If Daniel wants them resurrected for the new file, that's E.3 territory.

---

## §8 — Step E2.1.5: Add corrigendum to E0_API_DESIGN.md (CHECKING vs DEGRADED)

Per Daniel directive 2026-04-30: append one corrigendum to the existing `backend/E0_API_DESIGN.md` §5.12 "Corrigenda" section (where E.1's two corrigenda already live).

**Corrigendum text to append:**

```
### Corrigendum 2026-04-30 (3) — CHECKING replaces DEGRADED in E.2.0/E.2.1 status bar spec

**What changed:** E.2.0's `E2_0_NEW_FILE_DESIGN.md` §5 specifies a 3-state status bar with states
CHECKING / CONNECTED / UNREACHABLE. The original E.0 planning conversation locked DEGRADED as the
third state (CONNECTED / DEGRADED / UNREACHABLE). The shipped design replaces DEGRADED with CHECKING.

**Reason:** With no auth and permissive CORS in E.1/E.2, no realistic DEGRADED scenario exists.
The "backend reachable but unhealthy" case the DEGRADED state was meant to capture (e.g., 503
from auth-rejecting middleware) does not arise pre-security-phase. CHECKING captures the genuinely
useful "first 30s before /health responds" transition state, which the original 3-state design
omitted.

**Forward note:** When auth + CORS lockdown ship in the Postgres/security phase, DEGRADED gets
re-evaluated as part of that phase. The 503-style "reachable but rejecting" case is a real
diagnostic surface once auth exists. At that point either: (a) DEGRADED is added as a 4th state,
or (b) UNREACHABLE is split into UNREACHABLE/REJECTING, or (c) the security phase produces a
different state machine entirely. Decision deferred to that phase's own march orders.

**Canonical going forward (through E.2 + E.3):** 3 states are CHECKING / CONNECTED / UNREACHABLE
per `E2_0_NEW_FILE_DESIGN.md` §5.
```

**Style note:** match the format of the existing corrigenda 1 (404 body) and 2 (version string) in §5.12. Do not create a new top-level file for this; append to the existing section.

---

## §9 — Step E2.1.6: Update canon

Surgical edits only.

### `PROJECT_CLAUDE.md`

**§3 (state paragraphs, chronological order):** append a new paragraph after the E.2.0 paragraph documenting E.2.1 completion. Pattern per prior phases: branch, what shipped, sacred floor transition (138 → 20 frontend, backend unchanged), receipts.

**§7 (phase table):** update the E.2.1 row from `NEXT-eligible` to `COMPLETE 2026-04-30` with branch + receipt references. E.2.2 becomes `NEXT-eligible` (was "Available after E.2.1"). E.2.debug and E.2.hard-gate stay as scheduled.

**No other section is touched.**

### `backend/BLOCK_RUN.md`

Append **Phase 8 — E.2.1 strip + new file + v6.3.5 archival** section. Match the template used by Phase 7 (Files created / modified / deleted, Commits, Pushes, Dependency / config changes, Vault-ruled files touched, Frontend touched, CLAUDE.md, Sacred floor at session end, §10 stops fired, Key design decisions). Phase 9 placeholder reserved for E.2.2.

### `safe_for_removal/MANIFEST.md`

One-row addition documenting v6.3.5's move + reason + replacement file path.

---

## §10 — Step E2.1.7: Gate report

Final deliverable: `backend/E2_1_GATE_REPORT.md`. Contents:

§1 — Pre-flight results (test floors, SHA-1 captures, branch verification).
§2 — Done-definition checklist (§14 of this doc) — every item PASS / FAIL with evidence.
§3 — §11 stop conditions — explicit non-firing status with evidence per stop.
§4 — Sacred floors at session end (backend 222/19/0 unchanged; frontend new floor 20/20; vault SHA-1s match; v6.3.5 SHA-1 match — file content unchanged after move).
§5 — Wall-clock summary per E2.1.X step.
§6 — Deliverables produced (file paths + brief description).
§7 — Manual smoke verification (the new file loads in a browser without JS errors; status bar cycles CHECKING → CONNECTED or CHECKING → UNREACHABLE depending on uvicorn state; this is observed in dev, not a hard gate).
§8 — Open items for Daniel review before E.2.2 march orders draft.

**Note on manual smoke:** E.2.1 is the strip phase, not the connect phase. The manual smoke at gate time is "does the file open in Chrome and not throw JS errors at boot" — a sanity check, not the hard gate. The Silverleaf upload-to-display end-to-end hard gate is E.2.hard-gate, which runs after E.2.debug.

---

## §11 — Step E2.1.8: Commit and push

Single commit. Files in commit:

**Created:**
- `frontend/src/Huckleberry_AI_phase2.v1.0.0.html` (NEW — the strip-and-rebuild deliverable)
- `backend/E2_1_GATE_REPORT.md` (NEW — gate report)

**Modified:**
- `frontend/package.json` (`test` script repointed; potentially `test:spotchecks` and `test:mutations` removed per §7.1)
- `backend/E0_API_DESIGN.md` (§5.12 corrigendum 3 appended)
- `PROJECT_CLAUDE.md` (§3 paragraph + §7 phase table E.2.1 row → COMPLETE)
- `backend/BLOCK_RUN.md` (Phase 8 section appended)
- `safe_for_removal/MANIFEST.md` (one row added)

**Renamed (via `git mv`):**
- `frontend/Huckleberry_AI_6.3.5_Scope.html` → `safe_for_removal/frontend_versions/Huckleberry_AI_6.3.5_Scope.html`

**Deleted:** None. (v6.3.5 is moved, not deleted.)

Commit message: `E.2.1 strip: phase2.v1.0.0.html shipped + v6.3.5 archived + frontend floor 138 → 20`

Push to origin.

---

## §12 — Sacred floors to hold

| Check | Pre-session value | Post-session expectation |
|---|---|---|
| Backend tests | `222 passed, 19 skipped, 0 failed` | unchanged (no backend code touched) |
| Frontend tests (against v6.3.5) | `138/138 passed` | **N/A — v6.3.5 retired** (verified ONE LAST TIME at pre-flight, then floor retires) |
| Frontend tests (against new file) | n/a (new file doesn't exist yet) | **`20 / 20 passed, 0 failed`** |
| Vault SHA-1: `roofing_module.py` | `ae9e5b28…` | unchanged |
| Vault SHA-1: `glazing_module.py` | `52c01442…` | unchanged |
| Vault SHA-1: `roofing_vocabulary.py` | `ec6c17f8…` | unchanged |
| Vault SHA-1: `glazing_vocabulary.py` | `64249c8e…` | unchanged |
| Vault SHA-1: `debug_module.py` | `78f71d90…` | unchanged |
| v6.3.5 file content SHA-1 | `cf3765d6…` | unchanged (file moved, content unchanged) |
| `backend/api/main.py` SHA-1 | (capture pre-session) | unchanged |
| `backend/api/routes/jobs.py` SHA-1 | (capture pre-session) | unchanged |
| `backend/api/schemas/jobs.py` SHA-1 | (capture pre-session) | unchanged |
| `git diff backend/core/` | empty | empty |
| `git diff backend/api/` | empty | empty |
| `git diff backend/tests/` | empty | empty |
| `git diff backend/scripts/` | empty | empty |
| `pyproject.toml` | unchanged | unchanged |
| `package.json` deps | unchanged | unchanged (only `test` script field updated) |
| CLAUDE.md opened | no | no |

Any drift on any row → §11 stop.

---

## §13 — Stop conditions (any → halt + report, do not proceed)

1. Sacred floor regresses (backend < 222/19/0 OR pre-flight v6.3.5 floor < 138/138 OR new-file floor < 20/20).
2. Any vault-ruled module SHA-1 changes.
3. v6.3.5 file content SHA-1 changes (move via `git mv` preserves content; if it changes, something else happened — STOP).
4. Any of the three E.1 production-code SHA-1s change (`backend/api/main.py`, `routes/jobs.py`, `schemas/jobs.py`).
5. CLAUDE.md gets opened or edited.
6. Any code change in `backend/` source files.
7. `pyproject.toml` modified.
8. `package.json` `dependencies` or `devDependencies` modified (only the `test` script field is in scope).
9. Any new dependency added (Python or npm).
10. Strip exceeds the 14 targets in `E2_0_STRIP_PLAN.md` §1. If new pipeline-related code is found that wasn't in the strip plan, document the finding and STOP — do not creatively expand.
11. Frontend test count at session end ≠ 20 (e.g., a test was added that's not one of the 20 specified, or one of the 20 is missing).
12. Status bar polling broken at session end (manual smoke: open the file in Chrome, watch the status bar — must show CHECKING for ~1 second then transition to CONNECTED if uvicorn is running OR UNREACHABLE if not).
13. Manual annotation tools broken at session end (manual smoke: open the file in Chrome, load any small PDF, drop a pin in the viewer; pin must place at click coordinates).
14. Any `apiClient` method other than `healthCheck` is wired to a real backend call (E.2.2 territory; E.2.1 stubs everything else).
15. PROJECT_CLAUDE.md edits exceed §3 paragraph + §7 phase table scope.
16. The CHECKING/DEGRADED corrigendum doesn't land in `E0_API_DESIGN.md §5.12` per §8 above.
17. Push to origin fails.

---

## §14 — Karpathy procedure conformance

E.2.1 is destructive — strip + new file. Karpathy compliance:

1. **Read first.** All four E.2.0 deliverables in full per §2. v6.3.5 read for strip targets. API design + E.1 receipts read for apiClient implementation.
2. **Failing tests first.** The 20 tests are defined in the new file as it's built. The 11 ported TOOL_TESTS pass immediately (dependencies inlined per §6.2). The 13 new tests (3 status-bar + 4 takeoff + 2 stub + 4 ported takeoff = 13) are written before the implementations they target, then made to pass.
3. **Minimum implementation.** Only what D1/D2/D3/D4 specify. No "while we're in there" additions.
4. **Sacred floors held** at every verification point: pre-flight (138/138 + 222/19/0), mid-build (TOOL_TESTS pass after dependencies inlined), end-of-build (20/20 + 222/19/0).
5. **§11 stops** when something genuinely uncertain. Don't extrapolate; document and stop.

The B-16/17/18 anti-pattern (speculation patches without diagnostics) is the explicit thing-to-avoid: if the new file boots with a JS error, the response is to STOP, capture the error, and document — not to patch speculatively until it boots clean.

---

## §15 — Vault rule enforcement

Five trade modules + the three E.1 production-code files have SHA-1s captured at pre-flight, verified at session end. v6.3.5's content SHA-1 also verified post-move (move preserves content; `git mv` doesn't modify bytes).

E.2.1 doesn't open vault-ruled modules. It opens v6.3.5 read-only (for the strip walk), then moves it.

---

## §16 — Done-definition checklist

| # | Item | Verified by |
|---|---|---|
| 1 | Pre-flight: 222/19/0 backend, 138/138 frontend (last time), all SHA-1s captured | E2.1.0 |
| 2 | Branch `phase2-v0.3-E2-1-strip` from `a1c804c` | E2.1.1 |
| 3 | v6.3.5 moved to `safe_for_removal/frontend_versions/` via `git mv` (content SHA-1 preserved) | E2.1.2 |
| 4 | `frontend/src/Huckleberry_AI_phase2.v1.0.0.html` created per D2 design | E2.1.3 + E2.1.4 |
| 5 | All 14 strip targets from D1 §1 are absent from new file (grep confirmation: no `TP.run`, no `ROOF_VOCAB`, no `extractScope` real impl, no `classifyPage` real impl, no `STAGE_META`, no `buildSyntheticPlan`, no `visualize`, no `runPipeline`, no Pipeline tab markup, no SCOPE_TESTS, no SCOPE_INTEGRATION_TESTS, no operator-list walker) | E2.1.4 |
| 6 | `extractScope` and `classifyPage` exist as stubs returning `_stub: true` per §6.1 | E2.1.4 |
| 7 | `polygonArea`, `makePath`, `DEFAULT_WASTE_FACTOR` inlined per §6.2 | E2.1.4 |
| 8 | Status bar 3-state polling implemented per §6.3 (CHECKING/CONNECTED/UNREACHABLE) | E2.1.4 |
| 9 | `apiClient` skeleton: `healthCheck` real; `createJob` / `getJob` / `listJobs` / `getResults` / `dispatchJob` all stubs throwing | E2.1.4 |
| 10 | Tab indices renumbered per §6.4; all `showTab(` calls validated | E2.1.4 |
| 11 | 20 tests defined in new file; `npm test` reports 20/20 passed, 0 failed | E2.1.5 |
| 12 | `package.json` `test` script repoints to new file; obsolete `test:spotchecks` / `test:mutations` either removed or repointed per §7.1 | E2.1.5 |
| 13 | `backend/E0_API_DESIGN.md §5.12` has corrigendum 3 (CHECKING vs DEGRADED) appended per §8 | E2.1.6 |
| 14 | `PROJECT_CLAUDE.md` §3 paragraph + §7 phase table updated; no other sections touched | E2.1.6 |
| 15 | `backend/BLOCK_RUN.md` Phase 8 section appended; Phase 9 placeholder reserved | E2.1.6 |
| 16 | `safe_for_removal/MANIFEST.md` updated with v6.3.5 row | E2.1.6 |
| 17 | Sacred floors at session end: backend 222/19/0; frontend 20/20 against new file; vault SHA-1s + v6.3.5 content SHA-1 + 3 E.1 file SHA-1s all match pre-session | E2.1.7 |
| 18 | `git diff` against `backend/core/`, `backend/api/`, `backend/tests/`, `backend/scripts/`, `pyproject.toml` all empty | E2.1.7 |
| 19 | Manual smoke: new file opens in Chrome, status bar cycles correctly, annotation tools place pins at click coordinates (informal verification, documented in gate report §7) | E2.1.7 |
| 20 | CLAUDE.md not opened during session | E2.1.7 |
| 21 | `backend/E2_1_GATE_REPORT.md` produced; all §11 stop conditions explicitly confirmed non-firing | E2.1.7 |
| 22 | Single commit on branch with files per §11 | E2.1.8 |
| 23 | Commit pushed to origin | E2.1.8 |

---

## §17 — Estimated wall-clock

| Step | Estimated |
|---|---|
| E2.1.0 pre-flight (backend tests, v6.3.5 tests one last time, SHA-1s) | ~3 min |
| E2.1.1 branch | <30 sec |
| E2.1.2 v6.3.5 git mv to safe_for_removal/ | ~2 min |
| E2.1.3 new file scaffold (header + body markup + 7-tab structure + status bar + sidebar) | ~30–40 min |
| E2.1.4 strip targets removed + stubs + inlined functions + status bar polling + apiClient skeleton + tab renumbering (the heaviest step) | ~90–120 min |
| E2.1.5 test re-baseline (define 20 tests, run, 20/20 PASS) + package.json update | ~30–40 min |
| E2.1.6 corrigendum + canon updates (PROJECT_CLAUDE.md + BLOCK_RUN.md + MANIFEST.md) | ~10 min |
| E2.1.7 manual smoke verification + gate report | ~15 min |
| E2.1.8 commit + push | ~3 min |
| **Total** | **~3 to 4 hours** |

This is the largest single session in Phase E. If wall-clock exceeds 5 hours and the new file isn't yet at 20/20 floor, **STOP** and document; don't push past discipline timeline. A 5-hour soft ceiling forces honest scope assessment vs. quiet creep.

---

## §18 — What ships at end of E.2.1

A working, browser-loadable, 20-test-passing single-file HTML at `frontend/src/Huckleberry_AI_phase2.v1.0.0.html`. The file is *destructively complete* — pipeline JS gone, scope JS stubbed, status bar polling live, manual annotation tools intact. It does NOT yet talk to the backend for any data beyond `/health`.

After Daniel reviews:

- **If E.2.1 looks clean:** Daniel green-lights E.2.2. Extended-thinking Claude drafts E.2.2 march orders. E.2.2 wires `createJob` + `getJob` to real implementations, populates Scope tab + Pages tab from API data, adds the 5 API smoke tests bringing floor 20 → 25.
- **If something needs adjustment:** Daniel flags it; small follow-up commit on the same E.2.1 branch (or a sibling fix branch) before E.2.2 starts. Common adjustments expected: a strip cut needs revising (a kept tool depended on something marginal), an inlined function has a bug, a tab index missed an update, the corrigendum text needs editing.

Soft-gate-with-Daniel-review is the rule for every E sub-phase.

---

## §19 — Reminder: Daniel's locked decisions feeding E.2.1

| Q | Locked answer | Where it lives in this phase |
|---|---|---|
| Q1 | v6.3.5 → safe_for_removal/frontend_versions/; 138/138 floor retires; new floor TBD by E.2.0 | §5 (the move) + §7 (the new floor: 20) |
| Q2 | New file: `frontend/src/Huckleberry_AI_phase2.v1.0.0.html`; single-file HTML | §6 (build target) |
| Q3 | Five-sub-phase E.2; E.2.1 is the destructive sub-phase; E.2.2 / E.2.debug / E.2.hard-gate follow | §0 + §18 |
| Q4 | Confirmed keepers + strips per E.2.0 D1 §2/§3; pipeline tab strikes; manual annotation tools preserved | §6 + §13 stop #10 |
| Q5 | Vanilla fetch; hardcoded API_BASE; no auth; thin wrapper with stub slots; apiCall() helper | §6 + D3 spec |
| Q6 | Dynamic status bar; 30s + page-load + on-failure triggers; **3 states per E.2.0/E.2.1: CHECKING/CONNECTED/UNREACHABLE** (DEGRADED dropped per directive 2026-04-30, corrigendum landing this phase per §8) | §6.3 + §8 |

---

**End of MARCH ORDERS — Phase E.2.1.**

Daniel green-lights → Claude Code executes. Single autonomous session. Soft gate to E.2.2 after.
