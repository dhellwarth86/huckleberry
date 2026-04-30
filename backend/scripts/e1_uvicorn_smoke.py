"""E.1 discipline patch — uvicorn socket smoke (~60-second verification).

Per the E.1 discipline-patches spec: spin up the FastAPI app under a real
uvicorn subprocess (not TestClient), wait for the port to bind, hit the
four endpoints over real HTTP, capture results, write a report, kill the
subprocess. Verifies the production run-mode works the way the in-process
TestClient suite already proved the app contract works.

Four assertions:

1. GET  http://localhost:8000/health         → 200 + {"status": "ok"}
2. GET  http://localhost:8000/docs           → 200 (Swagger HTML)
3. POST http://localhost:8000/jobs           → 201 + JobResponse JSON (Silverleaf payload)
4. GET  http://localhost:8000/jobs/{id}      → 200 + same job

Usage:
    python backend/scripts/e1_uvicorn_smoke.py

Writes report to backend/E1_UVICORN_SMOKE.md. Exit 0 on PASS, 5 on FAIL,
3 on infra error (PDF missing, port can't bind, subprocess won't start).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import traceback
from pathlib import Path

import requests

HERE = Path(__file__).resolve()
BACKEND = HERE.parent.parent
sys.path.insert(0, str(BACKEND))

PDF_PATH = Path(
    r"C:\huck stage 2\full bid sets\B2607 AEA Silverleaf - St Augustine - Accelerated Construction Services (6).pdf"
)
OUT_PATH = BACKEND / "E1_UVICORN_SMOKE.md"

HOST = "127.0.0.1"
PORT = 8000
BASE = f"http://{HOST}:{PORT}"
READY_TIMEOUT_S = 30  # uvicorn boot ceiling
REQ_TIMEOUT_S = 10


def _wait_for_health(deadline: float) -> tuple[bool, str]:
    """Poll /health until it answers 200 or deadline passes."""
    last_err = ""
    while time.time() < deadline:
        try:
            r = requests.get(f"{BASE}/health", timeout=2)
            if r.status_code == 200:
                return True, ""
            last_err = f"status={r.status_code}"
        except requests.exceptions.ConnectionError as e:
            last_err = f"ConnectionError: {str(e)[:120]}"
        except Exception as e:  # pragma: no cover — defensive
            last_err = f"{type(e).__name__}: {str(e)[:120]}"
        time.sleep(0.4)
    return False, last_err or "deadline exceeded"


def main() -> int:  # noqa: PLR0915
    if not PDF_PATH.exists():
        print(f"ERROR: Silverleaf PDF not found at {PDF_PATH}", file=sys.stderr)
        return 3

    t_total = time.time()
    results: list[tuple[int, str, bool, str, str]] = []  # (n, desc, ok, evidence, body_excerpt)
    boot_dt: float | None = None
    proc: subprocess.Popen | None = None
    posted_id: str | None = None

    try:
        # ── Boot uvicorn subprocess ──
        env = os.environ.copy()
        # Ensure backend is on the path for `api.main:app` resolution
        env["PYTHONPATH"] = str(BACKEND) + (
            os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else ""
        )
        cmd = [
            sys.executable,
            "-m",
            "uvicorn",
            "api.main:app",
            "--host",
            HOST,
            "--port",
            str(PORT),
            "--log-level",
            "warning",
        ]
        print(f"[e1-smoke] launching uvicorn: {' '.join(cmd)}", flush=True)
        t_boot = time.time()
        proc = subprocess.Popen(
            cmd,
            cwd=str(BACKEND),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        ready, last_err = _wait_for_health(time.time() + READY_TIMEOUT_S)
        boot_dt = time.time() - t_boot

        if not ready:
            # Capture any subprocess output for diagnosis
            sub_out = ""
            if proc.poll() is not None:
                try:
                    sub_out = proc.stdout.read() if proc.stdout else ""
                except Exception:
                    sub_out = "(could not read subprocess stdout)"
            results.append((
                0,
                "uvicorn subprocess binds /health within 30s",
                False,
                f"boot_dt={boot_dt:.1f}s, last_err='{last_err}', proc_returncode={proc.returncode}",
                sub_out[:500],
            ))
            _write_report(results, boot_dt=boot_dt, posted_id=posted_id, total_dt=time.time() - t_total)
            return 5

        results.append((
            0,
            "uvicorn subprocess binds /health within 30s",
            True,
            f"boot_dt={boot_dt:.1f}s",
            "",
        ))
        print(f"[e1-smoke] uvicorn ready in {boot_dt:.1f}s", flush=True)

        # ── Assertion 1: GET /health ──
        try:
            r1 = requests.get(f"{BASE}/health", timeout=REQ_TIMEOUT_S)
            body1 = r1.json() if r1.headers.get("content-type", "").startswith("application/json") else None
            ok1 = r1.status_code == 200 and isinstance(body1, dict) and body1.get("status") == "ok"
            ev1 = f'status={r1.status_code}, body={json.dumps(body1) if body1 is not None else r1.text[:100]!r}'
            results.append((1, 'GET /health → 200 + {"status": "ok"}', ok1, ev1, json.dumps(body1)[:300] if body1 else ""))
        except Exception as e:
            results.append((1, 'GET /health → 200 + {"status": "ok"}', False, f"{type(e).__name__}: {str(e)[:120]}", traceback.format_exc()[:500]))

        # ── Assertion 2: GET /docs ──
        try:
            r2 = requests.get(f"{BASE}/docs", timeout=REQ_TIMEOUT_S)
            body2 = r2.text
            ok2 = r2.status_code == 200 and "swagger" in body2.lower()
            ev2 = f"status={r2.status_code}, content-type={r2.headers.get('content-type', '?')}, body_len={len(body2)}, swagger_in_body={'swagger' in body2.lower()}"
            results.append((2, "GET /docs → 200 (Swagger UI HTML)", ok2, ev2, body2[:300]))
        except Exception as e:
            results.append((2, "GET /docs → 200 (Swagger UI HTML)", False, f"{type(e).__name__}: {str(e)[:120]}", traceback.format_exc()[:500]))

        # ── Assertion 3: POST /jobs (Silverleaf payload) ──
        payload = {
            "name": "Silverleaf E.1 uvicorn smoke",
            "pdf_path": str(PDF_PATH),
            "gc": "Accelerated Construction Services",
            "location_city": "St Augustine",
            "location_state": "FL",
            "trade_scope": "roofing,glazing",
        }
        EXPECTED_FIELDS = {
            "id", "name", "gc", "location_city", "location_state", "trade_scope",
            "bid_due_date", "notes", "status", "created_at", "updated_at",
            "pdf_path", "pdf_sha1", "dispatch_complete",
        }
        try:
            r3 = requests.post(f"{BASE}/jobs", json=payload, timeout=REQ_TIMEOUT_S)
            body3 = r3.json() if r3.headers.get("content-type", "").startswith("application/json") else None
            ok3 = (
                r3.status_code == 201
                and isinstance(body3, dict)
                and set(body3.keys()) == EXPECTED_FIELDS
                and body3.get("status") == "draft"
                and len(body3.get("pdf_sha1", "")) == 40
            )
            if ok3:
                posted_id = body3["id"]
            ev3 = (
                f"status={r3.status_code}, "
                f"keys_match={set(body3.keys()) == EXPECTED_FIELDS if isinstance(body3, dict) else False}, "
                f"id={body3.get('id', 'n/a') if isinstance(body3, dict) else 'n/a'}"
            )
            body3_excerpt = json.dumps(body3, indent=2)[:600] if body3 else r3.text[:300]
            results.append((3, "POST /jobs → 201 + valid JobResponse JSON", ok3, ev3, body3_excerpt))
        except Exception as e:
            results.append((3, "POST /jobs → 201 + valid JobResponse JSON", False, f"{type(e).__name__}: {str(e)[:120]}", traceback.format_exc()[:500]))

        # ── Assertion 4: GET /jobs/{id} ──
        if posted_id:
            try:
                r4 = requests.get(f"{BASE}/jobs/{posted_id}", timeout=REQ_TIMEOUT_S)
                body4 = r4.json() if r4.headers.get("content-type", "").startswith("application/json") else None
                ok4 = (
                    r4.status_code == 200
                    and isinstance(body4, dict)
                    and body4.get("id") == posted_id
                    and body4.get("name") == payload["name"]
                )
                ev4 = (
                    f"status={r4.status_code}, "
                    f"id_match={body4.get('id') == posted_id if isinstance(body4, dict) else False}, "
                    f"name_match={body4.get('name') == payload['name'] if isinstance(body4, dict) else False}"
                )
                body4_excerpt = json.dumps(body4, indent=2)[:600] if body4 else r4.text[:300]
                results.append((4, "GET /jobs/{id} → 200 + same job", ok4, ev4, body4_excerpt))
            except Exception as e:
                results.append((4, "GET /jobs/{id} → 200 + same job", False, f"{type(e).__name__}: {str(e)[:120]}", traceback.format_exc()[:500]))
        else:
            results.append((4, "GET /jobs/{id} → 200 + same job", False, "skipped — POST did not return an id", ""))

    finally:
        # ── Tear down subprocess ──
        if proc is not None and proc.poll() is None:
            try:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait(timeout=5)
                print("[e1-smoke] uvicorn subprocess terminated", flush=True)
            except Exception as e:  # pragma: no cover — defensive
                print(f"[e1-smoke] WARN: subprocess teardown error: {e}", file=sys.stderr)

    total_dt = time.time() - t_total
    overall = all(r[2] for r in results)
    _write_report(results, boot_dt=boot_dt, posted_id=posted_id, total_dt=total_dt)

    print(f"\n[e1-smoke] OVERALL: {'PASS' if overall else 'FAIL'} (total {total_dt:.1f}s)", flush=True)
    for n, desc, ok, ev, _excerpt in results:
        print(f"  {n}. [{'PASS' if ok else 'FAIL'}] {desc} — {ev}", flush=True)

    return 0 if overall else 5


def _write_report(
    results: list[tuple[int, str, bool, str, str]],
    *,
    boot_dt: float | None,
    posted_id: str | None,
    total_dt: float,
) -> None:
    overall = all(r[2] for r in results) if results else False
    lines: list[str] = []
    a = lines.append

    a("# E.1 uvicorn Socket Smoke Report")
    a("")
    a(f"**Date:** {time.strftime('%Y-%m-%d')}")
    a("**Branch:** `phase2-v0.3-E1-discipline-patches`")
    a(f"**Bidset (POST payload):** B2607 AEA Silverleaf — `{PDF_PATH.name}`")
    a("**Mode:** real uvicorn subprocess + real HTTP via `requests` (not in-process TestClient)")
    a(f"**Endpoint base:** `{BASE}`")
    a(f"**uvicorn boot time:** {f'{boot_dt:.1f}s' if boot_dt is not None else 'n/a (boot failed)'}")
    a(f"**Total wall-clock:** {total_dt:.1f}s")
    if posted_id:
        a(f"**Job ID created during smoke:** `{posted_id}`")
    a(f"**Overall:** **{'PASS' if overall else 'FAIL'}**")
    a("")
    a("---")
    a("")
    a("## §1 — Assertions")
    a("")
    a("| # | Assertion | Result | Evidence |")
    a("|---|---|---|---|")
    for n, desc, ok, ev, _ex in results:
        a(f"| {n} | {desc} | {'PASS' if ok else 'FAIL'} | {ev} |")
    a("")
    a("---")
    a("")
    a("## §2 — Response bodies (verification)")
    a("")
    for n, desc, ok, ev, ex in results:
        if not ex:
            continue
        a(f"### {n}. {desc}")
        a("")
        a("```")
        a(ex)
        a("```")
        a("")
    a("---")
    a("")
    a(f"## §3 — Overall: **{'PASS' if overall else 'FAIL'}**")
    a("")
    if overall:
        a(
            "All four assertions passed against a real uvicorn subprocess on "
            f"{BASE}. Confirms the in-process TestClient suite (E.1's 6 tests) "
            "and the production run-mode (uvicorn over HTTP) agree on the "
            "`/health`, `/docs`, `POST /jobs`, and `GET /jobs/{id}` contracts."
        )
    else:
        a("Smoke FAIL — see failing rows above. §7 stop fired.")
    a("")
    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[e1-smoke] wrote {OUT_PATH}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
