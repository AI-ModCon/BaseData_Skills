# Additional gotchas

These are gotchas the day-to-day generation workflow doesn't hit
frequently — either they're schema-invisible (nothing in the validator
catches a violation) or the validator already produces a clear, actionable
error, so there's little value in front-loading them into `SKILL.md`'s main
Gotchas list. Read this file if you're debugging an unexpected result, or
before working with `created_by` ordering or `ai_model`/`software` agent
entries.

1. **`created_by` chronological ordering**: when
   `creation_method=Hybrid`, list the `ai_model` entry first (initial
   draft), then any `person` entry (reviewer). This ordering is not
   schema-enforced — nothing in the validator will flag a datacard that
   gets it backwards.

2. **`ai_model`/`software` agents require a `relationship` slot.** When
   `discoverability.datacard.created_by[].creator.ai_model` or `.software`
   is populated, `relationship` is required — one of `used_to_create |
   used_to_process | used_to_analyze | recorded_by | trained_on |
   evaluated_on` (`ExtendedRelationshipEnum`; there is no `other` value
   despite some upstream docs implying one). The same enum applies to
   `interoperability.related_resources.software[].relationship` and
   `.ai_models[].relationship`. The validator catches a missing
   `relationship` cleanly as `MISSING_REQUIRED`, so this is easy to fix
   once flagged.
