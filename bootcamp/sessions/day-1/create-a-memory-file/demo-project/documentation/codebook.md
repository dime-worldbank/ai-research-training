# Codebook

## Household survey (`household_survey.csv`)

| Variable | Description | Values |
|---|---|---|
| `household_id` | Unique ID for each household | 1001–1030 |
| `district` | District the household lives in | North Hills, Riverside, Lakeview, Central, Eastfield |
| `hh_size` | Number of people living in the household | Whole number |
| `monthly_income` | Total household income last month, in USD | Number. Raw data uses `-99` for "refused to answer" |
| `has_electricity` | Does the household have an electricity connection? | Raw: yes/no. Cleaned: 1 = yes, 0 = no |
| `survey_date` | Date of the interview | YYYY-MM-DD |

## District information (`district_info.csv`)

| Variable | Description | Values |
|---|---|---|
| `district` | District name (used to combine with the household survey) | Text |
| `region` | Region the district belongs to | North, South, East |
| `population` | Total district population | Whole number |
| `urban` | Is the district classified as urban? | 1 = urban, 0 = rural |

## Constructed variables (`data/final/analysis_data.csv`)

These are created in `code/cleaning/` and `code/construct/`.

| Variable | Description | How it is calculated |
|---|---|---|
| `area_type` | Urban or rural, as text | `urban` 1 → "Urban", 0 → "Rural" |
| `income_per_person` | Monthly income per household member, in USD | `monthly_income / hh_size`, rounded to 1 decimal |
| `income_group` | Income category based on income per person | Low: 0–75, Middle: 75–150, High: above 150. Blank if income is missing |
