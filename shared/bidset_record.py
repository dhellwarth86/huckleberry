"""
Wrapper schema for BidsetRecord — the JSON contract between Huckleberry's
frontend (Phase 1, single-file HTML) and backend (Phase 2, FastAPI + Postgres).

═══════════════════════════════════════════════════════════════════════════════
DRAFT v0.1 — produced by the Phase 2 v0.1 experiment, 2026-04-25.
═══════════════════════════════════════════════════════════════════════════════

This is the FIRST evidence-driven schema, replacing the dict[str, Any] stub.
Every field below was promoted by the experiment's two-criteria inclusion rule:

  (1) Field appears in >= 3 of 15 real-bidset extraction outputs, AND
  (2) Field has an identifiable downstream consumer (real or near-future
      user-facing capability that consumes it).

Fields that failed one or both criteria are listed in
`backend/EXPERIMENT_FINDINGS.md` -> "Deferred / observed appendix".
The experiment's per-PDF JSON outputs in
`backend/test_fixtures/experiment_outputs/` are the audit trail for every
inclusion decision.

═══════════════════════════════════════════════════════════════════════════════
What's locked-in by this draft:
═══════════════════════════════════════════════════════════════════════════════
  - The top-level shape: {schema_version, id, source_pdf_ref, dispatch,
    scope, assembly, annotations, provenance}.
  - 32 nested fields, each with a docstring naming its bidset count and
    consumer.

═══════════════════════════════════════════════════════════════════════════════
What's deliberately MISSING (and why):
═══════════════════════════════════════════════════════════════════════════════
  - `annotations` stays empty {} — annotations come from users, not the
    parser; v0.3 fills it. Schema-confirmed empty for now.
  - cross_references / legends / page_type_histogram / confidence_histogram
    appear in 15/15 bidsets but have NO identified downstream consumer
    yet. They're produced by the pipeline and live in extraction_metrics
    or evidence — but they don't appear in this contract.
  - manufacturer.products array, schedule_sheet relationships, glazing
    fields — all out-of-scope for v0.1.

Schema versioning policy (Decision #16 in CLAUDE.md):
  - Every record carries `schema_version`.
  - On breaking change, increment.
  - No migration scripts during the experiment phase; old records stay
    untouched in DB; backend handles version mismatch at read time
    (upgrade-on-read or mark-stale).
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


SCHEMA_VERSION = "0.1"


# ────────────────────────────────────────────────────────────────────────────
# source_pdf_ref — reference to the raw PDF
# ────────────────────────────────────────────────────────────────────────────

class SourcePdfRef(BaseModel):
    """Reference to the PDF in object storage (or local path during v0.1).

    Promoted shape: every field below appeared in 15/15 experiment outputs.
    Fields are populated by the upload script (`upload_fixtures.py`) or
    the local-mode equivalent (`local_manifest.py`); the backend trusts
    them as-is.
    """

    id: str = Field(
        ...,
        description=(
            "Stable identifier for the bidset. Used as routing key on "
            "every API call between frontend and backend. "
            "Bidset count: 15/15. Consumer: HTTP routing, DB primary key."
        ),
    )
    sha256: str = Field(
        ...,
        description=(
            "Content hash of the source PDF. "
            "Bidset count: 15/15. Consumer: integrity check on download; "
            "deduplication; cache invalidation on PDF replace."
        ),
    )
    size_bytes: int = Field(
        ...,
        description=(
            "Byte size of the source PDF. "
            "Bidset count: 15/15. Consumer: storage accounting; "
            "ETA estimation for upload/download."
        ),
    )
    page_count: int = Field(
        ...,
        description=(
            "Total page count of the source PDF. "
            "Bidset count: 15/15. Consumer: PAGES-tab thumbnail grid; "
            "viewer page navigation; pagination of intake jobs."
        ),
    )

    # Either s3_key (object storage) or local_path (v0.1 local-mode). One must
    # be present.  Schema doesn't enforce this — the upload script does.
    s3_key: str | None = Field(default=None, description="Object-storage key when storage.provider != 'local'.")
    local_path: str | None = Field(default=None, description="Absolute local path when storage.provider == 'local'.")


# ────────────────────────────────────────────────────────────────────────────
# dispatch — Layer 1 output: plan-document structure
# ────────────────────────────────────────────────────────────────────────────

class PageClassification(BaseModel):
    """Per-page classification record.

    Bidset count: 15/15 (every page on every bidset is classified, even if
    `page_type='unknown'`). Consumer: PAGES-tab classification badges;
    viewer's first-page-defaults-to-roof_plan logic; per-page filtering
    when scope is parsed (only roof-relevant pages enter Layer 2).
    """

    page_index: int = Field(..., description="0-indexed page number in source PDF.")
    sheet_number: str | None = Field(
        default=None,
        description="Extracted sheet number like 'A-2.0' or None when no title-block match.",
    )
    discipline: str | None = Field(
        default=None,
        description="Mapped from sheet-number prefix per dispatch_seed.DISCIPLINES.",
    )
    page_type: str = Field(
        ...,
        description="One of dispatch_seed.PAGE_TYPES; 'unknown' when no keyword matched.",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Per dispatch_seed.CONFIDENCE: 0.9/0.7/0.5/0.3/0.0.",
    )
    matched_keyword: str | None = Field(
        default=None,
        description="The keyword that triggered this classification (None if fallback).",
    )
    matched_in: str = Field(
        default="default",
        description="'title_block' | 'page_text' | 'fallback' | 'default'.",
    )


class ProjectMetadata(BaseModel):
    """Deterministic project metadata extracted from cover/index pages.

    LLM-only fields per `dispatch_seed.PROJECT_METADATA_LLM_ONLY` are
    intentionally absent from this model — they're a Phase 3 concern.
    Each promoted field carries its bidset count and consumer in its
    description.

    Note: `architect`, `owner`, `total_building_sf` were observed in the
    experiment but DEFERRED — see EXPERIMENT_FINDINGS.md appendix.
    """

    project_name: str | None = Field(
        default=None,
        description=(
            "Bidset count: 13/15. Consumer: Excel export header; "
            "project search; bidset list display."
        ),
    )
    project_address: str | None = Field(
        default=None,
        description=(
            "Bidset count: 14/15. Consumer: Excel export header; "
            "HVHZ county determination (FBC 'applies_to' rule); FBC "
            "wind-zone lookup. ALSO informs scope.evidence.florida_signals."
        ),
    )
    project_number: str | None = Field(
        default=None,
        description=(
            "Bidset count: 15/15. Consumer: Excel export header; "
            "estimator filing reference (matches their internal project "
            "number convention)."
        ),
    )


class Dispatch(BaseModel):
    """Layer 1 output: structural understanding of the plan document.

    Built by `backend/scripts/_pipeline/dispatch.py` against the page
    text, using `seeds/dispatch_seed.py`'s patterns. Drives the PAGES tab,
    page navigation, and which pages enter Layer 2.

    DEFERRED (in 15/15 but no consumer): cross_references_by_page,
    legends_by_page, page_type_histogram, confidence_histogram. They live
    in the per-PDF JSON evidence trail but not in this schema.
    """

    page_classifications: list[PageClassification] = Field(
        default_factory=list,
        description=(
            "Per-page classification records, in page order. "
            "Bidset count: 15/15. Consumer: PAGES-tab badges; scope-tab "
            "first-roof-page navigation; Layer 2 page filter."
        ),
    )

    sheet_map: dict[str, str] = Field(
        default_factory=dict,
        description=(
            "Mapping from page_index (as string) to sheet_number "
            "(e.g. 'A-2.0'). Bidset count: 15/15. Consumer: Sheet-number "
            "column in TAKEOFF / Excel export; deep-link references "
            "(`huckleberry://page-3` -> sheet 'A-2.0')."
        ),
    )

    project_metadata: ProjectMetadata = Field(
        default_factory=ProjectMetadata,
        description=(
            "Deterministic project metadata. LLM-only fields "
            "(building_type, wind_speed_mph, etc.) are NOT in this model; "
            "they're a Phase 3 concern."
        ),
    )

    roof_page_indices: list[int] = Field(
        default_factory=list,
        description=(
            "0-indexed page numbers classified as 'roof_plan'. "
            "Bidset count: 13/15 (2 bidsets are non-roofing-primary "
            "interior packages). Consumer: viewer auto-navigates to the "
            "first roof page on PDF open; SCOPE tab cross-link target."
        ),
    )


# ────────────────────────────────────────────────────────────────────────────
# scope — Layer 2 output: identified roofing systems
# ────────────────────────────────────────────────────────────────────────────

class ScopeSystem(BaseModel):
    """One identified roofing system.

    System identification is conservative: a system is emitted only when
    Layer 2 found at least one of {spec section, system_type keyword,
    insulation marker} on a roof-relevant page. Multi-system bidsets
    (Type 1 + Type V, etc.) are surfaced as multiple ScopeSystem entries
    sharing source_pages — clean per-zone separation is a v0.2 problem.
    """

    system_type: str = Field(
        ...,
        description=(
            "Membrane chemistry: 'tpo' | 'pvc' | 'epdm' | "
            "'modified_bitumen' | 'built_up' | 'metal_panel' | 'shingle' "
            "| 'tile' | 'spf'. Matches roofing_materials.MANUFACTURERS "
            "system entries and roof_assemblies.ROOF_SYSTEMS keys. "
            "Bidset count: 13/15. Consumer: pin/edge/polygon palette "
            "derivation in SCOPE tab; assembly lookup."
        ),
    )
    attachment: str | None = Field(
        default=None,
        description=(
            "Attachment method: 'mechanically_attached' | 'fully_adhered' "
            "| 'ballasted' | 'torch_applied' | 'cold_applied_adhesive' | "
            "'hot_mopped_asphalt' | 'concealed_clip' | 'exposed_fastener' "
            "| 'spray_applied' | 'nailed'. "
            "Bidset count: 9/15. Consumer: disambiguates which "
            "ROOF_SYSTEMS entry to use (e.g. tpo_mechanically_attached "
            "vs tpo_fully_adhered)."
        ),
    )
    manufacturer: str | None = Field(
        default=None,
        description=(
            "Canonical manufacturer name from roofing_materials."
            "MANUFACTURERS keys. "
            "Bidset count: 7/15. Consumer: Excel Manufacturer column; "
            "vendor-specific NOA/spec data lookup; HVHZ approval check."
        ),
    )
    spec_sections: list[str] = Field(
        default_factory=list,
        description=(
            "CSI MasterFormat section keys from roofing_materials."
            "SPEC_SECTIONS that resolved to this system_type "
            "(e.g. ['07 54 23']). "
            "Bidset count: 10/15. Consumer: cross-reference back to spec "
            "page; estimator audit trail."
        ),
    )
    source_pages: list[int] = Field(
        default_factory=list,
        description=(
            "0-indexed pages where this system's evidence appeared. "
            "Bidset count: 13/15. Consumer: click-to-page navigation in "
            "SCOPE tab; provenance audit."
        ),
    )
    confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description=(
            "Identification confidence per dispatch_seed.CONFIDENCE. "
            "Bidset count: 13/15. Consumer: drives 'parser said X, "
            "please confirm' UX in v0.3; sets badge color in SCOPE tab."
        ),
    )


class ScopeEvidence(BaseModel):
    """Raw evidence accumulated during Layer 2.

    Provenance trail for the ScopeSystem entries above. Phase 3 ML
    training depends on this audit being intact from v0.1 — every
    promoted field has a downstream consumer (provenance + UI).

    DEFERRED: thickness_markers (2/15 — not enough signal yet).
    """

    spec_section_hits: list[dict[str, Any]] = Field(
        default_factory=list,
        description=(
            "Per-page spec-section matches with key + system + raw_match. "
            "Bidset count: 14/15. Consumer: provenance audit trail."
        ),
    )
    manufacturer_hits: list[dict[str, Any]] = Field(
        default_factory=list,
        description=(
            "Per-page manufacturer matches with name + match_kind "
            "(name|alias|product). "
            "Bidset count: 9/15. Consumer: provenance audit trail; "
            "alternative-manufacturer suggestion in SCOPE tab."
        ),
    )
    attachment_hits: list[dict[str, Any]] = Field(
        default_factory=list,
        description=(
            "Per-page attachment-method matches. "
            "Bidset count: 9/15. Consumer: provenance audit trail."
        ),
    )
    insulation_markers: list[dict[str, Any]] = Field(
        default_factory=list,
        description=(
            "Per-page insulation/cover-board markers (polyiso, EPS, "
            "DensDeck, etc.). "
            "Bidset count: 8/15. Consumer: provenance + flat-roof "
            "detection (insulation present implies flat roof)."
        ),
    )
    florida_signals: list[dict[str, Any]] = Field(
        default_factory=list,
        description=(
            "FBC, HVHZ, NOA, FM ratings, etc. "
            "Bidset count: 13/15. Consumer: triggers FBC HVHZ warning "
            "chip in SCOPE / TAKEOFF; downstream wind-zone calculations "
            "in v0.3+."
        ),
    )
    system_type_keyword_hits: list[dict[str, Any]] = Field(
        default_factory=list,
        description=(
            "Per-page system-type keyword matches (TPO, PVC, EPDM, etc.). "
            "Bidset count: 12/15. Consumer: provenance audit trail."
        ),
    )


class Scope(BaseModel):
    """Layer 2 output: identified roofing systems with evidence trail.

    Built by `backend/scripts/_pipeline/scope.py` against text from
    pages classified by Layer 1 as roof-relevant, using
    `seeds/roofing_materials.py`. Drives the SCOPE tab and feeds Layer 3.
    """

    systems: list[ScopeSystem] = Field(
        default_factory=list,
        description=(
            "Identified roofing systems. May be empty for non-roofing-"
            "primary bidsets. "
            "Bidset count: 13/15. Consumer: SCOPE-tab card list; "
            "per-system Excel sheets."
        ),
    )
    evidence: ScopeEvidence = Field(
        default_factory=ScopeEvidence,
        description="Per-evidence-track raw hits (provenance trail).",
    )
    fallback_used: bool = Field(
        default=False,
        description=(
            "True when no system_type was directly observed but flat-roof "
            "insulation markers triggered the TPO fallback. "
            "Bidset count: 15/15 (boolean field present on every record; "
            "value True in 0/15 in this experiment). Consumer: QA flag — "
            "fallback systems show 'low confidence' badge in SCOPE tab."
        ),
    )


# ────────────────────────────────────────────────────────────────────────────
# assembly — Layer 3 output: components + relationship warnings per system
# ────────────────────────────────────────────────────────────────────────────

class AssemblySystemResult(BaseModel):
    """Layer 3 result for one ScopeSystem.

    Looks up the matching ROOF_SYSTEMS entry, walks required + conditional
    components, and tries to support each from page text. Reports which
    components have evidence vs which are 'expected but not found'. Then
    runs ASSEMBLY_RELATIONSHIPS rules and reports which warnings would
    fire (text-level today; pin-driven when v0.3 wires annotations in).
    """

    system_type: str
    attachment: str | None = None
    manufacturer: str | None = None
    matched_assembly_key: str | None = Field(
        default=None,
        description=(
            "Key into roof_assemblies.ROOF_SYSTEMS, like "
            "'tpo_mechanically_attached'. None when no match found. "
            "Bidset count: 13/15. Consumer: drives takeoff component "
            "shopping list; pin/edge/polygon palette derivation."
        ),
    )
    required_supported_components: list[str] = Field(
        default_factory=list,
        description=(
            "Components from ROOF_SYSTEMS[*].required_components that "
            "have at least one text match in the bidset. "
            "Bidset count: 13/15. Consumer: Excel takeoff rows that "
            "have evidence shown without a 'verify' badge."
        ),
    )
    required_missing_components: list[str] = Field(
        default_factory=list,
        description=(
            "Components from required_components that did NOT have text "
            "evidence. "
            "Bidset count: 13/15. Consumer: Excel takeoff rows flagged "
            "'expected but not found' for estimator review."
        ),
    )
    component_evidence: dict[str, list[dict[str, Any]]] = Field(
        default_factory=dict,
        description=(
            "Per-component list of {page_index, matched_keyword} hits. "
            "Bidset count: 13/15. Consumer: provenance per takeoff row; "
            "click-to-evidence audit in TAKEOFF tab."
        ),
    )
    warnings: list[dict[str, Any]] = Field(
        default_factory=list,
        description=(
            "ASSEMBLY_RELATIONSHIPS rules that fired (text-level today). "
            "Each entry: {id, rule, trigger_kind, note}. "
            "Bidset count: 9/15. Consumer: TAKEOFF / SCOPE warning chips."
        ),
    )


class Assembly(BaseModel):
    """Layer 3 output: per-system component lists + warnings.

    Built by `backend/scripts/_pipeline/assembly.py` against scope.systems,
    using `seeds/roof_assemblies.py`.
    """

    systems: list[AssemblySystemResult] = Field(
        default_factory=list,
        description=(
            "One entry per Scope.systems entry. "
            "Bidset count: 13/15. Consumer: TAKEOFF-tab line items."
        ),
    )
    florida_signals: list[str] = Field(
        default_factory=list,
        description=(
            "Distinct FBC/HVHZ/NOA/FM/UL signals observed across the "
            "bidset. "
            "Bidset count: 13/15. Consumer: FBC warning panel above "
            "the takeoff table."
        ),
    )


# ────────────────────────────────────────────────────────────────────────────
# annotations — user-supplied (NOT populated by v0.1 experiment)
# ────────────────────────────────────────────────────────────────────────────

class Annotations(BaseModel):
    """User-drawn annotations from the frontend.

    NOT populated by v0.1 — annotations come from users, not the parser.
    Schema-confirmed empty {} until v0.3 wires the Save flow. Shape
    mirrors Phase 1's frontend annotation model: areas[], pins[],
    lineSegments[], polygons[].

    Consumer: round-trips on the Save flow per Decision #5.
    """

    areas: list[dict[str, Any]] = Field(default_factory=list)
    pins: list[dict[str, Any]] = Field(default_factory=list)
    line_segments: list[dict[str, Any]] = Field(default_factory=list)
    polygons: list[dict[str, Any]] = Field(default_factory=list)


# ────────────────────────────────────────────────────────────────────────────
# provenance — audit trail (parser said vs user changed)
# ────────────────────────────────────────────────────────────────────────────

class FieldProvenance(BaseModel):
    """Per-field provenance entry. Phase 3 ML training depends on this."""

    extraction_method: str = Field(
        ...,
        description="Which extractor produced this value (regex name, function name, etc.).",
    )
    source_pages: list[int] | None = Field(
        default=None,
        description="0-indexed source pages where evidence was found.",
    )
    confidence: float | None = Field(
        default=None,
        description="Confidence from dispatch_seed.CONFIDENCE.",
    )
    parser_value: Any | None = Field(
        default=None,
        description="What the parser produced. The current value in the corresponding field of the BidsetRecord IS what the user has after edits; this records what the parser had.",
    )
    rule_source: str | None = Field(
        default=None,
        description="Pointer to the seed file rule (e.g. 'seeds/dispatch_seed.py').",
    )


class Provenance(BaseModel):
    """Audit trail: what the parser said vs what the user changed.

    Per Decision #6: on save, frontend wins (user is right) and
    provenance records the delta. Becomes labeled training data for
    Phase 3 ML.

    Bidset count: 15/15. Consumer: Phase 3 ML training labels;
    v0.3 'parser said X, you changed to Y' UX.
    """

    fields: dict[str, FieldProvenance] = Field(
        default_factory=dict,
        description=(
            "Field-path -> provenance entry. Field paths use dot "
            "notation: 'scope.systems[0].manufacturer'."
        ),
    )


# ────────────────────────────────────────────────────────────────────────────
# Top-level record
# ────────────────────────────────────────────────────────────────────────────

class BidsetRecord(BaseModel):
    """The top-level record produced by Phase 2 backend, consumed by Phase 1
    frontend. Persisted in Postgres. Round-trips on every Save from frontend.

    All eight top-level fields are layer-aligned and version-stamped.
    """

    schema_version: str = Field(
        default=SCHEMA_VERSION,
        description=(
            "Schema version. v0.1 = first evidence-driven schema, "
            "produced by the experiment on 2026-04-25. Incremented on "
            "every breaking change. Backend handles version mismatches "
            "at read time (upgrade-on-read or mark-stale)."
        ),
        examples=["0.1"],
    )

    id: str = Field(
        ...,
        description="Unique bidset identifier; matches manifest entry id.",
        examples=["chipotle-tarpon-springs-shell-tarpon-springs-strategic-construction"],
    )

    source_pdf_ref: SourcePdfRef = Field(
        ...,
        description="Reference to the source PDF in object storage (or local path during v0.1).",
    )

    dispatch: Dispatch = Field(
        default_factory=Dispatch,
        description="Layer 1: plan-document structure (page classifications, sheet map, project metadata).",
    )

    scope: Scope = Field(
        default_factory=Scope,
        description="Layer 2: identified roofing systems with evidence trail.",
    )

    assembly: Assembly = Field(
        default_factory=Assembly,
        description="Layer 3: per-system component lists + relationship warnings.",
    )

    annotations: Annotations = Field(
        default_factory=Annotations,
        description="User-drawn annotations from the frontend (empty in v0.1).",
    )

    provenance: Provenance = Field(
        default_factory=Provenance,
        description="Field-level audit trail (parser said vs user changed).",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "schema_version": "0.1",
                "id": "chipotle-tarpon-springs-shell-tarpon-springs-strategic-construction",
                "source_pdf_ref": {
                    "id": "chipotle-tarpon-springs-shell-tarpon-springs-strategic-construction",
                    "sha256": "68e799d94c031c924289efc9d5cd55ad...",
                    "size_bytes": 27849422,
                    "page_count": 39,
                    "local_path": "C:/huck stage 2/full bid sets/Chipotle - Tarpon Springs (Shell) - Tarpon Springs - Strategic Construction.pdf",
                },
                "dispatch": {
                    "page_classifications": [],
                    "sheet_map": {"0": "E102", "1": "G010"},
                    "project_metadata": {
                        "project_name": "Chipotle Tarpon Springs Shell",
                        "project_address": "140 Carillon Parkway",
                        "project_number": "CMG-2024-119",
                    },
                    "roof_page_indices": [11, 14, 15, 16],
                },
                "scope": {
                    "systems": [
                        {
                            "system_type": "tpo",
                            "attachment": "fully_adhered",
                            "manufacturer": None,
                            "spec_sections": ["07 54"],
                            "source_pages": [16, 19],
                            "confidence": 0.5,
                        },
                    ],
                    "fallback_used": False,
                },
                "assembly": {
                    "systems": [
                        {
                            "system_type": "tpo",
                            "matched_assembly_key": "tpo_fully_adhered",
                            "required_supported_components": ["field_membrane", "insulation"],
                            "required_missing_components": ["fastener_plates"],
                            "warnings": [
                                {"id": "overflow_pairing", "rule": "Every primary drain must have a paired overflow"},
                            ],
                        },
                    ],
                    "florida_signals": ["FBC"],
                },
                "annotations": {"areas": [], "pins": [], "line_segments": [], "polygons": []},
                "provenance": {"fields": {}},
            }
        }
    }
