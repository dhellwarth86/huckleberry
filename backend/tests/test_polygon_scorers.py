"""Tests for core/polygon_scorers.py — interior density + rectilinearity."""

import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from core.polygon_scorers import (
    score_interior, score_rectilinearity, InteriorScore,
)


# ============================================================
# Helpers
# ============================================================

@dataclass
class MockTextBlock:
    text: str
    x0: float
    y0: float
    x1: float
    y1: float


@dataclass
class MockZone:
    zone_type: str
    bbox: tuple


@dataclass
class MockPath:
    points: list


def _tb(text, x, y, w=20, h=10):
    return MockTextBlock(text=text, x0=x, y0=y, x1=x + w, y1=y + h)


# Polygon bbox: (0,0)-(720,720) = 100x100 inches at 72pt/in = 10000 sqin
POLY_BBOX = (0, 0, 720, 720)
POLY_AREA = 10000.0


# ============================================================
# Interior Density
# ============================================================

class TestScoreInterior:
    def test_no_text_blocks(self):
        s = score_interior(POLY_BBOX, [], [], POLY_AREA)
        assert s.total_text_blocks == 0
        assert s.callout_density == 0.0
        # No callouts -> density penalty -> negative score
        assert s.density_score < 0

    def test_high_callout_density(self):
        # Many short equipment labels inside polygon
        blocks = [_tb(f"RTU-{i}", 100 + i * 30, 100) for i in range(20)]
        s = score_interior(POLY_BBOX, blocks, [], POLY_AREA)
        assert s.callout_count == 20
        # 20 callouts * 2 / 10000 sqin = 0.004 — actually low density per sqin
        # Need a smaller polygon to get meaningful density. Use 50x50 in = 2500 sqin
        small_bbox = (0, 0, 360, 360)
        s2 = score_interior(small_bbox, blocks, [], 2500.0)
        # 20*2/2500 = 0.016 still under threshold
        # Try even smaller — 20x20 in = 400 sqin -> 0.1 density
        tiny_bbox = (0, 0, 1440, 1440)  # huge bbox so all blocks inside
        s3 = score_interior(tiny_bbox, blocks, [], 400.0)
        assert s3.callout_density > 0.04  # crosses high-density threshold
        assert s3.density_score > 0

    def test_low_callout_density(self):
        # Few blocks in a huge polygon
        blocks = [_tb("note", 100, 100), _tb("ref", 200, 200)]
        s = score_interior(POLY_BBOX, blocks, [], POLY_AREA)
        assert s.callout_density < 0.02
        assert s.density_score < 0  # density penalty

    def test_long_text_contamination(self):
        # 10 long paragraphs (notes) inside polygon
        long_text = "x" * 100
        blocks = [_tb(long_text, 100 + i * 50, 100) for i in range(10)]
        s = score_interior(POLY_BBOX, blocks, [], POLY_AREA)
        assert s.long_text_count == 10
        assert s.long_text_ratio == 1.0
        # Long-text penalty applied
        assert s.density_score < 0

    def test_zone_overlap_penalty(self):
        # Polygon overlaps a notes_area zone
        zones = [MockZone("notes_area", (0, 0, 720, 360))]  # half of polygon
        s = score_interior(POLY_BBOX, [_tb("RTU-1", 100, 100)], zones, POLY_AREA)
        assert s.noise_zone_overlap_pct > 0.05
        # Overlap penalty -1.0
        assert s.density_score <= -1.0

    def test_no_zones_provided(self):
        s = score_interior(POLY_BBOX, [_tb("RTU-1", 100, 100)], None, POLY_AREA)
        assert s.noise_zone_overlap_pct == 0.0

    def test_dimension_string_counted(self):
        blocks = [_tb("26'-8\"", 100, 100), _tb("4'-0\"", 200, 100)]
        s = score_interior(POLY_BBOX, blocks, [], POLY_AREA)
        assert s.dimension_count == 2

    def test_equipment_keywords(self):
        blocks = [
            _tb("RTU-1", 100, 100),
            _tb("DRAIN", 200, 100),
            _tb("EF-2", 300, 100),
            _tb("VTR", 400, 100),
        ]
        s = score_interior(POLY_BBOX, blocks, [], POLY_AREA)
        assert s.callout_count == 4

    def test_text_outside_polygon_excluded(self):
        # Block centered far outside
        blocks = [_tb("RTU-1", 5000, 5000)]
        s = score_interior(POLY_BBOX, blocks, [], POLY_AREA)
        assert s.total_text_blocks == 0

    def test_score_comparison_higher_callouts_wins(self):
        # Same area, two polygons — one with many callouts, one with few
        bbox = (0, 0, 1440, 1440)  # large area to test density
        many = [_tb(f"RTU-{i}", 100 + i * 20, 100) for i in range(15)]
        few = [_tb("RTU-1", 100, 100), _tb("RTU-2", 200, 100)]
        s_many = score_interior(bbox, many, [], 400.0)
        s_few = score_interior(bbox, few, [], 400.0)
        assert s_many.density_score > s_few.density_score


# ============================================================
# Rectilinearity
# ============================================================

class TestScoreRectilinearity:
    def test_empty(self):
        assert score_rectilinearity([]) == 0.0

    def test_all_horizontal(self):
        # Path with very wide bbox, near-zero height
        paths = [MockPath(points=[(0, 0), (100, 0.01)]) for _ in range(5)]
        assert score_rectilinearity(paths) == 1.0

    def test_all_vertical(self):
        paths = [MockPath(points=[(0, 0), (0.01, 100)]) for _ in range(5)]
        assert score_rectilinearity(paths) == 1.0

    def test_all_diagonal(self):
        # Square bbox = aspect 1 = not rectilinear
        paths = [MockPath(points=[(0, 0), (50, 50)]) for _ in range(5)]
        assert score_rectilinearity(paths) == 0.0

    def test_mixed(self):
        rect = [MockPath(points=[(0, 0), (100, 0.01)]) for _ in range(8)]
        diag = [MockPath(points=[(0, 0), (50, 50)]) for _ in range(2)]
        s = score_rectilinearity(rect + diag)
        assert 0.7 < s < 0.9

    def test_skips_point_like(self):
        # Point-like paths should be skipped (not counted in denominator)
        points = [MockPath(points=[(0, 0), (0, 0)])]
        rect = [MockPath(points=[(0, 0), (100, 0.01)])]
        s = score_rectilinearity(points + rect)
        assert s == 1.0  # only the rectilinear one counted
