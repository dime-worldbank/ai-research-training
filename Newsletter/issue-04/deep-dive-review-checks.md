# Deep Dive (Track C, Part 1): Add Review Checks Around the Reproducibility Skill

*Background article for AI for Research, Issue 4. Reading time: about 12 minutes.*

The [World Bank Reproducibility Package skill](https://github.com/worldbank/wb-reproducible-research-repository/releases/latest) already checks the official package requirements and common failure patterns. The [setup guide, slides, and demo project](https://dime-worldbank.github.io/ai-research-training/sessions/ai-skills-reproducibility/) show how to audit or build a package in VS Code with GitHub Copilot or Claude Code.

This guide covers the next layer: turning comments your team often leaves on code into checks that a linter, coding agent, or clean run can apply again. These project or team checks should add context without replacing the official skill.

The goal is a short review with evidence. Each finding should name the file and line, explain the risk, and suggest a small fix. The researcher still decides whether the finding is valid and whether to change the code.

## 1. Choose the right type of check

Review checks fall into four groups:

| Type | Example | Best tool |
| --- | --- | --- |
| **Syntax or style rule** | No hardcoded user paths | Linter or text search |
| **Contextual code check** | Merge type matches the expected unit of observation | Coding agent using a checklist |
| **Runtime check** | Main script runs from a clean session | Language runtime or CI |
| **Research decision** | Sample restriction is justified | Researcher, with agent support |

Use a linter when the rule can be stated in a precise pattern. Use an agent when the check needs context from several lines or files. Use execution when the claim is about what the code produces.

## 2. Rewrite comments as testable rules

A comment such as "check the merge" gives the reviewer little direction. A reusable check needs four parts:

1. **Scope:** which files or commands it applies to.
2. **Condition:** what the reviewer should look for.
3. **Evidence:** what must be cited in a finding.
4. **Severity:** what can happen if the issue is real.

Example:

```markdown
### CR-01: Verify merge assumptions

- Scope: every Stata `merge` command
- Check: confirm that the declared merge type matches the unit of observation
  in both inputs; confirm that the expected `_merge` values are asserted before
  `_merge` is dropped.
- Evidence: cite the merge command, the input datasets, and the nearby
  assertion (or its absence).
- Severity: high if a wrong match can duplicate or drop observations;
  medium if the issue is missing validation only.
```

The check tells the reviewer what evidence is needed. It also keeps a missing assertion separate from a demonstrably wrong merge.

## 3. Require evidence before recommendations

Ask for a findings-only report:

```text
Review the named files against checks CR-01 to CR-03.

For each finding, provide:
1. severity;
2. check ID;
3. file and line;
4. the observed code;
5. why it creates a risk in this project;
6. the smallest suggested fix.

Do not edit files. Omit checks with no finding. Mark uncertain findings
"needs confirmation" and state what information is missing.
```

This format makes the report easier to inspect. It also gives you a record of which rule produced each finding.

## 4. Keep severity tied to consequences

Use a small scale:

- **High:** can change the sample, estimate, treatment assignment, or published output.
- **Medium:** can break a clean run or make the result hard to trace.
- **Low:** affects readability or team style without changing results.

Severity should follow the likely consequence in this project. A hardcoded path is medium in a replication package because it can stop another user from running the code. The same path may be low in a private scratch script.

## 5. Separate review from editing

Run review first. Confirm the findings. Then ask for changes.

This matters because an agent can identify a real issue and still suggest the wrong fix. For example, it may notice an unchecked merge but infer the wrong expected match pattern. The author or reviewer needs to confirm the unit of observation before code changes.

A useful sequence is:

```text
Review → confirm findings → propose fixes → approve → edit → run tests
```

For a small, known change, the proposal can be brief. For a review across several scripts, keep the finding and editing steps separate.

## 6. Add runtime checks

Static review cannot show that a package runs. Add a clean-run check:

1. Start a fresh session or environment.
2. Run the documented main script.
3. Stop at the first error.
4. Record the command, error, and missing file or dependency.
5. Fix the cause and restart from a clean session.
6. Compare generated exhibits with the expected list.

The first successful run is only part of the check. Confirm that every expected table and figure was regenerated and is non-empty.

## 7. Track false positives

After each review, mark findings:

- confirmed;
- needs confirmation;
- false positive.

If the same false positive appears twice, rewrite the check. Add the missing context, narrow the scope, or move the rule to a linter.

Example:

```markdown
### Before
- Flag any use of `preserve`.

### After two false positives
- Flag `preserve` inside loops. Do not flag a single `preserve` / `restore`
  pair around a short export step.
```

The second version describes the actual team concern.

## 8. Store checks where they will be used

- Keep the official package requirements in the reproducibility skill. Download the current release instead of copying its checklist into another prompt.
- Put deterministic rules in the DECDI linter or another language-specific linter.
- Put project-wide review rules in `.github/copilot-instructions.md` or `AGENTS.md`.
- Put a longer review workflow in a skill or prompt file.
- Keep research decisions in the analysis plan, README, or review notes.

Do not copy the same rule into several files. Pick one source and link to it where needed.

## A small starting set

For a typical research project, start with three checks:

1. **Merge assumptions:** keys, unit of observation, and match assertions.
2. **Paths and inputs:** project-relative paths and documented source files.
3. **Randomness and outputs:** explicit seeds and outputs generated by code.

Run them on one script. Revise any rule that produces vague findings. Add a fourth check only after the first three work.

## One rule

Ask for evidence before edits. A short report with file and line references is easier to review than a large set of automatic changes.
