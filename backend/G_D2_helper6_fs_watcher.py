"""Helper 6 — Filesystem watcher (G.D2 diagnostic, TEMPORARY).

Watches ~/.tracepoint/ for any file create/modify/delete during the session.
Polls every 2 seconds (no watchdog dependency needed).

Output: backend/G_D2_FILESYSTEM.log

Run: python G_D2_helper6_fs_watcher.py
"""
from __future__ import annotations

import os
import time
from datetime import datetime, timezone
from pathlib import Path

WATCH_DIR = Path.home() / ".tracepoint"
LOG_PATH = Path(__file__).parent / "G_D2_FILESYSTEM.log"


def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _log(msg: str) -> None:
    line = f"[{_ts()}] {msg}\n"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line)
    print(line.rstrip())


def _scan(root: Path) -> dict[str, tuple[float, int]]:
    """Return {relative_path: (mtime, size)} for all files under root."""
    result = {}
    if not root.exists():
        return result
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in filenames:
            full = Path(dirpath) / fn
            try:
                st = full.stat()
                rel = str(full.relative_to(root))
                result[rel] = (st.st_mtime, st.st_size)
            except (OSError, ValueError):
                pass
    return result


def main() -> None:
    _log("Helper 6 (filesystem watcher) started")
    _log(f"Watching: {WATCH_DIR}")
    _log(f"Poll interval: 2s")

    if not WATCH_DIR.exists():
        _log(f"WARNING: {WATCH_DIR} does not exist yet. Waiting...")
        while not WATCH_DIR.exists():
            time.sleep(2)
        _log(f"{WATCH_DIR} appeared.")

    prev = _scan(WATCH_DIR)
    _log(f"Initial file count: {len(prev)}")
    for rel, (mtime, size) in sorted(prev.items()):
        _log(f"  EXISTS: {rel} ({size} bytes, mtime={mtime:.0f})")

    try:
        while True:
            time.sleep(2)
            curr = _scan(WATCH_DIR)

            for rel in sorted(set(curr.keys()) - set(prev.keys())):
                mtime, size = curr[rel]
                _log(f"CREATED: {rel} ({size} bytes)")

            for rel in sorted(set(prev.keys()) - set(curr.keys())):
                _log(f"DELETED: {rel}")

            for rel in sorted(set(prev.keys()) & set(curr.keys())):
                old_mtime, old_size = prev[rel]
                new_mtime, new_size = curr[rel]
                if old_mtime != new_mtime or old_size != new_size:
                    _log(f"MODIFIED: {rel} (size {old_size}->{new_size}, mtime {old_mtime:.0f}->{new_mtime:.0f})")

            prev = curr
    except KeyboardInterrupt:
        _log("Helper 6 stopped (KeyboardInterrupt)")


if __name__ == "__main__":
    main()
