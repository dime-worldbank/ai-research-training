# Field Notes: Can You Feel a Productivity Gain? Apparently Not.

*Background article for AI for Research — Issue 1. Reading time: ~8 minutes.*

This issue's Big Number — roughly **30% average task productivity gains** from AI tools in controlled trials, reviewed by the OECD and summarized by CaixaBank Research — is the right headline for where we are. The gains show up most clearly for people still getting started. So why does it often not *feel* that way when you use the tools yourself?

A METR randomized trial helps answer that. Experienced developers badly misjudged how much AI helped them, even about their own just-completed work. The lesson for DECDI is not "skip the tools." It is: when we evaluate the workflows from this training series, measure outcomes on comparable tasks — don't collect impressions.

**Source:** Becker, Rush, Barnes & Rein (METR, 2025), *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity*. [Blog and paper](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) · [arXiv:2507.09089](https://arxiv.org/abs/2507.09089) · [Data and code](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/)

> **On the effect size.** METR has marked the measured slowdown as out of date: the trial used early-2025 AI tools, and they published updated data on late-2025 tools in February 2026 (alongside a self-reported survey they caution has reliability limits). Don't quote that headline speed number as the current state of AI coding tools. The finding we care about is the *perception gap* — and that one still stands.

## What they did

Most evidence on AI coding productivity comes from vendor benchmarks or self-reports. METR ran an actual randomized controlled trial in the wild: 16 experienced open-source developers completed 246 real tasks (bug fixes, features, refactors) on mature repositories they had contributed to for years — on average 5 years of prior experience, codebases averaging over one million lines. Each task was randomly assigned to allow or disallow AI tools. When allowed, developers mostly used an AI-enabled editor with a frontier model of early 2025. Screens were recorded; time was measured.

This is about as close to the gold standard as this literature gets: real developers, real tasks, random assignment, revealed (not reported) outcomes.

## What they found: a ~40-point gap between belief and measurement

- Before the study, developers forecast AI would make them **24% faster**.
- *After* completing their tasks, they believed AI had made them **20% faster**.
- The clock said otherwise: with these early-2025 tools, in this setting, AI-allowed tasks actually took *longer* (a 19% slowdown — the dated part of the result; see the note above).
- Economics and ML experts fared no better, forecasting speedups of 39% and 38%.

The finding that lasts is the gap: developers misjudged the effect of AI on their *own, just-completed work* by roughly **40 percentage points** — and in the optimistic direction. That is a result about human judgment, not about any particular model version, and it is why every self-reported productivity number — including the ones we will collect in our own trainings — needs to be read with this study in mind.

## Why belief and measurement diverged: the boundary conditions

METR examined 20 candidate explanations for the measured slowdown. The ones that survived scrutiny matter directly for research work:

1. **Deep tacit context.** These developers knew their codebases intimately. The AI didn't, and briefing it (or reviewing its misunderstandings) cost more than the generation saved. The closer your task is to "I already know exactly what to do," the less AI adds — and the more its review overhead subtracts.
2. **High quality bars.** Mature open-source projects have strict style, testing, and documentation standards. AI output routinely needed rework to meet them. Sound familiar? Replication-grade code has the same property.
3. **Large, interconnected codebases.** AI suggestions that were locally plausible broke things globally.
4. **Time redistribution.** With AI, developers spent less time actively coding and searching — and more time prompting, waiting, and reviewing AI output. The work didn't disappear; it moved.

Crucially, the authors do *not* conclude "AI doesn't work." They flag the result as a snapshot of one setting — experts, familiar code, high standards — and note it doesn't contradict the large speedups measured elsewhere (e.g. for junior developers, unfamiliar codebases, or greenfield tasks). Their own follow-up work on late-2025 tools, and the broader trial evidence behind this issue's Big Number, point the same way: the tools improved, and the gains are real where the setting fits.

## What this means for a research department

- **The gains are real but conditional.** The OECD-reviewed trials find ~30% task-level productivity gains, concentrated among less-experienced workers on routine tasks. Both findings can be true: AI compresses skill gaps on routine work and can drag on experts doing familiar, high-standards work — unconfigured.
- **Configuration is the difference.** The METR developers used tools largely out of the box, with no project memory files, no team skills, no encoded conventions. That is exactly the gap the +AI Onboarding sessions address. An assistant that already knows your stack, path rules, and merge checklist removes much of the review-and-correct overhead that produced the slowdown.
- **Measure, don't ask.** If we want to know whether these tools help DECDI teams, self-assessment will mislead us — participants in this study were off by about 40 percentage points about their *own* just-completed work. Where possible, track time on comparable tasks.
- **Pick your spots.** Delegate what is routine, verifiable, and low-context (boilerplate, format conversion, first-draft checks). Keep tight ownership of what is novel, high-context, and hard to verify.

## One number to remember

Not the 19% — that one is dated. And not instead of the ~30% from the Big Number — that one is still the place to start. Remember the ~40-percentage-point gap between what developers felt and what the clock measured, about their own work, minutes after finishing it. Whatever else you take from this issue: measure your AI workflows; don't ask yourself how they felt.
