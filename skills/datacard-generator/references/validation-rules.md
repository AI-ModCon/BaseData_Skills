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

## Why these aren't in the schema

JSON Schema is binary pass/fail; it has no severity levels. The filename rule
is a cross-field invariant that JSON Schema *could* express via `allOf/if/then`
but would be awkward (and the schema is auto-generated upstream — we can't add to it).
The alignment rule is intentionally a recommendation, not a constraint — datacards
in transitional states (e.g., `archived` but recently `published`) are valid.

## Adding new extras

When upstream adds rules that JSON Schema can express, no change is needed here.
For new warn-level rules: add a check in `check_extras()` and document it above.
