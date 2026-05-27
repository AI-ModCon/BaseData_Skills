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


def check_enums(data: dict, rules: dict) -> list[Finding]:
    """For each field with a defined enum, verify its value is in the set."""
    enums = rules.get("enums", {}) or {}
    findings: list[Finding] = []
    for field_path, spec in enums.items():
        value = get_field(data, field_path)
        if value is MISSING or value is None:
            continue
        if isinstance(spec, list) and value not in spec:
            findings.append(Finding(
                code="BAD_ENUM",
                field=field_path,
                severity="error",
                message=f"value `{value}` not in allowed set {spec}",
            ))
    return findings


def _walk_path_template(data: dict, template: str) -> list[tuple[str, Any]]:
    """Resolve a dotted path template that may contain `[]` for list iteration.

    Returns a list of (concrete_path, value) pairs. If the path doesn't
    exist, returns []. Wildcards expand into one entry per list element.
    """
    parts = template.split(".")
    frontier: list[tuple[str, Any]] = [("", data)]
    for raw in parts:
        if raw.endswith("[]"):
            key = raw[:-2]
            next_frontier: list[tuple[str, Any]] = []
            for ppath, cur in frontier:
                if not isinstance(cur, dict) or key not in cur:
                    continue
                lst = cur[key]
                if not isinstance(lst, list):
                    continue
                for i, item in enumerate(lst):
                    new_path = f"{ppath}.{key}[{i}]".lstrip(".")
                    next_frontier.append((new_path, item))
            frontier = next_frontier
        else:
            next_frontier = []
            for ppath, cur in frontier:
                if isinstance(cur, dict) and raw in cur:
                    new_path = f"{ppath}.{raw}".lstrip(".")
                    next_frontier.append((new_path, cur[raw]))
            frontier = next_frontier
    return frontier


def check_formats(data: dict, rules: dict) -> list[Finding]:
    formats = rules.get("formats", {}) or {}
    fmt_fields = rules.get("format_fields", {}) or {}
    compiled = {name: re.compile(pat) for name, pat in formats.items()}
    findings: list[Finding] = []
    for fmt_name, field_templates in fmt_fields.items():
        regex = compiled.get(fmt_name)
        if regex is None:
            continue
        for tpl in field_templates:
            for concrete_path, value in _walk_path_template(data, tpl):
                if value is None or value == "":
                    continue
                if isinstance(value, str) and (value.startswith("${")
                                                or value.startswith("__")):
                    continue
                if not isinstance(value, str) or not regex.match(value):
                    findings.append(Finding(
                        code="BAD_FORMAT",
                        field=concrete_path,
                        severity="error",
                        message=f"value `{value}` does not match `{fmt_name}` pattern",
                    ))
    return findings


def _match_condition(data: dict, when: dict, negate: bool = False) -> bool:
    for key, expected in when.items():
        actual = get_field(data, key)
        if actual is MISSING:
            return False if not negate else True
        if (actual == expected) == negate:
            return False
    return True


def check_conditional_required(data: dict, rules: dict) -> list[Finding]:
    out: list[Finding] = []
    for rule in rules.get("conditional_required", []) or []:
        when = rule.get("when")
        when_not = rule.get("when_not")
        severity = rule.get("severity", "error")
        triggered = False
        if when:
            triggered = _match_condition(data, when, negate=False)
        elif when_not:
            triggered = _match_condition(data, when_not, negate=True)
        if not triggered:
            continue
        for path in rule.get("require", []) or []:
            if not _is_present(get_field(data, path)):
                trigger_desc = when or {f"NOT {k}": v for k, v in (when_not or {}).items()}
                out.append(Finding(
                    code="MISSING_REQUIRED",
                    field=path,
                    severity=severity,
                    message=f"required when {trigger_desc}",
                ))
    return out


def _snake_case(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def check_cross_field(data: dict, rules: dict, profile: str) -> list[Finding]:
    out: list[Finding] = []

    # 1. workflow.state <-> release_status alignment (warn).
    alignment = rules.get("workflow_release_alignment", {}) or {}
    state = get_field(data, "workflow.state")
    status = get_field(data, "release_status")
    if state in alignment and status is not MISSING:
        allowed = alignment[state]
        if status not in allowed:
            out.append(Finding(
                code="INCONSISTENT",
                field="workflow.state",
                severity="warn",
                message=(f"workflow.state=`{state}` typically aligns with "
                         f"release_status in {allowed}; got `{status}`"),
            ))

    # 2. is_primary uniqueness across access.intended_repositories.
    repos = get_field(data, "access.intended_repositories")
    if isinstance(repos, list):
        primaries = [i for i, r in enumerate(repos)
                     if isinstance(r, dict) and r.get("is_primary") is True]
        if len(primaries) > 1:
            out.append(Finding(
                code="INCONSISTENT",
                field="access.intended_repositories",
                severity="error",
                message=f"more than one repository marked is_primary=true: indices {primaries}",
            ))

    # 3. features form rule.
    features = get_field(data, "dataset_info.features")
    if isinstance(features, list) and len(features) > 0:
        has_str = any(isinstance(x, str) for x in features)
        has_obj = any(isinstance(x, dict) for x in features)
        if has_str and has_obj:
            out.append(Finding(
                code="INCONSISTENT",
                field="dataset_info.features",
                severity="error",
                message="features: mix of flat strings and structured objects; pick one form",
            ))
        if profile == "ai_ready" and has_str and not has_obj:
            out.append(Finding(
                code="INCONSISTENT",
                field="dataset_info.features",
                severity="error",
                message="ai_ready profile requires structured `features` objects, not flat strings",
            ))

    # 4. filename snake_case match.
    filename = get_field(data, "datacard.filename")
    name = get_field(data, "identification.name")
    if isinstance(filename, str) and isinstance(name, str):
        expected = f"genesis_datacard_{_snake_case(name)}.md"
        if filename != expected:
            out.append(Finding(
                code="INCONSISTENT",
                field="datacard.filename",
                severity="error",
                message=f"expected `{expected}` from identification.name=`{name}`; got `{filename}`",
            ))

    # 5. SENSITIVITY_MISMATCH (informational only).
    doc_tier = get_field(data, "datacard.sensitivity_tier")
    data_tier = get_field(data, "security.sensitivity_tier")
    if doc_tier is not MISSING and data_tier is not MISSING and doc_tier != data_tier:
        out.append(Finding(
            code="SENSITIVITY_MISMATCH",
            field="datacard.sensitivity_tier",
            severity="info",
            message=(f"datacard tier=`{doc_tier}` differs from data tier=`{data_tier}`; "
                     "this is often correct — confirm both are set independently"),
        ))

    return out


@dataclass
class Result:
    profile: str
    findings: list[Finding] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not any(f.severity == "error" for f in self.findings)

    def as_dict(self) -> dict:
        return {
            "profile": self.profile,
            "ok": self.ok,
            "findings": [f.as_dict() for f in self.findings],
        }


def validate(data: dict, rules: dict, profile: str) -> Result:
    findings: list[Finding] = []
    findings.extend(check_required(data, rules, profile))
    findings.extend(check_conditional_required(data, rules))
    findings.extend(check_enums(data, rules))
    findings.extend(check_formats(data, rules))
    findings.extend(check_cross_field(data, rules, profile))
    return Result(profile=profile, findings=findings)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a Genesis v1.0 datacard.")
    parser.add_argument("file", type=Path, help="Path to datacard .md file")
    parser.add_argument("--profile", required=True,
                        choices=["core", "extended", "ai_ready", "sensitive"])
    parser.add_argument("--rules", type=Path,
                        default=Path(__file__).resolve().parent.parent
                                / "references" / "validation-rules.md")
    parser.add_argument("--json", action="store_true",
                        help="Emit machine-readable JSON to stdout")
    args = parser.parse_args(argv)

    rules = load_rules(args.rules)
    data = load_datacard(args.file)
    result = validate(data, rules, profile=args.profile)

    if args.json:
        print(json.dumps(result.as_dict(), indent=2))
    else:
        if result.ok:
            print(f"OK: {args.file} valid for profile `{args.profile}`")
        else:
            n_errors = sum(1 for f in result.findings if f.severity == 'error')
            print(f"FAIL: {args.file} ({n_errors} errors)")
        for f in result.findings:
            print(f"  [{f.severity}] {f.code} {f.field}: {f.message}")
    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main())
