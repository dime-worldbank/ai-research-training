# Reproduce Manual Exhibits

`reproduce-manual-exhibit` is an AI-agent skill for converting manually
prepared tables and figures into reproducible Stata, R, or Python workflows.
It works with reference exhibits in Excel, Word, PDF, or image files.

The goal is to replace manual calculations, copying, chart editing, and
formatting with code while making the smallest practical change to the project.

## Quick start

Copy the complete `reproduce-manual-exhibit/` folder into the skills directory
of your project. Do not copy only `SKILL.md`; the skill also uses its
`references/` and `scripts/` folders.

```text
your-project/
└── .agents/
    └── skills/
        └── reproduce-manual-exhibit/
            ├── SKILL.md
            ├── references/
            └── scripts/
```

The `.agents/skills/` path is a convention. Use another location if required
by your AI agent.

Open the research project in VS Code or your AI coding tool. The agent can
inspect the project to identify relevant files. Mention filenames or paths only
when it is not clear which data, workbook, or exhibit it should use.

## Example prompts

**Figure in R**

```text
Use the reproduce-manual-exhibit skill to reproduce the Excel figure in this project using R. 
```

**Table in Stata**

```text
Use the reproduce-manual-exhibit skill to automate Table 1 in the paper using Stata. Output the table as an RTF file.
```

**Table from an Excel workbook with no code**

```text
Use the reproduce-manual-exhibit skill to reproduce Table 1 in analysis.xlsx using R, starting from source-data.csv. Output the table as an XLSX file.
```

**When the relevant file is ambiguous**

Name the file in the prompt:

```text
Use the reproduce-manual-exhibit skill to reproduce the exhibits in analysis.xlsx using R.
```

## How it works

1. The agent inspects the reference exhibit, data, existing code, and project
   conventions.
2. It settles the language and one output format. It uses the language you
   request; otherwise it keeps the language the project already uses; if there
   is none, it chooses one and says why. If no figure format is established,
   it uses PNG.
3. It recovers the calculations, plotting data, labels, ordering, and other
   display choices. Missing analytical information is reported rather than
   guessed.
4. It adds or updates only the code needed to regenerate the exhibit.
5. It validates the data and calculations first, then performs one focused
   visual inspection of the output.
6. It reports what changed, the numbered run order, the expected output, what
   can be deleted, and the validation status.

## Output choices

Choose the format used by the next stage of the research workflow:

| Use | Typical output |
|---|---|
| Figure | PNG |
| Word table | RTF or DOCX |
| LaTeX paper | TEX |
| Excel workflow | XLSX |
| Web report | HTML |

By default, the agent creates only the final file you requested. 

## Running and testing

When R, Python, or Stata is available, the agent runs the code and fixes errors
before delivery. The final response explains the run order as simple numbered
actions, for example:

1. Run `01-clean-data.R`.
2. Run `02-make-figure.R`.

It also lists the working folder and required packages. It won't give you
terminal commands as the main instructions.

If the agent cannot run Stata, it will ask you to run the do-file and return:

- the first error message;
- the Stata return code, such as `r(198)`;
- the nearby log lines showing the command that failed.

The agent then revises the code, and this loop continues until the do-file
runs successfully.

## Final handoff

The agent should finish with:

- **What changed:** files created or modified and the generated output.
- **New workflow:** working directory, required software, numbered run order,
  inputs, and output location.
- **Validation status:** what was checked and anything still unverified or
  unresolved.
- **What can be deleted:** exact paths of files that the new workflow has made
  obsolete, or a statement that nothing should be deleted. The agent only
  recommends candidates and does not delete them automatically.
