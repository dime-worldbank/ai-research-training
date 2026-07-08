# DECDI AI Roadmap — Training Materials

This repository hosts the materials for the **DECDI AI for Research** training series — a sequence of practical sessions on using AI tools across the research lifecycle.

📄 **Browse the sessions:** <https://worldbank.github.io/ai-roadmap-materials/>

Each session's slides, demo packages, and setup instructions are published here as the series runs.

## Structure

```
ai-roadmap-materials/
├── index.md          landing page for the site (session list)
├── _config.yml       GitHub Pages configuration
└── sessions/
    └── 01-reproducibility-packages/
        ├── README.md      session overview + setup prerequisites
        ├── slides/        the session deck
        └── materials/     demo package and other files
```

## Adding a session

1. Copy an existing session folder under `sessions/`, renamed with the next number (e.g. `02-automating-outputs`).
2. Replace its `README.md`, `slides/`, and `materials/` with the new session's content.
3. Add a row to the session table in `index.md` and flip its status to a link once materials are ready.

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
