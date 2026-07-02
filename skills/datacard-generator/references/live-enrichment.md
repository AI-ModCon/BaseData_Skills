# Live Enrichment Reference

**This step is not optional.** SKILL.md workflow step 7 is a required stop.
Skipping enrichment produces datacards where a typo'd ORCID resolves to the
wrong human and no one catches it until publication. The API round-trips
cost a handful of seconds; that's cheaper than a wrong-authorship
correction post-publication.

The skill's workflow step 7 ("Cross-check identifiers via live APIs") resolves every ORCID, ROR, DOI, and OSTI award number in the datacard against its public API — **even when the user already provided a value**. The goal is two-fold: (1) fill missing fields the authoritative source has (affiliations, names, emails), and (2) catch mistyped identifiers that would otherwise resolve to the wrong entity or 404 silently. This file is the agent's guide to those APIs. Use the `WebFetch` tool for all live calls.

Treat every resolved value as a candidate for cross-check, not as authoritative. When the API returns a value that conflicts with the datacard, **present both to the user** rather than silently overwriting.

**Format validation** (ORCID/ROR regex patterns) lives in `references/genesis_datacard.schema.json` (e.g. the `orcid` and `ror_id` field `pattern` entries) and is enforced automatically by `scripts/validate_datacard.py`. `references/validation-rules.md` covers only the warn-level extras JSON Schema can't express (filename alignment, workflow↔release_status alignment). This doc covers the unique value-add: checksum verification, live API endpoints, and DOE-specific OSTI guidance.

---

## Identifier paths to check (by capability)

Enrich every path below that is present in the datacard. The list is
grouped by capability so you can skip capabilities the user opted out of
(`supports_X = No`).

**`discoverability` (always present):**

- Every `discoverability.authors[].person.orcid` and `…person.affiliation.ror_id`
- Every `discoverability.authors[].organization.ror_id`
- Every `discoverability.contributors[].person.orcid` and `…ror_id`
- `discoverability.contact.person.orcid` and `…ror_id`
- Every `discoverability.additional_contacts[].person.orcid` and `…ror_id`
- Every `discoverability.sponsor_organizations[].ror_id` and `…award_number` (the latter via OSTI)
- Every `discoverability.research_organizations[].ror_id`
- Every `discoverability.facilities[].ror_id` and `…location.ror_id`
- `discoverability.identification.primary_id.value` (if `type: doi`)
- Every `discoverability.identification.additional_ids[].value` of type `doi`

**`reusability` (when `supports_reusability=Yes`):**

- `reusability.stewardship.maintainer.person.orcid` and `…ror_id`

**`governed_use` (when `supports_governed_use=Yes`):**

- Every `governed_use.review_provenance_companion[].reviewed_by.person.orcid`

**`interoperability` (when `supports_interoperability=Yes`):**

- Every `interoperability.related_resources.datasets[].identifier.value` (if `type: doi`)
- Every `interoperability.related_resources.publications[].value` (if `type: doi` or `arxiv`)

For each lookup, classify the outcome as one of: **Clean match** (silent
pass), **Mismatch** (present both side-by-side, ask the user), **Datacard
incomplete** (API has fields the datacard doesn't; offer to add), **Does
not resolve** (404/error; warn the user — likely typo), or **Rate-limited**
(retry once; if still failing, log and move on).

---

## ORCID

### Checksum verification (ISO 7064 MOD 11-2)

Before calling the API, you can self-check an ORCID without a network round-trip. Take the first 15 digits, run the algorithm below, and compare to the 16th character (which may be `X` = 10).

```
total = 0
for each of the first 15 digits d:
    total = (total + d) * 2
remainder = total % 11
result = (12 - remainder) % 11   # 10 → "X", else digit
```

If the checksum fails, warn the user before proceeding.

### Live Lookup

```
GET https://pub.orcid.org/v3.0/{orcid}/person
Headers: Accept: application/json
```

On success, extract:
- `name.given-names.value` → `person.given_name`
- `name.family-name.value` → `person.family_name`
- `emails.email[0].email` → `person.email` (only if visibility = `PUBLIC`)
- `researcher-urls.researcher-url[].url.value` — look for an institutional URL if affiliation is absent

For affiliation, also fetch:
```
GET https://pub.orcid.org/v3.0/{orcid}/employments
Headers: Accept: application/json
```
Use the most recent employment's:
- `organization.name` → `person.affiliation.name`
- `organization.disambiguated-organization.disambiguated-organization-identifier` (if `disambiguated-organization-source` is `ROR`) → `person.affiliation.ror_id` (store in URL form, `https://ror.org/XXXXXXX`)

**Present confirmed values to the user before writing them to the card.**

---

## ROR

### Storage convention

ROR identifiers are stored in **URL form** (`https://ror.org/XXXXXXX`) per the Genesis template. The format regex is in `references/genesis_datacard.schema.json`. When a user provides a bare 9-character ID (e.g., `03yrm5c26`), prepend `https://ror.org/` before storing.

### Live Lookup

The ROR API expects the bare 9-character ID, not the URL form. Strip the `https://ror.org/` prefix when querying, but **store** the URL form in the datacard.

```
GET https://api.ror.org/organizations/{bare_id}
```

On success, extract:
- `name` → the `name` field of whichever sub-block holds this ROR ID — e.g. `person.affiliation.name`, `organization.name`, `discoverability.sponsor_organizations[].name`, `discoverability.research_organizations[].name`, or `discoverability.facilities[].name`
- `country.country_name` — useful context for the user
- `types[]` — e.g., `["Education"]`, `["Government"]`
- `links[0]` — organization homepage

**Present the resolved name to the user for confirmation** — ROR IDs can be mistyped and resolve to the wrong institution.

---

## OSTI

OSTI (Office of Scientific and Technical Information) provides a public REST API for DOE-funded research outputs including datasets, reports, and journal articles. Use it to pre-fill funding and provenance fields.

### Lookup by Award Number

```
GET https://www.osti.gov/api/v1/datasets?award_number={award_number}
Headers: Accept: application/json
```

Or for reports/publications:
```
GET https://www.osti.gov/api/v1/records?award_number={award_number}
```

On success, extract from the first matching record:
- `sponsor_org` → `discoverability.sponsor_organizations[].name`
- `award_number` → `discoverability.sponsor_organizations[].award_number`
- `contract_number` → `discoverability.sponsor_organizations[].award_number` (fallback)
- `research_org` → `discoverability.research_organizations[].name`
- `site_url` / `doi` → cross-check against `discoverability.identification.primary_id.value` and `discoverability.identification.additional_ids[]`

### Lookup by DOI

If the dataset already has a DOI:
```
GET https://www.osti.gov/api/v1/datasets?doi={doi}
```

On success, also extract:
- `title` — cross-check against `discoverability.identification.name`
- `authors[].first_name` + `authors[].last_name` — cross-check or pre-fill `discoverability.authors[]`
- `description` — can seed `discoverability.dataset_description.dataset_summary` if none exists
- `publication_date` → `interoperability.dates.issued` (requires `supports_interoperability=Yes`)
- `keywords[]` → `discoverability.dataset_description.keywords`

Also consider whether the resolved DOI belongs in
`reusability.citation.preferred_citation` (the BibTeX-style block: `doi`,
`title`, `author`, `year`, `publisher`, `url`) if a preferred citation
isn't already set.

### Lookup by Site/Landing Page URL

```
GET https://www.osti.gov/api/v1/datasets?site_url={encoded_url}
```

### Usage Notes

- OSTI records are DOE-funded work. If there is no match, the dataset may not be DOE-funded or may not yet be registered — inform the user rather than leaving the field blank silently.
- Award numbers follow no single format: `DE-SC0012345`, `DE-AC02-06CH11357`, `89243021CSC000001` are all valid DOE patterns.
- If multiple records match an award number, present the list to the user and ask them to confirm which applies.
- The OSTI API returns JSON by default; no API key is required for read access.

---

## Batching guidance

When step 7 runs, resolve ALL identifiers first (batch the WebFetch calls)
THEN present a single consolidated diff table to the user showing every
mismatch, missing-field, and unresolvable ID at once. Do NOT interactively
prompt after each individual lookup — that produces 15+ pauses per
datacard and destroys the user experience.

Consolidated table format:

| Field | Current value | Resolved value | Action |
|---|---|---|---|
| authors[0].person.orcid | 0000-0002-1234-5678 | (name mismatch: J. Doe vs Jane Smith) | Choose which |
| contact.person.affiliation.ror_id | https://ror.org/03yrm5c26 | ✓ resolves to "MIT" | (silent pass) |
| sponsor_organizations[0].award_number | DE-SC0012345 | (not found in OSTI) | Confirm typo? |

## Re-check-only-changed on validation loops

When step 10 (Address findings) loops back to step 7 after re-prompting
for values in step 6: re-enrich ONLY identifiers the user added or changed
in this iteration. Do not re-check every identifier from scratch — that's
wasteful and produces the same passing lookups repeatedly.
