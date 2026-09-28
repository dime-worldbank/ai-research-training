# Deep Dive (Track B, Part 3): What GitHub Copilot's Enterprise Terms Cover

*Background article for AI for Research, Issue 5. Reading time: about 12 minutes.*

*Checked against GitHub's public documentation on September 22, 2026. These terms change. If this article and the Bank's guidance disagree, follow the Bank.*

The September 17 session covered which data can go into which tool. This article looks at one tool many of us already use: GitHub Copilot on a Business or Enterprise plan. The question here is not "is Copilot safe?" It is: what does GitHub actually promise about your prompts, and which everyday habits fall outside that promise?

## 1. What GitHub promises

GitHub says it **does not use Copilot Business or Copilot Enterprise data to train AI models.** This is part of GitHub's Data Protection Agreement. That's why people on these plans don't see the "use my data for training" setting that individual users see: training is already off.

But this promise is only about training. It doesn't mean your prompt stays on your computer.

To give you a suggestion, Copilot sends your prompt to GitHub, and then on to the company that runs the model you picked. The prompt includes your question, the code around it, and other context Copilot adds. So both things are true at once: your prompt is not used for training, and it is sent to another company.

Sources:

- [Managing Copilot policies as an individual subscriber](https://docs.github.com/copilot/how-tos/manage-your-account/managing-copilot-policies-as-an-individual-subscriber) (the training promise for Business and Enterprise is in the note on that page)
- [Hosting of models for GitHub Copilot](https://docs.github.com/en/copilot/reference/ai-models/model-hosting)

## 2. How long prompts are kept depends on where you use Copilot, and on the contract

For Copilot Business and Enterprise **bought directly from GitHub**, the [product terms](https://github.com/customer-terms/github-copilot-product-specific-terms) say prompts are encrypted when sent, used to make the suggestion, and then deleted. They are not stored unless you allow it.

The same terms list cases where prompts **are** kept:

| Case | What GitHub says |
| --- | --- |
| **Copilot outside the editor** | Copilot in the command line (CLI) and similar tools keeps prompts to run the service |
| **A private custom model** | Prompts are kept to train that custom model |
| **Extensions and other custom setups** | The extension's own rules on keeping data apply |

If the Bank's licence was bought through Microsoft, the GitHub terms above don't apply. Microsoft's Product Terms do. Ask ITS which contract the Bank is on. Don't assume it's the GitHub one.

A Microsoft blog post describes a similar split: chat and suggestions in the editor are not kept, other Copilot tools keep prompts and suggestions for 28 days, and usage data (not your code) is kept longer. This is a summary, not the contract, so check it against the contract that actually applies. ([Microsoft Community Hub, 2025](https://techcommunity.microsoft.com/blog/azuredevcommunityblog/demystifying-github-copilot-security-controls-easing-concerns-for-organizational/4468193))

## 3. The model you pick can change the rules

Before you switch models in Copilot's model picker, read GitHub's hosting page. As of September 22, 2026:

- **Business and Enterprise data is not used for training**, for every model company GitHub lists.
- **OpenAI models:** OpenAI has agreed to keep no data, and says it does not train on business customers' data.
- **Most Claude models:** Anthropic has agreed to keep no data.
- **Claude Fable 5 and Claude Fable 5.1 are the exception.** By default, Anthropic keeps prompts and answers to run safety checks. An organisation can ask for a no-data-kept arrangement until the end of 2026. Even after that is approved, an admin still has to turn the model on. Some Anthropic features still in beta are also not covered by the no-data-kept agreement.
- **Gemini models** run on Google Cloud. Google promises not to train on these prompts. GitHub also says it temporarily stores (caches) prompts at Anthropic, Amazon, and Google to make answers faster. It doesn't say for how long.
- **Grok models:** xAI says prompts are not logged, not saved, not used for training, and only held in memory long enough to answer.
- **Inline suggestions** (the grey text that appears as you type) come from models run on Microsoft Azure for Business and Enterprise users. On Copilot Free, they run on a company called Fireworks AI.

What this means in practice:

1. Having Copilot Enterprise doesn't mean every model in the picker has the same rules. Fable 5 and 5.1 are the current exception.
2. Caching and safety checks aren't training. But they still mean a copy of your prompt exists somewhere other than your computer.

## 4. A personal account is a different product

Since April 24, 2026, GitHub can use data from **Copilot Free, Pro, Pro+, and Max** to train its models, unless you opt out. This includes prompts, suggestions, and code. Business and Enterprise are not affected.

Opting out only stops future collection. It doesn't cover data already collected.

If you log into a personal Copilot account on your Bank laptop, or open a Bank project in a personal account, the personal terms apply. What counts is which account and licence you use, not which computer.

Source: [GitHub changelog, March 25, 2026](https://github.blog/changelog/2026-03-25-updates-to-our-privacy-statement-and-terms-of-service-how-we-use-your-data/)

## 5. What is still up to you

GitHub's terms don't know how sensitive your files are. You do. Use the classification rules from the session.

Even with the right licence, these habits can put data outside the protections above:

- Pasting microdata, survey answers, or unpublished material from partners into chat, including into an approved coding agent.
- Turning on a model your admin hasn't reviewed, if the picker lets you.
- Installing an extension or MCP server that sends your code to another company. Extensions follow their own rules on keeping data.
- Using Copilot on the website, the mobile app, or the command line, and assuming the editor rules still apply.
- Assuming sensitive files are blocked from Copilot. Organisations *can* block files ("content exclusion"), but only the files an admin has listed. It doesn't automatically cover every sensitive file. ([Resources for getting approval of GitHub Copilot](https://docs.github.com/en/copilot/tutorials/roll-out-at-scale/govern-at-scale/resources-for-approval))

Content exclusion, audit logs, and which models are allowed are all set by admins. If you can't tell whether they're on, ask ITS. The fact that Copilot works doesn't tell you anything about these settings.

## 6. A ten-minute check

Do this on the account you use for Bank work. Don't paste project data into a chatbot to answer these questions.

1. On GitHub, go to your profile, then Copilot settings. If you see "Allow GitHub to use my data for AI model training," you're on a personal plan. Stop, and switch to the Bank licence before doing any project work.
2. If you don't see that setting, you're probably on Business or Enterprise. Check the plan page to be sure.
3. In your editor, check which model is selected for chat. If it's Claude Fable 5 or 5.1, assume Anthropic keeps your prompts until an admin confirms otherwise.
4. List where you used Copilot this month: editor, command line, github.com, mobile. The editor rules don't automatically cover the others.
5. Name one file you would never want in a prompt. Check what actually keeps it out: content exclusion, or just your own habit.

If you can't answer one of these, write to ai@worldbankgroup.org.

## What this article doesn't cover

It doesn't cover the Bank's data classifications, which tools are approved, or which models ITS has turned on. Those are set by Bank policy and were covered in the session. This article only covers what GitHub promises: no training on Business and Enterprise, but prompts still go to other companies, and how long they're kept depends on where you use Copilot, which model you pick, and your contract.
