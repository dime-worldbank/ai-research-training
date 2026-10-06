# Table reconstruction

## Classify the table

Use the closest archetype, then record deviations.

### Grouped descriptive table

Recover the statistics, subgroup definitions, row sections, column spanners, sample counts, units, and missing-value rules.

### Balance table

Recover treatment and comparison definitions, unadjusted or adjusted means, difference definition, standard-error or test procedure, weights, clustering, standardized differences, joint tests, and significance policy. Never choose a test merely because a reference table contains stars.

### Baseline/endline table

Recover round-specific eligibility, panel versus repeated-cross-section structure, group means, within-round differences, change or interaction specification, fixed effects, and observation counts for each column.

### Adjusted comparison table

Recover the estimand, model formula, covariates, fixed effects, variance estimator, clustering level, weights, omitted categories, and reported model statistics.

### Regression table

Recover model sequence, outcomes, displayed terms, coefficient transformation, uncertainty measure, model metadata, controls indicators, fixed-effects indicators, and notes.

### Custom mixed table

Build a canonical results dataset first. Use direct LaTeX or raw file writing only for the final layout when a maintained renderer cannot express the structure.

## Separate computation from presentation

Compute values once and store them at full precision. Apply labels, ordering, rounding, parentheses, stars, rules, spacing, and column spans during rendering. Do not calculate values in presentation strings.

## Requirements for trustworthy reconstruction

- Every displayed value maps to a named calculation or model.
- Every row and column has an explicit inclusion rule and order.
- Sample sizes use the estimation sample relevant to the displayed statistic.
- Notes describe weights, clustering, fixed effects, missing values, and significance markers when applicable.
- Blank cells are distinguished from zero, missing, suppressed, and not applicable.
