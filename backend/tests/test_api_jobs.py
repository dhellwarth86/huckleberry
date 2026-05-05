"""Tests for the FastAPI /jobs endpoints + /health probe — E.1 + E.2.2 + G.4.

E.1 tests (1–6):  216 → 222.
E.2.2 tests (7–14): 222 → 230.
G.4 CP1 scope tests: 230 → 251.
G.4 CP2 multipart upload + file serving: 251 → 258.
G.4 CP3 retired the JSON path-string POST /jobs endpoint. Several E.1 /
E.2.2 tests that depended on the JSON path were retired; the rest were
migrated to use the multipart POST /jobs/upload endpoint via the
_upload_test_job helper below.

Tests use FastAPI's TestClient in-process (no uvicorn subprocess).
"""
from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


# ── Helpers ─────────────────────────────────────────────────────────


def _upload_test_job(pdf_path: Path, *, name: str = "upload test",
                     trade_scope: str = "roofing") -> str:
    """G.4 CP3: create a job by uploading the PDF bytes via multipart.
    Returns job_id. Replaces the legacy JSON path-string POST /jobs flow."""
    pdf_bytes = pdf_path.read_bytes()
    r = client.post(
        "/jobs/upload",
        files={"file": (pdf_path.name, pdf_bytes, "application/pdf")},
        data={"name": name, "trade_scope": trade_scope},
    )
    assert r.status_code == 201, f"upload helper failed: {r.status_code} {r.text}"
    return r.json()["id"]


def _create_test_job(small_pdf_path) -> str:
    """G.4 CP3: thin wrapper for tests that just need a job to exist.
    Uses the small fixture PDF (~200 bytes) so tests stay fast."""
    return _upload_test_job(small_pdf_path, name="scope test")


def _uploaded_pdf_path_for(job_id: str) -> Path:
    """Helper for cleanup / file-deletion simulation in tests."""
    from core.job_storage import get_uploaded_pdf_path
    return get_uploaded_pdf_path(job_id)


# ── E.1 tests (post-CP3 migration) ──────────────────────────────────


def test_health_probe_returns_ok():
    """/health returns 200 and status=ok."""
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "version" in body


def test_get_job_happy_path(small_pdf_path):
    """GET /jobs/{job_id} returns 200 and full JobResponse round-trip."""
    job_id = _upload_test_job(small_pdf_path, name="get job test")

    r = client.get(f"/jobs/{job_id}")
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == job_id
    assert body["name"] == "get job test"
    assert body["trade_scope"] == "roofing"  # default applied
    assert body["status"] == "draft"


def test_get_job_404_for_nonexistent_id():
    """GET /jobs/{nonexistent} returns 404 with safe error message."""
    r = client.get("/jobs/nonexistent-job-id-12345")
    assert r.status_code == 404
    body = r.json()
    assert body["detail"] == "Job not found"


def test_data_leak_response_shape_and_error_messages(small_pdf_path):
    """Combined data-leak detection.

    Asserts:
      Part 1 — JobResponse contains exactly the documented fields, no extras.
      Part 2 — Error responses contain only generic detail messages — no SQL
               fragments, no traceback markers, no DB engine names.
    """
    EXPECTED_FIELDS = {
        "id", "name", "gc", "location_city", "location_state", "trade_scope",
        "bid_due_date", "notes", "status", "created_at", "updated_at",
        "pdf_path", "pdf_sha1", "dispatch_complete",
    }

    # ── Part 1: response shape ──
    pdf_bytes = small_pdf_path.read_bytes()
    r = client.post(
        "/jobs/upload",
        files={"file": ("leak.pdf", pdf_bytes, "application/pdf")},
        data={"name": "Leak test"},
    )
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
    # paths can't realistically have leaked.
    assert len(err_str) < 100, f"Error body suspiciously verbose: {err_body}"


# ── E.2.2 dispatch + results tests (post-CP3 migration) ─────────────


def test_dispatch_job_returns_200(small_pdf_path):
    """POST /jobs/{id}/dispatch returns 200, status=dispatched, dispatch_complete=True."""
    job_id = _upload_test_job(small_pdf_path, name="dispatch test")

    r = client.post(f"/jobs/{job_id}/dispatch")
    assert r.status_code == 200, f"expected 200, got {r.status_code}: {r.text}"
    body = r.json()
    assert body["status"] == "dispatched"
    assert body["dispatch_complete"] is True


def test_dispatch_job_404_for_unknown_id():
    """POST /jobs/{bogus}/dispatch returns 404."""
    r = client.post("/jobs/nonexistent-dispatch-id-999/dispatch")
    assert r.status_code == 404
    assert r.json()["detail"] == "Job not found"


def test_dispatch_job_idempotent_on_second_call(small_pdf_path):
    """Dispatching a second time returns 200 (idempotent, no re-dispatch)."""
    job_id = _upload_test_job(small_pdf_path, name="idempotent test")

    r1 = client.post(f"/jobs/{job_id}/dispatch")
    assert r1.status_code == 200
    r2 = client.post(f"/jobs/{job_id}/dispatch")
    assert r2.status_code == 200
    assert r2.json()["status"] == "dispatched"


def test_dispatch_job_400_when_pdf_missing(small_pdf_path):
    """Dispatch returns 400 when the uploaded PDF was removed from disk."""
    job_id = _upload_test_job(small_pdf_path, name="missing pdf test")
    # Simulate disk failure: remove the uploaded source.pdf
    _uploaded_pdf_path_for(job_id).unlink()

    r = client.post(f"/jobs/{job_id}/dispatch")
    assert r.status_code == 400
    assert r.json()["detail"] == "pdf_path not found"


def test_get_results_returns_200_after_dispatch(small_pdf_path):
    """GET /jobs/{id}/results returns 200 with dicts after dispatch."""
    job_id = _upload_test_job(small_pdf_path, name="results test")
    client.post(f"/jobs/{job_id}/dispatch")

    r = client.get(f"/jobs/{job_id}/results")
    assert r.status_code == 200, f"expected 200, got {r.status_code}: {r.text}"
    body = r.json()
    assert body["job_id"] == job_id
    assert isinstance(body["dispatch_results"], dict)
    assert isinstance(body["trade_outputs"], dict)


def test_get_results_404_for_unknown_id():
    """GET /jobs/{bogus}/results returns 404."""
    r = client.get("/jobs/nonexistent-results-id-999/results")
    assert r.status_code == 404
    assert r.json()["detail"] == "Job not found"


def test_get_results_409_when_not_dispatched(small_pdf_path):
    """GET /jobs/{id}/results before dispatch returns 409."""
    job_id = _upload_test_job(small_pdf_path, name="no dispatch yet")

    r = client.get(f"/jobs/{job_id}/results")
    assert r.status_code == 409
    assert r.json()["detail"] == "Job not yet dispatched"


def test_get_results_response_shape_keys_are_strings(small_pdf_path):
    """dispatch_results + trade_outputs keys are all strings (not ints)."""
    job_id = _upload_test_job(small_pdf_path, name="string keys test")
    client.post(f"/jobs/{job_id}/dispatch")

    r = client.get(f"/jobs/{job_id}/results")
    assert r.status_code == 200
    body = r.json()
    for k in body["dispatch_results"]:
        assert isinstance(k, str), f"dispatch_results key {k!r} is not str"
    for k in body["trade_outputs"]:
        assert isinstance(k, str), f"trade_outputs key {k!r} is not str"


# ── G.4 scope tab tests ─────────────────────────────────────────────


def test_scope_get_empty_for_undispatched_job(small_pdf_path):
    """G.4: GET /jobs/{id}/scope on a fresh job returns 200 with empty systems."""
    job_id = _create_test_job(small_pdf_path)
    r = client.get(f"/jobs/{job_id}/scope")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["job_id"] == job_id
    assert body["trade"] is None
    assert body["systems"] == []


def test_scope_post_creates_manual_row(small_pdf_path):
    """G.4: POST /jobs/{id}/scope/systems creates a manual row, GET sees it."""
    job_id = _create_test_job(small_pdf_path)
    payload = {"trade": "roofing", "label": "TPO Single Ply",
               "system_code": "tpo", "user_fields": {"manufacturer": "Carlisle"}}
    r = client.post(f"/jobs/{job_id}/scope/systems", json=payload)
    assert r.status_code == 201, r.text
    created = r.json()
    assert created["trade"] == "roofing"
    assert created["label"] == "TPO Single Ply"
    assert created["system_code"] == "tpo"
    assert created["source"] == "manual"
    assert created["confidence"] == "manual"
    assert created["user_fields"] == {"manufacturer": "Carlisle"}
    assert "id" in created and len(created["id"]) > 0

    list_r = client.get(f"/jobs/{job_id}/scope")
    assert list_r.status_code == 200
    systems = list_r.json()["systems"]
    assert len(systems) == 1
    assert systems[0]["id"] == created["id"]


def test_scope_patch_updates_fields(small_pdf_path):
    """G.4: PATCH /jobs/{id}/scope/systems/{sys_id} updates only the provided fields."""
    job_id = _create_test_job(small_pdf_path)
    create_r = client.post(
        f"/jobs/{job_id}/scope/systems",
        json={"trade": "roofing", "label": "TPO Single Ply"},
    )
    sys_id = create_r.json()["id"]
    patch_r = client.patch(
        f"/jobs/{job_id}/scope/systems/{sys_id}",
        json={"label": "TPO 60-mil", "user_fields": {"thickness": "60 mil"}},
    )
    assert patch_r.status_code == 200, patch_r.text
    patched = patch_r.json()
    assert patched["label"] == "TPO 60-mil"
    assert patched["user_fields"] == {"thickness": "60 mil"}
    # system_code untouched (was None on create, still None)
    assert patched["system_code"] is None


def test_scope_delete_removes_row(small_pdf_path):
    """G.4: DELETE /jobs/{id}/scope/systems/{sys_id} returns 204 and row is gone."""
    job_id = _create_test_job(small_pdf_path)
    sys_id = client.post(
        f"/jobs/{job_id}/scope/systems",
        json={"trade": "roofing", "label": "Goes Away"},
    ).json()["id"]
    r = client.delete(f"/jobs/{job_id}/scope/systems/{sys_id}")
    assert r.status_code == 204
    list_r = client.get(f"/jobs/{job_id}/scope")
    assert list_r.json()["systems"] == []


def test_scope_get_filters_by_trade(small_pdf_path):
    """G.4: GET /jobs/{id}/scope?trade=roofing returns only roofing rows."""
    job_id = _create_test_job(small_pdf_path)
    client.post(f"/jobs/{job_id}/scope/systems",
                json={"trade": "roofing", "label": "TPO"})
    client.post(f"/jobs/{job_id}/scope/systems",
                json={"trade": "glazing", "label": "Storefront"})
    r = client.get(f"/jobs/{job_id}/scope", params={"trade": "roofing"})
    assert r.status_code == 200
    body = r.json()
    assert body["trade"] == "roofing"
    assert len(body["systems"]) == 1
    assert body["systems"][0]["trade"] == "roofing"

    r2 = client.get(f"/jobs/{job_id}/scope", params={"trade": "glazing"})
    assert len(r2.json()["systems"]) == 1
    assert r2.json()["systems"][0]["label"] == "Storefront"

    # Unfiltered: both rows returned.
    r3 = client.get(f"/jobs/{job_id}/scope")
    assert len(r3.json()["systems"]) == 2


def test_scope_post_404_for_unknown_job():
    """G.4: POST against nonexistent job returns 404."""
    r = client.post(
        "/jobs/nonexistent-scope-job/scope/systems",
        json={"trade": "roofing", "label": "x"},
    )
    assert r.status_code == 404


def test_scope_patch_404_for_unknown_sys_id(small_pdf_path):
    """G.4: PATCH on nonexistent sys_id returns 404."""
    job_id = _create_test_job(small_pdf_path)
    r = client.patch(
        f"/jobs/{job_id}/scope/systems/nonexistent-id-12345",
        json={"label": "x"},
    )
    assert r.status_code == 404


def test_scope_rescan_resets_auto_keeps_manual(small_pdf_path):
    """G.4: POST /scope/rescan resets auto rows but preserves manual rows.

    Setup: directly seed an auto roofing row + a manual roofing row via
    job_storage helpers (avoid running real dispatch — too slow).
    Rescan should delete the auto row, then re-derive nothing (no
    persisted project_scope yet), and leave the manual row untouched.
    """
    from core.job_storage import _connect, create_scope_system
    import json
    import uuid as _uuid
    from datetime import datetime, timezone

    job_id = _create_test_job(small_pdf_path)

    # Seed auto row directly via SQL (simulates persist_dispatch_result).
    auto_id = str(_uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    conn = _connect()
    try:
        conn.execute(
            "INSERT INTO scope_systems (id, job_id, trade, label, system_code, "
            "confidence, source, evidence_json, user_fields_json, "
            "created_at, updated_at) "
            "VALUES (?, ?, 'roofing', 'TPO Single Ply', 'tpo', 'high', 'auto', ?, NULL, ?, ?)",
            (auto_id, job_id, json.dumps({"system_evidence": "spec 07 54"}), now, now),
        )
        conn.commit()
    finally:
        conn.close()

    # Create a manual row via the public CRUD function.
    manual = create_scope_system(
        job_id, trade="roofing", label="Custom Manual System",
    )
    manual_id = manual["id"]

    # Confirm both exist.
    listing = client.get(f"/jobs/{job_id}/scope", params={"trade": "roofing"}).json()
    ids = {s["id"] for s in listing["systems"]}
    assert auto_id in ids and manual_id in ids

    # Rescan with no persisted project_scope — auto row deleted, no replacement.
    r = client.post(f"/jobs/{job_id}/scope/rescan", params={"trade": "roofing"})
    assert r.status_code == 200, r.text
    after = r.json()
    after_ids = {s["id"] for s in after["systems"]}
    # Manual preserved.
    assert manual_id in after_ids
    # Old auto gone (no project_scope persisted to re-derive from).
    assert auto_id not in after_ids


def test_scope_data_leak_response_shape(small_pdf_path):
    """G.4: ScopeSystem response uses extra='forbid'; no leaked fields."""
    EXPECTED = {
        "id", "job_id", "trade", "label", "system_code",
        "confidence", "source", "evidence", "user_fields",
        "created_at", "updated_at",
    }
    job_id = _create_test_job(small_pdf_path)
    r = client.post(
        f"/jobs/{job_id}/scope/systems",
        json={"trade": "roofing", "label": "shape test"},
    )
    assert r.status_code == 201
    keys = set(r.json().keys())
    assert keys == EXPECTED, (
        f"Unexpected fields in ScopeSystem response. "
        f"Missing: {EXPECTED - keys}; Extra: {keys - EXPECTED}"
    )


# ── G.4 CP2 multipart upload + file serving tests ───────────────────


def test_upload_creates_job_writes_file_to_uploads_dir(small_pdf_path):
    """CP2: POST /jobs/upload accepts multipart, writes bytes, returns 201."""
    from core.job_storage import get_uploaded_pdf_path

    pdf_bytes = small_pdf_path.read_bytes()
    r = client.post(
        "/jobs/upload",
        files={"file": ("upload.pdf", pdf_bytes, "application/pdf")},
        data={"name": "CP2 upload test", "trade_scope": "roofing"},
    )
    assert r.status_code == 201, f"expected 201, got {r.status_code}: {r.text}"
    body = r.json()
    job_id = body["id"]
    assert body["name"] == "CP2 upload test"
    assert body["trade_scope"] == "roofing"
    assert body["status"] == "draft"
    # pdf_sha1 computed from the actual bytes
    import hashlib
    assert body["pdf_sha1"] == hashlib.sha1(pdf_bytes).hexdigest()
    # File landed at ~/.tracepoint/uploads/{job_id}/source.pdf
    stored = get_uploaded_pdf_path(job_id)
    assert stored.exists(), f"upload file missing: {stored}"
    assert stored.read_bytes() == pdf_bytes, "stored bytes do not match upload"
    # Cleanup the upload directory
    try:
        stored.unlink()
        stored.parent.rmdir()
    except OSError:
        pass


def test_upload_rejects_empty_file():
    """CP2: empty multipart upload returns 400."""
    r = client.post(
        "/jobs/upload",
        files={"file": ("empty.pdf", b"", "application/pdf")},
        data={"name": "empty test"},
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "empty upload"


def test_upload_rejects_non_pdf_content_type():
    """CP2: non-PDF content type returns 415."""
    r = client.post(
        "/jobs/upload",
        files={"file": ("not.txt", b"hello world", "text/plain")},
        data={"name": "wrong type test"},
    )
    assert r.status_code == 415
    assert r.json()["detail"] == "PDF required"


def test_get_pdf_returns_uploaded_bytes(small_pdf_path):
    """CP2: GET /jobs/{id}/pdf streams the bytes that were uploaded."""
    from core.job_storage import get_uploaded_pdf_path

    pdf_bytes = small_pdf_path.read_bytes()
    create_resp = client.post(
        "/jobs/upload",
        files={"file": ("upload.pdf", pdf_bytes, "application/pdf")},
        data={"name": "CP2 get pdf test"},
    )
    assert create_resp.status_code == 201
    job_id = create_resp.json()["id"]

    r = client.get(f"/jobs/{job_id}/pdf")
    assert r.status_code == 200, f"expected 200, got {r.status_code}: {r.text}"
    assert r.headers["content-type"] == "application/pdf"
    assert r.content == pdf_bytes, "served bytes do not match uploaded bytes"

    # Cleanup
    stored = get_uploaded_pdf_path(job_id)
    try:
        stored.unlink()
        stored.parent.rmdir()
    except OSError:
        pass


def test_get_pdf_404_for_unknown_job():
    """CP2: GET /jobs/{bogus}/pdf returns 404."""
    r = client.get("/jobs/nonexistent-pdf-job-id/pdf")
    assert r.status_code == 404
    assert r.json()["detail"] == "Job not found"


def test_get_pdf_404_when_file_missing(small_pdf_path):
    """CP2 (post-CP3): GET /jobs/{id}/pdf returns 404 when the uploaded
    on-disk file is gone."""
    job_id = _upload_test_job(small_pdf_path, name="missing pdf get test")
    _uploaded_pdf_path_for(job_id).unlink()

    r = client.get(f"/jobs/{job_id}/pdf")
    assert r.status_code == 404
    assert r.json()["detail"] == "PDF not found"


# CP3 retired test_create_job_json_path_still_works — there's no JSON path
# anymore; the multipart upload path is the only way to create a job, and
# test_upload_creates_job_writes_file_to_uploads_dir already covers it.
