---
name: prepare-slides
description: Build, improve, rebrand, or review DECDI/DIME research presentations in Quarto/Reveal.js, Beamer/LaTeX, or PowerPoint. Use when turning a manuscript or results folder into slides; assessing or improving an existing .qmd, Beamer .tex, .pptx, PDF, or rendered HTML deck; applying DECDI or WBG branding; or checking presentation structure, figures, tables, and render quality.
---

# Prepare Slides

Create a new research deck or review an existing one through two distinct
phases: first plan and obtain approval, then build and verify. Keep this file
focused on the workflow. Load the bundled references for detailed structural,
evidence, branding, and format standards.

## Select the service

Route the request into one of three services:

- **Build:** create a new deck from a manuscript, results, project materials,
  or an approved outline.
- **Improve:** revise an existing deck's narrative, wording, content density,
  figures, tables, layouts, and branding. A substantial branded improvement
  uses the bundled starter as the visual base and transfers the approved
  content into it.
- **Rebrand:** preserve the existing narrative, wording, content arrangement,
  and slide count and order, while changing visual identity — fonts, colors,
  logos, backgrounds, chart styling, and the brand-carried structural
  treatments defined in `references/decdi-branding.md` (section-divider
  style, title-slide treatment, table styling, visual-note styling). A
  rebrand that only updates color values but leaves these structural
  treatments untouched has not fully applied the brand.

Treat rebranding as a targeted, faster service. Do not require a full narrative
redesign unless the review finds a problem that prevents a reliable rebrand.
If the requested service is ambiguous, state the inferred service and ask only
when the distinction would materially change the result.

## Establish the task

Inspect the supplied files before proposing an outline. Determine:

- Whether the service is build, improve, or rebrand.
- Whether the task starts from a manuscript, results folder, existing deck, or
  some combination.
- The intended audience, presentation purpose, and approximate speaking time.
- The source material available: manuscript, data, results, figures, tables,
  existing deck, or other supporting files.
- Whether DECDI, a specific program, LEADS, WBG, or another brand is expected.

### Source-access gate

Before Phase 1, classify each supplied source as **primary** or **supporting**.
A primary source is one the task depends on for its claims, narrative, or
requested content. Record each primary file as `read`, `partially read`, or
`unreadable`, with the sections or pages inspected when available.

When a manuscript PDF is a primary source, access and use its contents before
proposing the outline. Existing slides, filenames, summaries, and supplementary
files may support the work, but they do not replace reviewing the manuscript.
Follow the efficient PDF-reading procedure in `references/slide-structure.md`.
Do not present an outline as manuscript-based when the PDF was not read.

If a primary PDF cannot be accessed, report the problem and request an
accessible PDF or extracted text instead of inferring its contents. Do not
silently continue from secondary materials. This gate does not require reading
an unrelated PDF or a primary source that is irrelevant to a narrow,
already-specified edit.

Do not require the output format during Phase 1. If the user already specified
Quarto/Reveal.js, Beamer, or PowerPoint, record the choice and do not ask again.
Preserve an existing deck's format unless the user requests a conversion.

Ask only for information that materially affects the proposal. If a safe
assumption is possible, state it and proceed.

Do not use this skill for manuscripts or reports that remain documents rather
than presentations.

## Phase 1: Plan and approve

Do not create, edit, rebrand, or rebuild presentation files in this phase.

1. Inventory the available source material, apply the source-access gate, and
   identify what each source can support.
2. For build or improve, read `references/slide-structure.md` and plan the
   narrative, timing, and main-deck/appendix split.
3. For build or improve, read `references/figure-table-guidelines.md` and
   apply its mandatory exhibit-selection flow. Decide the claim and whether the
   evidence belongs in the main deck before choosing the exhibit form; choose
   the visual pattern only after the exhibit form is settled. Identify any
   figure or table that should be retained, simplified, replaced, moved, or
   omitted.
4. If an existing deck was supplied, apply
   `references/deck-review-checklist.md` and inspect the rendered deck whenever
   possible.
5. If branding is being assessed in an existing deck, apply
   `references/decdi-branding.md` during the review.
6. Present the Phase 1 proposal and wait for author approval.

### Fast path for narrow, already-specified changes

Use this instead of the full Phase 1 proposal when the author names a small
number of specific, unambiguous changes to an existing deck — for example
"fix the overflow on slide 4 and swap the chart on slide 7" — rather than
asking for a review or a broader improvement.

1. Restate the specific changes as a short list, noting any assumption
   needed to execute one of them.
2. Ask for a one-line go-ahead. Do not produce a narrative summary,
   slide-by-slide outline, visual decision table, or the full Author Decision
   Form for this case.
3. Proceed to Phase 2 and edit the existing deck's file directly (the same
   as a "Ready with minor revisions" verdict) — do not copy the starter
   folder or remap content into it for a narrowly-scoped request.

If executing a named change reveals a larger problem than the author
described — for example, fixing one slide's overflow reveals the whole deck
has no coherent narrative — stop, report what was found, and offer a full
Phase 1 review rather than silently expanding scope beyond what was asked.

### Phase 1 proposal for build or improve

Use this full proposal for a build, or an improve request broad enough that
the Fast path above does not apply. Provide:

1. A concise source-use summary listing each primary file, its role, its
   `read`, `partially read`, or `unreadable` status, the sections or pages used,
   and any access limitation.
2. A short narrative summary explaining the proposed story, audience fit, and
   approximate main-deck/appendix split.
3. A slide-by-slide outline following `references/slide-structure.md`, using
   stable IDs such as `S01`, `S02`, and `S03`. Record the shared visual pattern
   (`one-visual`, `visual-and-text`, or `comparison`) for each evidence slide
   after applying the exhibit-selection flow.
4. A decision table following `references/figure-table-guidelines.md` for every
   meaningful visual alternative, using stable IDs such as `V01`, `V02`, and
   `V03`. Include the slide claim, recommended exhibit form, evidence needed,
   and main-deck, appendix, or omit destination. Do not create alternatives
   solely to add visual variety.
5. For an existing deck, the assessment and prioritized recommendations
   required by `references/deck-review-checklist.md`.
6. A prefilled Author Decision Form.

Do not manufacture alternative visuals during Phase 1. Describe them clearly
enough for the author to choose. When data are unavailable, follow the
manuscript-results workflow in `references/figure-table-guidelines.md` and
state which options can be produced faithfully from the reported results.

### Compact Phase 1 proposal for rebrand

For a rebrand-only request, provide:

1. A brief assessment of the current branding.
2. The global elements to change, such as theme fonts, colors, chart styles,
   logos, backgrounds, slide numbers, and repeated objects.
3. Any slide-specific exceptions or problems that cannot be fixed globally.
4. A prefilled Author Decision Form.

Do not require a revised outline or visual-alternative table when content and
structure will remain unchanged. If a content or layout problem prevents a
clean rebrand, flag it separately and ask whether to expand the service to
improvement.

### Author Decision Form

End the Phase 1 proposal with a prefilled form that uses the same IDs:

```text
Service: Build / Improve / Rebrand
Outline: Approve / Approve with changes / Revise

Slide changes:
- S__: [requested change]

Visual decisions:
- V01: [option letter or Keep existing]
- V02: [option letter or Keep existing]

Logo family: DECDI/DEC logo (default) / World Bank Group logo

Other comments:
- [optional]
```

For a rebrand-only request, omit the outline and visual-decision fields unless
they are relevant. If the author approves the prefilled form without changing
the logo field, treat the DECDI/DEC logo as approved. Do not ask again when the
author already specified a logo family.

Include the **Logo family** field only when branding is actually in scope —
a Rebrand, a Build, or an Improve where the review flagged the logo as wrong,
missing, or ambiguous. Omit it for a content-only Improve request where the
existing logo is already correct; asking about logo family on every request
regardless of relevance adds friction without adding information.

The author may instead respond, `Approve the outline and all recommended visual
options.` Record clear natural-language responses even when they do not copy
the form exactly.

Before Phase 2:

- Resolve every requested outline change and required visual decision.
- Do not interpret silence as approval.
- Do not treat approval of a visual concept as permission to invent missing
  values or reconstruct unreported data.
- Summarize the approved outline, visual choices, and any remaining limitations.
- If an approved change cannot be implemented faithfully, return to the author
  with a specific alternative or deferral rather than silently skipping it.

If the user has already supplied or approved a complete outline and all visual
decisions, summarize that approval and proceed directly to Phase 2.

## Phase 2: Build and verify

Begin only after Phase 1 is approved.

1. Ask whether the final deck should be PowerPoint, Quarto/Reveal.js, or Beamer
   unless the user already selected a format.
2. Read the selected section of `references/format-conventions.md`.
3. Apply `references/decdi-branding.md` unless the user specifies another
   brand.
4. Follow the service-specific starting workflow:
   - **Build:** copy the complete format-specific starter folder from `assets/`
     and create the approved deck from that starter.
   - **Improve:** follow the targeted-revision or template-based-reconstruction
     direction stated in the approved Phase 1 review
     (`references/deck-review-checklist.md`'s Revision recommendation and
     Overall verdict).
     - If the verdict was **Ready with minor revisions** (targeted revision):
       edit the existing deck's file directly, in a copy. Do not copy the
       starter folder or remap content into it — that is unnecessary work for
       a deck whose structure and branding are already sound.
     - If the verdict was **Needs substantial revision** or **Rebuild
       recommended** (template-based reconstruction): copy the complete
       format-specific starter folder from `assets/`, map the approved content
       into the closest starter layouts, and rewrite, split, reorder, or move
       detail as approved.
     - Either way, do not preserve dense wording merely because it appeared in
       the original deck.
     - If no formal Phase 1 review preceded this (the author specified a
       small number of named changes directly — see "Fast path for narrow,
       already-specified changes" in Phase 1), edit the existing deck's file
       directly, the same as a minor-revisions verdict.
   - **Rebrand:** work in a copy of the existing editable deck or source
     project. Preserve its content, narrative, content arrangement, slide
     count, and order; apply approved theme-level, repeated, and
     brand-carried structural changes (see `references/decdi-branding.md`,
     including section-divider and title-slide treatment, which may
     legitimately change even though content arrangement does not) before
     slide-specific exceptions.
5. Build the approved outline and visual choices. If a new content decision is
   needed, flag it rather than silently changing the approved direction.
6. Batch related changes, then build or export the deck and inspect the
   rendered output.

For every Phase 2 run that creates or edits an output, keep a short
`production-decisions.txt` beside the editable source. Create it when Phase 2
begins and start it with an **Approval record** that preserves the completed
Author Decision Form, including:

- service and output format;
- primary source files and any source-access limitations;
- outline status and approved slide changes, when relevant;
- the selected option for every visual ID;
- logo family, when branding is in scope;
- other author comments and known limitations.

Normalize a clear natural-language approval into these fields even when the
author did not complete the form verbatim. Mark irrelevant fields as not
applicable; do not infer a decision that the author did not make.

After the approval record, record each slide ID, final title, approved visual
pattern, visual ID and exact local asset path, plus any figure-generation
script, input files, command or parameters (including a random seed when used),
and output path. For a narrow edit or rebrand, record the approved named changes
and affected source files instead of manufacturing a full slide record. For
generated imagery, retain the approved image file and record its prompt and
model when available. Record necessary deviations from the approved outline.
Keep generated visual assets with the deck. Do not calculate file hashes.

For a subsequent run on the same deck, read `production-decisions.txt` before
planning or building. Reuse its recorded approvals, layouts, and assets when
the new request does not supersede them and their dependencies remain
available. Do not ask the author to repeat those decisions. Record any newly
approved change or unavailable dependency in the same file; prior approval is
not permission for an unrequested change.

When a manuscript is the only source for a figure or table, implement the
author's approved choice: either adapt the reported result into a faithful,
branded presentation visual when enough exact information is available, or
leave an editable placeholder for the author to insert a screenshot. Do not
capture or insert screenshots from the manuscript yourself.

When improving or rebranding an existing deck, use it as the source of truth
for claims, evidence, and approved content. Keep the original file unchanged
unless the author explicitly requests in-place editing.

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

`assets/pptx/` also includes `duplicate_slide.py` — use it to duplicate a
starter slide rather than copying shapes by hand; see
`references/format-conventions.md` for why a hand-rolled copy silently drops
the slide's background fill.

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

1. Build or export the deck with the format-specific workflow after batching
   related changes; do not rerender after every minor edit unless needed to
   diagnose a problem.
2. Inspect the rendered HTML, PDF, or PowerPoint rather than relying only on
   source code.
3. Inspect every new or changed slide at full size and inspect the complete
   deck sequence. Check narrative order, content accuracy, branding, fonts,
   logo placement, contrast, image quality, clipping, overflow, overlap, and
   missing assets. Apply the shared preset-layout and raster-dimension tests in
   `references/figure-table-guidelines.md`. Run automated overflow or overlap
   checks when the available tooling supports them.
4. Fix material problems and rebuild until the output is presentation-ready.
5. Reconcile the result against every approved Phase 1 item and confirm that
   none was silently skipped.
6. Confirm that no template examples, unintended placeholders, or temporary
   build artifacts remain. Retain clearly labeled screenshot placeholders only
   when the author approved them. For a new or rebuilt slide, if an asset fails
   the raster-dimension rule and no suitable replacement exists, leave its visual
   area blank, identify the affected slide and asset in the handoff, and do not
   describe that deck as presentation-ready. For a targeted edit or rebrand,
   preserve and flag an existing failing visual unless replacement was approved.

Deliver the editable source, required local assets, and rendered output. Note
any approved screenshot placeholders, unresolved content questions,
substitutions, or validation limitations.
