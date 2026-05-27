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
