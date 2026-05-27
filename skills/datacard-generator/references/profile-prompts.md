# Profile prompt batches

Per-profile field-prompt sequences used by SKILL.md when interactively
filling a datacard. Batches are 1–5 fields each and ordered roughly by
how often the answer is already known (most-likely-known first).

## Prompts

```yaml
prompts:
  core:
    - title: "Identification"
      fields:
        - path: identification.name
          ask: "Single human-readable name for this dataset (used in filename)."
        - path: identification.project
          ask: "Project or sub-project this dataset belongs to (e.g., genesis-fusion)."
        - path: identification.version
          ask: "Dataset version (semver). Start at 1.0 if first release."
        - path: identification.primary_id.type
          ask: "Primary identifier type: doi | ark | handle | url | osti | local | other."
        - path: identification.primary_id.value
          ask: "Primary identifier value (use ark or local pre-publication)."
    - title: "Description"
      fields:
        - path: description.summary
          ask: "1–3 sentences in plain language for a broad scientific audience."
        - path: description.keywords
          ask: "5–10 keywords (comma-separated)."
    - title: "Type"
      fields:
        - path: object_type
          ask: "Object type: dataset | model | software | ai_agent | eval | framework | other."
        - path: dataset_type
          ask: "OSTI dataset type code (GD/IM/ND/SM/FP/I/MM/MD/AS/IP/IG). See lookup-tables.md."
        - path: release_status
          ask: "Release status: draft | under_review | approved | published | deprecated."
        - path: workflow.state
          ask: "Workflow state: raw | processing | qa | analysis | review | embargo | published | archived."
    - title: "Security"
      fields:
        - path: security.classification
          ask: "Classification: U | CUI | C | S | TS."
        - path: security.sensitivity_tier
          ask: "DATASET sensitivity tier (independent of datacard tier). tier0_open through tier6_classified."
        - path: security.export_control
          ask: "Export control: none | EAR | ITAR."
        - path: datacard.sensitivity_tier
          ask: "DOCUMENT (datacard) sensitivity tier. Set INDEPENDENTLY of dataset tier."
        - path: datacard.access_level
          ask: "DOCUMENT access level (Genesis currently only accepts `open`)."
    - title: "Access policy"
      fields:
        - path: access_policy.sensitivity_tier
          ask: "Dataset sensitivity for access control (typically matches security.sensitivity_tier)."
        - path: access_policy.access_level
          ask: "Dataset access level: open | restricted | controlled."
        - path: access_policy.authorization_required
          ask: "Authorization: none | account | user_agreement | data_use_agreement | sponsor_approval | export_control_review | irb_approval | other."
    - title: "Contact"
      fields:
        - path: contact.type
          ask: "Contact type: person | organization."
    - title: "Categorization & data"
      fields:
        - path: categorization.science_domain
          ask: "High-level domain (e.g., materials_science, biology, physics, computer_science)."
        - path: dataset_info.formats
          ask: "File formats present (e.g., CSV, HDF5, Parquet)."
    - title: "Provenance"
      fields:
        - path: provenance.was_generated_by
          ask: "How was this dataset generated? One line is fine but be specific (instrument, simulation, derivation)."
    - title: "Organizational context"
      fields:
        - path: sponsor_organizations
          ask: "Funding/sponsor organizations (name + ROR if known)."
        - path: research_organizations
          ask: "Creating/collecting organizations (name + ROR if known)."

  extended:
    - title: "Dates"
      fields:
        - path: dates.data_collection_start
          ask: "ISO 8601 date data collection began."
        - path: dates.data_collection_end
          ask: "ISO 8601 date data collection ended."
    - title: "Distribution & compliance"
      fields:
        - path: security.distribution_statement
          ask: "Distribution statement (e.g., 'Distribution A - Approved for public release')."
        - path: compliance.doe_data_management_plan
          ask: "Is a DOE Data Management Plan on file? true | false."
        - path: compliance.osti_elink2_metadata_compliant
          ask: "Is the metadata compliant with OSTI E-Link 2 API? true | false."

  ai_ready:
    - title: "Task categorization"
      fields:
        - path: categorization.task_category
          ask: "Primary ML task category (e.g., classification, regression, segmentation, detection)."
        - path: categorization.task_subcategory
          ask: "More specific ML task subcategory (e.g., binary_classification, time_series_forecasting)."
    - title: "AI/ML usage policy"
      fields:
        - path: ai_usage.ai_ready
          ask: "Is this dataset suitable for AI/ML? true | false | conditional."
        - path: ai_usage.training_use_allowed
          ask: "Training use allowed? true | false | conditional."
        - path: ai_usage.inference_use_allowed
          ask: "Inference use allowed? true | false | conditional."
        - path: ai_usage.evaluation_use_allowed
          ask: "Evaluation use allowed? true | false | conditional."
        - path: ai_usage.human_review_required
          ask: "Does AI use require human review? true | false."
    - title: "Data quality"
      fields:
        - path: data_quality.completeness
          ask: "Be specific. e.g., 'All channels present; 2% timesteps missing due to instrument downtime on 2023-04-12'."
        - path: data_quality.known_issues
          ask: "Known issues, sensor drift, anomalies, etc."
        - path: data_quality.validation_methods
          ask: "How was data quality validated? e.g., 'Cross-validated against NIST SRM 640f'."
    - title: "Integrity"
      fields:
        - path: integrity.checksum_available
          ask: "Are checksums available for integrity verification? true | false."

  sensitive:
    - title: "PII presence"
      fields:
        - path: security.pii.present
          ask: "Is PII present in the dataset? true | false. (Required if security.sensitivity_tier=tier5_regulated_personal.)"
    - title: "Compliance reviews"
      fields:
        - path: compliance.export_control_reviewed
          ask: "Has the dataset been export-control reviewed? true | false."
        - path: compliance.irb_approved
          ask: "IRB approval status: true | false | not_applicable (use not_applicable for non-human subjects)."
        - path: compliance.security_review_completed
          ask: "Security review completed? true | false."
```

The skill uses these batches to ask the user 3-5 fields at a time. The first batch in each profile is the most-likely-known information. `extends:`-style chaining is NOT used here — each profile lists ONLY its incremental batches; SKILL.md walks profile chains itself.
