"""Helper 1 — Backend watcher (G.D2 diagnostic, TEMPORARY).

Polls SQLite tables every 30s for row counts, monitors process stats.
Timestamps all entries.

Output: backend/G_D2_BACKEND_TIMELINE.log

Run: python G_D2_helper1_watcher.py [uvicorn_pid]
"""
from __future__ import annotations

import json
import os
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path.home() / ".tracepoint" / "cache.db"
LOG_PATH = Path(__file__).parent / "G_D2_BACKEND_TIMELINE.log"

TABLES = ["jobs", "dispatch_results", "trade_outputs", "dispatch_cache", "geometry_cache", "architect_profiles"]


def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _log(msg: str) -> None:
    line = f"[{_ts()}] {msg}\n"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line)
    print(line.rstrip())


def _row_counts(conn: sqlite3.Connection) -> dict[str, int]:
    counts = {}
    for table in TABLES:
        try:
            row = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
            counts[table] = row[0]
        except sqlite3.OperationalError:
            counts[table] = -1
    return counts


def _process_stats(pid: int | None) -> dict:
    if pid is None:
        return {"note": "no PID provided"}
    try:
        import psutil
        p = psutil.Process(pid)
        mem = p.memory_info()
        return {
            "pid": pid,
            "cpu_percent": p.cpu_percent(interval=0.1),
            "rss_mb": round(mem.rss / 1024 / 1024, 1),
            "vms_mb": round(mem.vms / 1024 / 1024, 1),
            "status": p.status(),
        }
    except ImportError:
        try:
            if sys.platform == "win32":
                import subprocess
                result = subprocess.run(
                    ["tasklist", "/fi", f"PID eq {pid}", "/fo", "csv", "/nh"],
                    capture_output=True, text=True, timeout=5
                )
                return {"pid": pid, "tasklist": result.stdout.strip()}
            return {"pid": pid, "note": "psutil not available"}
        except Exception as e:
            return {"pid": pid, "error": str(e)}
    except Exception as e:
        return {"pid": pid, "error": str(e)}


def main() -> None:
    pid = int(sys.argv[1]) if len(sys.argv) > 1 else None

    _log("Helper 1 (backend watcher) started")
    _log(f"Database: {DB_PATH}")
    _log(f"Monitoring PID: {pid or 'none'}")
    _log(f"Poll interval: 30s")

    try:
        while True:
            if DB_PATH.exists():
                try:
                    conn = sqlite3.connect(str(DB_PATH), timeout=5)
                    conn.execute("PRAGMA journal_mode=WAL")
                    counts = _row_counts(conn)
                    conn.close()
                    _log(f"Row counts: {json.dumps(counts)}")
                except Exception as e:
                    _log(f"DB error: {e}")
            else:
                _log("Database file not found")

            stats = _process_stats(pid)
            _log(f"Process stats: {json.dumps(stats)}")

            time.sleep(30)
    except KeyboardInterrupt:
        _log("Helper 1 stopped (KeyboardInterrupt)")


if __name__ == "__main__":
    main()
