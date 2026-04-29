"""run_dispatch_on_public_corpus.py — Public-corpus observation sweep.

Minimal modification of `run_dispatch_on_15_bidsets.py`:
  - Reads 4 hand-listed PDFs from C:/huck stage 2/not_stack-bidsets/ (no manifest)
  - Writes outputs to backend/test_fixtures/public_corpus_outputs/
  - Same try/except wrapper, same per-bidset summary, same corpus rollup,
    same filter-order audit

DOES NOT modify any ported TracePoint code. DOES NOT compare to STACK
outputs. This is observation only.

Usage:
    cd backend
    .venv/Scripts/python.exe -u scripts/run_dispatch_on_public_corpus.py
    .venv/Scripts/python.exe -u scripts/run_dispatch_on_public_corpus.py --only suwannee-county-school-board-suwannee-high-school-courtyard-renovation
    .venv/Scripts/python.exe -u scripts/run_dispatch_on_public_corpus.py --resume   # skip bidsets whose output already exists
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import traceback
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from core.dispatch_gate import run_dispatch  # noqa: E402

PUBLIC_CORPUS_DIR = Path("C:/huck stage 2/not_stack-bidsets")
OUTPUTS_DIR = BACKEND_DIR / "test_fixtures" / "public_corpus_outputs"

# Hand-listed bidsets — no manifest file. Daniel's brief: 4 PDFs at the
# fixed path, non-STACK producers.
BIDSETS = [
    {
        "id": "suwannee-county-school-board-suwannee-high-school-courtyard-renovation",
        "filename": "suwannee county school board suwannee high school courtyard renovation.pdf",
        "page_count": 31,
        "producer_hint": "Adobe Acrobat 9.4.1 / AutoCAD Architecture 2012",
    },
    {
        "id": "holabird-academy-elementary-middle-school",
        "filename": "Holabird academy elementary-middle school.pdf",
        "page_count": 96,
        "producer_hint": "Bluebeam Brewery 5.0 / Stapler 2016.5.2",
    },
    {
        "id": "sanibel-fire-and-rescue-station-172",
        "filename": "Sanibel Fire and Rescue station 172.pdf",
        "page_count": 90,
        "producer_hint": "Bluebeam Brewery 5.0 / Stapler 21.0.50.11",
    },
    {
        "id": "uccs-cybersecurity-and-space-ecosystem-expansion",
        "filename": "UCCS cybersecurity and space ecosystem expansion.pdf",
        "page_count": 133,
        "producer_hint": "Bluebeam PDF Library 20 / Revu x64",
    },
]


def write_output_json(bidset_id: str, ctx_json_str: str) -> Path:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUTS_DIR / f"{bidset_id}.json"
    tmp = out_path.with_suffix(".json.tmp")
    tmp.write_text(ctx_json_str, encoding="utf-8")
    tmp.replace(out_path)
    return out_path


def page_type_histogram(pages: dict) -> dict[str, int]:
    hist: dict[str, int] = {}
    for pc in pages.values():
        t = pc.get("page_type", "unknown")
        hist[t] = hist.get(t, 0) + 1
    return hist


def per_bidset_summary(entry: dict, ctx_data: dict, elapsed: float) -> dict:
    bidset_id = entry["id"]
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

    print(f"  [done] {bidset_id}  ({elapsed:.1f}s, {len(pages)}p)")
    print(f"         filename:        {entry['filename']}")
    print(f"         producer_hint:   {entry['producer_hint']}")
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
        "filename": entry["filename"],
        "producer_hint": entry["producer_hint"],
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
        "warnings": warnings,
        "dispatch_complete": dispatch_complete,
        "filters_completed": filters_completed,
    }


def corpus_summary(rolls: list[dict], failures: list[dict], total_elapsed: float):
    n_ok = len(rolls)
    n_fail = len(failures)
    print()
    print("=" * 72)
    print(f"PUBLIC CORPUS SUMMARY — {n_ok} ok, {n_fail} failed, total {total_elapsed:.1f}s")
    print("=" * 72)

    if n_ok:
        with_system = [r for r in rolls if r["detected_system"]]
        empty_scope = [r for r in rolls if r["scope_pages_count"] == 0]

        print(f"Bidsets with detected_system: {len(with_system)}/{n_ok}")
        for r in with_system:
            print(f"    {r['id']:<70} {r['detected_system']!r} (conf {r['system_confidence']:.2f})")
        print(f"Bidsets with empty scope:     {len(empty_scope)}/{n_ok}")
        for r in empty_scope:
            print(f"    {r['id']}")

        # sheet_map_source distribution
        sources: dict[str, int] = {}
        for r in rolls:
            sources[r["sheet_map_source"]] = sources.get(r["sheet_map_source"], 0) + 1
        print(f"\nsheet_map_source distribution:")
        for s, c in sorted(sources.items(), key=lambda kv: -kv[1]):
            print(f"    {s:<22} {c}")

        # Filter-order audit (preserved from STACK sweep)
        EXPECTED = ["filter_1", "filter_2", "filter_4", "filter_3", "filter_5"]
        bad = [r for r in rolls if r["filters_completed"] != EXPECTED]
        if bad:
            print(f"\nFilter-order audit: {len(bad)} bidsets do NOT match {EXPECTED}")
            for r in bad:
                print(f"    {r['id']:<70} {r['filters_completed']}")
        else:
            print(f"\nFilter-order audit: {n_ok}/{n_ok} match {EXPECTED}  OK")

    if n_fail:
        print(f"\nFAILURES:")
        for f in failures:
            print(f"    {f['id']:<70} {f['error_type']}: {f['error_msg'][:80]}")
            if f.get("traceback"):
                # Print first few lines of traceback for D-ticket evidence
                tb_lines = f["traceback"].splitlines()
                for line in tb_lines[-6:]:
                    print(f"        {line}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", action="append", help="Process only this bidset id (can repeat)")
    parser.add_argument("--resume", action="store_true", help="Skip bidsets whose output already exists")
    parser.add_argument("--limit", type=int, default=None, help="Process at most N bidsets")
    args = parser.parse_args()

    bidsets = list(BIDSETS)
    if args.only:
        wanted = set(args.only)
        bidsets = [b for b in bidsets if b["id"] in wanted]
    if args.limit:
        bidsets = bidsets[: args.limit]

    print(f"Public-corpus dispatch sweep — processing {len(bidsets)} bidset(s)")
    print(f"Source PDFs:    {PUBLIC_CORPUS_DIR}")
    print(f"Outputs go to:  {OUTPUTS_DIR}")
    print()

    rolls: list[dict] = []
    failures: list[dict] = []
    t_corpus_start = time.time()

    for entry in bidsets:
        bidset_id = entry["id"]
        local_path = PUBLIC_CORPUS_DIR / entry["filename"]
        out_path = OUTPUTS_DIR / f"{bidset_id}.json"

        if args.resume and out_path.exists():
            print(f"  [skip] {bidset_id}  (output exists)")
            continue

        if not local_path.is_file():
            print(f"  [miss] {bidset_id}  (not on disk: {local_path})")
            failures.append({
                "id": bidset_id,
                "error_type": "FileNotFoundError",
                "error_msg": str(local_path),
                "traceback": "",
            })
            continue

        print(f"  [run]  {bidset_id}  ({entry['filename']}, {entry.get('page_count', '?')} pp)")
        t0 = time.time()
        try:
            ctx = run_dispatch(str(local_path))
            elapsed = time.time() - t0
            ctx_json_str = ctx.to_json()
            ctx_data = json.loads(ctx_json_str)
            write_output_json(bidset_id, ctx_json_str)
            rolls.append(per_bidset_summary(entry, ctx_data, elapsed))
        except Exception as e:
            elapsed = time.time() - t0
            tb = traceback.format_exc()
            print(f"  [FAIL] {bidset_id}  after {elapsed:.1f}s — {type(e).__name__}: {e}")
            print(tb)
            failures.append({
                "id": bidset_id,
                "error_type": type(e).__name__,
                "error_msg": str(e),
                "traceback": tb,
            })

        print()

    corpus_summary(rolls, failures, time.time() - t_corpus_start)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
