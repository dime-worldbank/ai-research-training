# Field Notes: When a Failed Reproduction Is Useful

*Background article for AI for Research, Issue 4. Reading time: about 8 minutes.*

Kubota and coauthors built a system that reads a paper and codebook, writes analysis code, runs it, compares the output with published tables and figures, and tries again when the results differ. Their 2026 prototype tested the method on Bethany Bryson's 1996 paper on musical dislikes using the 1993 General Social Survey.

**Sources:** [paper](https://arxiv.org/abs/2602.18453) · [code and outputs](https://github.com/kubotaso/AI_Social_Replication)

## What the system did

The system used three inputs:

1. the published paper;
2. a data file drawn from the 1993 GSS;
3. the relevant codebook.

It then repeated three steps:

1. extract a specification from the paper and codebook;
2. write and execute Python code;
3. compare generated results with the published output and produce a discrepancy report.

The paper contains three tables and one figure. The authors ran a separate program for each output, with up to 100 attempts.

## What happened on Table 1

Table 1 models the number of music genres a respondent dislikes. It includes socioeconomic variables, demographic controls, and a political intolerance scale.

The system used all 100 attempts. Ninety-one produced valid output and nine ended in runtime errors. The best result came on attempt 18, with an alignment score of 74 out of 100.

The broad pattern was close, but several details remained different:

- sample sizes did not always match;
- some coefficient magnitudes differed;
- some significance levels changed;
- the Hispanic indicator and missing-value handling were hard to infer from the text and codebook.

One early attempt coded Hispanic as missing for 93% of respondents. That reduced one model to 37 observations and reversed some coefficient signs. The discrepancy report helped the system identify the problem and improve later attempts.

## The figure was a different problem

The figure plotted logistic-regression coefficients and average education levels by music genre. Early attempts reversed the category order, assigned series to the wrong axes, and used the wrong line styles.

After 24 attempts, the best score reached 95 out of 100. The system corrected most of the structure, including the mapping between series and axes. The figure required fewer attempts than the tables, but it still needed repeated comparison with the published image.

## What "informative failure" means

A failed reproduction can point to several causes:

- the generated code is wrong;
- the source paper leaves a step unclear;
- the codebook does not fully explain a constructed variable;
- preprocessing or missing-value rules are undocumented;
- the target output is hard for the system to read.

These causes have different implications. A mismatch does not by itself show that the published finding is wrong. It shows where a person should investigate.

The prototype's most useful output may be the discrepancy report. It records differences in sample size, coefficients, standard errors, significance, and figure structure. That gives an author or reviewer a list of questions to resolve.

## Reproducibility and validity

The authors make an important distinction. Reproducing a published result checks whether the stated procedure and data can produce the reported output. It does not test whether the research design identifies the claimed effect, whether the measure is valid, or whether the result holds in another sample.

Code review and reproducibility checks cover part of the review process:

| Check | Question |
| --- | --- |
| **Code review** | Does the implementation contain errors or risky choices? |
| **Computational reproducibility** | Can the same data and procedure regenerate the output? |
| **Robustness** | Does the result hold under other reasonable choices? |
| **Research validity** | Does the design support the claim? |

An automated system can help with the first two. Researchers and reviewers remain responsible for the last two.

## Limits of the case study

The published prototype tested one paper with public cross-sectional data and standard models. The authors note that panels, survey weights, multiple data sources, complex merges, and less standard methods need further work.

The public project repository now lists applications to five papers across economics, political science, and sociology. That expansion is useful, but the detailed results discussed here come from the published Bryson case study.

## What to use in your own review

- Treat a failed run as a finding to investigate.
- Save the error, generated output, and comparison.
- Ask which assumption or undocumented step could explain the gap.
- Keep an author in the loop when variable construction or sample rules are ambiguous.
- Use successful reproduction as a consistency check. Continue with substantive review.

## One number

Remember the 100 attempts. Repeated debugging improved the result, but it did not remove every difference. The remaining gaps were useful because they showed where the written record was incomplete or the generated code was still wrong.
