# Phase 1 Report

Begin with a brief **Review scope and limitations** section. Then present the
findings and recommendations table.

## Required structure

### Review scope and limitations

Include:

- review type: **Complete package** or **Selected files**;
- files and directories reviewed;
- languages and research tasks detected;
- presence of a README and entry point when reviewing a package;
- excluded files or components;
- data, execution, tests, and outputs not examined;
- any uncertainty about intended behavior.

State explicitly that Phase 1 is a static review and does not establish
computational reproducibility.

### Flags and recommendations

Sort findings by severity: Critical, High, Medium, then Low. Within a severity,
follow execution order when it can be inferred.

| Flag | Severity | Code location | Recommendation |
|---|---|---|---|
| Concise evidence-based finding | Critical / High / Medium / Low | `path/file.ext:line` | Specific best-practice response |

The **Flag** cell must state what was observed and the concrete concern. Use
`Possible:` when the evidence is incomplete. The **Recommendation** cell must
state when researcher judgment is required. Consolidate repeated instances
when they share one cause, while listing representative locations.

If there are no findings, say:

> No actionable flags were identified within the reviewed scope. This does
> not establish computational reproducibility because the code and outputs
> were not executed.

### Next step

End with:

> Would you like to make these changes yourself, or would you like me to
> implement the straightforward recommendations?

If some findings require research decisions, identify them before asking this
question and exclude them from the offer of straightforward implementation.

## Recommendation quality

Every recommendation must be:

- traceable to a rule in `review-flags.md` or `languages.md`;
- supported by evidence in the reviewed code;
- relevant to the project and proportionate to the risk;
- specific enough to act on;
- clear about what was not verified.
