# Genesis Mission Data Card v1.2 — Field Reference Guide

Document version: 2.0 (draft)
Applies to template: Genesis Mission Data Card **v1.2**
Companion schema: `genesis_datacard.yaml` (LinkML)

---

## How to Use This Guide

This guide is a companion to the Genesis Mission Data Card template (`genesis_datacard_merged_shared.md`, template v1.2). It explains every YAML frontmatter field: what it means, how to fill it in, which controlled vocabulary applies, and whether it accepts a single value or a list of entries.

The guide mirrors the template's structure exactly, organized under six top-level blocks: **Discoverability, Accessibility, Interoperability, Reusability, Governed Use,** and **AI Usability**.

---

## Getting Started

### What is a data card?

A data card combines structured metadata and computable natural language into a Markdown document that describes a dataset — what it is, where it came from, who created it, how it can be accessed, and how it can be used. Data cards serve both humans (who need to understand a dataset before using it) and machines (automated pipelines that ingest, catalog, and validate datasets).

In Genesis, every dataset — regardless of size, sensitivity, or publication state — should have a data card. A data card can be created at the same time as the dataset, or as early in the workflow as possible. Data cards may be updated over time as the dataset matures, and they may be shared publicly or kept private depending on the dataset's sensitivity and intended use.

### Choose your intended capabilities first

Version 1.2 of the Genesis Mission Data Card introduces six independent **intended capability** flags, set at the top of the data card. Each is a `"Yes"`/`"No"` switch that declares whether this data card is meant to support that capability, and each one turns on its own set of required/optional fields.

| Capability flag | Default | Meaning |
|---|---|---|
| `supports_discoverability` | **Always `"Yes"`** | Dataset can be found and identified in catalogs. Required for every data card, with no exceptions. |
| `supports_accessibility` | `"Yes"` \| `"No"` | Data card includes the metadata needed for others to know how to access the dataset (account, agreement, location, etc.). Recommended for all; required for datasets being shared. |
| `supports_interoperability` | `"Yes"` \| `"No"` | Data card includes the metadata needed to integrate or combine this dataset with others (formats, schema, provenance). |
| `supports_reusability` | `"Yes"` \| `"No"` | Data card includes licensing, stewardship, data quality, and citation metadata needed for reuse. |
| `supports_governed_use` | `"Yes"` \| `"No"` | Data card includes governance metadata (export control, privacy, rights, compliance, review history) for datasets subject to oversight. |
| `supports_ai_usability` | `"Yes"` \| `"No"` | Data card includes the metadata needed for AI/ML training, inference, or evaluation use. |

These capabilities are **not mutually exclusive tiers you "upgrade" through** — they are independent toggles. A datacard can have `supports_accessibility = "No"` and `supports_ai_usability = "Yes"` at the same time if that reflects the dataset's real situation. Setting a flag to `"Yes"` is a declaration of *intent* — it does not by itself certify that the dataset currently meets every criterion of that capability; it tells catalog tooling which fields to expect populated.

You can start with only `supports_discoverability = "Yes"` (everything else `"No"`) for a brand-new in-workflow dataset, and turn on more flags later as the datacard matures. The `change_log` field tracks these updates.

### Updates from v1.0 to v1.2 include
> **Mapping from the old profile model**, for teams migrating from v1.0:
> - `core` → `supports_discoverability = "Yes"` only
> - `extended` → also set `supports_accessibility = "Yes"`, `supports_interoperability = "Yes"`, `supports_reusability = "Yes"`
> - `ai_ready` → also set `supports_ai_usability = "Yes"`
> - `sensitive` → also set `supports_governed_use = "Yes"`
> - Use of CRediT-extended roles for `created_by` and `authors` (instead of the old `author_role` field)
> - `domain_metadata` support to capture domain-specific metadata in a structured way, rather than free-text `domain_metadata` field
> - `discoverability.datacard.updated_date` is now `[discoverability_if_applicable]` instead of `[discoverability_required]` to allow for datacards that are created but not yet updated.
> - `orcid` field pattern updated to allow uppercase letters in the ORCID identifier.

### Understanding field annotations

Every field in the template is annotated to tell you whether you need to fill it in. Annotations are now tied to capability flags:

| Annotation | Meaning |
|---|---|
| `[required]` | Required for **all** datacards regardless of which capability flags are set. |
| `[discoverability_required]` | Required because `supports_discoverability = "Yes"` (i.e., always, since this flag is mandatory). |
| `[discoverability_if_applicable]` | Optional under discoverability; populate if it applies, otherwise leave blank or delete. |
| `[accessibility_required]` | Required when `supports_accessibility = "Yes"`. |
| `[accessibility_if_applicable]` | Optional under accessibility. |
| `[interoperability_required]` | Required when `supports_interoperability = "Yes"`. |
| `[interoperability_if_applicable]` | Optional under interoperability. |
| `[reusability_required]` | Required when `supports_reusability = "Yes"`. |
| `[reusability_if_applicable]` | Optional under reusability. |
| `[governed_use_required]` | Required when `supports_governed_use = "Yes"`. |
| `[governed_use_if_applicable]` | Optional under governed use. |
| `[ai_usability_required]` | Required when `supports_ai_usability = "Yes"`. |
| `[ai_usability_if_applicable]` | Optional under AI usability. |
| `[reference_only_do_not_include]` | System-managed field shown only for reference; **do not** fill in or include this block in a submitted datacard. |

> **Note on conditional requirements:** many fields carry an additional condition beyond their capability flag — e.g. *"required if `cui_status` = `Yes`"* or *"required when `release_status` = `Approved` \| `Published`"*. These conditional requirements are called out field-by-field below; they apply on top of, not instead of, the capability-flag annotation.

### Understanding placeholder conventions

| Placeholder | Meaning |
|---|---|
| `${VALUE}` | Required for the capabilities you've enabled — you must replace this. |
| `__VALUE__` | Optional or conditional — replace if applicable, leave blank or delete if not. |
| `not_applicable` | Use this literal value when a field definitively does not apply to your dataset. |

**Important distinction:** leaving a field blank means the information is not yet known. Writing `not_applicable` means this field does not apply to this dataset. Catalog tooling uses this distinction for completeness scoring — blank fields may trigger reminders, while `not_applicable` fields are treated as complete.

### Single-entry vs. multi-entry fields

Throughout this guide, each field is marked as one of:
- **Single entry** — one object or scalar value (e.g., `dataset_description.dataset_summary`).
- **List (0 or more)** — a YAML list that may be left empty (`[]`) or contain multiple entries (e.g., `additional_ids`, `related_resources.datasets`).
- **List (1 or more required)** — a YAML list that must contain at least one entry when its parent capability is active (e.g., `authors`, `created_by`).

Watch for fields that nest a single-entry block inside a list item template — e.g., each entry under `created_by` contains its own `creator` block with sub-blocks for `person` / `organization` / `ai_model` / `software`. In some cases (e.g. dataset contact), only **one** of those four sub-blocks should be populated per entry, and the others deleted; in other cases (e.g., `created_by`), multiple entries may be present, each with its own populated sub-block.

### Yes \| No Fields
Yes or no fields are always single-entry, and the only valid values are `"Yes"` or `"No"` (case-sensitive and within quotes). Do not use `true`/`false`, `1`/`0`, or any other synonyms.

### Sensitivity — two independent fields, a critical concept

The template has two independent sensitivity blocks that are easy to confuse:

- **`discoverability.datacard.sensitivity`** — the sensitivity of *this data card document itself*
- **`discoverability.sensitivity`** — the sensitivity of *the dataset* the data card describes

These will often differ. A common and valid scenario: a researcher creates a publicly shareable data card (`discoverability.datacard.sensitivity.overall_sensitivity = Public`) that describes a dataset containing classified or controlled information (`discoverability.sensitivity.overall_sensitivity = CUI` or `Classified`). The open data card allows people to discover that the dataset exists and understand its general contents, while the underlying data remains protected.

**Never set these to match each other by default.** Set each one independently based on what it describes. The same independence applies to `accessibility.access_policy` fields, which describe access conditions for the *dataset* (not the data card).

### Workflow state vs. release status

Two fields describe complementary but distinct aspects of a dataset's lifecycle:

- **`discoverability.workflow.state`** — the technical/processing lifecycle position of the data itself (`Raw` → `Archived`)
- **`discoverability.release_status`** — the publication and governance state of the dataset record (`Draft` → `Deprecated`)

These should be kept logically consistent. Common alignments:

| `workflow.state` | Expected `release_status` |
|---|---|
| `Raw`, `Processing`, `QA`, `Analysis` | `Draft` |
| `Review` | `Under_Review` |
| `Embargo`, `Published` | `Approved` or `Published` |
| `Archived` | `Deprecated` or `Published` |

### Licenses and governance

A public/open license is not always the governing instrument for use. Some controlled datasets may not have an SPDX-style reuse license at all, and use may instead be governed by contract, agreement, institutional review, or repository policy — see the `governed_use` block for those cases.

### Schema validation

A companion LinkML/JSON Schema for machine validation is available in the Genesis data-cards repository. Validate your data card before submission using the Genesis LinkML data card validator, or any JSON Schema–compatible YAML validator.

---

## Section: Discoverability `[discoverability_required — always Yes]`

All required fields in this top-level `discoverability:` block are required for **all** datacards, regardless of which other capability flags are set, because `supports_discoverability` is always `"Yes"`. Populate `[discoverability_required]` fields for every dataset; `[discoverability_if_applicable]` fields are optional but recommended.

### Top-level capability flags

These six fields sit above the `discoverability:` block (i.e., at the document root, not nested under it).

| Field | Annotation | Single/Multi | Controlled vocabulary |
|---|---|---|---|
| `supports_discoverability` | `[required]` | Single | `"Yes"` (only valid value — always required and always Yes) |
| `supports_accessibility` | `[required]` | Single | `"Yes"` \| `"No"` |
| `supports_interoperability` | `[required]` | Single | `"Yes"` \| `"No"` |
| `supports_reusability` | `[required]` | Single | `"Yes"` \| `"No"` |
| `supports_governed_use` | `[required]` | Single | `"Yes"` \| `"No"` |
| `supports_ai_usability` | `[required]` | Single | `"Yes"` \| `"No"` |

Each flag is a high-level statement of *intent* — setting `supports_accessibility = "Yes"`, for example, declares that this datacard includes the metadata to support accessibility; it does not by itself certify that the dataset is currently accessible or meets every accessibility criterion.

---

### `discoverability.datacard` — Data Card Metadata

This sub-block describes the **data card document itself** — not the dataset.

#### `datacard.template_version`
- **Annotation:** `[discoverability_required]`
- **Single entry.**
- Do not modify. Fixed at `"1.2"` for this template version; used by parsers to apply correct version-specific validation logic.

#### `datacard.datacard_version`
- **Annotation:** `[discoverability_required]`
- **Single entry.**
- The version of this specific data card document — not the dataset, not the template. Start at `"1.0"` when first created.
- Use semantic versioning: increment PATCH (1.0 → 1.0.1) for minor corrections; MINOR (1.0 → 1.1) for content additions/updates; MAJOR (1.0 → 2.0) for structural changes (e.g., enabling/disabling a capability flag in a way that changes which sections are populated).
- Every time you update `datacard_version`, add a corresponding entry to `datacard.change_log`.

#### `datacard.filename`
- **Annotation:** `[discoverability_required]`
- **Single entry.**
- Follows the naming convention `genesis_datacard_<snake_case_dataset_name>.md`.
- If your dataset is not associated with the Genesis Mission, use a generic prefix like  `genesis_datacard_other_<snake_case_dataset_name>.md`.
- The `<snake_case_dataset_name>` portion should match `identification.name` converted to snake_case (lowercase, underscores instead of spaces, no special characters).
- Example: a dataset named "SNS Beam Position Monitor Data 2024" → `genesis_datacard_sns_beam_position_monitor_data_2024.md`
- Example: a non-Genesis funded dataset named "LCLS X-ray Diffraction Data" → `genesis_datacard_other_lcls_xray_diffraction_data.md`

#### `datacard.language`
- **Annotation:** `[discoverability_required]`
- **Single entry.**
- ISO 639-1 two-letter language code for the language this **data card document** is written in. Default `en`.
- Distinct from `interoperability.data_structure.language`, which describes the language of the *dataset content* (e.g., text corpora).

#### `datacard.id`
- **Annotation:** `[discoverability_if_applicable]`
- **Single entry** (sub-fields `type`, `value`).
- A persistent identifier (PID) for the data card document itself, distinct from the dataset identifier. Most data cards will not have this initially. Populate only if the data card has been registered in a catalog or repository as an independent citable object. Unregistered data cards should leave this block blank, delete it, or use the unregistered type/value pair without the value field (e.g., `type: unregistered`, `value: ""`).
- `type` controlled vocabulary (`IdentifierTypeEnum`): `ark` \| `doi` \| `handle` \| `local` \| `purl` \| `url` \| `urn` \| `uuid` \| `other` \| `unregistered`
- `value`: the identifier value.

#### `datacard.sensitivity` — sensitivity of the data card document
- **Annotation:** mixed — see sub-fields below.
- **Single entry** (one sensitivity block).
- See **Sensitivity — two independent fields** above. This block captures the sensitivity of the data card file itself — ask "if someone reads only this document, what is the most sensitive information they would see?"
- This is the same sub-structure used for `discoverability.sensitivity` (the dataset's sensitivity, documented later in this guide) — both blocks share an identical field layout, applied to different subjects.

| Field | Annotation | Single/Multi | Controlled vocabulary / format |
|---|---|---|---|
| `overall_sensitivity` | `[discoverability_required]` | Single | `OverallSensitivityEnum`: `Public` \| `Unclassified_Uncontrolled` \| `CUI` \| `UCNI` \| `Classified` \| `Legacy_Controlled` \| `Mixed` \| `Other_Controlled` |
| `source_marking_string` | `[discoverability_required]` | Single | Freetext — exact marking string as it appears on the source, if any |
| `source_marking_scheme` | `[discoverability_required]` | Single | `SourceMarkingSchemeEnum`: `DOE_CUI` \| `DOE_UCNI` \| `EO13526_Classified` \| `AEA_RD_FRD_TFNI` \| `DOD_CUI` \| `DHS_CUI` \| `Legacy_OUO` \| `Legacy_Site_Specific` \| `Other_Agency` \| `None` |
| `classified_status` | `[discoverability_required]` | Single | `"Yes"` \| `"No"` |
| `classification_level` | `[discoverability_if_applicable]` | Single | `Top_Secret` \| `Secret` \| `Confidential` (required if `classified_status = "Yes"`) |
| `classification_category` | `[discoverability_if_applicable]` | **List** | `NSI` \| `RD` \| `FRD` \| `TFNI` \| `Other_Classified` |
| `classified_control_markings` | `[discoverability_if_applicable]` | **List** | Freetext, e.g. `NOFORN`, `CNWDI`, `SIGMA 14`, `REL TO USA, CAN, GBR`, `ORCON` |
| `cui_status` | `[discoverability_required]` | Single | `"Yes"` \| `"No"` |
| `cui_basic_categories` | `[discoverability_if_applicable]` | **List** — at least one of `cui_basic_categories` / `cui_specified_categories` required if `cui_status = "Yes"` | DOE/ISOO-authoritative CUI Basic categories |
| `cui_specified_categories` | `[discoverability_if_applicable]` | **List** — see above | DOE/ISOO-authoritative CUI Specified categories |
| `cui_limited_dissemination_controls` | `[discoverability_if_applicable]` | **List** | e.g. `NOFORN`, `DL ONLY`, `REL TO USA, GBR`, `DISPLAY ONLY USA, GBR`, `RELIDO`. If populated with NOFORN/REL TO/similar, keep `foreign_national_access_status` (in Governed Use) consistent. |
| `ucni_status` | `[discoverability_required]` | Single | `"Yes"` \| `"No"` — represented separately from CUI; do not treat as an ordinary CUI category |
| `uk_mda_status` | `[discoverability_if_applicable]` | Single | `UKMDAStatusEnum`: `"Yes"` \| `"No"` \| `"Unknown"` \| `not_applicable` |
| `legacy_label_source` | `[discoverability_if_applicable]` | **List** | Freetext legacy/local labels, e.g. `OUO`, `SBU`. Populate if `source_marking_scheme = Legacy_OUO`. |
| `normalized_control_basis` | `[discoverability_if_applicable]` | **List** | `NormalizedControlBasisEnum`: `Classified` \| `CUI` \| `UCNI` \| `Public_Release_Approved` \| `Legacy_Needs_Mapping` \| `Other_Controlled`. If `source_marking_scheme = Legacy_OUO` and the marking is unresolved, populate as `Legacy_Needs_Mapping`. |

#### `datacard.created_date`
- **Annotation:** `[discoverability_required]`
- **Single entry.**
- ISO 8601 date (`YYYY-MM-DD`) this datacard was first created. Does not change once set.

#### `datacard.updated_date`
- **Annotation:** `[discoverability_if_applicable]`
- **Single entry.**
- ISO 8601 date of the most recent update. Update on every change, no matter how minor.

#### `datacard.change_log`
- **Annotation:** `[discoverability_required]`
- **List (1 or more required)** — append-only.
- A running chronological history of meaningful changes to this datacard. Add one entry each time you update it. Never delete or overwrite prior entries.
- The first entry is pre-filled with `"Initial creation"`.

| Sub-field | Format |
|---|---|
| `change_date` | ISO 8601 date of this change |
| `data_card_version` | Datacard version after this change (should match `datacard.datacard_version`) |
| `summary` | Brief plain-language description of what changed and why |


#### `datacard.creation_method`
- **Annotation:** `[discoverability_required]`
- **Single entry.**
- How this datacard was most recently created or updated.
- Controlled vocabulary (`DatacardCreationMethodEnum`): `Manual` (filled out entirely by hand) \| `Automated` (generated entirely by a pipeline/script/AI model with no human review) \| `Hybrid` (generated automatically, then reviewed/edited by a human)
- Update this field to reflect the method of the most recent significant update, not just the initial creation.

#### `datacard.created_by`
- **Annotation:** `[discoverability_required]`
- **List (1 or more required)**, in chronological order of contribution.
- All individuals, organizations, AI models, or software tools that created or updated this datacard. If an AI model generated the initial draft and a human then edited it, list the AI model entry first.

Each entry:

| Sub-field | Annotation | Notes |
|---|---|---|
| `contribution_date` | `[discoverability_required]` | ISO 8601 date of this specific contribution |
| `description` | `[discoverability_if_applicable]` | What this contributor did, e.g. "Automated generation of data card from dataset metadata" |
| `creator.agent_type` | `[discoverability_required]` | One of `person` \| `organization` \| `ai_model` \| `software` |

The `creator` block contains four optional sub-blocks (`person`, `organization`, `ai_model`, `software`) — **populate only the one matching `agent_type` and delete the other three.**

- **`person`** — for a human contributor: `given_name`, `family_name`, `orcid` *(if_applicable — format `https://orcid.org/0000-0000-0000-0000`; required where DOE employee/contractor author policy applies)*, `email`, `affiliation.name`, `affiliation.ror_id` *(if_applicable — format `https://ror.org/XXXXXXX`)*, `role` (**list**, see CRediT-extended `RoleEnum` below).
- **`organization`** — for a team/office/lab/site without a named individual: `name`, `ror_id`, `role` (**list**).
- **`ai_model`** — for an AI model that generated or substantially contributed content: `name` (e.g., "Chat GPT 5.5"), `version`, `accessed_date`, `identifier.type`/`identifier.value`, `role` (**list**), and `relationship` *(required for ai_model)* — see relationship vocabulary below.
- **`software`** — for an pipeline/script (not an LLM): `name`, `version`, `identifier.type`/`identifier.value`, `role` (**list**), and `relationship` *(required for software)*.

**`role` controlled vocabulary** (`RoleEnum`, extends CRediT taxonomy): `Conceptualization` \| `Data_Curation` \| `Formal_Analysis` \| `Funding_Acquisition` \| `Investigation` \| `Methodology` \| `Project_Administration` \| `Resources` \| `Software` \| `Supervision` \| `Validation` \| `Visualization` \| `Writing_Original_Draft` \| `Writing_Review_Editing` \| `Data_Collection` \| `Other`. (Full enum confirmed in schema; the truncated middle portion contains additional standard CRediT roles — Resources, Software, Supervision, Validation, Visualization, Writing roles — matching the template's listed set with no conflicts found.)

**`relationship` controlled vocabulary** (for `ai_model`/`software` entries only, `ExtendedRelationshipEnum`): `used_to_create` \| `used_to_process` \| `used_to_analyze` \| `recorded_by` \| `trained_on` \| `evaluated_on`. 

---

### `discoverability.identification`

Key metadata fields that uniquely identify this dataset.

#### `identification.name`
- **Annotation:** `[discoverability_required]`
- **Single entry.**
- A single human-readable name for this dataset. Use the same name (converted to snake_case) in the data card filename. If this data card covers a collection, provide the collection name.
- Be specific enough to distinguish this dataset from similar ones; avoid acronyms without expansion.
- Good example: "SNS Beam Position Monitor Calibration Data 2023–2024." Poor example: "BPM_data."

#### `identification.project`
- **Annotation:** `[discoverability_required]`
- **Single entry.**
- If the dataset is part of a Genesis project or sub-project, specify it here; otherwise, use "not_applicable". Used for catalog filtering and project-level reporting. Examples: `genesis` \| `genesis-fusion` \| `genesis-lightsource` \| `genesis-materials`. If unsure which project tag to use, contact your data manager.

#### `identification.version`
- **Annotation:** `[discoverability_required]`
- **Single entry.**
- The version of the dataset, using semantic versioning (`MAJOR.MINOR.PATCH`). Start at `1.0` for the first release.
- MAJOR: breaking changes (schema changed, files reorganized, fundamentally different dataset). MINOR: additions (new files, new variables, extended time range). PATCH: corrections (bug fixes, typo corrections, minor metadata updates).
- Distinct from `discoverability.datacard.datacard_version`, which tracks this document. See also `reusability.stewardship.versioning_strategy` for how versions are managed, and `supersedes` / `superseded_by` below for linking versions.

#### `identification.primary_id`
- **Annotation:** `[discoverability_required]`
- **Single entry** (sub-fields `type`, `value`).
- The primary persistent identifier for this dataset. Every dataset must have at least one identifier. Use `ark` or `local` if a DOI has not yet been assigned.
- `type` controlled vocabulary (`IdentifierTypeEnum`): `ark` \| `doi` \| `handle` \| `local` \| `purl` \| `url` \| `urn` \| `uuid` \| `other` \| `unregistered`
- ARK format: `ark:/NAAN/shoulder+assigned_name`, e.g. `ark:/12345/b2345679k`. Resolve via `https://n2t.net/ark:/NAAN/...`.
- Convention: use `ark` for pre-published states; mint a `doi` upon publication and retain the ARK in `additional_ids` for provenance continuity.

#### `identification.additional_ids`
- **Annotation:** `[discoverability_if_applicable]`
- **List (0 or more).**
- Additional identifiers for this dataset — secondary identifiers, legacy identifiers, or version-specific identifiers if `primary_id` is a collection-level identifier.
- Each entry: `type` (`IdentifierTypeEnum`, as above), `value` (e.g., `SAND2024-XXXXX` \| `LAUR-XX-XXXXX`).

#### `identification.supersedes`
- **Annotation:** `[discoverability_if_applicable]`
- **Single entry** (sub-fields `type`, `value`).
- Identifier of the prior version this dataset replaces. See `reusability.stewardship.versioning_strategy` for how versions are managed.
- `type`: `doi` \| `ark` \| `handle` \| `url` \| `local` \| `other`.

#### `identification.superseded_by`
- **Annotation:** `[discoverability_if_applicable]`
- **Single entry** (sub-fields `type`, `value`).
- Identifier of the newer version that replaces this dataset. Populate when this version is deprecated.

#### `identification.parent_collection`
- **Annotation:** `[discoverability_if_applicable]`
- **Single entry.**
- Parent collection or experimental campaign this dataset belongs to, when this dataset is one of many in a larger organized collection or ensemble.
- Sub-fields: `name`, `identifier.type` (`doi` \| `ark` \| `handle` \| `url` \| `local` \| `other`), `identifier.value`.

---

### `discoverability.dataset_description`

#### `dataset_description.science_domain`
- **Annotation:** `[discoverability_if_applicable]`
- **Single entry.**
- Extends the OSTI Subject Areas list with an `Other` category for datasets that don't fit.
- Controlled vocabulary (`ScienceDomainEnum`): `Biology and Medicine` \| `Chemistry` \| `Energy Storage, Conversion, and Utilization` \| `Engineering` \| `Environmental Sciences` \| `Fission and Nuclear Technologies` \| `Fossil Fuels` \| `Geosciences` \| `Materials` \| `Mathematics and Computing` \| `National Defense` \| `Physics` \| `Power Generation and Distribution` \| `Renewable Energy` \| `Other`.

#### `dataset_description.dataset_summary`
- **Annotation:** `[discoverability_required]`
- **Single entry.**
- The most important descriptive field in the entire data card. Write 1–3 sentences clearly explaining what this dataset is, in plain language accessible to a broad scientific audience unfamiliar with your specific project.
- Ask yourself: if a colleague outside your group found this dataset in the catalog, would this summary tell them whether it's relevant to their work?
- Good example: "This dataset contains time-series beam position monitor (BPM) readings from the Spallation Neutron Source (SNS) at ORNL, collected during accelerator commissioning runs in Q3 2023. Data includes horizontal and vertical beam positions at 120 monitor locations sampled at 1 MHz, with associated timestamps and beam current measurements. Intended for accelerator physics analysis and ML-based anomaly detection model development." Poor example: "BPM data from SNS 2023."

#### `dataset_description.purpose`
- **Annotation:** `[discoverability_if_applicable]`
- **Single entry.**
- Why was this dataset created? What scientific or operational question does it address? What gap does it fill? Distinct from `intended_use` (in `governed_use.use_governance`), which describes how the dataset should be used — `purpose` explains the motivation for creating it.

#### `dataset_description.collection_methodology`
- **Annotation:** `[discoverability_if_applicable]`
- **Single entry.**
- How was the data acquired? e.g., `experimental sensors` \| `computational simulation` \| `human annotation` \| `derived from prior datasets` — freetext, expand as needed.

#### `dataset_description.data_characteristics`
- **Annotation:** `[discoverability_if_applicable]`
- **Single entry.**
- Key structural and content characteristics that help users assess suitability — scale, dimensionality, temporal coverage, spatial resolution, or other notable properties.

#### `dataset_description.limitations`
- **Annotation:** `[discoverability_if_applicable]`
- **Single entry.**
- Known limitations, gaps, biases, or caveats users should be aware of before using this dataset. Be candid — undisclosed limitations that surface later damage trust in both the dataset and the catalog.

#### `dataset_description.tags`
- **Annotation:** `[discoverability_if_applicable]`
- **Single entry** (structured tag block).
- Structured tags for catalog filtering and discovery.
- `project`: e.g., `genesis` (should align with `identification.project`).
- `science`: freetext, e.g., `lightsource` \| `fusion` \| `materials` \| `biology`.
- `object_type`: controlled vocabulary (`ObjectTypeEnum`): `Dataset` \| `Model` \| `Software` \| `AI_Agent` \| `Infrastructure` \| `Resource` \| `Other`.

#### `dataset_description.task_category`
- **Annotation:** `[discoverability_if_applicable]`; at least one value required if `task_subcategory` is present.
- **List (0 or more).**
- Primary ML task category or categories for this dataset. Populate for AI-ready data; helps ML practitioners find relevant datasets in the catalog.
- Freetext examples: `classification` \| `regression` \| `segmentation` \| `detection` \| `generation` \| `translation` \| `summarization` \| `ranking` \| `anomaly_detection` \| `clustering` \| `reinforcement_learning` \| `other`.

#### `dataset_description.task_subcategory`
- **Annotation:** `[discoverability_if_applicable]`
- **List (0 or more).**
- More specific ML task subcategory or subcategories. Freetext examples: `binary_classification` \| `multi_class_classification` \| `multi_label_classification` \| `image_segmentation` \| `object_detection` \| `time_series_forecasting` \| `named_entity_recognition` \| `question_answering` \| `other`.

#### `dataset_description.keywords`
- **Annotation:** `[discoverability_required]`
- **List (1 or more required).**
- Terms that describe this dataset and aid discovery. Include a mix of domain terms (e.g., `neutron scattering`, `plasma physics`), method terms (e.g., `Monte Carlo simulation`, `machine learning`), instrument/facility terms (e.g., `Spallation Neutron Source`, `DIII-D`), and relevant ontology terms if known (e.g., `ENVO:00002006`).

---

### `discoverability.product_type`
- **Annotation:** `[discoverability_required]`
- **Single entry.**
- Primary type of product described by this data card. Aligns with and extends the STI Product Types to support interoperability with STI catalogs and the OSTI DOE Data Explorer.
- Controlled vocabulary (`ProductTypeEnum`): `Technical_Report` \| `Paper_or_Proceedings` \| `Journal_Article` \| `Software_Manual` \| `Data` \| `Collection` \| `Computer_Related` \| `Model` \| `Agent`.
- `Data` is expected here for a data card describing a dataset; select the best fit if this data card describes a different type of product.

### `discoverability.dataset_type`
- **Annotation:** `[discoverability_if_applicable]`
- **Single entry.**
- OSTI DOE Data Explorer type code. Select the single best fit.
- Controlled vocabulary (`DatasetTypeEnum`):

| Code | Type | Use when |
|---|---|---|
| `GD` | Genome/Genetic Data | DNA/RNA sequences, genetic markers, genomic annotations |
| `IM` | Image | Photographs, scans, microscopy, visualizations |
| `ND` | Numeric Data | Measurements, time series, tabular data, sensor readings |
| `SM` | Specialized Mix | Multiple data types combined in one dataset |
| `FP` | Figure/Plot | Charts or graphs as the primary deliverable |
| `I` | Interactive Resource | Web apps, dashboards, interactive visualizations |
| `MM` | Multimedia | Audio, video, combined media |
| `MD` | Model | Computational models, simulations, trained ML models |
| `AS` | Automated Software | Scripts, analysis pipelines, workflows |
| `IP` | Instrumentation/Protocols | Experimental protocols, instrument specifications |
| `IG` | Integrated Genomic Resources | Combined genomic databases and tools |

> If in doubt between `ND` and `SM`, use `ND` if the data is primarily numeric and `SM` if it genuinely combines distinct data types (e.g., images + tabular measurements + text annotations).

---

### `discoverability.release_status`
- **Annotation:** `[discoverability_required]`
- **Single entry.**
- Current publication and governance state of this dataset. See **Workflow state vs. release status** in Part 1 for expected alignment with `workflow.state`.
- Controlled vocabulary (`ReleaseStatusEnum`):

| Value | Meaning |
|---|---|
| `Draft` | Work in progress; not ready for sharing outside the immediate team |
| `Under_Review` | Submitted for formal review (security, export control, IRB, etc.) |
| `Approved` | Review complete; cleared for release |
| `Published` | Publicly released and accessible. Does not necessarily indicate the dataset was reviewed and approved by a formal governing body — reference the security section, categorization tags, and especially the `reviews` history for the actual review/approval status. |
| `Deprecated` | Superseded or retired; no longer recommended for use |

### `discoverability.dataset_publisher`
- **Annotation:** `[discoverability_if_applicable]`, required when `release_status = Approved` \| `Published`.
- **Single entry.**
- Entity responsible for making this dataset available. Often the same as the primary research organization, but may differ if a separate publisher is involved.
- Sub-fields: `name` (organization or individual that published this dataset), `ror_id` (format `https://ror.org/XXXXXXX`).

---

### `discoverability.contact`
- **Annotation:** `[discoverability_required]`
- **Single entry.**
- The primary point of contact for questions about this **dataset**. Required for all data cards — every dataset must have a reachable contact. This is who users will reach out to with questions, problems, or collaboration interest. If the dataset is part of a larger collection, the contact may be for the collection as a whole.
Contacts may only be valid until a certain date (e.g., for students, postdocs, or term staff), which can be provided in the `valid_until` field. If the contact is temporary, provide a `succession_note` with instructions for who to contact (role or person) if the primary contact is no longer reachable.
- `agent_type`: only `person` is allowed as the primary contact (to ensure accountability and a clear point of contact), or `organization` (e.g., a data management office, if no single named contact is appropriate).
- `person` sub-fields: `given_name`, `family_name`, `orcid` *(if_applicable — format `https://orcid.org/0000-0000-0000-0000`; required where DOE employee/contractor author policy applies)*, `email`, `affiliation.name`, `affiliation.ror_id` *(if_applicable)*.
- `valid_until` *(if_applicable)*: date after which this contact may no longer be valid — use for project-bound contacts (students, postdocs, term staff).
- `succession_note` *(if_applicable)*: who to contact if this contact is no longer reachable, e.g., "Contact the ORNL data management office at data@ornl.gov."
- Choose a contact who will be reachable for the foreseeable future. For datasets with long retention periods, consider whether the named contact will still be associated with the project in 5–10 years.

### `discoverability.additional_contacts`
- **Annotation:** `[discoverability_if_applicable]`
- **List (0 or more).**
- Additional contacts (e.g., instrument PI, data steward). Same structure as `contact` above, with `type: person | organization` per entry.

---

### `discoverability.authors`
- **Annotation:** `[discoverability_required]` — at least one author required. For draft or in-workflow datasets, populate with known contributors as early as possible.
- **List (1 or more required).**
- Authors are individuals or organizations with primary intellectual responsibility for the dataset — typically the PI, lead scientist, or data creator. For supporting roles (technicians, annotators, submitters), use `contributors` instead.
- Each entry: `type: person | organization`.
  - `person`: `given_name`, `family_name`, `orcid` *(if_applicable — strongly recommended; enables disambiguation and credit tracking; required where DOE employee/contractor author policy applies)*, `email` *(if_applicable)*, `affiliation.name`, `affiliation.ror_id` *(if_applicable)*, `role` (**list**, CRediT-extended `RoleEnum`, see above).
  - `organization`: `name`, `ror_id`, `role` (**list**).

### `discoverability.contributors`
- **Annotation:** `[discoverability_if_applicable]`
- **List (0 or more).**
- Supporting contributors who are not primary authors — e.g., sample preparers, annotators, reviewers, submitters. Same structure as `authors` above.

---

### `discoverability.sponsor_organizations`
- **Annotation:** `[discoverability_required]`
- **List (1 or more required).**
- Organizations that funded or sponsored this dataset. Populate with known information even for in-workflow data — this supports provenance tracking and credit assignment from the earliest stages of the project.
- Each entry: `name` (e.g., `DOE Office of Science` \| `NNSA` \| `NSF`), `ror_id` *(if_applicable)*, `award_number` *(if_applicable, e.g., `DE-AC05-00OR22725`)*, `funding_source` *(if_applicable — controlled vocabulary `FundingSourceEnum`: `DOE_Program_SC` \| `DOE_Program_NNSA` \| `LDRD` \| `WFO` \| `CRADA` \| `Other_Federal` \| `State_Government` \| `Subcontract` \| `Industry` \| `Nonprofit` \| `Internal` \| `Other`)*, `program` *(if_applicable, e.g., "Advanced Scientific Computing Research")*.

### `discoverability.sponsoring_doe_program_office`
- **Annotation:** `[discoverability_if_applicable]`
- **Single entry.**
- DOE program office that sponsored this dataset, if applicable.

### `discoverability.sponsoring_doe_subprogram`
- **Annotation:** `[discoverability_if_applicable]`
- **Single entry.**
- DOE subprogram that sponsored this dataset, if applicable.

---

### `discoverability.research_organizations`
- **Annotation:** `[discoverability_required]`
- **List (1 or more required).**
- Organizations that created or collected the data. Populate with known information even for in-workflow data, for the same provenance/credit reasons as `sponsor_organizations`.
- Each entry: `name` (e.g., `Oak Ridge National Laboratory` \| `Sandia National Laboratories`), `ror_id` *(if_applicable)*.

---

### `discoverability.facilities`
- **Annotation:** `[discoverability_if_applicable]`
- **List (0 or more).**
- User facilities, HPC centers, or research infrastructure used to collect, process, or store the dataset. Populate with known information even for in-workflow data.
- Each entry: `name` (e.g., `Spallation Neutron Source` \| `Summit` \| `Frontier`), `ror_id` *(if_applicable)*, `role` (**list**, CRediT-extended `RoleEnum`), `location.description` *(if_applicable, e.g., "SNS Beamline 1B, Oak Ridge National Laboratory, TN, USA")*, `location.ror_id` *(if_applicable — ROR ID of the facility, cross-reference with `name`)*.

---

### `discoverability.sensitivity` — sensitivity of the dataset

- **Annotation:** mixed — see sub-fields below.
- **Single entry.**
- Sensitivity of the **dataset** described by this data card — distinct from `discoverability.datacard.sensitivity`, the sensitivity of the data card document itself. See **Sensitivity — two independent fields** in Part 1. This structure is intended to preserve authoritative source markings/designations while minimizing redundant manual entry, separating actual source marking/control information from adjacent governance metadata (export control, privacy, rights, release, and records status — captured in `governed_use`).
- This sub-block shares an identical field layout with `discoverability.datacard.sensitivity` (see above for the full field table — `overall_sensitivity`, `source_marking_string`, `source_marking_scheme`, `classified_status`, `classification_level`, `classification_category`, `classified_control_markings`, `cui_status`, `cui_basic_categories`, `cui_specified_categories`, `cui_limited_dissemination_controls`, `ucni_status`, `uk_mda_status`, `legacy_label_source`, `normalized_control_basis`), applied here to the dataset rather than the document.

---

### `discoverability.workflow`
- **Annotation:** `[discoverability_required]` for `state`; other sub-fields `[discoverability_if_applicable]`.
- **Single entry.**
- Describes the technical and processing lifecycle position of the dataset. See **Workflow state vs. release status** in Part 1 for expected alignment with `release_status`.

#### `workflow.state`
- **Annotation:** `[discoverability_required]`
- **Single entry.**
- Current lifecycle position. Controlled vocabulary (`StateEnum`):

| Value | Meaning |
|---|---|
| `Raw` | Data as collected in its original, unprocessed form |
| `Processing` | Actively being cleaned, transformed, or reduced |
| `QA` | Undergoing quality assurance or validation |
| `Analysis` | In active scientific analysis |
| `Review` | Under formal review (security, export control, IRB, etc.) |
| `Embargo` | Complete but intentionally withheld from release until `embargo_until` date |
| `Published` | Publicly released |
| `Archived` | Preserved and no longer actively maintained |
| `not_applicable` | Lifecycle state does not apply to this dataset |

#### `workflow.is_intermediate`
- **Annotation:** `[discoverability_if_applicable]`
- **Single entry.**
- `"Yes"` if this dataset is an intermediate product in a processing pipeline (not a final deliverable); `"No"` if this is a final or publication-intended product.
- Example: raw detector output before calibration is intermediate; calibrated, analysis-ready data is final.

#### `workflow.pipeline_stage`
- **Annotation:** `[discoverability_if_applicable]`
- **Single entry.**
- Freetext description of where this dataset sits in a specific processing pipeline, useful when `workflow.state` alone is not granular enough. Examples: "post-detector, pre-reconstruction" \| "raw telemetry, pre-calibration."

#### `workflow.embargo_until`
- **Annotation:** `[discoverability_if_applicable]`, required if `workflow.state = Embargo`.
- **Single entry.**
- ISO 8601 date after which release is permitted.

---

## Section: Accessibility `[accessibility_required when supports_accessibility = "Yes"]`

Metadata elements that describe how this dataset can be accessed — access policy, access endpoints, and scale information. Important for users to understand how they can obtain the dataset and any restrictions that may apply. Access policy is distinct from sensitivity (which describes the nature of the data and its risks) and from release status (which describes the publication state of the dataset record).

---

### `accessibility.access_policy`

Describes who can access this dataset and under what conditions.

#### `access_policy.access_level`
- **Annotation:** `[accessibility_required]`
- **Single entry.**
- The level of permissions required for users to access the dataset.
- Controlled vocabulary (`AccessLevelEnum`):

| Value | Meaning |
|---|---|
| `Open` | No additional permissions required beyond standard account registration and agreement to terms of service. The dataset is freely accessible to the public and usable without special permissions. Note: `Open` does not necessarily mean free of copyright or other legal restrictions — only that there are no additional access controls. Users may still need to comply with applicable laws or regulations. |
| `Restricted` | Access may be granted to users who meet certain criteria — being part of a specific research community, having a legitimate research purpose, or agreeing to specific terms and conditions. The dataset is not freely accessible to the public. |
| `Controlled` | Access is tightly controlled and may require specific authorization, agreements, or approvals. The dataset contains sensitive information and only authorized users can access it. |

#### `access_policy.access_restrictions`
- **Annotation:** `[accessibility_if_applicable]`
- **Single entry.**
- Freetext description of access restrictions, e.g., "Requires signed DUA" \| "None - publicly accessible."

#### `access_policy.authorization_required`
- **Annotation:** `[accessibility_if_applicable]`, required if `access_level` is not `Open`.
- **List.**
- The specific type(s) of authorization required to access this dataset.
- Controlled vocabulary (`AuthorizationRequiredEnum`):

| Value | Meaning |
|---|---|
| `Account` | A registered account in the repository system |
| `User_Agreement` | Acceptance of a user agreement or terms of service |
| `Data_Use_Agreement` | A formal signed Data Use Agreement (DUA) |
| `Sponsor_Approval` | Approval from the dataset sponsor or PI |
| `Export_Control_Review` | A completed export control review |
| `IRB_Approval` | Institutional Review Board approval |
| `Other` | Describe in `access_restrictions` |

#### `access_policy.intended_partner_classes`
- **Annotation:** `[accessibility_if_applicable]`
- **List.**
- The intended partner classes or user groups for this dataset, if any.
- Controlled vocabulary (`IntendedPartnerClassEnum`): `Internal_Team` \| `Tri_Lab` \| `DOE_NNSA_Lab` \| `Federal_Partner` \| `Contractor` \| `Academic_Researchers` \| `External_Research_Partner` \| `Public` \| `Industry_Partner` \| `Other`.
- If absent or null, this field is not yet known or determined. Use an empty list (`[]`) if definitively no specific partner classes are targeted. Use `Public` if this dataset is intended for broad public use without restrictions.

#### `access_policy.approved_environments`
- **Annotation:** `[accessibility_if_applicable]`
- **List.**
- Freetext description of the approved environment(s) for access, if more than one applies — e.g., "DOE HPC facilities with export control review" \| "On-site access only at Oak Ridge National Laboratory."
- An empty list (`[]`) means no explicitly approved environments; access may still be granted case-by-case. `null` or absent means it has not yet been determined whether approved environments are required.

#### `access_policy.policy_url`
- **Annotation:** `[accessibility_if_applicable]`
- **Single entry.**
- URL to the full access policy document.

#### `access_policy.policy_text`
- **Annotation:** `[accessibility_if_applicable]`
- **Single entry.**
- Inline summary of the access policy if no `policy_url` exists.

---

### `accessibility.access`

Complete the fields you know at the time of data card creation. Repository-assigned fields (landing pages, accession numbers, access protocols) will be populated by the managing repository or catalog system at ingest — see the `_repository` block.

#### `access.current_location`
- **Annotation:** `[accessibility_required]`
- **Single entry.**
- Where the data physically resides right now. Use for in-workflow data not yet deposited in a repository, or for any dataset with a known internal or external storage path.
- Examples: `/mnt/ecs/scientific-data/project/dataset/` \| `/lustre/orion/proj-shared/dataset/` \| `s3://genesis-bucket/dataset/`.

#### `access.publicly_facing_landing_page_url`
- **Annotation:** `[accessibility_if_applicable]`
- **Single entry.**
- URL to the publicly facing landing page for this dataset — the URL that should be shared publicly and included in citations. May differ from `current_location` if the dataset is not yet publicly released, or if `current_location` is an internal storage path.

#### `access.intended_repositories`
- **Annotation:** `[accessibility_if_applicable]`
- **List (0 or more).**
- Repositories you intend to deposit or have deposited this dataset in. The managing repository or catalog system resolves and populates repository-assigned fields at ingest (see the `_repository` block). Repositories may be institutional, project-owned, community, or national (e.g., Zenodo, an institutional data repository, or a project data store).

Each entry:

| Sub-field | Annotation | Notes |
|---|---|---|
| `name` | `[accessibility_if_applicable]` | e.g., "Zenodo" \| "Globus" \| "internal" |
| `access_level` | `[accessibility_if_applicable]` | Intended access level for this repository: `Open` \| `Restricted` \| `Controlled` (`AccessLevelEnum`). The same dataset may have different access levels per repository. |
| `is_primary` | `[accessibility_if_applicable]` | `"Yes"` \| `"No"` — only one entry should be marked `"Yes"` |
| `date_deposited` | `[accessibility_if_applicable]` | ISO 8601 date |
| `data_services` | `[accessibility_if_applicable]` | **List** — see below |

`intended_repositories[].data_services` — populate if a Data Service / API endpoint exists for this dataset in this repository. Aligns with `dcterms:DataService`. List all that apply.

| Sub-field | Notes |
|---|---|
| `name` | e.g., "REST API" \| "GraphQL endpoint" |
| `endpoint` | URL |
| `documentation_url` | URL |
| `authentication` | Controlled vocabulary (`AuthenticationTypeEnum`): `None` \| `API_Key` \| `OAuth2` \| `SAML` \| `Certificate` \| `OpenID_Connect` \| `Basic_Auth` \| `Bearer_Token` \| `Other` |
| `version` | Freetext |
| `rate_limit` | e.g., "1000 requests/hour" |

---

### `accessibility.dataset_scale`
- **Annotation:** `[accessibility_if_applicable]`
- **Single entry.**
- Physical size and record counts for the dataset. Fill in what you know — even approximate values help catalog users assess whether a dataset is practical to download and use.

| Sub-field | Notes |
|---|---|
| `record_count` | Number of primary records, samples, or files |
| `record_unit` | `samples` \| `files` \| `records` \| `timesteps` \| `images` \| `tokens` \| `other` |
| `compressed_bytes` | Total dataset size when compressed, in bytes |
| `uncompressed_bytes` | Total dataset size when uncompressed, in bytes |

---

## Section: Interoperability `[interoperability_required when supports_interoperability = "Yes"]`

Metadata elements that describe the interoperability of this dataset — context of data collection, data structure, provenance, related resources, schema, and domain-specific metadata. Important for users to understand how they can use the dataset and what tools or software they may need to work with it.

---

### `interoperability.data_structure`

#### `data_structure.formats`
- **Annotation:** `[interoperability_required]`
- **List (1 or more required).**
- File formats present in this dataset. Be specific, including version where relevant. Example: `["CSV", "HDF5", "NetCDF4", "Parquet", "TIFF", "JSON"]`.

#### `data_structure.encoding`
- **Annotation:** `[interoperability_if_applicable]`
- **Single entry.**
- Character encoding for text-based formats, e.g. `UTF-8` \| `ASCII` \| `Latin-1`. UTF-8 is strongly recommended for new datasets. Use `not_applicable` for binary formats (HDF5, NetCDF, TIFF, etc.).

#### `data_structure.schema_version`
- **Annotation:** `[interoperability_if_applicable]`
- **Single entry.**
- Version of the data schema used in this dataset — distinct from `discoverability.datacard.datacard_version`. Increment when field names, types, or structure change between dataset versions in a way that would break existing parsers.

#### `data_structure.modalities`
- **Annotation:** `[interoperability_required]`
- **List (1 or more required).**
- Data modalities present in the dataset. Example: `["tabular", "image", "time-series", "text", "graph", "point-cloud"]`.

#### `data_structure.features`
- **Annotation:** `[interoperability_required]`
- **List (1 or more required).**
- Primary variables, fields, or features in the dataset. **Choose one form and use it consistently — do not mix flat strings and structured entries.**
  - **Basic documentation form** (flat list): each entry has only a `name`, e.g. `- name: temperature`.
  - **AI-ready structured form** (replaces the flat list): each entry has `name`, `data_type` (`float` \| `int` \| `string` \| `boolean` \| `datetime` \| `other`), `unit`, `description`, `range`.
    - Example:
    ```yaml
    - name: temperature
      data_type: float
      unit: kelvin
      description: "Measured temperature at the sample location."
      range: [0, 1000]
    ```

#### `data_structure.splits`
- **Annotation:** `[interoperability_if_applicable]`
- **List (0 or more).**
- Dataset splits, if the dataset is pre-divided. Example: `["train", "test", "validation"]`.

#### `data_structure.language`
- **Annotation:** `[interoperability_if_applicable]`
- **Single entry.**
- ISO 639-1 language code for the **dataset content** (e.g., text corpora, annotation labels) — distinct from `discoverability.datacard.language`, which describes the data card document's language. Use `not_applicable` for non-linguistic data (numeric, image, simulation output, etc.).

#### `data_structure.spatial_coverage`
- **Annotation:** `[interoperability_if_applicable]`
- **Single entry.**
- Geographic coverage of the dataset. Use for geospatial datasets or facility-based experiments.

| Sub-field | Notes |
|---|---|
| `description` | Freetext, e.g. "Continental United States" \| "SNS Beamline 1B, ORNL" |
| `geo_location_box.westBoundLongitude` | WGS84 decimal degrees; aligns with `datacite:geoLocationBox` / `datacite:westBoundLongitude` |
| `geo_location_box.eastBoundLongitude` | aligns with `datacite:eastBoundLongitude` |
| `geo_location_box.southBoundLatitude` | aligns with `datacite:southBoundLatitude` |
| `geo_location_box.northBoundLatitude` | aligns with `datacite:northBoundLatitude` |

Use `geo_location_box` for genuine area coverage; `description` alone is sufficient for most facility-based experimental data.

#### `data_structure.temporal_coverage`
- **Annotation:** `[interoperability_if_applicable]`
- **Single entry** (sub-fields `start_date`, `end_date`, `description`).
- Time period the **dataset content** represents — aligns with `schema:temporalCoverage`. Distinct from `interoperability.dates.data_collection_start`/`data_collection_end`, which describe when collection occurred. Use `temporal_coverage` when the dataset describes a specific historical or projected time period that differs from when collection happened.
- Example: monthly climate averages for 1950–2020, collected in 2024 → `temporal_coverage.start_date = 1950-01-01`, `temporal_coverage.end_date = 2020-12-31`, while `dates.data_collection_start = 2024-01-01`.
- `start_date` / `end_date` align with `dcterms:coverage`.

---

## Section: Interoperability `[interoperability_required when supports_interoperability = "Yes"]`

---

### `interoperability.provenance`

Describes how this dataset was created, what it was derived from, and what processing was applied.

#### `provenance.was_generated_by`
- **Annotation:** `[interoperability_required]`
- **Single entry.**
- High-level description of the generating process. Even a one-line answer dramatically improves catalog value.
- Examples: "Neutron scattering experiment at SNS Beamline 1B" \| "Monte Carlo simulation using MCNP 6.2" \| "Derived from raw telemetry via calibration pipeline v2.1".

#### `provenance.source_data`
- **Annotation:** `[interoperability_if_applicable]`
- **List (0 or more).**
- Source datasets this dataset was derived from.
- Each entry: `name`, `identifier.type` (`doi` \| `ark` \| `handle` \| `url` \| `local` \| `other`), `identifier.value`, `relationship` (base `RelationshipTypeEnum`: `is_derived_from` \| `is_based_on` \| `is_part_of` \| `has_part` \| `references` \| `other`).

#### `provenance.processing_steps`
- **Annotation:** `[interoperability_required]`
- **Single entry.**
- Key processing, cleaning, calibration, or transformation steps applied to produce this dataset from raw or source data. Include enough detail that a knowledgeable person in your domain could understand what was done.

#### `provenance.instrumentation`
- **Annotation:** `[interoperability_if_applicable]`
- **Single entry.**
- Instruments, sensors, detectors, or equipment used for data collection. Include make, model, and version where relevant. For computational datasets, this may describe the compute hardware used.

#### `provenance.simulation_details`
- **Annotation:** `[interoperability_if_applicable]`
- **Single entry.**
- For simulation-derived data: the simulation code, version, key parameters, and configuration. Example: "LAMMPS 23Jun2022, NVT ensemble, 300K, 10ns run, CHARMM36".

#### `provenance.software_environment`
- **Annotation:** `[interoperability_if_applicable]`
- **Single entry.**
- The software environment used to generate or process this dataset — captures what is needed for computational reproducibility.

| Sub-field | Notes |
|---|---|
| `os` | e.g., "RHEL 8.6" \| "Ubuntu 22.04" |
| `compiler` | e.g., "GCC 11.3" \| "Intel oneAPI 2023.1" |
| `container` | e.g., "docker://registry/image:tag" |
| `hpc_environment` | e.g., "module load python/3.10 cuda/11.8 openmpi/4.1" |
| `notes` | Additional environment details, key library versions, or a reference to a full environment manifest, e.g. "See requirements.txt in dataset root" |

```yaml
software_environment:
  os: "Ubuntu 22.04"
  compiler: "GCC 11.3"
  container: "docker://registry/image:tag"
  hpc_environment: "module load python/3.10 cuda/11.8 openmpi/4.1"
  notes: "See requirements.txt in dataset root"
```

---

### `interoperability.dates`
- **Annotation:** `[interoperability_if_applicable]`
- **Single entry.**

| Sub-field | Notes |
|---|---|
| `data_collection_start` | ISO 8601 date data collection or generation began |
| `data_collection_end` | ISO 8601 date data collection or generation ended |
| `issued` | ISO 8601 date the dataset was first publicly released |
| `modified` | ISO 8601 date of the most recent significant modification |

All dates ISO 8601 (`YYYY-MM-DD`). See `data_structure.temporal_coverage` above for the distinction between when data was *collected* (these `dates` fields) and the time period the data *represents* (`temporal_coverage`).

---

### `interoperability.semantic_layer`
- **Annotation:** `[interoperability_if_applicable]`
- **Single entry.**
- Formal schema and semantic context information. To support agentic use, federated use, or cross-domain use, populate `schema_url` at minimum.

| Sub-field | Single/Multi | Notes |
|---|---|---|
| `schema_url` | Single | URL to a formal schema for this dataset, e.g. a JSON Schema, XML Schema, or NeXus application definition |
| `semantic_context` | **List (0 or more)** | Semantic conventions applied, e.g. "NetCDF CF Conventions 1.10" \| "NeXus NXmonopd" |

---

### `interoperability.related_resources`
- **Annotation:** `[interoperability_if_applicable]`
- **Single entry** (containing four list sub-fields below).
- Links to related datasets, publications, software, and AI models.
- **Base relationship vocabulary** (`RelationshipTypeEnum`, applies to all resource types): `is_derived_from` \| `is_based_on` \| `is_part_of` \| `has_part` \| `references` \| `other`.
- **Extended relationship vocabulary** (`ExtendedRelationshipEnum`, software and AI models only — extends the base vocabulary, so base values remain valid too): `used_to_create` \| `used_to_process` \| `used_to_analyze` \| `recorded_by` \| `trained_on` \| `evaluated_on`.

#### `related_resources.datasets`
- **List (0 or more).**
- Each entry: `name`, `identifier.type` (`doi` \| `ark` \| `handle` \| `url` \| `local` \| `other`), `identifier.value`, `relationship` (base vocabulary).

Example:
```yaml
related_resources:
  datasets:
    - name: "Example Dataset A"
      identifier:
        type: "doi"
        value: "10.1234/example.dataset.a"
      relationship: "is_derived_from"
    - name: "Example Dataset B"
      identifier:
        type: "url"
        value: "https://example.org/dataset/b"
      relationship: "is_part_of"
```

#### `related_resources.publications`
- **List (0 or more).**
- Each entry: `type` (`doi` \| `ark` \| `arxiv` \| `url` \| `report` \| `other`), `value`, `relationship` (base vocabulary).

Example:
```yaml
related_resources:
  publications:
    - type: "doi"
      value: "10.5678/example.publication"
      relationship: "references"
    - type: "arxiv"
      value: "arXiv:2101.12345"
      relationship: "is_based_on"
```

#### `related_resources.software`
- **List (0 or more).**
- Each entry: `name`, `version`, `identifier.type`/`identifier.value`, `role` (**list**, CRediT-extended `RoleEnum`), `relationship` (extended vocabulary — software entries may use `used_to_create`, `used_to_process`, `used_to_analyze`, etc., in addition to the base vocabulary).

Example:
```yaml
related_resources:
  software:
    - name: "Example Software X"
      version: "1.2.3"
      identifier:
        type: "doi"
        value: "10.9876/example.software.x"
      role: 
        - "Software"
        - "Data Curation"
      relationship: "used_to_process"
```

#### `related_resources.ai_models`
- **List (0 or more).**
- Each entry: `name`, `version`, `accessed_date`, `identifier.type`/`identifier.value`, `role` (**list**, CRediT-extended `RoleEnum`), `relationship` (extended vocabulary — AI model entries may use `trained_on`, `evaluated_on`, etc., in addition to the base vocabulary).

Example:
```yaml
related_resources:
  ai_models:
    - name: "Example AI Model Y"
      version: "v0.9"
      accessed_date: "2024-01-15"
      identifier:
        type: "doi"
        value: "10.5432/example.ai.model.y"
      role:
        - "Software"
        - "Data Curation"
      relationship: "trained_on"
```

---

### `interoperability.domain_metadata`
- **Annotation:** `[interoperability_if_applicable]`
- **List (0 or more).**
- Any additional domain-specific metadata not otherwise captured in the data card. Supports multiple entries so a single dataset can carry metadata for more than one domain or schema. Domain-specific metadata supplements the discoverability-level metadata and should not replace the common metadata expected elsewhere in the data card.

Each entry:

| Sub-field | Annotation | Notes |
|---|---|---|
| `name` | `[interoperability_if_applicable]` | e.g., "Accelerator Operations Metadata" \| "Climate Data Variables" |
| `description` | `[interoperability_if_applicable]` | Freetext description of the domain-specific metadata, its purpose, and any important details |
| `science_domain` | `[interoperability_if_applicable]` | `ScienceDomainEnum` — same controlled vocabulary as `discoverability.dataset_description.science_domain` (see prior installment) |
| `schema_reference.type` | `[interoperability_if_applicable]` | `doi` \| `url` \| `ark` \| `handle` \| `local` \| `other` |
| `schema_reference.value` | `[interoperability_if_applicable]` | Identifier value for the referenced schema |
| `version` | `[interoperability_if_applicable]` | Version of the domain-specific schema or metadata convention used |
| `fields` | `[interoperability_if_applicable]` | **Map** of key-value pairs — see below |

`domain_metadata[].fields` is a map keyed by field name (not a list). For each named field, populate:

| Sub-field | Notes |
|---|---|
| `field_value` | The value for this domain-specific metadata field; the specific value depends on the field and schema referenced above |
| `data_type` | The data type of the value (e.g., `string`, `integer`, `float`, `boolean`) |
| `unit` | Unit of measurement for the value, if applicable |
| `description` | Description of the field and its significance |

Example:
```yaml
domain_metadata:
  - name: "Accelerator Operations Metadata"
    description: "Metadata specific to accelerator operations, including beam parameters and machine settings."
    science_domain: "Physics"
    schema_reference:
      type: "doi"
      value: "10.1234/accelerator.metadata.schema"
    version: "1.0"
    fields:
      beam_energy:
        field_value: 120
        data_type: "float"
        unit: "GeV"
        description: "The energy of the particle beam."
      beam_current:
        field_value: 0.5
        data_type: "float"
        unit: "mA"
        description: "The current of the particle beam."
  - name: "Climate Data Variables"
    description: "Metadata for climate datasets, including temperature and precipitation variables."
    science_domain: "Environmental Sciences"
    schema_reference:
      type: "url"
      value: "https://example.org/climate-data-schema"
    version: "2.1"
    fields:
      avg_temperature:
        field_value: 15.5
        data_type: "float"
        unit: "Celsius"
        description: "Average temperature over the specified period."
      total_precipitation:
        field_value: 120
        data_type: "float"
        unit: "mm"
        description: "Total precipitation over the specified period."
```
---


## Section: Reusability `[reusability_required when supports_reusability = "Yes"]`

Metadata elements that describe the reusability of this dataset — license and rights, stewardship, data quality, citation, and integrity information. Important for users to understand the legal and ethical considerations for using the dataset, who is responsible for maintaining it, and how its quality and integrity have been assessed.

---

### `reusability.license`
- **Annotation:** `[reusability_if_applicable]`, required when `release_status = Approved` \| `Published`. Use `pending` if not yet assigned.
- **Single entry.**
- The license governing use of this dataset. Note: a public/open license is not always the governing instrument — some controlled datasets may not have an SPDX-style reuse license at all, and use may instead be governed by contract, agreement, institutional review, or repository policy (see the `governed_use` block for those cases).

| Sub-field | Annotation | Notes |
|---|---|---|
| `spdx_id` | `[reusability_if_applicable]` | SPDX license identifier — see https://spdx.org/licenses/ for the full list. Common choices: `CC-BY-4.0` \| `CC0-1.0` \| `Apache-2.0` \| `MIT`. Use `Other` if the license is not in the SPDX registry. Use `pending` if not yet assigned. |
| `name` | `[reusability_if_applicable]` | Required if `spdx_id = Other` — the human-readable license name. |
| `url` | `[reusability_if_applicable]` | URL to the full license text, or `LICENSE.md` if the license file is in the same repository as the dataset. |
| `known_contractual_rights` | `[reusability_if_applicable]` | Freetext legal rights statement, separate from the license. Important for DOE/NNSA datasets, which may have complex contractual arrangements that affect how data can be used and shared beyond what the license terms specify. Examples: "Government has unlimited rights" \| "Contractor retains rights with government license." |

Example:
```yaml
reusability:
  license:
    spdx_id: "CC-BY-4.0"
    name: "Creative Commons Attribution 4.0 International"
    url: "https://creativecommons.org/licenses/by/4.0/"
    known_contractual_rights: "Government has unlimited rights."
```

### `reusability.additional_licenses`
- **Annotation:** `[reusability_if_applicable]`
- **List (0 or more).**
- Additional licenses that apply to subsets of the dataset — for example, if the dataset contains third-party data under different licensing terms. Each entry uses the same sub-fields as `reusability.license` above, plus a `description` field explaining which subset of the data the entry applies to.

---

### `reusability.stewardship`
- **Annotation:** `[reusability_if_applicable]`
- **Single entry.**
- Describes ongoing maintenance responsibilities and versioning approach for this dataset.
- **Note on versioning:** three fields work together to fully describe versioning. `discoverability.identification.version` carries the version number; `identification.supersedes` / `identification.superseded_by` link versions together; and `stewardship.versioning_strategy` describes how versioning is managed over time.

#### `stewardship.level`
- **Annotation:** `[reusability_if_applicable]`
- **Single entry.**
- Who is responsible for ongoing maintenance of this dataset.
- Controlled vocabulary (`StewardshipLevelEnum`):

| Value | Meaning |
|---|---|
| `Project_Managed` | Maintained by the originating project or research team, with maintenance and updates occurring based on project resources and priorities. |
| `Repository_Managed` | Maintained by the repository or catalog system where the dataset is hosted, with ongoing curation to ensure long-term accessibility. |
| `Externally_Managed` | Maintained by an external organization or entity, such as a government agency, research institution, or commercial provider. |
| `not_applicable` | Stewardship level is not applicable or not yet known. |

#### `stewardship.maintainer`
- **Annotation:** `[reusability_if_applicable]`
- **Single entry.**
- The specific person or organization responsible for ongoing maintenance. May differ from the dataset contact or authors.
- `type`: `person` \| `organization` — populate only the matching sub-block and delete the other.
  - `person`: `given_name`, `family_name`, `orcid` *(if_applicable)*, `email`, `affiliation.name`, `affiliation.ror_id` *(if_applicable)*.
  - `organization`: `name`, `ror_id` *(if_applicable)*.

#### `stewardship.update_frequency`
- **Annotation:** `[reusability_if_applicable]`
- **Single entry.**
- How often this dataset is updated after its initial release.
- Controlled vocabulary (`UpdateFrequencyEnum`): `None` \| `Ad_Hoc` \| `Monthly` \| `Quarterly` \| `Annually` \| `Continuously` \| `Other`.

#### `stewardship.retention_policy`
- **Annotation:** `[reusability_if_applicable]`
- **Single entry.**
- Freetext description of how long the dataset will be retained and where. For DOE datasets, reference the applicable data management policy. Example: "Retained for 10 years per DOE data management policy."

#### `stewardship.versioning_strategy`
- **Annotation:** `[reusability_if_applicable]`
- **Single entry.**
- Freetext description of how versions are tracked, archived, and retired. Examples: "Semantic versioning; all versions retained indefinitely in Zenodo" \| "Major versions only; prior versions available on request from data steward."

---

### `reusability.data_quality`
- **Annotation:** `[reusability_required]`
- **Single entry.**
- Be specific throughout this block. Vague entries like "good quality" or "data is clean" reduce trust and reuse. Provide enough information for a user to assess whether quality is adequate for their intended use.

#### `data_quality.completeness`
- **Annotation:** `[reusability_required]`
- **Single entry.**
- What fraction of expected data is present? What is missing and why? Example: "All 120 BPM channels present; 2.1% of timesteps missing due to instrument downtime on 2023-04-12 (14:00–16:30 UTC)."

#### `data_quality.known_issues`
- **Annotation:** `[reusability_required]`
- **Single entry.**
- Specific known errors, anomalies, or artifacts. Example: "Sensor drift observed in BPM channels 45–48 after 2023-06-01T12:00:00Z — apply drift correction factor from calibration file." Use `not_applicable` if there are genuinely no known issues, rather than leaving blank.

#### `data_quality.validation_methods`
- **Annotation:** `[reusability_required]`
- **Single entry.**
- How data quality was assessed. Example: "Cross-validated against NIST SRM 640f reference standard; outlier detection using 3σ threshold."

#### `data_quality.noise_characteristics`
- **Annotation:** `[reusability_if_applicable]`
- **Single entry.**
- The nature and magnitude of noise in the dataset.

#### `data_quality.uncertainty_notes`
- **Annotation:** `[reusability_if_applicable]`
- **Single entry.**
- Formal uncertainty quantification if available. Example: "Measurement uncertainty ±0.5% (k=2) per ISO/IEC Guide 98-3 (GUM)."

#### `data_quality.missing_data_codes`
- **Annotation:** `[reusability_if_applicable]`
- **List (0 or more).**
- Codes used to represent missing or invalid data in the dataset files. Documenting these is critical for downstream analysis pipelines and AI/ML workflows that need to handle missing values correctly.
- Each entry: `code` (e.g., `-999` \| `NaN` \| `NULL`), `description` (e.g., "Sensor malfunction — value not collected" \| "Below detection limit").

---

### `reusability.citation`
- **Annotation:** `[reusability_if_applicable]`, required when `release_status = Approved` \| `Published`. Replace all `${...}` placeholders before publishing.
- **Single entry.**
- Citation information for this dataset.

#### `citation.report_number`
- **Annotation:** `[reusability_if_applicable]`
- **Single entry.**
- Institutional report or release number, if applicable. Examples: `SAND2024-XXXXX` \| `LAUR-XX-XXXXX` \| `ORNL/TM-2024/XXXXX`.

#### `citation.preferred_citation`
- **Annotation:** `[reusability_if_applicable]`
- **Single entry.**
- The recommended citation for this dataset. All sub-fields below are `[reusability_if_applicable]`; however, when `preferred_citation` is included, `author`, `title`, `year`, and `publisher` are required within it, and at least one of `doi` or `url` must be provided.

| Sub-field | Conditional requirement | Notes |
|---|---|---|
| `author` | Required if `preferred_citation` is included | e.g., "Smith, John A.; Doe, Jane B." |
| `title` | Required if `preferred_citation` is included | e.g., "Neutron Scattering Data from SNS Beamline 1B, April 2023" |
| `year` | Required if `preferred_citation` is included | e.g., `2024` |
| `publisher` | Required if `preferred_citation` is included | e.g., "Oak Ridge National Laboratory" \| "DOE NNSA" |
| `howpublished` | At least one of `publisher` or `howpublished` required | e.g., "(Version v1) [Data set]. Zenodo" \| "Available at https://doi.org/..." |
| `doi` | At least one of `doi` or `url` required | e.g., `10.1234/zenodo.1234567` |
| `url` | At least one of `doi` or `url` required | e.g., `https://doi.org/10.1234/zenodo.1234567` |
| `eprinttype` | Optional | e.g., `arxiv` \| `biorxiv` \| `report_number` \| `other` |
| `eprint` | Optional | e.g., `1234.56789` \| `SAND2024-XXXXX` |
| `note` | Optional | Freetext note for identifiers that don't fit cleanly into other fields. For ARKs or other non-DOI identifiers in legacy BibTeX contexts, use the format: `Available at \url{ark:/12345/abcde}` |

Example citation block:
```yaml
citation:
  report_number: "SAND2024-12345"
  preferred_citation:
    author: "Smith, John A.; Doe, Jane B."
    title: "Neutron Scattering Data from SNS Beamline 1B, April 2023"
    year: 2024
    publisher: "Oak Ridge National Laboratory"
    doi: "10.1234/zenodo.1234567"
```
---

### `reusability.integrity`
- **Annotation:** `[reusability_if_applicable]`
Checksum and fixity information for the dataset. If `checksum_available = "Yes"`, then `checksum_type` and `checksum_value` are required. If `checksum_available = "No"`, then `checksum_type` and `checksum_value` must be absent or null.

#### `integrity.checksum_available`
- **Annotation:** `[reusability_if_applicable]`
- **Single entry.**
- `"Yes"` if a checksum is available for the primary data file(s); `"No"` if not. If `"Yes"`, then `checksum_type` and `checksum_value` are required. If `"No"`, then `checksum_type` and `checksum_value` should be absent.

#### `integrity.checksum_type`
- **Annotation:** `[reusability_if_applicable]`, required if `checksum_available = "Yes"`.
- **Single entry.**
- The checksum algorithm used. `sha256` is strongly recommended for new datasets. `sha512` is also acceptable. `md5` is not recommended for new datasets due to known collision vulnerabilities, but is acceptable for legacy datasets where SHA-256 is unavailable. `other` may be used with a description.

#### `integrity.checksum_value`
- **Annotation:** `[reusability_if_applicable]`, required if `checksum_available = "Yes"`.
- **Single entry.**
- The checksum of the primary data file(s). For multi-file datasets, create a checksum manifest file listing checksums for every file in the dataset, and provide the path or URL to that manifest here rather than individual file checksums.

#### `integrity.fixity_policy`
- **Annotation:** `[reusability_if_applicable]`
- **Single entry.**
- Freetext description of how and how often data integrity is verified after ingest. Example: "Monthly SHA-256 verification via repository integrity service; alerts on mismatch."

---
## Section: Governed Use `[governed_use_required when supports_governed_use = "Yes"]`

Metadata elements that describe the governance of this dataset — how it may be used, what export control and privacy obligations apply, what rights and agreements are required, compliance status, and the history of any formal reviews it has undergone. Important for users and automated systems to understand any oversight processes or restrictions that govern the dataset's use and sharing.

---

### `governed_use.use_governance`
- **Annotation:** `[governed_use_required]`
- **Single entry.**
- Describes the current and intended use of this dataset, as well as any explicit permitted, out-of-scope, or prohibited uses. For datasets that are actively in use in workflows, or where use governance is needed to manage risks, ensure responsible use, or enable discoverability for specific use cases.

#### `use_governance.current_use`
- **Annotation:** `[governed_use_required]`
- **Single entry.**
- What is this dataset actively being used for right now? Relevant for in-workflow data. Distinct from `intended_use`, which describes the eventual purpose. Example: "Active training data for the Genesis anomaly detection pipeline" \| "Currently under analysis for accelerator physics publication."

#### `use_governance.intended_use`
- **Annotation:** `[governed_use_if_applicable]`
- **Single entry.**
- Tasks or workflows this dataset is designed to support. Examples: "ML training" \| "physics analysis" \| "benchmarking" \| "visualization." Distinct from `dataset_description.purpose` (in Discoverability), which explains the scientific motivation for creating the dataset — `intended_use` focuses on the specific workflows and tasks the dataset is suited for.

#### `use_governance.permitted_use`
- **Annotation:** `[governed_use_if_applicable]`
- **Single entry.**
- Uses this dataset is suitable for beyond its primary `intended_use`. Example: "Exploratory analysis" \| "Hypothesis generation" \| "Educational use."

#### `use_governance.out_of_scope_use`
- **Annotation:** `[governed_use_if_applicable]`
- **Single entry.**
- Uses this dataset should NOT be applied to, even if not explicitly prohibited. Be specific — vague statements like "not for sensitive applications" are difficult for pipeline tooling to act on. Examples: "Not suitable for real-time accelerator control — data latency precludes safety-critical use" \| "Not for clinical decision-making — data was collected under non-clinical conditions."

#### `use_governance.prohibited_use`
- **Annotation:** `[governed_use_if_applicable]`
- **Single entry.**
- Uses that are explicitly prohibited for this dataset. Examples: "Any use involving human subjects" \| "Commercial applications" \| "Use in high-risk domains without prior approval."

#### `use_governance.need_to_know_basis`
- **Annotation:** `[governed_use_if_applicable]`
- **List (0 or more).**
- If access to this dataset is restricted based on a need-to-know requirement, list the specific basis or bases for that restriction.
- Controlled vocabulary (`NeedToKnowBasisEnum`):

| Value | Meaning |
|---|---|
| `Mission_Need` | Access restricted based on mission needs or operational requirements |
| `Job_Duty` | Access restricted based on job duties or role-based access controls |
| `Project_Program_Association` | Access restricted based on association with a specific project or program |
| `Agreement_Defined` | Access restricted based on terms defined in a user agreement, DUA, or other formal agreement |
| `DGB_Exception_Waiver` | Access granted via an exception or waiver from the Data Governance Board or equivalent governing body |

Example `use_governance:` block:
```yaml
use_governance:
  current_use: "Active training data for the Genesis anomaly detection pipeline"
  intended_use: "ML training for anomaly detection in accelerator operations"
  permitted_use: "Exploratory analysis and educational use"
  out_of_scope_use: "Not suitable for real-time accelerator control — data latency precludes safety-critical use"
  prohibited_use: "Any use involving human subjects or clinical decision-making"
  need_to_know_basis:
    - "Mission_Need"
    - "Project_Program_Association"
```

---

### `governed_use.non_sensitivity_governance_metadata`
- **Annotation:** `[governed_use_required]`
- **Single entry.**
- Governance-relevant metadata that may affect sharing and use decisions but is not part of the source sensitivity or marking block itself (those are captured in `discoverability.sensitivity`). This block describes governance as it applies to the dataset as a whole — which may differ from the sensitivity or classification of any source data from which it was derived.

#### `non_sensitivity_governance_metadata.export_control`
- **Annotation:** `[governed_use_required]`
- **Single entry.**

##### `export_control.export_control_status`
- **Annotation:** `[governed_use_required]`
- **Single entry.**
- Whether this dataset is subject to export control restrictions.
- Controlled vocabulary (`YesNoPendingUnknownEnum`): `"Yes"` \| `"No"` \| `"Pending_Review"` \| `"Unknown"` — always use quoted strings to prevent YAML from interpreting as booleans.

##### `export_control.export_control_basis`
- **Annotation:** `[governed_use_if_applicable]`, required if `export_control_status = "Yes"`.
- **Single entry.**
- The regulatory basis for the export control classification.
- Controlled vocabulary (`ExportControlBasisEnum`): `ITAR` \| `EAR` \| `DOE_Nuclear_Export_Control` \| `Other` \| `not_applicable`.
- If unsure of the correct basis, consult your institution's export control office before selecting a value other than `not_applicable`.

##### `export_control.foreign_national_access_status`
- **Annotation:** `[governed_use_if_applicable]`
- **Single entry.**
- Governance-facing outcome field indicating whether foreign national access is allowed, restricted, prohibited, or conditional, based on the combined effect of applicable export, classification, dissemination, agreement, or other source-authoritative constraints. This is not an export-control-only field — it synthesizes the net access outcome across all relevant constraints.
- Controlled vocabulary (`ForeignNationalAccessStatusEnum`): `Allowed` \| `Restricted` \| `Prohibited` \| `Conditional` \| `Unknown`.
- Keep consistent with `discoverability.sensitivity.cui_limited_dissemination_controls` — if that field contains `NOFORN`, `REL TO`, `DISPLAY ONLY`, or similar controls, this field should reflect that (e.g., `Prohibited` or `Conditional`).

---

#### `non_sensitivity_governance_metadata.privacy`
- **Annotation:** `[governed_use_required]`
- **Single entry.**

##### `privacy.privacy_status`
- **Annotation:** `[governed_use_required]`
- **Single entry.**
- Whether this dataset raises any privacy concerns.
- Controlled vocabulary (`YesNoPendingUnknownEnum`): `"Yes"` \| `"No"` \| `"Pending_Review"` \| `"Unknown"`.

##### `privacy.pii_status`
- **Annotation:** `[governed_use_required]`
- **Single entry.**
- Whether this dataset contains personally identifiable information (PII).
- Controlled vocabulary (`YesNoPendingUnknownEnum`): `"Yes"` \| `"No"` \| `"Pending_Review"` \| `"Unknown"`.

##### `privacy.phi_status`
- **Annotation:** `[governed_use_required]`
- **Single entry.**
- Whether this dataset contains protected health information (PHI).
- Controlled vocabulary (`YesNoPendingUnknownEnum`): `"Yes"` \| `"No"` \| `"Pending_Review"` \| `"Unknown"`.

##### `privacy.privacy_control_basis`
- **Annotation:** `[governed_use_if_applicable]`
- **List (0 or more).** Select all that apply.
- The regulatory or policy basis for any privacy controls applied to this dataset.
- Controlled vocabulary (`PrivacyControlBasisEnum`): `HIPPA` \| `Privacy_Act` \| `Human_Subjects` \| `Other_Regulated_Privacy` \| `Site_Specific` \| `not_applicable`.

##### `privacy.privacy_regime_notes`
- **Annotation:** `[governed_use_if_applicable]`
- **Single entry.**
- Optional freetext notes for privacy regimes or handling nuances not fully captured by the controlled vocabulary values above.

---

#### `non_sensitivity_governance_metadata.rights_release_records`
- **Annotation:** `[governed_use_required]`
- **Single entry.**

##### `rights_release_records.ip_restriction_type`
- **Annotation:** `[governed_use_if_applicable]`
- **Single entry.**
- The type of intellectual property restriction applied to this dataset, if any.
- Controlled vocabulary (`IPRestrictionTypeEnum`):

| Value | Meaning |
|---|---|
| `Proprietary` | Dataset contains proprietary information; distribution is restricted |
| `Limited_Rights` | Government may use but not disclose outside government |
| `Restricted_Rights` | Computer software with limited government rights |
| `Government_Purpose_Rights` | Government may use and disclose only for government purposes |
| `Unlimited_Rights` | Government has unlimited rights to use, disclose, reproduce, and distribute |
| `Third_Party_Licensed` | Dataset contains third-party licensed content with specific terms |
| `None` | No IP restrictions apply |

##### `rights_release_records.agreement_required`
- **Annotation:** `[governed_use_required]`
- **Single entry.**
- Whether a rights release agreement is required for use of this dataset.
- `"Yes"` \| `"No"` (always quoted).

##### `rights_release_records.agreement_type`
- **Annotation:** `[governed_use_if_applicable]`, required if `agreement_required = "Yes"`.
- **List (0 or more).** Select all that apply.
- The type(s) of agreement required for use or access.
- Controlled vocabulary (`AgreementTypeEnum`): `DUA` \| `CRADA` \| `MOU` \| `NDA` \| `LICENSE` \| `WFO` \| `OTHER`.

##### `rights_release_records.public_release_status`
- **Annotation:** `[governed_use_required]`
- **Single entry.**
- Whether this dataset has been approved for public release.
- Controlled vocabulary (`PublicReleaseStatusEnum`):

| Value | Meaning |
|---|---|
| `Approved` | Dataset has been approved for public release |
| `Pending` | Public release review is in progress |
| `Not_Approved` | Dataset has not been approved for public release |
| `Requires_STI_Review` | Dataset requires Scientific and Technical Information (STI) review before release status can be determined |

##### `rights_release_records.record_status`
- **Annotation:** `[governed_use_required]`
- **Single entry.**
- Whether this dataset constitutes a record that must be retained under applicable records management policies.
- Controlled vocabulary (`RecordStatusEnum`):

| Value | Meaning |
|---|---|
| `Federal_Record` | Dataset is a Federal record subject to federal records management requirements |
| `Contractor_Record` | Dataset is a contractor record subject to applicable contract records requirements |
| `Non_Record` | Dataset is not considered a record for records management purposes |
| `Mixed` | Dataset contains a mix of records and non-records |
| `Unknown` | Records status has not yet been determined |

---

### `governed_use.compliance`
- **Annotation:** `[governed_use_required]`
- **Single entry.**
- Compliance confirmation fields. Populate when `release_status = Under_Review` \| `Approved` \| `Published`. Leave blank or omit for `Draft` and in-workflow datasets.
- All three fields use `YesNoUnknownNotApplicableEnum`: `"Yes"` \| `"No"` \| `"Unknown"` \| `"not_applicable"` — always use quoted strings.

| Sub-field | Notes |
|---|---|
| `doe_data_management_plan` | Whether a DOE Data Management Plan (DMP) is on file for this dataset. Use `not_applicable` if the dataset is not DOE-funded. |
| `osti_elink2_metadata_compliant` | Whether the metadata in this data card complies with OSTI E-Link 2.0 API specifications. If unsure, check with your data manager before setting to `"Yes"`. |
| `irb_approved` | Whether Institutional Review Board (IRB) approval has been obtained. Use `not_applicable` if the dataset does not involve human subjects — do not use `"No"`, which implies an IRB review was needed but not obtained. |

---

### `governed_use.review_provenance_companion`
- **Annotation:** `[governed_use_if_applicable]`
- **List (0 or more)** — append-only.
- A running chronological history of all formal reviews this dataset has undergone or is currently undergoing. Add one entry per review event. Do not overwrite or delete prior entries — this is an append-only record that supports audit and compliance. This block allows multiple review records to be captured in a structured format, which is especially useful for datasets that have undergone multiple reviews or have complex review histories.

Each entry:

| Sub-field | Annotation | Notes |
|---|---|---|
| `source_review_reference` | `[governed_use_if_applicable]` | Type of review: e.g., `internal_qa` \| `security` \| `export_control` \| `irb` \| `partner` \| `publication` \| `other` |
| `review_purpose` | `[governed_use_if_applicable]` | Freetext description of why this review was conducted, e.g., "Export control review prior to public release" |
| `source_review_authority` | `[governed_use_if_applicable]` | The authority conducting or overseeing the review, e.g., "DOE Export Control Officer" \| "ORNL IRB" |
| `review_contact_name` | `[governed_use_if_applicable]` | Name of the primary contact for this review, if applicable |
| `review_contact_email` | `[governed_use_if_applicable]` | Email of the primary contact for this review, if applicable |
| `reviewed_by` | `[governed_use_if_applicable]` | Person or organization that conducted the review — `type: person \| organization`. Populate only the matching sub-block (`person`: `given_name`, `family_name`, `email`, `ror_id`; `organization`: `name`, `ror_id`) and delete the other. |
| `decontrol_or_declassify_on` | `[governed_use_if_applicable]` | ISO 8601 date (`"YYYY-MM-DD"`) when this dataset will be decontrolled or declassified, if known. Use `"not_applicable"` for datasets that are not export-controlled or classified. |
| `review_date` | `[governed_use_if_applicable]` | ISO 8601 date (`"YYYY-MM-DD"`) the review was completed or last updated. Use `"not_applicable"` if not yet completed. |
| `comments` | `[governed_use_if_applicable]` | Reviewer notes, conditions, or required follow-up actions |

Example review provenance entry:
```yaml
review_provenance_companion:
  - source_review_reference: "export_control"
    review_purpose: "Export control review prior to public release"
    source_review_authority: "DOE Export Control Officer"
    review_contact_name: "Jane Doe"
    review_contact_email: "jane.doe@example.com"
    reviewed_by:
      type: "person"
      person:
        given_name: "Jane"
        family_name: "Doe"
        email: "jane.doe@example.com"
        ror_id: "https://ror.org/012345678"
    decontrol_or_declassify_on: "2025-12-31"
    review_date: "2024-06-15"
    comments: "Dataset approved for public release with no restrictions."
  - source_review_reference: "irb"
    review_purpose: "IRB review for human subjects data"
    source_review_authority: "ORNL IRB"
    review_contact_name: "Dr. John Smith"
    review_contact_email: "john.smith@example.com"
    reviewed_by:
      type: "person"
      person:
        given_name: "John"
        family_name: "Smith"
        email: "john.smith@example.com"
        ror_id: "https://ror.org/987654321"
    decontrol_or_declassify_on: "not_applicable"
    review_date: "2024-06-15"
    comments: "IRB review completed with no restrictions."
```
---

## Section: AI Usability `[ai_usability_required when supports_ai_usability = "Yes"]`

Metadata elements that describe whether and how this dataset may be used in AI/ML workflows — training, inference, or evaluation. Be explicit throughout this block: these fields are read by automated pipeline tooling and AI agents, which make decisions about whether a dataset can be ingested into a workflow. Vague or blank entries may cause pipelines to reject the dataset or apply incorrect handling.

---

### `ai_usability.ai_usage`
- **Annotation:** `[ai_usability_required]`
- **Single entry.**

#### `ai_usage.training_use_status`
- **Annotation:** `[ai_usability_required]`
- **Single entry.**
- Whether this dataset may be used for training AI/ML models.
- Controlled vocabulary (`YesNoConditionalEnum`): `"Yes"` \| `"No"` \| `"Conditional"` — always use quoted strings.

| Value | Meaning |
|---|---|
| `"Yes"` | Suitable for use in AI/ML training workflows |
| `"No"` | Should not be used for AI/ML training |
| `"Conditional"` | Suitable for training only under the conditions described in `training_use_conditions` |

#### `ai_usage.training_use_conditions`
- **Annotation:** `[ai_usability_if_applicable]`, required if `training_use_status = "Conditional"`.
- **Single entry.**
- Specific conditions or restrictions that must be met for this dataset to be used in training. Be explicit — vague conditions are difficult for pipeline tooling to enforce. Examples: "Only for non-commercial research" \| "Requires citation of SAND2024-XXXXX" \| "Not for use in models intended for clinical decision-making."

#### `ai_usage.inference_use_status`
- **Annotation:** `[ai_usability_required]`
- **Single entry.**
- Whether this dataset may be used for inference with AI/ML models.
- Controlled vocabulary (`YesNoConditionalEnum`): `"Yes"` \| `"No"` \| `"Conditional"`.

#### `ai_usage.inference_use_conditions`
- **Annotation:** `[ai_usability_if_applicable]`, required if `inference_use_status = "Conditional"`.
- **Single entry.**
- Specific conditions or restrictions that must be met for this dataset to be used in inference. Example: "Inference outputs must be reviewed by a domain expert before operational use."

#### `ai_usage.evaluation_use_status`
- **Annotation:** `[ai_usability_required]`
- **Single entry.**
- Whether this dataset may be used for evaluation of AI/ML models.
- Controlled vocabulary (`YesNoConditionalEnum`): `"Yes"` \| `"No"` \| `"Conditional"`.

#### `ai_usage.evaluation_use_conditions`
- **Annotation:** `[ai_usability_if_applicable]`, required if `evaluation_use_status = "Conditional"`.
- **Single entry.**
- Specific conditions or restrictions that must be met for this dataset to be used in evaluation. Example: "Evaluation results may not be published without prior review by the originating team."

#### `ai_usage.restrictions`
- **Annotation:** `[ai_usability_required]`
- **Single entry.**
- Any specific restrictions or conditions on using this dataset in AI/ML workflows beyond what is captured in the per-task status and conditions fields above. Be explicit — use `not_applicable` if there are no restrictions rather than leaving this blank. Examples: "Not for use in models intended for clinical decision-making" \| "Export-controlled data — AI model outputs may themselves be export-controlled."

#### `ai_usage.bias_risks`
- **Annotation:** `[ai_usability_required]`
- **Single entry.**
- Known or potential bias risks or representational gaps that could affect the behavior of models trained on or evaluated against this dataset. Use `not_applicable` if no bias risks are known, rather than leaving blank. Examples: "Dataset overrepresents samples from facility X operating under nominal conditions; underrepresents fault and off-normal states" \| "Predominantly collected from a single demographic group, which may introduce bias in downstream models."

#### `ai_usage.safety_considerations`
- **Annotation:** `[ai_usability_required]`
- **Single entry.**
- Safety or ethical considerations for AI/ML use of this dataset. Use `not_applicable` if none apply. Examples: "Outputs may be export-controlled — review before sharing model outputs derived from this dataset" \| "Dataset includes sensitive operational parameters; models trained on it should not be deployed in safety-critical contexts without independent validation."

#### `ai_usage.human_review_required`
- **Annotation:** `[ai_usability_required]`
- **Single entry.**
- Whether a human must review AI/ML outputs derived from this dataset before they are used or acted upon.
- `"Yes"` \| `"No"` — always quoted.

---

## Section: Repository-Managed `[reference_only_do_not_include]`

> ⚠️ **Do not include this block in a completed data card.** The `_repository` block is shown in the template for reference only. These metadata are intended to be populated entirely by the managing repository or catalog system. The underscore prefix (`_repository`) signals to parsers that this block is system-owned. Submitting a data card with this block manually populated will cause validation errors.

This block is included in the template so authors understand what metadata the managing system will add. Fields are listed here for reference.

| Field | Notes |
|---|---|
| `populated_by_repository` | Always `true`; signals to parsers that this block is system-owned |
| `ingest_date` | ISO 8601 date this data card was ingested by the managing system |
| `repository_catalog_id` | Identifier assigned to this data card by the managing catalog |
| `completeness_score` | Catalog-computed completeness score against the fields expected for the declared intended capabilities |
| `datacard_checksum.type` | Checksum algorithm used for the data card document (`sha256` \| `sha512`) |
| `datacard_checksum.value` | Checksum of the raw data card `.md` file as ingested; recomputed on each ingest to detect post-ingest modifications |
| `repositories[].name` | Echoed from `accessibility.access.intended_repositories.name` |
| `repositories[].identifier.type` | Authoritative repository identifier type (`ror` \| `url` \| `local` \| `other`) |
| `repositories[].identifier.value` | Authoritative repository identifier value; ROR ID preferred |
| `repositories[].dataset_landing_page` | Human-readable dataset page assigned by the repository |
| `repositories[].dataset_download_url` | Direct download URL assigned by the repository |
| `repositories[].dataset_id_in_repo` | Accession number or ID assigned by this repository |
| `repositories[].access_protocol` | Protocol used to access the dataset (`https` \| `ftp` \| `s3` \| `globus` \| `nfs` \| `lustre` \| `other`) |
| `usage_metrics.download_count` | Populated by the managing repository |
| `usage_metrics.view_count` | Populated by the managing repository |
| `usage_metrics.citation_count` | Populated by the managing repository |
| `usage_metrics.last_accessed` | Populated by the managing repository |
| `distributions` | Distribution records populated at ingest |
| `data_services` | Data service endpoints populated at ingest |

---

## Appendix A: Common Mistakes

| Mistake | Correct approach |
|---|---|
| Setting `discoverability.datacard.sensitivity` to match `discoverability.sensitivity` by default | Set each independently based on what it describes — the data card document vs. the dataset. They will often differ. |
| Using `"No"` for `irb_approved` when the dataset has no human subjects | Use `"not_applicable"` — `"No"` implies an IRB review was needed but not obtained. |
| Leaving `restrictions`, `bias_risks`, or `safety_considerations` blank in the `ai_usage` block | Use `not_applicable` explicitly — blank fields may cause automated pipelines to reject or flag the data card. |
| Setting `doi` as `primary_id.type` before a DOI has been minted | Use `ark` or `local` until a DOI is assigned; retain the ARK in `additional_ids` after the DOI is minted for provenance continuity. |
| Leaving `provenance.was_generated_by` and `provenance.processing_steps` blank | Both are `[interoperability_required]` — fill them in for every dataset with `supports_interoperability = "Yes"`. Even a single sentence dramatically improves catalog value. |
| Writing "good" or "clean" for `data_quality.completeness` or `data_quality.known_issues` | Be specific — describe what is present, what is missing, why, and when. Vague quality statements reduce trust and reuse. |
| Not updating `datacard.change_log` when editing the data card | Add an entry every time the data card is updated; this is a `[discoverability_required]` field. Never delete or overwrite prior entries. |
| Setting `foreign_national_access_status` without checking `cui_limited_dissemination_controls` | If `discoverability.sensitivity.cui_limited_dissemination_controls` contains `NOFORN`, `REL TO`, or similar controls, `foreign_national_access_status` must be consistent with those controls. |
| Including the `_repository` block in a submitted data card | Remove it entirely before submission — it is populated by the system at ingest and must not be present in author-submitted data cards. |
| Mixing flat strings and structured entries in `data_structure.features` | Choose one form (flat list or structured form) and use it consistently throughout. |
| Using `true`/`false` or `1`/`0` for Yes/No fields | All Yes/No fields require quoted string values: `"Yes"` or `"No"`. See **Yes \| No Fields** in the Getting Started section. |
| Setting `export_control_basis` without consulting your export control office | If you are unsure of the correct basis, consult your institution's export control office before selecting a value other than `not_applicable`. |
| Omitting `succession_note` for project-bound contacts | If `contact.valid_until` is set, always provide a `succession_note` so users have a path to reach someone after the primary contact's end date. |

---

## Appendix B: Identifier Type Quick Reference

| Type | Format | When to use |
|---|---|---|
| `doi` | `10.XXXXX/XXXXXXX` | Published datasets with a registered DOI |
| `ark` | `ark:/NAAN/shoulder+name` | Pre-publication datasets at ARK-enabled institutions; retained after DOI is minted for provenance continuity |
| `handle` | `XXXXX/XXXXXXX` | Datasets in Handle-based repositories |
| `purl` | `https://purl.org/...` | Datasets with a PURL-based persistent identifier |
| `url` | `https://...` | When a stable URL is the best available identifier |
| `urn` | `urn:...` | Datasets with a URN-based persistent identifier |
| `uuid` | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` | Datasets with a UUID-based local identifier |
| `local` | Any internal ID | Pre-publication datasets with only an internal identifier (e.g., `genesis-ds-2024-0042`) |
| `other` | Any | Identifier systems not covered above |
| `unregistered` | — | Data card has not yet been registered; leave `value` blank |

ARK format: `ark:/NAAN/shoulder+assigned_name` — resolves via `https://n2t.net/ark:/NAAN/...`

---

## Appendix C: Sensitivity Quick Reference

Both `discoverability.datacard.sensitivity` and `discoverability.sensitivity` use the same `OverallSensitivityEnum`. Set each independently.

| Value | Meaning |
|---|---|
| `Public` | No sensitivity; publicly shareable |
| `Unclassified_Uncontrolled` | Unclassified and uncontrolled; may have minimal sensitivity; generally shareable with minimal controls |
| `CUI` | Controlled Unclassified Information; requires handling per CUI guidelines; access controls required |
| `UCNI` | Unclassified Controlled Nuclear Information; requires handling per UCNI guidelines; strict access controls required |
| `Classified` | Classified information; requires handling per classification level and guide; strict access controls required |
| `Legacy_Controlled` | Legacy controlled information; may have specific handling requirements based on legacy controls; access controls required |
| `Mixed` | Contains a combination of sensitive and non-sensitive information; handling requirements depend on specific content |
| `Other_Controlled` | Other controlled information with specific handling requirements |

---

## Appendix D: Capability Flag Field Requirements Summary

The table below shows which fields are required (`✅`), optional/if-applicable (`○`), or not applicable (`—`) for each capability flag. A field marked `✅` for a given capability must be populated when that capability flag is set to `"Yes"`.

| Field | Discoverability | Accessibility | Interoperability | Reusability | Governed Use | AI Usability |
|---|---|---|---|---|---|---|
| `supports_*` (all six flags) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `datacard.template_version` | ✅ | — | — | — | — | — |
| `datacard.datacard_version` | ✅ | — | — | — | — | — |
| `datacard.filename` | ✅ | — | — | — | — | — |
| `datacard.language` | ✅ | — | — | — | — | — |
| `datacard.id` | ○ | — | — | — | — | — |
| `datacard.sensitivity.*` | ✅/○ | — | — | — | — | — |
| `datacard.created_date` | ✅ | — | — | — | — | — |
| `datacard.updated_date` | ○ | — | — | — | — | — |
| `datacard.change_log` | ✅ | — | — | — | — | — |
| `datacard.creation_method` | ✅ | — | — | — | — | — |
| `datacard.created_by` | ✅ | — | — | — | — | — |
| `identification.name` | ✅ | — | — | — | — | — |
| `identification.project` | ✅ | — | — | — | — | — |
| `identification.version` | ✅ | — | — | — | — | — |
| `identification.primary_id` | ✅ | — | — | — | — | — |
| `identification.additional_ids` | ○ | — | — | — | — | — |
| `identification.supersedes` | ○ | — | — | — | — | — |
| `identification.superseded_by` | ○ | — | — | — | — | — |
| `identification.parent_collection` | ○ | — | — | — | — | — |
| `dataset_description.science_domain` | ○ | — | — | — | — | — |
| `dataset_description.dataset_summary` | ✅ | — | — | — | — | — |
| `dataset_description.purpose` | ○ | — | — | — | — | — |
| `dataset_description.collection_methodology` | ○ | — | — | — | — | — |
| `dataset_description.data_characteristics` | ○ | — | — | — | — | — |
| `dataset_description.limitations` | ○ | — | — | — | — | — |
| `dataset_description.tags` | ○ | — | — | — | — | — |
| `dataset_description.task_category` | ○ | — | — | — | — | — |
| `dataset_description.task_subcategory` | ○ | — | — | — | — | — |
| `dataset_description.keywords` | ✅ | — | — | — | — | — |
| `product_type` | ✅ | — | — | — | — | — |
| `dataset_type` | ○ | — | — | — | — | — |
| `release_status` | ✅ | — | — | — | — | — |
| `dataset_publisher` | ○ | — | — | — | — | — |
| `contact` | ✅ | — | — | — | — | — |
| `additional_contacts` | ○ | — | — | — | — | — |
| `authors` | ✅ | — | — | — | — | — |
| `contributors` | ○ | — | — | — | — | — |
| `sponsor_organizations` | ✅ | — | — | — | — | — |
| `sponsoring_doe_program_office` | ○ | — | — | — | — | — |
| `sponsoring_doe_subprogram` | ○ | — | — | — | — | — |
| `research_organizations` | ✅ | — | — | — | — | — |
| `facilities` | ○ | — | — | — | — | — |
| `discoverability.sensitivity.*` | ✅/○ | — | — | — | — | — |
| `workflow.state` | ✅ | — | — | — | — | — |
| `workflow.is_intermediate` | ○ | — | — | — | — | — |
| `workflow.pipeline_stage` | ○ | — | — | — | — | — |
| `workflow.embargo_until` | ○ | — | — | — | — | — |
| `access_policy.access_level` | — | ✅ | — | — | — | — |
| `access_policy.access_restrictions` | — | ○ | — | — | — | — |
| `access_policy.authorization_required` | — | ○ | — | — | — | — |
| `access_policy.intended_partner_classes` | — | ○ | — | — | — | — |
| `access_policy.approved_environments` | — | ○ | — | — | — | — |
| `access_policy.policy_url` | — | ○ | — | — | — | — |
| `access_policy.policy_text` | — | ○ | — | — | — | — |
| `access.current_location` | — | ✅ | — | — | — | — |
| `access.publicly_facing_landing_page_url` | — | ○ | — | — | — | — |
| `access.intended_repositories` | — | ○ | — | — | — | — |
| `dataset_scale` | — | ○ | — | — | — | — |
| `data_structure.formats` | — | — | ✅ | — | — | — |
| `data_structure.encoding` | — | — | ○ | — | — | — |
| `data_structure.schema_version` | — | — | ○ | — | — | — |
| `data_structure.modalities` | — | — | ✅ | — | — | — |
| `data_structure.features` | — | — | ✅ | — | — | — |
| `data_structure.splits` | — | — | ○ | — | — | — |
| `data_structure.language` | — | — | ○ | — | — | — |
| `data_structure.spatial_coverage` | — | — | ○ | — | — | — |
| `data_structure.temporal_coverage` | — | — | ○ | — | — | — |
| `provenance.was_generated_by` | — | — | ✅ | — | — | — |
| `provenance.source_data` | — | — | ○ | — | — | — |
| `provenance.processing_steps` | — | — | ✅ | — | — | — |
| `provenance.instrumentation` | — | — | ○ | — | — | — |
| `provenance.simulation_details` | — | — | ○ | — | — | — |
| `provenance.software_environment` | — | — | ○ | — | — | — |
| `dates` | — | — | ○ | — | — | — |
| `semantic_layer` | — | — | ○ | — | — | — |
| `related_resources` | — | — | ○ | — | — | — |
| `domain_metadata` | — | — | ○ | — | — | — |
| `license` | — | — | — | ○ | — | — |
| `additional_licenses` | — | — | — | ○ | — | — |
| `stewardship` | — | — | — | ○ | — | — |
| `data_quality.completeness` | — | — | — | ✅ | — | — |
| `data_quality.known_issues` | — | — | — | ✅ | — | — |
| `data_quality.validation_methods` | — | — | — | ✅ | — | — |
| `data_quality.noise_characteristics` | — | — | — | ○ | — | — |
| `data_quality.uncertainty_notes` | — | — | — | ○ | — | — |
| `data_quality.missing_data_codes` | — | — | — | ○ | — | — |
| `citation` | — | — | — | ○ | — | — |
| `integrity` | — | — | — | ○ | — | — |
| `use_governance.current_use` | — | — | — | — | ✅ | — |
| `use_governance.intended_use` | — | — | — | — | ○ | — |
| `use_governance.permitted_use` | — | — | — | — | ○ | — |
| `use_governance.out_of_scope_use` | — | — | — | — | ○ | — |
| `use_governance.prohibited_use` | — | — | — | — | ○ | — |
| `use_governance.need_to_know_basis` | — | — | — | — | ○ | — |
| `export_control.export_control_status` | — | — | — | — | ✅ | — |
| `export_control.export_control_basis` | — | — | — | — | ○ | — |
| `export_control.foreign_national_access_status` | — | — | — | — | ○ | — |
| `privacy.privacy_status` | — | — | — | — | ✅ | — |
| `privacy.pii_status` | — | — | — | — | ✅ | — |
| `privacy.phi_status` | — | — | — | — | ✅ | — |
| `privacy.privacy_control_basis` | — | — | — | — | ○ | — |
| `privacy.privacy_regime_notes` | — | — | — | — | ○ | — |
| `rights_release_records.ip_restriction_type` | — | — | — | — | ○ | — |
| `rights_release_records.agreement_required` | — | — | — | — | ✅ | — |
| `rights_release_records.agreement_type` | — | — | — | — | ○ | — |
| `rights_release_records.public_release_status` | — | — | — | — | ✅ | — |
| `rights_release_records.record_status` | — | — | — | — | ✅ | — |
| `compliance.doe_data_management_plan` | — | — | — | — | ✅ | — |
| `compliance.osti_elink2_metadata_compliant` | — | — | — | — | ✅ | — |
| `compliance.irb_approved` | — | — | — | — | ✅ | — |
| `review_provenance_companion` | — | — | — | — | ○ | — |
| `ai_usage.training_use_status` | — | — | — | — | — | ✅ |
| `ai_usage.training_use_conditions` | — | — | — | — | — | ○ |
| `ai_usage.inference_use_status` | — | — | — | — | — | ✅ |
| `ai_usage.inference_use_conditions` | — | — | — | — | — | ○ |
| `ai_usage.evaluation_use_status` | — | — | — | — | — | ✅ |
| `ai_usage.evaluation_use_conditions` | — | — | — | — | — | ○ |
| `ai_usage.restrictions` | — | — | — | — | — | ✅ |
| `ai_usage.bias_risks` | — | — | — | — | — | ✅ |
| `ai_usage.safety_considerations` | — | — | — | — | — | ✅ |
| `ai_usage.human_review_required` | — | — | — | — | — | ✅ |
| `_repository` (all sub-fields) | [reference_only_do_not_include] |||||| |

**Key:** ✅ Required when capability flag is `"Yes"` &nbsp;&nbsp; ○ Optional/if-applicable &nbsp;&nbsp; — Not governed by this capability &nbsp;&nbsp; ✅/○ Some sub-fields required, some optional (see field entry)

---

## Appendix E: Getting Help

| Resource | Location |
|---|---|
| Genesis data management team | TBD |
| Template and schema documentation | https://gitlab.com/amsc2/modcon/dbs/data-cards |
| LinkML schema validator | https://gitlab.com/amsc2/modcon/dbs/data-cards |
| ROR ID lookup | https://ror.org |
| ORCID registration | https://orcid.org |
| SPDX license list | https://spdx.org/licenses/ |
| CUI registry | https://www.archives.gov/cui |
| ARK identifier information | https://arks.org |
| OSTI E-Link 2 API documentation | https://www.osti.gov/elink |