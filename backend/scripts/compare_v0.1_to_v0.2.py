"""compare_v0.1_to_v0.2.py — Step 17 validation.

Reads the 15 v0.2 PlanSetContext JSONs in `backend/test_fixtures/v0.2_outputs/`
and applies the binary pass questions from `STEP_17_REVIEW_CHECKLIST.md`.
Writes a machine-readable summary to `backend/test_fixtures/v0_2_validation_summary.json`
and prints per-symptom roll-ups.

The narrative report at `backend/V0_2_VALIDATION.md` is written separately;
this script's output backs it.

Karpathy: this script measures only. It does NOT propose fixes.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

BACKEND_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = BACKEND_DIR / "test_fixtures" / "v0.2_outputs"
SUMMARY_JSON = BACKEND_DIR / "test_fixtures" / "v0_2_validation_summary.json"


# -----------------------------------------------------------------------
# Bidset id constants — referenced by Symptom-2 and Symptom-4 binary questions
# -----------------------------------------------------------------------

TACO_BELL_ID = "taco-bell-weeki-wachee-compass-construction-management-2"
AUTOZONE_JAX_ID = "auto-zone-10891-jacksonville-mec-24-others"
AUTOZONE_VERO_ID = "auto-zone-vero-beach-fl"
VINE_STREET_ID = "vine-street-retail-center-kissimmee-great-southern-constructors"
BEARSS_ID = "bearss-ave-distribution-center-university-marcobay-construction-3"

VALID_SYSTEM_TOKENS = {"tpo", "pvc", "epdm", "modified_bitumen", "built_up", "metal_panel"}

V01_BASELINE_ROOF_PLAN_TOTAL = 95
V01_BASELINE_ROOF_PLAN_EXPLICIT = 17
V01_BASELINE_RATIO = V01_BASELINE_ROOF_PLAN_EXPLICIT / V01_BASELINE_ROOF_PLAN_TOTAL  # 0.17894...


# -----------------------------------------------------------------------
# Loader
# -----------------------------------------------------------------------

def load_outputs() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for path in sorted(OUT_DIR.glob("*.json")):
        if path.name.endswith(".tmp"):
            continue
        out[path.stem] = json.loads(path.read_text(encoding="utf-8"))
    return out


# -----------------------------------------------------------------------
# Symptom 1 — project metadata field_sources tracking
# -----------------------------------------------------------------------
#
# CHECKLIST FIELD-PATH MISMATCH (per checklist §10):
# The checklist references `project.project_name` and
# `project.field_sources["project_name"].confidence`. The actual `to_json()`
# body in `core/context.py` (lines ~605-635) does NOT serialize the
# `project` field. Only `pdf_path`, `pdf_hash`, `total_pages`,
# `sheet_map_source`, `sheet_map`, `page_to_sheet`, `pages`, `all_cross_refs`,
# `resolved_count`, `unresolved_count`, `all_legends`, `filters_completed`,
# `dispatch_complete`, `dispatch_timestamp`, `dispatch_warnings`,
# `architect_profile`, and `project_scope` are written.
#
# Per checklist §10: "the fix is to grep core/context.py for the actual
# to_json() body and update this document." The checklist does need an
# update — but I'm not authorized to edit the checklist, only follow it.
# So Symptom 1 reports as "unmeasurable from JSON" with the underlying
# data unavailable.
# -----------------------------------------------------------------------

def measure_symptom_1(bidset_id: str, payload: dict) -> dict:
    """Symptom 1 cannot be measured from v0.2 outputs because to_json()
    doesn't serialize the `project` field. Report N/A."""
    has_project_in_json = "project" in payload
    return {
        "bidset_id": bidset_id,
        "project_in_json": has_project_in_json,
        "project_name": None,
        "source": None,
        "confidence": None,
        "pass": None,  # tri-state: None = unmeasurable
        "note": "to_json() does not serialize PlanSetContext.project — see checklist §10 mismatch",
    }


# -----------------------------------------------------------------------
# Symptom 2 — one detected_system per bidset (single string or null, never a list)
# -----------------------------------------------------------------------

def measure_symptom_2(bidset_id: str, payload: dict) -> dict:
    """Symptom 2 has 4 binary questions across 3 specific bidsets + 1 corpus-wide.
    This function answers the per-bidset questions; corpus-wide aggregation is
    in `roll_up_symptom_2()` below."""
    ps = payload.get("project_scope") or {}
    ds = ps.get("detected_system")  # may be None, str, or (per v0.1 bug) list
    sc = ps.get("system_confidence")
    sp = ps.get("scope_pages") or []
    ds_type = type(ds).__name__

    # Per-bidset questions only fire on Taco Bell, AutoZone Jax, AutoZone Vero.
    # Other bidsets contribute only to the corpus-wide "never a list" aggregate.
    bidset_passes: dict[str, Any] = {}

    if bidset_id == TACO_BELL_ID:
        # Taco Bell: detected_system must be exactly one of the valid tokens, conf >= 0.7
        q1 = ds in VALID_SYSTEM_TOKENS  # specific token check
        q2 = isinstance(sc, (int, float)) and sc >= 0.7
        bidset_passes["taco_bell_detected_system_valid_token"] = q1
        bidset_passes["taco_bell_system_confidence_ge_0p7"] = q2

    if bidset_id in (AUTOZONE_JAX_ID, AUTOZONE_VERO_ID):
        # AutoZone: must be either project_scope null OR detected_system null;
        # AND scope_pages empty
        q3 = (payload.get("project_scope") is None) or (ds is None)
        q4 = (sp == []) or (sp is None)
        bidset_passes[f"{bidset_id}_detected_system_null"] = q3
        bidset_passes[f"{bidset_id}_scope_pages_empty"] = q4

    return {
        "bidset_id": bidset_id,
        "detected_system": ds,
        "detected_system_type": ds_type,
        "system_confidence": sc,
        "scope_pages_count": len(sp),
        "is_list_type": isinstance(ds, list),  # per corpus-wide question
        "bidset_passes": bidset_passes,
    }


def roll_up_symptom_2(per_bidset: list[dict]) -> dict:
    """Aggregate Symptom 2 results into a pass/fail decision."""
    # Collect specific bidset passes
    specific = {}
    for r in per_bidset:
        specific.update(r["bidset_passes"])

    # Corpus-wide: type(detected_system) ever 'list' across all 15?
    any_list = any(r["is_list_type"] for r in per_bidset)
    specific["corpus_no_list_type_detected_system"] = not any_list

    # Per checklist: "All four questions return YES on the relevant bidsets."
    # I have 4 specific binary questions (taco bell × 2, AZ × 2 each = 4 questions
    # with two AZ instances and two taco questions = 6) PLUS the corpus check.
    # Actually re-reading checklist: 2 questions for Taco Bell, 2 for "both AutoZones",
    # 1 corpus-wide. That's 5 questions. The "both" wording for AZ questions means
    # both bidsets must satisfy them.
    all_yes = all(specific.values())

    return {
        "specific_questions": specific,
        "all_yes": all_yes,
        "corpus_any_list_type": any_list,
    }


# -----------------------------------------------------------------------
# Symptom 3 — drawing pages and scope pages are separate categories
# -----------------------------------------------------------------------

def measure_symptom_3(bidset_id: str, payload: dict) -> dict:
    """Symptom 3 has one specific-bidset question (Taco Bell page 18 in
    scope_pages) plus a corpus-wide aggregate. This function records the
    raw counts; corpus-wide aggregation is in `roll_up_symptom_3()`."""
    pages = payload.get("pages", {}) or {}
    ps = payload.get("project_scope") or {}
    scope_pages = ps.get("scope_pages") or []

    # Count: roof_plan pages total + roof_plan pages with confidence >= 0.9
    roof_plan_total = 0
    roof_plan_explicit = 0
    for pc in pages.values():
        if pc.get("page_type") == "roof_plan":
            roof_plan_total += 1
            if (pc.get("confidence") or 0.0) >= 0.9:
                roof_plan_explicit += 1

    # Specific: for Taco Bell, is page 18 in scope_pages?
    bidset_passes: dict[str, Any] = {}
    if bidset_id == TACO_BELL_ID:
        bidset_passes["taco_bell_page_18_in_scope_pages"] = (18 in scope_pages)

    return {
        "bidset_id": bidset_id,
        "roof_plan_total": roof_plan_total,
        "roof_plan_explicit": roof_plan_explicit,
        "taco_bell_scope_pages": scope_pages if bidset_id == TACO_BELL_ID else None,
        "bidset_passes": bidset_passes,
    }


def roll_up_symptom_3(per_bidset: list[dict]) -> dict:
    """Aggregate Symptom 3: corpus explicit-roof_plan ratio vs v0.1 baseline."""
    total = sum(r["roof_plan_total"] for r in per_bidset)
    explicit = sum(r["roof_plan_explicit"] for r in per_bidset)
    ratio = (explicit / total) if total else 0.0

    specific: dict[str, Any] = {}
    for r in per_bidset:
        specific.update(r["bidset_passes"])

    # Per checklist: "Is `ratio > 0.18`? (v0.1 was 17/95 ≈ 0.18.)"
    aggregate_pass = ratio > V01_BASELINE_RATIO
    specific["corpus_explicit_ratio_above_v01"] = aggregate_pass

    all_yes = all(specific.values())

    return {
        "roof_plan_total_v02": total,
        "roof_plan_explicit_v02": explicit,
        "ratio_v02": ratio,
        "ratio_v01_baseline": V01_BASELINE_RATIO,
        "ratio_v01_total": V01_BASELINE_ROOF_PLAN_TOTAL,
        "ratio_v01_explicit": V01_BASELINE_ROOF_PLAN_EXPLICIT,
        "specific_questions": specific,
        "all_yes": all_yes,
    }


# -----------------------------------------------------------------------
# Symptom 4 — sheet number extraction reliability
# -----------------------------------------------------------------------
#
# CHECKLIST FIELD-PATH MISMATCH (per §10):
# The checklist says `Counter(sheet_map.values())`. But `sheet_map.values()`
# are dicts (full SheetEntry payloads), not strings — unhashable. The
# checklist's intent is "did multiple pages get the same sheet number
# string?" The right field is `page_to_sheet` (page_index -> sheet_number),
# which IS keyed correctly to detect that. Substituting that here.
# -----------------------------------------------------------------------

def measure_symptom_4(bidset_id: str, payload: dict) -> dict:
    """Symptom 4: drawing_index sourcing on Vine Street + max-duplicate-sheet
    check across all 15."""
    sheet_map = payload.get("sheet_map", {}) or {}
    page_to_sheet = payload.get("page_to_sheet", {}) or {}
    sheet_map_source = payload.get("sheet_map_source")

    # max-duplicate-value count: how many pages map to the same sheet number?
    counter = Counter(page_to_sheet.values())
    max_dup = max(counter.values()) if counter else 0
    most_common = counter.most_common(3)

    # TS9D check
    ts9d_in_keys = "TS9D" in sheet_map
    ts9d_in_values = "TS9D" in set(page_to_sheet.values())

    # Real-architectural-sheets check (Vine Street): look for at least 3 keys
    # matching A-1.0/A-1.3/A6.1 style. Loose: starts with "A" and has digit+dot.
    arch_sheets = [k for k in sheet_map.keys() if k.startswith("A") and any(c.isdigit() for c in k)]

    bidset_passes: dict[str, Any] = {}
    if bidset_id == VINE_STREET_ID:
        bidset_passes["vine_street_sheet_map_source_drawing_index"] = (sheet_map_source == "drawing_index")
        bidset_passes["vine_street_real_arch_sheets_present"] = (len(arch_sheets) >= 3)
        bidset_passes["vine_street_no_TS9D"] = (not ts9d_in_keys and not ts9d_in_values)

    return {
        "bidset_id": bidset_id,
        "sheet_map_source": sheet_map_source,
        "sheet_map_size": len(sheet_map),
        "page_to_sheet_size": len(page_to_sheet),
        "max_duplicate_value_count": max_dup,
        "most_common": most_common,
        "ts9d_in_keys": ts9d_in_keys,
        "ts9d_in_values": ts9d_in_values,
        "arch_sheets_count": len(arch_sheets),
        "bidset_passes": bidset_passes,
    }


def roll_up_symptom_4(per_bidset: list[dict]) -> dict:
    """Aggregate Symptom 4: max-duplicate ≤ 2 for every bidset except
    documented multi-building cases (Bearss)."""
    specific: dict[str, Any] = {}
    for r in per_bidset:
        specific.update(r["bidset_passes"])

    # Aggregate: which bidsets have max-duplicate > 2?
    over_threshold = []
    for r in per_bidset:
        if r["max_duplicate_value_count"] > 2 and r["bidset_id"] != BEARSS_ID:
            over_threshold.append({
                "bidset_id": r["bidset_id"],
                "max_count": r["max_duplicate_value_count"],
                "most_common": r["most_common"],
            })

    aggregate_pass = (len(over_threshold) == 0)
    specific["corpus_no_unexpected_duplicates"] = aggregate_pass

    all_yes = all(specific.values())

    return {
        "over_threshold_bidsets": over_threshold,
        "specific_questions": specific,
        "all_yes": all_yes,
    }


# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------

def main() -> int:
    payloads = load_outputs()
    if len(payloads) != 15:
        print(f"WARNING: expected 15 outputs, found {len(payloads)}", file=sys.stderr)

    # Per-bidset measurements
    s1_rows = []
    s2_rows = []
    s3_rows = []
    s4_rows = []
    for bid, payload in payloads.items():
        s1_rows.append(measure_symptom_1(bid, payload))
        s2_rows.append(measure_symptom_2(bid, payload))
        s3_rows.append(measure_symptom_3(bid, payload))
        s4_rows.append(measure_symptom_4(bid, payload))

    s2_roll = roll_up_symptom_2(s2_rows)
    s3_roll = roll_up_symptom_3(s3_rows)
    s4_roll = roll_up_symptom_4(s4_rows)

    # Symptom 1 is unmeasurable from JSON; report N/A
    s1_pass = None  # tri-state
    s2_pass = s2_roll["all_yes"]
    s3_pass = s3_roll["all_yes"]
    s4_pass = s4_roll["all_yes"]

    print()
    print("=" * 72)
    print("STEP 17 SYMPTOM ROLL-UP")
    print("=" * 72)
    print(f"Symptom 1 (project_name field_sources):     {'N/A — to_json() does not serialize project (see checklist §10 mismatch)' if s1_pass is None else ('PASS' if s1_pass else 'FAIL')}")
    print(f"Symptom 2 (single detected_system, never list): {'PASS' if s2_pass else 'FAIL'}")
    print(f"Symptom 3 (drawing/scope categories separate): {'PASS' if s3_pass else 'FAIL'}")
    print(f"Symptom 4 (sheet_map cleanliness):          {'PASS' if s4_pass else 'FAIL'}")
    print()

    print("Symptom 2 details:")
    for k, v in s2_roll["specific_questions"].items():
        print(f"    {k:<60}  {'YES' if v else 'NO'}")
    print()

    print("Symptom 3 details:")
    print(f"    roof_plan total v0.1: {V01_BASELINE_ROOF_PLAN_TOTAL}, explicit: {V01_BASELINE_ROOF_PLAN_EXPLICIT}, ratio: {V01_BASELINE_RATIO:.4f}")
    print(f"    roof_plan total v0.2: {s3_roll['roof_plan_total_v02']}, explicit: {s3_roll['roof_plan_explicit_v02']}, ratio: {s3_roll['ratio_v02']:.4f}")
    for k, v in s3_roll["specific_questions"].items():
        print(f"    {k:<60}  {'YES' if v else 'NO'}")
    print()

    print("Symptom 4 details:")
    if s4_roll["over_threshold_bidsets"]:
        print("  Bidsets with max-duplicate-sheet > 2 (excluding documented Bearss):")
        for r in s4_roll["over_threshold_bidsets"]:
            print(f"    {r['bidset_id']:<60} max_count={r['max_count']} most_common={r['most_common']}")
    for k, v in s4_roll["specific_questions"].items():
        print(f"    {k:<60}  {'YES' if v else 'NO'}")
    print()

    # Gate decision
    measurable_pass_count = sum(1 for p in (s2_pass, s3_pass, s4_pass) if p)
    print("=" * 72)
    print("GATE DECISION")
    print("=" * 72)
    print(f"  Measurable symptoms passing: {measurable_pass_count} / 3")
    print(f"  Symptom 1 status: N/A (unmeasurable from JSON)")
    print()
    if s1_pass is None:
        print("  Per checklist gate threshold (>=3 of 4 PASS): the un-measurable")
        print("  Symptom 1 prevents reaching 4 PASS even if 2/3/4 all green.")
        print(f"  Strict reading: {measurable_pass_count} measured PASS, threshold 3, "
              f"{'STOP per <3-of-4 rule (open Discovered Issue)' if measurable_pass_count < 3 else 'inconclusive — Daniel decides whether to count S1 as PASS, FAIL, or N/A in the gate'}")

    summary = {
        "n_bidsets": len(payloads),
        "symptom_1": {
            "status": "unmeasurable",
            "reason": "to_json() does not serialize PlanSetContext.project",
            "checklist_section_10_mismatch": True,
            "rows": s1_rows,
        },
        "symptom_2": {
            "pass": s2_pass,
            "roll_up": s2_roll,
            "rows": s2_rows,
        },
        "symptom_3": {
            "pass": s3_pass,
            "roll_up": s3_roll,
            "rows": s3_rows,
        },
        "symptom_4": {
            "pass": s4_pass,
            "roll_up": s4_roll,
            "rows": s4_rows,
        },
        "gate": {
            "measurable_pass_count": measurable_pass_count,
            "symptom_1_status": "N/A",
        },
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2, default=str))
    print()
    print(f"OK summary written to {SUMMARY_JSON.relative_to(BACKEND_DIR)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
