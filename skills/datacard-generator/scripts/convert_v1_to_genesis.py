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

    Accepts two shapes:
      - thin: ``name: "First Last"`` (split on first whitespace)
      - rich: ``given_name: "First", family_name: "Last"`` (already split)

    Key rename: affiliation.type → removed (not in v2 person schema).
    Note: v2 AgentClass has no discriminator field (see _make_agent) — the
    caller is responsible for placing this dict under person/organization/etc.
    """
    out: dict[str, Any] = {}
    if v1_person.get("given_name") or v1_person.get("family_name"):
        if v1_person.get("given_name"):
            out["given_name"] = v1_person["given_name"]
        if v1_person.get("family_name"):
            out["family_name"] = v1_person["family_name"]
    elif v1_person.get("name"):
        parts = str(v1_person["name"]).split(None, 1)
        out["given_name"] = parts[0]
        out["family_name"] = parts[1] if len(parts) > 1 else ""
    if v1_person.get("orcid"):
        out["orcid"] = _as_orcid_url(v1_person["orcid"])
    if v1_person.get("email"):
        out["email"] = v1_person["email"]
    if "affiliation" in v1_person:
        aff = v1_person["affiliation"] or {}
        aff_name = aff.get("name") or ""
        aff_ror = aff.get("ror_id")
        # Skip the whole affiliation subblock when there's no meaningful data
        # (avoids emitting `affiliation: {name: ''}` for authors whose v1 source
        # had a null affiliation).
        if aff_name or aff_ror:
            aff_out: dict[str, Any] = {"name": aff_name}
            if aff_ror:
                aff_out["ror_id"] = aff_ror
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


def _unwrap_entity(entry: dict) -> dict:
    """Peel a v1-rich ``entity: {type: X, X: {...}}`` wrapper to v1-thin shape.

    Rich-schema entries wrap the discriminator + payload inside ``entity:``;
    thin-schema entries have them at the top level. Siblings (like ``role``)
    are preserved.
    """
    if not isinstance(entry, dict):
        return entry
    if "entity" in entry and isinstance(entry["entity"], dict):
        inner = entry["entity"]
        out = {k: v for k, v in entry.items() if k != "entity"}
        out.update(inner)
        return out
    return entry


def _flatten_affiliation(person: dict) -> dict:
    """Convert nested ``affiliation.entity.organization.{name,ror_id}`` → flat
    ``affiliation.{name,ror_id}`` shape expected by ``_person_from_v1``.
    """
    aff = person.get("affiliation") if isinstance(person, dict) else None
    if not isinstance(aff, dict) or "entity" not in aff:
        return person
    inner_org = (aff["entity"] or {}).get("organization", {}) or {}
    out = dict(person)
    out["affiliation"] = {k: v for k, v in {
        "name": inner_org.get("name") or "",
        "ror_id": inner_org.get("ror_id"),
    }.items() if v not in (None, "")} or {"name": ""}
    return out


def _normalize_person_entry(entry: dict) -> dict:
    """Normalize a rich-schema author/contact/contributor entry to thin shape:
    unwrap the outer ``entity`` and flatten any nested affiliation.
    """
    entry = _unwrap_entity(entry)
    if isinstance(entry, dict) and "person" in entry and isinstance(entry["person"], dict):
        entry = dict(entry)
        entry["person"] = _flatten_affiliation(entry["person"])
    return entry


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


# authorization_required (accessibility.access_policy) — v1-rich camelCase → v1.2 Title_Case
_AUTH_MAP = {
    "accountrequired": "Account",
    "account": "Account",
    "useragreement": "User_Agreement",
    "user_agreement": "User_Agreement",
    "dataUseAgreement".lower(): "Data_Use_Agreement",
    "dua": "Data_Use_Agreement",
    "sponsorapproval": "Sponsor_Approval",
    "exportcontrolreview": "Export_Control_Review",
    "irbapproval": "IRB_Approval",
    "irb": "IRB_Approval",
}


# Related-resources relationship enum: v1 camelCase → v1.2 snake_case
_RELATIONSHIP_MAP = {
    "ispartof": "is_part_of",
    "haspart": "has_part",
    "isderivedfrom": "is_derived_from",
    "isbasedon": "is_based_on",
    "references": "references",
    "usedtocreate": "used_to_create",
    "usedtoprocess": "used_to_process",
    "usedtoanalyze": "used_to_analyze",
    "recordedby": "recorded_by",
    "trainedon": "trained_on",
    "evaluatedon": "evaluated_on",
    "other": "other",
}


# reusability.stewardship.level — v1 camelCase → v1.2 Title_Case
_STEWARDSHIP_LEVEL_MAP = {
    "projectmanaged": "Project_Managed",
    "repositorymanaged": "Repository_Managed",
    "externallymanaged": "Externally_Managed",
    "not_applicable": "not_applicable",
}


# reusability.stewardship.update_frequency
_UPDATE_FREQ_MAP = {
    "none": "None",
    "adhoc": "Ad_Hoc",
    "ad_hoc": "Ad_Hoc",
    "monthly": "Monthly",
    "quarterly": "Quarterly",
    "annually": "Annually",
    "continuously": "Continuously",
    "other": "Other",
}


def _map_auth(v1_auth: str | None) -> list[str]:
    """Map a v1 authorization string to v1.2 authorization_required list."""
    if not v1_auth or not isinstance(v1_auth, str):
        return []
    key = re.sub(r"[^a-z0-9]", "", v1_auth.lower())
    if key in _AUTH_MAP:
        return [_AUTH_MAP[key]]
    return ["Other"]


def _map_relationship(v1_rel: str | None, default: str = "references") -> str:
    """Map v1 camelCase relationship to v1.2 snake_case enum. Default: references."""
    if not v1_rel or not isinstance(v1_rel, str):
        return default
    key = re.sub(r"[^a-z0-9]", "", v1_rel.lower())
    return _RELATIONSHIP_MAP.get(key, default)


def _infer_id_type_from_value(value: str, allowed: tuple[str, ...] = ("doi", "arxiv", "url")) -> str:
    """Infer identifier type from URL patterns (doi.org → doi, arxiv → arxiv)."""
    if not isinstance(value, str):
        return "url"
    v = value.lower()
    if "doi" in allowed and ("doi.org" in v or v.startswith("10.")):
        return "doi"
    if "arxiv" in allowed and "arxiv" in v:
        return "arxiv"
    return "url"


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
    """Map a single v1 role string to a list of v2 CRediT taxonomy values.

    Returns a fresh list per call so downstream YAML dumping doesn't emit
    ``&anchor``/``*alias`` references (which happens when the same list object
    appears at multiple sites — e.g., every "creator" author sharing the
    ``[Conceptualization, Methodology]`` list).
    """
    if not v1_role:
        return ["Other"]
    return list(_CREDIT_ROLE_MAP.get(v1_role.lower(), ["Other"]))


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


# ---------- v1 rich-schema → thin-schema normalization ----------

_RICH_TO_THIN_ALIASES = {
    "dataset_authors": "authors",
    "dataset_contributors": "contributors",
    "contact_point": "contact",
}


def _normalize_v1(v1: dict) -> dict:
    """Rewrite v1-rich shape into v1-thin so existing handlers process it.

    Handles: datacard_info wrapper hoist; dataset_authors/contributors/
    contact_point → thin aliases; entity-wrapper peeling on people;
    originating_research_organization (single) → research_organizations (list);
    fundings → sponsor_organizations with hoisted funder org.

    Rich→thin dropping: if both a rich and a thin key are present, the thin
    wins (rich is dropped). This keeps the thin-fixture path bit-for-bit
    identical.
    """
    v = dict(v1)

    # Hoist datacard_info.* → top-level. Prefer datacard_info values over
    # top-level ones only when the top-level is unset OR empty (e.g., a bare
    # ``id:`` line with no type/value — real MODCON v1 files often have both).
    if isinstance(v.get("datacard_info"), dict):
        di = v.pop("datacard_info")
        for k in ("filename", "id", "datacard_access", "language", "datacard_template_version"):
            if k not in di:
                continue
            top_val = v.get(k)
            is_empty_top = (
                top_val is None
                or (isinstance(top_val, dict) and not any(top_val.values()))
                or top_val == ""
            )
            if is_empty_top:
                v[k] = di[k]
        if "datacard_creation" in di and "datacard_creation" not in v:
            v["datacard_creation"] = di["datacard_creation"]

    # Normalize datacard_creation.update_date → updated_date; unwrap
    # datacard_contact_organization/person shapes inside created_by.
    if isinstance(v.get("datacard_creation"), dict):
        dcc = dict(v["datacard_creation"])
        if "update_date" in dcc and "updated_date" not in dcc:
            dcc["updated_date"] = dcc.pop("update_date")
        if isinstance(dcc.get("created_by"), list):
            normalized = []
            for cb in dcc["created_by"]:
                if not isinstance(cb, dict):
                    continue
                if "datacard_contact_organization" in cb:
                    inner = cb["datacard_contact_organization"] or {}
                    if inner.get("organization_name") or inner.get("name"):
                        normalized.append({"type": "organization", "organization": dict(inner)})
                elif "datacard_contact_person" in cb:
                    inner = cb["datacard_contact_person"] or {}
                    if inner.get("given_name") or inner.get("name"):
                        normalized.append({"type": "person", "person": dict(inner)})
                else:
                    normalized.append(cb)
            dcc["created_by"] = normalized
        v["datacard_creation"] = dcc

    # Alias renames (thin wins if both present)
    for rich, thin in _RICH_TO_THIN_ALIASES.items():
        if rich in v and thin not in v:
            v[thin] = v.pop(rich)
        elif rich in v:
            del v[rich]

    # Entity-unwrap on authors/contributors/contact/additional_contacts
    for key in ("authors", "contributors"):
        if isinstance(v.get(key), list):
            v[key] = [_normalize_person_entry(e) for e in v[key]]
    if isinstance(v.get("contact"), dict):
        v["contact"] = _normalize_person_entry(v["contact"])
    if isinstance(v.get("additional_contacts"), list):
        v["additional_contacts"] = [_normalize_person_entry(e) for e in v["additional_contacts"]]

    # originating_research_organization (single, with entity wrapper) → list
    if "originating_research_organization" in v and "research_organizations" not in v:
        oro = _unwrap_entity(v.pop("originating_research_organization"))
        if isinstance(oro, dict) and "organization" in oro:
            org_dict = _organization_from_v1(oro["organization"] or {})
            if org_dict:
                v["research_organizations"] = [org_dict]

    # fundings → sponsor_organizations (hoist funder org.name/ror_id to entry level)
    if "fundings" in v and "sponsor_organizations" not in v:
        f_list = v.pop("fundings") or []
        sponsors = []
        for f in f_list:
            funding = (f or {}).get("funding", {}) or {}
            funder = _unwrap_entity(funding.get("funder", {}) or {})
            org = funder.get("organization", {}) or {}
            entry = _organization_from_v1(org)
            if funding.get("award_number"):
                entry["award_number"] = funding["award_number"]
            if funding.get("program"):
                entry["program"] = funding["program"]
            if entry:
                sponsors.append(entry)
        if sponsors:
            v["sponsor_organizations"] = sponsors

    # facilities: entity-unwrap each entry, hoist organization fields
    if isinstance(v.get("facilities"), list):
        v["facilities"] = [
            _organization_from_v1((_unwrap_entity(f) or {}).get("organization", {}) or {})
            for f in v["facilities"]
        ]
        v["facilities"] = [f for f in v["facilities"] if f]

    return v


# ---------- supports_* flag inference ----------

def _infer_supports(v1: dict) -> dict[str, str]:
    """Infer v2 supports_* capability flags from v1 content.

    Sees both thin-schema (v1 fixture) and rich-schema (real MODCON v1) keys.
    """
    supports: dict[str, str] = {}
    supports["supports_discoverability"] = "Yes"  # always Yes per schema
    supports["supports_accessibility"] = (
        "Yes" if (v1.get("dataset_counts") or v1.get("dataset_storage") or v1.get("access_policy"))
        else "No"
    )
    supports["supports_interoperability"] = (
        "Yes" if (v1.get("dataset_info") or v1.get("dataset_provenance")
                  or v1.get("dates") or v1.get("semantic_layer")
                  or v1.get("related_resources"))
        else "No"
    )
    supports["supports_reusability"] = (
        "Yes" if (v1.get("license") or v1.get("citation") or v1.get("stewardship")
                  or v1.get("data_quality") or v1.get("integrity")
                  or v1.get("additional_licenses") or v1.get("maintenance"))
        else "No"
    )
    supports["supports_governed_use"] = (
        "Yes" if (v1.get("security") or v1.get("compliance") or v1.get("reviews")
                  or v1.get("security_marking") or v1.get("review_process"))
        else "No"
    )
    supports["supports_ai_usability"] = "Yes" if v1.get("ai_usage") else "No"
    return supports


# ---------- Main conversion ----------

def convert(v1_raw: dict) -> ConversionReport:  # noqa: C901 (complexity OK for a mapper)
    # Normalize v1-rich shape (real MODCON v1 files) to v1-thin so downstream
    # handlers work uniformly. Rich keys like dataset_authors, contact_point,
    # fundings, originating_research_organization, datacard_info wrappers, and
    # entity-wrapped author entries are all unwrapped/aliased here. The thin
    # fixture path is unaffected (aliases only fire when a rich key is present
    # AND its thin equivalent is not).
    v1 = _normalize_v1(v1_raw)
    # Track which raw v1 keys were folded away by the normalizer so they don't
    # appear as orphans in the final report.
    consumed_by_normalizer = {
        k for k in v1_raw
        if k in ("datacard_info", "dataset_authors", "dataset_contributors",
                 "contact_point", "originating_research_organization", "fundings")
    }

    today = date.today().isoformat()
    g: dict = {}
    consumed: set[str] = set(consumed_by_normalizer)
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
    # updated_date is if_applicable, not required — leave unset on initial
    # creation (see SKILL.md Gotcha #16). Only carry it forward if the
    # source v1 card already had one; the change_log entry below captures
    # the conversion date regardless.
    v1_updated_date = creation.get("updated_date") or v1.get("updated_date")
    if v1_updated_date:
        _setp(g, "discoverability.datacard.updated_date", v1_updated_date)
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
        # dataset_counts: thin uses record_count/record_unit; rich uses value/category
        # (with a freetext ``unit`` note). Accept either.
        record_count = dc.get("record_count") if dc.get("record_count") is not None else dc.get("value")
        record_unit = dc.get("record_unit") or dc.get("category")
        if record_count is not None:
            _setp(g, "accessibility.dataset_scale.record_count", record_count)
        if record_unit:
            _setp(g, "accessibility.dataset_scale.record_unit", record_unit)
        if ds.get("compressed_bytes") is not None:
            _setp(g, "accessibility.dataset_scale.compressed_bytes", ds["compressed_bytes"])
        # rich: unpacked_bytes; thin: uncompressed_bytes
        uncompressed = (ds.get("uncompressed_bytes")
                        if ds.get("uncompressed_bytes") is not None
                        else ds.get("unpacked_bytes"))
        if uncompressed is not None:
            _setp(g, "accessibility.dataset_scale.uncompressed_bytes", uncompressed)
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
            if l_v1.get("name"):
                _setp(g, "reusability.license.name", l_v1["name"])
            # rich uses ``link``; thin/v1.2 use ``url``
            license_url = l_v1.get("url") or l_v1.get("link")
            if license_url:
                _setp(g, "reusability.license.url", license_url)
    if v1.get("license"):
        consumed.add("license")
    if v1.get("citation"):
        consumed.add("citation")

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

    # =====================================================================
    # Rich-schema block mappings (Category A/B/C from converter expansion)
    # These handle keys the thin fixture doesn't have. Each block is guarded
    # by a v1.get(key) check so it's a silent no-op when the source uses the
    # thin schema.
    # =====================================================================

    # --- datacard.filename / id / language (from hoisted datacard_info) ----
    if v1.get("filename"):
        # The schema requires the ``genesis_datacard_*`` prefix. Rewrite the
        # MODCON-era prefix so validation doesn't hard-fail on carried-over
        # filenames. The extras layer will still emit a warn if the snake_case
        # name doesn't match identification.name.
        fname = str(v1["filename"])
        fname = re.sub(r"^modcon_datacard_", "genesis_datacard_", fname)
        if not fname.startswith("genesis_datacard_"):
            fname = "genesis_datacard_" + fname.lstrip("_")
        _setp(g, "discoverability.datacard.filename", fname)
        consumed.add("filename")
    if v1.get("id"):
        # id here is the datacard's own id (from hoisted datacard_info.id),
        # not the dataset id. Dataset id lives in identification.primary_id.
        # Only accept a mapping shape — bare top-level id: (empty) is meaningless.
        if isinstance(v1["id"], dict) and (v1["id"].get("type") or v1["id"].get("value")):
            _setp(g, "discoverability.datacard.id", {
                "type": (v1["id"].get("type") or "url").lower(),
                "value": v1["id"].get("value", ""),
            })
        consumed.add("id")
    if v1.get("language"):
        _setp(g, "discoverability.datacard.language", v1["language"])
        consumed.add("language")
    if v1.get("datacard_template_version"):
        # v1.2 datacard.template_version is fixed at "1.2"; the source
        # template_version is informational only. Consumed but not mapped.
        consumed.add("datacard_template_version")
    if v1.get("datacard_access"):
        # No direct target; access details live in accessibility.access_policy.
        consumed.add("datacard_access")

    # --- identification.name fallback from data_identifiers.name -----------
    if isinstance(v1.get("data_identifiers"), dict):
        di = v1["data_identifiers"]
        if di.get("name") and "identification.name" not in _flatten_keys(g.get("discoverability", {}), "identification"):
            if not (g.get("discoverability", {}).get("identification", {}).get("name")):
                _setp(g, "discoverability.identification.name", di["name"])
        # identification.primary_id
        if isinstance(di.get("dataset_id"), dict):
            did = di["dataset_id"]
            if did.get("type") or did.get("value"):
                _setp(g, "discoverability.identification.primary_id", {
                    "type": (did.get("type") or "url").lower(),
                    "value": did.get("value", ""),
                })
        consumed.add("data_identifiers")

    # --- identification.additional_ids from top-level identifiers[] --------
    if isinstance(v1.get("identifiers"), list) and v1["identifiers"]:
        # Dedup: MODCON v1 often lists the primary dataset URL in both
        # data_identifiers.dataset_id (→ primary_id) and identifiers[0].
        # Drop additional_ids entries whose value equals the primary_id value.
        primary_val = (
            g.get("discoverability", {}).get("identification", {})
             .get("primary_id", {}).get("value")
        )
        addl = []
        for ident in v1["identifiers"]:
            if not isinstance(ident, dict):
                continue
            val = ident.get("value")
            if not val or val == primary_val:
                continue
            declared_type = (ident.get("type") or "").lower()
            inferred = _infer_id_type_from_value(val)
            id_type = inferred if declared_type in ("url", "", None) else declared_type
            addl.append({"type": id_type, "value": val})
        if addl:
            _setp(g, "discoverability.identification.additional_ids", addl)
        consumed.add("identifiers")

    # --- additional_contacts (list of person entries) ----------------------
    if isinstance(v1.get("additional_contacts"), list):
        ac_out = []
        for ac in v1["additional_contacts"]:
            if isinstance(ac, dict) and "person" in ac:
                ac_out.append({"person": _person_from_v1(ac["person"])})
        if ac_out:
            _setp(g, "discoverability.additional_contacts", ac_out)
        consumed.add("additional_contacts")

    # --- facilities (already normalized to flat list of orgs) --------------
    if isinstance(v1.get("facilities"), list) and v1["facilities"]:
        _setp(g, "discoverability.facilities", v1["facilities"])
        consumed.add("facilities")

    # --- accessibility.access_policy ---------------------------------------
    if isinstance(v1.get("access_policy"), dict):
        ap = v1["access_policy"]
        access_out: dict[str, Any] = {}
        if ap.get("access_level"):
            access_out["access_level"] = _titlecase(ap["access_level"])
        auth = _map_auth(ap.get("authorization"))
        if auth:
            access_out["authorization_required"] = auth
        if ap.get("policy_url"):
            access_out["policy_url"] = ap["policy_url"]
        if ap.get("policy_text"):
            access_out["policy_text"] = ap["policy_text"]
        if access_out:
            _setp(g, "accessibility.access_policy", access_out)
        consumed.add("access_policy")

    # --- interoperability.provenance ---------------------------------------
    if isinstance(v1.get("dataset_provenance"), dict):
        dp = v1["dataset_provenance"]
        prov: dict[str, Any] = {}
        if dp.get("was_generated_by"):
            prov["was_generated_by"] = dp["was_generated_by"]
        # v1 source_data is freetext; v1.2 wants list of {name, identifier, relationship}.
        # ``identifier`` is schema-required per entry; fill with a not_applicable
        # local placeholder when the source only gave freetext.
        sd = dp.get("source_data")
        if isinstance(sd, str) and sd.strip():
            prov["source_data"] = [{
                "name": sd.strip(),
                "identifier": {"type": "local", "value": "not_applicable"},
                "relationship": "other",
            }]
        elif isinstance(sd, list) and sd:
            prov["source_data"] = sd
        if dp.get("processing_steps"):
            prov["processing_steps"] = dp["processing_steps"]
        if dp.get("instrumentation"):
            prov["instrumentation"] = dp["instrumentation"]
        if dp.get("simulation_details"):
            prov["simulation_details"] = dp["simulation_details"]
        if prov:
            _setp(g, "interoperability.provenance", prov)
        consumed.add("dataset_provenance")

    # --- interoperability.dates --------------------------------------------
    if isinstance(v1.get("dates"), dict):
        dates_out = {k: v for k, v in v1["dates"].items() if v}
        if dates_out:
            _setp(g, "interoperability.dates", dates_out)
        consumed.add("dates")

    # --- interoperability.semantic_layer -----------------------------------
    if isinstance(v1.get("semantic_layer"), dict):
        sl = v1["semantic_layer"]
        sl_out: dict[str, Any] = {}
        if sl.get("schema_url"):
            sl_out["schema_url"] = sl["schema_url"]
        # Merge semantic_context + controlled_vocabularies into semantic_context
        ctx_list = []
        for k in ("semantic_context", "controlled_vocabularies"):
            if isinstance(sl.get(k), list):
                ctx_list.extend(sl[k])
        if ctx_list:
            sl_out["semantic_context"] = ctx_list
        if sl_out:
            _setp(g, "interoperability.semantic_layer", sl_out)
        consumed.add("semantic_layer")

    # --- interoperability.related_resources (with publications fan-out) ----
    if isinstance(v1.get("related_resources"), dict):
        rr = v1["related_resources"]
        rr_out: dict[str, Any] = {}
        # related_datasets → datasets (dataset_name→name, identifiers[0]→identifier)
        if isinstance(rr.get("related_datasets"), list):
            ds_out = []
            for rd in rr["related_datasets"]:
                if not isinstance(rd, dict):
                    continue
                ds_entry: dict[str, Any] = {}
                if rd.get("dataset_name") or rd.get("name"):
                    ds_entry["name"] = rd.get("dataset_name") or rd["name"]
                idents = rd.get("identifiers") or []
                if idents and isinstance(idents[0], dict):
                    first = idents[0]
                    ds_entry["identifier"] = {
                        "type": (first.get("type") or "url").lower(),
                        "value": first.get("value", ""),
                    }
                ds_entry["relationship"] = _map_relationship(rd.get("relationship"))
                ds_out.append(ds_entry)
            if ds_out:
                rr_out["datasets"] = ds_out
        # publications: fan out dois/arxiv/urls to unified list. Schema enum
        # doesn't include 'arxiv' — emit as url pointing to the arxiv abs page.
        pubs = rr.get("publications")
        if isinstance(pubs, dict):
            pub_out = []
            for doi in pubs.get("dois", []) or []:
                pub_out.append({"type": "doi", "value": doi, "relationship": "references"})
            for arx in pubs.get("arxiv", []) or []:
                arx_url = arx if str(arx).startswith("http") else f"https://arxiv.org/abs/{arx}"
                pub_out.append({"type": "url", "value": arx_url, "relationship": "references"})
            for url in pubs.get("urls", []) or []:
                pub_out.append({"type": "url", "value": url, "relationship": "references"})
            if pub_out:
                rr_out["publications"] = pub_out
        elif isinstance(pubs, list):
            rr_out["publications"] = pubs
        # software: identifiers[0]→identifier; software.relationship uses a
        # DIFFERENT enum than datasets/publications
        # (used_to_create | used_to_process | used_to_analyze | recorded_by |
        # trained_on | evaluated_on). Default to used_to_analyze if the v1
        # value doesn't map cleanly.
        _SW_ENUM = {"used_to_create", "used_to_process", "used_to_analyze",
                    "recorded_by", "trained_on", "evaluated_on"}
        if isinstance(rr.get("software"), list):
            sw_out = []
            for sw in rr["software"]:
                if not isinstance(sw, dict):
                    continue
                sw_entry: dict[str, Any] = {"name": sw.get("name", "")}
                if sw.get("version"):
                    sw_entry["version"] = sw["version"]
                idents = sw.get("identifiers") or []
                if idents and isinstance(idents[0], dict):
                    first = idents[0]
                    sw_entry["identifier"] = {
                        "type": (first.get("type") or "url").lower(),
                        "value": first.get("value", ""),
                    }
                rel = _map_relationship(sw.get("relationship"), default="used_to_analyze")
                sw_entry["relationship"] = rel if rel in _SW_ENUM else "used_to_analyze"
                sw_out.append(sw_entry)
            if sw_out:
                rr_out["software"] = sw_out
        # aimodels → ai_models (rename key; direct passthrough of items)
        if isinstance(rr.get("aimodels"), list):
            rr_out["ai_models"] = rr["aimodels"]
        elif isinstance(rr.get("ai_models"), list):
            rr_out["ai_models"] = rr["ai_models"]
        if rr_out:
            _setp(g, "interoperability.related_resources", rr_out)
        consumed.add("related_resources")

    # --- reusability.data_quality ------------------------------------------
    if isinstance(v1.get("data_quality"), dict):
        dq = v1["data_quality"]
        dq_out: dict[str, Any] = {}
        for k in ("completeness", "known_issues", "validation_methods",
                  "noise_characteristics", "uncertainty_notes"):
            if dq.get(k):
                dq_out[k] = dq[k]
        if isinstance(dq.get("missing_data_codes"), list):
            dq_out["missing_data_codes"] = dq["missing_data_codes"]
        if dq_out:
            _setp(g, "reusability.data_quality", dq_out)
        consumed.add("data_quality")

    # --- reusability.additional_licenses -----------------------------------
    if isinstance(v1.get("additional_licenses"), list) and v1["additional_licenses"]:
        al_out = []
        for al in v1["additional_licenses"]:
            if not isinstance(al, dict):
                continue
            al_entry: dict[str, Any] = {}
            if al.get("spdx_id"):
                al_entry["spdx_id"] = al["spdx_id"]
            if al.get("name"):
                al_entry["name"] = al["name"]
            url = al.get("url") or al.get("link")
            if url:
                al_entry["url"] = url
            # 'note' → known_contractual_rights (only extra-text slot on License schema)
            if al.get("note"):
                al_entry["known_contractual_rights"] = al["note"]
            if al_entry:
                al_out.append(al_entry)
        if al_out:
            _setp(g, "reusability.additional_licenses", al_out)
        consumed.add("additional_licenses")

    # --- reusability.integrity + stewardship.versioning_strategy -----------
    if isinstance(v1.get("integrity"), dict):
        integ = v1["integrity"]
        integ_out: dict[str, Any] = {}
        if integ.get("checksum_available") is not None:
            integ_out["checksum_available"] = _map_yes_no(integ["checksum_available"]) or "No"
        if integ.get("checksum_type"):
            integ_out["checksum_type"] = integ["checksum_type"]
        if integ.get("checksum_value"):
            integ_out["checksum_value"] = integ["checksum_value"]
        if integ.get("fixity_policy"):
            integ_out["fixity_policy"] = integ["fixity_policy"]
        if integ_out:
            _setp(g, "reusability.integrity", integ_out)
        # versioning_strategy in v1.2 lives under stewardship, not integrity
        if integ.get("versioning_strategy"):
            _setp(g, "reusability.stewardship.versioning_strategy",
                  integ["versioning_strategy"])
        consumed.add("integrity")

    # --- reusability.stewardship (level from stewardship + freq from maintenance) ---
    if isinstance(v1.get("stewardship"), dict):
        st = v1["stewardship"]
        if st.get("level"):
            key = re.sub(r"[^a-z0-9_]", "", st["level"].lower())
            mapped_level = _STEWARDSHIP_LEVEL_MAP.get(key)
            if mapped_level:
                _setp(g, "reusability.stewardship.level", mapped_level)
        consumed.add("stewardship")
    if isinstance(v1.get("maintenance"), dict):
        mt = v1["maintenance"]
        if mt.get("update_frequency"):
            key = re.sub(r"[^a-z0-9_]", "", mt["update_frequency"].lower())
            mapped_freq = _UPDATE_FREQ_MAP.get(key)
            if mapped_freq:
                _setp(g, "reusability.stewardship.update_frequency", mapped_freq)
        if mt.get("retention_policy"):
            _setp(g, "reusability.stewardship.retention_policy", mt["retention_policy"])
        consumed.add("maintenance")

    # --- dataset_description task_category / task_subcategory --------------
    if isinstance(v1.get("categorization"), dict):
        cat = v1["categorization"]
        if isinstance(cat.get("task_category"), list) and cat["task_category"]:
            _setp(g, "discoverability.dataset_description.task_category", cat["task_category"])
        if isinstance(cat.get("task_subcategory"), list) and cat["task_subcategory"]:
            _setp(g, "discoverability.dataset_description.task_subcategory",
                  cat["task_subcategory"])
        # 'categorization' already consumed above by the science_domain handler,
        # but re-adding to consumed is idempotent.
        consumed.add("categorization")

    # --- governed_use.review_provenance_companion (from review_process) ----
    if isinstance(v1.get("review_process"), dict):
        rp = v1["review_process"]
        # source_review_reference is schema-required; v1 review_process has no
        # equivalent slot, so default to "other" (user can retype to
        # internal_qa | security | export_control | irb | partner | publication).
        entry: dict[str, Any] = {"source_review_reference": "other"}
        if rp.get("review_purpose"):
            entry["review_purpose"] = rp["review_purpose"]
        if isinstance(rp.get("review_institution"), dict):
            ri = rp["review_institution"]
            if ri.get("name"):
                # AgentClass has no discriminator field — see _make_agent
                entry["reviewed_by"] = _make_agent("organization", _organization_from_v1(ri))
        if rp.get("review_comments"):
            entry["comments"] = rp["review_comments"]
        if len(entry) > 1:  # more than just the source_review_reference default
            _setp(g, "governed_use.review_provenance_companion", [entry])
        consumed.add("review_process")

    # --- discoverability.sensitivity (from security_marking + access_policy) ---
    # Category C: best-effort derivation. Only fires when security_marking is
    # present; if only access_policy.sensitivity_tier is available, we still
    # capture that as overall_sensitivity.
    if isinstance(v1.get("security_marking"), dict) or (
        isinstance(v1.get("access_policy"), dict) and v1["access_policy"].get("sensitivity_tier")
    ):
        sm = v1.get("security_marking") or {}
        ap = v1.get("access_policy") or {}
        classification = (sm.get("classification") or "").lower().strip()
        cui_marking = sm.get("cui_marking")
        tier = (ap.get("sensitivity_tier") or "").lower().strip()

        sens_out: dict[str, Any] = {}
        # overall_sensitivity: derive from classification / tier
        if classification == "unclassified" or tier == "tier0":
            sens_out["overall_sensitivity"] = "Public"
        elif classification in ("confidential", "secret", "top_secret"):
            sens_out["overall_sensitivity"] = "Classified"
        elif cui_marking:
            sens_out["overall_sensitivity"] = "CUI"
        # classified_status
        if classification == "unclassified":
            sens_out["classified_status"] = "No"
        elif classification in ("confidential", "secret", "top_secret"):
            sens_out["classified_status"] = "Yes"
            sens_out["classification_level"] = classification.title().replace(" ", "_")
        # cui_status: presence of cui_marking → Yes; explicit absence → No
        if cui_marking:
            sens_out["cui_status"] = "Yes"
        elif "cui_marking" in sm:
            sens_out["cui_status"] = "No"
        # ucni_status default: No if unclassified/public
        if sens_out.get("overall_sensitivity") == "Public":
            sens_out["ucni_status"] = "No"
        # source_marking_string/scheme are schema-required. For unclassified
        # data with no source marking, "None" is the correct schema-valid
        # value (source_marking_scheme enum includes "None"). Leave unset
        # when we don't know — user must fill in.
        if sens_out.get("overall_sensitivity") == "Public":
            sens_out.setdefault("source_marking_string", "None")
            sens_out.setdefault("source_marking_scheme", "None")
        if sens_out:
            _setp(g, "discoverability.sensitivity", sens_out)
        # Consume security_marking and its top-level duplicates
        for k in ("security_marking", "distribution_statement",
                  "handling_instructions", "cui_markings"):
            if k in v1:
                consumed.add(k)

    # --- Silently drop reference-only rich-schema keys ---------------------
    # repository_access is marked [reference_only_do_not_include] in v1.2:
    # the managing repository populates it at ingest.
    if v1.get("repository_access"):
        consumed.add("repository_access")

    # --- dataset_readiness: dropped in v2 (orphan with explanation) ---
    if v1.get("dataset_readiness"):
        consumed.add("dataset_readiness")
        # will appear in orphans list with note below

    # --- Compute outputs ---
    mapped = sorted(_flatten_keys(g))

    # Orphans: raw v1 keys the converter didn't touch. Use v1_raw (pre-normalization)
    # so rich-schema key names appear if they weren't consumed. Keys hoisted by
    # the normalizer (datacard_info, dataset_authors, etc.) are pre-added to
    # `consumed` via `consumed_by_normalizer`.
    raw_orphans = sorted(k for k in v1_raw if k not in consumed)
    orphans: list[str] = list(raw_orphans)
    # dataset_readiness was consumed above but has no v2 home — add a note
    if "dataset_readiness" in v1_raw:
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


def _v1_body(src_path: Path) -> str:
    """Return the markdown body (post-frontmatter) of a v1 datacard file, or '' if none."""
    text = src_path.read_text(encoding="utf-8")
    parts = re.split(r"^---\s*$", text, maxsplit=2, flags=re.MULTILINE)
    return parts[2] if len(parts) >= 3 else ""


def write_genesis_file(
    report: ConversionReport,
    out_path: Path,
    src_path: Path | None = None,
    preserve_body: bool = False,
) -> None:
    """Render the Genesis dict as YAML frontmatter + the canonical template body.

    When ``preserve_body`` is True and ``src_path`` is given, the source v1 body
    is appended after the template body as ``## Legacy v1 body (unmerged)`` so
    the user can migrate prose manually. Default behaviour (flag off) is unchanged.
    """
    template_path = SKILL_ROOT / "references" / "genesis_v1.0_template.md"
    template_text = template_path.read_text()
    parts = re.split(r"^---\s*$", template_text, maxsplit=2, flags=re.MULTILINE)
    body = parts[2] if len(parts) >= 3 else ""

    # Force no `&anchor`/`*alias` refs in output: any shared list/dict object
    # (e.g., identical CRediT role lists across authors) would otherwise emit
    # as aliases and break parsers that don't resolve them.
    class _NoAliasDumper(yaml.SafeDumper):
        def ignore_aliases(self, data):  # type: ignore[override]
            return True

    yaml_block = yaml.dump(
        report.genesis, Dumper=_NoAliasDumper,
        sort_keys=False, allow_unicode=True, default_flow_style=False,
    )
    if preserve_body and src_path is not None:
        legacy = _v1_body(src_path).strip()
        if legacy:
            body = (body.rstrip() + "\n\n---\n\n## Legacy v1 body (unmerged)\n\n"
                    "> The following prose was carried over from the source v1 datacard.\n"
                    "> Migrate content into the appropriate sections above, then delete this appendix.\n\n"
                    + legacy + "\n")
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
    parser.add_argument("--preserve-body", action="store_true",
                        help="Append the source v1 markdown body as a "
                             "`## Legacy v1 body (unmerged)` appendix so prose "
                             "can be migrated manually. Default: drop v1 body "
                             "and use the empty Genesis template body.")
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
    write_genesis_file(report, out, src_path=args.file, preserve_body=args.preserve_body)
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
