---
name: croissant-validator
description: Validates and generates Croissant metadata for ML datasets. Use when checking dataset metadata compliance, creating new croissant.json files, validating existing metadata, or ensuring ML dataset descriptions follow the MLCommons Croissant format specification.
allowed-tools: Read, Bash, Write, Glob, Grep
---

# Croissant Metadata Validator & Generator

This skill helps validate and generate proper Croissant metadata for ML datasets. Croissant is a metadata format developed by MLCommons for describing machine learning datasets.

## What is Croissant?

Croissant is a metadata format for ML-ready datasets that extends schema.org. It consists of four layers:

1. **Dataset Metadata Layer**: Name, description, version, license, creators
2. **Resource Layer**: Source data files (FileObject/FileSet)
3. **Structure Layer**: RecordSets and Fields describing data organization
4. **Semantic Layer**: ML-specific semantics and interpretations

## Virtual Environment for Python Execution

**CRITICAL**: When running ANY Python code that requires package installation (mlcroissant, pandas, etc.), you MUST use a temporary virtual environment to avoid polluting the user's global Python environment.

### Steps for Using Virtual Environments:

1. **Create a virtual environment in the current directory**:
   ```bash
   python3 -m venv .venv_croissant
   ```

2. **Install required packages**:
   ```bash
   .venv_croissant/bin/pip install -q mlcroissant pandas
   ```

3. **Run your Python code using the venv's Python**:
   ```bash
   .venv_croissant/bin/python script.py
   # OR for inline code:
   .venv_croissant/bin/python -c "import mlcroissant as mlc; ..."
   ```

4. **Clean up the venv after use**:
   ```bash
   rm -rf .venv_croissant
   ```

### All-in-One Command Pattern:

Combine all steps into a single bash command for efficiency:

```bash
python3 -m venv .venv_croissant && \
.venv_croissant/bin/pip install -q mlcroissant && \
.venv_croissant/bin/python -c "
import mlcroissant as mlc
# Your validation code here
" && \
rm -rf .venv_croissant
```

### Example: Validating with mlcroissant

```bash
python3 -m venv .venv_croissant && \
.venv_croissant/bin/pip install -q mlcroissant && \
.venv_croissant/bin/python -c "
import mlcroissant as mlc
import sys

try:
    dataset = mlc.Dataset('croissant.json')
    print('✓ Valid Croissant metadata')
    print(f'Dataset: {dataset.metadata.name}')
    sys.exit(0)
except Exception as e:
    print(f'✗ Validation failed: {e}')
    sys.exit(1)
" && \
rm -rf .venv_croissant
```

### Example: Generating metadata from CSV

```bash
python3 -m venv .venv_croissant && \
.venv_croissant/bin/pip install -q pandas && \
.venv_croissant/bin/python -c "
import pandas as pd
import json
from datetime import date

df = pd.read_csv('data.csv', nrows=5)
# Generate metadata...
print(f'Analyzed {len(df.columns)} columns')
" && \
rm -rf .venv_croissant
```

**Important Notes**:
- NEVER use `pip install` without a virtual environment
- NEVER assume packages are installed globally
- Use `.venv_croissant` as the venv directory name (in current working directory)
- The `-q` flag on pip makes installation quieter
- Always clean up the venv after use with `rm -rf .venv_croissant`
- The venv approach works on all platforms (macOS, Linux, Windows with WSL)

## Validation Process

When validating Croissant metadata, follow these steps:

### 1. Check File Existence

Look for metadata files commonly named:
- `croissant.json`
- `metadata.json`
- `croissant-metadata.json`

### 2. Validate Required Fields

Every valid Croissant file MUST include:

```json
{
  "@context": "...",
  "@type": "sc:Dataset",
  "conformsTo": "http://mlcommons.org/croissant/1.0",
  "name": "Dataset name",
  "description": "Dataset description",
  "license": "License URL (e.g., SPDX)",
  "url": "Dataset URL",
  "creator": { ... },
  "datePublished": "YYYY-MM-DD",
  "distribution": [ ... ]
}
```

### 3. Check Recommended Fields

Best practices include:
- `keywords`: For discoverability
- `publisher`: If different from creator
- `version`: Semantic versioning (MAJOR.MINOR.PATCH)
- `dateCreated` and `dateModified`
- `inLanguage`: Content language

### 4. Validate Structure

- **RecordSets**: Must define data structure
- **Fields**: Must reference sources with proper `dataType`
- **IDs**: All `@id` values must be unique
- **FileObjects**: Must have `contentUrl` and `encodingFormat`

### 5. Use the Official Validator

Use the official Python library via a temporary virtual environment:

```bash
python3 -m venv .venv_croissant && \
.venv_croissant/bin/pip install -q mlcroissant && \
.venv_croissant/bin/python -c "
import mlcroissant as mlc

# Load and validate metadata
try:
    dataset = mlc.Dataset('path/to/croissant.json')
    print('✓ Valid Croissant metadata')

    # Inspect metadata
    metadata = dataset.metadata.to_json()
    print(f'Dataset: {dataset.metadata.name}')

except Exception as e:
    print(f'✗ Validation failed: {e}')
" && \
rm -rf .venv_croissant
```

### 6. Report Findings

Create a clear validation report that includes:

1. **File Location**: Path to metadata file
2. **Conformance Status**: Pass/Fail
3. **Required Fields**: Check all mandatory fields
4. **Recommended Fields**: Note missing best-practice fields
5. **Structural Issues**: ID conflicts, missing references, type mismatches
6. **Suggestions**: How to fix any issues found

## Common Issues to Check

- Missing `conformsTo` field (required for v1.0+)
- Invalid license URLs (should use SPDX)
- Duplicate `@id` values
- Fields without proper `source` references
- RecordSets without Fields
- Missing `encodingFormat` in FileObjects
- Incorrect date formats (should be ISO 8601)

## Example Validation Script

Always run validation scripts in a virtual environment:

```bash
python3 -m venv .venv_croissant && \
.venv_croissant/bin/pip install -q mlcroissant && \
.venv_croissant/bin/python -c "
import json
import mlcroissant as mlc
import sys

filepath = 'croissant.json'

# Check file exists and load
with open(filepath, 'r') as f:
    metadata = json.load(f)

# Required fields
required = [
    '@context', '@type', 'conformsTo', 'name',
    'description', 'license', 'url', 'creator',
    'datePublished', 'distribution'
]

missing = [field for field in required if field not in metadata]

if missing:
    print(f\"✗ Missing required fields: {', '.join(missing)}\")
    sys.exit(1)

# Validate with mlcroissant
try:
    dataset = mlc.Dataset(filepath)
    print(f'✓ Valid Croissant metadata for: {dataset.metadata.name}')
    sys.exit(0)
except Exception as e:
    print(f'✗ Validation error: {e}')
    sys.exit(1)
" && \
rm -rf .venv_croissant
```

## Resources

- Specification: https://docs.mlcommons.org/croissant/docs/croissant-spec.html
- GitHub: https://github.com/mlcommons/croissant
- Python Library: `mlcroissant` (requires Python 3.10+, use in venv as shown above)
- Official Release: http://mlcommons.org/croissant/1.0

**Remember**: Always use `.venv_croissant` virtual environment for any Python code execution that requires packages!

## Generating Croissant Metadata

When creating new metadata for a dataset, follow these steps:

### 1. Gather Dataset Information

Ask the user or inspect the dataset to collect:
- **Basic Info**: Name, description, purpose
- **Attribution**: Creators, publisher, license
- **Dates**: When created, published, modified
- **Data Files**: File paths, formats, sizes
- **Structure**: Column names, data types, relationships

### 2. Inspect Data Files

For CSV/tabular data:
- Read file headers to get column names
- Infer data types (text, integer, float, boolean, date)
- Note any special columns (IDs, labels, features)

For other formats:
- Identify file type and encoding
- Understand the data schema

### 3. Create Standard @context

**CRITICAL**: Always use the COMPLETE standard context from the official specification to avoid validation warnings:

```json
{
  "@context": {
    "@language": "en",
    "@vocab": "https://schema.org/",
    "citeAs": "cr:citeAs",
    "column": "cr:column",
    "conformsTo": "dct:conformsTo",
    "cr": "http://mlcommons.org/croissant/",
    "rai": "http://mlcommons.org/croissant/RAI/",
    "data": {"@id": "cr:data", "@type": "@json"},
    "dataType": {"@id": "cr:dataType", "@type": "@vocab"},
    "dct": "http://purl.org/dc/terms/",
    "examples": {"@id": "cr:examples", "@type": "@json"},
    "extract": "cr:extract",
    "field": "cr:field",
    "fileProperty": "cr:fileProperty",
    "fileObject": "cr:fileObject",
    "fileSet": "cr:fileSet",
    "format": "cr:format",
    "includes": "cr:includes",
    "isLiveDataset": "cr:isLiveDataset",
    "jsonPath": "cr:jsonPath",
    "key": "cr:key",
    "md5": "cr:md5",
    "parentField": "cr:parentField",
    "path": "cr:path",
    "recordSet": "cr:recordSet",
    "references": "cr:references",
    "regex": "cr:regex",
    "repeated": "cr:repeated",
    "replace": "cr:replace",
    "samplingRate": "cr:samplingRate",
    "sc": "https://schema.org/",
    "separator": "cr:separator",
    "source": "cr:source",
    "subField": "cr:subField",
    "transform": "cr:transform"
  }
}
```

**Important notes**:
- Include ALL properties even if not using them (this prevents validation warnings)
- Notable properties: `fileProperty`, `samplingRate` are often forgotten
- Never modify or omit properties from the standard context

### 4. Map Data Types

Use appropriate schema.org data types:
- **Text/String**: `sc:Text`
- **Integer**: `sc:Integer`
- **Float/Decimal**: `sc:Float`
- **Boolean**: `sc:Boolean`
- **Date**: `sc:Date`
- **DateTime**: `sc:DateTime`
- **URL**: `sc:URL`

### 5. Generate Complete Metadata

Create a complete croissant.json with all required and recommended fields:

```json
{
  "@context": { /* COMPLETE standard context from above */ },
  "@type": "sc:Dataset",
  "conformsTo": "http://mlcommons.org/croissant/1.0",
  "name": "Dataset Name",
  "description": "Detailed dataset description",
  "license": "https://spdx.org/licenses/LICENSE-ID.html",
  "url": "https://dataset-url.com",
  "citeAs": "@misc{dataset-name-2024, title={Dataset Name}, author={Creator}, year={2024}}",
  "creator": {
    "@type": "Person",
    "name": "Creator Name",
    "email": "creator@example.com"
  },
  "datePublished": "YYYY-MM-DD",
  "version": "1.0.0",
  "keywords": ["keyword1", "keyword2"],
  "distribution": [
    {
      "@type": "cr:FileObject",
      "@id": "file-id",
      "name": "filename.csv",
      "contentUrl": "path/to/file.csv",
      "encodingFormat": "text/csv",
      "sha256": "REQUIRED_SHA256_CHECKSUM_HERE"
    }
  ],
  "recordSet": [
    {
      "@type": "cr:RecordSet",
      "@id": "records",
      "name": "records",
      "field": [
        {
          "@type": "cr:Field",
          "@id": "records/column_name",
          "name": "column_name",
          "description": "Column description",
          "dataType": "sc:Text",
          "source": {
            "fileObject": {"@id": "file-id"},
            "extract": {"column": "column_name"}
          }
        }
      ]
    }
  ]
}
```

**CRITICAL REQUIREMENTS for validation to pass**:

1. **FileObject checksums**: EVERY `cr:FileObject` MUST have either `sha256` or `md5` checksum
   - Calculate with: `shasum -a 256 filename` or `sha256sum filename`
   - This is NOT optional - validation will fail without it

2. **Dataset name**: Avoid special characters like hyphens in the middle
   - ✅ Good: "Dataset Name", "DatasetName", "My Dataset"
   - ❌ Bad: "Dataset-Name", "My-Special-Dataset"

3. **citeAs property**: Include a citation string (recommended to avoid warnings)
   - Can be BibTeX, plain text, or any citation format

4. **FileSets without archives**: If using FileSets for local directories (not tar/zip):
   - DON'T use `containedIn` pointing to directories
   - Just use `includes` with the full path pattern
   - Example: `"includes": "data/images/**/*.jpg"`

5. **FileSets with archives**: If files are inside tar/zip:
   - Create a FileObject for the archive with sha256
   - Use `containedIn` to reference the archive FileObject
   - Example:
     ```json
     {
       "@type": "cr:FileObject",
       "@id": "archive",
       "name": "data.tar.gz",
       "contentUrl": "data.tar.gz",
       "encodingFormat": "application/x-tar",
       "sha256": "checksum-here"
     },
     {
       "@type": "cr:FileSet",
       "@id": "images",
       "containedIn": {"@id": "archive"},
       "includes": "images/**/*.jpg"
     }
     ```

### 6. Validation Checklist

Before finalizing any generated croissant.json, verify:

- [ ] Complete @context with ALL standard properties (including `fileProperty`, `samplingRate`)
- [ ] Dataset name has no special characters (hyphens, underscores at start/end)
- [ ] `citeAs` property is included
- [ ] EVERY FileObject has `sha256` or `md5` checksum
- [ ] FileSets use `containedIn` ONLY when referencing archive FileObjects
- [ ] All `@id` values are unique
- [ ] `conformsTo` points to `http://mlcommons.org/croissant/1.0`
- [ ] License uses SPDX URLs (https://spdx.org/licenses/...)
- [ ] RecordSet fields properly reference FileObjects or FileSets
- [ ] Extract uses valid properties: `column`, `jsonPath`, or `fileProperty`

**ALWAYS validate with mlcroissant before delivering**:
```bash
python3 -m venv .venv_croissant && \
.venv_croissant/bin/pip install -q mlcroissant && \
.venv_croissant/bin/python -c "
import mlcroissant as mlc
dataset = mlc.Dataset('croissant.json')
print('✅ Valid!')
" && \
rm -rf .venv_croissant
```

### 7. Interactive Generation

When generating metadata interactively:
1. Ask user for basic info if not provided
2. Scan data files to discover structure
3. Calculate sha256 checksums for all FileObjects
4. Generate complete metadata with full @context
5. Validate the generated file with mlcroissant
6. Fix any validation errors
7. Offer to save as `croissant.json`

### 8. License Selection

Common SPDX license URLs:
- MIT: `https://spdx.org/licenses/MIT.html`
- Apache 2.0: `https://spdx.org/licenses/Apache-2.0.html`
- CC-BY-4.0: `https://spdx.org/licenses/CC-BY-4.0.html`
- CC0-1.0: `https://spdx.org/licenses/CC0-1.0.html`
- GPL-3.0: `https://spdx.org/licenses/GPL-3.0.html`

## Generation Example Script

When generating metadata from CSV files, create a Python script and run it in a venv:

**Step 1**: Create the generation script (`generate_metadata.py`):

```python
import json
import pandas as pd
from datetime import date
import sys

csv_path = sys.argv[1]
name = sys.argv[2]
description = sys.argv[3]
license_url = sys.argv[4]
creator_name = sys.argv[5]
url = sys.argv[6]

# Read CSV to get structure
df = pd.read_csv(csv_path, nrows=5)

# Map pandas dtypes to schema.org types
dtype_map = {
    'int64': 'sc:Integer',
    'float64': 'sc:Float',
    'object': 'sc:Text',
    'bool': 'sc:Boolean'
}

# Create fields for each column
fields = []
for col in df.columns:
    dtype_str = str(df[col].dtype)
    data_type = dtype_map.get(dtype_str, 'sc:Text')

    fields.append({
        "@type": "cr:Field",
        "@id": f"records/{col}",
        "name": col,
        "description": f"The {col} column",
        "dataType": data_type,
        "source": {
            "fileObject": {"@id": "data-file"},
            "extract": {"column": col}
        }
    })

# Build complete metadata (context object here)
metadata = {
    "@context": {
        "@language": "en",
        "@vocab": "https://schema.org/",
        "cr": "http://mlcommons.org/croissant/",
        # ... (full context as shown earlier)
    },
    "@type": "sc:Dataset",
    "conformsTo": "http://mlcommons.org/croissant/1.0",
    "name": name,
    "description": description,
    "license": license_url,
    "url": url,
    "creator": {"@type": "Person", "name": creator_name},
    "datePublished": str(date.today()),
    "version": "1.0.0",
    "distribution": [{
        "@type": "cr:FileObject",
        "@id": "data-file",
        "name": csv_path.split('/')[-1],
        "contentUrl": csv_path,
        "encodingFormat": "text/csv"
    }],
    "recordSet": [{
        "@type": "cr:RecordSet",
        "@id": "records",
        "name": "records",
        "field": fields
    }]
}

# Write to file
with open("croissant.json", 'w') as f:
    json.dump(metadata, f, indent=2)

print(f"✓ Generated Croissant metadata: croissant.json")
```

**Step 2**: Run the script in a venv:

```bash
python3 -m venv .venv_croissant && \
.venv_croissant/bin/pip install -q pandas && \
.venv_croissant/bin/python generate_metadata.py \
    "data.csv" \
    "My Dataset" \
    "Description here" \
    "https://spdx.org/licenses/MIT.html" \
    "Creator Name" \
    "https://example.com/dataset" && \
rm -rf .venv_croissant
```

**Alternative**: For simple inline generation without pandas:

```bash
python3 -c "
import json
from datetime import date

# Manually define metadata without reading CSV
metadata = {
    '@context': {...},  # Full context
    '@type': 'sc:Dataset',
    'conformsTo': 'http://mlcommons.org/croissant/1.0',
    # ... rest of metadata
}

with open('croissant.json', 'w') as f:
    json.dump(metadata, f, indent=2)

print('✓ Generated croissant.json')
"
```

## When to Use This Skill

Invoke this skill when:
- User asks to "validate croissant metadata"
- User asks to "create croissant metadata" or "generate croissant.json"
- User mentions "check dataset metadata" in ML context
- User wants to ensure compliance with MLCommons standards
- User is preparing datasets for Kaggle, Hugging Face, or OpenML
- User asks about "croissant.json" files
- User wants to add metadata to an existing dataset
