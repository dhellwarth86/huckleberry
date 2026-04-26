"""run_dispatch_on_15_bidsets.py — Phase 2 v0.2 Step 16 sweep.

Iterates over the 15 PDFs in C:\\huck stage 2\\full bid sets\\ (read from
backend/test_fixtures/bidsets.json so ids and paths match v0.1's manifest),
calls run_dispatch(pdf_path) from core.dispatch_gate, serializes
ctx.to_json() to backend/test_fixtures/v0.2_outputs/<bidset_id>.json,
and prints per-bidset and corpus-level summaries.

Each bidset is wrapped in try/except so a single crash does NOT halt the
sweep. Crashes are logged and counted; sweep continues with the next PDF.

Per Step 16 brief: do NOT compare to v0.1 outputs here — that's Step 17.

Usage:
    cd backend
    .venv/Scripts/python.exe -u scripts/run_dispatch_on_15_bidsets.py
    .venv/Scripts/python.exe -u scripts/run_dispatch_on_15_bidsets.py --only chipotle-tarpon-springs-shell-tarpon-springs-strategic-construction
    .venv/Scripts/python.exe -u scripts/run_dispatch_on_15_bidsets.py --resume   # skip bidsets whose v0.2 output already exists
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import traceback
from pathlib import Path

# Make `core.<...>` and `seeds.<...>` importable when run from backend/
BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from core.dispatch_gate import run_dispatch  # noqa: E402

MANIFEST_PATH = BACKEND_DIR / "test_fixtures" / "bidsets.json"
V02_OUTPUTS_DIR = BACKEND_DIR / "test_fixtures" / "v0.2_outputs"


def load_bidsets() -> list[dict]:
    """Read the manifest produced by v0.1's local_manifest.py. Same ids and
    local_paths so v0.2 outputs align 1:1 with v0.1 outputs for Step 17."""
    if not MANIFEST_PATH.exists():
        print(f"ERROR: manifest not found at {MANIFEST_PATH}", file=sys.stderr)
        print("       Re-run scripts/local_manifest.py first.", file=sys.stderr)
        sys.exit(2)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return manifest.get("bidsets", [])


def write_output_json(bidset_id: str, ctx_json_str: str) -> Path:
    """Atomic write: <id>.json.tmp -> rename to <id>.json."""
    V02_OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = V02_OUTPUTS_DIR / f"{bidset_id}.json"
    tmp = out_path.with_suffix(".json.tmp")
    tmp.write_text(ctx_json_str, encoding="utf-8")
    tmp.replace(out_path)
    return out_path


def page_type_histogram(pages: dict) -> dict[str, int]:
    """Count pages by page_type. `pages` is the dict from ctx.to_json() -> 'pages'."""
    hist: dict[str, int] = {}
    for pc in pages.values():
        t = pc.get("page_type", "unknown")
        hist[t] = hist.get(t, 0) + 1
    return hist


def per_bidset_summary(bidset_id: str, filename: str, ctx_data: dict, elapsed: float) -> dict:
    """Print a per-bidset summary line and return a dict for corpus-level rollup."""
    pages = ctx_data.get("pages", {})
    sheet_map_source = ctx_data.get("sheet_map_source", "none")
    cross_refs = ctx_data.get("all_cross_refs", [])
    resolved = sum(1 for r in cross_refs if r.get("resolved"))
    total_refs = len(cross_refs)
    resolved_pct = (100.0 * resolved / total_refs) if total_refs else 0.0
    legends = ctx_data.get("all_legends", [])
    hist = page_type_histogram(pages)
    project_scope = ctx_data.get("project_scope")
    detected_system = (project_scope or {}).get("detected_system")
    system_conf = (project_scope or {}).get("system_confidence", 0.0)
    scope_pages_count = len((project_scope or {}).get("scope_pages", []) or [])
    warnings = ctx_data.get("dispatch_warnings", [])
    filters_completed = ctx_data.get("filters_completed", [])
    dispatch_complete = ctx_data.get("dispatch_complete", False)

    # Compact one-liner first, then a detail block
    print(f"  [done] {bidset_id}  ({elapsed:.1f}s, {len(pages)}p)")
    print(f"         filename:        {filename}")
    print(f"         dispatch_done:   {dispatch_complete}")
    print(f"         filters:         {filters_completed}")
    print(f"         sheet_map:       source={sheet_map_source}  count={len(ctx_data.get('sheet_map', {}))}")
    print(f"         cross_refs:      {total_refs} total, {resolved} resolved ({resolved_pct:.0f}%)")
    print(f"         legends:         {len(legends)} total")
    top_types = sorted(hist.items(), key=lambda kv: -kv[1])[:6]
    print(f"         page_types:      " + ", ".join(f"{t}={c}" for t, c in top_types))
    print(f"         project_scope:   detected_system={detected_system!r} conf={system_conf:.2f} scope_pages={scope_pages_count}")
    if warnings:
        print(f"         warnings({len(warnings)}):")
        for w in warnings[:5]:
            print(f"             - {w}")
        if len(warnings) > 5:
            print(f"             - ... and {len(warnings) - 5} more")

    return {
        "id": bidset_id,
        "elapsed_s": elapsed,
        "pages": len(pages),
        "sheet_map_count": len(ctx_data.get("sheet_map", {})),
        "sheet_map_source": sheet_map_source,
        "cross_refs_total": total_refs,
        "cross_refs_resolved": resolved,
        "cross_refs_resolved_pct": resolved_pct,
        "legends_total": len(legends),
        "page_type_histogram": hist,
        "detected_system": detected_system,
        "system_confidence": system_conf,
        "scope_pages_count": scope_pages_count,
        "warning_count": len(warnings),
        "dispatch_complete": dispatch_complete,
        "filters_completed": filters_completed,
    }


def corpus_summary(rolls: list[dict], failures: list[dict], total_elapsed: float):
    n_ok = len(rolls)
    n_fail = len(failures)
    print()
    print("=" * 72)
    print(f"CORPUS SUMMARY — {n_ok} ok, {n_fail} failed, total {total_elapsed:.1f}s")
    print("=" * 72)

    if n_ok:
        total_pages = sum(r["pages"] for r in rolls)
        total_refs = sum(r["cross_refs_total"] for r in rolls)
        total_resolved = sum(r["cross_refs_resolved"] for r in rolls)
        total_legends = sum(r["legends_total"] for r in rolls)
        with_system = [r for r in rolls if r["detected_system"]]
        empty_scope = [r for r in rolls if r["scope_pages_count"] == 0]

        # Aggregate page_type histogram
        agg_hist: dict[str, int] = {}
        for r in rolls:
            for t, c in r["page_type_histogram"].items():
                agg_hist[t] = agg_hist.get(t, 0) + c

        print(f"Pages processed:          {total_pages:,}")
        print(f"Cross-refs:               {total_refs:,} total, {total_resolved:,} resolved ({100.0*total_resolved/total_refs if total_refs else 0:.0f}%)")
        print(f"Legends total:            {total_legends:,}")
        print(f"Bidsets with detected_system: {len(with_system)}/{n_ok}")
        if with_system:
            sys_counts: dict[str, int] = {}
            for r in with_system:
                sys_counts[r["detected_system"]] = sys_counts.get(r["detected_system"], 0) + 1
            for s, c in sorted(sys_counts.items(), key=lambda kv: -kv[1]):
                print(f"    {s:<25} {c}")
        print(f"Bidsets with empty scope: {len(empty_scope)}/{n_ok}")
        for r in empty_scope:
            print(f"    {r['id']}  (system={r['detected_system']!r}, scope_pages={r['scope_pages_count']})")

        print(f"\nPage-type distribution (corpus-wide):")
        for t, c in sorted(agg_hist.items(), key=lambda kv: -kv[1]):
            print(f"    {t:<22} {c:>6}")

        # Filter-order audit per orders ("filter_4 before filter_3 by design")
        EXPECTED = ["filter_1", "filter_2", "filter_4", "filter_3", "filter_5"]
        bad = [r for r in rolls if r["filters_completed"] != EXPECTED]
        if bad:
            print(f"\nFilter-order audit: {len(bad)} bidsets do NOT match {EXPECTED}")
            for r in bad:
                print(f"    {r['id']:<60} {r['filters_completed']}")
        else:
            print(f"\nFilter-order audit: {n_ok}/{n_ok} match {EXPECTED}  OK")

    if n_fail:
        print(f"\nFAILURES:")
        for f in failures:
            print(f"    {f['id']:<60} {f['error_type']}: {f['error_msg'][:80]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", action="append", help="Process only this bidset id (can repeat)")
    parser.add_argument("--resume", action="store_true", help="Skip bidsets whose v0.2 output already exists")
    parser.add_argument("--limit", type=int, default=None, help="Process at most N bidsets")
    args = parser.parse_args()

    bidsets = load_bidsets()
    if args.only:
        wanted = set(args.only)
        bidsets = [b for b in bidsets if b["id"] in wanted]
    if args.limit:
        bidsets = bidsets[: args.limit]

    print(f"Phase 2 v0.2 Step 16 sweep — processing {len(bidsets)} bidset(s)")
    print(f"Outputs go to {V02_OUTPUTS_DIR}")
    print()

    rolls: list[dict] = []
    failures: list[dict] = []
    t_corpus_start = time.time()

    for entry in bidsets:
        bidset_id = entry["id"]
        local_path = entry.get("local_path", "")
        filename = entry.get("filename", Path(local_path).name)
        out_path = V02_OUTPUTS_DIR / f"{bidset_id}.json"

        if args.resume and out_path.exists():
            print(f"  [skip] {bidset_id}  (output exists)")
            continue

        if not Path(local_path).is_file():
            print(f"  [miss] {bidset_id}  (local_path not on disk: {local_path})")
            failures.append({
                "id": bidset_id,
                "error_type": "FileNotFoundError",
                "error_msg": local_path,
            })
            continue

        print(f"  [run]  {bidset_id}  ({filename}, {entry.get('page_count', '?')} pp)")
        t0 = time.time()
        try:
            ctx = run_dispatch(local_path)
            elapsed = time.time() - t0
            ctx_json_str = ctx.to_json()
            ctx_data = json.loads(ctx_json_str)
            write_output_json(bidset_id, ctx_json_str)
            rolls.append(per_bidset_summary(bidset_id, filename, ctx_data, elapsed))
        except Exception as e:
            elapsed = time.time() - t0
            print(f"  [FAIL] {bidset_id}  after {elapsed:.1f}s — {type(e).__name__}: {e}")
            traceback.print_exc()
            failures.append({
                "id": bidset_id,
                "error_type": type(e).__name__,
                "error_msg": str(e),
            })

        print()

    corpus_summary(rolls, failures, time.time() - t_corpus_start)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
