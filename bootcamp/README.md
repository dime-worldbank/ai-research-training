# AI-Enabled Research Bootcamp

Welcome to the **AI-Enabled Research Bootcamp**. This directory contains the training agenda, curriculum materials, and session documentation designed to equip researchers and staff at the World Bank Group with practical, agentic AI workflows.


## Template

To use the template for a new session, only copy the `bootcamp/sessions/template/presentation.qmd` file to the folder for that session. 

If you save it under the path `bootcamp/sessions/<day>/<session-topic>/<session-topic>.qmd`,  then all `../../..` relative paths within the presentation will continue to work correctly, and the template formatting will work out of the box.


## Directory Structure

The [`sessions/`](sessions) folder contains day-by-day guides, schedules, objectives, and training materials:

- **[Day 0: Setup for AI-enabled Research](sessions/day-0/README.md)**  
  *Prerequisites & Foundations*: Account setup, Git/GitHub fundamentals, IDE setup (VS Code), Python/R environment configuration, and setting up coding agents on WBG laptops.

- **[Day 1: Intro to Agentic AI at the WBG](sessions/day-1/README.md)**  
  *Core Concepts & Governance*: Introduction to AI agents, project onboarding with memory files, efficient prompting, reusable skills, safe AI usage, ethics, governance, and human-in-the-loop evaluation.

- **[Day 2: AI Tools For Data Acquisition and Analysis](sessions/day-2/README.md)**  
  *Data Pipeline Automation*: AI for quantitative survey design (Survey Solutions / SurveyCTO), transcription, data quality assurance, code improvement, and automated reproducible tables/charts.

- **[Day 3: AI Tools for Reproducible Research Products](sessions/day-3/README.md)**  
  *Research Publishing & Reproducibility*: Citation/reference tools, literature synthesis, dynamic presentations, working paper drafting, reproducibility package creation/verification, and AI adoption planning.

- **[Day 4: AI-enabled Workflows for Advanced Users](sessions/day-4/README.md)**  
  *Advanced & Scalable AI*: World Bank AI API integration in MEGA, AI-assisted web apps and dashboards, Model Context Protocols (MCPs), multi-agentic systems, geospatial analysis, and Git-based output verification.

## Render session PDFs

To render all session materials as PDFs, you can use the provided PowerShell script:

```powershell
.\render-pdfs.ps1
```