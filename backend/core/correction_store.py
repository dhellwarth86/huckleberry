"""
CorrectionStore — JSON-lines file storage for user corrections.

Each correction is one JSON object per line, appended to a file
named by doc_id. This keeps corrections persistent, grep-friendly,
and trivially exportable for future training pipelines.

File layout:
  corrections/
    {doc_id}.jsonl      — one correction per line
"""

import json
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Optional

from core.config import CORRECTION_DIR


@dataclass
class Correction:
    """Single user correction record."""

    # Identity
    id: str                          # unique correction ID
    doc_id: str                      # document this correction belongs to
    page: int                        # page index (0-based)
    timestamp: float                 # Unix epoch seconds

    # What was corrected
    field_key: str                   # e.g. "roof_area", "perimeter", "rtu_count"
    # ai_value/human_value accept numbers (e.g. drain count, scale fpi) OR
    # strings (e.g. pin labels like "DRAIN", pin type like "scupper"). Both
    # serialize cleanly to JSONL.
    ai_value: Optional[Any] = None   # what the system predicted
    human_value: Optional[Any] = None  # what the user set

    # For pin/symbol corrections
    symbol_type: Optional[str] = None    # e.g. "rtu", "drain", "scupper"
    action: Optional[str] = None         # "added", "removed", "moved"
    x: Optional[float] = None            # percentage coordinate (0-100)
    y: Optional[float] = None            # percentage coordinate (0-100)

    # For geometry corrections
    region_bbox: Optional[list] = None   # [x1, y1, x2, y2] percentage

    # Scale
    scale_ft_per_inch: Optional[float] = None

    # Metadata
    source: str = "manual"           # "manual" or "ai_review"


class CorrectionStore:
    """Append-only JSON-lines storage for corrections."""

    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or CORRECTION_DIR
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _file_for(self, doc_id: str) -> Path:
        return self.base_dir / f"{doc_id}.jsonl"

    def save(self, correction: Correction) -> str:
        """Append a correction to the doc's JSONL file. Returns the correction ID."""
        path = self._file_for(correction.doc_id)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(correction)) + "\n")
        return correction.id

    def list_for_doc(self, doc_id: str, page: Optional[int] = None) -> list[Correction]:
        """Load all corrections for a document, optionally filtered by page."""
        path = self._file_for(doc_id)
        if not path.exists():
            return []

        corrections = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                c = Correction(**data)
                if page is not None and c.page != page:
                    continue
                corrections.append(c)
        return corrections

    def delete(self, doc_id: str, correction_id: str) -> bool:
        """Remove a correction by ID. Rewrites the file without it."""
        path = self._file_for(doc_id)
        if not path.exists():
            return False

        lines = []
        found = False
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                if data.get("id") == correction_id:
                    found = True
                    continue
                lines.append(line)

        if found:
            with open(path, "w", encoding="utf-8") as f:
                for line in lines:
                    f.write(line + "\n")
        return found

    def clear_doc(self, doc_id: str) -> int:
        """Delete all corrections for a document. Returns count removed."""
        path = self._file_for(doc_id)
        if not path.exists():
            return 0
        count = sum(1 for line in open(path) if line.strip())
        path.unlink()
        return count

    def list_all_docs(self) -> list[str]:
        """Return doc_ids that have corrections."""
        return [p.stem for p in self.base_dir.glob("*.jsonl")]

    @staticmethod
    def make_id() -> str:
        """Generate a correction ID."""
        import random
        return f"corr_{int(time.time())}_{random.randint(1000, 9999)}"
