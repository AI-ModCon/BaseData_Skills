---
datacard:
  template_version: "0.1"
  datacard_version: "1.0"
  profile: core
  filename: "genesis_datacard_test_core_dataset.md"
  language: en
  sensitivity_tier: tier0_open
  access_level: open
  creation_method: hybrid
  created_date: "2026-05-26"
  updated_date: "2026-05-26"
  change_log:
    - date: "2026-05-26"
      datacard_version: "1.0"
      summary: "Initial creation"
  created_by:
    - role: initial_creation
      date: "2026-05-26"
      creator:
        type: ai_model
        ai_model:
          name: "Claude Opus 4.7"
          version: "4.7"
          date_accessed: "2026-05-26"
          identifier:
            type: url
            value: "https://www.anthropic.com/news/claude-4-7"

identification:
  project: "genesis"
  version: "1.0"
  primary_id:
    type: local
    value: "test_core_dataset_v1"

description:
  summary: "Synthetic dataset for validator testing — core profile fixture."
  keywords:
    - testing
    - validator
    - fixture

object_type: dataset
dataset_type: ND
release_status: draft

workflow:
  state: raw

security:
  classification: U
  sensitivity_tier: tier0_open
  export_control: none

access_policy:
  sensitivity_tier: tier0_open
  access_level: open
  authorization_required: none

contact:
  type: person
  person:
    given_name: Test
    family_name: User
    email: test@example.org
    affiliation:
      name: "Example Org"

categorization:
  science_domain: "computer_science"

dataset_info:
  formats: ["CSV"]

provenance:
  was_generated_by: "Hand-built fixture for validator testing"

sponsor_organizations:
  - name: "Example Funding Agency"

research_organizations:
  - name: "Example Org"
---

# Datacard for Test Core Dataset
