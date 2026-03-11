# BaseData Skills

Agentic skills for the ModCon Base Data project. These skills extend coding agent tools (Claude Code, Codex, Goose etc.) with domain-specific workflows for ML dataset metadata and documentation.

## Skills

| Skill | Description |
|-------|-------------|
| [`croissant-validator`](skills/croissant-validator/) | Validate and generate [Croissant](https://mlcommons.org/croissant/) metadata (`croissant.json`) for ML datasets following the MLCommons Croissant 1.0 spec. |
| [`datacard-generator`](skills/datacard-generator/) | Generate MODCON data cards for scientific datasets by introspecting a dataset directory. Supports three readiness levels: Discoverable (L1), Interoperable & Reusable (L2), and Understandable & Trustworthy (L3). |
| [`hdmf-schema-builder`](skills/hdmf-schema-builder/) | Build [HDMF](https://hdmf.readthedocs.io/) (Hierarchical Data Modeling Framework) schema for organizing HDF5 data files for AI training and data sharing |

## Structure

```
skills/
  <skill-name>/
    SKILL.md          # Skill definition loaded by coding agents
    references/       # Supporting templates and reference documents (if any)
```

## Installation

### Claude Code

**Global Installation (Recommended)**

Available in all your projects:

```bash
# Clone the repository
git clone https://github.com/AI-ModCon/BaseData_Skills.git ~/basedata-skills

# Create Claude Code skills directory if needed
mkdir -p ~/.claude/skills

# Symlink all skills
ln -s ~/basedata-skills/skills/* ~/.claude/skills/
```

**Project-Specific Installation**

Only available in a specific project:

```bash
cd /path/to/your/project

# Clone the repository
git clone https://github.com/AI-ModCon/BaseData_Skills.git

# Create project skills directory
mkdir -p .claude/skills

# Symlink the skills
ln -s $(pwd)/basedata-skills/skills/* .claude/skills/
```

### Codex (OpenAI)

**Global Installation (Recommended)**

```bash
# Clone the repository
git clone https://github.com/AI-ModCon/BaseData_Skills.git ~/basedata-skills

# Create Codex skills directory if needed
mkdir -p ~/.codex/skills

# Symlink all skills
ln -s ~/basedata-skills/skills/* ~/.codex/skills/
```

**Project-Specific Installation**

```bash
cd /path/to/your/project

# Clone the repository
git clone https://github.com/AI-ModCon/BaseData_Skills.git

# Create project skills directory
mkdir -p .agents/skills

# Symlink the skills
ln -s $(pwd)/basedata-skills/skills/* .agents/skills/
```

### Goose

**Global Installation (Recommended)**

```bash
# Clone the repository
git clone https://github.com/AI-ModCon/BaseData_Skills.git ~/basedata-skills

# Create agent-portable skills directory
mkdir -p ~/.config/agents/skills

# Symlink all skills
ln -s ~/basedata-skills/skills/* ~/.config/agents/skills/
```

**Project-Specific Installation**

```bash
cd /path/to/your/project

# Clone the repository
git clone https://github.com/AI-ModCon/BaseData_Skills.git

# Create project skills directory
mkdir -p .agents/skills

# Symlink the skills
ln -s $(pwd)/basedata-skills/skills/* .agents/skills/
```

### Quick Start (One-Command Install)

| Tool | Command |
|------|---------|
| **Claude Code** | `git clone https://github.com/AI-ModCon/BaseData_Skills.git ~/basedata-skills && mkdir -p ~/.claude/skills && ln -s ~/basedata-skills/skills/* ~/.claude/skills/` |
| **Codex** | `git clone https://github.com/AI-ModCon/BaseData_Skills.git ~/basedata-skills && mkdir -p ~/.codex/skills && ln -s ~/basedata-skills/skills/* ~/.codex/skills/` |
| **Goose** | `git clone https://github.com/AI-ModCon/BaseData_Skills.git ~/basedata-skills && mkdir -p ~/.config/agents/skills && ln -s ~/basedata-skills/skills/* ~/.config/agents/skills/` |

### Installation Locations

| Tool | Global Location | Project Location |
|------|----------------|------------------|
| **Claude Code** | `~/.claude/skills/` | `.claude/skills/` |
| **Codex** | `~/.codex/skills/` | `.agents/skills/` |
| **Goose** | `~/.config/agents/skills/` | `.agents/skills/` |

## Usage

Skills are automatically available in coding agent sessions when this repo is configured as a skills source. Invoke them by describing your task — the agent will select the appropriate skill — or reference them explicitly (e.g., "use the datacard-generator skill").

### Examples

**Claude Code:**
```bash
claude code

# Auto-trigger based on context
"Generate a datacard for my dataset in ./data/"

# Explicit invocation
"Use the datacard-generator skill to create a Level 3 datacard"
```

**Codex:**
```bash
codex

# Describe your task
"Validate the croissant.json file in this directory"

# Reference the skill directly
"Using croissant-validator, check my Croissant metadata"
```

**Goose:**
```bash
goose

# Simple description
"I need an HDMF schema for this HDF5 dataset"

# The agent will detect and use the appropriate skill
```

## Updating Skills

To get the latest version of all skills:

```bash
# Navigate to your cloned repository
cd ~/basedata-skills  # or wherever you cloned it

# Pull the latest changes
git pull

# The symlinks ensure all tools automatically get the updates
```

## Troubleshooting

### Skills Not Detected?

1. **Verify the symlinks:**
   ```bash
   ls -la ~/.claude/skills/
   # Should show symlinks to your skills
   ```

2. **Check that SKILL.md files exist:**
   ```bash
   cat ~/.claude/skills/datacard-generator/SKILL.md
   # Should display the skill definition
   ```

3. **Restart your tool** (especially important for Codex)

### References Folder Not Accessible?

Ensure you symlinked the entire skill folders (not just `SKILL.md` files):

```bash
# Correct structure after symlinking:
~/.claude/skills/datacard-generator/
  ├── SKILL.md
  └── references/
```

### Alternative: Copy Instead of Symlink

If symlinks don't work on your system:

```bash
# For Claude Code
git clone https://github.com/AI-ModCon/BaseData_Skills.git ~/basedata-skills
mkdir -p ~/.claude/skills
cp -r ~/basedata-skills/skills/* ~/.claude/skills/

# To update, manually copy again
cp -r ~/basedata-skills/skills/* ~/.claude/skills/
```
