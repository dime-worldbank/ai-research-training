# =============================================================================
# run_all.py
#
# What this script does:
#   Runs the whole project from start to finish, in the right order:
#     1. Cleaning     - fixes problems in the raw data
#     2. Construct    - combines the data and creates new variables
#     3. Analysis     - makes the tables and figures
#
#   Run it from a terminal with:   python run_all.py
#
#   Each script can also be run on its own, but they depend on each other,
#   so the earlier steps must have been run at least once first.
# =============================================================================

import runpy
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
CODE = PROJECT_ROOT / "code"

# The scripts to run, in the order they must be run.
STEPS = [
    CODE / "cleaning" / "clean_household_survey.py",
    CODE / "cleaning" / "clean_district_info.py",
    CODE / "construct" / "construct_analysis_data.py",
    CODE / "analysis" / "summary_tables.py",
    CODE / "analysis" / "figures.py",
]


def main():
    for script in STEPS:
        print(f"Running {script.relative_to(PROJECT_ROOT).as_posix()}")
        runpy.run_path(str(script), run_name="__main__")
    print("\nDone! All steps ran successfully. Results are in the output/ folder.")


if __name__ == "__main__":
    main()
