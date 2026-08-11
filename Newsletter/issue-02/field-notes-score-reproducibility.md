# Field Notes: Precise Reproducibility Is Still Hard --- SCORE and Why Packaging Matters

*Background article for AI for Research --- Issue 2. Reading time: ~8 minutes.*

This issue's Big Number is internal: only about **one in five** Policy Research Working Paper reproducibility packages pass verification on first review ([World Bank Impact Evaluations blog](https://blogs.worldbank.org/en/impactevaluations/a-milestone-for-open-science--500-packages-in-the-world-bank-s-r)). That is a package problem --- missing pieces, paths, documentation --- not usually a research-quality problem. The academic literature points the same way: even among published papers, precise reproducibility is far from automatic.

**Source:** Miske et al. (2026), *Investigating the reproducibility of the social and behavioural sciences*, *Nature*. [Nature](https://www.nature.com/articles/s41586-026-10203-5) · DOI [10.1038/s41586-026-10203-5](https://doi.org/10.1038/s41586-026-10203-5). Part of the DARPA SCORE program.

## What SCORE asked

Published claims should be reproducible: same analysis, same data, same result. SCORE took a stratified random sample of **600** papers (2009--2018) from 62 journals across the social and behavioural sciences and asked how often that standard held.

Two bottlenecks showed up immediately:

1. **Getting the materials.** Authors of only about **24%** of papers made data available for a reproducibility assessment. Without materials, you cannot even start.
2. **Getting the same numbers.** Among the papers that could be assessed (143 datasets), about **54%** were rated **precisely** reproducible, and about **74%** at least **approximately** reproducible (within 15% of the original effects, or within 0.05 of original *p*-values), after weighting claims within papers.

So even when data could be obtained, precise reproduction failed roughly half the time.

## What predicted success

Sharing was not all-or-nothing:

- When authors shared **both data and code**, approximate reproducibility was about **91%** and precise about **77%**.
- When analysts had to **reconstruct** the dataset from public sources (e.g. re-pull census extracts and rebuild the cleaning steps from the paper text), approximate fell to about **38%** and precise to about **11%**.

Reproducibility was also higher for political science and economics than for some other fields, for more recent papers, and for journals that required data sharing --- patterns consistent with "better packaging and norms help," not "some disciplines are magically careful."

## Why this is the right comparison for DECDI (and why Song et al. is not)

It is tempting to cite benchmarks where an LLM is asked to regenerate analysis from a paper PDF. That is a hard, interesting task --- and current agents are often weak at it. It is also **not** the task the July 16 training targeted.

| Task | What success means | Relevance here |
| --- | --- | --- |
| LLM regenerates analysis from a paper | Invent working code from text | Different problem; weak evidence of readiness |
| SCORE-style reproduction | Same data + same analysis -> same results | Closest academic mirror of "does this package work?" |
| PRWP verification | Outsider runs *your* package; exhibits match the paper | Exactly what the skill prepares you for |

The skill does not ask the model to rediscover your identification strategy from scratch. It asks the model to help you **package what you already have** so a reviewer can run it: checklist complete, common failure patterns caught, clean rerun possible.

## What to take into next week's package work

- **First-pass failure is normal.** The Bank's published "1 in 5" first-try rate and SCORE's ~54% precise rate (conditional on materials) are the same story: room for improvement is large, and most of it is operational.
- **Share code with data.** SCORE's steep drop when code is missing is a strong argument for a main script, a README, and a Data Availability Statement --- not as bureaucracy, but as the difference between ~77% and ~11% precise reproduction in their extreme comparison.
- **Catch failure patterns early.** Hardcoded paths, hand-edited tables, undocumented intermediate datasets, missing seeds --- these are exactly the recurring verification failures the skill's audit is built to surface before you submit.
- **Confirm current Bank numbers before you quote them externally.** The "1 in 5" figure is from the public RRR milestone blog; Mer Reyes Retana can give the latest internal share of packages that are complete and functional as first submitted (often cited around ~25%).

## One number to remember

Not a claim that half of science is wrong. Remember the packaging gap: **materials + runnable code** are what move reproducibility from rare to common --- inside PRWP verification and in SCORE alike.
