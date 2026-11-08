---
layout: default
title: "AI Skills for Code Review"
permalink: /sessions/ai-skills-review-code/
---

[← Back to the AI Roadmap series](../../)

# AI Skills for Code Review

Materials for the hands-on session on reviewing and improving research code with an AI skill.

This is a **hands-on** session. We use an AI skill to review research code for correctness, reproducibility, and privacy risks with an AI coding agent (Claude Code or GitHub Copilot) in VS Code. Then the agent fixes only the issues you approve. You can review **your own code** (a script you wrote recently, or a whole project), or use the demo project.

**Objective:** review one code file or package with the skill, triage the findings, and let the agent implement a few approved fixes that you check in the diff.

> **Short on time or can't install things?** You can just **watch**. The full demo runs live, and everything here stays available afterward so you can repeat it on your own machine. If you only do one setup step, do steps 1 and 2.

## In this folder

- [`slides/`](./slides/): **[view the slide deck](https://dime-worldbank.github.io/ai-research-training/sessions/ai-skills-review-code/slides/)**
- [`materials/water-pilot.zip`](https://github.com/dime-worldbank/ai-research-training/raw/refs/heads/main/sessions/ai-skills-review-code/materials/water-pilot.zip): the demo project, a synthetic impact evaluation with realistic mistakes in the code ([details and prompts](./materials/README.md))
- this README: session overview and setup

## Before the session

Please set these up beforehand (about 10 minutes) if you want to follow along on your own machine.

### 1. Visual Studio Code

Install **Visual Studio Code**. You can do it yourself using the **Software Center**.

### 2. Access to an AI assistant in VS Code

You need **one** of these, signed in inside VS Code:

- **GitHub Copilot**: your World Bank GitHub account connected to Copilot, signed in to the Copilot Chat extension; **or**
- **Claude account linked to VS Code**: the Claude Code extension, signed in with a personal or team Claude account.

Either one works. Quick test: open the chat panel in VS Code and confirm it responds.

> New to VS Code, or hitting setup issues? Follow the [coding agent setup slides](https://dime-worldbank.github.io/ai-research-training/bootcamp/sessions/day-0/setup-coding-agent/) from the AI bootcamp.

>  New to GitHub Copilot?Follow the [coding agent setup slides](https://dime-worldbank.github.io/ai-research-training/bootcamp/sessions/day-0/setup-coding-agent/) from the AI bootcamp. The World Bank OSPO's [Copilot getting-started, best-practices, and troubleshooting guides](https://github.com/worldbank/ospo) (Internal only) are a good first stop.

### 3. The skill

We download this together during the session, but feel free to download it beforehand:

[research-code-review.zip](https://github.com/dime-worldbank/coding-agents-hub/releases/download/research-code-review-latest/research-code-review.zip)

Unzip it. We will place the `research-code-review` folder inside your project's `.agents/skills/` folder during the session.

### 4. Your code, or the demo project

We encourage you to bring **your own code**. Before the session, move any non-public data out of the project folder.

If you don't have code with you, use the demo project (also downloaded during the session):

[water-pilot.zip](https://github.com/dime-worldbank/ai-research-training/raw/refs/heads/main/sessions/ai-skills-review-code/materials/water-pilot.zip)



## Setup checklist

- [ ] VS Code installed
- [ ] Claude Code **or** GitHub Copilot working in VS Code (chat opens and responds)
- [ ] Skill downloaded *(optional, we do this together)*
- [ ] Your own code ready, or the demo project downloaded *(optional, we do this together)*

## Questions

dimeanalytics@worldbank.org
