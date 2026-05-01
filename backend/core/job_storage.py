"""
Job persistence layer — D.2 job folder + multi-tenant identity.

SQLite-backed. No SQLAlchemy. stdlib sqlite3 only.
Postgres migration deferred to post-user-testing per Daniel directive.

Tables: jobs, dispatch_results, trade_outputs.
"""

import hashlib
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from core.storage import DB_PATH

_VALID_STATUSES = {"draft", "dispatching", "dispatched", "in_review", "exported", "archived"}
_SORTABLE_COLUMNS = {"created_at", "updated_at", "gc", "location_state",
                     "location_city", "trade_scope", "bid_due_date", "status", "name"}


def _get_db_path() -> Path:
    return DB_PATH


def _init_job_tables(conn: sqlite3.Connection) -> None:  # D.2:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gc TEXT,
            location_city TEXT,
            location_state TEXT,
            trade_scope TEXT NOT NULL,
            bid_due_date TEXT,
            notes TEXT,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            pdf_path TEXT NOT NULL,
            pdf_sha1 TEXT NOT NULL,
            dispatch_complete INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS dispatch_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT NOT NULL REFERENCES jobs(id),
            page_idx INTEGER NOT NULL,
            page_type TEXT,
            sheet_num TEXT,
            sheet_title TEXT,
            legends_count INTEGER NOT NULL DEFAULT 0,
            has_legend INTEGER NOT NULL DEFAULT 0,
            has_schedule INTEGER NOT NULL DEFAULT 0,
            raw_tables_json TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS trade_outputs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT NOT NULL REFERENCES jobs(id),
            page_idx INTEGER NOT NULL,
            trade_name TEXT NOT NULL,
            output_json TEXT NOT NULL
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_jobs_gc ON jobs(gc)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_jobs_location ON jobs(location_state, location_city)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_jobs_bid_due_date ON jobs(bid_due_date)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_jobs_created_at ON jobs(created_at)")


def _ensure_tables(conn: sqlite3.Connection) -> None:  # D.2:
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='jobs'"
    ).fetchone()
    if row is None:
        _init_job_tables(conn)


def _pdf_sha1(pdf_path: str) -> str:  # D.2:
    h = hashlib.sha1()
    with open(pdf_path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def _connect() -> sqlite3.Connection:  # D.2:
    db = _get_db_path()
    db.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db))
    conn.row_factory = sqlite3.Row
    _ensure_tables(conn)
    return conn


# ----------------------------------------------------------------
# Job lifecycle API
# ----------------------------------------------------------------

def create_job(  # D.2:
    name: str,
    pdf_path: str,
    *,
    gc: str | None = None,
    location_city: str | None = None,
    location_state: str | None = None,
    trade_scope: str = "roofing",
    bid_due_date: str | None = None,
    notes: str | None = None,
    status: str = "draft",
) -> str:
    """Create a job row. Returns job_id (UUID4). Computes pdf_sha1."""
    if status not in _VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}")
    job_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    sha1 = _pdf_sha1(pdf_path)
    conn = _connect()
    try:
        conn.execute(
            "INSERT INTO jobs (id, name, gc, location_city, location_state, "
            "trade_scope, bid_due_date, notes, status, created_at, updated_at, "
            "pdf_path, pdf_sha1, dispatch_complete) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)",
            (job_id, name, gc, location_city, location_state,
             trade_scope, bid_due_date, notes, status, now, now,
             pdf_path, sha1),
        )
        conn.commit()
    finally:
        conn.close()
    return job_id


def get_job(job_id: str) -> dict | None:  # D.2:
    """Return full job row as dict, or None if not found."""
    conn = _connect()
    try:
        row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def list_jobs(  # D.2:
    *,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    filter_gc: str | None = None,
    filter_status: str | None = None,
    filter_state: str | None = None,
) -> list[dict]:
    """Return list of job rows. sort_by must be one of the indexed columns."""
    if sort_by not in _SORTABLE_COLUMNS:
        raise ValueError(f"Invalid sort_by: {sort_by}")
    if sort_order.lower() not in ("asc", "desc"):
        raise ValueError(f"Invalid sort_order: {sort_order}")

    clauses = []
    params: list = []
    if filter_gc is not None:
        clauses.append("gc = ?")
        params.append(filter_gc)
    if filter_status is not None:
        clauses.append("status = ?")
        params.append(filter_status)
    if filter_state is not None:
        clauses.append("location_state = ?")
        params.append(filter_state)

    where = (" WHERE " + " AND ".join(clauses)) if clauses else ""
    sql = f"SELECT * FROM jobs{where} ORDER BY {sort_by} {sort_order}"

    conn = _connect()
    try:
        rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def update_job_status(job_id: str, status: str) -> None:  # D.2:
    """Update job status. Must be one of the valid enum values."""
    if status not in _VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}")
    now = datetime.now(timezone.utc).isoformat()
    conn = _connect()
    try:
        conn.execute(
            "UPDATE jobs SET status = ?, updated_at = ? WHERE id = ?",
            (status, now, job_id),
        )
        conn.commit()
    finally:
        conn.close()


def mark_dispatch_complete(job_id: str) -> None:  # D.2:
    """Mark job as dispatch_complete=1 and update timestamp."""
    now = datetime.now(timezone.utc).isoformat()
    conn = _connect()
    try:
        conn.execute(
            "UPDATE jobs SET dispatch_complete = 1, updated_at = ? WHERE id = ?",
            (now, job_id),
        )
        conn.commit()
    finally:
        conn.close()


# ----------------------------------------------------------------
# Dispatch result persistence
# ----------------------------------------------------------------

def persist_dispatch_result(job_id: str, ctx) -> None:  # D.2:
    """Walk ctx.pages and write one dispatch_results row per page."""
    conn = _connect()
    try:
        for page_idx, page_ctx in sorted(ctx.pages.items()):
            pt = getattr(page_ctx, "page_type", None)
            page_type_str = getattr(pt, "value", str(pt)) if pt is not None else None
            sheet_num = getattr(page_ctx, "sheet_number", None)
            title = getattr(page_ctx, "title", None)
            legends = getattr(page_ctx, "legends", []) or []
            legends_count = len(legends)
            has_legend = 1 if getattr(page_ctx, "has_legend", False) else 0
            has_schedule = 1 if getattr(page_ctx, "has_schedule", False) else 0
            raw_tables = getattr(page_ctx, "raw_tables", None)
            raw_tables_json = json.dumps(raw_tables) if raw_tables else None

            conn.execute(
                "INSERT INTO dispatch_results "
                "(job_id, page_idx, page_type, sheet_num, sheet_title, "
                "legends_count, has_legend, has_schedule, raw_tables_json) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (job_id, page_idx, page_type_str, sheet_num, title,
                 legends_count, has_legend, has_schedule, raw_tables_json),
            )
        conn.commit()
    finally:
        conn.close()


def persist_trade_outputs(job_id: str, ctx) -> None:  # D.2:
    """Walk ctx.trade_module_outputs and write one trade_outputs row per (page_idx, trade_name)."""
    from dataclasses import asdict, is_dataclass

    conn = _connect()
    try:
        for page_idx, per_page in sorted(ctx.trade_module_outputs.items()):
            for trade_name, output in per_page.items():
                if is_dataclass(output):
                    fields_dict = {}
                    for k, v in (output.fields or {}).items():
                        if is_dataclass(v):
                            fields_dict[k] = asdict(v)
                        else:
                            fields_dict[k] = v
                    out_dict = {
                        "fields": fields_dict,
                        "warnings": list(output.warnings or []),
                        "equipment_pins": list(output.equipment_pins or []),
                        "glazing_items": list(output.glazing_items) if output.glazing_items is not None else None,
                        "door_items": list(output.door_items) if output.door_items is not None else None,
                        "storefront_items": list(output.storefront_items) if output.storefront_items is not None else None,
                    }
                elif isinstance(output, dict):
                    out_dict = output
                else:
                    out_dict = {"raw": str(output)}
                conn.execute(
                    "INSERT INTO trade_outputs (job_id, page_idx, trade_name, output_json) "
                    "VALUES (?, ?, ?, ?)",
                    (job_id, page_idx, trade_name, json.dumps(out_dict, default=str)),
                )
        conn.commit()
    finally:
        conn.close()


# ----------------------------------------------------------------
# Loading persisted data
# ----------------------------------------------------------------

def load_dispatch_results(job_id: str) -> dict[int, dict]:  # D.2:
    """Reverse of persist_dispatch_result. Returns {page_idx: row_dict}."""
    conn = _connect()
    try:
        rows = conn.execute(
            "SELECT * FROM dispatch_results WHERE job_id = ? ORDER BY page_idx",
            (job_id,),
        ).fetchall()
        result: dict[int, dict] = {}
        for r in rows:
            d = dict(r)
            page_idx = d["page_idx"]
            if d.get("raw_tables_json"):
                d["raw_tables"] = json.loads(d["raw_tables_json"])
            else:
                d["raw_tables"] = None
            result[page_idx] = d
        return result
    finally:
        conn.close()


def load_trade_outputs(job_id: str) -> dict[int, dict[str, dict]]:  # D.2:
    """Reverse of persist_trade_outputs. Returns {page_idx: {trade_name: output_dict}}."""
    conn = _connect()
    try:
        rows = conn.execute(
            "SELECT page_idx, trade_name, output_json FROM trade_outputs "
            "WHERE job_id = ? ORDER BY page_idx, trade_name",
            (job_id,),
        ).fetchall()
        result: dict[int, dict[str, dict]] = {}
        for r in rows:
            page_idx = r["page_idx"]
            trade_name = r["trade_name"]
            output = json.loads(r["output_json"])
            result.setdefault(page_idx, {})[trade_name] = output
        return result
    finally:
        conn.close()
