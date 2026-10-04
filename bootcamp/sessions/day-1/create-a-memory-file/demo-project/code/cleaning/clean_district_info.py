# =============================================================================
# clean_district_info.py
#
# What this script does:
#   Cleans the district information table so district names match the names
#   used in the household survey. This is needed to combine the two files.
#
# Input:   data/original/district_info.csv
# Output:  data/cleaned/district_info_clean.csv
#
# Cleaning steps:
#   1. Remove extra spaces around district names
#   2. Write district names in "Title Case" (e.g. "CENTRAL" -> "Central")
#   3. Turn the 1/0 urban column into the words "Urban" and "Rural"
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
    districts = pd.read_csv(DATA_ORIGINAL / "district_info.csv")
    print(f"  Loaded {len(districts)} districts from the raw district file")

    # --- Steps 1 and 2: Tidy the district names ------------------------------
    # The raw file has names like "North Hills " (extra space), "riverside"
    # and "CENTRAL". We tidy them so they match the household survey exactly.
    districts["district"] = districts["district"].str.strip().str.title()

    # --- Step 3: Give the urban column readable labels -----------------------
    districts["area_type"] = districts["urban"].map({1: "Urban", 0: "Rural"})

    # --- Save the cleaned data -----------------------------------------------
    districts.to_csv(DATA_CLEANED / "district_info_clean.csv", index=False)
    print("  Saved cleaned district file to data/cleaned/")


# This makes it possible to run this script on its own.
if __name__ == "__main__":
    main()
