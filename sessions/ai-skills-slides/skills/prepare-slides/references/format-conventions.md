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

Never rely on ggplot2's default gray or hue scales. Apply the bundled DECDI
theme and explicit brand scales; use neutral gray only as an intentional,
documented choice.

Avoid a silent named-scale mismatch when building manual scales from
`decdi_palette()`. A lookup such as `decdi_palette("DECDI")["BlueMid"]`
retains the name `BlueMid`. Nesting that value inside another named vector can
produce names such as `TRUE.BlueMid`, so ggplot2 cannot match the scale to the
data and silently falls back to its defaults. Remove the inner name:

```r
status_colors <- c(
  "TRUE" = unname(decdi_palette("DECDI")["BlueMid"]),
  "FALSE" = unname(decdi_palette("DECDI")["Navy"])
)

scale_fill_manual(values = status_colors)
```

Use the same `unname()` pattern for `scale_color_manual()`.

Load only packages used by the deck. Do not install packages during rendering;
report missing dependencies and provide setup instructions instead.

### Rebranding an existing project

Work in a copy of the existing Quarto project, preserving content and slide
order per `SKILL.md`'s Rebrand definition. Apply approved brand changes
through the project YAML, DECDI extension or SCSS, font settings, palette
helpers, chart scales, logos, and footers — including the section-divider
navy fill and title-slide accent bar defined in `decdi-branding.md`'s
brand-carried layout treatments, not only color values — before making
slide-specific fixes.

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

### Rebranding an existing project

Work in a copy of the existing Beamer project, preserving content and frame
order per `SKILL.md`'s Rebrand definition. Apply approved brand changes
through theme colors, font settings, logo commands, and chart colors —
including the title-treatment and `\visualnote{}` styling defined in
`decdi-branding.md`'s brand-carried layout treatments, not only color values
— before making frame-specific fixes. Do not add a navy section-divider fill
to match Quarto/PowerPoint; Beamer's plain-white divider is an intentional
difference, not a gap to close, unless the user explicitly asks for that
visual change.

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

For a build, or an improvement using template-based reconstruction (see
`SKILL.md`'s Phase 2 Improve step — the Phase 1 verdict was "Needs
substantial revision" or "Rebuild recommended"), preserve `template.pptx` as
the clean starting point. Create a working copy with the requested output
name, then edit the copy with native PowerPoint presentation tooling.

For a targeted improvement (verdict "Ready with minor revisions," or a
Fast-path request), edit a copy of the *supplied* deck directly instead —
do not start from `template.pptx`. Use the bundled template and
`decdi-branding.md` only as a reference for any approved visual changes
within that copy.

When working from `template.pptx` (build, or template-based improvement),
use the starter slides as layout and styling references:

- Duplicate the closest starter slide for each new slide, using
  `assets/pptx/duplicate_slide.py`'s `duplicate_slide(prs, index)` rather
  than hand-rolling a shape-by-shape copy. A slide's background fill
  (`<p:bg>`, e.g. the navy section-divider background) lives outside the
  shape tree and is silently dropped by a naive copy — the duplicate ends
  up with no background fill at all (not even the wrong color), which on a
  divider slide means invisible white-on-white title text. The bundled
  helper also re-links copied images' relationships correctly, which a
  shape-by-shape copy does not. Run it directly (see the file's `__main__`
  block) or import `duplicate_slide` into a longer script.
- Replace all bracketed placeholder text and placeholder visual frames.
- Delete starter slides that are not needed in the final deck.
- Keep text, tables, charts, and simple shapes editable.
- Insert research figures and photographs as appropriately sized image assets.
- Preserve the template's 16:9 dimensions, typography, colors, margins, and
  visual hierarchy.
- Place the logo only on the title and closing slides, following
  `decdi-branding.md`.

For a template-based improvement, use the supplied deck as the source of
approved content and evidence, then map that content into the closest
starter layouts. Rewrite, split, reorder, or move detail according to the
approved plan; do not shrink text or carry dense wording forward merely to
preserve the old layout.

For a targeted improvement, apply the same rewriting principle — do not
preserve dense wording merely because it appeared in the original deck — but
edit the supplied deck's existing slides directly rather than duplicating
starter slides.

For a rebrand, work in a copy of the supplied deck, preserving content and
slide order per `SKILL.md`'s Rebrand definition. Apply approved theme fonts,
theme colors, master-level elements, SmartArt or shape colors, logos,
backgrounds, and numbering — including the section-divider treatment and
title-slide treatment defined in `decdi-branding.md`'s brand-carried layout
treatments, not only color values — in batches before addressing
slide-specific exceptions.

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

After batching related changes, render every slide for visual inspection
before delivery. Check every new or changed slide at full size as well as the
complete deck-level sequence. Do not rerender after every minor change unless
needed to diagnose a problem.

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
