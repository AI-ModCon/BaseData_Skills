# Genesis Mission Datacard v1.0
## Field Reference Guide

**Document version:** 1.0  
**Applies to template:** Genesis Mission Datacard v1.0  
**Last updated:** 2026-03-30  
**Maintained by:** Genesis Data Management Team  
**Companion schema:** TBD  
**Datacard changelog:** TBD

---

## How to Use This Guide

This guide is a companion to the Genesis Mission Datacard template (`genesis_datacard_v1.0.md`). It explains every field in the template: what it means, why it matters, how to fill it in correctly, and common mistakes to avoid.

**This guide is organized to mirror the template exactly.** If you are looking up a specific field, use the section headings below to navigate directly to it.

**If you are filling out a datacard for the first time**, read the [Getting Started](#getting-started) section first, then work through the template field by field using this guide as a reference.

---

## Getting Started

### What is a datacard?

A datacard is a structured metadata document that describes a dataset — what it is, where it came from, who created it, how it can be accessed, and how it can be used. Datacards serve both humans (who need to understand a dataset before using it) and machines (automated pipelines that ingest, catalog, and validate datasets).

In Genesis, every dataset — regardless of size, sensitivity, or publication state — should have a datacard. A datacard can be created at the same time as the dataset, or as early in the workflow as possible.

### Choose your profile first

Before filling anything out, decide which profile applies to your dataset. The profile determines which fields you are required to fill in.

| Profile | When to use | Time to complete |
|---|---|---|
| `core` | In-workflow, draft, or simple datasets not yet being shared | 10–15 minutes |
| `extended` | Datasets being shared with partners or submitted to OSTI, Zenodo, or similar | 30–45 minutes |
| `ai_ready` | Datasets intended for AI/ML training, inference, or evaluation | 45–60 minutes |
| `sensitive` | CUI, export-controlled, PII, or classified datasets | 45–60 minutes |

You can start with `core` and upgrade to a higher profile later as the dataset matures. The `change_log` field tracks these upgrades.

### Understanding field annotations

Every field in the template is annotated to tell you whether you need to fill it in:

| Annotation | Meaning |
|---|---|
| `[core]` | Required for all profiles — fill this in regardless |
| `[extended]` | Required for extended, ai_ready, and sensitive profiles |
| `[ai_ready]` | Required for the ai_ready profile only |
| `[sensitive]` | Required for the sensitive profile only |
| `[pub]` | Required when release_status = approved or published |
| `[if_applicable]` | Fill in if it applies to your dataset; skip if it does not |
| `[system]` | Do not fill in — the repository system populates this at ingest |

### Understanding placeholder conventions

| Placeholder | Meaning |
|---|---|
| `${VALUE}` | Required for your profile — you must replace this |
| `__VALUE__` | Optional or conditional — replace if applicable, leave blank or delete if not |
| `not_applicable` | Use this literal value when a field definitively does not apply to your dataset |

**Important distinction:** leaving a field blank means *the information is not yet known*. Writing `not_applicable` means *this field does not apply to this dataset*. Catalog tooling uses this distinction for completeness scoring — blank fields may trigger reminders, while `not_applicable` fields are treated as complete.

### Sensitivity tiers — a critical concept

The template has **two independent sensitivity tier fields** that are easy to confuse:

- **`datacard.sensitivity_tier`** — the sensitivity of *this document* (the datacard file itself)
- **`security.sensitivity_tier`** — the sensitivity of *the dataset* the datacard describes

These will often be different. A common and valid scenario: a researcher creates a publicly shareable datacard (`datacard.sensitivity_tier = tier0_open`) that describes a dataset containing PII (`security.sensitivity_tier = tier5_regulated_personal`). The open datacard allows people to discover that the dataset exists and understand its contents, while the underlying data remains protected.

**Never set these to match each other by default.** Set each one independently based on what it describes.

---

## Section 1: Datacard Metadata

*This section describes the datacard document itself — not the dataset.*

---

### `datacard.template_version`
**Annotation:** `[system]`  
Do not modify this field. It is set to `"1.0"` and used by parsers to apply the correct validation logic for this version of the template. Changing it will break automated processing.

---

### `datacard.datacard_version`
**Annotation:** `[core]`  
The version of *this specific datacard document*, not the dataset and not the template. Start at `"1.0"` when you first create the datacard. Increment using semantic versioning:
- Increment the **PATCH** (1.0 → 1.0.1) for minor corrections (typos, formatting)
- Increment the **MINOR** (1.0 → 1.1) for content additions or updates (new fields, updated descriptions)
- Increment the **MAJOR** (1.0 → 2.0) for structural changes (profile change, significant reorganization)

Every time you update `datacard_version`, add a corresponding entry to `change_log`.

---

### `datacard.profile`
**Annotation:** `[core]`  
Declares the completeness level you are committing to for this datacard. Valid values: `core | extended | ai_ready | sensitive`.

This field is read by catalog validation tooling to determine which fields are expected to be populated. Choosing a profile does not prevent you from filling in additional fields — it sets the *minimum* expectation.

**Common mistake:** Choosing `core` when the dataset is being submitted to OSTI or shared with a partner. Use `extended` or higher when the dataset is leaving your immediate team.

---

### `datacard.creation_method`
**Annotation:** `[core]`  
How this datacard was most recently created or updated. Valid values:
- `manual` — filled out entirely by hand by a human author
- `automated` — generated entirely by a pipeline, script, or AI model with no human review
- `hybrid` — initially generated automatically (e.g., by an LLM from dataset metadata), then reviewed and edited by a human

This field helps catalog administrators assess datacard quality and identify datacards that may need human review. An `automated` datacard that has never been reviewed by a human is treated differently from a `hybrid` one.

Update this field to reflect the creation method of the *most recent significant update*, not just the initial creation.

---

### `datacard.filename`
**Annotation:** `[core]`  
The filename of this datacard document, following the naming convention:
```
genesis_datacard_<snake_case_dataset_name>.md
```
The `<snake_case_dataset_name>` portion should match `identification.name` converted to snake_case (lowercase, underscores instead of spaces, no special characters).

**Example:** A dataset named "SNS Beam Position Monitor Data 2024" → `genesis_datacard_sns_beam_position_monitor_data_2024.md`

---

### `datacard.language`
**Annotation:** `[core]`  
The ISO 639-1 two-letter language code for the language this datacard is written in. Default is `en` (English). This describes the language of the *datacard document*, not the dataset content. See `dataset_info.language` for the dataset content language.

---

### `datacard.id`
**Annotation:** `[if_applicable]`  
A persistent identifier (PID) for the datacard document itself, if it has been registered separately from the dataset. Most datacards will not have this initially. Populate if the datacard is registered in a catalog or repository as an independent citable object.

**Sub-fields:**
- `type`: The identifier type — `doi | ark | handle | url | local | other`
- `value`: The identifier value

---

### `datacard.sensitivity_tier`
**Annotation:** `[core]`  
The sensitivity classification of *this datacard document* — not the dataset it describes. See [Sensitivity Tiers — a critical concept](#sensitivity-tiers--a-critical-concept) above.

Set this based solely on the sensitivity of the metadata contained in the datacard file. Ask yourself: *if someone reads only this document, what is the most sensitive information they would see?*

If the datacard contains internal paths, restricted contact information, classified system details, or PII (even incidentally), tier up accordingly.

Valid tiers:

| Tier | Name | Meaning |
|---|---|---|
| `tier0_open` | Open Science | No restrictions; publicly shareable |
| `tier1_controlled_research` | Controlled Research | Internal research use; limited sharing |
| `tier2_proprietary` | Proprietary | Proprietary; internal use only |
| `tier3_sensitive` | Sensitive | Sensitive; access controls required |
| `tier4_export_controlled` | Export Controlled | Subject to EAR or ITAR restrictions |
| `tier5_regulated_personal` | Regulated Personal | Contains PII or regulated personal data |
| `tier6_classified` | Classified | Formally classified; handle per classification guide |

**Note:** Genesis currently only accepts `open` datacards (`tier0_open`). Other tiers are reserved for future use but should still be set accurately.

---

### `datacard.access_level`
**Annotation:** `[core]`  
The access level for *this datacard document*. Valid values: `open | restricted | controlled`. Set independently of the dataset's access level.

**Note:** Genesis currently only accepts `open` datacards. Set to `open` unless instructed otherwise.

---

### `datacard.created_date`
**Annotation:** `[core]`  
The ISO 8601 date this datacard was first created. Format: `YYYY-MM-DD`. This date does not change once set — it records when the datacard was originally authored.

---

### `datacard.updated_date`
**Annotation:** `[core]`  
The ISO 8601 date this datacard was most recently updated. Update this field every time you make any change to the datacard, no matter how minor.

---

### `datacard.change_log`
**Annotation:** `[core]`  
A running chronological history of meaningful changes to this datacard. Add one entry each time you update the datacard. **Never delete or overwrite prior entries** — this is an append-only record.

The first entry is pre-filled with `"Initial creation"`. Update the `date` field and add subsequent entries as the datacard evolves.

**Sub-fields per entry:**
- `date`: ISO 8601 date of this change
- `datacard_version`: The datacard version *after* this change (should match `datacard.datacard_version`)
- `summary`: A brief plain-language description of what changed and why

**Example entries:**
```yaml
change_log:
  - date: "2024-03-15"
    datacard_version: "1.0"
    summary: "Initial creation"
  - date: "2024-06-01"
    datacard_version: "1.1"
    summary: "Updated license from CC-BY-3.0 to CC-BY-4.0 following project guidance"
  - date: "2024-09-20"
    datacard_version: "1.2"
    summary: "Added checksum after dataset transfer to OSTI; corrected collection end date"
```

---

### `datacard.created_by`
**Annotation:** `[core]`  
A list of all contributors who created or updated this datacard. List in chronological order — the first entry should be whoever created the initial draft. If an AI model generated the initial draft and a human then edited it, the AI model entry comes first.

Each entry has a `role`, `date`, optional `description`, and a `creator` block. The `creator` block has a `type` field — choose one of `person | organization | ai_model | software` and delete the blocks that do not apply.

**Creator types:**

**`person`** — Use for any individual human contributor.
```yaml
- role: editor
  date: "2024-03-15"
  description: "Reviewed and corrected AI-generated content for accuracy"
  creator:
    type: person
    person:
      given_name: Jane
      family_name: Smith
      orcid: 0000-0002-1234-5678
      email: jsmith@ornl.gov
      affiliation:
        name: Oak Ridge National Laboratory
        ror_id: https://ror.org/01qz5mb56
```

**`organization`** — Use when a team or office created the datacard without a single named individual.
```yaml
- role: initial_creation
  date: "2024-03-15"
  creator:
    type: organization
    organization:
      name: ORNL Data Management Office
      ror_id: https://ror.org/01qz5mb56
```

**`ai_model`** — Use when an AI model generated or substantially contributed to the datacard content. Always pair with a subsequent `person` or `organization` entry showing human review.
```yaml
- role: initial_creation
  date: "2024-03-15"
  description: "Automated generation of datacard content from dataset metadata and journal articles"
  creator:
    type: ai_model
    ai_model:
      name: Claude Sonnet 4.6
      version: claude-sonnet-4-6
      date_accessed: "2024-03-15"
      identifier:
        type: url
        value: https://anthropic.com/claude
```

**`software`** — Use when an automated pipeline or script (not an LLM) generated the datacard.
```yaml
- role: initial_creation
  date: "2024-03-15"
  description: "Automated generation via genesis-datacard-generator pipeline"
  creator:
    type: software
    software:
      name: genesis-datacard-generator
      version: 2.1.0
      identifier:
        type: url
        value: https://github.com/genesis/datacard-generator
```

---

## Section 2: Level 1 — Basic & Discoverable

*Required for all datasets regardless of profile or publication state.*

---

### `identification.name`
**Annotation:** `[core]`  
A single human-readable name for this dataset. This is the primary label by which the dataset will be known in the Genesis catalog.

**Guidelines:**
- Be specific enough to distinguish this dataset from similar ones
- Avoid acronyms without expansion in the name itself
- If this datacard describes a collection of related datasets, name the collection
- The name should match the snake_case portion of the datacard filename

**Good examples:**
- `SNS Beam Position Monitor Calibration Data 2023–2024`
- `Fusion Plasma Spectroscopy Measurements — DIII-D Campaign 42`
- `MNIST-Style Handwritten Digit Dataset for Materials Classification`

**Poor examples:**
- `Dataset 1` (not descriptive)
- `BPM_data` (acronym without expansion, too terse)

---

### `identification.project`
**Annotation:** `[core]`  
The Genesis project or sub-project this dataset belongs to. Used for catalog filtering and project-level reporting.

**Examples:** `genesis | genesis-fusion | genesis-lightsource | genesis-materials`

If you are unsure which project tag to use, contact your data manager.

---

### `identification.version`
**Annotation:** `[core]`  
The version of the *dataset*, using semantic versioning (`MAJOR.MINOR.PATCH`). Start at `1.0` for the first release.

- **MAJOR**: Breaking changes — the schema changed, files were reorganized, or the dataset is fundamentally different
- **MINOR**: Additions — new files, new variables, extended time range
- **PATCH**: Corrections — bug fixes, typo corrections, minor metadata updates

This is distinct from `datacard.datacard_version`, which tracks the version of this document. See also `stewardship.versioning_strategy` for how versions are managed, and `identification.supersedes`/`superseded_by` for linking versions together.

---

### `identification.primary_id`
**Annotation:** `[core]`  
The primary persistent identifier for this dataset. Every dataset must have at least one identifier. If a formal PID has not yet been assigned, use a `local` identifier (an internal system ID or path) as a placeholder.

**Identifier types:**

| Type | When to use | Format example |
|---|---|---|
| `doi` | Published datasets with a registered DOI | `10.25982/12345.6789` |
| `ark` | Pre-publication datasets at institutions using ARK | `ark:/12345/b2345679k` |
| `handle` | Datasets in Handle-based repositories | `11573/12345` |
| `url` | When a stable landing page URL is the best available identifier | `https://data.ornl.gov/dataset/12345` |
| `osti` | Datasets registered in OSTI | `1234567` |
| `local` | Pre-publication datasets with only an internal identifier | `genesis-ds-2024-0042` |
| `other` | Any other identifier system | describe in comments |

**ARK format:** `ark:/NAAN/shoulder+assigned_name`  
ARKs are well-suited for pre-publication datasets. When a dataset is published and a DOI is minted, retain the ARK in `additional_ids` for provenance continuity — the ARK remains a valid resolver even after publication.

---

### `identification.additional_ids`
**Annotation:** `[if_applicable]`  
Additional identifiers beyond the primary ID. Use for lab report numbers, accession numbers, prior identifiers, or any other relevant ID systems.

**Examples:**
```yaml
additional_ids:
  - type: sand
    value: SAND2024-12345
  - type: ark
    value: ark:/12345/b2345679k   # retained after DOI was minted
  - type: osti
    value: 1987654
```

---

### `identification.supersedes`
**Annotation:** `[if_applicable]`  
If this dataset is a new version that replaces a prior version, put the prior version's identifier here. This creates a machine-readable link between versions that catalog systems can traverse.

**Example:**
```yaml
supersedes:
  type: doi
  value: 10.25982/12345.6789   # this is version 1.0; current dataset is version 2.0
```

---

### `identification.superseded_by`
**Annotation:** `[if_applicable]`  
If this dataset has been replaced by a newer version, put the newer version's identifier here. Populate this field when you set `release_status = deprecated`. This ensures users who find an older version are directed to the current one.

---

### `identification.parent_collection`
**Annotation:** `[if_applicable]`  
If this dataset is one of many in a larger organized collection or experimental campaign, identify the parent collection here. This supports top-down navigation in the catalog — users browsing a collection can find all its constituent datasets.

**Example:**
```yaml
parent_collection:
  name: SNS Instrument Calibration Campaign 2023
  identifier:
    type: local
    value: genesis-collection-2023-sns-cal
```

---

### `description.summary`
**Annotation:** `[core]`  
The most important descriptive field in the entire datacard. Write 1–3 sentences that clearly explain what this dataset is, in plain language accessible to a broad scientific audience who may not be familiar with your specific project.

**Ask yourself:** If a colleague outside your group found this dataset in the catalog, would this summary tell them whether it is relevant to their work?

**Good example:**
> This dataset contains time-series beam position monitor (BPM) readings from the Spallation Neutron Source (SNS) at ORNL, collected during accelerator commissioning runs in Q3 2023. Data includes horizontal and vertical beam positions at 120 monitor locations sampled at 1 MHz, with associated timestamps and beam current measurements. Intended for accelerator physics analysis and ML-based anomaly detection model development.

**Poor example:**
> BPM data from SNS 2023.

---

### `description.purpose`
**Annotation:** `[if_applicable]`  
Why was this dataset created? What scientific or operational question does it address? What gap does it fill?

This is different from `intended_use`, which describes how the dataset should be used. `purpose` explains the motivation for creating it in the first place.

---

### `description.collection_methodology`
**Annotation:** `[if_applicable]`  
How was the data acquired? Choose the best-fit description and expand as needed:
- `experimental sensors` — physical measurements from instruments
- `computational simulation` — outputs from a simulation code
- `human annotation` — labels or annotations applied by people
- `derived from prior datasets` — processed or transformed from existing data

---

### `description.data_characteristics`
**Annotation:** `[if_applicable]`  
Key structural and content characteristics of the dataset that help users assess its suitability. Include things like scale (how many records), dimensionality, temporal range, spatial resolution, or other notable properties.

---

### `description.intended_use`
**Annotation:** `[if_applicable]`  
What tasks or workflows is this dataset designed to support? Be specific — this helps catalog tools surface the dataset for relevant use cases.

**Examples:** `accelerator physics analysis | ML anomaly detection training | benchmarking beam diagnostic algorithms`

---

### `description.current_use`
**Annotation:** `[if_applicable]`  
For in-workflow datasets: what is this dataset actively being used for *right now*? This is distinct from `intended_use` (eventual purpose) and helps collaborators understand the dataset's active role.

---

### `description.out_of_scope_use`
**Annotation:** `[if_applicable]`  
Explicitly describe uses this dataset should NOT be applied to. This is particularly important for AI/ML datasets where misapplication is a real risk.

**Examples:**
- `Not suitable for real-time accelerator control — data latency precludes safety-critical use`
- `Not for clinical decision-making — data was collected under non-clinical conditions`

---

### `description.limitations`
**Annotation:** `[if_applicable]`  
Known limitations, gaps, biases, or caveats that users should be aware of before using this dataset. Be candid — undisclosed limitations that surface later damage trust in both the dataset and the catalog.

---

### `description.keywords`
**Annotation:** `[core]`  
A list of keywords that describe this dataset and help users find it through catalog search. Include a mix of:
- Domain terms (e.g., `neutron scattering`, `plasma physics`)
- Method terms (e.g., `Monte Carlo simulation`, `machine learning`)
- Instrument or facility terms (e.g., `Spallation Neutron Source`, `DIII-D`)
- Relevant ontology terms if known (e.g., `ENVO:00002006`)

---

### `object_type`
**Annotation:** `[core]`  
The primary type of digital object described by this datacard.

| Value | Use when |
|---|---|
| `dataset` | The primary object is a collection of data files |
| `model` | The primary object is a trained ML or computational model |
| `software` | The primary object is a software tool or script |
| `ai_agent` | The primary object is an AI agent or workflow |
| `eval` | The primary object is an evaluation benchmark or test suite |
| `framework` | The primary object is a reusable computational framework |
| `other` | None of the above |

---

### `dataset_type`
**Annotation:** `[core]`  
The OSTI DOE Data Explorer type code. Select the single best-fit code for this dataset. Used for OSTI submission and catalog classification.

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

If in doubt between `ND` and `SM`, use `ND` if the data is primarily numeric and `SM` if it genuinely combines distinct data types (e.g., images + tabular measurements + text annotations).

---

### `release_status`
**Annotation:** `[core]`  
The current publication and governance state of this dataset. See also `workflow.state` — these two fields describe complementary aspects of the dataset's lifecycle and should be kept logically consistent.

| Value | Meaning |
|---|---|
| `draft` | Work in progress; not ready for sharing outside the immediate team |
| `under_review` | Submitted for formal review (security, export control, IRB, etc.) |
| `approved` | Review complete; cleared for release |
| `published` | Publicly released and accessible |
| `deprecated` | Superseded or retired; no longer recommended for use |

**Common alignment with `workflow.state`:**

| `workflow.state` | Expected `release_status` |
|---|---|
| `raw`, `processing`, `qa`, `analysis` | `draft` |
| `review` | `under_review` |
| `embargo`, `published` | `approved` or `published` |
| `archived` | `deprecated` or `published` |

---

### `workflow.state`
**Annotation:** `[core]`  
The current technical and processing lifecycle position of the data itself. This is distinct from `release_status`, which describes the publication and governance state. Both fields are needed because a dataset can be technically complete (`published` or `archived`) while still under governance review (`under_review`).

| Value | Meaning |
|---|---|
| `raw` | Data as collected; no processing applied |
| `processing` | Actively being cleaned, transformed, or reduced |
| `qa` | Undergoing quality assurance or validation |
| `analysis` | In active scientific analysis |
| `review` | Under formal review (security, export control, IRB, etc.) |
| `embargo` | Complete but intentionally withheld from release until `embargo_until` date |
| `published` | Publicly released |
| `archived` | Preserved and no longer actively maintained |

---

### `workflow.is_intermediate`
**Annotation:** `[if_applicable]`  
Set to `true` if this dataset is an intermediate product in a processing pipeline — it is not a final deliverable but a step toward one. Set to `false` if this is a final or publication-intended product.

**Example:** Raw detector output before calibration is intermediate. Calibrated, analysis-ready data is final.

---

### `workflow.pipeline_stage`
**Annotation:** `[if_applicable]`  
A freetext description of where this dataset sits in a specific processing pipeline. Useful for multi-stage workflows where `workflow.state` alone is not granular enough.

**Examples:**
- `"post-detector, pre-reconstruction"`
- `"raw telemetry, pre-calibration"`
- `"processed but not yet quality-reviewed"`

---

### `workflow.embargo_until`
**Annotation:** `[if_applicable]`  
Required if `workflow.state = embargo`. The ISO 8601 date after which release is permitted. Catalog tooling uses this date to automatically trigger release workflows.

---

### `dataset_readiness`
**Annotation:** `[if_applicable]`  
An assessment of the dataset's usability and interoperability level against the Genesis Dataset Readiness Model. **Readiness describes usability, not scientific quality or value.**

| Level | Name | Meaning |
|---|---|---|
| `1` | Discoverable | Sufficient metadata to find and identify the dataset in the catalog |
| `2` | Interoperable & Reusable | Accessible, governed, licensed, and documented for reuse |
| `3` | AI-Ready & Trustworthy | Semantically clear, provenance-aware, integrity-supported, suitable for AI/ML workflows |

A dataset with significant scientific value can be at Level 1 readiness — readiness reflects documentation completeness, not scientific merit.

**Sub-fields:**
- `level`: The assessed readiness level (1, 2, or 3)
- `evaluated_against`: The name and version of the readiness model used (e.g., `"Genesis Dataset Readiness Model v1.0"`)
- `evaluated_at`: ISO 8601 date of evaluation
- `evaluated_by`: The person or organization that performed the evaluation
- `confidence`: The evaluator's confidence in the assessment (`high | medium | low`)

---

## Section 3: Level 2 — Interoperable & Reusable

*Required for extended, ai_ready, and sensitive profiles; and for any dataset being shared outside the immediate team.*

---

### `security.classification`
**Annotation:** `[core]`  
The formal security classification of *the dataset*. This is a required field for all profiles because every dataset has a classification, even if it is simply Unclassified (`U`).

| Value | Meaning |
|---|---|
| `U` | Unclassified — no classification markings |
| `CUI` | Controlled Unclassified Information — see `security.cui_marking` |
| `C` | Confidential |
| `S` | Secret |
| `TS` | Top Secret |

If you are unsure of the correct classification, consult your institution's information security office before proceeding.

---

### `security.sensitivity_tier`
**Annotation:** `[core]`  
The sensitivity classification of *the dataset* — not this datacard. See [Sensitivity Tiers — a critical concept](#sensitivity-tiers--a-critical-concept) at the top of this guide. Set independently of `datacard.sensitivity_tier`.

Use the same tier definitions as `datacard.sensitivity_tier` (see that section above), but applied to the underlying data rather than the document.

---

### `security.sensitivity_level`
**Annotation:** `[if_applicable]`  
A simple human-readable label for quick catalog filtering. Use alongside `sensitivity_tier` — this does not replace it.

Valid values: `public | internal | confidential | restricted`

---

### `security.cui_marking`
**Annotation:** `[required if classification=CUI]`  
The specific CUI marking if the dataset is Controlled Unclassified Information. Consult the CUI registry at https://www.archives.gov/cui for the full list.

**Common markings:**
- `CUI` — basic CUI with no specific category
- `CUI//SP-PRVCY` — Privacy (PII)
- `CUI//SP-PROPIN` — Proprietary Business Information
- `CUI//SP-EXPT` — Export Controlled

---

### `security.distribution_statement`
**Annotation:** `[extended]`  
The distribution limitation statement for the dataset. Required for extended and higher profiles.

**Common statements:**
- `"Distribution A - Approved for public release; distribution is unlimited."`
- `"Distribution B - Distribution authorized to U.S. Government agencies only"`
- `"Distribution C - Distribution authorized to U.S. Government agencies and their contractors"`
- `"Distribution D - Distribution authorized to DoD and DoD contractors only"`

If unsure, check with your institution's classification or export control office.

---

### `security.handling_instructions`
**Annotation:** `[if_applicable]`  
Special handling requirements beyond what the distribution statement covers.

**Examples:**
- `"No foreign dissemination"`
- `"Export-controlled handling required — see EAR Part 734"`
- `"Protect as business sensitive"`

---

### `security.export_control`
**Annotation:** `[core]`  
The export control jurisdiction applicable to this dataset. Required for all profiles.

| Value | Meaning |
|---|---|
| `none` | Not subject to export control restrictions |
| `EAR` | Subject to Export Administration Regulations |
| `ITAR` | Subject to International Traffic in Arms Regulations |

If you are unsure, consult your institution's export control office before selecting a value other than `none`.

---

### `security.export_control_id`
**Annotation:** `[required if export_control != none]`  
The specific export control classification number if `export_control` is `EAR` or `ITAR`.

**Examples:**
- `EAR99` — subject to EAR but no specific ECCN
- `ECCN 3E001` — specific Export Control Classification Number
- `USML Category XV` — US Munitions List category

---

### `security.data_rights`
**Annotation:** `[if_applicable]`  
A legal statement about who holds rights to the dataset, separate from the license. This is particularly important for DOE/NNSA-funded datasets where government rights statements are required.

**Examples:**
- `"Government has unlimited rights"`
- `"Contractor retains rights with government license"`
- `"Government purpose rights — limited release"`

---

### `security.last_reviewed_date`
**Annotation:** `[if_applicable]`  
The date security markings were last reviewed and confirmed to be current. Update this field whenever the security markings are revalidated. For long-lived datasets, security markings should be reviewed periodically — this field documents that review cadence.

---

### `security.pii`
**Annotation:** `[sensitive]`  
Complete this block if `security.sensitivity_tier = tier5_regulated_personal`. This block captures the PII handling posture of the dataset.

**Sub-fields:**

- **`present`** (`true | false`): Whether PII is present in the dataset.

- **`types`**: A list of PII types present. Valid values:
  `names | email_addresses | phone_numbers | location_data | biometric_data | financial_data | health_data | other`

- **`deidentification_applied`** (`true | false`): Whether a deidentification or anonymization method has been applied to remove or obfuscate PII.

- **`deidentification_method`**: Required if `deidentification_applied = true`. Describe the method used.
  **Examples:**
  - `"k-anonymity (k=5) — direct identifiers removed, quasi-identifiers generalized"`
  - `"Differential privacy with ε=1.0 applied to numeric fields"`
  - `"Direct identifier removal per HIPAA Safe Harbor method"`

- **`deidentification_reviewed`** (`true | false`): Whether the deidentification method was formally reviewed for adequacy.

---

### `security.classification_reason`
**Annotation:** `[required if classification != U]`  
A brief explanation of why this dataset carries a classification other than Unclassified.

**Example:** `"Contains export-controlled simulation parameters for nuclear criticality calculations"`

---

### `security.declassification`
**Annotation:** `[required if classification != U]`  
Declassification review information for classified datasets.

- `review_date`: The scheduled date for declassification review in ISO 8601 format
- `authority`: The authority under which declassification will be reviewed

---

### `access_policy`
The `access_policy` block describes who can access *the dataset* and under what conditions. Note that `access_policy.sensitivity_tier` refers to the dataset's sensitivity — it will typically match `security.sensitivity_tier` since both describe the same subject (the dataset). Both are independent of `datacard.sensitivity_tier`.

### `access_policy.sensitivity_tier`
**Annotation:** `[core]`  
The sensitivity tier of the dataset for access control purposes. Typically carries the same value as `security.sensitivity_tier`. Both fields describe the dataset's sensitivity — they are reproduced separately because some access control systems evaluate the `access_policy` block independently of the `security` block.

---

### `access_policy.access_level`
**Annotation:** `[core]`  
The access level required to obtain this dataset. Valid values: `open | restricted | controlled`.

| Value | Meaning |
|---|---|
| `open` | Freely accessible without any authorization |
| `restricted` | Accessible with some form of authorization (account, agreement, etc.) |
| `controlled` | Access requires formal approval, review, or clearance |

---

### `access_policy.authorization_required`
**Annotation:** `[core]`  
The specific type of authorization required to access this dataset.

| Value | Meaning |
|---|---|
| `none` | No authorization required — freely accessible |
| `account` | A registered account in the repository system |
| `user_agreement` | Acceptance of a user agreement or terms of service |
| `data_use_agreement` | A formal signed Data Use Agreement (DUA) |
| `sponsor_approval` | Approval from the dataset sponsor or PI |
| `export_control_review` | A completed export control review |
| `irb_approval` | Institutional Review Board approval |
| `other` | Describe in `access_restrictions` |

---

### `license`
**Annotation:** `[pub]`  
Required when `release_status = approved | published`. Describes the license under which the dataset is made available.

**Sub-fields:**

- **`spdx_id`**: The standardized SPDX license identifier. Find the full list at https://spdx.org/licenses/
  Common choices for scientific datasets:
  - `CC-BY-4.0` — Creative Commons Attribution 4.0 (most common for open science)
  - `CC0-1.0` — Public domain dedication (no restrictions)
  - `Apache-2.0` — Common for software and code
  - `MIT` — Common for software
  Use `"other"` if your license is not in the SPDX registry. Use `"pending"` if not yet assigned.

- **`name`**: Required if `spdx_id = other`. The human-readable name of the license.

- **`url`**: URL to the full license text. Use `"LICENSE.md"` if the license file is in the same repository as the dataset.

---

### `contact`
**Annotation:** `[core]`  
The primary point of contact for questions about this dataset. Required for all profiles — **every dataset must have a reachable contact person or organization.** This is the person users will reach out to if they have questions, encounter problems, or want to collaborate.

Choose a contact who will be reachable for the foreseeable future. For datasets with long retention periods, consider whether the named contact will still be associated with the project in 5–10 years.

**Sub-fields:**
- `type`: `person | organization` — use `organization` (e.g., a data management office) if no single named individual is appropriate
- `valid_until`: If the contact is project-bound (a postdoc, student, or term employee), set this to their expected end date so the catalog knows to flag expiring contacts
- `succession_note`: Who to contact if this contact is no longer reachable — e.g., a permanent team email or data management office

---

### `authors`
**Annotation:** `[pub]`  
At least one author is required when `release_status = approved | published`. For draft or in-workflow datasets, populate with known contributors as early as possible.

Authors are individuals or organizations with primary intellectual responsibility for the dataset — typically the PI, lead scientist, or data creator. For supporting roles (technicians, annotators, submitters), use `contributors` instead.

**`role` values:**
- `creator` — primary intellectual responsibility
- `contributor` — supporting role
- `data_collector` — responsible for data collection/acquisition
- `curator` — responsible for data organization and maintenance
- `publisher` — responsible for submitting to a repository
- `sponsor` — funded the creation
- `other`

**ORCID strongly recommended** for all person entries — ORCIDs are persistent identifiers that survive name changes, institutional moves, and common name disambiguation issues.

---

### `sponsor_organizations`
**Annotation:** `[core]`  
Organizations that funded or sponsored this dataset. Required for all profiles. For DOE-funded projects, this is the DOE program office or agency. Include award numbers and program names to support compliance reporting and grant tracking.

---

### `research_organizations`
**Annotation:** `[core]`  
Organizations that created, collected, or produced the data. Required for all profiles. For national lab datasets, this is typically the lab itself.

---

### `facilities`
**Annotation:** `[if_applicable]`  
User facilities, HPC centers, or research infrastructure used to collect, process, or store the dataset. Include ROR IDs where available for unambiguous identification. The `role` field clarifies how the facility was used:
- `collection` — data was collected here (e.g., an instrument beamline)
- `processing` — data was processed here (e.g., an HPC cluster)
- `storage` — data is stored here (e.g., a data center)
- `access` — data is accessed through here (e.g., a data portal)

The `location` sub-field is for point-location experimental data — use it to name the specific beamline, instrument station, or laboratory room where data was collected.

---

### `categorization.science_domain`
**Annotation:** `[core]`  
The high-level scientific domain or discipline associated with this dataset. Used for catalog browsing and filtering.

**Examples:** `materials_science | biology | physics | chemistry | climate | fusion | lightsource | computer_science | other`

---

### `categorization.tags`
**Annotation:** `[if_applicable]`  
Structured tags for catalog filtering. Use consistent controlled values within your project.

- `project`: The Genesis project tag (e.g., `genesis`)
- `science`: Science area (e.g., `lightsource | fusion | materials | biology`)
- `type`: Object type (e.g., `dataset | model | agent | eval`)
- `risk`: Risk review level (e.g., `general | reviewed | restricted`)

---

### `categorization.task_category`
**Annotation:** `[ai_ready]`  
Required for the `ai_ready` profile. The primary ML task category or categories this dataset supports. Use this to help ML practitioners find datasets for their specific workflows.

**Valid values:**
`classification | regression | segmentation | detection | generation | translation | summarization | ranking | anomaly_detection | clustering | reinforcement_learning | other`

---

### `categorization.task_subcategory`
**Annotation:** `[ai_ready]`  
More specific ML task subcategory. Use alongside `task_category` for precise catalog filtering.

**Examples:**
`binary_classification | multi_class_classification | multi_label_classification | image_segmentation | object_detection | time_series_forecasting | named_entity_recognition | question_answering | other`

---

### `dataset_info.formats`
**Annotation:** `[core]`  
A list of file formats present in the dataset. Be specific — include the version where relevant.

**Examples:** `["CSV", "HDF5", "NetCDF4", "Parquet", "TIFF", "JSON", "ROOT", "HDDM"]`

---

### `dataset_info.encoding`
**Annotation:** `[if_applicable]`  
The character encoding for text-based formats. Use `not_applicable` for binary formats (HDF5, NetCDF, TIFF, etc.).

**UTF-8 is strongly recommended** for all new text-based datasets. Non-UTF-8 encodings (Latin-1, ASCII, Windows-1252) should be explicitly documented as they can cause data corruption in downstream pipelines that assume UTF-8.

---

### `dataset_info.schema_version`
**Annotation:** `[if_applicable]`  
The version of the *data schema* used in this dataset. This is distinct from `datacard_version` (which tracks this document) and `identification.version` (which tracks the dataset version). Increment `schema_version` when the structure of the data changes — field names, data types, file organization — in a way that would break existing parsers.

---

### `dataset_info.modalities`
**Annotation:** `[if_applicable]`  
The data modalities present in the dataset.

**Examples:** `["tabular", "image", "time-series", "text", "graph", "point-cloud", "audio", "video"]`

---

### `dataset_info.features`
**Annotation:** `[if_applicable]`  
The primary variables, fields, or features in the dataset. **Use one form consistently — do not mix flat strings and structured entries.**

**For `core` and `extended` profiles — flat string list:**
```yaml
features: ["temperature", "pressure", "timestamp", "beam_current"]
```

**For `ai_ready` profile — structured form:**
```yaml
features:
  - name: temperature
    type: float
    unit: Kelvin
    description: Sample temperature at time of measurement
    range: "273.15 - 373.15"
  - name: beam_current
    type: float
    unit: mA
    description: Instantaneous beam current
    range: "0 - 120"
```

---

### `dataset_info.spatial_coverage`
**Annotation:** `[if_applicable]`  
Geographic coverage for geospatial or facility-based datasets. The `description` field is sufficient for most facility-based experimental data (e.g., `"SNS Beamline 1B, ORNL"`). Use the `bounding_box` sub-field for datasets with genuine geographic area coverage.

---

### `dataset_info.temporal_coverage`
**Annotation:** `[if_applicable]`  
The time period the dataset *represents* — distinct from `dates.data_collection_start/end`, which describes when collection occurred.

**When these differ:** A dataset of historical climate reanalysis data collected in 2024 but representing the period 1950–2020 would have:
- `temporal_coverage.start = 1950-01-01`
- `temporal_coverage.end = 2020-12-31`
- `dates.data_collection_start = 2024-01-01`

---

### `dataset_scale`
**Annotation:** `[if_applicable]`  
Physical size and record counts for the dataset. Fill in what you know — even approximate values help catalog users assess whether a dataset is practical to download and use.

- `record_count`: Number of primary records, samples, or files
- `record_unit`: The unit for `record_count` — `samples | files | records | timesteps | images | tokens | other`
- `compressed_bytes`: Total dataset size when compressed, in bytes
- `uncompressed_bytes`: Total dataset size when uncompressed, in bytes

---

### `dates`
**Annotation:** varies by sub-field  

- **`data_collection_start`** `[extended]`: When data collection or generation began
- **`data_collection_end`** `[extended]`: When data collection or generation ended
- **`issued`** `[pub]`: When the dataset was first publicly released
- **`modified`** `[if_applicable]`: When the dataset was most recently significantly modified

All dates in ISO 8601 format: `YYYY-MM-DD`

---

### `access.current_location`
**Annotation:** `[if_applicable]`  
Where the data physically resides right now. This is the primary access field for pre-publication and in-workflow datasets. Update it as the dataset moves through the workflow.

**Examples:**
- `/mnt/ecs/scientific-data/project/dataset/` — internal NFS path
- `/lustre/orion/proj-shared/dataset/` — HPC scratch or project storage
- `s3://genesis-bucket/dataset/` — cloud object storage

---

### `access.intended_repositories`
**Annotation:** `[if_applicable]`  
Repositories where you intend to deposit or have deposited this dataset. Repository-assigned fields (landing pages, accession numbers, access protocols) will be populated by the managing system at ingest — you only need to fill in what you know.

**Sub-fields per entry:**
- `name`: Human-readable repository name (e.g., `"OSTI Data Explorer"`, `"Zenodo"`, `"Globus"`, `"internal"`)
- `access_level`: Intended access level for this dataset in this repository (`open | restricted | controlled`). The same dataset may have different access levels in different repositories.
- `is_primary`: Set `true` for the canonical/primary repository. Only one entry should be marked `true`.
- `date_deposited`: ISO 8601 date of submission to this repository
- `api`: Populate only if an API endpoint for this dataset exists

---

### `provenance`

Provenance describes how this dataset was created, what it was derived from, and what processing was applied. Good provenance is critical for reproducibility and for establishing trust in derived analyses and models.

### `provenance.was_generated_by`
**Annotation:** `[core]`  
A high-level description of the process that generated this dataset. Even a single sentence dramatically improves catalog value. This is a required core field — fill it in for every dataset regardless of profile.

**Examples:**
- `"Neutron scattering experiment at SNS Beamline 1B, Spallation Neutron Source, ORNL"`
- `"Monte Carlo simulation using MCNP 6.2 with ENDF/B-VIII.0 nuclear data library"`
- `"Derived from raw SNS telemetry using calibration pipeline v2.1 (see related_resources.software)"`
- `"Human annotation of optical microscopy images by three domain expert annotators"`

---

### `provenance.source_data`
**Annotation:** `[if_applicable]`  
Source datasets this dataset was derived from. List all direct sources. The `relationship` field describes how this dataset relates to the source:

| Value | Meaning |
|---|---|
| `is_derived_from` | This dataset was produced by processing or transforming the source |
| `is_based_on` | This dataset uses the source as a reference or starting point |
| `is_part_of` | This dataset is a subset of the source |
| `has_part` | This dataset contains the source as a component |
| `references` | This dataset references but is not derived from the source |
| `other` | Describe the relationship in comments |

---

### `provenance.processing_steps`
**Annotation:** `[if_applicable]`  
A description of key processing, cleaning, calibration, or transformation steps applied to produce this dataset from raw or source data. Include enough detail that a knowledgeable person in your domain could understand what was done.

---

### `provenance.instrumentation`
**Annotation:** `[if_applicable]`  
Instruments, sensors, detectors, or equipment used for data collection. Include make, model, and version where relevant. For computational datasets, this may describe the compute hardware used.

---

### `provenance.simulation_details`
**Annotation:** `[if_applicable]`  
For simulation-derived data: the simulation code, version, key parameters, and configuration. Include enough detail to support reproducibility.

**Example:** `"LAMMPS 23Jun2022, NVT ensemble, 300K, 10ns run, CHARMM36 force field, 5000 atoms, periodic boundary conditions"`

---

### `provenance.software_environment`
**Annotation:** `[if_applicable]`  
The software environment used to generate or process this dataset. Capturing this information is critical for computational reproducibility — without it, recreating the dataset's processing steps may be impossible years later.

**Sub-fields:**
- `os`: Operating system and version (e.g., `"RHEL 8.6"`, `"Ubuntu 22.04"`)
- `compiler`: Compiler and version if applicable (e.g., `"GCC 11.3"`, `"Intel oneAPI 2023.1"`)
- `container`: Container image if applicable (e.g., `"docker://registry/image:tag"`)
- `hpc_environment`: HPC module environment (e.g., `"module load python/3.10 cuda/11.8 openmpi/4.1"`)
- `notes`: Freetext for key library versions, dependencies, or a reference to a full environment manifest (e.g., `requirements.txt`, `environment.yml`)

---

### `stewardship`
**Annotation:** `[if_applicable]`  
Describes ongoing maintenance responsibilities and versioning approach.

- **`level`**: Who is responsible for ongoing maintenance:
  - `project_managed` — the originating project team
  - `repository_managed` — a repository or data center
  - `externally_managed` — a third party

- **`maintainer`**: The specific person or organization responsible. May differ from the dataset contact or authors.

- **`update_frequency`**: `none | ad_hoc | monthly | quarterly | annually | other`

- **`retention_policy`**: How long the dataset will be retained and where. For DOE datasets, reference the applicable data management policy.

- **`versioning_strategy`**: How versions are tracked, archived, and retired.
  **Examples:**
  - `"Semantic versioning; all versions retained indefinitely in OSTI"`
  - `"Major versions only; prior versions available on request from data steward"`

---

### `reviews`
**Annotation:** `[if_applicable]`  
A running chronological history of all formal reviews this dataset has undergone or is currently undergoing. **Add one entry per review stage. Do not overwrite earlier entries** — this is an append-only record that supports audit and compliance.

**Sub-fields per entry:**
- `stage`: The type of review — `internal_qa | security | export_control | irb | partner | publication | other`
- `purpose`: A brief description of why this review was conducted
- `status`: Current status — `not_started | submitted | pending | approved | declined`
- `institution`: The institution conducting the review (name and ROR ID)
- `reviewed_by`: The person or organization that conducted the review
- `review_date`: ISO 8601 date the review was completed or last updated
- `approval_document_url`: URL or path to the formal approval document, signed letter, or review record. **Particularly important for export control, IRB, and security reviews** — this creates a traceable link to the official record.
- `comments`: Reviewer notes, conditions, or required follow-up actions

---

### `related_resources`
**Annotation:** `[if_applicable]`  
Links to datasets, publications, software, and AI models related to this dataset.

**Relationship vocabulary** — use consistently across all resource types:

*Base vocabulary (all types):*
`is_derived_from | is_based_on | is_part_of | has_part | references | other`

*Extended vocabulary (software and AI models only):*
`used_to_create | used_to_process | used_to_analyze | trained_on | evaluated_on`

**Sections:**
- `datasets`: Related datasets — source data, derivatives, companion datasets
- `publications`: Papers, reports, or preprints associated with this dataset — DOIs, arXiv IDs, or URLs
- `software`: Software used to create, process, or analyze the data
- `ai_models`: AI models associated with this dataset (used to create it, or trained/evaluated on it)

---

### `compliance`
**Annotation:** `[extended]` for DOE fields; `[sensitive]` for review fields  
Populate when `release_status = under_review | approved | published`. Leave blank for draft and in-workflow datasets.

- **`doe_data_management_plan`** `[extended]`: A DOE data management plan is on file for this dataset
- **`osti_elink2_metadata_compliant`** `[extended]`: Metadata complies with OSTI E-Link 2 API specifications. If unsure, check with your data manager before setting to `true`.
- **`export_control_reviewed`** `[sensitive]`: Export control review has been completed
- **`irb_approved`** `[sensitive]`: IRB approval obtained. Use `not_applicable` if the dataset does not involve human subjects.
- **`security_review_completed`** `[sensitive]`: Institutional security review has been completed

---

### `citation`
**Annotation:** `[pub]`  
Required when `release_status = approved | published`. Provides the citation authors should use when referencing this dataset.

**`report_number`**: Institutional report or release number if applicable (e.g., `SAND2024-XXXXX`, `LAUR-XX-XXXXX`, `ORNL/TM-2024/XXXXX`).

**`preferred_citation`**: The recommended citation in BibTeX format. **Replace all `${...}` placeholders before publishing.** The BibTeX block is a YAML literal block scalar (indicated by the `|` character) — the indented content below it is the BibTeX text.

**Example completed citation:**
```bibtex
@dataset{smith2024sns_bpm,
  author    = {Smith, Jane A. and Jones, Robert B.},
  title     = {SNS Beam Position Monitor Calibration Data 2023-2024},
  year      = {2024},
  publisher = {Oak Ridge National Laboratory},
  doi       = {10.25982/12345.6789},
  url       = {https://doi.org/10.25982/12345.6789}
}
```

---

## Section 4: Level 3 — AI-Ready & Trustworthy

*Required for the `ai_ready` profile, or for any dataset used in AI/ML workflows.*

---

### `ai_usage`
**Annotation:** `[ai_ready]`  
Describes whether and how this dataset may be used in AI/ML workflows. **Be explicit** — these fields are read by automated pipeline tooling that makes decisions about whether a dataset can be ingested into a training or evaluation workflow.

- **`ai_ready`**: Overall AI/ML suitability:
  - `true` — suitable for direct use
  - `false` — should not be used in AI/ML workflows
  - `conditional` — suitable under specific conditions; describe in `restrictions`

- **`training_use_allowed`**, **`inference_use_allowed`**, **`evaluation_use_allowed`**: Per-task permission flags. Use `conditional` when a task is permitted only under certain conditions.

- **`restrictions`**: Any restrictions on AI/ML use. Be specific — vague restrictions are difficult for pipelines to enforce.
  **Examples:**
  - `"Not for use in models intended for clinical decision-making"`
  - `"Training use permitted only with attribution; no commercial use"`
  - `"Export-controlled data — AI model outputs may themselves be export-controlled"`

- **`bias_risks`**: Known bias risks or representational gaps that could affect model behavior.
  **Example:** `"Dataset overrepresents samples from facility X operating under nominal conditions; underrepresents fault and off-normal states"`

- **`safety_considerations`**: Safety or ethical considerations for AI use.

- **`human_review_required`**: Whether a human must review AI/ML outputs derived from this dataset before they are used or acted upon.

---

### `data_quality`
**Annotation:** `[ai_ready]`  
**Be specific.** Vague quality statements like "good quality" or "data is clean" are not useful. Provide enough information for a user to assess whether the quality is adequate for their intended use.

- **`completeness`**: What fraction of expected data is present? What is missing and why?
  **Example:** `"All 120 BPM channels present; 2.1% of timesteps missing due to instrument downtime on 2023-04-12 (14:00–16:30 UTC)"`

- **`known_issues`**: Specific known errors, anomalies, or artifacts.
  **Example:** `"Sensor drift observed in BPM channels 45–48 after 2023-06-01T12:00:00Z — apply drift correction factor from calibration file"`

- **`validation_methods`**: How data quality was assessed.
  **Example:** `"Cross-validated against NIST SRM 640f reference standard; outlier detection using 3σ threshold"`

- **`noise_characteristics`**: The nature and magnitude of noise in the dataset.

- **`uncertainty_notes`**: Formal uncertainty quantification if available.
  **Example:** `"Measurement uncertainty ±0.5% (k=2) per ISO/IEC Guide 98-3 (GUM)"`

- **`missing_data_codes`**: Codes used to represent missing or invalid data in the dataset files. This is critical for ML pipelines that need to handle missing values correctly.
  **Example:**
  ```yaml
  missing_data_codes:
    - code: -999
      description: "Sensor malfunction — value not collected"
    - code: -888
      description: "Below detection limit"
    - code: NaN
      description: "Computation error or division by zero"
  ```

---

### `integrity`
**Annotation:** `[ai_ready]`  
Checksums and fixity information for verifying data integrity after transfer or storage.

- **`checksum_available`** (`true | false`): Whether a checksum is available for this dataset.

- **`checksum_type`**: The checksum algorithm used. `sha256` is strongly recommended for new datasets. `md5` is not recommended for new datasets due to known collision vulnerabilities, but is acceptable for legacy datasets where SHA-256 is not available.

- **`checksum_value`**: The checksum of the primary data file. For multi-file datasets, create a checksum manifest file (a file listing checksums for every file in the dataset) and provide the path or URL to the manifest here rather than individual file checksums.

- **`fixity_policy`**: How and how often data integrity is verified after ingest.
  **Example:** `"Monthly SHA-256 verification via repository integrity service; alerts on mismatch"`

---

### `semantic_layer`
**Annotation:** `[ai_ready]`  
Formal schema and semantic context information. Required for Level 3 datasets intended for federated or cross-domain use. Populate `schema_url` at minimum.

- **`schema_url`**: URL to a formal schema definition for this dataset.
  **Examples:**
  - JSON Schema: TBD (example: `https://your-repo/schemas/bpm-data/v1.0.json`)
  - NeXus application definition: `https://manual.nexusformat.org/classes/applications/NXmonopd.html`
  - XML Schema: `https://example.org/schema/dataset-v2.xsd`

- **`semantic_context`**: Semantic conventions or standards applied to the dataset's field naming, units, or structure.
  **Examples:**
  - `"NetCDF CF Conventions 1.10"` — standard conventions for geoscience data
  - `"NeXus NXmonopd application definition"` — neutron/X-ray monochromator powder diffraction
  - `"QUDT Units Ontology v2.1"` — standardized unit representations

---

## Section 5: Repository-Managed Block

*Do not edit this section. It is populated by the managing repository or catalog system at ingest.*

---

### `_repository`
This entire block is system-owned. The underscore prefix (`_repository`) signals to parsers that this block is managed by the repository system, not by the datacard author. Fields are populated when the datacard is ingested.

**System-populated fields:**

- **`populated_by_repository`**: Always `true`. Used by parsers to confirm this block is system-owned.
- **`ingest_date`**: ISO 8601 date this datacard was ingested by the managing system.
- **`repository_catalog_id`**: The identifier assigned to this datacard by the managing catalog.
- **`completeness_score`**: A score computed by the catalog against the declared profile. Used for quality reporting and to surface incomplete datacards.
- **`datacard_checksum`**: A SHA-256 or SHA-512 checksum of the raw datacard `.md` file as ingested. Recomputed on each ingest to detect post-ingest modifications.
- **`repositories`**: Resolved repository records keyed to `access.intended_repositories`. The system looks up each repository by name and populates the authoritative identifier, landing page, download URL, accession number, and access protocol.
- **`usage_metrics`**: Download count, view count, citation count, and last accessed date, populated by the managing repository.
- **`distributions`** and **`data_services`**: Distribution records and data service endpoints populated at ingest.

---

## Appendix A: Common Mistakes

| Mistake | Correct approach |
|---|---|
| Setting `datacard.sensitivity_tier` to match `security.sensitivity_tier` by default | Set each independently based on what it describes |
| Leaving `access_policy.sensitivity_tier` blank because it "already appears in security" | Fill it in — it is reproduced for access control systems that evaluate this block independently |
| Using `published` for `workflow.state` when the dataset is still under review | Use `review` for `workflow.state` and `under_review` for `release_status` |
| Mixing flat strings and structured entries in `dataset_info.features` | Choose one form and use it consistently throughout |
| Setting `doi` as the `primary_id.type` before a DOI has been minted | Use `ark` or `local` until a DOI is assigned; add the DOI to `additional_ids` when minted |
| Leaving `provenance.was_generated_by` blank | This is a `[core]` field — fill it in for every dataset regardless of profile |
| Writing `"good"` or `"clean"` for `data_quality.completeness` | Be specific — describe what is present, what is missing, and why |
| Not updating `change_log` when editing the datacard | Add an entry every time the datacard is updated; this is a `[core]` field |
| Setting `irb_approved: false` for a dataset with no human subjects | Use `not_applicable` — `false` implies an IRB review was needed but not obtained |

---

## Appendix B: Identifier Type Quick Reference

| Type | Format | When to use |
|---|---|---|
| `doi` | `10.XXXXX/XXXXXXX` | Published datasets with a registered DOI |
| `ark` | `ark:/NAAN/shoulder+name` | Pre-publication datasets at ARK-enabled institutions |
| `handle` | `XXXXX/XXXXXXX` | Datasets in Handle-based repositories |
| `url` | `https://...` | When a stable URL is the best available identifier |
| `osti` | Numeric ID | Datasets registered in OSTI |
| `sand` | `SAND20XX-XXXXX` | Sandia National Laboratories report numbers |
| `la-ur` | `LA-UR-XX-XXXXX` | Los Alamos National Laboratory report numbers |
| `local` | Any internal ID | Pre-publication datasets with only internal identifiers |
| `other` | Any | Identifier systems not covered above |

---

## Appendix C: Sensitivity Tier Quick Reference

| Tier | Name | Typical use |
|---|---|---|
| `tier0_open` | Open Science | Fully open, publicly shareable data and datacards |
| `tier1_controlled_research` | Controlled Research | Internal research use, limited external sharing |
| `tier2_proprietary` | Proprietary | Proprietary or business-sensitive data |
| `tier3_sensitive` | Sensitive | Sensitive data requiring access controls |
| `tier4_export_controlled` | Export Controlled | EAR or ITAR controlled data |
| `tier5_regulated_personal` | Regulated Personal | Data containing PII, HIPAA-covered data |
| `tier6_classified` | Classified | Formally classified datasets |

---

## Appendix D: Profile Field Requirements Summary

| Field | core | extended | ai_ready | sensitive |
|---|---|---|---|---|
| `datacard.template_version` | system | system | system | system |
| `datacard.datacard_version` | ✅ | ✅ | ✅ | ✅ |
| `datacard.profile` | ✅ | ✅ | ✅ | ✅ |
| `datacard.creation_method` | ✅ | ✅ | ✅ | ✅ |
| `datacard.filename` | ✅ | ✅ | ✅ | ✅ |
| `datacard.sensitivity_tier` | ✅ | ✅ | ✅ | ✅ |
| `datacard.access_level` | ✅ | ✅ | ✅ | ✅ |
| `datacard.created_date` | ✅ | ✅ | ✅ | ✅ |
| `datacard.updated_date` | ✅ | ✅ | ✅ | ✅ |
| `datacard.change_log` | ✅ | ✅ | ✅ | ✅ |
| `datacard.created_by` | ✅ | ✅ | ✅ | ✅ |
| `identification.name` | ✅ | ✅ | ✅ | ✅ |
| `identification.project` | ✅ | ✅ | ✅ | ✅ |
| `identification.version` | ✅ | ✅ | ✅ | ✅ |
| `identification.primary_id` | ✅ | ✅ | ✅ | ✅ |
| `description.summary` | ✅ | ✅ | ✅ | ✅ |
| `description.keywords` | ✅ | ✅ | ✅ | ✅ |
| `object_type` | ✅ | ✅ | ✅ | ✅ |
| `dataset_type` | ✅ | ✅ | ✅ | ✅ |
| `release_status` | ✅ | ✅ | ✅ | ✅ |
| `workflow.state` | ✅ | ✅ | ✅ | ✅ |
| `provenance.was_generated_by` | ✅ | ✅ | ✅ | ✅ |
| `security.classification` | ✅ | ✅ | ✅ | ✅ |
| `security.sensitivity_tier` | ✅ | ✅ | ✅ | ✅ |
| `security.export_control` | ✅ | ✅ | ✅ | ✅ |
| `access_policy.sensitivity_tier` | ✅ | ✅ | ✅ | ✅ |
| `access_policy.access_level` | ✅ | ✅ | ✅ | ✅ |
| `access_policy.authorization_required` | ✅ | ✅ | ✅ | ✅ |
| `contact` | ✅ | ✅ | ✅ | ✅ |
| `sponsor_organizations` | ✅ | ✅ | ✅ | ✅ |
| `research_organizations` | ✅ | ✅ | ✅ | ✅ |
| `categorization.science_domain` | ✅ | ✅ | ✅ | ✅ |
| `dataset_info.formats` | ✅ | ✅ | ✅ | ✅ |
| `security.distribution_statement` | — | ✅ | ✅ | ✅ |
| `dates.data_collection_start/end` | — | ✅ | ✅ | ✅ |
| `compliance.doe_data_management_plan` | — | ✅ | ✅ | ✅ |
| `compliance.osti_elink2_metadata_compliant` | — | ✅ | ✅ | ✅ |
| `categorization.task_category` | — | — | ✅ | — |
| `categorization.task_subcategory` | — | — | ✅ | — |
| `ai_usage` | — | — | ✅ | — |
| `data_quality` | — | — | ✅ | — |
| `integrity` | — | — | ✅ | — |
| `semantic_layer` | — | — | ✅ | — |
| `security.pii` | — | — | — | ✅ |
| `compliance.export_control_reviewed` | — | — | — | ✅ |
| `compliance.irb_approved` | — | — | — | ✅ |
| `compliance.security_review_completed` | — | — | — | ✅ |
| `license` | at pub | at pub | at pub | at pub |
| `authors` | at pub | at pub | at pub | at pub |
| `citation` | at pub | at pub | at pub | at pub |
| `dates.issued` | at pub | at pub | at pub | at pub |

---

## Appendix E: Getting Help

- **Genesis data management team:** TBD
- **Template and schema documentation:** TBD
- **JSON Schema validator:** TBD
- **ROR ID lookup:** https://ror.org
- **ORCID registration:** https://orcid.org
- **SPDX license list:** https://spdx.org/licenses/
- **CUI registry:** https://www.archives.gov/cui
- **ARK identifier information:** https://arks.org
- **OSTI E-Link 2 API documentation:** https://www.osti.gov/elink
