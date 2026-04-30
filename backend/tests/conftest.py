"""Shared pytest fixtures for the backend test suite.

E.1 added the `silverleaf_path` fixture below for the API endpoint tests.
Future fixtures are appended; this file is shared across the whole
`backend/tests/` suite.
"""
from __future__ import annotations

from pathlib import Path

import pytest


# E.1: tests reference Silverleaf via the same path D.2 / D.1 used.
_SILVERLEAF_CANDIDATES = [
    # Primary: workspace-root location (matches d2_silverleaf_reference.py exactly)
    Path(r"C:\huck stage 2\full bid sets\B2607 AEA Silverleaf - St Augustine - Accelerated Construction Services (6).pdf"),
    # Fallback (without the trailing " (6)") in case a future copy drops the suffix
    Path(r"C:\huck stage 2\full bid sets\B2607 AEA Silverleaf - St Augustine - Accelerated Construction Services.pdf"),
]


@pytest.fixture
def silverleaf_path() -> Path:
    """Return a Path to the Silverleaf bidset PDF, or skip if unavailable.

    Used by E.1 API tests (test_api_jobs.py) and the E.1 hard gate harness.
    Skips rather than fails so the suite passes on machines without the
    real bidset (CI / fresh clone) without flagging as a regression.
    """
    for p in _SILVERLEAF_CANDIDATES:
        if p.exists():
            return p
    pytest.skip("Silverleaf bidset PDF not found; skipping tests that need a real PDF")
