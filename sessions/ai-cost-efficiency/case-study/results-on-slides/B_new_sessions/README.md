# Cash Plus RCT

Replication code for a cluster-randomized evaluation of a "cash plus" program in rural Kenya.
The program pairs unconditional cash transfers with nutrition coaching for households with
children under five. Randomization is at the village level: 60 villages and 1,200 households,
according to the abstract. See `paper/abstract.md` for the headline findings.

## Repository layout

```
.
├── .here                     # marks the project root for here::here()
├── code/
│   ├── 00_main.R             # runs the full pipeline in order
│   ├── 01_clean.R            # merges baseline + endline, builds derived variables
│   ├── 02_balance.R          # baseline balance table by treatment arm
│   └── 03_analysis.R         # main ITT regressions
├── data/
│   ├── raw/                  # input survey data (do not edit)
│   │   ├── baseline_hh.csv
│   │   └── endline_hh.csv
│   └── clean/                # created by 01_clean.R
├── output/                   # created by 02_balance.R / 03_analysis.R
├── docs/
│   ├── pre_analysis_plan.md  # registered PAP (AEA RCT Registry, v3)
│   ├── field_notes_2025.md   # daily notes from 2025 data collection
│   └── old_drafts/           # superseded paper drafts (v1, v2)
└── paper/
    └── abstract.md
```

## Requirements

- R (any recent version)
- Packages: `here`, `dplyr`, `fixest`

```r
install.packages(c("here", "dplyr", "fixest"))
```

## Running the pipeline

From anywhere inside the project:

```r
source(here::here("code", "00_main.R"))
```

or from a shell at the project root:

```sh
Rscript code/00_main.R
```

All paths go through `here::here()`, which finds the root via the `.here` file. You don't need to
set a working directory. Each script can also be run on its own, as long as the earlier scripts
have already produced their outputs.

| Step | Script | Reads | Writes |
|------|--------|-------|--------|
| 1 | `01_clean.R` | `data/raw/baseline_hh.csv`, `data/raw/endline_hh.csv` | `data/clean/hh_panel.rds` |
| 2 | `02_balance.R` | `data/clean/hh_panel.rds` | `output/balance_table.csv` |
| 3 | `03_analysis.R` | `data/clean/hh_panel.rds` | `output/itt_table.tex` |

## Data

Both raw files contain one row per household (1,200 rows each) and are keyed on `hhid`.

**`baseline_hh.csv`**

| Variable | Description |
|----------|-------------|
| `hhid` | Household ID (e.g. `HH00001`) |
| `village_id` | Village ID (e.g. `V018`); this is the randomization and clustering unit |
| `treatment` | 1 = cash plus arm, 0 = control |
| `hh_size` | Household size |
| `head_female` | 1 if the household head is female |
| `head_age` | Age of the household head |
| `head_educ_yrs` | Years of education of the household head |
| `consumption_pc` | Consumption per capita |
| `food_insecure` | 1 if the household is food insecure |
| `n_children_u5` | Number of children under five |
| `livestock_tlu` | Livestock holdings (tropical livestock units) |
| `dist_market_km` | Distance to the nearest market (km) |

**`endline_hh.csv`**

| Variable | Description |
|----------|-------------|
| `hhid` | Household ID |
| `consumption_pc_el` | Endline consumption per capita |
| `food_insecure_el` | Endline food insecurity indicator |
| `child_haz_el` | Endline child height-for-age z-score |

`01_clean.R` left-joins endline onto baseline by `hhid` and adds two variables:
`log_cons` (log baseline consumption per capita) and `large_hh` (1 if `hh_size >= 7`).

## Analysis

- **Balance** (`02_balance.R`): runs a two-sample t-test by treatment arm for each baseline
  characteristic and reports the control mean, the treatment mean, and the p-value.
- **ITT** (`03_analysis.R`): runs three OLS regressions with `fixest::feols`, with standard
  errors clustered by `village_id`:
  1. log endline consumption per capita on treatment and log baseline consumption
  2. endline food insecurity on treatment and baseline food insecurity
  3. endline child height-for-age on treatment (there is no baseline value for this outcome)

## Differences from the pre-analysis plan

The current code covers only part of `docs/pre_analysis_plan.md`. Not yet implemented:

- Strata fixed effects. The raw data has no strata variable.
- Sharpened q-values for multiple hypothesis testing within each outcome family.
- Heterogeneity by female headship, baseline poverty, and distance to market. The abstract
  reports heterogeneous effects, but no script produces them.
- Attrition tests and Lee bounds.
- Outcome families 4–10 (livestock, female decision-making, schooling, health expenditure,
  savings, debt, labor supply). The endline file has no variables for these.

`large_hh` is created in `01_clean.R` but is not used anywhere yet.
