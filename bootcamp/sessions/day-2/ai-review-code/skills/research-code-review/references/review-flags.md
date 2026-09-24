# Research Code Review Flags

This catalog turns the approved review checklists and standards into
evidence-based flags. Apply rules contextually. A pattern is not a finding when
surrounding code already controls the risk or the behavior is documented and
appropriate.

## Flag fields

Each row provides what to detect, severity guidance, the recommended
response, and whether an AI agent can normally implement the response.

- **Yes:** mechanical when intent is clear.
- **Conditional:** implement only after documentation, safe data, tests, or
  user confirmation establishes the intended behavior.
- **No:** do not offer as a straightforward fix because code and data alone
  cannot determine the correct research or privacy decision. The AI may still
  implement an exact decision after the responsible user provides and approves
  it.

Use only these three values. Data availability can make a **Conditional** fix
safe to implement, but it does not make a **No** fix automatic: research-design
and privacy decisions still require the responsible researcher.

Escalate only when evidence shows broader or more consequential impact.
De-escalate or report a limitation when the risk cannot be established through
static inspection.

## Privacy and secrets

| ID | What to detect | Severity guidance | Recommended response | AI implementation |
|---|---|---:|---|---|
| PRIV-001 | Credentials, tokens, passwords, private keys, or connection secrets embedded in code or configuration | Critical | Revoke exposed credentials, remove them from tracked files and history through an approved process, and load replacements securely. | No |
| PRIV-002 | The reviewed package appears to contain actual confidential data or exposed sensitive values despite the user's confirmation | Critical when supported by concrete evidence | Stop inspection, do not expose values, and ask the user to remove the data or move the review to an approved secure environment. Code that merely references restricted data is not enough to raise this flag; report that the referenced data were not inspected as a limitation. | No |
| PRIV-003 | Direct or indirect identifiers are retained in an output intended to be shared or published | Critical when confirmed; otherwise High | Apply an approved de-identification review before sharing and document the decision. | No |

## Package structure and documentation

| ID | What to detect | Severity guidance | Recommended response | AI implementation |
|---|---|---:|---|---|
| PKG-001 | A complete package has no single documented entry point | Medium | Add or document an entry-point script that runs the intended workflow in order. | Conditional |
| PKG-002 | A complete package lacks a README covering software, versions, runtime, folders, entry point, configuration, scripts, and outputs | Medium | Add the missing operational documentation. | Conditional |
| PKG-003 | The mapping from inputs to scripts to outputs is unclear | Medium | Document the data flow and the script responsible for each final output. | Conditional |
| PKG-004 | Cleaning, construction, and analysis responsibilities are combined in a way that obscures execution order, inputs, outputs, or research decisions | Medium | Separate the stages or make their boundaries clear with sections, functions, modules, or a documented pipeline. | Conditional |
| PKG-005 | A script depends on undocumented state left in memory by another script | High | Make inputs explicit and initialize every required object, option, or dependency. | Conditional |
| PKG-006 | Core parameters or research choices must be changed in several locations | Medium | Centralize shared configuration and pass values explicitly. | Conditional |

Do not require a README for a narrow review of one or two standalone scripts.
Combining cleaning, construction, and analysis in one script is acceptable for
a small project when the boundaries, execution order, inputs, outputs, and
research decisions remain clear.

## Stability and reproducibility

| ID | What to detect | Severity guidance | Recommended response | AI implementation |
|---|---|---:|---|---|
| STAB-001 | Sampling, assignment, simulation, imputation, or randomized algorithms lack controlled randomness | High | Set and document the appropriate seed or generator immediately before the stochastic workflow. | Conditional |
| STAB-002 | An order-dependent operation lacks a complete deterministic sort | High when results may change | Sort on complete keys and add a unique stable tie-breaker. | Conditional |
| STAB-003 | Ties in ranking, sampling, deduplication, or assignment are not resolved consistently | High | Define and document a consistent tie-breaking rule. | Conditional |
| STAB-004 | Behavior depends on current date, time, locale, time zone, or encoding without an explicit parameter | Medium | Fix or document the relevant setting and parse values explicitly. | Conditional |
| STAB-005 | Required runtime or dependency versions are neither declared nor documented | Medium | Record the tested runtime and a reproducible dependency specification. | Conditional |
| STAB-006 | Code downloads mutable remote data or code without a version, date, or integrity check | High | Pin a versioned source and record provenance or checksum where appropriate. | Conditional |
| STAB-007 | User-specific paths, repeated roots, case assumptions, or launch-directory dependence reduce portability | Medium | Configure or resolve the root once and derive explicit platform-safe paths. | Conditional |
| STAB-008 | Interactive input, editor actions, or manual file selection is required during a production run | Medium | Parameterize the choice or isolate it outside the reproducible workflow. | Conditional |
| STAB-009 | Running the code more than once creates duplicate results or changes the outcome | High | Make reruns rebuild or replace outputs instead of unintentionally adding to earlier results. | Conditional |
| STAB-010 | Raw source data are overwritten or modified in place | Critical when destructive; otherwise High | Treat raw inputs as immutable and write derived data to separate locations. | Conditional |
| STAB-011 | Code uses a fixed temporary filename that could be overwritten or mistaken for a current intermediate file | Medium when a collision is realistically possible; otherwise Low | Use the language's temporary-file feature or a run-specific temporary directory, and remove temporary files safely after the run. | Yes |
| STAB-012 | Cleanup code may delete files outside the intended output folder | Critical when destructive; otherwise High | Restrict deletion to specific validated output paths and prefer recoverable deletion. | Conditional |
| STAB-013 | An automated workflow can report success after a required step fails or a declared final output is missing | High when the workflow can silently produce incomplete results; otherwise Medium | Check required steps and declared final outputs, and stop with a clear error when one fails or is missing. | Conditional |
| STAB-014 | A failed run can leave an incomplete output that looks final | High | Write to a temporary file, validate it, and move it to the final location only after success. | Conditional |
| STAB-015 | Output row or column order can change between runs | Medium | Set the intended row and column order before export. | Yes |
| STAB-016 | The code relies on a documented condition, such as unique IDs, expected allocation, preserved observations, or valid ranges, but does not check that the condition still holds | Medium; High when violating the condition could materially change results | Add a focused check for the documented condition near the operation that could violate it. Flag this only when the condition is stated or clearly required elsewhere in the package; otherwise report a limitation or question. | Conditional |

Static inspection cannot establish identical outputs across clean runs. Report
that limitation even when no stability flags are found.

## Identifiers, duplicates, joins, and appends

| ID | What to detect | Severity guidance | Recommended response | AI implementation |
|---|---|---:|---|---|
| DATA-001 | The expected unique ID or combination of keys is absent, unclear, or never validated | Medium; High if a consequential operation relies on it | Document the unit of observation and assert key uniqueness. | Conditional |
| DATA-002 | Duplicate records are removed using input order, first/last retention, or a forced operation such as Stata's `duplicates drop, force` without documented stable logic | High | Define duplicate criteria, establish stable ordering, inspect cases, and verify the resulting keys. | Conditional |
| DATA-003 | Join cardinality is not documented or validated | Medium | State the expected relationship, check key uniqueness, and inspect unmatched records and row counts. | Conditional |
| DATA-004 | A many-to-many join is explicit or confirmed, including Stata's `merge m:m` | High; Critical if it materially corrupted results | Determine the intended unit and relationship; use validated keys or document an intentional Cartesian operation explicitly. | Conditional |
| DATA-005 | Observations are dropped without justification or before counts and identities are inspected | High | Document the rule, report affected observations, and assert the intended result. | No |
| DATA-006 | Appended inputs may have incompatible names, types, units, categories, or schemas, or force incompatible inputs together | High | Harmonize and validate schemas before appending, then revalidate identifiers. | Conditional |
| DATA-007 | Type coercion can silently change identifiers, dates, categories, or numeric precision | High when values may change; otherwise Medium | Convert explicitly and validate representative and boundary values. | Conditional |
| DATA-008 | Required columns, types, ranges, categories, or nonmissing identifiers are assumed but not validated | Medium | Add focused schema and domain assertions near ingestion. | Conditional |

## Cleaning and missing data

| ID | What to detect | Severity guidance | Recommended response | AI implementation |
|---|---|---:|---|---|
| CLEAN-001 | Specific values are changed without documentation or justification | High when analysis values change; otherwise Medium | Document the source and rule, preserve an audit trail, and validate counts. | No |
| CLEAN-002 | Categorical values are represented inconsistently or in a way that creates ambiguous ordering, grouping, joining, or modeling behavior | Medium; High when the representation can change results | Use a documented, consistent categorical representation suited to the language and task. Strings are acceptable when they behave as intended. | Conditional |
| CLEAN-003 | Variables or categories needed to understand the data are undocumented, contradictory, or inconsistent across the package | Medium; High when incorrect documentation can change interpretation | Document them through the format best suited to the project, such as labels, a codebook, metadata, schema definitions, or the README. Use an authoritative source and do not invent definitions. | Conditional |
| CLEAN-004 | Missing, refusal, and don't-know values are conflated or handled inconsistently | High when results change; otherwise Medium | Establish and document a consistent missing-value scheme. | No |
| CLEAN-005 | Multiple writes make it unclear which dataset is the final clean output, or a partial dataset can overwrite the completed output | Medium; High when a partial output can be mistaken for final | Give the final clean output one clear location and use separately named, documented checkpoints or intermediates when they are useful. | Conditional |
| CLEAN-006 | Cleaning code constructs analysis indicators without a documented reason | Medium | Move reusable indicator construction to its own stage or document the exception. | Conditional |

## Variable construction and aggregation

| ID | What to detect | Severity guidance | Recommended response | AI implementation |
|---|---|---:|---|---|
| CONST-001 | A constructed variable does not clearly implement its documented definition | High when a mismatch is evident; otherwise report a question | Reconcile the code with the codebook or obtain a researcher decision. | No |
| CONST-002 | Transformations, normalization, units, or denominators are undocumented or unchecked | Medium; High when likely incorrect | Document the formula and add assertions or summaries for boundaries and units. | Conditional |
| CONST-003 | Aggregation uses incomplete grouping keys or handles missing values ambiguously | High | Confirm the target unit, complete grouping keys, and intended missing-value behavior. | No |
| CONST-004 | Winsorization or outlier handling lacks documented cutoffs, tails, or justification | High when results are affected | Obtain and document the research decision; verify the number and distribution of changed values. | No |
| CONST-005 | The dataset structure is inconsistent with its documented unit of observation, key structure, or downstream use | Medium; High when joins or analysis can be incorrect | Align the structure with its declared purpose and validate the intended keys. Wide or other non-tidy structures are acceptable when intentional, documented, and appropriate for downstream use. | Conditional |

## Sampling and random treatment assignment

| ID | What to detect | Severity guidance | Recommended response | AI implementation |
|---|---|---:|---|---|
| RAND-001 | Sampling or assignment methodology, eligibility, strata, clusters, or allocation is not documented | High | Document the design and connect each parameter to the implementation. | Conditional |
| RAND-002 | The frame lacks required IDs, strata, clusters, or eligibility checks | High | Validate the frame against the design before drawing the sample or assignment. | Conditional |
| RAND-003 | Probability weights are required but not calculated, stored, or documented | High | Calculate and document weights from the approved design. | No |
| RAND-004 | Code creates or removes observations during assignment without an approved reason | Critical when confirmed; otherwise High | Stop and reconcile the frame before using the assignment. | No |
| RAND-005 | Final sample or assignment outputs can be accidentally overwritten | High | Add an explicit finalization guard and preserve immutable released outputs. | Conditional |
| RAND-006 | Output lacks clear sampled/assigned status, labels, or supporting documentation | Medium | Export a documented assignment dataset with stable IDs and labels. | Conditional |

## Analysis and outputs

| ID | What to detect | Severity guidance | Recommended response | AI implementation |
|---|---|---:|---|---|
| ANALYSIS-001 | Analysis code contains substantial reusable transformations that obscure the source of the analysis sample or should apply consistently across multiple outputs | Medium; High when outputs can use inconsistent samples or definitions | Move shared transformations upstream or isolate and document them clearly. Temporary transformations needed for one table, figure, or model are acceptable. | Conditional |
| ANALYSIS-002 | Sample selection, missing-data handling, model choices, or other research decisions are hard-coded without explanation | High | Document the decision and obtain researcher confirmation before changing it. | No |
| ANALYSIS-003 | A categorical variable is treated as continuous without evidence that this is intended | High when model interpretation changes | Confirm intended encoding and model specification with the researcher. | No |
| ANALYSIS-004 | Functions or statistical methods appear inconsistent with the documented estimand or design | High only with concrete evidence; otherwise report a question | Reconcile the implementation with the analysis plan or researcher intent. | No |
| OUTPUT-001 | Tables, figures, or final datasets require manual copying or undocumented formatting | Medium | Generate final outputs directly from code with stable filenames. | Conditional |
| OUTPUT-002 | Outputs are not clearly mapped to the scripts that generate them | Medium | Document the output-to-script mapping and use dedicated output locations. | Conditional |
| OUTPUT-003 | Shared results are not cross-checked for consistent totals, samples, or key statistics | Medium; High when inconsistencies are visible | Add checks for agreed invariants and reconcile discrepancies. | Conditional |

## High-frequency checks

Apply these only when the package implements survey monitoring or HFCs. An
absent check is a flag only when the survey design, monitoring plan, or
available instrument metadata establishes that the check is applicable.

| ID | What to detect | Severity guidance | Recommended response | AI implementation |
|---|---|---:|---|---|
| HFC-001 | Tracking outputs require manual refresh or edits | Medium | Build an automated refresh from declared inputs. | Conditional |
| HFC-002 | Attempts, completions, refusals, or response rates are missing overall or by important dimensions | Medium | Produce documented status and rate summaries by time and enumerator where applicable. | Conditional |
| HFC-003 | Interview duration, module duration, or extreme durations are not assessed | Medium | Add documented duration summaries and review thresholds. | Conditional |
| HFC-004 | Duplicate IDs, key missingness, outliers, or logical inconsistencies are not reported | High when collection decisions rely on the checks; otherwise Medium | Add transparent, reviewable flags without silently altering source data. | Conditional |
| HFC-005 | Form versions or changes over time are not tracked | Medium | Report records by version and date and flag unexpected version use. | Conditional |
| HFC-006 | Enumerator-level error, duration, missingness, or inconsistency summaries are absent where supervision requires them | Medium | Add fair, documented monitoring summaries and protect respondent confidentiality. | Conditional |

## Sources

- DIME peer code-review guidance and checklists:
  https://github.com/worldbank/dime-standards/tree/master/dime-coding-standards/checklists
- DIME research reproducibility standards:
  https://github.com/worldbank/dime-standards/tree/master/dime-research-standards/pillar-3-research-reproducibility
- DIME data security standards:
  https://github.com/worldbank/dime-standards/tree/master/dime-research-standards/pillar-4-data-security
- DIME Data Map:
  https://github.com/worldbank/dime-standards/tree/master/dime-coding-standards/data-map
