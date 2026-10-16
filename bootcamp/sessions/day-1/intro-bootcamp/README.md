# Intro presentation: baseline data refresh

Every Quarto render runs `baseline-render.lua`, which calls
`make_baseline_chart.py` before embedding the two baseline charts.
The coding-agent percentage, sample sizes in speaker notes, and both baseline
slide titles are populated from the same data. Chart bar labels show whole-number
percentages only (`<1%`/`>99%` at the extremes); footnotes retain sample sizes to
clarify the denominators.

- **Common uses chart:** writing, background research, and third-party chat AI
  among work-AI users. Any AI use (work or personal) appears in the footnote and
  drives the slide title ("Who you are: AI enthusiasts" when everyone uses AI,
  "mostly AI enthusiasts" for a majority, otherwise "AI-curious").
- **Research workflows chart:** four last-four-weeks workflow tasks plus a
  highlighted "Ever tried a coding agent" bar, separated by a dashed line. The
  title continues the first slide's ("…who don't use AI for code much (yet)") only
  while every workflow rate is below every common-use rate; otherwise it falls
  back to "…and how you use AI for research workflows".

## Input

Use the **raw SurveyCTO response export**, either wide CSV or XLSX with
question IDs as column headers (`q1_1`, `q1_3_5`, etc.). The XLSForm workbook
defines the questionnaire and is **not** a response dataset. For XLSX, the
first sheet with `q1_1` in its first nonempty row is read.

Set the environment variable `AI_BOOTCAMP_BASELINE_DATA` to the absolute export
path, or save that path as the only line in `baseline-path.local.txt` beside
the presentation. The environment variable takes precedence. The local path
file is git-ignored; do not add respondent-level data to the repository.

Python 3 is required; the generator uses only its standard library. If Python
is not on PATH, set `AI_BOOTCAMP_PYTHON` to the Python executable.

## Refresh

Replace/update the configured export with new baseline responses, then run
from the repository root:

```powershell
quarto render 'bootcamp\sessions\day-1\intro-bootcamp\intro-bootcamp.qmd'
```

There is no separate chart-generation step, caching, or fallback to old figures.
A missing source, invalid responses, or missing required columns stops the
render with an error. Binary tool/task questions must be present for every
work-AI user; survey skips for non-work users are excluded from those denominators.
Keep the input file unchanged for the duration of a render.

The two SVGs and self-contained `index.html` contain aggregate statistics only.
The goal of everyone using a coding agent by endline is a stated aspiration,
not a value calculated from baseline responses.

## Validation

```powershell
python -m unittest discover -s 'bootcamp\sessions\day-1\intro-bootcamp' -p 'test_baseline_chart.py'
```

The tests check percentage labels, denominators, CSV/XLSX parity, invalid
inputs, and ordinary Quarto renders after changing a temporary response export.
The render test restores the presentation using your configured real input.

## QR codes

The four QR codes on the "Before the next session" slide are static SVGs in
`images/qr-*.svg`, so renders do not need any extra package. If a link changes,
update it in both the slide and `make_qr_codes.py`, then regenerate (requires
`pip install segno`):

```powershell
python 'bootcamp\sessions\day-1\intro-bootcamp\make_qr_codes.py'
```
