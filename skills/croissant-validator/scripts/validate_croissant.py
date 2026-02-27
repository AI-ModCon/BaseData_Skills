#!/usr/bin/env python3
"""Validate Croissant metadata with required-field checks and optional mlcroissant parsing."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED_FIELDS = [
    "@context",
    "@type",
    "conformsTo",
    "name",
    "description",
    "license",
    "url",
    "creator",
    "datePublished",
    "distribution",
]



def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)



def validate_required_fields(metadata: dict) -> list[str]:
    return [field for field in REQUIRED_FIELDS if field not in metadata]



def validate_mlcroissant(path: Path) -> str | None:
    try:
        import mlcroissant as mlc  # type: ignore
    except ImportError:
        return "mlcroissant not installed; skipped library validation"

    try:
        dataset = mlc.Dataset(str(path))
        return f"mlcroissant parse OK: {dataset.metadata.name}"
    except Exception as exc:  # pragma: no cover - passthrough for runtime errors
        raise RuntimeError(f"mlcroissant validation failed: {exc}") from exc



def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Croissant metadata JSON file.")
    parser.add_argument("metadata_path", help="Path to croissant metadata JSON file")
    args = parser.parse_args()

    path = Path(args.metadata_path)
    if not path.exists():
        print(f"ERROR: File not found: {path}", file=sys.stderr)
        return 1

    try:
        metadata = load_json(path)
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON: {exc}", file=sys.stderr)
        return 1

    missing = validate_required_fields(metadata)
    if missing:
        print(f"ERROR: Missing required fields: {', '.join(missing)}", file=sys.stderr)
        return 1

    if metadata.get("conformsTo") != "http://mlcommons.org/croissant/1.0":
        print(
            "WARNING: conformsTo is not http://mlcommons.org/croissant/1.0",
            file=sys.stderr,
        )

    distribution = metadata.get("distribution", [])
    for idx, entry in enumerate(distribution):
        if entry.get("@type") == "cr:FileObject" and not (
            entry.get("sha256") or entry.get("md5")
        ):
            print(
                f"WARNING: distribution[{idx}] FileObject missing sha256/md5 checksum",
                file=sys.stderr,
            )

    try:
        msg = validate_mlcroissant(path)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print("OK: Required field validation passed")
    if msg:
        print(f"OK: {msg}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
