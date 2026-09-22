# Drafting Protocol

The full draft-mode procedure: clarifications, the floor, variants, grounding,
and voice. The design intent behind every step: the author's thinking enters
the text *before* generation, not as a cleanup afterwards.

## 1. Clarifications before drafting

Ask up to 5 questions, one batch, targeted at what only the author knows.
Derive them from the section's job (per the outline annotation) and the gaps
you can see. Good clarifications by section type:

- **Results**: which result leads? Which exhibits belong to this section and
  in what order? Any result to downplay or flag as fragile? Preferred
  benchmark for magnitudes?
- **Data**: any cleaning decisions that materially matter? Known limitations
  to state upfront vs. in a footnote? Access story for restricted data?
- **Introduction**: which hook strategy (the positioning relevance sentence
  usually implies one — confirm)? Which 5–10 papers are the closest
  literature? What's the "however" that creates the niche?
- **Empirical strategy**: how does the author explain the identifying
  variation *in conversation*? (Their seminar-answer version is usually better
  than a formula-first writeup — capture it.)
- **Conclusion**: which implication is the author willing to stand behind?
  What future work do they actually intend?

Skippable ("draft with your best guesses") — but then every guessed choice in
the draft gets an inline `%% [GUESS: chose X, alternative was Y]` comment so
the author sees where their input was substituted. Do not ask what the
profile, outline, or repo already answers.

## 2. The floor: outline → bullets → prose

Three escalations, each shown, each a decision (edit / approve / redirect):

1. **Section outline** — the paragraph plan: one line per paragraph stating
   its job and what evidence/exhibit it uses. This is where structure gets
   decided; it is cheap to move paragraphs here and expensive later.
2. **Bullet argument** — each paragraph expanded to 2–4 bullets: the claim,
   the evidence with actual numbers (from outputs), the connective logic.
   This is where the *argument* gets decided. The author editing bullets is
   the highest-value human input in the whole flow — encourage it ("reorder,
   strike, or reword any bullet; I draft from exactly what survives").
3. **Prose** — bullets become paragraphs in the author's voice.

Skipping levels is allowed as an explicit recorded choice. For sections under
~2 paragraphs (roadmap, short data note), levels 1–2 may merge — say so.
Likewise, when the bullets would merely restate an already-detailed section
outline, propose merging levels 1–2 as an option rather than performing
ceremony — the floor exists to force real decisions, not rituals.

## 3. Variants at the key passages

At prose stage, produce **two variants** of the passages that carry the most
weight, labeled with what differs ("A opens on the puzzle; B opens on the
magnitude"): the section's opening paragraph; any passage carrying a
positioning element; the results section's first statement of the main
finding. One variant for everything else — routine connective prose does not
need ceremony. The human picks, blends, or rewrites; record the choice.

## 4. Grounding rules

- **Numbers**: only from files named in the profile's Grounding pointers.
  Each drafted number carries a source comment in the draft, using the
  manuscript format's comment syntax (`% from outputs/tab2_main.tex col 2` in
  LaTeX; `<!-- from outputs/tab2_main.tex col 2 -->` in Quarto/markdown),
  that stays until the human removes it. Derived numbers state the derivation
  (`<!-- 5.4% = 0.042/0.783, tab2 col 2 / baseline mean -->`). No source →
  `[AUTHOR: number — not found in outputs]`.
- **Citations**: only works present in the project bibliography or supplied by
  the author in clarifications. A needed-but-missing citation becomes
  `[AUTHOR: cite — claim needs a source]`. Never generate a plausible
  reference.
- **Positioning elements**: inserted from the profile's human-authored text,
  adjusted only grammatically to fit the sentence; if the fit requires real
  rewording, show the reworded version beside the original as a variant
  choice.
- **Facts about the study** (sample, setting, timeline): from the repo
  (memory file, PAP, draft). Unverifiable specifics → `[AUTHOR: ...]`.

The `[AUTHOR: ...]` and `[GUESS: ...]` markers are part of the audit trail:
`wb-paper-review`'s accuracy domain treats any surviving marker as a P0
comment, so nothing slips into a "final" draft unresolved.

## 5. Voice application

Priority order when constraints collide:

1. Profile Non-negotiables and `overrides baseline` conventions.
2. Voice fingerprint (rhythm, person, hedging profile, signature moves — use
   signature moves sparingly and naturally, ~their observed frequency; a tic
   repeated every paragraph is parody, not voice).
3. Profile conventions (tag-matched to the section).
4. econ-write baseline (style rules, section formulas, anti-AI patterns —
   note the baseline's banned-word list applies to *your* drafting output
   always, voice fingerprint or not).

Read the draft back once before presenting: would the author's own Writing
Critic pass this? Fix what it would flag; do not present prose you know fails
the user's own standards.

## 6. After the draft

State plainly with the draft: which clarification answers shaped it, where the
variants differ, every `[AUTHOR:]`/`[GUESS:]` marker left in, and the
reminder that the section is `ai-draft, human-touched: no` until they edit
it. Suggest — as options, not homework — the two most useful next moves (e.g.
"edit the bullets I got wrong, or run the Writing Critic's language domain on
this section").
