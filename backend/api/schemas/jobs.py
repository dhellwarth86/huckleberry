"""Pydantic v2 schemas for the /jobs endpoints — E.1.

Two shapes:

- `JobCreateRequest`: POST /jobs request body. Strict input validation —
  `status` is a `Literal[...]` enforced by Pydantic, name + pdf_path required.
- `JobResponse`: GET /jobs/{id} and POST /jobs response. `extra="forbid"`
  is the data-leak guardrail: only the documented fields are emitted, and
  `JobResponse(**job)` rejects any unexpected fields surfaced by `get_job`.

See backend/E0_API_DESIGN.md §5.2 for the full contract.
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

# E.1: status enum ratified at the API layer; matches core.job_storage._VALID_STATUSES
JobStatus = Literal["draft", "dispatching", "dispatched", "in_review", "exported", "archived"]


class JobCreateRequest(BaseModel):
    """POST /jobs request body."""

    name: str = Field(..., min_length=1, max_length=200)  # E.1: required, non-empty
    pdf_path: str = Field(..., min_length=1)  # E.1: string path; upload comes at Postgres migration
    gc: Optional[str] = None
    location_city: Optional[str] = None
    location_state: Optional[str] = None
    trade_scope: str = "roofing"
    bid_due_date: Optional[str] = None  # E.1: ISO 8601 date string
    notes: Optional[str] = None
    status: JobStatus = "draft"  # E.1: strict Literal — Pydantic rejects "banana" etc.


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
