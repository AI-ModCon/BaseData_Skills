"""introspect.py — emit JSON summary of a dataset directory.

Cross-platform (Windows, macOS, Linux) replacement for introspect.sh.
Stdlib only — no external dependencies.

Usage: python3 introspect.py <dataset_dir>
Output: JSON to stdout. Exit 0 on success, 2 on usage error.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

EXT_TO_FORMAT: dict[str, str] = {
    "csv": "CSV", "tsv": "TSV", "json": "JSON",
    "yaml": "YAML", "yml": "YAML",
    "h5": "HDF5", "hdf5": "HDF5",
    "nc": "NetCDF4", "nc4": "NetCDF4",
    "parquet": "Parquet", "arrow": "Arrow",
    "tif": "TIFF", "tiff": "TIFF",
    "png": "PNG", "jpg": "JPEG", "jpeg": "JPEG",
    "txt": "Text", "md": "Markdown",
    "npy": "NumPy", "npz": "NumPy",
    "pkl": "Pickle", "pt": "PyTorch", "pth": "PyTorch",
}


def _files_at_depth(base: Path, max_depth: int):
    """Yield files whose path is at most `max_depth` components below `base`."""
    for p in base.rglob("*"):
        if not p.is_file():
            continue
        if len(p.relative_to(base).parts) <= max_depth:
            yield p


def _find_first(base: Path, prefixes: tuple[str, ...], max_depth: int = 2) -> str:
    """Return string path of the first file at depth<=max_depth whose name starts (case-insensitively) with any of `prefixes`."""
    for p in _files_at_depth(base, max_depth):
        name_upper = p.name.upper()
        if any(name_upper.startswith(pref.upper()) for pref in prefixes):
            return str(p)
    return ""


def _sample_csv_columns(csv_path: Path) -> list[str]:
    try:
        with csv_path.open(encoding="utf-8", errors="replace", newline="") as fp:
            reader = csv.reader(fp)
            first = next(reader, [])
            return [c.strip() for c in first]
    except (OSError, csv.Error):
        return []


def _license_hint(license_path: str) -> str:
    try:
        with open(license_path, encoding="utf-8", errors="replace") as fp:
            head_lines = [next(fp, "").rstrip() for _ in range(5)]
    except OSError:
        return ""
    joined = " ".join(line for line in head_lines if line)
    return joined[:200]


def _detect_splits(base: Path) -> list[str]:
    targets = {"train", "test", "val", "validation"}
    found: list[str] = []
    for p in base.rglob("*"):
        if not p.is_dir():
            continue
        if len(p.relative_to(base).parts) > 3:
            continue
        if p.name.lower() in targets and p.name.lower() not in found:
            found.append(p.name.lower())
    return found


def introspect(base: Path) -> dict:
    all_files = [p for p in base.rglob("*") if p.is_file()]
    formats = sorted({
        EXT_TO_FORMAT[p.suffix.lstrip(".").lower()]
        for p in all_files
        if p.suffix and p.suffix.lstrip(".").lower() in EXT_TO_FORMAT
    })
    total_bytes = 0
    for p in all_files:
        try:
            total_bytes += p.stat().st_size
        except OSError:
            continue

    sample_columns: dict[str, list[str]] = {}
    for csv_path in [p for p in all_files if p.suffix.lower() == ".csv"][:3]:
        cols = _sample_csv_columns(csv_path)
        if cols:
            sample_columns[csv_path.name] = cols

    readme = _find_first(base, ("README",), max_depth=2)
    citation = _find_first(base, ("CITATION",), max_depth=2)
    license_path = _find_first(base, ("LICENSE", "COPYING"), max_depth=2)

    return {
        "path": str(base),
        "file_count": len(all_files),
        "total_bytes": total_bytes,
        "formats": formats,
        "sample_columns": sample_columns,
        "readme_file": readme,
        "license_file_present": bool(license_path),
        "license_hint": _license_hint(license_path) if license_path else "",
        "citation_file": citation,
        "splits_detected": _detect_splits(base),
    }


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) < 1:
        print("usage: introspect.py <dataset_dir>", file=sys.stderr)
        return 2
    base = Path(args[0])
    if not base.is_dir():
        print(f"not a directory: {base}", file=sys.stderr)
        return 2
    out = introspect(base)
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
