"""Huckleberry API package — E.1.

FastAPI surface over the D.2 persistence layer (`core.job_storage`).
Phase E.1 ships two real endpoints (POST /jobs + GET /jobs/{id}) plus
an exempt /health probe. See backend/E0_API_DESIGN.md for the contract.
"""
