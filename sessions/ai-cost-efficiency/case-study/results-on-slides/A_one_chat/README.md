# Cash Plus RCT

Replication code for a cluster-randomized evaluation of a cash plus program in rural Kenya. The
program combines unconditional cash transfers with nutrition coaching for households with
children under five. Villages are the unit of randomization: 1,200 households in 60 villages.

## Repository structure

```
code/
  00_main.R        Runs the full pipeline in order
  01_clean.R       Merges baseline and endline, builds derived variables
  02_balance.R     Baseline balance table by treatment arm
  03_analysis.R    Main ITT estimates, SEs clustered by village
data/
  raw/             Baseline and endline household surveys (CSV)
  clean/           Created by 01_clean.R
output/            Created by the pipeline (tables)
docs/
  pre_analysis_plan.md   Registered pre-analysis plan (AEA RCT Registry, v3)
  field_notes_2025.md    Daily notes from 2025 data collection
  old_drafts/            Earlier paper drafts
paper/
  abstract.md
```

## Requirements

R with the packages `here`, `dplyr`, and `fixest`:

```r
install.packages(c("here", "dplyr", "fixest"))
```

The empty `.here` file marks the project root, so the scripts find their files from any
working directory.

## Running the pipeline

From the project root:

```sh
Rscript code/00_main.R
```

Or run the scripts one at a time, in order. Each one reads the output of the one before it.

| Script | Reads | Writes |
|---|---|---|
| `01_clean.R` | `data/raw/baseline_hh.csv`, `data/raw/endline_hh.csv` | `data/clean/hh_panel.rds` |
| `02_balance.R` | `data/clean/hh_panel.rds` | `output/balance_table.csv` |
| `03_analysis.R` | `data/clean/hh_panel.rds` | `output/itt_table.tex` |

## Data

Both raw files have one row per household, keyed by `hhid`.

**`baseline_hh.csv`**

| Variable | Description |
|---|---|
| `hhid` | Household ID |
| `village_id` | Village ID (cluster) |
| `treatment` | 1 = cash plus, 0 = control |
| `hh_size` | Household size |
| `head_female` | Female household head (0/1) |
| `head_age` | Age of household head |
| `head_educ_yrs` | Years of schooling of household head |
| `consumption_pc` | Consumption per capita |
| `food_insecure` | Food insecure (0/1) |
| `n_children_u5` | Number of children under five |
| `livestock_tlu` | Livestock holdings (tropical livestock units) |
| `dist_market_km` | Distance to nearest market (km) |

**`endline_hh.csv`**

| Variable | Description |
|---|---|
| `hhid` | Household ID |
| `consumption_pc_el` | Consumption per capita, endline |
| `food_insecure_el` | Food insecure (0/1), endline |
| `child_haz_el` | Child height-for-age z-score, endline |

`01_clean.R` adds `log_cons` (log baseline consumption per capita) and `large_hh` (household
size of 7 or more).

## Known gaps relative to the pre-analysis plan

- The balance table uses household-level t-tests. These are not clustered by village.
- The pre-analysis plan's primary specification includes strata fixed effects. The data has no
  strata variable, and `03_analysis.R` leaves them out.
- The plan lists ten outcome families. The code covers three so far (consumption, food
  insecurity, child height-for-age), with no multiple-testing adjustment, heterogeneity, or
  attrition analysis yet.
