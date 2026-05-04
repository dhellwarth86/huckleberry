"""Helper 4 — SQLite mutation watcher (G.D2 diagnostic, TEMPORARY).

Polls SQLite every 2 seconds, diffs row state, logs every detected mutation
with table name, row PK, and before/after column values.

Output: backend/G_D2_DB_MUTATIONS.log

Run: python G_D2_helper4_db_watcher.py
"""
from __future__ import annotations

import json
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path.home() / ".tracepoint" / "cache.db"
LOG_PATH = Path(__file__).parent / "G_D2_DB_MUTATIONS.log"

TABLES = {
    "jobs": ("id",),
    "dispatch_results": ("id",),
    "trade_outputs": ("id",),
    "dispatch_cache": ("pdf_hash",),
    "geometry_cache": ("pdf_hash", "page_number"),
    "architect_profiles": ("firm_name",),
}


def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _log(msg: str) -> None:
    line = f"[{_ts()}] {msg}\n"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line)
    print(line.rstrip())


def _snapshot(conn: sqlite3.Connection) -> dict[str, dict]:
    """Snapshot all tracked tables. Returns {table: {pk_value: {col: val, ...}}}."""
    snap = {}
    for table, pk_cols in TABLES.items():
        try:
            cursor = conn.execute(f"SELECT * FROM {table}")
            cols = [d[0] for d in cursor.description]
            pk_indices = [cols.index(c) for c in pk_cols]
            rows = {}
            for row in cursor.fetchall():
                pk_val = "|".join(str(row[i]) for i in pk_indices)
                rows[pk_val] = {cols[i]: row[i] for i in range(len(cols))}
            snap[table] = rows
        except (sqlite3.OperationalError, ValueError):
            snap[table] = {}
    return snap


def _diff(old: dict, new: dict) -> list[str]:
    """Compare two snapshots, return list of mutation descriptions."""
    mutations = []
    all_tables = set(old.keys()) | set(new.keys())
    for table in sorted(all_tables):
        old_rows = old.get(table, {})
        new_rows = new.get(table, {})
        all_pks = set(old_rows.keys()) | set(new_rows.keys())
        for pk in sorted(all_pks):
            if pk not in old_rows:
                mutations.append(f"INSERT {table} pk={pk}: {json.dumps(new_rows[pk], default=str)}")
            elif pk not in new_rows:
                mutations.append(f"DELETE {table} pk={pk}: was {json.dumps(old_rows[pk], default=str)}")
            else:
                old_row = old_rows[pk]
                new_row = new_rows[pk]
                changes = {}
                for col in set(old_row.keys()) | set(new_row.keys()):
                    ov = old_row.get(col)
                    nv = new_row.get(col)
                    if ov != nv:
                        changes[col] = {"before": ov, "after": nv}
                if changes:
                    mutations.append(
                        f"UPDATE {table} pk={pk}: {json.dumps(changes, default=str)}"
                    )
    return mutations


def main() -> None:
    _log("Helper 4 (DB mutation watcher) started")
    _log(f"Watching: {DB_PATH}")
    _log(f"Tables: {', '.join(TABLES.keys())}")
    _log(f"Poll interval: 2s")

    if not DB_PATH.exists():
        _log("WARNING: database file does not exist yet. Waiting for it to appear...")
        while not DB_PATH.exists():
            time.sleep(2)
        _log("Database file appeared.")

    conn = sqlite3.connect(str(DB_PATH), timeout=5)
    conn.execute("PRAGMA journal_mode=WAL")
    prev = _snapshot(conn)

    row_counts = {t: len(rows) for t, rows in prev.items()}
    _log(f"Initial row counts: {json.dumps(row_counts)}")

    try:
        while True:
            time.sleep(2)
            try:
                curr = _snapshot(conn)
                mutations = _diff(prev, curr)
                if mutations:
                    _log(f"=== {len(mutations)} mutation(s) detected ===")
                    for m in mutations:
                        _log(f"  {m}")
                    row_counts = {t: len(rows) for t, rows in curr.items()}
                    _log(f"  Row counts now: {json.dumps(row_counts)}")
                prev = curr
            except sqlite3.OperationalError as e:
                _log(f"SQLite error during poll: {e}")
    except KeyboardInterrupt:
        _log("Helper 4 stopped (KeyboardInterrupt)")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
