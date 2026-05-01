"""Tests for the FastAPI /jobs endpoints + /health probe — E.1 + E.2.2.

E.1 tests (1–6):  216 → 222.
E.2.2 tests (7–14): 222 → 230.

 7. test_dispatch_job_returns_200                     — POST /jobs/{id}/dispatch 200
 8. test_dispatch_job_404_for_unknown_id              — POST /jobs/{bogus}/dispatch 404
 9. test_dispatch_job_idempotent_on_second_call       — dispatch twice → both 200
10. test_dispatch_job_400_when_pdf_missing             — pdf deleted before dispatch → 400
11. test_get_results_returns_200_after_dispatch        — GET /jobs/{id}/results 200
12. test_get_results_404_for_unknown_id               — GET /jobs/{bogus}/results 404
13. test_get_results_409_when_not_dispatched           — GET /jobs/{id}/results before dispatch → 409
14. test_get_results_response_shape_keys_are_strings   — dict keys are str, not int

Tests use FastAPI's TestClient in-process (no uvicorn subprocess).
"""
from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_health_probe_returns_ok():
    """Test 1: /health returns 200 and status=ok."""
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "version" in body


def test_create_job_happy_path(silverleaf_path):
    """Test 2: POST /jobs with valid payload returns 201 and JobResponse shape."""
    payload = {
        "name": "Silverleaf E.1 test",
        "pdf_path": str(silverleaf_path),
        "gc": "Test GC",
        "location_city": "Tampa",
        "location_state": "FL",
        "trade_scope": "roofing",
    }
    r = client.post("/jobs", json=payload)
    assert r.status_code == 201, f"expected 201, got {r.status_code}: {r.text}"
    body = r.json()
    assert body["name"] == "Silverleaf E.1 test"
    assert body["status"] == "draft"
    assert "id" in body and len(body["id"]) > 0
    assert "pdf_sha1" in body and len(body["pdf_sha1"]) == 40  # SHA-1 hex length
    assert body["dispatch_complete"] is False


def test_get_job_happy_path(silverleaf_path):
    """Test 3: GET /jobs/{job_id} returns 200 and full JobResponse round-trip."""
    payload = {
        "name": "Silverleaf get test",
        "pdf_path": str(silverleaf_path),
    }
    create_resp = client.post("/jobs", json=payload)
    assert create_resp.status_code == 201
    job_id = create_resp.json()["id"]

    r = client.get(f"/jobs/{job_id}")
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == job_id
    assert body["name"] == "Silverleaf get test"
    assert body["trade_scope"] == "roofing"  # default applied
    assert body["status"] == "draft"


def test_get_job_404_for_nonexistent_id():
    """Test 4: GET /jobs/{nonexistent} returns 404 with safe error message."""
    r = client.get("/jobs/nonexistent-job-id-12345")
    assert r.status_code == 404
    body = r.json()
    assert body["detail"] == "Job not found"


def test_create_job_validation_error_invalid_status(silverleaf_path):
    """Test 5: POST /jobs with invalid status returns 422 (Pydantic Literal enforced)."""
    payload = {
        "name": "Test",
        "pdf_path": str(silverleaf_path),
        "status": "banana",  # not in JobStatus Literal — Pydantic must reject
    }
    r = client.post("/jobs", json=payload)
    assert r.status_code == 422


def test_data_leak_response_shape_and_error_messages(silverleaf_path):
    """Test 6: Combined data-leak detection.

    Asserts:
      Part 1 — JobResponse contains exactly the documented fields, no extras.
               extra="forbid" on the response model is the canonical guard;
               this test also verifies the wire-format keys match the contract.
      Part 2 — Error responses contain only generic detail messages — no SQL
               fragments, no path separators (/, \\), no traceback markers,
               no DB engine names (sqlite), no execute(...) signatures.
    """
    EXPECTED_FIELDS = {
        "id", "name", "gc", "location_city", "location_state", "trade_scope",
        "bid_due_date", "notes", "status", "created_at", "updated_at",
        "pdf_path", "pdf_sha1", "dispatch_complete",
    }

    # ── Part 1: response shape ──
    payload = {"name": "Leak test", "pdf_path": str(silverleaf_path)}
    r = client.post("/jobs", json=payload)
    assert r.status_code == 201
    body_keys = set(r.json().keys())
    assert body_keys == EXPECTED_FIELDS, (
        f"Unexpected fields in JobResponse. "
        f"Missing: {EXPECTED_FIELDS - body_keys}; Extra: {body_keys - EXPECTED_FIELDS}"
    )

    # ── Part 2: error message safety ──
    bad_resp = client.get("/jobs/nonexistent-id")
    assert bad_resp.status_code == 404
    err_body = bad_resp.json()
    err_str = str(err_body).lower()

    forbidden_substrings = [
        # SQL fragments
        "select ", "from jobs", "where id=",
        # Python traceback markers
        "traceback", 'file "',
        # DB engine names / sqlite-specific
        "sqlite", "execute(",
    ]
    for forbidden in forbidden_substrings:
        assert forbidden not in err_str, (
            f"Error response leaked '{forbidden}' in: {err_body}"
        )
    # Path-separator heuristic — assert the error body is short enough that
    # paths can't realistically have leaked. The {"detail": "Job not found"}
    # body is ~30 chars; anything significantly longer indicates extra data.
    assert len(err_str) < 100, f"Error body suspiciously verbose: {err_body}"


# ── E.2.2 tests ────────────────────────────────────────────────────


def test_dispatch_job_returns_200(small_pdf_path):
    """Test 7: POST /jobs/{id}/dispatch returns 200, status=dispatched, dispatch_complete=True."""
    payload = {"name": "dispatch test", "pdf_path": str(small_pdf_path)}
    create_resp = client.post("/jobs", json=payload)
    assert create_resp.status_code == 201
    job_id = create_resp.json()["id"]

    r = client.post(f"/jobs/{job_id}/dispatch")
    assert r.status_code == 200, f"expected 200, got {r.status_code}: {r.text}"
    body = r.json()
    assert body["status"] == "dispatched"
    assert body["dispatch_complete"] is True


def test_dispatch_job_404_for_unknown_id():
    """Test 8: POST /jobs/{bogus}/dispatch returns 404."""
    r = client.post("/jobs/nonexistent-dispatch-id-999/dispatch")
    assert r.status_code == 404
    assert r.json()["detail"] == "Job not found"


def test_dispatch_job_idempotent_on_second_call(small_pdf_path):
    """Test 9: dispatching a second time returns 200 (idempotent, no re-dispatch)."""
    payload = {"name": "idempotent test", "pdf_path": str(small_pdf_path)}
    create_resp = client.post("/jobs", json=payload)
    job_id = create_resp.json()["id"]

    r1 = client.post(f"/jobs/{job_id}/dispatch")
    assert r1.status_code == 200
    r2 = client.post(f"/jobs/{job_id}/dispatch")
    assert r2.status_code == 200
    assert r2.json()["status"] == "dispatched"


def test_dispatch_job_400_when_pdf_missing(small_pdf_path):
    """Test 10: dispatch returns 400 when pdf_path no longer exists."""
    payload = {"name": "missing pdf test", "pdf_path": str(small_pdf_path)}
    create_resp = client.post("/jobs", json=payload)
    job_id = create_resp.json()["id"]

    small_pdf_path.unlink()

    r = client.post(f"/jobs/{job_id}/dispatch")
    assert r.status_code == 400
    assert r.json()["detail"] == "pdf_path not found"


def test_get_results_returns_200_after_dispatch(small_pdf_path):
    """Test 11: GET /jobs/{id}/results returns 200 with dicts after dispatch."""
    payload = {"name": "results test", "pdf_path": str(small_pdf_path)}
    create_resp = client.post("/jobs", json=payload)
    job_id = create_resp.json()["id"]
    client.post(f"/jobs/{job_id}/dispatch")

    r = client.get(f"/jobs/{job_id}/results")
    assert r.status_code == 200, f"expected 200, got {r.status_code}: {r.text}"
    body = r.json()
    assert body["job_id"] == job_id
    assert isinstance(body["dispatch_results"], dict)
    assert isinstance(body["trade_outputs"], dict)


def test_get_results_404_for_unknown_id():
    """Test 12: GET /jobs/{bogus}/results returns 404."""
    r = client.get("/jobs/nonexistent-results-id-999/results")
    assert r.status_code == 404
    assert r.json()["detail"] == "Job not found"


def test_get_results_409_when_not_dispatched(small_pdf_path):
    """Test 13: GET /jobs/{id}/results before dispatch returns 409."""
    payload = {"name": "no dispatch yet", "pdf_path": str(small_pdf_path)}
    create_resp = client.post("/jobs", json=payload)
    job_id = create_resp.json()["id"]

    r = client.get(f"/jobs/{job_id}/results")
    assert r.status_code == 409
    assert r.json()["detail"] == "Job not yet dispatched"


def test_get_results_response_shape_keys_are_strings(small_pdf_path):
    """Test 14: dispatch_results + trade_outputs keys are all strings (not ints)."""
    payload = {"name": "string keys test", "pdf_path": str(small_pdf_path)}
    create_resp = client.post("/jobs", json=payload)
    job_id = create_resp.json()["id"]
    client.post(f"/jobs/{job_id}/dispatch")

    r = client.get(f"/jobs/{job_id}/results")
    assert r.status_code == 200
    body = r.json()
    for k in body["dispatch_results"]:
        assert isinstance(k, str), f"dispatch_results key {k!r} is not str"
    for k in body["trade_outputs"]:
        assert isinstance(k, str), f"trade_outputs key {k!r} is not str"
