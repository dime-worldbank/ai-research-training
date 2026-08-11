# Deep Dive (Track B, Part 2): Beyond the Skill --- House Rules That Stick

*Background article for AI for Research --- Issue 2. Reading time: ~12 minutes.*

The July 16 session shipped the **World Bank Reproducibility Package skill**: a four-phase workflow (Audit -> Outline -> Build -> Run check) that embeds the reproducibility team's checklist and the most common reproducibility issues the team faces. That skill is the right default. This piece is about the next layer --- what to add *around* it so the agent also respects your team's project-level choices (folder names, language stack, merge checks) without inventing a parallel standard.

**Get the skill first:** [github.com/worldbank/wb-reproducible-research-repository/.../reproducibility-skill](https://github.com/worldbank/wb-reproducible-research-repository/tree/main/ai-skills/reproducibility-skill) · [packaged zip](https://github.com/worldbank/wb-reproducible-research-repository/releases/download/skill-v2026.07.08/reproducibility-skill.zip)

## 1. Skill first, house rules second

| Layer | What it encodes | Where it lives |
| --- | --- | --- |
| **Reproducibility skill** | Official checklist, the most common verification-failure patterns, README / DAS / main-script templates | `.agents/skills/reproducibility-skill/` |
| **Memory / instructions** | Your stack, folder names, "things you get wrong," package constraints | `.github/copilot-instructions.md` (or `AGENTS.md`) + scoped `.github/instructions/` |
| **Extra prompt skills** | Team-specific audits you run often *in addition* to the official skill | `.github/prompts/*.prompt.md` |

Do not rebuild the WB checklist in a chat prompt or a home-grown "replication skill." Update the official skill when the standard changes; everyone's next run picks it up. Use memory files for what the skill deliberately leaves open: *your* names for folders, *your* language mix, *your* recurring mistakes.

## 2. Separate required outcomes from team choices

The published guidance defines what a package must accomplish. It does not prescribe every folder name. Start with the skill's standard; then document the project-level choices that satisfy it.

1. **Master script contract.** One root script per language runs the pipeline after a single top-level path change. The skill's Phase 2-3 outline and build enforce this; your memory file should state the filename (`main.do`, `main.R`, ...). ([WB reproducibility checklist](https://worldbank.github.io/wb-reproducible-research-repository/reproducibility_package_checklist.html); [DIME Standards](https://github.com/worldbank/dime-standards))
2. **Clear separation and traceability.** Readers must distinguish source data, derived data, code, and outputs. The skill maps to `data/ · code/ · output/` --- if your team uses `outputs/` or `data/raw` + `data/clean`, say so in the memory file so Outline doesn't fight you.
3. **Language style guides.** Stata: DIME Analytics style. R: document `data.table` vs tidyverse. Python: PEP 8. Put these in scoped instructions so they only load for matching files.
4. **Documentation for replicators.** README with software versions, the one line to change, Data Availability, exhibit map --- the skill's assets already ship templates; don't freehand a competing README shape.
5. **Project validation rules.** Seeds, merge asserts, treatment of manual steps belong in team instructions when they apply. Don't present a project-specific rule as if it were part of the official verification checklist.

## 3. Encode structure in instructions, not vibes

Add a short section to `.github/copilot-instructions.md` *before* you ask the agent to reorganize. Keep it short; the skill already carries the checklist.

Example block (illustrative --- adapt to the project; the skill's Phase 2 outline is authoritative for the package tree):

```markdown
## Repository structure (project choices --- do not invent alternatives)
- Prefer the skill's target tree: `data/`, `code/`, `output/`.
- If we keep finer splits: `data/raw/` is read-only; derived data only under `data/` as agreed in Outline.
- Root: one entry point per language (`main.do` / `main.R` / `main.py`). Replicator changes a path in exactly one place per language.

## Stack
- Stata 18 (primary). R for figures only unless Outline says otherwise.
- Fixed effects: `reghdfe`. Do not introduce new dependencies without asking.

## Things you get wrong
- After every merge: assert the expected `_merge` pattern, then drop `_merge`.
- Prefer editing existing scripts over creating parallel "v2" copies.
- If a step cannot be automated, stop and flag it --- do not invent a workaround.
```

Pair this with Issue 1's "things you get wrong" list. The skill tells the agent *what the package must pass*; the memory file tells it *how this team works day to day*.

### Scoped rules for language-specific files

- `.github/instructions/stata.instructions.md` with `applyTo: "**/*.do"`
- `.github/instructions/r.instructions.md` with `applyTo: "**/*.{R,r,Rmd}"`

House layout stays repo-wide; syntax and package constraints go in the scoped files.

## 4. Use the skill's phases --- don't skip gates

The session's control model is the point:

| Phase | What happens | You do |
| --- | --- | --- |
| **1 · Audit** | Checklist + common failure patterns; data <-> README / DAS cross-check | Read the report. Change nothing yet. |
| **2 · Outline** | Target structure + gap table | Approve, edit, or reject rows. |
| **3 · Build** | README, DAS, main script, approved fixes | Only after Outline approval. |
| **4 · Run check** | Clean rerun; every exhibit regenerates | Confirm timestamps / non-empty outputs (or follow the Stata clean-run protocol the agent prints). |

A package that audits clean but has never run from scratch is not done. That is Phase 4, not a vibe check.

Useful patterns to keep in your head when reading an Audit (the full list lives in the skill's `references/flags.md`):

- Hardcoded user-specific paths  
- No single entry point  
- Randomness without a seed  
- Input data missing from DAS  
- Outputs not produced by code  
- Missing README / List of Exhibits  

## 5. Optional extras --- only after the skill

Memory files are always-on. The reproducibility skill is the on-demand standard. Extra prompt files are optional *add-ons* for team habits the skill doesn't cover, for example:

| Extra skill | When you need it |
| --- | --- |
| `merge-assert-check.prompt.md` | Your Stata merge discipline isn't in the official failure-pattern list |
| `exhibit-map-diff.prompt.md` | Manuscript still moving; re-diff paper exhibits vs. outputs after a rewrite |

Rule of thumb: if you're re-checking the WB checklist, run the official skill again --- don't duplicate it in a prompt file.

A copy-paste starter for house-rule instructions lives in [`templates/style-guide-instructions-template.md`](../../templates/style-guide-instructions-template.md).

## 6. A practical workflow for an existing project

1. **Install the skill** under `.agents/skills/reproducibility-skill/` (one-time per project).
2. **Freeze house rules** in the memory file (stack, folder choices, gotchas).
3. **Run Phase 1** with: *"Prepare a reproducibility package for this project."* Stop at the audit.
4. **Approve Outline** (Phase 2) before any moves.
5. **Build** (Phase 3) only for approved rows; use git so you can see every change.
6. **Run check** (Phase 4) --- or follow the clean-run protocol if the agent can't execute Stata.
7. **Human sign-off** --- someone who knows the analysis confirms "runs" means "runs the right thing," not only "exits zero."

This matches the lesson in this issue's Field Notes (SCORE) and Big Number (PRWP first-pass verification): packaging and human-approved gates are what move a project from "runs on my machine" to "passes someone else's check."

## 7. What not to automate yet

Leave these for a person even when the agent offers:

- Deciding which "raw" files are truly original vs. intermediate (the skill should *ask* about mystery files like `final_merged_v2.csv` --- don't let it guess).
- Data access wording and licensing in the Data Availability statement.
- Whether a manual download step is acceptable vs. must be scripted.
- Final mapping of paper exhibits when the manuscript is still moving.

The agent drafts the package; the team owns the claim that it reproduces the paper.

## Sources and further reading

- Skill: [Reproducibility Package skill](https://github.com/worldbank/wb-reproducible-research-repository/tree/main/ai-skills/reproducibility-skill)
- Session materials: [AI Skills to Facilitate Reproducible Research](https://dime-worldbank.github.io/ai-research-training/sessions/ai-skills-reproducibility/) · slides short link [bit.ly/ai-reproducibility](https://bit.ly/ai-reproducibility)
- World Bank: [Reproducibility package checklist](https://worldbank.github.io/wb-reproducible-research-repository/reproducibility_package_checklist.html)
- World Bank: [README template](https://github.com/worldbank/wb-reproducible-research-repository/blob/main/resources/README_Template.md)
- DIME: [dime-standards](https://github.com/worldbank/dime-standards)
- DIME Analytics: [Data Handbook --- reproducibility](https://worldbank.github.io/dime-data-handbook/reproducibility.html)
- Questions: [reproducibility@worldbank.org](mailto:reproducibility@worldbank.org)
- Issue 1 Deep Dive: Persistent environment profiles (memory files + skills)
- SCORE / Miske et al. (2026): [Investigating the reproducibility of the social and behavioural sciences](https://www.nature.com/articles/s41586-026-10203-5) --- see this issue's Field Notes
- World Bank: [500 packages on RRR --- first-pass verification rate](https://blogs.worldbank.org/en/impactevaluations/a-milestone-for-open-science--500-packages-in-the-world-bank-s-r)
