# Equivalence validation

## Numerical validation

Compare, as applicable:

- row, column, series, and panel membership;
- full-precision values with a declared tolerance;
- displayed values after rounding;
- sample sizes and cluster counts;
- standard errors, confidence intervals, p-values, and significance markers;
- units, percentage scaling, transformations, and denominators;
- missing, suppressed, blank, zero, and not-applicable values;
- category, term, model, and display order.

Never use a large tolerance to conceal a methodological discrepancy.

## Semantic validation

Confirm that headings and notes describe the calculations actually performed. A matching number produced by a different sample, estimator, or transformation is not an exact reconstruction.

## Visual validation

Render the final artifact at its intended size. Check headers, column spans, panel organization, decimal alignment, labels, notes, axes, scales, legends, dimensions, clipping, overlaps, font substitution, and legibility.

For figures, compare the plotted data and mappings before rendered pixels. Different engines can produce harmless antialiasing and font differences.

## Classify every discrepancy

Use one of:

- `exact_match`
- `within_declared_tolerance`
- `rounding_difference`
- `formatting_difference`
- `statistical_difference`
- `missing_from_reference`
- `missing_from_generated`
- `unverifiable`

The final report should identify the affected row, column, series, or visual feature and explain whether user input is required.
