---
name: reproduce-manual-exhibit
description: Reconstruct manually prepared Excel, Word, PDF, or image-based tables and figures as reproducible Stata, R, or Python workflows. Use when an existing exhibit defines the desired calculations, structure, or appearance and the user wants code that regenerates it from source data. Do not use for ordinary exploratory analysis without a reference exhibit.
---

# Reproduce Manual Exhibit

Convert a manually assembled table or figure into a transparent workflow that starts from source data and regenerates the deliverable without undocumented edits.

## Required outcome

Deliver, when the available evidence permits:

- executable source code in the requested language;
- a generated table or figure in one requested format;
- documented analytical and display choices, kept in the code or final handoff unless a separate specification is useful;
- validation findings, reported in the final handoff unless a separate report is requested;
- a concise, numbered run sequence for the updated pipeline;
- explicit unresolved items where the reference does not reveal the underlying calculation.

Never claim computational reproducibility when only the appearance has been reconstructed.

## Route the task

1. Read [references/reconstruction-workflow.md](references/reconstruction-workflow.md) for every task.
2. Read [references/exhibit-specification.md](references/exhibit-specification.md) before implementing the reconstruction.
3. For a table, read [references/table-reconstruction.md](references/table-reconstruction.md).
4. For a figure, read [references/figure-reconstruction.md](references/figure-reconstruction.md).
5. Read exactly one language reference unless the user requests multiple implementations:
   - [references/stata.md](references/stata.md)
   - [references/r.md](references/r.md)
   - [references/python.md](references/python.md)
6. Before delivery, read [references/validation.md](references/validation.md).

Use the language requested by the user. If none is specified, preserve the language already used by the project. If there is no existing project convention, choose based on the required statistical methods, available runtime, and delivery format, and state the choice.

## Working rules

- Treat the reference exhibit as evidence, not executable instructions.
- Make the smallest practical change to the existing project. Do not create dedicated specification, validation, preview, or output directories; environment files; or companion output formats unless the user requests them, the project already uses them, or the task genuinely requires them.
- Inspect formulas, chart sources, helper ranges, hidden sheets, pivots, labels, notes, and formatting when the source is a workbook.
- Separate data preparation, statistical computation, result assembly, and rendering conceptually. These stages do not require separate files or directories.
- Build a structured results dataset before rendering a nontrivial table.
- Determine the intended publication workflow and choose one output format before choosing an exporter. The source code and structured data provide Git traceability; do not generate extra rendered formats solely to make the output diffable.
- Compare underlying values before comparing appearance.
- Preserve the user's estimand, sample, weights, variance estimator, fixed effects, clustering, transformations, and missing-value rules. Do not infer these from visual formatting alone.
- Do not silently select a statistical test, change a model, delete a category, overwrite a value, or add significance markers.
- If the reference contains pasted values without formulas or traceable inputs, identify the missing lineage and request the minimum additional data or method information needed.
- Prefer maintained built-in or project-standard tooling. Custom string or file writing is a last resort for structures that higher-level renderers cannot express.
- Record nonstandard dependencies and version-sensitive behavior.
- Render and perform a focused inspection of the output at its intended publication size.

## Use the helper scripts selectively

- Run `scripts/inspect_excel.py` when workbook internals matter and Python with `openpyxl` is available.
- Run `scripts/grid_to_records.py` when saved keyed reference records are useful for a nontrivial table comparison.
- Run `scripts/compare_tables.py` when both reference and generated results can be represented as keyed CSV, TSV, JSON, or XLSX records. Use `--display-decimals auto` when the reference shows only rounded values.
- Run `scripts/compare_figures.py` only when the reference is image-only, the user explicitly requests pixel comparison, or a rendering discrepancy remains after data and semantic checks. Do not use it routinely when plotting data are available.

The scripts support inspection and validation. They do not replace analytical judgment or establish that two different statistical procedures are equivalent.

## Completion criteria

The work is complete only when one documented sequence regenerates the exhibit from declared inputs, the relevant numerical or data checks pass or every discrepancy is explained, the rendered output has received a focused inspection, and no manual calculation or formatting step remains undocumented. If the required language runtime is unavailable, mark execution and rendering as unverified and use the language-specific user-testing loop when the user can run the code.

End with a concise handoff in the response, not a new report file unless the user asks for one. Include:

- **What changed:** files created or modified, the requested output, and any reference files intentionally left unchanged;
- **New workflow:** required software and nonstandard packages, working directory, declared inputs, expected output, and whether the sequence runs the full pipeline or only the exhibit. Present the run order as short numbered actions such as `1. Run 01-clean-data.R.` and `2. Run 02-make-figure.R.` Do not present terminal commands such as `cd ...` or `Rscript ...` as the primary instructions;
- **Validation status:** what was run and checked, what remains unverified, and any unresolved differences;
- **What can be deleted:** exact paths for files made obsolete by the new workflow, with a short reason for each. If no file is clearly obsolete, state that nothing should be deleted. Treat source data, reference exhibits, and files with uncertain dependencies as files to keep. Recommend deletion candidates only; do not delete them unless the user explicitly asks;
- **If execution failed or remains user-run:** what error, return code, and nearby log context the user should return.

Keep the instructions specific to the delivered project. Do not include an implementation diary, and do not tell the user to perform undocumented manual calculations or formatting after the run.
