# Slide Structure

Use this reference to plan the narrative and select content for Quarto, Beamer,
or PowerPoint decks. Keep format-specific syntax, styling, and build commands in
the corresponding format reference.

## Structural principles

### Give each slide one communicative purpose

A slide may contain several objects when they work together to make one point.
For example, two charts may belong on the same slide when their comparison is
the message.

- State the point in the title when possible: "Treatment effects are largest
  in urban areas" is stronger than "Results."
- Prefer 3-5 concise talking points when bullets are appropriate.
- Split a slide when its central message cannot be understood within a few
  seconds, not merely because one bullet wraps onto a second line.
- Do not shrink text to preserve excess content. Simplify the slide or move
  supporting detail to notes or the appendix.
- Use paragraphs sparingly; slides should support the speaker rather than serve
  as a manuscript page.

### Build an argument, not a collection of slides

The audience should be able to follow a clear progression from question to
evidence to implication. Each slide should prepare for or support the next one.
Avoid organizing the deck around filenames, software outputs, or manuscript
section labels when a claim-based sequence would be clearer.

### Match the deck to the available time

- Ask for the presentation length when it would materially change the result.
- As a planning heuristic, allow roughly 1.5-2 minutes per substantive slide.
- Treat title and section-divider slides as low-time slides.
- Prefer a shorter main deck with an appendix over an overfilled main deck.
- Use the timing estimate as a planning aid, not a hard limit.

## Core narrative shape

Adapt this sequence to the purpose and length of the presentation:

1. **Title** - title, optional subtitle, author, affiliation, and date.
2. **Opening question, problem, or decision** - establish why the audience
   should care.
3. **Essential context** - provide only the background required to understand
   the evidence.
4. **Approach or evidence base** - explain the data, method, or source at the
   level needed by the audience.
5. **Headline findings** - organize results around claims, not source-file
   order.
6. **Interpretation and implications** - explain what the evidence means and
   what it does not establish.
7. **Closing** - end with the conclusion, decision, action, or learning recap
   appropriate for the audience.
8. **Appendix, when needed** - retain technical detail, supporting results,
   robustness checks, and supplementary material.

Agenda and section-divider slides are optional:

- Omit an agenda from a short deck when it adds no useful orientation.
- Use section dividers when the deck contains several substantial narrative
  sections.
- Keep section titles short and meaningful. Their visual treatment belongs in
  the format-specific reference.

## Audience adaptations

| Audience | Emphasize | De-emphasize | Typical closing |
|---|---|---|---|
| Academic or technical | Contribution, identification, uncertainty, robustness | General background the audience already knows | Interpretation, limitations, research questions |
| Government or policy | Decision context, headline findings, operational relevance | Technical mechanics and secondary specifications | Implications, options, recommended action |
| Training | Learning progression, worked examples, practice | Project-specific detail that does not transfer | Recap, reusable pattern, exercise prompt |
| General | Motivation, plain-language evidence, concrete examples | Jargon and specification detail | Main takeaway and why it matters |

Do not remove methodological caveats merely to simplify a deck. Adjust their
placement and wording: keep essential limitations in the main narrative and
move secondary technical detail to notes or the appendix.

## Phase 1 outline proposal

Before any presentation files are created or edited, convert the proposed
narrative into a slide-by-slide outline for author review.

Use stable slide IDs so the author can approve or revise individual items
without relying on titles that may change:

| Slide ID | Proposed title or purpose | Content and evidence | Proposed visual | Source | Location |
|---|---|---|---|---|---|
| S01 | | | | | Main deck or appendix |

The outline should:

- Begin with a short summary of the proposed story and why it fits the audience.
- Give each slide one communicative purpose.
- Identify the source supporting each substantive slide.
- Indicate whether the slide belongs in the main deck or appendix.
- Fit the requested speaking time without assuming every manuscript section
  needs a slide.
- Use a proposed finding-led title only when the evidence already supports it.
- Mark unresolved questions instead of filling gaps with assumptions.

If the source is an existing deck, map the current slides to the proposed
sequence and state whether each should be kept, revised, combined, moved,
removed, or added. Use `deck-review-checklist.md` for the full assessment.

Keep the outline independent of PowerPoint, Quarto, or Beamer syntax. Format
selection and implementation occur only after the author approves Phase 1.

## Building from scratch

### From a manuscript

Select presentation content rather than reproducing the paper's full structure.

- Identify the research question, contribution, setting, data, method, main
  findings, limitations, and implications.
- Use the abstract, introduction, conclusion, headings, figure captions, and
  table notes to locate candidate claims, then verify those claims against the
  relevant manuscript sections and results.
- Preserve citations for claims that depend on prior literature.
- Retain only the methodological detail required for the intended audience to
  understand or trust the findings.
- Keep robustness checks and specification detail in the appendix unless they
  are central to the talk.
- Do not strengthen causal, statistical, or policy claims beyond what the
  manuscript supports.
- Maintain a traceable source for every numerical claim, quotation, figure,
  and table.

A typical research presentation may follow:

1. Motivation and research question.
2. Contribution or gap.
3. Context and data.
4. Research design or analytical approach.
5. Main findings.
6. Interpretation, limitations, and implications.

This is a starting pattern, not a requirement to create one section per item.

### From results

Organize results around the claims they support.

- Inventory the supplied figures, tables, captions, notes, variable
  definitions, and data-source information.
- Group related evidence by research question or conclusion, not by file type
  or filename.
- Lead with the most decision-relevant or substantively important result.
- Use one figure or table per slide by default, while allowing deliberate
  comparisons when the comparison itself is the message.
- Do not invent variable definitions, sample restrictions, dates, sources, or
  statistical interpretations.
- Do not imply causality unless the research design and supplied material
  support a causal claim.
- Move secondary outcomes, alternative specifications, and robustness checks
  to the appendix.
- Apply `figure-table-guidelines.md` to the selected visual evidence.

If a result cannot be interpreted safely from the available material, identify
the ambiguity rather than guessing.

## Closing and appendix

Choose a substantive closing that completes the narrative:

- **Academic:** contribution, interpretation, limitations, and open questions.
- **Policy:** implications, decision options, recommendations, or next actions.
- **Training:** learning recap, reusable method, and practice prompt.
- **Project update:** decisions needed, owners, and milestones.
- **Discussion:** two or three focused questions.

A branded "Thank you" slide may follow the substantive closing, but it should
not replace the conclusion.

Use the appendix for material that supports credibility without interrupting
the main argument. Appendix slides should still have clear titles, legible
content, and enough context to be understood when opened during discussion.

## Structural quality check

Before building or approving the final deck, confirm that:

- The argument can be summarized in 2-3 sentences.
- Every main slide has a clear communicative purpose.
- Reading the slide titles in order reveals the narrative.
- Every major claim is supported by supplied evidence.
- The level of technical detail fits the audience.
- The main deck fits the available presentation time.
- Supporting detail is available in the appendix when useful.
- The closing follows logically from the findings.
- No slide depends on invented context, interpretation, or evidence.
