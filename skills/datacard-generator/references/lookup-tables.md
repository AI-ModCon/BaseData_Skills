# Lookup tables

Human-readable reference for every fixed-vocabulary field in Genesis Mission
Datacard v1.0. Same data as the `enums` block in `validation-rules.md`,
with descriptions and use-when guidance. Sourced from the canonical
template comments and the Field Requirements doc Appendices A–D.

When prompting the user for a constrained field, load the relevant section
of this file and show the table.

---

## Datacard meta

### `datacard.profile`

Declares the completeness level of this datacard. Catalog tooling reads
this to determine which fields are expected.

| Value | When to use | Time |
|---|---|---|
| `core` | In-workflow, draft, or simple datasets not yet shared | 10-15 min |
| `extended` | Datasets shared with partners or submitted to OSTI/Zenodo | 30-45 min |
| `ai_ready` | Datasets intended for AI/ML training, inference, evaluation | 45-60 min |
| `sensitive` | CUI, export-controlled, PII, or classified datasets | 45-60 min |

### `datacard.creation_method`

How this datacard was most recently created or updated.

| Value | Meaning |
|---|---|
| `manual` | Filled out entirely by hand by a human author |
| `automated` | Generated entirely by a pipeline, script, or AI model with no human review |
| `hybrid` | Initially generated automatically, then reviewed and edited by a human (most common) |

### `datacard.created_by[].role`

Role each contributor played in creating this datacard.

| Value | Meaning |
|---|---|
| `initial_creation` | First created the datacard |
| `editor` | Modified content |
| `reviewer` | Reviewed without modifying |
| `updater` | Updated specific fields (e.g., after a workflow event) |

### `datacard.created_by[].creator.type`

Type of contributor entity.

| Value | When to use |
|---|---|
| `person` | A named human contributor |
| `organization` | A team or org without a named individual |
| `ai_model` | An AI model generated or substantially contributed (e.g., LLM-drafted) |
| `software` | An automated pipeline or script |

### `datacard.access_level` / `access_policy.access_level`

| Value | Meaning |
|---|---|
| `open` | No restrictions on access |
| `restricted` | Limited access; agreement or authentication required |
| `controlled` | Tightly controlled access; explicit approval required |

Note: Genesis currently only accepts `open` for `datacard.access_level`.
`restricted` and `controlled` are reserved for future use.

---

## Sensitivity & security

### Sensitivity tiers

Applies to BOTH `datacard.sensitivity_tier` (the document) and
`security.sensitivity_tier` (the data). These two fields are set
independently and often differ.

| Tier | Meaning |
|---|---|
| `tier0_open` | No restrictions; publicly shareable |
| `tier1_controlled_research` | Internal research use; limited sharing |
| `tier2_proprietary` | Proprietary; internal use only |
| `tier3_sensitive` | Sensitive; access controls required |
| `tier4_export_controlled` | Subject to EAR or ITAR restrictions |
| `tier5_regulated_personal` | Contains PII or regulated personal data |
| `tier6_classified` | Formally classified; handle per classification guide |

### `security.sensitivity_level`

Human-readable quick filter for catalog use. Use alongside `sensitivity_tier`, not as a replacement.

| Value | Meaning |
|---|---|
| `public` | Suitable for general public access |
| `internal` | Restricted to organization or project |
| `confidential` | Strictly limited distribution |
| `restricted` | Most restricted; few authorized recipients |

### `security.classification`

| Code | Meaning |
|---|---|
| `U` | Unclassified |
| `CUI` | Controlled Unclassified Information |
| `C` | Confidential |
| `S` | Secret |
| `TS` | Top Secret |

When `classification = CUI`, also fill `security.cui_marking`.

### CUI markings

Common markings (full registry: https://www.archives.gov/cui).

| Marking | Meaning |
|---|---|
| `CUI` | Generic Controlled Unclassified Information |
| `CUI//SP-PRVCY` | Privacy / PII |
| `CUI//SP-PROPIN` | Proprietary business information |
| `CUI//SP-EXPT` | Export controlled |
| `CUI//SP-LEI` | Law enforcement information |
| `CUI//SP-PRIVL` | Privilege (attorney-client, etc.) |

### `security.export_control`

| Value | Meaning |
|---|---|
| `none` | No export control restrictions |
| `EAR` | Export Administration Regulations (US Commerce Dept) |
| `ITAR` | International Traffic in Arms Regulations (US State Dept) |

If not `none`, set `security.export_control_id` (e.g., `EAR99`, `ECCN 3E001`, `USML Category XV`).

### `security.pii.types[]`

PII categories present when `security.pii.present = true`.

| Value | Meaning |
|---|---|
| `names` | Personal names |
| `email_addresses` | Email addresses |
| `phone_numbers` | Phone numbers |
| `location_data` | GPS coordinates, addresses, etc. |
| `biometric_data` | Fingerprints, facial scans, etc. |
| `financial_data` | Bank accounts, credit cards, etc. |
| `health_data` | Medical records, diagnoses (HIPAA-relevant) |
| `other` | Other PII not covered above |

---

## Identification & identifiers

### Identifier types (primary_id, supersedes, superseded_by, parent_collection, datacard.id, related_resources)

| Type | Format | When to use |
|---|---|---|
| `doi` | `10.XXXXX/XXXXXXX` | Published datasets with a registered DOI |
| `ark` | `ark:/NAAN/shoulder+name` (e.g., `ark:/12345/b2345679k`) | Pre-publication datasets at ARK-enabled institutions |
| `handle` | `XXXXX/XXXXXXX` | Datasets in Handle-based repositories |
| `url` | `https://...` | Stable URL is the best available identifier |
| `osti` | Numeric OSTI ID | Datasets registered with OSTI |
| `local` | Any internal ID | Pre-publication datasets with only internal identifiers |
| `other` | Any | Identifier systems not covered above |

### `identification.additional_ids[].type` (extended set)

Same as primary_id types PLUS DOE-lab report-number formats:

| Type | Format example | Source |
|---|---|---|
| `sand` | `SAND2024-XXXXX` | Sandia National Laboratories |
| `la-ur` | `LA-UR-XX-XXXXX` | Los Alamos National Laboratory |

Other DOE-lab formats (use `other` if not listed): ORNL/TM-YYYY/XXXXX, LBNL-XXXXX, etc.

### `related_resources.publications[].type`

| Type | When to use |
|---|---|
| `doi` | Published paper with a DOI |
| `ark` | ARK-identified publication |
| `arxiv` | arXiv preprint (e.g., `arXiv:2406.12345`) |
| `url` | Web-accessible publication without persistent ID |
| `report` | Internal or institutional report (use `report_number` for SAND/LA-UR) |
| `other` | Other publication types |

---

## Object & dataset typing

### `object_type`

Primary type of digital object described by this datacard.

| Value | Meaning |
|---|---|
| `dataset` | Scientific dataset (default) |
| `model` | Computational or ML model |
| `software` | Software package or library |
| `ai_agent` | AI agent (LLM-based or otherwise) |
| `eval` | Evaluation suite or benchmark |
| `framework` | Framework or methodology specification |
| `other` | Other digital object type |

### OSTI dataset type codes

| Code | Type | Description |
|---|---|---|
| `GD` | Genome/Genetic Data | DNA/RNA sequences, genomic annotations |
| `IM` | Image | Photographs, scans, microscopy, visualizations |
| `ND` | Numeric Data | Measurements, time series, tabular, sensor readings |
| `SM` | Specialized Mix | Multiple data types combined |
| `FP` | Figure/Plot | Charts, graphs, plots as primary deliverable |
| `I`  | Interactive Resource | Web apps, interactive visualizations, dashboards |
| `MM` | Multimedia | Audio, video, combined media |
| `MD` | Model | Computational models, simulations, trained ML models |
| `AS` | Automated Software | Scripts, analysis pipelines, workflows |
| `IP` | Instrumentation/Protocols | Experimental protocols, instrument specs |
| `IG` | Integrated Genomic Resources | Combined genomic databases and tools |

---

## Lifecycle & governance

## Workflow states

| State | Meaning |
|---|---|
| `raw` | Data as collected; no processing |
| `processing` | Cleaning, transforming, reducing |
| `qa` | Quality assurance / validation |
| `analysis` | Active scientific analysis |
| `review` | Formal review (security, export, IRB) |
| `embargo` | Complete but intentionally withheld |
| `published` | Publicly released |
| `archived` | Preserved; no longer actively maintained |

## Release statuses

| Status | Meaning |
|---|---|
| `draft` | Work in progress; not ready for sharing |
| `under_review` | Submitted for formal review |
| `approved` | Review complete; cleared for release |
| `published` | Publicly released and accessible |
| `deprecated` | Superseded or retired |

Typical workflow ↔ release alignment (warning on mismatch, not error):
- `raw` / `processing` / `qa` / `analysis` → `draft`
- `review` → `under_review`
- `embargo` / `published` → `approved` or `published`
- `archived` → `deprecated` or `published`

## Authorization required

| Value | Meaning |
|---|---|
| `none` | No authorization required |
| `account` | Registered account required |
| `user_agreement` | User agreement / terms of service |
| `data_use_agreement` | Formal DUA required |
| `sponsor_approval` | Sponsor or PI approval required |
| `export_control_review` | Export control review required |
| `irb_approval` | IRB approval required |
| `other` | Describe in `access_restrictions` |

---

## People & organizations

### Contact type (`contact.type`, `additional_contacts[].type`, `stewardship.maintainer.type`, `dataset_readiness.evaluated_by.type`, etc.)

| Value | When to use |
|---|---|
| `person` | A named individual contact |
| `organization` | A team, office, or organization without a single named contact |

When `person`, fill `person.given_name`, `family_name`, `email`, and ideally `orcid` and `affiliation`.
When `organization`, fill `organization.name` and ideally `ror_id`.

### `authors[].role` / `contributors[].role`

| Value | Meaning |
|---|---|
| `creator` | Primarily responsible for dataset creation (typical author) |
| `contributor` | Supporting role (annotation, review, processing) |
| `data_collector` | Performed the data collection |
| `curator` | Maintained or organized the dataset |
| `publisher` | Released the dataset (institution or repository) |
| `sponsor` | Funded the work |
| `other` | Role not covered above |

### `facilities[].role`

Role of a facility in the dataset's lifecycle.

| Value | Meaning |
|---|---|
| `collection` | Data was collected at this facility |
| `processing` | Data was processed at this facility |
| `storage` | Data is stored at this facility |
| `access` | Facility provides access (e.g., HPC cluster for downstream use) |

---

## Stewardship

### `stewardship.level`

Who manages this dataset over time.

| Value | Meaning |
|---|---|
| `project_managed` | Project team is the long-term steward |
| `repository_managed` | A repository (e.g., OSTI, Zenodo) is the long-term steward |
| `externally_managed` | An external entity manages stewardship |

### `stewardship.update_frequency`

| Value | Meaning |
|---|---|
| `none` | Static dataset, no planned updates |
| `ad_hoc` | Updates as needed, no schedule |
| `monthly` | Updated monthly |
| `quarterly` | Updated quarterly |
| `annually` | Updated annually |
| `other` | Other cadence; describe in `versioning_strategy` |

---

## Reviews

### `reviews[].stage`

Type of formal review.

| Value | Meaning |
|---|---|
| `internal_qa` | Internal quality assurance review |
| `security` | Information security review |
| `export_control` | Export control review (EAR/ITAR) |
| `irb` | Institutional Review Board (human subjects research) |
| `partner` | Partner organization review |
| `publication` | Publication / release review |
| `other` | Other review type |

### `reviews[].status`

| Value | Meaning |
|---|---|
| `not_started` | Review has not begun |
| `submitted` | Submitted for review |
| `pending` | Under active review |
| `approved` | Review passed |
| `declined` | Review rejected |

---

## Provenance & relationships

### Relationship vocabulary (base — used for `provenance.source_data[]`, `related_resources.datasets[]`)

| Value | Meaning |
|---|---|
| `is_derived_from` | This dataset was derived from the related dataset |
| `is_based_on` | This dataset is based on the related dataset (less direct than `is_derived_from`) |
| `is_part_of` | This dataset is a component of the related dataset/collection |
| `has_part` | This dataset has a component which is the related dataset |
| `references` | This dataset references the related dataset (no derivation) |
| `other` | Other relationship; describe in narrative |

### Relationship vocabulary (extended — used for `related_resources.software[]`, `related_resources.ai_models[]`)

Adds the base vocabulary above PLUS:

| Value | Meaning |
|---|---|
| `used_to_create` | The software/model was used to create this dataset |
| `used_to_process` | The software/model was used to process this dataset |
| `used_to_analyze` | The software/model was used to analyze this dataset |
| `trained_on` | The AI model was trained on this dataset |
| `evaluated_on` | The AI model was evaluated on this dataset |

---

## AI/ML & quality

### `ai_usage.ai_ready` / `training_use_allowed` / `inference_use_allowed` / `evaluation_use_allowed`

| Value | Meaning |
|---|---|
| `true` | Suitable for this AI/ML use |
| `false` | Should NOT be used for this AI/ML use |
| `conditional` | Suitable under conditions described in `ai_usage.restrictions` |

### `integrity.checksum_type`

| Value | When to use |
|---|---|
| `sha256` | SHA-256 — recommended for new datasets |
| `sha512` | SHA-512 — when stronger collision resistance needed |
| `md5` | MD5 — NOT recommended for new datasets (kept for legacy) |
| `other` | Custom hash — describe in `fixity_policy` |

### `compliance.irb_approved`

For datasets involving human subjects.

| Value | Meaning |
|---|---|
| `true` | IRB approval obtained |
| `false` | IRB approval was needed but NOT obtained — flag for review |
| `not_applicable` | No human subjects; IRB review was not required |

**Important:** for datasets without human subjects, use `not_applicable`, NOT `false`.

### `dataset_readiness.level`

| Value | Meaning |
|---|---|
| `1` | Discoverable — sufficient metadata to find and identify the dataset |
| `2` | Interoperable & Reusable — accessible, governed, licensed, documented |
| `3` | AI-Ready & Trustworthy — semantically clear, provenance-aware, integrity-supported |

### `dataset_readiness.confidence`

Confidence in the readiness-level evaluation.

| Value | Meaning |
|---|---|
| `high` | Evaluator highly confident in level assessment |
| `medium` | Some uncertainty in level assessment |
| `low` | Significant uncertainty; level may need re-evaluation |

---

## Access & APIs

### `access.intended_repositories[].api.authentication`

| Value | Meaning |
|---|---|
| `none` | No authentication required |
| `api_key` | API key required |
| `oauth2` | OAuth 2.0 authentication |
| `certificate` | Client certificate required |
| `other` | Other authentication scheme |

---

## SPDX licenses (quick reference)

Use the full SPDX registry (https://spdx.org/licenses/) for canonical identifiers. Common choices in Genesis datacards:

| `spdx_id` | Name |
|---|---|
| `CC0-1.0` | Creative Commons Zero (public domain dedication) |
| `CC-BY-4.0` | Creative Commons Attribution 4.0 |
| `CC-BY-SA-4.0` | CC Attribution-ShareAlike 4.0 |
| `MIT` | MIT License |
| `Apache-2.0` | Apache License 2.0 |
| `BSD-3-Clause` | BSD 3-Clause |
| `other` | Custom — also fill `license.name` |
| `pending` | License not yet assigned |
