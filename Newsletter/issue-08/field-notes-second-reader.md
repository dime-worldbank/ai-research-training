# Field Notes: The Second Reader

*Background article for AI for Research, Issue 8. Reading time: about 8 minutes.*

This issue's Big Number is what happens when a model grades its own homework: accuracy went down. The Deep Dive turns that into a habit, builder and critic in separate sessions. Field Notes is about the evidence behind the habit, including the parts that should make you careful.

## 1. Self-review makes things worse

**Source:** Huang, Chen, Mishra, Zheng, Yu, Song and Zhou, "Large Language Models Cannot Self-Correct Reasoning Yet", ICLR 2024. [arXiv:2310.01798](https://arxiv.org/abs/2310.01798)

The authors looked at a popular idea from 2023: ask a model to answer, then ask it to review its answer and fix any mistakes. Earlier papers had reported big gains from this. Huang and coauthors noticed that those papers had, in one way or another, let the model know when it was wrong, usually by stopping the loop once the answer matched the key. Take that away, so the model has to decide on its own whether to change its answer, and the gains disappear.

On grade-school maths problems, GPT-4 scored 95.5% on the first attempt. After one round of self-review it was at 91.5%. After two, 89.0%. On a common-sense reasoning benchmark, GPT-3.5 fell from 75.8% to 38.1%. The model changed right answers to wrong ones more often than the reverse.

The finding is about reasoning tasks, not code review. But the mechanism carries over. A model has no privileged access to its own mistakes. If it could see the bug, it would not have written it.

## 2. A separate critic helps

**Source:** McAleese, Pokorny, Ceron Uribe, Nitishinskaya, Trebacz and Leike (OpenAI), "LLM Critics Help Catch LLM Bugs", June 2024. [arXiv:2407.00215](https://arxiv.org/abs/2407.00215). Company report, not peer reviewed.

OpenAI trained a separate model, CriticGPT, whose only job was to write critiques of code that ChatGPT had produced. Then they ran a contest. Experienced contractors (median five years of Python, about fifty minutes per example) and the critic model both reviewed the same code, and other contractors judged which critique was better.

On bugs that occurred naturally in ChatGPT's output, the critic model's review was preferred over the human's 63% of the time. A human working with the critic was preferred over a human alone 60% of the time. The critic also beat ChatGPT itself when ChatGPT was simply prompted to review the code, which is the self-review case from Section 1.

Two caveats the authors are upfront about. The critic model nitpicked and invented problems more often than the humans did. And the best setup was not critic alone: a human plus the critic caught about as many bugs as the critic by itself, with fewer invented ones. The critic is a second reader, not a replacement for the first.

## 3. What happens in a real codebase

**Source:** Cihan, Haratian, İçöz, Gül, Devran, Bayendur, Uçar and Tüzün, "Automated Code Review In Practice", ICSE 2025 (Software Engineering in Practice track). [arXiv:2412.18531](https://arxiv.org/abs/2412.18531)

A software company switched on an LLM code reviewer for 238 developers and watched for a year: 4,335 pull requests, 1,568 of them reviewed by the tool. Developers resolved 74% of the tool's comments, which suggests most were worth acting on. They also reported irrelevant comments, unnecessary corrections and some plainly wrong reviews. And pull requests took longer to close: the average went from just under six hours to over eight, because people now had another set of comments to read and answer.

That is a fair picture of what to expect. The reviews are mostly useful, some are noise, and the time saved on finding bugs is partly spent on triage.

## 4. What this means for research code

Research code is a harder case than the code in these studies in one way and an easier one in another.

Harder, because research bugs rarely crash. A many-to-many merge that doubles rows, a missing-value code of -99 that enters a mean, a random draw with no seed. The script runs, the table comes out, and the number is wrong. A critic that only looks for things that break will miss all of these.

Easier, because we know what the common failures are. DEC's peer code review checklists and the reproducibility team's list of why packages fail are, between them, a fairly complete catalogue. That is why the code-review skill from Impact Analytics' November 9 training is built on a fixed list of flags rather than on "review this code". A critic with a checklist is looking for known failure patterns. A critic without one is guessing, and the CriticGPT paper tells you what guessing looks like: more invented problems.

Put the three studies together and the advice is the same from each angle:

- Do not ask the builder to check itself. It will mostly agree with itself, and sometimes break what was right.
- Do ask a separate reader with a checklist. It will find real problems, and it will also find some that are not there.
- Keep a person on the loop. Human plus critic beat either alone, in the one study that measured it.
- Budget the triage time. The review is quick. Reading it properly is not, and that is where the value is.

## 5. What the evidence does not cover

Nobody has yet run a controlled study showing that AI code review reduces the rate of wrong results in published research. The studies above are about software teams, reasoning benchmarks and a company's own model. The closest thing to research-specific evidence is the one-in-five reproduction rate from the reproducibility team's own checks, which tells you how much there is to find, not how much a critic finds. We will report our own numbers when we have them. If you ran the skill on your own project and it found something, or missed something, tell us. That is the evidence we are short of.

## One number

Remember 95.5 to 89.0. That is what self-review did to a model that was already good. Get a second reader.
