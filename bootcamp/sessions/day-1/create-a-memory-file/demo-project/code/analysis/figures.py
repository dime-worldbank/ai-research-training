# =============================================================================
# figures.py
#
# What this script does:
#   Creates simple charts from the analysis data and saves them as images.
#
# Input:   data/final/analysis_data.csv
# Outputs: output/figures/income_by_district.png
#          output/figures/electricity_by_area_type.png
# =============================================================================

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Save charts to files without opening a window
import matplotlib.pyplot as plt
import pandas as pd

# Let this script find the shared paths file in code/utils/
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "utils"))
from paths import DATA_FINAL, OUTPUT_FIGURES, make_output_folders

# One colour used for all charts so they look consistent
BAR_COLOUR = "#2a6f97"


def main():
    make_output_folders()

    data = pd.read_csv(DATA_FINAL / "analysis_data.csv")

    # --- Figure 1: Average monthly income per district -----------------------
    income = data.groupby("district")["monthly_income"].mean().sort_values()

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(income.index, income.values, color=BAR_COLOUR)
    ax.set_xlabel("Average monthly income (USD)")
    ax.set_title("Average household income by district")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUTPUT_FIGURES / "income_by_district.png", dpi=150)
    plt.close(fig)

    # --- Figure 2: Share of households with electricity, urban vs rural ------
    # Multiply by 100 to show percentages instead of shares (0.5 -> 50%).
    electricity = data.groupby("area_type")["has_electricity"].mean() * 100

    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(electricity.index, electricity.values, color=BAR_COLOUR, width=0.5)
    ax.set_ylabel("Households with electricity (%)")
    ax.set_ylim(0, 100)
    ax.set_title("Electricity access: urban vs rural")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUTPUT_FIGURES / "electricity_by_area_type.png", dpi=150)
    plt.close(fig)

    print("  Saved 2 figures to output/figures/")


# This makes it possible to run this script on its own.
if __name__ == "__main__":
    main()
