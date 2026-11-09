# DECDI AI Roadmap — Training Materials

This repository hosts the materials for the **DECDI AI for Research** training series — a sequence of practical sessions on using AI tools across the research lifecycle.

📄 **Browse the sessions:** <https://dime-worldbank.github.io/ai-research-training/>

Each session's slides, demo packages, and setup instructions are published here as the series runs.

## Structure

```
ai-research-training/
├── index.md             site landing page
├── roadmap.md           AI for Research series: session list
├── _config.yml          GitHub Pages configuration
├── _data/bootcamp.yml   bootcamp agenda: sessions, slide links, materials
├── _includes/ _layouts/ assets/   site templates and styles
├── sessions/            AI for Research series, one folder per session
│   └── ai-skills-reproducibility/
│       ├── README.md        session overview and setup
│       ├── slides/          the session deck (index.html is published)
│       └── materials/       demo package and other files
└── bootcamp/            AI-Enabled Research Bootcamp
    └── sessions/<day>/<topic>/   one folder per bootcamp session
```

The site is built by GitHub Pages from `main`. It serves the files committed to the repo; decks are rendered locally to `index.html` and committed.

## Adding a session

- **Bootcamp sessions:** see [`bootcamp/CONTRIBUTING.md`](bootcamp/CONTRIBUTING.md).
- **AI for Research series:** add a folder under `sessions/` with a `README.md`, `slides/` (deck rendered to `slides/index.html`) and `materials/`, then add a row to the session table in `roadmap.md`.

## Sessions

**Onboarding series (delivered):** Introduction to AI Coding Agents (May 18), Memory Files (Jun 22), Skills (Jul 2).

**AI bootcamp**

**AI for Research series:**

| # | Session | Date |
|---|---------|------|
| 1 | AI Skills to Facilitate Reproducible Research | Jul 16 |
| 2 | Using AI to Automate Research Outputs | Jul 30 |
| 3 | AI Ethics, Governance, and Safe Use at the World Bank | Sep 17 |
| 4 | Claude Enterprise at the World Bank | Oct 22 |
| 5 | Using AI Agents Cost Effectively: Best Practices and Case Studies | Nov 5 |
| 6 | AI Skills for Code Review | Nov 9 |
| 7 | AI Skills for Reproducible Research | Dec 2 |
| 8 | Making Your Workflows AI-Enabled | Dec 3 |

Questions: reproducibility@worldbank.org
