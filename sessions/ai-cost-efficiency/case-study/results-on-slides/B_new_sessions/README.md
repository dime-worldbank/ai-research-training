# Cash Plus RCT

Replication code and data for a cluster-randomized evaluation of a "cash plus" program in rural
Kenya. The program pairs unconditional cash transfers with nutrition coaching for households with
children under five. The sample is 1,200 households in 60 villages, and treatment is assigned at the
village level. See [`paper/abstract.md`](paper/abstract.md) for a summary of the findings.

## Repository structure

```
.
├── .here                     # Marks the project root for here::here()
├── code/
│   ├── 00_main.R             # Runs the full pipeline in order
│   ├── 01_clean.R            # Merges baseline and endline, builds derived variables
│   ├── 02_balance.R          # Baseline balance table by treatment arm
│   └── 03_analysis.R         # Main ITT estimates
├── data/
│   └── raw/
│       ├── baseline_hh.csv   # Baseline household survey (1,200 households)
│       └── endline_hh.csv    # Endline household outcomes (1,200 households)
├── docs/
│   ├── pre_analysis_plan.md  # Registered pre-analysis plan (AEA RCT Registry, v3)
│   ├── field_notes_2025.md   # Daily notes from the 2025 data collection
│   └── old_drafts/           # Earlier paper drafts (v1, v2)
└── paper/
    └── abstract.md
```

`data/clean/` and `output/` are created when the pipeline runs.

## Requirements

- R (≥ 4.0 recommended)
- R packages: `here`, `dplyr`, `fixest`

```r
install.packages(c("here", "dplyr", "fixest"))
```

## Running the analysis

Run the full pipeline from anywhere inside the project. `here::here()` uses the `.here` file to
find the project root.

```r
source("code/00_main.R")
```

Or from the shell:

```sh
Rscript code/00_main.R
```

The scripts must run in order, since each one reads the previous script's output.

| Step | Script | Input | Output |
|------|--------|-------|--------|
| 1 | `01_clean.R` | `data/raw/*.csv` | `data/clean/hh_panel.rds` |
| 2 | `02_balance.R` | `data/clean/hh_panel.rds` | `output/balance_table.csv` |
| 3 | `03_analysis.R` | `data/clean/hh_panel.rds` | `output/itt_table.tex` |

## What each step does

**Cleaning (`01_clean.R`).** Reads the baseline and endline files and creates `log_cons` (log of
baseline consumption per capita) and `large_hh` (household size ≥ 7). It then left-joins the endline
data onto the baseline by `hhid`.

**Balance (`02_balance.R`).** Runs a two-sample t-test comparing control and treatment means for
each of these baseline characteristics: household size, female head, head age, head years of
education, consumption per capita, food insecurity, number of children under five, livestock (TLU),
and distance to market.

**Analysis (`03_analysis.R`).** Estimates intent-to-treat effects with `fixest::feols`, with
standard errors clustered by `village_id`:

| Model | Outcome | Controls |
|-------|---------|----------|
| m1 | log endline consumption per capita | log baseline consumption |
| m2 | endline food insecurity | baseline food insecurity |
| m3 | endline child height-for-age z-score | none |

## Data

Both files are keyed on `hhid`.

**`baseline_hh.csv`**: `hhid`, `village_id`, `treatment` (0/1), `hh_size`, `head_female`,
`head_age`, `head_educ_yrs`, `consumption_pc`, `food_insecure`, `n_children_u5`, `livestock_tlu`,
`dist_market_km`

**`endline_hh.csv`**: `hhid`, `consumption_pc_el`, `food_insecure_el`, `child_haz_el`

## Pre-analysis plan

The registered pre-analysis plan is in [`docs/pre_analysis_plan.md`](docs/pre_analysis_plan.md). It
specifies more outcome families, controls (strata fixed effects), multiple-testing adjustments,
heterogeneity analyses and attrition checks than the code here currently implements.
