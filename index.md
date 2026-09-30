---
layout: default
title: "DECDI AI Roadmap — Training Materials"
---


This site hosts materials for the **DECDI AI for Research** training series: practical sessions on using AI tools across the research lifecycle — from coding agents and reusable skills through reproducibility, output generation, and responsible use.

Materials for each session — slides, demo packages, setup instructions — are published here as the series runs.

<div class="card-container">

<a href="#roadmap">
  <div class="card">
    <span class="pill pill-available">Series &middot; May&ndash;Dec 2026</span>
    <h3>Roadmap</h3>
    <p>Ten stand-alone sessions on AI for research. Follow along one session at a time.</p>
  </div>
</a>

<a href="#bootcamp">
  <div class="card" style="border-top-color: #800280;">
    <span class="pill pill-available" style="background: #800280;">Oct 1 &amp; Oct 5&ndash;8</span>
    <h3>AI-Enabled Research Bootcamp</h3>
    <p>Hands-on program across the full research lifecycle, with the day-by-day agenda and slides.</p>
  </div>
</a>

</div>

<div class="note" markdown="1">
**New to the series?** Start with a session that's live below. Each session folder is self-contained: overview, setup steps, slides, and any demo files.
</div>

---

## Roadmap

**Onboarding series (delivered)**

| Session | Date | Status |
|---------|------|--------|
| Intuitive Introduction to AI Coding Agents | May 18 | Delivered |
| AI Onboarding Part 1: Memory Files | Jun 22 | Delivered |
| AI Onboarding Part 2: Skills | Jul 2 | Delivered |

**AI for Research series**

| # | Session | Date | Status |
|---|---------|------|--------|
| 1 | [AI Skills to Facilitate Reproducible Research](./sessions/ai-skills-reproducibility/) | Jul 16 | **Available** &middot; [Slides →](./sessions/ai-skills-reproducibility/slides/) |
| 2 | [Using AI to Automate Research Outputs](./sessions/ai-skills-slides/) | Jul 30 | **Available** &middot; [Slides →](./sessions/ai-skills-slides/slides/) |
| 3 | Using AI to Review Code and Verify Research Reproducibility | Sep 8 | Upcoming |
| 4 | [AI Ethics, Governance, and Safe Use at the World Bank](./sessions/ai-ethics-governance/) | Sep 17 | **Available** &middot; [Slides →](./sessions/ai-ethics-governance/) |
| 5 | Using AI for Feedback on Your Research | Oct 1 | Upcoming |
| 6 | Using the World Bank AI API in MEGA | Oct 15 | Upcoming |
| 7 | AI for Survey Instrument Design | Oct 29 | Upcoming |
| 8 | AI for Transcribing Data | Nov 12 | Upcoming |
| 9 | AI for Data Quality Checks | Nov 19 | Upcoming |
| 10 | Creating Custom Coding Agents | Dec 3 | Upcoming |

*The onboarding series introduced AI coding agents, memory files, and skills. Materials for those sessions are held by Impact Analytics; contact the team if you need them.*

---

<div class="bootcamp" markdown="1">

## 🏕️ Bootcamp

<div class="bootcamp-hero">
  <img src="{{ '/assets/images/bootcamp-logo.png' | relative_url }}" alt="Bootcamp: AI-Enabled Research">
  <p class="bootcamp-dates">Oct 1 &amp; Oct 5–8, 2026</p>
  <p><a class="bootcamp-button" href="https://www.canva.com/design/DAHT37UVp3k/z8gvUN_hMD0hSYwGE1qYGw/edit">📋 Live agenda (Canva)</a></p>
</div>

Over four core days, participants move through the full research lifecycle: building confidence with agentic AI and directing it responsibly; transforming how they collect, clean, and analyze data; producing polished, reproducible, publication-ready outputs; and, for those ready to go further, designing advanced workflows that scale across teams. Every session is grounded in tools already available at the WBG, and more than half are hands-on.

**No prior AI experience is required.** Participants leave with reusable workflows, memory files, and AI skills configured for their own research.

| Day | Date | Track | Theme |
|-----|------|-------|-------|
| [Day 0](#day-0--setup-for-ai-enabled-research) | Oct 1 | Optional prerequisite | Setup for AI-enabled research |
| [Day 1](#day-1--intro-to-agentic-ai-at-the-wbg) | Oct 5 | Core | Intro to agentic AI at the WBG |
| [Day 2](#day-2--ai-tools-for-data-acquisition-and-analysis) | Oct 6 | Core | AI tools for data acquisition and analysis |
| [Day 3](#day-3--ai-tools-for-reproducible-research-products) | Oct 7 | Core | AI tools for reproducible research products |
| [Day 4](#day-4--ai-enabled-workflows-for-advanced-users) | Oct 8 | Optional, advanced | AI-enabled workflows for advanced users |

Hands-on sessions are marked 🛠️. Session links appear as materials are published.

### Day 0 · Setup for AI-enabled research

*Oct 1 · Prerequisite for Days 1–3; optional if you already use these tools.*

**You will leave with:** a GitHub repository for a current project with at least one commit, and VS Code set up and used for at least one interaction with GitHub Copilot or Claude Code.

| Time | Session | Lead | Materials |
|------|---------|------|-----------|
| 9:30 – 10:00 | 🛠️ Set up GitHub account and install GitHub Desktop | Impact Analytics | [Slides](./bootcamp/sessions/day-0/setup-github/) |
| 10:00 – 11:30 | Intuitive Introduction to Git/GitHub | Impact Analytics | [Materials](https://github.com/worldbank/dime-github-trainings/tree/main/GitHub-trainings/Intro-Git-GitHub-Contributor) |
| 11:30 – 12:30 | 🛠️ Migrating an existing project to GitHub (hands-on during lunch) | Impact Analytics | [Slides](./bootcamp/sessions/day-0/migrate-to-github/) |
| 12:30 – 1:45 | Lunch | | |
| 1:45 – 2:15 | Intro to Integrated Development Environments (VS Code) | Impact Analytics | [Slides](./bootcamp/sessions/day-0/intro-ide-vscode/) |
| 2:15 – 2:45 | 🛠️ Set up VS Code and open your project folder | Impact Analytics | [Slides](./bootcamp/sessions/day-0/setup-vscode/) |
| 2:45 – 3:15 | 🛠️ Set up command line software for agentic workflows | Impact Analytics | [Slides](./bootcamp/sessions/day-0/setup-python-r/) |
| 3:15 – 4:00 | 🛠️ Set up a coding agent on your computer | Impact Analytics | [Slides](./bootcamp/sessions/day-0/setup-coding-agent/) |

### Day 1 · Intro to agentic AI at the WBG

*Oct 5 · Core*

**You will leave with:** an AI readme (memory file) for at least one project, and one skill installed and used on one project.

| Time | Session | Lead | Materials |
|------|---------|------|-----------|
| 9:00 – 9:10 | Welcome | | |
| 9:10 – 9:45 | Introduction to AI Agents | Impact Analytics | [Slides](./bootcamp/sessions/day-1/intro-ai-agents/) |
| 9:45 – 10:15 | Onboarding AI Agents: Memory Files | Impact Analytics | [Slides](./bootcamp/sessions/day-1/onboarding-ai-agents/) |
| 10:15 – 10:30 | Break | | |
| 10:30 – 11:00 | Using AI agents efficiently and cost-effectively | Impact Analytics | [Slides](./bootcamp/sessions/day-1/cost-effective-ai/) |
| 11:00 – 11:30 | Intro to the World Bank's GitHub and Open Source Catalog | Open Source Program Office | Coming soon |
| 11:30 – 12:20 | AI Tools Bazaar (impactAI, AVA, ScoreSight, Knowledger, Translate) | Tool teams | Coming soon |
| 12:20 – 1:20 | Lunch | | |
| 1:20 – 2:15 | AI at the WBG: Current Landscape and Future Ambitions | ITSAE AI Literacy Team | Coming soon |
| 2:15 – 3:00 | Making AI agents work for you: good prompts and reusable skills | Impact Analytics | [Slides](./bootcamp/sessions/day-1/ai-agents-for-you/) |
| 3:00 – 3:15 | Break | | |
| 3:15 – 4:00 | 🛠️ Create a memory file for your project and install a skill | Impact Analytics | [Slides](./bootcamp/sessions/day-1/create-a-memory-file/) |
| 4:00 – 5:00 | AI ethics, governance, and safe use | Impact Analytics | [Slides](./bootcamp/sessions/day-1/ai-ethics/) |

### Day 2 · AI tools for data acquisition and analysis

*Oct 6 · Core*

**You will leave with:** an AI-programmed survey instrument, reusable AI workflows for data quality checks, one code file reviewed and improved with AI skills, and at least one table or chart created from your own data.

| Time | Session | Lead | Materials |
|------|---------|------|-----------|
| 9:00 – 9:10 | Welcome | | |
| 9:10 – 9:45 | AI for Quantitative Surveys | DECSU, Impact Analytics | Coming soon |
| 9:45 – 10:30 | Using AI for Transcription & Data Quality Assurance | DECSU | Coming soon |
| 10:30 – 10:45 | Break | | |
| 10:45 – 12:45 | 🛠️ Using AI agents in Survey Solutions \| SurveyCTO (parallel sessions) | DECSU \| Dobility | Coming soon |
| 12:45 – 1:45 | Lunch | | |
| 1:45 – 2:00 | AI skills to review and improve data processing, cleaning, and analysis | Impact Analytics | Coming soon |
| 2:00 – 2:45 | 🛠️ Using AI skills to improve code | Impact Analytics | Coming soon |
| 2:45 – 3:00 | Break | | |
| 3:00 – 3:30 | AI skills to create reproducible, publication-ready charts and tables | Impact Analytics | Coming soon |
| 3:30 – 4:15 | 🛠️ AI skills for automating tables and charts | Impact Analytics | Coming soon |
| 4:15 – 5:00 | Human-in-the-loop: evaluating AI outputs | Impact Analytics | [Slides](./bootcamp/sessions/day-2/human-in-the-loop/) |

### Day 3 · AI tools for reproducible research products

*Oct 7 · Core*

**You will leave with:** a presentation or policy brief for your project, a created and verified reproducibility package, and an AI adoption plan with 6-week and 3-month targets.

| Time | Session | Lead | Materials |
|------|---------|------|-----------|
| 9:00 – 9:10 | Welcome | | |
| 9:10 – 10:00 | AI tools for evidence aggregation and literature review | Impact Analytics | Coming soon |
| 10:00 – 10:15 | Break | | |
| 10:15 – 11:30 | 🛠️ AI skills for presentations: create a dynamic presentation | Impact Analytics | [Slides](./bootcamp/sessions/day-3/ai-skills-slides/slides/) |
| 11:30 – 12:15 | 🛠️ Use AI to draft and get feedback on working papers | Impact Analytics | [Slides](./bootcamp/sessions/day-3/writing_and_reviewing_workingpapers/) |
| 12:15 – 1:15 | Lunch | | |
| 1:15 – 3:00 | 🛠️ Reproducible research standards and AI reproducibility packages | Impact Analytics | [Slides](./bootcamp/sessions/day-3/reproducibility-skill/) |
| 3:00 – 3:15 | Break | | |
| 3:15 – 4:00 | 🛠️ Create an AI adoption plan for your project | Impact Analytics | [Slides](./bootcamp/sessions/day-3/ai-adoption-plan/) |
| 4:00 – 5:00 | AI tools for data documentation and publication | Data Group | Coming soon |

### Day 4 · AI-enabled workflows for advanced users

*Oct 8 · Optional, a deeper dive for staff with experience using AI workflows*

**You will leave with:** a MEGA workspace that queries the World Bank AI API, AI outputs for your projects reviewed and verified through your own GitHub repos, and one multi-agentic workflow set up for your project.

| Time | Session | Lead | Materials |
|------|---------|------|-----------|
| 9:00 – 9:10 | Welcome | | |
| 9:10 – 10:45 | 🛠️ Using the World Bank AI API in MEGA | MEGA | Coming soon |
| 10:45 – 11:00 | Break | | |
| 11:00 – 12:15 | 🛠️ AI-assisted dashboards and web apps with Replit | ITS | Coming soon |
| 12:15 – 1:15 | Lunch | | |
| 1:15 – 1:45 | Trustworthy AI: intro to Model Context Protocols (MCPs) | Data Group | Coming soon |
| 1:45 – 2:30 | Why and how to use multi-agentic workflows | WBG Institute | Coming soon |
| 2:30 – 3:00 | Embeddings in geospatial analysis | GOST | Coming soon |
| 3:00 – 3:15 | Break | | |
| 3:15 – 4:15 | 🛠️ Git workflows for verifying AI outputs | Impact Analytics | [Slides](./bootcamp/sessions/day-4/git-verify-ai-output/) |
| 4:15 – 4:45 | Closing session and course evaluation | | |

</div>

---

## About this repository

Each roadmap session lives in its own folder under `sessions/`:

```
sessions/
└── ai-skills-reproducibility/
    ├── README.md      session overview + setup prerequisites
    ├── slides/        the session deck
    └── materials/     demo package and other files
```

To add a session, copy an existing folder, then add a row to the Roadmap table above. For a bootcamp session, replace "Coming soon" in the relevant day's table with a link to the session page.

Questions: **reproducibility@worldbank.org**
