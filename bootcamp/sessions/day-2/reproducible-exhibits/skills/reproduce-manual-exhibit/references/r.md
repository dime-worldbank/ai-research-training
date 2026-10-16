# R implementation

Preserve the existing R project structure and package conventions. Default to the smallest practical change: normally one script or a focused edit to an existing script, plus the one requested artifact. Do not create separate specification, validation, preview, or output folders unless the project already uses them or the user requests them.

## Data and computation

Use explicit joins, grouping, reshaping, transformations, and sample filters. Assert join relationships and expected row counts. Keep full-precision results in a tibble separate from display strings.

Use model-aware extraction rather than copying console output. Preserve weights, fixed effects, clustering, variance estimators, contrasts, factor reference levels, and missing-value behavior.

## Rendering

- Use `ggplot2` or the project's plotting system for figures.
- Use `gt`, `gtsummary`, `modelsummary`, or the project's established table system when it represents the required structure.
- Use Quarto, LaTeX, Typst, Word, HTML, or image output according to the requested deliverable.
- Generate only the requested rendered format. For a figure with no established format, generate PNG only.

Treat package names as routing options, not mandatory dependencies. Use the project's existing environment mechanism. Do not initialize `renv`, add package manifests, or reorganize the project solely for an exhibit reconstruction unless the user asks for a new reproducible R project.

## Verification

Use the available results or plotting data for comparison. Save an additional canonical dataset only when the user requests it, the project convention expects it, or it is a meaningful pipeline input rather than validation clutter. Test explicit invariants such as sample sizes, totals, category coverage, and model term presence. Prefer data and semantic checks plus one focused visual inspection over pixel-level comparison.
