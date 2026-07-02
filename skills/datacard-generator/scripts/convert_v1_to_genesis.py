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


def _as_orcid_url(raw: str) -> str:
    """Normalize a bare ORCID id to the v2-required URL format.

    v2 requires ``https://orcid.org/XXXX-XXXX-XXXX-XXXX``; v1 sources sometimes
    supply just the bare id. Pass URLs through unchanged.
    """
    raw = raw.strip()
    if raw.startswith("http://") or raw.startswith("https://"):
        return raw
    return f"https://orcid.org/{raw}"


def _person_from_v1(v1_person: dict) -> dict:
    """Convert a v1 person sub-dict to a v2 person dict.

    Key rename: affiliation.type → removed (not in v2 person schema).
    Note: v2 AgentClass has no discriminator field (see _make_agent) — the
    caller is responsible for placing this dict under person/organization/etc.
    """
    out: dict[str, Any] = {}
    name = v1_person.get("name", "")
    if name:
        parts = name.split(None, 1)
        out["given_name"] = parts[0]
        out["family_name"] = parts[1] if len(parts) > 1 else ""
    if v1_person.get("orcid"):
        out["orcid"] = _as_orcid_url(v1_person["orcid"])
    if v1_person.get("email"):
        out["email"] = v1_person["email"]
    if "affiliation" in v1_person:
        aff = v1_person["affiliation"] or {}
        aff_out: dict[str, Any] = {"name": aff.get("name", "")}
        if aff.get("ror_id"):
            aff_out["ror_id"] = aff["ror_id"]
        out["affiliation"] = aff_out
    return out


def _organization_from_v1(v1_org: dict) -> dict:
    """Convert a v1 organization sub-dict to a v2 organization dict."""
    out: dict[str, Any] = {}
    name = v1_org.get("name") or v1_org.get("organization_name")
    if name:
        out["name"] = name
    if v1_org.get("ror_id"):
        out["ror_id"] = v1_org["ror_id"]
    return out


def _make_agent(agent_kind: str, sub_block: dict, roles: list[str] | None = None) -> dict:
    """Build a v1.2 AgentClass entry.

    v1.2's AgentClass has no discriminator field — exactly one of
    person/organization/ai_model/software must be populated (AgentClass.rules).
    CRediT roles live inside that sub-block's ``role`` list, not at the
    AgentClass or author-entry level.

    agent_kind: 'person' | 'organization' | 'ai_model' | 'software'
    sub_block: the fields going into person/organization/ai_model/software
    roles: CRediT roles list (goes inside sub_block['role'])
    """
    block = dict(sub_block)
    if roles:
        block["role"] = roles
    return {agent_kind: block}


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


# ---------- ScienceDomainEnum mapping (v1.2 closed vocabulary, 15 values) ----------

_SCIENCE_DOMAIN_KEYWORDS: list[tuple[str, str]] = [
    ("bio", "Biology and Medicine"),
    ("medic", "Biology and Medicine"),
    ("chem", "Chemistry"),
    ("energy storage", "Energy Storage, Conversion, and Utilization"),
    ("battery", "Energy Storage, Conversion, and Utilization"),
    ("fuel cell", "Energy Storage, Conversion, and Utilization"),
    ("engineer", "Engineering"),
    ("environment", "Environmental Sciences"),
    ("climate", "Environmental Sciences"),
    ("ecolog", "Environmental Sciences"),
    ("nuclear", "Fission and Nuclear Technologies"),
    ("fission", "Fission and Nuclear Technologies"),
    ("fossil", "Fossil Fuels"),
    ("petroleum", "Fossil Fuels"),
    ("coal", "Fossil Fuels"),
    ("natural gas", "Fossil Fuels"),
    ("geo", "Geosciences"),
    ("material", "Materials"),
    ("math", "Mathematics and Computing"),
    ("comput", "Mathematics and Computing"),
    ("data science", "Mathematics and Computing"),
    ("machine learning", "Mathematics and Computing"),
    ("artificial intelligence", "Mathematics and Computing"),
    ("defense", "National Defense"),
    ("military", "National Defense"),
    ("physic", "Physics"),
    ("power generation", "Power Generation and Distribution"),
    ("power distribution", "Power Generation and Distribution"),
    ("grid", "Power Generation and Distribution"),
    ("renewable", "Renewable Energy"),
    ("solar", "Renewable Energy"),
    ("wind energy", "Renewable Energy"),
]


def _map_science_domain(v1_value: str | None) -> str | None:
    """Best-effort map a v1 free-text science_domain to the closed ScienceDomainEnum.

    Returns the canonical quoted-string enum value, or None if there's no
    v1_value or no clean keyword match (caller should flag for user input
    rather than guess — a wrong pick silently degrades catalog quality).
    """
    if not v1_value or not isinstance(v1_value, str):
        return None
    val = v1_value.strip().lower()
    if not val:
        return None
    for keyword, enum_value in _SCIENCE_DOMAIN_KEYWORDS:
        if keyword in val:
            return enum_value
    return None


# ---------- ai_usage status mapping (v1 bool/str → v2 enum strings) ----------

def _map_use_status(v1_value: Any) -> str | None:
    """Map a v1 true/false/'conditional' AI-usage value to v2 YesNoConditionalEnum."""
    if isinstance(v1_value, bool):
        return "Yes" if v1_value else "No"
    if isinstance(v1_value, str):
        v = v1_value.strip().lower()
        if v in ("true", "yes"):
            return "Yes"
        if v in ("false", "no"):
            return "No"
        if v == "conditional":
            return "Conditional"
    return None


def _map_yes_no(v1_value: Any) -> str | None:
    """Map a v1 true/false AI-usage value to v2 YesNoEnum."""
    if isinstance(v1_value, bool):
        return "Yes" if v1_value else "No"
    if isinstance(v1_value, str):
        v = v1_value.strip().lower()
        if v in ("true", "yes"):
            return "Yes"
        if v in ("false", "no"):
            return "No"
    return None


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
    manual_missing: list[str] = []

    # --- supports_* flags (top-level) ---
    supports = _infer_supports(v1)
    for k, v in supports.items():
        g[k] = v

    # --- discoverability.datacard ---
    creation = v1.get("datacard_creation", {}) or {}
    _setp(g, "discoverability.datacard.template_version", "1.2")
    _setp(g, "discoverability.datacard.datacard_version", "1.2")
    _setp(g, "discoverability.datacard.creation_method",
          _titlecase(creation.get("creation_method", "Hybrid")))
    _setp(g, "discoverability.datacard.created_date",
          creation.get("created_date", today))
    _setp(g, "discoverability.datacard.updated_date", today)
    _setp(g, "discoverability.datacard.language", "en")
    _setp(g, "discoverability.datacard.change_log", [
        {"change_date": today, "datacard_version": "1.2", "summary": "Converted from MODCON v1"}
    ])

    # created_by: v1.2 AgentClass has no discriminator field — build via
    # _make_agent so exactly one of person/organization/ai_model/software is set.
    v1_creators = creation.get("created_by", []) or []
    if v1_creators:
        g_creators = []
        for c in v1_creators:
            entry: dict[str, Any] = {}
            contribution_date = (
                c.get("contribution_date")
                or c.get("date")
                or creation.get("created_date", today)
            )
            entry["contribution_date"] = contribution_date
            agent_t = c.get("type", "person")
            if agent_t == "organization" and "organization" in c:
                agent_kind, sub_block = "organization", _organization_from_v1(c["organization"])
            elif "ai_model" in c:
                ai = dict(c["ai_model"])
                # rename date_accessed → accessed_date
                if "date_accessed" in ai:
                    ai["accessed_date"] = ai.pop("date_accessed")
                # v1.2 requires a relationship on ai_model creators; default to
                # used_to_create (matches Hybrid creation-method semantics).
                ai.setdefault("relationship", "used_to_create")
                agent_kind, sub_block = "ai_model", ai
            elif "software" in c:
                sw = dict(c["software"])
                sw.setdefault("relationship", "used_to_create")
                agent_kind, sub_block = "software", sw
            elif "person" in c:
                agent_kind, sub_block = "person", _person_from_v1(c["person"])
            else:
                continue
            roles = _credit_roles_from_v1_role(c["role"]) if c.get("role") else None
            entry["creator"] = _make_agent(agent_kind, sub_block, roles)
            g_creators.append(entry)
        if g_creators:
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

    # --- discoverability.dataset_description.science_domain (v1.2 closed enum) ---
    categorization = v1.get("categorization", {}) or {}
    if categorization.get("science_domain"):
        mapped_domain = _map_science_domain(categorization["science_domain"])
        if mapped_domain:
            _setp(g, "discoverability.dataset_description.science_domain", mapped_domain)
        else:
            manual_missing.append("discoverability.dataset_description.science_domain")
        consumed.add("categorization")

    # --- discoverability.release_status ---
    if "release_status" in v1:
        _setp(g, "discoverability.release_status", _titlecase(v1["release_status"]))
        consumed.add("release_status")

    # --- discoverability.authors ---
    # v1.2: CRediT roles live inside author.person/organization.role, not at
    # the author-entry level (see _make_agent).
    if "authors" in v1:
        g_authors = []
        for a in v1["authors"] or []:
            roles = _credit_roles_from_v1_role(a.get("role"))
            if a.get("type") == "organization" and "organization" in a:
                entry_a = _make_agent("organization", _organization_from_v1(a["organization"]), roles)
            elif "person" in a:
                entry_a = _make_agent("person", _person_from_v1(a["person"]), roles)
            else:
                continue
            g_authors.append(entry_a)
        if g_authors:
            _setp(g, "discoverability.authors", g_authors)
        consumed.add("authors")

    # --- discoverability.contributors ---
    if "contributors" in v1:
        g_contribs = []
        for c in v1["contributors"] or []:
            roles = _credit_roles_from_v1_role(c.get("role"))
            if c.get("type") == "organization" and "organization" in c:
                entry_c = _make_agent("organization", _organization_from_v1(c["organization"]), roles)
            elif "person" in c:
                entry_c = _make_agent("person", _person_from_v1(c["person"]), roles)
            else:
                continue
            g_contribs.append(entry_c)
        if g_contribs:
            _setp(g, "discoverability.contributors", g_contribs)
        consumed.add("contributors")

    # --- discoverability.contact ---
    # v1.2 ContactClass only has a (required) `person` slot — no agent_type
    # discriminator and no organization/ai_model/software alternatives.
    if "contact" in v1:
        c_v1 = v1["contact"] or {}
        if "person" in c_v1:
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

    # --- ai_usability.ai_usage (requires supports_ai_usability=Yes) ---
    # v1.2 renames: training_use_allowed → training_use_status (+ *_conditions
    # required iff status == "Conditional"); same for inference_use_status.
    # v1 has no evaluation_use_allowed equivalent, so evaluation_use_status is
    # left unset and will surface via MISSING_REQUIRED for user input.
    if supports["supports_ai_usability"] == "Yes":
        au = v1.get("ai_usage", {}) or {}
        training_status = _map_use_status(au.get("training_use_allowed"))
        if training_status:
            _setp(g, "ai_usability.ai_usage.training_use_status", training_status)
            if training_status == "Conditional":
                _setp(g, "ai_usability.ai_usage.training_use_conditions",
                      au.get("restrictions") or "${TRAINING_USE_CONDITIONS}")
        inference_status = _map_use_status(au.get("inference_use_allowed"))
        if inference_status:
            _setp(g, "ai_usability.ai_usage.inference_use_status", inference_status)
            if inference_status == "Conditional":
                _setp(g, "ai_usability.ai_usage.inference_use_conditions",
                      au.get("restrictions") or "${INFERENCE_USE_CONDITIONS}")
        for v1_key, g_leaf in (
            ("restrictions", "restrictions"),
            ("bias_risks", "bias_risks"),
            ("safety_considerations", "safety_considerations"),
        ):
            if au.get(v1_key):
                _setp(g, f"ai_usability.ai_usage.{g_leaf}", au[v1_key])
        human_review = _map_yes_no(au.get("human_review_required"))
        if human_review:
            _setp(g, "ai_usability.ai_usage.human_review_required", human_review)
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

    # Validator: use the Pydantic-model-driven validator, extract MISSING_REQUIRED codes.
    # Merge in fields the converter deliberately left unset for user selection
    # (e.g. science_domain with no clean enum match) even though the schema
    # itself marks them optional.
    result = vd.validate(g)
    missing_required = sorted(
        {f.field for f in result.findings if f.code == "MISSING_REQUIRED"} | set(manual_missing)
    )

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
