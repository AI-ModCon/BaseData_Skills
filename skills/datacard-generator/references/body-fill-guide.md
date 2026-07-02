# Body-fill guide

The Genesis v1.2 datacard has two halves: the YAML frontmatter (machine-readable) and the markdown narrative body (human-readable). This skill fills both. The template's own instructions anticipate automated body-fill via the `<metadata_key: foo>` tags that point at YAML paths inside v2 capability containers (`discoverability.*`, `accessibility.*`, `interoperability.*`, `reusability.*`, `governed_use.*`, `ai_usability.*`).

This guide maps each markdown section to its source. For each section, the skill should:
1. Replace any `[!TODO]`, `<REPLACE: ...>`, `<INSTRUCTIONS: ...>` markers
2. Replace `<metadata_key: foo>` tags with the actual value from YAML (or rendered prose if it's a list/dict)
3. Strip any remaining `${VARIABLE}` placeholders or `__VALUE__` markers
4. **Leave no placeholder markup in the final output**

When a YAML value is missing or `not_applicable`, write a short prose note (e.g., "Not provided — see structured metadata above") rather than leaving the placeholder.

> **Known upstream inconsistency (v1.2):** the vendored template's markdown
> narrative body still tags the AI/ML Considerations section with the
> **old** `<metadata_key: ai_usability.ai_usage.training_use_allowed>` /
> `inference_use_allowed` / `evaluation_use_allowed` names, even though the
> YAML frontmatter uses the **new** `*_use_status` names
> (`training_use_status`, `inference_use_status`, `evaluation_use_status`).
> This was not fixed upstream in v1.2. When filling that section, treat the
> old `metadata_key` names as synonyms for the new `*_use_status` fields
> (translate old → new) rather than treating them as missing data.

---

## Mechanical mapping (single YAML source → single markdown section)

These sections have one or more `<metadata_key: foo>` tags pointing at a single logical source. Replace the section body with a formatted rendering of the YAML value(s) at those paths.

Capability gating: sections labelled `[capability_required]` or `[capability_if_applicable]` in the template only appear when the user set `supports_<capability>: "Yes"` in the frontmatter. The "Required when" column notes the gate.

| Markdown section | YAML source(s) | How to render | Required when |
|---|---|---|---|
| `# Datacard for ${DATASET_NAME}` | `discoverability.identification.name` | Literal substitution into H1 title | Always |
| `**Last Updated**` | `datacard.updated_date` | ISO date (YYYY-MM-DD) | Always |
| `### Dataset Description` | `discoverability.dataset_description.dataset_summary` | Prose paragraph | `supports_discoverability=Yes` |
| `## Keywords` | `discoverability.dataset_description.keywords` | Comma-separated list | `supports_discoverability=Yes` |
| `### Security / Marking Considerations` | `discoverability.sensitivity.overall_sensitivity`, `discoverability.sensitivity.classified_status`, `discoverability.sensitivity.cui_status`, `discoverability.sensitivity.ucni_status` | Compose a sentence: "Overall sensitivity: `<overall>`. Classification: `<classified>`. CUI: `<cui>`. UCNI: `<ucni>`." Omit sub-fields that are `not_applicable`. | `supports_discoverability=Yes` |
| `### Developed by` | `discoverability.authors[]` | Bulleted list: Name (ORCID) — Affiliation (ROR). Include CRediT roles if present. | `supports_discoverability=Yes` |
| `### Contributed by` | `discoverability.contributors[]` | Same format as authors | `supports_discoverability=Yes` (if_applicable) |
| `### Related datasets, standards, metadata, and ontologies` | `interoperability.related_resources.datasets`, `interoperability.domain_metadata`, `interoperability.semantic_layer.schema_url`, `interoperability.semantic_layer.semantic_context` | List each with name + identifier + relationship | `supports_interoperability=Yes` (if_applicable) |
| `### Related publications` | `interoperability.related_resources.publications` | List each with type + value (DOI/arXiv/URL) | `supports_interoperability=Yes` (if_applicable) |
| `### Related software` | `interoperability.related_resources.software` | List each with name + version + identifier + relationship | `supports_interoperability=Yes` (if_applicable) |
| `### Related ai model` | `interoperability.related_resources.ai_models` | List each with name + version + identifier + relationship | `supports_interoperability=Yes` (if_applicable) |
| `### List of variable name(s), description(s), unit(s), and value labels` | `interoperability.data_structure.features` (structured) | Markdown table: Variable / Description / Unit / Value labels | `supports_interoperability=Yes` |
| `### Related Schemas or Ontologies` | `interoperability.semantic_layer.schema_url`, `interoperability.semantic_layer.semantic_context` | Bulleted list of schema_url + semantic_context. If empty, write "No formal schema or ontology applied." | `supports_interoperability=Yes` (if_applicable) |
| `### Codes used for missing data` | `reusability.data_quality.missing_data_codes` | Markdown table: Code / Description | `supports_reusability=Yes` (if_applicable) or `supports_interoperability=Yes` (if_applicable) |
| `### Specialized formats or other abbreviations used` | `interoperability.data_structure.formats` | List the formats with one-line descriptions (e.g., "HDF5 — Hierarchical Data Format v5") | `supports_interoperability=Yes` (if_applicable) |
| `### Data Processing` | `interoperability.provenance.processing_steps` | Prose paragraph describing preprocessing, calibration, filtering, labeling, or transformations | `supports_interoperability=Yes` |
| `### Software used to preprocess/ clean/ label the data` | `interoperability.provenance.was_generated_by`, `interoperability.provenance.software_environment` | List relevant software with bibtex/PID/link + description of required packages | `supports_interoperability=Yes` (if_applicable) |
| `## Citation` | `reusability.citation.preferred_citation` | Fenced ` ```bibtex ` block, or plain text if not in BibTeX format | `supports_reusability=Yes` (if_applicable) |
| `## License and Usage Rights` | `reusability.license.spdx_id`, `reusability.license.license_name`, `reusability.license.license_url`, `reusability.additional_licenses` | Compose: "Licensed under `<spdx_id>` (`<license_name>`). See: `<license_url>`. `<additional_licenses if any>`." | `supports_reusability=Yes` (if_applicable) |
| `## Maintenance & Updates` | `reusability.stewardship.maintainer`, `reusability.stewardship.level`, `reusability.stewardship.update_frequency`, `reusability.stewardship.retention_policy`, `reusability.stewardship.versioning_strategy` | Compose: "Maintained by `<maintainer>` (level: `<level>`). Updated `<update_frequency>`. Retention: `<retention_policy>`. Versioning: `<versioning_strategy>`." | `supports_reusability=Yes` (if_applicable) |
| `## Data Quality & Limitations` | `reusability.data_quality.completeness`, `reusability.data_quality.known_issues`, `reusability.data_quality.validation_methods`, `reusability.data_quality.noise_characteristics`, `reusability.data_quality.uncertainty_notes`, `discoverability.dataset_description.limitations` | Multi-paragraph prose synthesizing all sub-fields. Each non-null sub-field becomes one sentence or bullet. | `supports_reusability=Yes` |
| `## Integrity & Versioning` | `reusability.integrity.checksum_available`, `reusability.integrity.checksum_type`, `reusability.integrity.checksum_value`, `reusability.integrity.fixity_policy`, `reusability.stewardship.versioning_strategy` | Compose: "Checksums (`<checksum_type>`) available: `<Yes/No>`. `<fixity_policy>`. Versioning: `<versioning_strategy>`." | `supports_reusability=Yes` (if_applicable) |
| `## Access and Permissions` | `governed_use.non_sensitivity_governance_metadata.export_control.export_control_status`, `governed_use.non_sensitivity_governance_metadata.privacy.*`, `governed_use.compliance.doe_data_management_plan`, `governed_use.compliance.irb_approved` | Compose a summary of export control, privacy, PII/PHI status, and compliance flags | `supports_governed_use=Yes` |
| `## Access conditions` | `governed_use.non_sensitivity_governance_metadata.rights_release_records.ip_restriction_type`, `.agreement_required`, `.agreement_type`, `.public_release_status`, `.record_status` | Bulleted list of each condition | `supports_governed_use=Yes` |
| `## Review Provenance / ### Release review process` | `governed_use.review_provenance_companion[]` | List each review entry with stage + status + date | `supports_governed_use=Yes` (if_applicable) |
| `## AI / Machine Learning Considerations` | `ai_usability.ai_usage.training_use_status`, `ai_usability.ai_usage.training_use_conditions`, `ai_usability.ai_usage.inference_use_status`, `ai_usability.ai_usage.inference_use_conditions`, `ai_usability.ai_usage.evaluation_use_status`, `ai_usability.ai_usage.evaluation_use_conditions`, `ai_usability.ai_usage.restrictions`, `ai_usability.ai_usage.bias_risks`, `ai_usability.ai_usage.safety_considerations`, `ai_usability.ai_usage.human_review_required` | Prose paragraph synthesizing all AI usage flags. Note which uses are allowed/conditional/prohibited; when a status is `Conditional`, include its `*_use_conditions` text. The template's `<metadata_key:>` tags for this section still use the old `*_use_allowed` names — see the known-inconsistency note above; map them to `*_use_status`. | `supports_ai_usability=Yes` |

---

## Synthesis sections (composition from multiple YAML sources)

These sections do NOT have a single `<metadata_key:>` tag pointing at one value. The skill must compose prose from multiple YAML values across capability containers.

| Markdown section | YAML sources to combine | Notes |
|---|---|---|
| `### Domain and Purpose` | `discoverability.dataset_description.purpose`, `discoverability.dataset_description.science_domain`, `interoperability.domain_metadata.science_domain` | Compose 2-3 sentences covering research domain, science sub-domain, and purpose. If `purpose` is absent, derive from `dataset_summary`. `science_domain` is a closed enum (`ScienceDomainEnum`, quoted strings with spaces) as of v1.2 — quote the value verbatim in prose rather than paraphrasing it. |
| `### Resources used, including funding and facilities, to create the dataset` | `discoverability.sponsor_organizations[]`, `discoverability.sponsoring_doe_program_office`, `discoverability.sponsoring_doe_subprogram`, `discoverability.research_organizations[]`, `discoverability.facilities[]` | Compose: "Sponsored by `<sponsors>` (DOE program: `<program>`). Created at `<research_orgs>` using `<facilities>` (roles: `<facility roles>`)." Include ROR IDs, grant/contract numbers when present. |
| `### Dataset generation, collection, and procedures` | `discoverability.dataset_description.collection_methodology`, `interoperability.provenance.processing_steps`, `interoperability.provenance.instrumentation`, `interoperability.provenance.simulation_details` | Multi-paragraph prose. One paragraph per populated sub-field. |
| `## Sharing & Access` | `accessibility.access`, `accessibility.access_policy` | Compose: "Access level: `<access level>`. `<access_policy prose>`." Include contact information and legal rights statement if present. |
| `### Files & Structure` | `discoverability.dataset_description.data_characteristics`, `accessibility.dataset_scale.record_count`, `accessibility.dataset_scale.compressed_bytes`, `accessibility.dataset_scale.uncompressed_bytes`, `interoperability.data_structure.formats`, `interoperability.data_structure.modalities`, `interoperability.data_structure.splits` | Compose: "The dataset consists of `<record_count>` `<record_unit>` in `<formats>` format(s), totaling `<compressed_bytes>` compressed / `<uncompressed_bytes>` uncompressed. Splits: `<splits>` (or 'no pre-defined splits' if none). Modalities: `<modalities>`." |
| `## Data Characteristics` | `interoperability.data_structure.features`, `interoperability.data_structure.splits`, `interoperability.data_structure.spatial_coverage`, `interoperability.data_structure.temporal_coverage`, `interoperability.data_structure.modalities` | Describe variables/features, splits, spatial/temporal coverage, and modalities. Use a table if features are structured. |
| `## Semantic / Schema Information` | `interoperability.domain_metadata`, `interoperability.semantic_layer.schema_url`, `interoperability.semantic_layer.semantic_context` | Two bullets: schema_url, semantic_context. Expand domain_metadata for JSON Schema, NETCDF CF conventions, ontology alignment, controlled vocabularies, units standards. If all empty, write "No formal schema or ontology applied." |
| `### Example of the contents` | Introspected sample columns (first 3 columns of first CSV, if any) | If non-CSV, leave a placeholder noting "Sample requires manual extraction for this format." |

---

## What to strip after filling

After substituting all values, remove these markers (they are template scaffolding, not content):

- `[!TODO]` — token
- `<REPLACE: ...>` — instruction blocks
- `<INSTRUCTIONS: ...>` — instruction blocks (the multi-paragraph block at the top of the markdown body; remove the entire block)
- `<metadata_key: ...>` — tags (replaced by the actual value above)
- `${VARIABLE}` — placeholder variables (substitute or remove)
- `__VALUE__` — placeholder markers (substitute or remove)
- Example tables in the template (those prefaced with "For example:" — remove once the real table is in place)

**Verification:** after writing the file, grep the output for `[!TODO]`, `<REPLACE:`, `<INSTRUCTIONS:`, `<metadata_key:`, `${`, `__VALUE__`. Any match means a section was missed.

---

## Machine Usability Snapshot table

The template body opens with a capability-snapshot table directly below `### Machine Usability Snapshot`. In v2 the rows represent the six capability containers plus license and checksum hygiene — not the five v1 AI/license rows.

```
| Intended Capability | DataCard Support |
| ------ | ------ |
| Discoverability  | Yes/No |
| Accessibility    | Yes/No |
| Interoperability | Yes/No |
| Reusability      | Yes/No |
| Governed Use     | Yes/No |
| AI Usability     | Yes/No |
| License Clarity  | Yes/No |
| Checksum / Fixity| Yes/No |
| Semantic Context | Yes/No |
```

Fill each row from the YAML frontmatter:

| Row | YAML source | Value logic |
|---|---|---|
| Discoverability | `supports_discoverability` | Copy verbatim (`Yes` / `No`) |
| Accessibility | `supports_accessibility` | Copy verbatim |
| Interoperability | `supports_interoperability` | Copy verbatim |
| Reusability | `supports_reusability` | Copy verbatim |
| Governed Use | `supports_governed_use` | Copy verbatim |
| AI Usability | `supports_ai_usability` | Copy verbatim |
| License Clarity | `reusability.license.spdx_id` | `Yes` if present and not `pending` / `__SPDX_ID__`; `No` otherwise |
| Checksum / Fixity | `reusability.integrity.checksum_available` | Copy verbatim (`Yes` / `No`) |
| Semantic Context | `interoperability.semantic_layer.semantic_context` | `Yes` if list is non-empty; `No` otherwise |
