"""Tests for core/architect_profile.py and storage profile methods."""

import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from core.architect_profile import (
    detect_firm, extract_firm_candidates, profile_is_trusted,
    FIRM_KEYWORDS, MATCH_THRESHOLD,
)
from core.storage import StorageEngine


@dataclass
class MockBlock:
    content: str


@pytest.fixture
def storage(tmp_path):
    return StorageEngine(db_path=tmp_path / "test_cache.db")


# ============================================================
# Storage profile methods
# ============================================================

class TestStorageProfiles:
    def test_empty_list(self, storage):
        assert storage.list_architect_profiles() == []

    def test_get_missing(self, storage):
        assert storage.get_architect_profile("Nobody") is None

    def test_upsert_new(self, storage):
        storage.upsert_architect_profile("Smith Architects",
                                         pdf_producer="AutoCAD 2024",
                                         sheet_pattern="A-#.#",
                                         typical_scale=4.0)
        prof = storage.get_architect_profile("Smith Architects")
        assert prof is not None
        assert prof["firm_name"] == "Smith Architects"
        assert prof["success_count"] == 0
        assert "AutoCAD 2024" in prof["pdf_producers"]
        assert "A-#.#" in prof["sheet_patterns"]
        assert "4.0" in prof["typical_scales"]

    def test_upsert_merges_lists(self, storage):
        storage.upsert_architect_profile("Smith", pdf_producer="AutoCAD")
        storage.upsert_architect_profile("Smith", pdf_producer="Revit")
        prof = storage.get_architect_profile("Smith")
        import json
        producers = json.loads(prof["pdf_producers"])
        assert "AutoCAD" in producers
        assert "Revit" in producers
        assert len(producers) == 2

    def test_upsert_no_duplicates_in_lists(self, storage):
        storage.upsert_architect_profile("Smith", pdf_producer="AutoCAD")
        storage.upsert_architect_profile("Smith", pdf_producer="AutoCAD")
        prof = storage.get_architect_profile("Smith")
        import json
        assert len(json.loads(prof["pdf_producers"])) == 1

    def test_increment_success(self, storage):
        storage.upsert_architect_profile("Smith")
        storage.increment_architect_success("Smith")
        storage.increment_architect_success("Smith")
        prof = storage.get_architect_profile("Smith")
        assert prof["success_count"] == 2

    def test_increment_creates_stub_if_absent(self, storage):
        storage.increment_architect_success("Brand New Firm")
        prof = storage.get_architect_profile("Brand New Firm")
        assert prof is not None
        assert prof["success_count"] == 1


# ============================================================
# Candidate extraction
# ============================================================

class TestExtractCandidates:
    def test_empty(self):
        assert extract_firm_candidates([]) == []
        assert extract_firm_candidates(None) == []

    def test_finds_architect_line(self):
        blocks = [MockBlock("Smith & Jones Architects, LLC")]
        cands = extract_firm_candidates(blocks)
        assert any("Smith" in c for c in cands)

    def test_skips_non_firm_text(self):
        blocks = [MockBlock("ROOF PLAN"), MockBlock("SHEET A-1.0")]
        assert extract_firm_candidates(blocks) == []

    def test_dedupes_lines(self):
        blocks = [MockBlock("ABC Architects"), MockBlock("ABC Architects")]
        cands = extract_firm_candidates(blocks)
        assert len(cands) == 1

    def test_handles_string_input(self):
        cands = extract_firm_candidates(["XYZ Engineering Group"])
        assert any("XYZ" in c for c in cands)

    def test_multiline_block(self):
        blocks = [MockBlock("Project Name\nFoo Architects PLLC\n123 Main St")]
        cands = extract_firm_candidates(blocks)
        assert any("Foo" in c for c in cands)


# ============================================================
# detect_firm()
# ============================================================

class TestDetectFirm:
    def test_no_storage_returns_none(self):
        assert detect_firm([MockBlock("ABC Architects")], None) is None

    def test_no_candidates_returns_none(self, storage):
        assert detect_firm([MockBlock("ROOF PLAN")], storage) is None

    def test_creates_stub_for_new_firm(self, storage):
        prof = detect_firm([MockBlock("New Firm Architects")], storage)
        assert prof is not None
        assert prof["success_count"] == 0
        # Stub persisted
        assert "New Firm Architects" in storage.list_architect_profiles()

    def test_matches_existing_profile(self, storage):
        # Seed an existing profile with successes
        storage.upsert_architect_profile("ABC Architects LLC")
        for _ in range(3):
            storage.increment_architect_success("ABC Architects LLC")

        # Slight variation — should fuzzy-match
        prof = detect_firm([MockBlock("ABC Architects, LLC")], storage)
        assert prof is not None
        assert prof["firm_name"] == "ABC Architects LLC"
        assert prof["success_count"] == 3

    def test_unrelated_firm_creates_new_stub(self, storage):
        storage.upsert_architect_profile("ABC Architects LLC")
        prof = detect_firm([MockBlock("Zeta Engineering Consultants")], storage)
        assert prof is not None
        assert prof["firm_name"] != "ABC Architects LLC"


# ============================================================
# profile_is_trusted()
# ============================================================

class TestProfileTrust:
    def test_none_not_trusted(self):
        assert profile_is_trusted(None) is False

    def test_low_success_not_trusted(self):
        assert profile_is_trusted({"success_count": 2}) is False

    def test_threshold_trusted(self):
        assert profile_is_trusted({"success_count": 3}) is True

    def test_high_success_trusted(self):
        assert profile_is_trusted({"success_count": 100}) is True

    def test_missing_field_not_trusted(self):
        assert profile_is_trusted({}) is False
