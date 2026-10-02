# Guide: Writing
<!-- Stock guide. wb-paper-setup copies this into wb-paper/guides/ and
     personalizes Priorities, Conventions, Scope guard, and Severity
     calibration. Adapted from econ-writing-skill (MIT, Lu Han). -->

## What this guide is
The prose brief: order, concreteness, and the author's own voice. Used while
drafting every section and when commenting on wording later.

## When drafting
Put the main result early. Cut throat-clearing. Match the voice fingerprint.
Do not "correct" a signature move of the author's into generic prose.

## When commenting
Flag padding, buried leads, and machine-flavored wording. Do not treat the
voice fingerprint as a defect. Leave methods and policy framing alone.

## Mandate
Every section does its job in the fewest words, the most important thing comes
first, and the prose gets out of the argument's way. The author's voice is
style, not error.

## Scope guard
Do not cover: the substance of claims, methods, or numbers (Methods guide);
policy framing and audience strategy (Policy guide); any feature listed in
the profile's Voice fingerprint signature moves; anything in Non-negotiables.
Never flag a voice-fingerprint feature as a defect.
<!-- setup adds: roster-specific and profile-specific exclusions, plus any
     opt-in recurring-weakness watch from Protocol B -->

## Priorities (ranked)
<!-- setup replaces with personalized ranking; extraction-derived structure
     conventions usually go first. Stock default: -->
1. Lead placement: main result stated concretely (with magnitude) early in the
   abstract and within the first three paragraphs of the introduction.
2. Throat-clearing and padding: openings that delay the point ("It is
   important to note", "The literature has long..."), sentences that add no
   information, repetition across abstract/intro/conclusion beyond the
   deliberate.
3. Concreteness: findings stated as findings ("a 10% increase in X lowers Y by
   3%"), not as activities ("we examine the relationship between X and Y").
4. Exhibit self-containment: tables and figures readable alone — caption,
   units, sample, and estimation note present; text references exhibits by
   what they show, not just by number.
5. Structural conventions from the profile (paragraph-function map of the
   intro, section ordering, length shares).
6. AI-flavored patterns: uniform sentence lengths, banned-word clusters
   ("delve", "crucial", "landscape", "furthermore", "robust" outside
   statistics), perfectly parallel lists, hedging that is uniform rather than
   calibrated. These matter double when parts of the draft were AI-assisted.

## Baseline to enforce
- econ-write › Core Principles, Writing Style Rules (phrases to delete, word
  choice, voice, paragraphs)
- econ-write › Avoiding AI-Generated Writing Patterns (banned words, sentence
  rhythm, structural tells) + review-checklist.md › Anti-AI Detection Checklist
- econ-write › section formulas (Abstract, Introduction, Conclusion) and
  Tables and Figures
- upstream-econ-review › table-audit.md, figure-audit.md, comment-style.md

## Conventions to enforce
<!-- setup lists the profile convention entries tagged `structure`, `tone`,
     or `tables` that belong to this critic; `overrides baseline` entries —
     including voice-fingerprint deviations — outrank the baseline list -->

## Severity calibration
<!-- setup sets from draft stage. Stock default: -->
Concept/early draft: priorities 1–3 only, P0/P1 only — never polish prose that
may be rewritten.
Full draft: priorities 1–5.
Pre-submission: all priorities, including a full pass for priority 6.

## Comment format
**Quote** the passage → **Concern**: what it costs the reader (time, clarity,
trust) → **Suggestion**: show the fix pattern; you may include one rewritten
example sentence, clearly marked as an example, but never rewrite passages
wholesale → **Severity**: P0 blocks credibility / P1 weakens the paper / P2
polish. Never edit the manuscript.
