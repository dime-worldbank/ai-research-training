# Project memory — Zambia School Meals Evaluation

## What this project is
Difference-in-differences evaluation of Zambia's Free School Meals Programme
(FSMP), rolled out in 46 of 92 districts in January 2022. Monthly
school-level attendance data 2021–2023 (EMIS), 1,840 schools. We estimate the
effect of the program on the attendance rate (share of school days attended,
0–1 scale).

## Team
PI: R. Demo (economist, fictional). RA: also fictional. Sole-authored for
demo purposes.

## Key paths
- Draft: `paper/draft.qmd` (Quarto, renders to PDF)
- Bibliography: `paper/references.bib`
- Output tables (LaTeX, produced by `code/03_analysis.R`):
  - `outputs/tab1_summary.tex` — baseline summary stats and balance
  - `outputs/tab2_main.tex` — main DiD estimates (3 specifications)
  - `outputs/tab3_het.tex` — heterogeneity (sex, urban/rural)
- AI-writing workflow: `wb-paper/` (profile, critics, log)

## Facts agents must not get wrong
- Outcome is the attendance *rate* (0–1); report effects in percentage points.
- Design is a two-period district-level DiD; **not** randomized. Rollout
  order was set by the ministry (poorer districts first).
- Preferred specification: Table 2, column 2 (with school controls).
- Data cannot leave the project folder; no external uploads.

## Status (as of demo date)
Full draft exists (`paper/draft.qmd`), pre-submission stage, targeting a
World Bank Policy Research Working Paper. The draft has NOT been through
review yet.
