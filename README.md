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

**AI for Research series:**

| # | Session | Date |
|---|---------|------|
| 1 | AI Skills to Facilitate Reproducible Research | Jul 16 |
| 2 | Using AI to Automate Research Outputs | Jul 30 |
| 3 | Using AI to Review Code and Verify Research Reproducibility | Sep 8 |
| 4 | AI Ethics, Governance, and Safe Use at the World Bank | Sep 17 |
| 5 | Using AI for Feedback on Your Research | Oct 1 |
| 6 | Using the World Bank AI API in MEGA | Oct 15 |
| 7 | AI for Survey Instrument Design | Oct 29 |
| 8 | AI for Transcribing Data | Nov 12 |
| 9 | AI for Data Quality Checks | Nov 19 |
| 10 | Creating Custom Coding Agents | Dec 3 |

Questions: reproducibility@worldbank.org
