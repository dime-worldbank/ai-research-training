#!/usr/bin/env python3
"""Compare keyed table-result records in CSV, TSV, JSON, or XLSX files."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any


def load_records(path: Path, sheet: str | None) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix in {".csv", ".tsv"}:
        with path.open(newline="", encoding="utf-8-sig") as stream:
            return list(csv.DictReader(stream, delimiter="\t" if suffix == ".tsv" else ","))
    if suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data = data.get("records")
        if not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
            raise ValueError("JSON must be a list of records or an object with a records list")
        return data
    if suffix == ".xlsx":
        try:
            import openpyxl
        except ImportError as exc:
            raise SystemExit("openpyxl is required to compare XLSX files") from exc
        workbook = openpyxl.load_workbook(path, data_only=True, read_only=True)
        worksheet = workbook[sheet] if sheet else workbook.active
        rows = worksheet.iter_rows(values_only=True)
        try:
            headers = [str(value) if value is not None else "" for value in next(rows)]
        except StopIteration:
            return []
        return [dict(zip(headers, row)) for row in rows]
    raise ValueError(f"Unsupported file type: {suffix}")


def numeric(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def index(records: list[dict[str, Any]], keys: list[str]) -> dict[tuple[str, ...], dict[str, Any]]:
    output = {}
    for record in records:
        key = tuple(str(record.get(name, "")) for name in keys)
        if key in output:
            raise ValueError(f"Duplicate key: {key}")
        output[key] = record
    return output


def compare(args: argparse.Namespace) -> dict[str, Any]:
    reference = index(load_records(args.reference, args.reference_sheet), args.keys)
    generated = index(load_records(args.generated, args.generated_sheet), args.keys)
    differences = []
    exact = within = 0
    for key in sorted(reference.keys() | generated.keys()):
        if key not in reference:
            differences.append({"key": key, "classification": "missing_from_reference"})
            continue
        if key not in generated:
            differences.append({"key": key, "classification": "missing_from_generated"})
            continue
        left = reference[key].get(args.value_column)
        right = generated[key].get(args.value_column)
        if left == right:
            exact += 1
            continue
        left_num, right_num = numeric(left), numeric(right)
        if left_num is not None and right_num is not None:
            delta = abs(left_num - right_num)
            tolerance = args.atol + args.rtol * abs(left_num)
            if delta <= tolerance:
                within += 1
                continue
            classification = "statistical_difference"
            detail = {"absolute_difference": delta, "tolerance": tolerance}
        else:
            classification = "formatting_difference"
            detail = {}
        differences.append(
            {
                "key": key,
                "classification": classification,
                "reference": left,
                "generated": right,
                **detail,
            }
        )
    return {
        "reference": str(args.reference.resolve()),
        "generated": str(args.generated.resolve()),
        "keys": args.keys,
        "value_column": args.value_column,
        "atol": args.atol,
        "rtol": args.rtol,
        "summary": {
            "reference_records": len(reference),
            "generated_records": len(generated),
            "exact_matches": exact,
            "within_tolerance": within,
            "differences": len(differences),
        },
        "differences": differences,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", type=Path)
    parser.add_argument("generated", type=Path)
    parser.add_argument("--keys", required=True, help="Comma-separated key columns")
    parser.add_argument("--value-column", default="value")
    parser.add_argument("--atol", type=float, default=0.0)
    parser.add_argument("--rtol", type=float, default=0.0)
    parser.add_argument("--reference-sheet")
    parser.add_argument("--generated-sheet")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    args.keys = [item.strip() for item in args.keys.split(",") if item.strip()]
    if not args.keys:
        parser.error("--keys must contain at least one column")
    for path in (args.reference, args.generated):
        if not path.is_file():
            parser.error(f"file not found: {path}")
    report = compare(args)
    encoded = json.dumps(report, indent=2, ensure_ascii=False, default=list) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
    raise SystemExit(1 if report["summary"]["differences"] else 0)


if __name__ == "__main__":
    main()
