# E.1 Silverleaf API Hard Gate Report

**Date:** 2026-04-30
**Branch:** `phase2-v0.3-E1-fastapi-scaffold`
**Bidset:** B2607 AEA Silverleaf — `B2607 AEA Silverleaf - St Augustine - Accelerated Construction Services (6).pdf`
**Pipeline:** FastAPI server (in-process via TestClient) + D.2 persistence layer
**Mode:** Single-bidset (3-bidset deferred to post-Phase-G per Daniel directive 2026-04-29)
**Overall:** **PASS**

**Silverleaf PDF SHA-1 (computed at gate run):** `76dc89072dae77c1b476b60da85870f3d799cd31`
**Job ID created during gate:** `c71dcdaa-b041-4cab-af41-337b9ce73448`

---

## §1 — API + persistence verification

| # | Test | Result | Evidence |
|---|---|---|---|
| 1 | Server starts without error (TestClient initialized) | PASS | TestClient(app) constructed; /openapi.json reachable |
| 2 | POST /jobs returns 201 with full JobResponse | PASS | status=201, body keys count=14, id=c71dcdaa-b041-4cab-af41-337b9ce73448, latency=33.7ms |
| 3 | GET /jobs/{id} returns 200 with same job | PASS | status=200, id matches: True, name='Silverleaf E.1 hard gate' |
| 4 | Job persists in SQLite (direct job_storage round-trip) | PASS | core.job_storage.get_job(c71dcdaa…) returned dict id matches |
| 5 | created_at is recent timestamp (within 60s) | PASS | created_at='2026-04-30T17:00:05.873460+00:00', age=0.0s (expected 0 <= age < 60) |
| 6 | pdf_sha1 in response matches actual file SHA-1 | PASS | response='76dc89072dae77c1b476b60da85870f3d799cd31', expected='76dc89072dae77c1b476b60da85870f3d799cd31' |
| 7 | Invalid status returns 422 (Pydantic Literal enforced) | PASS | status=422 (expected 422) |
| 8 | Non-existent job returns 404 with safe error body (data-leak guard) | PASS | status=404, body={'detail': 'Job not found'}, leaked markers: none |

---

## §2 — Sacred floor verification

Captured separately by the gate report at `backend/E1_GATE_REPORT.md`. Floors:

- Backend tests: **222/19/0** (216 pre-existing + 6 new E.1 tests)
- Frontend tests: **138/138 against v6.3.5** (vault-treated, untouched)
- Vault-ruled module SHA-1s: 5 unchanged (verified pre + post session)
- v6.3.5 SHA-1 unchanged

---

## §3 — Overall: **PASS**

All 8 hard gate criteria pass. The FastAPI scaffold + D.2 persistence layer round-trip cleanly on the Silverleaf bidset, with the data-leak guards (extra='forbid' on JobResponse, generic error messages) behaving as designed.

