"""Convert a MODCON v1 datacard to a Genesis Mission Datacard v2 draft.

Reads YAML frontmatter from the v1 .md file, applies a best-effort field
mapping to the Genesis v2 capability-container structure, and returns a
ConversionReport with: the populated Genesis dict, a list of Genesis core
required fields that the mapping couldn't fill (need user input), and a list
of v1 fields with no v2 equivalent (orphans).
"""

from __future__ import annotations

import argparse
import json
import re
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
    """Deep-set a value in a nested dict using a dotted key path."""
    parts = dotted.split(".")
    cur = target
    for p in parts[:-1]:
        cur = cur.setdefault(p, {})
    cur[parts[-1]] = value


def _person_from_v1(v1_person: dict) -> dict:
    """Convert a v1 person sub-dict to a v2 person dict.

    Key rename: affiliation.type → removed (not in v2 person schema).
    Contact/created_by entries use agent_type at a higher level, not inside person.
    """
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
        aff = v1_person["affiliation"]
        out["affiliation"] = {
            "name": aff.get("name", ""),
            "ror_id": aff.get("ror_id", "__ROR_ID__"),
        }
    return out


# ---------- Title-case re-casing ----------

_TITLE_CASE_MAP = {
    "draft": "Draft",
    "under_review": "Under_Review",
    "approved": "Approved",
    "published": "Published",
    "deprecated": "Deprecated",
    "raw": "Raw",
    "processing": "Processing",
    "qa": "QA",
    "analysis": "Analysis",
    "review": "Review",
    "embargo": "Embargo",
    "archived": "Archived",
    "open": "Open",
    "restricted": "Restricted",
    "controlled": "Controlled",
    "manual": "Manual",
    "automated": "Automated",
    "hybrid": "Hybrid",
    "true": "Yes",
    "false": "No",
}


def _titlecase(val: Any) -> Any:
    """Re-case a v1 lowercase enum value to its v2 Title_Case equivalent."""
    if not isinstance(val, str):
        return val
    return _TITLE_CASE_MAP.get(val.lower(), val)


# ---------- CRediT role translation ----------

_CREDIT_ROLE_MAP: dict[str, list[str]] = {
    "creator": ["Conceptualization", "Methodology"],
    "contributor": ["Other"],
    "data_collector": ["Data_Collection"],
    "curator": ["Data_Curation"],
    "publisher": ["Project_Administration"],
    "sponsor": ["Funding_Acquisition"],
    "other": ["Other"],
}


def _credit_roles_from_v1_role(v1_role: str | None) -> list[str]:
    """Map a single v1 role string to a list of v2 CRediT taxonomy values."""
    if not v1_role:
        return ["Other"]
    return _CREDIT_ROLE_MAP.get(v1_role.lower(), ["Other"])


# ---------- supports_* flag inference ----------

def _infer_supports(v1: dict) -> dict[str, str]:
    """Infer v2 supports_* capability flags from v1 content."""
    supports: dict[str, str] = {}
    supports["supports_discoverability"] = "Yes"  # always Yes per schema
    supports["supports_accessibility"] = (
        "Yes" if (v1.get("dataset_counts") or v1.get("dataset_storage") or v1.get("access_policy"))
        else "No"
    )
    supports["supports_interoperability"] = "Yes" if v1.get("dataset_info") else "No"
    supports["supports_reusability"] = (
        "Yes" if (v1.get("license") or v1.get("citation") or v1.get("stewardship"))
        else "No"
    )
    supports["supports_governed_use"] = (
        "Yes" if (v1.get("security") or v1.get("compliance") or v1.get("reviews"))
        else "No"
    )
    supports["supports_ai_usability"] = "Yes" if v1.get("ai_usage") else "No"
    return supports


# ---------- Main conversion ----------

def convert(v1: dict) -> ConversionReport:  # noqa: C901 (complexity OK for a mapper)
    today = date.today().isoformat()
    g: dict = {}
    consumed: set[str] = set()

    # --- supports_* flags (top-level) ---
    supports = _infer_supports(v1)
    for k, v in supports.items():
        g[k] = v

    # --- discoverability.datacard ---
    creation = v1.get("datacard_creation", {}) or {}
    _setp(g, "discoverability.datacard.template_version", "1.0")
    _setp(g, "discoverability.datacard.datacard_version", "1.0")
    _setp(g, "discoverability.datacard.creation_method",
          _titlecase(creation.get("creation_method", "Hybrid")))
    _setp(g, "discoverability.datacard.created_date",
          creation.get("created_date", today))
    _setp(g, "discoverability.datacard.updated_date", today)
    _setp(g, "discoverability.datacard.language", "en")
    _setp(g, "discoverability.datacard.change_log", [
        {"change_date": today, "datacard_version": "1.0", "summary": "Converted from MODCON v1"}
    ])

    # created_by: rename type → agent_type, date key → contribution_date
    v1_creators = creation.get("created_by", []) or []
    if v1_creators:
        g_creators = []
        for c in v1_creators:
            entry: dict[str, Any] = {}
            entry["agent_type"] = c.get("type", "person")
            contribution_date = (
                c.get("contribution_date")
                or c.get("date")
                or creation.get("created_date", today)
            )
            entry["contribution_date"] = contribution_date
            # creator sub-dict
            creator: dict[str, Any] = {}
            agent_t = c.get("type", "person")
            creator["agent_type"] = agent_t
            if agent_t == "person" and "person" in c:
                creator["person"] = _person_from_v1(c["person"])
            elif "ai_model" in c:
                ai = dict(c["ai_model"])
                # rename date_accessed → accessed_date
                if "date_accessed" in ai:
                    ai["accessed_date"] = ai.pop("date_accessed")
                creator["ai_model"] = ai
            entry["creator"] = creator
            g_creators.append(entry)
        _setp(g, "discoverability.datacard.created_by", g_creators)
    consumed.add("datacard_creation")

    # --- discoverability.identification ---
    if "title" in v1:
        _setp(g, "discoverability.identification.name", v1["title"])
        consumed.add("title")
    if "project" in v1:
        _setp(g, "discoverability.identification.project", v1["project"])
        consumed.add("project")

    # --- discoverability.dataset_description ---
    if "description" in v1:
        desc = v1["description"]
        if isinstance(desc, str):
            _setp(g, "discoverability.dataset_description.dataset_summary", desc)
        elif isinstance(desc, dict):
            summary = desc.get("summary", "${SUMMARY}")
            _setp(g, "discoverability.dataset_description.dataset_summary", summary)
            if "keywords" in desc:
                _setp(g, "discoverability.dataset_description.keywords", desc["keywords"])
        consumed.add("description")

    # --- discoverability.release_status ---
    if "release_status" in v1:
        _setp(g, "discoverability.release_status", _titlecase(v1["release_status"]))
        consumed.add("release_status")

    # --- discoverability.authors ---
    if "authors" in v1:
        g_authors = []
        for a in v1["authors"] or []:
            v1_role = a.get("role")
            credit_roles = _credit_roles_from_v1_role(v1_role)
            entry_a: dict[str, Any] = {
                "agent_type": "person",
                "credit_roles": credit_roles,
            }
            if "person" in a:
                entry_a["person"] = _person_from_v1(a["person"])
            g_authors.append(entry_a)
        if g_authors:
            _setp(g, "discoverability.authors", g_authors)
        consumed.add("authors")

    # --- discoverability.contributors ---
    if "contributors" in v1:
        g_contribs = []
        for c in v1["contributors"] or []:
            v1_role = c.get("role")
            credit_roles = _credit_roles_from_v1_role(v1_role)
            entry_c: dict[str, Any] = {
                "agent_type": "person",
                "credit_roles": credit_roles,
            }
            if "person" in c:
                entry_c["person"] = _person_from_v1(c["person"])
            g_contribs.append(entry_c)
        if g_contribs:
            _setp(g, "discoverability.contributors", g_contribs)
        consumed.add("contributors")

    # --- discoverability.contact ---
    if "contact" in v1:
        c_v1 = v1["contact"] or {}
        # rename type → agent_type
        agent_type = c_v1.get("type", "person")
        _setp(g, "discoverability.contact.agent_type", agent_type)
        if agent_type == "person" and "person" in c_v1:
            _setp(g, "discoverability.contact.person", _person_from_v1(c_v1["person"]))
        consumed.add("contact")

    # --- discoverability.sponsor_organizations ---
    if "sponsor_organizations" in v1:
        _setp(g, "discoverability.sponsor_organizations", v1["sponsor_organizations"])
        consumed.add("sponsor_organizations")

    # --- discoverability.research_organizations ---
    if "research_organizations" in v1:
        _setp(g, "discoverability.research_organizations", v1["research_organizations"])
        consumed.add("research_organizations")

    # --- accessibility (requires supports_accessibility=Yes) ---
    if supports["supports_accessibility"] == "Yes":
        dc = v1.get("dataset_counts", {}) or {}
        ds = v1.get("dataset_storage", {}) or {}
        if dc.get("record_count") is not None:
            _setp(g, "accessibility.dataset_scale.record_count", dc["record_count"])
        if dc.get("record_unit"):
            _setp(g, "accessibility.dataset_scale.record_unit", dc["record_unit"])
        if ds.get("compressed_bytes") is not None:
            _setp(g, "accessibility.dataset_scale.compressed_bytes", ds["compressed_bytes"])
        if ds.get("uncompressed_bytes") is not None:
            _setp(g, "accessibility.dataset_scale.uncompressed_bytes",
                  ds["uncompressed_bytes"])
    if v1.get("dataset_counts"):
        consumed.add("dataset_counts")
    if v1.get("dataset_storage"):
        consumed.add("dataset_storage")

    # --- interoperability (requires supports_interoperability=Yes) ---
    if supports["supports_interoperability"] == "Yes":
        di = v1.get("dataset_info", {}) or {}
        if "data_formats" in di:
            _setp(g, "interoperability.data_structure.formats", di["data_formats"])
        if "modalities" in di:
            _setp(g, "interoperability.data_structure.modalities", di["modalities"])
        if "features" in di:
            raw_features = di["features"]
            structured: list[dict] = []
            for feat in raw_features:
                if isinstance(feat, str):
                    structured.append({"name": feat})
                elif isinstance(feat, dict):
                    # rename type → data_type if present
                    feat_out = dict(feat)
                    if "type" in feat_out and "data_type" not in feat_out:
                        feat_out["data_type"] = feat_out.pop("type")
                    structured.append(feat_out)
            _setp(g, "interoperability.data_structure.features", structured)
        if "splits" in di:
            _setp(g, "interoperability.data_structure.splits", di["splits"])
    if v1.get("dataset_info"):
        consumed.add("dataset_info")

    # --- reusability (requires supports_reusability=Yes) ---
    if supports["supports_reusability"] == "Yes":
        if "license" in v1:
            l_v1 = v1["license"] or {}
            if l_v1.get("spdx_id"):
                _setp(g, "reusability.license.spdx_id", l_v1["spdx_id"])
    if v1.get("license"):
        consumed.add("license")
    if v1.get("citation"):
        consumed.add("citation")
    if v1.get("stewardship"):
        consumed.add("stewardship")

    # --- governed_use (requires supports_governed_use=Yes) ---
    if v1.get("security"):
        consumed.add("security")
    if v1.get("compliance"):
        consumed.add("compliance")
    if v1.get("reviews"):
        consumed.add("reviews")

    # --- ai_usability (requires supports_ai_usability=Yes) ---
    if v1.get("ai_usage"):
        consumed.add("ai_usage")

    # --- dataset_readiness: dropped in v2 (orphan with explanation) ---
    if v1.get("dataset_readiness"):
        consumed.add("dataset_readiness")
        # will appear in orphans list with note below

    # --- Compute outputs ---
    mapped = sorted(_flatten_keys(g))

    # Orphans: v1 keys not consumed, plus a special note for dataset_readiness
    raw_orphans = sorted(k for k in v1 if k not in consumed)
    orphans: list[str] = list(raw_orphans)
    # dataset_readiness was consumed above but has no v2 home — add a note
    if "dataset_readiness" in v1:
        orphans.insert(0, "dataset_readiness (dropped: no equivalent in Genesis v2)")

    # Validator: use the Pydantic-model-driven validator, extract MISSING_REQUIRED codes
    result = vd.validate(g)
    missing_required = sorted({f.field for f in result.findings if f.code == "MISSING_REQUIRED"})

    return ConversionReport(
        genesis=g,
        mapped=mapped,
        missing_required=missing_required,
        orphans=orphans,
    )


def _flatten_keys(d: dict, prefix: str = "") -> list[str]:
    """Recursively flatten a nested dict to dotted key paths, skipping list internals."""
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
    template_path = SKILL_ROOT / "references" / "genesis_v1.0_template.md"
    template_text = template_path.read_text()
    parts = re.split(r"^---\s*$", template_text, maxsplit=2, flags=re.MULTILINE)
    body = parts[2] if len(parts) >= 3 else ""
    yaml_block = yaml.safe_dump(report.genesis, sort_keys=False, allow_unicode=True)
    out_path.write_text(f"---\n{yaml_block}---\n{body}", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Convert MODCON v1 datacard → Genesis v2 capability-container draft."
    )
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
    print(f"Orphaned v1 fields (no v2 equivalent): {len(report.orphans)}")
    for path in report.orphans:
        print(f"  - {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
