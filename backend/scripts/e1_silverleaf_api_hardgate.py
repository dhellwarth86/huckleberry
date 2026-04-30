"""E.1 single-bidset hard gate — FastAPI + D.2 persistence end-to-end on Silverleaf.

Per MARCH_ORDERS_E_1_fastapi_scaffold.md §7. Single-bidset only — no 3-bidset
run (compute-heavy multi-bidset testing deferred until Phase G ships quadrant
smart scan, per Daniel directive 2026-04-29).

Uses FastAPI's TestClient (in-process, no uvicorn subprocess). Runs 8 checks:

1. Server starts without error (TestClient initializes successfully)
2. POST /jobs returns 201 with full JobResponse
3. GET /jobs/{id} returns 200 with same job
4. Job persists in SQLite (job_storage.get_job round-trip from outside the API)
5. created_at is a recent timestamp
6. pdf_sha1 in response matches actual file SHA-1
7. POST /jobs with status="banana" returns 422 (Pydantic Literal enforced)
8. GET /jobs/{nonexistent} returns 404 with safe error body

Writes hard gate report to backend/E1_HARD_GATE_silverleaf_api.md.

Usage:
    python backend/scripts/e1_silverleaf_api_hardgate.py
"""
from __future__ import annotations

import hashlib
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve()
BACKEND = HERE.parent.parent
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from api.main import app  # noqa: E402
from core.job_storage import get_job  # noqa: E402

PDF_PATH = Path(
    r"C:\huck stage 2\full bid sets\B2607 AEA Silverleaf - St Augustine - Accelerated Construction Services (6).pdf"
)
OUT_PATH = BACKEND / "E1_HARD_GATE_silverleaf_api.md"


def _file_sha1(p: Path) -> str:
    h = hashlib.sha1()
    with open(p, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if not PDF_PATH.exists():
        print(f"ERROR: PDF not found at {PDF_PATH}", file=sys.stderr)
        return 3

    expected_sha1 = _file_sha1(PDF_PATH)
    print(f"[e1-hardgate] Silverleaf PDF SHA-1: {expected_sha1}", flush=True)

    results: list[tuple[int, str, bool, str]] = []

    # ── Check 1: TestClient initializes ──
    try:
        client = TestClient(app)
        ok1 = True
        ev1 = "TestClient(app) constructed; /openapi.json reachable"
        # sanity probe
        op = client.get("/openapi.json")
        if op.status_code != 200:
            ok1 = False
            ev1 = f"openapi.json returned {op.status_code}"
    except Exception as exc:  # pragma: no cover — defensive
        ok1 = False
        ev1 = f"{type(exc).__name__}: {str(exc)[:160]}"
    results.append((1, "Server starts without error (TestClient initialized)", ok1, ev1))

    if not ok1:
        _write_report(results, expected_sha1=expected_sha1, posted_id=None)
        return 5

    # ── Check 2: POST /jobs returns 201 with full JobResponse ──
    payload = {
        "name": "Silverleaf E.1 hard gate",
        "pdf_path": str(PDF_PATH),
        "gc": "Accelerated Construction Services",
        "location_city": "St Augustine",
        "location_state": "FL",
        "trade_scope": "roofing,glazing",
        "status": "draft",
    }
    t_post = time.time()
    post_resp = client.post("/jobs", json=payload)
    post_dt = time.time() - t_post
    posted_body = post_resp.json() if post_resp.status_code in (200, 201) else None
    ok2 = post_resp.status_code == 201 and posted_body is not None and "id" in posted_body
    if ok2:
        EXPECTED = {
            "id", "name", "gc", "location_city", "location_state", "trade_scope",
            "bid_due_date", "notes", "status", "created_at", "updated_at",
            "pdf_path", "pdf_sha1", "dispatch_complete",
        }
        if set(posted_body.keys()) != EXPECTED:
            ok2 = False
    ev2 = (
        f"status={post_resp.status_code}, body keys count={len(posted_body) if posted_body else 0}, "
        f"id={posted_body['id'] if (posted_body and 'id' in posted_body) else 'n/a'}, "
        f"latency={post_dt*1000:.1f}ms"
    )
    results.append((2, "POST /jobs returns 201 with full JobResponse", ok2, ev2))

    if not ok2:
        _write_report(results, expected_sha1=expected_sha1, posted_id=None)
        return 5

    job_id = posted_body["id"]

    # ── Check 3: GET /jobs/{id} returns 200 with same job ──
    get_resp = client.get(f"/jobs/{job_id}")
    got_body = get_resp.json() if get_resp.status_code == 200 else None
    ok3 = get_resp.status_code == 200 and got_body is not None and got_body.get("id") == job_id
    ev3 = (
        f"status={get_resp.status_code}, "
        f"id matches: {got_body.get('id') == job_id if got_body else False}, "
        f"name={(got_body or {}).get('name', '?')!r}"
    )
    results.append((3, "GET /jobs/{id} returns 200 with same job", ok3, ev3))

    # ── Check 4: Job persists in SQLite (job_storage round-trip from outside the API) ──
    direct = get_job(job_id)
    ok4 = direct is not None and direct.get("id") == job_id and direct.get("name") == payload["name"]
    ev4 = (
        f"core.job_storage.get_job({job_id[:8]}…) returned "
        f"{'dict id matches' if ok4 else 'None or mismatch'}"
    )
    results.append((4, "Job persists in SQLite (direct job_storage round-trip)", ok4, ev4))

    # ── Check 5: created_at is a recent timestamp ──
    created_at_str = posted_body.get("created_at", "")
    ok5 = False
    age_sec: float | None = None
    try:
        created_at = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        age_sec = (now - created_at).total_seconds()
        ok5 = 0 <= age_sec < 60
    except Exception:  # pragma: no cover — defensive
        pass
    ev5 = (
        f"created_at={created_at_str!r}, age={age_sec:.1f}s "
        f"(expected 0 <= age < 60)" if age_sec is not None else f"created_at={created_at_str!r} (parse failed)"
    )
    results.append((5, "created_at is recent timestamp (within 60s)", ok5, ev5))

    # ── Check 6: pdf_sha1 in response matches actual file SHA-1 ──
    response_sha1 = posted_body.get("pdf_sha1", "")
    ok6 = response_sha1 == expected_sha1
    ev6 = f"response={response_sha1!r}, expected={expected_sha1!r}"
    results.append((6, "pdf_sha1 in response matches actual file SHA-1", ok6, ev6))

    # ── Check 7: Invalid status returns 422 ──
    bad_payload = {
        "name": "Should reject",
        "pdf_path": str(PDF_PATH),
        "status": "banana",  # not in JobStatus Literal
    }
    bad_status_resp = client.post("/jobs", json=bad_payload)
    ok7 = bad_status_resp.status_code == 422
    ev7 = f"status={bad_status_resp.status_code} (expected 422)"
    results.append((7, "Invalid status returns 422 (Pydantic Literal enforced)", ok7, ev7))

    # ── Check 8: Non-existent job returns 404 with safe error body ──
    nf_resp = client.get("/jobs/nonexistent-job-id-12345")
    nf_body = nf_resp.json() if nf_resp.status_code == 404 else None
    ok8 = (
        nf_resp.status_code == 404
        and nf_body is not None
        and nf_body.get("detail") == "Job not found"
    )
    # Data-leak guard: error body short and free of SQL/path/traceback markers
    err_str = str(nf_body).lower() if nf_body else ""
    forbidden = ["select ", "from jobs", "sqlite", "traceback", "execute("]
    leaked = [f for f in forbidden if f in err_str]
    if leaked:
        ok8 = False
    ev8 = (
        f"status={nf_resp.status_code}, body={nf_body!r}, "
        f"leaked markers: {leaked if leaked else 'none'}"
    )
    results.append((8, "Non-existent job returns 404 with safe error body (data-leak guard)", ok8, ev8))

    overall = all(r[2] for r in results)
    _write_report(results, expected_sha1=expected_sha1, posted_id=job_id)

    print(f"\n[e1-hardgate] OVERALL: {'PASS' if overall else 'FAIL'}", flush=True)
    for num, desc, ok, ev in results:
        print(f"  {num}. [{'PASS' if ok else 'FAIL'}] {desc} — {ev}", flush=True)

    return 0 if overall else 5


def _write_report(
    results: list[tuple[int, str, bool, str]],
    *,
    expected_sha1: str,
    posted_id: str | None,
) -> None:
    overall = all(r[2] for r in results) if results else False
    lines: list[str] = []
    a = lines.append

    a("# E.1 Silverleaf API Hard Gate Report")
    a("")
    a(f"**Date:** {time.strftime('%Y-%m-%d')}")
    a("**Branch:** `phase2-v0.3-E1-fastapi-scaffold`")
    a(f"**Bidset:** B2607 AEA Silverleaf — `{PDF_PATH.name}`")
    a("**Pipeline:** FastAPI server (in-process via TestClient) + D.2 persistence layer")
    a("**Mode:** Single-bidset (3-bidset deferred to post-Phase-G per Daniel directive 2026-04-29)")
    a(f"**Overall:** **{'PASS' if overall else 'FAIL'}**")
    a("")
    a(f"**Silverleaf PDF SHA-1 (computed at gate run):** `{expected_sha1}`")
    if posted_id:
        a(f"**Job ID created during gate:** `{posted_id}`")
    a("")
    a("---")
    a("")
    a("## §1 — API + persistence verification")
    a("")
    a("| # | Test | Result | Evidence |")
    a("|---|---|---|---|")
    for num, desc, ok, ev in results:
        a(f"| {num} | {desc} | {'PASS' if ok else 'FAIL'} | {ev} |")
    a("")
    a("---")
    a("")
    a("## §2 — Sacred floor verification")
    a("")
    a("Captured separately by the gate report at `backend/E1_GATE_REPORT.md`. Floors:")
    a("")
    a("- Backend tests: **222/19/0** (216 pre-existing + 6 new E.1 tests)")
    a("- Frontend tests: **138/138 against v6.3.5** (vault-treated, untouched)")
    a("- Vault-ruled module SHA-1s: 5 unchanged (verified pre + post session)")
    a("- v6.3.5 SHA-1 unchanged")
    a("")
    a("---")
    a("")
    a(f"## §3 — Overall: **{'PASS' if overall else 'FAIL'}**")
    a("")
    if overall:
        a(
            "All 8 hard gate criteria pass. The FastAPI scaffold + D.2 persistence "
            "layer round-trip cleanly on the Silverleaf bidset, with the data-leak "
            "guards (extra='forbid' on JobResponse, generic error messages) "
            "behaving as designed."
        )
    else:
        a("Hard gate FAIL — see failing rows above. §10 stop fired.")
    a("")
    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[e1-hardgate] wrote {OUT_PATH}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
