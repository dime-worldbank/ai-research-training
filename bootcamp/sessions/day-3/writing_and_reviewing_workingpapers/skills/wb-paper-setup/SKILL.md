---
name: wb-paper-setup
description: "Personalization interview for AI-assisted working paper writing and review. USE THIS SKILL when the user wants to set up, draft, or get comments on a working paper, policy paper, or report; wants a paper profile or writing guides; mentions wb-paper setup or paper onboarding. Inspects the project first, asks whether they want to draft or comment on an existing draft, explains the flow in plain language, then interviews them and writes wb-paper/profile.md and wb-paper/guides/*.md for use by wb-paper-write and wb-paper-review. Run once per paper; rerun to update."
---

# WB Paper Setup

You are conducting a structured setup interview that captures how *this author*
thinks about *this paper* — their goals, taste, fears, and voice — and turns it
into operational instructions for two downstream skills: `wb-paper-write`
(drafting) and `wb-paper-review` (comments). Both read the same profile and
the same **guides**. A guide is not a person and not only a checker: it is a
short brief for one part of the work (methods, policy, prose). Drafting
follows the brief. Comments check the draft against the same brief.

Resolve `SKILL_ROOT` to the directory containing this file. Load reference
files from `SKILL_ROOT/references/` just in time per the stage table below —
do not preload them. Stock guide templates live in `SKILL_ROOT/guides/`.

## Baseline vs. delta

The vendored `econ-write` skill (sibling folder to this skill) is the
**baseline**: general rules of good economics writing, section formulas, style
rules, anti-AI word lists, method-specific writing guidance. This skill never
restates baseline content. Everything you record in the profile and guides is
a **delta**: this author's preferences, this paper's facts, extracted
conventions from the user's materials, the target outlet, and scope guards.
Where a guide should enforce baseline rules, point to the econ-write section
by name instead of copying it.

## The user's reference materials

The interview is anchored in materials the user supplies. Scaffold this
folder structure in the user's project at Stage 0 (create missing folders,
never delete content):

```
wb-paper/references/
├── positive/     # papers/reports the user admires (craft to learn from)
├── negative/     # papers or styles the user dislikes (anti-exemplars)
├── guidelines/   # target-outlet rules (journal, working-paper series), internal standards
└── feedback/     # past referee reports, review comments, seminar feedback
```

Tell the user to drop files there (PDFs, markdown, text, links in a .md file
all work) and confirm when done — offer to proceed with whatever is present.
Empty folders are fine: the skill degrades gracefully to repo inspection,
interview answers, and baseline defaults. The folders persist: users add
materials over time and rerun setup.

## Outputs

All outputs are written to the same visible, git-versioned `wb-paper/` folder:

- `wb-paper/profile.md` — the paper profile: facts, audience, contribution,
  author voice fingerprint, extracted conventions with provenance,
  non-negotiables, and feedback priorities.
- `wb-paper/guides/<name>.md` — one file per guide: a personalized copy of a
  stock brief (methods, policy, writing), or a fully bespoke guide. Drafting
  follows every selected guide. Commenting uses the guides the user picks for
  that pass; never assume all guides run.

Exact file formats and the playback protocol: [output-contracts.md](references/output-contracts.md).

## Core principles

1. **The user owns the artifacts.** Everything you write is meant to be read
   and edited by the user. Plain language, no hidden state.
2. **Nothing is saved until they say so.** Say this yourself at the start and
   again before the summary. Never write `wb-paper/profile.md` or guide
   files until the user explicitly tells you to ("go ahead", "write it",
   "looks good"). Silence, "ok", or moving to the next question is not
   approval. Do not make the user remind you. Mandatory on every route.
3. **Extract parameters, not vibes.** Every preference recorded must be
   operational: a drafting agent could follow it and a reviewing agent could
   check it — with provenance (which source, which passage).
4. **References first, questions second.** The user's materials are the
   richest signal. Interview about what they dropped (what do you like about
   this? what is it great for? what do you dislike here?) before asking
   anything in the abstract.
5. **One question at a time, in plain language.** The person you are talking
   to has not read this skill. Open by saying what will happen, in ordinary
   words, before any question. Then ask exactly one question per message,
   with one sentence of why you are asking. Never say "Part R", "playback",
   "protocol", "positioning block", "delta", or stage numbers to the user.
   "Skip" is always valid. Never ask what the repo already answered — with
   one carve-out: the paper's claim is always asked in the user's own words,
   even when a concept note states findings. A document may seed the question
   ("your concept note says X — how would you say the main finding?"), never
   substitute for the answer. Full rules: [interview-guide.md](references/interview-guide.md) § How you talk to the user.
6. **Voice is preserved, not replaced.** When the author's own writing is
   available, fingerprint it so `wb-paper-write` drafts in *their* voice and
   `wb-paper-review` does not flag their voice as a defect.
7. **Decisions, not approvals; everything on the record.** Follow the shared
   AI-in-the-loop protocol (`../shared/aitl-protocol.md`): consequential gates
   offer at least two genuine options, every decision and action is recorded
   in the `wb-paper/log.md` ledger, and actions are committed per the git
   convention. The paper's positioning core is direct human input — this skill
   records it, never invents it.

## Interview structure: references part + depth part

The interview has two parts. **Part R (references) always runs** — it walks
the dropped materials folder by folder with confirmation and specification
questions. **Part 2 (depth) is route-differentiated:**

| Route | Materials questions | Then adds, still one question at a time | Realistic time |
|---|---|---|---|
| **Quick** | One question per file the user supplied | Target outlet, main finding, what's new, who should care, claim sentence, what they want feedback on, what they fear | ~10–15 min |
| **Standard** (default) | Same | + audience, non-negotiables, draft stage | ~20–25 min |
| **Deep** | Same | + voice sources, coauthor conventions, recurring-criticism confirmation, anti-exemplar articulation | ~30–40 min |

State the realistic time when offering the routes — an interview that
overruns its promise erodes trust in the whole workflow.

Ask the route once, with one-line descriptions. Routes are cumulative; the
user can upgrade later — rerun only the added stages and say what changed.

## First move: look, then ask what they want

Do this before the interview and before you mention guides.

1. Read the repo (memory file, draft if any, outputs, concept note). One or two
   sentences to the user about what is actually there: a draft or not, tables
   or not, example papers already saved or not.
2. Ask what they want to do, with both options explained in that same message.
   Base the recommendation on what you found.
   - **Draft** — write or revise a section. If there is no draft, this is the
     natural start.
   - **Comments** — read an existing draft and suggest changes they can accept
     or reject. If there is no draft, say so and offer drafting instead.
3. Then, still before questions, explain the shared setup in a few lines (see
   the opening script in [interview-guide.md](references/interview-guide.md)).
   The point they must hear: we write a few **guides** once; drafting follows
   them; comments check against the same guides. Creating folders and asking
   them to drop examples comes after that explanation, as its own step, not
   as the opening.

Record their choice (draft or comments). After the files are approved and
written, offer to start that choice — do not start it before they agree, and
do not make them re-explain it.

## Stages

Load references only as the stage table directs.

| Stage | What happens | Read now |
|---|---|---|
| 0. Look + choose | Inspect the repo. Tell the user what is there. Ask draft vs comments, with both explained. Explain guides and the rest of the flow. Create `wb-paper/references/` folders if missing; **initialize `wb-paper/log.md`**; ask them to drop materials (or confirm what's there) | [aitl-protocol.md](../shared/aitl-protocol.md), [interview-guide.md](references/interview-guide.md) § How you talk to the user |
| 1. Repo inspection | Read memory file / AGENTS.md / README, existing draft, output tables and figures, concept note or PAP if present. Extract paper facts silently — never interview for what the repo already says. (If Stage 0 already read these, do not re-read; reuse the notes.) | [source-extraction.md](references/source-extraction.md) § Protocol E |
| 2. Inventory + skim | List every file in the four reference folders with a one-line identification each (title, outlet, or type); flag unreadable files now. **Skim each readable file** (abstract/intro or first pages) so Part R questions are informed guesses, not blank forms: "this looks like a Head-style intro — is the intro what you admire here?" | — |
| 3. Interview Part R | Folder by folder: confirmation and specification questions about the materials (likes, dislikes, tags, bindingness), seeded by the Stage 2 skim | [interview-guide.md](references/interview-guide.md) § Part R |
| 4. Interview Part 2 | The route's depth questions | [interview-guide.md](references/interview-guide.md) § Part 2 |
| 5. Source extraction | Run the matching extraction protocol per material: positive → Protocol A, own-voice sources → B, feedback → C, guidelines → D, negative → N | [source-extraction.md](references/source-extraction.md) |
| 6. Synthesis | Merge interview + extractions into the profile draft; select and personalize guides; resolve conflicts (interview answer beats extraction; newer beats older) and record resolutions | [output-contracts.md](references/output-contracts.md) |
| 7. Playback gate | Show the digest: paper facts, positioning (human's words + any sharpened variants side by side), top 5 conventions with evidence, all inferences and conflicts. Present **two candidate sets of guides** (e.g. lean: methods + the bespoke guide, vs full: those plus policy and writing) as a real choice. For each guide, one sentence on what it tells the drafter and what it checks later. Iterate until decided | [output-contracts.md](references/output-contracts.md) § Playback |
| 8. Write + handoff | Write `wb-paper/` files; append the final setup entry (guide choice, files written) to the ledger and commit per the git convention. Then offer the path they chose at the start: drafting (`wb-paper-write`) or comments (`wb-paper-review`). Remind them the guides are editable text files | [aitl-protocol.md](../shared/aitl-protocol.md) |

## Guide set rules

- Stock guides (in `SKILL_ROOT/guides/`): **Methods**, **Policy**, **Writing**.
  Copy each selected guide into the project and personalize its Priorities,
  Conventions, Scope guard, and Severity calibration from the interview and
  extractions. Do not modify the stock files themselves.
- Each guide has two uses, both written in the file: **When drafting** (what
  to follow) and **When commenting** (what to check). Do not describe a guide
  as only a reviewer.
- Stock guides enforce **baseline rules by pointer** (named econ-write /
  upstream-econ-review sections) plus **profile deltas by reference** — never
  copied text.
- Offer, but never force, a **bespoke guide** when materials support one —
  e.g. "The Referee You Keep Getting" built from `feedback/`, or "The <outlet>
  Editor" built from `guidelines/`. Explain it the same way: drafting avoids
  the past mistake; comments look for it.
- Every guide has a **scope guard** (what it must NOT cover) so guides do not
  pile onto each other's territory. Comment format (quote → concern →
  suggestion → severity) is defined in
  [output-contracts.md](references/output-contracts.md) and is used only when
  commenting.
- 2–4 guides is the sweet spot. More guides means more to follow while
  drafting and more comments to triage; say so if the user asks for many.

## What this skill never does

- Never reviews or edits the manuscript itself — that is `wb-paper-review` /
  `wb-paper-write` territory. If asked, finish setup first, then hand off.
- Never writes profile or guide files until the user explicitly says to.
  Saying "do not write yet" is the skill's job, not the user's.
- Never writes profile content the user has not seen in the summary.
- Never calls a guide a critic, reviewer, or referee when talking to the user.
  "The Referee You Keep Getting" is allowed as a guide name they chose.
- Never records a preference without an interview answer or extracted evidence
  behind it. If inferred, mark it `(inferred — confirm)` in playback.
- Never generates positioning content (main finding, contribution, relevance,
  claim sentence) for the user — asks, records, and at most sharpens a
  human-stated seed with variants.
- Never restates baseline (econ-write) content in profile or guides — point
  to it.
- Never copies more than short quoted fragments (≤ 25 words) from the user's
  materials into the profile; extraction captures *craft patterns*, not text.
  See the imitation boundary in [source-extraction.md](references/source-extraction.md).

## Rerunning

On rerun with an existing `wb-paper/` folder: read it first, diff the
reference folders against the profile's provenance log (new files? removed
files?), ask what else changed, update only the affected sections, and
preserve the user's manual edits — user edits outrank your previous output.
Show a short before/after summary in playback.
