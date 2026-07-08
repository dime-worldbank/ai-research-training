---
layout: default
title: "AI Skills in Action: From Messy Project to Reproducibility Package"
---

[← Back to the AI Roadmap series](../../)

# AI Skills to Facilitate Reproducible Research

Materials for the hands-on session on preparing reproducibility packages with an AI skill.

This is a **hands-on** session: we take a research project that was *not* built for reproducibility and turn it into a package that passes World Bank verification — live, together, using an AI coding agent (Claude Code or GitHub Copilot) in VS Code.

**Objective:** show how to produce a package that passes reproducibility verification *on the first submission*, starting from code that was never written with reproducibility in mind.

> **Short on time or can't install things?** You can just **watch** — the full demo runs live, and everything here stays available afterward so you can repeat it on your own machine. If you only do one setup step, do step 1-2.

## In this folder

- `materials/demo-package.zip` — the (deliberately messy) project we will fix during the session
- `slides/` — the session slides
- this README — session overview and setup

## Before the session

Please set these up beforehand (about 10 minutes) if you want to follow along on your own machine.

### 1. Visual Studio Code

Install **Visual Studio Code**. You can request it from the **Software Center**.

### 2. Access to Claude in VS Code

You need **one** of these, signed in inside VS Code:

- **GitHub Copilot** — your World Bank GitHub account connected to Copilot, signed in to the Copilot Chat extension; **or**
- **Claude account linked to VS Code** — the Claude Code extension, signed in with a personal or team Claude account.

Either one works. Quick test: open the chat panel in VS Code and confirm it responds.

### 3. The skill

We download this together during the session, but feel free to grab it beforehand from the latest release:

<https://github.com/worldbank/wb-reproducible-research-repository/releases/latest>

Download the `.zip` — we place it into the demo project during the session.

### 4. The demo package

The project we will fix — also downloaded during the session. It's in this repo:

[`materials/demo-package.zip`]([./materials/demo-package.zip](https://github.com/dime-worldbank/ai-research-training/raw/refs/heads/main/sessions/ai-skills-reproducibility/materials/demo-project.zip))

Unzip it somewhere easy to find (e.g. `/Users/name/Github`; `C:/wb6849591f/Github`;) and leave the files as they are — the mess is the point.

## Setup checklist

- [ ] VS Code installed
- [ ] Claude Code **or** GitHub Copilot working in VS Code (chat opens and responds)
- [ ] Skill downloaded *(optional — we do this together)*
- [ ] Demo package downloaded *(optional — we do this together)*

## Questions

reproducibility@worldbank.org
