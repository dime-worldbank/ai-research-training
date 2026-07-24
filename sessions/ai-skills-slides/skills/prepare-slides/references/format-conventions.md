# Format Conventions

Use this reference for syntax, template selection, building, and delivery rules
that differ across Quarto, Beamer, and PowerPoint.

For a new deck, load this reference only in Phase 2, after the outline and
visual choices are approved and the output format is selected. During a Phase
1 review of an existing deck, consult the relevant section only when needed to
diagnose source-format or rendering problems.

Apply shared guidance from:

- `slide-structure.md` for narrative and content selection.
- `figure-table-guidelines.md` for figures and tables.
- `decdi-branding.md` for colors, fonts, and logos.

## Quarto

### Starting files

Copy the complete `assets/quarto/` folder into the output project.

The project requires:

- `template.qmd`
- `_extensions/decdi/`
- The bundled logo files
- The bundled R palette and theme helpers

Keep the relative paths intact when copying these files.

### Format

Use the custom DECDI Reveal.js format:

```yaml
format:
  decdi-revealjs:
    self-contained: true
```

Do not replace `decdi-revealjs` with plain `revealjs` unless the user requests
an unbranded deck.

Use `self-contained: true` when the deck needs to be shared as one HTML file.
It may be omitted when the deck will be hosted with its supporting files.

### Slide syntax

Use a level-one heading for a major section divider:

```markdown
# Results {background-color="#002A4F"}
```

Use a level-two heading for a content slide:

```markdown
## Enrollment increased after the program
```

Use columns for side-by-side content:

```markdown
:::: {.columns}

::: {.column width="50%"}
Left-side content
:::

::: {.column width="50%"}
Right-side content
:::

::::
```

Use a notes block for speaker notes:

```markdown
::: {.notes}
Explain the identifying assumption before presenting the result.
:::
```

Use `.smaller` or `.scrollable` only when restructuring the slide would not
produce a clearer result.

Place any required external source and interpretation notes immediately below
the visual using the bundled `.visual-note` class:

```markdown
::: {.visual-note}
**Source:** World Development Indicators.<br>
**Notes:** Lines show 95% confidence intervals. N = 2,149 farmers.
:::
```

Omit the `Source:` line for the manuscript authors' own analysis. Keep the
entire block concise; the template renders it much smaller and in muted gray.

### Code and results

Hide code that generates presentation results:

```r
#| echo: false
```

Source the bundled palette and plotting helpers once in the setup chunk:

```r
source("_extensions/decdi/setup_decdi_palettes.R")
source("_extensions/decdi/setup_ggplot2_decdi.R")
```

Load only packages used by the deck. Do not install packages during rendering;
report missing dependencies and provide setup instructions instead.

### Build

Render the deck with:

```sh
quarto render template.qmd
```

The current template produces:

```text
index.html
```

Inspect the rendered HTML rather than reviewing only the `.qmd` source.

## Beamer

### Starting files

Copy the complete `assets/beamer/` folder into the output project.

The project requires:

- `beamer-template.tex`
- `img/`
- Any additional figures referenced by the deck

Keep image paths relative to the `.tex` file.

### Structure

Use `\section{}` for major sections:

```tex
\section{Results}
```

Use one `frame` for each slide:

```tex
\begin{frame}{Enrollment increased after the program}
  Slide content
\end{frame}
```

Use `columns` for side-by-side content:

```tex
\begin{columns}[T]
  \column{0.48\textwidth}
  Left-side content

  \column{0.48\textwidth}
  Right-side content
\end{columns}
```

Use the existing title and closing frames as starting points. Apply logo
selection and placement from `decdi-branding.md`.

### Figures and tables

Insert figures with `\includegraphics`:

```tex
\includegraphics[width=0.8\textwidth]{img/main-result.png}
```

Use `booktabs` commands for tables:

```tex
\toprule
\midrule
\bottomrule
```

Use `threeparttable` when a table needs notes below it. Do not use vertical
rules or raw software output as the final table.

Use `\visualnote{}` immediately below a figure or table for any required
external source and interpretation details:

```tex
\visualnote{\textbf{Source:} World Development Indicators.\\
\textbf{Notes:} Lines show 95\% confidence intervals. $N=2{,}149$ farmers.}
```

Omit the source line for the manuscript authors' own analysis. The bundled
command uses muted `\scriptsize` text. Do not put sources inside `\caption{}`.

### Build

Compile the deck twice so the table of contents, sections, and navigation are
current:

```sh
pdflatex beamer-template.tex
pdflatex beamer-template.tex
```

The expected final output is:

```text
beamer-template.pdf
```

Do not deliver or commit LaTeX build artifacts such as:

```text
.aux
.log
.nav
.out
.snm
.synctex.gz
.toc
```

Inspect the rendered PDF rather than reviewing only the `.tex` source.

## PowerPoint

### Starting files

Copy the complete `assets/pptx/` folder into the output project.

The project requires:

- `template.pptx`
- `img/`

The template is a native, editable PowerPoint deck. It contains starter slides
for a title, section divider, text-and-visual layout, full-width evidence,
deliberate comparison, and substantive closing.

### Native PowerPoint workflow

Do not use Quarto to create PowerPoint output.

Preserve `template.pptx` as the clean starting point. Create a working copy
with the requested output name, then edit the copy with native PowerPoint
presentation tooling.

Use the starter slides as layout and styling references:

- Duplicate the closest starter slide for each new slide.
- Replace all bracketed placeholder text and placeholder visual frames.
- Delete starter slides that are not needed in the final deck.
- Keep text, tables, charts, and simple shapes editable.
- Insert research figures and photographs as appropriately sized image assets.
- Preserve the template's 16:9 dimensions, typography, colors, margins, and
  visual hierarchy.
- Place the logo only on the title and closing slides, following
  `decdi-branding.md`.

When revising an existing PowerPoint deck, use the supplied deck as the primary
source rather than replacing it with `template.pptx`. Review and obtain
approval before making changes, as required by `deck-review-checklist.md`.

### Creating content

- Use finding-led titles when supported by the evidence.
- Use one primary figure or table per slide by default.
- Use the comparison starter only when the comparison is the slide's message.
- Keep complete specifications and supporting results in the appendix.
- Add a small visible source line only for external sources; keep authors'
  analysis traceable internally.
- Add a small interpretation note when sample, uncertainty, significance, or
  other details are needed.
- Do not rasterize editable slide text or presentation tables.
- Do not use screenshots of unformatted software output as final slide
  content.

### Export and inspection

Save the editable output as a `.pptx` file. The output filename should describe
the presentation rather than retaining the generic `template.pptx` name.

Render every slide for visual inspection before delivery. Check the full-size
slides as well as the deck-level sequence.

Inspect the final `.pptx` for:

- Font substitution and unexpected line wrapping
- Text, image, table, or chart overflow
- Misaligned or overlapping objects
- Cropped or low-resolution figures
- Inconsistent title and content placement
- Missing required external sources or interpretation notes
- Missing or incorrectly placed title and closing-slide logos
- Remaining bracketed placeholders or sample slides

Fix all unintended overlap, clipping, and overflow before delivery.

### Font limitation

The template uses Montserrat and Lato but does not embed the font files. The
deck may use fallback fonts on a machine where those fonts are unavailable.
Report any substitution and inspect line wrapping on the machine used to
present the deck.

## Final format check

Before delivery, confirm that:

- Quarto and Beamer source files build without errors when applicable.
- PowerPoint files open without repair warnings.
- The expected final output exists.
- The final output has been visually inspected.
- Required logos and fonts appear as intended.
- Figures and tables are legible and not clipped.
- No template placeholders remain.
- Source files use relative paths.
- Temporary build artifacts are excluded.
