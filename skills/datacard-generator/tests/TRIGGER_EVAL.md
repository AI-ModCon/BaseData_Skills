# Trigger evaluation checklist

Manual eval — run each prompt as the *first* message in a fresh Claude Code
session. Confirm the datacard-generator skill is invoked (and not invoked
when it shouldn't be).

## Should trigger

- [ ] "Make a datacard for the dataset in `./my-data/`"
- [ ] "Document this dataset for OSTI"
- [ ] "Create dataset metadata for sharing"
- [ ] "Prepare this dataset for AI training"
- [ ] "Convert this MODCON v1 datacard to Genesis v1.0"
- [ ] "Write a Genesis datacard for my CSV files"
- [ ] "I need a datacard at the ai_ready profile"
- [ ] "Generate a datasheet for this corpus"
- [ ] "Add a sensitive datacard for our CUI data"

## Should NOT trigger

- [ ] "Tell me about MODCON" — informational, not generation
- [ ] "What's a datacard?" — informational
- [ ] "Open this CSV in pandas" — unrelated
- [ ] "Validate this JSON against a schema" — wrong domain
- [ ] "Write a model card" — adjacent but distinct (Genesis distinguishes
  model cards via `object_type: model` but model-card generation is not
  this skill's primary path)

## Notes

If a "should trigger" prompt fails to invoke the skill, edit the
`description:` field in `SKILL.md` to add the missing trigger phrasing.
If a "should NOT trigger" prompt does invoke, the description is too
broad — tighten it.
