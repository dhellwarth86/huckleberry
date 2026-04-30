"""D.2 soft gate — persistence round-trip verification on Silverleaf.

Per MARCH_ORDERS_D2_long_run.md §4.

Reads the Silverleaf job_id from D2_REFERENCE_silverleaf.md, closes and
reopens the storage handle (simulates session end/start), runs 10 round-trip
assertions.

Usage:
    python backend/scripts/d2_persistence_soft_gate.py
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve()
BACKEND = HERE.parent.parent
sys.path.insert(0, str(BACKEND))

from core.job_storage import get_job, load_dispatch_results, load_trade_outputs  # noqa: E402

REF_PATH = BACKEND / "D2_REFERENCE_silverleaf.md"
OUT_PATH = BACKEND / "D2_SOFT_GATE_silverleaf.md"


def _extract_job_id(ref_path: Path) -> str | None:
    text = ref_path.read_text(encoding="utf-8")
    m = re.search(r'\*\*Job ID:\*\*\s*`([^`]+)`', text)
    if m:
        return m.group(1)
    m = re.search(r'Job ID for soft gate:\s*`([^`]+)`', text)
    if m:
        return m.group(1)
    return None


def run_soft_gate() -> int:
    if not REF_PATH.exists():
        print(f"ERROR: {REF_PATH} not found — run d2_silverleaf_reference.py first", file=sys.stderr)
        return 3

    job_id = _extract_job_id(REF_PATH)
    if not job_id:
        print(f"ERROR: could not extract job_id from {REF_PATH}", file=sys.stderr)
        return 3

    print(f"[soft-gate] Job ID: {job_id}", flush=True)

    results: list[tuple[int, str, bool, str]] = []

    # 1. get_job returns non-None
    job = get_job(job_id)
    ok1 = job is not None
    results.append((1, "get_job returns non-None", ok1, f"returned {'dict with id=' + job['id'] if job else 'None'}"))

    if not ok1:
        print(f"[soft-gate] FATAL: get_job returned None — cannot proceed", file=sys.stderr)
        _write_report(job_id, results)
        return 5

    # 2. name == "B2607 AEA Silverleaf"
    ok2 = job["name"] == "B2607 AEA Silverleaf"
    results.append((2, 'name == "B2607 AEA Silverleaf"', ok2, f"actual: {job['name']!r}"))

    # 3. gc == "Accelerated Construction Services"
    ok3 = job["gc"] == "Accelerated Construction Services"
    results.append((3, 'gc == "Accelerated Construction Services"', ok3, f"actual: {job['gc']!r}"))

    # 4. trade_scope contains both trades
    ts = job.get("trade_scope", "")
    ok4 = "roofing" in ts and "glazing" in ts
    results.append((4, "trade_scope contains both trades", ok4, f"actual: {ts!r}"))

    # 5. dispatch_results has 40 page entries
    dr = load_dispatch_results(job_id)
    ok5 = len(dr) == 40
    results.append((5, "dispatch_results has 40 page entries", ok5, f"actual: {len(dr)}"))

    # 6. 18 pages classified schedule_sheet
    schedule_count = sum(1 for d in dr.values() if d.get("page_type") == "schedule_sheet")
    ok6 = schedule_count == 18
    results.append((6, "18 pages classified schedule_sheet", ok6, f"actual: {schedule_count}"))

    # 7. >= 18 pages with raw_tables_json
    tables_count = sum(1 for d in dr.values() if d.get("raw_tables_json") or d.get("raw_tables"))
    ok7 = tables_count >= 18
    results.append((7, ">= 18 pages with raw_tables_json", ok7, f"actual: {tables_count}"))

    # 8. trade_outputs has 40 page keys
    to = load_trade_outputs(job_id)
    ok8 = len(to) == 40
    results.append((8, "trade_outputs has 40 page keys", ok8, f"actual: {len(to)}"))

    # 9. Roofing fields aggregate == 338
    r_fields = 0
    for page_data in to.values():
        roofing = page_data.get("roofing", {})
        r_fields += len(roofing.get("fields", {}))
    ok9 = r_fields == 338
    results.append((9, "Roofing fields aggregate == 338", ok9, f"actual: {r_fields}"))

    # 10. Glazing items aggregate == 107 (20 + 81 + 6)
    g_total = 0
    g_items = 0
    d_items = 0
    s_items = 0
    for page_data in to.values():
        glazing = page_data.get("glazing", {})
        gi = glazing.get("glazing_items") or []
        di = glazing.get("door_items") or []
        si = glazing.get("storefront_items") or []
        g_items += len(gi)
        d_items += len(di)
        s_items += len(si)
    g_total = g_items + d_items + s_items
    ok10 = g_total == 107
    results.append((10, "Glazing items aggregate == 107", ok10, f"actual: {g_total} ({g_items}g + {d_items}d + {s_items}s)"))

    overall = all(r[2] for r in results)
    _write_report(job_id, results)

    print(f"[soft-gate] OVERALL: {'PASS' if overall else 'FAIL'}", flush=True)
    for num, desc, ok, evidence in results:
        status = "PASS" if ok else "FAIL"
        print(f"  {num}. [{status}] {desc} — {evidence}", flush=True)

    return 0 if overall else 5


def _write_report(job_id: str, results: list[tuple[int, str, bool, str]]) -> None:
    overall = all(r[2] for r in results) if results else False
    lines = []
    a = lines.append

    a("# D.2 Soft Gate — Silverleaf Persistence Round-Trip")
    a("")
    a(f"**Date:** {time.strftime('%Y-%m-%d')}")
    a("**Branch:** `phase2-v0.3-D2-job-folder-and-persistence`")
    a(f"**Job ID:** `{job_id}`")
    a("**Database:** ~/.tracepoint/cache.db")
    a(f"**Overall:** {'PASS' if overall else 'FAIL'}")
    a("")
    a("## Round-trip assertions")
    a("")
    a("| # | Assertion | Result | Evidence |")
    a("|---|---|---|---|")
    for num, desc, ok, evidence in results:
        a(f"| {num} | {desc} | {'PASS' if ok else 'FAIL'} | {evidence} |")
    a("")
    a(f"**Overall:** {'PASS' if overall else 'FAIL'} — {'all 10 assertions PASS' if overall else 'one or more assertions FAIL'}")
    a("")

    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[soft-gate] wrote {OUT_PATH}", flush=True)


if __name__ == "__main__":
    sys.exit(run_soft_gate())
