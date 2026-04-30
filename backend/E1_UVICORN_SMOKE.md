# E.1 uvicorn Socket Smoke Report

**Date:** 2026-04-30
**Branch:** `phase2-v0.3-E1-discipline-patches`
**Bidset (POST payload):** B2607 AEA Silverleaf — `B2607 AEA Silverleaf - St Augustine - Accelerated Construction Services (6).pdf`
**Mode:** real uvicorn subprocess + real HTTP via `requests` (not in-process TestClient)
**Endpoint base:** `http://127.0.0.1:8000`
**uvicorn boot time:** 1.1s
**Total wall-clock:** 1.2s
**Job ID created during smoke:** `98bd2e75-0458-41f8-865b-a4b8304c163b`
**Overall:** **PASS**

---

## §1 — Assertions

| # | Assertion | Result | Evidence |
|---|---|---|---|
| 0 | uvicorn subprocess binds /health within 30s | PASS | boot_dt=1.1s |
| 1 | GET /health → 200 + {"status": "ok"} | PASS | status=200, body='{"status": "ok", "version": "0.3.0-E.1"}' |
| 2 | GET /docs → 200 (Swagger UI HTML) | PASS | status=200, content-type=text/html; charset=utf-8, body_len=1013, swagger_in_body=True |
| 3 | POST /jobs → 201 + valid JobResponse JSON | PASS | status=201, keys_match=True, id=98bd2e75-0458-41f8-865b-a4b8304c163b |
| 4 | GET /jobs/{id} → 200 + same job | PASS | status=200, id_match=True, name_match=True |

---

## §2 — Response bodies (verification)

### 1. GET /health → 200 + {"status": "ok"}

```
{"status": "ok", "version": "0.3.0-E.1"}
```

### 2. GET /docs → 200 (Swagger UI HTML)

```

    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
    <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/
```

### 3. POST /jobs → 201 + valid JobResponse JSON

```
{
  "id": "98bd2e75-0458-41f8-865b-a4b8304c163b",
  "name": "Silverleaf E.1 uvicorn smoke",
  "gc": "Accelerated Construction Services",
  "location_city": "St Augustine",
  "location_state": "FL",
  "trade_scope": "roofing,glazing",
  "bid_due_date": null,
  "notes": null,
  "status": "draft",
  "created_at": "2026-04-30T18:04:14.069582+00:00",
  "updated_at": "2026-04-30T18:04:14.069582+00:00",
  "pdf_path": "C:\\huck stage 2\\full bid sets\\B2607 AEA Silverleaf - St Augustine - Accelerated Construction Services (6).pdf",
  "pdf_sha1": "76dc89072dae77c1b476b60da85870f3d799cd31",
  "dispatch_
```

### 4. GET /jobs/{id} → 200 + same job

```
{
  "id": "98bd2e75-0458-41f8-865b-a4b8304c163b",
  "name": "Silverleaf E.1 uvicorn smoke",
  "gc": "Accelerated Construction Services",
  "location_city": "St Augustine",
  "location_state": "FL",
  "trade_scope": "roofing,glazing",
  "bid_due_date": null,
  "notes": null,
  "status": "draft",
  "created_at": "2026-04-30T18:04:14.069582+00:00",
  "updated_at": "2026-04-30T18:04:14.069582+00:00",
  "pdf_path": "C:\\huck stage 2\\full bid sets\\B2607 AEA Silverleaf - St Augustine - Accelerated Construction Services (6).pdf",
  "pdf_sha1": "76dc89072dae77c1b476b60da85870f3d799cd31",
  "dispatch_
```

---

## §3 — Overall: **PASS**

All four assertions passed against a real uvicorn subprocess on http://127.0.0.1:8000. Confirms the in-process TestClient suite (E.1's 6 tests) and the production run-mode (uvicorn over HTTP) agree on the `/health`, `/docs`, `POST /jobs`, and `GET /jobs/{id}` contracts.

