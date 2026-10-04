# =============================================================================
# zip_demo_project.py
#
# What this script does:
#   Packs everything in the demo-project folder into one zip file,
#   memory-skill-demo-project.zip, saved next to this script.
#   When unzipped, the files end up in a single "demo-project" folder.
#
#   Python cache files and virtual environments are left out.
#
#   Run it with:   python zip_demo_project.py
# =============================================================================

import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE / "demo-project"
ZIP_FILE = HERE / "memory-skill-demo-project.zip"

# Folders that should never be included in the zip
SKIP_FOLDERS = {"__pycache__", ".venv", "venv"}


def main():
    with zipfile.ZipFile(ZIP_FILE, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(PROJECT.rglob("*")):
            relative = path.relative_to(PROJECT)
            if not path.is_file() or SKIP_FOLDERS.intersection(relative.parts):
                continue
            # Store each file under "demo-project/..." inside the zip
            zf.write(path, Path(PROJECT.name) / relative)

    print(f"Created {ZIP_FILE.name}")


if __name__ == "__main__":
    main()
