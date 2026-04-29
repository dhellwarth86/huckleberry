# PHASE_2_HANDOFF.md — Huckleberry AI Phase 2 Kickoff Runbook

> **What this is**: A runbook for the next session that enters Phase 2 of Huckleberry AI. Pairs with `CLAUDE.md` (which is the architectural canon, not a runbook).
>
> **What it isn't**: It is not the Phase 2 plan. The Phase 2 plan lives in CLAUDE.md's "Phases" section as 18 ratified architectural decisions. This document is the operational steps for executing the *first* Phase 2 milestone (v0.1 — the experiment).
>
> **What v0.1 is**: An experiment, not a backend build. Run via Claude Code against 15 real bidsets. Produces a draft Pydantic schema + findings report. **Does not produce a backend.** The backend is v0.2, planned after the experiment review checkpoint.
>
> **Pairs with**: CLAUDE.md "Phases" section (canon), CLAUDE.md "Karpathy Procedure" (TDD discipline), CLAUDE.md "Recovery Protocol" (the order of operations any future Claude follows when starting).
>
> **Not negotiable without explicit user approval**: the 18 decisions in CLAUDE.md "Phases" section. If a future session wants to renegotiate any of them, surface to the user, do not silently pivot.

---

## Section 1 — Pre-flight (do these before sitting down)

The user (Daniel) needs to have made or gathered each of these before any of the runbook steps below can execute. None requires Claude — these are user-side prep.

### 1.1 — Pick an S3-compatible object storage provider

The decision matters because it affects cost, offline capability, and credentials handling. Light recommendations:

- **Recommended for most: Cloudflare R2.** No egress fees (the killer feature for a POC where you'll re-download fixtures during testing), cheap storage (~$0.015/GB/month), S3-compatible API, runs on Cloudflare's edge. Sign-up requires a credit card but is genuinely free at POC scale.
- **Strong self-hosted option: MinIO.** Completely free, runs locally via Docker (`docker run -p 9000:9000 minio/minio server /data`). Keeps Phase 2 fully offline-capable. Matches the Phase 1 "no network required" ethos. Trade-off: you have to keep the Docker container running.
- **Workable: Backblaze B2.** Cheapest paid option ($0.005/GB/month). S3-compatible. Some egress allowance free, then $0.01/GB after. Good middle ground if you don't want to self-host but R2 doesn't fit.
- **Avoid for POC: real AWS S3.** Egress fees ($0.09/GB) add up surprisingly fast even at small scale, especially during experimentation when you'll download fixtures repeatedly.

**Final choice goes in `huckleberry/backend/.env.example`.** Real credentials live in `.env` which is gitignored. The decision can be revisited for production later — this is a POC choice.

### 1.2 — Gather the 15 bidsets

You said you have them in a folder. Confirm:
- 15 PDFs, all real-world commercial roofing bidsets (not synthetic)
- Reasonable diversity: different architects, different STACK/UniDoc producers, different scales, different page counts
- Each one named meaningfully (`chipotle-margate-2024.pdf` not `IMG_0042.pdf`)
- Total size noted (probably 200 MB – 2 GB total)

**Why 15 specifically**: it's the threshold where the inclusion rule (≥3-of-15 AND downstream consumer) starts producing useful signal. Fewer than 10, the signal is noisy; more than 20, the experiment runtime balloons. 15 was the user's call.

### 1.3 — Git remote ready to receive the monorepo

Either GitHub, GitLab, or a self-hosted Git server. Empty repo named `huckleberry` (or whatever you prefer — the inside structure is what matters). Have the SSH or HTTPS URL ready.

### 1.4 — PostgreSQL available locally

Three workable paths, pick one:
- **Docker Compose (recommended)**: ships in the monorepo as `docker-compose.yml`, runs `docker compose up postgres` to get a local instance. Makes onboarding trivial and matches what production will look like.
- **Postgres.app (Mac only)**: simplest if you're on a Mac and don't want Docker.
- **apt/brew install postgresql**: native install. Works fine. More setup than Docker but no container.

**The runbook below assumes Docker Compose.** If you pick something else, adapt the connection-string steps.

### 1.5 — Python 3.11+ and a package manager

- Python 3.11 minimum. 3.12 is fine. 3.13 is fine if it's released by the time you read this.
- **Recommended: `uv`** (Astral's package manager). Fast, modern, handles virtualenvs automatically. `pip install uv` then `uv pip install ...`.
- **Workable: `poetry`** if you already use it.
- **Avoid: bare pip + manual venv** for a project this scope. The dependency tree gets non-trivial fast.

### 1.6 — Claude Code installed and configured

Claude Code is the tool that runs the experiment in Section 5. Install per Anthropic's instructions. You'll need filesystem access scoped to the bidset folder (or the manifest, if step 2 has been done first).

---

## Section 2 — Setup task 1: Object storage + bidset upload

This is the first thing that happens after pre-flight. The 15 bidsets need to be in object storage before the experiment can pull from them in production-shaped code paths.

### 2.1 — Provider-specific bucket setup

Pick the subsection matching what you chose in 1.1:

#### Cloudflare R2 setup

```bash
# Sign up at dash.cloudflare.com → R2
# Create a bucket: huckleberry-fixtures
# Generate API tokens: R2 → Manage API Tokens → Create Token (Object Read & Write)
# Note the tokens — they only show once

# Add to ~/.aws/credentials (R2 uses S3-compatible auth):
[huckleberry-r2]
aws_access_key_id = <your_r2_access_key>
aws_secret_access_key = <your_r2_secret_key>

# Endpoint URL is per-account — it'll look like:
# https://<account_id>.r2.cloudflarestorage.com
```

#### MinIO setup (self-hosted)

```bash
# Run MinIO via Docker:
docker run -d -p 9000:9000 -p 9001:9001 \
  --name huckleberry-minio \
  -e MINIO_ROOT_USER=admin \
  -e MINIO_ROOT_PASSWORD=<choose_a_strong_password> \
  -v ~/minio-data:/data \
  minio/minio server /data --console-address ":9001"

# Access console at http://localhost:9001
# Create a bucket named: huckleberry-fixtures
# Endpoint for code: http://localhost:9000
```

#### Backblaze B2 setup

```bash
# Sign up at backblaze.com → B2 Cloud Storage
# Create a bucket: huckleberry-fixtures (private)
# Application keys → Add a New Application Key, scope to that bucket
# Note keyID and applicationKey

# Endpoint will look like: https://s3.us-west-002.backblazeb2.com
# (region will vary based on bucket location)
```

### 2.2 — Manifest schema

The manifest is what the repo carries. Each entry references one bidset in object storage by key + content hash. **Repo never carries the PDFs themselves.**

`huckleberry/backend/test_fixtures/bidsets.json`:

```json
{
  "schema_version": "0.1",
  "manifest_generated_at": "2026-04-25T12:00:00Z",
  "storage": {
    "provider": "cloudflare-r2",
    "bucket": "huckleberry-fixtures",
    "endpoint_url": "https://<account_id>.r2.cloudflarestorage.com"
  },
  "bidsets": [
    {
      "id": "chipotle-margate-2024",
      "s3_key": "fixtures/chipotle-margate-2024.pdf",
      "sha256": "0a1b2c3d4e5f...",
      "size_bytes": 12345678,
      "page_count": 35,
      "producer_hint": "STACK Construction Technologies",
      "notes": "STACK/UniDoc — known hard case from prior sessions",
      "uploaded_at": "2026-04-25T12:01:00Z"
    },
    {
      "id": "panda-express-margate",
      "s3_key": "fixtures/panda-express-margate.pdf",
      "sha256": "...",
      "size_bytes": 0,
      "page_count": 0,
      "producer_hint": "unknown",
      "notes": "",
      "uploaded_at": "2026-04-25T12:02:00Z"
    }
    // ... 13 more
  ]
}
```

**Field semantics:**
- `id`: unique slug per bidset, used everywhere downstream
- `s3_key`: object storage key (the path inside the bucket)
- `sha256`: content hash for integrity verification — catches silent re-upload errors
- `size_bytes` and `page_count`: metadata for the findings report; populated by the upload script
- `producer_hint`: best-guess of who produced the PDF (STACK, manual, AutoCAD-export, etc.) — populated heuristically by the upload script, manually corrected if wrong
- `notes`: any human-readable context the user wants attached

### 2.3 — Upload script

`huckleberry/backend/scripts/upload_fixtures.py` — a one-time-ish script that:
1. Reads PDFs from a local folder (path passed via `--source`)
2. For each PDF: computes sha256, gets size_bytes, opens with pdf.js or pdfplumber to get page_count, attempts producer detection from PDF metadata
3. Uploads to S3-compatible storage using credentials from `.env`
4. Generates / updates `bidsets.json`
5. Verifies every entry in `bidsets.json` is reachable via a HEAD request

Skeleton (this is illustrative; Claude Code can flesh out details):

```python
# huckleberry/backend/scripts/upload_fixtures.py
import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import boto3
import pdfplumber
from botocore.config import Config

MANIFEST_PATH = Path(__file__).parent.parent / "test_fixtures" / "bidsets.json"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="Local folder with the 15 PDFs")
    parser.add_argument("--bucket", default="huckleberry-fixtures")
    parser.add_argument("--endpoint", required=True, help="S3-compatible endpoint URL")
    args = parser.parse_args()

    s3 = boto3.client(
        "s3",
        endpoint_url=args.endpoint,
        config=Config(signature_version="s3v4"),
    )

    bidsets = []
    for pdf_path in sorted(Path(args.source).glob("*.pdf")):
        sha = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
        size = pdf_path.stat().st_size
        with pdfplumber.open(pdf_path) as p:
            pages = len(p.pages)
        s3_key = f"fixtures/{pdf_path.name}"
        s3.upload_file(str(pdf_path), args.bucket, s3_key)
        bidsets.append({
            "id": pdf_path.stem,
            "s3_key": s3_key,
            "sha256": sha,
            "size_bytes": size,
            "page_count": pages,
            "producer_hint": "unknown",  # filled in by hand or by future heuristic
            "notes": "",
            "uploaded_at": datetime.now(timezone.utc).isoformat(),
        })
        print(f"✓ {pdf_path.name} ({size} bytes, {pages} pages)")

    manifest = {
        "schema_version": "0.1",
        "manifest_generated_at": datetime.now(timezone.utc).isoformat(),
        "storage": {
            "provider": "cloudflare-r2",  # adjust per choice
            "bucket": args.bucket,
            "endpoint_url": args.endpoint,
        },
        "bidsets": bidsets,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2))
    print(f"\nManifest written: {MANIFEST_PATH} ({len(bidsets)} bidsets)")

if __name__ == "__main__":
    main()
```

Run as:
```bash
cd huckleberry/backend
uv run python scripts/upload_fixtures.py \
  --source ~/Documents/bidsets \
  --bucket huckleberry-fixtures \
  --endpoint https://<account_id>.r2.cloudflarestorage.com
```

### 2.4 — Verification

`huckleberry/backend/scripts/verify_fixtures.py` reads the manifest, HEAD-requests each S3 key, confirms size and (optionally) hash. Run after upload:

```bash
uv run python scripts/verify_fixtures.py
# Expected: ✓ 15/15 bidsets reachable, 15/15 hashes match
```

---

## Section 3 — Setup task 2: Monorepo skeleton

### 3.1 — Directory structure

```
huckleberry/
├── README.md                          # Repo-level overview, links to CLAUDE.md
├── CLAUDE.md                          # The architectural canon (move from current location)
├── PHASE_2_HANDOFF.md                 # This file
├── .gitignore
├── .env.example                       # template — never commit real .env
├── docker-compose.yml                 # local Postgres + optional MinIO
│
├── frontend/                          # Phase 1 lives here, intact
│   ├── Huckleberry_AI_6.3.5_Scope.html
│   ├── Huckleberry_AI_6.3.4_Scope.html  # prior versions kept for regression testing
│   ├── Huckleberry_AI_6.3.3_Scope.html
│   ├── Huckleberry_AI_6.3.2_Scope.html
│   ├── Huckleberry_AI_6.3.1_Scope.html
│   ├── extracted/Huckleberry_AI_6.3.0_Scope.html
│   ├── run_tests.js                   # the jsdom harness
│   ├── package.json
│   ├── spotcheck_*.js
│   └── mutation_test_step11.js
│
├── backend/
│   ├── pyproject.toml
│   ├── pytest.ini
│   ├── README.md                      # backend-specific dev notes
│   ├── app/
│   │   └── __init__.py                # empty for now — Phase 2 v0.2 fills this
│   ├── scripts/
│   │   ├── upload_fixtures.py
│   │   └── verify_fixtures.py
│   ├── seeds/                         # the four reference data files live here
│   │   ├── __init__.py
│   │   ├── dispatch_seed.py
│   │   ├── roofing_seed.py
│   │   ├── glazing_seed.py            # note: rename from glazingseed.py for consistency
│   │   ├── material_matrix_seed.py
│   │   └── roofing_materials.py       # already on disk; goes here
│   ├── test_fixtures/
│   │   ├── bidsets.json               # the manifest
│   │   └── experiment_outputs/        # populated by Claude Code's experiment
│   │       └── .gitkeep
│   └── tests/
│       ├── __init__.py
│       └── test_seeds_load.py         # smoke test: every seed file imports cleanly
│
└── shared/
    ├── __init__.py
    └── bidset_record.py               # placeholder — the experiment fills this in
```

### 3.2 — File stubs to create

`huckleberry/README.md`:
```markdown
# Huckleberry AI

Commercial roofing takeoff application.

- **frontend/** — Phase 1: single-file HTML viewer + manual takeoff toolchain. Runs offline in Chrome. Currently at v6.3.5, 138/138 tests green.
- **backend/** — Phase 2: Python service for PDF intake, data analysis, persistence. FastAPI + SQLAlchemy + Postgres + Pydantic. Localhost-only during POC.
- **shared/** — The wrapper schema: Pydantic models that define the contract between frontend and backend.

See `CLAUDE.md` for full architectural canon and the Phase 1 → Phase 2 handoff.
See `PHASE_2_HANDOFF.md` for the v0.1 experiment runbook.
```

`huckleberry/.gitignore`:
```
# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
.uv/
*.egg-info/

# Node
node_modules/

# Env / secrets
.env
*.env.local
~/.aws/credentials.huckleberry

# Docker volumes
postgres-data/
minio-data/

# Editor
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Experiment outputs that don't belong in git
backend/test_fixtures/experiment_outputs/*.json
!backend/test_fixtures/experiment_outputs/.gitkeep
```

`huckleberry/.env.example`:
```bash
# Object storage (S3-compatible)
S3_PROVIDER=cloudflare-r2  # or: minio | backblaze-b2 | aws-s3
S3_ENDPOINT_URL=https://<account_id>.r2.cloudflarestorage.com
S3_BUCKET=huckleberry-fixtures
S3_ACCESS_KEY_ID=<your_access_key>
S3_SECRET_ACCESS_KEY=<your_secret_key>

# PostgreSQL
DATABASE_URL=postgresql+asyncpg://huckleberry:huckleberry@localhost:5432/huckleberry

# App
APP_ENV=development
LOG_LEVEL=info
```

`huckleberry/docker-compose.yml`:
```yaml
version: "3.9"
services:
  postgres:
    image: postgres:16
    container_name: huckleberry-postgres
    environment:
      POSTGRES_USER: huckleberry
      POSTGRES_PASSWORD: huckleberry
      POSTGRES_DB: huckleberry
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data

  # Optional — only if you chose MinIO in 1.1
  minio:
    image: minio/minio
    container_name: huckleberry-minio
    profiles: ["with-minio"]
    environment:
      MINIO_ROOT_USER: admin
      MINIO_ROOT_PASSWORD: minio-dev-password-change-me
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio-data:/data
    command: server /data --console-address ":9001"

volumes:
  postgres-data:
  minio-data:
```

### 3.3 — Move v6.3.5 + ancillaries into `frontend/`

```bash
# Assuming you're at the new monorepo root
mkdir -p frontend
cp /path/to/current/Huckleberry_AI_6.3.*_Scope.html frontend/
cp /path/to/current/run_tests.js frontend/
cp /path/to/current/spotcheck_*.js frontend/
cp /path/to/current/mutation_test_step11.js frontend/
cp /path/to/current/package.json frontend/  # if exists
mkdir -p frontend/extracted
cp /path/to/current/extracted/Huckleberry_AI_6.3.0_Scope.html frontend/extracted/
```

**Verification** — Phase 1 still works after the move:
```bash
cd frontend
node run_tests.js Huckleberry_AI_6.3.5_Scope.html
# Expected: 138/138 passed, 0 failed
```

This is non-negotiable. If Phase 1 doesn't pass after the move, fix the move. Don't proceed to Section 4 until Phase 1 is green in its new location.

### 3.4 — First commit

```bash
cd huckleberry
git init
git add .
git commit -m "Phase 2 monorepo skeleton; Phase 1 (v6.3.5) preserved in frontend/"
git remote add origin <your-remote-url>
git push -u origin main
```

---

## Section 4 — Setup task 3: Backend bootstrap (minimal, just enough to run the experiment)

The full backend doesn't get built in v0.1 — that's v0.2. But we need just enough Python infrastructure for Claude Code to run the experiment.

### 4.1 — `backend/pyproject.toml`

```toml
[project]
name = "huckleberry-backend"
version = "0.1.0"
description = "Huckleberry AI Phase 2 backend"
requires-python = ">=3.11"
dependencies = [
    # Web framework — included now so v0.2 doesn't need to re-add
    "fastapi>=0.115",
    "uvicorn[standard]>=0.32",
    # DB
    "sqlalchemy>=2.0",
    "asyncpg>=0.30",
    "alembic>=1.13",
    # Pydantic for the wrapper schema
    "pydantic>=2.9",
    "pydantic-settings>=2.6",
    # Object storage
    "boto3>=1.35",
    # PDF — pdfplumber is the experiment's starting library; others may be added based on findings
    "pdfplumber>=0.11",
    "pypdfium2>=4.30",  # optional — useful as a comparison renderer during experimentation
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3",
    "pytest-asyncio>=0.24",
    "ruff>=0.7",
    "mypy>=1.13",
]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

### 4.2 — Initial Pydantic stub for the wrapper schema

`huckleberry/shared/bidset_record.py`:

```python
"""
Wrapper schema for BidsetRecord — the JSON contract between Huckleberry's
frontend (Phase 1, single-file HTML) and backend (Phase 2, FastAPI + Postgres).

THIS FILE IS A STUB. The Phase 2 v0.1 experiment is what fleshes it out, by
running 15 real bidsets through pdfplumber and observing what fields actually
appear with frequency >= 3 AND a downstream consumer.

The only field locked-in BEFORE the experiment is `schema_version`.
Every other field below is a tentative placeholder that the experiment will
either confirm, reshape, or replace.

DO NOT add fields to this schema speculatively. Add them only when the
experiment's findings report demonstrates they meet the inclusion rule:
  - Field appears in >= 3 of 15 bidsets, AND
  - Field has an identifiable downstream consumer
"""

from typing import Any
from pydantic import BaseModel, Field


class BidsetRecord(BaseModel):
    """The top-level record produced by Phase 2 backend, consumed by Phase 1 frontend."""

    schema_version: str = Field(
        ...,
        description=(
            "Schema version string. Incremented on every breaking change. "
            "Backend handles version mismatches at read time (upgrade-on-read or mark-stale)."
        ),
    )

    id: str = Field(..., description="Unique bidset identifier; matches manifest entry id.")

    source_pdf_ref: dict[str, Any] = Field(
        ...,
        description=(
            "Reference to the source PDF in object storage. "
            "Shape TBD by experiment — likely {s3_key, sha256, size_bytes, page_count}."
        ),
    )

    pages: list[dict[str, Any]] = Field(
        default_factory=list,
        description=(
            "Per-page extracted data. Shape TBD by experiment. "
            "Likely zones, extracted text, paths, scale candidates, classification."
        ),
    )

    scope: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Parsed scope: systems, manufacturers, attachments, materials. "
            "Shape TBD by experiment, will likely echo Phase 1's ROOF_VOCAB structure."
        ),
    )

    annotations: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "User-drawn annotations: pins, line segments, polygons. "
            "Frontend writes; backend stores. Round-trips via the Save flow. "
            "Shape mirrors Phase 1's annotation model (areas[], pins[], lineSegments[])."
        ),
    )

    provenance: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Audit trail of what the parser said vs what the user changed. "
            "On save, frontend wins (user is right) and provenance records the "
            "delta. Becomes labeled training data for Phase 3 ML work."
        ),
    )

    class Config:
        json_schema_extra = {
            "example": {
                "schema_version": "0.1",
                "id": "chipotle-margate-2024",
                "source_pdf_ref": {
                    "s3_key": "fixtures/chipotle-margate-2024.pdf",
                    "sha256": "0a1b...",
                    "size_bytes": 12345678,
                    "page_count": 35,
                },
                "pages": [],
                "scope": {},
                "annotations": {},
                "provenance": {},
            }
        }
```

### 4.3 — Smoke test: every seed file imports cleanly

`huckleberry/backend/tests/test_seeds_load.py`:

```python
"""Smoke test: every reference-data seed file imports without error and
exposes its expected top-level dict(s). This is the cheapest possible
guard against the seed files silently breaking."""

import pytest


def test_roofing_materials_loads():
    from seeds.roofing_materials import SPEC_SECTIONS, MANUFACTURERS, MATERIAL_PROPERTIES
    assert isinstance(SPEC_SECTIONS, dict) and len(SPEC_SECTIONS) > 0
    assert isinstance(MANUFACTURERS, dict) and len(MANUFACTURERS) > 0
    assert "Duro-Last" in MANUFACTURERS  # regression: Phase 1 added this in Step 9.x


def test_dispatch_seed_loads():
    """Will skip if dispatch_seed.py isn't yet at the expected path.
    Once that file is in place, this test enforces it imports cleanly."""
    pytest.importorskip("seeds.dispatch_seed")


def test_roofing_seed_loads():
    pytest.importorskip("seeds.roofing_seed")


def test_glazing_seed_loads():
    pytest.importorskip("seeds.glazing_seed")


def test_material_matrix_seed_loads():
    pytest.importorskip("seeds.material_matrix_seed")
```

`pytest.importorskip` is intentional: not all four seeds may be on disk yet at the time of the v0.1 experiment. The test passes if the file is missing (skipped) or if it imports cleanly. It fails only if the file exists but has a Python error in it.

### 4.4 — Bootstrap verification

```bash
cd huckleberry/backend
uv venv
uv pip install -e ".[dev]"
docker compose up -d postgres  # from monorepo root
psql postgresql://huckleberry:huckleberry@localhost:5432/huckleberry -c "SELECT 1"
# Expected: ?column? \n ---------- \n 1

uv run pytest tests/test_seeds_load.py -v
# Expected: 1 pass, 4 skip (or 5 pass if all four seeds are on disk)

uv run python scripts/verify_fixtures.py
# Expected: ✓ 15/15 bidsets reachable
```

If all three commands pass, infrastructure is ready for the experiment.

---

## Section 5 — The experiment prompt for Claude Code (verbatim)

Open Claude Code in a session scoped to the `huckleberry/` monorepo. Give it the prompt below verbatim. **Do not paraphrase. The exact wording is load-bearing — it locks in the experiment's discipline against scope creep.**

The prompt has been updated since the original Phase 2 plan was drafted: the four seed files (`dispatch_seed.py`, `roofing_materials.py`, `roof_assemblies.py`, `glazing_materials.py`, `glazing_assemblies.py`) now exist on disk in `backend/seeds/`. They form a four-layer reference architecture — see `backend/seeds/README.md`. The experiment now has concrete targets to measure against, including the documented baseline that **52 of 60 roof pages fell back to universal items** in a prior diagnostic. Improving (or honestly accepting) that baseline is part of the experiment's measurable success criterion.

> ---
>
> You are running the Phase 2 v0.1 experiment for Huckleberry AI. Read `CLAUDE.md` and `PHASE_2_HANDOFF.md` in full before doing anything else. Then read `backend/seeds/README.md` and skim each of the five seed files to understand the four-layer reference architecture (dispatch / materials / assemblies). The "Phases" section in CLAUDE.md is canon — do not negotiate against the 18 architectural decisions documented there.
>
> **Your goal**: produce three deliverables from running 15 real-world commercial roofing bidsets through a layered extraction pipeline that uses the seed files in `backend/seeds/`. The output is evidence-driven schema design, not a backend.
>
> **You are NOT building**:
>   - A FastAPI backend (no routes, no DB models, no migrations)
>   - A tool stack recommendation (don't pick libraries beyond what's already in `backend/pyproject.toml`)
>   - LLM / ML / vision-model integration (Phase 3, refused for Phase 2)
>   - A glazing pipeline (glazing seeds are skeletons per their author; glazing is out of v0.1 scope — only roofing-relevant pages of the 15 bidsets are in scope)
>
> **You ARE building**: an evidence-driven draft of the BidsetRecord wrapper schema, plus the findings that justify its shape.
>
> **Deliverables (all three required, none optional)**:
>
> 1. **Per-PDF JSON output** — one file per bidset, written to `backend/test_fixtures/experiment_outputs/<bidset_id>.json`. Each file contains everything you observed about that bidset, organized by:
>    - `dispatch` — Layer 1 output: page classifications, sheet map, cross-references, legend regions, project metadata (DETERMINISTIC fields only — leave the LLM-only fields as null per `dispatch_seed.PROJECT_METADATA_LLM_ONLY`)
>    - `scope` — Layer 2 output: identified roofing systems with manufacturer / attachment / spec section, source page(s), confidence (using `dispatch_seed.CONFIDENCE` levels)
>    - `assembly` — Layer 3 output: per identified system, the components-list and any triggered relationship warnings
>    - `provenance` — for every populated field, what extraction method produced it and where in the PDF it came from (page index, text-block coords, regex pattern, etc.)
>    - `extraction_metrics` — pages processed, classification confidence histogram, fields that were null because the data wasn't present, fields that were null because the extractor failed
>    Use whatever per-bidset shape feels natural inside each section; the goal is observation, not yet schema. The schema design comes after, from looking at the 15 outputs together.
>
> 2. **Draft Pydantic schema** — replaces the stub at `shared/bidset_record.py`. Built from observation, not guess. Apply the inclusion rule strictly:
>    - A field is in the schema if and only if it appears in **>= 3 of 15 bidsets** AND has an **identifiable downstream consumer** (a real or near-future user-facing capability that consumes it). Both conditions required.
>    - Fields that fail one or both conditions go in the deferred/observed appendix in the findings report, NOT in the schema.
>    - Every field in the schema must have a docstring justifying its inclusion: which bidsets had it, what consumes it.
>    - Top-level shape is layer-aligned: `id`, `schema_version`, `source_pdf_ref`, `dispatch`, `scope`, `assembly`, `annotations`, `provenance`. The stub already shows this — your job is to replace each layer's `dict[str, Any]` with concrete nested Pydantic models.
>
> 3. **Findings report** — `backend/EXPERIMENT_FINDINGS.md`. Markdown. Required sections:
>
>    - **Coverage matrix**: table with 15 rows (one per bidset) and N columns (one per observed field), marking which bidsets had which fields. The audit trail for the inclusion rule.
>
>    - **Dispatch layer accuracy**: how the four-layer pipeline performed against `dispatch_seed.py`'s patterns. Specifically measure against the **52 of 60 roof pages → universal fallback** baseline mentioned in `dispatch_seed.py`'s docstring — did the keyword lists in `PAGE_CLASSIFICATION_KEYWORDS` correctly classify roof pages on these 15 bidsets, or did they fall back? Report the new ratio (e.g., "44 of 53 roof pages classified correctly; 9 fell back"). If accuracy is worse than baseline, document why; if better, document what improved.
>
>    - **Scope layer accuracy**: for each bidset, how many systems were identified, with what confidence, and what manufacturer/spec-section data was attached. Note bidsets where scope was identified at the wrong level (e.g., "saw 'TPO' generically but missed the specific Carlisle product spec'd in the schedule").
>
>    - **Assembly layer accuracy**: for the systems that were identified, how many components from the matching `roof_assemblies.ROOF_SYSTEMS[*].required_components` could be supported by extracted text vs flagged as "expected but not found"? How many `ASSEMBLY_RELATIONSHIPS` warnings would have triggered if the user had drawn pins matching what's visible on the plans?
>
>    - **Promoted fields**: list of fields that made it into the schema. For each: count of bidsets in which it appeared, identified downstream consumer, short rationale.
>
>    - **Deferred / observed appendix**: fields that were observed but didn't meet the inclusion rule. For each: count, missing condition (frequency or consumer or both), notes on why it might still matter someday.
>
>    - **Surprises**: bullet list of things the experiment revealed that weren't predicted before looking at the data. This section is important — it's the signal that says "the experiment was actually useful." Examples of what counts as a surprise: "the title block was on the first page in 5 PDFs but on every page in 8" or "STACK-produced PDFs strip scale labels but preserve them in a hidden text layer." Examples of what doesn't count: "PDFs are sometimes large." Be specific.
>
>    - **Tooling notes**: which tools you used (start with pdfplumber per `pyproject.toml`; add others ONLY as specific failures justify, and document each addition with the failure that motivated it). Per-bidset success/failure record for each tool.
>
>    - **Recommended next experiments**: things you couldn't answer in v0.1 but that v0.2 should look into. Examples: "the dispatch keyword list misses architect-specific notation X — recommend expanding patterns" or "Sika Sarnafil's specs format differs enough from Carlisle that scope parser needs a per-manufacturer hook."
>
> **The discipline**:
>
> - **The four-layer architecture is canon.** Use the seeds. Don't reinvent classification or vocab — `dispatch_seed.py`'s patterns ARE the classification system, `roofing_materials.py`'s `MANUFACTURERS` and `SPEC_SECTIONS` ARE the vocab, `roof_assemblies.py`'s `ROOF_SYSTEMS` ARE the takeoff drivers. If a pattern fails, document the failure in tooling notes and recommended next experiments — DO NOT silently rewrite the seed file. Seed edits are a separate, explicit decision that goes through user review.
>
> - **Glazing is out of scope.** Pages classified as glazing-relevant get noted but not deeply parsed. The glazing seed files are skeletons per their authors and need an estimator's review before they're trustworthy. v0.1 produces no glazing observations beyond "this page references glazing."
>
> - **Don't pick a tool stack.** The experiment's output is a schema, not a stack recommendation. Tool picks happen after the schema is reviewed and the next milestone is planned. If pdfplumber fails on certain bidsets, document the failure mode in the findings report; do not pivot to Docling or Camelot mid-experiment unless pdfplumber is so broken that no useful output is being produced. If you do pivot, document why explicitly in tooling notes.
>
> - **Don't write a backend.** No FastAPI app. No SQLAlchemy models. No HTTP endpoints. The backend is v0.2, planned after the schema is reviewed. Your work is in `backend/scripts/` (extraction), `shared/bidset_record.py` (schema replacement), and `backend/EXPERIMENT_FINDINGS.md` (the report). Stay there.
>
> - **Use the inclusion rule honestly.** If only 2 bidsets have a field, it's deferred, not promoted. If a field is in 12 bidsets but you can't articulate a downstream consumer, it's deferred. Both criteria, every field, no shortcuts.
>
> - **Provenance is not optional, even at v0.1.** Every promoted field should have a provenance shape — what extraction step produced it, what page, what confidence. Phase 2's whole reason for capturing provenance is Phase 3 training data (Decision #6). Drop provenance now and you've corrupted the dataset for Phase 3.
>
> **Process**:
>
> 1. Read `CLAUDE.md` (especially "Phases" section), `PHASE_2_HANDOFF.md` (this doc), `shared/bidset_record.py` (the stub you're replacing), `backend/seeds/README.md`, and skim each of the five seed files.
>
> 2. Verify bootstrap: `cd backend && pytest tests/test_seeds_load.py` (expected: 7 passed). Then `python scripts/verify_fixtures.py` (expected: 15/15 reachable). Don't proceed if either fails.
>
> 3. Read the bidset manifest at `backend/test_fixtures/bidsets.json`. For each bidset:
>    - Download from S3
>    - Apply Layer 1 (dispatch filters) using `dispatch_seed.py` patterns
>    - On classified pages, apply Layer 2 (scope parsing) using `roofing_materials.py`
>    - For identified systems, apply Layer 3 (assembly mapping) using `roof_assemblies.py`
>    - Record everything in the per-PDF JSON, including failures and confidence
>    - Build the per-PDF JSON incrementally so partial progress survives session interruption
>
> 4. After all 15 are processed, build the coverage matrix from the 15 JSONs.
>
> 5. Apply the inclusion rule (≥3 of 15 AND downstream consumer). Promote fields. Defer fields.
>
> 6. Write the draft Pydantic schema in `shared/bidset_record.py`. Every promoted field must have a docstring justifying inclusion (which bidsets, what consumer). Replace the stub's `dict[str, Any]` placeholders with concrete nested models.
>
> 7. Write the findings report `backend/EXPERIMENT_FINDINGS.md`. All eight required sections.
>
> 8. Commit your work in `huckleberry/` with a descriptive message. Do not push (the user will review first).
>
> 9. Stop. Do not write a backend. Do not propose v0.2 architecture beyond the "recommended next experiments" section. Do not pick tool stacks. The next step after the experiment is the user's review checkpoint, not your code.
>
> **What "done" looks like**:
>
> - 15 JSON files in `backend/test_fixtures/experiment_outputs/`
> - `shared/bidset_record.py` updated from stub to draft schema
> - `backend/EXPERIMENT_FINDINGS.md` exists with all eight required sections
> - Coverage matrix has 15 rows
> - Dispatch layer accuracy is reported as a ratio against the 52/60 baseline
> - Every promoted field has a docstring with bidset count + downstream consumer
> - Deferred appendix has every observed-but-not-promoted field
> - Surprises section is non-empty and specific
> - You have not added a single FastAPI route, SQLAlchemy model, or HTTP endpoint
> - Glazing pages are noted but not deeply parsed
>
> Begin.
>
> ---

That ends the verbatim prompt. **The prompt is also saved to `huckleberry/backend/EXPERIMENT_PROMPT.md`** as a permanent record. If a future run wants to re-run the experiment with new bidsets, use the same prompt for consistency.

---

## Section 6 — Review checkpoint (after Claude Code finishes the experiment)

Once Claude Code has done its work, the user (Daniel) reviews the deliverables BEFORE any v0.2 backend work begins.

### 6.1 — What to review

In order:

1. **The 15 per-PDF JSONs.** Skim a few. Do they make sense? Did pdfplumber actually extract usable text + structure, or is it all unintelligible? If the JSONs are all empty or garbage, the experiment failed and needs to retry with a different starting tool.

2. **The findings report's coverage matrix.** Is the matrix legible? Can you read down the rows and see which fields appeared in which bidsets? Are there obvious patterns (e.g. "every STACK PDF lacks scale labels" or "all 15 have title blocks but only 4 in the same screen position")?

3. **The promoted-fields list.** For each promoted field, ask:
   - Does the bidset count match what the matrix shows? (Sanity check.)
   - Is the downstream consumer specific and real, or is it vague?
   - Would I, as a roofing estimator, want to see this field in a takeoff workflow?

4. **The deferred-fields list.** Anything in here that should have been promoted but wasn't? Anything you'd want to lower the threshold to capture? (Note: this is where the rule can be revisited — you can decide to lower from ≥3 to ≥2 if the inclusion rule was too strict, or raise to ≥5 if it was too lenient. But change the rule explicitly, not silently.)

5. **The surprises section.** This is the signal that the experiment was useful. If surprises is empty or trivial ("PDFs are sometimes large"), the experiment was probably superficial. Real surprises sound like "the title block was on the first page in 5 PDFs but on every page in 8 — we'll need a per-page detection pass, not a once-per-bidset pass."

6. **The draft schema.** Does it pass the smell test? Is it small enough to be reviewable in one sitting (~100-200 lines), or has it bloated to 800 lines? If bloated, that suggests the inclusion rule wasn't applied honestly.

### 6.2 — Decisions to make at the checkpoint

- **Does v0.1 schema graduate to v0.1 final?** If yes, tag it. If not, what changes?
- **Which deferred fields graduate before v0.2 starts?** None is fine. Some is fine. Be explicit.
- **What's the next milestone (v0.2)?** Most likely: build the minimal backend that produces a BidsetRecord from a PDF and stores it in Postgres. But that gets its own handoff doc, not added here.
- **Did the experiment reveal that pdfplumber alone is insufficient?** If yes, what's the next tool to add? (Documented in `EXPERIMENT_FINDINGS.md` → Tooling notes.)

### 6.3 — Output of the checkpoint

A short markdown file — `huckleberry/backend/V0_1_REVIEW.md` — capturing:
- Date of review
- Decisions made
- Fields graduated post-experiment
- Next milestone definition
- Pointer to the v0.2 handoff doc (which will be written next)

---

## Section 7 — What this handoff doc DOESN'T cover (explicit deferrals)

Each item below is intentionally not in this document. If a future Claude proposes any of them inside a v0.1 session, push back: this is v0.1, not v0.2+.

- **Backend architecture beyond the scripts directory.** No FastAPI routes, no DB models, no migrations. v0.2's handoff doc.
- **Frontend ↔ backend wiring.** The HTML doesn't yet talk to the backend. v0.3's handoff doc.
- **Real production stack picks.** Whether to add Docling, Camelot, Apryse, vision models — all decisions made AFTER the experiment, with experiment evidence in hand.
- **Authentication, sessions, multi-user.** Phase 3.
- **LLM / ML integration.** Phase 3.
- **Network exposure beyond localhost.** Phase 3.
- **Migrations infrastructure.** Schema versioning is in place; migration scripts come when actually needed.
- **Production deployment.** POC scale only. No Kubernetes, no CDN, no nothing yet.
- **CI/CD.** Local pytest + pre-commit hooks are sufficient until v0.2 ships.
- **Monitoring, logging beyond stdout.** v0.3+ when there's something to monitor.

---

## Section 8 — Honest flags / known unknowns

1. **The S3 provider choice has cost implications we haven't priced.** R2 looks free at POC scale but pricing changes; verify with current Cloudflare docs before committing real bidsets long-term.

2. **pdfplumber may not be the right starting library.** It's the experiment's starting choice because it's a well-maintained, coordinate-aware Python PDF library. If the 15 bidsets reveal it fails on STACK/UniDoc producers, the experiment will document that and v0.2 will pivot.

3. **15 bidsets assumes representative coverage.** If all 15 happen to be Florida fast-food remodels, the schema will overfit. Diversity matters more than count. If diversity is low, raise the inclusion threshold (≥4 of 15, or even ≥5) to compensate.

4. **The experiment may produce an unworkable schema.** Possibilities: too many fields (inclusion rule was applied too leniently), too few common patterns (inclusion rule too strict, or bidsets too diverse), or the schema feels right but the per-PDF JSONs reveal pdfplumber missed crucial information. Fallback plan is at the review checkpoint — adjust the rule, change tools, or split into multiple bidset profile types.

5. **Future Claude may silently re-architect against the 18 decisions.** This is the largest risk for the project's coherence. Mitigation = the canon clause in CLAUDE.md ("the 18 decisions are canon, do not negotiate without explicit user approval") + the verbatim experiment prompt above + this honest flag itself.

6. **The seed files (`dispatch_seed.py`, `roofing_seed.py`, `glazing_seed.py`, `material_matrix_seed.py`) may not all exist on disk yet.** The smoke test in `test_seeds_load.py` skips missing files; doesn't fail. As they land, they get tested. If a seed file lands later that contradicts the schema produced by the experiment, the schema needs revision — flag that as a v0.2 task.

7. **`roofing_materials.py` already exists and `dispatch_seed.py` is referenced in CLAUDE.md but I have not seen it.** If at experiment time `dispatch_seed.py` is on disk and contradicts assumptions in the experiment, the experiment's findings should call it out.

8. **The "≥3 of 15 AND downstream consumer" rule is itself untested.** It's a heuristic. If the experiment review checkpoint reveals it produced a bad schema, the rule changes — explicitly, with rationale, captured in `V0_1_REVIEW.md`.

9. **Phase 2's offline-capable property requires localhost-only deployment.** If you're tempted to put the backend on a hosted service even for development, that's a Phase 3 boundary crossing. Keep it local during Phase 2.

---

## Section 9 — Success metric for v0.1

Phase 2 v0.1's success has one criterion only: **the four deliverables exist and pass review.**

The four deliverables:
1. 15 per-PDF JSON files in `huckleberry/backend/test_fixtures/experiment_outputs/`
2. Draft Pydantic schema at `huckleberry/shared/bidset_record.py`
3. Findings report at `huckleberry/backend/EXPERIMENT_FINDINGS.md` with all five required sections (coverage matrix, promoted, deferred, surprises, tooling notes)
4. `V0_1_REVIEW.md` written by the user post-checkpoint

That's it. v0.1 is not the backend. v0.1 is not user-facing. v0.1 is not a PDF round-trip. v0.1 is **evidence-driven schema design**.

Later milestones (v0.2 backend MVP, v0.3 frontend integration, v0.x Phase 2 closed with 100+ bidsets in DB) get their own success metrics and their own handoff docs. Don't enumerate them here. **Each milestone earns its own runbook when it becomes the next thing.**

---

## Section 10 — Risks and mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| pdfplumber fails on most STACK/UniDoc PDFs | Medium | High | Documented in `EXPERIMENT_FINDINGS.md` tooling notes; fallback to alternative libraries listed in v0.2 plan |
| Experiment schema has too many fields | Medium | Medium | Inclusion rule strict by design; review checkpoint catches over-inclusion |
| Experiment schema has too few common fields | Low-Medium | High | Lower the inclusion threshold at review checkpoint; document the change |
| 15 bidsets not diverse enough | Medium | Medium | Acknowledge in findings; recommend broader fixture set in v0.2 |
| S3 costs spike unexpectedly | Low | Low | POC scale; R2 has no egress fees; can switch providers without code change |
| Postgres setup blocks experiment | Low | Medium | Docker Compose setup is pre-flight; experiment doesn't actually need DB until v0.2 |
| Future Claude session re-architects against 18 decisions | Medium | High | Canon clause in CLAUDE.md; verbatim prompt above; this honest flag list |
| `dispatch_seed.py` exists with content that contradicts experiment assumptions | Low | Medium | Smoke test skips on missing files; if conflict detected, flag in findings, defer to v0.2 |
| Experiment runs longer than expected (hours, not minutes) | Medium | Low | It's an experiment — running long is fine. Don't pressure Claude Code to skip steps to finish faster |
| Claude Code session loses context partway through | Medium | Medium | Per-PDF JSONs are written incrementally; experiment is resumable from the JSONs that already exist |

---

## Final Checklist (one-pager — print this, tick off as you go)

### Pre-flight
- [ ] S3-compatible provider chosen (R2 / MinIO / B2 / AWS S3)
- [ ] 15 bidsets gathered in a local folder, named meaningfully
- [ ] Git remote ready to receive `huckleberry` monorepo
- [ ] Postgres available locally (Docker Compose / Postgres.app / native install)
- [ ] Python 3.11+ installed; `uv` (or `poetry`) available
- [ ] Claude Code installed and configured

### Setup task 1 — Object storage
- [ ] Bucket created in chosen provider (`huckleberry-fixtures`)
- [ ] Credentials in `~/.aws/credentials` or `.env` (NOT committed)
- [ ] `upload_fixtures.py` runs without error
- [ ] All 15 bidsets uploaded
- [ ] `bidsets.json` manifest committed to repo
- [ ] `verify_fixtures.py` reports 15/15 reachable

### Setup task 2 — Monorepo
- [ ] Directory structure created (`frontend/`, `backend/`, `shared/`)
- [ ] v6.3.5 + ancillaries moved into `frontend/`
- [ ] **CRITICAL: Phase 1 still passes 138/138 in new location**
- [ ] Stub files created (`README.md`, `.gitignore`, `.env.example`, `docker-compose.yml`)
- [ ] First commit pushed to remote

### Setup task 3 — Backend bootstrap
- [ ] `pyproject.toml` created with dependencies
- [ ] `uv venv && uv pip install -e ".[dev]"` succeeds
- [ ] `docker compose up postgres` succeeds
- [ ] Postgres connection verified with psql
- [ ] `pytest tests/test_seeds_load.py` passes (or skips for missing seeds)
- [ ] `shared/bidset_record.py` stub in place
- [ ] `EXPERIMENT_PROMPT.md` saved verbatim to `backend/`

### The experiment
- [ ] Claude Code session opened, scoped to monorepo
- [ ] Verbatim prompt from Section 5 pasted in
- [ ] Experiment runs to completion
- [ ] 15 JSONs in `experiment_outputs/`
- [ ] Schema updated in `shared/bidset_record.py`
- [ ] Findings report in `EXPERIMENT_FINDINGS.md` with all 5 required sections

### Review checkpoint
- [ ] User reads all 4 deliverables
- [ ] Decisions made about field graduation, threshold tuning, next milestone
- [ ] `V0_1_REVIEW.md` written
- [ ] Phase 2 v0.1 declared complete OR re-run scoped

### Stop here
- [ ] **Do NOT proceed to v0.2 backend work without user approval and a v0.2 handoff doc**

---

*End of `PHASE_2_HANDOFF.md`. The next milestone (v0.2) gets its own handoff doc, written after the v0.1 review checkpoint.*
