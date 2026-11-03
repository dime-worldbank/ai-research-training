# Cash Plus RCT

Cash Plus is a cluster randomized controlled trial of cash transfers combined with nutrition coaching in rural Kenya. Sixty villages (30 treated) and 1,200 households were randomized at the village level, and the analysis estimates intention-to-treat effects on household consumption, food insecurity, and child height-for-age using baseline (2024) and endline (2025) surveys. Standard errors are clustered at the village level.

## Folder structure

```
code/
  00_main.R        runs the full pipeline in order
  01_clean.R       reads raw CSVs, saves data/clean/hh_panel.rds
  02_balance.R     baseline balance table -> output/balance_table.csv
  03_analysis.R    ITT regressions -> output/itt_table.tex
data/
  raw/             baseline_hh.csv, endline_hh.csv (merge on hhid)
  clean/           hh_panel.rds (created by 01_clean.R)
output/            balance and ITT tables
paper/
  abstract.md      current abstract
docs/              pre-analysis plan, field notes, old drafts
```

## How to run

Requirements: R with the packages `dplyr`, `fixest`, and `here`.

From the project root, run:

```r
source("code/00_main.R")
```

or from a shell:

```bash
Rscript code/00_main.R
```

This runs the cleaning, balance, and analysis scripts in order. Paths are built with `here::here()`, so the project root must be the working directory or inside the project.

## Data availability

- **Source:** Cash Plus household surveys, collected by the project's field team. The data are fictional and were generated for a training exercise.
- **Years:** baseline 2024, endline 2025.
- **Unit:** household (`hhid`), nested in villages (`village_id`).
- **Access:** the de-identified household files are in `data/raw/` and can be shared publicly. No personally identifiable information is stored in this project.
