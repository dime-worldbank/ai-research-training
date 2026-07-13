---
layout: default
title: "AI Skills in Action: From Messy Project to Reproducibility Package"
permalink: /sessions/ai-skills-reproducibility/
---

[← Back to the AI Roadmap series](../../)

# AI Skills to Facilitate Reproducible Research

Materials for the hands-on session on preparing reproducibility packages with an AI skill.

This is a **hands-on** session on using an AI skill to build, or audit, a reproducibility package, live, together, using an AI coding agent (Claude Code or GitHub Copilot) in VS Code. It works whether your code was **never written with reproducibility in mind** (a legacy or side project), or you already have a package and just want to **check it meets the standard** before submission.

**Objective:** produce a well-structured reproducibility package that runs on someone else computer and meets all requirements.

> **Short on time or can't install things?** You can just **watch** — the full demo runs live, and everything here stays available afterward so you can repeat it on your own machine. If you only do one setup step, do step 1-2.

## In this folder

- [`slides/`](./slides/) — **[view the slide deck](./slides/)**
- [`materials/demo-project.zip`](https://github.com/dime-worldbank/ai-research-training/raw/refs/heads/main/sessions/ai-skills-reproducibility/materials/demo-project.zip) — the (deliberately messy) project we will fix during the session
- this README — session overview and setup

## Before the session

Please set these up beforehand (about 10 minutes) if you want to follow along on your own machine.

### 1. Visual Studio Code

Install **Visual Studio Code**. You can do it yourself using the **Software Center**.

### 2. Access to Claude in VS Code

You need **one** of these, signed in inside VS Code:

- **GitHub Copilot** — your World Bank GitHub account connected to Copilot, signed in to the Copilot Chat extension; **or**
- **Claude account linked to VS Code** — the Claude Code extension, signed in with a personal or team Claude account.

Either one works. Quick test: open the chat panel in VS Code and confirm it responds.

> New to GitHub Copilot, or hitting setup issues? The World Bank OSPO's [Copilot getting-started, best-practices, and troubleshooting guides](https://github.com/worldbank/ospo) are a good first stop.

### 3. The skill

We download this together during the session, but feel free to grab it beforehand from the latest release:

<https://github.com/worldbank/wb-reproducible-research-repository/releases/latest>

Download the `.zip` — we place it into the demo project during the session.

### 4. The demo package

The project we will fix (also downloaded during the session). It's in this repo:

[`materials/demo-project.zip`](https://github.com/dime-worldbank/ai-research-training/raw/refs/heads/main/sessions/ai-skills-reproducibility/materials/demo-project.zip)

Unzip it somewhere easy to find (e.g. `/Users/name/Github`; `C:/wb6849591f/Github`;) and leave the files as they are — the mess is the point.

## Setup checklist

- [ ] VS Code installed
- [ ] Claude Code **or** GitHub Copilot working in VS Code (chat opens and responds)
- [ ] Skill downloaded *(optional — we do this together)*
- [ ] Demo package downloaded *(optional — we do this together)*

## Questions

reproducibility@worldbank.org
