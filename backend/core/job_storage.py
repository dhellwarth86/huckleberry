"""
Job persistence layer — D.2 job folder + multi-tenant identity.

SQLite-backed. No SQLAlchemy. stdlib sqlite3 only.
Postgres migration deferred to post-user-testing per Daniel directive.

Tables: jobs, dispatch_results, trade_outputs, job_project_scope (G.4), scope_systems (G.4).
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

# G.4: trade scope values accepted on scope_systems rows.
_VALID_TRADES = {"roofing", "glazing", "siding", "mechanical", "plumbing", "electrical", "structural"}

# G.4: source flag — 'auto' = pre-populated from ctx.project_scope; 'manual' = user-created/edited.
_VALID_SCOPE_SOURCES = {"auto", "manual"}

# G.4: confidence buckets stored on scope_systems rows.
_VALID_SCOPE_CONFIDENCE = {"high", "medium", "low", "manual"}

# G.4: minimum project_scope.system_confidence to pre-populate an auto row.
# Mirrors TracePoint's _resolve_scope_system threshold; below this we leave
# scope_systems empty and the user enters manually.
_AUTO_PREPOPULATE_THRESHOLD = 0.7

# G.4: canonical system code -> human-readable display label.
# Backend pre-computes this so the frontend never invents labels.
_DISPLAY_NAME_MAP = {
    "tpo": "TPO Single Ply",
    "pvc": "PVC Single Ply",
    "epdm": "EPDM Single Ply",
    "modified_bitumen": "Modified Bitumen",
    "mod_bit": "Modified Bitumen",
    "built_up": "Built-Up Roofing",
    "metal_ss": "Metal Standing Seam",
    "metal_standing_seam": "Metal Standing Seam",
    "metal_corrugated": "Metal Corrugated",
    "metal_panel": "Metal Panel",
}


def _display_label(system_code: Optional[str]) -> str:
    """Map a canonical system code to a display label, fallback to title-case."""
    if not system_code:
        return "Unknown System"
    code = system_code.strip().lower()
    if code in _DISPLAY_NAME_MAP:
        return _DISPLAY_NAME_MAP[code]
    # Fallback: turn 'some_thing' into 'Some Thing'
    return " ".join(p.capitalize() for p in code.replace("-", "_").split("_"))


def _bucket_confidence(score: float) -> str:
    """Map a 0.0–1.0 confidence float to a bucket label."""
    if score >= 0.85:
        return "high"
    if score >= 0.7:
        return "medium"
    return "low"


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

    # G.4: project-level scope blob, one row per job. Holds ctx.project_scope
    # JSON-serialized so rescan can re-derive auto scope_systems rows without
    # re-running dispatch.
    conn.execute("""
        CREATE TABLE IF NOT EXISTS job_project_scope (
            job_id TEXT PRIMARY KEY REFERENCES jobs(id),
            project_scope_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    # G.4: user-editable scope-system rows. Auto rows are pre-populated from
    # ctx.project_scope at dispatch time when confidence >= 0.7. Manual rows
    # are user-created via POST. PATCH updates fields; DELETE removes rows.
    # Rescan deletes auto rows and re-derives them from job_project_scope;
    # manual rows are never touched by rescan.
    conn.execute("""
        CREATE TABLE IF NOT EXISTS scope_systems (
            id TEXT PRIMARY KEY,
            job_id TEXT NOT NULL REFERENCES jobs(id),
            trade TEXT NOT NULL,
            label TEXT NOT NULL,
            system_code TEXT,
            confidence TEXT NOT NULL,
            source TEXT NOT NULL,
            evidence_json TEXT,
            user_fields_json TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_scope_systems_job ON scope_systems(job_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_scope_systems_job_trade ON scope_systems(job_id, trade)")


def _ensure_tables(conn: sqlite3.Connection) -> None:  # D.2:
    # G.4: always run init; every statement is CREATE IF NOT EXISTS so this
    # is idempotent and lets new G.4 tables (job_project_scope, scope_systems)
    # land on existing databases that already have D.2 tables.
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
        # G.4: persist project-level scope blob + pre-populate auto scope_systems row.
        # Done inside the same _connect() context to keep semantics consistent;
        # both helpers manage their own transactions so they're safe.
        try:
            persist_project_scope(job_id, ctx)
            _pre_populate_auto_scope_systems(job_id, ctx)
        except Exception:
            # Best-effort: if scope persistence fails, dispatch_results are still
            # safely committed above. dispatch_warnings would catch this upstream.
            pass
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


# ----------------------------------------------------------------
# G.4: project-level scope persistence
# ----------------------------------------------------------------

def _project_scope_to_dict(ps) -> dict:
    """Serialize a ProjectScope dataclass (or duck-typed object) to a JSON-safe dict.
    Tolerates None and missing attributes."""
    if ps is None:
        return {}
    return {
        "scope_pages": list(getattr(ps, "scope_pages", []) or []),
        "spec_sections": list(getattr(ps, "spec_sections", []) or []),
        "detected_system": getattr(ps, "detected_system", None),
        "system_confidence": float(getattr(ps, "system_confidence", 0.0) or 0.0),
        "system_evidence": getattr(ps, "system_evidence", "") or "",
        "manufacturers": list(getattr(ps, "manufacturers", []) or []),
        "material_mentions": list(getattr(ps, "material_mentions", []) or []),
        "florida_signals": list(getattr(ps, "florida_signals", []) or []),
        "roof_shape_signal": getattr(ps, "roof_shape_signal", None),
        "architect": getattr(ps, "architect", None),
        "contractor": getattr(ps, "contractor", None),
    }


def persist_project_scope(job_id: str, ctx) -> None:  # G.4:
    """Upsert the ctx.project_scope blob to job_project_scope.
    Idempotent — re-dispatch overwrites the prior row."""
    ps = getattr(ctx, "project_scope", None)
    blob = json.dumps(_project_scope_to_dict(ps), default=str)
    now = datetime.now(timezone.utc).isoformat()
    conn = _connect()
    try:
        existing = conn.execute(
            "SELECT job_id FROM job_project_scope WHERE job_id = ?", (job_id,)
        ).fetchone()
        if existing is None:
            conn.execute(
                "INSERT INTO job_project_scope (job_id, project_scope_json, created_at, updated_at) "
                "VALUES (?, ?, ?, ?)",
                (job_id, blob, now, now),
            )
        else:
            conn.execute(
                "UPDATE job_project_scope SET project_scope_json = ?, updated_at = ? WHERE job_id = ?",
                (blob, now, job_id),
            )
        conn.commit()
    finally:
        conn.close()


def load_project_scope(job_id: str) -> Optional[dict]:  # G.4:
    """Return the persisted project_scope dict, or None if not yet persisted."""
    conn = _connect()
    try:
        row = conn.execute(
            "SELECT project_scope_json FROM job_project_scope WHERE job_id = ?",
            (job_id,),
        ).fetchone()
        if row is None:
            return None
        return json.loads(row["project_scope_json"])
    finally:
        conn.close()


# ----------------------------------------------------------------
# G.4: scope_systems CRUD
# ----------------------------------------------------------------

def _row_to_scope_system(row) -> dict:
    """Convert a sqlite3.Row to a JSON-safe dict, parsing JSON columns."""
    d = dict(row)
    if d.get("evidence_json"):
        d["evidence"] = json.loads(d["evidence_json"])
    else:
        d["evidence"] = None
    d.pop("evidence_json", None)
    if d.get("user_fields_json"):
        d["user_fields"] = json.loads(d["user_fields_json"])
    else:
        d["user_fields"] = None
    d.pop("user_fields_json", None)
    return d


def _pre_populate_auto_scope_systems(job_id: str, ctx) -> None:  # G.4:
    """Derive an auto-source roofing scope_systems row from ctx.project_scope
    when system_confidence >= _AUTO_PREPOPULATE_THRESHOLD.

    Idempotent — deletes any prior auto rows for this job (across all trades)
    before inserting, so re-dispatch yields a clean auto state. Manual rows
    (source='manual') are never touched.

    Glazing project-level scope identification is deferred (own future phase)
    so this only seeds the roofing trade today.
    """
    ps = getattr(ctx, "project_scope", None)
    if ps is None:
        return
    detected = getattr(ps, "detected_system", None)
    confidence = float(getattr(ps, "system_confidence", 0.0) or 0.0)
    if not detected or confidence < _AUTO_PREPOPULATE_THRESHOLD:
        # Below threshold or no detection — clear auto rows and leave the
        # scope tab empty for the user to enter manually.
        _delete_auto_scope_systems(job_id, trade=None)
        return

    label = _display_label(detected)
    bucket = _bucket_confidence(confidence)
    evidence = {
        "system_evidence": getattr(ps, "system_evidence", "") or "",
        "manufacturers": list(getattr(ps, "manufacturers", []) or []),
        "spec_sections": list(getattr(ps, "spec_sections", []) or []),
        "scope_pages": list(getattr(ps, "scope_pages", []) or []),
        "system_confidence": confidence,
    }
    now = datetime.now(timezone.utc).isoformat()
    conn = _connect()
    try:
        # Wipe any prior auto rows so re-dispatch produces deterministic state.
        conn.execute(
            "DELETE FROM scope_systems WHERE job_id = ? AND source = 'auto'",
            (job_id,),
        )
        sys_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO scope_systems (id, job_id, trade, label, system_code, "
            "confidence, source, evidence_json, user_fields_json, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL, ?, ?)",
            (sys_id, job_id, "roofing", label, detected, bucket, "auto",
             json.dumps(evidence, default=str), now, now),
        )
        conn.commit()
    finally:
        conn.close()


def _delete_auto_scope_systems(job_id: str, trade: Optional[str] = None) -> int:
    """Delete auto-source rows for a job. Returns deleted-count.
    If trade is provided, scoped to that trade. Manual rows untouched."""
    conn = _connect()
    try:
        if trade is None:
            cur = conn.execute(
                "DELETE FROM scope_systems WHERE job_id = ? AND source = 'auto'",
                (job_id,),
            )
        else:
            cur = conn.execute(
                "DELETE FROM scope_systems WHERE job_id = ? AND trade = ? AND source = 'auto'",
                (job_id, trade),
            )
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()


def list_scope_systems(job_id: str, trade: Optional[str] = None) -> list[dict]:  # G.4:
    """Return scope_systems rows for a job, optionally filtered by trade."""
    conn = _connect()
    try:
        if trade is None:
            rows = conn.execute(
                "SELECT * FROM scope_systems WHERE job_id = ? ORDER BY trade, source DESC, created_at",
                (job_id,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM scope_systems WHERE job_id = ? AND trade = ? "
                "ORDER BY source DESC, created_at",
                (job_id, trade),
            ).fetchall()
        return [_row_to_scope_system(r) for r in rows]
    finally:
        conn.close()


def get_scope_system(sys_id: str) -> Optional[dict]:  # G.4:
    """Return a single scope_systems row by id, or None."""
    conn = _connect()
    try:
        row = conn.execute(
            "SELECT * FROM scope_systems WHERE id = ?", (sys_id,)
        ).fetchone()
        return _row_to_scope_system(row) if row else None
    finally:
        conn.close()


def create_scope_system(  # G.4:
    job_id: str,
    *,
    trade: str,
    label: str,
    system_code: Optional[str] = None,
    user_fields: Optional[dict] = None,
) -> dict:
    """Create a manual scope_systems row. Returns the inserted row."""
    if trade not in _VALID_TRADES:
        raise ValueError(f"Invalid trade: {trade}")
    if not label or not label.strip():
        raise ValueError("label is required")
    sys_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    user_fields_json = json.dumps(user_fields, default=str) if user_fields else None
    conn = _connect()
    try:
        conn.execute(
            "INSERT INTO scope_systems (id, job_id, trade, label, system_code, "
            "confidence, source, evidence_json, user_fields_json, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, NULL, ?, ?, ?)",
            (sys_id, job_id, trade, label.strip(), system_code,
             "manual", "manual", user_fields_json, now, now),
        )
        conn.commit()
    finally:
        conn.close()
    row = get_scope_system(sys_id)
    if row is None:
        raise RuntimeError("scope_system creation failed")
    return row


def update_scope_system(  # G.4:
    sys_id: str,
    *,
    label: Optional[str] = None,
    system_code: Optional[str] = None,
    user_fields: Optional[dict] = None,
) -> Optional[dict]:
    """Patch a scope_systems row. Only provided fields are updated.
    Returns updated row, or None if not found."""
    existing = get_scope_system(sys_id)
    if existing is None:
        return None
    sets: list[str] = []
    params: list = []
    if label is not None:
        if not label.strip():
            raise ValueError("label cannot be empty")
        sets.append("label = ?")
        params.append(label.strip())
    if system_code is not None:
        sets.append("system_code = ?")
        params.append(system_code)
    if user_fields is not None:
        sets.append("user_fields_json = ?")
        params.append(json.dumps(user_fields, default=str))
    if not sets:
        return existing  # nothing to do
    sets.append("updated_at = ?")
    params.append(datetime.now(timezone.utc).isoformat())
    params.append(sys_id)
    conn = _connect()
    try:
        conn.execute(
            f"UPDATE scope_systems SET {', '.join(sets)} WHERE id = ?",
            params,
        )
        conn.commit()
    finally:
        conn.close()
    return get_scope_system(sys_id)


def delete_scope_system(sys_id: str) -> bool:  # G.4:
    """Delete a scope_systems row by id. Returns True if deleted, False if not found."""
    conn = _connect()
    try:
        cur = conn.execute("DELETE FROM scope_systems WHERE id = ?", (sys_id,))
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()


def rescan_scope_systems(job_id: str, trade: str) -> list[dict]:  # G.4:
    """Reset auto-source rows for a job+trade by re-deriving from persisted
    project_scope. Manual rows untouched. Returns the fresh list (auto + manual,
    filtered to the requested trade).

    Today this only re-derives roofing auto rows (glazing project-level
    identification deferred). For other trades the call deletes any auto
    rows and returns whatever manual rows exist.
    """
    if trade not in _VALID_TRADES:
        raise ValueError(f"Invalid trade: {trade}")
    # Always clear the trade's auto rows first.
    _delete_auto_scope_systems(job_id, trade=trade)

    if trade == "roofing":
        ps_dict = load_project_scope(job_id)
        if ps_dict:
            detected = ps_dict.get("detected_system")
            confidence = float(ps_dict.get("system_confidence") or 0.0)
            if detected and confidence >= _AUTO_PREPOPULATE_THRESHOLD:
                label = _display_label(detected)
                bucket = _bucket_confidence(confidence)
                evidence = {
                    "system_evidence": ps_dict.get("system_evidence", "") or "",
                    "manufacturers": list(ps_dict.get("manufacturers") or []),
                    "spec_sections": list(ps_dict.get("spec_sections") or []),
                    "scope_pages": list(ps_dict.get("scope_pages") or []),
                    "system_confidence": confidence,
                }
                sys_id = str(uuid.uuid4())
                now = datetime.now(timezone.utc).isoformat()
                conn = _connect()
                try:
                    conn.execute(
                        "INSERT INTO scope_systems (id, job_id, trade, label, system_code, "
                        "confidence, source, evidence_json, user_fields_json, "
                        "created_at, updated_at) "
                        "VALUES (?, ?, 'roofing', ?, ?, ?, 'auto', ?, NULL, ?, ?)",
                        (sys_id, job_id, label, detected, bucket,
                         json.dumps(evidence, default=str), now, now),
                    )
                    conn.commit()
                finally:
                    conn.close()
    return list_scope_systems(job_id, trade=trade)
