# Validation extras

The bulk of Genesis Datacard validation lives in the upstream Pydantic model
(`scripts/genesis_models.py`) and is applied automatically by
`scripts/validate_datacard.py`.

This file documents the **handful of rules the Pydantic model cannot
express** — they live in the validator's `check_extras()` function
(`scripts/validate_datacard.py`).

## Filename rule (warn)

`datacard.filename` must equal `genesis_datacard_<snake_case(identification.name)>.md`,
where `snake_case` lowercases the dataset name and replaces any non-alphanumeric
run with a single underscore.

- Severity: `warn` (informational; doesn't block validation)
- Path checked (v2): `discoverability.datacard.filename` ↔ `discoverability.identification.name`
- Legacy path checked: `datacard.filename` ↔ `identification.name` (for v1-shaped datacards)

## Workflow ↔ release_status alignment (warn)

The workflow state of the dataset should align with its release status. Mismatches
are not errors but should be flagged.

| `workflow.state` | Typical `release_status` |
|---|---|
| `Raw` / `Processing` / `QA` / `Analysis` | `Draft` |
| `Review` | `Under_Review` |
| `Embargo` / `Published` | `Approved` or `Published` |
| `Archived` | `Deprecated` or `Published` |

- Severity: `warn`
- Paths checked (v2): `discoverability.workflow.state` ↔ `discoverability.release_status`
- Legacy paths checked: `workflow.state` ↔ `release_status`

## Why these aren't in the Pydantic model

The Pydantic model at `scripts/genesis_models.py` is auto-generated from
the upstream LinkML source and covers required fields, enums, and format
patterns. It doesn't natively express:

- **Severity levels.** Pydantic validators are binary pass/fail; the
  filename mismatch and workflow/release_status misalignment are best
  surfaced as warnings, not errors that block validation.
- **Cross-field slug computation.** The filename rule requires computing
  `snake_case(identification.name)` and comparing against `filename` —
  possible via a `@model_validator`, but keeping this in the extras layer
  avoids re-vendoring the Pydantic model every time the rule changes.
- **Recommendation vs constraint.** The workflow/release alignment
  describes typical (not required) pairings — datacards in transitional
  states (`archived` but recently `published`) are valid.

## Adding new extras

When upstream adds rules the Pydantic model can enforce (as required
fields, enums, or patterns), no change is needed here. For new warn-level
rules: add a check in `check_extras()` and document it above.
