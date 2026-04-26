"""verify_fixtures.py — read the manifest, HEAD-request each S3 key, confirm
size and (optionally) hash. Run after upload_fixtures.py to confirm everything
is reachable.

Usage:
    cd backend
    uv run python scripts/verify_fixtures.py
    # Or with hash verification (slower — re-downloads every PDF):
    uv run python scripts/verify_fixtures.py --check-hash
"""

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

MANIFEST_PATH = Path(__file__).parent.parent / "test_fixtures" / "bidsets.json"


def make_s3_client(endpoint_url: str):
    access_key = os.environ.get("S3_ACCESS_KEY_ID")
    secret_key = os.environ.get("S3_SECRET_ACCESS_KEY")
    region = os.environ.get("S3_REGION", "auto")

    if not access_key or not secret_key:
        print("ERROR: S3_ACCESS_KEY_ID and S3_SECRET_ACCESS_KEY must be set", file=sys.stderr)
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
    parser.add_argument(
        "--check-hash",
        action="store_true",
        help="Re-download each PDF and verify sha256 (slow but thorough)",
    )
    args = parser.parse_args()

    if not MANIFEST_PATH.exists():
        print(f"ERROR: manifest not found at {MANIFEST_PATH}", file=sys.stderr)
        print("       Run scripts/upload_fixtures.py first.", file=sys.stderr)
        return 2

    manifest = json.loads(MANIFEST_PATH.read_text())
    storage = manifest["storage"]
    bidsets = manifest["bidsets"]

    print(f"Verifying {len(bidsets)} bidset(s) in s3://{storage['bucket']}")
    print(f"Endpoint: {storage['endpoint_url']}")
    print(f"Provider: {storage['provider']}")
    if args.check_hash:
        print("Mode: HEAD + hash verify (slow)")
    else:
        print("Mode: HEAD only (fast)")
    print()

    s3 = make_s3_client(storage["endpoint_url"])

    ok_count = 0
    fail_count = 0

    for entry in bidsets:
        bid_id = entry["id"]
        s3_key = entry["s3_key"]
        expected_size = entry["size_bytes"]
        expected_sha = entry["sha256"]

        try:
            head = s3.head_object(Bucket=storage["bucket"], Key=s3_key)
            actual_size = head["ContentLength"]

            if actual_size != expected_size:
                print(f"  FAIL  {bid_id}")
                print(f"        size mismatch: manifest={expected_size}, s3={actual_size}")
                fail_count += 1
                continue

            if args.check_hash:
                # Stream download, hash, verify
                obj = s3.get_object(Bucket=storage["bucket"], Key=s3_key)
                h = hashlib.sha256()
                for chunk in obj["Body"].iter_chunks(1024 * 1024):
                    h.update(chunk)
                actual_sha = h.hexdigest()
                if actual_sha != expected_sha:
                    print(f"  FAIL  {bid_id}")
                    print(f"        sha mismatch: manifest={expected_sha[:12]}..., s3={actual_sha[:12]}...")
                    fail_count += 1
                    continue

            print(f"  OK    {bid_id}  ({actual_size} bytes)")
            ok_count += 1

        except ClientError as e:
            print(f"  FAIL  {bid_id}")
            print(f"        {e}")
            fail_count += 1

    print()
    print(f"RESULT: {ok_count}/{len(bidsets)} reachable" + (
        f", {fail_count} failed" if fail_count else ""
    ))
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
