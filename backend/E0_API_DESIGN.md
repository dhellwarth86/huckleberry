# E.0 API Design — FastAPI Surface for Phase E.1

**Date:** 2026-04-30
**Branch:** `phase2-v0.3-E0-api-design-and-frontend-audit`
**Status:** Design contract for E.1 — Daniel reviews and approves before E.1 builds.
**Scope:** E.1's two endpoints only. Future endpoints (E.2 / E.3) are sketched as forward-compat reference, not built.
**Companion:** `backend/E0_FRONTEND_AUDIT.md` (the strip target this API serves into)

---

## §5.1 — Stack decisions

| Concern | Decision | Reason |
|---|---|---|
| **Framework** | **FastAPI** | Daniel directive 2026-04-29 — chosen over Django Ninja. Keeps the stack lean; preserves the stdlib-`sqlite3` storage port (B.4 + D.2); Django freebies (admin, ORM, auth) arrive when needed in the same window as Postgres migration, not before. |
| **ASGI server** | **uvicorn** (with `[standard]` extras for httptools + uvloop where available) | FastAPI's standard pairing |
| **Validation** | **Pydantic v2** | FastAPI native; integrates with OpenAPI generation |
| **Auth** | **None in E.1** | Daniel directive — auth + security + multi-tenant isolation come at user-testing time as a separate phase. E.1 ships with no auth headers, no API key, no CORS lockdown. Local-dev only until that phase ships. |
| **Database access** | **stdlib `sqlite3` via `core.job_storage`** | D.2's `job_storage.py` is the data-access layer. **No SQLAlchemy. No ORM.** API routes call `job_storage.create_job` / `get_job` directly. |
| **CORS** | **Permissive in dev** (`allow_origins=["*"]`) | Frontend will run from `file://` or simple static serve in dev; locked-down origins arrive with the auth phase |
| **Error format** | **FastAPI `HTTPException` with consistent JSON shape** | `{"detail": "<message>"}` is FastAPI default; we don't customize for E.1. Future phases can add a structured-error middleware if needed. |
| **Logging** | **Python stdlib `logging`** | No structured-logging library in E.1. Stdlib logger configured to stdout at INFO level; uvicorn handles request access logs. |
| **Process model** | **Single process, single worker for dev** | `uvicorn api.main:app --reload --port 8000`. Production multi-worker setup deferred until deployment phase. |
| **Storage location** | **Same `~/.tracepoint/cache.db`** that D.2 writes to | One SQLite file, shared between dispatch_gate writes and API reads. No separate dev/prod DBs in E.1. |

---

## §5.2 — Endpoints (E.1 ships exactly these two)

### Endpoint A — `POST /jobs`

**Purpose:** Create a job row with metadata + computed `pdf_sha1`. Does NOT trigger dispatch — dispatch is a separate `POST /jobs/{id}/dispatch` endpoint reserved for E.2.

**Request (Pydantic schema `JobCreateRequest`):**

```json
{
  "name": "B2607 AEA Silverleaf",
  "pdf_path": "C:\\huck stage 2\\full bid sets\\B2607 AEA Silverleaf - St Augustine - Accelerated Construction Services (6).pdf",
  "gc": "Accelerated Construction Services",
  "location_city": "St Augustine",
  "location_state": "FL",
  "trade_scope": "roofing,glazing",
  "bid_due_date": "2026-05-15",
  "notes": null
}
```

**Field rules:**

| Field | Type | Required | Validation |
|---|---|---|---|
| `name` | str | yes | non-empty, max 255 |
| `pdf_path` | str | yes | non-empty; **E.1 trusts the caller** — file existence check happens at `create_job` time via `_pdf_sha1` (which raises `FileNotFoundError` if absent). E.1 surfaces that as 400. |
| `gc` | str \| null | no | max 255 |
| `location_city` | str \| null | no | max 255 |
| `location_state` | str \| null | no | max 2 (US state abbrev) — soft check, not strict regex |
| `trade_scope` | str | no, default `"roofing"` | comma-separated trades; non-empty |
| `bid_due_date` | str \| null | no | ISO 8601 date string `YYYY-MM-DD`; Pydantic validates if present |
| `notes` | str \| null | no | max 4000 |

**Response (Pydantic schema `JobResponse`, HTTP 201 Created):**

```json
{
  "id": "45d58c49-2e78-41d7-91c4-759a7a8de0de",
  "name": "B2607 AEA Silverleaf",
  "gc": "Accelerated Construction Services",
  "location_city": "St Augustine",
  "location_state": "FL",
  "trade_scope": "roofing,glazing",
  "bid_due_date": "2026-05-15",
  "notes": null,
  "status": "draft",
  "created_at": "2026-04-30T14:32:11.123456+00:00",
  "updated_at": "2026-04-30T14:32:11.123456+00:00",
  "pdf_path": "C:\\huck stage 2\\full bid sets\\B2607 AEA Silverleaf - St Augustine - Accelerated Construction Services (6).pdf",
  "pdf_sha1": "76dc89072dae77c1b476b60da85870f3d799cd31",
  "dispatch_complete": false
}
```

**Errors:**

| Status | Trigger | Body |
|---|---|---|
| 400 | `pdf_path` does not exist on disk (caught from `_pdf_sha1`'s `FileNotFoundError`) | `{"detail": "pdf_path not found: <path>"}` |
| 400 | Invalid `status` (defensive — `create_job` raises `ValueError`) | `{"detail": "<exception message>"}` |
| 422 | Pydantic validation failure (missing required field, wrong type) | FastAPI default validation envelope |
| 500 | Unexpected SQLite write failure | `{"detail": "Internal server error"}` |

**Implementation sketch:**

```python
# backend/api/routes/jobs.py
from fastapi import APIRouter, HTTPException, status
from core.job_storage import create_job, get_job
from api.schemas.jobs import JobCreateRequest, JobResponse

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job_endpoint(req: JobCreateRequest) -> JobResponse:
    try:
        job_id = create_job(
            name=req.name,
            pdf_path=req.pdf_path,
            gc=req.gc,
            location_city=req.location_city,
            location_state=req.location_state,
            trade_scope=req.trade_scope,
            bid_due_date=req.bid_due_date,
            notes=req.notes,
        )
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail=f"pdf_path not found: {req.pdf_path}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    job = get_job(job_id)
    if job is None:
        # Should be impossible immediately after create_job
        raise HTTPException(status_code=500, detail="job not found after create")
    return JobResponse(**job)
```

### Endpoint B — `GET /jobs/{job_id}`

**Purpose:** Load a job's full row by id.

**Request:** Path parameter `job_id: str` (UUID).

**Response (Pydantic schema `JobResponse`, HTTP 200 OK):** Same shape as the POST response above.

**Errors:**

| Status | Trigger | Body |
|---|---|---|
| 404 | `get_job(job_id)` returns `None` | `{"detail": "Job not found"}` |
| 422 | `job_id` parameter is malformed (FastAPI validates path param shape; we don't strictly type it as UUID — accept any string and let `get_job` return None) | (only if we choose strict UUID typing — recommend NOT, keep it permissive) |
| 500 | SQLite read failure | `{"detail": "Internal server error"}` |

**Implementation sketch:**

```python
@router.get("/{job_id}", response_model=JobResponse)
def get_job_endpoint(job_id: str) -> JobResponse:
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobResponse(**job)
```

### Notably absent from E.1

E.1 does NOT include:

- File upload (`POST /jobs` takes a `pdf_path` string, not multipart upload). File-upload handling lives in a later phase that touches the upload pipeline + storage location decisions.
- Triggering dispatch (no `POST /jobs/{id}/dispatch`). Reserved for E.2.
- Listing or filtering jobs (no `GET /jobs`). Reserved for E.2.
- Loading dispatch results / trade outputs (no `GET /jobs/{id}/results`). Reserved for E.2.
- Updating job metadata or status. Reserved for E.2.
- Annotation save/load. Reserved for E.3.

The minimal pair (POST + GET single) is intentional — E.1 proves the FastAPI-on-top-of-D.2 stack works end-to-end with the smallest possible surface, then E.2 expands.

---

## §5.3 — Endpoints reserved for E.2 / E.3 (sketched, not built)

These are forward-compat sketches so E.1 doesn't accidentally paint into a corner. Shapes will firm up in their own march orders.

### `POST /jobs/{job_id}/dispatch` (E.2)

**Purpose:** Trigger `run_dispatch(pdf_path, storage="auto", job_id=...)` for a created job. Returns `200 OK` when complete, or `202 Accepted` if we move to async dispatch (likely needed; Vine Street took 1195s in D.2).

**Open design questions for E.2:**
- Sync vs. async (background task, SSE, or webhook poll)? A 1195s sync request is unworkable for a real frontend; some form of progress reporting is needed.
- Lock state during in-progress dispatch?

### `GET /jobs/{job_id}/results` (E.2)

**Purpose:** Return `dispatch_results` + `trade_outputs` for the job. Reverse of `persist_dispatch_result` + `persist_trade_outputs`.

**Sketch response:**
```json
{
  "job_id": "...",
  "dispatch_results": {
    "0": { "page_idx": 0, "page_type": "cover", "sheet_num": "G-001", ... },
    "1": { ... }
  },
  "trade_outputs": {
    "0": { "roofing": { "fields": {...}, "warnings": [], ... }, "glazing": {...} },
    "1": { ... }
  }
}
```

### `GET /jobs` (E.2)

**Purpose:** List jobs with sort + filter. Backed by `list_jobs(sort_by, sort_order, filter_gc, filter_status, filter_state)`.

**Sketch:**
- Query params: `sort_by`, `sort_order`, `filter_gc`, `filter_status`, `filter_state`
- Response: `[JobResponse, ...]`
- Pagination deferred (jobs count will be small in early use)

### `PUT /jobs/{job_id}` and `PATCH /jobs/{job_id}/status` (E.2)

**Purpose:** Update job metadata (full PUT) or single status transition (PATCH). Backed by `update_job_status` and a new `update_job` helper that E.2 adds to `job_storage.py`.

### `POST /jobs/{job_id}/annotations` (E.3)

**Purpose:** Save user annotations (pin placements, line measurements, polygon areas) per page per system. Requires a new `annotations` table — schema design is E.3's job.

### `GET /jobs/{job_id}/debug` (E.2 or E.3)

**Purpose:** Wrap `debug_module.run_debug(ctx)` for the loaded job. Sections 1 (dispatch health), 3 (page intelligence), 6 (legends + quality flags) are the minimum useful surface.

**Open question:** debug_module currently consumes `ctx`, not `job_id`. Either reconstitute a partial ctx from `dispatch_results` + `trade_outputs` (requires shimming) or extract debug-friendly fields at dispatch time and persist them (requires schema addition). Either way an E.2/E.3 design decision.

---

## §5.4 — Project structure

E.1 introduces a new top-level `backend/api/` directory. No existing files moved. No existing tests broken. No `pyproject.toml` modifications by E.0 (E.1 adds three deps — see §5.5).

```
backend/
├── api/                        # NEW (E.1)
│   ├── __init__.py             # NEW — package marker (empty)
│   ├── main.py                 # NEW — FastAPI app + CORS middleware + router includes
│   ├── routes/
│   │   ├── __init__.py         # NEW
│   │   └── jobs.py             # NEW — POST /jobs + GET /jobs/{id}
│   └── schemas/
│       ├── __init__.py         # NEW
│       └── jobs.py             # NEW — JobCreateRequest + JobResponse Pydantic models
├── core/                       # UNCHANGED — vault-ruled (5 modules) + dispatch_gate + job_storage + others
├── scripts/                    # UNCHANGED in E.1
├── seeds/                      # UNCHANGED
├── tests/                      # E.1 ADDS test_api_jobs.py only; existing tests untouched
└── (existing reports/markdown remain at backend/ root)
```

**`backend/api/main.py` skeleton (~30 lines):**

```python
"""FastAPI application — E.1 ships with /jobs only."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import jobs as jobs_routes

app = FastAPI(
    title="Huckleberry API",
    version="0.3.0-E.1",
    description="Backend API for the Huckleberry takeoff platform.",
)

# Permissive CORS for E.1 dev — locked down with auth phase
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs_routes.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
```

A `/health` endpoint is a small bonus that costs nothing and pays off in the very first deployment moment. **It is NOT counted as a third endpoint** — it is a no-state liveness probe with zero coupling to job_storage.

---

## §5.5 — Dependencies

**E.0 adds zero dependencies.** This is enforced by §9 #8 (stop condition).

**E.1 adds exactly three pyproject.toml dependencies:**

| Package | Pin | Purpose |
|---|---|---|
| `fastapi` | `>=0.115` | API framework |
| `uvicorn[standard]` | `>=0.30` | ASGI server (the `[standard]` extras include httptools + uvloop + watchfiles) |
| `pydantic` | `>=2.7` | Validation (FastAPI's transitive dep, but pinning explicitly makes the schema layer's expectations clear) |

**Not added:**

- ❌ SQLAlchemy — D.2 chose stdlib `sqlite3` deliberately
- ❌ JWT / passlib / python-jose — auth is later
- ❌ httpx (FastAPI ships TestClient via starlette) — keep it minimal
- ❌ structlog / loguru — stdlib `logging` for now
- ❌ python-multipart — not needed in E.1 (no file upload)

**E.1's pyproject.toml change is small and local:** add three lines under `[project.dependencies]` (or `[tool.poetry.dependencies]` depending on the existing format — needs to be confirmed against the current pyproject in E.1).

---

## §5.6 — Run instructions (E.1 deliverable)

```bash
cd backend
uvicorn api.main:app --reload --port 8000
```

OpenAPI docs auto-generated at:
- `http://localhost:8000/docs` — Swagger UI
- `http://localhost:8000/redoc` — ReDoc

Health probe:
- `http://localhost:8000/health` → `{"status": "ok"}`

Smoke test (with curl, after creating a Silverleaf job manually via `d2_silverleaf_reference.py`):
```bash
curl http://localhost:8000/jobs/45d58c49-2e78-41d7-91c4-759a7a8de0de
# expects 200 + JobResponse body
```

---

## §5.7 — Test strategy for E.1

E.1 adds **one new test file**: `backend/tests/test_api_jobs.py`. Existing test count goes from **216 → ~220** (exact count depends on assertion granularity).

**Test approach:**

- Use FastAPI's `TestClient` (starlette under the hood). In-process, no network. Fast.
- Each test creates a temporary SQLite DB by setting `DB_PATH` to a tmp_path fixture, OR uses the shared cache.db with cleanup. **Recommended:** isolated tmp DB per test for clean state.
- Round-trip test: POST a synthetic job (using a small fixture PDF — backend already has fixtures from D.2), GET the same job_id, assert returned fields match what was POSTed.
- Error tests: POST with missing `name` → 422; POST with non-existent `pdf_path` → 400; GET with random UUID → 404.
- Storage integration: after POST, call `core.job_storage.get_job` directly and verify the row matches the API response.

**Test cases (~4 tests, parametrized may collapse to fewer files):**

1. `test_create_job_returns_201_with_full_payload` — POST happy path.
2. `test_create_job_400_when_pdf_path_missing` — POST error path.
3. `test_create_job_422_when_name_missing` — Pydantic validation.
4. `test_get_job_returns_200_with_full_payload` — GET happy path (round-trip from create).
5. `test_get_job_returns_404_for_unknown_id` — GET miss path.
6. (optional) `test_get_job_pdf_sha1_matches_disk_sha1` — verifies the ingestion path didn't corrupt the SHA-1 on round-trip.

E.1 march orders should set the test floor as **216 → at least 219**, allow a window up to 222.

**Test fixture needs:**
- A small fixture PDF (the existing `backend/test_fixtures/` will likely have one; if not, E.1 adds a tiny synthetic single-page PDF — bytes generated in `conftest.py` via `pypdf` or a fixture file).
- A `tmp_path`-scoped DB override mechanism (likely a small `monkeypatch` of `core.storage.DB_PATH` or `core.job_storage._get_db_path`).

---

## §5.8 — What E.0 explicitly does NOT decide

- **Auth implementation.** No JWT shape, no API-key strategy, no session model. Whole separate phase.
- **Frontend → backend connection mechanism.** E.2 designs the fetch/axios glue; E.0 only specifies the API surface that glue will hit.
- **File upload handling.** Multipart, presigned URLs, local-file references — none decided. E.1 takes paths because it's the cheapest unblock.
- **Pagination strategy** for list endpoints. Defer to E.2 when `GET /jobs` lands and we know the realistic job count.
- **Webhooks / events** for long-running dispatch. Defer to E.2 dispatch endpoint.
- **Rate limiting.** Not E.1.
- **Multi-tenant isolation.** GC is the natural tenant key per D.2's design, but enforcement is auth-phase work.
- **Async dispatch progress reporting.** Vine Street's 1195s dispatch makes this E.2's most interesting design problem; not solved here.
- **Migrations.** Schema changes after D.2 are minimal in E.1 (zero — no new tables). When E.3 adds annotations, a small migration helper appears in `job_storage.py` or a sibling module — not E.1's concern.
- **Postgres migration.** Decision Q2 reversed for D.2 (SQLite stays). Postgres migration is a deployment-phase decision; E.1 keeps SQLite.

---

## §5.9 — Forward-compat shape commitments E.1 should preserve

These are the small-but-load-bearing API design choices E.1 should ship with so E.2/E.3 don't paint into corners:

1. **`JobResponse` includes `pdf_sha1`** even though most consumers won't use it. Cheap to ship; useful for caching, idempotency, and "is this the same PDF" checks later.
2. **All datetime fields are RFC 3339 / ISO 8601 strings with timezone.** Already the case in `job_storage` (`datetime.now(timezone.utc).isoformat()`). Don't strip timezone.
3. **`status` field is a string with a known enum** (`draft`, `dispatched`, `in_review`, `exported`, `archived`) — Pydantic should use `Literal[...]` for response typing so OpenAPI documents the values, but accept arbitrary strings on the input side (defensive — backend validates via `_VALID_STATUSES`).
4. **No camelCase/snake_case translation layer.** API uses `snake_case` matching the SQLite columns. The frontend will adapt; cheaper than a translation middleware.
5. **`trade_scope` stays a comma-separated string** for E.1, matching the DB column. If a structured list shape is needed later (E.3+), the API can accept either via a Pydantic union type. Don't pre-build that.
6. **HTTP 201 Created for POST**, 200 OK for GET. Standard, predictable.

---

## §5.10 — Minimal-implementation discipline note

This design specifies what E.1 builds. Two endpoints. One health probe. One test file with ~4–6 tests. Three new dependencies. Approximately 200–300 lines of new Python total, including tests.

The temptation in API work is to pre-build the third, fourth, fifth endpoints "while we're in here." Resist. E.1 ships the smallest demonstrable surface, and E.2/E.3 expand from a proven base. The endpoints reserved in §5.3 are sketches, not orders.

The frontend audit (`backend/E0_FRONTEND_AUDIT.md`) shows that the strip work is the larger lift in Phase E. The API surface stays small and stable; the frontend changes a lot.

---

## §5.11 — Open questions for Daniel review

Daniel may flag any of the following before E.1 march orders are drafted:

1. **`pdf_path` as a string in `POST /jobs` request body** — comfortable with this for E.1 dev, or push for upload-from-the-start? My read: comfortable for E.1 (matches D.2 reference run pattern), but E.2 likely needs upload.
2. **Permissive CORS in E.1 dev** — fine, or lock it down even before auth phase? My read: fine.
3. **Health probe at `/health`** — counts as a third endpoint or an exempt liveness probe? My read: exempt; it's stateless and trivial.
4. **Test count window 216 → 219–222 in E.1** — comfortable, or set a tighter target? My read: 219 is the minimum (4 happy-path tests); 222 is the upper bound (6 tests including edge cases). E.1 march orders pick.
5. **`status` field validation strategy on the input side** — strict `Literal[...]` (Pydantic enforces) or permissive string + DB-side validation? My read: permissive on input, strict in OpenAPI docs via `Literal[...]` on response model only. Daniel may prefer strict input validation.
6. **OpenAPI auto-docs at `/docs` and `/redoc`** — fine, or hide them in production? My read: fine; production decision later.

Default position on all open questions: ship the simpler answer, defer the harder answer to its own phase.

---

## §5.12 — Corrigenda — landed during E.1

E.1 shipped against this design contract on 2026-04-30. Two small spec updates were landed in a follow-up discipline-patches branch (`phase2-v0.3-E1-discipline-patches`) so the design doc tracks what actually shipped, not what was first drafted. Both are surface-level — the contract itself is unchanged.

### Corrigendum 1 — 404 response body

**Spec drafted:** `{"detail": "job not found: <job_id>"}` (echoed user-supplied id).
**Shipped (canonical):** `{"detail": "Job not found"}` (no echo of user input).

**Reason:** Tighter data-leak posture. Reflecting the user-supplied `job_id` back into the 404 body is a small but real attack surface — it lets a caller distinguish between "id format invalid" and "id format valid but not in DB" through response-body shape, and confirms reflection of user input is happening at all. The shipped form stays opaque and matches the generic error-message discipline already applied to `POST /jobs` failures ("Job creation failed", "pdf_path not found").

This is the canonical form going forward; spec table and implementation sketch in §5.2 updated to match ship.

### Corrigendum 2 — `version` string in `FastAPI(...)` constructor

**Spec drafted:** `version="0.1.0"` (placeholder).
**Shipped (canonical):** `version="0.3.0-E.1"` (per `<phase2-version>-<phase-stage>` pattern).

**Reason:** Adopt a version-string convention that ties the API surface to the phase that shipped it. Going forward:

- Each E sub-phase increments the suffix: E.2 → `0.3.0-E.2`, E.3 → `0.3.0-E.3`.
- Each new letter-phase increments the minor: F → `0.4.0-F.0`, G → `0.5.0-G.0`.
- The major (`0.x.x`) stays at `0` until the v1 ship; the minor tracks Phase-2 stage; the patch stays `0` for now (reserved for hotfixes within a phase).

Spec updated to match ship; pattern adopted as project convention.

### Corrigendum 2026-04-30 (3) — CHECKING replaces DEGRADED in E.2.0/E.2.1 status bar spec

**What changed:** E.2.0's `E2_0_NEW_FILE_DESIGN.md` §5 specifies a 3-state status bar with states CHECKING / CONNECTED / UNREACHABLE. The original E.0 planning conversation locked DEGRADED as the third state (CONNECTED / DEGRADED / UNREACHABLE). The shipped design replaces DEGRADED with CHECKING.

**Reason:** With no auth and permissive CORS in E.1/E.2, no realistic DEGRADED scenario exists. The "backend reachable but unhealthy" case the DEGRADED state was meant to capture (e.g., 503 from auth-rejecting middleware) does not arise pre-security-phase. CHECKING captures the genuinely useful "first 30s before /health responds" transition state, which the original 3-state design omitted.

**Forward note:** When auth + CORS lockdown ship in the Postgres/security phase, DEGRADED gets re-evaluated as part of that phase. The 503-style "reachable but rejecting" case is a real diagnostic surface once auth exists. At that point either: (a) DEGRADED is added as a 4th state, or (b) UNREACHABLE is split into UNREACHABLE/REJECTING, or (c) the security phase produces a different state machine entirely. Decision deferred to that phase's own march orders.

**Canonical going forward (through E.2 + E.3):** 3 states are CHECKING / CONNECTED / UNREACHABLE per `E2_0_NEW_FILE_DESIGN.md` §5. Shipped in E.2.1 (`frontend/src/Huckleberry_AI_phase2.v1.0.0.html`).

---

**End of API design. E.1 builds against this contract.**
