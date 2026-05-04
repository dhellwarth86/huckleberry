# MARCH ORDERS — Phase E.1: FastAPI Scaffold + First Endpoints

**Date issued:** 2026-04-29
**Issued by:** Daniel (via extended-thinking Claude planning session)
**Executed by:** Claude Code
**Phase shape:** Single session, autonomous, soft-gates-only, single final gate report
**Phase scope:** FastAPI scaffold + 2 endpoints + 1 exempt health probe + 6 new tests + Silverleaf single-bidset hard gate. NO 3-bidset hard gate (deferred until Phase G ships quadrant smart scan).
**Read first:** PROJECT_CLAUDE.md, BLOCK_RUN.md, then this document

---

## §0 — What this phase is

First novel-code phase of Phase E. Build the FastAPI server, expose two real endpoints + one health probe, prove the API talks to D.2's persistence layer correctly, ship a single-bidset Silverleaf hard gate.

After this phase ships and Daniel green-lights, **soft-gate continuation** to E.2 (frontend strip + connect). Not auto-continue — soft gate means Daniel reviews E.1 deliverables, confirms direction, then E.2 march orders draft.

**OUT OF SCOPE for this phase:**
- 3-bidset hard gate (compute-heavy; deferred until Phase G ships quadrant smart scan)
- Authentication (deferred to Postgres/security phase)
- CORS lockdown (permissive in E.1, locked at Postgres/security)
- Frontend changes (E.2 territory)
- File upload via API (deferred — Postgres phase moves to upload + local disk save; cloud comes when data volume requires)
- Vault-ruled module changes (vault rule active)
- Other endpoints beyond POST /jobs + GET /jobs/{job_id} + GET /health (E.2/E.3 territory)

---

## §1 — Pre-flight reads (Karpathy step 1)

Full reads, in this order:

1. **PROJECT_CLAUDE.md** — entry point. §3 most-recent paragraph (E.0 complete); §7 phase table.
2. **BLOCK_RUN.md** — Phase 5 (E.0) entries. You extend with Phase 6 (E.1).
3. **VALIDATION_LEDGER.md** — sacred floors, vault list.
4. **`backend/E0_API_DESIGN.md`** — the contract this phase builds against. Read in full. The endpoint shapes, Pydantic schemas, error shapes, project structure are all specified.
5. **`backend/E0_FRONTEND_AUDIT.md`** — context for what's coming in E.2 (informs which endpoint shapes E.1 should leave clean room for).
6. **`backend/E0_GATE_REPORT.md`** — discipline pattern reference.
7. **`backend/D2_MASTER_GATE_REPORT.md`** — D.2 chain end state; the persistence layer this phase surfaces.
8. **`backend/core/job_storage.py`** — the lifecycle API the FastAPI endpoints will call.
9. **`backend/core/dispatch_gate.py`** — note that `run_dispatch` accepts `job_id` from D.2; not invoked in E.1 endpoints.
10. **`backend/core/context.py`** — `PlanSetContext` shape (forward-compat reference for later endpoints).

**Do NOT open:** five vault-ruled modules, frontend HTMLs (audit done; no frontend changes in E.1), anything in `safe_for_removal/`, CLAUDE.md (retired).

---

## §2 — Step E1.0: Pre-flight verification

- Run the full backend suite. Floor: **216 passed, 19 skipped, 0 failed**. Hard stop if not met.
- Run frontend test suite. Floor: **138/138 against v6.3.5**. Hard stop if not met.
- Capture pre-session SHA-1s for all five vault-ruled modules.
- Capture pre-session SHA-1s for v6.3.5 (the only frontend HTML still in workspace root after E.0 housekeeping).
- Verify branch state: `phase2-v0.3-E0-api-design-and-frontend-audit` head matches E.0 commit per BLOCK_RUN.md.
- Locate B2607 AEA Silverleaf PDF for hard gate.
- Confirm `git remote -v` shows `https://github.com/dhellwarth86/huckleberry.git`.

---

## §3 — Step E1.1: Branch

```
phase2-v0.3-E1-fastapi-scaffold  (NEW; from E.0 head)
```

Single commit at end of session. Pushed.

---

## §4 — Step E1.2: Add dependencies

Modify `backend/pyproject.toml`. Add three deps:

```toml
fastapi = ">=0.115"
uvicorn = { extras = ["standard"], version = ">=0.30" }
pydantic = ">=2.7"
```

(Adjust to project's actual pyproject.toml format — Poetry vs setuptools vs Hatch.)

Run `pip install` (or equivalent) to install the new deps. Verify import works:

```python
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
```

If imports fail, **§7 stop**.

---

## §5 — Step E1.3: Build the FastAPI scaffold

Create the directory structure per E0_API_DESIGN.md §5.4:

```
backend/api/
├── __init__.py        # NEW — package marker
├── main.py            # NEW — FastAPI app + uvicorn entry
├── routes/
│   ├── __init__.py
│   └── jobs.py        # POST /jobs + GET /jobs/{job_id}
└── schemas/
    ├── __init__.py
    └── jobs.py        # Pydantic models (JobCreateRequest, JobResponse)
```

### §5.1 — `backend/api/main.py`

The FastAPI app. Includes:

- App instance: `app = FastAPI(title="Huckleberry AI", version="0.3.0-E.1")`
- CORS middleware permissive in dev:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

(Comment: `# E.1: permissive CORS for dev; locked down at Postgres/security phase`)

- Health probe endpoint (exempt from budget):

```python
@app.get("/health")
def health():
    return {"status": "ok", "version": "0.3.0-E.1"}
```

- Include the jobs router:

```python
from api.routes import jobs as jobs_routes
app.include_router(jobs_routes.router)
```

- uvicorn entry block (for `python -m api.main` or similar):

```python
if __name__ == "__main__":
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)
```

OpenAPI docs auto-exposed at `/docs` and `/redoc`. (Comment: `# E.1: docs exposed in dev; hidden at Postgres/security phase`)

### §5.2 — `backend/api/schemas/jobs.py`

Pydantic v2 models. Two main shapes:

```python
from typing import Literal, Optional
from pydantic import BaseModel, Field

JobStatus = Literal["draft", "dispatched", "in_review", "exported", "archived"]
TradeScopeStr = str  # comma-separated; future Literal as trades expand


class JobCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    pdf_path: str = Field(..., min_length=1)  # E.1: string path; upload comes at Postgres migration
    gc: Optional[str] = None
    location_city: Optional[str] = None
    location_state: Optional[str] = None
    trade_scope: str = "roofing"
    bid_due_date: Optional[str] = None  # ISO 8601
    notes: Optional[str] = None
    status: JobStatus = "draft"


class JobResponse(BaseModel):
    id: str
    name: str
    gc: Optional[str]
    location_city: Optional[str]
    location_state: Optional[str]
    trade_scope: str
    bid_due_date: Optional[str]
    notes: Optional[str]
    status: JobStatus
    created_at: str
    updated_at: str
    pdf_path: str
    pdf_sha1: str
    dispatch_complete: bool

    model_config = {"extra": "forbid"}  # E.1: data-leak guard — extra fields rejected
```

`extra="forbid"` is the data-leak guardrail — the response schema only emits the listed fields. Anything extra from `job_storage.get_job` gets stripped before serialization.

### §5.3 — `backend/api/routes/jobs.py`

```python
from fastapi import APIRouter, HTTPException
from api.schemas.jobs import JobCreateRequest, JobResponse
from core.job_storage import create_job, get_job

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=JobResponse, status_code=201)
def create_job_endpoint(payload: JobCreateRequest) -> JobResponse:
    job_id = create_job(
        name=payload.name,
        pdf_path=payload.pdf_path,
        gc=payload.gc,
        location_city=payload.location_city,
        location_state=payload.location_state,
        trade_scope=payload.trade_scope,
        bid_due_date=payload.bid_due_date,
        notes=payload.notes,
        status=payload.status,
    )
    job = get_job(job_id)
    if job is None:
        # E.1: data-leak guard — generic message, no SQL details
        raise HTTPException(status_code=500, detail="Job creation failed")
    return JobResponse(**job)


@router.get("/{job_id}", response_model=JobResponse)
def get_job_endpoint(job_id: str) -> JobResponse:
    job = get_job(job_id)
    if job is None:
        # E.1: data-leak guard — generic 404 message, no query details
        raise HTTPException(status_code=404, detail="Job not found")
    return JobResponse(**job)
```

Tag every E.1-specific code line with `# E.1:` inline comment for traceability.

---

## §6 — Step E1.4: Tests

Create `backend/tests/test_api_jobs.py`. Add **6 new tests**, bringing backend test count from 216 → 222.

```python
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_health_probe_returns_ok():
    """Test 1: /health returns 200 and status=ok"""
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"


def test_create_job_happy_path(silverleaf_path):  # silverleaf_path fixture in conftest.py
    """Test 2: POST /jobs with valid payload returns 201 and JobResponse shape"""
    payload = {
        "name": "Silverleaf E.1 test",
        "pdf_path": str(silverleaf_path),
        "gc": "Test GC",
        "location_city": "Tampa",
        "location_state": "FL",
        "trade_scope": "roofing",
    }
    r = client.post("/jobs", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert body["name"] == "Silverleaf E.1 test"
    assert body["status"] == "draft"
    assert "id" in body
    assert "pdf_sha1" in body


def test_get_job_happy_path(silverleaf_path):
    """Test 3: GET /jobs/{job_id} returns 200 and full JobResponse"""
    payload = {
        "name": "Silverleaf get test",
        "pdf_path": str(silverleaf_path),
    }
    create_resp = client.post("/jobs", json=payload)
    job_id = create_resp.json()["id"]
    r = client.get(f"/jobs/{job_id}")
    assert r.status_code == 200
    assert r.json()["id"] == job_id
    assert r.json()["name"] == "Silverleaf get test"


def test_get_job_404_for_nonexistent_id():
    """Test 4: GET /jobs/{nonexistent} returns 404 with safe error message"""
    r = client.get("/jobs/nonexistent-job-id-12345")
    assert r.status_code == 404
    body = r.json()
    assert body["detail"] == "Job not found"


def test_create_job_validation_error_invalid_status(silverleaf_path):
    """Test 5: POST /jobs with invalid status returns 422"""
    payload = {
        "name": "Test",
        "pdf_path": str(silverleaf_path),
        "status": "banana",  # not in JobStatus Literal
    }
    r = client.post("/jobs", json=payload)
    assert r.status_code == 422


def test_data_leak_response_shape_and_error_messages(silverleaf_path):
    """Test 6: Combined data-leak detection.
    Asserts:
    1. JobResponse contains exactly the documented fields, no extras (no internal SQL,
       no full file paths beyond pdf_path which is part of the contract, no traceback strings).
    2. Error responses contain only generic detail messages — no SQL fragments,
       no file paths, no traceback strings, no DB column names beyond those in the schema.
    """
    EXPECTED_FIELDS = {
        "id", "name", "gc", "location_city", "location_state", "trade_scope",
        "bid_due_date", "notes", "status", "created_at", "updated_at",
        "pdf_path", "pdf_sha1", "dispatch_complete",
    }
    
    # Part 1: response shape
    payload = {"name": "Leak test", "pdf_path": str(silverleaf_path)}
    r = client.post("/jobs", json=payload)
    assert r.status_code == 201
    body_keys = set(r.json().keys())
    assert body_keys == EXPECTED_FIELDS, f"Unexpected fields in response: {body_keys ^ EXPECTED_FIELDS}"
    
    # Part 2: error message safety
    bad_resp = client.get("/jobs/nonexistent-id")
    err_body = bad_resp.json()
    err_str = str(err_body).lower()
    forbidden_substrings = [
        "select ", "from jobs", "where id=",  # SQL fragments
        "/", "\\",                              # file path separators (heuristic)
        "traceback", "file \"",                # Python traceback markers
        "sqlite", "execute(",                  # DB engine names
    ]
    for forbidden in forbidden_substrings:
        assert forbidden not in err_str, f"Error response leaked: '{forbidden}' found in: {err_body}"
```

Conftest entry for `silverleaf_path`:

```python
# backend/tests/conftest.py — append (NOT replace)
import pytest
from pathlib import Path

@pytest.fixture
def silverleaf_path():
    # E.1: tests reference Silverleaf via the same path D.2 / D.1 used
    # Path may need adjustment per workspace layout
    p = Path("C:/huck stage 2/full bid sets/B2607 AEA Silverleaf - St Augustine - Accelerated Construction Services.pdf")
    if not p.exists():
        # Fallback: try relative path from backend/
        p = Path("../../../full bid sets/B2607 AEA Silverleaf - St Augustine - Accelerated Construction Services.pdf").resolve()
    if not p.exists():
        pytest.skip("Silverleaf bidset not found; E.1 tests need real PDF for happy paths")
    return p
```

Conftest is shared across all backend tests — DO NOT replace; ONLY append the fixture if not already present.

**Test count target after E.1: 222 passed, 19 skipped, 0 failed.**

If any test fails, **§7 stop**. If conftest is broken in a way that affects the existing 216 tests, **§7 stop**.

---

## §7 — Step E1.5: Silverleaf single-bidset hard gate

Build `backend/scripts/e1_silverleaf_api_hardgate.py` (tracked).

**This hard gate is single-bidset only.** No 3-bidset run. Per Daniel directive 2026-04-29: multi-bidset compute-heavy testing deferred until Phase G ships quadrant smart scan.

The harness:

1. Starts the FastAPI server in a subprocess (or uses `TestClient` for simpler in-process testing — TestClient is preferred since uvicorn-spawning adds session state complications).
2. POSTs a Silverleaf job creation request.
3. GETs the job back.
4. Asserts:
   - POST returned 201 with all expected fields
   - GET returned 200 with same `id`
   - The job persists in SQLite (use `core.job_storage.get_job` directly to verify round-trip outside the API)
   - The job's `created_at` timestamp is recent
   - The job's `pdf_sha1` matches the actual file's SHA-1
5. Tests an invalid status:
   - POST with `status="banana"` returns 422
6. Tests a 404:
   - GET `/jobs/nonexistent-id` returns 404 with `{"detail": "Job not found"}` (verifying data-leak guard)
7. Writes hard gate report to `backend/E1_HARD_GATE_silverleaf_api.md`.

### §7.1 — Hard gate report skeleton

```markdown
# E.1 Silverleaf API Hard Gate Report

**Date:** 2026-04-29
**Branch:** `phase2-v0.3-E1-fastapi-scaffold`
**Bidset:** B2607 AEA Silverleaf
**Pipeline:** FastAPI server + D.2 persistence layer
**Overall:** PASS / FAIL

---

## §1 — API + persistence verification

| # | Test | Result | Evidence |
|---|---|---|---|
| 1 | Server starts without error | PASS / FAIL | (TestClient initialized) |
| 2 | POST /jobs returns 201 with full JobResponse | PASS / FAIL | (job_id returned) |
| 3 | GET /jobs/{id} returns 200 with same job | PASS / FAIL | (id matches) |
| 4 | Job persists in SQLite (job_storage round-trip) | PASS / FAIL | (get_job confirms) |
| 5 | created_at is recent timestamp | PASS / FAIL | (within 60s) |
| 6 | pdf_sha1 matches actual file | PASS / FAIL | (hash verify) |
| 7 | Invalid status returns 422 | PASS / FAIL | (Pydantic validation works) |
| 8 | Non-existent job returns 404 | PASS / FAIL | (data-leak guard) |

## §2 — Sacred floor verification

- Backend tests: 222/19/0 expected (216 pre-existing + 6 new E.1 tests)
- Frontend tests: 138/138 against v6.3.5 unchanged
- Vault-ruled module SHA-1s: all 5 unchanged
- v6.3.5 SHA-1: unchanged

## §3 — Overall: PASS / FAIL
```

---

## §8 — Step E1.6: PROJECT_CLAUDE.md update

Single surgical edit. Append to §3:

```
**Phase E.1 complete (2026-04-29):** FastAPI scaffold shipped with two endpoints (POST /jobs + GET /jobs/{id}) plus exempt /health probe. Backend tests 216 → 222 (six new tests including data-leak detection). Three new dependencies added: fastapi, uvicorn[standard], pydantic. Permissive CORS in dev; auth + CORS lockdown + OpenAPI docs hide deferred to Postgres/security phase. SQLite stays at ~/.tracepoint/cache.db; Postgres migration moves to backend/-relative path. 3-bidset hard gate deferred to post-Phase-G (quadrant smart scan). Silverleaf single-bidset hard gate PASS at backend/E1_HARD_GATE_silverleaf_api.md. Branch: phase2-v0.3-E1-fastapi-scaffold. E.2 (frontend strip + connect) ready to draft after Daniel review of E.1 deliverables.
```

Also update §7 phase table: E.0 → COMPLETE; E.1 → COMPLETE; E.2 → NEXT (after soft-gate review); G → INSERTED before any future multi-bidset testing.

Sections §1, §2, §4, §5, §6, §8, §9, §10 untouched.

---

## §9 — Step E1.7: BLOCK_RUN.md update

Append Phase 6 section:

```markdown
## Phase 6: E.1 — FastAPI Scaffold + First Endpoints (2026-04-29)

**Branch:** `phase2-v0.3-E1-fastapi-scaffold` (from E.0 head)
**Trigger:** Daniel directive 2026-04-29 — E.1 ships FastAPI server with 2 real endpoints + 1 exempt health probe + 6 new tests; single-bidset Silverleaf hard gate (3-bidset deferred to post-G); soft gate to E.2 after Daniel review.
**Scope discipline:** Three new deps (fastapi, uvicorn, pydantic); permissive CORS in dev; auth deferred; OpenAPI docs exposed in dev; data-leak guards in response schema and error messages; vault rule active; frontend untouched.

### Files created
- `backend/api/__init__.py`
- `backend/api/main.py`
- `backend/api/routes/__init__.py`
- `backend/api/routes/jobs.py`
- `backend/api/schemas/__init__.py`
- `backend/api/schemas/jobs.py`
- `backend/tests/test_api_jobs.py`
- `backend/scripts/e1_silverleaf_api_hardgate.py`
- `backend/E1_HARD_GATE_silverleaf_api.md`
- `backend/E1_GATE_REPORT.md`

### Files modified
- `backend/pyproject.toml` — added fastapi, uvicorn[standard], pydantic
- `backend/tests/conftest.py` — appended silverleaf_path fixture (if not already present)
- `PROJECT_CLAUDE.md` — §3 single paragraph append + §7 phase table update
- `backend/BLOCK_RUN.md` — this file

### Files deleted
None.

### Commits
(populate at session end)

### Pushes
(populate at session end)

### Dependency / config changes
Three new deps:
- `fastapi>=0.115`
- `uvicorn[standard]>=0.30`
- `pydantic>=2.7`

### Vault-ruled files touched
None. SHA-1 verification at session end (matches pre-session).

### Frontend touched
None. v6.3.5 SHA-1 verification at session end.

### Sacred floor at session end
Backend 222/19/0 (216 + 6 new E.1 tests). Frontend 138/138 against v6.3.5.
```

---

## §10 — Stop conditions

Stop, report, wait for Daniel if any fire:

1. **Sacred floor regresses.** Backend below 222/19/0 (after E.1's 6 new tests land) or frontend below 138/138.
2. **Vault-ruled module SHA-1 changes.** Should be impossible — not opened in E.1.
3. **v6.3.5 SHA-1 changes.** Frontend untouched in E.1.
4. **CLAUDE.md gets opened or edited.** Retired.
5. **PROJECT_CLAUDE.md edits exceed §8 surgical scope.** §3 paragraph append + §7 phase table update only.
6. **A test added that's not one of the 6 specified in §6.** Scope creep stop.
7. **An endpoint added that's not in scope.** Two real + one health = three endpoints total. No /jobs list, no dispatch trigger, no anything else.
8. **Auth, CORS lockdown, or OpenAPI docs hide added to E.1.** All three are deferred per Daniel directive.
9. **3-bidset hard gate attempted.** Single-bidset Silverleaf only.
10. **Silverleaf hard gate fails any criterion.**
11. **A new dependency beyond the three named (fastapi, uvicorn, pydantic) is added.**
12. **Push to origin fails.**

---

## §11 — Discipline reminders (Karpathy)

1. **Read first.** All §1 docs in full. E0_API_DESIGN.md is the contract; build against it precisely.
2. **Sacred floor first.** 222/19/0 backend (after E.1's 6 new tests), 138/138 frontend.
3. **Minimum implementation.** Two real endpoints + one health probe + six tests. Not more. The forward-compat endpoints in E0_API_DESIGN.md §5.3 are NOT built.
4. **Vault rule held.** Five trade modules untouched. v6.3.5 untouched. CLAUDE.md not opened.
5. **Data-leak discipline.** `extra="forbid"` on JobResponse. Generic error messages. Test 6 verifies both.
6. **No 3-bidset hard gate.** Compute-heavy multi-bidset testing waits for Phase G's quadrant smart scan.
7. **Soft gate to E.2.** Chain stops at E.1 hard gate PASS. Daniel reviews. Then E.2 march orders draft.

---

## §12 — Done definition (gate report checklist)

The final gate report `backend/E1_GATE_REPORT.md` confirms:

- [ ] Pre-flight: 216/19/0 backend; 138/138 frontend; vault SHA-1s captured; v6.3.5 SHA-1 captured
- [ ] Branch `phase2-v0.3-E1-fastapi-scaffold` from E.0 head
- [ ] Three deps added to pyproject.toml; imports verified
- [ ] FastAPI scaffold under `backend/api/` per §5.4 of E0_API_DESIGN.md
- [ ] Two real endpoints (POST /jobs + GET /jobs/{id}) + /health probe
- [ ] Permissive CORS configured (with `# E.1:` comment noting the deferral)
- [ ] OpenAPI docs accessible at /docs and /redoc in dev
- [ ] JobCreateRequest + JobResponse Pydantic schemas with `extra="forbid"` on response
- [ ] Six new tests in `backend/tests/test_api_jobs.py` per §6
- [ ] Backend tests 222/19/0 (216 + 6 new)
- [ ] silverleaf_path fixture in conftest.py
- [ ] Silverleaf single-bidset hard gate PASS per §7.1
- [ ] No 3-bidset hard gate attempted
- [ ] No vault-ruled module modification (5 SHA-1s match)
- [ ] No frontend SHA-1 change (v6.3.5 unchanged)
- [ ] CLAUDE.md not opened, not edited
- [ ] PROJECT_CLAUDE.md updated per §8 (§3 paragraph + §7 phase table)
- [ ] BLOCK_RUN.md Phase 6 section populated per §9
- [ ] Single commit on `phase2-v0.3-E1-fastapi-scaffold`; pushed to origin
- [ ] §10 stops: status of each enumerated explicitly
- [ ] Final gate report produced

---

## §13 — Commit shape

**Single commit** on `phase2-v0.3-E1-fastapi-scaffold`:

- All `backend/api/` files (NEW)
- `backend/tests/test_api_jobs.py` (NEW)
- `backend/tests/conftest.py` (MODIFIED if needed)
- `backend/scripts/e1_silverleaf_api_hardgate.py` (NEW)
- `backend/E1_HARD_GATE_silverleaf_api.md` (NEW)
- `backend/E1_GATE_REPORT.md` (NEW)
- `backend/pyproject.toml` (MODIFIED)
- `PROJECT_CLAUDE.md` (MODIFIED)
- `backend/BLOCK_RUN.md` (MODIFIED)

Commit message body:
- "E.1: FastAPI scaffold + 2 endpoints + 1 health probe + 6 new tests"
- "Backend 216 → 222; deps: fastapi/uvicorn/pydantic"
- "Vault SHA-1s unchanged; v6.3.5 unchanged; backend 222/19/0"
- "Silverleaf hard gate PASS"

Push at session end. Authorized.

---

## §14 — Execution mode

**Single chunk, autonomous, soft gates only.** Run E1.0 through E1.7 without per-step confirmation. Single final gate report at end.

§10 stops are the only hard pauses.

Total wall-clock estimate: ~60-90 minutes. FastAPI scaffold writing (~20 min), tests (~15 min), hard gate harness + run (~10 min), doc updates + commit + push (~15 min), pre-flight reads + buffer (~30 min).

---

## §15 — Closing

**Soft gate to E.2 after this phase ships.** Daniel reviews:

1. `backend/E1_GATE_REPORT.md` — discipline + done-definition status
2. `backend/E1_HARD_GATE_silverleaf_api.md` — empirical proof the API works end-to-end
3. The 6 new tests — confirm they cover what was intended (especially the data-leak detection)
4. The endpoint shapes vs E0_API_DESIGN.md — confirm no drift from the design contract

If E.1 looks clean: Daniel green-lights E.2 (frontend strip). Extended-thinking Claude drafts E.2 march orders.

E.2 is a re-architecture, not a refactor (per E0_FRONTEND_AUDIT.md finding: ~3,800-4,100 lines deletable, ~45% of v6.3.5). Probably needs sub-phasing: E.2.0 deletion plan + E.2.1 strip + E.2.2 connect to API. We'll discuss after E.1 ships.

Standing by for execution.

**End of MARCH_ORDERS_E_1_fastapi_scaffold.md.**
