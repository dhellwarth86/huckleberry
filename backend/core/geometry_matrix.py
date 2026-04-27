"""
TracePoint Geometry Matrix Engine — OpenCV + Shapely.

Handles:
  - Rasterized page → contour detection (OpenCV)
  - Contour → polygon conversion (Shapely)
  - Area and perimeter calculation in real-world units (sq ft, linear ft)
  - Building outline detection (largest contour heuristic)
  - Contour filtering, simplification, and classification
  - Polygon operations (union, intersection, subtraction)
  - Coordinate conversion between pixel, percentage, and real-world units

Decision tree for building outline (from CLAUDE.md):
  1. OpenCV contour — rasterize page, find largest contour, Shapely area
  2. Text search — find "ROOF AREA: X,XXX SF" (handled by pdf_engine)
  3. Dimension calc — two largest dims, multiply (handled by pdf_engine)
  4. Shape fallback — largest closed polygon from PDF vectors
  5. Claude fallback — only if all deterministic methods fail
"""

from dataclasses import dataclass, field
from typing import Optional

import cv2
import numpy as np
from PIL import Image
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from shapely.validation import make_valid

from core.config import ARCH_SCALES, CONTOUR_APPROX_EPSILON, CONTOUR_MIN_AREA_RATIO


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class DetectedContour:
    """A contour detected by OpenCV, converted to useful formats."""
    points_px: list              # [(x, y), ...] in pixel coordinates
    points_pct: list             # [(x%, y%), ...] in percentage coordinates
    area_px: float               # Area in pixels²
    perimeter_px: float          # Perimeter in pixels
    area_sqft: Optional[float] = None     # Area in sq ft (if scale known)
    perimeter_ft: Optional[float] = None  # Perimeter in ft (if scale known)
    bbox: tuple = ()             # (x, y, w, h) bounding box in pixels
    vertex_count: int = 0        # Number of vertices after simplification
    is_closed: bool = True
    hierarchy_level: int = 0     # 0 = outermost, 1 = hole, 2 = island, etc.


@dataclass
class GeometryResult:
    """Result of geometry analysis on a page."""
    contours: list = field(default_factory=list)          # List[DetectedContour]
    building_outline: Optional[DetectedContour] = None    # Largest qualifying contour
    area_sqft: Optional[float] = None                     # Building area in sq ft
    perimeter_ft: Optional[float] = None                  # Building perimeter in ft
    image_width_px: int = 0
    image_height_px: int = 0
    scale_ft_per_inch: Optional[float] = None
    dpi: int = 150


# ---------------------------------------------------------------------------
# Geometry Matrix Engine
# ---------------------------------------------------------------------------

class GeometryMatrix:
    """
    Core geometry engine using OpenCV for contour detection and
    Shapely for polygon math.

    Usage:
        gm = GeometryMatrix()
        result = gm.detect_contours(pil_image, page_meta, ft_per_inch=4.0)
        outline = result.building_outline
        print(f"Area: {outline.area_sqft} sqft")
        print(f"Perimeter: {outline.perimeter_ft} ft")
    """

    def __init__(self,
                 min_area_ratio: float = CONTOUR_MIN_AREA_RATIO,
                 approx_epsilon: float = CONTOUR_APPROX_EPSILON):
        self.min_area_ratio = min_area_ratio
        self.approx_epsilon = approx_epsilon

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def detect_contours(self, image: Image.Image,
                        page_meta=None,
                        ft_per_inch: Optional[float] = None,
                        dpi: int = 150) -> GeometryResult:
        """
        Detect contours in a rendered plan page.

        Args:
            image: PIL Image of the rendered page (from PDFEngine.render_page).
            page_meta: PageMeta from pdf_engine (for coordinate conversion).
            ft_per_inch: Scale factor (feet per inch on paper). If provided,
                         areas and perimeters are converted to real-world units.
            dpi: DPI the image was rendered at (for inch conversion).

        Returns:
            GeometryResult with all detected contours and the building outline.
        """
        # Convert PIL → OpenCV
        img_array = np.array(image)
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array

        h_px, w_px = gray.shape[:2]

        # Preprocess for contour detection
        binary = self._preprocess(gray)

        # Find contours with hierarchy
        contours_cv, hierarchy = cv2.findContours(
            binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

        if hierarchy is None:
            return GeometryResult(image_width_px=w_px, image_height_px=h_px,
                                  scale_ft_per_inch=ft_per_inch, dpi=dpi)

        hierarchy = hierarchy[0]  # Shape: (N, 4) — [next, prev, child, parent]
        page_area_px = w_px * h_px
        min_area = page_area_px * self.min_area_ratio

        # Pixels per inch at the rendering DPI
        px_per_inch = dpi

        detected = []
        for i, cnt in enumerate(contours_cv):
            area_px = cv2.contourArea(cnt)
            if area_px < min_area:
                continue

            # Simplify contour (Douglas-Peucker)
            peri = cv2.arcLength(cnt, True)
            epsilon = self.approx_epsilon * peri
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            # Extract points
            points_px = [(int(p[0][0]), int(p[0][1])) for p in approx]
            points_pct = [
                (p[0] / w_px * 100, p[1] / h_px * 100)
                for p in points_px
            ]

            # Bounding box
            x, y, w, h = cv2.boundingRect(approx)

            # Hierarchy level
            level = 0
            parent = hierarchy[i][3]
            while parent >= 0:
                level += 1
                parent = hierarchy[parent][3]

            dc = DetectedContour(
                points_px=points_px,
                points_pct=points_pct,
                area_px=area_px,
                perimeter_px=peri,
                bbox=(x, y, w, h),
                vertex_count=len(points_px),
                is_closed=True,
                hierarchy_level=level,
            )

            # Convert to real-world units if scale is known
            if ft_per_inch is not None:
                dc.area_sqft = self._px_area_to_sqft(
                    area_px, px_per_inch, ft_per_inch
                )
                dc.perimeter_ft = self._px_length_to_ft(
                    peri, px_per_inch, ft_per_inch
                )

            detected.append(dc)

        # Sort by area descending
        detected.sort(key=lambda c: c.area_px, reverse=True)

        # Find building outline — largest contour that isn't the page border.
        # The page border/title block hugs the edges (bbox covers >85% of
        # both width and height). Real building outlines don't.
        building = None
        for c in detected:
            bx, by, bw, bh = c.bbox
            width_ratio = bw / w_px
            height_ratio = bh / h_px
            if width_ratio > 0.85 and height_ratio > 0.85:
                continue  # Skip — this is the sheet border
            building = c
            break

        result = GeometryResult(
            contours=detected,
            building_outline=building,
            image_width_px=w_px,
            image_height_px=h_px,
            scale_ft_per_inch=ft_per_inch,
            dpi=dpi,
        )
        if building:
            result.area_sqft = building.area_sqft
            result.perimeter_ft = building.perimeter_ft

        return result

    # ------------------------------------------------------------------
    # Shapely polygon operations
    # ------------------------------------------------------------------

    def contour_to_polygon(self, contour: DetectedContour) -> Optional[Polygon]:
        """Convert a DetectedContour to a Shapely Polygon."""
        if len(contour.points_px) < 3:
            return None
        poly = Polygon(contour.points_px)
        if not poly.is_valid:
            poly = make_valid(poly)
            if isinstance(poly, MultiPolygon):
                poly = max(poly.geoms, key=lambda g: g.area)
        return poly if isinstance(poly, Polygon) else None

    def polygon_area_sqft(self, polygon: Polygon,
                          px_per_inch: float,
                          ft_per_inch: float) -> float:
        """Calculate area of a Shapely polygon in square feet."""
        area_px = polygon.area
        return self._px_area_to_sqft(area_px, px_per_inch, ft_per_inch)

    def polygon_perimeter_ft(self, polygon: Polygon,
                             px_per_inch: float,
                             ft_per_inch: float) -> float:
        """Calculate perimeter of a Shapely polygon in linear feet."""
        peri_px = polygon.length
        return self._px_length_to_ft(peri_px, px_per_inch, ft_per_inch)

    def subtract_polygons(self, outer: Polygon,
                          holes: list[Polygon]) -> Polygon:
        """
        Subtract hole polygons from an outer polygon.

        Used for: roof area minus penetrations, wall area minus openings.
        """
        result = outer
        for hole in holes:
            if hole.is_valid and result.intersects(hole):
                result = result.difference(hole)
        if isinstance(result, MultiPolygon):
            result = max(result.geoms, key=lambda g: g.area)
        return result

    def union_polygons(self, polygons: list[Polygon]) -> Polygon:
        """Merge multiple polygons into one (e.g., multi-section roofs)."""
        valid = [p for p in polygons if p.is_valid]
        if not valid:
            return Polygon()
        result = unary_union(valid)
        if isinstance(result, MultiPolygon):
            result = max(result.geoms, key=lambda g: g.area)
        return result

    # ------------------------------------------------------------------
    # Vector polygon clustering + scale scoring
    # ------------------------------------------------------------------

    def cluster_and_union_polygons(self, vector_paths, page_meta,
                                   min_area_sqin=0.5, gap_inches=0.5):
        """
        Cluster raw vector polygons by proximity, union each cluster,
        and score against architectural scales to find building outlines.

        Handles nearly-closed paths (first≈last point) that PyMuPDF
        doesn't flag as closePath — common in multi-section buildings.

        Args:
            vector_paths: list of VectorPath from pdf_engine.extract_vectors()
            page_meta: PageMeta for chrome filtering
            min_area_sqin: min polygon area on paper (square inches)
            gap_inches: max gap between bbox edges to cluster (inches)

        Returns:
            list of dicts sorted by score (best first), each with:
            polygon, area_sqft, perimeter_ft, scale_label, ft_per_inch,
            n_polygons, area_sqin
        """
        PTS = 72  # PDF points per inch
        gap_pts = gap_inches * PTS

        # --- Step 1: Convert paths to Shapely polygons ---
        polys = []
        for vp in vector_paths:
            pts = vp.points
            if len(pts) < 3:
                continue

            # Dedupe consecutive points (line segments share endpoints)
            unique = [pts[0]]
            for pt in pts[1:]:
                if abs(pt[0] - unique[-1][0]) > 0.01 or \
                   abs(pt[1] - unique[-1][1]) > 0.01:
                    unique.append(pt)
            if len(unique) < 3:
                continue

            # Accept closed paths OR nearly-closed (gap < 2pt ≈ 0.03in)
            gap = ((unique[0][0] - unique[-1][0]) ** 2 +
                   (unique[0][1] - unique[-1][1]) ** 2) ** 0.5
            if not vp.closed and gap > 2.0:
                continue

            try:
                poly = Polygon(unique)
                if not poly.is_valid:
                    poly = make_valid(poly)
                if isinstance(poly, MultiPolygon):
                    poly = max(poly.geoms, key=lambda g: g.area)
                if not isinstance(poly, Polygon) or poly.area == 0:
                    continue
                area_sqin = poly.area / (PTS ** 2)
                if area_sqin < min_area_sqin:
                    continue
                # Chrome filter
                b = poly.bounds
                w_in = (b[2] - b[0]) / PTS
                h_in = (b[3] - b[1]) / PTS
                if w_in / page_meta.width_in > 0.85 and \
                   h_in / page_meta.height_in > 0.85:
                    continue
                polys.append(poly)
            except Exception:
                continue

        if not polys:
            return []

        # --- Step 2: Cluster by bbox proximity (union-find) ---
        parent = list(range(len(polys)))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def merge(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        for i in range(len(polys)):
            bi = polys[i].bounds
            for j in range(i + 1, len(polys)):
                bj = polys[j].bounds
                dx = max(0, max(bi[0], bj[0]) - min(bi[2], bj[2]))
                dy = max(0, max(bi[1], bj[1]) - min(bi[3], bj[3]))
                if (dx * dx + dy * dy) ** 0.5 < gap_pts:
                    merge(i, j)

        from collections import defaultdict
        groups = defaultdict(list)
        for i in range(len(polys)):
            groups[find(i)].append(polys[i])

        # --- Step 3: Union each cluster, score against scales ---
        clusters = []
        for members in groups.values():
            merged = unary_union(members)
            if isinstance(merged, MultiPolygon):
                merged = max(merged.geoms, key=lambda g: g.area)
            area_sqin = merged.area / (PTS ** 2)
            if area_sqin < min_area_sqin:
                continue
            clusters.append((merged, area_sqin, len(members)))

        # Sort clusters largest first
        clusters.sort(key=lambda c: -c[1])

        # Also try pairs of the top clusters (multi-section buildings)
        combos = [(c[0], c[1], c[2]) for c in clusters]
        for i in range(min(len(clusters), 4)):
            for j in range(i + 1, min(len(clusters), 4)):
                pair = unary_union([clusters[i][0], clusters[j][0]])
                if isinstance(pair, MultiPolygon):
                    pair = max(pair.geoms, key=lambda g: g.area)
                area = pair.area / (PTS ** 2)
                n = clusters[i][2] + clusters[j][2]
                combos.append((pair, area, n))

        # Score each combo × scale
        # Building plan scales (used for floor/roof plans) vs site plan scales
        import math
        # Common building plan scales get bonus.
        # 1"=10' and 1"=16' are used for both building and site — neutral.
        _BUILDING_SCALES = {1, 1.333, 2, 2.667, 4, 5.333, 8, 10.667}
        _SITE_SCALES = {20, 30, 40, 50, 100}

        results = []
        for poly, area_sqin, n_polys in combos:
            perim_in = poly.length / PTS
            clean_perim_pts = GeometryMatrix.compute_clean_perimeter(poly)
            clean_perim_in = clean_perim_pts / PTS
            for scale in ARCH_SCALES:
                fpi = scale["ft_per_inch"]
                area_sf = area_sqin * fpi ** 2
                if area_sf < 400 or area_sf > 60000:
                    continue

                # Score: prefer typical commercial building areas at building scales
                # Log-distance from 3000 SF (center of QSR/retail/small commercial)
                area_score = -abs(math.log10(area_sf) - math.log10(3000))
                # Building scale strong bonus, site scale penalty
                if fpi in _BUILDING_SCALES:
                    scale_score = 1.0
                elif fpi in _SITE_SCALES:
                    scale_score = -1.0
                else:
                    scale_score = 0.0
                # Larger polygon area on paper = more likely actual building
                size_score = math.log10(max(area_sqin, 0.1))
                score = area_score + scale_score * 0.8 + size_score * 0.2

                results.append({
                    "polygon": poly,
                    "area_sqft": round(area_sf, 1),
                    "perimeter_ft": round(perim_in * fpi, 1),
                    "perimeter_ft_clean": round(clean_perim_in * fpi, 1),
                    "scale_label": scale["label"],
                    "ft_per_inch": fpi,
                    "n_polygons": n_polys,
                    "area_sqin": round(area_sqin, 2),
                    "_score": round(score, 3),
                })

        results.sort(key=lambda r: -r["_score"])
        return results

    # ------------------------------------------------------------------
    # Dimension-based area estimation (fallback)
    # ------------------------------------------------------------------

    @staticmethod
    def find_area_from_dimensions(dimensions, page_meta=None, ft_per_inch=None):
        """
        Estimate building area from dimension strings when no vector
        polygons are available. Multiplies the largest orthogonal
        dimensions found in the text layer.

        Args:
            dimensions: list of dicts from PDFEngine.find_dimensions()
                        Each has: text, value_ft, x0, y0, x1, y1
            page_meta: PageMeta (for page size context)
            ft_per_inch: scale factor (for page-area reasonableness check)

        Returns:
            dict with area_sqft, dim1_ft, dim2_ft, source="dimension_calc"
            or None if insufficient dimensions.
        """
        if not dimensions:
            return None

        # Filter to plausible building dimensions (20-500 ft)
        filtered = []
        for d in dimensions:
            if d["value_ft"] < 20 or d["value_ft"] > 500:
                continue
            # Skip elevation markers (T.O. WALL, T.O. PARAPET, etc.)
            text_upper = d["text"].upper()
            if "T.O." in text_upper or "TOP OF" in text_upper:
                continue
            filtered.append(d)

        if len(filtered) < 2:
            return None

        # Classify orientation by bbox aspect ratio
        h_dims = []  # horizontal
        v_dims = []  # vertical
        for d in filtered:
            w = d["x1"] - d["x0"]
            h = d["y1"] - d["y0"]
            if w > h * 1.5:
                h_dims.append(d)
            elif h > w * 1.5:
                v_dims.append(d)
            # Ambiguous → skip

        # Need at least one from each orientation
        if not h_dims or not v_dims:
            # Fall back to two largest overall if orientation fails
            by_size = sorted(filtered, key=lambda d: -d["value_ft"])
            if len(by_size) >= 2:
                area = by_size[0]["value_ft"] * by_size[1]["value_ft"]
                return {
                    "area_sqft": round(area, 1),
                    "dim1_ft": by_size[0]["value_ft"],
                    "dim2_ft": by_size[1]["value_ft"],
                    "perimeter_ft": round(2 * (by_size[0]["value_ft"] + by_size[1]["value_ft"]), 1),
                    "source": "dimension_calc",
                }
            return None

        # Deduplicate within each group (values within 5% → keep largest)
        def dedup(dims):
            sorted_dims = sorted(dims, key=lambda d: -d["value_ft"])
            result = []
            for d in sorted_dims:
                if not any(abs(d["value_ft"] - r["value_ft"]) / r["value_ft"] < 0.05
                           for r in result):
                    result.append(d)
            return result

        h_dims = dedup(h_dims)
        v_dims = dedup(v_dims)

        # Sort by value descending
        h_dims.sort(key=lambda d: -d["value_ft"])
        v_dims.sort(key=lambda d: -d["value_ft"])

        # Collect all plausible (H, V) pairs, sorted by area descending
        pairs = []
        for hd in h_dims[:5]:
            for vd in v_dims[:5]:
                area = hd["value_ft"] * vd["value_ft"]
                if area < 500 or area > 60000:
                    continue
                pairs.append((hd, vd, area))

        if not pairs:
            area = h_dims[0]["value_ft"] * v_dims[0]["value_ft"]
            return {
                "area_sqft": round(area, 1),
                "dim1_ft": h_dims[0]["value_ft"],
                "dim2_ft": v_dims[0]["value_ft"],
                "perimeter_ft": round(2 * (h_dims[0]["value_ft"] + v_dims[0]["value_ft"]), 1),
                "source": "dimension_calc",
            }

        # Prioritize the largest H dim, stepping down V dims until
        # area ≤ 10,000 SF. This avoids bounding-box overshoot on
        # L-shaped buildings while keeping the primary building dimension.
        best = None
        for hd in h_dims[:5]:
            for vd in v_dims[:5]:
                area = hd["value_ft"] * vd["value_ft"]
                if area < 500 or area > 60000:
                    continue
                if area <= 10000:
                    best = (hd, vd, area)
                    break
            if best:
                break

        # Fall back to largest pair overall if nothing under 10,000
        if not best:
            best = max(pairs, key=lambda p: p[2]) if pairs else pairs[0]

        return {
            "area_sqft": round(best[2], 1),
            "dim1_ft": best[0]["value_ft"],
            "dim2_ft": best[1]["value_ft"],
            "perimeter_ft": round(2 * (best[0]["value_ft"] + best[1]["value_ft"]), 1),
            "source": "dimension_calc",
        }

    # ------------------------------------------------------------------
    # Dimension-string scale validation
    # ------------------------------------------------------------------

    @staticmethod
    def validate_scale_from_dimensions(polygon, dimensions, candidates):
        """
        Cross-check a polygon's bounding box against text dimension strings
        to determine the correct architectural scale independently of scoring.

        For each building scale, converts the polygon bbox to real-world feet
        and checks how many dimension strings match (within 15%).

        Args:
            polygon: Shapely Polygon (the winning polygon from clustering)
            dimensions: list of dicts from PDFEngine.find_dimensions()
                        Each has: text, value_ft, x0, y0, x1, y1
            candidates: full candidate list from cluster_and_union_polygons()
                        (to find best candidate at the validated scale)

        Returns:
            dict with ft_per_inch, match_count, matches (detail list)
            or None if no dimension matches found.
        """
        if not dimensions or polygon is None:
            return None

        PTS = 72  # PDF points per inch

        # Filter dimensions to plausible building sizes (10-500 ft)
        valid_dims = []
        for d in dimensions:
            if d["value_ft"] < 10 or d["value_ft"] > 500:
                continue
            text_upper = d["text"].upper()
            if "T.O." in text_upper or "TOP OF" in text_upper:
                continue
            valid_dims.append(d["value_ft"])

        if not valid_dims:
            return None

        # Polygon bounding box in inches
        bounds = polygon.bounds  # (minx, miny, maxx, maxy) in PDF points
        bbox_w_in = (bounds[2] - bounds[0]) / PTS
        bbox_h_in = (bounds[3] - bounds[1]) / PTS

        # Building scales only (site scales produce implausibly large buildings)
        _BUILDING_FPIS = [1, 1.333, 2, 2.667, 4, 5.333, 8, 10.667]

        best_scale = None
        best_count = 0
        best_matches = []

        for fpi in _BUILDING_FPIS:
            bbox_w_ft = bbox_w_in * fpi
            bbox_h_ft = bbox_h_in * fpi

            matches = []
            for dim_ft in valid_dims:
                # Check if dimension matches bbox width or height (within 15%)
                w_err = abs(dim_ft - bbox_w_ft) / dim_ft if dim_ft > 0 else 999
                h_err = abs(dim_ft - bbox_h_ft) / dim_ft if dim_ft > 0 else 999
                if w_err <= 0.15:
                    matches.append({"dim_ft": dim_ft, "axis": "width",
                                    "bbox_ft": round(bbox_w_ft, 1), "error": round(w_err, 3)})
                elif h_err <= 0.15:
                    matches.append({"dim_ft": dim_ft, "axis": "height",
                                    "bbox_ft": round(bbox_h_ft, 1), "error": round(h_err, 3)})

            if len(matches) > best_count:
                best_count = len(matches)
                best_scale = fpi
                best_matches = matches

        if best_count == 0:
            return None

        return {
            "ft_per_inch": best_scale,
            "match_count": best_count,
            "matches": best_matches,
        }

    # ------------------------------------------------------------------
    # Confidence scoring
    # ------------------------------------------------------------------

    @staticmethod
    def compute_confidence(candidates):
        """Compute confidence based on score gap between best and second-best at a different scale.

        Returns "high" if gap > 0.5, "medium" if > 0.2, "low" otherwise.
        """
        if not candidates or len(candidates) < 2:
            return "high" if candidates else "low"

        best = candidates[0]
        best_fpi = best["ft_per_inch"]

        # Find best candidate at a DIFFERENT scale
        second_best = None
        for c in candidates[1:]:
            if abs(c["ft_per_inch"] - best_fpi) > 0.01:
                second_best = c
                break

        if second_best is None:
            return "high"  # Only one viable scale

        gap = best["_score"] - second_best["_score"]
        if gap > 0.5:
            return "high"
        elif gap > 0.2:
            return "medium"
        else:
            return "low"

    # ------------------------------------------------------------------
    # Perimeter cleanup
    # ------------------------------------------------------------------

    @staticmethod
    def compute_clean_perimeter(polygon, tolerance=2.0):
        """Get perimeter from simplified exterior ring only.

        Drops internal edges and micro-jogs from union artifacts.
        tolerance is in PDF points (2.0 pt ~ 0.028 inches).
        """
        exterior = polygon.exterior
        simplified = exterior.simplify(tolerance, preserve_topology=True)
        return simplified.length

    # ------------------------------------------------------------------
    # Coordinate conversions
    # ------------------------------------------------------------------

    def px_to_pct(self, x_px: float, y_px: float,
                  img_width: int, img_height: int) -> tuple[float, float]:
        """Convert pixel coordinates to percentage coordinates (0-100)."""
        return (x_px / img_width * 100, y_px / img_height * 100)

    def pct_to_px(self, x_pct: float, y_pct: float,
                  img_width: int, img_height: int) -> tuple[int, int]:
        """Convert percentage coordinates to pixel coordinates."""
        return (int(x_pct / 100 * img_width), int(y_pct / 100 * img_height))

    def px_to_feet(self, length_px: float, px_per_inch: float,
                   ft_per_inch: float) -> float:
        """Convert a pixel length to feet."""
        return self._px_length_to_ft(length_px, px_per_inch, ft_per_inch)

    def feet_to_px(self, length_ft: float, px_per_inch: float,
                   ft_per_inch: float) -> float:
        """Convert a length in feet to pixels."""
        inches = length_ft / ft_per_inch
        return inches * px_per_inch

    def measure_line_ft(self, x1_pct: float, y1_pct: float,
                        x2_pct: float, y2_pct: float,
                        page_width_in: float, page_height_in: float,
                        ft_per_inch: float) -> float:
        """
        Measure the length of a line in feet from percentage coordinates.

        This is the backend equivalent of the proven pctToFeet() function
        from the predecessor frontend.
        """
        dx_in = (x2_pct - x1_pct) / 100 * page_width_in
        dy_in = (y2_pct - y1_pct) / 100 * page_height_in
        length_in = (dx_in ** 2 + dy_in ** 2) ** 0.5
        return length_in * ft_per_inch

    def measure_polygon_sqft(self, corners_pct: list[tuple[float, float]],
                             page_width_in: float, page_height_in: float,
                             ft_per_inch: float) -> float:
        """
        Calculate area of a polygon from percentage coordinates.

        Backend equivalent of the proven polygonAreaSqft() function.
        Uses the shoelace formula.

        Args:
            corners_pct: List of (x%, y%) tuples.
            page_width_in: Page width in inches.
            page_height_in: Page height in inches.
            ft_per_inch: Scale factor.

        Returns:
            Area in square feet.
        """
        if len(corners_pct) < 3:
            return 0.0

        # Convert percentage coords to feet
        pts_ft = [
            ((c[0] / 100) * page_width_in * ft_per_inch,
             (c[1] / 100) * page_height_in * ft_per_inch)
            for c in corners_pct
        ]

        # Shoelace formula
        area = 0.0
        n = len(pts_ft)
        for i in range(n):
            j = (i + 1) % n
            area += pts_ft[i][0] * pts_ft[j][1]
            area -= pts_ft[j][0] * pts_ft[i][1]
        return abs(area) / 2.0

    # ------------------------------------------------------------------
    # Image preprocessing
    # ------------------------------------------------------------------

    def _preprocess(self, gray: np.ndarray) -> np.ndarray:
        """
        Preprocess grayscale image for contour detection.

        Pipeline: blur → adaptive threshold → morphological close → invert.
        Tuned for construction plan drawings (thin lines on white background).
        """
        # Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Adaptive threshold — handles varying line darkness across the page
        binary = cv2.adaptiveThreshold(
            blurred, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            blockSize=11,
            C=2,
        )

        # Morphological close — connect nearby line segments
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)

        return closed

    # ------------------------------------------------------------------
    # Unit conversion helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _px_area_to_sqft(area_px: float, px_per_inch: float,
                         ft_per_inch: float) -> float:
        """Convert pixel area to square feet."""
        # area_px / px_per_inch² = area in square inches on paper
        # × ft_per_inch² = area in square feet at scale
        area_sq_in = area_px / (px_per_inch ** 2)
        return area_sq_in * (ft_per_inch ** 2)

    @staticmethod
    def _px_length_to_ft(length_px: float, px_per_inch: float,
                         ft_per_inch: float) -> float:
        """Convert pixel length to feet."""
        length_in = length_px / px_per_inch
        return length_in * ft_per_inch
