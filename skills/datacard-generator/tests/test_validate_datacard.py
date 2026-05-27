from pathlib import Path
import pytest

import validate_datacard as vd

SKILL_ROOT = Path(__file__).resolve().parent.parent
FIXTURES = SKILL_ROOT / "tests" / "fixtures"
RULES = SKILL_ROOT / "references" / "validation-rules.md"


def test_load_rules_returns_expected_blocks():
    rules = vd.load_rules(RULES)
    for key in ("profiles", "enums", "formats", "conditional_required",
                "workflow_release_alignment", "pub_conditional", "format_fields"):
        assert key in rules, f"missing block: {key}"


def test_load_datacard_returns_frontmatter_dict():
    fm = vd.load_datacard(FIXTURES / "good_core.md")
    assert fm["datacard"]["profile"] == "core"
    assert fm["identification"]["name"] == "Test Core Dataset"


def test_expand_profile_required_unions_parents():
    rules = vd.load_rules(RULES)
    ai_ready_required = vd.expand_profile_required(rules, "ai_ready")
    assert "datacard.profile" in ai_ready_required  # from core
    assert "ai_usage.ai_ready" in ai_ready_required  # from ai_ready


def test_get_field_path_returns_nested_value():
    fm = vd.load_datacard(FIXTURES / "good_core.md")
    assert vd.get_field(fm, "datacard.profile") == "core"
    assert vd.get_field(fm, "identification.primary_id.type") == "local"
    assert vd.get_field(fm, "dataset_info.formats") == ["CSV"]
    assert vd.get_field(fm, "missing.field") is vd.MISSING


def test_check_required_passes_on_good_core():
    rules = vd.load_rules(RULES)
    fm = vd.load_datacard(FIXTURES / "good_core.md")
    findings = vd.check_required(fm, rules, profile="core")
    assert findings == [], f"unexpected findings: {findings}"


def test_check_required_flags_missing_name():
    rules = vd.load_rules(RULES)
    fm = vd.load_datacard(FIXTURES / "bad_missing_required.md")
    findings = vd.check_required(fm, rules, profile="core")
    codes = [f.code for f in findings]
    assert any(c == "MISSING_REQUIRED" for c in codes)
    targets = [f.field for f in findings if f.code == "MISSING_REQUIRED"]
    assert "identification.name" in targets


def test_finding_is_dataclass_with_severity():
    rules = vd.load_rules(RULES)
    fm = vd.load_datacard(FIXTURES / "bad_missing_required.md")
    findings = vd.check_required(fm, rules, profile="core")
    assert all(hasattr(f, "code") for f in findings)
    assert all(hasattr(f, "field") for f in findings)
    assert all(hasattr(f, "severity") for f in findings)
    assert all(f.severity in ("error", "warn", "info") for f in findings)


def test_check_enums_passes_good_core():
    rules = vd.load_rules(RULES)
    fm = vd.load_datacard(FIXTURES / "good_core.md")
    findings = vd.check_enums(fm, rules)
    assert findings == [], f"unexpected: {findings}"


def test_check_enums_flags_bad_classification():
    rules = vd.load_rules(RULES)
    fm = vd.load_datacard(FIXTURES / "bad_enum_classification.md")
    findings = vd.check_enums(fm, rules)
    bad = [f for f in findings if f.field == "security.classification"]
    assert len(bad) == 1
    assert bad[0].code == "BAD_ENUM"
    assert "BOGUS" in bad[0].message


def test_check_formats_passes_good_core():
    rules = vd.load_rules(RULES)
    fm = vd.load_datacard(FIXTURES / "good_core.md")
    findings = vd.check_formats(fm, rules)
    assert findings == []


def test_check_formats_flags_bad_orcid():
    rules = vd.load_rules(RULES)
    fm = vd.load_datacard(FIXTURES / "bad_format_orcid.md")
    findings = vd.check_formats(fm, rules)
    orcid_failures = [f for f in findings if f.code == "BAD_FORMAT" and "orcid" in f.field]
    assert len(orcid_failures) >= 1


def test_check_conditional_required_no_findings_when_no_trigger():
    rules = vd.load_rules(RULES)
    fm = vd.load_datacard(FIXTURES / "good_core.md")
    findings = vd.check_conditional_required(fm, rules)
    assert findings == [], f"unexpected: {findings}"


def test_check_conditional_required_embargo_missing_until():
    rules = vd.load_rules(RULES)
    fm = vd.load_datacard(FIXTURES / "bad_conditional_embargo.md")
    findings = vd.check_conditional_required(fm, rules)
    targets = [f.field for f in findings if f.code == "MISSING_REQUIRED"]
    assert "workflow.embargo_until" in targets
