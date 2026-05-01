"""/jobs endpoints — E.1 + E.2.2.

Four real endpoints:

- POST /jobs              create a job  (E.1)
- GET  /jobs/{id}         load a job    (E.1)
- POST /jobs/{id}/dispatch  trigger dispatch  (E.2.2)
- GET  /jobs/{id}/results   load results      (E.2.2)

Error messages are generic to avoid leaking SQL fragments, file paths,
or tracebacks.  See backend/E0_API_DESIGN.md §5.2 + §5.13.
"""
from __future__ import annotations

import logging
from pathlib import Path

from fastapi import APIRouter, HTTPException

from api.schemas.jobs import JobCreateRequest, JobResponse, JobResultsResponse  # E.1 + E.2.2
from core.job_storage import (  # E.1 + E.2.2
    create_job,
    get_job,
    load_dispatch_results,
    load_trade_outputs,
    update_job_status,
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
