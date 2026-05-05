"""/jobs endpoints — E.1 + E.2.2 + G.4.

Endpoints:

- POST   /jobs                              create a job  (E.1)
- GET    /jobs/{id}                         load a job    (E.1)
- POST   /jobs/{id}/dispatch                trigger dispatch  (E.2.2)
- GET    /jobs/{id}/results                 load results      (E.2.2)
- GET    /jobs/{id}/scope                   list scope systems (G.4)
- POST   /jobs/{id}/scope/systems           create manual scope system (G.4)
- PATCH  /jobs/{id}/scope/systems/{sys_id}  edit scope system (G.4)
- DELETE /jobs/{id}/scope/systems/{sys_id}  delete scope system (G.4)
- POST   /jobs/{id}/scope/rescan            reset auto rows from project_scope (G.4)

Error messages are generic to avoid leaking SQL fragments, file paths,
or tracebacks.  See backend/E0_API_DESIGN.md §5.2 + §5.13.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Response

from api.schemas.jobs import (  # E.1 + E.2.2 + G.4
    JobCreateRequest,
    JobResponse,
    JobResultsResponse,
    ScopeSystem,
    ScopeSystemCreate,
    ScopeSystemPatch,
    ScopeSystemsResponse,
    ScopeTrade,
)
from core.job_storage import (  # E.1 + E.2.2 + G.4
    create_job,
    create_scope_system,
    delete_scope_system,
    get_job,
    get_scope_system,
    list_scope_systems,
    load_dispatch_results,
    load_trade_outputs,
    rescan_scope_systems,
    update_job_status,
    update_scope_system,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/jobs", tags=["jobs"])  # E.1


@router.post("", response_model=JobResponse, status_code=201)  # E.1
def create_job_endpoint(payload: JobCreateRequest) -> JobResponse:
    """Create a job row. Returns 201 + JobResponse with computed pdf_sha1.

    Validation:
    - 422 if Pydantic rejects the input (missing name, invalid status, etc.)
    - 400 if pdf_path doesn't exist on disk (FileNotFoundError from _pdf_sha1)
    - 500 if SQLite write fails after a successful create (defensive)
    """
    try:
        job_id = create_job(  # E.1
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
    except FileNotFoundError:
        # E.1: data-leak guard — generic message, no full file path echoed back
        raise HTTPException(status_code=400, detail="pdf_path not found")
    except ValueError:
        # E.1: defensive — covers _VALID_STATUSES rejection inside create_job
        raise HTTPException(status_code=400, detail="Invalid job input")

    job = get_job(job_id)  # E.1
    if job is None:
        # E.1: data-leak guard — generic message, no SQL details
        raise HTTPException(status_code=500, detail="Job creation failed")
    return JobResponse(**job)


@router.get("/{job_id}", response_model=JobResponse)  # E.1
def get_job_endpoint(job_id: str) -> JobResponse:
    """Load a job by id. 200 + JobResponse on hit; 404 with generic detail on miss."""
    job = get_job(job_id)  # E.1
    if job is None:
        # E.1: data-leak guard — generic 404 message, no query details
        raise HTTPException(status_code=404, detail="Job not found")
    return JobResponse(**job)


# ── E.2.2 endpoints ────────────────────────────────────────────────


@router.post("/{job_id}/dispatch", response_model=JobResponse)  # E.2.2
def dispatch_job_endpoint(job_id: str) -> JobResponse:
    """Trigger synchronous dispatch. Idempotent on already-dispatched jobs.

    Status transitions: draft → dispatching → dispatched.
    Returns the updated JobResponse when dispatch completes.
    On failure, resets status to draft so the caller can retry.
    """
    from core.dispatch_gate import run_dispatch  # E.2.2: deferred import avoids circular at module load

    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if job["status"] == "dispatched":
        return JobResponse(**job)
    if job["status"] == "dispatching":
        raise HTTPException(status_code=409, detail="Dispatch already in progress")
    if not Path(job["pdf_path"]).exists():
        raise HTTPException(status_code=400, detail="pdf_path not found")

    update_job_status(job_id, "dispatching")
    try:
        run_dispatch(pdf_path=job["pdf_path"], storage="auto", job_id=job_id)
    except Exception:
        logger.exception("dispatch failed for job_id=%s", job_id)
        update_job_status(job_id, "draft")
        raise HTTPException(status_code=500, detail="Internal server error")

    update_job_status(job_id, "dispatched")
    refreshed = get_job(job_id)
    return JobResponse(**refreshed)


@router.get("/{job_id}/results", response_model=JobResultsResponse)  # E.2.2
def get_job_results_endpoint(job_id: str) -> JobResultsResponse:
    """Load dispatch results + trade outputs for a completed job.

    Returns string-keyed dicts (page indices as ``"0"``, ``"1"``, …).
    409 if the job has not been dispatched yet.
    """
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if job["status"] != "dispatched":
        raise HTTPException(status_code=409, detail="Job not yet dispatched")

    raw_dispatch = load_dispatch_results(job_id)
    raw_trades = load_trade_outputs(job_id)

    dispatch_by_page = {str(k): v for k, v in raw_dispatch.items()}
    trade_by_page: dict[str, dict] = {}
    for page_key in dispatch_by_page:
        idx = int(page_key)
        trade_by_page[page_key] = raw_trades.get(idx, {"roofing": None, "glazing": None})

    return JobResultsResponse(
        job_id=job_id,
        dispatch_results=dispatch_by_page,
        trade_outputs=trade_by_page,
    )


# ── G.4 endpoints — scope tab as backend-DB-frontend cycle ────────────


@router.get("/{job_id}/scope", response_model=ScopeSystemsResponse)  # G.4
def list_job_scope_endpoint(
    job_id: str,
    trade: Optional[ScopeTrade] = Query(None),
) -> ScopeSystemsResponse:
    """List scope_systems rows for a job, optionally filtered by trade.
    Always returns 200 (empty systems list if nothing yet)."""
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    rows = list_scope_systems(job_id, trade=trade)
    return ScopeSystemsResponse(
        job_id=job_id,
        trade=trade,
        systems=[ScopeSystem(**r) for r in rows],
    )


@router.post(
    "/{job_id}/scope/systems",
    response_model=ScopeSystem,
    status_code=201,
)  # G.4
def create_scope_system_endpoint(
    job_id: str,
    payload: ScopeSystemCreate,
) -> ScopeSystem:
    """Create a manual scope_systems row for a job. Returns 201 + the new row."""
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    try:
        row = create_scope_system(
            job_id,
            trade=payload.trade,
            label=payload.label,
            system_code=payload.system_code,
            user_fields=payload.user_fields,
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid scope system input")
    return ScopeSystem(**row)


@router.patch(
    "/{job_id}/scope/systems/{sys_id}",
    response_model=ScopeSystem,
)  # G.4
def patch_scope_system_endpoint(
    job_id: str,
    sys_id: str,
    payload: ScopeSystemPatch,
) -> ScopeSystem:
    """Patch a scope_systems row. Only provided fields are updated."""
    existing = get_scope_system(sys_id)
    if existing is None or existing["job_id"] != job_id:
        raise HTTPException(status_code=404, detail="Scope system not found")
    try:
        updated = update_scope_system(
            sys_id,
            label=payload.label,
            system_code=payload.system_code,
            user_fields=payload.user_fields,
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid scope system input")
    if updated is None:
        raise HTTPException(status_code=404, detail="Scope system not found")
    return ScopeSystem(**updated)


@router.delete(
    "/{job_id}/scope/systems/{sys_id}",
    status_code=204,
)  # G.4
def delete_scope_system_endpoint(job_id: str, sys_id: str) -> Response:
    """Delete a scope_systems row. 204 on success, 404 if not found."""
    existing = get_scope_system(sys_id)
    if existing is None or existing["job_id"] != job_id:
        raise HTTPException(status_code=404, detail="Scope system not found")
    if not delete_scope_system(sys_id):
        raise HTTPException(status_code=404, detail="Scope system not found")
    return Response(status_code=204)


@router.post(
    "/{job_id}/scope/rescan",
    response_model=ScopeSystemsResponse,
)  # G.4
def rescan_scope_endpoint(
    job_id: str,
    trade: ScopeTrade = Query(...),
) -> ScopeSystemsResponse:
    """Reset auto-source scope_systems rows for a job+trade by re-deriving
    from the persisted project_scope blob. Manual rows untouched."""
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    try:
        rows = rescan_scope_systems(job_id, trade)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid trade")
    return ScopeSystemsResponse(
        job_id=job_id,
        trade=trade,
        systems=[ScopeSystem(**r) for r in rows],
    )
