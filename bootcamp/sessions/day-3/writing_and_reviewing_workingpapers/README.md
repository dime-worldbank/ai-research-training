# AI to write and review papers

Skills and demo projects for the Day 3 session on drafting and commenting on working papers.

## The workflow

The agent looks at the project, then asks whether you want to **draft** or get **comments** on a draft. Either way starts with a short setup. You answer one question at a time: example papers, rules for the target outlet (a journal, a working-paper series), what the paper claims, what you fear a smart reader will say.

Setup writes two things you can edit:

- `wb-paper/profile.md` — the paper's claim, audience, and conventions, in your words.
- `wb-paper/guides/` — short briefs (methods, policy, writing). **Drafting follows a guide. Comments check the draft against the same guide.**

You choose at every step. Nothing is saved until you say so. Comments are accepted, rejected, or challenged before any edit. Each AI action is a git commit and a line in `wb-paper/log.md`, which is what a disclosure statement is generated from.

## Skills

In [`skills/`](skills/). Each paper folder links `skills/` there, so your agent sees them when that folder is the project.

| Skill | Role |
|---|---|
| `wb-paper-setup` | Interview. Writes the profile and guides. |
| `wb-paper-write` | Drafts from the guides and the project's output tables. |
| `wb-paper-review` | Comments using the guides you pick. Does not edit the paper. |

`econ-write` and `upstream-econ-review` are vendored baselines (MIT and PolyForm Noncommercial). The WB skills only add personalization and the human gates.

## Demo projects

Same fictional Zambia school-meals study in both.

| Folder | Use it to |
|---|---|
| [`zambia-attendance-no-draft/`](zambia-attendance-no-draft/) | Run setup, then draft a results section from the tables. No paper yet. |
| [`zambia-attendance-with-draft/`](zambia-attendance-with-draft/) | Comment on a draft that already has mistakes. Instructor key: `INSTRUCTOR-seeded-defects.md` (do not open it first). |

```bash
cd zambia-attendance-no-draft   # or zambia-attendance-with-draft
git init && git add -A && git commit -m "baseline"
```

Open your agent in that folder. First message: `Follow skills/wb-paper-setup/SKILL.md on the Quick route for this project. I am the author. Interview me.`
