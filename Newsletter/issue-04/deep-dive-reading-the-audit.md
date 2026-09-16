# Deep Dive (Track C, Part 1): Reading the Audit Report

*Background article for AI for Research, Issue 4. Reading time: about 12 minutes.*

The [World Bank Reproducibility Package skill](https://github.com/worldbank/wb-reproducible-research-repository/releases/latest) runs in four phases: Audit, Outline, Build, Run check. The [setup guide, slides, and demo project](https://dime-worldbank.github.io/ai-research-training/sessions/ai-skills-reproducibility/) cover installation and the full workflow.

This guide is about the first phase only. The audit is where the skill earns its keep, and it is the phase most people rush through. It produces four tables. Knowing what each one is for, and what none of them can tell you, is the difference between a useful report and a wall of text you approve without reading.

## 0. What the audit is checking

The audit checks **computational reproducibility**: can another person take your code and your data, run them on their machine, and regenerate the exhibits in the paper? That is the question the Reproducible Research team answers when it verifies a PRWP package.

It is not checking two other things that sound similar:

| Check | Question | Who does it |
| --- | --- | --- |
| **Computational reproducibility** | Same code + same data → same exhibits? | The audit; PRWP verification |
| **Replication** | Same data + the paper's description, no code → same results? | Replication studies (see this issue's Field Notes) |
| **Code review** | Does the code compute what the paper says, and can a colleague read it? | A human reviewer, with or without an agent |

Keep this table in mind while reading the report. Every row in the audit is evidence about the first question. None of it is evidence about the other two.

## 1. The four tables

The audit is read-only. It inventories the project, reads the manuscript if there is one, and returns:

1. **Checklist status.** Every item in the official package requirements, marked present, partial, or missing, with the file that satisfies it. "Present" is supposed to mean the content was verified, not that a file with the right name exists.
2. **Flag table.** Each of the 14 failure flags (F1–F14) marked PASS, FLAG, or N/A, with file and line evidence. These are the failures the Reproducible Research team encounters most often in verification.
3. **Data classification.** Every data file in scope, classified as an *external input* (nothing in the code writes it) or an *intermediate/output* (some script writes it), with a column showing whether each external input appears in the Data Availability Statement.
4. **Exhibit coverage.** Every table and figure in the manuscript mapped to the script and output file that produce it, with gaps marked.

Then it stops and asks whether to proceed. It should not propose fixes in the same message. If it does, tell it to hold them until Outline.

## 2. The flag table, grouped by what goes wrong

Fourteen flags is a lot to hold in your head. They fall into three families based on what happens on the reviewer's machine.

**The run stops.** These are the errors behind the 74% in this issue's Big Number.

- **F1** hardcoded user paths outside the main script
- **F2** no single entry point and no documented run order
- **F3** `cd` / `setwd` / `os.chdir` scattered through analysis scripts
- **F5** user-written packages not installed by code
- **F8** an external input the code reads that the package neither ships nor documents

**The run finishes, but the numbers differ.**

- **F4** randomness without a seed (including Stata sorts before `_n` without a unique key)
- **F6** software and package versions not pinned
- **F7** manuscript and code out of sync (about 35% of verification failures)
- **F9** exhibits or in-text numbers not produced by code
- **F12** outputs written into the raw data folder, or scripts overwriting their own inputs

**The run works, but the reviewer cannot tell.**

- **F10** no exhibit → script → output mapping in the README
- **F11** files the package does not need (notes, old versions, `.DS_Store`)
- **F14** long-running or oversized computation with no documented pathway

And one that outranks everything: **F13**, restricted or sensitive data physically present in a package headed for publication. If this is flagged, deal with it before reading anything else.

Sorting the flags this way also tells you the order to fix them in Outline: first the ones that stop the run, then the ones that change the numbers, then the ones that cost the reviewer time.

## 3. Triage every FLAG before you believe it

A FLAG is a claim with evidence attached. Your job is to check the evidence, not to trust the summary. Open the cited file at the cited line and mark the finding:

- **Confirmed.** The issue is there and matters for this package.
- **Needs confirmation.** The pattern is there but you are not sure it matters. Example: a `sample()` call flagged under F4 that only reorders labels for a plot.
- **False positive.** The detection pattern matched something harmless. Example: the string `Dropbox` inside a comment, or a `library()` call for a package that ships inside the project's `renv/` folder.

The skill's own reference file says a flag "is not automatically a failure — it is something the author must fix or explicitly justify in the README." Justifying is allowed. Ignoring is not.

If you find the same false positive twice across projects, tell the reproducibility team. The detection patterns are in `references/flags.md` and can be tightened.

## 4. The data classification table is the one to read slowly

This table does the work a reviewer would otherwise do by hand: figure out which files came from outside the project and whether each is documented.

Read it in two directions.

- **Forward:** every file marked EXTERNAL INPUT should have a DAS entry with filename, source, URL, and access year. Missing entry → F8.
- **Reverse:** every file the code *reads* should either exist in the package or be documented with access instructions. A read of a file that is neither present nor documented will crash the reviewer's run.

The audit also tries to identify external inputs against a list of common datasets (WDI, PWT, OECD, ILO and so on) and reports its confidence as LIKELY, POSSIBLE, or UNKNOWN. Treat UNKNOWN as a question addressed to you, not as a line item. Never let the agent fill in an access date, version, or license you have not confirmed.

## 5. Things only the author can answer

Several rows will come back as open questions. That is the audit working correctly, not failing. The skill is written to *ask* rather than invent when it hits:

- the source and access pathway for data it cannot identify;
- whether survey or monitoring data you collected is forthcoming, restricted, or public;
- run times per stage;
- whether the manuscript in the folder is the final version;
- whether an unreferenced file should be deleted or moved outside the package.

Answer these in your reply before approving anything in Outline. A DAS with an invented NDA pathway or an exhibit list with plausible-sounding filenames is worse than an honest gap, because a reviewer will find it and stop trusting the rest of the README.

## 6. Audit, then approve, then edit

The audit and the fixes are separate phases for a reason. An agent can spot a real problem and propose the wrong fix. It may notice a hardcoded path and "fix" it by moving the file, which breaks three other scripts that reference it. It may add a seed at the top of the main script and miss the bootstrap call two scripts down.

The sequence is:

```text
Audit → you confirm findings → Outline proposes fixes → you approve rows → Build → Run check
```

Nothing is written to the project until you approve the Outline. If you ask the agent to "just fix everything," the skill is written to show you the Outline first anyway. Let it.

## 7. Audit-clean is not done

A package that passes every flag but has never been run from scratch is not finished. Phase 4 sets aside the existing outputs, runs the main script from a fresh copy in a new location, and checks that every expected file regenerates with a new timestamp and is non-empty. For Stata and Matlab, which the agent usually cannot execute, it hands you the same checklist to run yourself.

Do the fresh-copy step. Copying the package to a new folder is what catches the path that still points at the old project.

## 8. Where the audit stops and code review starts

Everything above is about whether the package runs and regenerates the paper's exhibits. Nothing above tells you whether the exhibits are right.

An audit-clean package can:

- run the wrong specification;
- apply a sample restriction that does not match the one described in the paper;
- merge on the wrong key and silently duplicate or drop observations;
- be so hard to read that the next RA rewrites it from scratch.

Those are **code review** questions. Code review catches problems that a computational reproducibility check will never surface, because the package reproduces perfectly, just to the wrong answer. The two are complements, not substitutes: the audit tells you the package works; code review tells you it computes what the paper claims.

Teams that want to add their own checks (merge assertions, naming conventions, house rules for seeds) should keep them **separate** from the reproducibility skill. Put them in a project `AGENTS.md` or a dedicated review skill, and do not copy the official checklist into a home-grown prompt. Issue 2's Deep Dive covers how to encode team conventions in memory files. A later session in the series will cover AI-assisted code review using the DIME peer code review process.

## One rule

Read the four tables before you type "proceed." The audit is only useful if a human looks at the evidence.
