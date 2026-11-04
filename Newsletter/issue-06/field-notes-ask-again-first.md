# Field Notes: Ask Again Before You Switch Tools

*Background article for AI for Research, Issue 6. Reading time: about 7 minutes.*

Impact Analytics' October 22 training on Claude Enterprise gave a ladder for coding work: start in GitHub Copilot, move to Claude when Copilot struggles, and go to Claude Enterprise whenever confidential data is involved. The ladder makes sense on cost and on data rules. But "when Copilot struggles" leaves a question open. How many tries do you give a tool before you climb a rung?

A paper from last year gives a partial answer, and it is not the one most of us act on.

**Source:** Song, Wu and Zhou, "Code like an economist: Analyzing LLMs' code generation capabilities in economics and finance", *Finance Research Letters* 86 (December 2025), [doi:10.1016/j.frl.2025.108540](https://doi.org/10.1016/j.frl.2025.108540). The article is behind a paywall; what follows is based on the abstract and the published highlights.

## What they did

The authors collected 1,088 papers from the top 60 journals in economics, finance, econometrics and business statistics, published between 2004 and 2024, across 19 subfields. For each paper they wrote a structured prompt describing the analytical procedure and asked GPT-4 to write Python code that would replicate it. They scored the code for accuracy and completeness.

Then they did the thing most of us do when the first answer is wrong. They asked again. Two versions:

- **Self-regeneration.** The model is told to try again, with no new information from a person.
- **Human-assisted regeneration.** A person reads the output, points out what is wrong, and the model tries again with that feedback.

They modelled the results with a two-stage model and a clustered bootstrap, and checked that the pattern held for papers published after the model's training cut-off, so it is not just the model remembering code it had seen.

## What they found

Four results, in the authors' own order.

1. **Asking again helps.** Repeated self-regeneration improved the code. No new information, just another attempt.
2. **It helps less each time.** The better the first attempt, the smaller the gain from retrying. The authors describe this as diminishing marginal improvements.
3. **A person in the loop helps more.** Human-assisted regeneration improved the code further, and worked best when it came after a few self-regenerations rather than instead of them.
4. **Theory is harder than empirics.** Papers with theoretical models got worse code than empirical ones. The authors put this down to the abstract nature of the task: translating a model into code is a different job from writing a regression.

They also found that the original paper's author expertise predicted how well regeneration worked, which probably says more about how clearly well-established methods are described than about the model.

## What it means for the ladder

Put the ladder and the paper side by side and a rule falls out.

**Before you switch tools, retry in the one you are in.** The first attempt is rarely the best the tool can do. A plain "that's not right, try again" buys real improvement for a few cents. The gains shrink quickly, so two or three retries is the sensible budget, not ten.

**Then add yourself, not a bigger model.** The step that helped most in the study was a person reading the output and saying what was wrong. That is cheaper than any upgrade, and it is the step people skip when they are frustrated. "It used the wrong estimator, the paper clusters at the district level" gets you further than switching from Copilot to Claude with the same vague prompt.

**Switch when the task changes shape, not when you are annoyed.** The place the model genuinely struggled was turning abstract theory into code. That is the kind of task where a more capable model, or a model with a bigger context window, earns its price. If you are stuck on a merge, you are probably one specific sentence of feedback away from an answer in the tool you already have.

Together that is the ladder from the training, with the rungs spelled out: retry in Copilot, add feedback, and only then move to Claude. And confidential data still goes straight to Enterprise regardless of how many tries it takes.

## What the paper does not tell you

Be careful quoting this one. It tested a single model, GPT-4, which is two or three generations behind what you have in VS Code today. It scored the code; as far as we can tell from the public text, it did not run the code against the original data and compare the estimates. The target language was Python, so there is nothing here about Stata or R. And *Finance Research Letters* publishes short papers, so the methodological detail is limited. The full text may answer some of this. We could not reach it.

What survives those caveats is the shape of the result: iteration is cheap, feedback is cheaper than it feels, and the expensive tool is for the task that is actually hard.

## One number

Remember 1,088. That is how many published procedures the model was asked to code. The lesson from all of them was not about which model to buy. It was about asking twice, then saying what was wrong.
