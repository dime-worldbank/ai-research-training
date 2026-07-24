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

During Phase 1, identify meaningful choices before creating or editing any
visual. Do not force a choice when the existing form is already effective.

Assign each real decision a stable ID and present the options side by side:

| Visual ID | Slide ID | Current form | Options | Recommendation | Reason and data requirement |
|---|---|---|---|---|---|
| V01 | S05 | Manuscript Table 3 | A: simplified table; B: coefficient plot; C: keep existing | B | Comparisons are easier to scan; exact estimates and confidence intervals required |

Options may include keeping the existing visual, simplifying a table, using an
alternative chart, leaving a placeholder for an author-supplied screenshot,
moving the result to the appendix, or omitting it. Explain why the recommended
option communicates the result more clearly and state whether it requires
editable data, exact reported values, or an author-supplied image.

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
- **Placeholder:** Reserve an appropriately sized, editable area for the
  author to insert a screenshot of the original figure or table.

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
- Do not enlarge a low-resolution image.
- Check the rendered deck for clipping, blurring, and unreadable labels.

## Final check

Confirm that:

- The title accurately represents the result.
- The numbers and interpretation match the source.
- The visual is legible at presentation size.
- Units, groups, and uncertainty are clear.
- The underlying result is traceable internally.
- Any external source is cited visibly.
- Interpretation notes are included only when needed and remain legible.
- Colors are accessible and brand-consistent.
- The exported image is stored with the project.
- No missing information was invented.
