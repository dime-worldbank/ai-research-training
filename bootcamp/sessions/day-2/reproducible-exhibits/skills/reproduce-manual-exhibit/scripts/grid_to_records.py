#!/usr/bin/env python3
"""Convert a displayed table grid into keyed reference records for compare_tables.py.

The grid can come from any reference format. Extract it first (Excel range, Word
table, PDF text table, or manual transcription of an image) into CSV/TSV, or read
an Excel range directly. Header rows become column keys and label columns become
row keys. Generated keys are defaults: review them and align them with the keys
the generated results use.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path
from typing import Any

SOURCE_METHODS = ("excel_cell", "docx_table", "pdf_text", "transcribed", "other")
FIELDS = (
    "row_key",
    "row_label",
    "column_key",
    "column_label",
    "value",
    "display_order",
    "source_method",
    "source_location",
)


def text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def slug(label: str) -> str:
    return re.sub(r"[^0-9a-z]+", "_", label.lower()).strip("_")


def column_letter(index: int) -> str:
    letters = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters


def load_grid(args: argparse.Namespace) -> tuple[list[list[Any]], Any]:
    """Return grid rows and a function mapping (row, column) offsets to a location."""
    suffix = args.grid.suffix.lower()
    prefix = f"{args.location_prefix} " if args.location_prefix else ""
    if suffix in {".csv", ".tsv"}:
        with args.grid.open(newline="", encoding="utf-8-sig") as stream:
            rows = list(csv.reader(stream, delimiter="\t" if suffix == ".tsv" else ","))
        return rows, lambda r, c: f"{prefix}r{r + 1}c{c + 1}"
    if suffix in {".xlsx", ".xlsm"}:
        if not args.range:
            raise SystemExit("--range is required for Excel input, for example B4:H20")
        try:
            import openpyxl
        except ImportError as exc:
            raise SystemExit("openpyxl is required to read Excel input") from exc
        workbook = openpyxl.load_workbook(args.grid, data_only=True, read_only=False)
        worksheet = workbook[args.sheet] if args.sheet else workbook.active
        cells = worksheet[args.range]
        if not isinstance(cells[0], tuple):
            cells = (cells,)
        rows = [[cell.value for cell in row] for row in cells]
        top, left = cells[0][0].row, cells[0][0].column
        return rows, lambda r, c: (
            f"{prefix}{worksheet.title}!{column_letter(left + c)}{top + r}"
        )
    raise SystemExit(f"Unsupported grid type: {suffix} (use CSV, TSV, or XLSX)")


def fill_right(row: list[str]) -> list[str]:
    filled, current = [], ""
    for value in row:
        current = value or current
        filled.append(current)
    return filled


def unique(key: str, seen: dict[str, int]) -> str:
    seen[key] = seen.get(key, 0) + 1
    return key if seen[key] == 1 else f"{key}__{seen[key]}"


def convert(args: argparse.Namespace) -> list[dict[str, Any]]:
    rows, locate = load_grid(args)
    width = max((len(row) for row in rows), default=0)
    rows = [list(row) + [None] * (width - len(row)) for row in rows]
    if args.header_rows >= len(rows) or args.label_columns >= width:
        raise SystemExit("Grid has no body cells after removing header rows and label columns")

    headers = [[text(value) for value in row[args.label_columns :]] for row in rows[: args.header_rows]]
    if args.fill_header_spans:
        headers = [fill_right(row) for row in headers]
    column_labels, column_keys, seen_columns = [], [], {}
    for index in range(width - args.label_columns):
        parts = [row[index] for row in headers if row[index]]
        label = " | ".join(parts)
        column_labels.append(label)
        column_keys.append(unique(slug(label) or f"col{index + 1}", seen_columns))

    records, seen_rows = [], {}
    previous_labels = [""] * args.label_columns
    for offset, row in enumerate(rows[args.header_rows :]):
        labels = [text(value) for value in row[: args.label_columns]]
        if args.fill_down_labels:
            labels = [label or previous for label, previous in zip(labels, previous_labels)]
            previous_labels = labels
        row_label = " | ".join(label for label in labels if label)
        row_key = unique(slug(row_label) or f"row{offset + 1}", seen_rows)
        for index, value in enumerate(row[args.label_columns :]):
            if text(value) == "" and not args.keep_blank:
                continue
            records.append(
                {
                    "row_key": row_key,
                    "row_label": row_label,
                    "column_key": column_keys[index],
                    "column_label": column_labels[index],
                    "value": value if not isinstance(value, str) else value.strip(),
                    "display_order": len(records) + 1,
                    "source_method": args.source_method,
                    "source_location": locate(args.header_rows + offset, args.label_columns + index),
                }
            )
    return records


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("grid", type=Path, help="CSV, TSV, or XLSX file containing the grid")
    parser.add_argument("--sheet", help="Excel sheet name (default: active sheet)")
    parser.add_argument("--range", help="Excel range containing headers, labels, and body")
    parser.add_argument("--header-rows", type=int, default=1)
    parser.add_argument("--label-columns", type=int, default=1)
    parser.add_argument(
        "--fill-header-spans",
        action="store_true",
        help="Carry spanning header text rightward into blank header cells",
    )
    parser.add_argument(
        "--fill-down-labels",
        action="store_true",
        help="Carry row labels downward into blank label cells, such as panel labels",
    )
    parser.add_argument(
        "--keep-blank",
        action="store_true",
        help="Emit records for blank body cells instead of skipping them",
    )
    parser.add_argument("--source-method", choices=SOURCE_METHODS)
    parser.add_argument(
        "--location-prefix",
        help="Text prepended to each source location, for example 'report.pdf p.12 Table 3'",
    )
    parser.add_argument("--output", type=Path, help="Write CSV to this path instead of stdout")
    args = parser.parse_args()
    if not args.grid.is_file():
        parser.error(f"file not found: {args.grid}")
    if args.header_rows < 0 or args.label_columns < 0:
        parser.error("--header-rows and --label-columns must be non-negative")
    if args.source_method is None:
        if args.grid.suffix.lower() in {".xlsx", ".xlsm"}:
            args.source_method = "excel_cell"
        else:
            parser.error("--source-method is required for CSV/TSV grids")

    records = convert(args)
    stream = args.output.open("w", newline="", encoding="utf-8") if args.output else sys.stdout
    try:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)
    finally:
        if args.output:
            stream.close()


if __name__ == "__main__":
    main()
