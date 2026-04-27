"""
Post-clustering polygon scorers.

These are NOT filter gates. They are scoring factors applied to
candidate polygons after clustering and scale determination to
improve polygon selection. They never reject a polygon outright —
the only candidate always wins, they just adjust its score.

Exports:
  score_interior()       — callout density + noise zone overlap
  score_rectilinearity() — how horizontal/vertical the paths are
  InteriorScore          — dataclass of per-polygon interior stats
"""

import re
from dataclasses import dataclass
from typing import Optional

# ---------------------------------------------------------------------------
# Interior density
# ---------------------------------------------------------------------------

EQUIPMENT_KEYWORDS = [
    "RTU", "DRAIN", "RD", "SCUPPER", "EF", "VTR", "PIPE",
    "HATCH", "CURB", "VENT", "FAN", "CONDENSING", "HVAC",
    "WALKWAY", "PAD", "UNIT", "MECH", "ELEC", "GAS",
    "LADDER", "SAFETY", "OVERFLOW", "CRICKET", "SLOPE",
    "CANT", "COPING", "PARAPET", "FLASHING", "MEMBRANE",
]

# matches 26'-8", 4'-0", 12' — feet with optional inches
DIMENSION_PATTERN = re.compile(r"\d+['\u2019\u2032][\-\s]*\d*[\"\u201D\u2033]?")

NOISE_ZONE_TYPES = ("notes_area", "legend_area", "title_block")


@dataclass
class InteriorScore:
    """Interior analysis of a candidate polygon."""
    polygon_area_sqin: float

    total_text_blocks: int
    callout_count: int
    short_label_count: int
    long_text_count: int
    dimension_count: int

    noise_zone_overlap_pct: float

    callout_density: float
    text_density: float
    long_text_ratio: float

    @property
    def density_score(self) -> float:
        """Combined score, higher = more likely a real building.

        Full formula (callout density + long-text + noise overlap).
        Ranges roughly -2.5 to +1.0. Used by diagnostics and tests.

        NOTE: the geometry route currently uses `safe_penalty` only
        (penalties_only and noise-overlap) to avoid pre-calibration
        regressions. Callout-density thresholds (0.04, 0.02) are
        paper-area thresholds and over-penalize correctly-sized
        polygons with sparse annotation. Step 56 (15 bid set sweep)
        will calibrate before the full formula is enabled.
        """
        score = 0.0

        # Primary: callout density
        # Calibrated from 15 bid set sweep (Step 56, 105 polygons):
        # p25=0.061, p10=0.031 — thresholds set at p25 and below-p10.
        if self.callout_density > 0.06:
            score += 1.0
        elif self.callout_density > 0.03:
            score += 0.5
        else:
            score -= 0.5

        # Long-text contamination
        # Calibrated from sweep: p50=0.15, p75=0.64. Threshold 0.5
        # sits between — penalizes the upper quartile only.
        if self.long_text_ratio > 0.5:
            score -= 0.5

        # Noise-zone overlap
        if self.noise_zone_overlap_pct > 0.05:
            score -= 1.0
        elif self.noise_zone_overlap_pct > 0.02:
            score -= 0.5

        return score

    @property
    def safe_penalty(self) -> float:
        """Conservative pre-calibration penalty.

        Returns a non-positive score factor based ONLY on the
        noise-zone overlap signal. This is the documented Panda
        fix — does not depend on paper-area density thresholds
        that would regress sparsely-annotated correct polygons.
        """
        if self.noise_zone_overlap_pct > 0.05:
            return -1.0
        if self.noise_zone_overlap_pct > 0.02:
            return -0.5
        return 0.0


def _tb_bbox(tb):
    """Normalise a text block to (x0,y0,x1,y1). Accepts TextBlock dataclass
    (x0/y0/x1/y1 attrs), or a dict with 'bbox', or an object with .bbox."""
    if hasattr(tb, "x0") and hasattr(tb, "y0"):
        return (tb.x0, tb.y0, tb.x1, tb.y1)
    b = getattr(tb, "bbox", None)
    if b is None and isinstance(tb, dict):
        b = tb.get("bbox")
    return tuple(b) if b else None


def _tb_text(tb):
    """Extract text content from a text block."""
    for attr in ("text", "content"):
        v = getattr(tb, attr, None)
        if v is not None:
            return v
    if isinstance(tb, dict):
        return tb.get("text") or tb.get("content") or ""
    return ""


def _zone_bbox(z):
    """Normalise a zone to (x0,y0,x1,y1)."""
    b = getattr(z, "bbox", None)
    if b is None and isinstance(z, dict):
        b = z.get("bbox")
    return tuple(b) if b else None


def _zone_type(z):
    v = getattr(z, "zone_type", None)
    if v is not None:
        return v
    if isinstance(z, dict):
        return z.get("zone_type", "")
    return ""


def score_interior(polygon_bbox: tuple,
                   text_blocks: list,
                   zones: Optional[list] = None,
                   polygon_area_sqin: Optional[float] = None) -> InteriorScore:
    """Score the interior of a candidate polygon.

    Args:
        polygon_bbox: (x0, y0, x1, y1) in PDF points
        text_blocks: list of TextBlock dataclasses or dicts
        zones: optional list of PageZone dataclasses or dicts
        polygon_area_sqin: if None, uses bbox area in sqin (pts/72)

    Returns: InteriorScore
    """
    x0, y0, x1, y1 = polygon_bbox
    bbox_w = abs(x1 - x0)
    bbox_h = abs(y1 - y0)
    bbox_area_pts = bbox_w * bbox_h

    if polygon_area_sqin is None:
        # pts² → in² (72 pts per inch)
        polygon_area_sqin = bbox_area_pts / (72.0 * 72.0)

    callout_count = 0
    short_label_count = 0
    long_text_count = 0
    dimension_count = 0
    total_inside = 0

    for tb in text_blocks or []:
        bb = _tb_bbox(tb)
        if not bb:
            continue
        cx = (bb[0] + bb[2]) / 2
        cy = (bb[1] + bb[3]) / 2
        if not (x0 <= cx <= x1 and y0 <= cy <= y1):
            continue

        total_inside += 1
        content = _tb_text(tb).strip()
        n = len(content)
        if n == 0:
            continue

        if DIMENSION_PATTERN.search(content):
            dimension_count += 1

        if n <= 30:
            upper = content.upper()
            if any(kw in upper for kw in EQUIPMENT_KEYWORDS):
                callout_count += 1
            else:
                short_label_count += 1
        elif n > 60:
            long_text_count += 1
        else:
            short_label_count += 1

    # Noise zone overlap (% of polygon bbox area)
    noise_overlap_pct = 0.0
    if zones and bbox_area_pts > 0:
        for z in zones:
            if _zone_type(z) not in NOISE_ZONE_TYPES:
                continue
            zb = _zone_bbox(z)
            if not zb:
                continue
            ix0 = max(x0, zb[0])
            iy0 = max(y0, zb[1])
            ix1 = min(x1, zb[2])
            iy1 = min(y1, zb[3])
            if ix0 < ix1 and iy0 < iy1:
                noise_overlap_pct += ((ix1 - ix0) * (iy1 - iy0)) / bbox_area_pts

    area = max(polygon_area_sqin, 0.01)
    callout_density = (callout_count * 2 + short_label_count + dimension_count) / area
    text_density = total_inside / area
    long_text_ratio = long_text_count / max(total_inside, 1)

    return InteriorScore(
        polygon_area_sqin=polygon_area_sqin,
        total_text_blocks=total_inside,
        callout_count=callout_count,
        short_label_count=short_label_count,
        long_text_count=long_text_count,
        dimension_count=dimension_count,
        noise_zone_overlap_pct=noise_overlap_pct,
        callout_density=callout_density,
        text_density=text_density,
        long_text_ratio=long_text_ratio,
    )


# ---------------------------------------------------------------------------
# Rectilinearity
# ---------------------------------------------------------------------------

def score_rectilinearity(paths_in_cluster: list) -> float:
    """Score how rectilinear a cluster's paths are.

    Returns 0.0-1.0 where 1.0 = all paths strongly horizontal/vertical.
    Buildings typically score 0.85+. Equipment symbols and curves score
    lower. Used as a tiebreaker, weighted at most 0.3 in total scoring.
    """
    if not paths_in_cluster:
        return 0.0

    rect = 0
    counted = 0
    for p in paths_in_cluster:
        xs = [pt[0] for pt in getattr(p, "points", []) or []]
        ys = [pt[1] for pt in getattr(p, "points", []) or []]
        if not xs or not ys:
            continue
        dx = max(xs) - min(xs)
        dy = max(ys) - min(ys)
        if dx < 0.001 and dy < 0.001:
            continue
        counted += 1
        aspect = max(dx, dy) / max(min(dx, dy), 0.001)
        if aspect > 5.0:
            rect += 1

    return rect / max(counted, 1)
