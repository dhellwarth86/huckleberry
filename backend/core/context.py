"""
PlanSetContext schema — the data contract for dispatch.

Produced by: dispatch gate (filters 1-7)
Consumed by: geometry engine, trade modules, UI, search

Trade-agnostic. No trade-specific code lives here.
"""

from dataclasses import dataclass, field
from typing import Optional, Any
from enum import Enum


# ============================================================
# CONFIDENCE SCALE (use consistently across all filters)
# ============================================================
# 0.9 = explicit text match (keyword found in title block)
# 0.7 = strong heuristic (pattern match with good context)
# 0.5 = inferred (reasonable assumption from partial data)
# 0.3 = weak guess (discipline prefix only, no confirming text)
# 0.0 = unknown (no data)

CONFIDENCE_EXPLICIT = 0.9
CONFIDENCE_STRONG = 0.7
CONFIDENCE_INFERRED = 0.5
CONFIDENCE_WEAK = 0.3
CONFIDENCE_UNKNOWN = 0.0


# ============================================================
# AUDIT — tracks origin of every populated field
# ============================================================

@dataclass
class SourceTag:
    """Tracks where a value came from. Kept simple for v1.
    LLM audit fields (prompt, raw_response) will be added
    when Filter 6 is implemented."""
    origin: str             # "filter_1", "filter_2", "filter_3",
                            # "filter_4", "filter_5", "filter_6_llm",
                            # "filter_7_user"
    confidence: float       # use CONFIDENCE_* constants
    evidence: str           # what text/data produced this value


# ============================================================
# ENUMS — platform-level only, no trade-specific values
# ============================================================

class Discipline(Enum):
    GENERAL = "G"
    ARCHITECTURAL = "A"
    STRUCTURAL = "S"
    MECHANICAL = "M"
    ELECTRICAL = "E"
    PLUMBING = "P"
    CIVIL = "C"
    LANDSCAPE = "L"
    FIRE_PROTECTION = "FP"
    UNKNOWN = "?"


class PageType(Enum):
    COVER = "cover"
    DRAWING_INDEX = "drawing_index"
    SYMBOL_LEGEND = "symbol_legend"
    GENERAL_NOTES = "general_notes"
    SITE_PLAN = "site_plan"
    FLOOR_PLAN = "floor_plan"
    ROOF_PLAN = "roof_plan"
    CEILING_PLAN = "ceiling_plan"
    FRAMING_PLAN = "framing_plan"
    ELEVATION = "elevation"
    SECTION = "section"
    DETAIL_SHEET = "detail_sheet"
    SCHEDULE_SHEET = "schedule_sheet"
    LIFE_SAFETY = "life_safety"
    MEP_PLAN = "mep_plan"
    SHOP_DRAWING = "shop_drawing"
    UNKNOWN = "unknown"


class ConstructionType(Enum):
    NEW = "new"
    REROOF = "reroof"
    RECOVER = "recover"
    REPAIR = "repair"
    ADDITION = "addition"
    UNKNOWN = "unknown"


# ============================================================
# SCALE — dedicated object, multi-source truth
# ============================================================

@dataclass
class ScaleInfo:
    """Scale for a page or zone. Tracks source and confidence."""
    scale_string: str           # "1/4\" = 1'-0\""
    ft_per_inch: float          # 4.0
    source: str                 # "drawing_index" | "zone_label" |
                                # "text_near_title" | "dimension_validation" |
                                # "multi_page_search" | "scoring_fallback" |
                                # "user_override"
    source_page: Optional[int] = None
    confidence: float = CONFIDENCE_UNKNOWN
    source_tag: Optional[SourceTag] = None


# ============================================================
# BUILDING BLOCKS
# ============================================================

@dataclass
class SheetEntry:
    sheet_number: str           # "A-1.3"
    title: str                  # "BUILDING B ROOF PLAN"
    page_index: int             # 0-based PDF page number
    discipline: Discipline
    page_type: PageType
    scale: Optional[ScaleInfo] = None
    confidence: float = CONFIDENCE_UNKNOWN
    source_tag: Optional[SourceTag] = None


@dataclass
class CrossReference:
    ref_type: str               # "detail", "keynote", "see_ref", "schedule_tag"
                                # NOTE: no "section" — dropped per diagnostic
    identifier: str             # "5", "DETAIL 5/A-1.3"
    text: str                   # original text as found on page
    source_page: int
    source_x: float             # position (PDF pts)
    source_y: float
    target_sheet: Optional[str] = None
    target_page: Optional[int] = None
    target_detail: Optional[str] = None
    resolved: bool = False
    confidence: float = CONFIDENCE_UNKNOWN
    source_tag: Optional[SourceTag] = None


@dataclass
class LegendEntry:
    key: str                    # "1", "1.01", "A"
    description: str


@dataclass
class Legend:
    legend_type: str            # "keynote", "material_notes", "roof_notes",
                                # "general_notes", "door_schedule", etc.
    title: str                  # "MATERIAL NOTES"
    page_index: int
    entries: list[LegendEntry] = field(default_factory=list)
    entry_count: int = 0
    bbox: Optional[tuple] = None
    confidence: float = CONFIDENCE_UNKNOWN
    source_tag: Optional[SourceTag] = None


@dataclass
class PageZone:
    zone_type: str              # "main_drawing", "detail_view",
                                # "title_block", "notes_area",
                                # "legend_area", "schedule_area"
    bbox: tuple                 # (x0, y0, x1, y1)
    label: Optional[str] = None
    scale: Optional[ScaleInfo] = None
    confidence: float = CONFIDENCE_UNKNOWN


@dataclass
class PageContext:
    page_index: int
    sheet_number: Optional[str] = None
    title: Optional[str] = None
    discipline: Discipline = Discipline.UNKNOWN
    page_type: PageType = PageType.UNKNOWN
    scale: Optional[ScaleInfo] = None
    confidence: float = CONFIDENCE_UNKNOWN

    # Zones
    zones: list[PageZone] = field(default_factory=list)
    primary_zone: Optional[PageZone] = None  # largest main_drawing zone

    # Content
    legends: list[Legend] = field(default_factory=list)
    cross_refs_out: list[CrossReference] = field(default_factory=list)
    cross_refs_in: list[CrossReference] = field(default_factory=list)

    # Text classification (EXPERIMENTAL — may be noisy)
    callout_texts: list[dict] = field(default_factory=list)
    spec_note_texts: list[dict] = field(default_factory=list)

    # Quick flags
    has_drawing_area: bool = False
    has_title_block: bool = False
    has_details: bool = False
    has_schedule: bool = False
    has_legend: bool = False
    detail_count: int = 0

    # Raw table data from pdfplumber (populated by Filter 4 for schedule pages)
    raw_tables: Optional[list] = None

    source_tag: Optional[SourceTag] = None


# ============================================================
# PROJECT METADATA
# ============================================================

@dataclass
class ProjectMetadata:
    # Deterministic (from cover/title block)
    project_name: Optional[str] = None
    project_address: Optional[str] = None
    project_number: Optional[str] = None
    owner: Optional[str] = None
    architect: Optional[str] = None
    structural_engineer: Optional[str] = None
    mep_engineer: Optional[str] = None
    total_pages: int = 0
    total_building_sf: Optional[float] = None

    # Interpreted (Filter 6 LLM — leave None for now)
    building_type: Optional[str] = None
    building_code: Optional[str] = None
    construction_type: Optional[ConstructionType] = None
    occupancy_type: Optional[str] = None
    wind_speed_mph: Optional[int] = None
    flood_zone: Optional[str] = None
    system_classifications: dict[str, str] = field(default_factory=dict)
    scope_summary: Optional[str] = None

    # Source tracking
    field_sources: dict[str, SourceTag] = field(default_factory=dict)


# ============================================================
# TRADE CONTEXT — registry pattern
# ============================================================

@dataclass
class ScopePage:
    """A page classified as cover/separator/specification/scope content.

    Identified during dispatch by combining text/vector density and
    scope-indicator keywords. Scope pages are NOT drawing pages —
    they carry the project's textual scope information.
    """
    page_number: int
    score: int                          # higher = stronger scope-page signal
    evidence: list[str] = field(default_factory=list)
    text: str = ""                      # concatenated text on the page


@dataclass
class ProjectScope:
    """Project-level roofing scope accumulated from ALL scope pages.

    Multiple scope pages (cover + Division 07 separator + spec excerpt)
    can exist anywhere in the bid set. Their signals are merged into
    one ProjectScope attached to PlanSetContext.
    """
    scope_pages: list[int] = field(default_factory=list)
    spec_sections: list[str] = field(default_factory=list)
    detected_system: Optional[str] = None
    system_confidence: float = CONFIDENCE_UNKNOWN
    system_evidence: str = ""
    manufacturers: list[str] = field(default_factory=list)
    material_mentions: list[str] = field(default_factory=list)
    florida_signals: list[str] = field(default_factory=list)
    roof_shape_signal: Optional[str] = None    # "flat_roof" | "steep_roof" | None
    architect: Optional[str] = None
    contractor: Optional[str] = None


@dataclass
class TradeContext:
    """Base class. Each trade module defines its own subclass.
    Platform stores these in trade_contexts dict.
    PlanSetContext never imports trade-specific code."""
    trade_id: str               # "roofing", "glazing", "siding"
    trade_name: str             # "Commercial Roofing"
    scope_summary: Optional[str] = None
    relevant_pages: list[int] = field(default_factory=list)
    relevant_legends: list[Legend] = field(default_factory=list)
    relevant_refs: list[CrossReference] = field(default_factory=list)
    code_requirements: dict[str, str] = field(default_factory=dict)
    confidence: float = CONFIDENCE_UNKNOWN
    source: str = "interpreted"
    source_tag: Optional[SourceTag] = None


# ============================================================
# BID CONTEXT — user input, not from PDF
# ============================================================

@dataclass
class BidContext:
    general_contractor: Optional[str] = None
    gc_contact_name: Optional[str] = None
    gc_contact_email: Optional[str] = None
    gc_contact_phone: Optional[str] = None
    estimator_assigned: Optional[str] = None
    bid_date: Optional[str] = None
    bid_time: Optional[str] = None
    pre_bid_meeting: Optional[str] = None
    pre_bid_required: bool = False
    trades_solicited: list[str] = field(default_factory=list)
    scope_description: Optional[str] = None
    alternates: list[str] = field(default_factory=list)
    bid_status: str = "open"
    notes: Optional[str] = None


# ============================================================
# LLM CONTRACTS (for future Filter 6 — define now, implement later)
# ============================================================

@dataclass
class LLMInput:
    """ONLY data the LLM sees. No coordinates, no paths, no geometry."""
    cover_page_text: str = ""
    general_notes_text: str = ""
    legend_texts: dict[str, str] = field(default_factory=dict)
    page_titles: list[str] = field(default_factory=list)
    sheet_index_text: str = ""


@dataclass
class LLMOutput:
    """ONLY fields the LLM produces. Validated before storage.
    Rule: LLM may relay numbers explicitly stated in source text.
    LLM must NEVER derive, estimate, count, or calculate numbers."""
    project_name: Optional[str] = None
    project_address: Optional[str] = None
    building_type: Optional[str] = None
    construction_type: Optional[str] = None
    building_code: Optional[str] = None
    occupancy_type: Optional[str] = None
    wind_speed_mph: Optional[int] = None       # OK if stated in source
    total_building_sf: Optional[float] = None  # OK if stated in source
    scope_summary: Optional[str] = None
    system_classifications: dict[str, str] = field(default_factory=dict)


ALLOWED_BUILDING_TYPES = [
    "retail", "restaurant", "office", "warehouse", "industrial",
    "medical", "educational", "religious", "residential_multi",
    "residential_single", "mixed_use", "government", "hospitality",
    "parking", "recreational", "unknown"
]

ALLOWED_CONSTRUCTION_TYPES = [
    "new", "reroof", "recover", "repair", "addition",
    "renovation", "tenant_improvement", "unknown"
]


def validate_llm_output(output: LLMOutput, source_text: str) -> tuple[bool, list[str]]:
    """Iron cage validation. Checks LLM output against rules.
    source_text = concatenated input text the LLM was given."""
    errors = []

    if output.scope_summary and len(output.scope_summary) > 500:
        errors.append("scope_summary exceeds 500 chars")

    if output.building_type and output.building_type not in ALLOWED_BUILDING_TYPES:
        errors.append(f"building_type '{output.building_type}' not in allowed list")

    if output.construction_type and output.construction_type not in ALLOWED_CONSTRUCTION_TYPES:
        errors.append(f"construction_type '{output.construction_type}' not in allowed list")

    # Numeric values must appear in source text (relay, not invent)
    if output.wind_speed_mph is not None:
        if str(output.wind_speed_mph) not in source_text:
            errors.append(f"wind_speed_mph {output.wind_speed_mph} not found in source text — REJECTED")

    if output.total_building_sf is not None:
        # Check for the number in source (allow comma-formatted)
        sf_str = f"{output.total_building_sf:,.0f}"
        sf_str_plain = f"{output.total_building_sf:.0f}"
        if sf_str not in source_text and sf_str_plain not in source_text:
            errors.append(f"total_building_sf {output.total_building_sf} not found in source text — REJECTED")

    return (len(errors) == 0, errors)


# ============================================================
# LEAK DETECTION
# ============================================================

DETERMINISTIC_FIELDS = [
    "sheet_map", "page_to_sheet", "total_pages",
    "all_cross_refs", "resolved_count", "unresolved_count",
    "all_legends"
]

def check_for_leaks(context: 'PlanSetContext') -> list[str]:
    warnings = []
    for field_name, tag in context.project.field_sources.items():
        if tag.origin == "filter_6_llm" and field_name in DETERMINISTIC_FIELDS:
            warnings.append(f"LEAK: LLM wrote to deterministic field '{field_name}'")
    for page_idx, page in context.pages.items():
        if page.confidence == 0.0 and page.page_type != PageType.UNKNOWN:
            warnings.append(f"UNSCORED: page {page_idx} typed as {page.page_type.value} with 0 confidence")
    if context.unresolved_count > 0 and context.resolved_count > 0:
        rate = context.resolved_count / (context.resolved_count + context.unresolved_count)
        if rate < 0.3:
            warnings.append(f"LOW RESOLUTION: {rate:.0%} cross-references resolved")
    return warnings


# ============================================================
# PLANSETCONTEXT — the main object
# ============================================================

@dataclass
class PlanSetContext:
    """
    THE data contract for dispatch.
    Produced by: dispatch gate (filters 1-7)
    Consumed by: geometry engine, trade modules, UI, search
    Trade-agnostic. No trade-specific code lives here.
    """

    # Identity
    pdf_path: str
    pdf_hash: str
    total_pages: int

    # Sheet Map (Filter 1)
    sheet_map: dict[str, SheetEntry] = field(default_factory=dict)
    page_to_sheet: dict[int, str] = field(default_factory=dict)
    sheet_map_source: str = "none"

    # Page Contexts (Filters 2 + 5)
    pages: dict[int, PageContext] = field(default_factory=dict)

    # Reference Graph (Filter 3)
    all_cross_refs: list[CrossReference] = field(default_factory=list)
    resolved_count: int = 0
    unresolved_count: int = 0

    # Legends (Filter 4)
    all_legends: list[Legend] = field(default_factory=list)
    legends_by_type: dict[str, list[Legend]] = field(default_factory=dict)

    # Project Metadata (Filters 1 + 6)
    project: ProjectMetadata = field(default_factory=ProjectMetadata)

    # Trade Contexts (registry — modules populate, NOT dispatch)
    trade_contexts: dict[str, TradeContext] = field(default_factory=dict)

    # D.1: Per-page TradeModuleOutput records, populated when run_dispatch
    # runs with storage activated (storage="auto" or a Storage instance).
    # Shape: {page_idx: {trade_name: TradeModuleOutput}}. Default empty dict
    # preserves all v0.2 / Phase B / Phase C ship behaviour for storage=None
    # callers (calibration harness, legacy tests).
    trade_module_outputs: dict[int, dict[str, Any]] = field(default_factory=dict)

    # Bid Context (Filter 7 — user input)
    bid: BidContext = field(default_factory=BidContext)

    # Architect Profile (optional, populated after Filter 5)
    architect_profile: Optional[dict] = None

    # Project scope — accumulated from scope/cover/separator pages
    project_scope: Optional[ProjectScope] = None

    # Dispatch Status
    filters_completed: list[str] = field(default_factory=list)
    dispatch_complete: bool = False
    dispatch_timestamp: Optional[str] = None
    dispatch_warnings: list[str] = field(default_factory=list)

    # Quick Access
    def get_pages_by_type(self, page_type: PageType) -> list[PageContext]:
        return [p for p in self.pages.values() if p.page_type == page_type]

    def get_pages_by_discipline(self, disc: Discipline) -> list[PageContext]:
        return [p for p in self.pages.values() if p.discipline == disc]

    def resolve_sheet(self, sheet_number: str) -> Optional[int]:
        entry = self.sheet_map.get(sheet_number)
        return entry.page_index if entry else None

    def lookup_keynote(self, number: str) -> Optional[str]:
        for legend in self.legends_by_type.get("keynote", []):
            for entry in legend.entries:
                if entry.key == number:
                    return entry.description
        for legend in self.legends_by_type.get("material_notes", []):
            for entry in legend.entries:
                if entry.key == number:
                    return entry.description
        return None

    def get_trade_context(self, trade_id: str) -> Optional[TradeContext]:
        return self.trade_contexts.get(trade_id)

    # --------------------------------------------------------
    # Serialization (for SQLite persistence)
    # --------------------------------------------------------

    def to_json(self) -> str:
        """Serialize to JSON string for caching.
        Uses the same format as dispatch_gate._ctx_to_dict()."""
        import json

        def _source_tag(tag):
            if tag is None:
                return None
            return {"origin": tag.origin, "confidence": tag.confidence, "evidence": tag.evidence}

        def _scale_info(si):
            if si is None:
                return None
            return {
                "scale_string": si.scale_string,
                "ft_per_inch": si.ft_per_inch,
                "source": si.source,
                "source_page": si.source_page,
                "confidence": si.confidence,
            }

        sheet_map = {}
        for sn, entry in self.sheet_map.items():
            sheet_map[sn] = {
                "sheet_number": entry.sheet_number,
                "title": entry.title,
                "page_index": entry.page_index,
                "discipline": entry.discipline.value,
                "page_type": entry.page_type.value,
                "scale": _scale_info(entry.scale),
                "confidence": entry.confidence,
            }

        pages = {}
        for idx, pc in self.pages.items():
            zones = []
            for z in pc.zones:
                zones.append({
                    "zone_type": z.zone_type,
                    "bbox": list(z.bbox) if z.bbox else [],
                    "label": z.label,
                    "scale": _scale_info(z.scale),
                    "confidence": z.confidence,
                })
            legends = []
            for leg in pc.legends:
                entries = [{"key": e.key, "description": e.description} for e in leg.entries]
                legends.append({
                    "legend_type": leg.legend_type,
                    "title": leg.title,
                    "page_index": leg.page_index,
                    "entries": entries,
                    "entry_count": leg.entry_count,
                    "bbox": list(leg.bbox) if leg.bbox else None,
                    "confidence": leg.confidence,
                    "source_tag": _source_tag(leg.source_tag),
                })
            pages[str(idx)] = {
                "page_index": pc.page_index,
                "sheet_number": pc.sheet_number,
                "title": pc.title,
                "discipline": pc.discipline.value,
                "page_type": pc.page_type.value,
                "scale": _scale_info(pc.scale),
                "confidence": pc.confidence,
                "zones": zones,
                "legends": legends,
                "has_drawing_area": pc.has_drawing_area,
                "has_title_block": pc.has_title_block,
                "has_details": pc.has_details,
                "has_schedule": pc.has_schedule,
                "has_legend": pc.has_legend,
                "detail_count": pc.detail_count,
            }

        cross_refs = []
        for ref in self.all_cross_refs:
            cross_refs.append({
                "ref_type": ref.ref_type,
                "identifier": ref.identifier,
                "text": ref.text,
                "source_page": ref.source_page,
                "source_x": ref.source_x,
                "source_y": ref.source_y,
                "target_sheet": ref.target_sheet,
                "target_page": ref.target_page,
                "target_detail": ref.target_detail,
                "resolved": ref.resolved,
                "confidence": ref.confidence,
            })

        all_legends = []
        for leg in self.all_legends:
            entries = [{"key": e.key, "description": e.description} for e in leg.entries]
            all_legends.append({
                "legend_type": leg.legend_type,
                "title": leg.title,
                "page_index": leg.page_index,
                "entries": entries,
                "entry_count": leg.entry_count,
                "bbox": list(leg.bbox) if leg.bbox else None,
                "confidence": leg.confidence,
                "source_tag": _source_tag(leg.source_tag),
            })

        data = {
            "pdf_path": self.pdf_path,
            "pdf_hash": self.pdf_hash,
            "total_pages": self.total_pages,
            "sheet_map_source": self.sheet_map_source,
            "sheet_map": sheet_map,
            "page_to_sheet": {str(k): v for k, v in self.page_to_sheet.items()},
            "pages": pages,
            "all_cross_refs": cross_refs,
            "resolved_count": self.resolved_count,
            "unresolved_count": self.unresolved_count,
            "all_legends": all_legends,
            "filters_completed": self.filters_completed,
            "dispatch_complete": self.dispatch_complete,
            "dispatch_timestamp": self.dispatch_timestamp,
            "dispatch_warnings": self.dispatch_warnings,
            "architect_profile": self.architect_profile,
            "project_scope": (None if self.project_scope is None else {
                "scope_pages": self.project_scope.scope_pages,
                "spec_sections": self.project_scope.spec_sections,
                "detected_system": self.project_scope.detected_system,
                "system_confidence": self.project_scope.system_confidence,
                "system_evidence": self.project_scope.system_evidence,
                "manufacturers": self.project_scope.manufacturers,
                "material_mentions": self.project_scope.material_mentions,
                "florida_signals": self.project_scope.florida_signals,
                "roof_shape_signal": self.project_scope.roof_shape_signal,
                "architect": self.project_scope.architect,
                "contractor": self.project_scope.contractor,
            }),
        }
        return json.dumps(data)

    @classmethod
    def from_json(cls, json_str: str) -> 'PlanSetContext':
        """Deserialize from JSON string."""
        import json
        data = json.loads(json_str)

        def _parse_source_tag(d):
            if d is None:
                return None
            return SourceTag(origin=d["origin"], confidence=d["confidence"], evidence=d["evidence"])

        def _parse_scale(d):
            if d is None:
                return None
            return ScaleInfo(
                scale_string=d["scale_string"],
                ft_per_inch=d["ft_per_inch"],
                source=d["source"],
                source_page=d.get("source_page"),
                confidence=d.get("confidence", CONFIDENCE_UNKNOWN),
            )

        ctx = cls(
            pdf_path=data["pdf_path"],
            pdf_hash=data["pdf_hash"],
            total_pages=data["total_pages"],
        )
        ctx.sheet_map_source = data.get("sheet_map_source", "none")
        ctx.filters_completed = data.get("filters_completed", [])
        ctx.dispatch_complete = data.get("dispatch_complete", False)
        ctx.dispatch_timestamp = data.get("dispatch_timestamp")
        ctx.dispatch_warnings = data.get("dispatch_warnings", [])
        ctx.resolved_count = data.get("resolved_count", 0)
        ctx.unresolved_count = data.get("unresolved_count", 0)
        ctx.architect_profile = data.get("architect_profile")

        ps_d = data.get("project_scope")
        if ps_d:
            ctx.project_scope = ProjectScope(
                scope_pages=ps_d.get("scope_pages", []),
                spec_sections=ps_d.get("spec_sections", []),
                detected_system=ps_d.get("detected_system"),
                system_confidence=ps_d.get("system_confidence", CONFIDENCE_UNKNOWN),
                system_evidence=ps_d.get("system_evidence", ""),
                manufacturers=ps_d.get("manufacturers", []),
                material_mentions=ps_d.get("material_mentions", []),
                florida_signals=ps_d.get("florida_signals", []),
                roof_shape_signal=ps_d.get("roof_shape_signal"),
                architect=ps_d.get("architect"),
                contractor=ps_d.get("contractor"),
            )

        # Sheet map
        for sn, entry_d in data.get("sheet_map", {}).items():
            ctx.sheet_map[sn] = SheetEntry(
                sheet_number=entry_d["sheet_number"],
                title=entry_d["title"],
                page_index=entry_d["page_index"],
                discipline=Discipline(entry_d["discipline"]),
                page_type=PageType(entry_d["page_type"]),
                scale=_parse_scale(entry_d.get("scale")),
                confidence=entry_d.get("confidence", CONFIDENCE_UNKNOWN),
            )

        # Page to sheet
        for k, v in data.get("page_to_sheet", {}).items():
            ctx.page_to_sheet[int(k)] = v

        # Cross refs
        for ref_d in data.get("all_cross_refs", []):
            ctx.all_cross_refs.append(CrossReference(
                ref_type=ref_d["ref_type"],
                identifier=ref_d["identifier"],
                text=ref_d["text"],
                source_page=ref_d["source_page"],
                source_x=ref_d.get("source_x", 0),
                source_y=ref_d.get("source_y", 0),
                target_sheet=ref_d.get("target_sheet"),
                target_page=ref_d.get("target_page"),
                target_detail=ref_d.get("target_detail"),
                resolved=ref_d.get("resolved", False),
                confidence=ref_d.get("confidence", CONFIDENCE_UNKNOWN),
            ))

        # All legends
        for leg_d in data.get("all_legends", []):
            entries = [LegendEntry(key=e["key"], description=e["description"])
                       for e in leg_d.get("entries", [])]
            legend = Legend(
                legend_type=leg_d["legend_type"],
                title=leg_d["title"],
                page_index=leg_d["page_index"],
                entries=entries,
                entry_count=leg_d.get("entry_count", len(entries)),
                bbox=tuple(leg_d["bbox"]) if leg_d.get("bbox") else None,
                confidence=leg_d.get("confidence", CONFIDENCE_UNKNOWN),
                source_tag=_parse_source_tag(leg_d.get("source_tag")),
            )
            ctx.all_legends.append(legend)

        # Build legends_by_type index
        for legend in ctx.all_legends:
            ctx.legends_by_type.setdefault(legend.legend_type, []).append(legend)

        # Pages
        for idx_str, pc_d in data.get("pages", {}).items():
            idx = int(idx_str)
            zones = []
            for z_d in pc_d.get("zones", []):
                zones.append(PageZone(
                    zone_type=z_d["zone_type"],
                    bbox=tuple(z_d["bbox"]) if z_d.get("bbox") else (0, 0, 0, 0),
                    label=z_d.get("label"),
                    scale=_parse_scale(z_d.get("scale")),
                    confidence=z_d.get("confidence", CONFIDENCE_UNKNOWN),
                ))

            page_legends = []
            for leg_d in pc_d.get("legends", []):
                entries = [LegendEntry(key=e["key"], description=e["description"])
                           for e in leg_d.get("entries", [])]
                page_legends.append(Legend(
                    legend_type=leg_d["legend_type"],
                    title=leg_d["title"],
                    page_index=leg_d["page_index"],
                    entries=entries,
                    entry_count=leg_d.get("entry_count", len(entries)),
                    bbox=tuple(leg_d["bbox"]) if leg_d.get("bbox") else None,
                    confidence=leg_d.get("confidence", CONFIDENCE_UNKNOWN),
                    source_tag=_parse_source_tag(leg_d.get("source_tag")),
                ))

            # Find primary zone
            primary = None
            for z in zones:
                if z.zone_type == "main_drawing":
                    primary = z
                    break

            pc = PageContext(
                page_index=idx,
                sheet_number=pc_d.get("sheet_number"),
                title=pc_d.get("title"),
                discipline=Discipline(pc_d["discipline"]),
                page_type=PageType(pc_d["page_type"]),
                scale=_parse_scale(pc_d.get("scale")),
                confidence=pc_d.get("confidence", CONFIDENCE_UNKNOWN),
                zones=zones,
                primary_zone=primary,
                legends=page_legends,
                has_drawing_area=pc_d.get("has_drawing_area", False),
                has_title_block=pc_d.get("has_title_block", False),
                has_details=pc_d.get("has_details", False),
                has_schedule=pc_d.get("has_schedule", False),
                has_legend=pc_d.get("has_legend", False),
                detail_count=pc_d.get("detail_count", 0),
            )

            # Re-associate cross refs with pages
            pc.cross_refs_out = [r for r in ctx.all_cross_refs if r.source_page == idx]
            pc.cross_refs_in = [r for r in ctx.all_cross_refs
                                if r.resolved and r.target_page == idx]

            ctx.pages[idx] = pc

        return ctx
