# Deep Dive (Track B, Part 1): Persistent Environment Profiles

*Background article for AI for Research — Issue 1. Reading time: ~12 minutes.*

A recurring finding across the productivity evidence — including the METR trial covered in this issue's Field Notes — is that AI assistance underdelivers when the assistant simply doesn't know the project: its conventions, its constraints, the things "everyone on the team knows." Memory files and skills are how you close that gap. This article walks through both, for GitHub Copilot, with research-specific examples.

## 1. What a memory file is (and is not)

A memory file is a plain-text instruction file that your coding assistant reads automatically at the start of every task in a repository. Think of it as onboarding documentation for a new RA — except this RA reads it every single time, never skims, and never forgets it mid-task.

GitHub Copilot supports several forms:

- **Repo instructions** (`.github/copilot-instructions.md`) — whole repository, every request. Team-wide conventions everyone must follow.
- **Agent instructions** (`AGENTS.md`) — whole repository (agent mode / coding agent). Same role; use one or the other consistently.
- **Scoped instructions** (`.github/instructions/*.instructions.md`) — files matching an `applyTo` glob. Language- or folder-specific rules (e.g. Stata-only rules).
- **Prompt files** (`.github/prompts/*.prompt.md`) — invoked on demand. Reusable task templates; see "skills" below.

A memory file is **not** a wish list ("write good code") and not documentation for humans (that's the README). Every line should change what the assistant *does*.

## 2. What belongs in a research team's memory file

The highest-value content, in order:

1. **The stack and versions.** "Stata 18 and R 4.4. No Python unless explicitly requested."
2. **Package constraints.** "R: use `data.table`, not `dplyr`. Stata: `reghdfe` for fixed effects, `estout` for tables. Do not introduce new dependencies without asking."
3. **Folder and path conventions.** "All paths relative to the project root set in `main.do`. Never hardcode absolute paths. Raw data in `data/raw/` is read-only."
4. **Output conventions.** "Every table goes to `outputs/tables/` as `.tex` via `esttab`. Figures as `.pdf`, 300dpi, named `fig_<section>_<slug>`."
5. **The things it always gets wrong.** This is the most underrated section. If the assistant keeps using `merge 1:1` where your team requires an assert on `_merge`, write that down: "After every merge, `assert` the expected `_merge` pattern and drop `_merge`."
6. **Reproducibility rules.** "Set seeds explicitly. The main script must run top-to-bottom on a clean machine. Any manual step must be flagged loudly."

### A minimal starting template

Example file to save as `.github/copilot-instructions.md`:

```markdown
# Project instructions for AI assistants

## Stack
- Stata 18 (primary), R 4.4 (figures only). No Python.

## Conventions
- Paths: relative only, root defined in `main.do`. `data/raw/` is read-only.
- Fixed effects: `reghdfe`. Tables: `esttab` to `outputs/tables/*.tex`.
- After every merge: assert the expected `_merge` pattern, then drop `_merge`.
- Every new .do file gets a header: purpose, inputs, outputs, author.

## Things you get wrong
- Do not use `preserve/restore` inside loops.
- Variable labels are required for every generated variable.

## Reproducibility
- `main.do` must run top-to-bottom on a clean machine.
- Set seeds explicitly wherever randomness is involved.
```

Keep it under a page to start. A bloated memory file gets partially ignored — by the model and by the teammates who are supposed to maintain it.

## 3. Skills: from standing rules to repeatable workflows

Memory files hold *standing rules*. Skills hold *procedures* — multi-step workflows you want to run the same way every time, invoked on demand rather than always active.

In GitHub Copilot, the closest native mechanism is **prompt files** (`.github/prompts/*.prompt.md`): a markdown file describing a task, its steps, and its quality bar, which you invoke by name. Examples that map directly onto DECDI work:

- `clean-merge-check.prompt.md` — run the team's post-merge assertion checklist on the current file.
- `replication-audit.prompt.md` — scan a project for hardcoded paths, missing seeds, and undocumented manual steps; output a table of findings.
- `table-to-tex.prompt.md` — convert a results log into a formatted `esttab` call following house style.

The rule of thumb: the **third time** you type the same multi-step instruction into chat, it should become a skill file. The July 2 training materials include staff-built examples; the [DIME coding-agent exercises](https://github.com/dime-worldbank/coding-agent-exercise) let you practice both levels on four use cases of increasing complexity.

## 4. How memory files and skills work together

A useful mental model:

- **Memory file** = who we are, how we work, what never changes. Loaded always.
- **Instructions files** (`applyTo` globs) = the same, but scoped ("in `/stata/`, these rules apply").
- **Skills / prompt files** = named procedures with steps and acceptance criteria. Loaded when invoked.

A well-configured project means a new task starts with the assistant already knowing your stack, constraints, and quality bar (memory), and your recurring workflows are one command away (skills). That combination is precisely the "configuration investment" the productivity literature says separates AI users who gain time from those who lose it.

## 5. Maintenance: the part everyone skips

- Put the memory file in version control and review changes in PRs like code.
- When the assistant makes the same mistake twice, the fix is a line in the memory file, not a better one-off prompt.
- Prune quarterly. Rules that no longer bind are noise that dilutes the rules that do.
- One person owns it per project — usually whoever owns the replication package.

## Sources and further reading

- GitHub Docs: [Adding repository custom instructions for GitHub Copilot](https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot)
- GitHub Docs: [Prompt files](https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot#enabling-and-using-prompt-files)
- DIME: [coding-agent-exercise](https://github.com/dime-worldbank/coding-agent-exercise) — four hands-on exercises at increasing complexity
- METR (2025): [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) — the trial behind this issue's Field Notes (see caveats there)
