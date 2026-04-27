"""
SQLite persistence for dispatch results and geometry cache.

Local-first: everything stays on the user's machine.
Cache location: ~/.tracepoint/cache.db
"""

import hashlib
import sqlite3
from pathlib import Path
from typing import Optional

DB_PATH = Path.home() / ".tracepoint" / "cache.db"


class StorageEngine:
    """SQLite persistence for dispatch results and geometry cache."""

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS dispatch_cache (
                    pdf_hash TEXT PRIMARY KEY,
                    pdf_path TEXT,
                    total_pages INTEGER,
                    context_json TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    dispatch_version TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS geometry_cache (
                    pdf_hash TEXT,
                    page_number INTEGER,
                    result_json TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (pdf_hash, page_number)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS architect_profiles (
                    firm_name TEXT PRIMARY KEY,
                    display_name TEXT,
                    pdf_producers TEXT,
                    sheet_patterns TEXT,
                    typical_scales TEXT,
                    weight_threshold REAL,
                    title_block_position TEXT,
                    success_count INTEGER DEFAULT 0,
                    last_seen TEXT,
                    gate_params TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def get_dispatch_context(self, pdf_hash: str) -> Optional[str]:
        """Get cached PlanSetContext JSON. Returns None if not cached."""
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT context_json FROM dispatch_cache WHERE pdf_hash = ?",
                (pdf_hash,)
            ).fetchone()
            return row[0] if row else None

    def save_dispatch_context(self, pdf_hash: str, pdf_path: str,
                              total_pages: int, context_json: str,
                              version: str):
        """Cache a PlanSetContext."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO dispatch_cache
                (pdf_hash, pdf_path, total_pages, context_json, dispatch_version)
                VALUES (?, ?, ?, ?, ?)
            """, (pdf_hash, pdf_path, total_pages, context_json, version))

    def get_geometry_result(self, pdf_hash: str, page: int) -> Optional[str]:
        """Get cached geometry result JSON."""
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT result_json FROM geometry_cache WHERE pdf_hash = ? AND page_number = ?",
                (pdf_hash, page)
            ).fetchone()
            return row[0] if row else None

    def save_geometry_result(self, pdf_hash: str, page: int, result_json: str):
        """Cache a geometry result."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO geometry_cache
                (pdf_hash, page_number, result_json)
                VALUES (?, ?, ?)
            """, (pdf_hash, page, result_json))

    # ------------------------------------------------------------------
    # Architect profiles
    # ------------------------------------------------------------------

    def list_architect_profiles(self) -> list[str]:
        """Return list of known firm names."""
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT firm_name FROM architect_profiles"
            ).fetchall()
            return [r[0] for r in rows]

    def get_architect_profile(self, firm_name: str) -> Optional[dict]:
        """Return the row dict for a firm, or None."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM architect_profiles WHERE firm_name = ?",
                (firm_name,)
            ).fetchone()
            return dict(row) if row else None

    def upsert_architect_profile(self, firm_name: str,
                                 success_count: int = None,
                                 pdf_producer: str = None,
                                 sheet_pattern: str = None,
                                 typical_scale: float = None,
                                 weight_threshold: float = None,
                                 title_block_position: str = None,
                                 gate_params: str = None) -> None:
        """Create or update an architect profile.

        For repeating fields (pdf_producers, sheet_patterns, typical_scales),
        appends to the JSON list rather than replacing.
        """
        import json
        from datetime import datetime, timezone
        existing = self.get_architect_profile(firm_name)
        now = datetime.now(timezone.utc).isoformat()

        def _merge_list(field_value, new_item):
            if new_item is None:
                return field_value
            try:
                lst = json.loads(field_value) if field_value else []
            except Exception:
                lst = []
            if new_item not in lst:
                lst.append(new_item)
            return json.dumps(lst)

        if existing:
            new_producers = _merge_list(existing.get("pdf_producers"), pdf_producer)
            new_patterns = _merge_list(existing.get("sheet_patterns"), sheet_pattern)
            new_scales = _merge_list(existing.get("typical_scales"), typical_scale)
            new_success = success_count if success_count is not None \
                else existing.get("success_count", 0)
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    UPDATE architect_profiles
                    SET pdf_producers = ?, sheet_patterns = ?, typical_scales = ?,
                        weight_threshold = COALESCE(?, weight_threshold),
                        title_block_position = COALESCE(?, title_block_position),
                        success_count = ?, last_seen = ?,
                        gate_params = COALESCE(?, gate_params),
                        updated_at = ?
                    WHERE firm_name = ?
                """, (new_producers, new_patterns, new_scales,
                      weight_threshold, title_block_position,
                      new_success, now, gate_params, now, firm_name))
        else:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO architect_profiles
                    (firm_name, display_name, pdf_producers, sheet_patterns,
                     typical_scales, weight_threshold, title_block_position,
                     success_count, last_seen, gate_params, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (firm_name, firm_name,
                      json.dumps([pdf_producer]) if pdf_producer else "[]",
                      json.dumps([sheet_pattern]) if sheet_pattern else "[]",
                      json.dumps([typical_scale]) if typical_scale is not None else "[]",
                      weight_threshold, title_block_position,
                      success_count or 0, now, gate_params, now, now))

    def increment_architect_success(self, firm_name: str) -> None:
        """Bump success_count by 1 for a firm. Creates stub if absent."""
        existing = self.get_architect_profile(firm_name)
        if existing:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "UPDATE architect_profiles SET success_count = success_count + 1, "
                    "updated_at = CURRENT_TIMESTAMP WHERE firm_name = ?",
                    (firm_name,)
                )
        else:
            self.upsert_architect_profile(firm_name, success_count=1)

    def clear_cache(self, pdf_hash: str = None):
        """Clear cache for a specific PDF or all."""
        with sqlite3.connect(self.db_path) as conn:
            if pdf_hash:
                conn.execute("DELETE FROM dispatch_cache WHERE pdf_hash = ?", (pdf_hash,))
                conn.execute("DELETE FROM geometry_cache WHERE pdf_hash = ?", (pdf_hash,))
            else:
                conn.execute("DELETE FROM dispatch_cache")
                conn.execute("DELETE FROM geometry_cache")


def hash_pdf(pdf_path: str) -> str:
    """Compute hash of a PDF file for cache key.
    Uses first 1MB + last 1MB + file size for fast hashing."""
    h = hashlib.sha256()
    with open(pdf_path, 'rb') as f:
        h.update(f.read(1024 * 1024))
        f.seek(0, 2)
        size = f.tell()
        h.update(str(size).encode())
        if size > 1024 * 1024:
            f.seek(-1024 * 1024, 2)
            h.update(f.read())
    return h.hexdigest()[:16]
