"""
Architect profile — firm detection from title block text + profile lookup.

When a plan is dispatched, we extract title-block text and try to match
it against known architect profiles in storage. Repeated successes
against a firm grow that profile's success_count; once >=3 the profile
is trusted enough to influence pipeline parameters (weight thresholds,
gate params, etc.).

Trade-agnostic. Lives in Layer 3 (dispatch), called after Filter 5.
"""

from typing import Optional

try:
    from rapidfuzz import fuzz
    HAS_RAPIDFUZZ = True
except ImportError:
    HAS_RAPIDFUZZ = False

# Strong signals — a line containing any of these is likely a firm name.
# Matched as whole words only (see _STRONG_RE). Deliberately narrow — the
# 15 bid set sweep showed equipment callouts (K-CHEM DISPENSER, PARAPET DRAIN,
# TOUCH-FREE SOAP DISPENSER) matching on loose tokens like "design"/"group"/"inc".
_STRONG_FIRM_TOKENS = [
    "architect", "architects", "architecture",
    "engineer", "engineers", "engineering",
    "associates", "consultants", "consulting",
    "aia", "ncarb",
]

# Suffix tokens — only count when combined with another signal
_SUFFIX_TOKENS = ["llc", "ltd", "pllc", "plc", "p.a.", "pa", "p.c.", "pc",
                  "inc", "corp", "company"]

# Retained for backward compatibility (tests + callers reading the list)
FIRM_KEYWORDS = _STRONG_FIRM_TOKENS + _SUFFIX_TOKENS

import re as _re
_STRONG_RE = _re.compile(
    r"\b(" + "|".join(_re.escape(t) for t in _STRONG_FIRM_TOKENS) + r")\b",
    _re.IGNORECASE,
)
_SUFFIX_RE = _re.compile(
    r"\b(" + "|".join(_re.escape(t) for t in _SUFFIX_TOKENS) + r")\b",
    _re.IGNORECASE,
)

# Noise patterns — lines that look like equipment / legend entries, never firms
_NOISE_RE = _re.compile(
    r"\b(DISPENSER|DRAIN|FASTENER|GRAVEL|PROPERTY\s+LINE|GRANULAR|"
    r"BASE|OWNER|DEVELOPER|STOP|PAPER|TOWEL|HOLDER|SOAP|PARAPET|"
    r"PERIMETER|DIMENSION|EDGE|CURB|VENT|RTU|SCUPPER|MEMBRANE|FLASHING|"
    r"COPING|INSULATION|SUBSTRATE)\b",
    _re.IGNORECASE,
)

# Match threshold for fuzzy comparison against existing profiles
MATCH_THRESHOLD = 80.0


def _extract_text(item) -> str:
    """Pull a plain string from a TextBlock-like object or raw dict/string."""
    if item is None:
        return ""
    if isinstance(item, str):
        return item
    for attr in ("content", "text"):
        v = getattr(item, attr, None)
        if v:
            return str(v)
    if isinstance(item, dict):
        return str(item.get("content") or item.get("text") or "")
    return str(item)


def extract_firm_candidates(title_block_text) -> list[str]:
    """Pull candidate firm-name lines out of title-block text.

    A line qualifies only if it contains a strong firm token
    (architect / engineer / associates / consultants / AIA / NCARB)
    AND does not match a known equipment/legend noise pattern.
    Lines that are just a bare suffix ('LLC', 'Inc.') are dropped.

    Returns a list of cleaned candidate strings in original order.
    """
    candidates: list[str] = []
    seen = set()
    for raw in title_block_text or []:
        text = _extract_text(raw)
        if not text:
            continue
        for line in text.splitlines():
            line_clean = line.strip()
            if not line_clean or len(line_clean) < 4:
                continue
            if _NOISE_RE.search(line_clean):
                continue
            if not _STRONG_RE.search(line_clean):
                continue
            # Drop lines that are mostly punctuation/numbers
            alpha = sum(1 for c in line_clean if c.isalpha())
            if alpha < 6:
                continue
            # Drop lines that are clearly a sentence (contain multiple commas,
            # periods, or are long instructional text)
            if len(line_clean) > 80:
                continue
            key = line_clean.lower()
            if key in seen:
                continue
            seen.add(key)
            candidates.append(line_clean)
    return candidates


def detect_firm(title_block_text, storage) -> Optional[dict]:
    """Detect the architecture firm from title-block text.

    1. Extract candidate firm-name lines using FIRM_KEYWORDS.
    2. Fuzzy-match each candidate against existing profiles in storage.
    3. If best match >= MATCH_THRESHOLD: load and return that profile.
    4. If no match but we found candidates: create a stub profile
       (success_count=0) for the strongest candidate and return it.
    5. If no candidates at all: return None.
    """
    if storage is None:
        return None

    candidates = extract_firm_candidates(title_block_text)
    if not candidates:
        return None

    existing = storage.list_architect_profiles()

    best_match = None
    best_score = 0.0
    best_candidate = candidates[0]

    if existing and HAS_RAPIDFUZZ:
        for cand in candidates:
            for firm in existing:
                score = fuzz.token_set_ratio(cand.lower(), firm.lower())
                if score > best_score:
                    best_score = score
                    best_match = firm
                    best_candidate = cand
    elif existing:
        # Fallback: substring match
        for cand in candidates:
            cl = cand.lower()
            for firm in existing:
                fl = firm.lower()
                if fl in cl or cl in fl:
                    best_score = 100.0
                    best_match = firm
                    best_candidate = cand
                    break
            if best_match:
                break

    if best_match and best_score >= MATCH_THRESHOLD:
        return storage.get_architect_profile(best_match)

    # No match — create stub with success_count=0 for the strongest candidate
    storage.upsert_architect_profile(best_candidate, success_count=0)
    return storage.get_architect_profile(best_candidate)


def profile_is_trusted(profile: Optional[dict], min_success: int = 3) -> bool:
    """Profiles only influence pipeline parameters once proven."""
    if not profile:
        return False
    return (profile.get("success_count") or 0) >= min_success
