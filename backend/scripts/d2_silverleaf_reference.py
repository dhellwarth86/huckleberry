"""D.2 Silverleaf reference run — create a persistent job and run dispatch.

Per MARCH_ORDERS_D2_long_run.md §3.5.

Usage:
    python backend/scripts/d2_silverleaf_reference.py
"""
from __future__ import annotations

import sys
import time
import traceback
from pathlib import Path

HERE = Path(__file__).resolve()
BACKEND = HERE.parent.parent
sys.path.insert(0, str(BACKEND))

from core.job_storage import create_job, get_job, update_job_status  # noqa: E402
from core.dispatch_gate import run_dispatch  # noqa: E402

PDF_PATH = Path(r"C:\huck stage 2\full bid sets\B2607 AEA Silverleaf - St Augustine - Accelerated Construction Services (6).pdf")
OUT_PATH = BACKEND / "D2_REFERENCE_silverleaf.md"


def main() -> int:
    if not PDF_PATH.exists():
        print(f"ERROR: PDF not found at {PDF_PATH}", file=sys.stderr)
        return 3

    print(f"[d2-ref] Creating job for Silverleaf...", flush=True)
    job_id = create_job(
        name="B2607 AEA Silverleaf",
        pdf_path=str(PDF_PATH),
        gc="Accelerated Construction Services",
        location_city="St Augustine",
        location_state="FL",
        trade_scope="roofing,glazing",
        status="draft",
    )
    print(f"[d2-ref] job_id = {job_id}", flush=True)

    print(f"[d2-ref] run_dispatch starting (storage='auto', job_id={job_id})...", flush=True)
    t0 = time.time()
    try:
        ctx = run_dispatch(str(PDF_PATH), storage="auto", job_id=job_id)
    except Exception:
        print(f"[d2-ref] DISPATCH RAISED:", file=sys.stderr)
        traceback.print_exc()
        return 3
    elapsed = time.time() - t0
    print(f"[d2-ref] dispatch complete in {elapsed:.1f}s", flush=True)

    update_job_status(job_id, "dispatched")
    print(f"[d2-ref] job status updated to 'dispatched'", flush=True)

    job = get_job(job_id)
    if job is None:
        print(f"[d2-ref] ERROR: get_job returned None", file=sys.stderr)
        return 4

    # Aggregate module output for report
    r_fields = 0
    g_items = 0
    d_items = 0
    s_items = 0
    for per_page in ctx.trade_module_outputs.values():
        if "roofing" in per_page:
            out = per_page["roofing"]
            r_fields += len(out.fields) if hasattr(out, "fields") else 0
        if "glazing" in per_page:
            out = per_page["glazing"]
            g_items += len(out.glazing_items or []) if hasattr(out, "glazing_items") else 0
            d_items += len(out.door_items or []) if hasattr(out, "door_items") else 0
            s_items += len(out.storefront_items or []) if hasattr(out, "storefront_items") else 0

    md = f"""# D.2 Reference Run — Silverleaf

**Date:** {time.strftime('%Y-%m-%d')}
**Branch:** `phase2-v0.3-D2-job-folder-and-persistence`
**Job ID:** `{job_id}`
**PDF:** `{PDF_PATH}`
**Dispatch wall-clock:** {elapsed:.1f}s

## Job metadata

| Field | Value |
|---|---|
| name | {job['name']} |
| gc | {job['gc']} |
| location_city | {job['location_city']} |
| location_state | {job['location_state']} |
| trade_scope | {job['trade_scope']} |
| status | {job['status']} |
| pdf_sha1 | `{job['pdf_sha1']}` |
| dispatch_complete | {job['dispatch_complete']} |
| created_at | {job['created_at']} |

## Module output (from ctx.trade_module_outputs)

- Roofing fields: {r_fields}
- Glazing items: {g_items}
- Door items: {d_items}
- Storefront items: {s_items}
- Total pages with trade output: {len(ctx.trade_module_outputs)}

## Dispatch summary

- total_pages: {ctx.total_pages}
- filters_completed: {ctx.filters_completed}
- dispatch_complete: {ctx.dispatch_complete}
- dispatch_warnings: {len(ctx.dispatch_warnings)}

**Reference run complete. Job ID for soft gate: `{job_id}`**
"""
    OUT_PATH.write_text(md.strip() + "\n", encoding="utf-8")
    print(f"[d2-ref] wrote {OUT_PATH}", flush=True)
    print(f"[d2-ref] Job ID: {job_id}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
