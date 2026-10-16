# Reconstruction workflow

## 1. Establish the evidence

Identify the reference exhibit, source data, target language, intended single output format, and existing project conventions. Use the user's requested format or the established paper or project workflow. If neither resolves a consequential choice, ask before selecting the exporter; for a figure where the format is otherwise immaterial, default to PNG. Generate additional formats only when the user explicitly requests them. Source code and structured data supply Git traceability even when the rendered artifact is binary. A workbook may contain enough evidence to recover calculations; a screenshot usually contains only displayed values and appearance.

Preserve the current project layout. A simple reconstruction should usually add or modify only the code needed to generate the requested artifact and that artifact itself. Do not translate conceptual stages into new folders or standalone specification and validation files by default.

For Excel, inspect:

- visible and hidden sheets;
- formulas and cached values;
- named ranges, tables, filters, pivots, and helper ranges;
- chart types, series, category ranges, axes, labels, and annotations;
- merged cells, row and column dimensions, number formats, and notes;
- values pasted over formulas or linked from unavailable workbooks.

Treat macros, external links, and unsupported Excel features as unresolved until independently understood.

## 2. Record the reference values for tables

For a nontrivial table, capture displayed reference values in keyed records when automated comparison adds value. Keep those records in memory or a temporary location unless the user requests a saved validation input or the project already has a suitable location. For a small table, a direct comparison in the implementation or validation step may be sufficient.

First extract the table as a plain grid, using the method that fits the reference:

| Reference format | Extraction | Reliability |
| --- | --- | --- |
| Excel | Read the range directly | High: stored values, possibly more precise than displayed |
| Word | Read the table with `python-docx` | High: exact displayed text |
| PDF with a text layer | Extract the table with `pdfplumber` or a PDF skill | Medium: check merged headers and column alignment |
| Scanned PDF or image | Transcribe manually or with OCR | Low: requires a check pass |

When a saved keyed representation is useful, convert the grid with `scripts/grid_to_records.py`. It reads CSV, TSV, or an Excel range. Its generated row and column keys are defaults: review them and rename them to match the keys used by the generated results.

Keep provenance on every record: `source_method` (`excel_cell`, `docx_table`, `pdf_text`, `transcribed`, or `other`) and `source_location` (cell address, page and table number, or image name).

For transcribed or OCR values, check the transcription before relying on it: reread each value against the source, and test any internal consistency the table offers, such as totals, shares summing to 100, row counts, or sample sizes repeated across columns. Record values that remain illegible as unresolved instead of guessing.

Excel cached values can be absent or stale when a workbook was last saved by software that does not recalculate formulas. A formula cell with no cached value appears blank; recover its value from the formula and inputs, or mark it unresolved.

For a figure, do not transcribe every visible point merely to satisfy this table workflow. Prefer the chart's source ranges or another recoverable plotting dataset. When only a rendered image exists, record the visual features and any readable anchor values that can actually be verified, then mark unavailable plotted values as unresolved.

## 3. Reverse-engineer the exhibit

Describe separately:

- input data and unit of observation;
- sample restrictions and exclusions;
- transformations and aggregations;
- estimands, statistics, or models;
- row, column, series, and panel membership;
- display labels, ordering, rounding, units, notes, and styling.

Distinguish observed facts from inferred choices. Record confidence and unresolved questions in the compact specification, wherever it is being maintained for this task.

## 4. Implement in layers

Organize nontrivial work into four conceptual stages:

1. Prepare analysis data.
2. Compute full-precision results or plotted data.
3. Assemble a structured results object.
4. Render the publication artifact.

Keep full-precision values until the rendering stage. Do not use displayed, rounded values as analytical inputs.

These are logical stages, not a requirement for four scripts, four folders, or intermediate deliverables. Keep them in one script when that is clearer and consistent with the project.

## 5. Validate in the right order

Validate data lineage and sample definitions first, calculations second, table or chart semantics third, and visual appearance last. A visually identical output can still be analytically wrong.

## 6. Stop when evidence is insufficient

Do not reverse-engineer a preferred answer. If the reference does not establish how a value was computed, mark it unresolved. Reconstructing the displayed value from a manually entered constant is not computational reproducibility.
