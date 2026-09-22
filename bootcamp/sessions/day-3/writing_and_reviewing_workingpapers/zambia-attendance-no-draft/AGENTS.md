# Project memory — Zambia School Meals Evaluation

## What this project is
Difference-in-differences evaluation of Zambia's Free School Meals Programme
(FSMP), rolled out in 46 of 92 districts in January 2022. Monthly
school-level attendance data 2021–2023 (EMIS), 1,840 schools. We estimate the
effect of the program on the attendance rate (share of school days attended,
0–1 scale).

## Team
PI: R. Demo (economist, fictional). Sole-authored for demo purposes.

## Key paths
- Concept note: `concept-note.md` (design, context, results summary)
- Bibliography: `paper/references.bib`
- Output tables (LaTeX, produced by `code/03_analysis.R`):
  - `outputs/tab1_summary.tex` — baseline summary stats and balance
  - `outputs/tab2_main.tex` — main DiD estimates (3 specifications;
    **column 2 preferred**)
  - `outputs/tab3_het.tex` — heterogeneity (sex, urban/rural)

## Facts agents must not get wrong
- Outcome is the attendance *rate* (0–1); report effects in percentage points.
- Design is a two-period district-level DiD; **not** randomized. Rollout
  order was set by the ministry (poorer districts first) — treat
  identification claims accordingly.
- Data cannot leave the project folder; no external uploads.

## Status (as of demo date)
Analysis complete, all tables final. **No draft exists yet.** Target output:
World Bank Policy Research Working Paper. Ministry scale-up decision expected
next year.
