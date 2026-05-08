"""
TracePoint PDF Engine — PyMuPDF (fitz) wrapper.

Handles:
  - Opening and validating PDF files
  - Page rendering to PIL images at configurable DPI
  - Thumbnail generation
  - Text extraction (full page + search)
  - Vector path extraction (lines, curves, rectangles)
  - Page metadata (dimensions in points, inches, pixel size)

All coordinates use PDF points (1 pt = 1/72 inch) unless noted otherwise.
"""

import io
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import fitz  # PyMuPDF
from PIL import Image

from core.config import PDF_MAX_DIMENSION, PDF_RENDER_DPI, PDF_THUMBNAIL_DPI


# ---------------------------------------------------------------------------
# Phase G.5b — Tile rendering constants
# ---------------------------------------------------------------------------
# G.0 scout (`backend/G_0_SCOUT_REPORT.md`) computed the tiling math:
#   ARCH-D (24x36 in) @ 250 DPI = 154.5 MB raw RGB; single 2x2 tile = 38.6 MB.
#   Letter (8.5x11 in) @ 250 DPI = 16.7 MB → under threshold, no tile needed.
# 250 DPI balances detail (callout precision for Stage 6 contour detection
# in G.6) against per-allocation memory cost. 5% overlap ensures content
# crossing tile boundaries appears in adjacent tiles.

PDF_TILE_DPI = 250
PDF_TILE_OVERLAP_PCT = 0.05
PDF_TILE_MEMORY_THRESHOLD_MB = 50.0
PDF_TILE_GRID = (2, 2)


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class PageMeta:
    """Metadata for a single PDF page."""
    page_number: int          # 0-indexed
    width_pts: float          # Page width in PDF points
    height_pts: float         # Page height in PDF points
    width_in: float           # Page width in inches
    height_in: float          # Page height in inches
    rotation: int             # Page rotation in degrees (0/90/180/270)


@dataclass
class TextBlock:
    """A block of text extracted from a page."""
    text: str
    x0: float   # Left edge (pts)
    y0: float   # Top edge (pts)
    x1: float   # Right edge (pts)
    y1: float   # Bottom edge (pts)
    page: int    # 0-indexed page number


@dataclass
class VectorPath:
    """A vector drawing element extracted from a page."""
    path_type: str            # "line", "rect", "curve", "quad"
    points: list              # List of (x, y) tuples in PDF points
    color: Optional[tuple] = None        # Stroke color (r, g, b) 0-1
    fill: Optional[tuple] = None         # Fill color (r, g, b) 0-1
    width: float = 1.0        # Stroke width in pts
    closed: bool = False       # Whether the path is closed
    page: int = 0
    dashes: str = ""           # Dash pattern string from PyMuPDF (empty = solid)

    @property
    def bbox_diag_pts(self) -> float:
        """Bounding box diagonal in PDF points — proxy for path length."""
        if not self.points:
            return 0.0
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]
        dx = max(xs) - min(xs)
        dy = max(ys) - min(ys)
        return (dx * dx + dy * dy) ** 0.5


@dataclass
class PDFDocument:
    """Represents an opened PDF with its pages and metadata."""
    path: str
    page_count: int
    pages: list = field(default_factory=list)   # List[PageMeta]
    _doc: object = field(default=None, repr=False)

    def close(self):
        if self._doc:
            self._doc.close()
            self._doc = None


# ---------------------------------------------------------------------------
# PDF Engine
# ---------------------------------------------------------------------------

class PDFEngine:
    """
    Core PDF engine wrapping PyMuPDF.

    Usage:
        engine = PDFEngine()
        doc = engine.open("plans.pdf")
        img = engine.render_page(doc, 0)           # PIL Image of page 0
        text = engine.extract_text(doc, 0)          # full text of page 0
        blocks = engine.extract_text_blocks(doc, 0) # positioned text blocks
        paths = engine.extract_vectors(doc, 0)      # vector drawing elements
        engine.close(doc)
    """

    def __init__(self, render_dpi: int = PDF_RENDER_DPI,
                 thumbnail_dpi: int = PDF_THUMBNAIL_DPI,
                 max_dimension: int = PDF_MAX_DIMENSION):
        self.render_dpi = render_dpi
        self.thumbnail_dpi = thumbnail_dpi
        self.max_dimension = max_dimension
        # Phase G.3: per-(doc, page, method) extraction cache. RAM-only,
        # instance-scoped. Key = (id(pdf_doc), page_num, method_name).
        # Purged on engine.close(pdf_doc).
        self._extract_cache: dict = {}

    # ------------------------------------------------------------------
    # Open / close
    # ------------------------------------------------------------------

    def open(self, pdf_path: str | Path) -> PDFDocument:
        """Open a PDF file and return a PDFDocument with page metadata."""
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        if not pdf_path.suffix.lower() == ".pdf":
            raise ValueError(f"Not a PDF file: {pdf_path}")

        doc = fitz.open(str(pdf_path))
        pages = []
        for i in range(doc.page_count):
            page = doc[i]
            rect = page.rect
            pages.append(PageMeta(
                page_number=i,
                width_pts=rect.width,
                height_pts=rect.height,
                width_in=rect.width / 72.0,
                height_in=rect.height / 72.0,
                rotation=page.rotation,
            ))

        return PDFDocument(
            path=str(pdf_path),
            page_count=doc.page_count,
            pages=pages,
            _doc=doc,
        )

    def close(self, pdf_doc: PDFDocument):
        """Close the PDF document and free resources.

        Phase G.3: purge any extraction-cache entries keyed on this doc.
        """
        doc_key = id(pdf_doc)
        self._extract_cache = {
            k: v for k, v in self._extract_cache.items() if k[0] != doc_key
        }
        pdf_doc.close()

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render_page(self, pdf_doc: PDFDocument, page_num: int,
                    dpi: Optional[int] = None) -> Image.Image:
        """
        Render a page to a PIL Image.

        Args:
            pdf_doc: An opened PDFDocument.
            page_num: 0-indexed page number.
            dpi: Override render DPI (defaults to self.render_dpi).

        Returns:
            PIL Image in RGB mode.
        """
        self._validate_page(pdf_doc, page_num)
        dpi = dpi or self.render_dpi
        page = pdf_doc._doc[page_num]

        # Calculate zoom factor from DPI (PDF base is 72 DPI)
        zoom = dpi / 72.0
        mat = fitz.Matrix(zoom, zoom)

        # Clamp to max dimension
        meta = pdf_doc.pages[page_num]
        max_side = max(meta.width_pts, meta.height_pts) * zoom
        if max_side > self.max_dimension:
            scale_down = self.max_dimension / max_side
            mat = fitz.Matrix(zoom * scale_down, zoom * scale_down)

        pix = page.get_pixmap(matrix=mat, alpha=False)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        return img.convert("RGB")

    def render_thumbnail(self, pdf_doc: PDFDocument,
                         page_num: int) -> Image.Image:
        """Render a small thumbnail of a page."""
        return self.render_page(pdf_doc, page_num, dpi=self.thumbnail_dpi)

    # ------------------------------------------------------------------
    # Phase G.5b — Tile rendering
    # ------------------------------------------------------------------

    def _estimate_render_memory_mb(self, page, dpi: int) -> float:
        """Estimate the raw-RGB memory footprint of rendering `page` at `dpi`.

        Formula: width_in × height_in × dpi² × 3 bytes / 1024² (RGB, no alpha).
        """
        width_in = page.rect.width / 72.0
        height_in = page.rect.height / 72.0
        bytes_total = width_in * height_in * (dpi ** 2) * 3
        return bytes_total / (1024 ** 2)

    def _compute_tile_rects(self, page, grid: tuple = PDF_TILE_GRID,
                            overlap_pct: float = PDF_TILE_OVERLAP_PCT) -> list:
        """Compute clip rectangles in PDF points for a tile grid with overlap.

        Returns row-major list of `fitz.Rect` objects. With grid=(2,2) and
        overlap_pct=0.05, returns 4 rects: TL, TR, BL, BR. Adjacent tiles
        share a 5%-of-page overlap band so content crossing tile boundaries
        appears in both tiles. Edge tiles extend exactly to the page edge.
        """
        cols, rows = grid
        page_w = page.rect.width
        page_h = page.rect.height
        overlap_w = page_w * overlap_pct
        overlap_h = page_h * overlap_pct
        # Base tile dimensions (without overlap)
        base_w = page_w / cols
        base_h = page_h / rows
        rects = []
        for ry in range(rows):
            for cx in range(cols):
                x0 = cx * base_w
                y0 = ry * base_h
                x1 = x0 + base_w
                y1 = y0 + base_h
                # Extend interior edges into the next tile by overlap band
                if cx < cols - 1:
                    x1 += overlap_w
                if ry < rows - 1:
                    y1 += overlap_h
                # Clamp to page
                x1 = min(x1, page_w)
                y1 = min(y1, page_h)
                rects.append(fitz.Rect(x0, y0, x1, y1))
        return rects

    def render_page_tiled(self, pdf_doc: PDFDocument, page_num: int,
                          dpi: int = PDF_TILE_DPI,
                          force_tiles: bool = False) -> list:
        """Render a page as one-or-more tiles, returning [(tile_rect, PIL.Image)].

        If the estimated full-page memory at `dpi` is at or below
        `PDF_TILE_MEMORY_THRESHOLD_MB` (default 50 MB) and `force_tiles` is
        False, returns a single-element list with the full page render —
        API uniformity for callers that want to iterate regardless of size.

        Otherwise returns a 2x2 grid of tiles with 5% overlap. Each tile's
        pixmap is freed before the next is allocated so peak memory is
        bounded by the per-tile size, not the full-page size.
        """
        self._validate_page(pdf_doc, page_num)
        page = pdf_doc._doc[page_num]
        full_mb = self._estimate_render_memory_mb(page, dpi)
        zoom = dpi / 72.0
        mat = fitz.Matrix(zoom, zoom)

        if full_mb <= PDF_TILE_MEMORY_THRESHOLD_MB and not force_tiles:
            pix = page.get_pixmap(matrix=mat, alpha=False)
            img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
            pix = None
            return [(page.rect, img)]

        tiles = []
        for tile_rect in self._compute_tile_rects(page):
            pix = page.get_pixmap(matrix=mat, clip=tile_rect, alpha=False)
            img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
            pix = None  # release pixmap before next allocation
            tiles.append((tile_rect, img))
        return tiles

    # ------------------------------------------------------------------
    # Text extraction
    # ------------------------------------------------------------------

    def extract_text(self, pdf_doc: PDFDocument, page_num: int) -> str:
        """Extract all text from a page as a single string.

        Phase G.3: result cached per (doc, page); repeat calls return the
        same string object, no re-extraction.
        """
        self._validate_page(pdf_doc, page_num)
        cache_key = (id(pdf_doc), page_num, "extract_text")
        cached = self._extract_cache.get(cache_key)
        if cached is not None:
            return cached
        page = pdf_doc._doc[page_num]
        result = page.get_text("text")
        self._extract_cache[cache_key] = result
        return result

    def extract_text_blocks(self, pdf_doc: PDFDocument,
                            page_num: int) -> list[TextBlock]:
        """
        Extract positioned text blocks from a page.

        Each block has text content and its bounding box in PDF points.
        Useful for locating dimensions, labels, and notes on plans.

        Phase G.3: result cached per (doc, page); repeat calls return the
        same list object, no re-extraction.
        """
        self._validate_page(pdf_doc, page_num)
        cache_key = (id(pdf_doc), page_num, "extract_text_blocks")
        cached = self._extract_cache.get(cache_key)
        if cached is not None:
            return cached
        page = pdf_doc._doc[page_num]
        blocks = page.get_text("blocks")
        result = []
        for b in blocks:
            # blocks format: (x0, y0, x1, y1, text, block_no, block_type)
            # block_type 0 = text, 1 = image
            if b[6] == 0:  # text block
                text = b[4].strip()
                if text:
                    result.append(TextBlock(
                        text=text,
                        x0=b[0], y0=b[1], x1=b[2], y1=b[3],
                        page=page_num,
                    ))
        self._extract_cache[cache_key] = result
        return result

    def search_text(self, pdf_doc: PDFDocument, query: str,
                    pages: Optional[list[int]] = None) -> list[TextBlock]:
        """
        Search for text across pages. Returns blocks containing the query.

        Args:
            pdf_doc: Opened PDF document.
            query: Text to search for (case-insensitive).
            pages: List of page numbers to search (default: all pages).

        Returns:
            List of TextBlock matches with page numbers.
        """
        if pages is None:
            pages = list(range(pdf_doc.page_count))

        query_lower = query.lower()
        results = []
        for pn in pages:
            self._validate_page(pdf_doc, pn)
            page = pdf_doc._doc[pn]
            # Use PyMuPDF's built-in search for bbox locations
            quads = page.search_for(query)
            for q in quads:
                rect = q.rect if hasattr(q, 'rect') else fitz.Rect(q)
                results.append(TextBlock(
                    text=query,
                    x0=rect.x0, y0=rect.y0,
                    x1=rect.x1, y1=rect.y1,
                    page=pn,
                ))
        return results

    def find_dimensions(self, pdf_doc: PDFDocument,
                        page_num: int) -> list[dict]:
        """
        Find architectural dimension strings on a page.

        Looks for patterns like: 45'-6", 12'-0", 120', 6"
        Returns list of {text, value_ft, x0, y0, x1, y1}.
        """
        blocks = self.extract_text_blocks(pdf_doc, page_num)
        dims = []
        for block in blocks:
            parsed = _parse_dimension_to_feet(block.text)
            if parsed is not None:
                dims.append({
                    "text": block.text.strip(),
                    "value_ft": parsed,
                    "x0": block.x0, "y0": block.y0,
                    "x1": block.x1, "y1": block.y1,
                })
        return dims

    # ------------------------------------------------------------------
    # Vector path extraction
    # ------------------------------------------------------------------

    def extract_vectors(self, pdf_doc: PDFDocument,
                        page_num: int) -> list[VectorPath]:
        """
        Extract vector drawing paths from a page.

        Returns lines, rectangles, curves, and quads with their
        coordinates, colors, and stroke widths. These are the raw
        CAD/drawing elements — essential for detecting building outlines,
        walls, and symbols.
        """
        self._validate_page(pdf_doc, page_num)
        page = pdf_doc._doc[page_num]
        paths = []

        for drawing in page.get_drawings():
            items = drawing.get("items", [])
            color = drawing.get("color")
            fill_color = drawing.get("fill")
            width = drawing.get("width", 1.0)
            closepath = drawing.get("closePath", False)
            dashes = drawing.get("dashes", "")

            # Normalize color tuples
            stroke = tuple(color) if color else None
            fill_c = tuple(fill_color) if fill_color else None

            all_points = []
            path_type = "line"

            for item in items:
                kind = item[0]  # "l" = line, "re" = rect, "c" = curve, "qu" = quad
                if kind == "l":
                    # Line: item = ("l", Point, Point)
                    p1, p2 = item[1], item[2]
                    all_points.append((p1.x, p1.y))
                    all_points.append((p2.x, p2.y))
                    path_type = "line"

                elif kind == "re":
                    # Rectangle: item = ("re", Rect)
                    r = item[1]
                    all_points = [
                        (r.x0, r.y0), (r.x1, r.y0),
                        (r.x1, r.y1), (r.x0, r.y1),
                    ]
                    path_type = "rect"
                    closepath = True

                elif kind == "c":
                    # Bezier curve: item = ("c", P1, P2, P3, P4)
                    for pt in item[1:]:
                        all_points.append((pt.x, pt.y))
                    path_type = "curve"

                elif kind == "qu":
                    # Quad: item = ("qu", Quad)
                    q = item[1]
                    all_points = [
                        (q.ul.x, q.ul.y), (q.ur.x, q.ur.y),
                        (q.lr.x, q.lr.y), (q.ll.x, q.ll.y),
                    ]
                    path_type = "quad"
                    closepath = True

            if all_points:
                paths.append(VectorPath(
                    path_type=path_type,
                    points=all_points,
                    color=stroke,
                    fill=fill_c,
                    width=width,
                    closed=closepath,
                    page=page_num,
                    dashes=str(dashes) if dashes else "",
                ))

        return paths

    def extract_closed_polygons(self, pdf_doc: PDFDocument,
                                page_num: int) -> list[VectorPath]:
        """
        Extract only closed vector paths (potential building outlines).

        Filters extract_vectors() to return only closed paths with 3+ points.
        """
        all_paths = self.extract_vectors(pdf_doc, page_num)
        return [
            p for p in all_paths
            if p.closed and len(p.points) >= 3
        ]

    # ------------------------------------------------------------------
    # Page metadata helpers
    # ------------------------------------------------------------------

    def get_page_meta(self, pdf_doc: PDFDocument,
                      page_num: int) -> PageMeta:
        """Get metadata for a specific page."""
        self._validate_page(pdf_doc, page_num)
        return pdf_doc.pages[page_num]

    def get_all_page_metas(self, pdf_doc: PDFDocument) -> list[PageMeta]:
        """Get metadata for all pages."""
        return pdf_doc.pages

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _validate_page(self, pdf_doc: PDFDocument, page_num: int):
        if pdf_doc._doc is None:
            raise RuntimeError("PDF document is closed")
        if not 0 <= page_num < pdf_doc.page_count:
            raise IndexError(
                f"Page {page_num} out of range (0-{pdf_doc.page_count - 1})"
            )


# ---------------------------------------------------------------------------
# Dimension parser (proven from predecessor project)
# ---------------------------------------------------------------------------

_DIM_PATTERN = re.compile(r"""
    (\d+)           # feet
    \s*['\u2032]    # foot mark
    \s*-?\s*        # optional dash
    (\d+)           # inches
    (?:\s+(\d+)/(\d+))?  # optional fraction
    \s*["\u2033\u201D]?  # optional inch mark
""", re.VERBOSE)

_DIM_FEET_ONLY = re.compile(r'(?<![.\d])(\d+)\s*[\'\u2032]\s*(?:-?\s*0\s*["\u2033\u201D]?)?$')
_DIM_DECIMAL = re.compile(r'(?<!\d)(\d+\.?\d*)\s*([\'\"\u2032\u2033])')


def _parse_dimension_to_feet(text: str) -> Optional[float]:
    """
    Parse architectural dimension strings to feet.

    Examples: "45'-6\"" → 45.5, "12'-0\"" → 12.0, "6\"" → 0.5
    Returns None if no dimension pattern found.
    """
    if not text or not isinstance(text, str):
        return None
    text = text.strip()

    m = _DIM_PATTERN.search(text)
    if m:
        feet = int(m.group(1))
        inches = int(m.group(2))
        frac = 0.0
        if m.group(3) and m.group(4):
            denom = int(m.group(4))
            if denom > 0:
                frac = int(m.group(3)) / denom
        return feet + (inches + frac) / 12.0

    m = _DIM_FEET_ONLY.search(text)
    if m:
        return float(m.group(1))

    m = _DIM_DECIMAL.search(text)
    if m:
        val = float(m.group(1))
        unit = m.group(2)
        if unit in ('"', '\u2033', '\u201D'):
            return val / 12.0
        return val

    return None


# ---------------------------------------------------------------------------
# Stated area parser
# ---------------------------------------------------------------------------

_STATED_AREA_PATTERN = re.compile(
    r'(\d[\d,]+)\s*SQ\.?\s*FT', re.IGNORECASE
)


def find_stated_areas(text: str) -> list[float]:
    """
    Find stated area values in text (e.g. "5746 SQ FT", "1,111 SQ FT.").

    Returns list of area values in square feet, largest first.
    """
    if not text:
        return []
    matches = _STATED_AREA_PATTERN.findall(text)
    areas = []
    for m in matches:
        val = float(m.replace(",", ""))
        if val >= 500:  # Ignore tiny values that aren't building areas
            areas.append(val)
    areas.sort(reverse=True)
    return areas


# ---------------------------------------------------------------------------
# Scale parser (proven from predecessor project)
# ---------------------------------------------------------------------------

_SCALE_PATTERN = re.compile(r"""
    (\d+)\s*/\s*(\d+)   # fraction: 1/4, 1/8, 3/16
    \s*["\u2033\u201D]?  # inch mark
    \s*=\s*              # equals
    1\s*['\u2032]        # 1 foot
""", re.VERBOSE)


def parse_scale_to_ft_per_inch(text: str) -> Optional[float]:
    """
    Parse architectural scale strings to feet-per-inch.

    Example: '3/16" = 1\'-0"' → 5.333
    """
    if not text:
        return None
    m = _SCALE_PATTERN.search(text.strip())
    if m:
        num, den = int(m.group(1)), int(m.group(2))
        if num > 0 and den > 0:
            return den / num
    return None


def find_roof_plan_scale(text_blocks) -> Optional[float]:
    """
    Find the architectural scale associated with the ROOF PLAN view.

    Strategy:
      1. Search text blocks for ones containing BOTH a scale pattern
         AND "ROOF PLAN" — these are title block labels like
         "Scale= 1/4\" = 1'-0\"  ROOF PLAN".
      2. If not found in the same block, search for scale blocks within
         ~2 inches (144 pts) of a "ROOF PLAN" label block.
      3. If no ROOF PLAN association found, return None — don't trust
         unassociated scale strings (they may be detail callouts).

    Args:
        text_blocks: list of TextBlock from extract_text_blocks()

    Returns:
        ft_per_inch if a ROOF PLAN scale is found, else None.
    """
    if not text_blocks:
        return None

    PTS_PER_INCH = 72
    PROXIMITY_PTS = 2.5 * PTS_PER_INCH  # ~2.5 inches

    # Collect blocks with scale patterns and blocks with "ROOF PLAN"
    scale_blocks = []  # (block, fpi)
    roof_plan_blocks = []

    for block in text_blocks:
        upper = block.text.upper()
        m = _SCALE_PATTERN.search(block.text)
        if m:
            num, den = int(m.group(1)), int(m.group(2))
            if num > 0 and den > 0:
                fpi = den / num
                scale_blocks.append((block, fpi))

        if "ROOF PLAN" in upper:
            roof_plan_blocks.append(block)

    # Strategy 1: scale + "ROOF PLAN" in the same text block
    for block, fpi in scale_blocks:
        if "ROOF PLAN" in block.text.upper():
            return fpi

    # Strategy 2: scale block near a "ROOF PLAN" block
    for sb, fpi in scale_blocks:
        sb_cx = (sb.x0 + sb.x1) / 2
        sb_cy = (sb.y0 + sb.y1) / 2
        for rpb in roof_plan_blocks:
            rpb_cx = (rpb.x0 + rpb.x1) / 2
            rpb_cy = (rpb.y0 + rpb.y1) / 2
            dist = ((sb_cx - rpb_cx) ** 2 + (sb_cy - rpb_cy) ** 2) ** 0.5
            if dist < PROXIMITY_PTS:
                return fpi

    return None


def find_scale_from_any_page(engine, pdf_doc) -> list[dict]:
    """
    Search ALL pages of a PDF for scale labels associated with ROOF PLAN.

    Returns list of {page, fpi, scale_str, title_text} for each
    roof-plan-associated scale found on any page.

    Useful as fallback when the current page has no text scale.
    For single-page PDFs, this returns the same as find_roof_plan_scale().
    """
    results = []
    _BUILDING_FPIS = {1, 1.333, 2, 2.667, 4, 5.333, 8, 10.667}

    for pg in range(pdf_doc.page_count):
        text_blocks = engine.extract_text_blocks(pdf_doc, pg)

        # Collect scale blocks and ROOF PLAN blocks on this page
        scale_blocks = []
        roof_plan_blocks = []
        for block in text_blocks:
            m = _SCALE_PATTERN.search(block.text)
            if m:
                num, den = int(m.group(1)), int(m.group(2))
                if num > 0 and den > 0:
                    fpi = den / num
                    scale_blocks.append((block, fpi, m.group(0).strip()))
            if "ROOF PLAN" in block.text.upper():
                roof_plan_blocks.append(block)

        if not scale_blocks or not roof_plan_blocks:
            continue

        PTS_PER_INCH = 72
        PROXIMITY_PTS = 3 * PTS_PER_INCH

        # Same block match
        for block, fpi, scale_str in scale_blocks:
            if "ROOF PLAN" in block.text.upper():
                results.append({
                    "page": pg,
                    "fpi": fpi,
                    "scale_str": scale_str,
                    "title_text": block.text.strip()[:60],
                })

        # Proximity match
        for sb, fpi, scale_str in scale_blocks:
            sb_cx = (sb.x0 + sb.x1) / 2
            sb_cy = (sb.y0 + sb.y1) / 2
            for rpb in roof_plan_blocks:
                rpb_cx = (rpb.x0 + rpb.x1) / 2
                rpb_cy = (rpb.y0 + rpb.y1) / 2
                dist = ((sb_cx - rpb_cx) ** 2 + (sb_cy - rpb_cy) ** 2) ** 0.5
                if dist < PROXIMITY_PTS:
                    # Avoid duplicates from same-block match
                    already = any(r["page"] == pg and abs(r["fpi"] - fpi) < 0.01
                                  for r in results)
                    if not already:
                        results.append({
                            "page": pg,
                            "fpi": fpi,
                            "scale_str": scale_str,
                            "title_text": rpb.text.strip()[:60],
                        })

    # Filter to building scales only
    results = [r for r in results
               if any(abs(r["fpi"] - bs) < 0.01 for bs in _BUILDING_FPIS)]

    return results


