<!-- LOCAL FIX: citation.preferred_citation YAML block reformatted to parse cleanly. Original upstream at /Users/jlbez/Documents/repositories/data-cards/template/genesis_datacard_merged_shared.md has buggy indent. -->
---
# ============================================================
# GENESIS MISSION DATACARD v1.0
# ============================================================
# This datacard describes datasets ingested or created within
# the Genesis Mission. It is designed for human and machine
# authorship and ingestion across all sensitivity levels and
# publication states — from raw in-workflow data through
# published and archived datasets.
#
# TIERED STRUCTURE:
#   Level 1 — Basic & Discoverable       [REQUIRED — all datasets]
#   Level 2 — Interoperable & Reusable   [REQUIRED for sharing/publishing]
#   Level 3 — AI-Ready & Trustworthy     [REQUIRED for AI/ML workflows]
#
# PROFILES — set datacard.profile to declare your intent.
# The profile tells you which fields to fill in and tells
# catalog tooling what completeness to validate against.
#
#   core       — minimum viable datacard; 10–15 min to complete by hand.
#                Use for in-workflow, draft, or simple datasets.
#                Fill in all [core] fields.
#
#   extended   — full documentation for published or shared datasets.
#                Use for datasets going to OSTI, Zenodo, or partners.
#                Fill in all [core] and [extended] fields.
#
#   ai_ready   — extended plus all Level 3 fields.
#                Use for datasets intended for AI/ML training,
#                inference, or evaluation workflows.
#                Fill in all [core], [extended], and [ai_ready] fields.
#
#   sensitive  — extended plus full security, PII, and compliance blocks.
#                Use for CUI, export-controlled, or classified datasets.
#                Fill in all [core], [extended], and [sensitive] fields.
#
# FIELD ANNOTATIONS:
#   [core]          — required for all profiles
#   [extended]      — required for extended | ai_ready | sensitive profiles
#   [ai_ready]      — required for ai_ready profile only
#   [sensitive]     — required for sensitive profile only
#   [pub]           — required when release_status = approved | published
#   [if_applicable] — populate when the condition applies; skip if not relevant
#   [system]        — populated by the managing repository at ingest; do not edit
#
# PLACEHOLDER CONVENTIONS:
#   ${VALUE}        — fill in your value; field is required for your profile
#   __VALUE__       — fill in if applicable; delete or leave blank if not
#   not_applicable  — use when a field definitively does not apply
#                     (distinct from blank, which means "not yet known")
#
# NOTE ON null vs. not_applicable:
#   Blank / __VALUE__ = information not yet known or not yet captured.
#   not_applicable    = this field definitively does not apply to this dataset.
#   This distinction enables automated completeness scoring and catalog quality metrics.
#
# NOTE ON SENSITIVITY TIERS:
#   This template has two independent sensitivity tier fields:
#     datacard.sensitivity_tier  — sensitivity of THIS DATACARD DOCUMENT
#     security.sensitivity_tier  — sensitivity of THE DATASET ITSELF
#   These are intentionally independent and will often differ.
#   Example: an open datacard (datacard.sensitivity_tier=tier0_open) may
#   describe a classified dataset (security.sensitivity_tier=tier6_classified).
#   Do not assume they should match. Set each based on its own subject.
#   Note: access_policy.sensitivity_tier is a second reference to the
#   dataset's sensitivity (same subject as security.sensitivity_tier)
#   and will typically carry the same value.
#
# NOTE ON WORKFLOW STATE vs. RELEASE STATUS:
#   workflow.state   — describes the technical/processing lifecycle position
#                      of the data itself (raw → archived)
#   release_status   — describes the publication and governance state
#                      of the dataset record (draft → deprecated)
#   These should be logically consistent. Common alignments:
#     workflow.state=raw|processing|qa|analysis → release_status=draft
#     workflow.state=review                     → release_status=under_review
#     workflow.state=embargo|published          → release_status=approved|published
#     workflow.state=archived                   → release_status=deprecated|published
#
# SCHEMA VALIDATION:
#   A companion JSON Schema for machine validation is available at:
#   https://genesis.ornl.gov/schemas/datacard/v1.0.json
#   Validate your datacard before submission using the Genesis datacard
#   validator or any JSON Schema-compatible YAML validator.
#
# FUTURE EXTENSIONS:
#   This template will evolve. Fields under consideration for future
#   versions include ontology alignment, interoperability standards
#   (DCAT, schema.org), audience classification, consent typing,
#   and catalog-managed collection membership.
#   See https://genesis.ornl.gov/datacard/changelog for the roadmap.
# ============================================================


# ------------------------------------------------------------
# DATACARD METADATA
# Describes this document itself — not the dataset.
# ------------------------------------------------------------
datacard:
  template_version: "0.1"                     # [system] Do not modify — used by parsers to apply version-specific logic
  datacard_version: "1.0"                     # [core] Version of this specific datacard document.
                                               # Increment when the datacard is meaningfully updated.
                                               # Use semantic versioning: MAJOR.MINOR.PATCH
                                               # e.g., 1.0 → 1.1 for content updates; 1.x → 2.0 for structural changes
  profile: ${PROFILE}                          # [core] Declares the completeness level of this datacard.
                                               # core | extended | ai_ready | sensitive
                                               # See profile descriptions in the header above.
  filename: "genesis_datacard_${SNAKE_CASE_DATASET_NAME}.md"  # [core] Follow naming convention; align with identification.name
  language: en                                 # [core] ISO 639-1 language code for this datacard's content

  id:                                          # [if_applicable] Persistent identifier for this datacard document itself,
                                               # distinct from the dataset identifier. Assign if the datacard is
                                               # registered in a catalog or repository independently of the dataset.
    type: __TYPE__                             # doi | ark | handle | url | local | other
    value: __VALUE__

  sensitivity_tier: ${TIER}                   # [core] Sensitivity of THIS DATACARD DOCUMENT only.
                                               # Set based solely on the sensitivity of the metadata in this file —
                                               # not the dataset it describes. See NOTE ON SENSITIVITY TIERS above.
                                               # These two tiers are independent and will often differ.
                                               #   tier0_open               — no restrictions; publicly shareable
                                               #   tier1_controlled_research — internal research use; limited sharing
                                               #   tier2_proprietary        — proprietary; internal use only
                                               #   tier3_sensitive          — sensitive; access controls required
                                               #   tier4_export_controlled  — subject to EAR or ITAR restrictions
                                               #   tier5_regulated_personal — contains PII or regulated personal data
                                               #   tier6_classified         — formally classified; handle per classification guide
  access_level: ${LEVEL}                       # [core] Access level for THIS DATACARD DOCUMENT.
                                               # open | restricted | controlled
                                               # Set independently of the dataset's access level.
                                               # NOTE: Genesis currently only accepts "open" datacards.
                                               # Restricted and controlled tiers are reserved for future use.

  creation_method: ${METHOD}                  # [core] How this datacard was created or most recently updated.
                                               # manual    — filled out entirely by hand
                                               # automated — generated entirely by a pipeline or AI model
                                               # hybrid    — initially generated automatically, then reviewed/edited by a human
                                               # This field supports downstream quality assessment and provenance tracking.

  created_date: "${YYYY-MM-DD}"               # [core] ISO 8601 date this datacard was first created
  updated_date: "${YYYY-MM-DD}"               # [core] ISO 8601 date of most recent update; revise on every change

  change_log:                                  # [core] Running history of meaningful changes to this datacard.
                                               # Add a new entry every time the datacard is updated.
                                               # Do not overwrite or delete prior entries.
    - date: "${YYYY-MM-DD}"                   # [core] ISO 8601 date of this change
      datacard_version: "1.0"                 # [core] Datacard version after this change; pre-filled for initial creation
      summary: "Initial creation"             # [core] Brief description of what changed and why.
                                               # Update this text for all subsequent revisions.
                                               # e.g., "Updated license to CC-BY-4.0"
                                               # e.g., "Added checksum after file transfer to OSTI"
                                               # e.g., "Corrected collection end date"

  created_by:                                  # [core] All individuals, organizations, AI models, or software tools
                                               # that created or updated this datacard. List in chronological order
                                               # of contribution — e.g., if an AI model generated the initial draft
                                               # and a person then edited it, list the AI model first.
    - role: ${ROLE}                            # [core] initial_creation | editor | reviewer | updater
      date: "${YYYY-MM-DD}"                   # [core] ISO 8601 date of this specific contribution
      description: __DESCRIPTION__             # [if_applicable] Describe what this contributor did.
                                               # e.g., "Automated generation of datacard from dataset metadata"
                                               # e.g., "Reviewed and corrected AI-generated content"
      creator:
        type: ${TYPE}                          # [core] person | organization | ai_model | software
                                               # Delete the three blocks below that do not apply.

        # TYPE: person — use for a human contributor
        person:
          given_name: ${GIVEN_NAME}
          family_name: ${FAMILY_NAME}
          orcid: __ORCID__                     # [if_applicable] Format: 0000-0000-0000-0000
                                               # Register at https://orcid.org if needed
          email: ${EMAIL}
          affiliation:
            name: ${ORG_NAME}
            ror_id: __ROR_ID__                 # [if_applicable] Format: https://ror.org/XXXXXXX
                                               # Look up at https://ror.org

        # TYPE: organization — use when a team or org created the datacard without a named individual
        organization:
          name: ${ORG_NAME}
          ror_id: __ROR_ID__

        # TYPE: ai_model — use when an AI model generated or substantially contributed to this datacard
        ai_model:
          name: ${MODEL_NAME}                  # e.g., Claude 3.5 Sonnet | GPT-4o | Llama 3
          version: __VERSION__
          date_accessed: "${YYYY-MM-DD}"
          identifier:
            type: __TYPE__                     # doi | ark | handle | url | local | other
            value: __VALUE__                   # Link to model card or documentation if available

        # TYPE: software — use when an automated pipeline or script generated this datacard
        software:
          name: ${SOFTWARE_NAME}
          version: __VERSION__
          identifier:
            type: __TYPE__                     # doi | ark | handle | url | local | other
            value: __VALUE__


# ============================================================
# LEVEL 1 — BASIC & DISCOVERABLE                   [REQUIRED]
# ============================================================
# Required for all datasets regardless of publication state
# or profile. A dataset at release_status=draft filing a
# core profile need only satisfy Level 1.
# ============================================================

# --- Identification ---------------------------------------------
identification:
  name: "${DATASET_NAME}"                     # [core] Single human-readable name for this dataset.
                                               # Use the same name in the datacard filename.
                                               # If this datacard covers a collection, provide the collection name.
  project: "${PROJECT_NAME}"                  # [core] Genesis project or sub-project this dataset belongs to.
                                               # e.g., genesis | genesis-fusion | genesis-lightsource
  version: "1.0"                              # [core] Dataset version using semantic versioning: MAJOR.MINOR.PATCH
                                               # Increment MAJOR for breaking changes, MINOR for additions,
                                               # PATCH for corrections. Start at 1.0 for first release.
                                               # See supersedes / superseded_by below for linking versions,
                                               # and stewardship.versioning_strategy for how versions are managed.

  primary_id:                                 # [core] Primary persistent identifier for this dataset.
                                               # Use ark or local if a DOI has not yet been assigned.
    type: ${TYPE}                             # doi | ark | handle | url | osti | local | other
    value: ${VALUE}
    # ARK format:  ark:/NAAN/shoulder+assigned_name  e.g., ark:/12345/b2345679k
    # Resolve via: https://n2t.net/ark:/NAAN/...
    # Convention:  use ark for pre-published states; mint a doi upon publication
    #              and retain the ark in additional_ids for provenance continuity

  additional_ids:                             # [if_applicable] Additional identifiers for this dataset.
    - type: __TYPE__                          # doi | ark | handle | url | osti | sand | la-ur | local | other
      value: __VALUE__                        # e.g., SAND2024-XXXXX | LAUR-XX-XXXXX

  supersedes:                                 # [if_applicable] Identifier of the prior version this dataset replaces.
                                               # See stewardship.versioning_strategy for how versions are managed.
    type: __TYPE__                            # doi | ark | handle | url | local | other
    value: __VALUE__

  superseded_by:                              # [if_applicable] Identifier of the newer version that replaces this dataset.
                                               # Populate when this version is deprecated.
    type: __TYPE__                            # doi | ark | handle | url | local | other
    value: __VALUE__

  parent_collection:                          # [if_applicable] Parent collection or experimental campaign this
                                               # dataset belongs to. Use when this dataset is one of many in a
                                               # larger organized collection or ensemble.
    name: __NAME__
    identifier:
      type: __TYPE__                          # doi | ark | handle | url | local | other
      value: __VALUE__

# --- Description ------------------------------------------------
description:
  summary: "${SUMMARY}"                       # [core] 1–3 sentence plain-language description of the dataset.
                                               # Write for a broad scientific audience unfamiliar with your project.
  purpose: __PURPOSE__                        # [if_applicable] Why was this dataset created? What gap does it fill?
  collection_methodology: __METHODOLOGY__     # [if_applicable] How was data acquired?
                                               # e.g., experimental sensors | computational simulation |
                                               #        human annotation | derived from prior datasets
  data_characteristics: __CHARACTERISTICS__  # [if_applicable] Key structural and content characteristics:
                                               # scale, dimensionality, temporal coverage, spatial resolution
  intended_use: __INTENDED_USE__             # [if_applicable] Tasks or workflows this dataset is designed to support.
                                               # e.g., ML training | physics analysis | benchmarking | visualization
  current_use: __CURRENT_USE__               # [if_applicable] For in-workflow data: what is this dataset actively
                                               # being used for right now? Distinct from intended_use.
  out_of_scope_use: __OUT_OF_SCOPE__         # [if_applicable] Uses this dataset should NOT be applied to.
                                               # e.g., clinical decision-making | real-time control systems
  limitations: __LIMITATIONS__               # [if_applicable] Known limitations, gaps, or caveats users should
                                               # be aware of before using this dataset.
  keywords:                                   # [core] Terms that describe this dataset and aid discovery.
    - ${KEYWORD}                              # Include domain terms, methods, instruments, and relevant ontology terms.

# --- Object & Dataset Type --------------------------------------
object_type: ${TYPE}                          # [core] Primary type of digital object described by this datacard.
                                              # dataset | model | software | ai_agent | eval | framework | other

dataset_type: ${TYPE}                         # [core] OSTI DOE Data Explorer type code. Select the single best-fit:
                                              #   GD  Genome/Genetic Data     — DNA/RNA sequences, genomic annotations
                                              #   IM  Image                   — photographs, scans, microscopy, visualizations
                                              #   ND  Numeric Data            — measurements, time series, tabular, sensor readings
                                              #   SM  Specialized Mix         — multiple data types combined
                                              #   FP  Figure/Plot             — charts, graphs, plots as primary deliverable
                                              #   I   Interactive Resource    — web apps, interactive visualizations, dashboards
                                              #   MM  Multimedia              — audio, video, combined media
                                              #   MD  Model                   — computational models, simulations, trained ML models
                                              #   AS  Automated Software      — scripts, analysis pipelines, workflows
                                              #   IP  Instrumentation/Protocols — experimental protocols, instrument specs
                                              #   IG  Integrated Genomic Resources — combined genomic databases and tools

# --- Release Status ---------------------------------------------
release_status: ${STATUS}                     # [core] Current publication and governance state of this dataset.
                                              # See NOTE ON WORKFLOW STATE vs. RELEASE STATUS in the header
                                              # for expected alignment with workflow.state.
                                              #   draft         — work in progress; not ready for sharing
                                              #   under_review  — submitted for formal review
                                              #   approved      — review complete; cleared for release
                                              #   published     — publicly released and accessible
                                              #   deprecated    — superseded or retired; no longer recommended for use

# --- Workflow & Lifecycle ---------------------------------------
# [core] Describes the technical and processing lifecycle position
# of the dataset. See NOTE ON WORKFLOW STATE vs. RELEASE STATUS
# in the header for expected alignment with release_status.
workflow:
  state: ${STATE}                             # [core] Current lifecycle position:
                                              #   raw        — data as collected; no processing applied
                                              #   processing — actively being cleaned, transformed, or reduced
                                              #   qa         — undergoing quality assurance or validation
                                              #   analysis   — in active scientific analysis
                                              #   review     — under formal review (security, export, IRB, etc.)
                                              #   embargo    — complete but intentionally withheld from release
                                              #   published  — publicly released
                                              #   archived   — preserved; no longer actively maintained
  is_intermediate: __BOOL__                   # [if_applicable] true if this is an intermediate processing artifact
                                              # rather than a final deliverable. false if this is final.
  pipeline_stage: __STAGE__                   # [if_applicable] Freetext position in processing pipeline.
                                              # e.g., "post-detector, pre-reconstruction"
                                              # e.g., "raw telemetry, pre-calibration"
  embargo_until: __YYYY-MM-DD__              # [if_applicable] Required if state=embargo.
                                              # ISO 8601 date after which release is permitted.

# --- Dataset Readiness ------------------------------------------
# Readiness describes usability — not scientific quality or value.
#   Level 1 — Discoverable: sufficient metadata to find and identify the dataset
#   Level 2 — Interoperable & Reusable: accessible, governed, licensed, and
#              documented for use within defined sensitivity and access constraints
#   Level 3 — AI-Ready & Trustworthy: semantically clear, provenance-aware,
#              integrity-supported, and suitable for AI/ML workflows
dataset_readiness:
  level: __LEVEL__                            # [if_applicable] 1 | 2 | 3
  evaluated_against: __MODEL__               # [if_applicable] e.g., "Genesis Dataset Readiness Model v1.0"
  evaluated_at: __YYYY-MM-DD__               # [if_applicable] ISO 8601 date the evaluation was performed
  evaluated_by:                               # [if_applicable] Person or organization that performed the evaluation.
                                              # Delete the block that does not apply.
    type: __TYPE__                            # person | organization
    person:
      given_name: __GIVEN_NAME__             # [if_applicable]
      family_name: __FAMILY_NAME__           # [if_applicable]
      orcid: __ORCID__                       # [if_applicable]
      email: __EMAIL__                       # [if_applicable]
      affiliation:
        name: __ORG_NAME__                   # [if_applicable]
        ror_id: __ROR_ID__                   # [if_applicable]
    organization:
      name: __ORG_NAME__                     # [if_applicable]
      ror_id: __ROR_ID__                     # [if_applicable]
  confidence: __CONF__                        # [if_applicable] high | medium | low


# ============================================================
# LEVEL 2 — INTEROPERABLE & REUSABLE      [REQUIRED TO SHARE]
# ============================================================
# Required for extended | ai_ready | sensitive profiles, and
# when release_status is under_review, approved, or published,
# or when data is shared beyond the originating team.
# Fields annotated [pub] are additionally required when
# release_status = approved | published.
# ============================================================

# --- Security & Classification ----------------------------------
# Describes the formal security classification and handling
# requirements for THE DATASET (not this datacard).
# Consult your institution's information security office if
# unsure of the correct markings.
# See NOTE ON SENSITIVITY TIERS in the header — the dataset's
# sensitivity tier is independent of the datacard's sensitivity tier.
security:
  classification: ${CLASS}                   # [core] Formal classification level of the dataset:
                                              #   U    — Unclassified
                                              #   CUI  — Controlled Unclassified Information
                                              #   C    — Confidential
                                              #   S    — Secret
                                              #   TS   — Top Secret
  sensitivity_tier: ${TIER}                  # [core] Sensitivity of THE DATASET — set independently of
                                              # datacard.sensitivity_tier. See NOTE ON SENSITIVITY TIERS above.
                                              # Example: datacard.sensitivity_tier=tier0_open with
                                              # security.sensitivity_tier=tier5_regulated_personal is valid —
                                              # it means the datacard is publicly shareable but the data is PII.
                                              # See datacard.sensitivity_tier for tier definitions.
  sensitivity_level: __LEVEL__               # [if_applicable] Human-readable quick filter for catalog use.
                                              # public | internal | confidential | restricted
                                              # Use alongside sensitivity_tier; does not replace it.
  cui_marking: __MARKING__                   # [required if classification=CUI] Specific CUI marking.
                                              # e.g., CUI | CUI//SP-PRVCY (PII) | CUI//SP-PROPIN (Proprietary)
                                              #        CUI//SP-EXPT (Export Controlled)
                                              # See https://www.archives.gov/cui for full registry.
  distribution_statement: __STMT__           # [extended] Distribution limitation statement.
                                              # e.g., "Distribution A - Approved for public release; distribution is unlimited."
                                              # e.g., "Distribution D - Distribution authorized to DoD and DoD contractors only."
  handling_instructions: __INSTR__           # [if_applicable] Special handling beyond the distribution statement.
                                              # e.g., "No foreign dissemination" | "Export-controlled handling required"
  export_control: ${CONTROL}                 # [core] Export control jurisdiction: none | EAR | ITAR
  export_control_id: __ID__                  # [required if export_control != none] Classification number.
                                              # e.g., EAR99 | ECCN 3E001 | USML Category XV
  data_rights: __RIGHTS__                    # [if_applicable] Legal rights statement, separate from license.
                                              # e.g., "Government has unlimited rights"
                                              # e.g., "Contractor retains rights with government license"
  last_reviewed_date: __YYYY-MM-DD__         # [if_applicable] Date security markings were last reviewed and
                                              # confirmed current. Update whenever markings are revalidated.
  pii:                                        # [sensitive] Complete this block if sensitivity_tier=tier5_regulated_personal
    present: __BOOL__                         # [sensitive] true | false
    types: []                                 # [required if present=true] PII types present:
                                              # names | email_addresses | phone_numbers | location_data |
                                              # biometric_data | financial_data | health_data | other
    deidentification_applied: __BOOL__        # [if_applicable] true | false
    deidentification_method: __METHOD__       # [required if deidentification_applied=true]
                                              # e.g., "k-anonymity (k=5)" | "differential privacy (ε=1.0)" |
                                              #        "direct identifier removal per HIPAA Safe Harbor"
    deidentification_reviewed: __BOOL__       # [if_applicable] true | false — was the method formally reviewed?
  classification_reason: __REASON__          # [required if classification != U]
                                              # e.g., "Contains export-controlled simulation parameters"
  declassification:
    review_date: __YYYY-MM-DD__              # [required if classification != U]
    authority: __AUTHORITY__                 # [required if classification != U]

# --- Access Policy ----------------------------------------------
# Describes who can access this dataset and under what conditions.
# access_policy.sensitivity_tier describes the dataset's access
# sensitivity — the same subject as security.sensitivity_tier above,
# reproduced here for access control systems that evaluate this
# block independently. It will typically carry the same value as
# security.sensitivity_tier. Both are independent of
# datacard.sensitivity_tier. See NOTE ON SENSITIVITY TIERS above.
access_policy:
  sensitivity_tier: ${TIER}                  # [core] Sensitivity of the dataset for access control purposes.
                                              # Typically matches security.sensitivity_tier (same subject — the dataset).
                                              # Both are independent of datacard.sensitivity_tier (the document).
  access_level: ${LEVEL}                     # [core] open | restricted | controlled
  access_restrictions: __RESTRICTIONS__      # [if_applicable] Freetext description of access restrictions.
                                              # e.g., "Requires signed DUA" | "None - publicly accessible"
  authorization_required: ${AUTH}            # [core] Authorization needed to access this dataset:
                                              #   none                  — no authorization required
                                              #   account               — registered account required
                                              #   user_agreement        — user agreement or terms of service
                                              #   data_use_agreement    — formal DUA required
                                              #   sponsor_approval      — sponsor or PI approval required
                                              #   export_control_review — export control review required
                                              #   irb_approval          — IRB approval required
                                              #   other                 — describe in access_restrictions
  policy_url: __URL__                        # [if_applicable] URL to the full access policy document
  policy_text: __TEXT__                      # [if_applicable] Inline summary if no policy_url exists

# --- License ----------------------------------------------------
# [pub] Required when release_status = approved | published.
# Use "pending" if not yet assigned.
license:
  spdx_id: __SPDX_ID__                      # [pub] SPDX license identifier: https://spdx.org/licenses/
                                             # e.g., CC-BY-4.0 | CC0-1.0 | Apache-2.0 | MIT
                                             # Use "other" if not in SPDX registry. Use "pending" if not yet assigned.
  name: __LICENSE_NAME__                     # [required if spdx_id=other]
  url: __LICENSE_URL__                       # [if_applicable] URL to license text or "LICENSE.md" for repo-local file

additional_licenses: []                      # [if_applicable] For multi-licensed datasets (e.g., data under CC-BY,
                                             # code under Apache-2.0). Same structure as license above:
                                             # - spdx_id: __SPDX_ID__
                                             #   name: __LICENSE_NAME__
                                             #   url: __LICENSE_URL__

# --- Contacts ---------------------------------------------------
contact:                                     # [core] Primary point of contact for questions about this dataset.
                                             # Required for all profiles — every dataset must have a reachable contact.
  type: ${TYPE}                              # person | organization
  person:
    given_name: ${GIVEN_NAME}
    family_name: ${FAMILY_NAME}
    orcid: __ORCID__                         # [if_applicable] Format: 0000-0000-0000-0000
    email: ${EMAIL}
    affiliation:
      name: ${ORG_NAME}
      ror_id: __ROR_ID__                     # [if_applicable] Format: https://ror.org/XXXXXXX
  organization:                              # Use if no single named contact (e.g., a data management office)
    name: __ORG_NAME__
    ror_id: __ROR_ID__
  valid_until: __YYYY-MM-DD__               # [if_applicable] Date after which this contact may no longer be valid.
                                             # Use for project-bound contacts (students, postdocs, term staff).
  succession_note: __NOTE__                 # [if_applicable] Who to contact if this contact is no longer reachable.
                                             # e.g., "Contact the ORNL data management office at data@ornl.gov"

additional_contacts: []                      # [if_applicable] Additional contacts (e.g., instrument PI, data steward).
                                             # Same structure as contact above:
                                             # - type: person | organization
                                             #   person:
                                             #     given_name: __GIVEN_NAME__
                                             #     family_name: __FAMILY_NAME__
                                             #     orcid: __ORCID__
                                             #     email: __EMAIL__
                                             #     affiliation:
                                             #       name: __ORG_NAME__
                                             #       ror_id: __ROR_ID__
                                             #   valid_until: __YYYY-MM-DD__
                                             #   succession_note: __NOTE__

# --- Authorship & Credit ----------------------------------------
# [pub] At least one author required when release_status = approved | published.
# For draft or in-workflow data, populate with known contributors.
authors:
  - type: ${TYPE}                            # person | organization
    person:
      given_name: ${GIVEN_NAME}
      family_name: ${FAMILY_NAME}
      orcid: __ORCID__                       # [if_applicable] Strongly recommended — enables disambiguation and credit tracking
      email: __EMAIL__                       # [if_applicable]
      affiliation:
        name: ${ORG_NAME}
        ror_id: __ROR_ID__                   # [if_applicable]
    organization:
      name: __ORG_NAME__
      ror_id: __ROR_ID__
    role: ${ROLE}                            # creator | contributor | data_collector | curator | publisher | sponsor | other

contributors: []                             # [if_applicable] Supporting contributors who are not primary authors.
                                             # e.g., sample preparers, annotators, reviewers, submitters.
                                             # Same structure as authors above.

# --- Organizational Context -------------------------------------
sponsor_organizations:                       # [core] Organizations that funded or sponsored this dataset.
  - name: ${ORG_NAME}                        # e.g., DOE Office of Science | NNSA | NSF
    ror_id: __ROR_ID__                       # [if_applicable]
    award_number: __AWARD__                  # [if_applicable] e.g., DE-AC05-00OR22725
    program: __PROGRAM__                     # [if_applicable] e.g., "Advanced Scientific Computing Research"

research_organizations:                      # [core] Organizations that created or collected the data.
  - name: ${ORG_NAME}                        # e.g., Oak Ridge National Laboratory | Sandia National Laboratories
    ror_id: __ROR_ID__                       # [if_applicable]

facilities: []                               # [if_applicable] User facilities, HPC centers, or research infrastructure
                                             # used to collect, process, or store the dataset.
  # - name: __FACILITY_NAME__               # e.g., Spallation Neutron Source | Summit | Frontier
  #   ror_id: __ROR_ID__
  #   role: __ROLE__                        # collection | processing | storage | access
  #   location:                             # [if_applicable] Point location for facility-based experimental data.
  #     description: __DESC__               # e.g., "SNS Beamline 1B, Oak Ridge National Laboratory, TN, USA"
  #     ror_id: __ROR_ID__                  # ROR ID of the facility; cross-reference with name above

# --- Categorization ---------------------------------------------
categorization:
  science_domain: "${DOMAIN}"               # [core] High-level scientific domain or discipline.
                                             # e.g., materials_science | biology | physics | chemistry
                                             #        climate | fusion | lightsource | computer_science | other
  tags:                                      # [if_applicable] Structured tags for catalog filtering and discovery.
    project: ${PROJECT}                      # e.g., genesis
    science: __SCIENCE__                     # e.g., lightsource | fusion | materials | biology
    type: __TYPE__                           # e.g., dataset | model | agent | eval | framework | software
    risk: __RISK__                           # e.g., general | reviewed | restricted
  task_category: []                          # [ai_ready] Primary ML task category or categories for this dataset.
                                             # Populate for ai_ready profile; helps ML practitioners find
                                             # relevant datasets in the catalog.
                                             # e.g., classification | regression | segmentation | detection |
                                             #        generation | translation | summarization | ranking |
                                             #        anomaly_detection | clustering | reinforcement_learning | other
  task_subcategory: []                       # [ai_ready] More specific ML task subcategory or subcategories.
                                             # e.g., binary_classification | multi_class_classification |
                                             #        multi_label_classification | image_segmentation |
                                             #        object_detection | time_series_forecasting |
                                             #        named_entity_recognition | question_answering | other

# --- Dataset Characteristics ------------------------------------
dataset_info:
  formats: []                               # [core] File formats in this dataset.
                                             # e.g., ["CSV", "HDF5", "NetCDF4", "Parquet", "TIFF", "JSON"]
  encoding: __ENCODING__                    # [if_applicable] Character encoding for text-based formats.
                                             # e.g., UTF-8 | ASCII | Latin-1
                                             # UTF-8 strongly recommended. Use not_applicable for binary formats.
  schema_version: __VERSION__               # [if_applicable] Version of the data schema used in this dataset.
                                             # Distinct from datacard_version. Increment when field names,
                                             # types, or structure change between dataset versions.
  modalities: []                            # [if_applicable] Data modalities present.
                                             # e.g., ["tabular", "image", "time-series", "text", "graph", "point-cloud"]
  features: []                              # [if_applicable] Primary variables, fields, or features.
                                             # IMPORTANT: choose ONE form and use it consistently — do not mix.
                                             #
                                             # For core | extended profiles — flat string list:
                                             # e.g., ["temperature", "pressure", "timestamp", "label"]
                                             #
                                             # For ai_ready profile — structured form (replace flat list above):
                                             # - name: temperature
                                             #   type: float           # float | int | string | boolean | datetime | other
                                             #   unit: Kelvin
                                             #   description: Sample temperature at time of measurement
                                             #   range: "273.15 - 373.15"
  splits: []                                # [if_applicable] Dataset splits if pre-divided.
                                             # e.g., ["train", "test", "validation"]
  language: __LANG__                        # [if_applicable] ISO 639-1 language code for dataset content
                                             # (e.g., text corpora, annotation labels).
                                             # Distinct from datacard.language. Use not_applicable for
                                             # non-linguistic data (numeric, image, simulation output, etc.)
  spatial_coverage:                         # [if_applicable] Geographic coverage of the dataset.
                                             # Use for geospatial datasets or facility-based experiments.
    description: __DESC__                   # [if_applicable] e.g., "Continental United States" | "SNS Beamline 1B, ORNL"
    bounding_box:                            # [if_applicable] WGS84 decimal degrees; use for area coverage
      west: __DECIMAL_DEG__
      east: __DECIMAL_DEG__
      south: __DECIMAL_DEG__
      north: __DECIMAL_DEG__
  temporal_coverage:                        # [if_applicable] Time period the dataset content represents.
                                             # NOTE: distinct from dates.data_collection_start/end, which describe
                                             # when collection occurred. Use temporal_coverage when the dataset
                                             # describes a specific historical or projected time period that differs
                                             # from when collection happened.
                                             # e.g., "Monthly climate averages 1950–2020" collected in 2024:
                                             #   temporal_coverage.start = 1950-01-01
                                             #   dates.data_collection_start = 2024-01-01
    start: __YYYY-MM-DD__                   # [if_applicable]
    end: __YYYY-MM-DD__                     # [if_applicable]
    description: __DESC__                   # [if_applicable]

dataset_scale:
  record_count: __COUNT__                   # [if_applicable] Number of primary records, samples, or files
  record_unit: __UNIT__                     # [if_applicable] samples | files | records | timesteps | images | tokens | other
  compressed_bytes: __BYTES__               # [if_applicable] Total size when compressed, in bytes
  uncompressed_bytes: __BYTES__             # [if_applicable] Total size when uncompressed, in bytes

# --- Dates ------------------------------------------------------
dates:
  data_collection_start: __YYYY-MM-DD__    # [extended] ISO 8601 date data collection or generation began
  data_collection_end: __YYYY-MM-DD__      # [extended] ISO 8601 date data collection or generation ended
  issued: __YYYY-MM-DD__                   # [pub] ISO 8601 date the dataset was first publicly released
  modified: __YYYY-MM-DD__                 # [if_applicable] ISO 8601 date of most recent significant modification

# --- Access Endpoints -------------------------------------------
# Complete the fields you know at the time of datacard creation.
# Repository-assigned fields (landing pages, accession numbers,
# access protocols) will be populated by the managing repository
# or catalog system at ingest — see the REPOSITORY-MANAGED block.
access:
  current_location: __PATH_OR_URL__         # [if_applicable] Where the data physically resides right now.
                                            # Use for in-workflow data not yet deposited in a repository,
                                            # or for any dataset with a known internal or external storage path.
                                            # e.g., /mnt/ecs/scientific-data/project/dataset/
                                            # e.g., /lustre/orion/proj-shared/dataset/
                                            # e.g., s3://genesis-bucket/dataset/

  intended_repositories:                    # [if_applicable] Repositories you intend to deposit or have deposited
                                            # this dataset in. The managing repository or catalog system will
                                            # resolve and populate repository-assigned fields at ingest
                                            # (see REPOSITORY-MANAGED block). Repositories may be institutional,
                                            # project-owned, community, or national (e.g., OSTI, Zenodo,
                                            # institutional data repository, project data store).
    - name: __NAME__                        # [if_applicable] e.g., "OSTI Data Explorer" | "Zenodo" | "Globus" | "internal"
      access_level: __LEVEL__              # [if_applicable] Intended access level: open | restricted | controlled
                                            # The same dataset may have different access levels per repository.
      is_primary: __BOOL__                  # [if_applicable] true | false — only one entry should be marked true
      date_deposited: __YYYY-MM-DD__        # [if_applicable]
      api:                                  # [if_applicable] Populate if an API endpoint exists for this dataset
        endpoint: __URL__
        documentation_url: __URL__
        authentication: __AUTH__           # none | api_key | oauth2 | certificate | other
        version: __VERSION__
        rate_limit: __LIMIT__              # e.g., "1000 requests/hour"

# --- Provenance -------------------------------------------------
# Describes how this dataset was created, what it was derived
# from, and what processing was applied.
provenance:
  was_generated_by: __DESCRIPTION__        # [core] High-level description of the generating process.
                                            # Even a one-line answer dramatically improves catalog value.
                                            # e.g., "Neutron scattering experiment at SNS Beamline 1B"
                                            # e.g., "Monte Carlo simulation using MCNP 6.2"
                                            # e.g., "Derived from raw telemetry via calibration pipeline v2.1"
  source_data:                              # [if_applicable] Source datasets this dataset was derived from.
    - name: __NAME__
      identifier:
        type: __TYPE__                      # doi | ark | handle | url | local | other
        value: __VALUE__
      relationship: __REL__                # is_derived_from | is_based_on | is_part_of | has_part | references | other
  processing_steps: __DESCRIPTION__        # [if_applicable] Key processing, cleaning, calibration, or
                                            # transformation steps applied to produce this dataset.
  instrumentation: __DESCRIPTION__         # [if_applicable] Instruments, sensors, detectors, or equipment used.
                                            # Include make, model, and version where relevant.
  simulation_details: __DESC__             # [if_applicable] For simulation-derived data: code, version, key
                                            # parameters, and configuration.
                                            # e.g., "LAMMPS 23Jun2022, NVT ensemble, 300K, 10ns run, CHARMM36"
  software_environment:                    # [if_applicable] Software environment used to generate or process
                                            # this dataset. Captures what is needed for computational reproducibility.
    os: __OS__                              # [if_applicable] e.g., "RHEL 8.6" | "Ubuntu 22.04"
    compiler: __COMPILER__                  # [if_applicable] e.g., "GCC 11.3" | "Intel oneAPI 2023.1"
    container: __CONTAINER__               # [if_applicable] e.g., "docker://registry/image:tag"
    hpc_environment: __ENV__               # [if_applicable] e.g., "module load python/3.10 cuda/11.8 openmpi/4.1"
    notes: __NOTES__                        # [if_applicable] Additional environment details, key library versions,
                                            # or reference to a full environment manifest.
                                            # e.g., "See requirements.txt in dataset root"
                                            # e.g., "numpy 1.24, pytorch 2.0.1, h5py 3.8.0"

# --- Stewardship & Versioning -----------------------------------
# NOTE ON VERSIONING: Three fields work together to describe versioning:
#   identification.version        — the version number of this dataset
#   identification.supersedes /
#   identification.superseded_by  — links to prior and successor versions
#   stewardship.versioning_strategy — how versioning is managed over time
stewardship:
  level: __LEVEL__                         # [if_applicable] project_managed | repository_managed | externally_managed
  maintainer:                               # [if_applicable] Person or organization responsible for ongoing maintenance.
    type: __TYPE__                          # person | organization
    person:
      given_name: __GIVEN_NAME__           # [if_applicable]
      family_name: __FAMILY_NAME__         # [if_applicable]
      orcid: __ORCID__                     # [if_applicable]
      email: __EMAIL__                     # [if_applicable]
      affiliation:
        name: __ORG_NAME__                 # [if_applicable]
        ror_id: __ROR_ID__                 # [if_applicable]
    organization:
      name: __ORG_NAME__                   # [if_applicable]
      ror_id: __ROR_ID__                   # [if_applicable]
  update_frequency: __FREQ__              # [if_applicable] none | ad_hoc | monthly | quarterly | annually | other
  retention_policy: __POLICY__            # [if_applicable] e.g., "Retained for 10 years per DOE data management policy"
  versioning_strategy: __STRATEGY__       # [if_applicable] e.g., "Semantic versioning; all versions retained in Zenodo"
                                           # e.g., "Major versions only; prior versions available on request"

# --- Review History ---------------------------------------------
# [if_applicable] Running history of all formal reviews. Add one
# entry per review stage in chronological order. Do not overwrite
# earlier entries when adding new ones.
reviews:
  - stage: __STAGE__                       # [if_applicable] internal_qa | security | export_control | irb | partner | publication | other
    purpose: __PURPOSE__                   # [if_applicable] e.g., "Export control review prior to public release"
    status: __STATUS__                     # [if_applicable] not_started | submitted | pending | approved | declined
    institution:
      name: __NAME__                       # [if_applicable]
      ror_id: __ROR_ID__                   # [if_applicable]
    reviewed_by:                           # [if_applicable] Delete the block that does not apply.
      type: __TYPE__                       # person | organization
      person:
        given_name: __GIVEN_NAME__         # [if_applicable]
        family_name: __FAMILY_NAME__       # [if_applicable]
        email: __EMAIL__                   # [if_applicable]
        ror_id: __ROR_ID__                 # [if_applicable]
      organization:
        name: __ORG_NAME__                 # [if_applicable]
        ror_id: __ROR_ID__                 # [if_applicable]
    review_date: __YYYY-MM-DD__            # [if_applicable]
    approval_document_url: __URL__         # [if_applicable] URL or path to the formal approval letter,
                                           # signed review document, or official review record.
                                           # Particularly important for export control, IRB, and security reviews.
    comments: __COMMENTS__                 # [if_applicable]

# --- Related Resources ------------------------------------------
# [if_applicable] Links to related datasets, publications,
# software, and AI models. The base relationship vocabulary is
# shared across all resource types; extended terms are available
# for software and AI models.
#
# Base vocabulary (all types):
#   is_derived_from | is_based_on | is_part_of | has_part | references | other
# Extended (software and AI models):
#   used_to_create | used_to_process | used_to_analyze | trained_on | evaluated_on
related_resources:
  datasets: []
  # - name: __NAME__
  #   identifier:
  #     type: __TYPE__                     # doi | ark | handle | url | local | other
  #     value: __VALUE__
  #   relationship: __REL__               # see vocabulary above

  publications: []
  # - type: __TYPE__                       # doi | ark | arxiv | url | report | other
  #   value: __VALUE__

  software: []
  # - name: __NAME__
  #   version: __VERSION__
  #   identifier:
  #     type: __TYPE__                     # doi | ark | handle | url | local | other
  #     value: __VALUE__
  #   relationship: __REL__               # see vocabulary above

  ai_models: []
  # - name: __NAME__
  #   version: __VERSION__
  #   date_accessed: __YYYY-MM-DD__
  #   identifier:
  #     type: __TYPE__                     # doi | ark | handle | url | local | other
  #     value: __VALUE__
  #   relationship: __REL__               # see vocabulary above

# --- Compliance -------------------------------------------------
# [extended] Populate when release_status = under_review | approved | published.
# Fields marked [sensitive] are additionally required for the sensitive profile.
# Leave blank or omit for draft and in-workflow datasets.
compliance:
  doe_data_management_plan: __BOOL__       # [extended] true | false — a DOE DMP is on file for this dataset
  osti_elink2_metadata_compliant: __BOOL__ # [extended] true | false — metadata complies with OSTI E-Link 2 API specs
  export_control_reviewed: __BOOL__        # [sensitive] true | false
  irb_approved: __BOOL__                   # [sensitive] true | false | not_applicable
  security_review_completed: __BOOL__      # [sensitive] true | false

# --- Citation ---------------------------------------------------
# [pub] Populate when release_status = approved | published.
# Replace ALL ${...} placeholders in the BibTeX block below before publishing.
citation:
  report_number: __NUMBER__                # [if_applicable] e.g., SAND2024-XXXXX | LAUR-XX-XXXXX | ORNL/TM-2024/XXXXX
  # [pub] Recommended citation in BibTeX format.
  # IMPORTANT: replace every ${...} value below before publishing.
  preferred_citation: |
    @dataset{${DATASET_KEY},
      author    = {${AUTHOR}},
      title     = {${DATASET_NAME}},
      year      = {${YEAR}},
      publisher = {${PUBLISHER}},
      doi       = {${DOI}},
      url       = {${URL}}
    }


# ============================================================
# LEVEL 3 — AI-READY & TRUSTWORTHY     [REQUIRED FOR AI/ML]
# ============================================================
# Required for the ai_ready profile, or for any dataset used
# in AI/ML training, inference, or evaluation workflows, or
# where semantic interoperability and verifiable integrity
# are needed.
# ============================================================

# --- AI / ML Usage ----------------------------------------------
# [ai_ready] Describes whether and how this dataset may be used
# in AI/ML workflows. Be explicit — these fields are read by
# automated pipeline tooling.
ai_usage:
  ai_ready: __BOOL__                       # [ai_ready] true | false | conditional
                                            # true        — suitable for direct use in AI/ML workflows
                                            # false       — should not be used in AI/ML workflows
                                            # conditional — suitable under conditions described in restrictions
  training_use_allowed: __BOOL__           # [ai_ready] true | false | conditional
  inference_use_allowed: __BOOL__          # [ai_ready] true | false | conditional
  evaluation_use_allowed: __BOOL__         # [ai_ready] true | false | conditional
  restrictions: __DESCRIPTION__            # [if_applicable] e.g., "Not for clinical decision-making"
  bias_risks: __DESCRIPTION__              # [if_applicable] e.g., "Overrepresents samples from facility X"
  safety_considerations: __DESC__          # [if_applicable] e.g., "Outputs may be export-controlled"
  human_review_required: __BOOL__          # [ai_ready] true | false

# --- Data Quality -----------------------------------------------
# [ai_ready] Be specific — vague entries reduce trust and reuse.
data_quality:
  completeness: __DESCRIPTION__            # [ai_ready] e.g., "All detector channels present; 2% of timesteps
                                            # missing due to instrument downtime on 2023-04-12"
  known_issues: __DESCRIPTION__            # [ai_ready] e.g., "Sensor drift observed after 2023-06-01T12:00:00Z"
  validation_methods: __DESC__             # [ai_ready] e.g., "Cross-validated against NIST SRM 640f"
  noise_characteristics: __DESC__          # [if_applicable]
  uncertainty_notes: __NOTES__             # [if_applicable] e.g., "Measurement uncertainty ±0.5% (k=2) per ISO/IEC Guide 98-3"
  missing_data_codes: []                   # [if_applicable]
  # - code: __CODE__                       # e.g., -999 | NaN | NULL
  #   description: __DESC__               # e.g., "Sensor malfunction" | "Below detection limit"

# --- Integrity & Fixity -----------------------------------------
# [ai_ready] Checksums enable automated validation of data
# integrity after transfer or storage.
integrity:
  checksum_available: __BOOL__             # [ai_ready] true | false
  checksum_type: __TYPE__                  # [required if checksum_available=true] sha256 | sha512 | md5 | other
                                            # sha256 recommended; md5 not recommended for new datasets
  checksum_value: __VALUE__                # [required if checksum_available=true] Checksum of primary data file(s).
                                            # For multi-file datasets, provide a checksum manifest and link here.
  fixity_policy: __POLICY__               # [if_applicable] e.g., "Monthly sha256 verification via repository integrity service"

# --- Semantic Layer ---------------------------------------------
# [ai_ready] Required for Level 3 datasets intended for
# federated or cross-domain use. Populate schema_url at minimum.
semantic_layer:
  schema_url: __URL__                      # [if_applicable] URL to a formal schema for this dataset.
                                            # e.g., JSON Schema | XML Schema | NeXus application definition
  semantic_context: []                     # [if_applicable] Semantic conventions applied.
                                            # e.g., "NetCDF CF Conventions 1.10" | "NeXus NXmonopd"


# ------------------------------------------------------------
# REPOSITORY-MANAGED
# Populated by the managing repository or catalog system at
# ingest. Do not edit manually. The managing system may be
# institutional, project-owned, community, or national
# (e.g., OSTI, Zenodo, an institutional data repository,
# or a project data store). Fields here are authoritative
# as assigned by that system.
# ------------------------------------------------------------
_repository:
  populated_by_repository: true            # [system] Always true; signals to parsers this block is system-owned
  ingest_date: null                         # [system] ISO 8601 date this datacard was ingested by the managing system
  repository_catalog_id: null              # [system] Identifier assigned to this datacard by the managing catalog
  completeness_score: null                 # [system] Catalog-computed completeness score against the declared profile
  datacard_checksum:                        # [system] Integrity record for this datacard document file
    type: null                              # [system] sha256 | sha512 — checksum algorithm used
    value: null                             # [system] Checksum of the raw datacard .md file as ingested.
                                            # Recomputed on each ingest to detect post-ingest modifications.
  repositories:                             # [system] Resolved repository records keyed to access.intended_repositories
    - name: null                            # [system] Echoed from access.intended_repositories.name
      identifier:
        type: null                          # [system] ror | url | local | other
        value: null                         # [system] Authoritative repository identifier; ROR ID preferred
      dataset_landing_page: null            # [system] Human-readable dataset page assigned by the repository
      dataset_download_url: null            # [system] Direct download URL assigned by the repository
      dataset_id_in_repo: null              # [system] Accession number or ID assigned by this repository
      access_protocol: null                 # [system] https | ftp | s3 | globus | nfs | lustre | other
  usage_metrics:                            # [system] Populated by the managing repository; do not edit
    download_count: null
    view_count: null
    citation_count: null
    last_accessed: null
  distributions: []                         # [system] Distribution records populated at ingest
  data_services: []                         # [system] Data service endpoints populated at ingest

---
### Instructions  
<INSTRUCTIONS: Provide relevant information regarding your dataset in this file.  The information can be a combination of text blocks and values in YAML sections.  For the text, replace all Examples, and [!TODO], and REPLACE: ... placeholder tags with the appropriate information for your dataset. Be sure to remove the header TODO and INSTRUCTION tags once you have completed the datacard.  In each section you can complete YAML values as available.  Required fields are marked.>  
  
<INSTRUCTIONS: Considerations for filling out the datacard: Deciding the appropriate resolution for documenting a scientific dataset in a datacard can be complex. Datacards may describe single or multiple data files, datasets, or versions. Too granular, and there will be too many datacards; too broad, and details may be lost. Consider the datacard's use, audience, and documentation needs to maintain transparency without duplication. Reflect on these relationships to balance clarity, usability, and sustainability.>  
  
<INSTRUCTIONS: The sections and questions in the markdown section of this datacard template are meant to be a guide for the types of information that should be included in a datacard. You can choose to answer all, some, or additional questions as appropriate for your dataset. The goal is to provide enough information for users to understand the dataset and its context, but you can use your judgment to determine what information is most relevant and important to include.>  
  
<INSTRUCTIONS: Data readiness in a shared environment can be generally sorted into three high-level categories:  
Level 1: Discoverable  
Level 2: Interoperable & Reusable (Accessible, reusable, and governed within defined sensitivity, license, and access constraints)  
Level 3: Understandable & Trustworthy (Semantically clear, context-rich, provenance-aware, integrity-supported, and reliable for advanced reuse by humans and machines, including AI workflows)  
Readiness Levels describe usability, interoperability, and governance characteristics.  They do NOT represent dataset quality, scientific merit, or value ranking.  
Prompts for data are generally organized into sections that support these efforts.  Some fields are required to be considered for use at each level and for making datasets available to tools targeting each level.  Requirements are labelled for each level.  
>  
  
<INSTRUCTIONS: metadata_key: [KEY_NAME] tags indicate that the information for the markdown section can be found in the corresponding key in the YAML metadata at the top of this file, and is for use in the human and the automated bi-directional generation from YAML-to-markdown, or markdown-to-YAML. You can choose to either manually copy, or you can leave the placeholders and use an automation tool (such as an LLM) to populate the sections. If you choose to automatically populate the markdown sections from the YAML metadata, make sure to replace metadata_key: [KEY_NAME] tags in each relevant markdown section before sharing the datacard, and note the LLM or aiagent used to do this in the datacard_creation section of the YAML frontmatter metadata.>  
  
  
# Datacard for ${DATASET_NAME}  
**Last Updated**: [!TODO]<REPLACE: YYYY-MM-DD>  
  
**Dataset Readiness Level:** <metadata_key: dataset_readiness.level>  
  
### Machine Usability Snapshot  
| Aspect | Status |  
|--------|--------|  
| AI Ready | Yes/No/Conditional|  
| License Clarity | Yes/No|  
| Machine Access | Yes/No|  
| Checksum / Fixity | Yes/No|  
| Semantic Context | Yes/No|  
  
  
# ---- Level 1: Discoverable ----  
---  
## Identification  
  
  
### Files & Structure  
[!TODO] [required level1] <REPLACE: Summarize dataset organization, formats, and relationships between files.>  
  
---  
## Description  
  
### Dataset Description [required]  
[!TODO] <REPLACE: Provide a concise description of the dataset, including its purpose, scope, and context.><metadata_key: description>  
  
### Keywords [strongly recommended]  
[!TODO] <REPLACE: Provide a comma-separated list of keywords that describe the dataset and can help with discoverability.><metadata_key: description.keywords>  
  
### Citation  
[!TODO] <REPLACE: Provide a recommended citation if known. Recommend bibtex format.><metadata_key: citation.preferred_citation>
  
---  
  
# ---- Level 2: Interoperable and Reusable ----  
  
### Sharing & Access  
[!TODO] <REPLACE:  Describe the sharing methods and any contact information for access.>  
  
### Security / Marking Considerations  
[!TODO]<Describe classification, CUI marking, distribution limitations, and handling requirements.><metadata_key: security.classification> <metadata_key: security.sensitivity_tier> <metadata_key: security.sensitivity_level> <metadata_key: security.cui_marking>
  
---  
### Access and Permissions  
[!TODO] <REPLACE: Describe the dataset`s access posture and any high-level agreements or review constraints. > <metadata_key: access.permissions>
  
### Access conditions  
[!TODO] <REPLACE: Describe any conditions that must be met to access the dataset, such as training requirements, proposal processes, collaboration requirements, data use agreements, etc.><metadata_key: access_policy>  
  
### Release review process  
[!TODO] <REPLACE: Describe the release review process for the dataset, including any institutional reviews, export control reviews, IRB reviews, or other review processes that were conducted before the dataset was released.> <metadata_key: release_status>  
  
---  
## Context  
  
### Domain and Purpose  
[!TODO] <REPLACE: Describe the domain and the key research areas involved in collecting the dataset. Can list below>  
  
### Resources used, including funding and facilities, to create the dataset  
[!TODO] <REPLACE: Provide a list of the resources used to create the dataset, including funding sources, facilities, computing resources, and any other relevant resources. Facilities can include user facilities, national laboratories, research institutions, and other organizations that provided access to equipment, data, or expertise. Funding sources can include government agencies, private foundations, industry partners, and other organizations that provided financial support for the dataset creation. Computing resources can include high-performance computing clusters, cloud computing platforms, and other computational resources used for data processing and analysis. Include [ROR ID](https://ror.org/), grant numbers, contract numbers, or other identifiers as appropriate. Can list below> <metadata_key: facilities> 
  
---  
## Provenance  
  
### Developed by  
[!TODO] <REPLACE: A person or group that was primarily responsible for the creation and design of the dataset. It suggests a leading role, such as a Principal Investigator, in the development of the dataset. If available, provide the Name, [ORCID](https://orcid.org/), affiliation ([ROR ID](https://ror.org/)) and email address of the person or group responsible for the dataset.> <metadata_key: authors> 
  
### Contributed by  
[!TODO] <REPLACE: Person, or group that provided input or support to the datasets development but may not have been the primary creators. Contributions can include sample collection, processing, analysis, documentation, and-or submission of the dataset. This suggests collaboration, where multiple parties might have played various roles in the dataset development. Can list below> <metadata_key: contributors> 
  
---  
## Related Resources  
  
### Related datasets, standards, metadata, and ontologies  
[!TODO] <REPLACE: If the dataset is related to or derived from other datasets, standards, metadata and ontologies, please list those datasets and describe the relationship. For example, This dataset was derived from [DATASET NAME] (DOI: [DATASET DOI]) by applying [TRANSFORMATION OR PROCESS].> <metadata_key: related_resources.related_datasets>  
  
### Related publications  
[!TODO] <REPLACE: List any publications that are associated with the dataset, including DOIs, arXiv IDs, or URLs.> <metadata_key: related_resources.publications>  
  
### Related software  
[!TODO] <REPLACE: List any software that is associated with the dataset, including links or PIDs if available.> <metadata_key: related_resources.software>  

### Related ai model   
[!TODO] <REPLACE: List any AI models that are associated with the dataset, including links or PIDs if available.> <metadata_key: related_resources.aimodels>    

---  
## Methods  
  
### Dataset generation, collection, and procedures  
[!TODO] <REPLACE: Describe how the dataset was generated or collected. For example, raw experimental measurements from user facilities, processed, physics-ready experimental data, outputs from computational simulations, or data derived from prior datasets? For each instrument, facility, or source used to generate and collect the data, what mechanisms or procedures were used for the data collection? If the data was derived, list and describe the source(s) and describe how they were used.>  
  
### Maintenance & Updates  
[!TODO] <REPLACE: Describe update expectations and stewardship responsibility.> <metadata_key: stewardship>
  
  
# ---- Level 3: Understandable & Trustworthy ----  
  
### Data Characteristics  
[!TODO] <REPLACE: Describe variables or features, schema conventions, and missing data handling.><metadata_key: dataset_info.features>  
  
### Data Quality & Limitations  
[!TODO] <REPLACE: Describe completeness, known issues, uncertainties, noise characteristics, and bias considerations.><metadata_key: data_quality>  
  
### Related Schemas or Ontologies  
[!TODO] <REPLACE: list any relevant schemas, ontologies, or vocabularies.><metadata_key: semantic_layer>  
  
### List of variable name(s), description(s), unit(s), and value labels for each variable in the dataset/file.  
[!TODO] <REPLACE: If appropriate, replace the example table with a table listing each variable in the dataset or file, along with its description, unit, and any value labels if applicable.><metadata_key: dataset_info.features>  
  
For example:  
| Variable Name | Description  | Unit  | Value Labels  |  
|---------------|---------------------------|-----------|-----------------------------|  
| temp  | Temperature measurement  | Celsius  | N/A  |  
| status  | Operational status  | N/A  | 0 = Off, 1 = On  |  
  
### Codes used for missing data  
[!TODO] <REPLACE: Replace the example table of codes used to represent missing data in the dataset or file.>  <metadata_key: data_quality.missing_data_codes>
  
For example:  
| Code | Description  |  
|------|---------------------------|  
| -999 | Data not collected  |  
| -888 | Measurement error  |  
  
### Specialized formats or other abbreviations used  
[!TODO] <REPLACE: Describe any specialized data formats, abbreviations, or conventions used in the dataset or file. For example, if the dataset is in a specific file format (e.g., ROOT, HDDM, HDF5), or if there are any domain-specific abbreviations used in variable names or values.>  <metadata_key: dataset_info.formats>
  
### Example of the contents  
[!TODO] <REPLACE: Optional. Provide a sample of the dataset or file, or a citation (in bibtex format) or link to where one can review an example of the contents. This can help users understand the structure and content of the dataset.>  
  
### Data Processing  
[!TODO] <REPLACE: Describe preprocessing, calibration, filtering, labeling, or transformations applied to the dataset.><metadata_key: provenance.processing_steps>  
  
### Software used to preprocess/ clean/ label the data  
[!TODO] <REPLACE: If the software used to preprocess, clean, or label the data is available, please provide a bibtex format, PID, link, or other access point, along with descriptions of any required packages or libraries to run the scripts.> <metadata_key: related_resources.software>  
  
## Integrity & Versioning  
[!TODO] <REPLACE: Describe checksum availability, fixity strategy, and dataset versioning approach.><metadata_key: integrity>  
  
## Semantic / Schema Information  
[!TODO] <REPLACE: Describe schema, ontology alignment, semantic context, and controlled vocabularies. If no formal schema or ontology exists, this section may remain empty.  Examples may include:  JSON Schema or XML schema, NETCDF CF conventions, data dictionary or feature definitions, domain  ontologies like ENVO, controlled vocabularies, or units standards. For example:  schema_URL: "https://example.org/schema.json" or ontology_alignment: "http://purl.obolibrary.org/obo/ENVO_00002005"><metadata_key: semantic_layer>  
  
## AI / Machine Learning Considerations  
[!TODO] <REPLACE: Describe appropriate AI/ML uses, restrictions, bias risks, and safety considerations.><metadata_key: ai_usage>  
  
---  
  
## Additional Information  
[!TODO] <REPLACE: Optional. Include any relevant contextual notes.>  

---