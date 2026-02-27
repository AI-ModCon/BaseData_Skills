#!/usr/bin/env python3
"""Generate Croissant metadata from a CSV file."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import date
from pathlib import Path

CONTEXT = {
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
    "transform": "cr:transform",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()



def infer_type(sample: str) -> str:
    s = sample.strip()
    if not s:
        return "sc:Text"
    if s.lower() in {"true", "false"}:
        return "sc:Boolean"
    try:
        int(s)
        return "sc:Integer"
    except ValueError:
        pass
    try:
        float(s)
        return "sc:Float"
    except ValueError:
        pass
    return "sc:Text"



def read_headers_and_sample(csv_path: Path) -> tuple[list[str], dict[str, str]]:
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        first_row = next(reader, None) or {}
    samples = {h: str(first_row.get(h, "")) for h in headers}
    return headers, samples



def build_metadata(args: argparse.Namespace, headers: list[str], samples: dict[str, str]) -> dict:
    csv_path = Path(args.csv_path)
    file_id = "data-file"

    fields = []
    for col in headers:
        fields.append(
            {
                "@type": "cr:Field",
                "@id": f"records/{col}",
                "name": col,
                "description": f"The {col} column",
                "dataType": infer_type(samples.get(col, "")),
                "source": {
                    "fileObject": {"@id": file_id},
                    "extract": {"column": col},
                },
            }
        )

    return {
        "@context": CONTEXT,
        "@type": "sc:Dataset",
        "conformsTo": "http://mlcommons.org/croissant/1.0",
        "name": args.name,
        "description": args.description,
        "license": args.license_url,
        "url": args.url,
        "citeAs": args.cite_as,
        "creator": {"@type": "Person", "name": args.creator_name},
        "datePublished": str(date.today()),
        "version": args.version,
        "distribution": [
            {
                "@type": "cr:FileObject",
                "@id": file_id,
                "name": csv_path.name,
                "contentUrl": args.csv_path,
                "encodingFormat": "text/csv",
                "sha256": sha256_file(csv_path),
            }
        ],
        "recordSet": [
            {
                "@type": "cr:RecordSet",
                "@id": "records",
                "name": "records",
                "field": fields,
            }
        ],
    }



def main() -> int:
    parser = argparse.ArgumentParser(description="Generate croissant.json from a CSV file.")
    parser.add_argument("csv_path", help="Path to CSV file")
    parser.add_argument("name", help="Dataset name")
    parser.add_argument("description", help="Dataset description")
    parser.add_argument("license_url", help="SPDX license URL")
    parser.add_argument("creator_name", help="Creator name")
    parser.add_argument("url", help="Dataset URL")
    parser.add_argument("--output", default="croissant.json", help="Output JSON path")
    parser.add_argument("--version", default="1.0.0", help="Dataset semantic version")
    parser.add_argument(
        "--cite-as",
        default="",
        help="Citation string (recommended)",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    headers, samples = read_headers_and_sample(csv_path)
    if not headers:
        raise ValueError("CSV has no headers")

    metadata = build_metadata(args, headers, samples)
    out_path = Path(args.output)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
        f.write("\n")

    print(f"Generated {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
