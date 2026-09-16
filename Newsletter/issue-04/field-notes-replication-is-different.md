# Field Notes: Replication Is a Different Problem

*Background article for AI for Research, Issue 4. Reading time: about 8 minutes.*

This issue's Big Number is about **computational reproducibility**: Trisovic and coauthors re-ran more than 9,000 published R scripts on their own data in a clean environment, and 74% stopped with an error ([Scientific Data, 2022](https://www.nature.com/articles/s41597-022-01143-6)). Same code, same data, different machine.

Field Notes looks at a study that sounds similar and is not. Kubota and coauthors built an AI system that reads a paper and a codebook, writes its own analysis code, runs it, compares the output with the published tables, and tries again when the results differ. The system never sees the authors' code.

**Sources:** [paper](https://arxiv.org/abs/2602.18453) · [code and outputs](https://github.com/kubotaso/AI_Social_Replication)

## Two questions that get confused

| | Inputs | Question |
| --- | --- | --- |
| **Computational reproducibility** | Authors' code + authors' data | Does running this regenerate the exhibits in the paper? |
| **Replication** | Authors' data + the paper's text, **no code** | Can the results be rebuilt from the description alone? |

The Reproducible Research team's verification, and the reproducibility skill's audit, answer the first question. Kubota's system attempts the second. A package can pass the first and fail the second (the code runs, but the paper does not describe what the code does well enough for someone else to rebuild it). It can also fail the first and pass the second (a hardcoded path stops the run, but the method section is precise enough to reconstruct).

When the two get mixed together, a replication failure gets read as "the package is broken," and a clean reproducibility check gets read as "the analysis is right." Neither follows.

## What the system did

The system used three inputs:

1. the published paper;
2. a data file drawn from the 1993 General Social Survey;
3. the relevant codebook.

It then repeated three steps, up to 100 times per exhibit:

1. extract a specification from the paper and codebook;
2. write and execute Python code;
3. compare generated results with the published output and produce a discrepancy report.

The 2026 prototype was tested on Bethany Bryson's 1996 paper on musical dislikes, which contains three tables and one figure.

## What happened on Table 1

Table 1 models the number of music genres a respondent dislikes, with socioeconomic variables, demographic controls, and a political intolerance scale.

The system used all 100 attempts. Ninety-one produced valid output; nine ended in runtime errors. The best result came on attempt 18, with an alignment score of 74 out of 100.

The broad pattern was close, but several details never matched:

- sample sizes differed;
- some coefficient magnitudes differed;
- some significance levels changed;
- how to code the Hispanic indicator and handle missing values was hard to infer from the text and codebook.

One early attempt coded Hispanic as missing for 93% of respondents. That shrank one model to 37 observations and reversed several coefficient signs. The discrepancy report let the system spot the problem and improve later attempts, but it never fully closed the gap.

## The figure was a different problem

The figure plotted logistic-regression coefficients and average education levels by music genre. Early attempts reversed the category order, assigned series to the wrong axes, and used the wrong line styles.

After 24 attempts, the best score reached 95 out of 100. The system corrected most of the structure, including the mapping between series and axes. It needed fewer attempts than the tables, but it still needed repeated comparison with the published image.

## Why the gaps are informative

When a replication attempt fails, the cause can be any of:

- the generated code is wrong;
- the paper leaves a step unclear;
- the codebook does not fully explain a constructed variable;
- preprocessing or missing-value rules are undocumented;
- the target output is hard for the system to read.

These have different implications. A mismatch does not show that the published finding is wrong. It shows where the written record is incomplete, and where a person should look.

That is why the most useful output of the prototype is not the alignment score but the discrepancy report. It records differences in sample size, coefficients, standard errors, significance, and figure structure, and it gives an author or reviewer a list of questions to resolve.

## Why this matters for a reproducibility package

A well-built package makes the replication question much easier to answer, because the code *is* the precise description. Every ambiguity that stopped Kubota's system (how missing values were coded, which respondents were dropped, how a scale was constructed) is a line of code in a package that runs.

So the two checks are not in competition. Computational reproducibility is the lower bar, and it is the one an author controls directly. The audit in this issue's Try This Today checks it. Replication from text is the higher bar, and it depends on how well the paper describes what the code does.

Neither is a test of whether the research design identifies the claimed effect, whether the measure is valid, or whether the result holds in another sample. Those remain the job of referees and readers.

## Limits of the case study

The prototype tested one paper with public cross-sectional data and standard models. The authors note that panels, survey weights, multiple data sources, complex merges, and less standard methods need further work.

The public project repository now lists applications to five papers across economics, political science, and sociology. The detailed results discussed here come from the published Bryson case study.

## What to take from this

- Use the words carefully. If the code ran and the numbers matched, say *reproduced*. If someone rebuilt the analysis from the text, say *replicated*.
- Treat a failed replication as a documentation finding first. Ask which undocumented step could explain the gap before asking whether the result is wrong.
- Save the error, the generated output, and the comparison. The discrepancy report is the deliverable.
- A package that passes the audit removes most of the ambiguity a replicator would otherwise hit. That is the practical link between the two problems.

## One number

Remember the 100 attempts. Repeated debugging improved the result, but it did not remove every difference, and it was never trying to answer the question a reproducibility check answers. Keep the two apart.
