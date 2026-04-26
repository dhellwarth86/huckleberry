"""Layer 1 — Dispatch: plan-document structure.

Consumes seeds/dispatch_seed.py to classify pages, extract sheet numbers,
parse cross-references, find legends, and pull deterministic project
metadata. LLM-only fields (PROJECT_METADATA_LLM_ONLY) are left as None.

Inputs:  per-page extracted text + bbox-aware tokens (from pdfplumber)
Outputs: dict matching the dispatch layer's per-bidset shape
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any

from seeds import dispatch_seed as DS


@dataclass
class PageText:
    """Per-page text for Layer 1 input. Title block = bottom-right quadrant
    text (where sheet numbers and titles typically live)."""
    page_index: int                       # 0-indexed
    full_text: str                        # entire page concatenated
    title_block_text: str                 # bottom-right quadrant only
    text_blocks: list[dict[str, Any]] = field(default_factory=list)
    width: float = 0.0
    height: float = 0.0


@dataclass
class PageClassification:
    page_index: int
    sheet_number: str | None              # like "A-1.3" or None
    discipline: str | None                # "ARCHITECTURAL" / "MECHANICAL" / etc.
    page_type: str                        # one of dispatch_seed.PAGE_TYPES
    confidence: float                     # 0.0-0.9 from dispatch_seed.CONFIDENCE
    matched_keyword: str | None           # the keyword that triggered classification
    matched_in: str                       # "title_block" | "page_text" | "fallback" | "default"


def extract_sheet_number(title_block_text: str) -> str | None:
    """Find a sheet number in the title block. Tries the SHEET_NUMBER_REGEX
    against the bottom-right quadrant text. Returns the *last* match
    (sheet number is conventionally bottom-right-most token)."""
    if not title_block_text:
        return None
    matches = re.findall(DS.SHEET_NUMBER_REGEX, title_block_text)
    if not matches:
        return None
    # Filter out trivially-short or numeric-only matches that aren't real sheet numbers
    real = [m for m in matches if re.match(r"^[A-Z]{1,2}", m)]
    return real[-1] if real else None


def extract_discipline(sheet_number: str | None) -> str | None:
    """Map a sheet number's leading letter(s) to a discipline."""
    if not sheet_number:
        return None
    m = re.match(r"^([A-Z]{1,2})", sheet_number)
    if not m:
        return None
    prefix = m.group(1)
    return DS.DISCIPLINES.get(prefix) or DS.DISCIPLINES.get(prefix[0])


def classify_page(page: PageText) -> PageClassification:
    """Apply dispatch_seed PAGE_CLASSIFICATION_KEYWORDS in order. First match
    wins. Title-block matches get title_conf, body matches get page_conf.
    Fall back to discipline_fallback or 'unknown'."""
    sheet_number = extract_sheet_number(page.title_block_text)
    discipline = extract_discipline(sheet_number)

    title_upper = (page.title_block_text or "").upper()
    body_upper = (page.full_text or "").upper()

    for keywords, page_type, title_conf, page_conf in DS.PAGE_CLASSIFICATION_KEYWORDS:
        for kw in keywords:
            if kw in title_upper:
                return PageClassification(
                    page_index=page.page_index,
                    sheet_number=sheet_number,
                    discipline=discipline,
                    page_type=page_type,
                    confidence=title_conf,
                    matched_keyword=kw,
                    matched_in="title_block",
                )
        for kw in keywords:
            if kw in body_upper:
                return PageClassification(
                    page_index=page.page_index,
                    sheet_number=sheet_number,
                    discipline=discipline,
                    page_type=page_type,
                    confidence=page_conf,
                    matched_keyword=kw,
                    matched_in="page_text",
                )

    # Fallback: discipline letter alone
    if sheet_number:
        m = re.match(r"^([A-Z]{1,2})", sheet_number)
        if m:
            prefix = m.group(1)
            fallback = DS.DISCIPLINE_FALLBACK.get(prefix) or DS.DISCIPLINE_FALLBACK.get(prefix[0])
            if fallback:
                page_type, conf = fallback
                return PageClassification(
                    page_index=page.page_index,
                    sheet_number=sheet_number,
                    discipline=discipline,
                    page_type=page_type,
                    confidence=conf,
                    matched_keyword=None,
                    matched_in="fallback",
                )

    return PageClassification(
        page_index=page.page_index,
        sheet_number=sheet_number,
        discipline=discipline,
        page_type="unknown",
        confidence=0.0,
        matched_keyword=None,
        matched_in="default",
    )


def find_cross_references(text_blocks: Iterable[dict[str, Any]], full_text: str) -> list[dict[str, Any]]:
    """Apply CROSS_REFERENCE_PATTERNS. Returns list of {ref_type, raw, identifier?,
    target_sheet?, source_block_chars}. Block-length gates honored where defined."""
    refs: list[dict[str, Any]] = []

    # Detail-explicit and see-ref work on full text (they're self-anchored)
    explicit = DS.CROSS_REFERENCE_PATTERNS["detail_explicit"]
    for m in re.finditer(explicit["regex"], full_text, re.IGNORECASE):
        refs.append({
            "ref_type": explicit["ref_type"],
            "raw": m.group(0),
            "identifier": m.group(1),
            "target_sheet": m.group(2),
            "pattern": "detail_explicit",
        })

    see = DS.CROSS_REFERENCE_PATTERNS["see_ref"]
    for m in re.finditer(see["regex"], full_text, re.IGNORECASE):
        refs.append({
            "ref_type": see["ref_type"],
            "raw": m.group(0),
            "target_sheet": m.group(1),
            "pattern": "see_ref",
        })

    # Detail-implicit needs short text blocks (max 50 chars)
    implicit = DS.CROSS_REFERENCE_PATTERNS["detail_implicit"]
    max_chars = implicit.get("max_block_chars", 50)
    for blk in text_blocks:
        text = (blk.get("text") or "").strip()
        if not text or len(text) > max_chars:
            continue
        for m in re.finditer(implicit["regex"], text):
            refs.append({
                "ref_type": implicit["ref_type"],
                "raw": m.group(0),
                "identifier": m.group(1),
                "target_sheet": m.group(2),
                "source_block_chars": len(text),
                "pattern": "detail_implicit",
            })

    return refs


def find_legends(full_text: str) -> list[dict[str, Any]]:
    """Detect legends: numbered lists with a qualifying header word nearby.
    v0.1 implementation operates on flat text (no spatial lookback) — counts
    as a legend if the page contains a header keyword AND >=
    LEGEND_MIN_ENTRIES sequential numbered items in the same block."""
    legends: list[dict[str, Any]] = []
    upper = full_text.upper()

    for header_kw in DS.LEGEND_HEADER_KEYWORDS:
        if header_kw not in upper:
            continue
        # Find sequential numbered entries (1. 2. 3. or 1.01 1.02 ...)
        # Counts "1." "2." or decimal codes "1.01" "1.02".
        seq_count = 0
        for m in re.finditer(r"(?:^|\s)(\d{1,2})\.(?:\d{0,2})?(?=\s|$|[A-Z])", full_text, re.MULTILINE):
            seq_count += 1
        if seq_count >= DS.LEGEND_MIN_ENTRIES:
            # Map header to legend type
            ltype = DS.LEGEND_TYPE_DEFAULT
            for substr, legend_type in DS.LEGEND_TYPE_FROM_HEADER:
                if substr in upper:
                    ltype = legend_type
                    break
            legends.append({
                "header_keyword": header_kw,
                "legend_type": ltype,
                "entry_count_estimate": seq_count,
            })
            break  # one legend record per page
    return legends


# ─────────────────────────────────────────────────────────────────────────────
# Project metadata extraction (deterministic only)
# ─────────────────────────────────────────────────────────────────────────────

PROJECT_METADATA_PATTERNS = {
    "project_name": [
        re.compile(r"PROJECT\s*(?:NAME)?[:\s]+([A-Z0-9][A-Z0-9 &',\-./#]{3,80})", re.IGNORECASE),
    ],
    "project_address": [
        re.compile(r"\b(\d{2,6}\s+[A-Z][A-Z .'\-]{2,60}(?:STREET|ST|AVENUE|AVE|ROAD|RD|BOULEVARD|BLVD|DRIVE|DR|HIGHWAY|HWY|LANE|LN|PARKWAY|PKWY|WAY|COURT|CT|CIR|CIRCLE|TRAIL|TRL|PLACE|PL))\b", re.IGNORECASE),
    ],
    "project_number": [
        re.compile(r"\b(?:PROJECT|JOB|FILE)\s*(?:NO\.?|NUMBER|#)?[:\s]*([A-Z0-9][A-Z0-9\-./]{2,15})", re.IGNORECASE),
    ],
    "owner": [
        re.compile(r"\bOWNER[:\s]+([A-Z][A-Z0-9 &',\-./]{3,80})", re.IGNORECASE),
    ],
    "architect": [
        re.compile(r"\bARCHITECT[:\s]+([A-Z][A-Z0-9 &',\-./]{3,80})", re.IGNORECASE),
    ],
    "total_building_sf": [
        re.compile(r"\b(?:TOTAL|BUILDING|GROSS)\s*(?:AREA|SF|S\.?F\.?)[:\s]*([\d,]+)\s*(?:SF|S\.?F\.?)?", re.IGNORECASE),
    ],
}


def extract_project_metadata(cover_text: str) -> dict[str, Any]:
    """Pull deterministic metadata from cover/index page text. LLM-only fields
    are left as None per dispatch_seed.PROJECT_METADATA_LLM_ONLY."""
    out: dict[str, Any] = {f: None for f in DS.PROJECT_METADATA_DETERMINISTIC}
    for f in DS.PROJECT_METADATA_LLM_ONLY:
        out[f] = None  # explicitly nulled; LLM-only

    if not cover_text:
        return out

    for field_name, patterns in PROJECT_METADATA_PATTERNS.items():
        for pat in patterns:
            m = pat.search(cover_text)
            if m:
                value = m.group(1).strip().rstrip(".,")
                if field_name == "total_building_sf":
                    try:
                        value = int(value.replace(",", ""))
                    except ValueError:
                        continue
                out[field_name] = value
                break
    return out


def build_dispatch_layer(pages: list[PageText]) -> dict[str, Any]:
    """Run Layer 1 over all pages. Returns the per-bidset dispatch dict."""
    classifications = [classify_page(p) for p in pages]

    # Sheet map: page_index -> sheet_number (where extracted)
    sheet_map = {c.page_index: c.sheet_number for c in classifications if c.sheet_number}

    # Cross-references per page
    cross_refs_per_page: dict[int, list[dict[str, Any]]] = {}
    for p in pages:
        refs = find_cross_references(p.text_blocks, p.full_text)
        if refs:
            cross_refs_per_page[p.page_index] = refs

    # Legends per page
    legends_per_page: dict[int, list[dict[str, Any]]] = {}
    for p in pages:
        legs = find_legends(p.full_text)
        if legs:
            legends_per_page[p.page_index] = legs

    # Project metadata: try cover page(s) and index page(s) first, then any title block
    cover_pages = [p for p, c in zip(pages, classifications) if c.page_type in ("cover", "drawing_index", "general_notes")]
    cover_text = "\n".join(p.full_text for p in cover_pages[:3]) if cover_pages else ""
    if not cover_text and pages:
        # Fall back to first 3 pages
        cover_text = "\n".join(p.full_text for p in pages[:3])
    project_metadata = extract_project_metadata(cover_text)

    # Roof-page identification: pages typed as roof_plan
    roof_page_indices = [c.page_index for c in classifications if c.page_type == "roof_plan"]

    # Confidence histogram for the dispatch report
    conf_hist: dict[str, int] = {k: 0 for k in DS.CONFIDENCE.keys()}
    for c in classifications:
        bucket = "unknown"
        if c.confidence >= 0.85:
            bucket = "explicit"
        elif c.confidence >= 0.6:
            bucket = "strong"
        elif c.confidence >= 0.4:
            bucket = "inferred"
        elif c.confidence > 0.0:
            bucket = "weak"
        conf_hist[bucket] = conf_hist.get(bucket, 0) + 1

    # Page-type histogram
    type_hist: dict[str, int] = {}
    for c in classifications:
        type_hist[c.page_type] = type_hist.get(c.page_type, 0) + 1

    return {
        "page_classifications": [
            {
                "page_index": c.page_index,
                "sheet_number": c.sheet_number,
                "discipline": c.discipline,
                "page_type": c.page_type,
                "confidence": c.confidence,
                "matched_keyword": c.matched_keyword,
                "matched_in": c.matched_in,
            }
            for c in classifications
        ],
        "sheet_map": sheet_map,
        "cross_references_by_page": cross_refs_per_page,
        "legends_by_page": legends_per_page,
        "project_metadata": project_metadata,
        "roof_page_indices": roof_page_indices,
        "page_type_histogram": type_hist,
        "confidence_histogram": conf_hist,
    }
