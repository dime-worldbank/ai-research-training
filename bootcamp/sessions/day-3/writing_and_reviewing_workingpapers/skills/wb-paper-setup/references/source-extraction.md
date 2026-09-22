# Source Extraction Protocols

How to read each input and turn it into profile content. Inputs live in the
user's `wb-paper/references/` folders (plus the project repo); Part R of the
interview supplies each file's tags, likes, dislikes, bindingness, and
fairness calls. The unifying rule: every extraction produces **convention
entries** — operational, checkable parameters with provenance — never
summaries or admiration.

| Input | Protocol |
|---|---|
| `references/positive/` (admired papers) | A |
| Author's own writing (tagged in positive/, or interview Q7, or current draft) | B |
| `references/feedback/` (referee reports, seminar feedback) | C |
| `references/guidelines/` (target-outlet guidelines, internal standards) | D |
| `references/negative/` (anti-exemplars) | N |
| Project repo | E |

## The convention entry (the atomic unit of extraction)

```markdown
- **<short name>**: <the operational rule, stated imperatively>
  - Check: <how a critic verifies it in one pass over the draft>
  - Evidence: <source file>, "<quoted fragment, ≤ 25 words>" (<location>)
  - Applies to: <sections/aspects> · Tag: <structure|tone|results|tables|policy|outlet|voice>
```

A valid entry passes three tests:

1. **Writable** — `wb-paper-write` could follow it while drafting without
   asking for clarification.
2. **Checkable** — `wb-paper-review` could mark a draft pass/fail against it
   without judgment calls a model can't make.
3. **Grounded** — it points at a specific passage, answer, or document; if you
   cannot cite where it came from, do not record it.

If an observation fails these tests, either sharpen it until it passes or drop
it. "The intro flows well" fails. "Each intro paragraph opens with a claim
sentence; evidence and citations follow within the paragraph" passes.

## The delta rule (applies to every protocol)

The vendored `econ-write` skill is the baseline; the profile records only
**deltas**. Before recording an entry, check whether it merely restates a
baseline rule (e.g. "state the main result early" is econ-write's triangular
style; "abstract under 150 words" is its abstract formula). If it does:

- **Restatement** → do not record it as a convention entry. The baseline
  already enforces it everywhere.
- **Emphasis** (the user or their materials show this baseline rule matters
  unusually much to them) → record it as a *critic priority*, phrased as a
  pointer: "econ-write › Introduction Formula — top priority for this author",
  not as a copied rule.
- **Deviation** (the user's preference *conflicts* with baseline — e.g. their
  target outlet wants a separate literature section, against econ-write's advice) →
  record it as a convention entry explicitly marked `overrides baseline:
  <section name>`. Deviations are the most valuable entries; never silently
  drop them, and confirm each at playback.

## The imitation boundary (applies to every protocol)

Extract **craft**, never **content**. Permitted: structure, ordering,
proportions, rhetorical moves, exhibit design, caption style, hedging norms,
sentence rhythm. Forbidden: claims, results, arguments, distinctive phrasings
for reuse, anything that would put another paper's text or ideas into the
user's paper. Quoted fragments in Evidence fields exist so the user can verify
the extraction — they are never drafting material. If a "convention" only makes
sense for the exemplar's content (its sample size, its result, its setting),
it is content, not craft: do not record it (see Transferability below).

## Protocol A — `positive/`: exemplar papers ("great for X")

Part R gave each file one or more tags: what it is great *for*, and what the
user admires about it. The tag scopes the reading. Do not read the whole paper
and summarize; read what the tag directs and extract 2–5 entries per tag.
More is overfitting.

**A.1 Read by tag:**

| Tag | Read | Extract (examples of the *kind* of parameter) |
|---|---|---|
| `structure` / intro | Title, abstract, full introduction; section headings of the rest | Paragraph-function map of the intro (para 1 = hook type, para N = result with magnitude, where lit review sits, roadmap present?); intro length as share of paper; section ordering |
| `tone` / voice | ~3 dispersed prose pages: one from intro, one from results, one from conclusion | Sentence-length range and mix; hedging vocabulary and frequency; first person usage; how confident claims are phrased vs. caveated; use of asides/em-dashes |
| `results` narration | Results section + the 2–3 exhibits it references | Order of presentation (main result first? build-up?); how coefficients are translated into meaningful units; benchmark comparisons used; ratio of interpretation to reporting; where robustness lives |
| `tables` / exhibits | All numbered tables/figures + captions + first text reference to each | Caption self-containment pattern; what lives in notes vs. caption; decimal/significant-digit conventions; figure-vs-table choices; how text references exhibits |
| `policy` framing | Abstract, intro hook, conclusion/policy section | Where policy relevance enters; how findings translate to recommendations; how far claims extend beyond the evidence (usually: not at all — record the restraint pattern) |
| method handling | The empirical strategy section | How assumptions are stated and defended in prose; what is asserted vs. shown; how threats are sequenced; what goes to appendix. Cross-check against the matching upstream gate (`upstream-econ-review/gates/`) — extract how this paper *satisfies* the gate's checks in prose |

**A.2 Map, then parameterize.** For structural tags, first write a short
function map (what job each paragraph/section does), then convert the map into
convention entries. The map itself goes nowhere; only entries survive.

**A.3 Apply the delta rule.** Much of what makes an admired paper good is
baseline (econ-write) practice done well. Extract the delta: what this paper
does that the baseline does not already prescribe, or where the user's
admiration marks an emphasis.

**A.4 Transferability check.** For each candidate entry ask: does this depend
on the exemplar's content, data, or result rather than its craft? "State the
main effect in the first sentence of the abstract" transfers. "Report
precision-driven robustness across 40 specifications" does not transfer to a
paper with n=800 — either drop it or generalize it to the transferable core.
Record dropped-as-untransferable candidates in the provenance log so the user
sees what was considered.

**A.5 Conflict rule.** When two exemplars disagree: prefer the one whose tag
covers the disputed territory; if both cover it, surface the conflict at
playback as a one-line question. Never average two conventions into mush.

## Protocol N — `negative/`: anti-exemplars

Part R gave each file the user's dislikes. Negative preferences are often the
crispest — treat this folder as a first-class source, not an afterthought.

**N.1 Locate the offense.** For each stated dislike, find 1–2 passages in the
file that exemplify it. The quoted fragment goes in Evidence — the user should
recognize exactly what they hate.

**N.2 Parameterize the avoidance.** Convert to a negative convention entry
("Never open a section with literature positioning"; "Never let a table exceed
the page without a panel split") with a check a critic can run. Vague distaste
("it's boring") gets one sharpening pass via the concrete passages: "boring =
three pages before the first number? So: first magnitude on page 1?"

**N.3 Delta rule applies.** If the dislike is something econ-write already
bans (throat-clearing, "delve"), record it as *emphasis* (critic priority
pointer), not a new entry — the baseline ban stands; the user's feeling makes
it high-priority.

**N.4 Do not build a strawman.** Extract only what the user actually dislikes,
not everything imperfect about the file.

## Protocol B — The author's own writing (voice fingerprint)

Input: own papers tagged in `positive/` or named in interview Q7; else the
current draft; else skip. Purpose: `wb-paper-write` drafts in the author's
voice; the Writing Critic distinguishes *defects* from *style* and never flags
the latter.

Read 4–6 dispersed prose pages and record a fingerprint (a dedicated profile
section, not convention entries):

- **Rhythm**: typical and extreme sentence lengths; paragraph length norm.
- **Person and stance**: I/we usage; active/passive ratio; present/past for
  results.
- **Hedging profile**: which hedges they use ("likely", "suggests", "consistent
  with") and how often; whether they hedge conclusions or state them flat.
- **Signature moves**: recurring constructions the author evidently favors
  (colon-led sentences, rhetorical questions, numbered arguments, dry asides).
  Max 4 — these are protected, not enforced.
- **Vocabulary temperature**: plain vs. technical register; any pet words.
- **Weaknesses the author did not ask about — handle with care**: if the same
  mechanical issue recurs (comma splices, dangling modifiers), record it as a
  *candidate* Writing Critic priority and ask at playback: "I noticed X recurs
  in your writing — want the Writing Critic to watch for it?" Never add it
  silently; being corrected on an unasked-for weakness must be opt-in.

The fingerprint states facts about the author's writing, not judgments of it.
Where the fingerprint deviates from econ-write baseline style rules, the
fingerprint wins for this author — record the deviation explicitly
(`overrides baseline`) so the Writing Critic does not "correct" the voice.

## Protocol C — `feedback/`: past referee reports and seminar feedback

This is the highest-signal personalization source: criticism actually received
predicts criticism to come. Part R supplied the context (which paper) and the
author's fairness calls.

**C.1 Strip identity.** Work only with the content of the criticism. Do not
record referee identities or the outlet's decision in the profile.

**C.2 Cluster the criticisms** across all supplied reports into recurring
themes (identification doubts, overclaiming, unclear contribution, exhibit
quality, writing density...). A theme needs ≥ 2 independent occurrences or one
occurrence the author confirms as fair. Confirm the clustering with the author
(interview Q8).

**C.3 For each theme record**: the theme; a paraphrase of the strongest
version of the criticism; what the author did about it (ask if unclear); and a
check derived from it ("verify no claim in the abstract exceeds the estimated
population and horizon").

**C.4 Build the bespoke guide** ("The Referee You Keep Getting") from the top
3–5 themes, ranked by recurrence. Fill both uses: when drafting, avoid
repeating these mistakes; when commenting, look for them before a human
referee does. Where a theme has a matching upstream audit
(`upstream-econ-review/` design/inference/claim audits or a method gate), the
guide points to that protocol as its checking procedure. Offer this guide
when you ask about their old reports, not as a surprise at the end; the
author may find it uncomfortable — that is its value, but it is their call.

**C.5 Fairness routing.** Fair criticism → compliance check (does the draft
now satisfy it). Unfair criticism → *defensibility* check ("ensure the draft
preempts the misreading that leads referees to say X"). Both are valuable;
route per the author's Part R fairness calls.

## Protocol D — `guidelines/`: target-outlet guidelines and internal standards

Part R supplied bindingness (binding vs. aspirational) and scope per file.

Extract **binding, checkable constraints** into the profile's Outlet
constraints section: length/word limits, abstract limits, required sections or
statements (data availability, disclosure, ethics), citation style, exhibit
placement rules, submission format. One entry per constraint with the
guideline as provenance. **Aspirational** guidelines are treated like positive
exemplars: extract style deltas via Protocol A logic, marked aspirational.

Soft advice in guidelines ("write clearly") is ignored — baseline covers
craft. If the target outlet publishes AI-use or disclosure policies, extract them
verbatim into a dedicated entry; `wb-paper-review` surfaces them at every run.
Where guidelines conflict with econ-write baseline (e.g. a required separate
literature-review section), record `overrides baseline` — binding guidelines
outrank baseline and personal preference alike.

## Protocol E — Repo inspection (Stage 1, every route)

Read, if present: memory file (`AGENTS.md`, `CLAUDE.md`, project README), the
current draft, output tables/figures and the code that names them, concept
note / PAP, `wb-paper/` from a previous run. Extract **paper facts** (topic,
method, data, unit of observation, key outcomes, coauthors, formats in use —
LaTeX/Quarto/markdown) and **grounding pointers** (paths to the outputs
directory, the draft, the bibliography). Facts feed the interview's opening
guess; pointers feed both downstream skills (`wb-paper-write` may only take
numbers from these outputs; `wb-paper-review` checks the draft's numbers
against them). Do not interview for anything found here — confirm instead.

**Positioning carve-out**: findings and intended claims stated in a concept
note or PAP are *not* positioning. They seed the positioning questions but
never pre-fill the profile's Positioning section — that section holds only
what the human states in the interview (aitl-protocol § 5).

## Budget and degradation

Per source, extraction should take one focused reading pass. Cap: ~5
convention entries per exemplar tag, 3 per anti-exemplar dislike, 4 signature
moves, 5 referee themes. Caps are ceilings, not quotas: a short excerpt may
honestly support only 1–2 entries — record what the source supports and never
pad to the cap. If a source is unreadable (scanned PDF without text
layer, paywalled link), say so, record it as `not extracted` in the provenance
log, and continue — never guess at a source's content, and never present an
unread source as extracted.
