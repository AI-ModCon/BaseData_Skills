# Lookup tables

Reference tables for fixed-vocabulary fields in Genesis Mission Datacard
v1.0. Same data as the `enums` block in `validation-rules.md`, formatted
for human reading.

## OSTI dataset type codes

| Code | Type | Description |
|------|------|-------------|
| GD | Genome/Genetic Data | DNA/RNA sequences, genomic annotations |
| IM | Image | Photographs, scans, microscopy, visualizations |
| ND | Numeric Data | Measurements, time series, tabular, sensor readings |
| SM | Specialized Mix | Multiple data types combined |
| FP | Figure/Plot | Charts, graphs, plots as primary deliverable |
| I  | Interactive Resource | Web apps, interactive visualizations, dashboards |
| MM | Multimedia | Audio, video, combined media |
| MD | Model | Computational models, simulations, trained ML models |
| AS | Automated Software | Scripts, analysis pipelines, workflows |
| IP | Instrumentation/Protocols | Experimental protocols, instrument specs |
| IG | Integrated Genomic Resources | Combined genomic databases and tools |

## Sensitivity tiers

Applies to BOTH `datacard.sensitivity_tier` (the document) and
`security.sensitivity_tier` (the data). These two fields are set
independently and often differ.

| Tier | Meaning |
|------|---------|
| tier0_open | No restrictions; publicly shareable |
| tier1_controlled_research | Internal research use; limited sharing |
| tier2_proprietary | Proprietary; internal use only |
| tier3_sensitive | Sensitive; access controls required |
| tier4_export_controlled | Subject to EAR or ITAR restrictions |
| tier5_regulated_personal | Contains PII or regulated personal data |
| tier6_classified | Formally classified; handle per classification guide |

## Classifications

| Code | Meaning |
|------|---------|
| U   | Unclassified |
| CUI | Controlled Unclassified Information |
| C   | Confidential |
| S   | Secret |
| TS  | Top Secret |

When `classification = CUI`, also fill `security.cui_marking` (e.g.,
`CUI//SP-PRVCY` for PII, `CUI//SP-PROPIN` for proprietary, `CUI//SP-EXPT`
for export-controlled). Registry: https://www.archives.gov/cui

## Workflow states

| State | Meaning |
|-------|---------|
| raw | Data as collected; no processing |
| processing | Cleaning, transforming, reducing |
| qa | Quality assurance / validation |
| analysis | Active scientific analysis |
| review | Formal review (security, export, IRB) |
| embargo | Complete but intentionally withheld |
| published | Publicly released |
| archived | Preserved; no longer actively maintained |

## Release statuses

| Status | Meaning |
|--------|---------|
| draft | Work in progress; not ready for sharing |
| under_review | Submitted for formal review |
| approved | Review complete; cleared for release |
| published | Publicly released and accessible |
| deprecated | Superseded or retired |

Typical workflow ↔ release alignment (warning, not error):
- raw / processing / qa / analysis → draft
- review → under_review
- embargo / published → approved or published
- archived → deprecated or published

## Authorization required

| Value | Meaning |
|-------|---------|
| none | No authorization required |
| account | Registered account required |
| user_agreement | User agreement / terms of service |
| data_use_agreement | Formal DUA required |
| sponsor_approval | Sponsor or PI approval required |
| export_control_review | Export control review required |
| irb_approval | IRB approval required |
| other | Describe in access_restrictions |

## SPDX licenses (quick reference)

Use the full SPDX registry (https://spdx.org/licenses/) for canonical
identifiers. Common choices in Genesis datacards:

| spdx_id | Name |
|---------|------|
| CC0-1.0 | Creative Commons Zero |
| CC-BY-4.0 | Creative Commons Attribution 4.0 |
| CC-BY-SA-4.0 | CC Attribution-ShareAlike 4.0 |
| MIT | MIT License |
| Apache-2.0 | Apache License 2.0 |
| BSD-3-Clause | BSD 3-Clause |
| other | Custom — also fill `license.name` |
| pending | License not yet assigned |
