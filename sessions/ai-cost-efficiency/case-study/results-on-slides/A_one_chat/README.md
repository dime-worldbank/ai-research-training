# Cash Plus RCT

Replication code for a cluster-randomized evaluation of a cash plus program in rural Kenya.
The program combines unconditional cash transfers with nutrition coaching for households with
children under five. Treatment was assigned at the village level: 60 villages, 1,200 households
(601 treatment, 599 control).

## Running the pipeline

From the project root:

```sh
Rscript code/00_main.R
```

This runs the three scripts below in order. Paths are resolved with `here::here()`, which finds
the project root through the `.here` file, so leave that file in place.

**Requirements:** R with the `here`, `dplyr` and `fixest` packages.

```r
install.packages(c("here", "dplyr", "fixest"))
```

## Scripts

| Script | What it does | Writes |
|---|---|---|
| `code/01_clean.R` | Merges baseline and endline on `hhid`; adds `log_cons` (log baseline consumption per capita) and `large_hh` (household size ≥ 7) | `data/clean/hh_panel.rds` |
| `code/02_balance.R` | Compares baseline means by arm, with t-test p-values | `output/balance_table.csv` |
| `code/03_analysis.R` | Estimates ITT effects on consumption, food insecurity and child height-for-age, with SEs clustered by village | `output/itt_table.tex` |

`data/clean/` and `output/` are created when the scripts run.

## Data

`data/raw/baseline_hh.csv` has one row per household:

| Variable | Description |
|---|---|
| `hhid` | Household ID |
| `village_id` | Village (unit of randomization) |
| `treatment` | 1 = cash plus arm, 0 = control |
| `hh_size` | Household size |
| `head_female` | Female household head (0/1) |
| `head_age` | Age of household head |
| `head_educ_yrs` | Years of schooling of household head |
| `consumption_pc` | Consumption per capita |
| `food_insecure` | Food insecure (0/1) |
| `n_children_u5` | Number of children under five |
| `livestock_tlu` | Livestock holdings, tropical livestock units |
| `dist_market_km` | Distance to nearest market, km |

`data/raw/endline_hh.csv` has one row per household, keyed on `hhid`. It holds
`consumption_pc_el`, `food_insecure_el` and `child_haz_el` (child height-for-age z-score).

## Documents

- `docs/pre_analysis_plan.md`: pre-analysis plan registered with the AEA RCT Registry (version 3)
- `docs/field_notes_2025.md`: daily notes from the 2025 data collection
- `docs/old_drafts/`: earlier paper drafts
- `paper/abstract.md`: current abstract

## Where the code differs from the pre-analysis plan

- The plan covers 10 outcome families. `03_analysis.R` estimates 3 of them.
- The plan includes strata fixed effects in the primary specification. The data has no strata
  variable, and the regressions leave them out.
- The plan calls for sharpened q-values within each outcome family, heterogeneity analysis,
  and attrition tests with Lee bounds. None of these are in the code yet.
- The balance table uses plain t-tests, which don't cluster by village.
