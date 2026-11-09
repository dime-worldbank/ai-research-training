# Deep Dive (Track C, Part 3): Builder and Critic

*Background article for AI for Research, Issue 8. Reading time: about 12 minutes.*

*Based on Impact Analytics' November 9 training, "AI Skills for Code Review", and the `research-code-review` skill. Checked against the skill as released on November 9, 2026.*

Impact Analytics' November 9 training showed a skill that reviews research code the way DEC's peer code review used to: against a fixed checklist, with severity levels, and with nothing changed until you say so. This article is about one way to use it that the training only touched on. If an agent wrote the code, have a different agent review it. Builder and critic, kept apart.

## 1. Why not just ask the same agent to check its work?

Because it will mostly say the work is fine.

This is not a quirk of one tool. A model asked to review code it has just written is looking at output that it, by construction, judged to be the best answer. It has the same blind spots the second time round. Ask it "are you sure?" and it will usually either agree with itself or change something that was right. The research on this is fairly consistent: models correct themselves reliably only when something from outside tells them what is wrong, such as a failing test, a compiler error, or a person. Field Notes in this issue goes through the evidence.

In human terms, this is why the author of a do-file is the worst person to find the bug in it, and why peer code review paired people up in the first place. The AI version of the problem is the same, and so is the fix.

## 2. What "a different agent" means in practice

You do not need a second license. You need a second conversation, with a different brief, that has not seen the first one.

The builder is whatever wrote the code: Copilot in agent mode, Claude Code, or you. The critic is a new session, pointed at the code, with the review skill loaded and a prompt that says nothing about how the code came to exist.

```text
Read .agents/skills/research-code-review/SKILL.md and review only:
- code/02_clean_baseline.R
- code/03_merge_rounds.R
Treat this as a selected-files review.
```

Three things make it a real critic rather than the builder in a new window.

**Fresh context.** Start a new session. Do not continue the chat where the code was written. The builder's reasoning about why it did things a certain way is exactly what the critic should not have.

**A checklist it did not write.** This is what the code-review skill adds. The sixty-odd flags in `references/review-flags.md` come from DEC's peer review checklists and from the failures the reproducibility team sees most. The critic is not asked "is this good?" It is asked "does this have a many-to-many merge, a random draw without a seed, a missing-value code treated as a number, an absolute path?" Specific questions get specific answers.

**Read-only.** Phase 1 of the skill does not run code, open data, or edit anything. That matters for privacy, and it also keeps the critic honest: it has to find problems by reading, and report them with a file and line number, not by quietly fixing them and moving on.

A different model helps a little, and if you have both Copilot and Claude it costs nothing to use one as builder and the other as critic. But the separation of context and the checklist do most of the work. Same model, new session, skill loaded is already a big improvement on "check your work".

## 3. A worked example

The demo project from the training is an evaluation of a water pilot in twelve districts: one Stata do-file that assigns treatment, three R scripts that clean, check balance and estimate effects. Say Copilot wrote the R scripts from your codebook this morning.

Open a new session as the critic. After the privacy confirmation (the demo data are synthetic), the review comes back as a table. Three rows from a real run:

| ID | Flag | Severity | Location | AI implementation | Proposed next action |
| --- | --- | --- | --- | --- | --- |
| `STAB-001` | `runiform()` with no seed | High | `01_randomize_treatment.do:23` | Conditional | Provide a seed, then set it before the draw |
| `DATA-005` | Attriters dropped without a documented rule | High | `04_analyze_impacts.R:27` | No | Researcher decides and documents the rule |
| `STAB-007` | Absolute user path in every script | Medium | `02_clean_baseline.R:11` | Yes | Define the project root once, derive all paths |

Now the part that makes this a loop and not a one-off. You answer the form (`STAB-007: approve`, `STAB-001: provide: seed = 20261109`, `DATA-005: discuss`) and let the critic implement the approved items on a new Git branch. Then you read the diff. Then, if the diff touched anything that matters, you run the critic once more on the changed files, in yet another fresh session. The second review is usually short. If it is not, something in the first fix went wrong, and you have found it before the data did.

## 4. When the critic is wrong

It will be, sometimes. Two kinds of error, handled differently.

**False alarms.** The critic flags a pattern that is guarded somewhere it did not look, or misreads intent. The skill asks the agent to inspect surrounding code before flagging and to report a limitation rather than a finding when it cannot tell. Even so, read every High and Critical row against the code yourself before approving anything. Answer `defer` for the ones you disagree with; they stay on the open list, nothing changes, and you have a record of having considered them.

**Silence.** The critic cannot see what is not in the code. It does not know your sample should be 2,400 households, that attrition was 8% in the field report, or that the treatment variable is supposed to be balanced by stratum. Those are the `No` rows: research decisions it refuses to make. They are also the rows most worth your time, because the critic has done the cheap part (noticing that a decision exists and is undocumented) and left you the part only you can do.

The skill's own line on this is the right one: a code review tells you whether the code does what it says. It does not tell you whether what it says is the right analysis.

## 5. Making it a habit

Three places where a critic pass fits naturally.

- **End of a coding task.** The agent says it is done. Before you look at the output, run the critic on the files it touched. Ten minutes, and the findings are fresh enough to fix cheaply.
- **Before you hand code to someone else.** An RA sending scripts to a TTL, or a TTL sending a package to the reproducibility team. The critic's report is a useful cover note, especially the open items.
- **When a result surprises you.** Before you write the paragraph explaining the surprising coefficient, run the critic on the construction and analysis scripts. Merges that double rows produce surprising coefficients too.

If your team already has conventions the skill does not know, do not edit the skill. Put them in the project memory file or in a separate review skill of your own. Impact Analytics' December 3 training, Making Your Workflows AI-Enabled, is about writing those.

## What this article doesn't cover

It does not cover setting up the skill (the [session materials](https://dime-worldbank.github.io/ai-research-training/sessions/ai-skills-review-code/) do that), or the reproducibility audit, which is a different skill for a different question. It covers one habit: never let the agent that wrote the code be the only agent that read it.
