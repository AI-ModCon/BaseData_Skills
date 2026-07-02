# Capability prompt batches

Per-capability field-prompt sequences used by SKILL.md (workflow step 6) when
interactively filling a datacard. Batches are 1–5 fields each and ordered
roughly by how often the answer is already known.

Each top-level key in the YAML below is a `supports_*` capability. The skill
loads ONLY the sections for capabilities the user opted into via the
`supports_*` flags in step 1. `discoverability` is always loaded (it is
schema-forced to Yes).

For comprehensive enum values, see `references/lookup-tables.md`.

## Prompts

```yaml
prompts:
  discoverability:
    # always Yes
    - title: "Identification"
      fields:
        - path: discoverability.identification.name
          ask: "Single human-readable name for this dataset (used in filename)."
        - path: discoverability.identification.project
          ask: "Project or sub-project this dataset belongs to (e.g., genesis-fusion)."
        - path: discoverability.identification.version
          ask: "Dataset version (semver). Start at 1.0 if first release."
        - path: discoverability.identification.primary_id.type
          ask: "Primary identifier type: doi | ark | handle | url | osti | local | unregistered | other."
        - path: discoverability.identification.primary_id.value
          ask: "Primary identifier value (use ark, local, or unregistered pre-publication)."
    - title: "Description"
      fields:
        - path: discoverability.dataset_description.dataset_summary
          ask: "1–3 sentences in plain language for a broad scientific audience."
        - path: discoverability.dataset_description.keywords
          ask: "5–10 keywords (comma-separated)."
    - title: "Object & dataset typing"
      fields:
        - path: discoverability.dataset_description.tags.object_type
          ask: "Object type: Dataset | Model | Software | AI_Agent | Infrastructure | Resource | Other."
        - path: discoverability.dataset_type
          ask: "OSTI dataset type code (GD/IM/ND/SM/FP/I/MM/MD/AS/IP/IG)."
        - path: discoverability.product_type
          ask: "Product type: Technical_Report | Paper_or_Proceedings | Journal_Article | Software_Manual | Data | Collection | Computer_Related | Model | Agent."
    - title: "Lifecycle"
      fields:
        - path: discoverability.release_status
          ask: "Release status: Draft | Under_Review | Approved | Published | Deprecated."
        - path: discoverability.workflow.state
          ask: "Workflow state: Raw | Processing | QA | Analysis | Review | Embargo | Published | Archived | not_applicable."
    - title: "Contact"
      fields:
        - path: discoverability.contact.agent_type
          ask: "Contact agent type: person | organization."
    - title: "Contact (person details if contact.agent_type=person)"
      fields:
        - path: discoverability.contact.person.given_name
          ask: "Given (first) name."
        - path: discoverability.contact.person.family_name
          ask: "Family (last) name."
        - path: discoverability.contact.person.email
          ask: "Email address for inquiries about this dataset."
        - path: discoverability.contact.person.affiliation.name
          ask: "Affiliation organization name."
    - title: "Creator agent details"
      fields:
        - path: discoverability.datacard.created_by[].creator.person.role
          ask: "CRediT role(s) for this creator, if a person or organization (multi-valued). See lookup-tables.md for the 16 CRediT values. Enter inside the person/organization sub-block, not at the creator entry level."
        - path: discoverability.datacard.created_by[].creator.ai_model.relationship
          ask: "If this creator is an ai_model: its relationship to the datacard creation process — used_to_create | used_to_process | used_to_analyze | recorded_by | trained_on | evaluated_on."
        - path: discoverability.datacard.created_by[].creator.software.relationship
          ask: "If this creator is software: its relationship to the datacard creation process — used_to_create | used_to_process | used_to_analyze | recorded_by | trained_on | evaluated_on."
    - title: "Categorization"
      fields:
        - path: discoverability.dataset_description.science_domain
          ask: "Scientific domain — select exactly one from the closed ScienceDomainEnum list (quoted strings with spaces, not snake_case): \"Biology and Medicine\" | \"Chemistry\" | \"Energy Storage, Conversion, and Utilization\" | \"Engineering\" | \"Environmental Sciences\" | \"Fission and Nuclear Technologies\" | \"Fossil Fuels\" | \"Geosciences\" | \"Materials\" | \"Mathematics and Computing\" | \"National Defense\" | \"Physics\" | \"Power Generation and Distribution\" | \"Renewable Energy\" | \"Other\". See lookup-tables.md for descriptions."
    - title: "Sensitivity (dataset)"
      fields:
        - path: discoverability.sensitivity.overall_sensitivity
          ask: "Overall dataset sensitivity: Public | Unclassified_Uncontrolled | CUI | UCNI | Classified | Legacy_Controlled | Mixed | Other_Controlled."
    - title: "Sensitivity (datacard document)"
      fields:
        - path: discoverability.datacard.sensitivity.overall_sensitivity
          ask: "Overall datacard document sensitivity (independent of dataset sensitivity). Same enum as above."
    - title: "Authorship"
      fields:
        - path: discoverability.authors
          ask: "Primary authors with CRediT roles (multi-valued). See lookup-tables.md for the 16 CRediT values. `role[]` goes inside each author's `person` or `organization` sub-block (e.g., `authors[].person.role`), not on the author entry itself."
    - title: "Organizational context"
      fields:
        - path: discoverability.sponsor_organizations
          ask: "Funding/sponsor organizations (name + ROR if known)."
        - path: discoverability.research_organizations
          ask: "Creating/collecting organizations (name + ROR if known)."

  accessibility:
    - title: "Access policy"
      fields:
        - path: accessibility.access_policy.access_level
          ask: "Dataset access level: Open | Restricted | Controlled."
        - path: accessibility.access_policy.authorization_required
          ask: "Authorization required (multi-valued): Account | User_Agreement | Data_Use_Agreement | Sponsor_Approval | Export_Control_Review | IRB_Approval | Other."
    - title: "Dataset scale"
      fields:
        - path: accessibility.dataset_scale.record_count
          ask: "Number of records (or files, or samples — depends on record_unit)."
        - path: accessibility.dataset_scale.record_unit
          ask: "Unit for record_count: samples | files | records | timesteps | images | tokens | other."
        - path: accessibility.dataset_scale.compressed_bytes
          ask: "Total compressed size in bytes (from `du` or stat sum)."
    - title: "Access location"
      fields:
        - path: accessibility.access.current_location
          ask: "Where the data physically resides right now (path or URL)."
        - path: accessibility.access.publicly_facing_landing_page_url
          ask: "Publicly facing landing page URL (if already published or deposited)."

  interoperability:
    - title: "Data structure"
      fields:
        - path: interoperability.data_structure.formats
          ask: "File formats present (e.g., CSV, HDF5, Parquet)."
        - path: interoperability.data_structure.modalities
          ask: "Data modalities (e.g., tabular, image, time-series, text). [required when supports_interoperability=Yes]"
    - title: "Features"
      fields:
        - path: interoperability.data_structure.features
          ask: "Variable list as structured objects: name, data_type, unit, description, range."
    - title: "Dates"
      fields:
        - path: interoperability.dates.data_collection_start
          ask: "ISO 8601 date data collection began."
        - path: interoperability.dates.data_collection_end
          ask: "ISO 8601 date data collection ended."
    - title: "Provenance"
      fields:
        - path: interoperability.provenance.was_generated_by
          ask: "How was this dataset generated? (instrument, simulation, derivation)."
        - path: interoperability.provenance.processing_steps
          ask: "Key processing, cleaning, calibration, or transformation steps applied."
    - title: "Semantic layer"
      fields:
        - path: interoperability.semantic_layer.schema_url
          ask: "URL to formal schema for this dataset (if any)."
        - path: interoperability.semantic_layer.semantic_context
          ask: "Semantic conventions applied (e.g., NetCDF CF, NeXus)."

  reusability:
    - title: "License"
      fields:
        - path: reusability.license.spdx_id
          ask: "SPDX license identifier (e.g., CC-BY-4.0, MIT, Apache-2.0). Use 'other' if not in SPDX, 'pending' if not yet assigned."
    - title: "Citation"
      fields:
        - path: reusability.citation.preferred_citation
          ask: "Recommended citation in BibTeX format (required when release_status = Approved or Published)."
    - title: "Integrity"
      fields:
        - path: reusability.integrity.checksum_available
          ask: "Are checksums available? Yes | No."
        - path: reusability.integrity.checksum_type
          ask: "Checksum algorithm: sha256 | sha512 | md5 | other (sha256 recommended)."
    - title: "Stewardship"
      fields:
        - path: reusability.stewardship.level
          ask: "Stewardship: Project_Managed | Repository_Managed | Externally_Managed | not_applicable."
        - path: reusability.stewardship.update_frequency
          ask: "Update frequency: None | Ad_Hoc | Monthly | Quarterly | Annually | Continuously | Other."
    - title: "Data quality"
      fields:
        - path: reusability.data_quality.completeness
          ask: "Be specific: 'All channels present; 2% timesteps missing due to instrument downtime on 2023-04-12'."
        - path: reusability.data_quality.known_issues
          ask: "Known issues, sensor drift, anomalies."
        - path: reusability.data_quality.validation_methods
          ask: "How was data quality validated? e.g., 'Cross-validated against NIST SRM 640f'."

  governed_use:
    - title: "Use governance"
      fields:
        - path: governed_use.use_governance.intended_use
          ask: "What is this dataset intended for?"
        - path: governed_use.use_governance.out_of_scope_use
          ask: "Uses this dataset should NOT be applied to."
        - path: governed_use.use_governance.need_to_know_basis
          ask: "Need-to-know basis (multi-valued): Mission_Need | Job_Duty | Project_Program_Association | Agreement_Defined | DGB_Exception_Waiver."
    - title: "Export control"
      fields:
        - path: governed_use.non_sensitivity_governance_metadata.export_control.export_control_status
          ask: "Export control status: Yes | No | Pending_Review | Unknown."
        - path: governed_use.non_sensitivity_governance_metadata.export_control.export_control_basis
          ask: "Export control basis: ITAR | EAR | DOE_Nuclear_Export_Control | Other | not_applicable."
        - path: governed_use.non_sensitivity_governance_metadata.export_control.foreign_national_access_status
          ask: "Foreign national access: Allowed | Restricted | Prohibited | Conditional | Unknown."
    - title: "Privacy / PII / PHI"
      fields:
        - path: governed_use.non_sensitivity_governance_metadata.privacy.privacy_status
          ask: "Privacy status: Yes | No | Pending_Review | Unknown."
        - path: governed_use.non_sensitivity_governance_metadata.privacy.pii_status
          ask: "Is PII present? Yes | No | Pending_Review | Unknown."
        - path: governed_use.non_sensitivity_governance_metadata.privacy.phi_status
          ask: "Is PHI (HIPAA-covered health info) present? Yes | No | Pending_Review | Unknown."
    - title: "Rights & release"
      fields:
        - path: governed_use.non_sensitivity_governance_metadata.rights_release_records.ip_restriction_type
          ask: "IP restriction: Proprietary | Limited_Rights | Restricted_Rights | Government_Purpose_Rights | Unlimited_Rights | Third_Party_Licensed | None."
        - path: governed_use.non_sensitivity_governance_metadata.rights_release_records.agreement_required
          ask: "Is a data-use agreement required? Yes | No."
        - path: governed_use.non_sensitivity_governance_metadata.rights_release_records.public_release_status
          ask: "Public release status: Approved | Pending | Not_Approved | Requires_STI_Review."
        - path: governed_use.non_sensitivity_governance_metadata.rights_release_records.record_status
          ask: "Record status: Federal_Record | Contractor_Record | Non_Record | Mixed | Unknown."
    - title: "Compliance"
      fields:
        - path: governed_use.compliance.doe_data_management_plan
          ask: "Is a DOE Data Management Plan on file? Yes | No | Unknown | not_applicable. [required]"
        - path: governed_use.compliance.osti_elink2_metadata_compliant
          ask: "Is the metadata compliant with OSTI E-Link 2 API? Yes | No | Unknown | not_applicable. [required]"
        - path: governed_use.compliance.irb_approved
          ask: "IRB approval status: Yes | No | Unknown | not_applicable (use not_applicable for non-human-subject data). [required]"

  ai_usability:
    - title: "AI/ML usage policy"
      fields:
        - path: ai_usability.ai_usage.training_use_status
          ask: "Training use status? Yes | No | Conditional. (renamed from training_use_allowed in v1.2) If Conditional, also fill training_use_conditions."
        - path: ai_usability.ai_usage.training_use_conditions
          ask: "Conditions under which training use is allowed (required only if training_use_status = Conditional)."
        - path: ai_usability.ai_usage.inference_use_status
          ask: "Inference use status? Yes | No | Conditional. (renamed from inference_use_allowed in v1.2) If Conditional, also fill inference_use_conditions."
        - path: ai_usability.ai_usage.inference_use_conditions
          ask: "Conditions under which inference use is allowed (required only if inference_use_status = Conditional)."
        - path: ai_usability.ai_usage.evaluation_use_status
          ask: "Evaluation use status? Yes | No | Conditional. (renamed from evaluation_use_allowed in v1.2) If Conditional, also fill evaluation_use_conditions."
        - path: ai_usability.ai_usage.evaluation_use_conditions
          ask: "Conditions under which evaluation use is allowed (required only if evaluation_use_status = Conditional)."
        - path: ai_usability.ai_usage.human_review_required
          ask: "Does AI use require human review? Yes | No."
    - title: "AI/ML risks"
      fields:
        - path: ai_usability.ai_usage.bias_risks
          ask: "Known bias risks (e.g., 'overrepresents samples from facility X'). Enter 'None' if none."
        - path: ai_usability.ai_usage.safety_considerations
          ask: "Safety considerations (e.g., 'outputs may be export-controlled'). Enter 'None' if none."
        - path: ai_usability.ai_usage.restrictions
          ask: "Any conditional-use restrictions. Enter 'None' if none."
```
