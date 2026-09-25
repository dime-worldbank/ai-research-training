# Deep Dive (Track B, Part 3): Working Inside the Enterprise Boundary

*Background article for AI for Research, Issue 5. Reading time: about 12 minutes.*

*Checked against GitHub's public documentation on September 22, 2026. Vendor terms change. If this article and the Bank's approved-tool guidance disagree, follow the guidance from the September 17 session and ITS.*

The September 17 session covered which data may go into which tool. This article covers one tool researchers already have open: GitHub Copilot on a Business or Enterprise plan. The useful question is narrower than "is Copilot safe?" It is: what does GitHub publish about training and retention, and which of your habits fall outside that publication?

## 1. The sentence that is actually true

GitHub's current documentation states that **GitHub does not use Copilot Business or Copilot Enterprise customer data to train AI models.** Those customers' data is covered by GitHub's Data Protection Agreement, which prohibits that use without customer authorization. The opt-out control shown to individual subscribers is not shown on these plans, because the training use is already off.

That sentence is about model training. It is not a statement that your prompt stays on your laptop.

To produce a suggestion, Copilot sends the prompt — the instruction, the surrounding code, and other context it includes — to GitHub and then to the host for the model you selected. "Not used for training" and "sent to a model host" are both true of the same request.

Sources:

- [Managing Copilot policies as an individual subscriber](https://docs.github.com/copilot/how-tos/manage-your-account/managing-copilot-policies-as-an-individual-subscriber) (the Business/Enterprise training statement is in the note on that page)
- [Hosting of models for GitHub Copilot](https://docs.github.com/en/copilot/reference/ai-models/model-hosting)

## 2. Retention depends on the surface and the contract

For Copilot Business and Copilot Enterprise **purchased from GitHub**, the [product-specific terms](https://github.com/customer-terms/github-copilot-product-specific-terms) say that prompts are encrypted in transit, used to generate suggestions, deleted once the suggestion is generated, and not stored at rest unless you allow it.

The same terms list cases where prompts **are** retained:

| Case | What GitHub says |
| --- | --- |
| **Tools outside the editor** | Copilot in the CLI and similar non-editor tools retains prompts in order to provide the service |
| **A private custom model** | Prompts are retained to fine-tune that model |
| **Custom data handling** | Third-party extensions and other alternative settings follow the retention of that configuration |

If the license is bought through Microsoft, those GitHub product terms do not apply. Microsoft Product Terms do, including the terms for GitHub offerings. World Bank staff should confirm which contract they are under with ITS, rather than assuming the GitHub customer terms are the Bank's contract.

A separate Microsoft write-up of enterprise controls describes a related split: IDE chat and completions are not retained; other Copilot surfaces retain prompts and suggestions for 28 days; engagement metadata is kept longer and is not the same thing as your code. Treat that as a secondary summary and check it against the contract you are actually on. ([Microsoft Community Hub, 2025](https://techcommunity.microsoft.com/blog/azuredevcommunityblog/demystifying-github-copilot-security-controls-easing-concerns-for-organizational/4468193))

## 3. The model you pick can change the promise

The hosting page is the list to read before you switch models in the picker. As published on September 22, 2026:

- **Business and Enterprise customer data is not used to train models**, across the hosts GitHub documents.
- **OpenAI models** in Copilot are covered by a zero-data-retention agreement with OpenAI. OpenAI's stated commitment on that page is that it does not train on customer business data.
- **Most Claude models** in Copilot are covered by a zero-data-retention agreement with Anthropic.
- **Claude Fable 5 and Claude Fable 5.1 are the exception.** By default, Anthropic retains prompts and outputs to run safety classifiers. An enterprise can request a time-bound zero-retention arrangement through the end of 2026. Approval does not turn the model on. An admin still has to enable it. Some Anthropic features in beta, including tool search via the Messages API, are also outside the default zero-retention agreement.
- **Gemini models** are hosted on Google Cloud. Google commits not to train on those prompts. GitHub also documents prompt caching on Anthropic, Amazon Bedrock, and Google Cloud to reduce latency. The hosting page does not state how long a cache entry lives.
- **Grok models** are described under an xAI zero-data-retention policy: not logged, not saved to disk, not used for training, held in memory only long enough to answer.
- **Inline suggestions** (ghost text and next-edit suggestions) on Business and Enterprise are powered by models hosted on Azure. On Copilot Free they are hosted on Fireworks AI.

Two practical consequences:

1. "We have Copilot Enterprise" does not mean every model in the picker has the same retention terms. Fable 5 and 5.1 are the current documented exception.
2. Prompt caching and safety-classifier retention are service operations. They are still a copy of prompt content outside your machine, for a purpose other than training a foundation model.

## 4. A personal account is a different product

From April 24, 2026, GitHub may use interaction data from **Copilot Free, Pro, Pro+, and Max** — prompts, suggestions, code snippets, and surrounding context — to train and improve models, unless the user opts out. Business and Enterprise licenses are excluded from that change.

Opting out stops collection from that point forward. It does not describe data already collected.

A personal Copilot login on a Bank laptop, or a Bank repo opened in a personal account, follows the consumer terms. The enterprise boundary is the license and the account, not the building.

Source: [GitHub changelog, March 25, 2026](https://github.blog/changelog/2026-03-25-updates-to-our-privacy-statement-and-terms-of-service-how-we-use-your-data/)

## 5. What you still decide

Published enterprise terms do not classify your files. You do, using the sensitivity tiers and permissible-use rules from the session.

A few habits sit outside the "my IDE is on the enterprise plan" story even when the license is correct:

- Pasting microdata, respondent text, or unpublished counterpart material into chat, including into a coding agent that is otherwise approved.
- Turning on a model your enterprise admin has not reviewed, if the picker lets you.
- Installing an extension or MCP server that sends repository contents to a third party. The product terms say custom extensions follow that extension's retention.
- Using Copilot on the website, mobile app, or CLI and assuming the IDE retention rule applies there.
- Relying on content exclusion without checking that it is configured. Enterprises *can* exclude files from Copilot. Exclusion applies to paths an admin has set. It does not automatically cover every sensitive file in a repo. ([Resources for getting approval of GitHub Copilot](https://docs.github.com/en/copilot/tutorials/roll-out-at-scale/govern-at-scale/resources-for-approval))

Content exclusion, audit logs, and model allow-lists are admin controls. If you cannot see whether they are on, that is a question for ITS, not a fact to infer from a successful suggestion.

## 6. A ten-minute check

Do this on the account you actually use for Bank work. Do not paste project data into a chatbot to answer the questions.

1. Open GitHub → your profile → Copilot settings. If you see "Allow GitHub to use my data for AI model training," you are on an individual plan. Stop and switch to the Bank license before any project work.
2. If that setting is absent, you are likely on Business or Enterprise. Confirm with the plan page rather than with the absence of a toggle alone.
3. In the editor, note the model selected for chat. If it is Claude Fable 5 or 5.1, treat retention as the Fable exception until an admin confirms the zero-retention arrangement.
4. List the surfaces you used this month: IDE, CLI, github.com chat, mobile. The IDE rule does not automatically cover the others.
5. Name one file you would not want in a prompt. Check whether content exclusion, or your own habit, actually keeps it out.

Bring any row you cannot answer to the September 24 DECRG session, or to the contact path from the September 17 session.

## What this article does not settle

It does not state the World Bank's data-sensitivity tiers, which tools are approved, or which models ITS has enabled. Those decisions live in the session materials and in Bank policy. This article is the vendor layer underneath one common coding assistant: training is off on Business and Enterprise, prompts are still sent to a host, and the host's retention depends on the surface, the model, and the contract.
