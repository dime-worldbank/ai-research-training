# =============================================================================
# construct_analysis_data.py
#
# What this script does:
#   Combines the cleaned household survey with the cleaned district
#   information, and creates the new variables (indicators) used in the
#   analysis.
#
# Inputs:  data/cleaned/household_survey_clean.csv
#          data/cleaned/district_info_clean.csv
# Output:  data/final/analysis_data.csv
#
# New variables created (see documentation/codebook.md):
#   - income_per_person : monthly income divided by household size
#   - income_group      : "Low", "Middle" or "High" based on income per person
# =============================================================================

import sys
from pathlib import Path

import pandas as pd

# Let this script find the shared paths file in code/utils/
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "utils"))
from paths import DATA_CLEANED, DATA_FINAL, make_output_folders


def main():
    make_output_folders()

    # --- Load the cleaned data -----------------------------------------------
    survey = pd.read_csv(DATA_CLEANED / "household_survey_clean.csv")
    districts = pd.read_csv(DATA_CLEANED / "district_info_clean.csv")

    # --- Combine the two files -----------------------------------------------
    # Each household gets the information about the district it lives in.
    # "validate" makes the code stop if a district appears twice in the
    # district file, which would create duplicate households.
    data = survey.merge(districts, on="district", how="left", validate="many_to_one")

    # Check that every household found its district. Stop if not.
    if data["region"].isna().any():
        missing = data.loc[data["region"].isna(), "district"].unique()
        raise ValueError(f"These districts were not found in the district file: {missing}")

    # --- Create new variables ------------------------------------------------
    # Income per person makes large and small households comparable.
    data["income_per_person"] = (data["monthly_income"] / data["hh_size"]).round(1)

    # Put households into three income groups based on income per person.
    # Households with missing income are left without a group.
    data["income_group"] = pd.cut(
        data["income_per_person"],
        bins=[0, 75, 150, float("inf")],
        labels=["Low", "Middle", "High"],
    )

    # --- Save the analysis-ready data ----------------------------------------
    data.to_csv(DATA_FINAL / "analysis_data.csv", index=False)
    print(f"  Saved analysis data with {len(data)} households to data/final/")


# This makes it possible to run this script on its own.
if __name__ == "__main__":
    main()
