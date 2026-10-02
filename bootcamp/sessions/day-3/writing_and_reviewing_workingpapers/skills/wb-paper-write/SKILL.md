---
name: wb-paper-write
description: "Personalized, grounded drafting and revision for a working paper. USE THIS SKILL when the user asks to outline, draft, write, rewrite, revise, tighten, or implement review comments on their paper or a section of it; mentions wb-paper write, drafting a section, or working the review queue. Follows the econ-write baseline plus the user's wb-paper/profile.md; drafts through an outline→bullets→prose floor with human choices at each step; takes numbers only from project outputs; never invents the paper's positioning core. Requires wb-paper/profile.md (else runs wb-paper-setup first)."
---

# WB Paper Write

You run the drafting half of the AI-in-the-loop writing workflow. The
`econ-write` baseline says what good economics writing is; the profile says
what *this author* wants; the project's outputs say what is true. You draft
and revise inside those three constraints, with the human choosing at every
consequential step — the goal is a paper the author owns intellectually and
can prove they own.

Resolve `SKILL_ROOT` to the directory containing this file. Sibling folders:
`../econ-write/` (baseline — apply its rules by default), `../shared/
aitl-protocol.md` (ledger, git, decision rule, critical-input rule — binding),
`../wb-paper-setup/references/output-contracts.md` (profile format).

## Preflight (every run)

1. **Profile check.** No `wb-paper/profile.md` → offer to run `wb-paper-setup`
   (drafting without a profile falls back to econ-write baseline + interview
   of the essentials; say so and record it).
2. **Reconcile** section statuses per the shared protocol.
3. **Guides.** Read `wb-paper/guides/` and follow each guide's **When
   drafting** section. If the user has not heard what a guide is, one
   sentence: these are the briefs from setup; drafting follows them, comments
   check against them. Do not call them critics.
4. **Positioning check.** Read the profile's Positioning section. Unsettled
   elements block any section that needs them (abstract, intro, conclusion
   need all four; results needs the main finding): before drafting such a
   section, ask the human to state the missing element — an ugly version is
   fine — then offer 2 sharpened variants. Never proceed on an invented
   placeholder for positioning (ordinary factual gaps still use
   `[AUTHOR: ...]`).
5. **Git cleanliness** per the shared protocol before any file-touching mode.

## Mode menu (a decision)

- **Outline** — propose paper skeleton + writing order.
- **Draft** — write a section through the drafting floor.
- **Revise** — implement accepted comments from `wb-paper/review/work-queue.md`.
- **Rewrite** — improve existing human text without changing meaning.

Suggest a mode from state (empty draft → outline; non-empty queue → revise),
but the user chooses. Record the choice.

## Outline mode

1. Build **two genuinely different outline variants** from the paper type's
   structure (econ-write § Paper Structure Overview) + profile deltas
   (`overrides baseline` conventions, sections the target outlet requires) — e.g. variant
   A: standard applied-paper structure; variant B: the structure the user's
   `structure`-tagged exemplar uses. Annotate each section with its job and
   the positioning element it must carry.
2. Propose a **writing order** with baseline rationale (econ-write: intro
   first and rewritten often, abstract last, results before conclusion),
   adjusted to what already exists.
3. The user picks, merges, or rewrites; iterate until decided. Save
   `wb-paper/outline.md` per the format in the output contracts
   (`../wb-paper-setup/references/output-contracts.md`); ledger + commit.
4. If the profile's Grounding pointers have no draft path yet, decide one now
   (offer the project's convention if visible, else `paper/draft.qmd` for
   Quarto projects / `paper/draft.tex` for LaTeX) and record it in the
   profile's Grounding pointers — a one-line edit, noted in the ledger.

## Draft mode (per section — the drafting floor)

Full protocol: [drafting-protocol.md](references/drafting-protocol.md). Shape:

1. **Section choice** (from outline; flag dependencies — "abstract last" if
   intro/results aren't drafted).
2. **Clarifications before drafting** — up to 5 targeted questions whose
   answers only the author has (which result leads, which exhibits belong,
   what the section must NOT say). Never draft first and ask later.
3. **The floor: outline → bullets → prose.** Each escalation is shown and the
   human chooses: edit / approve / redirect. Skipping straight to prose is
   allowed but is itself an explicit choice, recorded.
4. **At prose**, offer **two variants of the key passages** (opening
   paragraph, transition carrying the main claim); the human picks or blends.
5. **Grounding**: numbers only from the profile's Grounding pointers, cited to
   file in a draft comment; everything else `[AUTHOR: ...]`. Positioning
   sentences inserted from the profile (human-authored text), fitted
   grammatically, never re-invented.
6. **Voice**: draft to the voice fingerprint; baseline style rules apply where
   the fingerprint is silent; profile `overrides baseline` win.
7. Ledger + commit; section status `ai-draft`, `human-touched: no`. Remind the
   user: this text is a proposal until they've edited it, and
   `wb-paper-review` will warn on unedited AI text.

## Revise mode (working the queue)

Read `wb-paper/review/work-queue.md`. Per item, in the user's priority order:

1. Show the full comment (from its round file) + your proposed **smallest
   adequate change** — as a concrete before/after. Where two repairs are
   plausible (narrow the claim vs. add analysis), present both as options.
2. The user decides: apply / apply-with-edits / skip / send back to triage.
3. Apply, show the diff, get acceptance. One queue item = one commit
   (`AI-Action: revise C-<NN>`). Update the comment status to `implemented`
   (+ commit hash) and tick the queue item.
4. Batch application is allowed for P2 mechanical items if the user asks —
   one batch = one decision = one commit, diff still shown.

Never implement a comment that is not in the queue (i.e. not user-accepted).

## Rewrite mode

econ-write's rewriting rules (fix passive voice, throat-clearing, buried
leads, vague language) applied to existing text, with: meaning and claims
preserved exactly (no new numbers, no strengthened conclusions); voice
fingerprint and non-negotiables untouched; before/after shown per passage with
what-changed-and-why; the human accepts per passage or per batch. Rewritten
human text keeps `human-touched: yes` — but the ledger records the rewrite as
an AI action on that section.

## Hard rules

- Never invent positioning content, numbers, citations, or results. Uncited
  facts become `[AUTHOR: ...]`; missing positioning triggers a question.
- Never touch non-negotiable passages; never mix AI and human edits in one
  commit; never edit outside the chosen scope.
- Every action → ledger entry + commit per the shared protocol; disclosure
  ledger must remain able to say exactly which text AI produced.
- Drafts are proposals: no AI-drafted section is "done" until the human has
  edited it, and this skill says so rather than implying completion.
