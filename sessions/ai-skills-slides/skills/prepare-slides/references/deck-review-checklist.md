# Existing Deck Review Checklist

Use this checklist when an author shares an existing Quarto, Beamer,
PowerPoint, PDF, or rendered HTML deck and asks whether it is effective,
properly branded, or ready to present.

Evaluate the deck against the same structural, visual, branding, and
format-specific standards used when building a new deck with this skill.

Review and report first. Do not modify, restructure, rebrand, or rebuild the
deck unless the user approves the proposed changes.

This review is Phase 1 of the skill. It must produce both an assessment of the
current deck and an approvable revision plan. Editing begins only in Phase 2.

## Standards used in the review

Apply:

- `slide-structure.md` when evaluating audience fit, narrative, section flow,
  slide purpose, closing, and appendix content.
- `figure-table-guidelines.md` when evaluating figures, tables, sources,
  uncertainty, manuscript-derived results, and image quality.
- `decdi-branding.md` when evaluating colors, fonts, logos, contrast, and
  program-specific branding.
- The relevant section of `format-conventions.md` when evaluating Quarto,
  Beamer, or PowerPoint implementation and rendering.

## Review scope

Before reviewing, identify or reasonably infer:

- Intended audience.
- Presentation purpose.
- Expected presentation length.
- Output format.
- Whether DECDI, LEADS, WBG, or another branding standard is expected.
- Whether manuscript, results, data, or other source material is available.

If any of these are uncertain and materially affect the review, state the
assumption or ask the user for clarification.

Review the rendered deck whenever possible. Inspect source files when they are
available and useful for diagnosing structure, rendering, or missing assets.

If only a PDF, PowerPoint, or rendered HTML file is available, review what can
be observed and state any limitations.

## Review ratings

Use the following category ratings:

| Rating | Meaning |
|---|---|
| Strong | Effective and presentation-ready in this area |
| Adequate | Generally effective, with some improvements possible |
| Needs attention | Material problems affect clarity, consistency, or readiness |

Classify individual recommendations by priority:

| Priority | Meaning |
|---|---|
| Must fix | Incorrect, unsupported, broken, unreadable, or missing |
| Should improve | Weakens clarity, structure, consistency, or usability |
| Optional | Stylistic refinement that does not affect correctness |

## Audience and purpose

Apply `slide-structure.md`.

- [ ] Is the intended audience clear?
- [ ] Is the presentation’s purpose clear?
- [ ] Is the technical level appropriate for the audience?
- [ ] Are important terms explained at the appropriate level?
- [ ] Does the amount of content fit the expected presentation time?
- [ ] Does the opening establish the research question, problem, or decision?

## Narrative and structure

Apply `slide-structure.md`.

- [ ] Does the deck progress logically from context to evidence to conclusion?
- [ ] Do the slide titles reveal a coherent narrative when read in order?
- [ ] Does each slide have one clear communicative purpose?
- [ ] Are major narrative transitions clear?
- [ ] Is any content repetitive, unnecessary, or out of sequence?
- [ ] Is supporting technical detail placed in the appendix where appropriate?
- [ ] Does the deck include a substantive conclusion, implication, action, or
      learning recap before the final thank-you slide?
- [ ] Can appendix slides be understood when opened independently?

## Content and evidence

Evaluate only what can be verified from the materials provided.

- [ ] Are the central claims supported by evidence shown or cited in the deck?
- [ ] Do numerical claims match the accompanying figures and tables?
- [ ] Does the language match the strength of the evidence?
- [ ] Is causal language used only when supported?
- [ ] Are limitations and uncertainty represented appropriately?
- [ ] Is any important result missing from the main narrative?
- [ ] Is any context, value, source, or interpretation apparently invented?
- [ ] Are citations sufficient for the audience to trace important claims?

If the manuscript, results, or source data were not provided, state that the
review assesses presentation quality rather than independently validating the
research findings.

## Figures and tables

Apply `figure-table-guidelines.md`.

- [ ] Does each figure or table support a clear slide message?
- [ ] Are titles accurate and appropriately finding-led?
- [ ] Are axes, units, groups, and time periods clear?
- [ ] Is uncertainty shown where it matters?
- [ ] Is each figure and table traceable internally?
- [ ] Are external sources cited visibly, without unnecessary manuscript
      table or figure numbers?
- [ ] Are small interpretation notes included where significance, uncertainty,
      sample, units, or restrictions require explanation?
- [ ] Are visuals legible at presentation size?
- [ ] Are tables simplified appropriately for presentation?
- [ ] Does the deck use unformatted software output as final slide content?
- [ ] Are manuscript-derived figures and tables represented faithfully?
- [ ] Are author-supplied manuscript-table or figure crops legible and used
      intentionally?
- [ ] Are colors accessible and consistent with the expected branding?
- [ ] Are images sharp, correctly proportioned, and free of clipping?

## Branding

Apply `decdi-branding.md`.

When DECDI branding is expected:

- [ ] Are Montserrat and Lato used where the format supports them?
- [ ] Are colors drawn from the approved palette?
- [ ] Are program-specific colors used only when appropriate?
- [ ] Is the correct DEC, LEADS, or WBG logo family used?
- [ ] Is the correct logo variant used for the background?
- [ ] Does logo placement follow the current template convention?
- [ ] Are logos undistorted and given adequate visual space?
- [ ] Are any legacy, conflicting, or unrelated institutional elements present?
- [ ] Is text and visual contrast sufficient?

If the deck intentionally follows another institution’s branding, report that
it does not follow DECDI branding and ask whether rebranding is desired. Do not
treat intentional external branding as an error without confirming the
expected standard.

## Format implementation

Apply the relevant section of `format-conventions.md`.

- [ ] Does the deck follow the conventions of its source format?
- [ ] Is the rendered output free of clipping, overlap, and layout errors?
- [ ] Are fonts rendered as intended?
- [ ] Are figures and tables positioned correctly?
- [ ] Are section layouts consistent?
- [ ] Are logos present where expected?
- [ ] Are links, citations, and internal references working?
- [ ] Are any images or other assets missing?
- [ ] Are placeholders or template examples still present?

When editable source files are available:

- [ ] Does the deck build successfully?
- [ ] Do relative image and asset paths resolve?
- [ ] Does the build produce the expected output format?

## Visual consistency

- [ ] Are title placement and heading styles consistent?
- [ ] Are bullet styles, capitalization, and punctuation consistent?
- [ ] Are spacing, margins, and alignment consistent?
- [ ] Are font sizes readable and used consistently?
- [ ] Are page numbers, footers, and section labels correct?
- [ ] Are author, affiliation, date, and contact details correct?
- [ ] Are there any `TODO` markers, placeholder values, or sample content?

## Overall verdict

Choose one verdict:

| Verdict | Meaning |
|---|---|
| Ready to present | No material problems prevent presentation |
| Ready with minor revisions | Targeted improvements are recommended |
| Needs substantial revision | Major issues affect clarity or readiness |
| Rebuild recommended | Incremental revision is unlikely to be efficient or reliable |

## Review report

Present the findings using this structure:

```markdown
# Existing Deck Review

## Overall assessment

**Verdict:** Ready with minor revisions

Briefly explain the deck’s overall effectiveness and the most important issues.

## What works well

- Strength one.
- Strength two.
- Strength three.

## Highest-priority improvements

1. Most important improvement.
2. Second improvement.
3. Third improvement.

## Category assessment

| Category | Rating | Summary |
|---|---|---|
| Audience and purpose | Strong | |
| Narrative and structure | Adequate | |
| Content and evidence | Adequate | |
| Figures and tables | Needs attention | |
| Branding | Adequate | |
| Format implementation | Strong | |
| Visual consistency | Adequate | |

## Slide-level recommendations

| Current slide | Slide ID | Observation | Priority | Proposed action |
|---|---|---|---|---|
| 4 | S04 | | | Keep, revise, combine, move, or remove |
| 7 | S05 | | | |
| New | S06 | | | Add |

## Proposed revised outline

Include the slide-by-slide outline defined in `slide-structure.md`. Map current
slide numbers to the stable `S01`, `S02`, and related IDs where applicable.

## Visual decisions

List each meaningful alternative using the `V01`, `V02`, and related decision
IDs defined in `figure-table-guidelines.md`. Do not create the alternatives yet.

## Revision recommendation

State whether targeted revision is sufficient or a full rebuild should be
considered.

## Author Decision Form

Include the prefilled approval form from `SKILL.md`, covering the outline,
slide-specific changes, visual options, and the targeted-revision or rebuild
direction. Stop after the report and wait for the author's response.
```

## When to recommend a rebuild

Recommend discussing a rebuild when:

- The deck lacks a coherent narrative.
- Most slides require structural changes.
- Incorrect or conflicting branding is deeply embedded.
- The current format cannot support the requested result cleanly.
- The deck contains pervasive layout or rendering problems.
- Incremental edits would be slower or less reliable than rebuilding from the
  provided template.

Do not silently replace an existing deck. Summarize the problems, explain the
tradeoff, and ask whether the user wants targeted revisions or a full rebuild.
