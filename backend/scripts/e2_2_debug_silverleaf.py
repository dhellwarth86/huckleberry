"""E.2.2 Debug module output verification — Silverleaf.

Runs dispatch in-process (no HTTP), captures ctx, calls run_debug(ctx),
writes structured output to E2_2_DEBUG_silverleaf.md, and compares
against the D.2 calibration baseline.

Per MARCH_ORDERS_E_2_2_frontend_connect_and_hard_gate.md §11.

Usage:
    cd backend
    python scripts/e2_2_debug_silverleaf.py
"""
from __future__ import annotations

import sys
import time
import traceback
from pathlib import Path

HERE = Path(__file__).resolve()
BACKEND = HERE.parent.parent
sys.path.insert(0, str(BACKEND))

from core.dispatch_gate import run_dispatch  # noqa: E402
from core.debug_module import run_debug  # noqa: E402

PDF_PATH = Path(r"C:\huck stage 2\full bid sets\B2607 AEA Silverleaf - St Augustine - Accelerated Construction Services (6).pdf")
OUT_PATH = BACKEND / "E2_2_DEBUG_silverleaf.md"

# D.2 calibration baseline (from D2_REFERENCE_silverleaf.md)
BASELINE_PAGES = 40
BASELINE_ROOFING_FIELDS = 338
BASELINE_GLAZING_TOTAL = 107  # 20 glazing + 81 door + 6 storefront
TOLERANCE = 0.05  # ±5%


def main() -> int:
    if not PDF_PATH.exists():
        print(f"ERROR: PDF not found at {PDF_PATH}", file=sys.stderr)
        return 3

    # Step 1: dispatch (in-process, no job_id — not persisted)
    print(f"[e2.2-debug] run_dispatch starting (no job_id)...", flush=True)
    t0 = time.time()
    try:
        ctx = run_dispatch(str(PDF_PATH), storage="auto")
    except Exception:
        print(f"[e2.2-debug] DISPATCH RAISED:", file=sys.stderr)
        traceback.print_exc()
        return 3
    elapsed = time.time() - t0
    print(f"[e2.2-debug] dispatch complete in {elapsed:.1f}s", flush=True)

    # Step 2: run debug module
    print(f"[e2.2-debug] running debug module...", flush=True)
    try:
        debug_ctx = run_debug(ctx, geometry_results=None)
    except Exception:
        print(f"[e2.2-debug] run_debug RAISED:", file=sys.stderr)
        traceback.print_exc()
        return 4
    print(f"[e2.2-debug] debug module complete", flush=True)

    # Step 3: aggregate numbers
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
    glazing_total = g_items + d_items + s_items

    # Step 4: per-page table (ctx.pages is a dict keyed by page index)
    page_rows = []
    page_type_counts = {}
    for idx, pg in sorted(ctx.pages.items()):
        pt_raw = pg.page_type if hasattr(pg, "page_type") else None
        page_type = pt_raw.name if hasattr(pt_raw, "name") else str(pt_raw) if pt_raw else "UNKNOWN"
        page_type_counts[page_type] = page_type_counts.get(page_type, 0) + 1
        r_count = 0
        g_count = 0
        if idx in ctx.trade_module_outputs:
            per_page = ctx.trade_module_outputs[idx]
            if "roofing" in per_page:
                r_out = per_page["roofing"]
                r_count = len(r_out.fields) if hasattr(r_out, "fields") else 0
            if "glazing" in per_page:
                g_out = per_page["glazing"]
                g_count = (len(g_out.glazing_items or []) if hasattr(g_out, "glazing_items") else 0) + \
                          (len(g_out.door_items or []) if hasattr(g_out, "door_items") else 0) + \
                          (len(g_out.storefront_items or []) if hasattr(g_out, "storefront_items") else 0)
        sheet_num = pg.sheet_number or "—"
        page_rows.append((idx, sheet_num, page_type, r_count, g_count))

    # Step 5: debug module sections
    sec1_lines = []
    if debug_ctx.dispatch_health:
        for k, v in debug_ctx.dispatch_health.items():
            sec1_lines.append(f"- **{k}:** {v}")
    sec1_text = "\n".join(sec1_lines) if sec1_lines else "(empty)"

    sec3_lines = []
    if debug_ctx.page_intelligence:
        for entry in debug_ctx.page_intelligence:
            if isinstance(entry, dict):
                sec3_lines.append(f"- page {entry.get('page_idx', '?')}: {entry.get('page_type', '?')} (sheet: {entry.get('sheet_num', '?')})")
            else:
                sec3_lines.append(f"- {entry}")
    sec3_text = "\n".join(sec3_lines) if sec3_lines else "(empty)"

    sec6_lines = []
    if debug_ctx.legend_contents:
        for entry in debug_ctx.legend_contents:
            if isinstance(entry, dict):
                sec6_lines.append(f"- page {entry.get('page_idx', '?')}: {entry.get('legend_count', 0)} legends")
            else:
                sec6_lines.append(f"- {entry}")
    sec6_text = "\n".join(sec6_lines) if sec6_lines else "(empty)"

    quality_flags = debug_ctx.legend_quality_flags if debug_ctx.legend_quality_flags else []
    quality_text = "\n".join(f"- {f}" for f in quality_flags) if quality_flags else "(none)"

    # Step 6: comparison verdict
    checks = []
    page_count = ctx.total_pages

    if page_count == BASELINE_PAGES:
        checks.append(f"Page count: {page_count} == {BASELINE_PAGES} — PASS")
    else:
        checks.append(f"Page count: {page_count} != {BASELINE_PAGES} — FAIL")

    r_lo = BASELINE_ROOFING_FIELDS * (1 - TOLERANCE)
    r_hi = BASELINE_ROOFING_FIELDS * (1 + TOLERANCE)
    if r_lo <= r_fields <= r_hi:
        checks.append(f"Roofing fields: {r_fields} within ±5% of {BASELINE_ROOFING_FIELDS} ({r_lo:.0f}–{r_hi:.0f}) — PASS")
    else:
        checks.append(f"Roofing fields: {r_fields} OUTSIDE ±5% of {BASELINE_ROOFING_FIELDS} ({r_lo:.0f}–{r_hi:.0f}) — FAIL")

    g_lo = BASELINE_GLAZING_TOTAL * (1 - TOLERANCE)
    g_hi = BASELINE_GLAZING_TOTAL * (1 + TOLERANCE)
    if g_lo <= glazing_total <= g_hi:
        checks.append(f"Glazing total: {glazing_total} within ±5% of {BASELINE_GLAZING_TOTAL} ({g_lo:.0f}–{g_hi:.0f}) — PASS")
    else:
        checks.append(f"Glazing total: {glazing_total} OUTSIDE ±5% of {BASELINE_GLAZING_TOTAL} ({g_lo:.0f}–{g_hi:.0f}) — FAIL")

    has_roof_plan = page_type_counts.get("ROOF_PLAN", 0) > 0
    if has_roof_plan:
        checks.append(f"ROOF_PLAN pages: {page_type_counts.get('ROOF_PLAN', 0)} — PASS")
    else:
        checks.append("ROOF_PLAN pages: 0 — FAIL (expected at least 1)")

    has_errors = False
    if debug_ctx.dispatch_health:
        for k, v in debug_ctx.dispatch_health.items():
            if isinstance(v, str) and "ERROR" in v.upper():
                has_errors = True
    if not has_errors:
        checks.append("Section 1 ERROR markers: none — PASS")
    else:
        checks.append("Section 1 ERROR markers: FOUND — FAIL")

    all_pass = all("PASS" in c for c in checks)
    verdict = "PASS" if all_pass else "FAIL"

    # Step 7: write report
    page_table_rows = "\n".join(
        f"| {idx} | {sn} | {pt} | {rc} | {gc} |"
        for idx, sn, pt, rc, gc in page_rows
    )
    page_type_summary = ", ".join(f"{k}: {v}" for k, v in sorted(page_type_counts.items()))

    md = f"""# E.2.2 Debug Module Output — Silverleaf

**Date:** {time.strftime('%Y-%m-%d')}
**Script:** `backend/scripts/e2_2_debug_silverleaf.py`
**PDF:** `{PDF_PATH}`
**Dispatch wall-clock:** {elapsed:.1f}s

## Summary

| Metric | Value |
|---|---|
| Total pages | {page_count} |
| Roofing fields | {r_fields} |
| Glazing items | {g_items} |
| Door items | {d_items} |
| Storefront items | {s_items} |
| Glazing total | {glazing_total} |
| Page type distribution | {page_type_summary} |
| Dispatch warnings | {len(ctx.dispatch_warnings)} |

## Per-page table

| page_idx | sheet_num | page_type | roofing_items | glazing_items |
|---|---|---|---|---|
{page_table_rows}

## Section 1 — Dispatch health

{sec1_text}

## Section 3 — Page intelligence

{sec3_text}

## Section 6 — Legends + quality flags

### Legend contents
{sec6_text}

### Quality flags
{quality_text}

## Sections 2/4/5 — Stub markers

- Section 2 (Scale comparison): stubbed (pending scale-engine route)
- Section 4 (Cross-reference graph): stubbed (pending networkx + sheet-index)
- Section 5 (Geometry diagnostics): stubbed (pending geometry_results from Stages 6–9)

## Comparison verdict

Baseline: D2_REFERENCE_silverleaf.md (dispatch {BASELINE_PAGES} pages, {BASELINE_ROOFING_FIELDS} roofing, {BASELINE_GLAZING_TOTAL} glazing total)

{chr(10).join('- ' + c for c in checks)}

**Verdict: {verdict}**
"""
    OUT_PATH.write_text(md.strip() + "\n", encoding="utf-8")
    print(f"[e2.2-debug] wrote {OUT_PATH}", flush=True)
    print(f"[e2.2-debug] Verdict: {verdict}", flush=True)
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
