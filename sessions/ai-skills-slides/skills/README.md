# Prepare Slides

`prepare-slides` is a reusable AI-agent skill for creating, reviewing,
improving, and rebranding DECDI/DIME research presentations. It can:

- **Create a new deck:** from a manuscript, results folder, or other project files.
- **Improve an existing deck:** the content, structure, visuals, and branding.
- **Rebrand an existing deck:** while preserving its content arrangement and order.

It supports native PowerPoint, Quarto/Reveal.js, and Beamer/LaTeX. PDF and
rendered HTML decks can be reviewed, but editable source is needed for reliable
revisions.

This README explains how to set up and request work from the skill. The AI
agent should read `prepare-slides/SKILL.md`, which contains the detailed
workflow and identifies the references and templates it must use.

## Quick start

### 1. Download the complete skill

Download the whole `prepare-slides/` folder (not just `SKILL.md`) and place it
inside your project:

```
your-project/
├── .agents/
│   └── skills/                 ← create this folder if it does not exists
│       └── prepare-slides/     ← the folder you downloaded
│           ├── SKILL.md
│           ├── assets/
│           ├── branding/
│           └── references/
├── manuscript.pdf
└── results/
```

Create an `.agents/skills/` folder at the root of your project if one does not already exist. This folder name is a convention rather than a requirement. If your AI agent uses a designated skills directory, place the skill there and follow that agent’s installation instructions.

- You can clone the entire repository and copy the complete `prepare-slides/`
  folder into your project.
- [Download `prepare-slides.zip`](https://github.com/dime-worldbank/ai-research-training/releases/latest/download/prepare-slides.zip),
  unzip it, and place the `prepare-slides/` folder in your project's
  `.agents/skills/` folder.

### 2. Identify the source files

You do not need to reorganize an existing project or add research files to an
AI memory file. In your prompt, give the agent the exact paths to the relevant
manuscript, results folder, existing deck, or other supporting files.

Make sure the agent has permission to read those locations.

### 3. Describe the task

Use one of these prompts as a starting point.

**Create a deck from the contents of a project folder**

```text
Read prepare-slides/SKILL.md and use it to create a [30-minute] presentation using the relevant materials in
[YOUR PROJECT OR CONTENT FOLDER PATH]. The audience is [government policymakers]. Focus on the main findings and
policy implications. 
```

**Improve an existing deck**

```text
Read prepare-slides/SKILL.md and use it to improve [YOUR DECK FILENAME.pptx]. Use
[MANUSCRIPT, RESULTS, OR SUPPORTING-MATERIAL PATHS] to check the content.
```

**Rebrand an existing deck**

```text
Read prepare-slides/SKILL.md and follow it.

Rebrand [YOUR DECK FILENAME.pptx] using the bundled DECDI template and
branding guidance. 
```


## How the process works

1. **The agent proposes.** Depending on the task, this may be a new outline,
   an existing-deck review, visual alternatives, or a compact rebranding plan.
2. **You approve.** You can accept the recommendations or request changes.
3. **The agent produces and checks.** It creates or edits the presentation,
   renders or exports it, inspects the result, and delivers editable files.

For a narrow request such as “fix the overflow on slide 4,” the agent may use a
short confirmation instead of producing a full review.

## Research and approval safeguards

- The agent should not invent missing values, sources, or research findings.
- It should not reconstruct unreported data.
- If a manuscript is the only source for a figure or table, it should propose
  a faithful adaptation or an editable screenshot placeholder.
- No presentation files should be created, edited, or rebranded before the
  relevant proposal or requested change is approved.
- Claims can be independently checked only when the supporting manuscript,
  data, results, code, captions, or notes are available.

## Requirements

| Format | What you need |
|---|---|
| PowerPoint | An AI agent capable of editing native `.pptx` files; PowerPoint, LibreOffice Impress, or another compatible viewer |
| Quarto | The Quarto CLI and a web browser; R or Python only if the slides execute code in that language |
| Beamer | A TeX distribution with the required Beamer packages, or an Overleaf account |

The agent must be able to read project files, create or edit the selected
presentation format, run local build commands when needed, and inspect or
provide the rendered output.

### Quarto

Install the [Quarto CLI](https://quarto.org/docs/get-started/). Open a terminal
such as Terminal, PowerShell, or the VS Code terminal and run:

```sh
quarto check
```

Render a deck from its project folder with:

```sh
quarto render template.qmd
```

Missing Python or R components reported by `quarto check` do not matter when
the deck does not execute that language. If the deck executes R or Python, the
corresponding language and packages are required. The agent should report
missing dependencies and setup instructions rather than silently installing
packages during rendering.

### Beamer and LaTeX

Install MacTeX on macOS, MiKTeX or TeX Live on Windows, or TeX Live on Linux.
A sufficiently complete installation should include Beamer, Metropolis,
Montserrat, Lato, and the standard graphics and table packages.

Verify the compiler in a terminal:

```sh
pdflatex --version
```

Compile the main document twice so navigation and references are current:

```sh
pdflatex main.tex
pdflatex main.tex
```

### PowerPoint

Quarto and LaTeX are not required. The agent must have tooling capable of
creating or editing native `.pptx` files.

Install Montserrat and Lato on the computer used to open or present the deck.
The bundled PowerPoint template references these fonts but does not embed them.

### Optional: continue editing Beamer slides in Overleaf

Ask the agent to prepare a self-contained project with `main.tex`, relative
paths, and all required figures and bibliography files. Exclude temporary
files such as `.aux`, `.log`, `.nav`, `.out`, `.snm`, and `.toc`.

Create a ZIP whose top level contains `main.tex`, then in Overleaf select
**New Project → Upload Project**. After uploading, confirm that the correct
main document and the **pdfLaTeX** compiler are selected.

See Overleaf’s
[upload instructions](https://docs.overleaf.com/managing-projects-and-files/uploading-a-project)
for additional details.

## Troubleshooting

### The agent cannot find the skill

Give it the exact path to `prepare-slides/SKILL.md` and ask it to read the file
before starting. Confirm that the complete skill folder is available.

### A Quarto deck does not render

Run `quarto check` and `quarto render` in a terminal. The render error is the
decisive result. Check missing packages, relative paths, images, and Quarto
extensions only when the render reports them.

### A Beamer deck does not compile

Run `pdflatex main.tex` and inspect the first error. Common causes include
missing TeX packages, missing images, incorrect relative paths, and special
characters that require LaTeX escaping.

### A PowerPoint deck looks different on another computer

Check for missing Montserrat or Lato fonts, font substitution, unexpected line
wrapping, shifted objects, and image clipping.
