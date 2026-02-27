---
name: croissant-validator
description: Validates and generates Croissant metadata for ML datasets. Use when checking dataset metadata compliance, creating new croissant.json files, validating existing metadata, or ensuring ML dataset descriptions follow the MLCommons Croissant format specification.
allowed-tools: Read, Bash, Write, Glob, Grep
---

# Croissant Metadata Validator & Generator

Validate and generate `croissant.json` metadata for ML datasets.

## Use This Skill When

- User asks to validate Croissant metadata.
- User asks to create or update `croissant.json`.
- User asks for MLCommons Croissant conformance checks.

## Skill Layout

- `scripts/validate_croissant.py`: required-field checks + optional `mlcroissant` validation.
- `scripts/generate_croissant_from_csv.py`: generate metadata from CSV headers and sample values.

Keep executable code in `scripts/`; keep `SKILL.md` focused on workflow.

## Python Environment Rule

For any command requiring package installs, use a temporary venv in the working directory and remove it after execution.

```bash
python3 -m venv .venv_croissant && \
.venv_croissant/bin/pip install -q mlcroissant pandas && \
# ... run command(s) ... && \
rm -rf .venv_croissant
```

Never run global `pip install`.

## Validation Workflow

1. Locate metadata file (`croissant.json`, `metadata.json`, or user-provided path).
2. Run script-level validation:
   ```bash
   python3 skills/croissant-validator/scripts/validate_croissant.py path/to/croissant.json
   ```
3. If `mlcroissant` validation is required, run in venv:
   ```bash
   python3 -m venv .venv_croissant && \
   .venv_croissant/bin/pip install -q mlcroissant && \
   .venv_croissant/bin/python skills/croissant-validator/scripts/validate_croissant.py path/to/croissant.json && \
   rm -rf .venv_croissant
   ```
4. Report: pass/fail, missing required fields, structural warnings, and fix suggestions.

## Generation Workflow (CSV)

1. Collect required inputs:
   - dataset name
   - description
   - SPDX license URL
   - creator name
   - dataset URL
2. Generate metadata from CSV:
   ```bash
   python3 skills/croissant-validator/scripts/generate_croissant_from_csv.py \
     data.csv \
     "My Dataset" \
     "Dataset description" \
     "https://spdx.org/licenses/MIT.html" \
     "Creator Name" \
     "https://example.com/dataset" \
     --output croissant.json \
     --cite-as "@misc{my-dataset-2026, title={My Dataset}, author={Creator Name}, year={2026}}"
   ```
3. Validate generated file with `validate_croissant.py`.
4. If needed, rerun generation or patch metadata manually.

## Required Metadata Fields

- `@context`
- `@type` = `sc:Dataset`
- `conformsTo` = `http://mlcommons.org/croissant/1.0`
- `name`
- `description`
- `license`
- `url`
- `creator`
- `datePublished`
- `distribution`

## High-Value Checks

- All `@id` values are unique.
- Each `cr:FileObject` has `sha256` or `md5`.
- `recordSet`/`field` references are valid.
- Dates use ISO format (`YYYY-MM-DD`).
- License uses SPDX URL.

## Common Fixes

- Add missing `conformsTo`.
- Replace non-SPDX license values with SPDX URLs.
- Add checksums to `cr:FileObject` entries.
- Add missing `field.source` mappings.

## Resources

- Spec: https://docs.mlcommons.org/croissant/docs/croissant-spec.html
- GitHub: https://github.com/mlcommons/croissant
- Release: http://mlcommons.org/croissant/1.0
