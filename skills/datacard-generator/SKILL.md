---
name: datacard-generator
description: Generate Genesis Mission Datacard v1.0 documentation for scientific datasets by introspecting a directory and filling the structured template. Use when the user asks to create a datacard, dataset card, dataset documentation, dataset metadata, document a dataset, or prepare a dataset for sharing. Supports four profiles — core (in-workflow/draft), extended (shared/published), ai_ready (AI/ML use), sensitive (CUI/export/PII). Also converts MODCON v1 datacards to Genesis v1.0.
allowed-tools: Bash(*) Read WebSearch WebFetch
---

# Generating Datacards

Generate a Genesis Mission Datacard v1.0 by introspecting a dataset
directory and filling the YAML frontmatter of the canonical template,
prompting the user for fields that introspection can't infer. The
markdown narrative body is preserved with `<metadata_key:foo>`
placeholders intact (downstream tooling expands them).

The skill also has a one-shot **Convert** path for migrating an existing
MODCON v1 datacard to Genesis v1.0.

## Workflow

Copy this checklist and check off steps as you go.

```
Progress:
- [ ] 1. Gather context (dataset_path + profile)
- [ ] 2. Run python3 scripts/introspect.py on the dataset directory
- [ ] 3. Load profile-specific guidance
- [ ] 4. Auto-fill YAML from introspect output
- [ ] 5. Confirm dataset_readiness.level with the user
- [ ] 6. Prompt for remaining required fields in batches
- [ ] 7. Compute filename and write the datacard
- [ ] 8. Run scripts/validate_datacard.py
- [ ] 9. Address findings; re-validate
- [ ] 10. Present review summary
```

### 1. Gather context

Ask the user, in this order:

- **Dataset path** — directory to document.
- **Profile** — `core` | `extended` | `ai_ready` | `sensitive`. See
  `references/profile-prompts.md` "When to use" guidance.
  - core (10-15 min): in-workflow / draft / simple
  - extended (30-45 min): shared with partners or published to
    OSTI/Zenodo/etc.
  - ai_ready (45-60 min): for AI/ML training, inference, or evaluation
  - sensitive (45-60 min): CUI / export-controlled / PII / classified

The Genesis Field Requirements doc is explicit: **choose the profile
first**. The profile dictates which fields are required.

### 2. Introspect the directory

Run `python3 scripts/introspect.py <dataset_path>` and capture the JSON. See
[references/introspection-commands.md](references/introspection-commands.md)
for what each output field means.

### 3. Load profile-specific guidance

Read `references/profile-prompts.md` (full file — it's structured by
profile). For deeper field-by-field explanation, load the relevant
section of `references/genesis_field_guide.md` only as needed (the file
is large; load by section anchor).

### 4. Auto-fill the data card

Read `references/genesis_v1.0_template.md` (the canonical template). Copy
it as the starting point for the new datacard. Populate the YAML
frontmatter using this decision table:

| Genesis field | Auto-fill if… | Otherwise |
|---|---|---|
| `datacard.created_date` / `.updated_date` | always (today, ISO 8601) | — |
| `datacard.creation_method` | always → `"hybrid"` | — |
| `datacard.change_log[0]` | always (date, version 1.0, "Initial creation" or "Converted from MODCON v1") | — |
| `datacard.filename` | computed from `identification.name` (see Filename rule below) | — |
| `datacard.language` | always → `"en"` (override if README is non-English) | — |
| `datacard.created_by[]` | always (AI model first if hybrid; see Gotcha #5) | — |
| `identification.name` | from README / CITATION.cff title | prompt |
| `identification.version` | from CITATION.cff or default "1.0" | prompt |
| `description.summary` | from README first paragraph | prompt |
| `description.keywords` | from README / CITATION.cff | prompt |
| `dataset_info.formats` | introspect.py `formats` | prompt |
| `dataset_info.features` | introspect.py `sample_columns` (flat for core/extended; structured for ai_ready) | prompt at ai_ready |
| `dataset_info.splits` | introspect.py `splits_detected` | leave empty |
| `dataset_scale.record_count` / `.compressed_bytes` | introspect.py | prompt |
| `license.spdx_id` | introspect.py `license_hint` | prompt at extended+ |
| `authors[]` | from CITATION.cff | prompt at extended+ |
| `citation.preferred_citation` | from CITATION.cff bibtex | prompt at `[pub]` |
| `provenance.was_generated_by` | always prompt (`[core]`, often forgotten) | — |
| `_repository.*` | **NEVER** — system-owned | — |

For ORCID / ROR / funding-ID live enrichment via public APIs, see
[references/live-enrichment.md](references/live-enrichment.md). Format
validation is handled automatically by the validator.

### 5. Confirm `dataset_readiness.level`

Suggest a level from the profile using this mapping:
- `core` → 1
- `extended` → 2
- `ai_ready` → 3
- `sensitive` → 2

Ask the user: *"Based on profile=`<p>`, I've set `dataset_readiness.level
= <n>`. Confirm or override?"* This mapping is a skill convention, not a
documented Genesis rule.

### 6. Prompt for missing fields

Present auto-discovered values for confirmation. Then ask for unfilled
required fields. Ask **3–5 at a time** following the batches in
`references/profile-prompts.md`. Stop and confirm after each batch.

### 7. Filename + write

**Filename rule:** `genesis_datacard_<snake_case(identification.name)>.md`,
where `snake_case` lowercases the name and replaces any non-alphanumeric
run with a single `_`.

**Where to save:** inside `<dataset_dir>/` by default; ask if the user
prefers elsewhere.

**What to write:** the canonical template
(`references/genesis_v1.0_template.md`) with the YAML frontmatter fully
populated. Leave the markdown body (below the second `---`) unchanged —
keep `<metadata_key:foo>` placeholders intact for downstream automation.

### 8. Validate

Run:

```bash
python3 scripts/validate_datacard.py <written_file> --profile <p>
```

The validator emits structured codes:

- `MISSING_REQUIRED:<field>` — re-prompt the user
- `BAD_ENUM:<field>` — show enum from `references/lookup-tables.md`; re-prompt
- `BAD_FORMAT:<field>` — show format hint; re-prompt (ORCID, ROR, DOI, ISO 8601)
- `INCONSISTENT:<field>` — show both conflicting fields; ask user which to change
- `SENSITIVITY_MISMATCH` — informational; mention in review summary but do not block

### 9. Address findings

Loop steps 6 → 7 → 8 until `--json` output has `"ok": true`. **Do not
claim done with un-addressed errors.** `warn` and `info` severity
findings can stand in the review summary but errors must be resolved.

### 10. Review summary

Present:
- Auto-populated fields (count + brief list)
- User-provided fields (count + brief list)
- Empty / `not_applicable` fields (with reason)
- Validator warnings (e.g., alignment mismatch, deprecated without supersedure)
- Suggestions for improvement (e.g., add `data_quality.completeness`
  even though it's [if_applicable])

Ask if the user wants to revise any section before finishing.

---

## Convert path (MODCON v1 -> Genesis v1.0)

When the user asks to convert an existing MODCON v1 datacard:

1. Run `python3 scripts/convert_v1_to_genesis.py <v1_path> --json` and capture the JSON report. The report has three lists:
   - `mapped` — Genesis fields the converter populated from v1 (no user input needed).
   - `missing_required` — Genesis fields required by the `core` profile that the converter could not map. **Iterate over this list and prompt the user for each** (batched 3–5 per `references/profile-prompts.md`).
   - `orphans` — v1 fields with no Genesis equivalent. Surface them to the user so they can decide whether to drop or relocate.
2. After prompting, rerun the converter without `--json` to write the file (`--out <path>`), or compose the final YAML inline and write directly.
3. Set `datacard.creation_method = "hybrid"` and ensure `change_log[0] = {date: today, datacard_version: "1.0", summary: "Converted from MODCON v1"}` (the converter already does this — verify after writing).
4. Run the validator (step 8 of the Generate path above).
5. Present the review summary (step 10 of the Generate path above).

---

## Gotchas (read before generating)

1. **Two sensitivity tiers are independent.** `datacard.sensitivity_tier`
   (the document) does not equal `security.sensitivity_tier` (the data). Never default
   them to match. A common valid case: open datacard describing a
   PII-bearing dataset.

2. **`workflow.state` is not `release_status`.** Both required. See alignment
   table in `references/lookup-tables.md`.

3. **`access_policy.sensitivity_tier`** is a third reference to the
   dataset's sensitivity (same subject as `security.sensitivity_tier`).
   Set it independently; it will typically match `security.sensitivity_tier`.

4. **`dataset_info.features`** must use one form consistently: flat
   strings for `core`/`extended`, structured objects for `ai_ready`.
   Never mix.

5. **`created_by` chronological ordering**: when `creation_method=hybrid`,
   list the `ai_model` entry first (initial draft), then any `person`
   entry (reviewer).

6. **`primary_id.type`** should not be `doi` before a DOI is minted. Use
   `ark` or `local` for pre-publication states; mint a DOI on publication
   and retain the ARK in `additional_ids`.

7. **`provenance.was_generated_by`** is `[core]` and often forgotten.
   Even a one-line answer dramatically improves catalog value.

8. **`data_quality.completeness`** must be specific. "Complete" is not
   informative. "All detector channels present; 2% of timesteps missing
   due to instrument downtime on 2023-04-12" is.

9. **`change_log` is append-only.** On re-runs, add a new entry plus
   `updated_date` bump. Never edit or delete prior entries.

10. **`compliance.irb_approved`** uses `not_applicable` for non-human-subject
    data, **never** `false`. False means "we tried to get IRB approval and
    were denied."

11. **`_repository` block is system-owned.** Do not populate. Leave it
    as-is in the template (the underscore prefix is the parser signal).

12. **`not_applicable` is not blank.** Blank = "not yet known"; `not_applicable`
    = "definitively does not apply". Catalog completeness scoring uses
    this distinction.

13. **Filename convention is `genesis_datacard_<snake_case>.md`** — not
    `modcon_datacard_*` (the legacy v1 prefix).

---

## References

- **Template (do not edit)**: [references/genesis_v1.0_template.md](references/genesis_v1.0_template.md)
- **Field-by-field guidance**: [references/genesis_field_guide.md](references/genesis_field_guide.md) (load on demand by section)
- **Per-profile prompts**: [references/profile-prompts.md](references/profile-prompts.md)
- **Validation rules** (data — read by validator): [references/validation-rules.md](references/validation-rules.md)
- **Live ORCID/ROR/OSTI enrichment via public APIs**: [references/live-enrichment.md](references/live-enrichment.md)
- **Lookup tables** (enums in human form): [references/lookup-tables.md](references/lookup-tables.md)
- **Introspection commands**: [references/introspection-commands.md](references/introspection-commands.md)
- **Validator**: `scripts/validate_datacard.py`
- **Introspector**: `scripts/introspect.py`
- **Converter**: `scripts/convert_v1_to_genesis.py`
