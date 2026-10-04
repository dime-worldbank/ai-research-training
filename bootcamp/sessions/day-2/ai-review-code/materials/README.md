# Demo project

A small practice project for the `research-code-review` skill. All data are
synthetic. The code contains common research-code mistakes, and the task is to
find them with the skill and fix the ones you approve.

| Project | What's inside | What it does |
|---|---|---|
| [water-pilot.zip](water-pilot.zip) | `code/` (one Stata do-file, three R scripts), `data/`, `outputs/` | Impact evaluation of a water conservation pilot in 12 districts: Stata assigns districts to treatment; R cleans the baseline and endline surveys, checks balance and attrition, and estimates treatment effects |

## Set up

1. Download the project and unzip it.
2. Download the skill, [research-code-review.zip](../skills/research-code-review.zip), and unzip it.
3. Inside the `water-pilot/` folder, create `.agents/skills/` and move the
   `research-code-review/` folder into it.
4. Open the `water-pilot/` folder in VS Code.

## Prompts

**Review the whole project**

```text
Read .agents/skills/research-code-review/SKILL.md and use it to review the research-code package in this folder.
```

**Review selected files**

```text
Read .agents/skills/research-code-review/SKILL.md and review only:
- code/01_randomize_treatment.do
- code/04_analyze_impacts.R
Treat this as a selected-files review.
```

When the agent asks about private data, you can confirm: the demo data are
synthetic.

The review itself only reads the code, so you don't need Stata or R installed.
To run the scripts after making fixes, you need Stata and R with `dplyr`,
`readr`, `haven`, `fixest`, and `ggplot2`.
