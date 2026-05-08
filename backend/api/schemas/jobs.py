"""Pydantic v2 schemas for the /jobs endpoints — E.1 + G.4.

Shapes:

- `JobResponse`: GET /jobs/{id} and POST /jobs/upload response. `extra="forbid"`
  is the data-leak guardrail — only the documented fields are emitted, and
  `JobResponse(**job)` rejects any unexpected fields surfaced by `get_job`.
- `JobResultsResponse`: GET /jobs/{id}/results.
- `ScopeSystem` + family: G.4 scope-tab CRUD shapes.

G.4 CP3 retired `JobCreateRequest` — the JSON path-string POST /jobs
endpoint is gone. The multipart POST /jobs/upload endpoint takes its
input as `File` + `Form` parameters, not a Pydantic body, so no schema
is needed for the request side.

See backend/E0_API_DESIGN.md §5.2 for the full contract.
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

# E.1: status enum ratified at the API layer; matches core.job_storage._VALID_STATUSES
JobStatus = Literal["draft", "dispatching", "dispatched", "in_review", "exported", "archived"]


class JobResponse(BaseModel):
    """POST /jobs (201) and GET /jobs/{id} (200) response body.

    `extra="forbid"` is the E.1 data-leak guardrail — instantiating
    `JobResponse(**job)` raises if the dict from `get_job` contains any
    field not declared below. That keeps internal columns (or accidental
    additions to the `jobs` table) from leaking out of the API.
    """

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

    # E.1: data-leak guard — extra fields rejected
    model_config = ConfigDict(extra="forbid")


class JobResultsResponse(BaseModel):
    """GET /jobs/{id}/results response body — E.2.2.

    String-keyed dicts: page indices are ``"0"``, ``"1"``, etc.
    ``trade_outputs[page_key]`` maps trade names to their output dicts
    (or ``null`` if the trade produced nothing for that page).
    """

    job_id: str
    dispatch_results: dict[str, dict]
    trade_outputs: dict[str, dict]

    model_config = ConfigDict(extra="forbid")


# G.4: Scope tab schemas. Backend owns scope source-of-truth; the frontend
# is a render+relay layer per the architectural rule.

ScopeTrade = Literal["roofing", "glazing", "siding", "mechanical",
                     "plumbing", "electrical", "structural"]
ScopeSource = Literal["auto", "manual"]
ScopeConfidence = Literal["high", "medium", "low", "manual"]


class ScopeSystem(BaseModel):
    """One scope_systems row — auto or manual, owned by a job + trade."""

    id: str
    job_id: str
    trade: ScopeTrade
    label: str
    system_code: Optional[str]
    confidence: ScopeConfidence
    source: ScopeSource
    evidence: Optional[dict]
    user_fields: Optional[dict]
    created_at: str
    updated_at: str

    model_config = ConfigDict(extra="forbid")


class ScopeSystemsResponse(BaseModel):
    """GET /jobs/{id}/scope response body."""

    job_id: str
    trade: Optional[ScopeTrade]   # None means "all trades"
    systems: list[ScopeSystem]

    model_config = ConfigDict(extra="forbid")


class ScopeSystemCreate(BaseModel):
    """POST /jobs/{id}/scope/systems request body."""

    trade: ScopeTrade
    label: str = Field(..., min_length=1, max_length=200)
    system_code: Optional[str] = None
    user_fields: Optional[dict] = None

    model_config = ConfigDict(extra="forbid")


class ScopeSystemPatch(BaseModel):
    """PATCH /jobs/{id}/scope/systems/{sys_id} request body. All fields optional."""

    label: Optional[str] = Field(None, min_length=1, max_length=200)
    system_code: Optional[str] = None
    user_fields: Optional[dict] = None

    model_config = ConfigDict(extra="forbid")


# G.5a: Annotation schemas. Single-table design with type discriminator
# ('area' | 'pin' | 'line') and free-form data dict that varies per type.
# Mirrors ScopeSystem CRUD shape; full-row replace PATCH semantics (Q4).

AnnotationType = Literal["area", "pin", "line"]
AnnotationSource = Literal["auto", "manual"]


class Annotation(BaseModel):
    """One annotation row — auto-extracted from a trade module or manually
    placed by the user via a viewer tool. data is type-specific:
    - area:  { name?, points: [{x,y}, ...], sqft?, perimeter_ft?, scaleUsed?, polygonTypeId?, kind? }
    - pin:   { equipment_type? | pinTypeId?, x?, y? | pt:{x,y}, note?, source_module?, confidence?, origin_keyword?, bbox? }
    - line:  { lineTypeId?, ptStart:{x,y}, ptEnd:{x,y}, ft?, scaleUsed? }
    """

    id: str
    job_id: str
    system_id: Optional[str]
    type: AnnotationType
    page_idx: int
    source: AnnotationSource
    data: dict
    created_at: str
    updated_at: str

    model_config = ConfigDict(extra="forbid")


class AnnotationsResponse(BaseModel):
    """GET /jobs/{id}/annotations response body."""

    job_id: str
    annotations: list[Annotation]

    model_config = ConfigDict(extra="forbid")


class AnnotationCreate(BaseModel):
    """POST /jobs/{id}/annotations request body."""

    type: AnnotationType
    page_idx: int = Field(..., ge=0)
    system_id: Optional[str] = None
    data: dict = Field(default_factory=dict)

    model_config = ConfigDict(extra="forbid")


class AnnotationPatch(BaseModel):
    """PATCH /jobs/{id}/annotations/{ann_id} request body — full-row replace
    semantics per Q4 (callers send the whole `data` dict; backend overwrites)."""

    page_idx: Optional[int] = Field(None, ge=0)
    system_id: Optional[str] = None  # empty string detaches (stored as NULL)
    data: Optional[dict] = None

    model_config = ConfigDict(extra="forbid")
