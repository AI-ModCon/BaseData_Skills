---
datacard_creation:
  created_date: "2025-12-01"
  creation_method: "hybrid"
  created_by:
    - person:
        name: "Test User"
        orcid: "0000-0002-1234-5678"
        email: test@example.org
        affiliation:
          name: "Example Org"
          ror_id: "https://ror.org/01qz5mb56"

title: "Example MODCON v1 Dataset"
project: "modcon-legacy"

description: "A synthetic MODCON v1 datacard used as the converter test fixture."

dataset_info:
  modalities: ["tabular"]
  data_formats: ["CSV"]
  features: ["timestamp", "temperature"]
  splits: []

dataset_counts:
  record_count: 3
  record_unit: "rows"

dataset_storage:
  compressed_bytes: 256
  uncompressed_bytes: 256

dataset_readiness:
  level: 2

release_status: "draft"

authors:
  - person:
      name: "Test User"
      orcid: "0000-0002-1234-5678"
      affiliation:
        name: "Example Org"

license:
  spdx_id: "MIT"

sponsor_organizations:
  - name: "Example Funding Agency"

research_organizations:
  - name: "Example Org"

contact:
  type: "person"
  person:
    name: "Test User"
    email: test@example.org
---

# Datacard for Example MODCON v1 Dataset

This is the test fixture.
