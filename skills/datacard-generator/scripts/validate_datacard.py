"""validate_datacard.py — validate a Genesis v1.0 datacard against the upstream JSON Schema.

The bulk of validation lives in references/genesis_datacard.schema.json
(draft 2019-09, generated from the upstream LinkML source). This module is a
thin wrapper that:

1. Loads the .md datacard, splits frontmatter from body, parses YAML.
2. Runs the JSON Schema validator and collects errors as Finding objects.
3. Runs a small set of *extras* (filename rule, workflow↔release alignment warning)
   that the JSON Schema cannot express.
4. Emits structured findings via JSON (--json) or human-readable text.

Replaces the previous hand-rolled rule engine. To re-sync with upstream,
re-vendor `genesis_datacard.schema.json` (see references/UPSTREAM_VERSION.md).
"""

from __future__ import annotations
import argparse, json, re, sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
import jsonschema
from jsonschema import Draft201909Validator


SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SCHEMA = SKILL_ROOT / "references" / "genesis_datacard.schema.json"
DEFAULT_EXTRAS = SKILL_ROOT / "references" / "validation-rules.md"


@dataclass
class Finding:
    code: str            # MISSING_REQUIRED | BAD_ENUM | BAD_FORMAT | INCONSISTENT | SCHEMA_VIOLATION
    field: str           # dotted path of the offending field
    severity: str = "error"   # error | warn | info
    message: str = ""

    def as_dict(self) -> dict:
        return {"code": self.code, "field": self.field,
                "severity": self.severity, "message": self.message}


@dataclass
class Result:
    findings: list[Finding] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not any(f.severity == "error" for f in self.findings)

    def as_dict(self) -> dict:
        return {"ok": self.ok, "findings": [f.as_dict() for f in self.findings]}


# ---------- Loading ----------

def load_datacard(path: Path) -> dict:
    """Load YAML frontmatter from a .md datacard."""
    text = Path(path).read_text(encoding="utf-8")
    parts = re.split(r"^---\s*$", text, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 2:
        raise ValueError(f"{path}: file does not have YAML frontmatter delimited by `---` lines")
    data = yaml.safe_load(parts[1])
    if not isinstance(data, dict):
        raise ValueError(f"{path}: frontmatter is not a YAML mapping")
    return data


def load_schema(path: Path = DEFAULT_SCHEMA) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


# ---------- Schema validation ----------

def _pointer(error: jsonschema.ValidationError) -> str:
    """Build a dotted path from a ValidationError's absolute_path."""
    parts = []
    for p in error.absolute_path:
        if isinstance(p, int):
            parts.append(f"[{p}]")
        else:
            if parts:
                parts.append(f".{p}")
            else:
                parts.append(str(p))
    return "".join(parts) or "(root)"


def _code_for(error: jsonschema.ValidationError) -> str:
    """Map jsonschema validator names to our Finding codes."""
    v = error.validator
    if v == "required":
        return "MISSING_REQUIRED"
    if v == "enum":
        return "BAD_ENUM"
    if v == "pattern" or v == "format":
        return "BAD_FORMAT"
    if v in ("if", "then", "else", "allOf", "oneOf", "anyOf"):
        return "INCONSISTENT"
    return "SCHEMA_VIOLATION"


def _missing_field_path(error: jsonschema.ValidationError) -> str:
    """For 'required' errors, jsonschema's path is the parent — append the missing field name."""
    parent = _pointer(error)
    # error.message is like "'description' is a required property" — extract the name
    m = re.match(r"^'([^']+)' is a required property", error.message)
    if m:
        name = m.group(1)
        if parent == "(root)":
            return name
        return f"{parent}.{name}"
    return parent


def check_schema(data: dict, schema: dict) -> list[Finding]:
    validator = Draft201909Validator(schema)
    findings: list[Finding] = []
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path)):
        code = _code_for(err)
        if code == "MISSING_REQUIRED":
            field_path = _missing_field_path(err)
        else:
            field_path = _pointer(err)
        findings.append(Finding(
            code=code,
            field=field_path,
            severity="error",
            message=err.message,
        ))
    return findings


# ---------- Extras (warn-level checks not in the schema) ----------

def get_field(data: dict, path: str) -> Any:
    """Dot-path lookup; returns None if any segment is absent."""
    MISSING = object()
    cur: Any = data
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return MISSING
    return cur


def _snake_case(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def check_extras(data: dict) -> list[Finding]:
    """Warn-level rules JSON Schema cannot express.

    All paths use v2 (capability-container) field locations. Update here
    when upstream renames blocks.
    """
    out: list[Finding] = []

    # 1. Filename rule: datacard.filename == "genesis_datacard_<snake_case(identification.name)>.md"
    # In v2 these live under discoverability.datacard.filename and discoverability.identification.name
    name_paths = (
        "discoverability.identification.name",
        # legacy v1 fallback (in case the datacard is in old shape)
        "identification.name",
    )
    filename_paths = (
        "discoverability.datacard.filename",
        "datacard.filename",
    )
    name = next((v for p in name_paths for v in [get_field(data, p)] if isinstance(v, str)), None)
    filename = next((v for p in filename_paths for v in [get_field(data, p)] if isinstance(v, str)), None)
    if name and filename:
        expected = f"genesis_datacard_{_snake_case(name)}.md"
        if filename != expected:
            out.append(Finding(
                code="INCONSISTENT",
                field="datacard.filename",
                severity="warn",
                message=f"expected `{expected}` from name=`{name}`; got `{filename}`",
            ))

    # 2. workflow.state ↔ release_status alignment (warn). v2 paths:
    #    discoverability.workflow.state and discoverability.release_status
    alignment = {
        "Raw": ["Draft"], "Processing": ["Draft"], "QA": ["Draft"], "Analysis": ["Draft"],
        "Review": ["Under_Review"],
        "Embargo": ["Approved", "Published"],
        "Published": ["Approved", "Published"],
        "Archived": ["Deprecated", "Published"],
    }
    state = next((v for p in ("discoverability.workflow.state", "workflow.state")
                  for v in [get_field(data, p)] if isinstance(v, str)), None)
    status = next((v for p in ("discoverability.release_status", "release_status")
                   for v in [get_field(data, p)] if isinstance(v, str)), None)
    if state in alignment and status:
        allowed = alignment[state]
        if status not in allowed:
            out.append(Finding(
                code="INCONSISTENT",
                field="workflow.state",
                severity="warn",
                message=(f"workflow.state=`{state}` typically aligns with "
                         f"release_status in {allowed}; got `{status}`"),
            ))

    return out


# ---------- Orchestrator ----------

def validate(data: dict, schema: dict | None = None) -> Result:
    if schema is None:
        schema = load_schema()
    findings: list[Finding] = []
    findings.extend(check_schema(data, schema))
    findings.extend(check_extras(data))
    return Result(findings=findings)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Validate a Genesis Mission Datacard v1.0 file.")
    p.add_argument("file", type=Path, help="Path to datacard .md file")
    p.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA,
                   help="Path to JSON Schema (default: references/genesis_datacard.schema.json)")
    p.add_argument("--profile",
                   help="Legacy compatibility flag — ignored. Profiles were replaced by supports_* capability flags in v2.")
    p.add_argument("--json", dest="emit_json", action="store_true",
                   help="Emit machine-readable JSON")
    args = p.parse_args(argv)

    if args.profile:
        sys.stderr.write(f"[warn] --profile is ignored in v2 (profiles replaced by supports_* flags).\n")

    schema = load_schema(args.schema)
    data = load_datacard(args.file)
    result = validate(data, schema)

    if args.emit_json:
        print(json.dumps(result.as_dict(), indent=2))
    else:
        if result.ok:
            print(f"OK: {args.file} valid against Genesis Datacard schema")
        else:
            n_errors = sum(1 for f in result.findings if f.severity == "error")
            print(f"FAIL: {args.file} ({n_errors} schema errors)")
        for f in result.findings:
            print(f"  [{f.severity}] {f.code} {f.field}: {f.message}")
    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main())


# ---------- Legacy compatibility shims ----------
# Stage 8 will rewrite tests against the JSON-Schema-driven validator.
# These stubs let the existing test module import without error.

MISSING = object()

def load_rules(*_a, **_kw):
    """Legacy stub — rules are now in the JSON Schema."""
    return {}

def expand_profile_required(*_a, **_kw):
    return []

def check_required(*_a, **_kw):
    return []

def check_enums(*_a, **_kw):
    return []

def check_formats(*_a, **_kw):
    return []

def check_conditional_required(*_a, **_kw):
    return []

def check_cross_field(*_a, **_kw):
    return []

def _walk_path_template(*_a, **_kw):
    return []
