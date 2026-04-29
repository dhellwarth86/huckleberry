"""intake_diagnostic.py — read-only diagnostic measuring what dispatch's
intake actually saw on each of 19 bidsets (15 STACK + 4 public-corpus) vs
what the scope scanner detected.

Reads:
  - JSON outputs at:
      backend/test_fixtures/v0.2_outputs/<bidset_id>.json     (15 STACK)
      backend/test_fixtures/public_corpus_outputs/<bidset_id>.json  (4 public)
  - Source PDFs at:
      C:/huck stage 2/full bid sets/                          (15 STACK)
      C:/huck stage 2/not_stack-bidsets/                       (4 public)
  - Vocabulary from seeds/roofing_spec_database.py (verbatim, not extended)

Writes:
  - Per-bidset per-page CSV:
      backend/test_fixtures/intake_diagnostic_outputs/<bidset_id>.csv
  - Markdown summary at:
      backend/INTAKE_DIAGNOSTIC.md (NOT written here — separate writeup step)
  - Machine-readable summary:
      backend/test_fixtures/intake_diagnostic_summary.json

DOES NOT modify any ported file. DOES NOT extend vocabulary. DOES NOT
propose fixes. DOES NOT compare to ground-truth (no ground-truth exists).
"""

from __future__ import annotations

import csv
import json
import re
import sys
import time
import traceback
from collections import Counter
from pathlib import Path
from typing import Any

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

import fitz  # PyMuPDF — same library dispatch_gate uses for text extraction

from seeds.roofing_spec_database import (  # noqa: E402
    SPEC_SECTIONS,
    MANUFACTURERS,
    MATERIAL_PROPERTIES,
    all_manufacturer_names,
)

STACK_MANIFEST = BACKEND_DIR / "test_fixtures" / "bidsets.json"
STACK_OUTPUTS_DIR = BACKEND_DIR / "test_fixtures" / "v0.2_outputs"
PUBLIC_OUTPUTS_DIR = BACKEND_DIR / "test_fixtures" / "public_corpus_outputs"

PER_PAGE_CSV_DIR = BACKEND_DIR / "test_fixtures" / "intake_diagnostic_outputs"
SUMMARY_JSON = BACKEND_DIR / "test_fixtures" / "intake_diagnostic_summary.json"

PUBLIC_CORPUS_BIDSETS = [
    {
        "id": "suwannee-county-school-board-suwannee-high-school-courtyard-renovation",
        "filename": "suwannee county school board suwannee high school courtyard renovation.pdf",
        "local_path": "C:/huck stage 2/not_stack-bidsets/suwannee county school board suwannee high school courtyard renovation.pdf",
        "page_count": 31,
    },
    {
        "id": "holabird-academy-elementary-middle-school",
        "filename": "Holabird academy elementary-middle school.pdf",
        "local_path": "C:/huck stage 2/not_stack-bidsets/Holabird academy elementary-middle school.pdf",
        "page_count": 96,
    },
    {
        "id": "sanibel-fire-and-rescue-station-172",
        "filename": "Sanibel Fire and Rescue station 172.pdf",
        "local_path": "C:/huck stage 2/not_stack-bidsets/Sanibel Fire and Rescue station 172.pdf",
        "page_count": 90,
    },
    {
        "id": "uccs-cybersecurity-and-space-ecosystem-expansion",
        "filename": "UCCS cybersecurity and space ecosystem expansion.pdf",
        "local_path": "C:/huck stage 2/not_stack-bidsets/UCCS cybersecurity and space ecosystem expansion.pdf",
        "page_count": 133,
    },
]


# ─── Vocabulary (verbatim from seeds/roofing_spec_database.py) ──────────

# system_signal: distinct membrane chemistry tokens from SPEC_SECTIONS values'
#   "system" field. EPDM is added because it appears in MANUFACTURERS.systems
#   even though no SPEC_SECTIONS entry maps to it directly.
SYSTEM_TOKENS = sorted({v["system"] for v in SPEC_SECTIONS.values() if v.get("system")} | {"epdm"})
# Build whole-word patterns; treat "tpo" / "pvc" specially (often appear inside
# longer words; require word boundary).
_SYSTEM_PATTERNS = [
    (tok, re.compile(rf"\b{re.escape(tok.replace('_', ' '))}\b", re.IGNORECASE))
    for tok in SYSTEM_TOKENS
]
# Also map "modified bitumen" → modified_bitumen, "built up" → built_up, etc.
_SYSTEM_ALIASES = {
    "modified bitumen": "modified_bitumen",
    "modified-bitumen": "modified_bitumen",
    "mod-bit": "modified_bitumen",
    "mod bit": "modified_bitumen",
    "built up": "built_up",
    "built-up": "built_up",
    "bur": "built_up",
    "metal panel": "metal_panel",
    "standing seam": "metal_panel",
}
_SYSTEM_ALIAS_PATTERNS = [
    (canonical, re.compile(rf"\b{re.escape(alias)}\b", re.IGNORECASE))
    for alias, canonical in _SYSTEM_ALIASES.items()
]

# spec_section: Division 7 section number patterns ("07 54", "07 54 23",
# "07-54", "075400" etc.). Same shape as dispatch_gate._SPEC_SECTION_RX
# but limited here to Division 07 only.
_SPEC_SECTION_RX = re.compile(r"\b(0?7)[\s\-]?(\d{2})(?:[\s\-]?(\d{2,4}))?\b")

# manufacturer: full search-name → canonical map from
# all_manufacturer_names() (canonical + aliases + product names).
_MFR_PAIRS = all_manufacturer_names()  # already sorted longest-first

# manufacturer regex patterns (case-insensitive whole-word)
_MFR_PATTERNS = [
    (canonical, search_name, re.compile(rf"\b{re.escape(search_name)}\b", re.IGNORECASE))
    for search_name, canonical in _MFR_PAIRS
]

# Material markers
_THICKNESS_KEYS = list(MATERIAL_PROPERTIES["thickness_markers"].keys())
_INSULATION_KEYS = list(MATERIAL_PROPERTIES["insulation_markers"].keys())
_METAL_MARKER_KEYS = list(MATERIAL_PROPERTIES["metal_markers"].keys())
_FLORIDA_SIGNAL_KEYS = list(MATERIAL_PROPERTIES["florida_signals"].keys())

_MATERIAL_PATTERNS = {
    "thickness": [(k, re.compile(rf"\b{re.escape(k)}\b", re.IGNORECASE)) for k in _THICKNESS_KEYS],
    "insulation": [(k, re.compile(rf"\b{re.escape(k)}\b", re.IGNORECASE)) for k in _INSULATION_KEYS],
    "metal": [(k, re.compile(rf"\b{re.escape(k)}\b", re.IGNORECASE)) for k in _METAL_MARKER_KEYS],
}
_FLORIDA_PATTERNS = [(k, re.compile(rf"\b{re.escape(k)}\b", re.IGNORECASE)) for k in _FLORIDA_SIGNAL_KEYS]

# Accessory: SPEC_SECTIONS entries WITHOUT a system mapping (scope-related but
# not a primary system). Keys: 07 71 (Roof Specialties), 07 72 (Roof
# Accessories), 07 84 (Firestopping), 07 92 (Joint Sealants).
_ACCESSORY_SECTIONS = {k for k, v in SPEC_SECTIONS.items() if v.get("system") is None and not v.get("signal")}
_ACCESSORY_NAMES = {SPEC_SECTIONS[k]["name"].lower() for k in _ACCESSORY_SECTIONS}

# Negation phrases. Daniel's brief specifies these three exactly.
_NEGATION_PHRASES = ["NOT ACCEPTABLE", "NOT PERMITTED", "NOT APPROVED"]
_NEGATION_RX = re.compile(r"\b(NOT\s+(?:ACCEPTABLE|PERMITTED|APPROVED))\b", re.IGNORECASE)
NEGATION_RADIUS_CHARS = 50


# ─── Helpers ────────────────────────────────────────────────────────────

_DISCIPLINE_PREFIX_RX = re.compile(r"^([A-Z]{1,2})")


def discipline_prefix(sheet_number: str | None) -> str:
    if not sheet_number:
        return ""
    m = _DISCIPLINE_PREFIX_RX.match(sheet_number.strip().upper())
    return m.group(1) if m else ""


def scan_systems(text: str) -> list[str]:
    hits: list[str] = []
    seen: set[str] = set()
    for tok, pat in _SYSTEM_PATTERNS:
        if pat.search(text) and tok not in seen:
            hits.append(tok)
            seen.add(tok)
    for canonical, pat in _SYSTEM_ALIAS_PATTERNS:
        if pat.search(text) and canonical not in seen:
            hits.append(canonical)
            seen.add(canonical)
    return hits


def scan_spec_sections(text: str) -> list[str]:
    """Return the matching SPEC_SECTIONS keys found in text (Division 07 only)."""
    keys: list[str] = []
    seen: set[str] = set()
    for m in _SPEC_SECTION_RX.finditer(text):
        a, b, c = m.group(1), m.group(2), m.group(3)
        if a.lstrip("0") != "7":  # restrict to Division 7
            continue
        # Try most-specific to least-specific lookup
        candidates = []
        if c:
            sub2 = c[:2]
            sub4 = c[:4]
            candidates.append(f"{int(a):02d} {b} {sub4}" if len(c) >= 4 else f"{int(a):02d} {b} {sub2}")
            candidates.append(f"{int(a):02d}{b}{sub2}")
            candidates.append(f"{int(a):02d} {b}{sub2}")
        candidates.append(f"{int(a):02d} {b}")
        for cand in candidates:
            if cand in SPEC_SECTIONS:
                if cand not in seen:
                    keys.append(cand)
                    seen.add(cand)
                break
    return keys


def scan_manufacturers(text: str) -> list[dict[str, Any]]:
    """Return list of {canonical, matched_name, position, negated}.
    A hit is "negated" if a NEGATION_PHRASE appears within ±50 chars."""
    if not text:
        return []
    out: list[dict[str, Any]] = []
    seen_canonicals: set[str] = set()
    for canonical, search_name, pat in _MFR_PATTERNS:
        if canonical in seen_canonicals:
            # Only record one position per canonical to keep CSV bounded.
            continue
        m = pat.search(text)
        if not m:
            continue
        seen_canonicals.add(canonical)
        # Negation context: window ±50 chars around the hit
        start = max(0, m.start() - NEGATION_RADIUS_CHARS)
        end = min(len(text), m.end() + NEGATION_RADIUS_CHARS)
        window = text[start:end]
        negated = bool(_NEGATION_RX.search(window))
        out.append({
            "canonical": canonical,
            "matched_name": search_name,
            "position": m.start(),
            "negated": negated,
            "window": window.replace("\n", " "),
        })
    return out


def scan_material_markers(text: str) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for cat, pats in _MATERIAL_PATTERNS.items():
        hits: list[str] = []
        seen: set[str] = set()
        for k, pat in pats:
            if pat.search(text) and k not in seen:
                hits.append(k)
                seen.add(k)
        if hits:
            out[cat] = hits
    return out


def scan_florida(text: str) -> list[str]:
    hits: list[str] = []
    seen: set[str] = set()
    for k, pat in _FLORIDA_PATTERNS:
        if pat.search(text) and k not in seen:
            hits.append(k)
            seen.add(k)
    return hits


def scan_accessory(text: str, spec_section_hits: list[str]) -> bool:
    """An 'accessory' hit = at least one SPEC_SECTION key from the
    accessory subset (07 71, 07 72, 07 84, 07 92) was found in spec
    section scan. Returns True/False."""
    return any(k in _ACCESSORY_SECTIONS for k in spec_section_hits)


# ─── Per-page processing ────────────────────────────────────────────────

def process_page(text: str, page_idx: int, json_data: dict, scope_pages_set: set[int],
                 unresolved_xref_count_per_page: dict[int, int]) -> dict[str, Any]:
    pages_meta = json_data.get("pages", {})
    pc = pages_meta.get(str(page_idx), {})
    sheet_num = pc.get("sheet_number")
    page_type = pc.get("page_type", "unknown")
    confidence = pc.get("confidence", 0.0)
    discipline = discipline_prefix(sheet_num)

    word_count = len(text.split())
    in_scope_pages = page_idx in scope_pages_set

    sys_hits = scan_systems(text)
    spec_hits = scan_spec_sections(text)
    mfr_hits = scan_manufacturers(text)
    mfr_positive = sum(1 for h in mfr_hits if not h["negated"])
    mfr_negation = sum(1 for h in mfr_hits if h["negated"])
    material_hits = scan_material_markers(text)
    florida_hits = scan_florida(text)
    accessory_hit = scan_accessory(text, spec_hits)
    unresolved_xrefs = unresolved_xref_count_per_page.get(page_idx, 0)

    has_roofing_evidence = bool(
        sys_hits or spec_hits or mfr_hits or material_hits or florida_hits
    )

    return {
        "page_index": page_idx,
        "sheet_number": sheet_num or "",
        "discipline_prefix": discipline,
        "page_type": page_type,
        "confidence": confidence,
        "word_count": word_count,
        "in_scope_pages": in_scope_pages,
        "system_hits": ";".join(sys_hits),
        "spec_section_hits": ";".join(spec_hits),
        "manufacturer_hits_total": len(mfr_hits),
        "manufacturer_hits_positive": mfr_positive,
        "manufacturer_hits_negation": mfr_negation,
        "manufacturer_hit_names": ";".join(h["canonical"] for h in mfr_hits),
        "material_thickness_hits": ";".join(material_hits.get("thickness", [])),
        "material_insulation_hits": ";".join(material_hits.get("insulation", [])),
        "material_metal_hits": ";".join(material_hits.get("metal", [])),
        "florida_signal_hits": ";".join(florida_hits),
        "accessory_hit": accessory_hit,
        "unresolved_xrefs_on_page": unresolved_xrefs,
        "has_roofing_evidence": has_roofing_evidence,
    }


def unresolved_xrefs_per_page(json_data: dict) -> dict[int, int]:
    counter: dict[int, int] = {}
    for ref in json_data.get("all_cross_refs", []) or []:
        if not ref.get("resolved"):
            sp = ref.get("source_page")
            if isinstance(sp, int):
                counter[sp] = counter.get(sp, 0) + 1
    return counter


def process_bidset(bidset_id: str, pdf_path: Path, json_path: Path) -> dict[str, Any]:
    json_data = json.loads(json_path.read_text(encoding="utf-8"))
    ps = json_data.get("project_scope") or {}
    scope_pages_set = set(ps.get("scope_pages") or [])
    unresolved_per_page = unresolved_xrefs_per_page(json_data)

    rows: list[dict[str, Any]] = []
    doc = fitz.open(str(pdf_path))
    try:
        for idx in range(doc.page_count):
            try:
                page = doc.load_page(idx)
                text = page.get_text("text") or ""
            except Exception as e:
                text = ""
                # Continue with empty text — diagnostic does not crash on bad pages
            row = process_page(text, idx, json_data, scope_pages_set, unresolved_per_page)
            rows.append(row)
    finally:
        doc.close()

    # Per-bidset aggregate
    n_pages = len(rows)
    zero_text_pages = sum(1 for r in rows if r["word_count"] == 0)
    pages_with_evidence = sum(1 for r in rows if r["has_roofing_evidence"])
    pages_in_scope = sum(1 for r in rows if r["in_scope_pages"])
    mfr_pos_total = sum(r["manufacturer_hits_positive"] for r in rows)
    mfr_neg_total = sum(r["manufacturer_hits_negation"] for r in rows)
    mfr_canonicals_seen: set[str] = set()
    for r in rows:
        for c in r["manufacturer_hit_names"].split(";"):
            if c:
                mfr_canonicals_seen.add(c)
    accessory_pages = sum(1 for r in rows if r["accessory_hit"])

    aggregate = {
        "bidset_id": bidset_id,
        "n_pages": n_pages,
        "zero_text_pages": zero_text_pages,
        "pages_with_roofing_evidence": pages_with_evidence,
        "pages_in_scope_pages": pages_in_scope,
        "scope_pages_indices": sorted(scope_pages_set),
        "scanner_detected_system": ps.get("detected_system"),
        "scanner_system_confidence": ps.get("system_confidence", 0.0),
        "scanner_system_evidence": (ps.get("system_evidence") or "")[:200],
        "manufacturer_hits_positive_total": mfr_pos_total,
        "manufacturer_hits_negation_total": mfr_neg_total,
        "manufacturer_canonicals_seen": sorted(mfr_canonicals_seen),
        "accessory_pages": accessory_pages,
        "page_type_histogram": dict(Counter(r["page_type"] for r in rows)),
    }
    return {"aggregate": aggregate, "rows": rows}


def write_csv(bidset_id: str, rows: list[dict[str, Any]]) -> Path:
    PER_PAGE_CSV_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PER_PAGE_CSV_DIR / f"{bidset_id}.csv"
    fieldnames = [
        "page_index", "sheet_number", "discipline_prefix", "page_type", "confidence",
        "word_count", "in_scope_pages", "has_roofing_evidence",
        "system_hits", "spec_section_hits",
        "manufacturer_hits_total", "manufacturer_hits_positive", "manufacturer_hits_negation",
        "manufacturer_hit_names",
        "material_thickness_hits", "material_insulation_hits", "material_metal_hits",
        "florida_signal_hits", "accessory_hit", "unresolved_xrefs_on_page",
    ]
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    return out_path


def load_stack_bidsets() -> list[dict[str, Any]]:
    """Return list of {id, local_path, json_path, page_count} for STACK."""
    if not STACK_MANIFEST.exists():
        print(f"ERROR: STACK manifest not found at {STACK_MANIFEST}", file=sys.stderr)
        return []
    manifest = json.loads(STACK_MANIFEST.read_text(encoding="utf-8"))
    out: list[dict[str, Any]] = []
    for entry in manifest.get("bidsets", []):
        json_path = STACK_OUTPUTS_DIR / f"{entry['id']}.json"
        if not json_path.exists():
            continue
        out.append({
            "id": entry["id"],
            "local_path": entry["local_path"],
            "json_path": str(json_path),
            "page_count": entry.get("page_count", 0),
            "corpus": "stack",
        })
    return out


def load_public_bidsets() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for entry in PUBLIC_CORPUS_BIDSETS:
        json_path = PUBLIC_OUTPUTS_DIR / f"{entry['id']}.json"
        if not json_path.exists():
            continue
        out.append({
            "id": entry["id"],
            "local_path": entry["local_path"],
            "json_path": str(json_path),
            "page_count": entry.get("page_count", 0),
            "corpus": "public",
        })
    return out


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", action="append", help="Process only these bidset ids")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    bidsets = load_stack_bidsets() + load_public_bidsets()
    if args.only:
        wanted = set(args.only)
        bidsets = [b for b in bidsets if b["id"] in wanted]
    if args.limit:
        bidsets = bidsets[: args.limit]

    print(f"Intake diagnostic — processing {len(bidsets)} bidset(s)")
    print(f"Per-page CSVs go to: {PER_PAGE_CSV_DIR}")
    print()

    aggregates: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    t_start = time.time()
    for entry in bidsets:
        bid = entry["id"]
        pdf_path = Path(entry["local_path"])
        json_path = Path(entry["json_path"])
        if not pdf_path.is_file():
            print(f"  [miss] {bid}  PDF not on disk: {pdf_path}")
            failures.append({"id": bid, "error": "PDF missing"})
            continue
        if not json_path.is_file():
            print(f"  [miss] {bid}  JSON not on disk: {json_path}")
            failures.append({"id": bid, "error": "JSON missing"})
            continue
        print(f"  [run]  {bid}  ({entry['corpus']})")
        t0 = time.time()
        try:
            res = process_bidset(bid, pdf_path, json_path)
            elapsed = time.time() - t0
            csv_path = write_csv(bid, res["rows"])
            agg = res["aggregate"]
            agg["corpus"] = entry["corpus"]
            agg["elapsed_s"] = round(elapsed, 1)
            aggregates.append(agg)
            print(
                f"     pages={agg['n_pages']:>3}  "
                f"evidence_pages={agg['pages_with_roofing_evidence']:>3}  "
                f"scope_pages={len(agg['scope_pages_indices']):>2}  "
                f"detected={agg['scanner_detected_system']!s}  "
                f"mfr_pos/neg={agg['manufacturer_hits_positive_total']}/{agg['manufacturer_hits_negation_total']}  "
                f"acc_pgs={agg['accessory_pages']}  "
                f"{elapsed:.1f}s"
            )
        except Exception as e:
            tb = traceback.format_exc()
            print(f"  [FAIL] {bid}  {type(e).__name__}: {e}")
            print(tb)
            failures.append({"id": bid, "error_type": type(e).__name__, "error_msg": str(e), "traceback": tb})
        print()

    total_elapsed = time.time() - t_start
    print(f"Done. {len(aggregates)} ok, {len(failures)} failed, total {total_elapsed:.1f}s")

    summary = {
        "n_bidsets_processed": len(aggregates),
        "n_failures": len(failures),
        "elapsed_s": round(total_elapsed, 1),
        "vocabulary_source": "seeds/roofing_spec_database.py (verbatim, not extended)",
        "vocabulary_categories_present": {
            "system_signal": SYSTEM_TOKENS,
            "spec_section_keys_count": len(SPEC_SECTIONS),
            "manufacturer_canonicals": list(MANUFACTURERS.keys()),
            "thickness_markers": _THICKNESS_KEYS,
            "insulation_markers": _INSULATION_KEYS,
            "metal_markers": _METAL_MARKER_KEYS,
            "florida_signals": _FLORIDA_SIGNAL_KEYS,
            "accessory_section_keys": sorted(_ACCESSORY_SECTIONS),
        },
        "vocabulary_categories_NOT_present_in_seed": [
            "penetration (drain/scupper/RTU/vent/pipe-boot vocabulary lives in roof_assemblies.py, NOT in roofing_spec_database.py)",
            "edge (coping/edge metal/drip edge/gravel stop vocabulary lives in roof_assemblies.py, NOT in roofing_spec_database.py)",
        ],
        "negation_phrases": _NEGATION_PHRASES,
        "negation_radius_chars": NEGATION_RADIUS_CHARS,
        "aggregates": aggregates,
        "failures": failures,
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2, default=str))
    print(f"Summary JSON: {SUMMARY_JSON.relative_to(BACKEND_DIR)}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
