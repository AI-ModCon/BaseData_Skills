#!/usr/bin/env bash
# introspect.sh — emit JSON summary of a dataset directory.
#
# Reads: $1 = dataset directory path
# Writes: JSON to stdout with keys:
#   path, file_count, total_bytes, formats, sample_columns,
#   readme_file, license_file_present, license_hint, citation_file,
#   splits_detected
#
# macOS BSD stat; Linux: replace stat -f%z with stat -c%s

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: introspect.sh <dataset_dir>" >&2
  exit 2
fi

DIR="$1"

if [[ ! -d "$DIR" ]]; then
  echo "not a directory: $DIR" >&2
  exit 2
fi

FILE_COUNT=$(find "$DIR" -type f | wc -l | tr -d ' ')
TOTAL_BYTES=$(find "$DIR" -type f -exec stat -f%z {} \; 2>/dev/null \
                | awk '{s+=$1} END {print s+0}')

# Discover unique extensions and map to format names.
# Using case statement for bash 3.2 compatibility (macOS stock bash lacks declare -A).
ext_to_format() {
  case "$(printf '%s' "$1" | tr 'A-Z' 'a-z')" in
    csv)      echo CSV ;;
    tsv)      echo TSV ;;
    json)     echo JSON ;;
    yaml|yml) echo YAML ;;
    h5|hdf5)  echo HDF5 ;;
    nc|nc4)   echo NetCDF4 ;;
    parquet)  echo Parquet ;;
    arrow)    echo Arrow ;;
    tif|tiff) echo TIFF ;;
    png)      echo PNG ;;
    jpg|jpeg) echo JPEG ;;
    txt)      echo Text ;;
    md)       echo Markdown ;;
    npy|npz)  echo NumPy ;;
    pkl)      echo Pickle ;;
    pt|pth)   echo PyTorch ;;
    *)        ;;
  esac
}

EXT_LIST=$(find "$DIR" -type f -name '*.*' | sed -E 's|.*\.||' | sort -u)
FORMATS=()
for ext in $EXT_LIST; do
  fmt=$(ext_to_format "$ext")
  if [[ -n "$fmt" ]]; then
    FORMATS+=("$fmt")
  fi
done
FORMATS_JSON=$(printf '%s\n' "${FORMATS[@]:-}" | awk 'NF' | sort -u \
                 | awk 'BEGIN{first=1; printf "["} {if(!first)printf ","; printf "\"%s\"",$0; first=0} END{print "]"}')

# Sample columns of any CSV (first line of first 3 CSVs).
SAMPLE_COLUMNS="{}"
CSV_FILES=$(find "$DIR" -type f -name '*.csv' | head -n 3)
if [[ -n "$CSV_FILES" ]]; then
  SAMPLE_COLUMNS=$(
    while IFS= read -r csv; do
      base=$(basename "$csv")
      head -n 1 "$csv" | awk -v name="$base" -F',' '{
        printf "\"%s\":[", name
        for (i=1;i<=NF;i++) {
          gsub(/^[ \t]+|[ \t\r\n]+$/, "", $i)
          if (i>1) printf ","
          printf "\"%s\"", $i
        }
        printf "]"
      }'
      printf ","
    done <<< "$CSV_FILES" | sed 's/,$//'
  )
  SAMPLE_COLUMNS="{${SAMPLE_COLUMNS}}"
fi

# README / CITATION.
README=$(find "$DIR" -maxdepth 2 -type f \( -iname 'README*' \) | head -n 1)
CITATION=$(find "$DIR" -maxdepth 2 -type f \( -iname 'CITATION*' \) | head -n 1)

# License detection.
LICENSE_PATH=$(find "$DIR" -maxdepth 2 -type f \( -iname 'LICENSE*' -o -iname 'COPYING*' \) | head -n 1)
LICENSE_PRESENT="false"
LICENSE_HINT=""
if [[ -n "$LICENSE_PATH" ]]; then
  LICENSE_PRESENT="true"
  # Read first 5 lines, strip double-quotes to avoid JSON breakage, truncate to 200 chars.
  LICENSE_HINT=$(head -n 5 "$LICENSE_PATH" | tr '"' "'" | tr '\n' ' ' | cut -c1-200)
fi

# Splits.
SPLITS=()
for s in train test val validation; do
  if find "$DIR" -maxdepth 3 -type d -iname "$s" | grep -q .; then
    SPLITS+=("$s")
  fi
done
SPLITS_JSON=$(printf '%s\n' "${SPLITS[@]:-}" | awk 'NF' \
                 | awk 'BEGIN{first=1; printf "["} {if(!first)printf ","; printf "\"%s\"",$0; first=0} END{print "]"}')

# Escape backslashes and remaining special chars in string fields.
json_str() {
  printf '%s' "$1" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g'
}

README_ESC=$(json_str "${README:-}")
CITATION_ESC=$(json_str "${CITATION:-}")
DIR_ESC=$(json_str "$DIR")
LICENSE_HINT_ESC=$(json_str "$LICENSE_HINT")

cat <<JSON
{
  "path": "$DIR_ESC",
  "file_count": $FILE_COUNT,
  "total_bytes": $TOTAL_BYTES,
  "formats": $FORMATS_JSON,
  "sample_columns": $SAMPLE_COLUMNS,
  "readme_file": "$README_ESC",
  "license_file_present": $LICENSE_PRESENT,
  "license_hint": "$LICENSE_HINT_ESC",
  "citation_file": "$CITATION_ESC",
  "splits_detected": $SPLITS_JSON
}
JSON
