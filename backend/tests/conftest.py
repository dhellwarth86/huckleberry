"""Shared pytest fixtures for the backend test suite.

E.1 added the `silverleaf_path` fixture below for the API endpoint tests.
E.2.2 adds `small_pdf_path` — a minimal 1-page PDF for fast dispatch tests.
"""
from __future__ import annotations

from pathlib import Path

import pytest


# Minimal valid PDF (1 blank page, ~200 bytes). Used by dispatch tests so
# they complete in <5s instead of the ~140s a real bidset like Silverleaf takes.
_MINIMAL_PDF = (
    b"%PDF-1.0\n"
    b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
    b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
    b"3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<<>>>>endobj\n"
    b"xref\n0 4\n"
    b"0000000000 65535 f \n"
    b"0000000009 00000 n \n"
    b"0000000058 00000 n \n"
    b"0000000115 00000 n \n"
    b"trailer<</Size 4/Root 1 0 R>>\n"
    b"startxref\n190\n%%EOF\n"
)


@pytest.fixture
def small_pdf_path(tmp_path: Path) -> Path:
    """Write a minimal 1-page PDF to a temp directory and return its path.

    Dispatch on this PDF completes quickly (~1-3s), keeping the test suite
    fast. The PDF has one blank page — dispatch produces empty results, which
    is fine for testing endpoint behavior (status transitions, response shapes).
    """
    pdf = tmp_path / "small_fixture.pdf"
    pdf.write_bytes(_MINIMAL_PDF)
    return pdf


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
