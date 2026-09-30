# Reconstruction workflow

## 1. Establish the evidence

Identify the reference exhibit, source data, target language, intended output format, and existing project conventions. Determine whether the final artifact should be Git-trackable and whether a second rendered format is also needed. Infer these choices from an established paper or project workflow when clear; otherwise ask the user before selecting the exporter. A workbook may contain enough evidence to recover calculations; a screenshot usually contains only displayed values and appearance.

For Excel, inspect:

- visible and hidden sheets;
- formulas and cached values;
- named ranges, tables, filters, pivots, and helper ranges;
- chart types, series, category ranges, axes, labels, and annotations;
- merged cells, row and column dimensions, number formats, and notes;
- values pasted over formulas or linked from unavailable workbooks.

Treat macros, external links, and unsupported Excel features as unresolved until independently understood.

## 2. Reverse-engineer the exhibit

Describe separately:

- input data and unit of observation;
- sample restrictions and exclusions;
- transformations and aggregations;
- estimands, statistics, or models;
- row, column, series, and panel membership;
- display labels, ordering, rounding, units, notes, and styling.

Distinguish observed facts from inferred choices. Record confidence and unresolved questions in the exhibit specification.

## 3. Implement in layers

Organize nontrivial work into four conceptual stages:

1. Prepare analysis data.
2. Compute full-precision results or plotted data.
3. Assemble a structured results object.
4. Render the publication artifact.

Keep full-precision values until the rendering stage. Do not use displayed, rounded values as analytical inputs.

## 4. Validate in the right order

Validate data lineage and sample definitions first, calculations second, table or chart semantics third, and visual appearance last. A visually identical output can still be analytically wrong.

## 5. Stop when evidence is insufficient

Do not reverse-engineer a preferred answer. If the reference does not establish how a value was computed, mark it unresolved. Reconstructing the displayed value from a manually entered constant is not computational reproducibility.
