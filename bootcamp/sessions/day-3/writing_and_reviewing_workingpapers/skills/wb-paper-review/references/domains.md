# Review Domains

The domain axis of the scope menu: what lens the review applies and which
protocols it loads. Load only the selected domain's files, and only when the
run starts. Paths are relative to the skills folder root.

Each domain lists a **default guide** — used when the user picks a domain
without naming guides; say which guide was auto-selected and why, in plain
language.

## `accuracy` — numbers, claims, citations

*Does the text say what the evidence says?* Default guide: Methodologist.

Load: `upstream-econ-review/reader-claim-audit.md`;
`econ-write/SKILL.md` § Citation Integrity.

**Intrinsic scope**: the claim surface — abstract, introduction (incl. its
citations), conclusion, and the bibliography — belongs to this domain even
under a section scope, unless the user explicitly excludes it after the
scope-interaction warning (see SKILL.md § Configure).

Checks: every in-scope number traced to the output files in the profile's
Grounding pointers — an untraceable number is **P0 at pre-submission stage**
(report each individually); abstract, intro, and conclusion claims within the
estimated population, magnitude, and horizon; positioning consistency (does
the text deliver the profile's claimed main finding?); citation integrity —
every in-scope citation resolves to a bibliography entry, and flag any entry
whose existence or attribution cannot be confirmed (unresolvable outlet,
implausible detail) for the author to verify.

## `design` — identification, inference, robustness

*Would the analysis survive a methods seminar?* Default guide: Methodologist.

Load: `upstream-econ-review/design-audit.md`;
`upstream-econ-review/inference-audit.md`; the matching gate
(`upstream-econ-review/gates/did.md` / `iv.md` / `rdd.md`) when the profile's
method has one; `econ-write/identification-strategies.md` section for the
method (for how the *prose* should present it).

Checks: the gate's required design facts present in the text; identifying
assumption stated and defended in economic terms; threats sequenced and
addressed; clustering/inference choices stated and appropriate; robustness
proportionate to the fragile assumptions.

## `argument` — structure, logic, narrative

*Does the paper's argument hold together and land in the right order?*
Default guide: Writing Critic (structure priorities) + Methodologist for
logic gaps — say which owns which comment.

Load: `upstream-econ-review/argument-evidence-audit.md`; `econ-write/SKILL.md`
section formulas (Abstract, Introduction, Conclusion) and Paper Structure
Overview; profile `structure` conventions.

Checks: main result placement; each section's job done (intro formula
satisfied or a recorded profile override applies); claim–evidence chains
unbroken; redundancy across abstract/intro/conclusion beyond the deliberate;
roadmap and cross-references consistent.

## `presentation` — tables, figures, exhibits

*Are the exhibits self-contained, consistent, and pulling their weight?*
Default guide: Writing Critic.

Load: `upstream-econ-review/table-audit.md`;
`upstream-econ-review/figure-audit.md`; `econ-write/SKILL.md` § Tables and
Figures; profile `tables` conventions.

Checks: caption self-containment (regression, variables, SE/clustering
stated); every table number discussed in text and consistent with it
(overlaps accuracy — exhibit-side of the same check); figure-vs-table choices;
decimal and unit consistency; exhibit ordering vs. narrative.

## `language` — style, clarity, voice, AI patterns

*Is the prose fast, concrete, and the author's own?* Default guide: Writing
Critic.

Load: `econ-write/SKILL.md` § Writing Style Rules + § Avoiding AI-Generated
Writing Patterns; `econ-write/review-checklist.md` § Anti-AI Detection
Checklist; profile Voice fingerprint (protection list) and `tone` conventions.

Checks: phrases-to-delete and banned-word scan; passive/throat-clearing/
concreteness; sentence rhythm vs. the voice fingerprint (deviations from
*fingerprint*, not from generic style, are the finding); AI-tell patterns —
run this scan double-strength on sections whose ledger status is `ai-draft`
or `human-touched: no`.

## `policy` — audience, relevance, implications

*Will the intended reader get it, believe it, and know what to do?* Default
guide: Policy.

Load: the Policy guide file (its priorities are the protocol);
`econ-write/SKILL.md` § Writing the Conclusion › Implications;
`econ-write/specialized-tasks.md` § non-academic audiences (when the target
includes policy readers).

Checks: the so-what test against the profile's Audience; recommendations
earned by results; magnitudes in the audience's units; external validity
honesty; positioning relevance sentence actually cashed out in the text.

## `outlet` — compliance

*Does the draft meet the binding constraints of its target outlet (for example a journal)?* Default guide: a bespoke outlet guide if one exists, otherwise the Writing guide.

Load: profile Outlet constraints only.

Checks: each binding constraint pass/fail (lengths, required sections and
statements, citation style, format). Surface the outlet's AI-disclosure policy
and check the ledger supports the required disclosure (see
`shared/aitl-protocol.md` § 6).

## `full` — everything

All domains, all selected guides. State the cost implication before running
and get explicit confirmation — this produces a long triage session. Suggest
`accuracy` + the user's fear-matched domain as the high-value alternative.

## Adding domains

Users may define their own domains in `wb-paper/domains.md` (same format:
name, question, load list, checks). User-defined domains appear in the menu
alongside these.
