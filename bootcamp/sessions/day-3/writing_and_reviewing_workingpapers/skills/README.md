# WB Working Paper Skills

Skills for the AI-enabled Research Bootcamp (Day 3, *Hands-on: Use AI to draft
and get feedback on Working Papers*). Together they implement an
**AI-in-the-loop writing workflow**: the human designs the guides, drafting
follows them, comments check against the ones they pick, and they triage
every comment and every edit.

## Layering: upstream baseline + WB layer

We vendor the best available upstream skills verbatim and only modify and
build on top. Upstream files are never edited in place.

| Layer | Folder | Role | Status |
| --- | --- | --- | --- |
| Baseline | [`econ-write/`](econ-write/) | Full upstream economics writing skill (verbatim): section formulas, style rules, anti-AI word/pattern lists, identification-strategy writing guidance, LaTeX tips, review checklist, specialized tasks | Vendored (MIT) |
| Baseline | [`upstream-econ-review/`](upstream-econ-review/) | Curated review protocols from econ-paper-review-skill: DiD/IV/RDD gates, design/inference/exhibit/claim audits, comment style | Vendored (PolyForm NC) |
| WB layer | [`wb-paper-setup/`](wb-paper-setup/) | Looks at the project, asks draft vs comments, then interviews. Produces `wb-paper/profile.md` and `wb-paper/guides/*.md`. A guide is a brief used both to draft and to comment | Draft |
| WB layer | [`wb-paper-review/`](wb-paper-review/) | Guide × domain × section comments using the upstream audit protocols; triage with accept/reject/challenge/defer; never edits the manuscript | Draft |
| WB layer | [`wb-paper-write/`](wb-paper-write/) | Outline-first grounded drafting (outline → bullets → prose floor), revision from the review work queue, rewriting; numbers only from project outputs, `[AUTHOR: ...]` otherwise | Draft |
| Shared | [`shared/aitl-protocol.md`](shared/aitl-protocol.md) | The AI-in-the-loop contract binding all three skills: decision rule (≥2 options at every gate), the `wb-paper/log.md` ledger, one-AI-action-one-commit git convention, human-touched tracking, positioning-is-human-input rule, disclosure generation | Draft |

Division of labor: **econ-write owns the general rules** (what good economics
writing is); **the WB layer owns personalization and grounding** (what *this
author* wants, what *this paper's* artifacts say, the target outlet). The
profile and guides reference econ-write sections rather than restating them;
they record only deltas: personal preferences, extracted conventions, WB
conventions, and scope guards.

## The pipeline

```
user drops materials into  wb-paper/references/{positive,negative,guidelines,feedback}
      │
wb-paper-setup  (interview always starts from those materials)
      │
      ▼
wb-paper/profile.md  +  wb-paper/guides/<name>.md     (user-owned, git-versioned)
      │                          │
      ▼                          ▼
wb-paper-write              wb-paper-review
(econ-write baseline        (upstream audit protocols
 + profile deltas)           + the guides the user picks for that pass)
```

## Human gates (non-negotiable design principle)

1. Setup plays back its understanding and drafted files before writing anything.
2. The user edits their guides before those guides are used to draft or comment.
3. When commenting, guides only comment — they never edit the manuscript.
4. The user triages every comment (accept / reject / **challenge** / defer)
   before any revision is implemented; challenged comments must be withdrawn,
   sharpened, or upheld with reasons.
5. Revisions are reviewed as git diffs; one AI action = one commit, never
   mixed with human edits.
6. The paper's positioning core (main finding, contribution + type, relevance,
   claim sentence) is direct human input — AI sharpens human seeds, never
   invents.
7. Every AI action and human decision lands in the `wb-paper/log.md` ledger;
   the submission-time AI-use disclosure is generated from it.

## Attribution

`econ-write/` is [econ-writing-skill](https://github.com/hanlulong/econ-writing-skill)
by Lu Han (MIT), vendored verbatim. `upstream-econ-review/` contains verbatim
extracts from [econ-paper-review-skill](https://github.com/hanlulong/econ-paper-review-skill)
by the same author (PolyForm Noncommercial 1.0.0 — educational/public-research
use permitted); see its README for what was and wasn't vendored. For full
referee-grade reviews beyond the bootcamp workflow, install the upstream
econ-review skill directly.
