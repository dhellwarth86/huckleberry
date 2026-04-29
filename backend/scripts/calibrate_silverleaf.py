"""Calibration harness — B2607 AEA Silverleaf.

Per MARCH_ORDERS_calibration_silverleaf.md §4. Tracked, reusable template
for future per-bidset calibration sessions.

Procedure:
    1. run_dispatch(pdf, storage=None) -> PlanSetContext (wall-clock timed)
    2. For each page in ctx.pages:
         - extract text_blocks + tables (pdfplumber)
         - build TradeModuleInput via build_trade_input() when geometry is
           available, otherwise the C.2-established direct-construction path
         - call RoofingModule().analyze(input)
         - call GlazingModule().analyze(input)
    3. run_debug(ctx) -> DebugContext
    4. Write iteration report to backend/CALIBRATION_RUN_silverleaf_iter_<N>.md

Usage:
    python backend/scripts/calibrate_silverleaf.py <iteration_number> ["description of fix"]
"""
from __future__ import annotations

import json
import sys
import time
import traceback
from collections import Counter
from dataclasses import asdict, is_dataclass
from pathlib import Path

HERE = Path(__file__).resolve()
BACKEND = HERE.parent.parent
sys.path.insert(0, str(BACKEND))

import pdfplumber  # noqa: E402

from core.dispatch_gate import run_dispatch  # noqa: E402
from core.debug_module import run_debug  # noqa: E402
from core.roofing_module import RoofingModule  # noqa: E402
from core.glazing_module import GlazingModule  # noqa: E402
from core.trade_module import TradeModuleInput, TradeModuleOutput  # noqa: E402
from core.trade_input_builder import build_trade_input  # noqa: E402

PDF_PATH = Path(r"C:\huck stage 2\full bid sets\B2607 AEA Silverleaf - St Augustine - Accelerated Construction Services (6).pdf")
BIDSET_NAME = "silverleaf"


class _TextBlock:
    __slots__ = ("text", "x0", "y0", "x1", "y1")

    def __init__(self, text, x0, y0, x1, y1):
        self.text = text
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1


def _extract_page_blocks_and_tables(pdf_page):
    text_blocks: list = []
    try:
        words = pdf_page.extract_words() or []
    except Exception:
        words = []
    for w in words:
        try:
            text_blocks.append(
                _TextBlock(
                    text=str(w.get("text", "")),
                    x0=float(w.get("x0", 0.0)),
                    y0=float(w.get("top", 0.0)),
                    x1=float(w.get("x1", 0.0)),
                    y1=float(w.get("bottom", 0.0)),
                )
            )
        except Exception:
            continue

    tables: list = []
    try:
        ext = pdf_page.extract_tables() or []
        if ext:
            tables = [t for t in ext if t]
    except Exception:
        tables = []

    return text_blocks, tables


def _build_input_for_page(ctx, page_idx, text_blocks, tables):
    page_ctx = ctx.pages.get(page_idx)
    page_type = "UNKNOWN"
    page_legends: list = []
    page_zones: list = []
    if page_ctx is not None:
        pt = getattr(page_ctx, "page_type", None)
        page_type = getattr(pt, "value", str(pt)) if pt is not None else "UNKNOWN"
        page_legends = list(page_ctx.legends or [])
        page_zones = list(page_ctx.zones or [])
    project_scope = getattr(ctx, "project_scope", None)

    return TradeModuleInput(
        polygon_area_sqin=0.0,
        polygon_area_sf=0.0,
        polygon_perimeter_in=0.0,
        polygon_perimeter_lf=0.0,
        polygon_bbox=(0.0, 0.0, 0.0, 0.0),
        polygon_vertices=0,
        scale_fpi=0.0,
        scale_source="unwired",
        scale_confidence=0.0,
        detection_source="none",
        interior_text_blocks=text_blocks,
        equipment_callouts=[],
        dimension_strings=[],
        page_type=page_type,
        page_legends=page_legends,
        page_zones=page_zones,
        tables=tables if tables else None,
        project_scope=project_scope,
        page_number=page_idx,
    )


def _output_to_dict(out: TradeModuleOutput) -> dict:
    fields_dict = {}
    for k, v in (out.fields or {}).items():
        if is_dataclass(v):
            fields_dict[k] = asdict(v)
        else:
            fields_dict[k] = v
    return {
        "fields": fields_dict,
        "warnings": list(out.warnings or []),
        "equipment_pins": list(out.equipment_pins or []),
        "glazing_items": list(out.glazing_items) if out.glazing_items is not None else None,
        "door_items": list(out.door_items) if out.door_items is not None else None,
        "storefront_items": list(out.storefront_items) if out.storefront_items is not None else None,
    }


def _serialize(obj, max_items=50):
    if obj is None:
        return None
    if isinstance(obj, dict):
        return {k: _serialize(v, max_items) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        if len(obj) > max_items:
            head = [_serialize(x, max_items) for x in obj[:max_items]]
            return head + [f"... ({len(obj) - max_items} more items truncated)"]
        return [_serialize(x, max_items) for x in obj]
    if hasattr(obj, "value") and hasattr(obj, "name"):
        return obj.value
    if is_dataclass(obj):
        try:
            return _serialize(asdict(obj), max_items)
        except Exception:
            return str(obj)
    if hasattr(obj, "__dict__"):
        try:
            return _serialize(vars(obj), max_items)
        except Exception:
            return str(obj)
    return obj


def run_calibration(iteration: int, fix_description: str) -> int:
    if not PDF_PATH.exists():
        print(f"ERROR: PDF not found at {PDF_PATH}", file=sys.stderr)
        return 3

    out_path = BACKEND / f"CALIBRATION_RUN_silverleaf_iter_{iteration}.md"

    print(f"\n{'='*60}", flush=True)
    print(f"[silverleaf] Iteration {iteration}: {fix_description}", flush=True)
    print(f"[silverleaf] PDF: {PDF_PATH}", flush=True)

    # --- 1. Dispatch ---
    print(f"[silverleaf] dispatch starting...", flush=True)
    t0 = time.time()
    try:
        ctx = run_dispatch(str(PDF_PATH), storage=None)
    except Exception:
        print(f"[silverleaf] DISPATCH RAISED — §7 stop:", file=sys.stderr)
        traceback.print_exc()
        return 3
    t_dispatch = time.time() - t0
    print(f"[silverleaf] dispatch complete in {t_dispatch:.1f}s", flush=True)

    total_pages = ctx.total_pages

    # --- 2. Per-page module runs ---
    print(f"[silverleaf] per-page module runs ({total_pages} pages)...", flush=True)
    roofing_mod = RoofingModule()
    glazing_mod = GlazingModule()

    roofing_outputs: dict[int, dict] = {}
    glazing_outputs: dict[int, dict] = {}
    per_page_errors: list[dict] = []
    pages_attempted = 0
    tables_populated_count = 0

    t1 = time.time()
    with pdfplumber.open(str(PDF_PATH)) as pdf:
        for page_idx in sorted(ctx.pages.keys()):
            if page_idx >= len(pdf.pages):
                continue
            pdf_page = pdf.pages[page_idx]
            try:
                text_blocks, tables = _extract_page_blocks_and_tables(pdf_page)
            except Exception as exc:
                per_page_errors.append({
                    "page": page_idx, "module": "extract",
                    "exception_type": type(exc).__name__,
                    "message": str(exc)[:200],
                })
                pages_attempted += 1
                continue

            tinput = _build_input_for_page(ctx, page_idx, text_blocks, tables)
            if tinput.tables:
                tables_populated_count += 1
            pages_attempted += 1

            # Roofing
            try:
                r_out = roofing_mod.analyze(tinput)
                roofing_outputs[page_idx] = _output_to_dict(r_out)
            except Exception as exc:
                per_page_errors.append({
                    "page": page_idx, "module": "roofing",
                    "exception_type": type(exc).__name__,
                    "message": str(exc)[:200],
                })

            # Glazing
            try:
                g_out = glazing_mod.analyze(tinput)
                glazing_outputs[page_idx] = _output_to_dict(g_out)
            except Exception as exc:
                per_page_errors.append({
                    "page": page_idx, "module": "glazing",
                    "exception_type": type(exc).__name__,
                    "message": str(exc)[:200],
                })

    t_modules = time.time() - t1
    print(f"[silverleaf] modules complete in {t_modules:.1f}s", flush=True)

    # --- 3. run_debug ---
    ctx.trade_contexts["roofing_per_page"] = roofing_outputs
    ctx.trade_contexts["glazing_per_page"] = glazing_outputs

    print(f"[silverleaf] run_debug...", flush=True)
    t2 = time.time()
    try:
        debug = run_debug(ctx)
    except Exception:
        print(f"[silverleaf] run_debug RAISED — §7 stop:", file=sys.stderr)
        traceback.print_exc()
        return 6
    t_debug = time.time() - t2
    print(f"[silverleaf] run_debug complete in {t_debug:.1f}s", flush=True)

    # --- 4. Format and write report ---
    md = format_report(
        iteration=iteration,
        fix_description=fix_description,
        t_dispatch=t_dispatch,
        t_modules=t_modules,
        t_debug=t_debug,
        ctx=ctx,
        debug=debug,
        roofing_outputs=roofing_outputs,
        glazing_outputs=glazing_outputs,
        per_page_errors=per_page_errors,
        pages_attempted=pages_attempted,
        tables_populated_count=tables_populated_count,
    )
    out_path.write_text(md, encoding="utf-8")
    print(f"[silverleaf] wrote {out_path} ({out_path.stat().st_size} bytes)", flush=True)
    return 0


def format_report(*, iteration, fix_description, t_dispatch, t_modules, t_debug,
                  ctx, debug, roofing_outputs, glazing_outputs, per_page_errors,
                  pages_attempted, tables_populated_count) -> str:
    ps = ctx.project_scope
    lines: list[str] = []
    a = lines.append

    a(f"# Calibration Run — Silverleaf — Iteration {iteration}")
    a("")
    a(f"**Date:** 2026-04-29")
    a(f"**Iteration:** {iteration} of max 4")
    a(f"**Fix applied this iteration:** {fix_description}")
    a(f"**Wall-clock:** dispatch {t_dispatch:.1f}s / modules {t_modules:.1f}s / debug {t_debug:.1f}s / total {t_dispatch + t_modules + t_debug:.1f}s")
    a("")

    # §1 — Dispatch output summary
    a("## §1 — Dispatch output summary")
    a("")
    if ps:
        a(f"- detected_system: `{ps.detected_system!r}` / confidence: `{ps.system_confidence}` / scope_pages: `{list(ps.scope_pages)}`")
    else:
        a("- project_scope: None")
    a(f"- dispatch_complete: `{ctx.dispatch_complete}` / filters_completed: `{ctx.filters_completed}`")
    a(f"- dispatch_warnings: `{list(ctx.dispatch_warnings)}`")
    a(f"- total_pages: `{ctx.total_pages}` / sheet_count: `{len(ctx.sheet_map)}` / mapped_pages: `{len(ctx.page_to_sheet)}`")
    a("")

    # Page-type histogram
    type_counts = Counter()
    for pc in ctx.pages.values():
        type_counts[pc.page_type.value] += 1
    a("### Page-type histogram")
    a("")
    for pt, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        a(f"- `{pt}`: {count}")
    a("")

    # Per-page type listing
    a("### Per-page type listing")
    a("")
    a("| Page | Sheet | Title | Type | Conf | has_legend | has_schedule | legend_count |")
    a("|---:|---|---|---|---:|---|---|---:|")
    for page_idx in sorted(ctx.pages.keys()):
        pc = ctx.pages[page_idx]
        sheet = pc.sheet_number or "---"
        title = (pc.title or "---")[:50]
        a(f"| {page_idx} | {sheet} | {title} | {pc.page_type.value} | {pc.confidence} | {pc.has_legend} | {pc.has_schedule} | {len(pc.legends)} |")
    a("")

    # §2 — Module output summary
    a("## §2 — Module output summary")
    a("")
    r_fields = sum(len(d.get("fields", {})) for d in roofing_outputs.values())
    r_warnings = sum(len(d.get("warnings", [])) for d in roofing_outputs.values())
    r_nonempty = sum(1 for d in roofing_outputs.values() if d.get("fields") or d.get("warnings") or d.get("equipment_pins"))
    a(f"- Roofing: {r_nonempty} pages with content, {r_fields} total fields, {r_warnings} total warnings")

    g_items = sum(len(d.get("glazing_items", []) or []) for d in glazing_outputs.values())
    d_items = sum(len(d.get("door_items", []) or []) for d in glazing_outputs.values())
    s_items = sum(len(d.get("storefront_items", []) or []) for d in glazing_outputs.values())
    g_nonempty = sum(1 for d in glazing_outputs.values()
                     if (d.get("glazing_items") or d.get("door_items") or d.get("storefront_items")))
    a(f"- Glazing: {g_nonempty} pages with content, {g_items} glazing / {d_items} door / {s_items} storefront items")
    a(f"- Tables populated on TradeModuleInput: {tables_populated_count} of {pages_attempted} pages")
    a(f"- Per-page errors: {len(per_page_errors)}")
    a("")

    # §3 — Debug section 1 / 3 / 6 highlights
    a("## §3 — Debug section 1 / 3 / 6 highlights")
    a("")

    a("### Section 1 — dispatch_health")
    a("")
    a("```json")
    a(json.dumps(_serialize(debug.dispatch_health), indent=2, default=str))
    a("```")
    a("")

    # Section 3 summary
    if isinstance(debug.page_intelligence, list):
        sec3_types = Counter()
        sec3_has_legend = 0
        for entry in debug.page_intelligence:
            sec3_types[entry.get("type", "unknown")] += 1
            if entry.get("has_legend"):
                sec3_has_legend += 1
        a(f"### Section 3 — page_intelligence ({len(debug.page_intelligence)} entries)")
        a("")
        a("Type distribution:")
        for t, c in sorted(sec3_types.items(), key=lambda x: -x[1]):
            a(f"- `{t}`: {c}")
        a(f"- has_legend pages: {sec3_has_legend}")
    a("")

    # Section 6
    legend_count = len(debug.legend_contents) if isinstance(debug.legend_contents, list) else 0
    flag_count = len(debug.legend_quality_flags) if isinstance(debug.legend_quality_flags, list) else 0
    a(f"### Section 6 — legends: {legend_count}, quality_flags: {flag_count}")
    a("")
    if flag_count > 0 and isinstance(debug.legend_quality_flags, list):
        a("Quality flags:")
        a("")
        a("```json")
        a(json.dumps(_serialize(debug.legend_quality_flags), indent=2, default=str))
        a("```")
        a("")

    # §4 — Delta from previous iteration
    a("## §4 — Delta from previous iteration")
    a("")
    if iteration == 0:
        a("(Baseline — no previous iteration to compare against.)")
    else:
        a("(Compare against previous iteration's report for deltas.)")
    a("")

    # §5 — Worst single problem identified
    a("## §5 — Worst single problem identified (for next iteration's fix)")
    a("")
    a("(Populated by Claude after reviewing this output.)")
    a("")

    # §6 — Iteration log
    a("## §6 — Iteration log")
    a("")
    a(f"- Iteration: {iteration}")
    a(f"- Fix: {fix_description}")
    a(f"- Wall-clock: dispatch {t_dispatch:.1f}s / modules {t_modules:.1f}s / debug {t_debug:.1f}s")
    a(f"- Backend test floor: (verified separately)")
    a("")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python calibrate_silverleaf.py <iteration> [fix_description]", file=sys.stderr)
        sys.exit(1)

    iteration = int(sys.argv[1])
    fix_description = sys.argv[2] if len(sys.argv) > 2 else "BASELINE — no fix"

    rc = run_calibration(iteration, fix_description)
    sys.exit(rc)


if __name__ == "__main__":
    main()
