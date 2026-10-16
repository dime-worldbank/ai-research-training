# Figure and Table Guidelines

Use this reference when selecting, creating, simplifying, or reviewing figures
and tables for a presentation. Keep format-specific implementation details in
the corresponding format reference.

## General principles

- Give each figure or table one clear communicative purpose.
- Use one primary figure or table per slide by default.
- Place two visuals together only when their comparison is the message.
- Use a title that communicates the finding when the evidence supports it.
- Size content for the rendered slide, not for a manuscript page.
- Simplify or split dense content instead of shrinking the text.
- Move secondary results and complete specifications to the appendix.
- Apply the colors and accessibility guidance in `decdi-branding.md`.

## Mandatory exhibit-selection flow

Use this sequence for every evidence slide. Decide what evidence belongs on
the slide before choosing its layout.

1. **State the slide claim.** Write the single conclusion or question the
   exhibit must support. If the slide has no evidence-based claim or question,
   do not add an exhibit merely for decoration.
2. **Apply the main-deck test.** Keep the exhibit in the main deck only when
   the audience needs it to understand, compare, or trust a main conclusion.
   Move useful supporting detail to the appendix; omit material that does not
   advance either purpose.
3. **Prefer faithful existing evidence.** Retain an existing exhibit when it
   directly supports the claim, is accurate, and will be legible on a slide.
   Simplify it when the evidence is right but the presentation is too dense.
   Do not replace it merely to make the deck look different.
4. **Check what can be produced faithfully.** Create or adapt an exhibit only
   from supplied editable data or exact reported results. When these are not
   available, retain an approved usable exhibit or offer an editable
   placeholder. Never infer values from a plotted image.
5. **Choose the exhibit form from the audience's task.** Use the simplest form
   that performs that task:
   - one headline value or short factual result: text or a numeric callout,
     not a chart;
   - comparison across discrete categories: bar or dot plot;
   - change over time or another ordered sequence: line chart;
   - estimates with uncertainty: points with intervals;
   - relationship between continuous variables: scatterplot;
   - exact values the audience must look up: simplified table.
6. **Choose the visual pattern.** After the exhibit form is settled, select
   `one-visual`, `visual-and-text`, or `comparison` using the rules below. If
   none fits cleanly, split the content or move secondary evidence to the
   appendix instead of inventing a custom layout.
7. **Record only real choices.** Assign a visual ID when two or more faithful
   options would materially change the slide. Recommend one option and explain
   the claim fit, audience task, source requirement, and main-deck or appendix
   decision. Do not create artificial alternatives for an exhibit that is
   already effective.

This order is mandatory: claim, deck relevance, available evidence, exhibit
form, then layout pattern. Visual variety is not a selection criterion.

## Shared visual patterns and size test

Use these preset patterns for new decks and template-based improvements in
PowerPoint, Quarto, and Beamer. Select one pattern during Phase 1, use the
corresponding format-specific layout in Phase 2, and fill its visual area. Do
not create a custom geometry for each slide.

| Pattern | Use | Required composition | Minimum raster dimensions |
|---|---|---|---|
| `one-visual` | One figure or table carries the slide | Full content width below the title | 1600 × 500 px |
| `visual-and-text` | The figure and explanatory text both matter | Two approximately equal columns; visual fills one column | 900 × 500 px |
| `comparison` | Two equally important visuals support one comparison | Two equal visual areas | 720 × 425 px for each visual |

Select the pattern using these rules:

- Use `one-visual` when the visual can carry the message without visible
  explanatory prose.
- Use `visual-and-text` only when the audience must see explanatory text while
  reading the visual.
- Use `comparison` only when the slide's message depends on comparing exactly
  two visuals.
- Split the slide or move secondary evidence to the appendix when it requires
  more than two independent visuals.

Keep content within these default budgets:

- `one-visual`: title, visual, and any required source or interpretation note;
  no separate body-text block.
- `visual-and-text`: no more than three bullets or about 45 words beside the
  visual.
- `comparison`: two short labels and, when needed, one short interpretation
  statement; do not add a separate bullet list.

When content exceeds the relevant budget, shorten it, move detail to speaker
notes or the appendix, or split the slide. Do not shrink the visual or its
labels to retain excess text.

The raster dimensions are a fast pre-insertion screen, not a target for
resampling. Read the image's pixel dimensions once. Do not calculate effective
PPI or repeatedly resize and reassess it. The pixel test does not apply to
vector files or native editable charts and tables; still inspect their labels
at presentation size.

Crop unnecessary outer whitespace before placement, then make the visual fill
the selected layout's visual area while preserving its aspect ratio. A large
image box containing a small plot does not pass. For a short native table, use
the full available width but let the row count set its height; do not add empty
rows or stretch it. For a comparison, use equal-sized areas and the same scale
when the evidence is comparable.

If a visual cannot fill the preset layout without distortion, cropped evidence,
or unreadable labels, simplify it, select another preset pattern, or split the
slide. Do not spend time tuning custom layout dimensions. Preserve the existing
structure for a targeted edit or rebrand unless the author approved a layout
change; flag a failing visual instead of silently redesigning the deck.

If a raster visual fails in a new or rebuilt slide, use this bounded fallback:

1. Check once for an existing vector or higher-resolution export in the
   supplied project.
2. When supplied code and data support it, regenerate the visual once.
3. If neither succeeds, leave the visual area blank rather than inserting a
   blurry asset; identify the slide, missing visual, and required replacement
   in the final handoff.

Do not begin an open-ended asset search or repeatedly regenerate the visual.
For a targeted edit or rebrand, retain and flag an existing failing visual
unless the author approved its replacement.

## Accuracy

- Preserve the meaning, values, signs, units, and uncertainty of the original
  result.
- Do not invent missing values, labels, sources, variable definitions, or
  interpretations.
- Use causal language only when the manuscript or research design supports it.
- Keep a traceable source for every figure, table, and numerical claim.

If the source material is ambiguous or inconsistent, flag the issue instead of
guessing.

## Phase 1 visual decisions

During Phase 1, apply the mandatory exhibit-selection flow before creating or
editing any visual. Identify meaningful choices, but do not force a choice when
the existing form is already effective.

Assign each real decision a stable ID and present the options side by side:

| Visual ID | Slide ID | Slide claim | Current form | Options | Recommendation and reason | Evidence requirement | Destination |
|---|---|---|---|---|---|---|---|
| V01 | S05 | Effects differ across outcomes | Manuscript Table 3 | A: simplified table; B: point-and-interval plot; C: keep existing | B: comparison is the audience task | Exact estimates and confidence intervals | Main deck |

Options may include keeping the existing visual, simplifying a table, using an
alternative chart, leaving a placeholder for an author-supplied screenshot,
moving the result to the appendix, or omitting it. Explain why the recommended
option supports the slide claim and audience task. State whether it requires
editable data, exact reported values, or an author-supplied image, and whether
the result belongs in the main deck, appendix, or should be omitted.

Do not produce multiple finished alternatives during Phase 1. The author
selects an option by visual ID in the Author Decision Form defined in
`SKILL.md`. Build only the approved option in Phase 2.

## When the underlying data are unavailable

Results may be available only in a manuscript or manuscript PDF.

Before proposing or recreating a result:

1. Locate the exact result in the manuscript.
2. Record the table, figure, section, or page where it appears.
3. Preserve the reported estimate, unit, comparison, and uncertainty.
4. Identify which presentation options can be supported faithfully by the
   reported information.
5. Show the reported result and proposed slide interpretation to the user for
   approval during Phase 1.

For each manuscript visual, offer two options when they are feasible:

- **Adapt:** Recreate a cleaner branded figure or simplified table from exact
  information reported in the manuscript.
- **Placeholder:** Reserve the selected pattern's visual area for the author to
  insert a screenshot of the original figure or table.

Use a side-by-side review table:

| Visual ID | Manuscript result | Option A: Adapt | Option B: Placeholder | Recommendation |
|---|---|---|---|---|
| V01 | Table 3, Column 2: 0.12; SE 0.04 | Branded coefficient plot using the reported estimate and uncertainty | `[Insert screenshot of Table 3 here]` | A: exact values are reported |
| V02 | Figure 4: effects differ by location | Not faithful without the plotted values | `[Insert screenshot of Figure 4 here]` | B: exact group estimates are unavailable |

Do not reconstruct a detailed dataset from a plotted image.

After the author selects an option:

- Recreate a simplified figure or table only when the manuscript reports enough
  exact information.
- Preserve values, units, comparison groups, uncertainty, sample definitions,
  and statistical meaning in any adaptation.
- Otherwise, create an editable placeholder that names the intended figure or
  table and, when useful, identifies the content that should remain visible.
- Do not take, crop, or insert a screenshot from the manuscript. The author
  supplies it later.
- Record the manuscript table, figure, column, section, or page in speaker
  notes or another internal provenance record rather than as a visible source.

## Figures

### Chart selection

- Choose the simplest chart that communicates the intended comparison.
- Use bars for comparisons across discrete categories.
- Use lines for change over time or another ordered dimension.
- Use points and intervals for estimates and uncertainty.
- Use scatterplots for relationships between continuous variables.
- Avoid 3D charts, unnecessary dual axes, excessive gridlines, and decorative
  effects.

### Labels and scales

- Label axes, units, groups, and time periods clearly.
- Define abbreviations that may not be familiar to the audience.
- Use a meaningful baseline.
- Start bar-chart axes at zero unless there is a documented reason not to.
- Clearly disclose truncated or transformed axes.
- Keep comparable panels on comparable scales.
- Order categories deliberately rather than relying on software defaults.

### Titles and interpretation

Use finding-led titles carefully:

- “The program increased enrollment by 12 percentage points.”
- “Estimated effects are larger in urban areas.”
- “Employment estimates are positive but imprecise.”

Avoid causal wording when the evidence only shows an association.

Do not describe an estimate as “no effect” solely because it is statistically
insignificant. Describe its magnitude and uncertainty.

### Emphasis and uncertainty

- Highlight the evidence supporting the slide’s message.
- Direct-label series when that is clearer than using a separate legend.
- Show confidence intervals or another uncertainty measure when relevant.
- Explain what error bars represent.
- Do not present a point estimate as definitive when its uncertainty is
  material.
- Do not use color as the only way to distinguish groups or results.
- Use the DECDI palette instead of default software colors.

## Tables

### Creating a presentation table

Do not use unformatted software output as the final presentation table.

When editable data or exact manuscript values are available, create a clean
presentation table containing only the information needed for the slide.

If the author supplies a separate image or an existing deck already contains a
usable table image, a legible crop may be retained with approval. When only the
manuscript is available, follow the adapt-or-placeholder workflow above rather
than extracting a screenshot from the manuscript.

### Content and formatting

- Include only the rows and columns needed for the slide’s message.
- Move complete specifications and secondary outcomes to the appendix.
- Use informative row and column labels.
- Put measurement units in headers where practical.
- Round values consistently and appropriately for the audience.
- Preserve negative signs, leading zeroes, and meaningful precision.
- Clearly distinguish estimates, standard errors, and confidence intervals.
- Explain significance symbols and abbreviations.
- Include sample size, controls, or sample restrictions when needed for
  interpretation.
- Highlight substantively important results rather than every statistically
  significant cell.
- Use simple horizontal rules and avoid vertical lines.

### When using an image of a table

- Crop unrelated rows, columns, and excessive margins.
- Do not distort or enlarge a low-resolution image.
- Confirm that all necessary labels and notes remain visible.
- Add a visible source only when the table uses an external source.
- Add a small note when sample, uncertainty, significance, or other
  interpretation details are needed.
- Place the full original table in the appendix when useful.

## Sources and interpretation notes

Do not add a visible source line when a figure or table presents the
manuscript authors' own analysis. Maintain its manuscript location in speaker
notes or another internal provenance record.

Add a visible source only when the visual, data, or analysis comes from an
external source. Use a natural presentation citation rather than the source
table or figure number from the manuscript.

Examples:

- `Source: World Development Indicators, accessed July 2026.`
- `Source: Bangladesh Bureau of Statistics.`
- `Source: Smith et al. (2025).`

Add a separate `Notes:` line only when the audience needs information to
interpret the visual. Notes may define significance stars, confidence
intervals, standard errors, sample size, units, reference groups, clustering,
sample restrictions, adjustments, or unfamiliar abbreviations.

Examples:

- `Notes: Points show treatment-effect estimates; lines show 95% confidence intervals. N = 2,149 farmers.`
- `Notes: Standard errors clustered by farmer group in parentheses. *p* < 0.10, **p** < 0.05, ***p*** < 0.01.`

Place `Source:` and `Notes:` directly below the visual in much smaller, muted
text. Keep them separate from the figure or table title. Do not display labels
such as `Manuscript Table 6` or `Table 1 from the paper` as the source.

If an external source is required but unknown, insert a visible source
placeholder and flag it for the user. Do not invent a source.

## Export quality

Use a file format that can be stored with the project and reviewed in GitHub.

- Use PNG as the default for charts, diagrams, and rendered tables.
- Use JPG for photographs or other continuous-tone images.
- Use SVG when the output format supports it reliably and editability matters.
- Use descriptive filenames such as `main-treatment-effect.png`.
- Avoid spaces and generic filenames such as `plot1.png`.
- Store generated visuals in a predictable folder such as `figures/`.
- Preserve each image’s aspect ratio.
- Crop unnecessary whitespace.
- Apply the minimum-pixel and blank-area rule above; do not enlarge a
  low-resolution image to make it appear to fill the slide.
- Check the rendered deck for clipping, blurring, and unreadable labels.

Use `deck-review-checklist.md` for the final visual and evidence checks rather
than repeating a second checklist here.
