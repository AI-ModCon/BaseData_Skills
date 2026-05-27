from pathlib import Path

import convert_v1_to_genesis as conv

SKILL_ROOT = Path(__file__).resolve().parent.parent
FIXTURES = SKILL_ROOT / "tests" / "fixtures"


def test_load_v1_returns_frontmatter():
    fm = conv.load_v1(FIXTURES / "modcon_v1_sample.md")
    assert fm["title"] == "Example MODCON v1 Dataset"
    assert fm["dataset_readiness"]["level"] == 2


def test_convert_maps_basic_identification():
    v1 = conv.load_v1(FIXTURES / "modcon_v1_sample.md")
    report = conv.convert(v1)
    g = report.genesis
    assert g["identification"]["name"] == "Example MODCON v1 Dataset"
    assert g["identification"]["project"] == "modcon-legacy"
    assert g["description"]["summary"].startswith("A synthetic MODCON v1")


def test_convert_maps_dataset_info():
    v1 = conv.load_v1(FIXTURES / "modcon_v1_sample.md")
    report = conv.convert(v1)
    g = report.genesis
    assert "CSV" in g["dataset_info"]["formats"]
    assert "timestamp" in g["dataset_info"]["features"]


def test_convert_maps_license_and_authors():
    v1 = conv.load_v1(FIXTURES / "modcon_v1_sample.md")
    report = conv.convert(v1)
    g = report.genesis
    assert g["license"]["spdx_id"] == "MIT"
    assert g["authors"][0]["person"]["orcid"] == "0000-0002-1234-5678"


def test_convert_sets_creation_method_and_change_log():
    v1 = conv.load_v1(FIXTURES / "modcon_v1_sample.md")
    report = conv.convert(v1)
    g = report.genesis
    assert g["datacard"]["creation_method"] == "hybrid"
    assert g["datacard"]["change_log"][0]["summary"] == "Converted from MODCON v1"


def test_convert_report_lists_missing_required_for_genesis_core():
    v1 = conv.load_v1(FIXTURES / "modcon_v1_sample.md")
    report = conv.convert(v1)
    assert "object_type" in report.missing_required
    assert "workflow.state" in report.missing_required
    assert "security.classification" in report.missing_required


def test_convert_report_lists_orphaned_v1_fields():
    v1 = conv.load_v1(FIXTURES / "modcon_v1_sample.md")
    report = conv.convert(v1)
    assert isinstance(report.orphans, list)
