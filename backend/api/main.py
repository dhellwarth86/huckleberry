"""FastAPI application — E.1.

Three endpoints total:
- GET  /health       exempt liveness probe (zero state, no DB)
- POST /jobs         create a job
- GET  /jobs/{id}    load a job

Permissive CORS in dev. OpenAPI docs at /docs and /redoc. Auth deferred
to the Postgres/security phase. See backend/E0_API_DESIGN.md.

Run:
    cd backend
    python -m uvicorn api.main:app --reload --port 8000
"""
from __future__ import annotations

import uvicorn  # E.1
from fastapi import FastAPI  # E.1
from fastapi.middleware.cors import CORSMiddleware  # E.1

from api.routes import jobs as jobs_routes  # E.1

app = FastAPI(  # E.1
    title="Huckleberry AI",
    version="0.3.0-E.1",
    description=(
        "Huckleberry AI backend API — E.1 ships /health + POST /jobs + GET /jobs/{id} "
        "over the D.2 SQLite persistence layer."
    ),
)

# E.1: permissive CORS for dev; locked down at Postgres/security phase
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")  # E.1: exempt liveness probe (out of the 2-endpoint budget)
def health() -> dict:
    """Liveness probe. Zero state, no DB coupling."""
    return {"status": "ok", "version": "0.3.0-E.1"}


app.include_router(jobs_routes.router)  # E.1


# E.1: docs at /docs and /redoc are FastAPI defaults; hidden at Postgres/security phase
if __name__ == "__main__":
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)
