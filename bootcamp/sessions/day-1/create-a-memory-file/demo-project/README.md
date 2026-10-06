# Household Survey Demo Project

A small, made-up research project used in the AI-Enabled Research Bootcamp.
It looks at household income and electricity access across five districts.

The data is fictional and the analysis is deliberately simple. The point of the
project is to have a realistic folder structure to practice on.

## Folder structure

```
demo-project/
├── README.md               <- You are here
├── requirements.txt        <- Python packages the project needs
├── run_all.py              <- Runs the whole project from start to finish
├── data/
│   ├── original/           <- Raw data exactly as received. NEVER edit these files.
│   ├── cleaned/            <- Data after cleaning (created by code/cleaning)
│   └── final/              <- Analysis-ready data (created by code/construct)
├── code/
│   ├── cleaning/           <- Fix problems in the raw data, one script per raw file
│   ├── construct/          <- Combine data and create new variables
│   ├── analysis/           <- Make tables and figures
│   └── utils/              <- Shared helpers (all folder paths are defined in paths.py)
├── output/
│   ├── tables/             <- Summary tables (CSV, open in Excel)
│   └── figures/            <- Charts (PNG)
└── documentation/
    ├── codebook.md         <- What every variable means
    └── data-cleaning-log.md <- Why each cleaning decision was made
```

Data flows in one direction:
`data/original` → **cleaning** → `data/cleaned` → **construct** → `data/final` → **analysis** → `output`

## How to run the project

Follow these steps exactly. You only need to do steps 1–4 once.

### Step 1: Check that Python is installed

Open a terminal:

- **Windows:** Press the Windows key, type `PowerShell`, and press Enter.
- **Mac:** Press Cmd + Space, type `Terminal`, and press Enter.
- **VS Code:** In the top menu, click *Terminal* → *New Terminal*.

Type the following and press Enter:

```
python --version
```

You should see something like `Python 3.12.4`. Any version 3.9 or newer is fine.

- If you see an error on **Mac**, try `python3 --version` instead. If that works,
  type `python3` everywhere this guide says `python`.
- If neither works, install Python from <https://www.python.org/downloads/>.
  On Windows, **tick the box "Add python.exe to PATH"** during installation.
  Close and reopen the terminal afterwards.

### Step 2: Go to the project folder in the terminal

Type `cd ` (with a space after it), then drag the `demo-project` folder from your
file explorer into the terminal window and press Enter. It should look something like:

```
cd C:\Users\yourname\Downloads\demo-project
```

If you opened the `demo-project` folder in VS Code and used its terminal, you are already there.

### Step 3 (recommended): Create a virtual environment

A virtual environment keeps this project's packages separate from everything
else on your computer. Run:

```
python -m venv .venv
```

Then activate it:

- **Windows (PowerShell):** `.venv\Scripts\Activate.ps1`
- **Windows (Command Prompt):** `.venv\Scripts\activate.bat`
- **Mac:** `source .venv/bin/activate`

You should now see `(.venv)` at the start of the line in the terminal.
You need to activate it again each time you open a new terminal.

### Step 4: Install the required packages

```
python -m pip install -r requirements.txt
```

This installs `pandas` (for working with data tables) and `matplotlib` (for charts).
It can take a minute.

### Step 5: Run the project

```
python run_all.py
```

You should see each script listed as it runs, ending with:

```
Done! All steps ran successfully. Results are in the output/ folder.
```

The tables are now in `output/tables/` and the charts in `output/figures/`.

## Troubleshooting

| Problem | Solution |
|---|---|
| `python` is not recognized / command not found | See Step 1. On Mac try `python3`. On Windows reinstall Python and tick "Add python.exe to PATH". |
| `pip` is not recognized | Always use `python -m pip ...` instead of just `pip ...`. |
| `ModuleNotFoundError: No module named 'pandas'` | The packages are not installed in the Python you are using. Activate the virtual environment (Step 3) and run Step 4 again. |
| `No such file or directory: 'run_all.py'` | The terminal is not in the project folder. Repeat Step 2. |
| `FileNotFoundError` for a file in `data/cleaned` or `data/final` | You ran one script on its own before the earlier steps. Run `python run_all.py` instead. |
