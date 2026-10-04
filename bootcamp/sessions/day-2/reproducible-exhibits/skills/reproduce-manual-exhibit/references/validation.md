# Equivalence validation

## Numerical validation

For nontrivial tables, compare the generated results with keyed reference values as described in [reconstruction-workflow.md](reconstruction-workflow.md). Expose matching keys during validation, but do not require a saved validation file when an in-memory or temporary comparison is sufficient. For figures, compare recoverable plotting data and mappings when available; do not require transcribed records for points that exist only as pixels in a rendered reference.

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

### Displayed and full-precision references

What a comparison can establish depends on the reference:

- An Excel reference usually stores full-precision values. Compare at full precision with a small declared tolerance.
- A Word, PDF, or image reference shows only rounded values. Use `--display-decimals auto` so values that agree at the displayed precision are classified as `rounding_difference` rather than `statistical_difference`. `auto` reads the number of decimals from each reference value.

When the reference shows only rounded values, the strongest possible conclusion is that the generated values match at the displayed precision. State this in the report.

### Displayed-value normalization

`compare_tables.py` normalizes displayed values before numeric comparison:

- missing-value tokens (by default blank, `.`, `-`, en and em dashes, `NA`, `n/a`, `n.a.`, `NaN`, `none`, `null`; override with `--missing-tokens`);
- thousands separators, Unicode minus signs, and percent signs;
- trailing significance or footnote markers such as `*`, `†`, `‡`, `§`, or superscripts.

Parentheses and brackets are treated literally by default because parentheses can mean either a wrapper around a standard error or an accounting-style negative number. After confirming the table's convention, use `--parentheses unwrap` for positive wrapped statistics, `--parentheses negative` for accounting negatives, or `--brackets unwrap` for positive bracketed statistics.

Percent signs are removed without rescaling, so `12.3%` compares as `12.3`. Generate values on the displayed scale or record the scaling explicitly. Where a dash or blank means zero rather than missing, pass `--missing-tokens` without that token.

When the reference contains significance or footnote markers, include them in the generated values or reference annotations and use `--check-annotations` so that differing markers are reported.

### Transcribed values

When a reference value was transcribed from an image or scanned PDF, treat a discrepancy first as a possible transcription error. Recheck the source before attributing the difference to the calculation, and state which compared values were transcribed.

## Semantic validation

Confirm that headings and notes describe the calculations actually performed. A matching number produced by a different sample, estimator, or transformation is not an exact reconstruction.

## Visual validation

Render the final artifact at its intended size and perform one focused visual inspection. Check the features relevant to the exhibit, such as labels, axes, scales, legends, dimensions, clipping, overlaps, font substitution, and legibility. Do not create extra rendered formats or validation folders merely for this inspection.

For figures, compare plotted data and mappings before rendered pixels. When the plotted data and semantics are available and correct, a focused visual inspection is normally enough; do not spend time on pixel-level comparison. Use image comparison only when the reference is image-only, the user asks for it, or a suspected rendering problem cannot be resolved from the data and chart specification. Different engines can produce harmless antialiasing and font differences.

## Classify every discrepancy

Use one of:

- `exact_match`
- `within_declared_tolerance`
- `rounding_difference`: values agree after rounding to the displayed precision
- `formatting_difference`
- `annotation_difference`: values agree but significance or footnote markers differ
- `missing_vs_value`: one side is blank or missing and the other has a value, including zero
- `statistical_difference`
- `missing_from_reference`
- `missing_from_generated`
- `unverifiable`

`compare_tables.py` exits with status 1 when any value is classified as anything other than `exact_match`, `within_declared_tolerance`, or `rounding_difference`.

The final response should identify the affected row, column, series, or visual feature and explain whether user input is required. Do not create a separate validation report unless requested.
