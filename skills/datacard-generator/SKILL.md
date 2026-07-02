---
name: datacard-generator
description: Generate Genesis Mission Datacard v1.2 documentation for scientific datasets by introspecting a directory and filling the structured template. Use when the user asks to create a datacard, dataset card, dataset documentation, dataset metadata, document a dataset, or prepare a dataset for sharing. Supports six capability dimensions (discoverability, accessibility, interoperability, reusability, governed_use, ai_usability) — pick which ones apply via `supports_*` flags. Also converts MODCON v1 datacards to Genesis v1.2.
allowed-tools: Bash(*) Read WebSearch WebFetch
---

# Generating Datacards

Generate a Genesis Mission Datacard v1.2 by introspecting a dataset
directory and filling both the YAML frontmatter and the markdown narrative
body of the canonical template, prompting the user for fields that
introspection can't infer.

The skill also has a one-shot **Convert** path for migrating an existing
MODCON v1 datacard to Genesis v1.2.

**Validation is driven by the upstream JSON Schema** (`references/genesis_datacard.schema.json`)
applied via `scripts/validate_datacard.py`. The few warn-level rules JSON
Schema cannot express live in `references/validation-rules.md`.

## Workflow

Copy this checklist and check off steps as you go.

```
Progress:
- [ ] 1. Gather context (dataset_path + which `supports_*` capabilities apply)
- [ ] 2. Run python3 scripts/introspect.py on the dataset directory
- [ ] 3. Load capability-specific guidance
- [ ] 4. Auto-fill YAML from introspect output
- [ ] 5. Confirm dataset readiness level with the user (optional)
- [ ] 6. Prompt for remaining required fields in batches
- [ ] 7. Cross-check every ORCID/ROR/DOI/OSTI identifier via live APIs
- [ ] 8. Compute filename and write the datacard (YAML + markdown body)
- [ ] 9. Run scripts/validate_datacard.py
- [ ] 10. Address findings; re-validate
- [ ] 11. Present review summary
```

### 1. Gather context

Ask the user, in this order:

- **Dataset path** — directory to document.
- **Which capabilities does this dataset support?** Genesis v1.2 organizes fields into six capability containers. Ask Yes/No for each:
  - `supports_discoverability` — **always Yes** (schema enforces this). Identification, description, project, release status, contacts, authorship. Minimum core fields.
  - `supports_accessibility` — Yes if the dataset is meant to be accessed/shared. Adds access policy, endpoints, dataset scale.
  - `supports_interoperability` — Yes if the dataset uses standard formats, structured features, controlled vocabularies, or has documented provenance. Adds data_structure, dates, semantic_layer, provenance, related_resources.
  - `supports_reusability` — Yes if the dataset is licensed for downstream use. Adds license, citation, integrity, stewardship, data_quality.
  - `supports_governed_use` — Yes if the dataset has access restrictions, PII, export control, or formal review requirements. Adds use_governance, security/sensitivity blocks, compliance, review_provenance_companion.
  - `supports_ai_usability` — Yes if the dataset is suitable for AI/ML training, inference, or evaluation. Adds ai_usage policy block.

Each `supports_X = Yes` triggers a required `X` block in the YAML and a corresponding set of required fields. Each `supports_X = No` omits that block entirely.

### 2. Introspect the directory

Run `python3 scripts/introspect.py <dataset_path>` and capture the JSON. See
[references/introspection-commands.md](references/introspection-commands.md) for
what each output field means.

### 3. Load capability-specific guidance

Read `references/capability-prompts.md` (the per-capability prompt sequence).

For deep field-by-field explanation, load the relevant section of
`references/genesis_field_guide.md` only as needed (the file is large).

The upstream LinkML schema source is at `references/genesis_datacard_linkml.yaml`
for cases where you need to understand a class definition.

### 4. Auto-fill the data card

Read `references/genesis_v1.0_template.md` (the canonical template). Copy it
as the starting point for the new datacard. Populate the YAML frontmatter
using this decision table (paths use v2 capability-container structure):

| Genesis field | Auto-fill if… | Otherwise |
|---|---|---|
| `discoverability.datacard.created_date` | always (today, ISO 8601) | — |
| `discoverability.datacard.updated_date` | `if_applicable` — leave blank on initial creation; only set on subsequent edits (see Gotcha below) | — |
| `discoverability.datacard.creation_method` | always → `"Hybrid"` (Title case in v2) | — |
| `discoverability.datacard.template_version` | always → `"1.2"` (matches the vendored schema/template version) | — |
| `discoverability.datacard.change_log[0]` | always (`change_date`, `datacard_version: "1.2"`, "Initial creation" or "Converted from MODCON v1") | — |
| `discoverability.datacard.filename` | computed from `discoverability.identification.name` (see Filename rule below) | — |
| `discoverability.datacard.language` | always → `en` (override if README is non-English) | — |
| `discoverability.datacard.created_by[]` | always (AI model first if Hybrid; see Gotcha #4) | — |
| `discoverability.identification.name` | from README / CITATION.cff title | prompt |
| `discoverability.identification.version` | from CITATION.cff or default `"1.0"` | prompt |
| `discoverability.product_type` | never — `ProductTypeEnum` (see `references/lookup-tables.md`) | always prompt |
| `discoverability.datacard.id` | never — `IdentifierClass` (`{type: local, value: <slug>}` for pre-publication is a sensible default) | prompt |
| `discoverability.dataset_description.dataset_summary` | from README first paragraph | prompt |
| `discoverability.dataset_description.keywords` | from README / CITATION.cff | prompt |
| `interoperability.data_structure.formats` | introspect.py `formats` | prompt (requires `supports_interoperability=Yes`) |
| `interoperability.data_structure.features` | introspect.py `sample_columns` (structured form: `- name: x` objects) | prompt |
| `interoperability.data_structure.splits` | introspect.py `splits_detected` | leave empty |
| `accessibility.dataset_scale.record_count` / `.compressed_bytes` | introspect.py | prompt (requires `supports_accessibility=Yes`) |
| `reusability.license.spdx_id` | introspect.py `license_hint` | prompt (requires `supports_reusability=Yes`) |
| `reusability.license.name` | never | prompt whenever the `reusability.license` block is emitted (Pydantic requires it always, not just when `spdx_id=other`) |
| `discoverability.authors[]` | from CITATION.cff (use **CRediT roles** — see `references/lookup-tables.md`) | prompt |
| `reusability.citation.preferred_citation` | from CITATION.cff bibtex | prompt at `[pub]` |
| `interoperability.provenance.was_generated_by` | always prompt (often forgotten) | — |
| `discoverability.dataset_description.science_domain` | never auto-filled — closed `ScienceDomainEnum` (see `references/lookup-tables.md`) | prompt |
| `ai_usability.ai_usage.training_use_status` / `.inference_use_status` / `.evaluation_use_status` | never auto-filled | prompt (`Yes \| No \| Conditional`); if `Conditional`, also prompt for the matching `*_use_conditions` free-text field |
| `_repository.*` | **NEVER** — system-owned | — |

For each `supports_X=Yes`, also write `supports_X: "Yes"` at the top level
of the YAML. The JSON Schema enforces that the matching `X:` block must
exist when `supports_X=Yes`.

ORCID, ROR, DOI, and OSTI award numbers gathered here will be
**cross-checked against their public APIs in step 7** — not optional.
Format validation is handled automatically by the validator.

### 5. Confirm dataset readiness level (optional)

If the user wants to indicate dataset readiness, ask them to set a level
(1, 2, or 3) as freetext in the datacard narrative. There is no dedicated
`dataset_readiness` YAML field in Genesis v1.2 — readiness is expressed
through the combination of `supports_*` flags that are set to `"Yes"`.

As a heuristic to guide the user:

- 1 = Discoverable (metadata only; `supports_discoverability=Yes` + perhaps `accessibility`)
- 2 = Interoperable & Reusable (also license, contacts, provenance; `supports_interoperability` and `supports_reusability`)
- 3 = AI-Ready & Trustworthy (also semantic layer, integrity, governed use; `supports_ai_usability` or `supports_governed_use`)

A heuristic: count how many `supports_*` are Yes; >= 4 typically maps to
level 3, 2-3 maps to level 2, 1 maps to level 1. Confirm with the user.

### 6. Prompt for missing fields

Present auto-discovered values for confirmation. Then ask for unfilled
required fields. Ask **3-5 at a time** following the batches in
`references/capability-prompts.md`. Stop and confirm after each batch.

**Key vocabulary changes in v2** (full list in `references/lookup-tables.md`):

- **CRediT taxonomy** for `authors[].person.role` / `.organization.role` and
  `contributors[].person.role` / `.organization.role` (role[] lives **inside**
  the agent sub-block — see Gotcha below) —
  `Conceptualization`, `Data_Curation`, `Data_Collection`, `Formal_Analysis`,
  `Funding_Acquisition`, `Investigation`, `Methodology`, `Project_Administration`,
  `Resources`, `Software`, `Supervision`, `Validation`, `Visualization`,
  `Writing_Original_Draft`, `Writing_Review_Editing`, `Other` (16 values). **Multi-valued
  per author.** Replaces our previous `creator | contributor | data_collector | curator | publisher | sponsor | other` list.
- **Title_Case for all enums** — `Published` not `published`, `Draft` not `draft`, `Hybrid` not `hybrid`, etc.
- **Sensitivity** is no longer a tier ladder. Use `OverallSensitivityEnum`:
  `Public | Unclassified_Uncontrolled | CUI | UCNI | Classified | Legacy_Controlled | Mixed | Other_Controlled`.
- **Yes/No/Conditional** strings (not Python booleans) for
  `ai_usability.ai_usage.training_use_status` / `.inference_use_status` /
  `.evaluation_use_status` (renamed from `*_use_allowed`) and governance
  Yes/No fields. If any `*_use_status = "Conditional"`, the matching
  `*_use_conditions` free-text field is required.
- **`science_domain` is a closed enum** (`ScienceDomainEnum`, 15 values) —
  see `references/lookup-tables.md`. No longer free text.

### 7. Cross-check identifiers via live APIs

For EVERY ORCID, ROR, DOI, and OSTI award number in the datacard —
whether the user provided it or introspection inferred it — resolve it
against the public API per `references/live-enrichment.md`. **Do not
skip this step.** Run it even when the field is already populated.

Identifiers to check (v2 paths, when present):

- Every `discoverability.authors[].person.orcid` and `…person.affiliation.ror_id`
- Every `discoverability.authors[].organization.ror_id`
- Every `discoverability.contributors[].person.orcid` and `…ror_id`
- `discoverability.contact.person.orcid` and `…ror_id`
- Every `discoverability.additional_contacts[].person.orcid` and `…ror_id`
- `reusability.stewardship.maintainer.person.orcid` and `…ror_id` (when `supports_reusability=Yes`)
- Every `governed_use.review_provenance_companion[].reviewed_by.person.orcid` (when `supports_governed_use=Yes`)
- Every `discoverability.sponsor_organizations[].ror_id` and `…award_number` (the latter via OSTI)
- Every `discoverability.research_organizations[].ror_id`
- Every `discoverability.facilities[].ror_id` and `…location.ror_id`
- `discoverability.identification.primary_id.value` (if `type: doi`)
- Every `discoverability.identification.additional_ids[].value` of type `doi`
- Every `interoperability.related_resources.datasets[].identifier.value` (if `type: doi`)
- Every `interoperability.related_resources.publications[].value` (if `type: doi` or `arxiv`)

For each lookup:

- **Clean match** — silent pass.
- **Mismatch** — present both side-by-side, ask the user.
- **Datacard incomplete** — API has fields the datacard doesn't; offer to add.
- **Does not resolve** (404, error) — warn the user; likely typo.
- **Rate-limited** — retry once; if still failing, log and move on.

Use `WebFetch`. Endpoints in [references/live-enrichment.md](references/live-enrichment.md).

### 8. Filename + write

**Filename rule:** `genesis_datacard_<snake_case(discoverability.identification.name)>.md`,
where `snake_case` lowercases the name and replaces any non-alphanumeric
run with a single `_`.

**Where to save:** inside `<dataset_dir>/` by default; ask if the user
prefers elsewhere.

**What to write:** the canonical template
(`references/genesis_v1.0_template.md`) with **both halves filled**:

- **YAML frontmatter** — fully populated from the workflow above. Set
  `supports_discoverability: "Yes"` and any other `supports_X: "Yes"` the
  user opted into; omit the corresponding `X:` block (or set
  `supports_X: "No"`) for capabilities the user opted out of.
- **Markdown narrative body** — also fully filled. See
  [references/body-fill-guide.md](references/body-fill-guide.md) for the
  section-by-section mapping.

**Strip all placeholder markup before saving.** No `[!TODO]`, `<REPLACE:>`,
`<INSTRUCTIONS:>`, `<metadata_key:>`, `${VARIABLE}`, or `__VALUE__` tokens
should remain. Verify with:
`grep -E '\[!TODO\]|<REPLACE:|<INSTRUCTIONS:|<metadata_key:|\$\{|__VALUE__' <output_file>`

### 9. Validate

Run:

```bash
python3 scripts/validate_datacard.py <written_file>
```

The validator emits structured codes:

- `MISSING_REQUIRED:<field>` — re-prompt
- `BAD_ENUM:<field>` — show enum from `references/lookup-tables.md`; re-prompt
- `BAD_FORMAT:<field>` — show format hint; re-prompt
- `INCONSISTENT:<field>` — show conflicting values; ask user
- `SCHEMA_VIOLATION:<field>` — unexpected; investigate

Use `--json` to get machine-readable output for parsing the findings list.

### 10. Address findings

Loop steps 6 → 7 → 8 → 9 until `--json` output has `"ok": true`. **Do not
claim done with un-addressed errors.** `warn` severity findings can stand
in the review summary but errors must be resolved.

### 11. Review summary

Present:
- Auto-populated fields (count + brief list)
- User-provided fields (count + brief list)
- Empty / `not_applicable` fields (with reason)
- Validator warnings (e.g., filename alignment, workflow↔release alignment)
- Suggestions for improvement (e.g., add `reusability.data_quality.completeness` if
  reusability is supported and the field is empty)

Ask if the user wants to revise any section before finishing.

---

## Convert path (MODCON v1 → Genesis v1.2)

When the user asks to convert an existing MODCON v1 datacard:

1. Run `python3 scripts/convert_v1_to_genesis.py <v1_path> --json` and capture the JSON report. The report has three lists:
   - `mapped` — fields the converter populated.
   - `missing_required` — Genesis fields the converter couldn't map. **Iterate over this list and prompt the user.**
   - `orphans` — v1 fields with no v2 equivalent.
2. After prompting, rerun the converter or compose the final YAML inline.
3. Set `discoverability.datacard.creation_method = "Hybrid"`, `template_version = "1.2"`, and ensure
   `change_log[0] = {change_date: today, datacard_version: "1.2", summary: "Converted from MODCON v1"}`.
4. **Fill the markdown body** using `references/body-fill-guide.md`.
5. **Cross-check every identifier via live APIs** (step 7 of the Generate path).
6. Run the validator (step 9 of the Generate path).
7. Present the review summary (step 11 of the Generate path).

---

## Gotchas (read before generating)

1. **Title_Case for all enum values.** v2 uses `Published`, `Draft`, `Raw`,
   `Hybrid`, `Yes`, `No` — NOT lowercase. The JSON Schema enforces this.

2. **`workflow.state` ≠ `release_status`.** Both are needed (under
   `discoverability.workflow.state` and `discoverability.release_status`).
   Recommended alignments are in `references/lookup-tables.md`.

3. **Sensitivity is no longer a tier ladder.** Use
   `OverallSensitivityEnum` (`Public | Unclassified_Uncontrolled | CUI |
   UCNI | Classified | Legacy_Controlled | Mixed | Other_Controlled`) on
   both `discoverability.datacard.sensitivity.overall_sensitivity` (the
   document) and `discoverability.sensitivity.overall_sensitivity` (the
   dataset). These are independent and often differ — never default them
   to match.

4. **`created_by` chronological ordering**: when
   `creation_method=Hybrid`, list the `ai_model` entry first (initial
   draft), then any `person` entry (reviewer).

5. **CRediT roles** are multi-valued and replace the old role enum.
   See `references/lookup-tables.md` for the 16 valid values.

6. **`primary_id.type`** should not be `doi` before a DOI is minted.
   Use `ark`, `local`, or `unregistered` for pre-publication states.

7. **`provenance.was_generated_by`** is required (when
   `supports_interoperability=Yes`) and often forgotten. Even a one-line
   answer adds catalog value.

8. **`change_log` is append-only.** On re-runs, add a new entry plus
   `updated_date` bump. Never edit or delete prior entries. The field
   name inside each entry is `datacard_version` (the upstream template at line 244 has a typo — `data_card_version` — that conflicts with the schema; our local copy is fixed).

9. **`_repository` block is system-owned.** Do not populate. Leave it
   as-is in the template (the underscore prefix is the parser signal).

10. **`supports_discoverability` is always `"Yes"`.** The JSON Schema
    enforces this — every Genesis datacard has at least the
    discoverability block.

11. **Filename convention** is `genesis_datacard_<snake_case>.md` — not
    `modcon_datacard_*` (legacy v1 prefix).

12. **No `dataset_readiness` YAML field.** Genesis v1.2 does not have a
    top-level `dataset_readiness` key. Readiness is expressed through
    which `supports_*` flags are set to `"Yes"` and in narrative prose.

13. **`role[]` lives INSIDE the agent sub-block, not on the agent entry
    itself.** `AgentClass` (used by `created_by`, `contact`,
    `additional_contacts`, `authors`, `contributors`, `facilities`,
    `related_resources.software|ai_models`) has no top-level `role` slot —
    it is a tagged union of `person` / `organization` / `ai_model` /
    `software`, and each of those four sub-classes carries its own `role[]`
    (CRediT taxonomy). Do **not** write `role:` as a sibling of `person:`.
    Correct shape:
    ```yaml
    - contribution_date: "2026-07-01"
      creator:
        person:
          given_name: "Jane"
          family_name: "Doe"
          role: [Conceptualization, Data_Curation]   # inside person, not sibling
    ```

14. **`science_domain` is a closed, quoted-string-with-spaces enum.**
    `discoverability.dataset_description.science_domain` and
    `interoperability.domain_metadata.science_domain` both use
    `ScienceDomainEnum` — 15 values, all quoted strings containing spaces
    (e.g., `"Biology and Medicine"`, `"Energy Storage, Conversion, and
    Utilization"`), unlike every other enum in the schema which uses
    `Title_Case` / `snake_case` tokens. See `references/lookup-tables.md`
    for the full list. Free text is no longer accepted.

15. **`ai_model`/`software` agents require a `relationship` slot.** When
    `discoverability.datacard.created_by[].creator.ai_model` or `.software`
    is populated, `relationship` is required — one of `used_to_create |
    used_to_process | used_to_analyze | recorded_by | trained_on |
    evaluated_on` (`ExtendedRelationshipEnum`; there is no `other` value
    despite some upstream docs implying one). The same enum applies to
    `interoperability.related_resources.software[].relationship` and
    `.ai_models[].relationship`.

16. **`discoverability.datacard.updated_date` is now `if_applicable`, not
    required.** Leave it blank on initial creation (a datacard that has
    never been updated has nothing to report). Only set it when performing
    a genuine update to an existing datacard, alongside a new `change_log`
    entry (see Gotcha #8).

---

## References

- **Template (do not edit)**: [references/genesis_v1.0_template.md](references/genesis_v1.0_template.md)
- **Template YAML reference**: [references/genesis_v1.0_template.yaml](references/genesis_v1.0_template.yaml)
- **JSON Schema** (validator source of truth): `references/genesis_datacard.schema.json`
- **LinkML schema source**: `references/genesis_datacard_linkml.yaml`
- **Field-by-field guidance**: [references/genesis_field_guide.md](references/genesis_field_guide.md)
- **Per-capability prompts**: [references/capability-prompts.md](references/capability-prompts.md)
- **Body-fill guide**: [references/body-fill-guide.md](references/body-fill-guide.md)
- **Lookup tables** (enums, vocabularies): [references/lookup-tables.md](references/lookup-tables.md)
- **Validation extras** (warn-level rules): [references/validation-rules.md](references/validation-rules.md)
- **Live ORCID/ROR/OSTI enrichment**: [references/live-enrichment.md](references/live-enrichment.md)
- **Introspection commands**: [references/introspection-commands.md](references/introspection-commands.md)
- **Upstream provenance / vendor manifest**: [references/UPSTREAM_VERSION.md](references/UPSTREAM_VERSION.md)
- **Validator**: `scripts/validate_datacard.py`
- **Introspector**: `scripts/introspect.py`
- **Converter**: `scripts/convert_v1_to_genesis.py`
