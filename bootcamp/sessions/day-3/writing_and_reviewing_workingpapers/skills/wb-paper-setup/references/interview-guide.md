# Interview Guide

How to run the setup interview. The interview captures what cannot be read
from files: the author's intent, taste, fears, and non-negotiables. It has two
parts: **Part R** (about the user's reference materials — always runs) and
**Part 2** (depth questions — differentiated by route).

## How you talk to the user

The user does not know this skill. Talk as if they have never seen it.

**Opening comes after you have looked at the repo and they have chosen draft
or comments.** Do not open with the interview. First message shape:

> I looked through the project. <One sentence: draft or not, tables or not.>
>
> Two things you can do with this:
> - **Draft** — write or revise a section from your tables and notes. You choose what to keep.
> - **Comments** — read a draft and suggest changes. You accept, reject, or argue with each one.
>
> Which do you want? <If there is no draft: "Comments need a draft, so drafting is the place to start.">

After they choose, explain the shared setup before the first interview question. This is where **guides** are defined. Do not use the word earlier.

> Either way starts the same. I'll ask a few questions and write a short profile plus a few **guides**.
>
> A guide is a brief for one part of the paper — methods, policy, or the writing. It is not a person.
> - When we **draft**, I follow the guides (what to say first, what never to claim, whose taste to match).
> - When we **comment**, I check the draft against the same guides.
>
> I'll ask about examples you want to imitate or avoid, then what this paper is claiming. Nothing is saved until you say so. You can say "skip". About <route time>.

If they say they only want to draft: "The guides are what the draft follows. You don't have to run comments afterwards."

Then create the reference folders if needed and, as its own message, ask them to drop files — explain the four folders in plain words (papers you admire, writing you dislike, rules for the target outlet (a journal, a working-paper series), old referee reports). Empty is fine.

**One question per message.** Never a numbered list of questions. A guess
plus "right?" counts as the one question. After they answer, one sentence
acknowledging it, then the next question. One follow-up only when the answer
cannot be used as written; otherwise move on.

**Say why, in one line, when the step changes** — not before every question
of the same kind. Examples:

- Starting the examples: "Next, the papers you saved. What you like and dislike becomes the guides, so the draft and any later comments follow your taste instead of a generic checklist."
- Starting the claim questions: "Next, what this paper is actually saying — I'll use your words, not mine. The methods guide checks that the draft doesn't claim more than this."
- Offering a set of guides: name each guide and say both uses in one line ("Methods: when drafting, state the result and the assumption up front; when commenting, check that the design actually supports the sentence.").
- Before the summary: "Here's what I heard. Nothing is saved yet."

**Words you do not use with the user:** Part R, Part 2, playback, protocol,
positioning block, delta, stage numbers, critic, reviewer, roster, scope
guard. Say "the examples you saved", "what the paper claims", "the summary",
"guides". A past referee report may be called a referee report — that is
their document, not your role.

**Other rules**

- State the default in brackets. "Skip" and "use defaults for the rest" are
  always valid; record used defaults as `(default)` in the profile.
- Never ask what the repo already answered. Open with a guess:
  "This looks like a DiD paper on X using Y data, for a Policy Research
  Working Paper — right?"
- The claim questions are the exception: always ask them in the user's words,
  even if a concept note states findings. The note may seed the question; it
  never fills the profile.
- Keep their phrasing. Do not translate "I hate padded intros" into "concision
  preference: high."
- Do not dump leftover questions at the summary. Ask each when it comes up.
  The summary confirms what you inferred; it does not introduce a new questionnaire.

## Part R — The reference materials (always runs)

These names are for you. Do not say "Part R" to the user.

Walk the four folders in this order, **one file, one question, then stop and
wait.** Skip an empty folder with one line ("No journal guidelines in the
folder — I'll use Policy Research Working Paper defaults unless you say
otherwise") and move to the next question. If a folder has several files, still
one file per message.

### R1. `positive/` — for each file:
- **Identify + confirm**: "This is <best guess of what it is> — correct?"
- **The tag question (critical)**: "What is this one great *for* — intro
  structure, tone, results narration, tables, policy framing, method
  handling — and what specifically do you admire about it?" One tag minimum
  per file; the tag scopes extraction (Protocol A).
- If the user says "everything": propose the two tags the paper is best known
  for and confirm.
- If a positive file is the *user's own* prior writing, ask whether it should
  also serve as a voice source (Protocol B) — own papers usually should.

### R2. `negative/` — for each file:
- **The dislike question**: "What specifically puts you off here — structure,
  tone, density, overclaiming, exhibit style?" Push once for the operational
  version: "so the rule is 'never <X>' — right?"
- Negative answers often produce the crispest conventions; give this folder
  real attention, not a courtesy pass.

### R3. `guidelines/` — for each file:
- **Bindingness**: "Is this the binding target (hard constraints) or
  aspirational (style to lean toward)?"
- **Scope**: which parts apply — length limits, structure, citation style,
  disclosure requirements?
- If multiple guidelines conflict, ask which wins.

### R4. `feedback/` — for each file (or the set):
- **Confirm context**: "These are reports on <this paper / a previous paper> —
  correct?"
- **The fairness question**: "Looking back, which of these criticisms were
  fair, and which were misreadings?" (Fair → check compliance; unfair → check
  defensibility. See Protocol C.)
- **Offer the bespoke guide** (its own message, after the fairness answer).
  Explain both uses: "I can add a guide called 'The Referee You Keep Getting,'
  built from the comments that were fair. When drafting, it keeps the new
  text from repeating those mistakes. When commenting, it looks for them
  again. Want that?"

Part R output: a per-file record of {identification, tags/likes/dislikes,
bindingness, fairness calls} that Stage 5 extraction consumes.

## Part 2 — Depth questions (route-differentiated)

### Quick route (every route asks these)

1. **Target outlet.** Where is this paper going? A journal, a working-paper
   series, an internal report. [default: World Bank Policy Research Working Paper]

2. **What the paper claims** — the intellectual core. This is **direct human
   input** (see shared/aitl-protocol.md § 5): record the user's words
   verbatim; never supply generated candidates for missing answers. Ask these
   as four separate messages, each one sentence, in this order:
   - **a. Main finding.** What is the headline result, with magnitude if
     known? ("X raises Y by about Z%.")
   - **b. Contribution + type.** What is new here, and new *to what* — method,
     evidence base, theory, practice, or policy? Multiple types allowed;
     ask for a ranking if more than one.
   - **c. Relevance.** Who should care, and why now — in one sentence?
   - **d. Claim sentence.** Finish: "This paper is the first to / the best
     evidence that ..."

   If a concept note or PAP states findings or intended claims, use it to
   seed the question ("your concept note says attendance rose 4.2 pp — state
   your main finding in your own words"), but always ask — documents never
   substitute for the human's answer.

   Every element accepts "not settled yet" — record the unsettled state; it
   becomes a top guide priority (an unclear contribution is the most common
   fatal review outcome) and `wb-paper-write` will re-ask before drafting any
   section that needs it. After the human answers, **offer sharpening once
   for the whole block** ("want me to suggest tightened versions of any of
   these?") rather than pushing two variants per element — sharpening all
   four by default doubles the interview for marginal gain. Canonical text is
   whatever the human confirms; the profile records the origin.

3. **Feedback priorities.** Two separate questions. What do you most *want*
   feedback on? Then: what do you most *fear* a smart reader would say?
   [default: want = framing of contribution; fear = identification challenge]

The fear answer is the single highest-value personalization input: it becomes
the top-ranked priority of the matching guide.

### Standard route (adds)

4. **Audience.** Who must this paper convince — a journal referee, a policy
   counterpart, an operations team, your manager? Who is the *secondary*
   reader? [default: PRWP audience — technical reviewers + policy readers]
5. **Non-negotiables.** Anything the AI must never touch or change? (e.g. "my
   intro's opening paragraph stays as I wrote it", "we, never I", "British
   spelling") [default: none]
6. **Stage + horizon.** How far along is the draft, and what is the next
   deadline or milestone? (Calibrates how strict the guides are: a concept-stage
   draft should not be scored like a submission.) [default: early draft, no
   deadline]

### Deep route (adds)

7. **Voice sources.** Beyond anything already tagged in `positive/`: which
   1–2 pieces of your own writing best represent your voice at its best?
   [default: the current draft, if one exists]
8. **Recurring-criticism confirmation.** (After Protocol C clustering.) "Across
   your feedback files, the recurring themes look like <themes> — does that
   match your experience? Anything missing?"
9. **Anti-exemplar articulation.** If `negative/` was empty: is there a paper
   or style you actively dislike, and why? Negative space is often easier to
   articulate than positive preferences. [default: none]
10. **Coauthors.** Are there coauthors whose preferences bind? Voice
    conventions agreed? Who is voice editor? [default: sole-authored / user
    decides]

## Handling answer quality

- **Vague answer** ("I want it to be good"): offer 3 concrete options drawn
  from the repo inspection or materials ("good = tighter prose / stronger
  identification narrative / clearer policy relevance?") — once. Then record
  the best available version.
- **Contradiction** (wants "short punchy intro", positive exemplar has a
  6-page intro): surface it in one sentence at playback, propose a resolution,
  let the user decide. Interview answers outrank extractions.
- **Overload** (user pastes ten preferences): record all, but ask them to star
  the top three; guides rank by the stars.

## What the interview feeds

| Answer | Profile section | Critic effect |
|---|---|---|
| R1 tags/likes | Conventions (via Protocol A) | Checkable convention entries |
| R2 dislikes | Conventions, negative entries (Protocol N) | "Never do X" checks |
| R3 bindingness | Outlet constraints (via Protocol D) | Hard checks (limits, required sections) |
| R4 fairness calls | Feedback priorities (via Protocol C) | Bespoke guide "The Referee You Keep Getting" |
| 1 target outlet | Paper facts | Guide strictness + how the outlet is framed |
| 2 positioning block | Positioning (human-authored) | Methodologist checks every section serves it; unsettled elements become top priorities |
| 3 want/fear | Feedback priorities | Top-ranked priority of matching guide |
| 4 audience | Audience | Policy Reviewer calibration |
| 5 non-negotiables | Non-negotiables | Scope guards — guides must not flag these |
| 6 stage | Paper facts | Severity calibration in every guide |
| 7 voice sources | Voice fingerprint (via Protocol B) | Writing Critic protects, not polices, the voice |
| 8 criticism themes | Feedback priorities | Bespoke guide priorities |
| 9 anti-exemplar | Conventions (negative entries) | "Never do X" checks |
| 10 coauthors | Paper facts + non-negotiables | Voice consistency checks |
