---
layout: default
title: "AI Onboarding: Memory Files and Skills"
permalink: /sessions/ai-skills-and-memory-files/
---

[← Back to the AI Roadmap series](../../)

# AI Onboarding: Memory Files and Skills

Hands-on exercises that show how **memory files** and **agent skills** change what a coding agent produces on the same research task.

Exercises live in a separate repo — do not clone it as one workspace. Download each exercise folder (or ZIP) and open them separately so you can compare runs with a clean agent context.

**Exercises:** [dime-worldbank/coding-agent-exercise](https://github.com/dime-worldbank/coding-agent-exercise)

**Objective:** see the difference between a bare coding agent, an agent with project memory, and an agent with both memory and reusable skills.

## Exercises

| Exercise | What you practice |
| --- | --- |
| [Main do-file](https://github.com/dime-worldbank/coding-agent-exercise/tree/main/basic-main-dofile) | In a small Stata project, run the same prompt three ways: no memory or skills → memory only → memory and skills. Compare the master do-file the agent writes. |
| [Agent skills (Lumora)](https://github.com/dime-worldbank/coding-agent-exercise/tree/main/advanced-research-roles-skills) | On a synthetic cash-transfer evaluation, compare agent output with and without role-specific skills for deck updates, high-frequency checks, and reproducible analysis. |

Each exercise folder has its own README with download links, prompts, and checklists.

### Main do-file (quick start)

1. Download the three ZIPs from the [latest release](https://github.com/dime-worldbank/coding-agent-exercise/releases/latest) (no memory/skills · memory only · memory and skills).
2. Unzip each into its own folder and open one folder at a time in VS Code or Cursor.
3. Paste the same prompt into the coding agent for each:

   ```
   Create a main-do file that runs all other scripts
   ```

4. Compare the three outputs.

### Lumora skills demo (quick start)

1. Open [advanced-research-roles-skills](https://github.com/dime-worldbank/coding-agent-exercise/tree/main/advanced-research-roles-skills) and follow its README.
2. Run a task with no project skills, then with the role-specific skills from `skills/`.
3. Score the before/after results with the exercise checklist.

Lumora data are **synthetic** — for training only, not program impact estimates.

## Before the session

### 1. Visual Studio Code (or Cursor)

Install **Visual Studio Code** from the Software Center, or use Cursor if that is your usual setup.

### 2. A coding agent in the editor

You need one of the following, signed in:

- **GitHub Copilot** (Claude model in Copilot Chat), or
- **Claude Code**

Quick test: open chat and confirm it responds. World Bank setup: [GitHub Copilot at the World Bank](https://github.com/worldbank/ospo/tree/main/docs/copilot) (WB GitHub membership required).

### 3. Exercise materials

Download the exercise ZIPs from [coding-agent-exercise](https://github.com/dime-worldbank/coding-agent-exercise) (see the READMEs linked above). Stata is optional if you only want to inspect agent output; use Stata 17+ if you want to run the Lumora pipeline.

## Setup checklist

- [ ] VS Code installed
- [ ] Copilot or Claude Code working in the editor
- [ ] Main do-file ZIPs downloaded (three separate folders)
- [ ] Lumora materials available if you will do the advanced exercise

## Questions

dimeanalytics@worldbank.org
