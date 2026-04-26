"""Layer 2 — Scope: identified roofing systems with manufacturer / attachment.

Consumes seeds/roofing_materials.py. Operates on text from pages classified
by Layer 1 as roof-relevant (roof_plan, schedule_sheet, detail_sheet,
general_notes, symbol_legend, cover) — those are where spec-section
numbers, manufacturer names, and assembly callouts typically live.
"""

from __future__ import annotations

import re
from collections import Counter
from typing import Any

from seeds import dispatch_seed as DS
from seeds import roofing_materials as RM


# Confidence levels mirror dispatch_seed.CONFIDENCE
EXPLICIT = DS.CONFIDENCE["explicit"]    # 0.9 — spec section + manufacturer
STRONG = DS.CONFIDENCE["strong"]        # 0.7 — manufacturer + product
INFERRED = DS.CONFIDENCE["inferred"]    # 0.5 — system type only
WEAK = DS.CONFIDENCE["weak"]            # 0.3 — keyword present but ambiguous
UNKNOWN = DS.CONFIDENCE["unknown"]      # 0.0


# Pages worth inspecting for scope. Glazing is OUT OF SCOPE per march orders.
ROOF_RELEVANT_PAGE_TYPES = {
    "roof_plan", "schedule_sheet", "detail_sheet",
    "general_notes", "symbol_legend", "cover",
    "drawing_index",
}


# ─────────────────────────────────────────────────────────────────────────────
# Detection primitives
# ─────────────────────────────────────────────────────────────────────────────

# Attachment terms — drawn from roof_assemblies.ROOF_SYSTEMS.attachment values
# plus common spec phrasings.
ATTACHMENT_PATTERNS = {
    "mechanically_attached": [
        re.compile(r"\bMECHANICALLY\s+(?:ATTACHED|FASTENED)\b", re.IGNORECASE),
        re.compile(r"\bMECH\.?\s+ATT(?:ACHED|\.)\b", re.IGNORECASE),
    ],
    "fully_adhered": [
        re.compile(r"\bFULLY\s+ADHERED\b", re.IGNORECASE),
        re.compile(r"\bF\.?A\.?\b\s*(?:TPO|PVC|EPDM)", re.IGNORECASE),
    ],
    "ballasted": [
        re.compile(r"\bBALLASTED\b", re.IGNORECASE),
        re.compile(r"\bSTONE\s+BALLAST\b", re.IGNORECASE),
    ],
    "torch_applied": [
        re.compile(r"\bTORCH(?:ED|\s+APPLIED|\s+DOWN)\b", re.IGNORECASE),
    ],
    "cold_applied_adhesive": [
        re.compile(r"\bCOLD[\s\-]+APPLIED\b", re.IGNORECASE),
    ],
    "hot_mopped_asphalt": [
        re.compile(r"\bHOT[\s\-]+MOPPED?\b", re.IGNORECASE),
    ],
    "concealed_clip": [
        re.compile(r"\bSTANDING[\s\-]+SEAM\b", re.IGNORECASE),
        re.compile(r"\bCONCEALED\s+CLIP\b", re.IGNORECASE),
    ],
    "exposed_fastener": [
        re.compile(r"\bR[\s\-]+PANEL\b", re.IGNORECASE),
        re.compile(r"\bEXPOSED\s+FASTENER\b", re.IGNORECASE),
    ],
}


# Fallback system-type keywords (for when no spec section is present)
SYSTEM_TYPE_KEYWORDS = {
    "tpo":               [re.compile(r"\bTPO\b", re.IGNORECASE)],
    "pvc":               [re.compile(r"\bPVC\b\s*(?:ROOF|MEMBRANE)", re.IGNORECASE)],
    "epdm":              [re.compile(r"\bEPDM\b", re.IGNORECASE)],
    "modified_bitumen":  [
        re.compile(r"\bMODIFIED\s+BITUMEN\b", re.IGNORECASE),
        re.compile(r"\bMOD[\s\-]+BIT\b", re.IGNORECASE),
        re.compile(r"\bSBS\b", re.IGNORECASE),
        re.compile(r"\bAPP\b\s*(?:CAP|MEMBRANE)", re.IGNORECASE),
    ],
    "built_up":          [
        re.compile(r"\bBUILT[\s\-]+UP\b", re.IGNORECASE),
        re.compile(r"\bBUR\b", re.IGNORECASE),
    ],
    "metal_panel":       [
        re.compile(r"\bSTANDING[\s\-]+SEAM\b", re.IGNORECASE),
        re.compile(r"\bMETAL\s+(?:ROOF|PANEL)\b", re.IGNORECASE),
        re.compile(r"\bR[\s\-]+PANEL\b", re.IGNORECASE),
    ],
    "shingle":           [
        re.compile(r"\bASPHALT\s+SHINGLE", re.IGNORECASE),
        re.compile(r"\bARCHITECTURAL\s+SHINGLE", re.IGNORECASE),
    ],
    "tile":              [re.compile(r"\b(?:CLAY|CONCRETE)\s+TILE\b", re.IGNORECASE)],
    "spf":               [
        re.compile(r"\bSPRAY\s+(?:POLYURETHANE|FOAM)\b", re.IGNORECASE),
        re.compile(r"\bSPF\b", re.IGNORECASE),
    ],
}


# Spec section regex — matches "07 54", "07 54 23", with hyphens or dots.
SPEC_SECTION_RE = re.compile(
    r"\b(0?7)\s*[-\s.]?\s*(\d{2})(?:\s*[-\s.]?\s*(\d{2,4}))?\b"
)


def find_spec_sections(text: str) -> list[dict[str, Any]]:
    """Match SPEC_SECTIONS keys in the text. Returns list of {key, system, name, raw}."""
    if not text:
        return []
    seen: set[str] = set()
    hits: list[dict[str, Any]] = []
    for m in SPEC_SECTION_RE.finditer(text):
        # Build candidate keys at progressively coarser granularity
        major = f"{int(m.group(1)):02d} {m.group(2)}"
        sub = m.group(3)
        candidates = []
        if sub:
            sub2 = sub[:2]
            sub4 = sub[:4]
            candidates.append(f"{major} {sub4}" if len(sub) >= 4 else f"{major} {sub}")
            candidates.append(f"{major}{sub2}")  # 07 5400
            candidates.append(f"{major} {sub2}")
        candidates.append(major)

        for cand in candidates:
            if cand in RM.SPEC_SECTIONS:
                if cand in seen:
                    continue
                seen.add(cand)
                entry = RM.SPEC_SECTIONS[cand]
                hits.append({
                    "key": cand,
                    "system": entry.get("system"),
                    "name": entry.get("name"),
                    "raw_match": m.group(0),
                })
                break
    return hits


def find_manufacturers(text: str) -> list[dict[str, Any]]:
    """Match manufacturer names + aliases + product names. Returns list of
    {manufacturer, matched_name, match_kind} where match_kind in
    {'name','alias','product'}."""
    if not text:
        return []
    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    for canonical, info in RM.MANUFACTURERS.items():
        names_to_try: list[tuple[str, str]] = [(canonical, "name")]
        for alias in info.get("aliases", []):
            names_to_try.append((alias, "alias"))
        for product in info.get("products", {}).keys():
            names_to_try.append((product, "product"))
        for name, kind in names_to_try:
            # Word-boundary match, case-insensitive
            pat = re.compile(r"\b" + re.escape(name) + r"\b", re.IGNORECASE)
            if pat.search(text):
                key = (canonical, name, kind)
                if key in seen:
                    continue
                seen.add(key)
                out.append({
                    "manufacturer": canonical,
                    "matched_name": name,
                    "match_kind": kind,
                    "supported_systems": info.get("systems", []),
                })
    return out


def find_attachments(text: str) -> list[str]:
    """Return distinct attachment methods detected in text."""
    if not text:
        return []
    found: list[str] = []
    for attach, pats in ATTACHMENT_PATTERNS.items():
        for pat in pats:
            if pat.search(text):
                if attach not in found:
                    found.append(attach)
                break
    return found


def find_thicknesses(text: str) -> list[str]:
    if not text:
        return []
    found: list[str] = []
    for marker in RM.MATERIAL_PROPERTIES["thickness_markers"].keys():
        if re.search(r"\b" + re.escape(marker), text, re.IGNORECASE):
            found.append(marker)
    return found


def find_insulation_markers(text: str) -> list[str]:
    if not text:
        return []
    found: list[str] = []
    for marker in RM.MATERIAL_PROPERTIES["insulation_markers"].keys():
        if re.search(r"\b" + re.escape(marker) + r"\b", text, re.IGNORECASE):
            found.append(marker)
    return found


def find_florida_signals(text: str) -> list[str]:
    if not text:
        return []
    found: list[str] = []
    for marker in RM.MATERIAL_PROPERTIES["florida_signals"].keys():
        if re.search(r"\b" + re.escape(marker) + r"\b", text, re.IGNORECASE):
            found.append(marker)
    return found


def find_system_type_keywords(text: str) -> list[str]:
    if not text:
        return []
    found: list[str] = []
    for sys_type, pats in SYSTEM_TYPE_KEYWORDS.items():
        for pat in pats:
            if pat.search(text):
                if sys_type not in found:
                    found.append(sys_type)
                break
    return found


# ─────────────────────────────────────────────────────────────────────────────
# Scope assembly
# ─────────────────────────────────────────────────────────────────────────────

def build_scope_layer(
    pages: list[Any],                       # PageText-like
    classifications: list[dict[str, Any]],
) -> dict[str, Any]:
    """Walk roof-relevant pages, accumulate evidence, and identify systems.

    Strategy: aggregate all evidence across all roof-relevant pages first,
    then synthesize systems. v0.1 produces ONE consolidated system per
    detected system_type — multi-system buildings will surface in the
    findings as a deferred concern; cleanly separating multi-system in
    flat-text is a v0.2 problem.
    """
    classmap = {c["page_index"]: c for c in classifications}

    # Accumulate evidence across pages
    spec_section_hits: list[dict[str, Any]] = []
    manufacturer_hits: list[dict[str, Any]] = []
    attachment_hits: list[tuple[str, int]] = []        # (method, page_index)
    thickness_hits: list[tuple[str, int]] = []
    insulation_hits: list[tuple[str, int]] = []
    florida_hits: list[tuple[str, int]] = []
    system_kw_hits: list[tuple[str, int]] = []

    pages_inspected: list[int] = []
    pages_skipped_glazing = 0

    for p in pages:
        cls = classmap.get(p.page_index)
        if not cls:
            continue
        # Skip glazing: not in v0.1 scope.  Glazing pages are NOT a dispatch
        # page_type — they're roof/schedule/detail pages whose content is
        # glazing-relevant.  Use cheap text gating to detect.
        text = p.full_text or ""
        upper = text.upper()
        if cls["page_type"] not in ROOF_RELEVANT_PAGE_TYPES:
            continue
        # Detect predominantly-glazing pages (window/storefront/curtain wall heavy)
        glazing_signal = sum(1 for kw in (
            "STOREFRONT", "CURTAIN WALL", "WINDOW SCHEDULE",
            "GLAZING", "ALUMINUM ENTRANCE",
        ) if kw in upper)
        if glazing_signal >= 2 and "ROOF" not in upper and "MEMBRANE" not in upper:
            pages_skipped_glazing += 1
            continue

        pages_inspected.append(p.page_index)

        for hit in find_spec_sections(text):
            hit = {**hit, "page_index": p.page_index}
            spec_section_hits.append(hit)
        for hit in find_manufacturers(text):
            hit = {**hit, "page_index": p.page_index}
            manufacturer_hits.append(hit)
        for a in find_attachments(text):
            attachment_hits.append((a, p.page_index))
        for t in find_thicknesses(text):
            thickness_hits.append((t, p.page_index))
        for i in find_insulation_markers(text):
            insulation_hits.append((i, p.page_index))
        for f in find_florida_signals(text):
            florida_hits.append((f, p.page_index))
        for k in find_system_type_keywords(text):
            system_kw_hits.append((k, p.page_index))

    # Collapse: best system_type guess per evidence track
    system_types_from_specs = Counter(h["system"] for h in spec_section_hits if h.get("system"))
    system_types_from_kw = Counter(k for k, _ in system_kw_hits)

    # Identify systems — per distinct system_type observed
    detected_system_types: list[str] = []
    for sys_t, _ in system_types_from_specs.most_common():
        if sys_t and sys_t not in detected_system_types:
            detected_system_types.append(sys_t)
    for sys_t, _ in system_types_from_kw.most_common():
        if sys_t and sys_t not in detected_system_types:
            detected_system_types.append(sys_t)

    # If we have NO direct evidence of a system_type but DO have insulation
    # markers that signal flat_roof, fall back to "tpo" as the most-common
    # FL commercial flat roof system — but with WEAK confidence.
    fallback_used = False
    if not detected_system_types and any(
        RM.MATERIAL_PROPERTIES["insulation_markers"].get(t, {}).get("signal") == "flat_roof"
        for t, _ in insulation_hits
    ):
        detected_system_types.append("tpo")
        fallback_used = True

    systems_out: list[dict[str, Any]] = []
    for sys_t in detected_system_types:
        # Pick best matching attachment for this system_type
        attachments_seen = [a for a, _ in attachment_hits]
        best_attach = None
        if attachments_seen:
            best_attach = Counter(attachments_seen).most_common(1)[0][0]

        # Per-system manufacturer: any manufacturer whose `systems` list
        # includes this system_type
        sys_manufacturers = [
            h for h in manufacturer_hits
            if sys_t in (h.get("supported_systems") or [])
        ]
        # Sort manufacturers by hit count
        mfr_counter: Counter[str] = Counter(h["manufacturer"] for h in sys_manufacturers)

        # Source pages: union of pages where this system's evidence appeared
        src_pages: set[int] = set()
        for h in spec_section_hits:
            if h.get("system") == sys_t:
                src_pages.add(h["page_index"])
        for k, pidx in system_kw_hits:
            if k == sys_t:
                src_pages.add(pidx)

        # Confidence
        if any(h.get("system") == sys_t for h in spec_section_hits):
            confidence = EXPLICIT if sys_manufacturers else STRONG
        elif sys_manufacturers:
            confidence = STRONG
        elif fallback_used and sys_t == "tpo":
            confidence = WEAK
        else:
            confidence = INFERRED

        systems_out.append({
            "system_type": sys_t,
            "attachment": best_attach,
            "manufacturer": (mfr_counter.most_common(1)[0][0] if mfr_counter else None),
            "manufacturer_candidates": [
                {"name": m, "hits": c} for m, c in mfr_counter.most_common(5)
            ],
            "thickness_markers": sorted({t for t, _ in thickness_hits}),
            "spec_sections": sorted({h["key"] for h in spec_section_hits if h.get("system") == sys_t}),
            "source_pages": sorted(src_pages),
            "confidence": confidence,
        })

    return {
        "systems": systems_out,
        "fallback_used": fallback_used,
        "evidence": {
            "spec_section_hits": spec_section_hits,
            "manufacturer_hits": manufacturer_hits,
            "attachment_hits": [{"method": a, "page_index": p} for a, p in attachment_hits],
            "thickness_markers": [{"marker": t, "page_index": p} for t, p in thickness_hits],
            "insulation_markers": [{"marker": m, "page_index": p} for m, p in insulation_hits],
            "florida_signals": [{"marker": m, "page_index": p} for m, p in florida_hits],
            "system_type_keyword_hits": [{"system_type": k, "page_index": p} for k, p in system_kw_hits],
        },
        "pages_inspected": pages_inspected,
        "pages_skipped_glazing": pages_skipped_glazing,
    }
