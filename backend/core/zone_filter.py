"""
Zone filtering — detect and mask detail views, title blocks, and notes areas.

Used to remove non-building paths before clustering. Applied to
heavy-line pass only; all-paths fallback is untouched.
"""

import re
from typing import Optional

PTS = 72  # PDF points per inch

# Patterns that identify detail view zone titles
_DETAIL_PATTERNS = [
    re.compile(r'\bDETAIL\b', re.IGNORECASE),
    re.compile(r'\bSECTION\b', re.IGNORECASE),
]

# Scale pattern (reuse from pdf_engine)
_SCALE_WITH_LABEL = re.compile(
    r'Scale\s*[:=]?\s*', re.IGNORECASE
)


def detect_detail_zones(text_blocks, page_meta):
    """
    Detect detail view zones from text blocks.

    Looks for text blocks containing scale labels paired with detail
    keywords (DETAIL, SECTION, etc.). Each detected zone gets a
    bounding rectangle estimated from the text position.

    Returns list of dicts: {name, x0, y0, x1, y1, fpi}
    Coordinates are in PDF points.
    """
    pw = page_meta.width_pts
    ph = page_meta.height_pts
    zones = []

    for block in text_blocks:
        text = block.text.strip()
        if not text:
            continue

        # Look for "Scale= ..." blocks that contain a detail keyword
        has_scale_label = bool(_SCALE_WITH_LABEL.search(text))
        has_detail = any(p.search(text) for p in _DETAIL_PATTERNS)

        if not (has_scale_label and has_detail):
            continue

        # This text block is a detail view label with its own scale.
        # Estimate the zone rectangle around it.
        # Detail views are typically 3-8 inches on each side of the label.
        cx = (block.x0 + block.x1) / 2
        cy = (block.y0 + block.y1) / 2

        # Zone size: 5 inches radius (conservative)
        radius = 5 * PTS
        x0 = max(0, cx - radius)
        y0 = max(0, cy - radius)
        x1 = min(pw, cx + radius)
        y1 = min(ph, cy + radius)

        zones.append({
            "name": text[:40].replace("\n", " "),
            "x0": x0, "y0": y0,
            "x1": x1, "y1": y1,
        })

    return zones


def detect_title_block(text_blocks, page_meta):
    """
    Detect the title block zone (bottom-right quadrant).

    Returns dict {x0, y0, x1, y1} or None.
    """
    pw = page_meta.width_pts
    ph = page_meta.height_pts

    # Bottom-right quadrant
    qx = pw * 0.6
    qy = ph * 0.6

    br_blocks = [b for b in text_blocks if b.x0 >= qx and b.y0 >= qy]
    if len(br_blocks) < 3:
        return None

    min_x = min(b.x0 for b in br_blocks)
    min_y = min(b.y0 for b in br_blocks)
    max_x = pw  # extend to page edge
    max_y = ph

    return {"x0": min_x, "y0": min_y, "x1": max_x, "y1": max_y}


def filter_paths_by_zone(paths, exclusion_zones):
    """
    Remove paths whose center falls inside any exclusion zone.

    Args:
        paths: list of VectorPath
        exclusion_zones: list of dicts with x0, y0, x1, y1

    Returns:
        filtered list of VectorPath (paths NOT in any exclusion zone)
    """
    if not exclusion_zones:
        return paths

    filtered = []
    for p in paths:
        if not p.points:
            filtered.append(p)
            continue

        # Center of path bounding box
        xs = [pt[0] for pt in p.points]
        ys = [pt[1] for pt in p.points]
        cx = (min(xs) + max(xs)) / 2
        cy = (min(ys) + max(ys)) / 2

        in_zone = False
        for zone in exclusion_zones:
            if zone["x0"] <= cx <= zone["x1"] and zone["y0"] <= cy <= zone["y1"]:
                in_zone = True
                break

        if not in_zone:
            filtered.append(p)

    return filtered
