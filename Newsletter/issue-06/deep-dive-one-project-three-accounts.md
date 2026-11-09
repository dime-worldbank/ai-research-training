# Deep Dive (Track B, Part 4): One Project, Three Accounts

*Background article for AI for Research, Issue 6. Reading time: about 12 minutes.*

*Based on Impact Analytics' October 22 training, "Understand Claude Enterprise and Other WB AI Tools", and checked against the Bank's tool list on October 27, 2026. Approvals and prices change. If this article and Bank guidance disagree, follow the Bank.*

Impact Analytics' October 22 training on Claude Enterprise ended with a simple rule: pick the tool by the data, and when in doubt, use Claude Enterprise. That rule is easy to apply to a single task. It gets harder on a real project, where one week you are scanning raw survey data for phone numbers and the next you are fixing a merge that has nothing confidential in it. Most of us now have three accounts that can do both jobs: Claude Enterprise, GitHub Copilot Enterprise, and a personal Claude or ChatGPT subscription. This article is about running one project across all three without losing track of which one you are talking to.

## 1. Why three accounts, and not just Enterprise

Claude Enterprise is approved for Strictly Confidential files, and it is the only coding agent at the Bank with that level of approval. It is also the most expensive way to run Claude. Enterprise is billed per use, and running AI models is expensive. Consumer plans are flat-rate, with usage caps and different data terms, so the same twenty dollars goes much further there. Part of what the Enterprise price buys is the data protection.

GitHub Copilot sits in between. Its credits are cheaper than Enterprise, it is classified as Official Use, and it is well integrated with VS Code. For routine coding it is the right default. mAI is free to you (with a monthly cap on the most advanced models) and is approved for Strictly Confidential work, but it cannot open your files or run your code.

So the three accounts are not interchangeable. Each one is the cheapest tool that is still allowed for some part of your work. The job is to send each step of the project to the right one.

## 2. Sort the steps, not the project

Do not ask "is this project confidential?" Almost every project is, somewhere. Ask it of each step. Here is how a typical survey project splits:

| Step | What the tool would see | Use |
| --- | --- | --- |
| Scan raw data for direct and indirect identifiers | Names, phone numbers, GPS points | **Claude Enterprise** |
| Build a codebook and a small synthetic dataset | The real data, once | **Claude Enterprise**, or do it yourself |
| Write and fix cleaning and analysis code | Codebook and synthetic data only | **GitHub Copilot** |
| Run the code on the real data | The real data | **You**, outside any AI tool |
| Debug an error that only appears on the real data | The error message, maybe a few rows | **Claude Enterprise** |
| Draft a methods section from the pre-analysis plan | Public or Official Use text | **mAI** or Copilot |
| Draft a results memo with unpublished numbers | Unpublished estimates | **Claude Enterprise** or mAI |
| Learn a new package, write a generic function | Nothing from the project | Any tool, **personal** included |

Two things stand out. First, most of the coding happens in Copilot, with no real data in sight. Second, the real data touches an AI tool in only two or three steps, and in all of them the tool is Enterprise. That is the shape to aim for.

## 3. The codebook is the hinge

Everything in the Copilot column depends on one document: a codebook that describes the data without containing it. Variable names, types, what each variable means, how missing values are coded. Plus a synthetic dataset, fifty or a hundred rows of made-up values with the same structure, so the code has something to run on.

A codebook can leak. Before it leaves Enterprise, strip:

- value labels that name places, clinics, schools or people
- minimum and maximum values (a single household with 14 children is identifiable)
- category lists copied from the real data
- file paths that reveal the project, the country or the partner

Claude Enterprise is good at drafting both the codebook and the synthetic data. Ask it to, then read the result yourself before you move it anywhere. We are building a dedicated tool for this step. Until it is ready, Enterprise is the place to do it.

One more line to remember: de-identified is not the same as safe for every tool. Copilot is Official Use. A de-identified survey dataset is usually still Confidential. Give Copilot the codebook and the synthetic rows, not the de-identified data itself.

## 4. Moving a task down a level

Moving from a personal account up to Enterprise needs no precautions. Moving the other way does, because the conversation you had in Enterprise may be full of things the personal account should never see.

Never continue a conversation across accounts. Instead:

1. **Ask Enterprise for a handoff note.** The training suggested this prompt, and it works well as written:

   > Write a handoff note so another assistant can continue this task without access to the data. Include the goal, what has been done so far, the current problem, and the next steps. Describe datasets only by structure: generic variable names, types and what they represent. Do not include any data values, statistics, results, names of people, places or projects, or file paths. Use placeholders like `[dataset A]` where needed.

2. **Read the note.** Models follow instructions most of the time, not all of the time. You are the last check.
3. **Open a clean folder** with code only. No data, no logs, no `output/` folder, no notebook with saved results.
4. **Start a new session** in the other account and paste the note.

Before any of this, check which account is active. In Claude Code, type `/status`. In Claude Web or Desktop, look for the WB logo and your email at the bottom of the sidebar. The VS Code extension follows whichever account Claude Web is signed into, so if you switch, switch there first.

## 5. How data slips through anyway

The three cases from the training are worth keeping in mind, because in each one the person did nothing obviously wrong.

**You ask Claude to fix `clean.do`.** It runs the file. The do-file has a `list in 1/5` and a `summarize` in it. Five household records are now in the chat, and Claude never opened the data file.

**Claude cannot find the survey file** in the project folder, so it searches your user folder and finds the copy on OneDrive. You clicked Allow without reading the prompt.

**You ask why the results look off.** Claude opens `output/tables.tex` and a `.log` file with unpublished estimates. The code was clean. The outputs in the same folder were not.

The rule of thumb from the training: on a personal account, assume Claude can see anything in the folder, and anything your code prints.

## 6. Settings that make the personal account safer

None of this is needed on Enterprise. On a personal account, the training recommended four settings for Claude Code, all in `C:\Users\<you>\.claude\settings.json`:

- **Start in Manual mode, not Auto.** Claude asks before it acts. This is the main safeguard; the rest are backups.
- **Block reads outside the project folder.** By default Claude can read anything your Windows account can reach.
- **Deny data files and confidential folders**, for example `**/*.dta`, `**/*.csv`, `**/*.xlsx` and your OneDrive folder.
- **Block running Stata, R and Python.** Run scripts yourself. Otherwise a script can load the data and print it into the chat.

The training slides have a settings file you can copy ([Appendix B1](https://dime-worldbank.github.io/ai-research-training/sessions/ai-claude-enterprise/#/b1-personal-license-settings)). Two caveats. The list of blocked commands is a starting point, not a complete one, and approvals you click through without reading still get through.

There is a catch. That settings file belongs to your computer, not to an account. When you sign in to Enterprise, the same restrictions apply, and Claude can no longer read your data files or run your scripts. The fix is two profiles: one folder with normal settings for Enterprise, one with the strict settings for personal, each with its own login. You pick the account by picking the profile, and you never type `/logout` again. Setup takes about ten minutes and is described in [Appendix B2 and B3](https://dime-worldbank.github.io/ai-research-training/sessions/ai-claude-enterprise/#/b2-why-set-up-two-profiles) of the training slides. Anthropic documents the underlying feature as [logging in with multiple accounts](https://code.claude.com/docs/en/authentication).

## 7. When a tool runs out

Credits run out. When they do, the question is where to go next, and the answer depends on what the work touches.

| Your work involves | Start with | When that runs out |
| --- | --- | --- |
| Confidential data: chat, writing, documents | mAI or Microsoft 365 Copilot (no usage limit) | Claude Enterprise, when they can't do the task |
| Confidential data: code or files | Claude Enterprise | De-identify and move the coding to Copilot, or request more credits |
| Codebook or synthetic data only | GitHub Copilot | Personal Claude, with the settings above |
| Public data, generic code, learning | Personal Claude or Copilot | Switch between them |

Running out of credits is never a reason to move confidential data to a personal account or to Copilot. If you need more Enterprise credits, talk to your manager (your unit's BB is charged), agree on a spending limit, and submit the [eServices request](https://worldbankgroup.service-now.com/wbg/en/productivity-software-license-request?id=wbg_sc_catalog&sys_id=ebfd4d6693065210a2f6fd647aba10d7). Only actual usage is charged. Before you ask for hundreds of dollars more, though, check whether you are spending what you have well. Impact Analytics' November 5 training on using AI agents cost effectively was about exactly that; the [slides](https://dime-worldbank.github.io/ai-research-training/sessions/ai-cost-efficiency/) are online, and the next issue covers it.

## What this article doesn't cover

It doesn't cover which tools ITS has approved for which classification, or how to get a license. Those come from Bank policy and from [AI@WBG](https://ai.worldbankgroup.org/). It covers one thing: how to keep a project moving across three accounts without the confidential parts drifting into the cheap one.
