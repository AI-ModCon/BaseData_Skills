# BaseData Skills

Agentic skills for the ModCon Base Data project. These skills extend coding agent tools (Claude Code, Codex, Goose etc.) with domain-specific workflows for ML dataset metadata and documentation.

## Skills

| Skill | Description |
|-------|-------------|
| [`croissant-validator`](skills/croissant-validator/) | Validate and generate [Croissant](https://mlcommons.org/croissant/) metadata (`croissant.json`) for ML datasets following the MLCommons Croissant 1.0 spec. |
| [`datacard-generator`](skills/datacard-generator/) | Generate MODCON data cards for scientific datasets by introspecting a dataset directory. Supports three readiness levels: Discoverable (L1), Interoperable & Reusable (L2), and Understandable & Trustworthy (L3). |
| [`hdmf-schema-builder`](skills/hdmf-schema-builder/) | Design [HDMF](https://hdmf.readthedocs.io/) (Hierarchical Data Modeling Framework) schemas for organizing scientific data in HDF5 format. Conducts an interactive interview to propose schemas, generate implementation code, and integrate with DSAGT pipelines. |

## Structure

```
skills/
  <skill-name>/
    SKILL.md          # Skill definition loaded by Claude Code
    references/       # Supporting templates and reference documents (if any)
```

## Usage

Skills are automatically available in Claude Code sessions when this repo is configured as a skills source. Invoke them by describing your task — Claude will select the appropriate skill — or reference them explicitly (e.g., "use the datacard-generator skill").
