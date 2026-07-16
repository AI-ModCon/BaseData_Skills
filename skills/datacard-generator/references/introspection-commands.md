# Introspection commands

Reference for auto-filling Genesis Mission Datacard v1.2 fields by
inspecting a dataset directory. The script `scripts/introspect.py` does
the common work; this doc covers (1) the script's JSON output and how it
maps to datacard fields, (2) commands for formats the script doesn't
touch, and (3) advanced patterns the agent should run manually.

---

## 1. `introspect.py` — bulk inspection (use this first)

```bash
python3 scripts/introspect.py <dataset_dir>
```

Emits JSON to stdout. Stdlib-only; cross-platform (Windows, macOS, Linux).

### JSON output schema → datacard field mapping

| JSON key | Type | Maps to (Genesis field) | Notes |
|---|---|---|---|
| `path` | string | — | Echoed for confirmation; not a datacard field |
| `file_count` | int | `accessibility.dataset_scale.record_count` (when file-based) | Use `record_unit: files` |
| `total_bytes` | int | `accessibility.dataset_scale.compressed_bytes` (use as-is for stored size) | The script does not distinguish compressed vs uncompressed — see § 4 for that |
| `formats` | list of strings | `interoperability.data_structure.formats` | Recognized extensions (CSV/HDF5/Parquet/NetCDF4/TIFF/PNG/JPEG/Text/Markdown/NumPy/Pickle/PyTorch/JSON/YAML/Arrow/TSV) |
| `sample_columns` | dict (filename → list of strings) | `interoperability.data_structure.features` (flat form) | First-row column names from up to 3 CSVs |
| `readme_file` | string path | (use to extract `description.summary`, `description.keywords`) | First `README*` at depth ≤ 2 |
| `license_file_present` | bool | (gates `license.spdx_id` prompt) | True if any `LICENSE*` or `COPYING*` at depth ≤ 2 |
| `license_hint` | string | (use to guess `license.spdx_id`) | First 5 non-empty lines of the license file, joined; max 200 chars |
| `citation_file` | string path | (use to extract `authors[]`, `citation.preferred_citation`) | First `CITATION*` at depth ≤ 2 |
| `splits_detected` | list of strings | `interoperability.data_structure.splits` | Subdirs named train/test/val/validation at depth ≤ 3 |

### What introspect.py does NOT cover

- HDF5/Parquet/NetCDF internal schema (use § 2 manually)
- NumPy/PyTorch/Arrow/Image file inspection (use § 2 manually)
- Checksums (use § 3.1)
- CITATION.cff parsing (use § 3.2)
- README summary/keyword extraction (use § 3.3)
- LICENSE → SPDX ID matching (use § 3.4)
- Modality inference (use § 3.5)
- Encoding detection (use § 3.6)
- Splits detection from filenames (only subdirs are detected — use § 3.7)
- Uncompressed-size measurement for compressed archives (use § 4)

---

## 2. Per-format schema extraction (manual)

Run these when the script's `sample_columns` isn't enough or the format isn't CSV.

### CSV / TSV

```bash
head -n 1 "$FILE" | tr ',' '\n'    # column names (CSV)
head -n 1 "$FILE" | tr '\t' '\n'   # column names (TSV)
head -n 5 "$FILE"                  # sample rows for type inference
wc -l "$FILE"                      # row count (record_count for tabular)
```

Maps to: `interoperability.data_structure.features` (flat list by default; when `supports_ai_usability=Yes` use the structured form — see § 3.8).

### HDF5

```bash
h5ls -r "$FILE"                    # recursive group/dataset listing
h5dump -H "$FILE"                  # header (datatypes, dimensions, attributes)
h5dump -A -o /dev/null "$FILE" | head -200   # attributes summary
```

Maps to: `interoperability.data_structure.features` (dataset names), `interoperability.data_structure.spatial_coverage` / `temporal_coverage` if dimensions hint at them, `semantic_layer.schema_url` (if attributes reference a schema).

If h5tools aren't installed, use Python:

```bash
python3 -c "import h5py; f=h5py.File('$FILE','r'); f.visit(print)"
```

### Parquet

```bash
parquet-tools schema "$FILE"       # columns + types
parquet-tools meta "$FILE"         # row count, compression, etc.
```

Or via Python (pyarrow):

```bash
python3 -c "import pyarrow.parquet as pq; t=pq.read_table('$FILE'); print(t.schema)"
```

Maps to: `interoperability.data_structure.features` (structured — name + type + nullable).

### NetCDF

```bash
ncdump -h "$FILE"                  # header (variables, dimensions, global attributes)
ncdump -v <var> "$FILE" | head -50 # sample values for a variable
```

Or via Python (netCDF4):

```bash
python3 -c "import netCDF4 as nc; ds=nc.Dataset('$FILE'); print(ds.variables.keys()); print(ds.dimensions)"
```

Maps to: `interoperability.data_structure.features` (variable names), `interoperability.data_structure.spatial_coverage` (lat/lon bounding box from coordinate variables), `interoperability.data_structure.temporal_coverage` (time variable bounds), `semantic_layer.semantic_context` (CF conventions if `Conventions` global attribute is present).

### JSON / YAML

```bash
head -n 50 "$FILE"                              # eyeball structure
python3 -c "import json; print(list(json.load(open('$FILE')).keys()))"
python3 -c "import yaml; print(list(yaml.safe_load(open('$FILE')).keys()))"
```

Maps to: `interoperability.data_structure.features` (top-level keys), `interoperability.data_structure.schema_version` (if a `version` or `schema_version` key is present).

### NumPy (`.npy`, `.npz`)

```bash
python3 -c "import numpy as np; a=np.load('$FILE'); print(a.shape, a.dtype)"
python3 -c "import numpy as np; z=np.load('$FILE'); print(z.files)"   # for .npz archives
```

Maps to: `interoperability.data_structure.features` (array name for .npz, single-array shape for .npy), `accessibility.dataset_scale.record_count` (first dim of array).

### PyTorch (`.pt`, `.pth`)

```bash
python3 -c "import torch; obj=torch.load('$FILE', map_location='cpu'); print(type(obj)); print(list(obj.keys()) if isinstance(obj, dict) else None)"
```

Maps to: `object_type: model` likely; the file is usually a state_dict for a model rather than data.

### Apache Arrow (`.arrow`, `.feather`)

```bash
python3 -c "import pyarrow as pa, pyarrow.ipc as ipc; r=ipc.open_file('$FILE'); print(r.schema); print('rows:', r.num_record_batches)"
```

Maps to: `interoperability.data_structure.features` (structured), `accessibility.dataset_scale.record_count`.

### Images (TIFF, PNG, JPEG)

```bash
identify "$FILE"                                                          # ImageMagick: dimensions, color
python3 -c "from PIL import Image; im=Image.open('$FILE'); print(im.size, im.mode, im.format)"
```

For a directory of images:

```bash
identify "$DIR"/*.png | awk '{print $3}' | sort -u                       # unique resolutions
find "$DIR" -type f \( -iname '*.png' -o -iname '*.tif' \) | wc -l       # image count
```

Maps to: `interoperability.data_structure.modalities: [image]`, `accessibility.dataset_scale.record_count` (image count), `interoperability.data_structure.features` (per-image structured: width/height/channels).

---

## 3. Advanced introspection patterns

### 3.1 Checksums (for `integrity.checksum_*`)

For a single primary file:

```bash
# Linux:
sha256sum "$FILE"
# macOS:
shasum -a 256 "$FILE"
# Cross-platform via Python:
python3 -c "import hashlib; h=hashlib.sha256(open('$FILE','rb').read()).hexdigest(); print(h)"
```

For a multi-file dataset, compute a manifest:

```bash
# Linux:
find "$DIR" -type f -exec sha256sum {} \; > checksums.sha256
# macOS:
find "$DIR" -type f -exec shasum -a 256 {} \; > checksums.sha256
```

Maps to:
- `integrity.checksum_available: true`
- `integrity.checksum_type: sha256`
- `integrity.checksum_value: <hash>` (for single-file) or path to the manifest (for multi-file)

`sha256` recommended; do not use `md5` for new datasets (kept in enum for legacy compatibility).

### 3.2 CITATION.cff parsing (for `authors[]`, `citation.preferred_citation`)

The CITATION.cff file is YAML. Extract structured fields:

```bash
python3 - <<'PY'
import yaml
cff = yaml.safe_load(open('CITATION.cff'))
# Title -> identification.name (cross-check with directory name)
print('title:', cff.get('title'))
# Authors -> authors[]
for a in cff.get('authors', []):
    print('author:', {
        'given_name': a.get('given-names'),
        'family_name': a.get('family-names'),
        'orcid': a.get('orcid', '').replace('https://orcid.org/', ''),
        'email': a.get('email'),
        'affiliation_name': a.get('affiliation'),
    })
# DOI -> identification.primary_id (type=doi)
print('doi:', cff.get('doi'))
# Date -> dates.issued
print('date_released:', cff.get('date-released'))
# Version -> identification.version
print('version:', cff.get('version'))
# Keywords -> description.keywords
print('keywords:', cff.get('keywords'))
PY
```

Note: CFF uses kebab-case (`family-names`); Genesis uses snake_case (`family_name`). Translate.

For BibTeX (`.bib`), parse the entry directly into `citation.preferred_citation`.

### 3.3 README extraction (for `description.summary`, `description.keywords`)

```bash
# First paragraph after the title:
awk '/^# /{found=1; next} found && NF==0 && body{exit} found{body=1; print}' README.md
# Headings (potential keywords):
grep -E '^##+ ' README.md | sed 's/^#* //'
```

For keywords specifically:
- Domain terms in section headings
- Bold-italic emphasis (`**X**`, `*Y*`) inside the first 500 chars
- A `Keywords:` line if present (some READMEs use this convention)

Maps to: `description.summary` (1-3 sentences from first paragraph; **trim and confirm with user**), `description.keywords` (3-10 terms, **always confirm with user**).

### 3.4 LICENSE → SPDX matching

Common patterns to detect from `license_hint` (the first 5 lines of the license file):

| `license_hint` contains | Best-guess `license.spdx_id` |
|---|---|
| `MIT License` | `MIT` |
| `Apache License` AND `Version 2.0` | `Apache-2.0` |
| `Apache License` (other version) | `Apache-1.1` or prompt |
| `BSD 3-Clause` | `BSD-3-Clause` |
| `BSD 2-Clause` | `BSD-2-Clause` |
| `Creative Commons Attribution 4.0` | `CC-BY-4.0` |
| `Creative Commons Attribution-ShareAlike 4.0` | `CC-BY-SA-4.0` |
| `Creative Commons Zero` OR `CC0` | `CC0-1.0` |
| `GNU General Public License` AND `version 3` | `GPL-3.0-only` (or `GPL-3.0-or-later` if explicit) |
| `GNU General Public License` AND `version 2` | `GPL-2.0-only` |
| `Mozilla Public License` AND `2.0` | `MPL-2.0` |
| `Unlicense` | `Unlicense` |
| Anything else | `other` and set `license.name` to the human name |

**Always confirm the guess with the user** before writing — license attribution is high-stakes.

### 3.5 Modality inference (for `interoperability.data_structure.modalities`)

Infer from `formats` and per-file inspection:

| Formats detected | `modalities` |
|---|---|
| CSV / TSV / Parquet / Arrow / NumPy (1D-2D) | `tabular` |
| HDF5 / NetCDF / NumPy (3D+) | `time-series` (if time dim) or `multi-dimensional` |
| TIFF / PNG / JPEG | `image` |
| WAV / MP3 / FLAC | `audio` |
| MP4 / MOV / AVI | `video` |
| TXT (large) / JSONL | `text` |
| GraphML / GEXF / DOT | `graph` |
| LAS / PLY / PCD | `point-cloud` |
| Multiple of the above | `multimodal` |

### 3.6 Encoding detection (for `interoperability.data_structure.encoding`)

```bash
file -bi "$FILE"                                     # macOS/Linux: shows charset=
python3 -c "import chardet; print(chardet.detect(open('$FILE','rb').read(8192)))"
```

Almost always `UTF-8` for new datasets. Use `not_applicable` for binary formats (HDF5, NetCDF, NumPy, Pickle, images).

### 3.7 Splits detection from filenames (introspect.py only checks subdirs)

When splits aren't directory-organized, check filenames:

```bash
find "$DIR" -maxdepth 2 -type f \( -iname '*train*' -o -iname '*test*' -o -iname '*val*' \) | head
```

Then deduplicate by inferred split:

```bash
find "$DIR" -maxdepth 2 -type f -name '*.csv' | \
  grep -oE 'train|test|val(idation)?' | sort -u
```

Maps to: `interoperability.data_structure.splits`.

### 3.8 Structured `features` (for `supports_ai_usability=Yes` datacards)

When `supports_ai_usability=Yes`, `interoperability.data_structure.features` should be structured objects, not flat strings. For a CSV:

```bash
python3 - <<'PY'
import csv, statistics
rows = list(csv.DictReader(open('$FILE')))
if not rows: exit()
for col in rows[0].keys():
    vals = [r[col] for r in rows[:1000] if r[col]]
    # Type inference
    try:
        nums = [float(v) for v in vals]
        ftype = 'int' if all(v == int(v) for v in nums) else 'float'
        rng = f"{min(nums):.4g} - {max(nums):.4g}"
    except (ValueError, TypeError):
        ftype = 'string'
        rng = None
    print(f"- name: {col}\n  type: {ftype}" + (f"\n  range: '{rng}'" if rng else ""))
PY
```

Maps to: structured `interoperability.data_structure.features:` entries with `name`, `type`, optionally `unit`, `description`, `range`.

---

## 4. Uncompressed vs compressed bytes

`introspect.py` emits `total_bytes` from `stat()` — that's the stored size on disk (compressed if the files are compressed). For `accessibility.dataset_scale.uncompressed_bytes`, you need to extract first:

```bash
# Total size of all .gz files when uncompressed:
find "$DIR" -name '*.gz' -exec gzip -l {} \; | awk 'NR>1 && $2!="" {s+=$2} END {print s}'

# For .zip archives:
find "$DIR" -name '*.zip' -exec unzip -l {} \; | awk '/^[ \t]*[0-9]+/ {s+=$1} END {print s}'

# For .tar.gz, requires extraction or `tar -tzvf`:
find "$DIR" -name '*.tar.gz' -exec sh -c 'tar -tzvf "$1" | awk "{s+=\$3} END {print s}"' _ {} \;

# For HDF5 with internal compression — `h5stat`:
h5stat "$FILE" | grep -E 'Total raw data size|Total file size'
```

If files aren't compressed at all, `uncompressed_bytes == compressed_bytes` (set both equal).

---

## 5. Recap: minimum auto-fillable set

When `introspect.py` runs cleanly on a typical dataset directory, these Genesis fields can be pre-filled without prompting:

- `interoperability.data_structure.formats` (from `formats`)
- `interoperability.data_structure.features` flat-form (from `sample_columns` for CSVs)
- `interoperability.data_structure.splits` (from `splits_detected`)
- `accessibility.dataset_scale.record_count` (from `file_count`)
- `accessibility.dataset_scale.compressed_bytes` (from `total_bytes`)

Everything else requires either (a) running the manual commands in § 2–3, (b) parsing CITATION.cff/README/LICENSE per § 3.2–3.4, or (c) prompting the user.
