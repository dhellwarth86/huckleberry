"""local_manifest.py — generate the bidsets.json manifest for local-mode v0.1.

Phase 2 v0.1 march orders explicitly skip S3 upload: read PDFs locally. This
script mirrors upload_fixtures.py's manifest shape but populates a `local`
storage block instead of `s3`. Same schema_version (0.1) so downstream
consumers don't branch.

Usage:
    cd backend
    .venv/Scripts/python.exe scripts/local_manifest.py --source "C:/huck stage 2/full bid sets"
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pdfplumber

MANIFEST_PATH = Path(__file__).parent.parent / "test_fixtures" / "bidsets.json"


def slugify(name: str) -> str:
    """Turn a PDF stem into a stable, filesystem-safe id."""
    out = []
    last_dash = False
    for ch in name.lower():
        if ch.isalnum():
            out.append(ch)
            last_dash = False
        elif not last_dash:
            out.append("-")
            last_dash = True
    return "".join(out).strip("-")


def sha256_of_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def page_count_of(pdf_path: Path) -> int:
    with pdfplumber.open(pdf_path) as p:
        return len(p.pages)


def producer_hint_of(pdf_path: Path) -> str:
    """Best-effort producer detection from PDF metadata."""
    try:
        with pdfplumber.open(pdf_path) as p:
            meta = p.metadata or {}
            producer = meta.get("Producer", "") or ""
            creator = meta.get("Creator", "") or ""
            if "STACK" in producer.upper() or "STACK" in creator.upper():
                return "STACK Construction Technologies"
            if "UniDoc" in producer or "UNIDOC" in producer.upper():
                return f"UniDoc ({producer})"
            if producer:
                return producer.strip()
            if creator:
                return creator.strip()
    except Exception:
        pass
    return "unknown"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--source", required=True, type=Path, help="Local folder with the 15 PDFs")
    args = parser.parse_args()

    source: Path = args.source.resolve()
    if not source.is_dir():
        print(f"ERROR: --source {source} is not a directory", file=sys.stderr)
        return 2

    pdfs = sorted(source.glob("*.pdf"))
    if not pdfs:
        print(f"ERROR: no PDFs found in {source}", file=sys.stderr)
        return 2

    print(f"Found {len(pdfs)} PDF(s) in {source}")
    if len(pdfs) != 15:
        print(f"WARNING: expected 15 bidsets, found {len(pdfs)}. Continuing.")

    bidsets = []
    seen_ids: set[str] = set()
    for pdf_path in pdfs:
        bid_id = slugify(pdf_path.stem)
        if bid_id in seen_ids:
            n = 2
            while f"{bid_id}-{n}" in seen_ids:
                n += 1
            bid_id = f"{bid_id}-{n}"
        seen_ids.add(bid_id)

        print(f"\n-> {pdf_path.name}  ->  id={bid_id}")
        sha = sha256_of_file(pdf_path)
        size = pdf_path.stat().st_size
        try:
            pages = page_count_of(pdf_path)
        except Exception as e:
            print(f"  WARNING: pdfplumber failed to open: {e}")
            pages = 0
        producer = producer_hint_of(pdf_path)
        print(f"  sha256:     {sha}")
        print(f"  size_bytes: {size}")
        print(f"  page_count: {pages}")
        print(f"  producer:   {producer}")

        bidsets.append({
            "id": bid_id,
            "filename": pdf_path.name,
            "local_path": str(pdf_path),
            "sha256": sha,
            "size_bytes": size,
            "page_count": pages,
            "producer_hint": producer,
            "notes": "",
            "uploaded_at": datetime.now(timezone.utc).isoformat(),
        })

    manifest = {
        "schema_version": "0.1",
        "manifest_generated_at": datetime.now(timezone.utc).isoformat(),
        "storage": {
            "provider": "local",
            "base_path": str(source),
        },
        "bidsets": bidsets,
    }

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = MANIFEST_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(manifest, indent=2))
    tmp.replace(MANIFEST_PATH)
    print(f"\nManifest written: {MANIFEST_PATH}")
    print(f"{len(bidsets)} bidset(s) cataloged")

    # Reachability check (same code path as future S3 verify_fixtures)
    missing = [b for b in bidsets if not Path(b["local_path"]).is_file()]
    if missing:
        print(f"WARNING: {len(missing)} entries point to missing files", file=sys.stderr)
        return 1
    print(f"OK {len(bidsets)}/{len(bidsets)} bidsets reachable from disk")
    return 0


if __name__ == "__main__":
    sys.exit(main())
