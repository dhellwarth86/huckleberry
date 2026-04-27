"""Tests for core/filter_pipeline.py — composable gate chain."""

import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from core.filter_pipeline import (
    gate_zone_mask, gate_weight_filter, gate_length_filter, gate_dash_filter,
    gate_color_filter,
    run_heavy_pipeline, run_allpaths_pipeline, GateLog, FilterResult,
)


# ============================================================
# Mock VectorPath for testing
# ============================================================

@dataclass
class MockPath:
    """Minimal mock of VectorPath for filter testing."""
    points: list
    width: float = 2.0
    dashes: str = ""
    closed: bool = True
    color: Optional[tuple] = None

    @property
    def bbox_diag_pts(self) -> float:
        if not self.points:
            return 0.0
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]
        dx = max(xs) - min(xs)
        dy = max(ys) - min(ys)
        return (dx * dx + dy * dy) ** 0.5


def _make_path(cx=100, cy=100, size=50, width=2.0, dashes="", color=None):
    """Create a mock path centered at (cx, cy) with given size."""
    half = size / 2
    return MockPath(
        points=[(cx - half, cy - half), (cx + half, cy - half),
                (cx + half, cy + half), (cx - half, cy + half)],
        width=width,
        dashes=dashes,
        color=color,
    )


# ============================================================
# Gate 1: Zone Mask
# ============================================================

class TestGateZoneMask:
    def test_no_zones_passes_all(self):
        paths = [_make_path(100, 100), _make_path(200, 200)]
        filtered, log = gate_zone_mask(paths, [])
        assert len(filtered) == 2
        assert log.paths_removed == 0
        assert "no exclusion zones" in log.details

    def test_removes_paths_in_zone(self):
        paths = [_make_path(100, 100), _make_path(500, 500)]
        zones = [{"x0": 50, "y0": 50, "x1": 150, "y1": 150}]
        filtered, log = gate_zone_mask(paths, zones)
        assert len(filtered) == 1
        assert log.paths_removed == 1

    def test_keeps_paths_outside_zone(self):
        paths = [_make_path(500, 500)]
        zones = [{"x0": 0, "y0": 0, "x1": 100, "y1": 100}]
        filtered, log = gate_zone_mask(paths, zones)
        assert len(filtered) == 1
        assert log.paths_removed == 0

    def test_multiple_zones(self):
        paths = [_make_path(100, 100), _make_path(300, 300), _make_path(500, 500)]
        zones = [
            {"x0": 50, "y0": 50, "x1": 150, "y1": 150},
            {"x0": 250, "y0": 250, "x1": 350, "y1": 350},
        ]
        filtered, log = gate_zone_mask(paths, zones)
        assert len(filtered) == 1  # only (500,500) survives
        assert log.paths_removed == 2

    def test_empty_paths(self):
        filtered, log = gate_zone_mask([], [{"x0": 0, "y0": 0, "x1": 100, "y1": 100}])
        assert len(filtered) == 0
        assert log.paths_removed == 0


# ============================================================
# Gate 2: Weight Filter
# ============================================================

class TestGateWeightFilter:
    def test_keeps_heavy_paths(self):
        paths = [_make_path(width=2.0), _make_path(width=0.5)]
        filtered, log = gate_weight_filter(paths, min_weight=1.0)
        assert len(filtered) == 1
        assert log.paths_removed == 1

    def test_threshold_boundary(self):
        paths = [_make_path(width=1.0), _make_path(width=1.01)]
        filtered, log = gate_weight_filter(paths, min_weight=1.0)
        assert len(filtered) == 1  # 1.0 is not > 1.0

    def test_all_heavy(self):
        paths = [_make_path(width=3.0), _make_path(width=5.0)]
        filtered, log = gate_weight_filter(paths, min_weight=1.0)
        assert len(filtered) == 2
        assert log.paths_removed == 0


# ============================================================
# Gate 3: Length Filter
# ============================================================

class TestGateLengthFilter:
    def test_removes_short_paths(self):
        short = _make_path(size=10)   # diag ~14 pts
        long = _make_path(size=100)   # diag ~141 pts
        filtered, log = gate_length_filter([short, long], min_pts=36.0)
        assert len(filtered) == 1
        assert log.paths_removed == 1

    def test_keeps_long_paths(self):
        paths = [_make_path(size=200)]
        filtered, log = gate_length_filter(paths, min_pts=36.0)
        assert len(filtered) == 1


# ============================================================
# Gate 4: Dash Filter
# ============================================================

class TestGateDashFilter:
    def test_keeps_solid(self):
        solid = _make_path(dashes="")
        solid2 = _make_path(dashes="[] 0")
        filtered, log = gate_dash_filter([solid, solid2])
        assert len(filtered) == 2
        assert log.paths_removed == 0

    def test_removes_dashed(self):
        dashed = _make_path(dashes="[3 5] 0")
        solid = _make_path(dashes="")
        filtered, log = gate_dash_filter([dashed, solid])
        assert len(filtered) == 1
        assert log.paths_removed == 1

    def test_removes_dotted(self):
        dotted = _make_path(dashes="[1 2] 0")
        filtered, log = gate_dash_filter([dotted])
        assert len(filtered) == 0


# ============================================================
# Full Pipelines
# ============================================================

class TestRunHeavyPipeline:
    def test_full_pipeline_runs_all_gates(self):
        # Color filter is opt-in; default runs 4 gates
        paths = [_make_path(width=2.0, size=100)]
        result = run_heavy_pipeline(paths)
        assert len(result.gate_logs) == 4
        gate_names = [g.gate_name for g in result.gate_logs]
        assert gate_names == ["zone_mask", "weight_filter", "length_filter",
                              "dash_filter"]

    def test_color_filter_opt_in(self):
        paths = [_make_path(width=2.0, size=100)]
        result = run_heavy_pipeline(paths, enable_color_filter=True)
        assert len(result.gate_logs) == 5
        assert result.gate_logs[-1].gate_name == "color_filter"

    def test_gates_chain_correctly(self):
        # Create a mix: one path that passes all, one that fails weight, one that fails dash
        good = _make_path(cx=500, cy=500, width=2.0, size=100, dashes="")
        thin = _make_path(cx=500, cy=500, width=0.3, size=100, dashes="")
        dashed = _make_path(cx=500, cy=500, width=2.0, size=100, dashes="[3 5] 0")
        result = run_heavy_pipeline([good, thin, dashed])
        assert len(result.paths) == 1  # only good survives
        assert result.total_removed == 2

    def test_empty_input(self):
        result = run_heavy_pipeline([])
        assert len(result.paths) == 0
        assert len(result.gate_logs) == 4

    def test_summary_format(self):
        result = run_heavy_pipeline([_make_path()])
        summary = result.summary()
        assert "zone_mask" in summary
        assert "weight_filter" in summary

    def test_with_exclusion_zones(self):
        in_zone = _make_path(cx=100, cy=100, width=2.0, size=50)
        outside = _make_path(cx=500, cy=500, width=2.0, size=100)
        zones = [{"x0": 50, "y0": 50, "x1": 150, "y1": 150}]
        result = run_heavy_pipeline([in_zone, outside], exclusion_zones=zones)
        assert len(result.paths) == 1
        assert result.gate_logs[0].paths_removed == 1  # zone mask removed 1


class TestRunAllpathsPipeline:
    def test_no_filtering(self):
        paths = [_make_path(), _make_path()]
        result = run_allpaths_pipeline(paths)
        assert len(result.paths) == 2
        assert len(result.gate_logs) == 1
        assert result.gate_logs[0].gate_name == "allpaths_passthrough"
        assert result.total_removed == 0

    def test_empty_input(self):
        result = run_allpaths_pipeline([])
        assert len(result.paths) == 0
        assert result.gate_logs[0].paths_in == 0


# ============================================================
# Gate 5: Color Filter
# ============================================================

class TestGateColorFilter:
    def test_empty_input(self):
        filtered, log = gate_color_filter([])
        assert filtered == []
        assert log.paths_removed == 0

    def test_no_color_attribute_is_monochrome(self):
        # All paths default color=None -> normalized to (0,0,0) -> 100% dominant
        paths = [_make_path() for _ in range(5)]
        filtered, log = gate_color_filter(paths)
        assert len(filtered) == 5
        assert log.paths_removed == 0
        assert "monochrome" in log.details

    def test_all_black(self):
        paths = [_make_path(color=(0, 0, 0)) for _ in range(5)]
        filtered, log = gate_color_filter(paths)
        assert len(filtered) == 5
        assert log.paths_removed == 0

    def test_dominant_passes_through(self):
        # 95% black + 5% red -> below threshold? 0.05 < 0.10 so dominant=0.95 >= 0.90 -> skip
        paths = [_make_path(color=(0, 0, 0)) for _ in range(19)]
        paths.append(_make_path(color=(1, 0, 0)))
        filtered, log = gate_color_filter(paths)
        assert len(filtered) == 20  # all kept (95% dominant)
        assert log.paths_removed == 0

    def test_below_threshold_filters(self):
        # 80% black + 20% red -> below 90% threshold -> filter to dominant
        paths = [_make_path(color=(0, 0, 0)) for _ in range(8)]
        paths.extend(_make_path(color=(1, 0, 0)) for _ in range(2))
        filtered, log = gate_color_filter(paths)
        assert len(filtered) == 8
        assert log.paths_removed == 2

    def test_single_non_black_color(self):
        # All red -> dominant -> kept
        paths = [_make_path(color=(1, 0, 0)) for _ in range(5)]
        filtered, log = gate_color_filter(paths)
        assert len(filtered) == 5
