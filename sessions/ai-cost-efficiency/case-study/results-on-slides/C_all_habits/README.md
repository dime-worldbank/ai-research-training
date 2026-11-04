# Cash Plus RCT

Cluster-randomized trial of cash transfers plus nutrition coaching in rural Kenya: 60 villages (30 treated) and 1,200 households, randomized at the village level. The code cleans the baseline (2024) and endline (2025) household surveys, checks baseline balance, and estimates intent-to-treat effects with standard errors clustered by village.

## Folder structure

```
code/     R scripts; 00_main.R runs the pipeline in order
  00_main.R      runs 01 → 02 → 03
  01_clean.R     reads raw CSVs, saves data/clean/hh_panel.rds
  02_balance.R   baseline balance table → output/balance_table.csv
  03_analysis.R  ITT regressions → output/itt_table.tex
data/raw/   baseline_hh.csv, endline_hh.csv (merged on hhid)
paper/      abstract.md
docs/       pre-analysis plan, field notes, old drafts (not needed to run the code)
```

## Running the code

Requirements: R with the `dplyr`, `fixest`, and `here` packages.

1. Open R or RStudio with the project root as the working directory (the folder containing `.here`), or launch from a terminal in that folder.
2. Run the full pipeline:

   ```r
   source("code/00_main.R")
   ```

   or from a shell:

   ```sh
   Rscript code/00_main.R
   ```

Paths are built with `here::here()`, so the scripts run from any working directory inside the project. Outputs are written to `data/clean/` and `output/`.

## Data availability

- **Source:** Cash Plus household surveys, collected by the project's field team. The data are fictional, generated for a training exercise.
- **Years:** baseline 2024, endline 2025.
- **Unit:** household (`hhid`), nested in villages (`village_id`).
- **Access:** `data/raw/` contains de-identified household data and is included in this repository. No personally identifiable information is stored.
