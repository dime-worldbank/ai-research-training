# Exhibit specification

Create a compact YAML or JSON specification before writing substantial code. Adapt the fields to the task; omit irrelevant fields.

```yaml
id: table-01
kind: table
reference:
  file: reference.xlsx
  location: Results!B4:H20
source_data:
  files: [data/analysis.dta]
  unit_of_observation: household
  identifiers: [household_id, survey_round]
target:
  language: stata
  outputs: [outputs/table-01.tex]
  canonical_output: outputs/table-01.tex
  git_trackable: true
  publication_workflow: latex
sample:
  restrictions: []
  missing_value_rule: null
computation:
  archetype: baseline-endline-comparison
  weights: null
  variance_estimator: cluster
  cluster: community_id
display:
  decimals: 3
  standard_errors: parentheses
  significance_thresholds: null
assumptions: []
unresolved_items: []
```

## Canonical table results

For a nontrivial table, prefer one record per displayed statistic with fields such as:

| Field | Meaning |
| --- | --- |
| `panel` | Row block or panel identifier |
| `row_key` | Stable machine-readable row key |
| `row_label` | Displayed row label |
| `column_key` | Stable column identifier |
| `statistic` | Mean, SD, coefficient, SE, p-value, N, or another statistic |
| `value` | Full-precision numeric value |
| `display_order` | Explicit ordering |
| `format` | Display rule, not a modified analytical value |
| `annotation` | Stars, reference markers, or brackets |
| `source_model` | Calculation or model that produced the value |

For figures, preserve a plotting dataset containing the exact x, y, group, panel, and uncertainty values used by the renderer.

## Assumptions versus unresolved items

An assumption is a reversible interpretation supported by the reference. An unresolved item is information required for faithful reconstruction but not present in the supplied material. Do not convert unresolved analytical choices into assumptions merely to continue.
