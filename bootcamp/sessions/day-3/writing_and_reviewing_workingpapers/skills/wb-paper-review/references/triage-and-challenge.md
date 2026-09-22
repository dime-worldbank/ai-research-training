# Triage and Challenge

The comments file format, the comment lifecycle, and the challenge protocol.

## Comments file: `wb-paper/review/round-<NN>.md`

Header block:

```markdown
# Review round <NN> — <date>
- Scope: critics <list> · domain <list> · sections <list>
- Draft state: <commit hash or "no git">; unedited-AI sections in scope: <list or none>
- Comments: <N> (P0: n / P1: n / P2: n)
```

Each comment:

```markdown
### C-<NN> · <Critic> · <domain> · <section/location> · <severity>
**Quote**: "<verbatim manuscript text>" — or, for checked comparisons:
Basis: <e.g. "text §4.2 says 0.34; outputs/tab2_main.tex col 2 says 0.29">
**Concern**: <why this matters for THIS paper — reference the positioning
element, convention, gate check, or critic priority that makes it matter>
**Suggestion**: <smallest adequate fix; claim narrowing is a valid fix>
**Provenance**: <critic priority #n / convention short-name / protocol § >
**Status**: open
```

Statuses and the lifecycle:

```
open ──► accepted (P0/P1/P2, user's priority) ──► queued ──► implemented
   │──► rejected (+ optional reason)
   │──► challenged ──► withdrawn | sharpened | upheld ──► (user then accepts/rejects)
   └──► deferred (stays open for a later session)
```

Rules: round files are append-only — triage updates the `Status:` line (and
appends the triage note under the comment), never deletes a comment. The
user's triage priority overrides the critic's severity from acceptance onward.
`accepted → queued` happens at handoff, when the comment is written into
`work-queue.md` (accepting alone does not queue); `queued → implemented` when
the user accepts the revision diff, recording the revision's commit hash.

Commit granularity: one triage session = one commit (all status updates and
challenge dialogues from that sitting), per the one-action-one-commit rule —
a challenge is part of the triage action, not a separate one. Multiple review
runs before any triage are allowed (each run = its own round file and commit);
when triage starts with several untriaged rounds open, ask whether to triage
them together or per round — a decision, recorded.

## The challenge protocol

The user disputes a comment; the reviewer must engage with the objection —
this is the dialogic gate that keeps the human the epistemic owner.

1. **The user states the objection** in their own words ("the parallel-trends
   figure is in appendix C", "that's my voice, not a defect", "the referee
   misread this last time too").
2. **Re-examine against evidence only.** Search the draft, appendix, exhibits,
   and profile for what the objection points to. No new sweep, no new
   comments, no doubling down by restating the original wording louder.
3. **Rule, with reasons**, one of:
   - **Withdrawn** — the objection defeats the concern (evidence found,
     comment misread the text, scope guard violated). Status → withdrawn;
     record what was missed. A withdrawal is a good outcome, not a failure —
     never resist it to save face.
   - **Sharpened** — the objection partially lands: restate the concern
     narrower, with better evidence, possibly lower severity. Status →
     sharpened; the user then accepts/rejects the sharpened version.
   - **Upheld** — the objection does not defeat the concern: explain
     specifically why (what the appendix figure does not cover, why the
     misread is likely for other readers too). The user still decides —
     upheld comments can be rejected; record `upheld-then-rejected` honestly.
4. **One round by default.** The user may iterate, but suggest settling
   repeat-challenges by a targeted fix ("add one clarifying sentence and
   re-run this check") rather than argument loops.
5. **Everything on the record.** The challenge dialogue (objection, ruling,
   reasons) is appended under the comment in the round file; the ledger entry
   for the triage session counts challenges by outcome.

Challenge outcomes feed learning: at session end, if ≥2 comments from one
critic were withdrawn for the same reason, propose (as a decision) an edit to
that critic's scope guard or priorities — the user's challenges are how
critics get better.

## The work queue: `wb-paper/review/work-queue.md`

Created/updated at handoff. Accepted comments only, ordered by the user's
priority then paper order:

```markdown
# Work queue — updated <date>
## P0
- [ ] C-03 (round 02) · Results §4.2 · <one-line instruction distilled from
      the suggestion + any user instruction added at triage>
## P1
...
```

Each item carries its comment ID so `wb-paper-write` (revise mode) can read
the full comment, implement the smallest adequate change, and update the
status to `implemented` (with commit hash) when the user accepts the revision.
The queue is the contract between review and write: nothing enters it without
an explicit user acceptance, and nothing in it gets implemented without the
user seeing the diff.
