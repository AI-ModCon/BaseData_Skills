# Validation & Lookup Reference

When the user provides ORCID, ROR, or funding identifiers, validate the format and attempt live enrichment via the APIs below. Use the `WebFetch` tool for all API calls.

---

## ORCID

### Format Validation

An ORCID must match: `^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$`

Examples of valid forms the user may provide:
- `0000-0001-5000-0007` — bare ID (preferred in YAML)
- `https://orcid.org/0000-0001-5000-0007` — full URL (strip prefix before storing)

**Checksum (ISO 7064 MOD 11-2):** Take the first 15 digits, run the algorithm below, compare to the 16th character (which may be `X` = 10).

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
Use the most recent employment's `organization.name` and `organization.disambiguated-organization.disambiguated-organization-identifier` (if type is `ROR`, use it directly).

**Present confirmed values to the user before writing them to the card.**

---

## ROR

### Format Validation

A ROR identifier in this skill is stored in **URL form** to match the Genesis template's documented convention (`Format: https://ror.org/XXXXXXX`). The full URL must match: `^https://ror\.org/[0-9a-z]{9}$`

Valid forms:
- `https://ror.org/03yrm5c26` — full URL (canonical for Genesis datacards)
- `03yrm5c26` — bare 9-character ID; prepend `https://ror.org/` before storing

### Live Lookup

The ROR API expects the bare 9-character ID, not the URL form. Strip the `https://ror.org/` prefix when querying, but **store** the URL form in the datacard.

```
GET https://api.ror.org/organizations/{bare_id}
```

On success, extract:
- `name` → `organization.name`
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
- `sponsor_org` → `fundings[].funder.organization.name`
- `award_number` → `fundings[].award_number`
- `contract_number` → `fundings[].award_number` (fallback)
- `research_org` → `originating_research_organization.organization.name`
- `site_url` / `doi` → cross-check against `data_identifiers`

### Lookup by DOI

If the dataset already has a DOI:
```
GET https://www.osti.gov/api/v1/datasets?doi={doi}
```

On success, also extract:
- `title` — cross-check against `data_identifiers.name`
- `authors[].first_name` + `authors[].last_name` — cross-check or pre-fill `dataset_authors`
- `description` — can seed the dataset description if none exists
- `publication_date` → `dates.issued`
- `keywords[]` → keywords

### Lookup by Site/Landing Page URL

```
GET https://www.osti.gov/api/v1/datasets?site_url={encoded_url}
```

### Usage Notes

- OSTI records are DOE-funded work. If there is no match, the dataset may not be DOE-funded or may not yet be registered — inform the user rather than leaving the field blank silently.
- Award numbers follow no single format: `DE-SC0012345`, `DE-AC02-06CH11357`, `89243021CSC000001` are all valid DOE patterns.
- If multiple records match an award number, present the list to the user and ask them to confirm which applies.
- The OSTI API returns JSON by default; no API key is required for read access.
