import base64
import csv
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from make_baseline_chart import read_responses


FOLDER = Path(__file__).resolve().parent
FIELDS = ["q1_1", "q1_3_2", "q1_3_5", "q1_5_3", "q1_5_4",
          "q1_5_6", "q1_5_7", "q1_5_8", "q1_5_9"]


def sample_rows():
    return [
        dict.fromkeys(FIELDS, "1"),
        {field: "1" if field == "q1_1" else "0" for field in FIELDS},
        {field: "2" if field == "q1_1" else "" for field in FIELDS},
    ]


def write_csv(path, rows, fields=FIELDS):
    with path.open("w", encoding="utf-8-sig", newline="") as source:
        writer = csv.DictWriter(source, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def chart_values(svg):
    return re.findall(r'<text class="value"[^>]*>(.*?)</text>', svg)


class BaselineChartTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.folder = Path(self.temporary.name)
        self.input = self.folder / "responses.csv"
        write_csv(self.input, sample_rows())

    def generate(self):
        return subprocess.run(
            [sys.executable, str(FOLDER / "make_baseline_chart.py"),
             "--input", str(self.input), "--output-dir", str(self.folder)],
            capture_output=True, text=True,
        )

    def test_percentage_labels_and_denominators(self):
        result = self.generate()
        self.assertEqual(result.returncode, 0, result.stderr)
        stats = json.loads(result.stdout)
        self.assertEqual(stats["BASELINE_CODING_PERCENT"], "50.0%")
        self.assertEqual(stats["BASELINE_TOTAL"], "3")
        self.assertEqual(stats["BASELINE_WORK_USERS"], "2")
        self.assertEqual(
            chart_values((self.folder / "baseline-common-uses.svg").read_text()),
            ["100%", "50%", "50%", "50%"],
        )
        self.assertEqual(
            chart_values((self.folder / "baseline-research-workflows.svg").read_text()),
            ["50%"] * 4,
        )

    def test_invalid_responses_fail(self):
        for field, value, message in (
            ("q1_1", "", "valid q1_1"),
            ("q1_5_3", "", "binary response"),
            ("q1_3_5", "yes", "binary response"),
        ):
            with self.subTest(field=field, value=value):
                rows = sample_rows()
                rows[0][field] = value
                write_csv(self.input, rows)
                result = self.generate()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(message, result.stderr)

    def test_missing_empty_and_no_work_data_fail(self):
        for rows, message in (
            ([], "no response rows"),
            ([sample_rows()[2]], "no respondents using AI for work"),
        ):
            with self.subTest(message=message):
                write_csv(self.input, rows)
                result = self.generate()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(message, result.stderr)
        self.input.unlink()
        self.assertNotEqual(self.generate().returncode, 0)

    def test_missing_columns_fail(self):
        write_csv(self.input, [{"q1_1": "1"}], ["q1_1"])
        result = self.generate()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing expected baseline fields", result.stderr)

    def test_xlsx_matches_csv(self):
        ns = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
        sheet = ET.Element("worksheet", xmlns=ns)
        data = ET.SubElement(sheet, "sheetData")
        rows = [FIELDS] + [[row[field] for field in FIELDS] for row in sample_rows()]
        for index, values in enumerate(rows, 1):
            row = ET.SubElement(data, "row", r=str(index))
            for column, value in enumerate(values):
                cell = ET.SubElement(row, "c", r=f"{chr(65 + column)}{index}", t="inlineStr")
                ET.SubElement(ET.SubElement(cell, "is"), "t").text = value
        path = self.folder / "responses.xlsx"
        with ZipFile(path, "w") as workbook:
            workbook.writestr("xl/workbook.xml",
                             f'<workbook xmlns="{ns}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Responses" sheetId="1" r:id="rId1"/></sheets></workbook>')
            workbook.writestr("xl/_rels/workbook.xml.rels",
                             '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Target="worksheets/sheet1.xml"/></Relationships>')
            workbook.writestr("xl/worksheets/sheet1.xml", ET.tostring(sheet))
        self.assertEqual(read_responses(path), read_responses(self.input))

    def test_normal_render_refreshes_embedded_charts_and_text(self):
        environment = os.environ.copy()
        environment["AI_BOOTCAMP_BASELINE_DATA"] = str(self.input)
        environment["AI_BOOTCAMP_PYTHON"] = sys.executable
        command = ["quarto", "render", str(FOLDER / "intro-bootcamp.qmd")]
        try:
            for writing, coding in (("1", "1"), ("0", "0")):
                rows = sample_rows()
                rows[0]["q1_5_3"] = writing
                rows[0]["q1_3_5"] = coding
                rows[2]["q1_1"] = "3"
                write_csv(self.input, rows)
                result = subprocess.run(command, env=environment, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                html = (FOLDER / "index.html").read_text(encoding="utf-8")
                self.assertNotRegex(html, r"BASELINE_[A-Z_]+")
                self.assertIn(f'<strong>{"50.0%" if coding == "1" else "0.0%"}</strong>', html)
                self.assertIn("Most participants are experimenting with AI", html)
                self.assertIn("(n = 3)", html)
                svgs = [
                    base64.b64decode(value).decode("utf-8")
                    for value in re.findall(r'data:image/svg\+xml;base64,([^"]+)', html)
                ]
                expected = ["66.7%", "50%" if writing == "1" else "0%", "50%", "50%"]
                self.assertTrue(any(chart_values(svg) == expected for svg in svgs))
            environment["AI_BOOTCAMP_BASELINE_DATA"] = str(self.folder / "missing.csv")
            result = subprocess.run(command, env=environment, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0, "Missing source must stop render")
        finally:
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, "Restore actual deck: " + result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
