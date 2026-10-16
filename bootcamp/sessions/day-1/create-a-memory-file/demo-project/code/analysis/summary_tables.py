# =============================================================================
# summary_tables.py
#
# What this script does:
#   Creates simple summary tables from the analysis data and saves them as
#   CSV files that can be opened in Excel.
#
# Input:   data/final/analysis_data.csv
# Outputs: output/tables/summary_by_district.csv
#          output/tables/electricity_by_area_type.csv
#          output/tables/income_groups.csv
# =============================================================================

import sys
from pathlib import Path

import pandas as pd

# Let this script find the shared paths file in code/utils/
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "utils"))
from paths import DATA_FINAL, OUTPUT_TABLES, make_output_folders


def main():
    make_output_folders()

    data = pd.read_csv(DATA_FINAL / "analysis_data.csv")

    # --- Table 1: Key numbers for each district ------------------------------
    # For each district: number of households, average household size,
    # average monthly income and the share of households with electricity.
    by_district = (
        data.groupby(["region", "district"])
        .agg(
            households=("household_id", "count"),
            avg_hh_size=("hh_size", "mean"),
            avg_monthly_income=("monthly_income", "mean"),
            share_with_electricity=("has_electricity", "mean"),
        )
        .round(2)
        .reset_index()
    )
    by_district.to_csv(OUTPUT_TABLES / "summary_by_district.csv", index=False)

    # --- Table 2: Electricity access in urban vs rural districts -------------
    by_area = (
        data.groupby("area_type")
        .agg(
            households=("household_id", "count"),
            share_with_electricity=("has_electricity", "mean"),
        )
        .round(2)
        .reset_index()
    )
    by_area.to_csv(OUTPUT_TABLES / "electricity_by_area_type.csv", index=False)

    # --- Table 3: How many households are in each income group ---------------
    # "Missing" counts households whose income was not reported.
    income_groups = (
        data["income_group"]
        .fillna("Missing")
        .value_counts()
        .reindex(["Low", "Middle", "High", "Missing"], fill_value=0)
        .rename_axis("income_group")
        .reset_index(name="households")
    )
    income_groups.to_csv(OUTPUT_TABLES / "income_groups.csv", index=False)

    print("  Saved 3 summary tables to output/tables/")


# This makes it possible to run this script on its own.
if __name__ == "__main__":
    main()
