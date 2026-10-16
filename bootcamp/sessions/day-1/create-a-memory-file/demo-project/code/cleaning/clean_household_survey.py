# =============================================================================
# clean_household_survey.py
#
# What this script does:
#   Cleans the raw household survey so it is consistent and ready to use.
#
# Input:   data/original/household_survey.csv
# Output:  data/cleaned/household_survey_clean.csv
#
# Cleaning steps (see also documentation/data-cleaning-log.md):
#   1. Remove households that were entered twice
#   2. Replace the code -99 (meaning "refused to answer") with a blank value
#   3. Make the electricity answers consistent (Yes / YES / yes -> yes)
#   4. Store the survey date as a real date
# =============================================================================

import sys
from pathlib import Path

import pandas as pd

# Let this script find the shared paths file in code/utils/
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "utils"))
from paths import DATA_ORIGINAL, DATA_CLEANED, make_output_folders


def main():
    make_output_folders()

    # --- Load the raw data ---------------------------------------------------
    survey = pd.read_csv(DATA_ORIGINAL / "household_survey.csv")
    print(f"  Loaded {len(survey)} rows from the raw household survey")

    # --- Step 1: Remove duplicate households ---------------------------------
    # Each household should appear only once. If the exact same row appears
    # more than once, we keep the first one.
    rows_before = len(survey)
    survey = survey.drop_duplicates()
    print(f"  Removed {rows_before - len(survey)} duplicate row(s)")

    # Check that every household ID is now unique. Stop if not.
    if survey["household_id"].duplicated().any():
        raise ValueError("Some household IDs still appear more than once!")

    # --- Step 2: Replace -99 with a blank (missing) value --------------------
    # In this survey, -99 means the respondent refused to answer.
    # Leaving -99 in place would wrongly pull down average income.
    survey["monthly_income"] = survey["monthly_income"].mask(survey["monthly_income"] == -99)

    # --- Step 3: Make electricity answers consistent -------------------------
    # The raw data has "yes", "Yes", "YES", "no", "No". We make them all
    # lowercase and then turn them into 1 (yes) and 0 (no).
    survey["has_electricity"] = (
        survey["has_electricity"].str.strip().str.lower().map({"yes": 1, "no": 0})
    )

    # --- Step 4: Store the survey date as a date -----------------------------
    survey["survey_date"] = pd.to_datetime(survey["survey_date"])

    # --- Save the cleaned data -----------------------------------------------
    survey.to_csv(DATA_CLEANED / "household_survey_clean.csv", index=False)
    print(f"  Saved {len(survey)} cleaned rows to data/cleaned/")


# This makes it possible to run this script on its own.
if __name__ == "__main__":
    main()
