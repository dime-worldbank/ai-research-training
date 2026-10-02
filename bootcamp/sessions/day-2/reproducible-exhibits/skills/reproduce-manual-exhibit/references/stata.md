# Stata implementation

Preserve the project's supported Stata version and existing conventions. Do not migrate a working exporter solely because a newer command exists.

## Choose the output before the exporter

Identify the paper or reporting workflow before writing export code. Produce one output format. If the desired table format is not established by the project or reference, ask whether the user wants Excel, Word-compatible DOCX or RTF, LaTeX, PDF, or HTML. For a figure with no established format, use PNG. Generate additional formats only when the user explicitly requests them.

Choose a deterministic format when practical:

- LaTeX workflow: `.tex`;
- Word workflow: `.docx`, `.rtf`, or `.html`, according to the requested workflow;
- Excel workflow: `.xlsx` or `.csv`, according to the requested workflow;
- web workflow: `.html` or Markdown.

The code and structured results remain the Git-trackable source of truth. Do not create a companion export solely because the requested artifact is binary. Avoid timestamps, machine-specific paths, and unstable ordering in generated text outputs.

## Data and computation

Use explicit `merge`, `collapse`, `contract`, `reshape`, `generate`, and `egen` steps as appropriate. Assert merge keys and inspect unmatched observations. Keep sample restrictions near the calculation they affect.

For nontrivial tables, store results in a `collect` collection, frame, posted dataset, or documented results dataset. Avoid long chains in which formatted table objects are the only surviving representation of computed values.

Choose the intermediate representation deliberately:

- Use a matrix for compact, rectangular, primarily numeric results, especially when results already exist in `r()` or `e()` matrices. Preserve row and column names and do not let display formatting replace the full-precision values.
- Use `postfile`, a frame, or a results dataset when combining commands, models, labels, p-values, annotations, and display metadata. Prefer this for bespoke publication tables and for outputs that require independent validation.
- Use `collect` when the supported Stata version can capture the results and express the required layout, especially when the same table may be exported to multiple formats.

## Table routing

Choose a renderer based on the requested output and the supported Stata version:

- Excel: `collect export`, `putexcel`, or `export excel` from a results dataset;
- DOCX: `collect export` or `putdocx`;
- RTF: an established project command such as `esttab` or `asdoc`, or controlled text generation when necessary;
- LaTeX: `collect export`, an established project command such as `esttab`, or controlled `file write`;
- PDF: `putpdf` or a generated LaTeX source compiled outside Stata;
- HTML or Markdown: `collect export`, dynamic reporting, or controlled text generation.

Prefer built-in or already-established project tooling when it can express the table. Community commands such as `asdoc`, `esttab`, or `outreg` are valid choices when they match the requested format and project conventions; record their installation source or version and do not install them without authorization.

Use `file write` when a text format requires layout that higher-level tools cannot express. Handle escaping, delimiters, missing values, decimal formatting, special characters, and line endings explicitly. Do not recompute statistics while rendering.

## Models

Make fixed effects, weights, clustered or robust variance estimators, omitted categories, interaction coding, and estimation samples explicit. Derive observation and cluster counts from the relevant estimation result rather than a convenient neighboring model.

## Figures

Create graphs from a declared plotting dataset and export them with explicit dimensions and format. Preserve scheme dependencies or replace them with documented graph options.

## Verification

Determine whether Stata can be run with a bounded preflight. Perform at most one ordinary executable-discovery step, checking the configured project command and common Stata command names together, followed by at most one minimal batch smoke invocation if an executable is found. Do not scan the filesystem broadly, attempt installation, debug licensing, or spend extended time discovering a runtime.

If Stata is available and execution is permitted:

1. Run the generated code rather than stopping at syntax review.
2. Fix syntax and runtime errors before delivery.
3. Run the final workflow from a clean Stata session, save the log, and inspect the generated exhibit.
4. Do not ask the user to test code that can be tested directly.

If the executable is not found, the smoke invocation fails because Stata cannot start, or execution is not permitted, switch promptly to the user-run loop:

1. Mark the code, values, and rendering as unverified.
2. Ask the user to run the do-file and paste the first error, its return code, and nearby log output.
3. Diagnose and revise one error at a time. Treat the proposed cause as a hypothesis until the revised command runs.
4. Repeat the run-report-revise loop until the do-file completes.
5. Ask the user to share the generated artifact or a rendered view for visual validation when feasible.

Do not require the user to diagnose the error. If the user cannot run Stata either, deliver the draft code with the unverified status and exact future validation steps.
