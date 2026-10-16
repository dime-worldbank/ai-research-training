import argparse
import csv
import json
import math
from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile


def read_workbook(path):
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with ZipFile(path) as workbook:
        strings = []
        if "xl/sharedStrings.xml" in workbook.namelist():
            root = ET.fromstring(workbook.read("xl/sharedStrings.xml"))
            strings = [
                "".join(node.text or "" for node in item.findall(".//m:t", ns))
                for item in root.findall("m:si", ns)
            ]
        root = ET.fromstring(workbook.read("xl/workbook.xml"))
        relations = ET.fromstring(workbook.read("xl/_rels/workbook.xml.rels"))
        targets = {item.attrib["Id"]: item.attrib["Target"] for item in relations}
        for sheet in root.findall("m:sheets/m:sheet", ns):
            relation = sheet.attrib[
                "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
            ]
            target = targets[relation]
            target = target.lstrip("/") if target.startswith("/") else "xl/" + target
            content = ET.fromstring(workbook.read(target))
            rows = []
            for row in content.findall("m:sheetData/m:row", ns):
                values = {}
                for cell in row.findall("m:c", ns):
                    column = "".join(char for char in cell.attrib["r"] if char.isalpha())
                    value = cell.find("m:v", ns)
                    text = value.text or "" if value is not None else ""
                    if cell.attrib.get("t") == "s":
                        text = strings[int(text)]
                    elif cell.attrib.get("t") == "inlineStr":
                        text = "".join(node.text or "" for node in cell.findall(".//m:t", ns))
                    values[column] = text
                if any(values.values()):
                    rows.append(values)
            if rows and "q1_1" in rows[0].values():
                headers = rows[0]
                return [
                    {header: row.get(column, "") for column, header in headers.items() if header}
                    for row in rows[1:]
                ]
    raise ValueError(
        "No response sheet with a q1_1 column found. Supply the raw response export, "
        "not the XLSForm questionnaire."
    )


def read_responses(path):
    if path.suffix.lower() == ".xlsx":
        return read_workbook(path)
    if path.suffix.lower() != ".csv":
        raise ValueError("Baseline responses must be a .csv or .xlsx export.")
    with path.open(encoding="utf-8-sig", newline="") as source:
        return list(csv.DictReader(source))


def selected_count(responses, field):
    return sum(response.get(field, "").strip() == "1" for response in responses)


def format_percent(count, denominator):
    percent = count / denominator * 100
    if 0 < percent < 0.5:
        return "<1%"
    if 99.5 <= percent < 100:
        return ">99%"
    return f"{math.floor(percent + 0.5)}%"


def build_chart(responses):
    work_ai_users = [response for response in responses if response.get("q1_1", "").strip() == "1"]
    denominator = len(work_ai_users)

    common = [
        ("Writing / editing documents", selected_count(work_ai_users, "q1_5_3"), denominator, "current"),
        ("Background research", selected_count(work_ai_users, "q1_5_4"), denominator, "current"),
        ("Third-party chat AI", selected_count(work_ai_users, "q1_3_2"), denominator, "current"),
    ]
    research = [
        ("Data analysis / visualization", selected_count(work_ai_users, "q1_5_7"), denominator, "current"),
        ("Survey workflows", selected_count(work_ai_users, "q1_5_6"), denominator, "current"),
        ("Dashboards / web apps", selected_count(work_ai_users, "q1_5_8"), denominator, "current"),
        ("Reproducibility packages", selected_count(work_ai_users, "q1_5_9"), denominator, "current"),
        ("Ever tried a coding agent", selected_count(work_ai_users, "q1_3_5"), denominator, "coding"),
    ]
    return common, research


def workflow_title(common, research):
    rate = lambda metric: metric[1] / metric[2]
    workflows = [metric for metric in research if metric[3] == "current"]
    if max(map(rate, workflows)) < min(map(rate, common)):
        return "…who don't use AI for code much (yet)"
    return "…and how you use AI for research workflows"


def cohort_title(any_ai_count, cohort_size):
    if any_ai_count == cohort_size:
        return "Who you are: AI enthusiasts"
    if any_ai_count > cohort_size / 2:
        return "Who you are: mostly AI enthusiasts"
    return "Who you are: AI-curious"


def svg_chart(metrics, title, note):
    label_x, bar_x, bar_width = 16, 445, 570
    first_y, row_gap, bar_height, coding_gap = 44, 54, 26, 18
    offset = lambda category: coding_gap if category == "coding" else 0
    grid_bottom = first_y + (len(metrics) - 1) * row_gap + offset(metrics[-1][3]) + 26
    note_lines = note.split("\n")
    width, height = 1200, grid_bottom + 72 + 26 * (len(note_lines) - 1)
    colors = {
        "current": "#6d397f",
        "coding": "#c2410c",
    }
    output = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(title)}</title>',
        f'<desc id="desc">{len(metrics)} horizontal bars show self-reported baseline use as percentages.</desc>',
        '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#25212a}.label{font-size:27px}.value{font-size:25px;font-weight:700}.axis{font-size:20px;fill:#666}.note{font-size:20px;fill:#555}.emphasis{font-weight:700}</style>',
    ]
    for tick in range(0, 101, 20):
        x = bar_x + bar_width * tick / 100
        output.append(
            f'<line x1="{x:.1f}" y1="20" x2="{x:.1f}" y2="{grid_bottom}" stroke="#e7e2e9" stroke-width="1"/>'
        )
        output.append(f'<text class="axis" x="{x:.1f}" y="{grid_bottom + 30}" text-anchor="middle">{tick}%</text>')

    for index, (label, count, denominator, category) in enumerate(metrics):
        y = first_y + index * row_gap + offset(category)
        if category == "coding":
            output.append(
                f'<line x1="{label_x}" y1="{y - 39}" x2="{bar_x + bar_width}" y2="{y - 39}" stroke="#c9bfcd" stroke-width="1.5" stroke-dasharray="6 6"/>'
            )
        percent = count / denominator * 100
        percent_label = format_percent(count, denominator)
        color = colors[category]
        output.append(f'<text class="label{" emphasis" if category == "coding" else ""}" x="{label_x}" y="{y + 7}">{escape(label)}</text>')
        output.append(
            f'<rect x="{bar_x}" y="{y - bar_height + 4}" width="{bar_width}" height="{bar_height}" rx="8" fill="#f1eef2"/>'
        )
        output.append(
            f'<rect x="{bar_x}" y="{y - bar_height + 4}" width="{bar_width * percent / 100:.1f}" height="{bar_height}" rx="8" fill="{color}"/>'
        )
        output.append(
            f'<text class="value" x="{bar_x + bar_width + 18}" y="{y + 7}">{percent_label}</text>'
        )

    for index, line in enumerate(note_lines):
        y = height - 13 - 26 * (len(note_lines) - 1 - index)
        output.append(f'<text class="note" x="16" y="{y}">{escape(line)}</text>')
    output.append("</svg>")
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Build two aggregate-only SVG charts from baseline survey responses."
    )
    parser.add_argument("--input", required=True, type=Path, help="Path to the raw baseline CSV or XLSX response export")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).parent / "images",
        help="Directory for the two output SVG charts",
    )
    args = parser.parse_args()

    responses = read_responses(args.input)
    if not responses:
        parser.error("The baseline CSV contains no response rows.")
    required_fields = {"q1_1", "q1_3_2", "q1_3_5", "q1_5_3", "q1_5_4", "q1_5_6", "q1_5_7", "q1_5_8", "q1_5_9"}
    missing_fields = required_fields.difference(responses[0])
    if missing_fields:
        parser.error(f"Missing expected baseline fields: {', '.join(sorted(missing_fields))}")
    if any(row["q1_1"].strip() not in {"1", "2", "3"} for row in responses):
        parser.error("Every response must have a valid q1_1 value (1, 2, or 3).")

    work_ai_users = [row for row in responses if row["q1_1"].strip() == "1"]
    if not work_ai_users:
        parser.error("The baseline contains no respondents using AI for work.")
    for field in required_fields - {"q1_1"}:
        if any(row[field].strip() not in {"0", "1"} for row in work_ai_users):
            parser.error(f"Expected a binary response from every work-AI user for {field}.")

    common, research = build_chart(responses)
    any_ai_count = sum(row["q1_1"].strip() in {"1", "2"} for row in responses)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    charts = [
        (
            "baseline-common-uses.svg",
            common,
            cohort_title(any_ai_count, len(responses)),
            f"Baseline: {len(work_ai_users)} work-AI users. Tasks: last four weeks; chat AI: ever used.\n"
            f"Any AI use (work or personal): {format_percent(any_ai_count, len(responses))} "
            f"of {len(responses)} respondents.",
        ),
        (
            "baseline-research-workflows.svg",
            research,
            workflow_title(common, research),
            f"Baseline: {len(work_ai_users)} work-AI users. Tasks: last four weeks; coding agent: ever used.",
        ),
    ]
    for filename, metrics, title, note in charts:
        path = args.output_dir / filename
        path.write_text(svg_chart(metrics, title, note), encoding="utf-8")
    count = selected_count(work_ai_users, "q1_3_5")
    print(json.dumps({
        "BASELINE_CODING_PERCENT": format_percent(count, len(work_ai_users)),
        "BASELINE_TOTAL": str(len(responses)),
        "BASELINE_WORK_USERS": str(len(work_ai_users)),
        "BASELINE_WORKFLOW_TITLE": workflow_title(common, research),
        "BASELINE_TITLE": cohort_title(any_ai_count, len(responses)),
    }))


if __name__ == "__main__":
    main()
