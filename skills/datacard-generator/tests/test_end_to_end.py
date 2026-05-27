"""End-to-end smoke test:
1. Run introspect.sh on sample_dataset.
2. Validate good_core.md.
3. Convert modcon_v1_sample.md.
4. Confirm validator + converter + introspector hang together.
"""

import json
import subprocess
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
FIXTURES = SKILL_ROOT / "tests" / "fixtures"


def test_pipeline_introspect_then_validate_then_convert(tmp_path):
    # 1. Introspect
    intro = subprocess.run(
        ["bash", str(SKILL_ROOT / "scripts" / "introspect.sh"),
         str(FIXTURES / "sample_dataset")],
        capture_output=True, text=True, check=True,
    )
    summary = json.loads(intro.stdout)
    assert "CSV" in summary["formats"]

    # 2. Validate good_core
    val = subprocess.run(
        [sys.executable, str(SKILL_ROOT / "scripts" / "validate_datacard.py"),
         str(FIXTURES / "good_core.md"),
         "--profile", "core", "--json"],
        capture_output=True, text=True,
    )
    assert val.returncode == 0
    val_payload = json.loads(val.stdout)
    assert val_payload["ok"] is True

    # 3. Convert v1 -> v1.0
    out_file = tmp_path / "converted.genesis.md"
    conv = subprocess.run(
        [sys.executable, str(SKILL_ROOT / "scripts" / "convert_v1_to_genesis.py"),
         str(FIXTURES / "modcon_v1_sample.md"),
         "--out", str(out_file)],
        capture_output=True, text=True, check=True,
    )
    assert out_file.exists()

    # The converted file is a draft; many required fields are still placeholders.
    val2 = subprocess.run(
        [sys.executable, str(SKILL_ROOT / "scripts" / "validate_datacard.py"),
         str(out_file), "--profile", "core", "--json"],
        capture_output=True, text=True,
    )
    payload = json.loads(val2.stdout)
    assert payload["profile"] == "core"
