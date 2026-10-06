# AI Adoption Guide

Reference material for writing `AI-ADOPTION-PLAN.md`. Keep this file next to the plan in the root of your project folder. Read it yourself, or ask your coding agent to walk you through it.

The plan answers two questions:

1. **What could AI do for me, and do I want it to?** Plan sections 2–4, one per A of the 3A model: Activities, Actors, Artefacts.
2. **What do I need to do, and what is in the way?** Plan sections 5 and 6.

| If you are working on… | Look at |
|---|---|
| Plan section 1: take stock | [Setup checklist](#setup-checklist) |
| Plan sections 2–4: Activities, Actors, Artefacts | [The 3A design model](#the-3a-design-model), [A 3A matrix, step by step](#a-3a-matrix-step-by-step), [Three workflows, redesigned](#three-workflows-redesigned), [An AI data map](#an-ai-data-map) |
| Plan section 3: team access | [Team access](#team-access) |
| Plan section 4: data preparation and rules | [Confidential data](#confidential-data), [Data rules for the memory file](#data-rules-for-the-memory-file) |
| Plan section 5: targets | [Example targets](#example-targets), [Skills](#skills) |
| Plan section 6: roadblocks | [Confidential data](#confidential-data), [Risks and mitigations](#risks-and-mitigations) |
| Plan section 7 (optional): full 3A matrix | [A 3A matrix, step by step](#a-3a-matrix-step-by-step), [Three workflows, redesigned](#three-workflows-redesigned) |

---

## Instructions for the agent

If a user asks you to walk them through their AI adoption plan, follow these rules.

- **Never open data files.** Do not read anything in data folders (for example `data/`, `raw/`, `identified/`), or any `.dta`, `.csv`, `.xlsx`, `.parquet` or `.sav` file. Work from `README.md`, the memory file (`AGENTS.md` / `CLAUDE.md`), code and the folder structure only.
- **Go one plan section at a time**, in order. Before each section, explain in two or three sentences what it is for, using the matching part of this guide.
- **Ask, then draft.** Ask the user short questions, offer options, and draft text for them to edit. Do not fill in judgment calls on your own: whether they *want* AI in a task, their targets, their roadblocks, and data classifications are theirs to decide. Mark anything you guessed with `TODO`.
- **Section 2 (Activities):** help the user list recurring tasks, their main steps, and what starts each one. Most tasks start with someone asking, in a chat or by email; that is fine. Ask whether they want AI involved, and record where they do not.
- **Section 3 (Actors):** for each task they want AI in, propose which steps could happen without them and which need their judgment, and say why. The user decides.
- **Section 4 (Artefacts):** for each task, ask what the tool would see and what it should hand back, and who checks it. Ask the user for the classification; do not guess it. If identified data would be needed, add it to the data preparation table.
- **Section 5:** push for targets the user can report on in six weeks. "Use AI more" is not a target. "Every change to the cleaning code gets an AI review before merge" is.
- **Section 6:** ask what worries them, including vague worries. For each roadblock, ask whether they can resolve it themselves, with help, or not at all, and who could help. Do not talk a worry away.
- **Section 7 is optional.** Offer the full 3A matrix once sections 2–6 are drafted. It often takes longer than the session, so it is fine to leave it with `TODO`s to finish later.
- **Keep to time.** The bootcamp session gives 30 minutes: about 5 for section 1, 12 for sections 2–4, 10 for sections 5 and 6, and 3 to commit.

---

## Q1 · What could AI do for me?

Start from work you already do, not from a tool. Good candidates are:

- **recurring**: every month, every survey round, every mission
- **the same steps** each time
- **checkable**: the output can be checked in minutes
- **shareable**: the data involved may be shared with the tool

Keep for yourself: judgment calls, relationships with counterparts, and sign-off. Deciding that AI does not belong in a task is a valid answer.

### The 3A design model

Use it as a thinking aid first: three questions to ask of any task. Plan sections 2–4 take one A each. Mapping a whole workflow as a matrix (plan section 7) is optional and takes longer.

Most AI use today is a chat window next to a workflow that stays the same. The 3A design model starts from the workflow instead, and splits it into stages. For each stage, describe three things:

| | Question | What to write |
|---|---|---|
| **Activities** | What happens, in what order? | 5–7 stages, each a verb: pull, check, decide, draft, sign off. Add what starts each one (you asking, a request, a file arriving, a date) and what is true once it is done. |
| **Actors** | Who does each stage? | You, colleagues, counterparts, or an agent. Mark each stage *I'm in it* or *happens without me*. |
| **Artefacts** | What goes in, what comes out? | The tools and data each stage uses (with their classification), and the output it hands to the next stage. |

**Agent in the loop:** the workflow is built around handoffs. The agent owns whole stages; you own the decisions between them. To redesign a workflow, ask three questions of each stage:

1. **Does this stage need my judgment?** No: it can happen without you. Yes: keep it, but let the agent prepare it.
2. **What does the agent hand back?** An artefact you can check in minutes: a memo, a diff, a flag list. No artefact, no handoff.
3. **What starts it?** You asking in a chat, a request from a colleague, a file arriving, a date. Most stages start with someone asking; name who and when, so the handoff is clear.

### A 3A matrix, step by step

Example: a ministry asks for school attendance figures by district and gender.

| | 1 Request arrives | 2 Scope it | 3 Disclosure check | 4 Produce tables | 5 Package & document | 6 Clear & send |
|---|---|---|---|---|---|---|
| **Activity** | Ministry asks for attendance by district and gender | Agree indicators, years, breakdowns, deadline | Check the spec against the data-sharing agreement | Agent writes the code; I review code and numbers | Format tables, write notes on definitions and sample | TTL clears the reply and sends it |
| **When** | Email, any day | 15-minute call | Once the spec is agreed | Same day | When I ask, after my review | Email, async |
| **Outcome** | Request on our desk | Everyone wants the same table | Small cells and identifiers flagged | Numbers I'd stand behind | Readable without us in the room | Request answered and logged |
| **My role** | Without me | I'm in it | Without me | I'm in it | Without me | Without me |
| **Who** | Ministry, TTL | Me, Ministry | Agent | Me, agent | Agent | TTL |
| **Tools in** | Email | Call, notes | Agent, data agreement | Agent, clean data, Git | Agent, table template | Email, request log |
| **Output** | Request email | Request spec | Disclosure memo | Tables, code | Excel file, data note | Sent reply, log entry |

I am only in stages 2 and 4. The agent runs stages 3 and 5 on its own, and every agent stage ends in something someone can check.

### Three workflows, redesigned

**Monthly welfare nowcast.** Updating poverty projections for one country, every month, with the same code. You keep the two judgment calls: which data to trust, and what the new numbers mean.

| Stage | When | My role | Who | Output |
|---|---|---|---|---|
| 1 Pull new data: latest CPI, GDP projections, remittances, exchange rates, saved with source and date | 1st working day, I ask | Without me | Agent | Data vintage, source log |
| 2 Check what changed: revisions, gaps, unit or base-year changes; flagged, never fixed | Same session, right after | Without me | Agent | "What changed" memo |
| 3 Decide assumptions: accept, override, or ask the statistics office; agent records each decision and reason | Same day, 30 min | I'm in it | Me, agent | Assumptions file (committed) |
| 4 Run the projection: microsimulation on the latest household survey; decompose the change since last month | Once I commit the assumptions | Without me | Agent | Tables, decomposition |
| 5 Interpret & draft: check the numbers make sense; agent drafts the one-page note, I rewrite | Next day | I'm in it | Me, agent | Draft note |
| 6 Clear & publish: peer review and clearance; numbers go to the country dashboard | Email, async | Without me | Peer reviewer, manager | Cleared note, dashboard |

**Stakeholder results presentation.** Presenting midline evaluation results at a Ministry of Education workshop. The agent does the assembly and the checking; you own the conversation with the counterpart, and the messages.

| Stage | When | My role | Who | Output |
|---|---|---|---|---|
| 1 Agree the brief: audience, time slot, the three questions the Ministry wants answered | Call, 3 weeks out | I'm in it | Me, TTL, Ministry | One-page brief |
| 2 Map the evidence: match each question to tables and figures in the results repo; list gaps | Once the brief is agreed | Without me | Agent | Evidence map |
| 3 Write the storyline: agent proposes messages; I rewrite them and choose the exhibits | 1 hour | I'm in it | Me, agent | Storyline |
| 4 Build the deck: slides from the template, plain chart labels, speaker notes, handout | When I ask; runs while I do other work | Without me | Agent | Draft deck, handout |
| 5 Check every claim: every number against the results tables; flag claims stronger than the evidence | Right after stage 4 | Without me | Agent | Check report |
| 6 Rehearse & finalise: fix flags, dry run with the TTL, practise likely questions | Week before | I'm in it | Me, TTL, agent | Final deck, Q&A sheet |

**Cleaning a survey round.** Weekly batches from a phone survey, run by a survey firm. The agent never touches raw data and never decides what counts as an error. It finds, records and rebuilds.

| Stage | When | My role | Who | Output |
|---|---|---|---|---|
| 1 Batch arrives: the survey firm uploads the week's interviews | Every Monday | Without me | Survey firm | Raw batch |
| 2 Run checks: duplicates, outliers, skip logic, interview length, enumerator patterns; raw data read-only | When the batch lands, I ask | Without me | Agent | Flag list, check report |
| 3 Triage flags: agent proposes a category per flag; I decide | Monday, 1 hour | I'm in it | Me, agent | Decision log |
| 4 Field follow-up: call back respondents and enumerators | Tuesday to Thursday | Without me | Field coordinator, survey firm | Resolved queries |
| 5 Apply corrections: in the cleaning script, never in raw data; rerun the pipeline, update the codebook | Once the sheet is filled in | Without me | Agent | Clean data, changelog |
| 6 Approve & lock: review the changelog, spot-check ten records, tag the version | Friday | I'm in it | Me | Tagged release |

### An AI data map

A data map shows how data moves through a project. Adding the AI tool shows where AI is used and which data it receives. If you cannot say which data goes into the tool at a stage, that stage is not ready yet.

| Stage | AI task | Data in | Classification | Data out | Checked by |
|---|---|---|---|---|---|
| Design | Literature search, concept note feedback | Concept note, published papers | Official Use Only | Summary, cited sources | PI verifies every citation |
| Acquisition | Program survey form, translate questions | Questionnaire, codebook | Official Use Only | Form code, translations | Field team pilots, local-language review |
| Processing | Write and review cleaning code | Code, variable names, **synthetic** data | Official Use Only | Cleaning scripts | RA compares counts before and after |
| Analysis | Write and review analysis code, exhibits | Code, **de-identified** data | Confidential | Tables, figures | Analyst inspects every exhibit |
| Publication | Slides, brief, reproducibility package | Paper draft, exhibits | Official Use Only | Drafts, package | Author owns every claim; AI use disclosed |

Illustrative only: classifications depend on the project's data agreements. Identified data does not appear in the "Data in" column at any stage.

---

## Q2 · What do I need to do?

### Setup checklist

What the bootcamp covered. Check what is done **in this project**, not the demo project. Anything unchecked is a candidate "Now" target.

- **Setup (Day 0):** project in a GitHub repository; project opened in VS Code; coding agent installed and signed in with an approved account
- **Onboarding (Day 1):** memory file in the project; at least one skill installed and tested
- **Analysis (Day 2):** AI review of data processing or analysis code; reproducible chart or table produced with a skill; AI output checked by a human, with a record of the check
- **Research products (Day 3):** presentation or brief from project materials; draft reproducibility package

### Example targets

| Horizon | What fits here | Examples |
|---|---|---|
| **Now** (this week) | Already works, low risk | Memory file in the real project; coding agent for cleaning and analysis code; finish anything unchecked from the setup checklist |
| **6 weeks** | Needs some setup or team agreement | De-identified or synthetic data; data rules in the memory file; AI code review as a routine step; team members onboarded |
| **3 months** | Not plug-and-play yet. Start defining the need now | Review and quality-control workflows; skills that do not exist yet; reproducibility package for a paper |

Write a few specific targets rather than many general ones. The 6-week and 3-month targets are the ones in the follow-up survey.

### Skills

Good skill candidates are tasks the team repeats with the same steps every time.

- **Known skills** from the bootcamp: code review; reproducible charts and tables; presentations; working-paper feedback; reproducibility packages.
- **Skills not yet found:** write them down anyway. What is the task? How often does it recur? What does a good result look like? Who could build it, or should you ask Impact Analytics?

### Team access

AI adoption fails when only one person on the team uses the tools. Not everyone needs a coding agent, but everyone who touches project data needs the data classification rules.

| Team member | Role | Needs access to | Trained on | Next step |
|---|---|---|---|---|
| *Name* | PI | Approved chat tool | Ethics, verifying outputs | Review AI-assisted drafts |
| *Name* | RA | Coding agent, GitHub repo | Memory files, skills, code review | Onboard by end of month |
| *Name* | Field coordinator | Approved chat tool | Data classification | Ethics session recording |

### Data rules for the memory file

The agent reads the memory file at the start of every session. Add a block like this:

```markdown
## Data rules (read before any task)

- Never open files in `data/raw/` or `data/identified/`.
- Work only with `data/deidentified/` or `data/synthetic/`.
- If a task seems to need identified data, stop and ask.
- Refer to variables by name. Do not copy data values into output.
- Record AI-assisted changes in the commit message.
```

A memory file guides the agent, but it does not enforce anything. Where the tool supports it, also block those folders in the agent's permission settings, and keep identified data out of the repository.

---

## Roadblocks · What is in the way?

### Confidential data

The biggest roadblock for most teams: the most useful parts of the work would let the agent see confidential data. Prepare the data **before** an AI tool reaches the project folder.

- **Remove PII.** Run a de-identification script on the raw data, outside any AI tool. Removing names is not enough: indirect identifiers such as village, exact dates and rare combinations of characteristics matter too.
- **Create synthetic data.** If you cannot remove PII safely, generate a synthetic dataset with the same structure, so the agent can write and test code against it.
- **Separate folders.** Keep identified data in a location the agent never opens.

De-identification is a human responsibility. An agent can help write the script from the codebook, but it should never see the raw data while doing so.

### Risks and mitigations

| Risk | Mitigation |
|---|---|
| Confidential data reaches an AI tool | Classify first; de-identified or synthetic data only; data rules in the memory file; block folders in agent settings |
| AI output is wrong but looks right | Human review of every exhibit and number; Git diffs to see what changed |
| Only one person uses the tools | Shared memory file and skills in the repository; onboarding target in the plan |
| Costs or token limits run out | Use cheaper models for routine tasks (Day 1 cost session) |
| AI use is not documented | Record AI use in commits and in the reproducibility package; disclose meaningful assistance |
| The plan is forgotten | Save the plan in the repository; follow-up survey on the 6-week targets |

Some roadblocks you cannot resolve alone, for example a data agreement that may not allow processing by an AI tool, or tool approvals. Write them in plan section 4 anyway, with who could help. That is how the bootcamp team knows what to fix.
