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
