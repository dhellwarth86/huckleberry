"""
G.2 Classifier Upgrade — 4-bidset hard gate harness.

Verifies:
  1. Bearss byte-equivalence (769/177/31/24)
  2. Hampshire UNKNOWN-with-sheet 4→0
  3. Chipotle Tarpon UNKNOWN-with-sheet 3→0
  4. Shoppes Avalon UNKNOWN-with-sheet 2→0
  5. No bidset UNKNOWN-with-sheet INCREASES vs baseline

Usage:
    cd backend && python scripts/g2_classifier_hardgate.py
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.dispatch_gate import run_dispatch
from core.context import PageType

BIDSET_DIR = Path(r"C:\huck stage 2\full bid sets")

BIDSETS = {
    "Bearss": BIDSET_DIR / "Bearss Ave Distribution Center - University - Marcobay Construction (3).pdf",
    "Hampshire": BIDSET_DIR / "Hampshire Self Storage.pdf",
    "Chipotle Tarpon": BIDSET_DIR / "Chipotle - Tarpon Springs (Shell) - Tarpon Springs - Strategic Construction.pdf",
    "Shoppes Avalon": BIDSET_DIR / "Shoppes at Avalon - Spring Hill - MEC.pdf",
}

BASELINES = {
    "Bearss": 0,
    "Hampshire": 4,
    "Chipotle Tarpon": 3,
    "Shoppes Avalon": 2,
}

EXPECTED_POST = {
    "Bearss": 0,
    "Hampshire": 0,
    "Chipotle Tarpon": 0,
    "Shoppes Avalon": 0,
}


def count_unknown_with_sheet(ctx):
    return sum(
        1 for pc in ctx.pages.values()
        if pc.page_type == PageType.UNKNOWN and pc.sheet_number
    )


def get_unknown_with_sheet_pages(ctx):
    return [
        (pc.page_index, pc.sheet_number, pc.title, pc.page_type.value)
        for pc in ctx.pages.values()
        if pc.page_type == PageType.UNKNOWN and pc.sheet_number
    ]


def run_bearss_byte_equiv(ctx):
    tmo = ctx.trade_module_outputs
    roofing_fields = 0
    glazing_items = 0
    door_items = 0
    storefront_items = 0

    for page_idx, trades in tmo.items():
        if "roofing" in trades:
            roofing_fields += len(trades["roofing"].fields)
        if "glazing" in trades:
            out = trades["glazing"]
            glazing_items += len(out.glazing_items or [])
            door_items += len(out.door_items or [])
            storefront_items += len(out.storefront_items or [])

    return (roofing_fields, glazing_items, door_items, storefront_items)


def main():
    results = {}
    all_pass = True
    report_lines = []

    report_lines.append("# G.2 Hard Gate Report — Corpus-wide Classifier Upgrade\n")
    report_lines.append(f"**Date:** 2026-05-03")
    report_lines.append(f"**Branch:** `phase2-v0.3-G2-classifier-upgrade`")
    report_lines.append(f"**Sacred floor pre:** 237/19/0")
    report_lines.append("")

    for name, pdf_path in BIDSETS.items():
        print(f"\n{'='*60}")
        print(f"Dispatching: {name}")
        print(f"{'='*60}")

        if not pdf_path.exists():
            print(f"  ERROR: PDF not found at {pdf_path}")
            all_pass = False
            continue

        t0 = time.time()
        storage = "auto" if name == "Bearss" else None
        ctx = run_dispatch(str(pdf_path), storage=storage)
        elapsed = time.time() - t0

        unk_count = count_unknown_with_sheet(ctx)
        unk_pages = get_unknown_with_sheet_pages(ctx)

        results[name] = {
            "unknown_with_sheet": unk_count,
            "baseline": BASELINES[name],
            "expected": EXPECTED_POST[name],
            "elapsed": elapsed,
            "total_pages": len(ctx.pages),
            "unk_pages": unk_pages,
        }

        passed = unk_count == EXPECTED_POST[name]
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_pass = False

        print(f"  Total pages: {len(ctx.pages)}")
        print(f"  UNKNOWN-with-sheet: {BASELINES[name]} → {unk_count} (expected {EXPECTED_POST[name]}) [{status}]")
        print(f"  Wall-clock: {elapsed:.1f}s")

        if name == "Bearss":
            byte_eq = run_bearss_byte_equiv(ctx)
            expected_eq = (769, 177, 31, 24)
            eq_pass = byte_eq == expected_eq
            if not eq_pass:
                all_pass = False
            print(f"  Byte-equivalence: {byte_eq} {'PASS' if eq_pass else 'FAIL'}")
            results[name]["byte_equiv"] = byte_eq
            results[name]["byte_equiv_pass"] = eq_pass

        if unk_pages:
            print(f"  Remaining UNKNOWN-with-sheet pages:")
            for pg in unk_pages:
                print(f"    page={pg[0]}, sheet={pg[1]}, title='{pg[2]}', type={pg[3]}")

    # Build report
    report_lines.append("## Results\n")
    report_lines.append("| Bidset | Baseline | Post-patch | Expected | Delta | Status |")
    report_lines.append("|--------|----------|-----------|----------|-------|--------|")
    for name, r in results.items():
        delta = r["unknown_with_sheet"] - r["baseline"]
        status = "PASS" if r["unknown_with_sheet"] == r["expected"] else "FAIL"
        report_lines.append(f"| {name} | {r['baseline']} | {r['unknown_with_sheet']} | {r['expected']} | {delta:+d} | {status} |")

    report_lines.append("")
    report_lines.append("## Bearss Byte-Equivalence\n")
    if "Bearss" in results and "byte_equiv" in results["Bearss"]:
        be = results["Bearss"]["byte_equiv"]
        report_lines.append(f"- roofing_fields: {be[0]} (expected 769)")
        report_lines.append(f"- glazing_items: {be[1]} (expected 177)")
        report_lines.append(f"- door_items: {be[2]} (expected 31)")
        report_lines.append(f"- storefront_items: {be[3]} (expected 24)")
        report_lines.append(f"- **Status:** {'PASS' if results['Bearss']['byte_equiv_pass'] else 'FAIL'}")
    report_lines.append("")

    report_lines.append("## Per-page Detail (named pages from corpus scout)\n")
    report_lines.append("| Bidset | Page | Sheet | Title | Post-patch type | Expected type |")
    report_lines.append("|--------|------|-------|-------|----------------|---------------|")

    # Named pages from march orders
    named_pages = {
        "Hampshire": [(None, "FP0.1", "GENERAL_NOTES"), (None, "FP1.1", "MEP_PLAN"), (None, "FP1.2", "MEP_PLAN"), (None, "FP1.3", "MEP_PLAN")],
        "Chipotle Tarpon": [(None, "S001", "GENERAL_NOTES"), (None, "S301", "DETAIL_SHEET"), (None, "S200", "FRAMING_PLAN")],
        "Shoppes Avalon": [(None, "A-102", "FLOOR_PLAN"), (None, "A-602", "SCHEDULE_SHEET")],
    }

    for name, pdf_path in BIDSETS.items():
        if name == "Bearss" or name not in named_pages:
            continue
        if name not in results:
            continue
        # Re-dispatch without storage for page-level detail
        ctx = run_dispatch(str(pdf_path), storage=None)
        for _, sheet_expected, expected_type in named_pages[name]:
            for pc in ctx.pages.values():
                if pc.sheet_number and pc.sheet_number.replace("-", "") == sheet_expected.replace("-", ""):
                    report_lines.append(f"| {name} | {pc.page_index} | {pc.sheet_number} | {pc.title} | {pc.page_type.value} | {expected_type} |")
                    break
            else:
                # Try exact match
                for pc in ctx.pages.values():
                    if pc.sheet_number == sheet_expected:
                        report_lines.append(f"| {name} | {pc.page_index} | {pc.sheet_number} | {pc.title} | {pc.page_type.value} | {expected_type} |")
                        break

    report_lines.append("")
    report_lines.append("## Wall-clock\n")
    for name, r in results.items():
        report_lines.append(f"- {name}: {r['elapsed']:.1f}s ({r['total_pages']} pages)")

    report_lines.append("")
    report_lines.append("## Hard Gate Criteria\n")
    report_lines.append(f"1. Bearss UNKNOWN-with-sheet 0→0 AND byte-identical (769/177/31/24): **{'PASS' if results.get('Bearss', {}).get('byte_equiv_pass') else 'FAIL'}**")
    report_lines.append(f"2. Hampshire UNKNOWN-with-sheet 4→0: **{'PASS' if results.get('Hampshire', {}).get('unknown_with_sheet') == 0 else 'FAIL'}**")
    report_lines.append(f"3. Chipotle Tarpon UNKNOWN-with-sheet 3→0: **{'PASS' if results.get('Chipotle Tarpon', {}).get('unknown_with_sheet') == 0 else 'FAIL'}**")
    report_lines.append(f"4. Shoppes Avalon UNKNOWN-with-sheet 2→0: **{'PASS' if results.get('Shoppes Avalon', {}).get('unknown_with_sheet') == 0 else 'FAIL'}**")
    report_lines.append(f"5. No UNKNOWN-with-sheet INCREASE: **{'PASS' if all(r['unknown_with_sheet'] <= r['baseline'] for r in results.values()) else 'FAIL'}**")
    report_lines.append("")
    report_lines.append(f"## Overall: **{'PASS' if all_pass else 'FAIL'}**")

    report_text = "\n".join(report_lines)
    report_path = Path(__file__).resolve().parent.parent / "G_2_HARD_GATE_REPORT.md"
    report_path.write_text(report_text, encoding="utf-8")
    print(f"\n\nReport written to: {report_path}")
    print(f"\nOVERALL: {'PASS' if all_pass else 'FAIL'}")

    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
