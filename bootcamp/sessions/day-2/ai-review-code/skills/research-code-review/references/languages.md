# Language-Specific Review Flags

Apply these rules alongside `review-flags.md`. This file contains only
language-specific style or syntax checks. Shared risks such as joins, paths,
randomness, dependencies, hidden state, and output stability are defined only
in `review-flags.md`.

## Stata

| ID | What to detect | Severity guidance | Recommended response | AI implementation |
|---|---|---:|---|---|
| STATA-STYLE-001 | Hard tabs or inconsistent indentation inside braces or after `///` | Low | Replace tabs with consistent spaces and indent nested blocks and continued lines. | Yes |
| STATA-STYLE-002 | Abstract loop locals such as `i` or `x` when a descriptive name is available | Low | Rename the loop local and all references to describe the iterated object. | Yes |
| STATA-STYLE-003 | Long lines that obscure logical components | Low | Break at a meaningful boundary with `///` and indent the continuation. | Yes |
| STATA-STYLE-004 | Missing whitespace around operators or before opening braces | Low | Add consistent spacing without changing expressions. | Yes |
| STATA-COND-001 | Implicit truth checks such as `if var` | Medium | State the intended comparison explicitly. Researcher input is required if the intended value is unclear. | Conditional |
| STATA-COND-002 | Numeric comparisons that unintentionally include Stata missing values | High when the sample or result changes; otherwise Medium | Add an explicit missing-value condition suited to the intended logic. | Conditional |
| STATA-COND-003 | Tilde used for logical negation | Low | Use `!` consistently. | Yes |
| STATA-LABEL-001 | Variables or coded categorical values lack the Stata variable or value labels needed to interpret them, or related label definitions are contradictory | Medium; High when an incorrect label can change interpretation | Use the authoritative codebook or project documentation to add or correct variable and value labels, then verify the label definitions. Do not invent labels. | Conditional |
| STATA-MACRO-001 | Global reference without `${...}` | Low; raise only when expansion can be ambiguous or incorrect | Use braced global references to avoid ambiguous expansion. | Yes |
| STATA-PATH-001 | Backslashes in likely file paths | Medium | Quote paths and use forward slashes. | Yes |
| STATA-SYNTAX-001 | `#delimit` in analytical code | Low | Prefer readable line continuation with `///`. | Conditional |

Do not flag an isolated pattern when surrounding code already makes the
behavior safe. Style findings remain Low unless they create a concrete higher
risk. When a Stata label issue also matches `CLEAN-003`, report one finding
using the more specific `STATA-LABEL-001` rule.

## R

| ID | What to detect | Severity guidance | Recommended response | AI implementation |
|---|---|---:|---|---|
| R-STYLE-001 | Inconsistent naming, spacing, assignment, or file organization materially impedes review | Low | Apply focused Tidyverse-style improvements without broad unrelated formatting changes. | Yes |

## Python

| ID | What to detect | Severity guidance | Recommended response | AI implementation |
|---|---|---:|---|---|
| PY-STYLE-001 | PEP 8 naming, spacing, import, or layout problems materially impede readability or obscure logic | Low | Apply focused formatting and naming improvements without broad unrelated changes. | Yes |

## Other languages

Apply the shared flags in `review-flags.md`. Inspect project-native dependency,
format, and test configuration when present, but do not run it in Phase 1. Do
not invent ecosystem-specific requirements. Flag only patterns whose
effect can be explained from the code and the shared research-code principles.

## Sources

- DIME Analytics Coding Guide and Stata Style Guide:
  https://worldbank.github.io/dime-data-handbook/coding.html
- DIME Stata Peer Code Review Checklist:
  https://github.com/worldbank/dime-standards/blob/master/dime-coding-standards/checklists/Stata%20Code%20Review%20Checklist.md
- Tidyverse Style Guide: https://style.tidyverse.org/
- PEP 8: https://peps.python.org/pep-0008/
