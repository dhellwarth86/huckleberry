"""Wrapper schema package — the JSON contract between Huckleberry's frontend
(Phase 1, single-file HTML) and backend (Phase 2, FastAPI + Postgres).

The Pydantic models in this package are simultaneously:
  - The DB row shape (via SQLAlchemy hybrid)
  - The API response shape (FastAPI)
  - The frontend payload shape (consumed by HTML)

One source of truth across the stack. See bidset_record.py.
"""
