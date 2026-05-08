"""/jobs endpoints — E.1 + E.2.2 + G.4 + G.5a.

Endpoints:

- POST   /jobs/upload                       create a job (multipart upload)  (G.4 CP2)
- GET    /jobs/{id}                         load a job    (E.1)
- GET    /jobs/{id}/pdf                     download the stored PDF bytes    (G.4 CP2)
- POST   /jobs/{id}/dispatch                trigger dispatch                 (E.2.2)
- GET    /jobs/{id}/results                 load results                     (E.2.2)
- GET    /jobs/{id}/scope                   list scope systems               (G.4)
- POST   /jobs/{id}/scope/systems           create manual scope system       (G.4)
- PATCH  /jobs/{id}/scope/systems/{sys_id}  edit scope system                (G.4)
- DELETE /jobs/{id}/scope/systems/{sys_id}  delete scope system              (G.4)
- POST   /jobs/{id}/scope/rescan            reset auto rows from project_scope (G.4)
- GET    /jobs/{id}/annotations             list annotations (filters: page/system/type/source) (G.5a)
- POST   /jobs/{id}/annotations             create manual annotation         (G.5a)
- PATCH  /jobs/{id}/annotations/{ann_id}    edit annotation (full-row replace) (G.5a)
- DELETE /jobs/{id}/annotations/{ann_id}    delete annotation                (G.5a)

G.4 CP3 retired the JSON path-string POST /jobs endpoint. Multipart
upload is the single upload point. Dev scripts that need direct dispatch
on a local PDF path call core.dispatch_gate.run_dispatch directly
without going through the API (see backend/scripts/d2_*.py).

Error messages are generic to avoid leaking SQL fragments, file paths,
or tracebacks.  See backend/E0_API_DESIGN.md §5.2 + §5.13.
"""
from __future__ import annotations

import logging
import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, Query, Response, UploadFile
from fastapi.responses import FileResponse

from api.schemas.jobs import (  # E.1 + E.2.2 + G.4 + G.5a
    Annotation,
    AnnotationCreate,
    AnnotationPatch,
    AnnotationsResponse,
    AnnotationType,
    AnnotationSource,
    JobResponse,
    JobResultsResponse,
    ScopeSystem,
    ScopeSystemCreate,
    ScopeSystemPatch,
    ScopeSystemsResponse,
    ScopeTrade,
)
from core.job_storage import (  # E.1 + E.2.2 + G.4 + G.5a
    create_annotation,
    create_job,
    create_scope_system,
    delete_annotation,
    delete_scope_system,
    get_annotation,
    get_job,
    get_scope_system,
    list_annotations,
    list_scope_systems,
    load_dispatch_results,
    load_trade_outputs,
    rescan_scope_systems,
    store_uploaded_pdf,
    update_annotation,
    update_job_status,
    update_scope_system,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/jobs", tags=["jobs"])  # E.1

# G.4 CP3: POST /jobs (JSON path-string) endpoint retired. Multipart upload
# at POST /jobs/upload is the single upload point. See module docstring.


@router.get("/{job_id}", response_model=JobResponse)  # E.1
def get_job_endpoint(job_id: str) -> JobResponse:
    """Load a job by id. 200 + JobResponse on hit; 404 with generic detail on miss."""
    job = get_job(job_id)  # E.1
    if job is None:
        # E.1: data-leak guard — generic 404 message, no query details
        raise HTTPException(status_code=404, detail="Job not found")
    return JobResponse(**job)


# ── G.4 CP2 — multipart upload + file serving ────────────────────────


@router.post("/upload", response_model=JobResponse, status_code=201)  # G.4 CP2
async def create_job_via_upload(
    file: UploadFile = File(...),
    name: str = Form(..., min_length=1, max_length=200),
    trade_scope: str = Form("roofing"),
    gc: Optional[str] = Form(None),
    location_city: Optional[str] = Form(None),
    location_state: Optional[str] = Form(None),
    bid_due_date: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
) -> JobResponse:
    """Multipart upload variant of POST /jobs.

    Receives a PDF as multipart/form-data, writes the bytes to
    ~/.tracepoint/uploads/{job_id}/source.pdf, then creates the
    job row pointing at that path. Status defaults to draft.

    The JSON-path-string variant (POST /jobs) is kept for backwards
    compatibility through CP2 and retired in CP3.
    """
    # Reject non-PDF content types (defensive — frontend's <input accept>
    # already filters, but the API shouldn't trust the client).
    if file.content_type and file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(status_code=415, detail="PDF required")
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="empty upload")

    # Pre-generate the job id so the file lands at the keyed path before
    # we create the DB row that references it.
    new_job_id = str(uuid.uuid4())

    try:
        stored_path = store_uploaded_pdf(new_job_id, content)
    except OSError:
        # G.4: data-leak guard — don't echo paths or filesystem errors.
        raise HTTPException(status_code=500, detail="upload storage failed")

    try:
        job_id = create_job(
            name=name,
            pdf_path=str(stored_path),
            job_id=new_job_id,
            gc=gc,
            location_city=location_city,
            location_state=location_state,
            trade_scope=trade_scope,
            bid_due_date=bid_due_date,
            notes=notes,
        )
    except FileNotFoundError:
        # Defensive — shouldn't happen since we just wrote it.
        raise HTTPException(status_code=500, detail="upload missing after write")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid job input")

    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=500, detail="Job creation failed")
    return JobResponse(**job)


@router.get("/{job_id}/pdf")  # G.4 CP2
def get_job_pdf_endpoint(job_id: str) -> FileResponse:
    """Stream the stored PDF bytes for a job. 404 if job or file missing."""
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    pdf_path = job["pdf_path"]
    if not pdf_path or not Path(pdf_path).exists():
        raise HTTPException(status_code=404, detail="PDF not found")
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=Path(pdf_path).name,
    )


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


# ── G.5a endpoints — annotations CRUD ────────────────────────────────


@router.get("/{job_id}/annotations", response_model=AnnotationsResponse)  # G.5a
def list_job_annotations_endpoint(
    job_id: str,
    page_idx: Optional[int] = Query(None, ge=0),
    system_id: Optional[str] = Query(None),
    type: Optional[AnnotationType] = Query(None),
    source: Optional[AnnotationSource] = Query(None),
) -> AnnotationsResponse:
    """List annotation rows for a job, optionally filtered by page_idx,
    system_id, type, or source. Always 200 (empty list if nothing yet)."""
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    rows = list_annotations(
        job_id, page_idx=page_idx, system_id=system_id, type=type, source=source,
    )
    return AnnotationsResponse(
        job_id=job_id,
        annotations=[Annotation(**r) for r in rows],
    )


@router.post(
    "/{job_id}/annotations",
    response_model=Annotation,
    status_code=201,
)  # G.5a
def create_annotation_endpoint(
    job_id: str,
    payload: AnnotationCreate,
) -> Annotation:
    """Create a manual annotation row. Returns 201 + the new row."""
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    try:
        row = create_annotation(
            job_id,
            type=payload.type,
            page_idx=payload.page_idx,
            system_id=payload.system_id,
            source="manual",
            data=payload.data,
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid annotation input")
    return Annotation(**row)


@router.patch(
    "/{job_id}/annotations/{ann_id}",
    response_model=Annotation,
)  # G.5a
def patch_annotation_endpoint(
    job_id: str,
    ann_id: str,
    payload: AnnotationPatch,
) -> Annotation:
    """Patch an annotation row. Full-row replace semantics on `data` per Q4."""
    existing = get_annotation(ann_id)
    if existing is None or existing["job_id"] != job_id:
        raise HTTPException(status_code=404, detail="Annotation not found")
    try:
        updated = update_annotation(
            ann_id,
            page_idx=payload.page_idx,
            system_id=payload.system_id,
            data=payload.data,
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid annotation input")
    if updated is None:
        raise HTTPException(status_code=404, detail="Annotation not found")
    return Annotation(**updated)


@router.delete(
    "/{job_id}/annotations/{ann_id}",
    status_code=204,
)  # G.5a
def delete_annotation_endpoint(job_id: str, ann_id: str) -> Response:
    """Delete an annotation row. 204 on success, 404 if not found."""
    existing = get_annotation(ann_id)
    if existing is None or existing["job_id"] != job_id:
        raise HTTPException(status_code=404, detail="Annotation not found")
    if not delete_annotation(ann_id):
        raise HTTPException(status_code=404, detail="Annotation not found")
    return Response(status_code=204)
