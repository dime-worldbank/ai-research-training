#!/usr/bin/env python3
"""Compare keyed table-result records in CSV, TSV, JSON, or XLSX files.

Reference values may be displayed text transcribed from Excel, Word, PDF, or an
image. Before numeric comparison, displayed values are normalized: missing-value
tokens are recognized, and parentheses, brackets, thousands separators, percent
signs (without rescaling), Unicode minus signs, and trailing footnote or
significance markers are handled. Parentheses and brackets remain literal unless
their interpretation is selected explicitly.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import Counter
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path
from typing import Any

DEFAULT_MISSING_TOKENS = ("", ".", "-", "–", "—", "na", "n/a", "n.a.", "nan", "none", "null")
ANNOTATION = re.compile(r"[*†‡§¶#¹²³⁰-₟ᵃ-ᶿ]+$")
THOUSANDS = re.compile(r"^[+-]?\d{1,3}(,\d{3})+(\.\d+)?$")
# A rounding difference is expected when the reference shows rounded values, so it
# does not fail the comparison on its own.
ACCEPTED_CLASSIFICATIONS = {"exact_match", "within_declared_tolerance", "rounding_difference"}


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


def is_missing(value: Any, tokens: set[str]) -> bool:
    if value is None:
        return True
    if isinstance(value, float) and math.isnan(value):
        return True
    return isinstance(value, str) and value.strip().lower() in tokens


def parse_display(
    value: Any, parentheses: str = "literal", brackets: str = "literal"
) -> tuple[float | None, str, int | None]:
    """Return the numeric value, stripped annotation markers, and displayed decimals."""
    if isinstance(value, bool):
        return None, "", None
    if isinstance(value, (int, float)):
        return (float(value) if math.isfinite(value) else None), "", None
    raw = str(value).strip().replace("−", "-")
    annotation = ""

    def strip_annotation(current: str) -> str:
        nonlocal annotation
        match = ANNOTATION.search(current)
        if match:
            annotation = match.group() + annotation
            current = current[: match.start()].strip()
        return current

    raw = strip_annotation(raw)
    if len(raw) >= 2 and (raw[0], raw[-1]) == ("(", ")"):
        if parentheses == "literal":
            return None, annotation, None
        raw = strip_annotation(raw[1:-1].strip())
        if parentheses == "negative" and not raw.startswith("-"):
            raw = f"-{raw}"
    elif len(raw) >= 2 and (raw[0], raw[-1]) == ("[", "]"):
        if brackets == "literal":
            return None, annotation, None
        raw = strip_annotation(raw[1:-1].strip())
    raw = raw.rstrip("%").strip()
    if THOUSANDS.match(raw):
        raw = raw.replace(",", "")
    try:
        number = float(raw)
    except ValueError:
        return None, annotation, None
    if not math.isfinite(number):
        return None, annotation, None
    decimals = None if "e" in raw.lower() else len(raw.split(".", 1)[1]) if "." in raw else 0
    return number, annotation, decimals


def round_half_up(number: float, decimals: int) -> Decimal:
    return Decimal(repr(number)).quantize(Decimal(1).scaleb(-decimals), rounding=ROUND_HALF_UP)


def index(records: list[dict[str, Any]], keys: list[str]) -> dict[tuple[str, ...], dict[str, Any]]:
    output = {}
    for record in records:
        key = tuple(str(record.get(name, "")) for name in keys)
        if key in output:
            raise ValueError(f"Duplicate key: {key}")
        output[key] = record
    return output


def classify(left: Any, right: Any, args: argparse.Namespace) -> tuple[str, dict[str, Any]]:
    left_missing, right_missing = is_missing(left, args.missing_tokens), is_missing(right, args.missing_tokens)
    if left_missing and right_missing:
        return "exact_match", {}
    if left_missing or right_missing:
        return "missing_vs_value", {}

    left_num, left_note, left_decimals = parse_display(
        left, args.parentheses, args.brackets
    )
    right_num, right_note, _ = parse_display(
        right, args.parentheses, args.brackets
    )
    if left_num is None or right_num is None:
        if str(left).strip() == str(right).strip():
            return "exact_match", {}
        return "formatting_difference", {}

    annotations = {"reference_annotation": left_note, "generated_annotation": right_note}
    delta = abs(left_num - right_num)
    tolerance = args.atol + args.rtol * abs(left_num)
    if delta == 0 or delta <= tolerance:
        if args.check_annotations and left_note != right_note:
            return "annotation_difference", annotations
        return ("exact_match" if delta == 0 else "within_declared_tolerance"), {}

    detail: dict[str, Any] = {"absolute_difference": delta, "tolerance": tolerance}
    decimals = left_decimals if args.display_decimals == "auto" else args.display_decimals
    if decimals is not None and round_half_up(left_num, decimals) == round_half_up(right_num, decimals):
        detail["display_decimals"] = decimals
        if args.check_annotations and left_note != right_note:
            return "annotation_difference", {**detail, **annotations}
        return "rounding_difference", detail
    return "statistical_difference", detail


def compare(args: argparse.Namespace) -> dict[str, Any]:
    reference = index(load_records(args.reference, args.reference_sheet), args.keys)
    generated = index(load_records(args.generated, args.generated_sheet), args.keys)
    counts: Counter[str] = Counter()
    differences = []
    for key in sorted(reference.keys() | generated.keys()):
        if key not in reference:
            classification, left, right, detail = "missing_from_reference", None, None, {}
        elif key not in generated:
            classification, left, right, detail = "missing_from_generated", None, None, {}
        else:
            left = reference[key].get(args.value_column)
            right = generated[key].get(args.value_column)
            classification, detail = classify(left, right, args)
        counts[classification] += 1
        if classification in {"exact_match", "within_declared_tolerance"}:
            continue
        entry: dict[str, Any] = {"key": key, "classification": classification}
        if classification not in {"missing_from_reference", "missing_from_generated"}:
            entry.update({"reference": left, "generated": right, **detail})
        differences.append(entry)
    unresolved = sum(n for name, n in counts.items() if name not in ACCEPTED_CLASSIFICATIONS)
    return {
        "reference": str(args.reference.resolve()),
        "generated": str(args.generated.resolve()),
        "keys": args.keys,
        "value_column": args.value_column,
        "atol": args.atol,
        "rtol": args.rtol,
        "display_decimals": args.display_decimals,
        "parentheses": args.parentheses,
        "brackets": args.brackets,
        "check_annotations": args.check_annotations,
        "missing_tokens": sorted(args.missing_tokens),
        "summary": {
            "reference_records": len(reference),
            "generated_records": len(generated),
            "exact_matches": counts["exact_match"],
            "within_tolerance": counts["within_declared_tolerance"],
            "differences": len(differences),
            "unresolved_differences": unresolved,
            "by_classification": dict(sorted(counts.items())),
        },
        "differences": differences,
    }


def display_decimals(value: str) -> int | str:
    if value == "auto":
        return value
    try:
        decimals = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a non-negative integer or 'auto'") from exc
    if decimals < 0:
        raise argparse.ArgumentTypeError("must be a non-negative integer or 'auto'")
    return decimals


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("reference", type=Path)
    parser.add_argument("generated", type=Path)
    parser.add_argument("--keys", required=True, help="Comma-separated key columns")
    parser.add_argument("--value-column", default="value")
    parser.add_argument("--atol", type=float, default=0.0)
    parser.add_argument("--rtol", type=float, default=0.0, help="Relative to the reference value")
    parser.add_argument(
        "--display-decimals",
        type=display_decimals,
        help=(
            "Classify values that agree after half-up rounding to N decimals as "
            "rounding_difference; 'auto' uses the decimals shown in each reference value"
        ),
    )
    parser.add_argument(
        "--check-annotations",
        action="store_true",
        help="Treat differing trailing markers, such as significance stars, as annotation_difference",
    )
    parser.add_argument(
        "--parentheses",
        choices=("literal", "unwrap", "negative"),
        default="literal",
        help=(
            "Interpret parenthesized values literally (default), as positive wrapped "
            "statistics (unwrap), or as accounting-style negatives (negative)"
        ),
    )
    parser.add_argument(
        "--brackets",
        choices=("literal", "unwrap"),
        default="literal",
        help="Interpret bracketed values literally (default) or unwrap them as positive statistics",
    )
    parser.add_argument(
        "--missing-tokens",
        help="Comma-separated, case-insensitive values treated as missing "
        f"(default: {', '.join(repr(t) for t in DEFAULT_MISSING_TOKENS)})",
    )
    parser.add_argument("--reference-sheet")
    parser.add_argument("--generated-sheet")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    args.keys = [item.strip() for item in args.keys.split(",") if item.strip()]
    if not args.keys:
        parser.error("--keys must contain at least one column")
    tokens = DEFAULT_MISSING_TOKENS if args.missing_tokens is None else args.missing_tokens.split(",")
    args.missing_tokens = {token.strip().lower() for token in tokens}
    for path in (args.reference, args.generated):
        if not path.is_file():
            parser.error(f"file not found: {path}")
    report = compare(args)
    encoded = json.dumps(report, indent=2, ensure_ascii=False, default=list) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
    raise SystemExit(1 if report["summary"]["unresolved_differences"] else 0)


if __name__ == "__main__":
    main()
