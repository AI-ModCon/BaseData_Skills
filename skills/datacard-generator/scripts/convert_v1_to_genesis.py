"""Convert a MODCON v1 datacard to a Genesis Mission Datacard v1.0 draft.

Reads YAML frontmatter from the v1 .md file, applies a best-effort field
mapping to the Genesis v1.0 structure, and returns a ConversionReport
with: the populated Genesis dict, a list of Genesis core required fields
that the mapping couldn't fill (need user input), and a list of v1 fields
with no v1.0 equivalent (orphans).
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

import yaml

SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

import validate_datacard as vd  # noqa: E402


@dataclass
class ConversionReport:
    genesis: dict
    mapped: list[str] = field(default_factory=list)
    missing_required: list[str] = field(default_factory=list)
    orphans: list[str] = field(default_factory=list)


def load_v1(path: Path) -> dict:
    return vd.load_datacard(path)


def _setp(target: dict, dotted: str, value: Any) -> None:
    parts = dotted.split(".")
    cur = target
    for p in parts[:-1]:
        cur = cur.setdefault(p, {})
    cur[parts[-1]] = value


def _person_from_v1(v1_person: dict) -> dict:
    out: dict[str, Any] = {}
    name = v1_person.get("name", "")
    if name:
        parts = name.split(None, 1)
        out["given_name"] = parts[0]
        out["family_name"] = parts[1] if len(parts) > 1 else ""
    for key in ("orcid", "email"):
        if key in v1_person:
            out[key] = v1_person[key]
    if "affiliation" in v1_person:
        out["affiliation"] = {
            "name": v1_person["affiliation"].get("name", ""),
            "ror_id": v1_person["affiliation"].get("ror_id", "__ROR_ID__"),
        }
    return out


def convert(v1: dict) -> ConversionReport:
    today = date.today().isoformat()
    g: dict = {}
    consumed: set[str] = set()

    # datacard block (v1 had datacard_creation; Genesis has datacard)
    creation = v1.get("datacard_creation", {}) or {}
    _setp(g, "datacard.template_version", "0.1")
    _setp(g, "datacard.datacard_version", "1.0")
    _setp(g, "datacard.profile", "${PROFILE}")
    _setp(g, "datacard.creation_method", "hybrid")
    _setp(g, "datacard.created_date", creation.get("created_date", today))
    _setp(g, "datacard.updated_date", today)
    _setp(g, "datacard.language", "en")
    _setp(g, "datacard.access_level", "open")
    _setp(g, "datacard.sensitivity_tier", "${TIER}")
    _setp(g, "datacard.change_log", [
        {"date": today, "datacard_version": "1.0", "summary": "Converted from MODCON v1"}
    ])
    v1_creators = creation.get("created_by", []) or []
    g_creators = []
    for c in v1_creators:
        if "person" in c:
            g_creators.append({
                "role": "initial_creation",
                "date": creation.get("created_date", today),
                "creator": {
                    "type": "person",
                    "person": _person_from_v1(c["person"]),
                },
            })
    if g_creators:
        _setp(g, "datacard.created_by", g_creators)
    consumed.add("datacard_creation")

    # identification
    if "title" in v1:
        _setp(g, "identification.name", v1["title"])
        consumed.add("title")
    if "project" in v1:
        _setp(g, "identification.project", v1["project"])
        consumed.add("project")
    _setp(g, "identification.version", "1.0")
    _setp(g, "identification.primary_id.type", "local")
    _setp(g, "identification.primary_id.value", "${VALUE}")

    # description
    if "description" in v1:
        if isinstance(v1["description"], str):
            _setp(g, "description.summary", v1["description"])
        elif isinstance(v1["description"], dict):
            _setp(g, "description.summary", v1["description"].get("summary", "${SUMMARY}"))
        consumed.add("description")
    _setp(g, "description.keywords", ["${KEYWORD}"])

    # dataset_info
    di = v1.get("dataset_info", {}) or {}
    if "data_formats" in di:
        _setp(g, "dataset_info.formats", di["data_formats"])
    if "modalities" in di:
        _setp(g, "dataset_info.modalities", di["modalities"])
    if "features" in di:
        _setp(g, "dataset_info.features", di["features"])
    if "splits" in di:
        _setp(g, "dataset_info.splits", di["splits"])
    if di:
        consumed.add("dataset_info")

    # dataset_scale (v1 had dataset_counts + dataset_storage)
    dc = v1.get("dataset_counts", {}) or {}
    ds = v1.get("dataset_storage", {}) or {}
    if dc.get("record_count") is not None:
        _setp(g, "dataset_scale.record_count", dc["record_count"])
    if dc.get("record_unit"):
        _setp(g, "dataset_scale.record_unit", dc["record_unit"])
    if ds.get("compressed_bytes") is not None:
        _setp(g, "dataset_scale.compressed_bytes", ds["compressed_bytes"])
    if ds.get("uncompressed_bytes") is not None:
        _setp(g, "dataset_scale.uncompressed_bytes", ds["uncompressed_bytes"])
    if dc:
        consumed.add("dataset_counts")
    if ds:
        consumed.add("dataset_storage")

    # dataset_readiness
    rd = v1.get("dataset_readiness", {}) or {}
    if "level" in rd:
        _setp(g, "dataset_readiness.level", rd["level"])
        consumed.add("dataset_readiness")

    # release_status
    if "release_status" in v1:
        _setp(g, "release_status", v1["release_status"])
        consumed.add("release_status")

    # authors
    if "authors" in v1:
        g_authors = []
        for a in v1["authors"] or []:
            entry: dict[str, Any] = {"type": "person", "role": "creator"}
            if "person" in a:
                entry["person"] = _person_from_v1(a["person"])
            g_authors.append(entry)
        if g_authors:
            _setp(g, "authors", g_authors)
        consumed.add("authors")

    # contact
    if "contact" in v1:
        c_v1 = v1["contact"] or {}
        ctype = c_v1.get("type", "person")
        _setp(g, "contact.type", ctype)
        if ctype == "person" and "person" in c_v1:
            _setp(g, "contact.person", _person_from_v1(c_v1["person"]))
        consumed.add("contact")

    # license
    if "license" in v1:
        l_v1 = v1["license"] or {}
        if l_v1.get("spdx_id"):
            _setp(g, "license.spdx_id", l_v1["spdx_id"])
        consumed.add("license")

    # sponsor / research / categorization
    if "sponsor_organizations" in v1:
        _setp(g, "sponsor_organizations", v1["sponsor_organizations"])
        consumed.add("sponsor_organizations")
    if "research_organizations" in v1:
        _setp(g, "research_organizations", v1["research_organizations"])
        consumed.add("research_organizations")

    # _repository block: write the system-owned skeleton untouched.
    _setp(g, "_repository.populated_by_repository", False)

    mapped = sorted(_flatten_keys(g))
    orphans = sorted(k for k in v1 if k not in consumed)

    rules = vd.load_rules(SKILL_ROOT / "references" / "validation-rules.md")
    missing_required_findings = vd.check_required(g, rules, profile="core")
    missing_required = sorted({f.field for f in missing_required_findings})

    return ConversionReport(
        genesis=g, mapped=mapped, missing_required=missing_required, orphans=orphans,
    )


def _flatten_keys(d: dict, prefix: str = "") -> list[str]:
    out: list[str] = []
    for k, v in d.items():
        path = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            out.extend(_flatten_keys(v, path))
        else:
            out.append(path)
    return out


def write_genesis_file(report: ConversionReport, out_path: Path) -> None:
    """Render the Genesis dict as YAML frontmatter + the canonical template's markdown body."""
    import re as _re
    template_path = SKILL_ROOT / "references" / "genesis_v1.0_template.md"
    template_text = template_path.read_text()
    parts = _re.split(r"^---\s*$", template_text, maxsplit=2, flags=_re.MULTILINE)
    body = parts[2] if len(parts) >= 3 else ""
    yaml_block = yaml.safe_dump(report.genesis, sort_keys=False, allow_unicode=True)
    out_path.write_text(f"---\n{yaml_block}---\n{body}", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Convert MODCON v1 datacard → Genesis v1.0 draft.")
    parser.add_argument("file", type=Path, help="Path to v1 .md file")
    parser.add_argument("--out", type=Path, default=None,
                        help="Output path (default: <input>.genesis.md)")
    parser.add_argument("--json", action="store_true",
                        help="Emit report as JSON to stdout (do not write file)")
    args = parser.parse_args(argv)

    v1 = load_v1(args.file)
    report = convert(v1)

    if args.json:
        print(json.dumps({
            "mapped": report.mapped,
            "missing_required": report.missing_required,
            "orphans": report.orphans,
        }, indent=2))
        return 0

    out = args.out or args.file.with_suffix(".genesis.md")
    write_genesis_file(report, out)
    print(f"Wrote {out}")
    print(f"Mapped: {len(report.mapped)} fields")
    print(f"Missing required (need user input): {len(report.missing_required)}")
    for path in report.missing_required:
        print(f"  - {path}")
    print(f"Orphaned v1 fields (no v1.0 equivalent): {len(report.orphans)}")
    for path in report.orphans:
        print(f"  - {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
