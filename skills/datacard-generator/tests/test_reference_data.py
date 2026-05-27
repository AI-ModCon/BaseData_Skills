import re
from pathlib import Path
import yaml

SKILL_ROOT = Path(__file__).resolve().parent.parent
REF = SKILL_ROOT / "references"


def _frontmatter(path: Path) -> dict:
    text = path.read_text()
    # Line-anchored split so the comment block's `# ----...` lines don't confuse us.
    parts = re.split(r"^---\s*$", text, maxsplit=2, flags=re.MULTILINE)
    assert len(parts) >= 2, f"{path} does not have YAML frontmatter delimited by `---` lines"
    return yaml.safe_load(parts[1])


def test_genesis_template_exists_and_parses():
    path = REF / "genesis_v1.0_template.md"
    assert path.exists(), f"missing: {path}"
    fm = _frontmatter(path)
    assert isinstance(fm, dict), "frontmatter is not a YAML mapping (template may be malformed)"
    assert "datacard" in fm
    assert fm["datacard"]["template_version"] == "0.1"


def test_genesis_template_has_top_level_sections():
    path = REF / "genesis_v1.0_template.md"
    fm = _frontmatter(path)
    expected_top_level = {
        "datacard", "identification", "description", "object_type",
        "dataset_type", "release_status", "workflow", "dataset_readiness",
        "security", "access_policy", "license", "contact",
        "authors", "sponsor_organizations", "research_organizations",
        "categorization", "dataset_info", "dataset_scale", "dates",
        "access", "provenance", "stewardship", "related_resources",
        "compliance", "citation", "ai_usage", "data_quality",
        "integrity", "semantic_layer", "_repository",
    }
    missing = expected_top_level - set(fm.keys())
    assert not missing, f"missing top-level keys: {missing}"


def _fenced_yaml_blocks(path: Path) -> dict[str, dict]:
    """Extract fenced ```yaml blocks tagged by the section heading immediately above them."""
    text = path.read_text()
    pattern = re.compile(
        r"^##\s+(?P<name>[A-Za-z_][\w\- ]*)\s*\n+```yaml\n(?P<body>.*?)\n```",
        re.MULTILINE | re.DOTALL,
    )
    out = {}
    for m in pattern.finditer(text):
        key = m.group("name").strip().lower().replace(" ", "_")
        body = yaml.safe_load(m.group("body"))
        if isinstance(body, dict) and len(body) == 1 and key in body:
            out[key] = body[key]
        else:
            out[key] = body
    return out


def test_validation_rules_has_profile_matrix():
    path = REF / "validation-rules.md"
    assert path.exists(), f"missing: {path}"
    blocks = _fenced_yaml_blocks(path)
    assert "profiles" in blocks, f"no `profiles` YAML block found; got blocks: {list(blocks)}"
    profiles = blocks["profiles"]
    for name in ("core", "extended", "ai_ready", "sensitive"):
        assert name in profiles, f"profile `{name}` missing"
        assert "required" in profiles[name], f"profile `{name}` missing `required` list"
        assert isinstance(profiles[name]["required"], list)
        assert len(profiles[name]["required"]) > 0, f"profile `{name}` has empty required list"


def test_validation_rules_core_required_includes_essentials():
    blocks = _fenced_yaml_blocks(REF / "validation-rules.md")
    core_required = set(blocks["profiles"]["core"]["required"])
    must_have = {
        "datacard.datacard_version",
        "datacard.profile",
        "datacard.creation_method",
        "datacard.created_date",
        "datacard.updated_date",
        "identification.name",
        "identification.project",
        "identification.version",
        "identification.primary_id.type",
        "identification.primary_id.value",
        "description.summary",
        "description.keywords",
        "object_type",
        "dataset_type",
        "release_status",
        "workflow.state",
        "security.classification",
        "security.sensitivity_tier",
        "security.export_control",
        "datacard.sensitivity_tier",
        "datacard.access_level",
        "access_policy.sensitivity_tier",
        "access_policy.access_level",
        "access_policy.authorization_required",
        "contact.type",
        "categorization.science_domain",
        "dataset_info.formats",
        "provenance.was_generated_by",
        "sponsor_organizations",
        "research_organizations",
    }
    missing = must_have - core_required
    assert not missing, f"core required is missing: {missing}"


def test_validation_rules_has_enums_block():
    blocks = _fenced_yaml_blocks(REF / "validation-rules.md")
    assert "enums" in blocks
    enums = blocks["enums"]
    expected_fields = {
        "datacard.profile",
        "datacard.creation_method",
        "datacard.sensitivity_tier",
        "datacard.access_level",
        "security.classification",
        "security.sensitivity_tier",
        "security.export_control",
        "workflow.state",
        "release_status",
        "object_type",
        "dataset_type",
        "access_policy.access_level",
        "access_policy.authorization_required",
        "license.spdx_id",
    }
    missing = expected_fields - set(enums.keys())
    assert not missing, f"enums missing: {missing}"
    assert "core" in enums["datacard.profile"]
    assert "tier0_open" in enums["datacard.sensitivity_tier"]
    assert "CUI" in enums["security.classification"]
    assert "embargo" in enums["workflow.state"]


def test_validation_rules_has_formats_block():
    blocks = _fenced_yaml_blocks(REF / "validation-rules.md")
    assert "formats" in blocks
    fmts = blocks["formats"]
    for key in ("orcid", "ror_url", "doi", "iso8601_date"):
        assert key in fmts, f"format `{key}` missing"
    for key, pat in fmts.items():
        re.compile(pat)


def test_validation_rules_has_conditional_required_block():
    blocks = _fenced_yaml_blocks(REF / "validation-rules.md")
    assert "conditional_required" in blocks
    rules = blocks["conditional_required"]
    assert isinstance(rules, list)
    embargo_rule = next(
        (r for r in rules if r.get("when", {}).get("workflow.state") == "embargo"), None
    )
    assert embargo_rule is not None, "no rule for workflow.state=embargo"
    assert "workflow.embargo_until" in embargo_rule["require"]


def test_profile_prompts_exists_and_has_all_profiles():
    path = REF / "profile-prompts.md"
    assert path.exists()
    blocks = _fenced_yaml_blocks(path)
    assert "prompts" in blocks
    prompts = blocks["prompts"]
    for profile in ("core", "extended", "ai_ready", "sensitive"):
        assert profile in prompts, f"missing profile `{profile}`"
        batches = prompts[profile]
        assert isinstance(batches, list) and len(batches) > 0
        for batch in batches:
            assert "title" in batch
            assert "fields" in batch
            assert 1 <= len(batch["fields"]) <= 5, "batch size must be 1-5"


def test_field_guide_exists_and_has_section_anchors():
    path = REF / "genesis_field_guide.md"
    assert path.exists(), f"missing: {path}"
    text = path.read_text()
    for needle in (
        "## Section 1: Datacard Metadata",
        "## Section 2:",
        "## Section 3:",
        "## Section 4:",
        "## Section 5:",
        "## Appendix A",
        "## Appendix D",
    ):
        assert needle in text, f"missing anchor: {needle}"


def test_lookup_tables_covers_genesis_axes():
    path = REF / "lookup-tables.md"
    assert path.exists()
    text = path.read_text()
    for needle in (
        "OSTI",
        "tier0_open",
        "tier6_classified",
        "CUI",
        "## Workflow states",
        "## Release statuses",
        "## Authorization",
        "## SPDX",
    ):
        assert needle in text, f"missing section/value: {needle}"
