# Field Notes: When the Measure Is the Wrong One

*Background article for AI for Research, Issue 5. Reading time: about 8 minutes.*

Obermeyer, Powers, Vogeli, and Mullainathan studied a commercial algorithm used to flag patients for extra care. It was applied to about **200 million** people a year. At the same risk score, Black patients were much sicker than white patients. The reason was what the model had been trained to predict.

**Source:** [Obermeyer et al., Science (2019)](https://doi.org/10.1126/science.aax2342)

## What the model was asked to predict

The health system needed a measure of health need. The algorithm was trained to predict healthcare **cost**.

Less money has historically been spent treating Black patients at the same level of illness, because of differences in access to care, insurance, and how symptoms are followed up. A model that predicts cost learns those differences. Equally sick Black patients scored as healthier, because their care had cost less.

The target already carried that gap. Cost reflected who had been able to get care.

## What changed when the measure changed

The authors compared the cost-based score with measures of actual health, including the number of active chronic conditions. Patients with the same risk score had different levels of illness.

Fixing the measure would have raised the share of Black patients flagged for the extra-care program from **17.7%** to **46.5%**. Same people, same decision, a different answer to "who needs help."

A model can fit the data it was given and still be the wrong tool for the decision in front of it. Overall accuracy can sit next to failure for the people a project exists to serve.

## Where the same pattern shows up in research

The session asked teams to review output for unintended bias, and to ask who is left out and how that could change the result. Bias can enter in four places: the training data, the design of the model (what it is told to predict, and what counts as success), the documents and examples we give it, and use in a language or a population where it has not been checked.

The health algorithm is the second of those. Cost was easy to observe. It was a poor stand-in for need.

The same question applies when a model codes open-ended answers, when satellite images stand in for wealth, or when a retrieved page stands in for an official statistic. Agreement on the cases you checked leaves the other languages, livelihoods, and groups unchecked. The session's coding example made that concrete: one overall agreement score can hide a group the model handles badly.

## What to ask of a stand-in measure

Before a model, a coder, or a summary becomes a variable or a rule for who receives help:

1. Name the thing you actually need (need, welfare, a concept in the questionnaire) and the thing the model is predicting or coding. If those differ, say so in the paper.
2. Check whether the stand-in means the same thing in every group and place you will report on. A signal that fits where the training data are dense can mark everyone else as low-need.
3. Keep a person able to review and reverse an individual case. An overall accuracy score leaves a wrongly excluded household with nowhere to go. The same session made that point with Telangana's system for merging welfare records.

## One number

Remember 17.7% and 46.5%. The algorithm followed its target. That target had already left people out.
