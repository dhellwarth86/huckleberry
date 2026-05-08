"""
Tests for core/pdf_engine.py

Tests are split into:
  - Unit tests for dimension/scale parsers (no PDF needed)
  - Integration tests for PDF operations (require a test PDF)
"""

import pytest
from pathlib import Path
from unittest.mock import MagicMock

from PIL import Image

from core.pdf_engine import (
    PDFEngine,
    PDFDocument,
    PageMeta,
    TextBlock,
    VectorPath,
    _parse_dimension_to_feet,
    parse_scale_to_ft_per_inch,
)


# ---------------------------------------------------------------------------
# Dimension parser tests (proven patterns from predecessor)
# ---------------------------------------------------------------------------

class TestDimensionParser:
    """Test _parse_dimension_to_feet with all known architectural formats."""

    def test_feet_and_inches(self):
        assert _parse_dimension_to_feet("45'-6\"") == pytest.approx(45.5)

    def test_feet_and_zero_inches(self):
        assert _parse_dimension_to_feet("12'-0\"") == pytest.approx(12.0)

    def test_feet_only(self):
        assert _parse_dimension_to_feet("120'") == pytest.approx(120.0)

    def test_inches_only(self):
        assert _parse_dimension_to_feet("6\"") == pytest.approx(0.5)

    def test_feet_inches_fraction(self):
        # 10'-6 1/2" = 10 + 6.5/12 = 10.5417
        assert _parse_dimension_to_feet("10'-6 1/2\"") == pytest.approx(10.5417, abs=0.001)

    def test_unicode_foot_mark(self):
        assert _parse_dimension_to_feet("45\u2032-6\u2033") == pytest.approx(45.5)

    def test_no_dash(self):
        assert _parse_dimension_to_feet("45' 6\"") == pytest.approx(45.5)

    def test_none_input(self):
        assert _parse_dimension_to_feet(None) is None

    def test_empty_string(self):
        assert _parse_dimension_to_feet("") is None

    def test_no_dimension(self):
        assert _parse_dimension_to_feet("hello world") is None

    def test_non_string(self):
        assert _parse_dimension_to_feet(42) is None

    def test_decimal_feet(self):
        assert _parse_dimension_to_feet("10.5'") == pytest.approx(10.5)

    def test_decimal_inches(self):
        assert _parse_dimension_to_feet("4.5\"") == pytest.approx(0.375)


class TestScaleParser:
    """Test parse_scale_to_ft_per_inch with architectural scale strings."""

    def test_quarter_inch(self):
        assert parse_scale_to_ft_per_inch('1/4" = 1\'') == pytest.approx(4.0)

    def test_eighth_inch(self):
        assert parse_scale_to_ft_per_inch('1/8" = 1\'') == pytest.approx(8.0)

    def test_three_sixteenths(self):
        assert parse_scale_to_ft_per_inch('3/16" = 1\'-0"') == pytest.approx(5.333, abs=0.01)

    def test_half_inch(self):
        assert parse_scale_to_ft_per_inch('1/2" = 1\'') == pytest.approx(2.0)

    def test_none_input(self):
        assert parse_scale_to_ft_per_inch(None) is None

    def test_empty_string(self):
        assert parse_scale_to_ft_per_inch("") is None

    def test_no_match(self):
        assert parse_scale_to_ft_per_inch("not a scale") is None

    def test_unicode_marks(self):
        assert parse_scale_to_ft_per_inch('1/4\u2033 = 1\u2032') == pytest.approx(4.0)


# ---------------------------------------------------------------------------
# PDFEngine unit tests (data class construction, validation)
# ---------------------------------------------------------------------------

class TestPageMeta:
    def test_construction(self):
        meta = PageMeta(
            page_number=0,
            width_pts=2592, height_pts=1728,
            width_in=36.0, height_in=24.0,
            rotation=0,
        )
        assert meta.width_in == 36.0
        assert meta.height_in == 24.0

    def test_standard_arch_d(self):
        """ARCH D size: 36 x 24 inches = 2592 x 1728 pts."""
        meta = PageMeta(0, 2592, 1728, 36.0, 24.0, 0)
        assert meta.width_pts == 2592
        assert meta.height_pts == 1728


class TestPDFEngineValidation:
    """Test engine behavior with invalid inputs (no real PDF needed)."""

    def test_open_nonexistent_file(self):
        engine = PDFEngine()
        with pytest.raises(FileNotFoundError):
            engine.open("/nonexistent/file.pdf")

    def test_open_non_pdf(self, tmp_path):
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("not a pdf")
        engine = PDFEngine()
        with pytest.raises(ValueError, match="Not a PDF"):
            engine.open(txt_file)

    def test_page_out_of_range(self):
        engine = PDFEngine()
        doc = PDFDocument(path="fake.pdf", page_count=3, pages=[], _doc=MagicMock())
        with pytest.raises(IndexError):
            engine._validate_page(doc, 5)

    def test_negative_page(self):
        engine = PDFEngine()
        doc = PDFDocument(path="fake.pdf", page_count=3, pages=[], _doc=MagicMock())
        with pytest.raises(IndexError):
            engine._validate_page(doc, -1)

    def test_closed_doc(self):
        engine = PDFEngine()
        doc = PDFDocument(path="fake.pdf", page_count=3, pages=[], _doc=None)
        with pytest.raises(RuntimeError, match="closed"):
            engine._validate_page(doc, 0)


# ---------------------------------------------------------------------------
# PDF integration tests (require PyMuPDF to create a real test PDF)
# ---------------------------------------------------------------------------

@pytest.fixture
def test_pdf(tmp_path) -> Path:
    """Create a minimal test PDF with known content."""
    doc = fitz.open()  # New empty PDF
    page = doc.new_page(width=792, height=612)  # Letter size (11x8.5")

    # Add some text
    text_point = fitz.Point(72, 72)
    page.insert_text(text_point, "ROOF PLAN", fontsize=24)
    page.insert_text(fitz.Point(72, 120), "Scale: 1/4\" = 1'-0\"", fontsize=12)
    page.insert_text(fitz.Point(72, 150), "45'-6\" x 30'-0\"", fontsize=12)

    # Draw a rectangle (simulating a building outline)
    rect = fitz.Rect(100, 200, 500, 400)
    page.draw_rect(rect, color=(0, 0, 0), width=2)

    # Draw a line
    page.draw_line(fitz.Point(100, 300), fitz.Point(500, 300), color=(0.5, 0.5, 0.5))

    pdf_path = tmp_path / "test_plan.pdf"
    doc.save(str(pdf_path))
    doc.close()
    return pdf_path


import fitz  # needed for test_pdf fixture


class TestPDFEngineIntegration:
    """Integration tests using a real test PDF."""

    def test_open_and_close(self, test_pdf):
        engine = PDFEngine()
        doc = engine.open(test_pdf)
        assert doc.page_count == 1
        assert doc._doc is not None
        engine.close(doc)
        assert doc._doc is None

    def test_page_metadata(self, test_pdf):
        engine = PDFEngine()
        doc = engine.open(test_pdf)
        meta = engine.get_page_meta(doc, 0)
        assert meta.page_number == 0
        assert meta.width_pts == pytest.approx(792, abs=1)
        assert meta.height_pts == pytest.approx(612, abs=1)
        assert meta.width_in == pytest.approx(11.0, abs=0.1)
        assert meta.height_in == pytest.approx(8.5, abs=0.1)
        engine.close(doc)

    def test_render_page(self, test_pdf):
        engine = PDFEngine()
        doc = engine.open(test_pdf)
        img = engine.render_page(doc, 0)
        assert isinstance(img, Image.Image)
        assert img.mode == "RGB"
        assert img.width > 0
        assert img.height > 0
        engine.close(doc)

    def test_render_thumbnail(self, test_pdf):
        engine = PDFEngine()
        doc = engine.open(test_pdf)
        full = engine.render_page(doc, 0)
        thumb = engine.render_thumbnail(doc, 0)
        # Thumbnail should be smaller
        assert thumb.width < full.width
        assert thumb.height < full.height
        engine.close(doc)

    def test_extract_text(self, test_pdf):
        engine = PDFEngine()
        doc = engine.open(test_pdf)
        text = engine.extract_text(doc, 0)
        assert "ROOF PLAN" in text
        engine.close(doc)

    def test_extract_text_blocks(self, test_pdf):
        engine = PDFEngine()
        doc = engine.open(test_pdf)
        blocks = engine.extract_text_blocks(doc, 0)
        assert len(blocks) > 0
        texts = [b.text for b in blocks]
        assert any("ROOF PLAN" in t for t in texts)
        # Verify blocks have valid bounding boxes
        for b in blocks:
            assert b.x0 < b.x1
            assert b.y0 < b.y1
            assert b.page == 0
        engine.close(doc)

    def test_search_text(self, test_pdf):
        engine = PDFEngine()
        doc = engine.open(test_pdf)
        results = engine.search_text(doc, "ROOF")
        assert len(results) > 0
        assert results[0].page == 0
        engine.close(doc)

    def test_search_text_no_match(self, test_pdf):
        engine = PDFEngine()
        doc = engine.open(test_pdf)
        results = engine.search_text(doc, "XYZNOTFOUND")
        assert len(results) == 0
        engine.close(doc)

    def test_extract_vectors(self, test_pdf):
        engine = PDFEngine()
        doc = engine.open(test_pdf)
        paths = engine.extract_vectors(doc, 0)
        assert len(paths) > 0
        # We drew a rect and a line
        types = [p.path_type for p in paths]
        assert "rect" in types or "line" in types
        engine.close(doc)

    def test_extract_closed_polygons(self, test_pdf):
        engine = PDFEngine()
        doc = engine.open(test_pdf)
        polys = engine.extract_closed_polygons(doc, 0)
        # The rectangle we drew should be a closed polygon
        assert len(polys) > 0
        for p in polys:
            assert p.closed
            assert len(p.points) >= 3
        engine.close(doc)

    def test_find_dimensions(self, test_pdf):
        engine = PDFEngine()
        doc = engine.open(test_pdf)
        dims = engine.find_dimensions(doc, 0)
        # "45'-6\"" should be found → 45.5 ft
        values = [d["value_ft"] for d in dims]
        assert any(abs(v - 45.5) < 0.1 for v in values)
        engine.close(doc)

    def test_get_all_page_metas(self, test_pdf):
        engine = PDFEngine()
        doc = engine.open(test_pdf)
        metas = engine.get_all_page_metas(doc)
        assert len(metas) == 1
        assert metas[0].page_number == 0
        engine.close(doc)


# ---------------------------------------------------------------------------
# Phase G.3 — extract_text / extract_text_blocks per-(doc, page) cache
# ---------------------------------------------------------------------------

@pytest.fixture
def two_page_pdf(tmp_path) -> Path:
    """Create a 2-page synthetic PDF for cache-separation tests."""
    doc = fitz.open()
    p0 = doc.new_page(width=792, height=612)
    p0.insert_text(fitz.Point(72, 72), "PAGE ZERO TEXT", fontsize=18)
    p0.insert_text(fitz.Point(72, 120), "ROOF PLAN A", fontsize=12)
    p1 = doc.new_page(width=792, height=612)
    p1.insert_text(fitz.Point(72, 72), "PAGE ONE TEXT", fontsize=18)
    p1.insert_text(fitz.Point(72, 120), "FLOOR PLAN B", fontsize=12)
    pdf_path = tmp_path / "two_page.pdf"
    doc.save(str(pdf_path))
    doc.close()
    return pdf_path


class TestPDFEngineCache:
    """Phase G.3: PDFEngine must cache extract_text/extract_text_blocks
    per (doc, page) so repeat calls return the SAME object, not a re-extraction.
    """

    def test_cache_returns_same_object_on_repeat_call(self, two_page_pdf):
        engine = PDFEngine()
        doc = engine.open(two_page_pdf)
        try:
            text_a = engine.extract_text(doc, 0)
            text_b = engine.extract_text(doc, 0)
            blocks_a = engine.extract_text_blocks(doc, 0)
            blocks_b = engine.extract_text_blocks(doc, 0)
            assert text_a is text_b, "extract_text must return cached object on repeat call"
            assert blocks_a is blocks_b, "extract_text_blocks must return cached list on repeat call"
        finally:
            engine.close(doc)

    def test_cache_separates_pages(self, two_page_pdf):
        engine = PDFEngine()
        doc = engine.open(two_page_pdf)
        try:
            # Cache must be in effect (repeat call → same obj) AND key per page.
            text_p0a = engine.extract_text(doc, 0)
            text_p0b = engine.extract_text(doc, 0)
            text_p1 = engine.extract_text(doc, 1)
            assert text_p0a is text_p0b, "cache must hit on repeat call (page 0)"
            assert text_p0a is not text_p1, "cache key must include page index"

            blocks_p0a = engine.extract_text_blocks(doc, 0)
            blocks_p0b = engine.extract_text_blocks(doc, 0)
            blocks_p1 = engine.extract_text_blocks(doc, 1)
            assert blocks_p0a is blocks_p0b, "cache must hit on repeat call (blocks page 0)"
            assert blocks_p0a is not blocks_p1, "cache key must include page index (blocks)"
        finally:
            engine.close(doc)

    def test_cache_separates_text_and_blocks(self, two_page_pdf):
        engine = PDFEngine()
        doc = engine.open(two_page_pdf)
        try:
            text_a = engine.extract_text(doc, 0)
            text_b = engine.extract_text(doc, 0)
            blocks_a = engine.extract_text_blocks(doc, 0)
            blocks_b = engine.extract_text_blocks(doc, 0)
            assert text_a is text_b, "cache must hit on repeat call (text)"
            assert blocks_a is blocks_b, "cache must hit on repeat call (blocks)"
            assert text_a is not blocks_a, "cache key must include method name"
            assert isinstance(text_a, str)
            assert isinstance(blocks_a, list)
        finally:
            engine.close(doc)

    def test_cache_invalidates_on_doc_close(self, two_page_pdf):
        engine = PDFEngine()
        doc1 = engine.open(two_page_pdf)
        cached_a = engine.extract_text(doc1, 0)
        cached_b = engine.extract_text(doc1, 0)
        # Pre-close: cache must be hot.
        assert cached_a is cached_b, "cache must hit on repeat call before close"
        engine.close(doc1)
        doc2 = engine.open(two_page_pdf)
        try:
            fresh = engine.extract_text(doc2, 0)
            assert fresh is not cached_a, (
                "cache must purge entries for a closed doc; new doc must "
                "produce a fresh extraction object"
            )
        finally:
            engine.close(doc2)

    def test_cache_separates_documents(self, two_page_pdf, test_pdf):
        engine = PDFEngine()
        doc_a = engine.open(two_page_pdf)
        doc_b = engine.open(test_pdf)
        try:
            text_a1 = engine.extract_text(doc_a, 0)
            text_a2 = engine.extract_text(doc_a, 0)
            text_b1 = engine.extract_text(doc_b, 0)
            text_b2 = engine.extract_text(doc_b, 0)
            assert text_a1 is text_a2, "doc_a cache must hit on repeat call"
            assert text_b1 is text_b2, "doc_b cache must hit on repeat call"
            assert text_a1 is not text_b1, "two open docs must have separate cache entries"
        finally:
            engine.close(doc_a)
            engine.close(doc_b)


# ---------------------------------------------------------------------------
# Phase G.5b — Tile rendering API for high-DPI rasters
# ---------------------------------------------------------------------------

@pytest.fixture
def arch_d_pdf(tmp_path) -> Path:
    """Create a single-page ARCH-D-sized PDF (36 x 24 inches = 2592 x 1728 pts).

    Used for testing the tile-rendering threshold: at 250 DPI an ARCH-D page
    is ~154.5 MB raw RGB, well over the 50 MB memory threshold, so the tile
    API must return a 2x2 grid of tiles, each ~38.6 MB.
    """
    doc = fitz.open()
    p = doc.new_page(width=2592, height=1728)
    p.insert_text(fitz.Point(72, 72), "ARCH D TEST", fontsize=24)
    pdf_path = tmp_path / "arch_d.pdf"
    doc.save(str(pdf_path))
    doc.close()
    return pdf_path


class TestPDFEngineTileAPI:
    """Phase G.5b: PDFEngine tile rendering API.

    The render_page() method (existing) renders the full page at any DPI;
    for high-DPI rasters on large pages (e.g. ARCH-D at 250 DPI = 154.5 MB
    raw RGB), full rendering allocates a single huge pixmap. The tile API
    splits large pages into a 2x2 grid with 5% overlap, freeing each tile's
    pixmap before allocating the next. Small pages (under the memory
    threshold) short-circuit to a single full render for API uniformity.

    render_page() stays unchanged — the tile API is additive.
    """

    def test_estimate_render_memory_letter_under_threshold(self, test_pdf):
        """Letter (11 x 8.5 in) at 250 DPI is ~16.7 MB raw RGB, under 50 MB."""
        engine = PDFEngine()
        doc = engine.open(test_pdf)
        try:
            page = doc._doc[0]
            mb = engine._estimate_render_memory_mb(page, dpi=250)
            assert mb < 50.0, (
                f"Letter @ 250 DPI should be < 50 MB threshold, got {mb:.1f}"
            )
            assert mb > 10.0, (
                f"Letter @ 250 DPI should be > 10 MB (sanity), got {mb:.1f}"
            )
        finally:
            engine.close(doc)

    def test_estimate_render_memory_arch_d_over_threshold(self, arch_d_pdf):
        """ARCH-D (36 x 24 in) at 250 DPI is ~154.5 MB raw RGB, over 50 MB."""
        engine = PDFEngine()
        doc = engine.open(arch_d_pdf)
        try:
            page = doc._doc[0]
            mb = engine._estimate_render_memory_mb(page, dpi=250)
            assert mb > 50.0, (
                f"ARCH-D @ 250 DPI should exceed 50 MB threshold, got {mb:.1f}"
            )
            assert 140.0 < mb < 170.0, (
                f"ARCH-D @ 250 DPI ≈ 154.5 MB expected (G.0 scout math), got {mb:.1f}"
            )
        finally:
            engine.close(doc)

    def test_compute_tile_rects_2x2_with_overlap(self, arch_d_pdf):
        """2x2 grid with 5% overlap: 4 tiles, adjacent tiles share an overlap band."""
        engine = PDFEngine()
        doc = engine.open(arch_d_pdf)
        try:
            page = doc._doc[0]
            rects = engine._compute_tile_rects(page, grid=(2, 2), overlap_pct=0.05)
            assert len(rects) == 4, f"2x2 grid → 4 tiles, got {len(rects)}"

            # Index convention: row-major. rects[0]=TL, rects[1]=TR,
            # rects[2]=BL, rects[3]=BR.
            tl, tr, bl, br = rects[0], rects[1], rects[2], rects[3]
            page_w = page.rect.width    # 2592 pts
            page_h = page.rect.height   # 1728 pts

            # Horizontal overlap: TL.x1 should extend past TR.x0
            assert tr.x0 < tl.x1, (
                f"horizontally adjacent tiles must overlap "
                f"(TL.x1={tl.x1:.1f}, TR.x0={tr.x0:.1f})"
            )
            h_overlap = tl.x1 - tr.x0
            expected_h = page_w * 0.05
            assert abs(h_overlap - expected_h) < page_w * 0.02, (
                f"horizontal overlap ~{expected_h:.1f} pts expected, got {h_overlap:.1f}"
            )

            # Vertical overlap: TL.y1 should extend past BL.y0
            assert bl.y0 < tl.y1, (
                f"vertically adjacent tiles must overlap "
                f"(TL.y1={tl.y1:.1f}, BL.y0={bl.y0:.1f})"
            )
            v_overlap = tl.y1 - bl.y0
            expected_v = page_h * 0.05
            assert abs(v_overlap - expected_v) < page_h * 0.02, (
                f"vertical overlap ~{expected_v:.1f} pts expected, got {v_overlap:.1f}"
            )

            # Union of tiles must cover the full page (corners check)
            assert tl.x0 <= 0.5 and tl.y0 <= 0.5, (
                f"TL tile must cover top-left corner, got ({tl.x0:.1f}, {tl.y0:.1f})"
            )
            assert br.x1 >= page_w - 0.5 and br.y1 >= page_h - 0.5, (
                f"BR tile must cover bottom-right corner, "
                f"got ({br.x1:.1f}, {br.y1:.1f}) vs page ({page_w}, {page_h})"
            )
        finally:
            engine.close(doc)

    def test_render_page_tiled_letter_returns_single_full_render(self, test_pdf):
        """Letter @ 250 DPI is under threshold → tile API short-circuits to full render."""
        engine = PDFEngine()
        doc = engine.open(test_pdf)
        try:
            tiles = engine.render_page_tiled(doc, 0, dpi=250)
            assert len(tiles) == 1, (
                f"Letter @ 250 DPI is under memory threshold; expected single "
                f"full render, got {len(tiles)} tiles"
            )
            tile_rect, img = tiles[0]
            assert isinstance(img, Image.Image)
            assert img.mode == "RGB"
        finally:
            engine.close(doc)

    def test_render_page_tiled_arch_d_returns_4_tiles(self, arch_d_pdf):
        """ARCH-D @ 250 DPI exceeds threshold → 2x2 = 4 tiles, each under threshold."""
        engine = PDFEngine()
        doc = engine.open(arch_d_pdf)
        try:
            tiles = engine.render_page_tiled(doc, 0, dpi=250)
            assert len(tiles) == 4, (
                f"ARCH-D @ 250 DPI exceeds memory threshold; expected 2x2 = 4 "
                f"tiles, got {len(tiles)}"
            )
            for tile_rect, img in tiles:
                assert isinstance(img, Image.Image)
                assert img.mode == "RGB"
                # Each tile raw RGB should be under the threshold
                tile_mb = (img.width * img.height * 3) / (1024 ** 2)
                assert tile_mb < 50.0, (
                    f"each tile raster must be < 50 MB threshold, got {tile_mb:.1f}"
                )
        finally:
            engine.close(doc)
