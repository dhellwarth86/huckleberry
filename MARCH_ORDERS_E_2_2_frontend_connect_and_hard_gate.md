# MARCH ORDERS — Phase E.2.2: Frontend Connect + Silverleaf Hard Gate

**Date issued:** 2026-05-01
**Issued by:** Daniel (via extended-thinking Claude General planning session)
**Executed by:** Claude Code
**Phase shape:** Single autonomous big-block session, three soft gates, one hard gate, soft-gates pause between sub-steps. Collapses prior E.2.2 + E.2.debug + E.2.hard-gate into one phase per Daniel directive 2026-05-01.
**Phase scope:** Wire `apiClient.createJob` + `getJob` + `dispatchJob` + `getResults` to live backend. Add two new backend endpoints (`POST /jobs/{id}/dispatch` + `GET /jobs/{id}/results`). Populate Scope tab from `trade_outputs`; populate Pages tab from `dispatch_results.page_type`. Add 5 API smoke tests (frontend) + 6–8 endpoint tests (backend). Re-run Silverleaf via the API, read debug module output against calibration baseline, then end-to-end visual hard gate in browser.
**Read first:** PROJECT_CLAUDE.md, backend/BLOCK_RUN.md, then this document, then the four E.2.0 design deliverables, then `backend/E2_1_GATE_REPORT.md`, then `backend/CALIBRATION_GATE_REPORT_silverleaf.md` + `backend/D2_REFERENCE_silverleaf.md`.

---

## §0 — What this phase is

E.2.2 is the connect phase. The strip phase (E.2.1) shipped a frontend with `healthCheck` real and five `apiClient` methods stubbed. E.2.2 wires four of those five (createJob / getJob / dispatchJob / getResults) to a live backend and proves the end-to-end loop on Silverleaf.

Five concrete things happen, in order:

1. **Two new backend endpoints ship.** `POST /jobs/{id}/dispatch` triggers `run_dispatch(pdf_path, storage="auto", job_id=...)` synchronously — returns 200 OK with the updated `JobResponse` when complete. `GET /jobs/{id}/results` returns `{dispatch_results, trade_outputs}` from the SQLite tables D.2 wrote. Both are reserved per `E0_API_DESIGN.md §5.3`.
2. **Backend test coverage extends.** ~6–8 new tests in `backend/tests/test_api_jobs.py` covering happy + error paths for both endpoints. Backend floor 222 → 228–230.
3. **Frontend wires four apiClient methods to the live backend.** `createJob`, `getJob`, `dispatchJob`, `getResults` all become real `fetch()` calls per `E2_0_API_CLIENT_SPEC.md`. The 5 API smoke tests reserved in `E2_0_TEST_FLOOR_PROPOSAL.md §3.1` ship in the new file's TESTS section. Frontend floor 20 → 25.
4. **Scope and Pages tabs populate from API data.** Scope tab consumes `trade_outputs` (the fields, warnings, and systems the trade modules produced). Pages tab consumes `dispatch_results[i].page_type` to populate the ROOF_PLAN / DETAIL / SPEC / COVER / OTHER bucket counts and per-page badges. Both today render placeholder text — after E.2.2 they render real data.
5. **Silverleaf end-to-end runs through the browser.** Daniel pastes the local Silverleaf path, drag-drops the PDF (frontend renders pages client-side), the frontend POSTs `/jobs` then POSTs `/jobs/{id}/dispatch`, awaits ~140s for dispatch to complete, then GETs `/jobs/{id}/results` and renders. **Two soft gates and one debug-output soft gate fire before the visual hard gate.**

After all five things succeed and Daniel green-lights at each soft gate, E.2.2 ratifies as complete. Phase E.2 is then DONE — no E.2.debug or E.2.hard-gate sub-phases follow.

**Why these five and not more:** Daniel's 2026-05-01 directive collapsed the original 5-sub-phase E.2 into a single big-block E.2.2 ending in the bidset hard gate. The intermediate "debug" sub-phase is kept as a soft gate (debug module output read) rather than its own session, because the debug verification doesn't need code changes — it needs a script run + a human read of the output. Folding it into E.2.2 keeps the discipline shape without creating a separate session for a one-shot verification.

**Architectural commitments landing in canon:**

- **`POST /jobs/{id}/dispatch` is synchronous in E.2.2.** Returns when `run_dispatch` returns. Silverleaf's reference run is ~137.6s; that's the expected wait. Async + progress reporting is deferred to a later phase that handles user-traffic-class bidsets (Vine Street's 1195s cannot ship sync). E.2.2 is single-bidset on Silverleaf — sync is appropriate scope.
- **`pdf_path` stays a string parameter.** No multipart upload in E.2.2. The frontend exposes a `Server file path` text field on the New Session tab; Daniel pastes the local Silverleaf path. File upload via multipart is deferred per `E0_API_DESIGN.md §5.8`.
- **Job status enum extends.** `'draft'` (after create, before dispatch) → `'dispatching'` (briefly, while dispatch is in flight — set by the endpoint at start) → `'dispatched'` (after `mark_dispatch_complete` runs). The intermediate `'dispatching'` state is added so a second client GET-ing `/jobs/{id}` mid-dispatch sees the in-progress state. Pydantic `Literal[...]` extends accordingly.
- **`apiClient.listJobs` stays stubbed.** `GET /jobs` is reserved for a later phase. Same stub-throws-`not_implemented_in_e2_2` pattern E.2.1 used; no behavior change.

---

## §1 — What this phase is NOT

**OUT OF SCOPE for E.2.2:**

- **`GET /jobs` (list jobs).** Reserved for a later phase. `apiClient.listJobs` keeps the E.2.1 stub, with the error string updated from `not_implemented_in_e2_1` → `not_implemented_in_e2_2`.
- **`PUT /jobs/{id}` / `PATCH /jobs/{id}/status`.** Job metadata updates beyond the dispatch lifecycle. Not E.2.2.
- **`POST /jobs/{id}/annotations`.** Annotation save/load. Phase F territory.
- **`GET /jobs/{id}/debug`.** The debug-module endpoint sketch in `E0_API_DESIGN.md §5.3`. Not in E.2.2 — debug verification happens via in-process script (§11), not via a frontend endpoint.
- **Multipart file upload.** Deferred per `E0_API_DESIGN.md §5.8`. Frontend exposes a `Server file path` text field; Daniel pastes the path.
- **Async dispatch / background tasks / progress reporting.** Sync POST that blocks until done. Frontend shows a "dispatching" UI state but does not poll.
- **Auth / CORS lockdown / OpenAPI hidden in production.** Security cluster, post-user-testing. Permissive CORS stays.
- **Postgres migration.** SQLite stays.
- **Phase G optimizations (PyMuPDF, Pandas, tiling).** Separate phase.
- **Phase F annotation lifecycle.** Separate phase.
- **3-bidset benchmarking.** Single-bidset Silverleaf only. Multi-bidset re-runs are post-Phase G.
- **Vault-ruled module changes.** All five trade modules + debug module untouched.
- **`safe_for_removal/` cleanout.** Daniel personally empties post-E.2.2 ratification, saved outside the project. **Claude Code does NOT touch `safe_for_removal/` in E.2.2** beyond the standard MANIFEST.md row append (if anything new is archived, which is unlikely).
- **CLAUDE.md.** Retired, do not open.
- **Cosmetic UI polish on stubs that aren't fully integrated.** Per Daniel directive 2026-05-01: do NOT polish pin/polygon/rectangle finalize behavior for "no system" edge cases beyond what wiring `getResults` naturally fixes. The post-wiring system dropdown populates from real scope; tools then attach correctly. If anything still misbehaves after wiring, document for a later phase — do not patch speculatively. (B-16/17/18 anti-pattern defense.)
- **`pyproject.toml` changes.** No new Python deps. fastapi / uvicorn / pydantic already in from E.1.
- **`package.json` `dependencies` changes.** Browser uses native `fetch()`. The `test` script field stays as E.2.1 set it.

---

## §2 — Pre-flight reads (Karpathy step 1)

Full reads, in this order:

1. **PROJECT_CLAUDE.md** — entry point. §3 paragraphs through E.2.1 (most recent); §7 phase table; §4 discipline; §6 misconceptions.
2. **`backend/BLOCK_RUN.md`** — Phase 8 (E.2.1). Phase 9 placeholder is the row E.2.2 fills in.
3. **`VALIDATION_LEDGER.md`** — sacred floors, vault list.
4. **`backend/E0_API_DESIGN.md`** — full read. Especially §5.2 (E.1 endpoints — pattern E.2.2's two new endpoints follow), §5.3 (the dispatch + results sketches you are now implementing), §5.7 (test strategy template), §5.9 (forward-compat shape commitments — `pdf_sha1` in responses, ISO 8601 datetimes with timezone, snake_case throughout, Literal status enum), §5.12 (corrigenda — append corrigendum 4 if E.2.2 ships any spec deviation).
5. **`backend/E1_GATE_REPORT.md`** + **`backend/E1_HARD_GATE_silverleaf_api.md`** + **`backend/E1_UVICORN_SMOKE.md`** — what E.1 actually shipped on the wire. Match the pattern.
6. **`backend/E2_0_NEW_FILE_DESIGN.md`** — full read. Especially §4 (script-block ordering — wire goes into script block 1 next to the other apiClient methods) and §5 (status bar polling — extends with on-failure trigger now that `createJob` / `dispatchJob` failures count as cascade triggers per D2 §5.2 trigger 3).
7. **`backend/E2_0_API_CLIENT_SPEC.md`** — full read. §1 skeleton, §2 apiCall helper, §3 real method shapes, §4 stub pattern (you are converting 4 of 5 stubs to real), §5 error matrix.
8. **`backend/E2_0_TEST_FLOOR_PROPOSAL.md`** — full read. §3.1 (the 5 API smoke tests — these ship now), §5.2 (SKIP convention — already wired into runTestBatch in E.2.1; verify it still works when uvicorn is unreachable).
9. **`backend/E2_1_GATE_REPORT.md`** — what E.2.1 shipped, the §8 open items list (especially items 3 and 4 — the ones E.2.2 closes).
10. **`backend/CALIBRATION_GATE_REPORT_silverleaf.md`** — Silverleaf calibration baseline. The debug-soft-gate compares against the numbers in this report.
11. **`backend/D2_REFERENCE_silverleaf.md`** — Silverleaf D.2 reference run (job_id, dispatch wall-clock, module output counts). The soft-gate comparison numbers also live here.
12. **`backend/api/main.py`** + **`backend/api/routes/jobs.py`** + **`backend/api/schemas/jobs.py`** — read fully. E.2.2 extends both `routes/jobs.py` (two new endpoints) and `schemas/jobs.py` (one or two new response models). `main.py` is unchanged.
13. **`backend/core/dispatch_gate.py`** lines around `run_dispatch` — read the D.2-tagged extension (lines 229–231 per BLOCK_RUN). Confirm signature: `run_dispatch(pdf_path, storage="auto", job_id=None)`. The new `/dispatch` endpoint calls this directly.
14. **`backend/core/job_storage.py`** — full read. `create_job`, `get_job`, `update_job_status`, `mark_dispatch_complete`, plus the `dispatch_results` and `trade_outputs` table accessors. `GET /jobs/{id}/results` calls these.
15. **`backend/core/debug_module.py`** — read-only walkthrough. Vault-ruled; no edits. Confirm `run_debug(ctx)` signature. The debug-soft-gate script invokes this on the in-memory ctx after a fresh dispatch.
16. **`backend/scripts/d2_silverleaf_reference.py`** — read fully. The debug-soft-gate script (§11) is structured as a sibling: same `run_dispatch` invocation, with `debug_module.run_debug(ctx)` called immediately after, and structured output written.
17. **`frontend/src/Huckleberry_AI_phase2.v1.0.0.html`** — read sections containing `apiClient`, `extractScope`, `classifyPage`, `renderScopeTab`, `renderPagesTab`, the New Session tab markup, and the test harness. These are the surfaces E.2.2 modifies.

**Do NOT open:**
- Five vault-ruled trade modules + `debug_module.py` (read-only walkthrough only — no edits).
- `CLAUDE.md` (retired).
- Files in `safe_for_removal/` (Daniel's cleanout — out of scope).
- v6.3.5 in its archived location (don't reopen the corpse).

---

## §3 — Step E2.2.0: Pre-flight verification

Establish the floor before any code changes.

- Run full backend suite. Floor: **222 passed, 19 skipped, 0 failed**. Hard stop if not met.
- Run frontend suite against new file. Floor: **20/20 passed**. Hard stop if not met.
- Capture pre-session SHA-1s for all 5 vault-ruled modules + `debug_module.py` (already vault-ruled — confirm SHA-1 `78f71d9030cde3b173389603f5f39bd6bedaac07`).
- Capture pre-session SHA-1s for the 3 E.1 production-code files (`backend/api/main.py`, `routes/jobs.py`, `schemas/jobs.py`). E.2.2 modifies `routes/jobs.py` and `schemas/jobs.py`; `main.py` should remain unchanged. Capture them all so the gate report can verify `main.py` non-drift.
- Capture pre-session SHA-1 for `frontend/src/Huckleberry_AI_phase2.v1.0.0.html` (E.2.2 will modify this file; capture for the diff record only).
- **`git status` check.** Daniel's 2026-04-30 session left untracked workspace deletions/moves outside the E.2.1 commit. Document the working-tree state in the gate report. Do NOT stage anything not in the E.2.2 deliverable list (§17). If untracked files cause confusion, stash them.
- Verify branch state: head matches commit `4f7c90f` per BLOCK_RUN Phase 8.
- Confirm `git remote -v` shows `https://github.com/dhellwarth86/huckleberry.git`.
- Verify `pyproject.toml` already has fastapi / uvicorn / pydantic from E.1. No new deps in E.2.2 — confirm at start so any drift mid-session is immediately visible.

Pre-flight failure → §19 stop, no work begins.

---

## §4 — Step E2.2.1: Branch

```
phase2-v0.3-E2-2-frontend-connect-and-hard-gate  (NEW; from E.2.1 head 4f7c90f)
```

Single commit at end of session. Pushed.

---

## §5 — Step E2.2.2: Backend — `POST /jobs/{id}/dispatch`

Add the dispatch trigger endpoint to `backend/api/routes/jobs.py`. Pattern matches E.1's existing endpoints exactly.

**Behavior:**

1. Look up the job by id via `get_job`. 404 if missing.
2. If `status == 'dispatched'`: return 200 with the existing `JobResponse` (idempotent — dispatching twice returns the existing results, does NOT re-dispatch). Document this in the docstring.
3. If `status == 'dispatching'`: return 409 Conflict with `{"detail": "Dispatch already in progress"}`. Defensive — sync mode shouldn't see this in practice but covers a hung-process case.
4. Otherwise: set `status='dispatching'` via `update_job_status`. Then call `run_dispatch(pdf_path=job['pdf_path'], storage="auto", job_id=job_id)`. The D.2-wired persistence runs inside `run_dispatch` — it persists `dispatch_results` + `trade_outputs` and calls `mark_dispatch_complete(job_id)` on success.
5. Return 200 with the updated `JobResponse` (re-fetched after `mark_dispatch_complete`).

**Pydantic schema:** No new request body — the endpoint takes only the path parameter `job_id`. Response is `JobResponse` (existing schema, no shape change).

**Status enum extension:** `backend/api/schemas/jobs.py` Literal for `status` extends to include `'dispatching'`. Backend `_VALID_STATUSES` in `core/job_storage.py` likely already includes `'dispatching'` (verify); if not, that's a STOP — adding to the enum is a vault-adjacent change that needs Daniel approval before it lands.

**Error responses:**

| Status | Trigger | Body |
|---|---|---|
| 200 | Dispatch complete (or idempotent re-call on already-dispatched job) | `JobResponse` with `dispatch_complete: true` |
| 404 | Job not found | `{"detail": "Job not found"}` (matches E.1 corrigendum 1 — opaque, no echo) |
| 409 | Dispatch already in progress | `{"detail": "Dispatch already in progress"}` |
| 400 | `pdf_path` no longer exists on disk (file moved/deleted between create and dispatch) | `{"detail": "pdf_path not found"}` (opaque — no path echo) |
| 500 | `run_dispatch` raised | `{"detail": "Internal server error"}` (do NOT echo the exception text — log it server-side via stdlib logging) |

**Implementation sketch (~30–40 lines):**

```python
@router.post("/{job_id}/dispatch", response_model=JobResponse)
def dispatch_job_endpoint(job_id: str) -> JobResponse:
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if job["status"] == "dispatched":
        return JobResponse(**job)  # idempotent
    if job["status"] == "dispatching":
        raise HTTPException(status_code=409, detail="Dispatch already in progress")
    if not Path(job["pdf_path"]).exists():
        raise HTTPException(status_code=400, detail="pdf_path not found")
    update_job_status(job_id, "dispatching")
    try:
        run_dispatch(pdf_path=job["pdf_path"], storage="auto", job_id=job_id)
    except Exception:
        logger.exception("dispatch failed for job_id=%s", job_id)
        # Reset status so a retry is possible
        update_job_status(job_id, "draft")
        raise HTTPException(status_code=500, detail="Internal server error")
    refreshed = get_job(job_id)
    return JobResponse(**refreshed)
```

**Wall-clock note for the sync block:** Silverleaf's D.2 reference run was 137.6s. The `TestClient` in pytest must use a smaller fixture (the existing E.1 fixture PDF is single-page — dispatches in <5s). The Silverleaf run via this endpoint happens at the hard gate (§13), not in tests.

---

## §6 — Step E2.2.3: Backend — `GET /jobs/{id}/results`

Add the results-loader endpoint. Pattern matches the dispatch endpoint exactly for consistency.

**Behavior:**

1. Look up the job by id. 404 if missing.
2. If `status != 'dispatched'`: return 409 with `{"detail": "Job not yet dispatched"}`. Do NOT return partial / in-progress results.
3. Otherwise: read `dispatch_results` (per-page rows from the `dispatch_results` table) and `trade_outputs` (per-page rows from the `trade_outputs` table). Group by `page_idx` into the response shape `E0_API_DESIGN.md §5.3` sketches.

**Response shape (Pydantic schema `JobResultsResponse`, HTTP 200 OK):**

```json
{
  "job_id": "45d58c49-2e78-41d7-91c4-759a7a8de0de",
  "dispatch_results": {
    "0": { "page_idx": 0, "page_type": "COVER", "sheet_num": "G-001", ... },
    "1": { "page_idx": 1, "page_type": "ROOF_PLAN", "sheet_num": "A-101", ... }
  },
  "trade_outputs": {
    "0": { "roofing": null, "glazing": null },
    "1": { "roofing": { "fields": {...}, "warnings": [], "systems": [...] }, "glazing": null }
  }
}
```

**Field shape rules:**

- Keys of `dispatch_results` and `trade_outputs` are **string-encoded page indices** (`"0"`, `"1"`, ... `"37"` for Silverleaf). JSON object keys are always strings; this matches the §5.3 sketch and avoids a list/array shape change later.
- `dispatch_results[i]` is the raw SQLite row from the `dispatch_results` table — same field names as the SQLite columns. No reshape.
- `trade_outputs[i]` is `{"roofing": <row or null>, "glazing": <row or null>}`. If a page has no output for a trade, the value is `null`. If a page has output, the value is the `output_json` field deserialized (it's stored as a JSON string in SQLite per D.2's design).

**Errors:**

| Status | Trigger | Body |
|---|---|---|
| 200 | Results available | `JobResultsResponse` |
| 404 | Job not found | `{"detail": "Job not found"}` |
| 409 | Job exists but `status != 'dispatched'` | `{"detail": "Job not yet dispatched"}` |
| 500 | SQLite read failure | `{"detail": "Internal server error"}` |

**Implementation sketch (~40–50 lines including the new schema):**

```python
# In backend/api/schemas/jobs.py — new model:
class JobResultsResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    job_id: str
    dispatch_results: dict[str, dict]
    trade_outputs: dict[str, dict]

# In backend/api/routes/jobs.py — new endpoint:
@router.get("/{job_id}/results", response_model=JobResultsResponse)
def get_job_results_endpoint(job_id: str) -> JobResultsResponse:
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if job["status"] != "dispatched":
        raise HTTPException(status_code=409, detail="Job not yet dispatched")
    dispatch_rows = load_dispatch_results(job_id)  # from job_storage
    trade_rows = load_trade_outputs(job_id)        # from job_storage
    dispatch_by_page = {str(r["page_idx"]): r for r in dispatch_rows}
    trade_by_page: dict[str, dict] = {}
    for r in trade_rows:
        page_key = str(r["page_idx"])
        slot = trade_by_page.setdefault(page_key, {"roofing": None, "glazing": None})
        slot[r["trade"]] = json.loads(r["output_json"])
    # Ensure every page in dispatch_results has a corresponding trade_outputs entry (null fill)
    for page_key in dispatch_by_page:
        trade_by_page.setdefault(page_key, {"roofing": None, "glazing": None})
    return JobResultsResponse(
        job_id=job_id,
        dispatch_results=dispatch_by_page,
        trade_outputs=trade_by_page,
    )
```

If `load_dispatch_results` / `load_trade_outputs` don't already exist in `job_storage.py`, they need to be added — small additions, ~10–15 lines each. Read `job_storage.py` first to confirm what's there. **Adding read accessors to `job_storage.py` is in scope for E.2.2**; modifying its existing write accessors is NOT.

---

## §7 — Step E2.2.4: Backend tests

Add **6–8 new tests** to `backend/tests/test_api_jobs.py`. Pattern matches the existing E.1 tests in that file.

**Required tests:**

1. `test_dispatch_job_returns_200_after_dispatch` — POST /jobs with the small fixture PDF + POST /jobs/{id}/dispatch + assert response status 200, `dispatch_complete: true`, `status: 'dispatched'`.
2. `test_dispatch_job_404_for_unknown_id` — POST /jobs/<random-uuid>/dispatch → 404 with opaque body.
3. `test_dispatch_job_idempotent_on_second_call` — POST /jobs + POST /jobs/{id}/dispatch + POST /jobs/{id}/dispatch (twice) → both 200, second response equals first.
4. `test_dispatch_job_400_when_pdf_missing_at_dispatch_time` — POST /jobs with a path that exists, then delete the file, then POST /jobs/{id}/dispatch → 400.
5. `test_get_results_returns_200_after_dispatch` — POST /jobs + POST /jobs/{id}/dispatch + GET /jobs/{id}/results → 200 with non-empty `dispatch_results` and `trade_outputs` dicts.
6. `test_get_results_404_for_unknown_id` — GET /jobs/<random-uuid>/results → 404.
7. `test_get_results_409_when_not_dispatched` — POST /jobs + GET /jobs/{id}/results (without dispatch) → 409.
8. (optional) `test_get_results_response_shape_keys_are_string_indices` — verify that `dispatch_results.keys()` are all `str`, not `int` (forward-compat invariant per §5.9 #4).

**Fixture:** Use the existing small fixture PDF from E.1's `backend/tests/conftest.py` (or wherever it lives — read to confirm). Dispatch on a single-page synthetic PDF should complete in <5s, keeping the test suite fast.

**Backend floor:** 222 → **228** (6 required tests) to **230** (with the two optional). Set the floor as a window in the gate report: PASS if 228 ≤ count ≤ 230.

---

## §8 — SOFT GATE 1 — Backend ready

**Cannot proceed to frontend wiring until all of the following are true:**

- New endpoints implemented per §5 + §6.
- New tests in §7 all PASS. Backend test count in window 228–230.
- Existing 222 tests still PASS (no regression).
- 19 skipped tests still skipped (no skip leakage).
- Vault SHA-1s + 3 E.1 production-code SHA-1s + `debug_module.py` SHA-1 all match pre-session capture (read accessors added to `job_storage.py` are NOT vault-ruled, but `dispatch_gate.py` and the modules ARE — confirm zero diff against them).
- Uvicorn manual smoke (~2 min): start the server, hit the four endpoints from `curl` or browser, confirm response shapes match spec. New: hit `POST /jobs/{id}/dispatch` against a small fixture PDF; observe sync block; confirm response when complete. Hit `GET /jobs/{id}/results` after; confirm shape.
- `git status` shows only the expected modified + new files in the E.2.2 deliverable list — no scope creep into vault-ruled or unrelated files.

**Soft gate output:** Inline summary in the running gate report draft (§16) — no separate document. If any item fails: STOP, document, do not proceed to frontend.

---

## §9 — Step E2.2.5: Frontend — wire 4 apiClient methods

Modify `frontend/src/Huckleberry_AI_phase2.v1.0.0.html` Script Block 1. The `apiClient` object currently has `healthCheck` real and 5 stubs throwing `not_implemented_in_e2_1`. Convert four of those stubs to real:

- **`apiClient.createJob(payload)`** — `POST` to `${API_BASE}/jobs` with the payload as JSON body. Response is `JobResponse`. Errors: 400 (bad path), 422 (validation), 500 — surface to caller as a thrown `Error` with `{status, body}` attached for caller inspection.
- **`apiClient.getJob(jobId)`** — `GET ${API_BASE}/jobs/${encodeURIComponent(jobId)}`. Response is `JobResponse`. Errors: 404, 500.
- **`apiClient.dispatchJob(jobId)`** — `POST ${API_BASE}/jobs/${encodeURIComponent(jobId)}/dispatch` with empty body. Response is `JobResponse` with `dispatch_complete: true`. **This call may block for ~140s on Silverleaf** — the `apiCall` helper's `AbortController` timeout (currently 5000ms per `HEALTH_PROBE_TIMEOUT_MS`) MUST be overridden for this call. Add a per-call timeout option to the `apiCall` helper signature (e.g., `apiCall(method, path, {timeoutMs: 240000})`) and pass `240000` (4 minutes — Silverleaf headroom) for `dispatchJob`. Other calls keep the default. Errors: 404, 409, 400, 500.
- **`apiClient.getResults(jobId)`** — `GET ${API_BASE}/jobs/${encodeURIComponent(jobId)}/results`. Response is `JobResultsResponse`. Errors: 404, 409, 500.

**`apiClient.listJobs(filters)`** — stays stubbed. Update the error string from `not_implemented_in_e2_1: listJobs ships in E.2.2` to `not_implemented_in_e2_2: listJobs ships in a later phase`.

**Status bar on-failure trigger (D2 §5.2 trigger 3):** When any of `createJob` / `dispatchJob` / `getResults` throws a network error (caught in the apiCall helper as a fetch reject), call `probeHealth()` immediately to re-evaluate the connection state. Don't wait for the next 30s tick.

**Stub-marker removal:** Delete the two `extractScope` and `classifyPage` stubs entirely — they were E.2.1 placeholders for client-side scope inference that no longer happens. The Scope tab and Pages tab now consume API data via the new wiring; nothing calls these stubs anymore. Their 2 stub-correctness tests in the test harness retire (see §10 — replaced by the 5 API smoke tests, net floor change +3 not +5).

**WAIT — re-check that retirement.** The test floor proposal is: 20 (current) − 2 (retired stub tests) + 5 (new API smoke tests) = **23, not 25**. Daniel's earlier framing said "20 → 25" which assumed both stubs and stub-tests stayed. If the stubs go because nothing calls them, the tests must go too. **Recommended floor: 23.** If Daniel wants 25, keep the 2 stub tests as documentation of what those calls returned in E.2.1 — but that's vestigial, not value-add.

**General's call:** floor is **23**. Daniel ratifies in the soft-gate review. Document the deviation from "20 → 25" framing in the gate report §8 open items.

**New Session tab — Server file path field:**

Add a small text input to the New Session tab markup, between the trade selector (Step 1) and the drag-drop zone (Step 2):

```html
<div class="step-block">
  <div class="step-num">STEP 1.5</div>
  <div class="step-title">SERVER FILE PATH</div>
  <p class="step-help">Until file upload ships, paste the absolute path to the bidset on the machine running uvicorn. The drag-drop below renders pages client-side; the path tells the backend where to dispatch.</p>
  <input type="text" id="serverFilePathInput" placeholder="C:\path\to\bidset.pdf" class="path-field" />
</div>
```

Renumber STEP 2 to STEP 2 still (don't shift numbering — STEP 1.5 is intentionally interstitial, signals temporary). Style the input with the existing dark-theme conventions.

**Dispatch trigger flow:**

When all three preconditions are true — trade selected (Step 1), file dropped (Step 2 — frontend has the File object loaded into pdf.js), path entered (Step 1.5) — the New Session tab enables a "RUN DISPATCH" button (replace or sit alongside Step 3's existing "REVIEW SCOPE" button). On click:

1. Disable the button. Show a spinner / inline "DISPATCHING — this takes ~2 minutes" status.
2. Call `apiClient.createJob({name, pdf_path, trade_scope, ...})`.
3. On success, store `App.currentJobId`. Call `apiClient.dispatchJob(jobId)`.
4. On dispatch success, call `apiClient.getResults(jobId)`. Store the response on `App.currentResults`.
5. Re-render Scope tab (consumes `App.currentResults.trade_outputs`) and Pages tab (consumes `App.currentResults.dispatch_results`).
6. Re-enable button. Show "DISPATCH COMPLETE" inline confirmation.

On failure at any step: show the error in the status area, re-enable the button, log the error to console. Do NOT auto-retry.

**Scope tab population:**

Replace the current "Upload a bidset on the NEW SESSION tab to populate scope" placeholder. When `App.currentResults` is set, render:

- For each system found across `trade_outputs[*].roofing.systems` (and same for `glazing` once trades support it — currently glazing is "coming later" per the trade selector UI), one card per system: name, member type counts, edge type counts, drawn from the trade module output structure.
- Re-use the existing `renderScopeTab` function structure where possible — it currently renders from a `ROOFING_SEED_ITEMS` constant for the seed UI. Refactor to take the API trade_outputs as primary source; fall back to seed items if no results yet (preserves current placeholder behavior).

**Pages tab population:**

Replace the current "all 38 pages = OTHER" rendering. When `App.currentResults` is set:

- Compute counts per page_type across `dispatch_results[*].page_type` (already shown as bucket counts at top of Pages tab — currently all 0 except OTHER 38).
- Per-page badges show `dispatch_results[String(pageIdx)].page_type` instead of hardcoded "OTHER".

The thumbnail rendering (the actual PDF page images) stays client-side — those don't depend on dispatch.

---

## §10 — Step E2.2.6: Frontend tests — 5 API smoke tests

Add the 5 API smoke tests reserved in `E2_0_TEST_FLOOR_PROPOSAL.md §3.1` to the new file's TESTS section. Use the SKIP convention already wired into `runTestBatch` from E.2.1 (per `E2_0_TEST_FLOOR_PROPOSAL.md §5.2` — verify it works when uvicorn is unreachable).

**Required tests:**

1. **`api · healthCheck returns ok`** — calls `apiClient.healthCheck()`; expects `{status: "ok"}`. SKIPs if `apiClient.healthCheck` rejects (uvicorn down).
2. **`api · createJob returns JobResponse with id and status=draft`** — calls `apiClient.createJob({name: "smoke test", pdf_path: <fixture path>, trade_scope: "roofing"})`; expects response with non-empty `id`, `status: "draft"`. SKIPs if uvicorn down. (Fixture path: a path the test harness knows exists on the dev machine — see fixture note below.)
3. **`api · getJob returns JobResponse for created id`** — round-trip: createJob → getJob with the returned id → assert ids match.
4. **`api · getJob returns 404 for unknown id`** — calls `apiClient.getJob('00000000-0000-0000-0000-000000000000')`; expects thrown error with `{status: 404}`.
5. **`api · createJob returns 422 for missing required field`** — calls `apiClient.createJob({})`; expects thrown error with `{status: 422}`.

**Fixture path for tests 2 and 3:** The smoke tests need a real PDF path the backend can resolve. Two options:

- **Option A (recommended):** Hardcode the tests to use the path of a known-small fixture from `backend/tests/fixtures/` (or wherever the existing fixture PDF lives — read to confirm). Test harness URL-encodes the path; Daniel runs the harness from the project root. Dependencies on absolute path are tolerable for a smoke test.
- **Option B:** Skip tests 2 and 3 if no fixture path is configured. Leaves the smoke at 3 of 5 SKIP-allowed.

Recommended: **Option A**. Worst case the test SKIPs on a clean machine — acceptable for a SKIP-tolerant smoke suite.

**Stub-correctness tests retire.** Per §9 the 2 E.2.1 stub tests for `extractScope` and `classifyPage` go away with the stubs. Net floor: **20 − 2 + 5 = 23**.

**Frontend floor:** 20 → **23**. (NOT 25 — see §9 General's call.)

---

## §11 — Step E2.2.7: Debug module output verification

Add a new tracked harness: `backend/scripts/e2_2_debug_silverleaf.py`.

**Purpose:** Run Silverleaf through `run_dispatch` in-process (NOT via the HTTP API), capture the in-memory `ctx`, call `debug_module.run_debug(ctx)`, write structured output to `backend/E2_2_DEBUG_silverleaf.md`. Compare key counts against the calibration baseline.

**Why in-process and not via the new endpoint:** `debug_module.run_debug(ctx)` consumes the live `ctx` object, not persisted SQLite data. Reconstituting ctx from SQLite is the open question `E0_API_DESIGN.md §5.3` flagged for the future `/debug` endpoint — out of scope here. In-process re-run gives us the ctx for free, takes ~140s, runs once during the soft gate, doesn't need to ship to production.

**Script behavior:**

1. Resolve the Silverleaf PDF path (hardcode to the same path D.2 reference run used — `backend/D2_REFERENCE_silverleaf.md` documents it).
2. Call `run_dispatch(pdf_path=<silverleaf>, storage="auto", job_id=None)`. Note `job_id=None` — this run is NOT persisted; it's verification-only. The persisted dispatch happens at the visual hard gate (§13) via the API.
3. Capture the returned `ctx`.
4. Call `debug_module.run_debug(ctx)`. Capture the returned debug structure.
5. Write `backend/E2_2_DEBUG_silverleaf.md` with sections:
   - **Summary:** page count, dispatch wall-clock, total scope items per trade, total warnings.
   - **Per-page table:** page_idx, sheet_num, page_type, roofing item count, glazing item count.
   - **Section 1 (dispatch health):** raw output from debug_module section 1.
   - **Section 3 (page intelligence):** raw output from debug_module section 3.
   - **Section 6 (legends + quality flags):** raw output from debug_module section 6.
   - **Sections 2/4/5:** stub markers (per Phase C.5 — not ported yet).
6. Read `backend/CALIBRATION_GATE_REPORT_silverleaf.md` and `backend/D2_REFERENCE_silverleaf.md` for baseline values: 38 pages total, 338 roofing items, 20+81+6 glazing items (verify the exact split — read the docs).
7. Compare:
   - Page count: must be exactly 38.
   - Roofing items: must be within ±5% of 338 (~321 to ~355). Drift outside this range is a STOP.
   - Glazing items: must be within ±5% of 107 total (or whatever the calibration sums to — confirm in D2_REFERENCE).
   - No `ERROR` markers in section 1 dispatch health output.
   - At least one page classified as `ROOF_PLAN` (Silverleaf has roof plans — zero ROOF_PLAN classifications is a regression).
8. Write the comparison verdict to the bottom of `E2_2_DEBUG_silverleaf.md`: PASS / FAIL with the specific drift if FAIL.

**Run the script.** Output lives at `backend/E2_2_DEBUG_silverleaf.md`. ~140s wall-clock for the dispatch.

---

## §12 — SOFT GATE 2 — Frontend ready

**Cannot proceed to debug-output soft gate until all of the following are true:**

- Frontend wiring complete per §9 (4 apiClient methods real, listJobs stub updated, status bar on-failure trigger wired, New Session path field + dispatch button shipped, Scope tab + Pages tab consume API data).
- 5 API smoke tests added per §10. Frontend test count = 23. PASS-or-SKIP (skips acceptable when uvicorn down — but for the soft gate, run with uvicorn UP and confirm all 5 PASS).
- Manual browser smoke (~3 min, Daniel does this):
  - Open the new file in Chrome.
  - Status bar transitions CHECKING → CONNECTED (uvicorn must be running for this gate).
  - Open VIEWER tab. Drawing tools (measure, exclude, polygon-draw, rectangle-draw, scale picker) still work — no E.2.1 regressions.
  - Open Scope tab. Shows the placeholder text ("Upload a bidset...") since no job has been dispatched yet. (Population happens at the hard gate.)
  - Open Pages tab. Shows the placeholder text. (Same reason.)
  - Open Tests tab. Run all tests. 23/23 PASS or 18/23 PASS with 5 SKIP (depending on uvicorn state — if up, all PASS).
- Vault SHA-1s + `debug_module.py` SHA-1 + 3 E.1 production-code SHA-1s all unchanged.
- `git status` shows only expected files modified.

**Soft gate output:** Inline summary in the running gate report draft. If any item fails: STOP, document, do not proceed.

---

## §13 — SOFT GATE 3 — Debug output matches calibration baseline

**Cannot proceed to visual hard gate until all of the following are true:**

- `backend/scripts/e2_2_debug_silverleaf.py` ran to completion without uncaught exceptions.
- `backend/E2_2_DEBUG_silverleaf.md` exists and contains the comparison verdict.
- Comparison verdict = PASS:
  - Silverleaf page count = 38 (exact).
  - Roofing items within ±5% of calibration baseline (338).
  - Glazing items within ±5% of calibration baseline (verify exact number from D2_REFERENCE).
  - At least one page classified as ROOF_PLAN.
  - No `ERROR` markers in section 1 dispatch health output.
- Daniel reads `E2_2_DEBUG_silverleaf.md` and confirms the per-page table looks sensible (no all-OTHER classifications, scope items distributed across the right pages).

**If FAIL:** STOP. The dispatch is producing different numbers than calibration — that's a regression somewhere. Surface the drift; do not proceed to the visual hard gate. Daniel decides next step (debug session, vault rule lift, etc.). Do not patch speculatively.

**Soft gate output:** Reference `E2_2_DEBUG_silverleaf.md` as the receipt in the running gate report.

---

## §14 — Step E2.2.8: HARD GATE — Silverleaf end-to-end

The user-flow hard gate. Daniel runs this manually with uvicorn up.

**Steps Daniel performs (Claude Code documents the procedure in the gate report; does not perform itself):**

1. Start uvicorn: `cd backend && uvicorn api.main:app --reload --port 8000`.
2. Open `frontend/src/Huckleberry_AI_phase2.v1.0.0.html` in Chrome.
3. Verify status bar transitions CHECKING → CONNECTED.
4. NEW SESSION tab:
   - Step 1: Select Roofing trade.
   - Step 1.5: Paste the Silverleaf absolute path into the Server file path field.
   - Step 2: Drag-drop the Silverleaf PDF into the upload zone. Confirm "38 page(s) loaded" appears.
   - Click "RUN DISPATCH" button.
5. Wait ~140s. Status bar should remain CONNECTED throughout (health polling continues during dispatch — though may briefly fail if uvicorn is single-worker and busy; document the observed behavior).
6. After dispatch complete, the inline status shows "DISPATCH COMPLETE".
7. Open SCOPE tab. Verify roofing systems are listed with item counts derived from the dispatched data.
8. Open PAGES tab. Verify bucket counts at top show non-zero ROOF_PLAN / DETAIL / SPEC counts (not all OTHER). Verify per-page badges show real classifications.
9. Open VIEWER tab. Pick a ROOF_PLAN page. Confirm pdf renders. Confirm system dropdown now lists real systems (not "no systems — upload a bidset"). Drop a pin — confirm it places at click coordinates and attaches to the selected system.
10. Open TAKEOFF tab. Verify it shows scope-derived rows (not "No scope yet" placeholder).
11. Open TESTS tab. Run all tests. 23/23 PASS expected with uvicorn up.

**Hard gate criteria (each must PASS):**

| # | Criterion | Verification |
|---|---|---|
| 1 | uvicorn starts cleanly, no errors | uvicorn console |
| 2 | Frontend loads, status bar CONNECTED | Browser observation |
| 3 | Server file path field accepts and forwards path | Network tab shows POST /jobs body has correct pdf_path |
| 4 | Dispatch completes within 4 min wall-clock | Browser timer |
| 5 | Scope tab populates with non-empty systems | Browser observation |
| 6 | Pages tab shows non-OTHER classifications for at least 50% of pages | Browser observation; baseline ~62% non-OTHER per Silverleaf calibration |
| 7 | Viewer system dropdown populates from real scope | Browser observation |
| 8 | Pin placement attaches to selected system (no "upload a bidset" error) | Browser action |
| 9 | Takeoff tab shows derived rows | Browser observation |
| 10 | Tests tab shows 23/23 PASS | Browser observation |

**Daniel reports the 10-criterion verdict back to the General; gate report (§16) records it.**

---

## §15 — Step E2.2.9: Documentation + housecleaning

Surgical edits only.

### `PROJECT_CLAUDE.md`

**§3 (state paragraphs, chronological):** append a new paragraph after the E.2.1 paragraph documenting E.2.2 completion. Pattern per prior phases: branch, what shipped (4 wired methods, 2 new endpoints, scope+pages population, hard gate result), sacred floor transitions (backend 222 → 228–230; frontend 20 → 23 — note the deviation from prior "20 → 25" framing per §10), receipts.

**§7 (phase table):**
- E.2.2 row: `NEXT-eligible` → `COMPLETE 2026-05-XX` with branch + receipt references.
- **Remove** E.2.debug and E.2.hard-gate rows (collapsed into E.2.2 per Daniel directive 2026-05-01). Replace with a single note row: `~~E.2.debug, E.2.hard-gate~~ — collapsed into E.2.2 big block per directive 2026-05-01`.
- **Promote** Phase G (quadrant smart scan) to NEXT-eligible.

**No other section is touched.**

### `backend/BLOCK_RUN.md`

Append **Phase 9 — E.2.2 frontend connect + Silverleaf hard gate** section (replacing the RESERVED placeholder). Match the template Phase 7 + Phase 8 used (Files created / modified / deleted, Commits, Pushes, Dependency / config changes, Vault-ruled files touched, E.1 production-code SHA-1s, Frontend touched, CLAUDE.md, Sacred floor at session end, §19 stops fired, Test composition, Key design decisions). Reserve a Phase 10 placeholder for Phase G.

### `backend/E0_API_DESIGN.md`

Append **§5.13 — Endpoints landed in E.2.2** documenting:
- `POST /jobs/{id}/dispatch` — actual shipped behavior (sync, idempotent, status transitions draft → dispatching → dispatched).
- `GET /jobs/{id}/results` — actual shipped response shape (string-indexed dicts, `null` slots for trades with no output).
- Promotes the §5.3 sketches for these two endpoints to canonical implementations. The sketches stay in §5.3 for historical context with a "→ shipped per §5.13" note.

If the implementation deviates from the §5.3 sketch in any small way, append it as a **corrigendum 4** to §5.12 — same format as corrigenda 1, 2, 3. (Likely small deviations: status enum extension to include `dispatching`; per-call timeout option in apiCall helper. Document if so.)

### `VALIDATION_LEDGER.md`

Update sacred floor entries:
- Backend: `222 → 228–230` (within window; cite exact post-session count).
- Frontend: `20 → 23` (against `frontend/src/Huckleberry_AI_phase2.v1.0.0.html`).
- Vault SHA-1s: unchanged (5 modules + debug_module.py).

### `safe_for_removal/MANIFEST.md`

**Likely no edit.** E.2.2 doesn't archive anything. Confirm at gate time. Daniel personally empties `safe_for_removal/` post-ratification — that's HIS task, not Claude Code's, and happens AFTER E.2.2 ships.

### NOT touched

- `CHECKLIST.md` — General signs the row after Daniel ratifies, in a separate session.
- `ITINERARY.md` — General updates after ratification.
- `PROJECT_ETIQUETTE.md`, `ROLES.md` — never touched in phase work.

---

## §16 — Step E2.2.10: Gate report

Final deliverable: `backend/E2_2_GATE_REPORT.md`. Contents:

§1 — Pre-flight results (test floors, SHA-1 captures, branch verification, git status snapshot).
§2 — Done-definition checklist (§22 of this doc) — every item PASS / FAIL with evidence.
§3 — §19 stop conditions — explicit non-firing status with evidence per stop.
§4 — Sacred floors at session end (backend 228–230 with exact count; frontend 23/23; vault SHA-1s + debug_module SHA-1 + E.1 production SHA-1s all match).
§5 — Wall-clock summary per E2.2.X step.
§6 — Deliverables produced (file paths + brief description).
§7 — Soft gate 1 (backend) verdict + evidence.
§8 — Soft gate 2 (frontend) verdict + evidence.
§9 — Soft gate 3 (debug output) verdict + evidence + reference to `E2_2_DEBUG_silverleaf.md`.
§10 — Hard gate (Silverleaf end-to-end) — Daniel's 10-criterion verdict + observations.
§11 — Open items for Daniel review before Phase G march orders draft.

---

## §17 — Step E2.2.11: Commit and push

Single commit. Files in commit:

**Created:**
- `backend/scripts/e2_2_debug_silverleaf.py`
- `backend/E2_2_DEBUG_silverleaf.md` (script output)
- `backend/E2_2_GATE_REPORT.md`

**Modified:**
- `backend/api/routes/jobs.py` (2 new endpoints)
- `backend/api/schemas/jobs.py` (status enum extension; new `JobResultsResponse` model)
- `backend/core/job_storage.py` (read accessors `load_dispatch_results`, `load_trade_outputs` if not already present — confirm at read time)
- `backend/tests/test_api_jobs.py` (6–8 new tests)
- `frontend/src/Huckleberry_AI_phase2.v1.0.0.html` (4 wired methods; listJobs error string update; New Session path field + dispatch button; Scope + Pages population; 5 API smoke tests; 2 stub tests removed; 2 stubs removed)
- `backend/E0_API_DESIGN.md` (§5.13 + possibly §5.12 corrigendum 4)
- `PROJECT_CLAUDE.md` (§3 paragraph + §7 phase table updates including E.2.debug/hard-gate collapse note)
- `backend/BLOCK_RUN.md` (Phase 9 section)
- `VALIDATION_LEDGER.md` (sacred floor updates)

**Deleted:** None.

**Renamed:** None.

Commit message: `E.2.2: frontend connect + 2 new endpoints + Silverleaf hard gate (backend 222 → 228–230, frontend 20 → 23)`

Push to origin.

---

## §18 — Sacred floors to hold

| Check | Pre-session value | Post-session expectation |
|---|---|---|
| Backend tests | 222 passed, 19 skipped, 0 failed | **228–230 passed**, 19 skipped, 0 failed |
| Frontend tests vs new file | 20/20 passed | **23/23 passed** (or PASS-with-SKIP if uvicorn down at test run, but soft gate 2 requires uvicorn UP) |
| `roofing_module.py` SHA-1 | `ae9e5b28…` | unchanged |
| `glazing_module.py` SHA-1 | `52c01442…` | unchanged |
| `roofing_vocabulary.py` SHA-1 | `ec6c17f8…` | unchanged |
| `glazing_vocabulary.py` SHA-1 | `64249c8e…` | unchanged |
| `debug_module.py` SHA-1 | `78f71d90…` | unchanged |
| `backend/api/main.py` SHA-1 | (capture) | unchanged |
| `backend/api/routes/jobs.py` SHA-1 | (capture) | **CHANGED** (2 new endpoints) — capture post-session SHA-1 |
| `backend/api/schemas/jobs.py` SHA-1 | (capture) | **CHANGED** (status enum + new model) — capture post-session SHA-1 |
| `git diff backend/core/dispatch_gate.py` | empty | **empty** (E.2.2 does not modify dispatch_gate; D.2 already wired persistence) |
| `git diff backend/core/` excluding `job_storage.py` | empty | empty |
| `pyproject.toml` | unchanged | unchanged |
| `package.json` `dependencies` | unchanged | unchanged (only `version` field may bump if convention; do not touch `dependencies`) |
| CLAUDE.md opened | no | no |
| `safe_for_removal/` modified | n/a | n/a (Daniel does the cleanout post-ratification) |

Any drift on any row → §19 stop.

---

## §19 — Stop conditions (any → halt + report, do not proceed)

1. Sacred floor regresses (backend < 228 OR frontend < 23 at session end with uvicorn up).
2. Any vault-ruled module SHA-1 changes (5 trade modules + `debug_module.py`).
3. `backend/api/main.py` SHA-1 changes (E.2.2 doesn't touch main.py).
4. Any vault-ruled module is opened with edit intent.
5. CLAUDE.md gets opened or edited.
6. Backend code change in `backend/core/` other than read accessors added to `job_storage.py`.
7. `pyproject.toml` modified.
8. `package.json` `dependencies` or `devDependencies` modified.
9. Any new dependency added (Python or npm).
10. Multipart upload added to backend (deferred — path field is the E.2.2 answer).
11. `apiClient.listJobs` or any new endpoint wired beyond the 4 specified.
12. Annotation save/load wired (Phase F territory).
13. `safe_for_removal/` files modified (Daniel's cleanout).
14. Async dispatch / background tasks introduced.
15. Soft gate 1 (backend) fails — proceed to frontend wiring forbidden.
16. Soft gate 2 (frontend) fails — proceed to debug-output gate forbidden.
17. Soft gate 3 (debug output) fails — proceed to visual hard gate forbidden.
18. Hard gate criteria 1–10 partial PASS — gate report documents which criteria failed; do not retroactively edit code to pass a failed criterion within this session (separate fix session).
19. Frontend test count at session end ≠ 23 (e.g., extra test added that's not one of the 5 new smoke tests; or one of the 5 missing).
20. Backend test count at session end < 228 or > 230 (window).
21. PROJECT_CLAUDE.md edits exceed §3 paragraph + §7 phase table scope.
22. The §5.13 documentation append doesn't land in `E0_API_DESIGN.md`.
23. `E2_2_DEBUG_silverleaf.md` is missing or doesn't contain the comparison verdict.
24. Push to origin fails.
25. Speculative bug-patches on stub-coupling artifacts (pin/polygon/rectangle finalize) made WITHOUT real-data verification — per Daniel directive 2026-05-01 these "bugs" resolve when scope wiring lands; do not pre-patch.

---

## §20 — Karpathy procedure conformance

E.2.2 is constructive — adds endpoints, wires frontend, runs the bidset. Karpathy compliance:

1. **Read first.** All E.2.0 deliverables + E.0 API design + E.1 receipts + E.2.1 gate report + Silverleaf calibration + D.2 reference + relevant `core/` files (read-only) per §2.
2. **Failing tests first.** The 6–8 new backend tests are written BEFORE the endpoint implementations (or in a tight loop with the implementations — write test, write impl, run, repeat). The 5 API smoke tests are written BEFORE the apiClient wiring (against the spec; will SKIP until uvicorn is up).
3. **Minimum implementation.** Only what §5 / §6 / §9 / §10 specify. No "while we're in there" additions. No premature optimization. No async dispatch (sync is the spec).
4. **Sacred floors held** at every verification point: pre-flight (222/19/0 + 20/20), post-soft-gate-1 (228–230 + 20/20), post-soft-gate-2 (228–230 + 23/23), post-soft-gate-3 (debug PASS), post-hard-gate (all of above + 10-criterion verdict).
5. **Stops fire** when something is genuinely uncertain. Don't extrapolate; document and stop.
6. **Diagnostic before action.** Especially at soft gate 3: if debug output drifts from baseline, STOP — do not patch the modules to make the numbers match. Drift is signal.

The B-16/17/18 anti-pattern (speculation patches without diagnostics) and the cosmetic-improvement-as-drift trap are the explicit things to avoid. Per Daniel directive 2026-05-01: the pin/polygon/rectangle "bugs" Daniel observed in E.2.1 Chrome smoke are stub-coupling artifacts — they resolve when scope wiring lands. Do NOT pre-patch them; let the wiring fix them naturally. If they persist post-wiring, document for a later phase.

---

## §21 — Vault rule enforcement

Five trade modules + `debug_module.py` are vault-ruled. SHA-1s captured at pre-flight, verified at session end. E.2.2 reads `debug_module.py` to confirm the `run_debug(ctx)` signature for the soft-gate script (§11), but does NOT edit it.

`backend/core/dispatch_gate.py` is NOT vault-ruled but is cap-protected: D.2 added 8 lines; E.2.2 adds zero lines (the new endpoint calls `run_dispatch` via the existing public signature D.2 finalized). Verify zero diff at gate time.

`backend/core/job_storage.py` is NOT vault-ruled. E.2.2 may add read accessors (`load_dispatch_results`, `load_trade_outputs`) if they don't already exist. Read the file first to confirm. Adding read accessors is in scope; modifying existing write accessors or schema is NOT.

---

## §22 — Done-definition checklist

| # | Item | Verified by |
|---|---|---|
| 1 | Pre-flight: 222/19/0 backend, 20/20 frontend, all SHA-1s captured, git status documented | E2.2.0 |
| 2 | Branch `phase2-v0.3-E2-2-frontend-connect-and-hard-gate` from `4f7c90f` | E2.2.1 |
| 3 | `POST /jobs/{id}/dispatch` endpoint shipped per §5 (sync, idempotent, status transitions wired) | E2.2.2 |
| 4 | `GET /jobs/{id}/results` endpoint shipped per §6 (string-indexed dicts, null trade slots) | E2.2.3 |
| 5 | Status enum extended to include `dispatching` (or confirmed already present in `_VALID_STATUSES`) | E2.2.2 |
| 6 | `JobResultsResponse` Pydantic model shipped with `extra="forbid"` | E2.2.3 |
| 7 | `load_dispatch_results` + `load_trade_outputs` accessors exist in `job_storage.py` (pre-existing or newly added) | E2.2.3 |
| 8 | 6–8 new backend tests added per §7; backend test count in window 228–230 | E2.2.4 |
| 9 | All 19 pre-existing skipped tests still skipped (no skip leakage) | E2.2.4 |
| 10 | Soft gate 1 (backend) PASS — all backend criteria + uvicorn smoke | §8 |
| 11 | `apiClient.createJob` real (POST /jobs) | E2.2.5 |
| 12 | `apiClient.getJob` real (GET /jobs/{id}) | E2.2.5 |
| 13 | `apiClient.dispatchJob` real (POST /jobs/{id}/dispatch) with 240s timeout override | E2.2.5 |
| 14 | `apiClient.getResults` real (GET /jobs/{id}/results) | E2.2.5 |
| 15 | `apiClient.listJobs` stays stubbed; error string updated to `not_implemented_in_e2_2` | E2.2.5 |
| 16 | `extractScope` + `classifyPage` stubs removed; their 2 tests removed | E2.2.5 + E2.2.6 |
| 17 | Status bar on-failure trigger wired (network error → immediate `probeHealth()`) | E2.2.5 |
| 18 | New Session tab — Server file path field added, RUN DISPATCH button added | E2.2.5 |
| 19 | Scope tab consumes API trade_outputs; falls back to placeholder if no results | E2.2.5 |
| 20 | Pages tab consumes API dispatch_results.page_type; bucket counts populate | E2.2.5 |
| 21 | 5 API smoke tests added per §10; SKIP convention works when uvicorn down | E2.2.6 |
| 22 | Frontend test count = 23 (20 − 2 + 5) | E2.2.6 |
| 23 | Soft gate 2 (frontend) PASS — all frontend criteria + Daniel browser smoke | §12 |
| 24 | `backend/scripts/e2_2_debug_silverleaf.py` runs to completion | E2.2.7 |
| 25 | `backend/E2_2_DEBUG_silverleaf.md` exists with summary + per-page table + sections 1/3/6 + comparison verdict | E2.2.7 |
| 26 | Soft gate 3 (debug output) PASS — counts within ±5% of calibration baseline | §13 |
| 27 | Hard gate (Silverleaf end-to-end) — Daniel's 10-criterion verdict captured in gate report | §14 |
| 28 | `backend/E0_API_DESIGN.md §5.13` appended documenting shipped endpoints | E2.2.8 |
| 29 | `PROJECT_CLAUDE.md` §3 + §7 updates (including E.2.debug/hard-gate collapse note + Phase G promotion) | E2.2.8 |
| 30 | `backend/BLOCK_RUN.md` Phase 9 section appended; Phase 10 placeholder reserved | E2.2.8 |
| 31 | `VALIDATION_LEDGER.md` sacred floor updates landed | E2.2.8 |
| 32 | `safe_for_removal/MANIFEST.md` confirmed unchanged (or row added if anything was archived — unlikely) | E2.2.8 |
| 33 | Sacred floors at session end (§18 table) all confirmed | E2.2.10 |
| 34 | `git diff` against vault-ruled modules + `dispatch_gate.py` + `main.py` + `pyproject.toml` + `package.json` deps all empty | E2.2.10 |
| 35 | CLAUDE.md not opened during session | E2.2.10 |
| 36 | `safe_for_removal/` files not modified during session | E2.2.10 |
| 37 | `backend/E2_2_GATE_REPORT.md` produced; all 25 §19 stop conditions explicitly confirmed non-firing | E2.2.10 |
| 38 | Single commit on branch with files per §17 | E2.2.11 |
| 39 | Commit pushed to origin | E2.2.11 |

---

## §23 — Estimated wall-clock

| Step | Estimated |
|---|---|
| E2.2.0 pre-flight (backend tests, frontend tests, SHA-1s, git status) | ~5 min |
| E2.2.1 branch | <1 min |
| E2.2.2 + E2.2.3 backend endpoints (read job_storage, write 2 endpoints + 1 schema, possibly add 2 read accessors) | ~30–40 min |
| E2.2.4 backend tests (6–8 new tests, iterate to PASS) | ~20–30 min |
| Soft gate 1 verification (backend tests + uvicorn smoke + SHA-1 check) | ~5–10 min |
| E2.2.5 frontend wiring (4 apiClient methods, status bar trigger, New Session UI, Scope + Pages population) | ~60–90 min |
| E2.2.6 frontend tests (5 API smoke + remove 2 stub tests, iterate to 23/23) | ~20–30 min |
| Soft gate 2 verification (frontend tests + Daniel browser smoke) | ~10 min |
| E2.2.7 debug script + run + write `E2_2_DEBUG_silverleaf.md` | ~20 min (mostly the ~140s dispatch wait) |
| Soft gate 3 verification (Daniel reads debug output) | ~10 min |
| E2.2.8 hard gate (Daniel performs full 11-step browser walkthrough; ~140s dispatch wait) | ~15 min |
| E2.2.9 docs + housecleaning (PROJECT_CLAUDE, BLOCK_RUN, E0_API_DESIGN §5.13, VALIDATION_LEDGER) | ~15 min |
| E2.2.10 gate report | ~15 min |
| E2.2.11 commit + push | ~3 min |
| **Total** | **~4 to 6 hours** |

This is a substantial big-block phase. If wall-clock exceeds **8 hours** and any soft gate hasn't fired, **STOP** and document. The 8-hour ceiling forces honest scope assessment vs. quiet creep.

---

## §24 — What ships at end of E.2.2

A frontend that talks to the backend for one bidset end-to-end. Daniel can paste a Silverleaf path, drag-drop the PDF, click RUN DISPATCH, wait ~140s, and see real scope + page classifications populated from the backend. The `apiClient` has 4 of 5 methods real; the last (listJobs) waits for `GET /jobs` in a later phase. Backend test floor 228–230. Frontend test floor 23.

After Daniel reviews and ratifies:

- **CHECKLIST.md** row E2 signed by General with hard-gate verdict + commit SHA + receipt path.
- **ITINERARY.md** mutated: E.2.2 becomes Last-1; E.2.1 shifts to Last-2; E.2.0 to Last-3; E.1 falls off. Phase G promotes to Next-1; Phase F to Next-2.
- **PROJECT_CLAUDE.md** §7 updated (already done in E2.2.8).
- **`safe_for_removal/` cleanout** — Daniel's task. Empties the directory; saves contents outside the project for future reference. Out of scope for Claude Code.

Phase E ships clean at this point. Next-eligible: Phase G (quadrant smart scan) — design phase first (G.0), then build (G.1).

---

## §25 — Reminder: Daniel's locked decisions feeding E.2.2

| Decision | Locked answer | Where it lives in this phase |
|---|---|---|
| Big block vs sub-phases | Single big block; collapse E.2.debug + E.2.hard-gate into E.2.2 | §0 + §15 (PROJECT_CLAUDE.md collapse note) |
| 2 soft gates + debug soft gate + hard gate | Soft gates after backend, frontend, debug output read; hard gate at end | §8, §12, §13, §14 |
| Sync vs async dispatch | Sync; ~140s block acceptable for Silverleaf | §5 |
| File upload | Deferred; pdf_path string field on New Session tab | §1 + §9 |
| Don't polish stub-coupling bugs | Pin/polygon/rectangle "bugs" resolve when scope wires; do NOT pre-patch | §1 + §19 #25 + §20 |
| safe_for_removal cleanout | Daniel does it personally post-ratification; not Claude Code's task | §1 + §15 + §24 |
| Karpathy applied before drafting | Read first; soft gate 3 enforces "diagnostic before action" | §2 + §11 + §20 |

---

**End of MARCH ORDERS — Phase E.2.2.**

Daniel green-lights → Claude Code executes. Single autonomous big-block session. Three soft gates pause execution between sub-steps; one hard gate at the end. Daniel personally performs the browser-side hard gate steps + reviews debug output at soft gate 3.
