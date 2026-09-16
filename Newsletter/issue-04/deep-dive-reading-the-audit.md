# Deep Dive (Track C, Part 1): Reading the Audit Report

*Background article for AI for Research, Issue 4. Reading time: about 12 minutes.*

The [World Bank Reproducibility Package skill](https://github.com/worldbank/wb-reproducible-research-repository/releases/latest) has four phases: Audit, Outline, Build, Run check. The [setup guide, slides, and demo project](https://dime-worldbank.github.io/ai-research-training/sessions/ai-skills-reproducibility/) cover how to install it and how the full workflow works.

This is only about the first phase. Most people skip past it. That's a mistake. The audit is the part that actually tells you something, and it comes back as four tables. If you don't know what you're looking at, it's easy to nod through the report and approve a pile of changes you haven't checked.

## What the audit is checking

The audit asks whether someone else can take your code and your data, run them on their machine, and get the exhibits in the paper. That's computational reproducibility. It's also what the Reproducible Research team checks when they verify a PRWP package.

Two other things sound similar and are not the same:

| Check | Question | Who does it |
| --- | --- | --- |
| **Computational reproducibility** | Same code + same data → same exhibits? | The audit; PRWP verification |
| **Replication** | Same data + the paper, no code → same results? | Replication studies (see this issue's Field Notes) |
| **Code review** | Does the code do what the paper says, and can someone else read it? | A person, with or without an agent |

Every row in the audit is about the first question. None of it answers the other two.

## The four tables

The audit doesn't change files. It looks through the project, reads the manuscript if there is one, and gives you:

1. **Checklist status.** Each item in the official package requirements, marked present, partial, or missing, with the file that is supposed to cover it. "Present" should mean someone checked the contents, not that a file with the right name exists.
2. **Flag table.** Each of the 14 common failure flags (F1–F14), marked PASS, FLAG, or N/A, with a file and line. These are the things that most often send a package back.
3. **Data classification.** Every data file in scope, marked as an *external input* (nothing in the code writes it) or an *intermediate/output* (some script writes it), plus whether each external input is in the Data Availability Statement.
4. **Exhibit coverage.** Every table and figure in the manuscript, mapped to the script and output file that produce it. Gaps get marked.

Then it should stop and ask if you want to continue. If it starts proposing fixes in the same message, tell it to wait.

## The flag table, grouped by what actually happens

Fourteen flags is a lot. Easier to think about what would happen on a reviewer's machine.

**The run stops.** These are the errors behind the 74% in this issue's Big Number.

- **F1** hardcoded user paths outside the main script
- **F2** no single entry point and no documented run order
- **F3** `cd` / `setwd` / `os.chdir` scattered through analysis scripts
- **F5** user-written packages not installed by the code
- **F8** an external input the code reads that the package doesn't ship and doesn't document

**The run finishes, but the numbers differ.**

- **F4** randomness without a seed (including Stata sorts before `_n` without a unique key)
- **F6** software and package versions not pinned
- **F7** manuscript and code out of sync (about 35% of verification failures)
- **F9** exhibits or in-text numbers not produced by code
- **F12** outputs written into the raw data folder, or scripts overwriting their own inputs

**The run works, but the reviewer has to guess.**

- **F10** no exhibit → script → output mapping in the README
- **F11** files the package doesn't need (notes, old versions, `.DS_Store`)
- **F14** a long or oversized run with no documented pathway

One flag sits above the rest: **F13**, restricted or sensitive data sitting in a package that is about to be published. If that one comes up, deal with it first.

This grouping is also a decent order for later fixes. Stop the crashes first, then the number changes, then the things that waste the reviewer's time.

## Don't take a FLAG at its word

A FLAG is a claim with a citation. Open the file at the line it names and decide:

- **Confirmed.** It's there, and it matters.
- **Needs a look.** The pattern is there, but you're not sure it matters. A `sample()` call flagged under F4 that only reorders labels on a plot, for example.
- **False alarm.** The search matched something harmless. `Dropbox` in a comment. A `library()` call for a package that already lives in the project's `renv/` folder.

The skill's own notes say a flag is not automatically a failure. You can fix it, or you can explain it in the README. What you shouldn't do is ignore it.

If the same false alarm shows up on two projects, tell the reproducibility team. The patterns live in `references/flags.md` and can be tightened.

## Read the data table slowly

This is the table a reviewer would otherwise build by hand: which files came from outside the project, and which of those are documented.

Read it both ways.

- Every file marked EXTERNAL INPUT should have a DAS entry with filename, source, URL, and access year. If it doesn't, that's F8.
- Every file the code *reads* should either be in the package or documented with access instructions. If it is neither, the reviewer's run will crash.

The audit also tries to match external inputs against a list of common datasets (WDI, PWT, OECD, ILO, and so on) and rates its confidence as LIKELY, POSSIBLE, or UNKNOWN. Treat UNKNOWN as a question for you. Don't let the agent fill in an access date, version, or license you haven't confirmed.

## Some rows only you can answer

A few items will come back as open questions. That's the audit doing its job. It is supposed to ask, not invent, when it hits:

- the source of a dataset it can't identify
- whether survey or monitoring data you collected is forthcoming, restricted, or public
- run times
- whether the manuscript in the folder is the final one
- whether an unused file should be deleted or just moved out of the package

Answer those before you approve anything in Outline. A DAS with a made-up access story, or an exhibit list with filenames that only sound right, is worse than a gap. A reviewer will notice, and then they won't trust the rest of the README.

## Don't let it edit yet

The audit and the fixes are separate on purpose. An agent can spot a real problem and still "fix" it badly. It might move a file to clean up a hardcoded path and break three other scripts. It might put a seed at the top of `main` and miss the bootstrap two files down.

The order is: audit, you check the findings, Outline proposes fixes, you approve the rows you want, then Build, then Run check.

Nothing should be written until you approve the Outline. If you tell it to "just fix everything," it is supposed to show you the plan first. Let it.

## A clean audit is not the end

A package that passes every flag but has never been run from scratch isn't finished. Phase 4 sets the old outputs aside, runs the main script from a fresh copy in a new folder, and checks that every expected file comes back with a new timestamp and is not empty. For Stata and Matlab, which the agent usually can't run, it hands you the same checklist.

Do the fresh-copy step. That's how you catch the path that still points at the old project.

## What the audit won't tell you

None of this tells you whether the exhibits are *right*.

A package that audits clean can still:

- run the wrong specification
- apply a sample cut that isn't the one in the paper
- merge on the wrong key and quietly duplicate or drop rows
- be so hard to read that the next RA starts over

Those are code review problems. They survive a reproducibility check because the package reproduces. It just reproduces the wrong thing.

If your team has extra checks (merge assertions, naming rules, how you set seeds), keep them out of the reproducibility skill. Put them in a project `AGENTS.md` or a separate review skill. Don't copy the official checklist into a home-grown prompt. Issue 2's Deep Dive is about encoding team conventions in memory files.

## One thing to remember

Read the four tables before you type "proceed." The audit only helps if someone looks at the evidence.
