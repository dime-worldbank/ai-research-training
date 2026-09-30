# Instructor answer key — seeded defects

Do not distribute before the exercise. Every defect below is intentional.
"Domain" refers to the wb-paper-review domain expected to catch it; a good
run of the named domain + critic should surface the defect.

| # | Defect | Where | Domain / critic | Expected severity |
|---|---|---|---|---|
| D1 | Text says **5.2 pp**; preferred spec (Table 2 col 2) says **4.2 pp** (0.042) | Results, first sentence | accuracy / Methodologist | P0 |
| D2 | Text says girls' effect is **7 pp**, "twice as large"; Table 3 says **5.6 pp** vs 2.9 | Results, heterogeneity para | accuracy / Methodologist | P0 |
| D3 | "Reduced dropout by 11 percent" — no dropout result exists in any output | Results, end of first para | accuracy / Methodologist | P0 |
| D4 | `@mwansa2021` cited but **missing from references.bib** | Intro, lit paragraph | accuracy (citations) | P1 |
| D5 | `johnson2020` — fabricated-looking entry (journal doesn't exist) | Intro + bib | accuracy (citations) | P1 |
| D6 | "Quasi-random rollout … interpret causally" — contradicted by Table 1 notes (poorer districts first; rural share & assets imbalanced, p≤0.04) and AGENTS.md ("not randomized") | §2 + §5 stability claim | design / Methodologist (DiD gate: comparability, parallel trends) | P0 |
| D7 | Parallel trends **asserted, never shown** ("we assume parallel trends, which is standard"); no event study or pre-trends figure exists | §4 Empirical strategy | design / Methodologist (gates/did.md) | P0 |
| D8 | Buried lead: introduction contains **no result**; magnitudes first appear in §5. Roadmap-style intro ends without findings | Introduction | argument / Writing Critic | P1 |
| D9 | Throat-clearing + AI-pattern language: "The literature has long been interested", "It is important to note", "delved/delve" ×3, "crucial" ×2, "landscape" ×3, "furthermore" ×3, "pave the way" ×2, "transformative", "robust" (non-statistical) | Intro + Conclusion + Abstract | language / Writing Critic (anti-AI checklist) | P1–P2 |
| D10 | Table 3 caption not self-contained: no notes, no clustering, no sample definition, no baseline means | outputs/tab3_het.tex | presentation / Writing Critic | P1 |
| D11 | Overclaiming: abstract "demonstrates … most cost-effective … worldwide" (no cost data anywhere); conclusion "scaled nationwide immediately", "adopted across the continent" — external validity and cost claims unearned | Abstract + Conclusion | policy / Policy Reviewer + accuracy (claim scope) | P0 |
| D12 | Abstract ≈ 185 words vs. outlet constraint ≤ 150 (see profile Outlet constraints) | Abstract | outlet | P2 |

## Cross-flow notes

- D1/D2/D3 are the live-demo defects: fast to show, unambiguous, and they
  demonstrate grounding against `outputs/`.
- D6+D7 make a good **challenge-protocol** demo: have a participant challenge
  D7 ("everyone assumes parallel trends") and watch the critic uphold with
  reasons (imbalanced rollout documented in Table 1 notes makes the assertion
  weaker here than in a generic DiD).
- D8 is the best **revise-mode handoff**: accepting it creates a concrete
  work-queue item ("state 4.2 pp result by intro paragraph 3").
- The profile's fear ("reviewers will doubt parallel trends") should rank
  D6/D7 at the top of the Methodologist's output — check that personalization
  visibly reorders priorities; if it doesn't, that's a skill bug.
- After fixing D1–D3, rerun accuracy: it should come back clean — good
  closing beat for the demo.
