# Introspection commands

Commands SKILL.md can run (directly or via `python3 scripts/introspect.py`) to
auto-fill Genesis v1.0 datacard fields. Each command's output maps to one
or more YAML fields.

## File structure & counts

| Command | Maps to |
|---------|---------|
| `find "$DIR" -type f \| wc -l` | `dataset_scale.record_count` (when file-based) |
| `du -sb "$DIR"` (Linux) / `find -f%z` (macOS) | `dataset_scale.compressed_bytes` |
| `find "$DIR" -type f -name '*.*' \| sed -E 's\|.*\\.\|\|' \| sort -u` | `dataset_info.formats` |

## Schema extraction

### CSV / TSV
| Command | Maps to |
|---------|---------|
| `head -n 1 "$FILE" \| tr ',' '\n'` | `dataset_info.features` (flat list) |
| `head -n 2 "$FILE"` | example for `dataset_info.features` (ai_ready) |

### HDF5
| Command | Maps to |
|---------|---------|
| `h5ls "$FILE"` | `dataset_info.features` (group/dataset names) |
| `h5dump -H "$FILE"` | full schema for `semantic_layer.schema_url` cross-ref |

### Parquet
| Command | Maps to |
|---------|---------|
| `parquet-tools schema "$FILE"` | `dataset_info.features` (structured) |

### NetCDF
| Command | Maps to |
|---------|---------|
| `ncdump -h "$FILE"` | `dataset_info.features`, `dataset_info.spatial_coverage` |

## Metadata file discovery

| File pattern | Maps to |
|--------------|---------|
| `README*` | `description.summary` (first paragraph), `description.keywords` |
| `LICENSE*` / `COPYING*` | `license.spdx_id` (best-guess from content) |
| `CITATION.cff` | `authors[]`, `citation.preferred_citation` |
| `*.bib` | `citation.preferred_citation` |

## Splits detection

| Command | Maps to |
|---------|---------|
| `find "$DIR" -maxdepth 3 -type d -iname 'train' -o -iname 'test' -o -iname 'val*'` | `dataset_info.splits` |

## Bulk inspection (use scripts/introspect.py)

`python3 scripts/introspect.py <dataset_dir>` runs all the above and emits
JSON. SKILL.md should prefer this over running commands ad hoc unless the
auto-fill missed something specific.
