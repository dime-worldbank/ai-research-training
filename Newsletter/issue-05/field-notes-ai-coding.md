# Field Notes: When AI Does the Coding, It Becomes Part of the Measurement

*Background article for AI for Research, Issue 5. Reading time: about 8 minutes.*

This issue's Big Number is about a measure that was wrong more often for one group. A health algorithm used cost to measure need. Less is spent on Black patients who are just as sick, so the algorithm missed most of the Black patients who needed extra help ([Obermeyer et al., Science, 2019](https://doi.org/10.1126/science.aax2342)).

Field Notes looks at a version of the same problem that is much closer to our own work: using AI to code survey answers or documents. The September 17 session ended its validity section with this case ([slide: "Validity: when AI does the measuring"](https://dime-worldbank.github.io/ai-research-training/sessions/ai-ethics-governance/#/validity-when-ai-does-the-measuring)). This article goes one step further, using a study by Egami, Hinck, Stewart and Wei.

**Source:** [Egami et al., NeurIPS 2023](https://arxiv.org/abs/2306.04746)

## The session's example

You have 20,000 open-ended survey answers in French and Hausa. An AI model codes them in an hour. You check ten, and it agrees with you on all ten. Coding them by hand would take two weeks, and the paper is due Friday.

The tempting answer is "check a random sample, and if agreement is above 85%, use the AI codes as they are." That feels safe. But one overall agreement score tells you nothing about the Hausa answers on their own. If the model is worse in Hausa, the errors are not random. They pile up in one group, which is exactly the pattern in the health algorithm.

## What the study found

Egami and coauthors looked at what happens when researchers take labels from an AI model and use them as a variable in a regression, as if a person had coded them.

Their finding: this gives **biased estimates and confidence intervals that are too narrow, even when the labels are 80–90% accurate**.

The reason is simple. Accuracy tells you how often the model is right. It does not tell you *where* it is wrong. If the mistakes are linked to anything in your analysis (language, region, education, the outcome itself), they push the estimate in one direction. The confidence interval still looks tight, because the analysis treats the AI labels as if they had no error at all.

So a high accuracy score is not enough. The question is whether the errors change your result.

## What fixes it

The fix does not require hand-coding everything. It needs a small sample coded by a person, chosen at random.

1. **Pick a random sample to hand-code.** Random matters. If you only check the answers the model was unsure about, you miss the ones it got wrong with confidence.
2. **Compare the AI codes with the hand codes, group by group.** Look at the errors by language and by any group you will report on. An overall score can hide a group where the model does badly.
3. **Use a method that corrects for the errors.** Egami and coauthors propose one called design-based supervised learning. A related approach is prediction-powered inference ([Angelopoulos et al., Science, 2023](https://doi.org/10.1126/science.adi6000)). Both combine the cheap AI labels with the small hand-coded sample so the estimate and the confidence interval stay honest. Both rely on assumptions, the main one being that the hand-coded sample is truly random, so read the papers before using them.
4. **Plan the hand-coded sample size early.** It depends on how common each code is, how many groups you need to compare, and how precise the result has to be. Budget the time when you design the study, not the week the paper is due.

## Where else this shows up

The same question applies whenever AI turns text, images or recordings into a variable:

- coding open-ended survey answers or interview transcripts
- classifying documents, news articles or project reports
- estimating wealth or crop type from satellite images
- translating questions or answers before analysis

In each case, ask: who could the AI be wrong for more often, and would that change the finding?

## What to take from this

- Treat AI coding as part of your measurement, not as a shortcut before the "real" analysis.
- Don't trust one overall accuracy number. Check errors for each group you care about.
- Keep a random, hand-coded sample, and use it in the analysis, not just as a check.
- Say in the paper how the codes were made and how you checked them.

## One number

Remember 80–90%. That's how accurate the AI labels were, and the results were still biased. What matters is not how often the model is right. It is who it is wrong for.
