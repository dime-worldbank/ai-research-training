# AI-Enabled Research Bootcamp

Welcome to the **AI-Enabled Research Bootcamp**. This directory contains the training agenda, curriculum materials, and session documentation designed to equip researchers and staff at the World Bank Group with practical, agentic AI workflows.


## Contributing

To add or update a session (slides, materials, or the agenda on the [bootcamp site](https://dime-worldbank.github.io/ai-research-training/bootcamp/)), see [CONTRIBUTING.md](CONTRIBUTING.md).

## Template

To use the template for a new session, only copy the `bootcamp/sessions/template/_presentation.qmd` file to the folder for that session. 

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

## Publish session presentations to Teams

The day-grouped publishing list in [`sessions/push-to-teams.yml`](sessions/push-to-teams.yml) is the complete allowlist. It contains `.qmd` paths relative to each day folder. Only presentations listed there are rendered and copied; adding a presentation without listing it in this file will not publish it to the teams folder automatically.

Each listed presentation must render as a standalone HTML file. Set `embed-resources: true` in its format configuration so the HTML can be used as a single file in Teams:

```yaml
format:
  bootcamp-revealjs:
    embed-resources: true
```

Install Quarto, then render the listed presentations and publish them to the configured Teams folder by running:

```powershell
.\render-and-push-html.ps1
```

The script publishes HTML only. It does not generate PDFs or require Chrome or Edge. It first renders each listed `.qmd` to its sibling `.html` and verifies the output.

A sibling `render-meta.yml` `name` property, when present, is used for both the Teams session folder and HTML filename. For example, `name: 1-my-topic` publishes to `<day>/1-my-topic/1-my-topic.html`. Without a `name` property, the `.qmd` basename is used for both.

To enable copying, sync the Bootcamp Teams folder to your computer and create the git-ignored `sharepoint-path.local.txt` file in this directory with the local destination path, for example:

```text
C:\Users\WB123456\WBG\AI-Enabled Research Bootcamp - WB Group - Announcements\Session Materials
```

The script asks for confirmation before copying. It copies only the allowlisted HTML files to `<Teams>/<day>/<name>/<name>.html`; it updates matching files and does not delete or alter other Teams content. Without the local path file, it renders the HTML and skips copying.