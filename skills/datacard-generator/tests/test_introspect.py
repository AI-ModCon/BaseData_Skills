import json
import subprocess
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
FIXTURES = SKILL_ROOT / "tests" / "fixtures"
INTROSPECT = SKILL_ROOT / "scripts" / "introspect.py"


def _run(path: Path) -> dict:
    result = subprocess.run(
        [sys.executable, str(INTROSPECT), str(path)],
        capture_output=True, text=True, check=True,
    )
    return json.loads(result.stdout)


def test_introspect_reports_formats():
    out = _run(FIXTURES / "sample_dataset")
    assert "CSV" in out["formats"]


def test_introspect_reports_size_and_count():
    out = _run(FIXTURES / "sample_dataset")
    assert out["file_count"] >= 4
    assert out["total_bytes"] > 0


def test_introspect_detects_license():
    out = _run(FIXTURES / "sample_dataset")
    assert out["license_file_present"] is True
    assert "MIT" in out["license_hint"]


def test_introspect_detects_readme_and_citation():
    out = _run(FIXTURES / "sample_dataset")
    assert out["readme_file"].endswith("README.md")
    assert out["citation_file"].endswith("CITATION.cff")


def test_introspect_extracts_csv_columns():
    out = _run(FIXTURES / "sample_dataset")
    assert "timestamp" in out["sample_columns"]["data.csv"]
    assert "temperature" in out["sample_columns"]["data.csv"]
