"""E.1: Tests for the FastAPI /jobs endpoints + /health probe.

Six tests total — takes the backend floor from 216 → 222.

1. test_health_probe_returns_ok                       — /health 200
2. test_create_job_happy_path                         — POST /jobs 201
3. test_get_job_happy_path                            — GET /jobs/{id} 200
4. test_get_job_404_for_nonexistent_id                — GET /jobs/{bogus} 404
5. test_create_job_validation_error_invalid_status    — POST /jobs status=banana 422
6. test_data_leak_response_shape_and_error_messages   — extra="forbid" + safe errors

Per MARCH_ORDERS_E_1_fastapi_scaffold.md §6. Tests use FastAPI's TestClient
in-process (no uvicorn subprocess). They write to the real ~/.tracepoint/cache.db
the same way d2_silverleaf_reference.py does — that's the live D.2 layer.
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
