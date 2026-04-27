"""
Filter Pipeline — composable gate chain for vector path filtering.

Each gate is a pure function: paths_in -> (paths_out, GateLog).
Gates run in sequence; each gate's output feeds the next gate's input.

Heavy-line pipeline: zone_mask -> weight -> length -> dash
All-paths pipeline: passthrough (no filtering — sacred fallback)

Future gates (color, rectilinear, hatching, containment) follow the
same pattern: add a gate_*() function and append to run_heavy_pipeline().
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GateLog:
    """What a single gate did to the path set."""
    gate_name: str
    paths_in: int
    paths_out: int
    paths_removed: int
    details: str = ""


@dataclass
class FilterResult:
    """Output of the full filter pipeline."""
    paths: list
    gate_logs: list[GateLog] = field(default_factory=list)

    @property
    def total_removed(self) -> int:
        return sum(g.paths_removed for g in self.gate_logs)

    def summary(self) -> str:
        lines = []
        for g in self.gate_logs:
            lines.append(
                f"  {g.gate_name}: {g.paths_in} -> {g.paths_out} "
                f"(-{g.paths_removed}) {g.details}"
            )
        return "\n".join(lines)


# ============================================================
# Gate 1: Zone Mask
# ============================================================

def gate_zone_mask(paths: list, exclusion_zones: list) -> tuple[list, GateLog]:
    """Remove paths whose center falls inside any exclusion zone.

    exclusion_zones: list of dicts with x0, y0, x1, y1 keys
    (from zone_filter.py detect_detail_zones / detect_title_block).
    """
    count_before = len(paths)

    if not exclusion_zones:
        return paths, GateLog("zone_mask", count_before, count_before, 0,
                              "no exclusion zones")

    filtered = []
    for p in paths:
        if not p.points:
            filtered.append(p)
            continue

        xs = [pt[0] for pt in p.points]
        ys = [pt[1] for pt in p.points]
        cx = (min(xs) + max(xs)) / 2
        cy = (min(ys) + max(ys)) / 2

        excluded = False
        for zone in exclusion_zones:
            if zone["x0"] <= cx <= zone["x1"] and zone["y0"] <= cy <= zone["y1"]:
                excluded = True
                break
        if not excluded:
            filtered.append(p)

    removed = count_before - len(filtered)
    return filtered, GateLog("zone_mask", count_before, len(filtered), removed,
                             f"{len(exclusion_zones)} exclusion zones")


# ============================================================
# Gate 2: Weight Filter
# ============================================================

def gate_weight_filter(paths: list, min_weight: float = 1.0) -> tuple[list, GateLog]:
    """Keep only paths above minimum stroke weight."""
    count_before = len(paths)
    filtered = [p for p in paths if (p.width or 0) > min_weight]
    removed = count_before - len(filtered)
    return filtered, GateLog("weight_filter", count_before, len(filtered), removed,
                             f"threshold: {min_weight}pt")


# ============================================================
# Gate 3: Length Filter
# ============================================================

def gate_length_filter(paths: list, min_pts: float = 36.0) -> tuple[list, GateLog]:
    """Remove paths shorter than minimum length (bbox diagonal)."""
    count_before = len(paths)
    filtered = [p for p in paths if p.bbox_diag_pts > min_pts]
    removed = count_before - len(filtered)
    return filtered, GateLog("length_filter", count_before, len(filtered), removed,
                             f"threshold: {min_pts}pts ({min_pts/72:.1f}in)")


# ============================================================
# Gate 4: Dash Filter
# ============================================================

def gate_dash_filter(paths: list) -> tuple[list, GateLog]:
    """Remove dashed/dotted paths. Solid = starts with '[]' or empty."""
    count_before = len(paths)
    filtered = []
    for p in paths:
        dashes = p.dashes if p.dashes else ""
        if not dashes or dashes.startswith("[]"):
            filtered.append(p)
    removed = count_before - len(filtered)
    return filtered, GateLog("dash_filter", count_before, len(filtered), removed)


# ============================================================
# Gate 5: Color Filter (adaptive)
# ============================================================

def gate_color_filter(paths: list,
                      dominance_threshold: float = 0.90) -> tuple[list, GateLog]:
    """Gate 5: Remove non-dominant-color paths.

    Adaptive: computes the most common color among input paths. If
    >dominance_threshold share that color, the gate is a no-op
    (monochrome plans pass through). Otherwise only dominant-color
    paths are kept — useful for plans with red/blue annotation markup.
    """
    count_before = len(paths)
    if count_before == 0:
        return paths, GateLog("color_filter", 0, 0, 0, "empty input")

    def _norm(color):
        # Coarse buckets: round each channel to nearest 0.5 so near-black
        # shade variants (0.0, 0.05, 0.1) all bucket as "black" and only
        # genuinely distinct colors (red 1,0,0 vs black 0,0,0) split.
        if color is None:
            return (0, 0, 0)
        if isinstance(color, (tuple, list)):
            return tuple(round((c or 0) * 2) / 2 for c in color)
        return color

    counts = {}
    for p in paths:
        k = _norm(getattr(p, "color", None))
        counts[k] = counts.get(k, 0) + 1

    dominant = max(counts, key=counts.get)
    dominant_pct = counts[dominant] / count_before

    if dominant_pct >= dominance_threshold:
        return paths, GateLog(
            "color_filter", count_before, count_before, 0,
            f"monochrome ({dominant_pct:.0%} dominant) - skipped"
        )

    filtered = [p for p in paths if _norm(getattr(p, "color", None)) == dominant]
    removed = count_before - len(filtered)
    return filtered, GateLog(
        "color_filter", count_before, len(filtered), removed,
        f"kept dominant color, removed {removed} non-dominant"
    )


# ============================================================
# Pipeline runners
# ============================================================

def run_heavy_pipeline(paths: list, exclusion_zones: list = None,
                       enable_color_filter: bool = False) -> FilterResult:
    """Run the full heavy-line filter pipeline.
    Returns filtered paths + complete gate log.

    Gate order: zone_mask -> weight -> length -> dash [-> color]

    The color filter (gate 5) is opt-in. It is wired into the pipeline
    and unit-tested, but defaults OFF: across the 10 test plans, several
    plans (Chipotle, CFA, Murphy) draw equipment symbols in distinct
    colors (pink/green/blue) on top of black building outlines, and
    those colored heavy paths contribute to clustering. Step 55
    architect profiles or Step 56 calibration can opt specific firms in.
    """
    result = FilterResult(paths=list(paths))

    # Gate 1: Zone mask
    result.paths, log = gate_zone_mask(result.paths, exclusion_zones or [])
    result.gate_logs.append(log)

    # Gate 2: Weight filter (heavy lines only)
    result.paths, log = gate_weight_filter(result.paths, min_weight=1.0)
    result.gate_logs.append(log)

    # Gate 3: Length filter
    result.paths, log = gate_length_filter(result.paths, min_pts=36.0)
    result.gate_logs.append(log)

    # Gate 4: Dash filter
    result.paths, log = gate_dash_filter(result.paths)
    result.gate_logs.append(log)

    # Gate 5: Color filter (opt-in)
    if enable_color_filter:
        result.paths, log = gate_color_filter(result.paths)
        result.gate_logs.append(log)

    return result


def run_allpaths_pipeline(paths: list) -> FilterResult:
    """Run the all-paths pipeline (no filtering — sacred fallback).
    Still produces a FilterResult for consistent interface."""
    return FilterResult(
        paths=list(paths),
        gate_logs=[GateLog("allpaths_passthrough", len(paths), len(paths), 0,
                          "no filtering applied")]
    )
