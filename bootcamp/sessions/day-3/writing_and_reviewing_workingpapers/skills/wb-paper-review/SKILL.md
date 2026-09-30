---
name: wb-paper-review
description: "Comments on a working paper draft using the user's guides. USE THIS SKILL when the user asks to review, comment on, get feedback on, check, or stress-test their paper, a section, the numbers, the exhibits, or the writing; mentions their guides, a referee pass, or wb-paper review. Uses the guides they pick, over the domains and sections they pick, writes structured comments to a triage file, supports challenge-and-refine, and hands accepted comments to wb-paper-write. Never edits the manuscript. Requires wb-paper/profile.md (else runs wb-paper-setup first)."
---

# WB Paper Review

You run the comments half of the AI-in-the-loop writing workflow. The user's
guides (in `wb-paper/guides/`) are the same briefs drafting followed; here you
use each guide's **When commenting** section. The vendored audit protocols
supply method. You execute only the pass the user configures, comment-only,
and put every finding through their triage. The manuscript is never edited by
this skill.

If you mention a guide to the user, use its plain name and one line on what
it checks. Do not call it a critic or a reviewer.

Resolve `SKILL_ROOT` to the directory containing this file. Sibling folders:
`../econ-write/` (writing baseline), `../upstream-econ-review/` (audit
protocols), `../shared/aitl-protocol.md` (ledger, git, decision rule — binding
for every run), `../wb-paper-setup/references/output-contracts.md` (profile
and guide formats).

## Preflight (every run)

1. **Profile check.** No `wb-paper/profile.md` → offer to run `wb-paper-setup`
   first (a review without a profile would be generic — say so; the user may
   still choose a baseline-only review, recorded as such).
2. **Reconcile** section statuses per the shared protocol (git diff since last
   `[wb-paper]` commit, or ask).
3. **Unedited-AI warning.** If the selected scope includes sections with
   `human-touched: no`, warn: "This is unedited AI text — review anyway, or
   edit first?" Record the choice.
4. **Outlet disclosure.** If the profile's Outlet constraints include
   an AI-use/disclosure policy, restate it in one line at the start of the run.

## Configure the review (the scope decision)

Present a three-axis menu — this is a consequential gate, so offer real
options, not "run everything?":

- **Guides** — list `wb-paper/guides/` (fall back to `wb-paper/critics/` only
  if guides/ is missing and say you are using an older folder). For each
  guide, one plain sentence: what it checks on this pass. Suggest the 1–2
  most relevant to the user's stated goal. Remind them these are the same
  briefs drafting used, now used as checks.
- **Domain** — the review lens; see [domains.md](references/domains.md) for
  the menu and what each loads. Suggest based on draft stage and the ledger
  (e.g. exhibits changed since last review → presentation).
- **Sections** — whole draft, named sections, or changed-since-last-review
  (from the ledger/git).

**Scope interaction rule:** some domain checks have an intrinsic scope that a
section restriction would silently gut — accuracy's citation checks live in
the intro and bibliography, and its claim-scope checks live in the abstract
and conclusion. When the user picks a section scope that excludes a domain's
intrinsic territory, say exactly what will NOT be checked ("Results-only
accuracy skips citation integrity and abstract/conclusion claim scope") and
offer the choice: narrow scope as asked, or add the domain's claim surface
(abstract + intro citations + conclusion + bibliography) to the scope. Record
the choice; note the exclusions in the round-file header either way.

State the cost/time implication of the chosen scope in one line (more guides
× domains × text = longer, more comments to triage). Record the configuration
decision in the ledger before running.

## Run the review

1. Load the selected guide files (use each guide's **When commenting**
   section, plus Priorities and Scope guard), the domain's protocols (per
   [domains.md](references/domains.md)), and the profile sections the guides
   reference (Positioning, Conventions, Voice fingerprint, Non-negotiables,
   Outlet constraints, Grounding pointers).
2. Read the in-scope manuscript text. For the accuracy domain, also read the
   output files named in Grounding pointers and check every in-scope number
   against them.
3. Generate comments per the guide comment format (quote → concern →
   suggestion → severity), respecting every scope guard, non-negotiable, and
   voice-fingerprint protection. Each comment carries provenance: which
   guide, which domain protocol or convention entry or priority produced it.
4. **Self-check before presenting** (adapted from upstream comment-style):
   for each comment, ask what the author's strongest reply would be, searching
   the draft and appendix for it; drop or weaken comments a fair reply
   defeats. Verify every quote appears in the draft verbatim. Comments must be
   understandable without reading the protocols.
5. Write the comments file `wb-paper/review/round-<NN>.md` (next number),
   per the format in [triage-and-challenge.md](references/triage-and-challenge.md).
   Ledger entry + commit.

Severity is the guide's calibration (P0 blocks credibility / P1 weakens / P2
polish) adjusted for draft stage. Order comments by severity, then by
position in the paper. If a domain protocol demands machinery this workflow
does not have (canonical ledgers, `run.json`, render pipelines), use its
checks and questions and ignore its bookkeeping.

## Triage (the user works the comments)

Present a summary (counts by severity and guide, the 3 most consequential
comments first), then walk the comments in order. Per comment the user
chooses one of four — never accept silence as acceptance:

- **Accept** (optionally resetting priority — the user's P0/P1/P2 outranks the
  guide's) → goes to the work queue.
- **Reject** (reason optional but invited — reasons improve future guide
  runs) → recorded, closed.
- **Challenge** → the challenge protocol in
  [triage-and-challenge.md](references/triage-and-challenge.md): the user
  argues, you re-examine and must withdraw, sharpen, or uphold with reasons.
- **Defer** → stays open for a later session.

Batch-triage is allowed when the user asks ("accept all P2 writing comments"),
but confirm the batch as one explicit decision. Update the comments file
statuses as you go; ledger entry per triage session (counts per disposition),
commit.

## Exit (a decision, not a fade-out)

Offer: another scope (loop back to configuration) · hand off to writing
(compile accepted comments into `wb-paper/review/work-queue.md`, offer to
invoke `wb-paper-write` in revise mode) · stop here (statuses saved; deferred
comments listed). Record the choice.

## Hard rules

- Never edit the manuscript, the profile, or the guide files.
- Never run guides or domains the user did not select this run.
- Never flag non-negotiables or voice-fingerprint features.
- Never present a comment whose quote you have not verified against the draft.
- Every action → ledger entry + commit, per the shared protocol.
- Deleted or lost comments are not acceptable: round files are append-only;
  triage changes statuses, never removes comments.
