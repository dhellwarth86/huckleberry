"""analyze_outputs.py — read the 15 per-PDF JSONs, produce the coverage
matrix, dispatch accuracy ratio, and observed-fields inventory used to
populate EXPERIMENT_FINDINGS.md and inform schema design.

Output: two side files in backend/test_fixtures/:
  - experiment_summary.json  — machine-readable
  - experiment_summary.md    — human-readable digest

Run AFTER run_experiment.py finishes (or with --partial for partial data).
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

BACKEND_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BACKEND_DIR / "test_fixtures" / "experiment_outputs"
SUMMARY_JSON = BACKEND_DIR / "test_fixtures" / "experiment_summary.json"
SUMMARY_MD = BACKEND_DIR / "test_fixtures" / "experiment_summary.md"


# Fields we want to track presence-of in the coverage matrix. Keys are
# top-level "field paths" the schema may eventually adopt.
FIELDS_TO_TRACK = [
    # source_pdf_ref-derived
    "source_pdf_ref.id",
    "source_pdf_ref.sha256",
    "source_pdf_ref.size_bytes",
    "source_pdf_ref.page_count",
    "source_pdf_ref.producer_hint",
    # dispatch
    "dispatch.page_classifications",
    "dispatch.sheet_map",
    "dispatch.cross_references_by_page",
    "dispatch.legends_by_page",
    "dispatch.project_metadata.project_name",
    "dispatch.project_metadata.project_address",
    "dispatch.project_metadata.project_number",
    "dispatch.project_metadata.owner",
    "dispatch.project_metadata.architect",
    "dispatch.project_metadata.total_building_sf",
    "dispatch.roof_page_indices",
    "dispatch.page_type_histogram",
    "dispatch.confidence_histogram",
    # scope
    "scope.systems",
    "scope.systems[*].system_type",
    "scope.systems[*].attachment",
    "scope.systems[*].manufacturer",
    "scope.systems[*].spec_sections",
    "scope.systems[*].thickness_markers",
    "scope.systems[*].source_pages",
    "scope.systems[*].confidence",
    "scope.evidence.spec_section_hits",
    "scope.evidence.manufacturer_hits",
    "scope.evidence.attachment_hits",
    "scope.evidence.thickness_markers",
    "scope.evidence.insulation_markers",
    "scope.evidence.florida_signals",
    "scope.evidence.system_type_keyword_hits",
    "scope.fallback_used",
    "scope.pages_skipped_glazing",
    # assembly
    "assembly.systems",
    "assembly.systems[*].matched_assembly_key",
    "assembly.systems[*].required_supported_components",
    "assembly.systems[*].required_missing_components",
    "assembly.systems[*].component_evidence",
    "assembly.systems[*].warnings",
    "assembly.florida_signals",
    # provenance
    "provenance.fields",
    # extraction_metrics
    "extraction_metrics.elapsed_seconds",
    "extraction_metrics.pages_processed",
    "extraction_metrics.scope_systems_identified",
]


def field_present(payload: dict, path: str) -> bool:
    """Return True if `path` exists and is non-empty/non-null in payload.

    Path uses dot notation. `[*]` means 'any element of the list satisfies
    the rest of the path' — used to check if any system has a manufacturer."""
    parts = path.split(".")
    cur: Any = payload
    for i, part in enumerate(parts):
        if part.endswith("[*]"):
            # Drill into list and recurse on remaining path
            base = part[:-3]
            if base:
                cur = cur.get(base) if isinstance(cur, dict) else None
            if not isinstance(cur, list) or not cur:
                return False
            rest = ".".join(parts[i + 1:])
            return any(field_present(item if isinstance(item, dict) else {"_": item}, rest or "_") for item in cur)
        if isinstance(cur, dict):
            cur = cur.get(part)
        else:
            return False
        if cur is None:
            return False
    if isinstance(cur, (list, dict, str)):
        return bool(cur)
    return cur is not None


def load_outputs() -> list[dict]:
    """Load all per-PDF JSONs in alphabetical order."""
    if not OUTPUTS_DIR.is_dir():
        print(f"ERROR: {OUTPUTS_DIR} doesn't exist", file=sys.stderr)
        return []
    payloads = []
    for path in sorted(OUTPUTS_DIR.glob("*.json")):
        if path.name.endswith(".tmp"):
            continue
        try:
            payloads.append(json.loads(path.read_text(encoding="utf-8")))
        except Exception as e:
            print(f"WARN: couldn't read {path.name}: {e}", file=sys.stderr)
    return payloads


def build_coverage_matrix(payloads: list[dict]) -> dict[str, Any]:
    """Coverage matrix: for each field, which bidsets had it."""
    matrix: dict[str, dict[str, bool]] = {}
    for f in FIELDS_TO_TRACK:
        matrix[f] = {}
        for p in payloads:
            matrix[f][p["id"]] = field_present(p, f)
    return matrix


def field_counts(matrix: dict[str, dict[str, bool]]) -> dict[str, int]:
    """For each field, how many bidsets had it."""
    return {f: sum(1 for v in row.values() if v) for f, row in matrix.items()}


def dispatch_accuracy(payloads: list[dict]) -> dict[str, Any]:
    """Compute the dispatch-classification ratio for the report.

    The march orders measure against `dispatch_seed.py`'s 52/60 baseline.
    Here we count: total roof_pages classified vs pages with sheet numbers
    that LOOK like architectural roof sheets (A-prefix) where the keyword
    classifier may have missed.
    """
    total_roof_classified = 0
    total_pages = 0
    a_sheets = 0
    a_sheets_classified_as_roof = 0
    a_sheets_classified_as_other = 0
    classified_distribution: Counter[str] = Counter()
    confidence_distribution: Counter[str] = Counter()
    no_match_unknown = 0

    for p in payloads:
        disp = p.get("dispatch", {})
        if not disp:
            continue
        for cls in disp.get("page_classifications", []):
            total_pages += 1
            classified_distribution[cls.get("page_type", "unknown")] += 1
            conf = cls.get("confidence", 0.0)
            if conf >= 0.85:
                confidence_distribution["explicit"] += 1
            elif conf >= 0.6:
                confidence_distribution["strong"] += 1
            elif conf >= 0.4:
                confidence_distribution["inferred"] += 1
            elif conf > 0.0:
                confidence_distribution["weak"] += 1
            else:
                confidence_distribution["unknown"] += 1
                if cls.get("page_type") == "unknown":
                    no_match_unknown += 1
            if cls.get("page_type") == "roof_plan":
                total_roof_classified += 1

            # Architectural sheet number heuristic — "A-1.3", "A-2.0"
            sheet = cls.get("sheet_number") or ""
            if sheet and sheet.startswith("A"):
                a_sheets += 1
                if cls.get("page_type") == "roof_plan":
                    a_sheets_classified_as_roof += 1
                else:
                    a_sheets_classified_as_other += 1

    return {
        "total_pages": total_pages,
        "total_roof_pages_classified": total_roof_classified,
        "architectural_sheets_total": a_sheets,
        "architectural_sheets_classified_roof": a_sheets_classified_as_roof,
        "architectural_sheets_classified_other": a_sheets_classified_as_other,
        "page_type_distribution": dict(classified_distribution),
        "confidence_distribution": dict(confidence_distribution),
        "no_keyword_match_unknown_count": no_match_unknown,
    }


def scope_summary(payloads: list[dict]) -> dict[str, Any]:
    """Summarize Layer 2 results: systems per bidset, manufacturer hits,
    fallback usage."""
    by_bidset: dict[str, Any] = {}
    system_type_counter: Counter[str] = Counter()
    manufacturer_counter: Counter[str] = Counter()
    attachment_counter: Counter[str] = Counter()
    thickness_counter: Counter[str] = Counter()
    florida_signal_counter: Counter[str] = Counter()
    insulation_counter: Counter[str] = Counter()
    fallback_count = 0
    bidsets_with_any_system = 0
    bidsets_with_manufacturer = 0
    bidsets_with_florida_signals = 0

    for p in payloads:
        scope = p.get("scope", {}) or {}
        systems = scope.get("systems", []) or []
        if systems:
            bidsets_with_any_system += 1
        if scope.get("fallback_used"):
            fallback_count += 1
        sys_summary = []
        manufacturers_in_bidset: set[str] = set()
        for s in systems:
            sys_t = s.get("system_type")
            attach = s.get("attachment")
            mfr = s.get("manufacturer")
            if sys_t:
                system_type_counter[sys_t] += 1
            if attach:
                attachment_counter[attach] += 1
            if mfr:
                manufacturer_counter[mfr] += 1
                manufacturers_in_bidset.add(mfr)
            sys_summary.append({
                "system_type": sys_t,
                "attachment": attach,
                "manufacturer": mfr,
                "confidence": s.get("confidence"),
                "spec_sections": s.get("spec_sections", []),
                "source_pages_count": len(s.get("source_pages", [])),
            })
        if manufacturers_in_bidset:
            bidsets_with_manufacturer += 1

        evidence = scope.get("evidence", {}) or {}
        for h in evidence.get("thickness_markers", []) or []:
            thickness_counter[h.get("marker", "?")] += 1
        for h in evidence.get("florida_signals", []) or []:
            florida_signal_counter[h.get("marker", "?")] += 1
        for h in evidence.get("insulation_markers", []) or []:
            insulation_counter[h.get("marker", "?")] += 1
        if evidence.get("florida_signals"):
            bidsets_with_florida_signals += 1
        by_bidset[p["id"]] = sys_summary

    return {
        "by_bidset": by_bidset,
        "system_type_counts": dict(system_type_counter.most_common()),
        "manufacturer_counts": dict(manufacturer_counter.most_common()),
        "attachment_counts": dict(attachment_counter.most_common()),
        "thickness_marker_counts": dict(thickness_counter.most_common()),
        "florida_signal_counts": dict(florida_signal_counter.most_common()),
        "insulation_marker_counts": dict(insulation_counter.most_common()),
        "fallback_used_count": fallback_count,
        "bidsets_with_any_system": bidsets_with_any_system,
        "bidsets_with_manufacturer": bidsets_with_manufacturer,
        "bidsets_with_florida_signals": bidsets_with_florida_signals,
    }


def assembly_summary(payloads: list[dict]) -> dict[str, Any]:
    """Summarize Layer 3 results: components-supported ratio, warning trigger counts."""
    total_required = 0
    total_supported = 0
    warning_counter: Counter[str] = Counter()
    matched_assemblies: Counter[str] = Counter()
    bidsets_with_warnings = 0
    by_bidset: dict[str, Any] = {}
    bidsets_with_matched = 0

    for p in payloads:
        asm = p.get("assembly", {}) or {}
        sys_list = asm.get("systems", []) or []
        any_match = False
        any_warning = False
        bidset_supported = []
        for s in sys_list:
            if s.get("matched_assembly_key"):
                any_match = True
                matched_assemblies[s["matched_assembly_key"]] += 1
            req_total = s.get("required_total", 0) or 0
            req_sup = s.get("required_supported", 0) or 0
            total_required += req_total
            total_supported += req_sup
            for w in s.get("warnings", []) or []:
                warning_counter[w["id"]] += 1
                any_warning = True
            bidset_supported.append({
                "system_type": s.get("system_type"),
                "matched_assembly_key": s.get("matched_assembly_key"),
                "required_supported": req_sup,
                "required_total": req_total,
                "warning_ids": [w["id"] for w in (s.get("warnings") or [])],
            })
        if any_match:
            bidsets_with_matched += 1
        if any_warning:
            bidsets_with_warnings += 1
        by_bidset[p["id"]] = bidset_supported

    pct = (100.0 * total_supported / total_required) if total_required else 0.0
    return {
        "by_bidset": by_bidset,
        "matched_assembly_counts": dict(matched_assemblies.most_common()),
        "warning_id_counts": dict(warning_counter.most_common()),
        "components_required_total": total_required,
        "components_supported_total": total_supported,
        "components_supported_pct": round(pct, 1),
        "bidsets_with_matched_assembly": bidsets_with_matched,
        "bidsets_with_any_warning": bidsets_with_warnings,
    }


# ─── Inclusion rule ──────────────────────────────────────────────────────────

# Each tracked field gets a downstream-consumer note. This is the "is there
# a real or near-future user-facing capability that consumes this?" criterion.
# Fields without a consumer get DEFERRED no matter how often they appear.
FIELD_CONSUMERS: dict[str, str | None] = {
    # source_pdf_ref
    "source_pdf_ref.id":            "Routing key on every API call between frontend and backend.",
    "source_pdf_ref.sha256":        "Integrity check on download; deduplication.",
    "source_pdf_ref.size_bytes":    "Storage accounting.",
    "source_pdf_ref.page_count":    "PAGES-tab thumbnail grid + viewer page navigation in v0.3.",
    "source_pdf_ref.producer_hint": None,  # interesting but no near-term consumer
    # dispatch
    "dispatch.page_classifications":         "PAGES-tab classification badges; viewer's first-page-defaults-to-roof_plan logic.",
    "dispatch.sheet_map":                    "Sheet-number column in TAKEOFF / Excel export; deep-link references.",
    "dispatch.cross_references_by_page":     None,  # speculative; defer
    "dispatch.legends_by_page":              None,  # speculative; defer
    "dispatch.project_metadata.project_name":     "Excel export header; project search.",
    "dispatch.project_metadata.project_address":  "Excel export header; HVHZ county determination (FBC).",
    "dispatch.project_metadata.project_number":   "Excel export header; estimator filing reference.",
    "dispatch.project_metadata.owner":            None,  # nice-to-have; defer
    "dispatch.project_metadata.architect":        None,  # nice-to-have; defer
    "dispatch.project_metadata.total_building_sf":"Sanity-check vs measured roof area.",
    "dispatch.roof_page_indices":            "Viewer auto-navigates to first roof page on PDF open.",
    "dispatch.page_type_histogram":          None,  # debugging only; defer
    "dispatch.confidence_histogram":         None,  # debugging only; defer
    # scope
    "scope.systems":                                "SCOPE-tab card list; per-system Excel sheets.",
    "scope.systems[*].system_type":                 "Pin/edge/polygon palette derivation; assembly lookup.",
    "scope.systems[*].attachment":                  "Disambiguates which ROOF_SYSTEMS entry to use.",
    "scope.systems[*].manufacturer":                "Excel Manufacturer column; vendor-specific NOA/spec data.",
    "scope.systems[*].spec_sections":               "Cross-reference back to spec page; estimator audit trail.",
    "scope.systems[*].thickness_markers":           "Excel material column; warranty calculation.",
    "scope.systems[*].source_pages":                "Click-to-page navigation in SCOPE tab.",
    "scope.systems[*].confidence":                  "Drives 'parser said X, please confirm' UX in v0.3.",
    "scope.evidence.spec_section_hits":             "Provenance audit trail; not user-facing directly.",
    "scope.evidence.manufacturer_hits":             "Provenance audit trail.",
    "scope.evidence.attachment_hits":               "Provenance audit trail.",
    "scope.evidence.thickness_markers":             "Provenance.",
    "scope.evidence.insulation_markers":            "Provenance + flat-roof detection.",
    "scope.evidence.florida_signals":               "Triggers FBC HVHZ warning chip in SCOPE / TAKEOFF.",
    "scope.evidence.system_type_keyword_hits":      "Provenance.",
    "scope.fallback_used":                          "QA flag — fallback systems show 'low confidence' badge.",
    "scope.pages_skipped_glazing":                  None,  # debugging only; defer
    # assembly
    "assembly.systems":                             "TAKEOFF tab line items.",
    "assembly.systems[*].matched_assembly_key":     "Drives takeoff component shopping list.",
    "assembly.systems[*].required_supported_components":  "Excel takeoff rows that have evidence.",
    "assembly.systems[*].required_missing_components":    "Excel takeoff rows flagged 'expected but not found'.",
    "assembly.systems[*].component_evidence":             "Provenance per takeoff row.",
    "assembly.systems[*].warnings":                       "TAKEOFF / SCOPE warning chips.",
    "assembly.florida_signals":                           "FBC warning panel.",
    # provenance
    "provenance.fields":                            "Phase 3 ML training labels; v0.3 'parser said vs you said' UX.",
    # metrics
    "extraction_metrics.elapsed_seconds":           None,  # debugging only
    "extraction_metrics.pages_processed":           None,
    "extraction_metrics.scope_systems_identified":  None,
}


def apply_inclusion_rule(field_counts: dict[str, int], n_total: int, threshold: int = 3) -> dict[str, dict]:
    """For each tracked field, decide promote/defer with the two-criteria rule.

    A field is promoted iff:
      (1) field_count >= threshold, AND
      (2) FIELD_CONSUMERS[field] is not None (downstream consumer identified)

    Returns a dict keyed by field with: {count, threshold_met, has_consumer, consumer, decision}.
    """
    out = {}
    for field, count in field_counts.items():
        consumer = FIELD_CONSUMERS.get(field)
        threshold_met = count >= threshold
        has_consumer = consumer is not None
        if threshold_met and has_consumer:
            decision = "PROMOTE"
        elif not threshold_met and not has_consumer:
            decision = "DEFER (frequency + consumer)"
        elif not threshold_met:
            decision = "DEFER (frequency)"
        else:
            decision = "DEFER (consumer)"
        out[field] = {
            "count": count,
            "out_of": n_total,
            "threshold": threshold,
            "threshold_met": threshold_met,
            "has_consumer": has_consumer,
            "consumer": consumer,
            "decision": decision,
        }
    return out


def render_md(matrix: dict[str, dict[str, bool]],
              counts: dict[str, int],
              dispatch_acc: dict[str, Any],
              scope_sum: dict[str, Any],
              assembly_sum: dict[str, Any],
              decisions: dict[str, dict],
              payloads: list[dict]) -> str:
    bidset_ids = [p["id"] for p in payloads]
    n = len(payloads)

    lines: list[str] = []
    lines.append(f"# Experiment summary — auto-generated\n")
    lines.append(f"Generated from {n} per-bidset JSON outputs in `experiment_outputs/`.\n")
    lines.append("This file is the analysis script's output and is regenerated by ")
    lines.append("`backend/scripts/analyze_outputs.py`. The narrative findings live ")
    lines.append("in `EXPERIMENT_FINDINGS.md`; this digest backs them.\n\n")

    # Coverage matrix
    lines.append("## Coverage matrix\n")
    short_ids = []
    for bid in bidset_ids:
        first = bid.split("-")[0]
        short_ids.append(first[:8])
    lines.append(f"Columns are bidset short-ids: " + ", ".join(f"`{s}`" for s in short_ids) + "\n\n")
    lines.append("| Field | " + " | ".join(short_ids) + " | Count |")
    lines.append("|" + "---|" * (len(short_ids) + 2))
    for f in FIELDS_TO_TRACK:
        row = matrix.get(f, {})
        cells = ["X" if row.get(b) else "." for b in bidset_ids]
        lines.append(f"| `{f}` | " + " | ".join(cells) + f" | {counts.get(f, 0)}/{n} |")
    lines.append("")

    # Dispatch accuracy
    lines.append("## Dispatch layer accuracy\n")
    lines.append(f"- Total pages classified: **{dispatch_acc['total_pages']}**")
    lines.append(f"- Pages classified as roof_plan: **{dispatch_acc['total_roof_pages_classified']}**")
    lines.append(f"- Architectural-sheet pages (A-prefix): **{dispatch_acc['architectural_sheets_total']}**")
    lines.append(f"  - of which classified as roof_plan: **{dispatch_acc['architectural_sheets_classified_roof']}**")
    lines.append(f"  - of which classified as other type: **{dispatch_acc['architectural_sheets_classified_other']}**")
    lines.append(f"- Pages with no keyword match (page_type=unknown): **{dispatch_acc['no_keyword_match_unknown_count']}**")
    lines.append("\n### Page-type distribution\n")
    for k, v in sorted(dispatch_acc["page_type_distribution"].items(), key=lambda kv: -kv[1]):
        lines.append(f"- {k}: {v}")
    lines.append("\n### Confidence distribution\n")
    for k, v in sorted(dispatch_acc["confidence_distribution"].items(), key=lambda kv: -kv[1]):
        lines.append(f"- {k}: {v}")
    lines.append("")

    # Scope summary
    lines.append("## Scope layer summary\n")
    lines.append(f"- Bidsets with any system identified: **{scope_sum['bidsets_with_any_system']}/{n}**")
    lines.append(f"- Bidsets with at least one manufacturer attached: **{scope_sum['bidsets_with_manufacturer']}/{n}**")
    lines.append(f"- Bidsets with Florida signals (FBC/HVHZ/NOA/etc): **{scope_sum['bidsets_with_florida_signals']}/{n}**")
    lines.append(f"- Bidsets where fallback was used: **{scope_sum['fallback_used_count']}/{n}**")

    lines.append("\n### System type counts (across all bidsets)\n")
    for k, v in scope_sum["system_type_counts"].items():
        lines.append(f"- {k}: {v}")
    lines.append("\n### Manufacturer counts\n")
    for k, v in scope_sum["manufacturer_counts"].items():
        lines.append(f"- {k}: {v}")
    lines.append("\n### Attachment method counts\n")
    for k, v in scope_sum["attachment_counts"].items():
        lines.append(f"- {k}: {v}")
    lines.append("\n### Thickness marker counts\n")
    for k, v in scope_sum["thickness_marker_counts"].items():
        lines.append(f"- {k}: {v}")
    lines.append("\n### Florida signal counts\n")
    for k, v in scope_sum["florida_signal_counts"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")

    # Assembly summary
    lines.append("## Assembly layer summary\n")
    lines.append(f"- Bidsets with at least one matched assembly: **{assembly_sum['bidsets_with_matched_assembly']}/{n}**")
    lines.append(f"- Bidsets with any warning fired: **{assembly_sum['bidsets_with_any_warning']}/{n}**")
    lines.append(f"- Required components supported by text evidence: **{assembly_sum['components_supported_total']}/{assembly_sum['components_required_total']}**  ({assembly_sum['components_supported_pct']}%)")
    lines.append("\n### Matched assembly counts\n")
    for k, v in assembly_sum["matched_assembly_counts"].items():
        lines.append(f"- {k}: {v}")
    lines.append("\n### Warning trigger counts\n")
    for k, v in assembly_sum["warning_id_counts"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")

    # Inclusion-rule decisions
    lines.append("## Inclusion-rule decisions\n")
    promotes = sorted([f for f, d in decisions.items() if d["decision"] == "PROMOTE"])
    defers = sorted([f for f, d in decisions.items() if d["decision"] != "PROMOTE"])
    lines.append(f"### PROMOTE ({len(promotes)} fields)\n")
    lines.append("| Field | Bidset count | Consumer |")
    lines.append("|---|---|---|")
    for f in promotes:
        d = decisions[f]
        lines.append(f"| `{f}` | {d['count']}/{d['out_of']} | {d['consumer']} |")
    lines.append(f"\n### DEFER ({len(defers)} fields)\n")
    lines.append("| Field | Count | Decision | Notes |")
    lines.append("|---|---|---|---|")
    for f in defers:
        d = decisions[f]
        lines.append(f"| `{f}` | {d['count']}/{d['out_of']} | {d['decision']} | {d.get('consumer') or '(no consumer identified)'} |")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=int, default=3, help="Inclusion-rule threshold (default 3)")
    parser.add_argument("--partial", action="store_true", help="Don't error if fewer than 15 outputs found")
    args = parser.parse_args()

    payloads = load_outputs()
    if not payloads:
        print("No outputs to analyze.", file=sys.stderr)
        return 2
    if len(payloads) < 15 and not args.partial:
        print(f"Only {len(payloads)}/15 outputs found. Use --partial to analyze anyway.", file=sys.stderr)
        return 2

    matrix = build_coverage_matrix(payloads)
    counts = field_counts(matrix)
    dispatch_acc = dispatch_accuracy(payloads)
    scope_sum = scope_summary(payloads)
    assembly_sum = assembly_summary(payloads)
    decisions = apply_inclusion_rule(counts, len(payloads), args.threshold)

    summary = {
        "n_bidsets": len(payloads),
        "bidset_ids": [p["id"] for p in payloads],
        "field_counts": counts,
        "coverage_matrix": matrix,
        "dispatch_accuracy": dispatch_acc,
        "scope_summary": scope_sum,
        "assembly_summary": assembly_sum,
        "inclusion_decisions": decisions,
    }

    SUMMARY_JSON.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2, default=str))
    print(f"OK summary JSON: {SUMMARY_JSON.relative_to(BACKEND_DIR)}")

    md = render_md(matrix, counts, dispatch_acc, scope_sum, assembly_sum, decisions, payloads)
    SUMMARY_MD.write_text(md)
    print(f"OK summary MD:   {SUMMARY_MD.relative_to(BACKEND_DIR)}")

    n_promote = sum(1 for d in decisions.values() if d["decision"] == "PROMOTE")
    n_defer = sum(1 for d in decisions.values() if d["decision"] != "PROMOTE")
    print(f"\n  PROMOTE: {n_promote}  DEFER: {n_defer}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
