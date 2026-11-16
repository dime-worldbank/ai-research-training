# Field Notes: Same Model Name, Different Answer

*Background article for AI for Research, Issue 7. Reading time: about 8 minutes.*

This issue is about spending tokens well: smaller models for routine work, bigger ones where they earn their keep. Sensible advice. But once you start switching models to save money, a second question appears that Impact Analytics' training on cost-effective AI agents did not have time for. If the model that coded your survey answers in March is not the model you have in November, are the results still the same results?

Three political scientists spent most of 2024 finding out. Their paper is still a working draft, but it is the most careful attempt we know of to measure the problem, and the title tells you what they found: "Trust me bro".

**Source:** Barrie, Palmer and Spirling, "Replication for Language Models: Problems, Principles, and Best Practice for Political Science", working paper, draft of December 17, 2024. [PDF](https://arthurspirling.org/documents/BarriePalmerSpirling_TrustMeBro.pdf) · [code and data](https://github.com/ArthurSpirling/LargeLanguageReplication). Presented at APSA 2024 and Princeton in 2025. Not yet peer reviewed.

## What they did

They picked three standard text-coding jobs from political science: placing party manifestos on a left-right scale, coding protest events from news reports, and scoring speeches for populism. Then, on the 25th of every month from April to December 2024, they ran the same prompts on the same texts through the same models. GPT-4, two versions of Gemini, and a Llama model running on their own machine. Crowdworkers did the same tasks as a baseline.

That is what they call a rolling, iterated replication design. Nothing changes except the date.

They also took a published paper (Bor and Petersen, 2022) and re-estimated its regressions with AI-coded versions of the key variable, using five different OpenAI models.

## What they found

**The models were more accurate than the crowdworkers, and less stable.** On average the AI codings beat the humans. But month to month, the AI codings moved around more than the human ones did, even though nothing in the prompt or the text had changed.

**The local model barely moved.** Llama, running on their own hardware with a fixed version, had almost no variance across months on the static tasks. It was not the best coder. It was the most repeatable one. In their words, open models "have the best replication performance".

**Fixing the temperature did not fix it.** Setting the temperature to zero is the standard advice for making a model deterministic. It helps within a single day. It does nothing about the model being quietly updated between April and June. As they put it: "Setting temperatures may help, but this is no panacea."

**Some of the models stopped existing.** Gemini's back end was updated without notice in June 2024, and the code they had used for the first two months of the project no longer ran. One Gemini version could not be re-run at all. Two of the OpenAI monthly runs came back empty and had to be redone. The paper's line on this is the one to remember: "at worst, they may simply cease to exist overnight".

**Downstream, the answer changed.** When they re-ran the published regressions with AI-coded variables, most of the key coefficients stopped being significant. On the populism task, the AI-coded versions produced coefficients less than a third the size of the published ones. Same data, same model specification, different coder.

## Why this belongs in a newsletter about token costs

Because the cheapest way to cut your bill is to switch to a smaller or newer model, and this paper is about what happens when the model changes.

If you use an AI model to produce a *variable* (coded answers, classified documents, extracted numbers), the model is part of your measurement, the way an enumerator or a coding team is. Issue 5's Field Notes made that point about bias. This paper makes it about stability. A measurement that gives a different answer next month, with no change in inputs, is a measurement you cannot build a result on.

That does not mean do not switch models. It means be deliberate about which tasks you switch.

- **Switch freely for tasks where you check the output anyway.** Drafting, proofreading, explaining syntax, writing a function you will test. If the smaller model gets it wrong, you will see it, and the model's identity is not part of the result.
- **Pin the model for tasks that produce data.** If a model coded your open-ended answers, record exactly which model and version, the date, the prompt, and the temperature. Treat a model change as a change to the instrument, which means re-coding a sample and reporting the agreement.
- **Prefer a version you can hold on to.** The authors' first recommendation is to consider open models that can be versioned offline. At the Bank, the practical equivalent is the MEGA environment, where a model can be run inside the Bank's infrastructure rather than through a vendor's web service that may be updated tomorrow. Ask the Impact Analytics team if you want to go that route.
- **Replicate your own work.** Their last recommendation is the simplest. Run the coding step more than once, on different days, and report how much it moved. If the answer is "a lot", that is a finding about your method, and it should be in the paper.

## What the paper does not tell you

It is a working paper, and the draft we read is from December 2024, so the specific models are a generation or two old. The tasks are political text, not survey data from Kano or Kinshasa. And the authors are measuring a moving target: vendors have since added more explicit version pinning to their APIs, which addresses some, not all, of what went wrong here. The point that survives all of that is structural. A closed model behind an API is a service, not a tool you own, and services change.

## One number

Remember a third. That is how large the AI-coded coefficients were, compared with the published ones, on the populism task. Nothing about the data had changed. Only the coder had.
