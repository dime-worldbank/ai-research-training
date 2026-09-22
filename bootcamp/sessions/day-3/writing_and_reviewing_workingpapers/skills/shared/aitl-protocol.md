# AI-in-the-Loop Protocol

Shared contract for `wb-paper-setup`, `wb-paper-review`, and `wb-paper-write`.
Every skill in this suite follows these rules without exception. Together they
guarantee: the human defines the standard, initiates every action, finalizes
every artifact, and can prove the division of labor afterwards.

## 1. The decision rule: decisions, not approvals

At every consequential gate, present **at least two genuine, labeled options**
(plus "other — tell me") and make the user choose. Never reduce a
consequential gate to a yes/no approval — approvals invite rubber-stamping;
choices force engagement.

Consequential gates include: which guides to keep, outline and writing
order, comment scope (guides × domain × sections), prose variants for key
passages, triage of every review comment, challenge outcomes, and revision
acceptance. Trivial mechanics (file naming, folder creation) are not gates —
do not pester.

Every decision is recorded in the ledger: the options offered, the option
chosen, and any user modification. "User chose neither and wrote their own"
is the best possible outcome — record it as such.

## 2. The ledger: `wb-paper/log.md`

Append-only. Every AI action and every human decision gets one entry, written
by the acting skill **immediately after** the action — never batched to the
end of a session. Two parts:

### Section status table (kept at the top, updated in place)

```markdown
| Section | Status | Last AI action | Human-touched |
|---|---|---|---|
| Introduction | ai-draft | 2026-10-07 draft v1 (wb-paper-write) | no |
| Results | human-edited | 2026-10-07 revise C-03 | yes |
| Data | human-only | — | yes |
```

Status values: `human-only` (no AI text), `ai-outline`, `ai-bullets`,
`ai-draft`, `human-edited` (AI text since revised by the human), `mixed`.
`Human-touched: no` means no human has substantively edited AI-produced text
in that section yet.

### Entries (append-only)

```markdown
### <date time> · <skill> · <action> · <scope>
- Inputs: <files/profile sections/comments used>
- Options offered: <A: ... | B: ...> → Human chose: <A / B / own: "...">
- Output: <what was produced, path> (committed with this entry)
- Human decision: <verbatim or close paraphrase>
- Section status after: <status>, human-touched: <yes/no>
```

An entry never contains its own commit hash — it cannot know it. The commit
containing the entry *is* its identifier: `git log -- wb-paper/log.md` maps
entries to hashes. Only *references to earlier work* (e.g. a revise entry
citing the draft it modifies, a comment status update) cite explicit hashes.

Action vocabulary (keep to these so the ledger stays greppable): `setup`,
`interview`, `extract`, `outline`, `clarify`, `draft`, `revise`, `rewrite`,
`review`, `triage`, `challenge`, `handoff`, `reconcile`, `disclose`.

## 3. Git convention

Check once per run whether the project is a git repository. If yes:

- **One AI action = one commit.** Never mix AI-produced changes and human
  edits in a single commit.
- **Before acting**: if the working tree has uncommitted changes to files the
  action will touch, stop and ask the user to commit or stash them first
  (offer to make that human commit for them, clearly labeled as their work).
- **Commit message shape**:

  ```
  [wb-paper] <skill>: <action> (<scope>)

  AI-Assisted: <skill name>
  AI-Action: <action> <scope>
  AI-Inputs: <key inputs>
  Human-Decision: <chosen option / instruction>
  ```

- Commit the ledger update **in the same commit** as the action it records,
  so history and ledger can never drift apart.
- If not a git repo: ledger only, and once per project suggest `git init`
  (the diff-based review of AI changes is lost without it — say so).

## 4. Human-touched reconciliation (run start, every skill)

At the start of every run, reconcile the section status table with reality:

- **With git**: diff the manuscript since the last `[wb-paper]` commit. Any
  changes not made by a wb-paper commit are human edits → update the affected
  sections to `human-edited`, `human-touched: yes`, and append a `reconcile`
  entry crediting the human.
- **Without git**: ask which sections the user has edited since last time.

`wb-paper-review` must warn before reviewing any section with
`human-touched: no`: "This section is unedited AI text — review it anyway, or
edit it first?" AI text that no human has touched must never sail through
review just because it looks finished.

## 5. Critical human input: the positioning core

The paper's intellectual core is **direct human input, never AI-invented**:

- the main finding (one sentence),
- the contribution claim and its type(s) (method / evidence / theory /
  practice / policy),
- the relevance sentence (who should care and why now),
- the intro's thesis/hook *content* (the idea, not the polish).

These live in the profile's Positioning section, marked human-authored. Rules:

- If a positioning element is missing or unsettled when a skill needs it:
  **ask the human to state it** (an ugly, unpolished version is fine). Never
  fill the gap with a generated candidate.
- AI may **sharpen** a human-stated element: offer 2 polished variants beside
  the human's original; the human picks or edits; the ledger records origin
  (`human seed + AI sharpening, human chose B with edits`).
- AI may draft *any* section, including sections containing these elements —
  but the elements themselves are inserted from the human-authored Positioning
  text (or a fresh human seed), and the surrounding draft is offered with
  variants at the key passages.

## 6. Disclosure generation

On request ("generate my AI disclosure"), produce a submission-ready
disclosure statement **from the ledger**: which sections had AI drafting or
revision, what kinds of assistance (drafting, editing, review comments,
exhibit checks), and the verification the human performed (triage counts,
human-edited statuses). Cross-check against the target outlet's disclosure
policy in the profile's Outlet constraints. The ledger is the source of truth — if the
ledger can't support a claim ("all AI text was human-reviewed"), the
disclosure must not make it, and the gap should be reported to the user.

## 7. Failure honesty

If a skill skips any part of this protocol (no git, ledger write failed, a
gate was collapsed to yes/no by user request), it says so in chat and records
the deviation in the ledger. Silent deviations are the one unforgivable bug in
an audit-trail system.
