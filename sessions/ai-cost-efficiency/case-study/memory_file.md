# Cash Plus RCT

Cluster RCT of cash transfers + nutrition coaching in rural Kenya. 60 villages (30 treated), 1,200 households. Randomized at village level.

## Language and packages
- R only: dplyr, fixest, here. Paths built with `here::here()`.

## Folder structure
- `code/00_main.R`: runs everything in order (01_clean → 02_balance → 03_analysis)
- `code/01_clean.R`: reads raw CSVs, saves `data/clean/hh_panel.rds`
- `code/02_balance.R`: baseline balance table → `output/balance_table.csv`
- `code/03_analysis.R`: ITT regressions, SEs clustered by `village_id` → `output/itt_table.tex`
- `data/raw/`: `baseline_hh.csv`, `endline_hh.csv` (merge on `hhid`)
- `paper/abstract.md`: current abstract
- `docs/`: pre-analysis plan, field notes, old drafts. Not needed for coding tasks; don't read unless asked.

## Key variable names
- Treatment: `treatment` (0/1). Cluster: `village_id`. ID: `hhid`.
- Baseline: `hh_size`, `head_female`, `head_age`, `head_educ_yrs`, `consumption_pc`, `food_insecure`, `n_children_u5`, `livestock_tlu`, `dist_market_km`
- Created in 01_clean.R: `log_cons`, `large_hh`
- Endline: `consumption_pc_el`, `food_insecure_el`, `child_haz_el`

## Data 
Data 
