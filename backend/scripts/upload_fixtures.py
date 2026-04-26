"""upload_fixtures.py — one-time-ish script to upload the 15 bidsets to
S3-compatible object storage and generate the test_fixtures/bidsets.json
manifest.

Usage:
    cd backend
    uv run python scripts/upload_fixtures.py \\
        --source ~/Documents/bidsets \\
        --bucket huckleberry-fixtures \\
        --endpoint https://<account_id>.r2.cloudflarestorage.com \\
        --provider cloudflare-r2

Reads credentials from environment (S3_ACCESS_KEY_ID, S3_SECRET_ACCESS_KEY).
See .env.example at repo root.

For each PDF in --source:
  1. Compute sha256
  2. Get size_bytes
  3. Open with pdfplumber to get page_count
  4. Upload to s3://<bucket>/fixtures/<filename>
  5. Append entry to manifest

Writes manifest to backend/test_fixtures/bidsets.json (atomic write).
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import boto3
import pdfplumber
from botocore.config import Config
from botocore.exceptions import ClientError

MANIFEST_PATH = Path(__file__).parent.parent / "test_fixtures" / "bidsets.json"


def sha256_of_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    """Stream-hash a file to avoid loading multi-MB PDFs into RAM."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def page_count_of(pdf_path: Path) -> int:
    """Open with pdfplumber, return page count. Closes promptly."""
    with pdfplumber.open(pdf_path) as p:
        return len(p.pages)


def make_s3_client(endpoint_url: str):
    """Build an S3 client from env credentials."""
    access_key = os.environ.get("S3_ACCESS_KEY_ID")
    secret_key = os.environ.get("S3_SECRET_ACCESS_KEY")
    region = os.environ.get("S3_REGION", "auto")

    if not access_key or not secret_key:
        print("ERROR: S3_ACCESS_KEY_ID and S3_SECRET_ACCESS_KEY must be set in env.", file=sys.stderr)
        print("       See .env.example at the repo root.", file=sys.stderr)
        sys.exit(2)

    return boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
        config=Config(signature_version="s3v4"),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--source", required=True, type=Path, help="Local folder containing the bidset PDFs")
    parser.add_argument("--bucket", required=True, help="S3 bucket name")
    parser.add_argument("--endpoint", required=True, help="S3-compatible endpoint URL")
    parser.add_argument(
        "--provider",
        default="cloudflare-r2",
        choices=["cloudflare-r2", "minio", "backblaze-b2", "aws-s3"],
        help="Provider name (recorded in manifest for reference)",
    )
    parser.add_argument("--key-prefix", default="fixtures/", help="S3 key prefix (default: fixtures/)")
    args = parser.parse_args()

    source: Path = args.source
    if not source.is_dir():
        print(f"ERROR: --source {source} is not a directory", file=sys.stderr)
        return 2

    pdfs = sorted(source.glob("*.pdf"))
    if not pdfs:
        print(f"ERROR: no PDFs found in {source}", file=sys.stderr)
        return 2

    print(f"Found {len(pdfs)} PDF(s) in {source}")
    if len(pdfs) != 15:
        print(f"WARNING: expected 15 bidsets, found {len(pdfs)}. Continuing anyway.")

    s3 = make_s3_client(args.endpoint)

    # Verify the bucket exists
    try:
        s3.head_bucket(Bucket=args.bucket)
    except ClientError as e:
        print(f"ERROR: bucket {args.bucket} not reachable: {e}", file=sys.stderr)
        return 2

    bidsets = []
    for pdf_path in pdfs:
        print(f"\n→ {pdf_path.name}")

        sha = sha256_of_file(pdf_path)
        size = pdf_path.stat().st_size
        try:
            pages = page_count_of(pdf_path)
        except Exception as e:
            print(f"  WARNING: pdfplumber failed to open: {e}")
            print(f"  Continuing with page_count=0; experiment will surface the issue.")
            pages = 0

        s3_key = f"{args.key_prefix.rstrip('/')}/{pdf_path.name}"
        print(f"  sha256:     {sha}")
        print(f"  size_bytes: {size}")
        print(f"  page_count: {pages}")
        print(f"  uploading → s3://{args.bucket}/{s3_key} ...")

        try:
            s3.upload_file(str(pdf_path), args.bucket, s3_key)
        except ClientError as e:
            print(f"  ERROR: upload failed: {e}", file=sys.stderr)
            return 2

        bidsets.append({
            "id": pdf_path.stem,
            "s3_key": s3_key,
            "sha256": sha,
            "size_bytes": size,
            "page_count": pages,
            "producer_hint": "unknown",  # filled in manually or by future heuristic
            "notes": "",
            "uploaded_at": datetime.now(timezone.utc).isoformat(),
        })
        print("  ✓ uploaded")

    manifest = {
        "schema_version": "0.1",
        "manifest_generated_at": datetime.now(timezone.utc).isoformat(),
        "storage": {
            "provider": args.provider,
            "bucket": args.bucket,
            "endpoint_url": args.endpoint,
            "key_prefix": args.key_prefix,
        },
        "bidsets": bidsets,
    }

    # Atomic write — write to .tmp, rename
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = MANIFEST_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(manifest, indent=2))
    tmp.replace(MANIFEST_PATH)

    print(f"\n✓ Manifest written: {MANIFEST_PATH}")
    print(f"✓ {len(bidsets)} bidset(s) cataloged")
    print("\nNext step: run scripts/verify_fixtures.py to confirm reachability.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
