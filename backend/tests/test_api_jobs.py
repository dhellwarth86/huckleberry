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


# ── G.5a CP4 — TradeModule Protocol vocabulary + palette auto-seed tests ──


def test_roofing_get_palette_seed_tpo():
    """CP4 + CP4.1: RoofingModule.get_palette_seed('tpo') returns palette
    payload keyed to TPO's typical_items, routed by item.unit:
      EA -> pinPalette, LF -> edgeTypes, SF -> polygonTypes, SQ -> skipped.
    """
    from core.roofing_module import RoofingModule
    seed = RoofingModule.get_palette_seed("tpo")
    assert isinstance(seed, dict)
    assert "pinPalette" in seed and "edgeTypes" in seed and "polygonTypes" in seed
    pin_names = [p["name"] for p in seed["pinPalette"]]
    edge_names = [e["name"] for e in seed["edgeTypes"]]
    poly_names = [p["name"] for p in seed["polygonTypes"]]
    # EA-unit items in pinPalette
    assert "Roof Drains" in pin_names
    assert "Scuppers" in pin_names
    assert "Rooftop Units / RTUs" in pin_names
    # LF-unit items in edgeTypes — including walkway_pads (manual derive)
    assert "Coping" in edge_names
    assert "Edge Metal" in edge_names
    assert "Walkway Pads" in edge_names, "walkway_pads (LF/manual) should land in edgeTypes per CP4.1 unit-based routing"
    # SF-unit items in polygonTypes — including cricket and curbs (both manual)
    assert any("Membrane" in n for n in poly_names)
    assert "Crickets" in poly_names, "cricket (SF/manual) should land in polygonTypes per CP4.1 unit-based routing"
    assert "Equipment Curbs" in poly_names, "Equipment Curbs (SF/manual after CP4.1) should land in polygonTypes"
    assert "Equipment Curbs" not in pin_names, "Equipment Curbs is no longer EA after CP4.1"
    # Each entry has the canonical shape
    for entry in seed["pinPalette"]:
        assert set(entry.keys()) >= {"id", "name", "color", "source", "seedId"}
        assert entry["source"] == "auto"
        assert entry["color"].startswith("#")
        assert len(entry["color"]) == 7  # #RRGGBB hex


def test_roofing_get_expected_items_tpo():
    """CP4: RoofingModule.get_expected_items('tpo') returns checklist payload."""
    from core.roofing_module import RoofingModule
    items = RoofingModule.get_expected_items("tpo")
    assert isinstance(items, list) and len(items) > 0
    by_name = {it["name"]: it for it in items}
    assert "drains" in by_name
    assert by_name["drains"]["display_name"] == "Roof Drains"
    assert by_name["drains"]["unit"] == "EA"
    assert by_name["drains"]["derive_from"] == "callout_count"
    # membrane_area carried for TPO too
    assert "membrane_area" in by_name
    assert by_name["membrane_area"]["unit"] == "SF"
    assert by_name["membrane_area"]["derive_from"] == "polygon_area"


def test_roofing_get_systems_catalog():
    """CP4: RoofingModule.get_systems_catalog returns sanitized SYSTEMS dict."""
    from core.roofing_module import RoofingModule
    cat = RoofingModule.get_systems_catalog()
    assert "tpo" in cat
    assert cat["tpo"]["display_name"] == "TPO Single Ply"
    assert "drains" in cat["tpo"]["typical_items"]
    # Should NOT include the keywords blob (UI doesn't need it; payload size).
    assert "keywords" not in cat["tpo"]


def test_glazing_get_palette_seed_returns_skeletal():
    """CP4: GlazingModule.get_palette_seed returns at least pin entries
    from GLAZING_PIN_TYPES (skeletal until C.3c)."""
    from core.glazing_module import GlazingModule
    seed = GlazingModule.get_palette_seed(None)
    assert isinstance(seed, dict)
    assert isinstance(seed["pinPalette"], list) and len(seed["pinPalette"]) > 0
    # Skeletal: no edges/polygons until C.3c.
    assert seed["edgeTypes"] == []
    assert seed["polygonTypes"] == []
    # Each entry has the canonical shape
    for entry in seed["pinPalette"]:
        assert set(entry.keys()) >= {"id", "name", "color", "source", "seedId"}
        assert entry["source"] == "auto"


def test_seed_palette_via_protocol_roofing_seeds_via_classmethod(small_pdf_path):
    """CP4: _seed_palette_via_protocol wires through the Protocol classmethod
    and writes user_fields onto a scope_systems row."""
    from core.job_storage import (
        create_job, create_scope_system, _seed_palette_via_protocol,
        get_scope_system, _connect,
    )
    job_id = create_job(name="cp4 protocol seed test", pdf_path=str(small_pdf_path))
    # Create a manual roofing system with explicit empty user_fields (so
    # the auto-seed in create_scope_system doesn't fire — we want to test
    # the helper directly).
    sys_row = create_scope_system(
        job_id, trade="roofing", label="manual TPO",
        user_fields={"placeholder": True},
    )
    sys_id = sys_row["id"]
    # Explicit auto-seed call
    _seed_palette_via_protocol(sys_id, "roofing", "tpo")
    after = get_scope_system(sys_id)
    uf = after.get("user_fields") or {}
    assert "pinPalette" in uf and len(uf["pinPalette"]) > 0
    assert "edgeTypes" in uf and len(uf["edgeTypes"]) > 0
    assert "polygonTypes" in uf and len(uf["polygonTypes"]) > 0
    # Cleanup
    conn = _connect()
    try:
        conn.execute("DELETE FROM scope_systems WHERE job_id = ?", (job_id,))
        conn.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
        conn.commit()
    finally:
        conn.close()


def test_create_scope_system_auto_seeds_when_user_fields_omitted(small_pdf_path):
    """CP4: POST /jobs/{id}/scope/systems with no user_fields → palette
    auto-populates via Protocol. POST WITH user_fields → respected, no clobber."""
    job_id = _upload_test_job(small_pdf_path, name="cp4 auto seed via api")

    # No user_fields supplied → auto-seed
    r1 = client.post(
        f"/jobs/{job_id}/scope/systems",
        json={"trade": "roofing", "label": "auto-seed test", "system_code": "tpo"},
    )
    assert r1.status_code == 201
    body1 = r1.json()
    uf1 = body1.get("user_fields") or {}
    assert "pinPalette" in uf1 and len(uf1["pinPalette"]) > 0, "TPO auto-seed should produce pins"

    # Explicit user_fields → respected, NOT clobbered
    r2 = client.post(
        f"/jobs/{job_id}/scope/systems",
        json={
            "trade": "roofing",
            "label": "explicit fields",
            "system_code": "tpo",
            "user_fields": {"pinPalette": [{"id": "x", "name": "mine"}]},
        },
    )
    assert r2.status_code == 201
    body2 = r2.json()
    uf2 = body2.get("user_fields") or {}
    assert len(uf2.get("pinPalette", [])) == 1, "explicit user_fields was clobbered!"
    assert uf2["pinPalette"][0]["name"] == "mine"


def test_no_per_trade_imports_in_job_storage():
    """CP4: job_storage.py must NOT import roofing_*, glazing_*, debug_* —
    enforces 'no hardcoding trade verbiage outside the module' rule.
    Per Daniel 2026-05-08."""
    from pathlib import Path
    src = (Path(__file__).resolve().parent.parent / "core" / "job_storage.py").read_text(encoding="utf-8")
    # Count only top-level (non-indented) imports — `_resolve_trade_module`
    # uses lazy LOCAL imports inside the function body, which is the
    # explicit pattern for trade-agnostic dispatch.
    forbidden = ["roofing_module", "roofing_vocabulary",
                 "glazing_module", "glazing_vocabulary",
                 "debug_module"]
    for line in src.splitlines():
        # Top-level imports start at column 0
        if line.startswith("from core.") or line.startswith("import core."):
            for f in forbidden:
                assert f not in line, (
                    f"job_storage.py top-level import leaks per-trade vocabulary: "
                    f"'{line.strip()}'. Use lazy import inside _resolve_trade_module instead."
                )


# ── G.5a annotations CRUD + auto-pin tests ──────────────────────────


def test_annotations_get_empty_for_undispatched_job(small_pdf_path):
    """G.5a: GET /jobs/{id}/annotations on a fresh upload returns 200 + empty list."""
    job_id = _upload_test_job(small_pdf_path, name="annotations empty test")
    r = client.get(f"/jobs/{job_id}/annotations")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["job_id"] == job_id
    assert body["annotations"] == []


def test_annotations_post_creates_manual_pin(small_pdf_path):
    """G.5a: POST /jobs/{id}/annotations creates a pin row, GET sees it."""
    job_id = _upload_test_job(small_pdf_path, name="ann post pin")
    payload = {
        "type": "pin",
        "page_idx": 3,
        "data": {"pinTypeId": "pt-abc", "pt": {"x": 100, "y": 200}, "note": "RTU 5"},
    }
    r = client.post(f"/jobs/{job_id}/annotations", json=payload)
    assert r.status_code == 201, r.text
    created = r.json()
    assert created["type"] == "pin"
    assert created["page_idx"] == 3
    assert created["source"] == "manual"
    assert created["data"]["pt"] == {"x": 100, "y": 200}
    assert created["data"]["note"] == "RTU 5"

    listing = client.get(f"/jobs/{job_id}/annotations").json()
    assert len(listing["annotations"]) == 1
    assert listing["annotations"][0]["id"] == created["id"]


def test_annotations_post_creates_manual_polygon(small_pdf_path):
    """G.5a: POST /jobs/{id}/annotations creates an area row with polygon data."""
    job_id = _upload_test_job(small_pdf_path, name="ann post poly")
    payload = {
        "type": "area",
        "page_idx": 0,
        "data": {
            "name": "Main roof",
            "points": [{"x": 0, "y": 0}, {"x": 100, "y": 0}, {"x": 100, "y": 50}, {"x": 0, "y": 50}],
            "sqft": 5000.0,
            "perimeter_ft": 300.0,
        },
    }
    r = client.post(f"/jobs/{job_id}/annotations", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert body["type"] == "area"
    assert body["data"]["sqft"] == 5000.0
    assert len(body["data"]["points"]) == 4


def test_annotations_patch_replaces_data(small_pdf_path):
    """G.5a: PATCH /jobs/{id}/annotations/{ann_id} full-row replace on data (Q4)."""
    job_id = _upload_test_job(small_pdf_path, name="ann patch")
    create_r = client.post(
        f"/jobs/{job_id}/annotations",
        json={"type": "pin", "page_idx": 1, "data": {"x": 10, "y": 20}},
    )
    ann_id = create_r.json()["id"]

    patch_r = client.patch(
        f"/jobs/{job_id}/annotations/{ann_id}",
        json={"data": {"x": 99, "y": 88, "note": "moved"}, "page_idx": 5},
    )
    assert patch_r.status_code == 200, patch_r.text
    patched = patch_r.json()
    assert patched["page_idx"] == 5
    assert patched["data"] == {"x": 99, "y": 88, "note": "moved"}


def test_annotations_delete_removes_row(small_pdf_path):
    """G.5a: DELETE /jobs/{id}/annotations/{ann_id} returns 204 and row is gone."""
    job_id = _upload_test_job(small_pdf_path, name="ann del")
    ann_id = client.post(
        f"/jobs/{job_id}/annotations",
        json={"type": "pin", "page_idx": 0, "data": {"x": 1, "y": 1}},
    ).json()["id"]
    r = client.delete(f"/jobs/{job_id}/annotations/{ann_id}")
    assert r.status_code == 204
    listing = client.get(f"/jobs/{job_id}/annotations").json()
    assert listing["annotations"] == []


def test_annotations_get_filters_by_page_idx(small_pdf_path):
    """G.5a: GET /jobs/{id}/annotations?page_idx=N returns only that page's rows."""
    job_id = _upload_test_job(small_pdf_path, name="ann filter page")
    for p in (0, 0, 5, 5, 5, 10):
        client.post(f"/jobs/{job_id}/annotations",
                    json={"type": "pin", "page_idx": p, "data": {"x": p, "y": p}})
    p0 = client.get(f"/jobs/{job_id}/annotations", params={"page_idx": 0}).json()
    p5 = client.get(f"/jobs/{job_id}/annotations", params={"page_idx": 5}).json()
    p10 = client.get(f"/jobs/{job_id}/annotations", params={"page_idx": 10}).json()
    assert len(p0["annotations"]) == 2
    assert len(p5["annotations"]) == 3
    assert len(p10["annotations"]) == 1


def test_annotations_get_filters_by_source(small_pdf_path):
    """G.5a: GET /jobs/{id}/annotations?source=manual returns only manual rows."""
    from core.job_storage import _connect
    import json as _json
    import uuid as _uuid
    from datetime import datetime as _dt, timezone as _tz

    job_id = _upload_test_job(small_pdf_path, name="ann filter source")
    # Manual via API
    client.post(f"/jobs/{job_id}/annotations",
                json={"type": "pin", "page_idx": 0, "data": {"x": 1, "y": 1}})
    # Auto via direct insert (simulating dispatch pre-populate)
    conn = _connect()
    try:
        now = _dt.now(_tz.utc).isoformat()
        conn.execute(
            "INSERT INTO annotations (id, job_id, system_id, type, page_idx, source, "
            "data_json, created_at, updated_at) "
            "VALUES (?, ?, NULL, 'pin', 0, 'auto', ?, ?, ?)",
            (str(_uuid.uuid4()), job_id, _json.dumps({"x": 50, "y": 50}), now, now),
        )
        conn.commit()
    finally:
        conn.close()

    manual = client.get(f"/jobs/{job_id}/annotations", params={"source": "manual"}).json()
    auto = client.get(f"/jobs/{job_id}/annotations", params={"source": "auto"}).json()
    assert len(manual["annotations"]) == 1
    assert manual["annotations"][0]["source"] == "manual"
    assert len(auto["annotations"]) == 1
    assert auto["annotations"][0]["source"] == "auto"


def test_annotations_get_filters_by_system_id(small_pdf_path):
    """G.5a: GET /jobs/{id}/annotations?system_id=X returns only annotations attached to X."""
    job_id = _upload_test_job(small_pdf_path, name="ann filter sys")
    # Make a system to attach to
    sys_r = client.post(f"/jobs/{job_id}/scope/systems",
                        json={"trade": "roofing", "label": "S1"})
    sys_id = sys_r.json()["id"]
    client.post(f"/jobs/{job_id}/annotations",
                json={"type": "pin", "page_idx": 0, "system_id": sys_id, "data": {"x": 1, "y": 1}})
    client.post(f"/jobs/{job_id}/annotations",
                json={"type": "pin", "page_idx": 1, "data": {"x": 2, "y": 2}})  # no system

    attached = client.get(f"/jobs/{job_id}/annotations", params={"system_id": sys_id}).json()
    assert len(attached["annotations"]) == 1
    assert attached["annotations"][0]["system_id"] == sys_id


def test_annotations_404_for_unknown_job_and_ann(small_pdf_path):
    """G.5a: 404 paths covered for POST/PATCH/DELETE on bad job_id and bad ann_id."""
    # Bad job
    r = client.post("/jobs/no-such-job/annotations",
                    json={"type": "pin", "page_idx": 0, "data": {}})
    assert r.status_code == 404
    r = client.get("/jobs/no-such-job/annotations")
    assert r.status_code == 404
    # Good job, bad ann
    job_id = _upload_test_job(small_pdf_path, name="ann 404")
    r = client.patch(f"/jobs/{job_id}/annotations/no-such-ann", json={"data": {}})
    assert r.status_code == 404
    r = client.delete(f"/jobs/{job_id}/annotations/no-such-ann")
    assert r.status_code == 404


def test_delete_scope_system_cascade_deletes_attached_annotations(small_pdf_path):
    """G.5a: deleting a scope_systems row also deletes its attached annotations
    (Q2 explicit cleanup helper). Annotations with NULL system_id are untouched."""
    job_id = _upload_test_job(small_pdf_path, name="ann cascade")
    sys_id = client.post(f"/jobs/{job_id}/scope/systems",
                         json={"trade": "roofing", "label": "doomed"}).json()["id"]
    # 2 attached, 1 floating
    client.post(f"/jobs/{job_id}/annotations",
                json={"type": "pin", "page_idx": 0, "system_id": sys_id, "data": {"x": 1, "y": 1}})
    client.post(f"/jobs/{job_id}/annotations",
                json={"type": "area", "page_idx": 1, "system_id": sys_id, "data": {"name": "A1"}})
    client.post(f"/jobs/{job_id}/annotations",
                json={"type": "pin", "page_idx": 2, "data": {"x": 9, "y": 9}})
    before = client.get(f"/jobs/{job_id}/annotations").json()
    assert len(before["annotations"]) == 3

    del_r = client.delete(f"/jobs/{job_id}/scope/systems/{sys_id}")
    assert del_r.status_code == 204
    after = client.get(f"/jobs/{job_id}/annotations").json()
    assert len(after["annotations"]) == 1, f"expected only the floating ann to remain, got {after}"
    assert after["annotations"][0]["system_id"] is None


def test_dispatch_pre_populates_auto_pins_when_equipment_pins_present():
    """G.5a: _pre_populate_auto_annotations extracts equipment_pins from
    ctx.trade_module_outputs and writes source='auto' annotation rows. Tested
    directly against the storage helpers (without running real dispatch) since
    the small_pdf_path fixture won't trigger RoofingModule output."""
    from core.job_storage import (
        _connect, _pre_populate_auto_annotations, create_job,
        create_scope_system, list_annotations,
    )
    from dataclasses import dataclass, field
    import shutil
    from pathlib import Path

    # Need a real existing PDF for create_job's _pdf_sha1 — reuse Silverleaf if present,
    # else the small minimal PDF written to tmp.
    silverleaf = Path(r"C:\huck stage 2\full bid sets\B2607 AEA Silverleaf - St Augustine - Accelerated Construction Services (6).pdf")
    if not silverleaf.exists():
        import pytest
        pytest.skip("Silverleaf bidset not found; this test needs an existing PDF for create_job's sha1 step")

    job_id = create_job(name="auto-pin extract test", pdf_path=str(silverleaf))
    # Pre-create a roofing scope_systems row so the auto-pin attaches to it.
    sys = create_scope_system(job_id, trade="roofing", label="Roofing target")

    # Build a fake ctx with trade_module_outputs containing equipment_pins.
    @dataclass
    class FakeCtx:
        trade_module_outputs: dict = field(default_factory=dict)

    ctx = FakeCtx()
    ctx.trade_module_outputs = {
        12: {
            "roofing": {
                "fields": {},
                "warnings": [],
                "equipment_pins": [
                    {"x": 100, "y": 200, "equipment_type": "drain", "confidence": 0.9},
                    {"x": 150, "y": 250, "equipment_type": "scupper", "confidence": 0.7},
                ],
            },
        },
        18: {
            "roofing": {
                "equipment_pins": [
                    {"x": 50, "y": 75, "equipment_type": "rtu", "confidence": 0.85},
                ],
            },
        },
        20: {
            "glazing": {
                "equipment_pins": [],  # empty — skip
            },
        },
    }

    _pre_populate_auto_annotations(job_id, ctx)

    rows = list_annotations(job_id, source="auto")
    assert len(rows) == 3, f"expected 3 auto-pin rows, got {len(rows)}"

    # All rows attached to the roofing system we created
    assert all(r["system_id"] == sys["id"] for r in rows), \
        "all auto roofing pins should attach to the roofing scope_systems row"
    assert all(r["type"] == "pin" for r in rows)
    assert all(r["source"] == "auto" for r in rows)

    # Idempotency: running again should clear & re-insert (3 rows, not 6)
    _pre_populate_auto_annotations(job_id, ctx)
    rows2 = list_annotations(job_id, source="auto")
    assert len(rows2) == 3, "auto pre-populate must be idempotent"

    # Cleanup
    conn = _connect()
    try:
        conn.execute("DELETE FROM annotations WHERE job_id = ?", (job_id,))
        conn.execute("DELETE FROM scope_systems WHERE job_id = ?", (job_id,))
        conn.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
        conn.commit()
    finally:
        conn.close()
