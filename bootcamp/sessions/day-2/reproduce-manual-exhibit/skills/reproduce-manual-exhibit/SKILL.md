---
name: reproduce-manual-exhibit
description: Reconstruct manually prepared Excel, Word, PDF, or image-based tables and figures as reproducible Stata, R, or Python workflows. Use when an existing exhibit defines the desired calculations, structure, or appearance and the user wants code that regenerates it from source data. Do not use for ordinary exploratory analysis without a reference exhibit.
---

# Reproduce Manual Exhibit

Convert a manually assembled table or figure into a transparent workflow that starts from source data and regenerates the deliverable without undocumented edits.

## Required outcome

Deliver, when the available evidence permits:

- executable source code in the requested language;
- a generated table or figure in the requested format;
- a compact reconstruction specification recording analytical and display choices;
- a validation report comparing the generated result with the reference;
- concise instructions for running the updated pipeline;
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
- Inspect formulas, chart sources, helper ranges, hidden sheets, pivots, labels, notes, and formatting when the source is a workbook.
- Separate data preparation, statistical computation, result assembly, and rendering in the generated workflow.
- Build a structured results dataset before rendering a nontrivial table.
- Determine the intended publication workflow and output format before choosing an exporter. When practical, generate a deterministic, Git-trackable canonical artifact alongside binary deliverables.
- Compare underlying values before comparing appearance.
- Preserve the user's estimand, sample, weights, variance estimator, fixed effects, clustering, transformations, and missing-value rules. Do not infer these from visual formatting alone.
- Do not silently select a statistical test, change a model, delete a category, overwrite a value, or add significance markers.
- If the reference contains pasted values without formulas or traceable inputs, identify the missing lineage and request the minimum additional data or method information needed.
- Prefer maintained built-in or project-standard tooling. Custom string or file writing is a last resort for structures that higher-level renderers cannot express.
- Record nonstandard dependencies and version-sensitive behavior.
- Render and inspect the output at its intended publication size.

## Use the helper scripts selectively

- Run `scripts/inspect_excel.py` when workbook internals matter and Python with `openpyxl` is available.
- Run `scripts/compare_tables.py` when both reference and generated results can be represented as keyed CSV, TSV, JSON, or XLSX records.
- Run `scripts/compare_figures.py` only as a secondary rendered-image check. Validate plotted data and chart semantics first.

The scripts support inspection and validation. They do not replace analytical judgment or establish that two different statistical procedures are equivalent.

## Completion criteria

The work is complete only when one documented command regenerates the exhibit from declared inputs, the numerical comparison passes or every discrepancy is explained, the rendered output has been inspected, and no manual calculation or formatting step remains undocumented. If the required language runtime is unavailable, mark execution and rendering as unverified and use the language-specific user-testing loop when the user can run the code.

End the handoff with run instructions that identify:

- required software and nonstandard packages;
- the working directory and any paths or configuration the user must set;
- the exact command or entry-point file to run;
- the expected outputs and where they will be written;
- whether the instructions run the full project pipeline or only the reconstructed exhibit;
- the current validation status;
- what error and log context to return if the pipeline fails.

Keep the instructions specific to the delivered project. Do not tell the user to perform undocumented manual calculations or formatting after the run.
