# Prepare Slides Skill

`prepare-slides` is a reusable AI-agent skill for creating, reviewing, and
improving DECDI/DIME research presentations.

It supports:

- Quarto presentations using Reveal.js
- Beamer presentations using LaTeX
- Native, editable PowerPoint presentations
- New decks created from manuscripts, figures, tables, or results folders
- Reviews and revisions of existing presentation decks
- DECDI typography, colors, logos, and presentation conventions

The complete `prepare-slides/` folder is self-contained. It includes the
instructions, references, branding files, and format-specific starter assets
needed by an AI agent.

## Requirements

### AI agent

Use an AI agent that can:

- Read files and folders in your project.
- Create and edit text and presentation files.
- Run local commands when rendering or compiling is required.
- Inspect the rendered output, or provide files for you to inspect.

The agent does not need native support for named skills. If it cannot install
or automatically discover skills, explicitly tell it to read `SKILL.md` and
follow the instructions there.

### Quarto presentations

To create or render a Quarto presentation locally, install the
[Quarto CLI](https://quarto.org/docs/get-started/).

Verify the installation with:

```sh
quarto check
```

Render a presentation with:

```sh
quarto render template.qmd
```

The bundled template produces a Reveal.js HTML presentation. A web browser is
needed to inspect the result.

If the presentation executes R or Python code, install the corresponding
language and every package used by the code. The DECDI Quarto starter includes
optional R helpers for branded `ggplot2` figures; R is not required when those
helpers are not used.

See the official [Quarto command-line documentation](https://quarto.org/docs/cli/)
for additional commands.

### Beamer and LaTeX presentations

To compile a Beamer presentation locally, install a TeX distribution:

- macOS: MacTeX
- Windows: MiKTeX or TeX Live
- Linux: TeX Live

A full or sufficiently complete installation is recommended. The bundled
template uses `pdflatex` and requires the Beamer ecosystem plus these packages:

- `metropolis`
- `lato`
- `montserrat`
- `graphicx`
- `booktabs`
- `threeparttable`
- `hyperref`
- `tikz`
- `multicol`

Verify the compiler with:

```sh
pdflatex --version
```

Compile the deck twice so section navigation and references are current:

```sh
pdflatex main.tex
pdflatex main.tex
```

You can use Overleaf instead of installing LaTeX locally. See
[Continue editing a Beamer project in Overleaf](#continue-editing-a-beamer-project-in-overleaf).

### PowerPoint presentations

PowerPoint decks are created and edited directly as `.pptx` files. Quarto and
LaTeX are not required.

The AI agent must have a tool capable of creating or editing native PowerPoint
files. Use Microsoft PowerPoint, LibreOffice Impress, or another compatible
viewer for final inspection and manual editing.

Install Montserrat and Lato on the computer used to open or present the deck.
The PowerPoint template references these fonts but does not embed them.

## Add the skill to your project

Download the complete `prepare-slides` folder. Do not download only
`SKILL.md`; the references, branding files, templates, logos, and supporting
assets are part of the skill.

Place the folder somewhere your AI agent can access. For example:

```text
your-project/
├── .agents/skills
│   └── prepare-slides/
│       ├── SKILL.md
│       ├── assets/
│       ├── branding/
│       └── references/
├── manuscript.pdf
├── results/
└── other-project-files/
```

If your AI agent supports a designated skills directory, copy the complete
folder there instead and follow that agent's installation instructions.

## Prepare the source material

Add the relevant research files to your project. These may include:

- A manuscript in PDF, LaTeX, Word, or Markdown format
- A folder containing results, figures, or tables
- Data and code used to generate the results
- An existing Quarto, Beamer, PowerPoint, PDF, or HTML presentation
- Bibliography files and cited sources

Keep related figures and tables in clearly named folders. Include captions,
notes, variable definitions, and source information whenever available.

## Tell the AI agent to use the skill

If the agent does not automatically recognize the skill, point it directly to
the instruction file:

```text
Read .agents/skills/prepare-slides/SKILL.md completely and follow its workflow.
Load the references it identifies for this task and use the bundled assets for
the selected output format.
```

Then describe the requested presentation. Include the audience, purpose,
speaking time, and source files. Include the desired output format when it is
already known; otherwise the agent should ask after the Phase 1 proposal is
approved.

### Create slides from a manuscript

```text
Read ai-skills/prepare-slides/SKILL.md and use it to create a 15-minute Quarto
presentation from manuscript.pdf. The audience is government policymakers.
Focus on the main findings and policy implications, and place technical details
in the appendix.
```

### Create slides from a results folder

```text
Read ai-skills/prepare-slides/SKILL.md and use it to create a Beamer
presentation from results/. The audience is academic economists, and the talk
should be approximately 20 minutes. Review the available evidence and propose
the narrative before building the deck.
```

### Create an Overleaf-ready Beamer project

```text
Read ai-skills/prepare-slides/SKILL.md and create a Beamer presentation from
manuscript.pdf. Put the main document at slides/main.tex, keep all paths
relative, include every required image and bibliography file, and make the
slides/ folder ready to upload to Overleaf as a ZIP file.
```

### Review an existing deck

```text
Read ai-skills/prepare-slides/SKILL.md and review presentation.pptx. Assess its
narrative, figures, tables, DECDI branding, visual consistency, and readiness
to present. Report the proposed changes before editing the file.
```

### Revise an approved deck

```text
Read ai-skills/prepare-slides/SKILL.md and apply the revisions we approved to
presentation.qmd. Preserve the existing format, rebuild the deck, and inspect
the rendered HTML for layout problems.
```

## Expected workflow

The skill uses two phases.

### Phase 1: Plan and approve

The agent should:

1. Inspect the manuscript, results, figures, tables, existing deck, and other
   supporting files.
2. Identify or confirm the audience, purpose, speaking time, and expected
   branding.
3. Propose a narrative and slide-by-slide outline using stable slide IDs such
   as `S01` and `S02`.
4. Show meaningful alternatives for figures and tables using decision IDs such
   as `V01` and `V02`, including a recommendation and any data requirements.
5. For an existing deck, also assess its narrative, evidence, branding,
   implementation, and readiness to present.
6. End with a prefilled Author Decision Form and wait for approval.

The agent should not create, edit, rebrand, or rebuild presentation files in
Phase 1. If underlying data are unavailable and a result exists only in a
manuscript, it should show the reported result beside the feasible slide
wording or visual options. It must not infer unreported values.

The author can reply concisely, for example:

```text
Outline: Approve with changes
S04: Shorten the methods discussion
V01: B — coefficient plot
V02: Keep existing
```

If no changes are needed, the author can say:

```text
Approve the outline and all recommended visual options.
```

### Phase 2: Build and verify

After approval, the agent should:

1. Summarize the approved outline and visual choices.
2. Ask whether the deck should be PowerPoint, Quarto/Reveal.js, or Beamer if the
   author has not already selected a format.
3. Copy and adapt the relevant starter assets.
4. Apply the branding and presentation-quality references.
5. Build or export the approved presentation.
6. Inspect the rendered output for accuracy, overflow, clipping, image quality,
   and branding.
7. Deliver editable source files, required assets, and the final presentation.

## Continue editing a Beamer project in Overleaf

The Beamer output is a normal LaTeX project and can be uploaded to Overleaf for
collaborative editing.

### 1. Check the project contents

The project folder should include:

```text
slides/
├── main.tex
├── img/
├── figures/
├── references.bib
└── other-required-files
```

Only include folders and files that the presentation actually uses. Keep all
image, bibliography, `\input`, and `\include` paths relative to `main.tex`.

Do not include temporary LaTeX build files such as `.aux`, `.log`, `.nav`,
`.out`, `.snm`, `.synctex.gz`, or `.toc`.

### 2. Put the main document at the project root

Rename the main presentation file to `main.tex`, or keep its existing name and
select it as the main document in Overleaf. Keeping the main `.tex` file at the
root of the uploaded project avoids path and compilation problems.

### 3. Create a ZIP file

Create a `.zip` containing the contents of the project folder. Make sure
`main.tex` is at the top level of the ZIP rather than inside an additional
unnecessary parent folder.

For example, run this command from inside the `slides/` directory:

```sh
zip -r slides-overleaf.zip . -x '*.aux' '*.log' '*.nav' '*.out' '*.snm' '*.synctex.gz' '*.toc'
```

### 4. Upload the project

In Overleaf:

1. Select **New Project**.
2. Select **Upload Project**.
3. Choose or drag in `slides-overleaf.zip`.
4. Wait for Overleaf to unpack the project and open the editor.

Overleaf preserves folders contained in the ZIP. See the official
[uploading-a-project instructions](https://docs.overleaf.com/managing-projects-and-files/uploading-a-project).

### 5. Confirm the compiler and main document

Open the project settings and confirm:

- **Compiler:** pdfLaTeX
- **Main document:** `main.tex`, or the actual primary `.tex` filename

The bundled Beamer template is designed for pdfLaTeX. Overleaf normally uses
pdfLaTeX by default, but confirm the setting after upload. See Overleaf's
[compiler settings](https://www.overleaf.com/learn/how-to/Changing_compiler)
and [main-document guidance](https://docs.overleaf.com/getting-started/recompiling-your-project/the-main-document).

### 6. Recompile and continue editing

Select **Recompile**. Resolve any missing-file or missing-package errors before
sharing the project. Once the deck compiles successfully, continue editing the
`.tex` source, figures, tables, citations, and speaker-facing content directly
in Overleaf.

## Troubleshooting

### The agent does not recognize the skill

Provide the exact path to `prepare-slides/SKILL.md` and explicitly ask the
agent to read it before starting. Confirm that the complete skill folder is
available, not only the instruction file.

### The Quarto deck does not render

Run `quarto check`, then ask the agent to report the exact `quarto render`
error. Check for missing language packages, broken relative paths, and missing
images or extensions.

### The Beamer deck does not compile

Run `pdflatex main.tex` and inspect the first reported error. Common causes
include missing TeX packages, missing images, incorrect relative paths, and
special characters that require LaTeX escaping.

### The Overleaf project does not compile

Confirm that the correct main document and pdfLaTeX compiler are selected.
Check that every locally referenced image, bibliography, and input file was
included in the ZIP with the same relative path.

### The PowerPoint deck looks different on another computer

Confirm that Montserrat and Lato are installed. Check for font substitution,
unexpected line wrapping, image clipping, and shifted objects.

### Figures or tables cannot be verified

Provide the source manuscript, table notes, figure captions, data, or results
code when possible. If those materials are unavailable, instruct the agent to
limit its claims to what can be traced to the supplied files and obtain
approval before reconstructing a result.
