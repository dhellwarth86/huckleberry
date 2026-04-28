"""
Trade input builder — assembles TradeModuleInput from pipeline outputs.

Extracted from `tracepoint_port/TracePoint/server/routes/trade.py` per
MARCH_ORDERS_C_2.md §2: the function body of `build_trade_input` and its
private helpers (`_tb_center`, `_tb_text`, `_bbox_pct_to_pts`,
`_inside_bbox`, `EQUIPMENT_KEYWORDS_BROAD`, `_DIM_RE`) are byte-identical
to TracePoint source. The FastAPI route handler (`run_trade_module`),
the `_get_module` registry, and their FastAPI/server/upload/geometry
dependencies are NOT ported — those belong to Phase E.

This is the DATA CONTRACT BOUNDARY. Platform code lives above this file;
trade modules only consume `TradeModuleInput`.
"""

from __future__ import annotations

import re as _re

from core.trade_module import TradeModuleInput


# -------- Helpers --------

EQUIPMENT_KEYWORDS_BROAD = {
    "RD", "DRAIN", "RTU", "AHU", "SCUPPER", "OVERFLOW", "HATCH",
    "VTR", "VENT", "PIPE", "EF", "EXHAUST", "FAN", "SKYLIGHT",
    "SKY", "CURB", "MECH",
}

_DIM_RE_TEXT = r"\d+['\u2019\u2032][\-\s]*\d*[\"\u201D\u2033]?"
_DIM_RE = _re.compile(_DIM_RE_TEXT)


def _tb_center(tb):
    if hasattr(tb, "x0") and hasattr(tb, "y0"):
        return ((tb.x0 + tb.x1) / 2, (tb.y0 + tb.y1) / 2)
    b = getattr(tb, "bbox", None)
    if b and len(b) >= 4:
        return ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
    return None


def _tb_text(tb) -> str:
    for attr in ("content", "text"):
        v = getattr(tb, attr, None)
        if v:
            return str(v)
    return ""


def _bbox_pct_to_pts(bbox_pct, width_pts, height_pts):
    """bbox_pct is [x_pct, y_pct, w_pct, h_pct] per geometry response."""
    if not bbox_pct or len(bbox_pct) < 4:
        return None
    x0 = bbox_pct[0] / 100.0 * width_pts
    y0 = bbox_pct[1] / 100.0 * height_pts
    x1 = x0 + bbox_pct[2] / 100.0 * width_pts
    y1 = y0 + bbox_pct[3] / 100.0 * height_pts
    return (x0, y0, x1, y1)


def _inside_bbox(center, bbox_pts, margin=0.0) -> bool:
    if not center or not bbox_pts:
        return False
    x0, y0, x1, y1 = bbox_pts
    return (x0 - margin) <= center[0] <= (x1 + margin) and \
           (y0 - margin) <= center[1] <= (y1 + margin)


def build_trade_input(geometry_result: dict,
                      dispatch_ctx,
                      page_num: int,
                      text_blocks: list,
                      page_width_pts: float,
                      page_height_pts: float) -> TradeModuleInput:
    """Assemble a clean TradeModuleInput from pipeline outputs.

    This is the DATA CONTRACT BOUNDARY. Platform code lives above;
    trade modules only consume `TradeModuleInput`.
    """
    building = (geometry_result or {}).get("building_outline") or {}
    contours = (geometry_result or {}).get("contours") or []

    # Polygon bbox in PDF points — use the top building contour's bbox_pct
    polygon_bbox_pts = None
    polygon_vertices = 0
    for c in contours:
        if c.get("is_building_outline"):
            polygon_bbox_pts = _bbox_pct_to_pts(c.get("bbox_pct"), page_width_pts, page_height_pts)
            polygon_vertices = c.get("vertex_count", 0) or 0
            break

    fpi = float(building.get("ft_per_inch") or 0.0)
    area_sqin = float(building.get("area_sqin") or 0.0)
    area_sf = float(building.get("area_sqft") or 0.0)
    perim_ft = float(building.get("perimeter_ft") or 0.0)
    perim_in = (perim_ft / fpi) if fpi else 0.0

    scale_info = (geometry_result or {}).get("scale_info") or {}
    scale_source = scale_info.get("source") or building.get("scale_method") or building.get("source") or "unknown"
    scale_confidence = float(scale_info.get("confidence") or geometry_result.get("confidence") or 0.0)
    detection_source = building.get("source") or ("vector_heavy" if polygon_bbox_pts else "none")

    # --- Filter text blocks to inside polygon (+ 10% margin) ---
    interior_texts: list = []
    equipment_callouts: list = []
    dimension_strings: list = []

    if polygon_bbox_pts:
        w = polygon_bbox_pts[2] - polygon_bbox_pts[0]
        h = polygon_bbox_pts[3] - polygon_bbox_pts[1]
        margin = max(w, h) * 0.30
        for tb in text_blocks or []:
            center = _tb_center(tb)
            if not _inside_bbox(center, polygon_bbox_pts, margin):
                continue
            interior_texts.append(tb)
            text = _tb_text(tb).strip()
            if not text:
                continue
            up = text.upper()
            # Equipment callouts = short and contain a broad keyword
            if len(text) <= 30 and any(kw in up for kw in EQUIPMENT_KEYWORDS_BROAD):
                equipment_callouts.append(tb)
            # Dimension strings
            if _DIM_RE.search(text):
                dimension_strings.append(tb)

    # --- Dispatch context for this page only ---
    page_type = "UNKNOWN"
    page_legends: list = []
    page_zones: list = []
    project_scope = None
    if dispatch_ctx is not None:
        page_ctx = dispatch_ctx.pages.get(page_num)
        if page_ctx is not None:
            page_type = getattr(page_ctx.page_type, "value", str(page_ctx.page_type))
            page_legends = list(page_ctx.legends or [])
            page_zones = list(page_ctx.zones or [])
        project_scope = getattr(dispatch_ctx, "project_scope", None)

    return TradeModuleInput(
        polygon_area_sqin=area_sqin,
        polygon_area_sf=area_sf,
        polygon_perimeter_in=perim_in,
        polygon_perimeter_lf=perim_ft,
        polygon_bbox=polygon_bbox_pts or (0.0, 0.0, 0.0, 0.0),
        polygon_vertices=polygon_vertices,
        scale_fpi=fpi,
        scale_source=scale_source,
        scale_confidence=scale_confidence,
        detection_source=detection_source,
        interior_text_blocks=interior_texts,
        equipment_callouts=equipment_callouts,
        dimension_strings=dimension_strings,
        page_type=page_type,
        page_legends=page_legends,
        page_zones=page_zones,
        project_scope=project_scope,
        page_number=page_num,
    )
