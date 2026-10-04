# Python implementation

Preserve the existing Python project structure and dependency manager when possible.

## Workbook inspection

Use `openpyxl` for workbook structure, formulas, styles, and chart metadata. It does not calculate formulas. Cached workbook values may be absent or stale, so do not treat them as authoritative without checking how the workbook was last recalculated.

## Data and computation

Use pandas, Polars, or the project's existing dataframe library. Validate joins, grouping keys, expected row counts, category order, and missing-value behavior. Keep full-precision results separate from formatted display values.

Use model-aware extraction from the statistical library rather than copying printed summaries. Preserve weights, fixed effects, clustering, variance estimators, categorical reference levels, and model samples.

## Rendering

- Use Matplotlib, Seaborn, Plotnine, Altair, or the existing plotting system for figures.
- Use Great Tables or an appropriate document-specific renderer for display tables.
- Export the format required by the manuscript or publication workflow.

Record dependencies with the project's existing mechanism. For a new project, a `pyproject.toml` and lockfile are preferable to an undocumented environment.

## Verification

Write the canonical results or plotting data to a machine-readable file when useful. Validate those values before comparing rendered output.
