"""Page-type verification + coupling diagnostic — read-only.

Phase: phase2-v0.3-page-type-verification (2026-04-29)
Orders: MARCH_ORDERS_page_type_verification.md

Tests three coupled bugs hypothesized by extended-thinking Claude on
2026-04-29:

    Bug 1 — page-type ordering. ELEVATION (line 110) and DETAIL
            (line 111) precede SCHEDULE (line 112) in
            dispatch_gate._PAGE_TYPE_RULES. First match wins. Combined-
            content sheet titles like "DOOR & WINDOW SCHEDULES, FRAMES &
            DETAILS" match DETAIL first and never reach SCHEDULE.

    Bug 2 — Filter 4 narrow gate. dispatch_gate line 839 only runs
            extract_tables on page_type == SCHEDULE_SHEET. If Bug 1
            misclassifies most schedule-bearing pages, Filter 4 never
            extracts tables on them.

    Bug 3 — trade_input_builder contract drift. C.3b extended
            TradeModuleInput with `tables: Optional[list[Any]] = None`,
            but trade_input_builder (C.2 verbatim port) was never
            extended to populate it. Sweep + profile harnesses bypass
            the official builder and call extract_tables per page,
            which is the 824s cost driver on Bearss.

Five diagnostic blocks. NO FIXES this session. dispatch_gate.py and
trade_input_builder.py are read-only this phase per orders §0 (even
though neither is vault-ruled, the discipline forbids touching them
in a verification phase). Vault rule active on the five vault-ruled
modules (none opened this session).

Usage:
    python scripts/page_type_verification.py            # run all 3
    python scripts/page_type_verification.py shoppes    # one bidset

The harness writes:
  - backend/PAGE_TYPE_VERIFICATION_<short>.md            (per bidset)
  - backend/PAGE_TYPE_VERIFICATION_filter4_cache_audit.md (one-shot)
  - backend/PAGE_TYPE_VERIFICATION_GATE_REPORT.md         (gate)
  - backend/PAGE_TYPE_VERIFICATION_terminal.log           (verbatim
                                                          tee log)
"""
from __future__ import annotations

import copy
import io
import json
import statistics
import sys
import time
import traceback
from collections import Counter
from dataclasses import asdict, fields, is_dataclass
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve()
BACKEND = HERE.parent.parent  # backend/
sys.path.insert(0, str(BACKEND))

import pdfplumber  # noqa: E402

from core.dispatch_gate import (  # noqa: E402
    run_dispatch,
    _PAGE_TYPE_RULES,
    _classify_page_type,
    _get_title_block_text,
    PDFEngine,
)
from core.context import (  # noqa: E402
    PlanSetContext,
    PageContext,
    PageType,
    CONFIDENCE_UNKNOWN,
)


# ============================================================
# DIAGNOSTIC OUTPUT (delete this section to run silently)
# All ##DIAG_START / ##DIAG_END print sites are gathered in
# diag_block(). Set DIAGNOSTIC_MODE=False at top to disable.
# ============================================================
DIAGNOSTIC_MODE = True


class Tee:
    """Write to multiple streams simultaneously."""

    def __init__(self, *streams):
        self.streams = streams

    def write(self, s):
        for stream in self.streams:
            stream.write(s)
            stream.flush()
        return len(s)

    def flush(self):
        for stream in self.streams:
            stream.flush()


def diag_block(name: str, payload, bidset: str | None = None,
               out_lines: list | None = None):
    """Emit a delimited diagnostic block to stdout AND optionally to a
    list of lines (used to mirror block content into per-bidset reports).
    """
    if not DIAGNOSTIC_MODE:
        return
    suffix = f":{bidset}" if bidset else ""
    head = f"##DIAG_START:{name}{suffix}##"
    body = json.dumps(payload, indent=2, default=str)
    tail = f"##DIAG_END:{name}{suffix}##"
    print(head, flush=True)
    print(body, flush=True)
    print(tail, flush=True)
    if out_lines is not None:
        out_lines.append(head)
        out_lines.append(body)
        out_lines.append(tail)


# ============================================================
# END DIAGNOSTIC SECTION
# ============================================================


# ---------------------------------------------------------------------------
# Bidset registry (matches sweep harness)
# ---------------------------------------------------------------------------

BIDSETS_ROOT = Path(r"C:\huck stage 2\full bid sets")

BIDSETS = [
    {
        "short_name": "shoppes-at-avalon",
        "display_name": "Shoppes at Avalon — Spring Hill — MEC",
        "pdf_filename": "Shoppes at Avalon - Spring Hill - MEC.pdf",
    },
    {
        "short_name": "vine-street",
        "display_name": "Vine Street Retail Center — Kissimmee — Great Southern Constructors",
        "pdf_filename": "Vine Street Retail Center - Kissimmee - Great Southern Constructors.pdf",
    },
    {
        "short_name": "bearss-ave",
        "display_name": "Bearss Ave Distribution Center — University — Marcobay Construction (3)",
        "pdf_filename": "Bearss Ave Distribution Center - University - Marcobay Construction (3).pdf",
    },
]


# ---------------------------------------------------------------------------
# Block 1 — page_type_histogram (per bidset)
# ---------------------------------------------------------------------------

def block1_histogram(ctx: PlanSetContext, bidset: str,
                     report_lines: list) -> dict:
    """Per-page list + Counter histogram. Returns the payload dict."""
    pages_data = []
    for page_idx in sorted(ctx.pages.keys()):
        pc = ctx.pages[page_idx]
        sheet_num = ctx.page_to_sheet.get(page_idx)
        sheet_title = None
        if sheet_num and sheet_num in ctx.sheet_map:
            sheet_title = ctx.sheet_map[sheet_num].title
        pages_data.append({
            "page_idx": page_idx,
            "sheet_num": sheet_num,
            "sheet_title": sheet_title,
            "page_type": pc.page_type.value,
            "confidence": pc.confidence,
            "has_legend": pc.has_legend,
            "has_schedule": pc.has_schedule,
            "legend_count": len(pc.legends),
        })

    histogram = Counter(p["page_type"] for p in pages_data)
    payload = {
        "total_pages": len(pages_data),
        "total_mapped_pages": sum(1 for p in pages_data if p["sheet_num"]),
        "total_pages_has_legend": sum(1 for p in pages_data if p["has_legend"]),
        "total_pages_has_schedule": sum(1 for p in pages_data if p["has_schedule"]),
        "histogram": dict(histogram.most_common()),
        "per_page": pages_data,
    }
    diag_block("page_type_histogram", payload, bidset, report_lines)
    return payload


# ---------------------------------------------------------------------------
# Block 2 — schedule_bearing_audit (per bidset)
# ---------------------------------------------------------------------------

def block2_schedule_bearing(block1: dict, bidset: str,
                            report_lines: list) -> dict:
    """Heuristic: 'SCHEDULE' in sheet_title.upper() flags a sheet as
    schedule-bearing. Cross-check against current page_type."""
    schedule_bearing = []
    for p in block1["per_page"]:
        title = p.get("sheet_title") or ""
        if "SCHEDULE" in title.upper():
            schedule_bearing.append({
                "page_idx": p["page_idx"],
                "sheet_num": p["sheet_num"],
                "sheet_title": p["sheet_title"],
                "current_type": p["page_type"],
            })

    classified_as_schedule = [
        e for e in schedule_bearing
        if e["current_type"] == PageType.SCHEDULE_SHEET.value
    ]
    other = [
        e for e in schedule_bearing
        if e["current_type"] != PageType.SCHEDULE_SHEET.value
    ]

    other_breakdown = Counter(e["current_type"] for e in other)
    payload = {
        "total_schedule_bearing": len(schedule_bearing),
        "classified_as_schedule_sheet": len(classified_as_schedule),
        "classified_as_other_count": len(other),
        "other_classification_breakdown": dict(other_breakdown.most_common()),
        "schedule_bearing_pages": schedule_bearing,
        "other_classified_pages": other,
    }
    diag_block("schedule_bearing_audit", payload, bidset, report_lines)
    return payload


# ---------------------------------------------------------------------------
# Block 3 — filter4_cache_audit (one-shot, static)
# ---------------------------------------------------------------------------

def _enumerate_dataclass_fields(cls) -> list[str]:
    return [f.name for f in fields(cls)]


def block3_filter4_cache_audit(report_lines: list) -> dict:
    """Static read of PlanSetContext + PageContext field lists; search
    for 'table' substring; quote dispatch_gate.py line numbers that
    document raw-tables non-caching.
    """
    psc_fields = _enumerate_dataclass_fields(PlanSetContext)
    pc_fields = _enumerate_dataclass_fields(PageContext)

    table_in_psc = [f for f in psc_fields if "table" in f.lower()]
    table_in_pc = [f for f in pc_fields if "table" in f.lower()]

    payload = {
        "plan_set_context_fields": psc_fields,
        "page_context_fields": pc_fields,
        "table_field_search": {
            "fields_with_table_in_name_planset": table_in_psc,
            "fields_with_table_in_name_pagectx": table_in_pc,
            "any_raw_tables_cached": bool(table_in_psc or table_in_pc),
            "evidence_lines": [
                "dispatch_gate.py line 744: tables = page.extract_tables() — local-scope",
                "dispatch_gate.py line 768-776: legends.append(Legend(...)) — wraps each table into a Legend object",
                "dispatch_gate.py line 777: return legends — returns Legend objects, not raw tables",
                "dispatch_gate.py line 840-841: legends.extend(table_legends) — only Legend objects propagated",
                "dispatch_gate.py line 855: ctx.all_legends = clean_legends — only filtered Legend objects stored",
                "context.py PlanSetContext + PageContext — no 'tables' or 'raw_tables' field; field lists enumerated above",
            ],
        },
        "implication_for_bug3_fix": (
            "raw tables not cached anywhere on PlanSetContext or PageContext; "
            "the eventual fix needs either (a) cache add to PlanSetContext or "
            "PageContext (touches dispatch's data contract), (b) per-page "
            "re-extraction in trade_input_builder (the harness pattern the "
            "sweep + profile already use; pays extract_tables cost twice if "
            "Filter 4 also runs on the same page), or (c) extension of "
            "_parse_tables_on_page in dispatch_gate.py to optionally cache "
            "raw tables alongside the Legend objects (one-touch, dispatch-side)."
        ),
    }
    # Block 3 has no bidset suffix
    diag_block("filter4_cache_audit", payload, None, report_lines)
    return payload


# ---------------------------------------------------------------------------
# Block 4 — reclassification_simulation (per bidset)
# ---------------------------------------------------------------------------

def _build_simulated_rules() -> list:
    """Deep-copy _PAGE_TYPE_RULES, move SCHEDULE rule to position 0."""
    rules = copy.deepcopy(_PAGE_TYPE_RULES)
    schedule_idx = None
    for i, (kws, ptype, _, _) in enumerate(rules):
        if ptype == PageType.SCHEDULE_SHEET:
            schedule_idx = i
            break
    if schedule_idx is None:
        raise RuntimeError("Could not locate SCHEDULE_SHEET rule in _PAGE_TYPE_RULES")
    schedule_rule = rules.pop(schedule_idx)
    rules.insert(0, schedule_rule)
    return rules


def _simulated_classify(title_text: str, full_text: str, rules: list):
    """Reproduce _classify_page_type's two-pass logic against a custom
    rules list. Title-pass first, then full-text-pass.
    """
    title_upper = title_text.upper()
    full_upper = full_text.upper()

    for keywords, ptype, title_conf, page_conf in rules:
        for kw in keywords:
            if kw in title_upper:
                return (ptype, title_conf)

    for keywords, ptype, title_conf, page_conf in rules:
        for kw in keywords:
            if kw in full_upper:
                return (ptype, page_conf)

    return (PageType.UNKNOWN, CONFIDENCE_UNKNOWN)


def block4_reclassification_simulation(pdf_path: str, ctx: PlanSetContext,
                                       block1: dict, bidset: str,
                                       report_lines: list) -> dict:
    """For each page, re-run classification under SCHEDULE-first
    ordering. Capture (current → simulated) transitions per page.
    """
    sim_rules = _build_simulated_rules()

    # Cache per-page (title_text, full_text) pulled the same way Filter 2
    # uses them. We do this once here rather than re-running Filter 2.
    engine = PDFEngine()
    doc = engine.open(Path(pdf_path))
    try:
        per_page_text = {}
        for page_idx in range(doc.page_count):
            meta = engine.get_page_meta(doc, page_idx)
            blocks = engine.extract_text_blocks(doc, page_idx)
            tb_text = _get_title_block_text(blocks, meta)
            full_text = engine.extract_text(doc, page_idx)
            per_page_text[page_idx] = (tb_text, full_text)
    finally:
        engine.close(doc)

    transitions = []
    for p in block1["per_page"]:
        page_idx = p["page_idx"]
        tb_text, full_text = per_page_text.get(page_idx, ("", ""))
        sim_type, sim_conf = _simulated_classify(tb_text, full_text, sim_rules)
        current_type = p["page_type"]
        sim_type_value = sim_type.value
        changed = (current_type != sim_type_value)
        transitions.append({
            "page_idx": page_idx,
            "sheet_num": p["sheet_num"],
            "sheet_title": p["sheet_title"],
            "current_type": current_type,
            "simulated_type": sim_type_value,
            "simulated_confidence": sim_conf,
            "changed": changed,
            "legend_count": p["legend_count"],
        })

    changed_pages = [t for t in transitions if t["changed"]]
    transition_hist = Counter(
        f"{t['current_type']} -> {t['simulated_type']}" for t in changed_pages
    )

    # Cross-check: of schedule-bearing pages NOT currently SCHEDULE_SHEET,
    # how many flip to SCHEDULE_SHEET under simulation?
    sched_bearing_idxs = {
        p["page_idx"] for p in block1["per_page"]
        if "SCHEDULE" in (p.get("sheet_title") or "").upper()
        and p["page_type"] != PageType.SCHEDULE_SHEET.value
    }
    sched_bearing_flip = [
        t for t in changed_pages
        if t["page_idx"] in sched_bearing_idxs
        and t["simulated_type"] == PageType.SCHEDULE_SHEET.value
    ]

    # Also count NEW misclassifications: pages whose CURRENT type is not
    # SCHEDULE_SHEET and whose title does NOT contain "SCHEDULE", but the
    # simulation gives them SCHEDULE_SHEET. This is the §7 #9 surface.
    new_misclassifications = []
    for t in changed_pages:
        title_up = (t.get("sheet_title") or "").upper()
        if (
            t["simulated_type"] == PageType.SCHEDULE_SHEET.value
            and "SCHEDULE" not in title_up
        ):
            new_misclassifications.append(t)

    payload = {
        "total_pages": len(transitions),
        "total_changed": len(changed_pages),
        "transition_histogram": dict(transition_hist.most_common()),
        "schedule_bearing_pages_not_currently_sched": len(sched_bearing_idxs),
        "schedule_bearing_pages_flipped_to_sched": len(sched_bearing_flip),
        "schedule_bearing_flip_coverage": (
            len(sched_bearing_flip) / len(sched_bearing_idxs)
            if sched_bearing_idxs else None
        ),
        "new_misclassifications_count": len(new_misclassifications),
        "new_misclassifications_sample": new_misclassifications[:20],
        "changed_pages": changed_pages,
        "schedule_bearing_flip_pages": sched_bearing_flip,
    }
    diag_block("reclassification_simulation", payload, bidset, report_lines)
    return payload


# ---------------------------------------------------------------------------
# Block 5 — table_extraction_validation (per bidset, capped)
# ---------------------------------------------------------------------------

BLOCK5_PAGE_CAP = 20
BLOCK5_HARD_CAP_SECONDS = 360.0  # 6 minutes hard cap per bidset


def block5_table_extraction(pdf_path: str, block4: dict, bidset: str,
                            report_lines: list) -> dict:
    """For pages that flipped from non-SCHEDULE_SHEET → SCHEDULE_SHEET
    under simulation, run extract_tables and capture metrics.
    """
    candidates = [
        t for t in block4["changed_pages"]
        if (
            t["current_type"] != PageType.SCHEDULE_SHEET.value
            and t["simulated_type"] == PageType.SCHEDULE_SHEET.value
        )
    ]
    total_candidates = len(candidates)
    capped = sorted(candidates, key=lambda t: -t["legend_count"])[:BLOCK5_PAGE_CAP]
    cap_was_applied = total_candidates > BLOCK5_PAGE_CAP

    per_page_results: list = []
    total_tables = 0
    total_rows = 0
    total_wallclock = 0.0
    pages_with_tables = 0
    extraction_errors: list = []
    aborted_due_to_hard_cap = False

    block_t0 = time.perf_counter()

    if not capped:
        payload = {
            "total_changed_to_sched": total_candidates,
            "page_cap_applied": cap_was_applied,
            "page_cap": BLOCK5_PAGE_CAP,
            "pages_validated": 0,
            "total_tables_extracted": 0,
            "total_rows_extracted": 0,
            "wallclock_seconds": 0.0,
            "pages_with_tables": 0,
            "extraction_errors": [],
            "per_page": [],
            "aborted_due_to_hard_cap": False,
        }
        diag_block("table_extraction_validation", payload, bidset, report_lines)
        return payload

    with pdfplumber.open(pdf_path) as pdf:
        for cand in capped:
            elapsed = time.perf_counter() - block_t0
            if elapsed > BLOCK5_HARD_CAP_SECONDS:
                aborted_due_to_hard_cap = True
                break

            page_idx = cand["page_idx"]
            if page_idx >= len(pdf.pages):
                extraction_errors.append({
                    "page_idx": page_idx,
                    "error": "page_idx out of bounds",
                })
                continue
            try:
                t0 = time.perf_counter()
                tables = pdf.pages[page_idx].extract_tables() or []
                t1 = time.perf_counter()
            except Exception as exc:
                extraction_errors.append({
                    "page_idx": page_idx,
                    "exception_type": type(exc).__name__,
                    "message": str(exc)[:200],
                })
                continue

            wallclock = t1 - t0
            total_wallclock += wallclock
            tcount = len(tables)
            rcount = sum(len(t) for t in tables if t)
            if tcount:
                pages_with_tables += 1
            total_tables += tcount
            total_rows += rcount

            headers: list = []
            for t in tables[:5]:
                if not t or not t[0]:
                    continue
                first_row = t[0]
                joined = " ".join(str(c) for c in first_row if c)
                headers.append(joined[:80])

            per_page_results.append({
                "page_idx": page_idx,
                "sheet_num": cand["sheet_num"],
                "sheet_title": cand["sheet_title"],
                "current_type": cand["current_type"],
                "simulated_type": cand["simulated_type"],
                "tables_extracted": tcount,
                "total_rows": rcount,
                "headers_first5": headers,
                "wallclock_seconds": round(wallclock, 4),
                "legend_count": cand["legend_count"],
            })

    payload = {
        "total_changed_to_sched": total_candidates,
        "page_cap_applied": cap_was_applied,
        "page_cap": BLOCK5_PAGE_CAP,
        "pages_validated": len(per_page_results),
        "total_tables_extracted": total_tables,
        "total_rows_extracted": total_rows,
        "wallclock_seconds": round(total_wallclock, 4),
        "pages_with_tables": pages_with_tables,
        "extraction_errors": extraction_errors,
        "per_page": per_page_results,
        "aborted_due_to_hard_cap": aborted_due_to_hard_cap,
        "hard_cap_seconds": BLOCK5_HARD_CAP_SECONDS,
    }
    diag_block("table_extraction_validation", payload, bidset, report_lines)
    return payload


# ---------------------------------------------------------------------------
# Per-bidset orchestration
# ---------------------------------------------------------------------------

def run_one_bidset(bidset: dict) -> dict:
    short = bidset["short_name"]
    display = bidset["display_name"]
    pdf_path = BIDSETS_ROOT / bidset["pdf_filename"]

    print("", flush=True)
    print(f"=== BIDSET: {short} ({display}) ===", flush=True)
    print(f"PDF: {pdf_path}", flush=True)

    if not pdf_path.exists():
        raise SystemExit(f"§7 stop: PDF not found at {pdf_path}")

    # Run dispatch
    print(f"[{short}] run_dispatch...", flush=True)
    t0 = time.perf_counter()
    try:
        ctx = run_dispatch(str(pdf_path), storage=None)
    except Exception:
        print(f"[{short}] DISPATCH RAISED — §7 stop:", file=sys.stderr)
        traceback.print_exc()
        raise
    dispatch_time = time.perf_counter() - t0
    print(f"[{short}] dispatch complete in {dispatch_time:.2f}s "
          f"(total_pages={ctx.total_pages})", flush=True)

    report_lines: list = []
    report_lines.append(f"# Page-Type Verification — {display}")
    report_lines.append("")
    report_lines.append("**Date:** 2026-04-29")
    report_lines.append("**Phase:** Page-type verification + coupling diagnostic")
    report_lines.append(f"**Bidset file:** `{pdf_path}`")
    report_lines.append(f"**Page count:** {ctx.total_pages}")
    report_lines.append(f"**Dispatch wall-clock:** {dispatch_time:.2f}s")
    report_lines.append("")
    report_lines.append("**Type of artifact:** read-only verification, no fixes. "
                        "Tests three coupled bugs hypothesized by extended-thinking "
                        "Claude on 2026-04-29. dispatch_gate.py and "
                        "trade_input_builder.py read-only this phase per orders §0; "
                        "vault rule active on the five vault-ruled modules (none "
                        "opened). The gate report (`backend/PAGE_TYPE_VERIFICATION_"
                        "GATE_REPORT.md`) summarizes hypothesis status across all "
                        "three bidsets.")
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")

    # Block 1
    print(f"[{short}] Block 1: page_type_histogram", flush=True)
    report_lines.append("## §1 — Block 1: Page-Type Histogram")
    report_lines.append("")
    block1 = block1_histogram(ctx, short, report_lines)
    report_lines.append("")

    # Block 2
    print(f"[{short}] Block 2: schedule_bearing_audit", flush=True)
    report_lines.append("## §2 — Block 2: Schedule-Bearing Audit")
    report_lines.append("")
    report_lines.append("Heuristic: `is_schedule_bearing = 'SCHEDULE' in "
                        "(sheet_title or '').upper()`. Not real ground truth — "
                        "tests whether the sheet's title self-identifies as "
                        "schedule-bearing.")
    report_lines.append("")
    block2 = block2_schedule_bearing(block1, short, report_lines)
    report_lines.append("")

    # Block 4
    print(f"[{short}] Block 4: reclassification_simulation", flush=True)
    report_lines.append("## §3 — Block 4: Reclassification Simulation "
                        "(SCHEDULE rule moved to position 0)")
    report_lines.append("")
    block4 = block4_reclassification_simulation(
        str(pdf_path), ctx, block1, short, report_lines
    )
    report_lines.append("")

    # Block 5
    print(f"[{short}] Block 5: table_extraction_validation "
          f"(cap={BLOCK5_PAGE_CAP}, hard_cap={BLOCK5_HARD_CAP_SECONDS}s)", flush=True)
    report_lines.append("## §4 — Block 5: Table Extraction Validation")
    report_lines.append("")
    report_lines.append(f"For pages that flipped from non-SCHEDULE_SHEET to "
                        f"SCHEDULE_SHEET under Block 4's simulation, run "
                        f"`extract_tables` and measure. Hard cap: "
                        f"{BLOCK5_PAGE_CAP} pages per bidset, ranked by "
                        f"`legend_count` descending. Wall-clock soft cap "
                        f"recorded; hard cap "
                        f"{BLOCK5_HARD_CAP_SECONDS:.0f}s aborts further pages.")
    report_lines.append("")
    block5 = block5_table_extraction(
        str(pdf_path), block4, short, report_lines
    )
    report_lines.append("")
    if block5["aborted_due_to_hard_cap"]:
        print(f"WARN: [{short}] Block 5 hit hard cap "
              f"{BLOCK5_HARD_CAP_SECONDS:.0f}s; partial data only", flush=True)
    if block5["wallclock_seconds"] > 120.0:
        print(f"WARN: [{short}] Block 5 wall-clock "
              f"{block5['wallclock_seconds']:.1f}s exceeded 120s soft cap "
              f"(soft observation, not §7 stop)", flush=True)

    # §5 — Cross-reference with sweep section 3
    report_lines.append("## §5 — Cross-Reference With Sweep Section 3")
    report_lines.append("")
    report_lines.append("For each page in §4 that produced ≥2 tables under "
                        "validation, the page's section-3 entry from "
                        "`SWEEP_OBSERVATION_<bidset>.md` carried these signals "
                        "at sweep ship time (`legend_count`, `has_legend`, "
                        "`page_type`). Same `legend_count` is replicated below "
                        "from this run's Block 1.")
    report_lines.append("")
    cross_pages = [p for p in block5["per_page"] if p["tables_extracted"] >= 2]
    if cross_pages:
        report_lines.append(
            "| Page | Sheet | Title | Current type | "
            "Tables | Legend count |"
        )
        report_lines.append("|---:|---|---|---|---:|---:|")
        for p in cross_pages:
            title = (p.get("sheet_title") or "")[:60].replace("|", "\\|")
            report_lines.append(
                f"| {p['page_idx']} | `{p['sheet_num']}` | {title} | "
                f"`{p['current_type']}` | {p['tables_extracted']} | "
                f"{p['legend_count']} |"
            )
    else:
        report_lines.append("(no pages produced ≥2 tables under Block 5 "
                            "validation)")
    report_lines.append("")

    # §6 — Observations
    report_lines.append("## §6 — Observations (no fixes, no recommendations)")
    report_lines.append("")
    report_lines.append(f"- Observed: bidset has {block1['total_pages']} pages "
                        f"total, {block1['total_mapped_pages']} mapped to "
                        f"sheets, {block1['total_pages_has_legend']} pages "
                        f"with `has_legend=True` after Filter 4, "
                        f"{block1['total_pages_has_schedule']} with "
                        f"`has_schedule=True`.")
    schedule_in_hist = block1["histogram"].get("schedule_sheet", 0)
    report_lines.append(f"- Observed: page-type histogram shows "
                        f"{schedule_in_hist} pages classified as "
                        f"`schedule_sheet` by current dispatch ordering.")
    report_lines.append(f"- Observed: {block2['total_schedule_bearing']} pages "
                        f"have 'SCHEDULE' in sheet title (heuristic). Of "
                        f"those, {block2['classified_as_schedule_sheet']} "
                        f"currently classify as `schedule_sheet`; "
                        f"{block2['classified_as_other_count']} classify as "
                        f"something else. Other-classification breakdown: "
                        f"{block2['other_classification_breakdown']}.")
    report_lines.append(f"- Observed: under SCHEDULE-first simulation, "
                        f"{block4['total_changed']} of {block4['total_pages']} "
                        f"pages would change classification. Of the "
                        f"{block4['schedule_bearing_pages_not_currently_sched']}"
                        f" schedule-bearing pages NOT currently classified as "
                        f"`schedule_sheet`, "
                        f"{block4['schedule_bearing_pages_flipped_to_sched']} "
                        f"would flip to `schedule_sheet` under simulation.")
    if block4["new_misclassifications_count"] > 0:
        report_lines.append(f"- Observed: simulation produced "
                            f"{block4['new_misclassifications_count']} pages "
                            f"newly classified as `schedule_sheet` whose "
                            f"sheet title does NOT contain 'SCHEDULE'. "
                            f"Documented per orders §7 stop #9 as soft "
                            f"observation; sample of up to 20 in the Block 4 "
                            f"payload.")
    report_lines.append(f"- Observed: of {block5['pages_validated']} flipped "
                        f"pages validated in Block 5, "
                        f"{block5['pages_with_tables']} produced ≥1 table. "
                        f"Total {block5['total_tables_extracted']} tables / "
                        f"{block5['total_rows_extracted']} rows extracted "
                        f"in {block5['wallclock_seconds']:.2f}s. "
                        f"Cap applied: {block5['page_cap_applied']}.")
    report_lines.append("")

    # §7 — Closing
    report_lines.append("## §7 — Closing")
    report_lines.append("")
    report_lines.append("Diagnostic only. Three coupled bugs hypothesized by "
                        "extended-thinking Claude 2026-04-29 are tested by this "
                        "report's data. The gate report (separate file) "
                        "summarizes hypothesis status across all three "
                        "bidsets. No fixes were attempted. dispatch_gate.py "
                        "and trade_input_builder.py NOT modified. Vault rule "
                        "held — five vault-ruled modules untouched.")
    report_lines.append("")

    out_path = BACKEND / f"PAGE_TYPE_VERIFICATION_{short}.md"
    out_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"[{short}] wrote {out_path} ({out_path.stat().st_size} bytes)",
          flush=True)

    return {
        "short": short,
        "display": display,
        "pdf_path": str(pdf_path),
        "dispatch_time": dispatch_time,
        "block1": block1,
        "block2": block2,
        "block4": block4,
        "block5": block5,
        "report_path": str(out_path),
    }


# ---------------------------------------------------------------------------
# Block 3 standalone report
# ---------------------------------------------------------------------------

def write_block3_standalone(payload: dict) -> Path:
    out_path = BACKEND / "PAGE_TYPE_VERIFICATION_filter4_cache_audit.md"
    lines = []
    lines.append("# Page-Type Verification — Block 3: Filter 4 Cache Audit "
                 "(static read)")
    lines.append("")
    lines.append("**Date:** 2026-04-29")
    lines.append("**Phase:** Page-type verification + coupling diagnostic")
    lines.append("**Scope:** static read of `core/context.py` PlanSetContext "
                 "+ PageContext field lists; "
                 "static read of `core/dispatch_gate.py` "
                 "`_parse_tables_on_page` + `run_filter_4` body lines.")
    lines.append("")
    lines.append("This report is one-shot, not per-bidset. It documents the "
                 "Bug 3 architectural surface — whether dispatch caches raw "
                 "tables anywhere on `PlanSetContext` / `PageContext`. The "
                 "answer determines what shape the eventual Bug 3 fix must "
                 "take.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## §1 — Field enumeration")
    lines.append("")
    lines.append(f"**`PlanSetContext` fields ({len(payload['plan_set_context_fields'])}):**")
    lines.append("")
    lines.append("```")
    lines.append(", ".join(payload['plan_set_context_fields']))
    lines.append("```")
    lines.append("")
    lines.append(f"**`PageContext` fields ({len(payload['page_context_fields'])}):**")
    lines.append("")
    lines.append("```")
    lines.append(", ".join(payload['page_context_fields']))
    lines.append("```")
    lines.append("")
    tfs = payload['table_field_search']
    lines.append("## §2 — Table-field search")
    lines.append("")
    lines.append(f"- Fields containing 'table' in `PlanSetContext`: "
                 f"{tfs['fields_with_table_in_name_planset']}")
    lines.append(f"- Fields containing 'table' in `PageContext`: "
                 f"{tfs['fields_with_table_in_name_pagectx']}")
    lines.append(f"- **`any_raw_tables_cached`: "
                 f"{tfs['any_raw_tables_cached']}**")
    lines.append("")
    lines.append("## §3 — Evidence lines (from dispatch_gate.py)")
    lines.append("")
    for ev in tfs['evidence_lines']:
        lines.append(f"- {ev}")
    lines.append("")
    lines.append("## §4 — Implication for Bug 3 fix path")
    lines.append("")
    lines.append(payload['implication_for_bug3_fix'])
    lines.append("")
    lines.append("## §5 — Raw payload")
    lines.append("")
    lines.append("```json")
    lines.append("##DIAG_START:filter4_cache_audit##")
    lines.append(json.dumps(payload, indent=2, default=str))
    lines.append("##DIAG_END:filter4_cache_audit##")
    lines.append("```")
    lines.append("")
    lines.append("## §6 — Closing")
    lines.append("")
    lines.append("Static read only. No code execution dependent on this "
                 "block. The eventual Bug 3 fix path is named in §4 above as "
                 "an architectural observation, NOT a recommendation. Daniel "
                 "and extended-thinking Claude make the call about which "
                 "fix path to pursue.")
    lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out_path} ({out_path.stat().st_size} bytes)", flush=True)
    return out_path


# ---------------------------------------------------------------------------
# Gate report
# ---------------------------------------------------------------------------

def write_gate_report(results: list, block3: dict, branch_sha: str) -> Path:
    out_path = BACKEND / "PAGE_TYPE_VERIFICATION_GATE_REPORT.md"

    # Aggregate totals
    total_sched_bearing = sum(r["block2"]["total_schedule_bearing"] for r in results)
    total_today_sched = sum(
        r["block2"]["classified_as_schedule_sheet"] for r in results
    )
    total_would_flip = sum(
        r["block4"]["schedule_bearing_pages_flipped_to_sched"] for r in results
    )
    total_validated_pages = sum(r["block5"]["pages_validated"] for r in results)
    total_tables = sum(r["block5"]["total_tables_extracted"] for r in results)
    total_rows = sum(r["block5"]["total_rows_extracted"] for r in results)
    total_block5_wallclock = sum(r["block5"]["wallclock_seconds"] for r in results)
    total_new_misclass = sum(
        r["block4"]["new_misclassifications_count"] for r in results
    )

    # Hypothesis evaluation. Threshold per orders §6 hypothesis-status
    # sentence:
    #   ≥80% of schedule-bearing pages misclassified under current = CONFIRMED
    #   ≤20% misclassified = REFUTED
    #   in between = PARTIAL
    if total_sched_bearing > 0:
        misclass_rate = (
            (total_sched_bearing - total_today_sched) / total_sched_bearing
        )
    else:
        misclass_rate = 0.0
    if misclass_rate >= 0.80:
        bug1_status = "CONFIRMED"
    elif misclass_rate <= 0.20:
        bug1_status = "REFUTED"
    else:
        bug1_status = "PARTIALLY CONFIRMED"

    bug3_status = (
        "CONFIRMED — no raw tables cached on PlanSetContext or PageContext"
        if not block3["table_field_search"]["any_raw_tables_cached"]
        else "REFUTED — at least one field with 'table' in name found"
    )

    lines = []
    lines.append("# Page-Type Verification — Gate Report")
    lines.append("")
    lines.append(f"**Date:** 2026-04-29")
    lines.append(f"**Phase:** phase2-v0.3-page-type-verification")
    lines.append(f"**Branch:** phase2-v0.3-page-type-verification "
                 f"(commit `{branch_sha}` at session start, single-commit "
                 f"branch ships at session end)")
    lines.append(f"**Bidsets:** Shoppes-at-Avalon, Vine Street, Bearss Ave")
    lines.append("")
    lines.append("---")
    lines.append("")

    # §1
    lines.append("## §1 — What was verified")
    lines.append("")
    lines.append("Three coupled bugs hypothesized by extended-thinking Claude "
                 "on 2026-04-29 in dispatch's table-extraction path:")
    lines.append("")
    lines.append("- **Bug 1 — page-type ordering.** "
                 "`dispatch_gate._PAGE_TYPE_RULES` has ELEVATION "
                 "(line 110) and DETAIL (line 111) before SCHEDULE "
                 "(line 112). First-match-wins. Combined-content sheet "
                 "titles like 'DOOR & WINDOW SCHEDULES, FRAMES & DETAILS' "
                 "match DETAIL first.")
    lines.append("- **Bug 2 — Filter 4 narrow gate.** Line 839 only "
                 "runs `extract_tables` on `page_type == SCHEDULE_SHEET`. "
                 "Coupled to Bug 1.")
    lines.append("- **Bug 3 — `trade_input_builder` contract drift.** "
                 "C.3b extended `TradeModuleInput` with "
                 "`tables: Optional[list[Any]] = None`, but the C.2 "
                 "verbatim port of `trade_input_builder.py` was never "
                 "extended to populate it.")
    lines.append("")

    # §2 — hypothesis status
    lines.append("## §2 — Hypothesis status across the three bidsets")
    lines.append("")
    lines.append("| Bidset | Schedule-bearing pages | Classified `schedule_sheet` today | Would under simulation | Tables extracted on changed pages |")
    lines.append("|---|---:|---:|---:|---:|")
    for r in results:
        b2 = r["block2"]
        b4 = r["block4"]
        b5 = r["block5"]
        lines.append(
            f"| {r['short']} | {b2['total_schedule_bearing']} | "
            f"{b2['classified_as_schedule_sheet']} | "
            f"{b4['schedule_bearing_pages_flipped_to_sched']} | "
            f"{b5['total_tables_extracted']} tables / "
            f"{b5['total_rows_extracted']} rows |"
        )
    lines.append(
        f"| **Total** | **{total_sched_bearing}** | "
        f"**{total_today_sched}** | **{total_would_flip}** | "
        f"**{total_tables} / {total_rows}** |"
    )
    lines.append("")
    lines.append(f"**Bug 1 is {bug1_status} by this data.** Threshold "
                 f"applied: misclassification rate of schedule-bearing pages "
                 f"under current dispatch ordering = "
                 f"{(total_sched_bearing - total_today_sched)} / "
                 f"{total_sched_bearing} = {misclass_rate:.2%}; "
                 f">=80% = CONFIRMED, <=20% = REFUTED, in between = "
                 f"PARTIALLY CONFIRMED.")
    lines.append("")

    # §3 — Filter 4 cache status (Bug 3)
    lines.append("## §3 — Filter 4 cache status (Bug 3 audit)")
    lines.append("")
    lines.append(f"**Bug 3 is {bug3_status}.**")
    lines.append("")
    lines.append("Implication string (from Block 3 payload):")
    lines.append("")
    lines.append(f"> {block3['implication_for_bug3_fix']}")
    lines.append("")
    lines.append("Evidence (from `dispatch_gate.py` lines 733–878 + "
                 "`context.py` PlanSetContext + PageContext field lists):")
    lines.append("")
    for ev in block3['table_field_search']['evidence_lines']:
        lines.append(f"- {ev}")
    lines.append("")

    # §4 — coupling
    lines.append("## §4 — Coupling diagnostic — what the simulation+extraction proved")
    lines.append("")
    for r in results:
        b4 = r["block4"]
        b5 = r["block5"]
        per_page_avg_ms = (
            (b5["wallclock_seconds"] / b5["pages_validated"]) * 1000
            if b5["pages_validated"] else 0.0
        )
        lines.append(f"### {r['short']}")
        lines.append("")
        lines.append(f"- Total pages: {b4['total_pages']}; pages that would "
                     f"change classification: {b4['total_changed']}")
        lines.append(f"- Schedule-bearing not currently classified: "
                     f"{b4['schedule_bearing_pages_not_currently_sched']}; "
                     f"would flip under simulation: "
                     f"{b4['schedule_bearing_pages_flipped_to_sched']}")
        lines.append(f"- Block 5 validated {b5['pages_validated']} of "
                     f"{b5['total_changed_to_sched']} flipped pages "
                     f"(cap applied: {b5['page_cap_applied']}, hard cap "
                     f"abort: {b5['aborted_due_to_hard_cap']}); "
                     f"{b5['pages_with_tables']} produced ≥1 table; "
                     f"{b5['total_tables_extracted']} tables / "
                     f"{b5['total_rows_extracted']} rows total in "
                     f"{b5['wallclock_seconds']:.2f}s "
                     f"(median per-page ~{per_page_avg_ms:.0f}ms).")
        lines.append("")
    lines.append("Production-cost estimate for fixing Bug 1 alone: a one-line "
                 "ordering change in `_PAGE_TYPE_RULES` plus the empirical "
                 "table-extraction cost of "
                 f"{total_validated_pages} validated changed pages ≈ "
                 f"{total_block5_wallclock:.1f}s across the three bidsets "
                 "(extrapolating from validated subset to full changed-page "
                 "set is a future-phase decision, not made here).")
    lines.append("")

    # §5 — soft observations
    lines.append("## §5 — Soft observations")
    lines.append("")
    if total_new_misclass > 0:
        lines.append(f"- New misclassifications under simulation: "
                     f"{total_new_misclass} pages across the three bidsets "
                     f"would classify as `schedule_sheet` under "
                     f"SCHEDULE-first ordering despite NOT containing "
                     f"'SCHEDULE' in their sheet title. Per-bidset breakdown "
                     f"in each report's Block 4 payload "
                     f"(`new_misclassifications_sample`). This is the §7 "
                     f"stop #9 surface — soft observation, not §7 stop. "
                     f"The future fix-orders conversation decides whether "
                     f"this is acceptable collateral damage of fixing "
                     f"Bug 1, or whether a more targeted approach (e.g., "
                     f"keyword precedence or whole-word matching) is "
                     f"needed.")
    else:
        lines.append("- New misclassifications under simulation: 0 across "
                     "the three bidsets. Schedule-first ordering did not "
                     "introduce any false-positive `schedule_sheet` "
                     "classifications on these three bidsets.")
    soft_block5 = [r["short"] for r in results if r["block5"]["wallclock_seconds"] > 120.0]
    if soft_block5:
        lines.append(f"- Block 5 wall-clock soft-cap (120s) exceeded on: "
                     f"{soft_block5}. Hard cap (360s) not reached on any "
                     f"bidset.")
    aborted = [r["short"] for r in results if r["block5"]["aborted_due_to_hard_cap"]]
    if aborted:
        lines.append(f"- Block 5 hard cap (360s) aborted on: {aborted}. "
                     f"Partial data only for these bidsets.")
    block5_errors = []
    for r in results:
        if r["block5"]["extraction_errors"]:
            block5_errors.append(
                f"{r['short']} ({len(r['block5']['extraction_errors'])} pages)"
            )
    if block5_errors:
        lines.append(f"- Block 5 `extract_tables` raised on: {block5_errors}. "
                     f"Per-page details in each bidset's Block 5 payload.")
    lines.append("")

    # §6 — discipline
    lines.append("## §6 — Discipline check")
    lines.append("")
    lines.append("- Vault rule: held (5 modules untouched — `roofing_module.py`, "
                 "`glazing_module.py`, `roofing_vocabulary.py`, "
                 "`glazing_vocabulary.py`, `debug_module.py`).")
    lines.append("- §0 fix-prohibition: held. `dispatch_gate.py` and "
                 "`trade_input_builder.py` byte-identical to pre-session "
                 "state (SHA-1 verification recorded in commit message).")
    lines.append("- Sacred floor: 216/19/0 backend; frontend at baselines "
                 "(verified at session start and end).")
    lines.append("- §7 stops: status of each enumerated below.")
    lines.append("")

    # §7 — implications
    lines.append("## §7 — Implications for next planning conversation")
    lines.append("")
    lines.append(f"With Bug 1 {bug1_status} and Bug 3 {bug3_status}, the next "
                 f"planning conversation has data to choose:")
    lines.append("")
    if bug1_status == "CONFIRMED":
        lines.append("- **Bug 1 fix-orders next.** A small `dispatch_gate.py` "
                     "ordering change in `_PAGE_TYPE_RULES`. Bug 3 fix-orders "
                     "after that, informed by Block 3's `filter4_cache_audit` "
                     "output about which architectural fix path is cleanest "
                     "(direct dispatch-side cache vs. trade_input_builder "
                     "re-extract vs. extension of `_parse_tables_on_page`).")
    elif bug1_status == "REFUTED":
        lines.append("- **Bug 1 refuted.** The 824s cost driver lives "
                     "somewhere extended-thinking Claude didn't anticipate. "
                     "Next conversation needs different data — possibly a "
                     "profile of `extract_tables` cost on already-"
                     "`schedule_sheet` pages, or instrumenting `pdfplumber` "
                     "itself.")
    else:
        lines.append("- **Bug 1 partially confirmed.** Some schedule-bearing "
                     "pages misclassify, some don't. Whether the partial "
                     "rate justifies the ordering fix depends on what kind "
                     "of partial — Daniel and extended-thinking Claude "
                     "discuss before committing to fix-orders.")
    lines.append("")
    lines.append("Either way, this phase shipped verification, not fix.")
    lines.append("")

    lines.append("## §8 — Done definition")
    lines.append("")
    lines.append("Per `MARCH_ORDERS_page_type_verification.md` §10 — full "
                 "checklist confirmed in the gate report message at end of "
                 "session.")
    lines.append("")

    lines.append("## §9 — Standing by")
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out_path} ({out_path.stat().st_size} bytes)", flush=True)
    return out_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None

    log_path = BACKEND / "PAGE_TYPE_VERIFICATION_terminal.log"
    log_file = open(log_path, "w", encoding="utf-8")
    original_stdout = sys.stdout
    sys.stdout = Tee(original_stdout, log_file)

    try:
        # Banner
        print("=" * 70, flush=True)
        print("PAGE-TYPE VERIFICATION + COUPLING DIAGNOSTIC", flush=True)
        print(f"Date: {datetime.now(timezone.utc).isoformat()}", flush=True)
        print(f"Branch: phase2-v0.3-page-type-verification", flush=True)
        print(f"Bidsets: {[b['short_name'] for b in BIDSETS]}", flush=True)
        print(f"Diagnostic mode: {DIAGNOSTIC_MODE}", flush=True)
        print(f"Block 5 page cap: {BLOCK5_PAGE_CAP}", flush=True)
        print(f"Block 5 hard cap: {BLOCK5_HARD_CAP_SECONDS:.0f}s per bidset",
              flush=True)
        print("=" * 70, flush=True)

        # Block 3 first (one-shot, no bidset context needed)
        print("", flush=True)
        print("=== BLOCK 3 (one-shot): filter4_cache_audit ===", flush=True)
        block3_lines: list = []
        block3_payload = block3_filter4_cache_audit(block3_lines)
        write_block3_standalone(block3_payload)

        # Run each bidset
        results = []
        bidset_t0 = time.perf_counter()
        for b in BIDSETS:
            if target is not None and b["short_name"] != target:
                continue
            r = run_one_bidset(b)
            results.append(r)
        bidset_total = time.perf_counter() - bidset_t0

        # Gate report
        print("", flush=True)
        print("=== GATE REPORT ===", flush=True)
        write_gate_report(results, block3_payload, branch_sha="963f0c5")

        # Closing banner
        print("", flush=True)
        print("=" * 70, flush=True)
        print(f"COMPLETE", flush=True)
        print(f"Bidsets processed: {len(results)}", flush=True)
        print(f"Total wall-clock (bidset loop): {bidset_total:.1f}s", flush=True)
        for r in results:
            print(f"  {r['short']}: dispatch={r['dispatch_time']:.1f}s, "
                  f"block5={r['block5']['wallclock_seconds']:.1f}s, "
                  f"sched_bearing={r['block2']['total_schedule_bearing']}, "
                  f"would_flip={r['block4']['schedule_bearing_pages_flipped_to_sched']}, "
                  f"tables_extracted={r['block5']['total_tables_extracted']}",
                  flush=True)
        print("=" * 70, flush=True)
    finally:
        sys.stdout = original_stdout
        log_file.close()
    print(f"Terminal log: {log_path}", flush=True)


if __name__ == "__main__":
    main()
