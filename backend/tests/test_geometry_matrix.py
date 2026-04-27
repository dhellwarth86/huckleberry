"""
Tests for core/geometry_matrix.py

Tests are split into:
  - Unit conversion tests (pure math, no images)
  - Measurement tests (percentage-coord line/polygon math)
  - Shapely polygon operation tests
  - Integration tests (OpenCV contour detection on synthetic images)
"""

import math
import pytest
import cv2
import numpy as np
from PIL import Image
from shapely.geometry import Polygon

from core.geometry_matrix import GeometryMatrix, DetectedContour, GeometryResult


# ---------------------------------------------------------------------------
# Unit conversion tests
# ---------------------------------------------------------------------------

class TestUnitConversions:
    """Test pixel ↔ feet conversions."""

    def setup_method(self):
        self.gm = GeometryMatrix()

    def test_px_area_to_sqft(self):
        # 150 DPI, 1/4" = 1' scale (4 ft/in)
        # A 150x150 px square = 1"x1" on paper = 4'x4' = 16 sqft
        result = GeometryMatrix._px_area_to_sqft(
            area_px=150 * 150, px_per_inch=150, ft_per_inch=4.0
        )
        assert result == pytest.approx(16.0)

    def test_px_length_to_ft(self):
        # 150 px = 1 inch at 150 DPI, at 1/4" scale = 4 ft
        result = GeometryMatrix._px_length_to_ft(
            length_px=150, px_per_inch=150, ft_per_inch=4.0
        )
        assert result == pytest.approx(4.0)

    def test_px_to_feet_method(self):
        result = self.gm.px_to_feet(300, px_per_inch=150, ft_per_inch=8.0)
        # 300 px = 2 inches, × 8 ft/in = 16 ft
        assert result == pytest.approx(16.0)

    def test_feet_to_px(self):
        result = self.gm.feet_to_px(16.0, px_per_inch=150, ft_per_inch=8.0)
        # 16 ft / 8 ft/in = 2 inches, × 150 px/in = 300 px
        assert result == pytest.approx(300.0)

    def test_roundtrip_px_ft(self):
        px = 450.0
        ft = self.gm.px_to_feet(px, 150, 4.0)
        back = self.gm.feet_to_px(ft, 150, 4.0)
        assert back == pytest.approx(px)


class TestCoordinateConversions:
    """Test pixel ↔ percentage coordinate conversions."""

    def setup_method(self):
        self.gm = GeometryMatrix()

    def test_px_to_pct(self):
        x_pct, y_pct = self.gm.px_to_pct(500, 300, 1000, 600)
        assert x_pct == pytest.approx(50.0)
        assert y_pct == pytest.approx(50.0)

    def test_pct_to_px(self):
        x_px, y_px = self.gm.pct_to_px(50.0, 50.0, 1000, 600)
        assert x_px == 500
        assert y_px == 300

    def test_origin(self):
        x_pct, y_pct = self.gm.px_to_pct(0, 0, 1000, 600)
        assert x_pct == 0.0
        assert y_pct == 0.0

    def test_corner(self):
        x_pct, y_pct = self.gm.px_to_pct(1000, 600, 1000, 600)
        assert x_pct == pytest.approx(100.0)
        assert y_pct == pytest.approx(100.0)


# ---------------------------------------------------------------------------
# Percentage-coordinate measurement tests (proven from predecessor)
# ---------------------------------------------------------------------------

class TestMeasureLine:
    """Test measure_line_ft — backend equivalent of pctToFeet()."""

    def setup_method(self):
        self.gm = GeometryMatrix()

    def test_horizontal_line(self):
        # Page: 36" × 24", scale 1/4" = 1' (4 ft/in)
        # Line from 0% to 50% horizontally = 18 inches = 72 ft
        ft = self.gm.measure_line_ft(0, 50, 50, 50, 36.0, 24.0, 4.0)
        assert ft == pytest.approx(72.0)

    def test_vertical_line(self):
        # 0% to 50% vertically on 24" page = 12 inches = 48 ft
        ft = self.gm.measure_line_ft(50, 0, 50, 50, 36.0, 24.0, 4.0)
        assert ft == pytest.approx(48.0)

    def test_diagonal_line(self):
        # 3-4-5 triangle: dx=30%, dy=40% on 36"×24" page
        # dx = 0.3 × 36 = 10.8", dy = 0.4 × 24 = 9.6"
        # length = √(10.8² + 9.6²) = √(116.64 + 92.16) = √208.8 ≈ 14.45"
        # × 4 ft/in ≈ 57.8 ft
        ft = self.gm.measure_line_ft(10, 10, 40, 50, 36.0, 24.0, 4.0)
        expected = math.sqrt((0.3 * 36) ** 2 + (0.4 * 24) ** 2) * 4.0
        assert ft == pytest.approx(expected)

    def test_zero_length(self):
        ft = self.gm.measure_line_ft(50, 50, 50, 50, 36.0, 24.0, 4.0)
        assert ft == pytest.approx(0.0)

    def test_different_scale(self):
        # 1/8" = 1' (8 ft/in), full width = 36" = 288 ft
        ft = self.gm.measure_line_ft(0, 50, 100, 50, 36.0, 24.0, 8.0)
        assert ft == pytest.approx(288.0)


class TestMeasurePolygon:
    """Test measure_polygon_sqft — backend equivalent of polygonAreaSqft()."""

    def setup_method(self):
        self.gm = GeometryMatrix()

    def test_rectangle(self):
        # 50% × 50% of a 36" × 24" page at 1/4" = 1'
        # = 18" × 12" on paper = 72' × 48' = 3456 sqft
        corners = [(25, 25), (75, 25), (75, 75), (25, 75)]
        sqft = self.gm.measure_polygon_sqft(corners, 36.0, 24.0, 4.0)
        assert sqft == pytest.approx(3456.0)

    def test_triangle(self):
        # Right triangle: base 50%, height 50%
        # base = 18" × 4 = 72', height = 12" × 4 = 48'
        # area = 0.5 × 72 × 48 = 1728 sqft
        corners = [(25, 75), (75, 75), (25, 25)]
        sqft = self.gm.measure_polygon_sqft(corners, 36.0, 24.0, 4.0)
        assert sqft == pytest.approx(1728.0)

    def test_too_few_points(self):
        assert self.gm.measure_polygon_sqft([(0, 0), (50, 50)], 36.0, 24.0, 4.0) == 0.0

    def test_empty(self):
        assert self.gm.measure_polygon_sqft([], 36.0, 24.0, 4.0) == 0.0

    def test_full_page(self):
        # Entire page: 36" × 24" at 4 ft/in = 144' × 96' = 13824 sqft
        corners = [(0, 0), (100, 0), (100, 100), (0, 100)]
        sqft = self.gm.measure_polygon_sqft(corners, 36.0, 24.0, 4.0)
        assert sqft == pytest.approx(13824.0)


# ---------------------------------------------------------------------------
# Shapely polygon operations
# ---------------------------------------------------------------------------

class TestPolygonOperations:
    """Test polygon subtract, union, and conversion."""

    def setup_method(self):
        self.gm = GeometryMatrix()

    def test_contour_to_polygon(self):
        contour = DetectedContour(
            points_px=[(0, 0), (100, 0), (100, 100), (0, 100)],
            points_pct=[(0, 0), (10, 0), (10, 10), (0, 10)],
            area_px=10000, perimeter_px=400, bbox=(0, 0, 100, 100),
            vertex_count=4,
        )
        poly = self.gm.contour_to_polygon(contour)
        assert poly is not None
        assert poly.area == pytest.approx(10000.0)

    def test_contour_to_polygon_too_few_points(self):
        contour = DetectedContour(
            points_px=[(0, 0), (100, 0)],
            points_pct=[(0, 0), (10, 0)],
            area_px=0, perimeter_px=100, bbox=(0, 0, 100, 0),
            vertex_count=2,
        )
        assert self.gm.contour_to_polygon(contour) is None

    def test_subtract_polygons(self):
        outer = Polygon([(0, 0), (100, 0), (100, 100), (0, 100)])
        hole = Polygon([(25, 25), (75, 25), (75, 75), (25, 75)])
        result = self.gm.subtract_polygons(outer, [hole])
        # 10000 - 2500 = 7500
        assert result.area == pytest.approx(7500.0)

    def test_subtract_no_overlap(self):
        outer = Polygon([(0, 0), (50, 0), (50, 50), (0, 50)])
        hole = Polygon([(60, 60), (80, 60), (80, 80), (60, 80)])
        result = self.gm.subtract_polygons(outer, [hole])
        assert result.area == pytest.approx(2500.0)

    def test_union_polygons(self):
        p1 = Polygon([(0, 0), (60, 0), (60, 50), (0, 50)])
        p2 = Polygon([(40, 0), (100, 0), (100, 50), (40, 50)])
        result = self.gm.union_polygons([p1, p2])
        # Union = 100 × 50 = 5000
        assert result.area == pytest.approx(5000.0)

    def test_union_empty(self):
        result = self.gm.union_polygons([])
        assert result.area == 0.0

    def test_polygon_area_sqft(self):
        poly = Polygon([(0, 0), (150, 0), (150, 150), (0, 150)])
        # 150×150 px at 150 DPI = 1"×1" = 4'×4' = 16 sqft
        sqft = self.gm.polygon_area_sqft(poly, px_per_inch=150, ft_per_inch=4.0)
        assert sqft == pytest.approx(16.0)

    def test_polygon_perimeter_ft(self):
        poly = Polygon([(0, 0), (150, 0), (150, 150), (0, 150)])
        # Perimeter = 600 px = 4 inches = 16 ft
        ft = self.gm.polygon_perimeter_ft(poly, px_per_inch=150, ft_per_inch=4.0)
        assert ft == pytest.approx(16.0)


# ---------------------------------------------------------------------------
# Integration tests — contour detection on synthetic images
# ---------------------------------------------------------------------------

def _make_white_image(width=1000, height=700) -> Image.Image:
    """Create a white image (simulates blank plan background)."""
    return Image.fromarray(np.ones((height, width, 3), dtype=np.uint8) * 255)


def _draw_rectangle(img: Image.Image, x1, y1, x2, y2,
                     color=(0, 0, 0), thickness=3) -> Image.Image:
    """Draw a black rectangle on a white image."""
    arr = np.array(img)
    cv2.rectangle(arr, (x1, y1), (x2, y2), color, thickness)
    return Image.fromarray(arr)


def _draw_filled_rectangle(img: Image.Image, x1, y1, x2, y2,
                            color=(0, 0, 0)) -> Image.Image:
    """Draw a filled rectangle."""
    arr = np.array(img)
    cv2.rectangle(arr, (x1, y1), (x2, y2), color, -1)
    return Image.fromarray(arr)


class TestContourDetection:
    """Integration tests with synthetic plan images."""

    def setup_method(self):
        self.gm = GeometryMatrix()

    def test_detect_single_rectangle(self):
        """A single black rectangle on white should produce one contour."""
        img = _make_white_image(1000, 700)
        img = _draw_rectangle(img, 100, 100, 800, 500)

        result = self.gm.detect_contours(img, dpi=100)
        assert isinstance(result, GeometryResult)
        assert len(result.contours) >= 1
        assert result.building_outline is not None

        # Building outline should be the rectangle
        outline = result.building_outline
        assert outline.area_px > 0
        assert outline.perimeter_px > 0
        assert outline.vertex_count >= 4

    def test_detect_with_scale(self):
        """Contour areas should convert to sqft when scale is provided."""
        img = _make_white_image(1000, 700)
        img = _draw_rectangle(img, 100, 100, 800, 500)

        result = self.gm.detect_contours(img, ft_per_inch=4.0, dpi=100)
        outline = result.building_outline
        assert outline is not None
        assert outline.area_sqft is not None
        assert outline.area_sqft > 0
        assert outline.perimeter_ft is not None
        assert outline.perimeter_ft > 0

    def test_percentage_coordinates(self):
        """Contour points_pct should be in 0-100 range."""
        img = _make_white_image(1000, 700)
        img = _draw_rectangle(img, 200, 150, 800, 550)

        result = self.gm.detect_contours(img)
        assert len(result.contours) >= 1
        for c in result.contours:
            for x_pct, y_pct in c.points_pct:
                assert 0 <= x_pct <= 100
                assert 0 <= y_pct <= 100

    def test_multiple_rectangles(self):
        """Two separated rectangles should produce multiple contours."""
        img = _make_white_image(1000, 700)
        img = _draw_rectangle(img, 50, 50, 400, 300)
        img = _draw_rectangle(img, 550, 350, 950, 650)

        result = self.gm.detect_contours(img)
        assert len(result.contours) >= 2

    def test_largest_is_building_outline(self):
        """Building outline should be the largest outermost contour."""
        img = _make_white_image(1000, 700)
        # Large rectangle
        img = _draw_rectangle(img, 50, 50, 900, 600)
        # Small rectangle
        img = _draw_rectangle(img, 100, 100, 200, 200)

        result = self.gm.detect_contours(img)
        outline = result.building_outline
        assert outline is not None
        # The outline should be the large one
        assert outline.bbox[2] > 500  # width > 500 px

    def test_small_contours_filtered(self):
        """Contours below min_area_ratio should be filtered out."""
        img = _make_white_image(1000, 700)
        # Large rectangle (significant)
        img = _draw_rectangle(img, 50, 50, 900, 600)
        # Tiny rectangle (noise — well below 1% of page)
        img = _draw_rectangle(img, 450, 300, 460, 310)

        gm = GeometryMatrix(min_area_ratio=0.01)
        result = gm.detect_contours(img)
        # Tiny contour should be filtered
        for c in result.contours:
            assert c.area_px >= 1000 * 700 * 0.01

    def test_empty_image(self):
        """Pure white image should produce no contours."""
        img = _make_white_image(1000, 700)
        result = self.gm.detect_contours(img)
        assert len(result.contours) == 0
        assert result.building_outline is None

    def test_result_metadata(self):
        """GeometryResult should store image dimensions and settings."""
        img = _make_white_image(1000, 700)
        result = self.gm.detect_contours(img, ft_per_inch=8.0, dpi=150)
        assert result.image_width_px == 1000
        assert result.image_height_px == 700
        assert result.scale_ft_per_inch == 8.0
        assert result.dpi == 150

    def test_building_area_reasonable(self):
        """
        Sanity check: a known-size rectangle should produce a reasonable area.

        700×400 px rectangle at 150 DPI, 1/4" = 1' scale (4 ft/in):
        Width: 700/150 = 4.667" → 18.67 ft
        Height: 400/150 = 2.667" → 10.67 ft
        Area ≈ 199 sqft

        We allow ±20% because OpenCV contour area varies slightly from
        the geometric rectangle due to pixel boundaries and preprocessing.
        """
        img = _make_white_image(1000, 700)
        img = _draw_rectangle(img, 100, 100, 800, 500, thickness=4)

        result = self.gm.detect_contours(img, ft_per_inch=4.0, dpi=150)
        outline = result.building_outline
        assert outline is not None

        # Expected: ~700×400 px rect → ~(4.67" × 2.67") × 16 = ~199 sqft
        expected_w_in = 700 / 150
        expected_h_in = 400 / 150
        expected_sqft = expected_w_in * expected_h_in * (4.0 ** 2)

        assert outline.area_sqft == pytest.approx(expected_sqft, rel=0.2)
