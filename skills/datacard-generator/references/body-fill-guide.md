# Body-fill guide

The Genesis v1.0 datacard has two halves: the YAML frontmatter (machine-readable) and the markdown narrative body (human-readable). This skill fills both. The template's own instructions (genesis_v1.0_template.md line 917) anticipate automated body-fill via the `<metadata_key: foo>` tags that point at YAML paths.

This guide maps each markdown section to its source. For each section, the skill should:
1. Replace any `[!TODO]`, `<REPLACE: ...>`, `<INSTRUCTIONS: ...>` markers
2. Replace `<metadata_key: foo>` tags with the actual value from YAML (or rendered prose if it's a list/dict)
3. Strip any remaining `${VARIABLE}` placeholders or `__VALUE__` markers
4. **Leave no placeholder markup in the final output**

When a YAML value is missing or `not_applicable`, write a short prose note (e.g., "Not provided — see structured metadata above") rather than leaving the placeholder.

---

## Mechanical mapping (single YAML source → single markdown section)

These sections have a `<metadata_key: foo>` tag. Replace the entire section body with a formatted rendering of the YAML value at that path.

| Markdown section | YAML source | How to render |
|---|---|---|
| `# Datacard for ${DATASET_NAME}` | `identification.name` | Literal substitution into the title |
| `**Last Updated**` | `datacard.updated_date` | ISO date |
| `**Dataset Readiness Level:**` | `dataset_readiness.level` | Single digit (1/2/3) |
| `### Dataset Description` | `description.summary` | Prose |
| `### Keywords` | `description.keywords` | Comma-separated list |
| `### Citation` | `citation.preferred_citation` | Fenced ` ```bibtex ` block, or plain if empty |
| `### Security / Marking Considerations` | `security.classification`, `security.sensitivity_tier`, `security.sensitivity_level`, `security.cui_marking` | Compose a sentence: "This dataset is classified as `<classification>` at sensitivity tier `<tier>` (`<level>`)..." plus CUI marking if applicable |
| `### Access conditions` | `access_policy` (whole block) | Render as a small bullet list |
| `### Release review process` | `reviews[]` | List each review with stage + status + date |
| `### Developed by` | `authors[]` | List names + ORCID + affiliation |
| `### Contributed by` | `contributors[]` | Same format as authors |
| `### Related datasets, standards, metadata, and ontologies` | `related_resources.datasets` | List each with name + identifier + relationship |
| `### Related publications` | `related_resources.publications` | List each with type + value |
| `### Related software` | `related_resources.software` | List each with name + version + identifier + relationship |
| `### Related ai model` | `related_resources.ai_models` | List each with name + version + identifier + relationship |
| `### Maintenance & Updates` | `stewardship` (whole block) | Compose: "Maintained by `<maintainer>`. Updated `<update_frequency>`. Retention: `<retention_policy>`." |
| `### Data Characteristics` | `dataset_info.features` | If flat list: comma-separated. If structured: small table (name/type/unit/description) |
| `### Data Quality & Limitations` | `data_quality` (completeness + known_issues + validation_methods + noise + uncertainty) | Multi-paragraph prose synthesizing all sub-fields |
| `### Related Schemas or Ontologies` | `semantic_layer` | Bulleted list of schema_url + semantic_context |
| `### List of variable name(s)...` | `dataset_info.features` (structured) | Markdown table: name/description/unit/value labels |
| `### Codes used for missing data` | `data_quality.missing_data_codes` | Markdown table: code/description |
| `### Specialized formats or other abbreviations used` | `dataset_info.formats` + domain knowledge | List the formats with one-line descriptions (e.g., "HDF5 — Hierarchical Data Format v5") |
| `### Data Processing` | `provenance.processing_steps` | Prose paragraph |
| `### Software used to preprocess/ clean/ label the data` | `related_resources.software` filtered to `relationship: used_to_process` | List the relevant software |
| `## Integrity & Versioning` | `integrity` + `identification.version` + `stewardship.versioning_strategy` | Compose: "Checksums (sha256) available for primary files. Dataset versioned `<version>`; `<versioning_strategy>`." |
| `## Semantic / Schema Information` | `semantic_layer` | Two bullets: schema_url, semantic_context. If empty, write "No formal schema or ontology applied." |
| `## AI / Machine Learning Considerations` | `ai_usage` | Prose paragraph synthesizing `ai_ready`, `training_use_allowed`, `restrictions`, `bias_risks`, `safety_considerations`, `human_review_required` |

---

## Synthesis sections (need composition from multiple YAML sources)

These sections do NOT have a single `<metadata_key:>` tag. The skill composes prose from multiple YAML values.

| Markdown section | YAML sources to combine |
|---|---|
| `### Files & Structure` | `dataset_info.formats`, `dataset_info.modalities`, `dataset_info.splits`, `dataset_scale.record_count`, `dataset_scale.compressed_bytes`. Compose a paragraph: "The dataset consists of `<N>` files in `<formats>` format(s) totaling `<size>`. Splits: `<splits>` (or 'no pre-defined splits' if none). Modalities: `<modalities>`." |
| `### Sharing & Access` | `access_policy.access_level`, `access_policy.authorization_required`, `access.intended_repositories[]`, `contact`. Compose: "Access level: `<level>`. Authorization: `<auth>`. Intended repositories: `<list>`. Contact: `<contact>`." |
| `### Domain and Purpose` | `categorization.science_domain`, `categorization.tags`, `description.purpose` (or `description.summary` if purpose absent). Compose 2-3 sentences. |
| `### Resources used, including funding and facilities` | `sponsor_organizations[]`, `research_organizations[]`, `facilities[]`. Compose: "Sponsored by `<sponsors>`. Created at `<research_orgs>` using `<facilities>` (roles: `<facility roles>`)." |
| `### Dataset generation, collection, and procedures` | `provenance.was_generated_by`, `provenance.collection_methodology`, `provenance.instrumentation`, `provenance.simulation_details`, `provenance.software_environment`. Multi-paragraph prose. |
| `### Example of the contents` | `introspect.py` `sample_columns` output (first 3 columns of first CSV, if any). If non-CSV, leave a placeholder noting "Sample requires manual extraction for this format." |
| `## Additional Information` | Optional — fill if the user provided notes not captured elsewhere; otherwise write "No additional information provided." |

---

## What to strip after filling

After substituting all values, remove these markers (they are template scaffolding, not content):

- `[!TODO]` — token
- `<REPLACE: ...>` — instruction blocks
- `<INSTRUCTIONS: ...>` — instruction blocks (these appear at the top of the markdown half; remove the whole block, lines 902-918 of the template)
- `<metadata_key: ...>` — tags (replaced by the value above)
- `${VARIABLE}` — placeholder variables (substitute or remove)
- `__VALUE__` — placeholder markers (substitute or remove)
- Example tables in the template (these show "For example:" — remove them once the real table is in place)

**Verification:** after writing the file, grep the output for `[!TODO]`, `<REPLACE:`, `<INSTRUCTIONS:`, `<metadata_key:`, `${`, `__VALUE__`. Any match means a section was missed.

---

## Machine Usability Snapshot table

The template has a small table near the top of the body:

```
| Aspect | Status |
|--------|--------|
| AI Ready | Yes/No/Conditional|
| License Clarity | Yes/No|
| Machine Access | Yes/No|
| Checksum / Fixity | Yes/No|
| Semantic Context | Yes/No|
```

Fill each row from the YAML:

| Row | YAML source | Value |
|---|---|---|
| AI Ready | `ai_usage.ai_ready` | Yes / No / Conditional |
| License Clarity | `license.spdx_id` | Yes if present and not `pending`; No otherwise |
| Machine Access | `access.intended_repositories[].api.endpoint` | Yes if any API endpoint present; No otherwise |
| Checksum / Fixity | `integrity.checksum_available` | Yes / No |
| Semantic Context | `semantic_layer.semantic_context` | Yes if list is non-empty; No otherwise |
