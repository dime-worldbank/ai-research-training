# =============================================================================
# paths.py
#
# What this file does:
#   Defines where every folder in the project is, in ONE place.
#   All other scripts get their folder locations from here, so if a folder
#   is ever moved or renamed, it only needs to be changed in this file.
#
#   The paths are worked out relative to where this file lives, so the
#   project works on any computer without anyone editing file paths.
# =============================================================================

from pathlib import Path

# The project's top folder. This file is in code/utils/, so we go up two levels.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# --- Data folders ---
DATA = PROJECT_ROOT / "data"
DATA_ORIGINAL = DATA / "original"  # Raw data exactly as received. Never edit.
DATA_CLEANED = DATA / "cleaned"    # Data after cleaning (created by code/cleaning)
DATA_FINAL = DATA / "final"        # Analysis-ready data (created by code/construct)

# --- Output folders ---
OUTPUT = PROJECT_ROOT / "output"
OUTPUT_TABLES = OUTPUT / "tables"
OUTPUT_FIGURES = OUTPUT / "figures"


def make_output_folders():
    """Create the folders that scripts write to, in case they do not exist yet."""
    for folder in [DATA_CLEANED, DATA_FINAL, OUTPUT_TABLES, OUTPUT_FIGURES]:
        folder.mkdir(parents=True, exist_ok=True)
