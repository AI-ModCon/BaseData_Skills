# Validation rules

This file is the single source of truth for what fields are required per
profile, what enums fields can take, and what format patterns to enforce.

It is read by `scripts/validate_datacard.py` at runtime via fenced YAML
blocks tagged by their `##` section heading. **Do not change a section
heading or fence language without also updating the parser.**

## Profiles

```yaml
profiles:
  core:
    required:
      - datacard.datacard_version
      - datacard.profile
      - datacard.creation_method
      - datacard.created_date
      - datacard.updated_date
      - datacard.change_log
      - datacard.created_by
      - datacard.filename
      - datacard.language
      - datacard.sensitivity_tier
      - datacard.access_level
      - identification.name
      - identification.project
      - identification.version
      - identification.primary_id.type
      - identification.primary_id.value
      - description.summary
      - description.keywords
      - object_type
      - dataset_type
      - release_status
      - workflow.state
      - security.classification
      - security.sensitivity_tier
      - security.export_control
      - access_policy.sensitivity_tier
      - access_policy.access_level
      - access_policy.authorization_required
      - contact.type
      - categorization.science_domain
      - dataset_info.formats
      - provenance.was_generated_by
      - sponsor_organizations
      - research_organizations
  extended:
    extends: core
    required:
      - dates.data_collection_start
      - dates.data_collection_end
      - security.distribution_statement
      - compliance.doe_data_management_plan
      - compliance.osti_elink2_metadata_compliant
  ai_ready:
    extends: extended
    required:
      - categorization.task_category
      - categorization.task_subcategory
      - ai_usage.ai_ready
      - ai_usage.training_use_allowed
      - ai_usage.inference_use_allowed
      - ai_usage.evaluation_use_allowed
      - ai_usage.human_review_required
      - data_quality.completeness
      - data_quality.known_issues
      - data_quality.validation_methods
      - integrity.checksum_available
  sensitive:
    extends: extended
    required:
      - security.pii.present
      - compliance.export_control_reviewed
      - compliance.irb_approved
      - compliance.security_review_completed
```

Required-field matrix per profile. Sourced from Appendix D of the Genesis
Mission Datacard v1.0 Field Requirements document. Field names use dotted
paths into the YAML frontmatter (e.g., `identification.primary_id.value`).

The `extends:` chain means: profile X's effective required set is the
union of its own `required:` and (recursively) all ancestors' required
sets. So `ai_ready` requires core ∪ extended ∪ ai_ready.

## Pub-conditional fields

```yaml
pub_conditional:
  when_release_status_in: [approved, published]
  required:
    - license.spdx_id
    - authors
    - citation.preferred_citation
    - dates.issued
```

Required when `release_status` is `approved` or `published`.

## Enums

```yaml
enums:
  datacard.profile: [core, extended, ai_ready, sensitive]
  datacard.creation_method: [manual, automated, hybrid]
  datacard.sensitivity_tier:
    - tier0_open
    - tier1_controlled_research
    - tier2_proprietary
    - tier3_sensitive
    - tier4_export_controlled
    - tier5_regulated_personal
    - tier6_classified
  datacard.access_level: [open, restricted, controlled]
  security.classification: [U, CUI, C, S, TS]
  security.sensitivity_tier:
    - tier0_open
    - tier1_controlled_research
    - tier2_proprietary
    - tier3_sensitive
    - tier4_export_controlled
    - tier5_regulated_personal
    - tier6_classified
  security.export_control: [none, EAR, ITAR]
  workflow.state:
    - raw
    - processing
    - qa
    - analysis
    - review
    - embargo
    - published
    - archived
  release_status: [draft, under_review, approved, published, deprecated]
  object_type: [dataset, model, software, ai_agent, eval, framework, other]
  dataset_type: [GD, IM, ND, SM, FP, I, MM, MD, AS, IP, IG]
  access_policy.access_level: [open, restricted, controlled]
  access_policy.authorization_required:
    - none
    - account
    - user_agreement
    - data_use_agreement
    - sponsor_approval
    - export_control_review
    - irb_approval
    - other
  license.spdx_id:
    escape_values: [other, pending]
  ai_usage.ai_ready: [true, false, conditional]
  ai_usage.training_use_allowed: [true, false, conditional]
  ai_usage.inference_use_allowed: [true, false, conditional]
  ai_usage.evaluation_use_allowed: [true, false, conditional]
  integrity.checksum_type: [sha256, sha512, md5, other]
  dataset_readiness.level: [1, 2, 3]
  dataset_readiness.confidence: [high, medium, low]
  compliance.irb_approved: [true, false, not_applicable]
```

Values are sourced from the Genesis v1.0 template comments and Appendix B of the Field Requirements doc; `license.spdx_id` is special — the SPDX registry is too large to enumerate, so the validator treats any value not in `escape_values` as an informational pass-through.

## Formats

```yaml
formats:
  orcid: '^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$'
  ror_url: '^https://ror\.org/[0-9a-z]{9}$'
  doi: '^10\.\d+/.+'
  iso8601_date: '^\d{4}-\d{2}-\d{2}$'
  ark: '^ark:/\d+/.+'
  handle: '^\d+/.+'
```

These are pragmatic patterns since Genesis has not published an authoritative schema.

## Format fields

```yaml
format_fields:
  orcid:
    - datacard.created_by[].creator.person.orcid
    - contact.person.orcid
    - authors[].person.orcid
    - contributors[].person.orcid
    - stewardship.maintainer.person.orcid
    - dataset_readiness.evaluated_by.person.orcid
  ror_url:
    - datacard.created_by[].creator.person.affiliation.ror_id
    - datacard.created_by[].creator.organization.ror_id
    - contact.person.affiliation.ror_id
    - contact.organization.ror_id
    - authors[].person.affiliation.ror_id
    - authors[].organization.ror_id
    - sponsor_organizations[].ror_id
    - research_organizations[].ror_id
    - facilities[].ror_id
    - facilities[].location.ror_id
    - stewardship.maintainer.person.affiliation.ror_id
    - stewardship.maintainer.organization.ror_id
  iso8601_date:
    - datacard.created_date
    - datacard.updated_date
    - datacard.change_log[].date
    - datacard.created_by[].date
    - workflow.embargo_until
    - dates.data_collection_start
    - dates.data_collection_end
    - dates.issued
    - dates.modified
    - security.last_reviewed_date
    - security.declassification.review_date
    - contact.valid_until
    - reviews[].review_date
```

Paths use `[]` to indicate iteration over each element of a list field.

## Conditional required

```yaml
conditional_required:
  - when: {workflow.state: embargo}
    require: [workflow.embargo_until]
  - when: {security.classification: CUI}
    require: [security.cui_marking]
  - when_not: {security.classification: U}
    require:
      - security.classification_reason
      - security.declassification.review_date
      - security.declassification.authority
  - when_not: {security.export_control: none}
    require: [security.export_control_id]
  - when: {security.sensitivity_tier: tier5_regulated_personal}
    require:
      - security.pii.present
  - when: {security.pii.deidentification_applied: true}
    require: [security.pii.deidentification_method]
  - when: {license.spdx_id: other}
    require: [license.name]
  - when: {datacard.profile: ai_ready}
    require:
      - categorization.task_category
      - categorization.task_subcategory
  - when: {release_status: deprecated}
    severity: warn
    require: [identification.superseded_by]
```

`when` triggers if all key/value pairs match; `when_not` triggers if the key value differs from the given value; `severity: warn` makes the rule non-blocking.

## Workflow release alignment

```yaml
workflow_release_alignment:
  raw: [draft]
  processing: [draft]
  qa: [draft]
  analysis: [draft]
  review: [under_review]
  embargo: [approved, published]
  published: [approved, published]
  archived: [deprecated, published]
```

This is the recommended alignment; the validator emits a `warn`, not an `error`, on mismatch.

## Features form rule

`dataset_info.features` must use one form consistently:
- For `core` and `extended` profiles: flat list of strings.
- For `ai_ready` profile: list of objects with `name`, `type`, etc.
Never mix in the same datacard.

## Filename rule

`datacard.filename` snake_case portion must equal `identification.name`
lowercased, with non-alphanumeric runs replaced by `_`, prefixed with
`genesis_datacard_`, suffixed with `.md`.
