"""/jobs endpoints — E.1.

Two real endpoints:

- POST /jobs       create a job (calls `core.job_storage.create_job`)
- GET  /jobs/{id}  load a job  (calls `core.job_storage.get_job`)

Both use the Pydantic schemas in `api.schemas.jobs`. Error messages are
generic ("Job not found", "Job creation failed") to avoid leaking SQL
fragments, file paths, or tracebacks. See backend/E0_API_DESIGN.md §5.2.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.schemas.jobs import JobCreateRequest, JobResponse  # E.1
from core.job_storage import create_job, get_job  # E.1

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
