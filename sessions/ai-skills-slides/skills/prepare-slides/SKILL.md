---
name: prepare-slides
description: Create, revise, or review DECDI/DIME research presentations in Quarto/Reveal.js, Beamer/LaTeX, or PowerPoint. Use when turning a manuscript or results folder into slides; assessing or improving an existing .qmd, Beamer .tex, .pptx, PDF, or rendered HTML deck; applying DECDI branding; or checking presentation structure, figures, tables, and render quality.
---

# Prepare Slides

Create a new research deck or review an existing one through two distinct
phases: first plan and obtain approval, then build and verify. Keep this file
focused on the workflow. Load the bundled references for detailed structural,
evidence, branding, and format standards.

## Establish the task

Inspect the supplied files before proposing an outline. Determine:

- Whether the task starts from a manuscript, results folder, existing deck, or
  some combination.
- The intended audience, presentation purpose, and approximate speaking time.
- The source material available: manuscript, data, results, figures, tables,
  existing deck, or other supporting files.
- Whether DECDI, a specific program, LEADS, WBG, or another brand is expected.

Do not require the output format during Phase 1. If the user already specified
Quarto/Reveal.js, Beamer, or PowerPoint, record the choice and do not ask again.
Preserve an existing deck's format unless the user requests a conversion.

Ask only for information that materially affects the proposal. If a safe
assumption is possible, state it and proceed.

Do not use this skill for manuscripts or reports that remain documents rather
than presentations.

## Phase 1: Plan and approve

Do not create, edit, rebrand, or rebuild presentation files in this phase.

1. Inventory the available source material and identify the claims and visuals
   it can support.
2. Read `references/slide-structure.md` and plan the narrative, timing, and
   main-deck/appendix split.
3. Read `references/figure-table-guidelines.md` and identify any figure or
   table that should be retained, simplified, replaced, moved, or omitted.
4. If an existing deck was supplied, also apply
   `references/deck-review-checklist.md` and inspect the rendered deck whenever
   possible.
5. If branding is being assessed in an existing deck, apply
   `references/decdi-branding.md` during the review.
6. Present the Phase 1 proposal and wait for author approval.

### Required Phase 1 proposal

Provide:

1. A short narrative summary explaining the proposed story, audience fit, and
   approximate main-deck/appendix split.
2. A slide-by-slide outline following `references/slide-structure.md`, using
   stable IDs such as `S01`, `S02`, and `S03`.
3. A decision table following `references/figure-table-guidelines.md` for every
   meaningful visual alternative, using stable IDs such as `V01`, `V02`, and
   `V03`.
4. For an existing deck, the assessment and prioritized recommendations
   required by `references/deck-review-checklist.md`.
5. A prefilled Author Decision Form.

Do not manufacture alternative visuals during Phase 1. Describe them clearly
enough for the author to choose. When data are unavailable, follow the
manuscript-results workflow in `references/figure-table-guidelines.md` and
state which options can be produced faithfully from the reported results.

### Author Decision Form

End the Phase 1 proposal with a prefilled form that uses the same IDs:

```text
Outline: Approve / Approve with changes / Revise

Slide changes:
- S__: [requested change]

Visual decisions:
- V01: [option letter or Keep existing]
- V02: [option letter or Keep existing]

Other comments:
- [optional]
```

The author may instead respond, `Approve the outline and all recommended visual
options.` Record clear natural-language responses even when they do not copy
the form exactly.

Before Phase 2:

- Resolve every requested outline change and required visual decision.
- Do not interpret silence as approval.
- Do not treat approval of a visual concept as permission to invent missing
  values or reconstruct unreported data.
- Summarize the approved outline, visual choices, and any remaining limitations.

If the user has already supplied or approved a complete outline and all visual
decisions, summarize that approval and proceed directly to Phase 2.

## Phase 2: Build and verify

Begin only after Phase 1 is approved.

1. Ask whether the final deck should be PowerPoint, Quarto/Reveal.js, or Beamer
   unless the user already selected a format.
2. Read the selected section of `references/format-conventions.md`.
3. Apply `references/decdi-branding.md` unless the user specifies another
   brand.
4. Copy the complete format-specific starter folder from `assets/` into the
   output project and adapt the copy. Do not build a branded deck from an empty
   file when a bundled template is available.
5. Build the approved outline and visual choices. If a new content decision is
   needed, flag it rather than silently changing the approved direction.
6. Build or export the deck and inspect the rendered output.

When a manuscript is the only source for a figure or table, implement the
author's approved choice: either adapt the reported result into a faithful,
branded presentation visual when enough exact information is available, or
leave an editable placeholder for the author to insert a screenshot. Do not
capture or insert screenshots from the manuscript yourself.

When revising an existing deck, use the supplied deck as the primary source.
Apply only the approved targeted revisions or rebuild direction. Do not
silently replace the author's deck.

## Reference guide

Read each selected reference completely before applying it.

| Reference | Load when |
|---|---|
| `references/slide-structure.md` | Phase 1 for audience fit, narrative, content selection, timing, closing, appendix decisions, and the outline |
| `references/figure-table-guidelines.md` | Phase 1 whenever the deck contains or makes claims from figures, tables, or numerical results; reuse during Phase 2 production |
| `references/deck-review-checklist.md` | Phase 1 when an existing deck is supplied for review or revision |
| `references/decdi-branding.md` | Phase 1 when assessing an existing deck's branding; Phase 2 when producing a branded deck |
| `references/format-conventions.md` | Phase 2 after the output format is selected; during Phase 1 only when source-format problems must be diagnosed in an existing deck |

References define standards and decision rules. Do not copy them into the
user's output.

## Branding source

Treat `branding/colors.yml` and `branding/logos/` as the canonical branding
files for this skill. Use them to maintain the format-specific copies bundled
under `assets/`; do not require a repository-level branding folder.

When the brand changes, update `branding/` first, synchronize the affected
copies in all three starter projects, and render each format for visual
verification. Do not copy `branding/` into a user's output project unless the
output specifically needs one of its files.

## Bundled starters

Use assets as working files in the output project:

| Format | Copy |
|---|---|
| Quarto/Reveal.js | `assets/quarto/` |
| Beamer | `assets/beamer/` |
| PowerPoint | `assets/pptx/` |

Copy the complete folder so templates, extensions, logos, supporting files,
and relative paths remain intact. Follow `references/format-conventions.md`
for the required build or export workflow. Create and edit PowerPoint directly
as `.pptx`; do not route PowerPoint output through Quarto.

## Protect research integrity

- Base every substantive claim on the supplied manuscript, results, data, or
  another traceable source.
- Preserve values, units, signs, uncertainty, sample definitions, and the
  strength of the original claim.
- Do not invent missing context, citations, sources, definitions, or results.
- Flag ambiguity or inconsistency instead of guessing.
- Keep a traceable source for every numerical claim, figure, and table.

## Final verification and delivery

Work in a copy or designated output location; preserve the user's original
source unless they explicitly ask for in-place edits.

Before delivery:

1. Build or export the deck with the format-specific workflow.
2. Inspect the rendered HTML, PDF, or PowerPoint rather than relying only on
   source code.
3. Check narrative order, content accuracy, branding, fonts, logo placement,
   contrast, image quality, clipping, overflow, and missing assets.
4. Fix material problems and rebuild until the output is presentation-ready.
5. Confirm that no template examples, unintended placeholders, or temporary
   build artifacts remain. Retain clearly labeled screenshot placeholders only
   when the author approved them.

Deliver the editable source, required local assets, and rendered output. Note
any approved screenshot placeholders, unresolved content questions,
substitutions, or validation limitations.
