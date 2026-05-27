"""Profile-aware validator for Genesis Mission Datacard v1.0 files.

Reads validation rules from references/validation-rules.md (single source
of truth) and checks a datacard against them. Returns structured codes
that the SKILL.md workflow can route on.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


MISSING = object()  # sentinel for absent fields


# ---------- Loading ----------

def _read_text(path: Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def load_datacard(path: Path) -> dict:
    """Load the YAML frontmatter from a datacard .md file."""
    text = _read_text(path)
    parts = re.split(r"^---\s*$", text, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 2:
        raise ValueError(f"{path}: file does not have YAML frontmatter delimited by `---` lines")
    data = yaml.safe_load(parts[1])
    if not isinstance(data, dict):
        raise ValueError(f"{path}: frontmatter is not a YAML mapping")
    return data


_FENCE_RE = re.compile(
    r"^##\s+(?P<name>[A-Za-z_][\w\- ]*)\s*\n+```yaml\n(?P<body>.*?)\n```",
    re.MULTILINE | re.DOTALL,
)


def load_rules(path: Path) -> dict:
    """Parse all fenced YAML blocks from validation-rules.md.

    Each block is keyed by its `##` heading slugified to lowercase_underscore.
    If the block body is a single-key dict whose key equals the slug, the
    inner value is hoisted up (so `## Profiles` with body `profiles: {...}`
    yields `{"profiles": {...}}` directly).
    """
    text = _read_text(path)
    out: dict[str, Any] = {}
    for m in _FENCE_RE.finditer(text):
        key = m.group("name").strip().lower().replace(" ", "_")
        body = yaml.safe_load(m.group("body"))
        if isinstance(body, dict) and len(body) == 1 and key in body:
            out[key] = body[key]
        else:
            out[key] = body
    return out


def expand_profile_required(rules: dict, profile: str) -> list[str]:
    """Walk `extends:` chain to compute the union of required fields, parent-first."""
    profiles = rules["profiles"]
    if profile not in profiles:
        raise KeyError(f"unknown profile: {profile}")
    seen: set[str] = set()
    chain: list[str] = []

    def walk(name: str) -> None:
        if name in seen:
            return
        seen.add(name)
        spec = profiles[name]
        parent = spec.get("extends")
        if parent:
            walk(parent)
        for field_path in spec.get("required", []) or []:
            if field_path not in chain:
                chain.append(field_path)

    walk(profile)
    return chain


def get_field(data: dict, path: str) -> Any:
    """Dot-path lookup; returns MISSING if any segment is absent."""
    cur: Any = data
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return MISSING
    return cur


@dataclass
class Finding:
    code: str
    field: str
    severity: str = "error"
    message: str = ""

    def as_dict(self) -> dict:
        return {"code": self.code, "field": self.field,
                "severity": self.severity, "message": self.message}


def _is_present(value: Any) -> bool:
    """A field counts as present unless it's MISSING, None, '', or [].

    Placeholder strings like `${VALUE}` or `__VALUE__` count as absent so
    template scaffolding doesn't pass validation.
    """
    if value is MISSING or value is None:
        return False
    if isinstance(value, str):
        if value == "":
            return False
        if value.startswith("${") and value.endswith("}"):
            return False
        if value.startswith("__") and value.endswith("__"):
            return False
    if isinstance(value, (list, dict)) and len(value) == 0:
        return False
    return True


def check_required(data: dict, rules: dict, profile: str) -> list[Finding]:
    """Walk every dotted-path required for `profile`; flag any absent."""
    required = expand_profile_required(rules, profile)
    findings: list[Finding] = []
    for path in required:
        value = get_field(data, path)
        if not _is_present(value):
            findings.append(Finding(
                code="MISSING_REQUIRED",
                field=path,
                severity="error",
                message=f"required by profile `{profile}` but missing or placeholder",
            ))
    return findings


if __name__ == "__main__":  # pragma: no cover - CLI added in a later task
    sys.exit(0)
