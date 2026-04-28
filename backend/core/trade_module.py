"""
Trade module data contract — the platform/trade boundary.

A trade module receives a `TradeModuleInput`: a clean, filtered slice
of pipeline data for a single page. It never touches raw vector paths,
the full PlanSetContext, or pipeline internals. It returns a
`TradeModuleOutput`: values for the Trade Panel, relationship warnings,
and equipment pins for the overlay.

This module defines the dataclasses and the protocol. Concrete trade
modules live under `modules/<trade>/`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional, Protocol


@dataclass
class TradeFieldValue:
    """A single trade-panel field value with provenance."""
    value: Any                    # number, string, None (None = manual entry needed)
    confidence: float             # 0.0 - 1.0
    source: str                   # "auto_geometry" | "auto_text" | "auto_legend" | "manual_needed"
    evidence: str                 # human-readable origin string
    display_name: str = ""        # label to show in the Trade Panel
    unit: str = ""                # "SF" | "LF" | "EA" | "SQ" | ""


@dataclass
class TradeModuleInput:
    """Filtered input for a trade module — a single page's worth.

    Built by `server.routes.trade.build_trade_input()` from the geometry
    result + PlanSetContext. The trade module must NOT reach past this
    dataclass for pipeline internals.
    """

    # --- Geometry (from the pipeline) ---
    polygon_area_sqin: float
    polygon_area_sf: float
    polygon_perimeter_in: float
    polygon_perimeter_lf: float
    polygon_bbox: tuple                # (x0, y0, x1, y1) in PDF points
    polygon_vertices: int
    scale_fpi: float
    scale_source: str                  # "dispatch" | "manual" | "scoring" | ...
    scale_confidence: float
    detection_source: str              # "vector_heavy" | "vector_all" | "dimension_calc" | "stated_area"

    # --- Text filtered to inside polygon (+ small margin) ---
    interior_text_blocks: list = field(default_factory=list)
    equipment_callouts: list = field(default_factory=list)
    dimension_strings: list = field(default_factory=list)

    # --- Dispatch context for THIS page only ---
    page_type: str = "UNKNOWN"
    page_legends: list = field(default_factory=list)
    page_zones: list = field(default_factory=list)

    # --- Tabular data (e.g., schedule pages) ---
    # Added in C.3b for schedule-driven trade modules (glazing first, then
    # plumbing / electrical / mechanical when those modules ship). Optional;
    # default None preserves C.1/C.2 behaviour. RoofingModule (C.2) ignores
    # this field. Type is intentionally loose — table representation is the
    # producer's choice (pdfplumber rows, dispatch's `_parse_tables_on_page`
    # output, or a future Table dataclass) and consumers cast as needed.
    # See MARCH_ORDERS_C_3b.md §0 (deliberate adaptation of C.1-ported file).
    tables: Optional[list[Any]] = None

    # --- Project-level scope (accumulated from scope/cover pages) ---
    project_scope: Optional[Any] = None

    # --- Page identity (for pin metadata) ---
    page_number: Optional[int] = None

    # --- Helpers ---
    def to_sf(self, sqin: float) -> float:
        return sqin * (self.scale_fpi ** 2)

    def to_lf(self, inches: float) -> float:
        return inches * self.scale_fpi


@dataclass
class TradeModuleOutput:
    """Module-produced values for the Trade Panel."""
    fields: dict[str, TradeFieldValue] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    equipment_pins: list[dict] = field(default_factory=list)


class TradeModule(Protocol):
    """Protocol every trade module implements."""

    TRADE_NAME: str
    FIELDS: list[str]

    def analyze(self, input: TradeModuleInput) -> TradeModuleOutput: ...
