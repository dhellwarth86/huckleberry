"""Three-bidset sweep — observation-only diagnostic harness.

Per MARCH_ORDERS_three_bidset_sweep.md §6. Untracked / one-shot. Same
shape as backend/scripts/c5_run_through.py. Produces three observation
markdown reports under backend/SWEEP_OBSERVATION_<short_name>.md.

Procedure per bidset:
    1. run_dispatch(pdf, storage=None) -> PlanSetContext (wall-clock timed)
    2. For each page in ctx.pages:
         - extract text_blocks + tables (pdfplumber)
         - construct TradeModuleInput directly (the "C.2-established
           equivalent" path — build_trade_input requires geometry results
           which are not wired this phase; harness builds the dataclass
           with the dispatch-side state available now: page_legends,
           page_zones, page_type, project_scope, plus per-page text and
           tables. polygon_* fields stay zero/empty.)
         - call RoofingModule().analyze(input)
         - call GlazingModule().analyze(input)
       Soft-recover per page on raise (log + continue). Tracks error rate.
    3. Attach per-page module outputs onto ctx.trade_contexts["roofing"]
       and ctx.trade_contexts["glazing"] (per orders §6 step 4 — sweep
       stores per-page lists as-is and lets debug section 6 emit whatever
       it emits).
    4. run_debug(ctx) -> DebugContext
    5. Format observation report and write to disk.

This script is a one-shot verification artifact. NOT committed. NOT a
regression test. NOT a production builder.

Modifies zero backend/core/ files. Adds zero dependencies. Reads-only the
five vault-ruled modules' public surfaces.

§7 stops:
    - dispatch raises (hard stop, surface traceback)
    - per-page module error rate >25% on any single bidset (hard stop)
    - bidset PDF not at expected path (hard stop)

Soft observations (recorded but not stops):
    - per-page error rate 0-25% (logged in report §6 + gate report)
"""
from __future__ import annotations

import json
import sys
import time
import traceback
from dataclasses import asdict, is_dataclass
from pathlib import Path

# Make the backend package importable when this script runs from repo root
HERE = Path(__file__).resolve()
BACKEND = HERE.parent.parent  # backend/
sys.path.insert(0, str(BACKEND))

import pdfplumber  # noqa: E402

from core.dispatch_gate import run_dispatch  # noqa: E402
from core.debug_module import run_debug  # noqa: E402
from core.roofing_module import RoofingModule  # noqa: E402
from core.glazing_module import GlazingModule  # noqa: E402
from core.trade_module import TradeModuleInput, TradeModuleOutput  # noqa: E402


# ---------------------------------------------------------------------------
# Bidset registry
# ---------------------------------------------------------------------------

BIDSETS_ROOT = Path(r"C:\huck stage 2\full bid sets")

BIDSETS = [
    {
        "short_name": "shoppes-at-avalon",
        "display_name": "Shoppes at Avalon — Spring Hill — MEC",
        "pdf_filename": "Shoppes at Avalon - Spring Hill - MEC.pdf",
        "characterization_note": "Prior C.3a glazing-seed characterization in backend/C3_GLAZING_SEED_VALIDATION.md (single-bidset glazing scope walkthrough). Sanity-check baseline only; not a comparison target.",
    },
    {
        "short_name": "vine-street",
        "display_name": "Vine Street Retail Center — Kissimmee — Great Southern Constructors",
        "pdf_filename": "Vine Street Retail Center - Kissimmee - Great Southern Constructors.pdf",
        "characterization_note": "Uncharacterized.",
    },
    {
        "short_name": "bearss-ave",
        "display_name": "Bearss Ave Distribution Center — University — Marcobay Construction (3)",
        "pdf_filename": "Bearss Ave Distribution Center - University - Marcobay Construction (3).pdf",
        "characterization_note": "Uncharacterized.",
    },
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _serialize(obj, max_items=50):
    """Pretty-serialize for markdown embedding.
    Truncates long lists to keep artifact size bounded.
    """
    if obj is None:
        return None
    if isinstance(obj, dict):
        return {k: _serialize(v, max_items) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        if len(obj) > max_items:
            head = [_serialize(x, max_items) for x in obj[:max_items]]
            return head + [f"... ({len(obj) - max_items} more items truncated for artifact readability)"]
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


class _TextBlock:
    """Simple per-page text-block container matching what trade modules
    expect via _tb_text / _tb_center: attributes .text, .x0, .y0, .x1, .y1.
    pdfplumber's `Word` objects have most of these but as dict-like; we
    normalize here.
    """
    __slots__ = ("text", "x0", "y0", "x1", "y1")

    def __init__(self, text, x0, y0, x1, y1):
        self.text = text
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1


def _extract_page_blocks_and_tables(pdf_page):
    """Return (text_blocks, tables) for a single pdfplumber page.

    text_blocks: list[_TextBlock] — words promoted to lines for shorter
                 callouts; works with the modules' .text/.x0.. interface.
    tables: list[list[list[str]]] — pdfplumber.extract_tables() output if
            any tables are detected; an empty list otherwise.
    """
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
    """Construct TradeModuleInput directly with dispatch-side state and
    per-page text/tables. The C.2-established equivalent of build_trade_input
    when geometry results are not yet wired (Phase D/E concern).

    polygon_* fields are zero/empty (no geometry). interior_text_blocks
    receives all per-page text (whole-page treatment, since there's no
    polygon to filter to). tables receives pdfplumber.extract_tables()
    output as-is.
    """
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
    """Convert TradeModuleOutput to a plain dict for serialization."""
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


# ---------------------------------------------------------------------------
# Per-bidset run
# ---------------------------------------------------------------------------

def run_one(bidset: dict) -> int:
    """Run dispatch + per-page modules + run_debug for one bidset, write
    the observation report, return process exit code (0 ok, 3+ §7 stop)."""

    short = bidset["short_name"]
    display = bidset["display_name"]
    pdf_path = BIDSETS_ROOT / bidset["pdf_filename"]
    out_path = BACKEND / f"SWEEP_OBSERVATION_{short}.md"

    print(f"\n{'='*60}", flush=True)
    print(f"[{short}] PDF: {pdf_path}", flush=True)
    if not pdf_path.exists():
        print(f"ERROR: PDF not found at {pdf_path}", file=sys.stderr)
        return 3

    file_size = pdf_path.stat().st_size

    # --- 1. Dispatch ---
    print(f"[{short}] dispatch starting...", flush=True)
    t0 = time.time()
    try:
        ctx = run_dispatch(str(pdf_path), storage=None)
    except Exception:
        print(f"[{short}] DISPATCH RAISED — §7 stop:", file=sys.stderr)
        traceback.print_exc()
        return 3
    t_dispatch = time.time() - t0
    print(f"[{short}] dispatch complete in {t_dispatch:.1f}s", flush=True)

    total_pages = ctx.total_pages

    # --- 2. Per-page module runs ---
    print(f"[{short}] per-page module runs ({total_pages} pages)...", flush=True)
    roofing_mod = RoofingModule()
    glazing_mod = GlazingModule()

    roofing_outputs: dict[int, dict] = {}
    glazing_outputs: dict[int, dict] = {}
    per_page_errors: list[dict] = []
    pages_with_module_attempt = 0
    roofing_error_pages = 0
    glazing_error_pages = 0

    t1 = time.time()
    with pdfplumber.open(str(pdf_path)) as pdf:
        for page_idx in sorted(ctx.pages.keys()):
            if page_idx >= len(pdf.pages):
                # pdfplumber & dispatch agree on page count for normal PDFs;
                # bound-check defensively.
                continue
            pdf_page = pdf.pages[page_idx]
            try:
                text_blocks, tables = _extract_page_blocks_and_tables(pdf_page)
            except Exception as exc:
                # Page-level extraction failure — record once and skip both modules
                per_page_errors.append({
                    "page": page_idx,
                    "module": "extract",
                    "exception_type": type(exc).__name__,
                    "message": str(exc)[:200],
                })
                roofing_error_pages += 1
                glazing_error_pages += 1
                pages_with_module_attempt += 1
                continue

            tinput = _build_input_for_page(ctx, page_idx, text_blocks, tables)
            pages_with_module_attempt += 1

            # Roofing
            try:
                r_out = roofing_mod.analyze(tinput)
                roofing_outputs[page_idx] = _output_to_dict(r_out)
            except Exception as exc:
                roofing_error_pages += 1
                per_page_errors.append({
                    "page": page_idx,
                    "module": "roofing",
                    "exception_type": type(exc).__name__,
                    "message": str(exc)[:200],
                })

            # Glazing
            try:
                g_out = glazing_mod.analyze(tinput)
                glazing_outputs[page_idx] = _output_to_dict(g_out)
            except Exception as exc:
                glazing_error_pages += 1
                per_page_errors.append({
                    "page": page_idx,
                    "module": "glazing",
                    "exception_type": type(exc).__name__,
                    "message": str(exc)[:200],
                })

    t_modules = time.time() - t1
    print(f"[{short}] modules complete in {t_modules:.1f}s; "
          f"roofing errors {roofing_error_pages}/{pages_with_module_attempt}, "
          f"glazing errors {glazing_error_pages}/{pages_with_module_attempt}", flush=True)

    # §7 stop: per-module per-page error rate above 25%
    denom = max(pages_with_module_attempt, 1)
    roofing_err_rate = roofing_error_pages / denom
    glazing_err_rate = glazing_error_pages / denom
    if roofing_err_rate > 0.25 or glazing_err_rate > 0.25:
        print(f"[{short}] §7 STOP: per-page error rate >25% "
              f"(roofing={roofing_err_rate:.1%}, glazing={glazing_err_rate:.1%})",
              file=sys.stderr)
        for e in per_page_errors[:20]:
            print(f"  page {e['page']} {e['module']} {e['exception_type']}: {e['message']}",
                  file=sys.stderr)
        return 5

    # --- 3. Attach trade_contexts (orders §6 step 4) ---
    # Per orders: store per-page outputs as-is on ctx.trade_contexts; section
    # 6 of the debug module emits whatever it emits. The C.5 debug module's
    # section 6 reads ctx.all_legends, NOT ctx.trade_contexts; the modules'
    # outputs are attached for completeness and surfaced in §3/§4 of this
    # report directly.
    ctx.trade_contexts["roofing_per_page"] = roofing_outputs
    ctx.trade_contexts["glazing_per_page"] = glazing_outputs

    # --- 4. run_debug ---
    print(f"[{short}] run_debug...", flush=True)
    t2 = time.time()
    try:
        debug = run_debug(ctx)
    except Exception:
        print(f"[{short}] run_debug RAISED — §7 stop:", file=sys.stderr)
        traceback.print_exc()
        return 6
    t_debug = time.time() - t2
    print(f"[{short}] run_debug complete in {t_debug:.1f}s", flush=True)

    # --- 5. Format and write report ---
    print(f"[{short}] writing report...", flush=True)
    md = _format_report(
        bidset=bidset,
        pdf_path=pdf_path,
        file_size=file_size,
        total_pages=total_pages,
        t_dispatch=t_dispatch,
        t_modules=t_modules,
        t_debug=t_debug,
        ctx=ctx,
        debug=debug,
        roofing_outputs=roofing_outputs,
        glazing_outputs=glazing_outputs,
        per_page_errors=per_page_errors,
        pages_with_module_attempt=pages_with_module_attempt,
        roofing_err_rate=roofing_err_rate,
        glazing_err_rate=glazing_err_rate,
    )
    out_path.write_text(md, encoding="utf-8")
    size = out_path.stat().st_size
    print(f"[{short}] wrote {out_path} ({size} bytes)", flush=True)
    return 0


# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------

def _summarize_roofing(outs: dict[int, dict]) -> dict:
    total_fields = 0
    total_warnings = 0
    total_eq_pins = 0
    pages_with_content = 0
    for _, d in outs.items():
        f = d.get("fields") or {}
        w = d.get("warnings") or []
        e = d.get("equipment_pins") or []
        # _scope is a pseudo-field; count it in fields but record separately
        if f or w or e:
            pages_with_content += 1
        total_fields += len(f)
        total_warnings += len(w)
        total_eq_pins += len(e)
    return {
        "total_fields": total_fields,
        "total_warnings": total_warnings,
        "total_equipment_pins": total_eq_pins,
        "pages_with_content": pages_with_content,
        "pages_with_empty": len(outs) - pages_with_content,
    }


def _summarize_glazing(outs: dict[int, dict]) -> dict:
    total_g = 0
    total_d = 0
    total_s = 0
    pages_with_content = 0
    for _, d in outs.items():
        gi = d.get("glazing_items") or []
        di = d.get("door_items") or []
        si = d.get("storefront_items") or []
        if gi or di or si:
            pages_with_content += 1
        total_g += len(gi)
        total_d += len(di)
        total_s += len(si)
    return {
        "total_glazing_items": total_g,
        "total_door_items": total_d,
        "total_storefront_items": total_s,
        "pages_with_content": pages_with_content,
        "pages_with_empty": len(outs) - pages_with_content,
    }


def _format_report(*, bidset, pdf_path, file_size, total_pages,
                   t_dispatch, t_modules, t_debug,
                   ctx, debug,
                   roofing_outputs, glazing_outputs,
                   per_page_errors, pages_with_module_attempt,
                   roofing_err_rate, glazing_err_rate) -> str:
    short = bidset["short_name"]
    display = bidset["display_name"]
    char_note = bidset["characterization_note"]

    ps = ctx.project_scope

    # Serialize debug sections
    s1 = _serialize(debug.dispatch_health)
    s2 = _serialize(debug.scale_comparison)
    s3 = _serialize(debug.page_intelligence, max_items=200)
    s4 = _serialize(debug.crossref_summary)
    s5 = _serialize(debug.geometry_diagnostics)
    s6_legends = _serialize(debug.legend_contents, max_items=80)
    s6_flags = _serialize(debug.legend_quality_flags)

    # Stub-marker confirmations
    s2_ok = (isinstance(debug.scale_comparison, dict)
             and debug.scale_comparison.get("stub_marker") == "C.5_partial_port_pending_scale_engine_route")
    s4_ok = (isinstance(debug.crossref_summary, dict)
             and debug.crossref_summary.get("stub_marker") == "C.5_partial_port_pending_networkx_and_sheet_index")
    s5_ok = (isinstance(debug.geometry_diagnostics, dict)
             and debug.geometry_diagnostics.get("stub_marker") == "C.5_partial_port_pending_geometry_results")

    rsum = _summarize_roofing(roofing_outputs)
    gsum = _summarize_glazing(glazing_outputs)

    # Build per-page summary tables. Roofing and glazing share page set.
    page_indexes = sorted(set(roofing_outputs.keys()) | set(glazing_outputs.keys()))

    lines: list[str] = []
    a = lines.append

    a(f"# Sweep Observation Report — {display}")
    a("")
    a(f"**Date:** 2026-04-28")
    a(f"**Phase:** Three-bidset sweep (post-C.3c-build, post-C.5; modules vault-ruled)")
    a(f"**Bidset short name:** `{short}`")
    a(f"**Bidset file:** `{pdf_path}`")
    a(f"**Page count:** {total_pages}")
    a(f"**File size:** {file_size:,} bytes (~{file_size / (1024 * 1024):.1f} MB)")
    a(f"**Wall-clock dispatch time:** {t_dispatch:.1f}s")
    a(f"**Wall-clock per-page module time (roofing+glazing combined):** {t_modules:.1f}s")
    a(f"**Wall-clock run_debug time:** {t_debug:.1f}s")
    a("")
    a("**Type of artifact:** observation only. No grading. No correctness")
    a("comparison. No 'needs ground truth' labels. No fix lists. No tuning")
    a("recommendations. The roofing module, glazing module, and debug")
    a("module are vault-ruled per CLAUDE.md §3 Decision 15. This report")
    a("describes what the modules produced; the future tuning planning")
    a("conversation decides what to do with the data.")
    a("")
    a("**Harness note (TradeModuleInput construction).** The standard")
    a("`build_trade_input()` in `core/trade_input_builder.py` requires a")
    a("`geometry_result` dict from Stages 6-9 (polygon, area, perimeter,")
    a("scale). Stages 6-9 geometry is ported (B.2/B.3) but the dispatch")
    a("→ geometry route is not wired (Phase D/E). The sweep harness")
    a("therefore constructs `TradeModuleInput` directly per page with")
    a("dispatch-side state available now: `page_legends`, `page_zones`,")
    a("`page_type`, `project_scope`, plus per-page text and tables")
    a("extracted via pdfplumber. `polygon_*` fields are zero/empty;")
    a("`scale_source = 'unwired'`. This is the 'C.2-established")
    a("equivalent' path explicitly permitted by `MARCH_ORDERS_three_")
    a("bidset_sweep.md §6` when the standard builder's preconditions")
    a("aren't met.")
    a("")
    a("---")
    a("")

    # ----- §1 -----
    a(f"## §1 — Bidset Metadata")
    a("")
    a(f"- Display name: {display}")
    a(f"- Short name: `{short}`")
    a(f"- Filename: `{bidset['pdf_filename']}`")
    a(f"- Full path: `{pdf_path}`")
    a(f"- Page count: {total_pages}")
    a(f"- File size: {file_size:,} bytes ({file_size / (1024 * 1024):.1f} MB)")
    a(f"- Prior characterization: {char_note}")
    a("")

    # ----- §2 -----
    a(f"## §2 — Dispatch Output (PlanSetContext)")
    a("")
    a(f"### project_scope")
    a("")
    if ps is None:
        a("- (project_scope is None — no scope summary attached)")
    else:
        a(f"- detected_system: `{ps.detected_system!r}`")
        a(f"- system_confidence: `{ps.system_confidence}`")
        a(f"- system_evidence: `{ps.system_evidence!r}`")
        a(f"- scope_pages: `{list(ps.scope_pages)}`")
        a(f"- spec_sections: `{list(ps.spec_sections)}`")
        a(f"- manufacturers: `{list(ps.manufacturers)}`")
        a(f"- material_mentions: `{list(ps.material_mentions)}`")
        a(f"- florida_signals: `{list(ps.florida_signals)}`")
        a(f"- roof_shape_signal: `{ps.roof_shape_signal!r}`")
        a(f"- architect: `{ps.architect!r}`")
        a(f"- contractor: `{ps.contractor!r}`")
    a("")
    a(f"### dispatch_complete: `{ctx.dispatch_complete}`")
    a(f"### filters_completed: `{ctx.filters_completed}`")
    a(f"### dispatch_warnings: `{list(ctx.dispatch_warnings)}`")
    a(f"### total_pages: `{ctx.total_pages}`")
    a(f"### sheet_count: `{len(ctx.sheet_map)}`")
    a(f"### mapped_pages: `{len(ctx.page_to_sheet)}`")
    a(f"### sheet_map_source: `{ctx.sheet_map_source}`")
    a("")

    # ----- §3 Roofing -----
    a(f"## §3 — Roofing Module Output")
    a("")
    a(f"### Aggregated")
    a("")
    a(f"- Total `fields` entries across all pages: {rsum['total_fields']}")
    a(f"- Total warnings: {rsum['total_warnings']}")
    a(f"- Total equipment_pins: {rsum['total_equipment_pins']}")
    a(f"- Pages with non-empty output: {rsum['pages_with_content']}")
    a(f"- Pages with empty output: {rsum['pages_with_empty']}")
    a("")
    a(f"### Per-page summary (only pages with non-empty output shown)")
    a("")
    a(f"| Page | Sheet | Fields | Warnings | Equip pins |")
    a(f"|---:|---|---:|---:|---:|")
    nonempty_roofing = [(p, d) for p, d in sorted(roofing_outputs.items())
                        if (d.get("fields") or d.get("warnings") or d.get("equipment_pins"))]
    for p, d in nonempty_roofing[:200]:
        sheet = ctx.page_to_sheet.get(p, "---")
        f_count = len(d.get("fields") or {})
        w_count = len(d.get("warnings") or [])
        e_count = len(d.get("equipment_pins") or [])
        a(f"| {p} | {sheet} | {f_count} | {w_count} | {e_count} |")
    if len(nonempty_roofing) > 200:
        a(f"| ... | ({len(nonempty_roofing) - 200} more rows truncated) | | | |")
    if not nonempty_roofing:
        a(f"| (none) | | | | |")
    a("")

    a(f"### Per-page detail (only pages with non-empty output)")
    a("")
    if not nonempty_roofing:
        a("(no pages with non-empty roofing module output)")
        a("")
    else:
        for p, d in nonempty_roofing[:60]:
            sheet = ctx.page_to_sheet.get(p, "---")
            a(f"#### Page {p} (sheet `{sheet}`)")
            a("")
            a("```json")
            a(json.dumps(_serialize(d), indent=2, default=str))
            a("```")
            a("")
        if len(nonempty_roofing) > 60:
            a(f"*({len(nonempty_roofing) - 60} more non-empty roofing pages truncated for artifact size)*")
            a("")

    # ----- §4 Glazing -----
    a(f"## §4 — Glazing Module Output")
    a("")
    a(f"### Aggregated")
    a("")
    a(f"- Total glazing_items across all pages: {gsum['total_glazing_items']}")
    a(f"- Total door_items: {gsum['total_door_items']}")
    a(f"- Total storefront_items: {gsum['total_storefront_items']}")
    a(f"- Pages with any glazing module content (any of the three lists non-empty): {gsum['pages_with_content']}")
    a(f"- Pages with empty output: {gsum['pages_with_empty']}")
    a("")
    a(f"### Per-page summary (only pages with non-empty output shown)")
    a("")
    a(f"| Page | Sheet | glazing_items | door_items | storefront_items |")
    a(f"|---:|---|---:|---:|---:|")
    nonempty_glazing = []
    for p, d in sorted(glazing_outputs.items()):
        gi = d.get("glazing_items") or []
        di = d.get("door_items") or []
        si = d.get("storefront_items") or []
        if gi or di or si:
            nonempty_glazing.append((p, d, len(gi), len(di), len(si)))
    for p, _d, g_, d_, s_ in nonempty_glazing[:200]:
        sheet = ctx.page_to_sheet.get(p, "---")
        a(f"| {p} | {sheet} | {g_} | {d_} | {s_} |")
    if len(nonempty_glazing) > 200:
        a(f"| ... | ({len(nonempty_glazing) - 200} more rows truncated) | | | |")
    if not nonempty_glazing:
        a(f"| (none) | | | | |")
    a("")

    a(f"### Per-page detail (only pages with non-empty output)")
    a("")
    if not nonempty_glazing:
        a("(no pages with non-empty glazing module output)")
        a("")
    else:
        for p, d, _g, _dn, _s in nonempty_glazing[:60]:
            sheet = ctx.page_to_sheet.get(p, "---")
            a(f"#### Page {p} (sheet `{sheet}`)")
            a("")
            a("```json")
            a(json.dumps(_serialize(d), indent=2, default=str))
            a("```")
            a("")
        if len(nonempty_glazing) > 60:
            a(f"*({len(nonempty_glazing) - 60} more non-empty glazing pages truncated for artifact size)*")
            a("")

    # ----- §5 Debug -----
    a(f"## §5 — Debug Module Output")
    a("")
    a(f"### Section 1 — dispatch_health")
    a("")
    a("```json")
    a(json.dumps(s1, indent=2, default=str))
    a("```")
    a("")

    a(f"### Section 2 — scale_comparison (STUB)")
    a(f"- stub_marker confirmed: `{s2_ok}`")
    a("")
    a("```json")
    a(json.dumps(s2, indent=2, default=str))
    a("```")
    a("")

    a(f"### Section 3 — page_intelligence")
    if isinstance(debug.page_intelligence, list):
        a(f"- Page entry count: {len(debug.page_intelligence)}")
    a("")
    a("```json")
    a(json.dumps(s3, indent=2, default=str))
    a("```")
    a("")

    a(f"### Section 4 — cross_reference_graph (STUB)")
    a(f"- stub_marker confirmed: `{s4_ok}`")
    a("")
    a("```json")
    a(json.dumps(s4, indent=2, default=str))
    a("```")
    a("")

    a(f"### Section 5 — geometry_diagnostics (STUB)")
    a(f"- stub_marker confirmed: `{s5_ok}`")
    a("")
    a("```json")
    a(json.dumps(s5, indent=2, default=str))
    a("```")
    a("")

    a(f"### Section 6 — legend_and_quality_flags")
    if isinstance(debug.legend_contents, list):
        a(f"- Legend count: {len(debug.legend_contents)}")
    if isinstance(debug.legend_quality_flags, list):
        a(f"- Quality flag count: {len(debug.legend_quality_flags)}")
    a("")
    a(f"#### Quality flags raised")
    a("")
    a("```json")
    a(json.dumps(s6_flags, indent=2, default=str))
    a("```")
    a("")
    a(f"#### Legend contents (sample, truncated)")
    a("")
    a("```json")
    a(json.dumps(s6_legends, indent=2, default=str))
    a("```")
    a("")

    # ----- §6 errors -----
    a(f"## §6 — Per-Page Errors (if any)")
    a("")
    a(f"- Pages where module raised: {len(per_page_errors)}")
    a(f"- Pages with module attempt: {pages_with_module_attempt}")
    a(f"- Roofing per-page error rate: {roofing_err_rate:.2%}")
    a(f"- Glazing per-page error rate: {glazing_err_rate:.2%}")
    a("")
    if per_page_errors:
        a(f"| Page | Module | Exception | Message (first 200 chars) |")
        a(f"|---:|---|---|---|")
        for e in per_page_errors:
            msg = e["message"].replace("|", "\\|").replace("\n", " ")
            a(f"| {e['page']} | {e['module']} | `{e['exception_type']}` | {msg} |")
        a("")
    else:
        a("(no per-page errors)")
        a("")

    # ----- §7 closing -----
    a(f"## §7 — Closing")
    a("")
    a("Observation only. No grades. No fixes proposed. No tuning")
    a("recommendations. The roofing module and glazing module are")
    a("vault-ruled per CLAUDE.md §3 Decision 15. The debug module is")
    a("vault-ruled per the same. Tuning is a future phase with `core/`")
    a("frozen. Section 2/4/5 stub markers confirmed above; sections 1/3/6")
    a("ran on real input.")
    a("")
    # Optional 3–5 plain "observed:" statements per orders §7. Generated
    # mechanically from the run's totals, NOT interpretive. If a number
    # is zero we still record the observation; if there's nothing to say,
    # we omit. NEVER "should be:" or "recommend:".
    a("Mechanical observations:")
    a("")
    a(f"- Observed: roofing module produced {rsum['total_fields']} `fields` entries across "
      f"{rsum['pages_with_content']} pages with non-empty output (of {pages_with_module_attempt} "
      f"pages attempted), with {rsum['total_warnings']} warnings and "
      f"{rsum['total_equipment_pins']} equipment_pins.")
    a(f"- Observed: glazing module produced {gsum['total_glazing_items']} glazing_items, "
      f"{gsum['total_door_items']} door_items, {gsum['total_storefront_items']} storefront_items "
      f"across {gsum['pages_with_content']} pages with non-empty output (of "
      f"{pages_with_module_attempt} pages attempted).")
    if ps is not None:
        a(f"- Observed: dispatch project_scope detected_system = `{ps.detected_system!r}` "
          f"with confidence `{ps.system_confidence}`; scope_pages = `{list(ps.scope_pages)}`; "
          f"manufacturers = `{list(ps.manufacturers)}`.")
    a(f"- Observed: debug section 6 emitted {len(debug.legend_contents) if isinstance(debug.legend_contents, list) else 'N/A'} "
      f"legend entries and {len(debug.legend_quality_flags) if isinstance(debug.legend_quality_flags, list) else 'N/A'} "
      f"legend quality flags.")
    a(f"- Observed: per-page module error rate roofing={roofing_err_rate:.2%}, "
      f"glazing={glazing_err_rate:.2%} (§7 stop threshold = 25%; soft-observation band = 5–25%).")
    a("")
    a("---")
    a("")
    a("**End of report.** Vault rule active on `roofing_module.py`,")
    a("`roofing_vocabulary.py`, `glazing_module.py`, `glazing_vocabulary.py`,")
    a("and `debug_module.py`. The sweep modified zero `backend/core/` files")
    a("and added zero dependencies. This report is a descriptive artifact")
    a("for the future tuning planning conversation per Daniel's directive")
    a("2026-04-28 (PROJECT_CLAUDE.md §3).")
    a("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None
    overall_rc = 0
    for b in BIDSETS:
        if target is not None and b["short_name"] != target:
            continue
        rc = run_one(b)
        if rc != 0:
            overall_rc = rc
            # Per orders: §7 stop is hard. Stop the whole sweep on any §7.
            print(f"\n!!! §7 stop on {b['short_name']} (rc={rc}) — halting sweep.\n",
                  file=sys.stderr)
            break
    sys.exit(overall_rc)


if __name__ == "__main__":
    main()
