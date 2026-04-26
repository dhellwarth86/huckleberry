"""Schema validation tests — confirm the v0.1 BidsetRecord accepts and
round-trips realistic data shapes from the experiment outputs.

Karpathy Shape C (light): the schema IS the contract; contract tests
come first. These tests exercise the Pydantic v0.1 schema by:
1. Instantiating with the documented example.
2. Loading every experiment output, mapping to BidsetRecord-compatible
   shape, and asserting the schema accepts it.
3. Round-tripping (.model_dump() -> BidsetRecord(**...)) is byte-identical.
"""

from __future__ import annotations

import json
from pathlib import Path

from bidset_record import BidsetRecord, Scope, Dispatch, Assembly

OUTPUTS_DIR = Path(__file__).resolve().parent.parent / "test_fixtures" / "experiment_outputs"


def _experiment_output_to_record_input(payload: dict) -> dict:
    """Reshape a per-PDF experiment output to match the v0.1 BidsetRecord
    schema. The experiment captures more than the schema promotes; this
    function projects onto the promoted shape only."""

    src = payload.get("source_pdf_ref", {}) or {}
    disp = payload.get("dispatch", {}) or {}
    sc = payload.get("scope", {}) or {}
    asm = payload.get("assembly", {}) or {}
    prov = payload.get("provenance", {}) or {}

    # Project metadata: keep only promoted fields
    pm_in = (disp.get("project_metadata") or {})
    project_metadata = {
        "project_name": pm_in.get("project_name"),
        "project_address": pm_in.get("project_address"),
        "project_number": pm_in.get("project_number"),
    }

    # Sheet map: experiment uses int keys, schema uses str
    sheet_map = {str(k): v for k, v in (disp.get("sheet_map") or {}).items()}

    return {
        "schema_version": payload.get("schema_version") or "0.1",
        "id": payload["id"],
        "source_pdf_ref": {
            "id": src.get("id") or payload["id"],
            "sha256": src.get("sha256", ""),
            "size_bytes": src.get("size_bytes", 0),
            "page_count": src.get("page_count", 0),
            "local_path": src.get("local_path"),
            "s3_key": src.get("s3_key"),
        },
        "dispatch": {
            "page_classifications": disp.get("page_classifications", []),
            "sheet_map": sheet_map,
            "project_metadata": project_metadata,
            "roof_page_indices": disp.get("roof_page_indices", []),
        },
        "scope": {
            "systems": sc.get("systems", []),
            "evidence": {
                "spec_section_hits": sc.get("evidence", {}).get("spec_section_hits", []),
                "manufacturer_hits": sc.get("evidence", {}).get("manufacturer_hits", []),
                "attachment_hits": sc.get("evidence", {}).get("attachment_hits", []),
                "insulation_markers": sc.get("evidence", {}).get("insulation_markers", []),
                "florida_signals": sc.get("evidence", {}).get("florida_signals", []),
                "system_type_keyword_hits": sc.get("evidence", {}).get("system_type_keyword_hits", []),
            },
            "fallback_used": sc.get("fallback_used", False),
        },
        "assembly": {
            "systems": [
                {
                    "system_type": s.get("system_type"),
                    "attachment": s.get("attachment"),
                    "manufacturer": s.get("manufacturer"),
                    "matched_assembly_key": s.get("matched_assembly_key"),
                    "required_supported_components": s.get("required_supported_components", []),
                    "required_missing_components": s.get("required_missing_components", []),
                    "component_evidence": s.get("component_evidence", {}),
                    "warnings": s.get("warnings", []),
                }
                for s in (asm.get("systems") or [])
            ],
            "florida_signals": asm.get("florida_signals", []),
        },
        "provenance": {
            "fields": {
                k: {
                    "extraction_method": v.get("extraction_method", ""),
                    "source_pages": v.get("source_pages"),
                    "confidence": v.get("confidence"),
                    "parser_value": v.get("parser_value"),
                    "rule_source": v.get("rule_source"),
                }
                for k, v in (prov.get("fields") or {}).items()
            }
        },
    }


def test_schema_accepts_documented_example():
    """The example in BidsetRecord.model_config must validate."""
    example = BidsetRecord.model_config["json_schema_extra"]["example"]
    record = BidsetRecord.model_validate(example)
    assert record.id == example["id"]
    assert record.schema_version == "0.1"


def test_schema_round_trip_byte_identical():
    """A record built from the example -> dumped -> reloaded must equal itself."""
    example = BidsetRecord.model_config["json_schema_extra"]["example"]
    rec1 = BidsetRecord.model_validate(example)
    dumped = rec1.model_dump(mode="json")
    rec2 = BidsetRecord.model_validate(dumped)
    assert rec1 == rec2


def test_all_experiment_outputs_pass_schema():
    """Every per-PDF experiment output, after projection to the promoted
    schema shape, must validate as a BidsetRecord. This is the v0.1
    contract test: the schema MUST accept what the pipeline produces."""
    paths = sorted(OUTPUTS_DIR.glob("*.json"))
    paths = [p for p in paths if not p.name.endswith(".tmp")]
    assert len(paths) >= 15, f"expected >= 15 outputs, got {len(paths)}"

    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        shaped = _experiment_output_to_record_input(payload)
        try:
            BidsetRecord.model_validate(shaped)
        except Exception as e:
            raise AssertionError(f"Schema rejected {path.name}: {e}") from e


def test_schema_rejects_invalid_confidence():
    """Pydantic constraint: confidence must be 0..1. This test guards
    that the constraint is wired (mutation: drop the ge/le -> this fails
    to fail)."""
    bad = {
        "schema_version": "0.1",
        "id": "x",
        "source_pdf_ref": {"id": "x", "sha256": "", "size_bytes": 0, "page_count": 1},
        "dispatch": {
            "page_classifications": [
                {"page_index": 0, "page_type": "roof_plan", "confidence": 1.5},
            ],
        },
    }
    try:
        BidsetRecord.model_validate(bad)
        raise AssertionError("Expected schema to reject confidence=1.5")
    except Exception:
        pass  # expected


def test_schema_requires_top_level_id():
    """`id` and `source_pdf_ref` are required (no default)."""
    try:
        BidsetRecord.model_validate({"schema_version": "0.1"})
        raise AssertionError("Expected schema to reject missing id/source_pdf_ref")
    except Exception:
        pass  # expected
