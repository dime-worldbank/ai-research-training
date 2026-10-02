# Demo projects

Three small practice projects for the `reproduce-manual-exhibit` skill. All
data are synthetic. Each project has a table or figure that was prepared by
hand, and the task is to make code produce it instead.

| Project | What's inside | Manual step |
|---|---|---|
| [r-demo.zip](r-demo.zip) | `01-clean-data.R`, `data/`, `output/manual-figure.xlsx` | Chart built and formatted in Excel |
| [excel-demo.zip](excel-demo.zip) | `analysis.xlsx`, `source-data.csv` | All calculations done with Excel formulas |
| [stata-demo.zip](stata-demo.zip) | `Clean Data.do`, `Analysis.do`, `data/`, `Coaching Pilot Paper.docx` | Table 1 typed into Word from Stata output |

## Set up

1. Download one project and unzip it.
2. Download the skill, [reproduce-manual-exhibit.zip](../skills/reproduce-manual-exhibit.zip), and unzip it.
3. Inside the project folder, create `.agents/skills/` and move the
   `reproduce-manual-exhibit/` folder into it.
4. Open the project folder in VS Code.

## Prompts

**r-demo**

```text
Use the reproduce-manual-exhibit skill to reproduce the Excel figure in this project using R. Generate one PNG and keep the project changes minimal.
```

**excel-demo** (replace "using R" with Python or Stata if you prefer)

```text
Use the reproduce-manual-exhibit skill to reproduce Table 1 in analysis.xlsx using R, starting from source-data.csv. Output the table as an XLSX file.
```

**stata-demo**

```text
Use the reproduce-manual-exhibit skill to automate Table 1 in the paper using Stata. Output the table as an RTF file.
```

If the agent can't find Stata, add its location to the prompt, for example
`Stata is at C:\Program Files\Stata18\StataMP-64.exe`.
