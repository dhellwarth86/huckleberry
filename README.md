# Huckleberry AI

Commercial roofing takeoff application.

## Repo layout

- **`frontend/`** — Phase 1: single-file HTML viewer + manual takeoff toolchain. Runs offline in Chrome. Currently at v6.3.5, 138/138 tests green.
- **`backend/`** — Phase 2: Python service for PDF intake, data analysis, persistence. FastAPI + SQLAlchemy + Postgres + Pydantic. Localhost-only during POC.
- **`shared/`** — The wrapper schema. Pydantic models that define the contract between frontend and backend.

## Documentation (read in order)

1. **`CLAUDE.md`** — architectural canon. Phases, the 18 ratified Phase 2 decisions, Karpathy Procedure, full session history. **Read this completely before any code change.**
2. **`PHASE_2_HANDOFF.md`** — runbook for the v0.1 experiment. Pre-flight, setup tasks, the verbatim Claude Code experiment prompt, review checkpoint instructions.
3. **`backend/README.md`** — backend-specific dev setup notes.
4. **`backend/seeds/README.md`** — explains the four-layer reference architecture (dispatch / materials / assemblies).

## Quick start

### Phase 1 (frontend, already working)
```bash
cd frontend
npm install
npm test
# Expected: RESULT: 138/138 passed, 0 failed
```

### Phase 2 (backend, bootstrap only — experiment hasn't run yet)
```bash
cd backend
uv venv
uv pip install -e ".[dev]"
docker compose up -d postgres   # from repo root
pytest tests/test_seeds_load.py
# Expected: 5 pass (all five seed files import cleanly)
```

## Phase status

- Phase 1: **closed at v6.3.5.** Manual toolchain mature, mutation-tested, browser-verified.
- Phase 2: **planned, not started.** Eighteen architectural decisions ratified 2026-04-25 (see `CLAUDE.md` "Phases" section).
- Phase 3: **deferred.** Auth, multi-user, network exposure, LLM/ML — not planned. Requires explicit user re-decision.

The Phase 1 HTML must remain runnable standalone forever as the offline fallback, even after Phase 2 ships.
