# Guide: Methods
<!-- Stock guide. wb-paper-setup copies this into wb-paper/guides/ and
     personalizes Priorities, Conventions, Scope guard, and Severity
     calibration. Adapted from econ-writing-skill (MIT, Lu Han). -->

## What this guide is
The methods brief: what the paper is allowed to claim, given how it was
estimated. Used when drafting those sentences and when checking them later.

## When drafting
State the design, the main assumption, and the result in plain language before
the equations. Do not call a non-random rollout quasi-random. Do not put a
number in the text that is not in the output files.

## When commenting
Check that the design supports the claim. Leave prose style and policy
framing to the other guides.

## Mandate
What exactly is being claimed, and does the design and evidence support that
claim — no more, no less. Identification, inference, and the match between
what was estimated and what is asserted. Not whether the prose sparkles.

## Scope guard
Do not cover: writing style, word choice, or exhibit cosmetics (Writing
guide); policy framing and audience fit (Policy guide); anything listed in
the profile's Non-negotiables.
<!-- setup adds: roster-specific and profile-specific exclusions -->

## Priorities (ranked)
<!-- setup replaces with personalized ranking; the author's stated fear goes
     first when it is methodological. Stock default: -->
1. The positioning core (profile › Positioning): is the contribution stated,
   singular, and supported end-to-end; does the paper deliver the claimed main
   finding; does the text's framing match the claimed contribution type(s)?
2. Identification: is the key assumption stated, defended in economic terms,
   and are the main threats (selection, reverse causality, omitted variables)
   addressed?
3. Claim–evidence match: does every claim in the abstract, intro, and
   conclusion stay within the estimated population, magnitude, and horizon?
4. Numbers integrity: does every number in the text match the project's output
   tables (see profile Grounding pointers)? Flag any number with no source.
5. Inference: standard errors and clustering appropriate and stated; nulls
   framed as informative with precision discussed, not as absence of findings.
6. Robustness proportionality: checks cover the fragile assumptions, not just
   the easy ones.

## Baseline to enforce
- econ-write › Empirical Work Rules (identification, results presentation,
  null results, common mistakes, standard errors and inference)
- econ-write › Modern Empirical Practices (pre-registration, multiple testing,
  citation integrity)
- econ-write › identification-strategies.md — the section matching this
  paper's method (from profile Paper facts)
- upstream-econ-review › design-audit.md, inference-audit.md,
  reader-claim-audit.md; the matching gate in gates/ (did/iv/rdd) if the
  paper's method has one

## Conventions to enforce
<!-- setup lists the profile convention entries tagged `method` or `results`
     that belong to this critic; `overrides baseline` entries outrank the
     baseline list -->

## Severity calibration
<!-- setup sets from draft stage. Stock default: -->
Concept/early draft: comment only on priorities 1–3; P0/P1 only.
Full draft: all priorities.
Pre-submission: all priorities, and re-run priority 4 exhaustively.

## Comment format
**Quote** the passage (or state the checked comparison, e.g. "text says 0.34;
table 3 column 2 says 0.29") → **Concern**: why this matters for this paper's
contribution claim → **Suggestion**: the smallest change that fixes it (a
narrower claim is a valid fix; do not demand new analysis when claim narrowing
suffices) → **Severity**: P0 blocks credibility / P1 weakens the paper / P2
polish. Never edit the manuscript.
