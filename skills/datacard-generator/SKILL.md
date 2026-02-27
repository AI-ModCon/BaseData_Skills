---
name: datacard-generator
description: Generate MODCON data cards for scientific datasets by introspecting a dataset directory. Automatically analyzes file structure, formats, schemas, and metadata to pre-fill data card fields, then prompts for missing information. Supports three readiness levels — Level 1 (Discoverable), Level 2 (Interoperable & Reusable), Level 3 (Understandable & Trustworthy). Use when the user wants to create a data card, dataset card, datacard, dataset documentation, or dataset metadata following the MODCON/Genesis datacard template. Also use when asked to document a dataset, describe a dataset for sharing, or prepare dataset metadata for a repository.
---

# Datacard Generator

Generate structured data cards for scientific datasets using the MODCON Datacard v1 template. Introspect a dataset directory to auto-populate fields, then interactively fill remaining gaps.

## Workflow

### 1. Gather Initial Context

Ask the user two questions:

**Dataset directory**: "What is the path to the dataset directory you want to document?"

**Readiness level**: "What level of detail do you want for this data card?"
- **Level 1 — Discoverable**: Identification, basic description, file structure, keywords. Minimal metadata for discoverability.
- **Level 2 — Interoperable & Reusable**: Level 1 + contacts, access policy, license, domain/purpose, provenance, authors, contributors, related resources, maintenance plan.
- **Level 3 — Understandable & Trustworthy**: Level 2 + semantic/schema info, data quality details, integrity/fixity, AI/ML usage considerations, variable-level documentation.

### 2. Introspect the Dataset Directory

Explore the dataset directory to automatically extract as much information as possible:

#### File structure analysis
- List all files and directories recursively (use `find` or `ls -R`)
- Compute total size (compressed and uncompressed)
- Count files by extension
- Identify data formats (CSV, JSON, Parquet, HDF5, NetCDF, FITS, ROOT, images, etc.)

#### Data sampling and schema extraction
- For tabular files (CSV, TSV, Parquet): read headers, column names, dtypes, row counts, sample rows
- For JSON files: extract top-level keys and structure
- For HDF5/NetCDF: list groups, datasets, attributes, dimensions
- For image directories: count images, identify formats, check for metadata files
- Look for existing metadata files: README, CITATION, LICENSE, metadata.json, .zenodo.json, datacite.json, croissant.json, etc.

#### Identify splits
- Look for train/test/validation directory structure or naming conventions

#### Extract existing metadata
- Parse any README files for dataset description, citation, authors
- Parse any LICENSE files for license information
- Parse any CITATION.cff or .bib files for citation info
- Parse any existing metadata files for additional context

### 3. Auto-Fill the Data Card

Read the template from `references/datacard_template_v1.md`. Using the introspection results, populate as many fields as possible:

**Always auto-fillable:**
- `datacard_info.datacard_creation.created_date` — today's date
- `datacard_info.datacard_creation.creation_method` — "hybrid" (automated introspection + human input)
- `dataset_info.data_formats` — from file extension analysis
- `dataset_info.modalities` — inferred from file types (tabular, image, time-series, etc.)
- `dataset_info.features` — from column headers / schema extraction
- `dataset_info.splits` — from directory structure
- `dataset_counts` — from file/record counts
- `dataset_storage` — from size computation
- Files & Structure section — from directory listing

**Often auto-fillable (from existing metadata files):**
- `title` / `name` — from README or metadata
- Description — from README
- Keywords — from metadata files
- License — from LICENSE file
- Authors / contributors — from CITATION.cff
- Citation — from .bib or CITATION.cff

### 4. Prompt for Missing Required Fields

Present what was auto-discovered and ask the user to confirm or correct it. Then prompt for fields that could not be auto-filled, organized by the chosen level.

**Level 1 required prompts** (if not auto-filled):
- Dataset name and title
- Project name
- Dataset identifiers (DOI, URL, etc.)
- Dataset description
- Keywords
- Release status

**Level 2 additional prompts** (if not auto-filled):
- Contact point (name, email, affiliation, ORCID)
- Access policy (sensitivity tier, access level, authorization)
- License (SPDX ID, name, link)
- Science domain
- Originating research organization
- Funding sources
- Dataset authors and contributors
- Provenance (how was the data generated/collected?)
- Related resources (datasets, publications, software)
- Maintenance and stewardship plans
- Key dates (collection start/end, issued, modified)

**Level 3 additional prompts** (if not auto-filled):
- Semantic/schema information (ontologies, controlled vocabularies)
- Data quality (completeness, known issues, validation methods, noise, uncertainty)
- Integrity (checksums, fixity policy, versioning strategy)
- AI/ML usage (AI-ready status, training/inference allowed, bias risks, safety)
- Variable-level documentation table (name, description, unit, value labels)
- Missing data codes
- Data processing steps

When prompting, group related fields and provide examples. Do not overwhelm — ask 3-5 fields at a time using the AskUserQuestion tool where appropriate, or ask in natural conversation for open-ended fields.

### 5. Generate the Data Card

Produce the completed data card as a markdown file following the template structure:
- Output filename: `modcon_datacard_<snake_case_dataset_name>.md`
- Include the complete YAML frontmatter with all populated metadata fields
- Include the markdown body sections with filled-in content replacing all `[!TODO]` and `<REPLACE:...>` placeholders
- Remove all `<INSTRUCTIONS:...>` blocks
- Remove all `<REPLACE:...>` tags
- Remove all `<metadata_key:...>` tags
- Set `dataset_readiness.level` to the chosen level (1, 2, or 3)
- For fields not applicable or not provided, use "N/A" or leave the YAML value empty — do not leave TODO markers in the output

Ensure YAML frontmatter values and markdown sections are consistent (information should match between the two).

### 6. Review and Iterate

After generating the data card, present a summary of:
- Fields that were auto-populated vs. user-provided
- Any fields left empty or marked N/A
- Suggestions for improving the data card (e.g., "Consider adding checksums for Level 3 readiness")

Ask if the user wants to revise any sections.

## References

- **Full datacard template**: See [references/datacard_template_v1.md](references/datacard_template_v1.md) — the complete MODCON Datacard v1 template with YAML frontmatter and markdown sections. Read this to understand all available fields and their structure.
- **Datasheet reference**: See [references/datasheet_template.md](references/datasheet_template.md) — a companion datasheet format. Consult if the user mentions "datasheet" style questions or if additional context prompts from the datasheet format would help fill out the data card.

## Level Summary

| Level | Name | Focus | Required Sections |
|-------|------|-------|-------------------|
| 1 | Discoverable | Find the data | Identification, description, file structure, keywords |
| 2 | Interoperable & Reusable | Use the data | Level 1 + contacts, access, license, provenance, authors, related resources |
| 3 | Understandable & Trustworthy | Trust the data | Level 2 + schema, quality, integrity, AI/ML, variable docs |

## OSTI Dataset Type Codes

Use these when setting `dataset_info.dataset_type`:

| Code | Type |
|------|------|
| `GD` | Genome/Genetic Data |
| `IM` | Image |
| `ND` | Numeric Data |
| `SM` | Specialized Mix |
| `FP` | Figure/Plot |
| `I` | Interactive Resource |
| `MM` | Multimedia |
| `MD` | Model |
| `AS` | Automated Software |
| `IP` | Instrumentation and Protocols |
| `IG` | Integrated Genomic Resources |

## Sensitivity Tiers

Use these when setting `access_policy.sensitivity_tier`:

| Tier | Label |
|------|-------|
| tier0 | Open Science |
| tier1 | Controlled Research |
| tier2 | Proprietary |
| tier3 | Sensitive / Export Controlled |
| tier4 | Regulated / Personal |
| tier5 | Classified |
