# R implementation

Preserve the existing R project structure and package conventions when possible.

## Data and computation

Use explicit joins, grouping, reshaping, transformations, and sample filters. Assert join relationships and expected row counts. Keep full-precision results in a tibble separate from display strings.

Use model-aware extraction rather than copying console output. Preserve weights, fixed effects, clustering, variance estimators, contrasts, factor reference levels, and missing-value behavior.

## Rendering

- Use `ggplot2` or the project's plotting system for figures.
- Use `gt`, `gtsummary`, `modelsummary`, or the project's established table system when it represents the required structure.
- Use Quarto, LaTeX, Typst, Word, HTML, or image output according to the requested deliverable.

Treat package names as routing options, not mandatory dependencies. Record the environment with the project's existing mechanism; use `renv` when appropriate for a new R project.

## Verification

Save the canonical table results or plotting data alongside the rendered artifact when doing so supports comparison. Test explicit invariants such as sample sizes, totals, category coverage, and model term presence.
