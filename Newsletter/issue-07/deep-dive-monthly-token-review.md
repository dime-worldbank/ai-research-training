# Deep Dive (Track C, Part 2): The Monthly Token Review

*Background article for AI for Research, Issue 7. Reading time: about 12 minutes.*

*Based on Impact Analytics' November 5 training, "Using AI Agents Cost Effectively", and the session of the same name at the October AI-Enabled Research Bootcamp. Prices and limits change; check the current ones before you quote them.*

The training gave three habits: use the smallest model that does the job, keep a memory file so the agent does not re-discover your project on every request, and start a new session for every new task. Those habits cover most of the waste. What they do not do is tell you whether they are working. For that you need to look at your own usage now and then, the way you would look at a field budget. This article is a routine for doing that once a month, in about half an hour, with the numbers your tools already give you.

## 1. Why a routine, and not just good intentions

Three reasons.

First, waste is invisible at the moment it happens. A session that has grown to 150,000 tokens of context does not feel any different from a fresh one. The bill is the same whether you are using those tokens or dragging them along.

Second, the tools change under you. A model that was the right default in September may be two generations old by December, and a cheaper one may now handle the same task. Nobody will tell you.

Third, Enterprise credits are a line in your unit's budget. When you ask for more, the first question will be what you did with the last allocation. "Mostly debugging, I think" is not a great answer. A monthly note is.

## 2. Where the numbers are

You do not need a spreadsheet of every request. Three places give you enough.

**Claude usage page.** On claude.ai, Settings, then Usage ([direct link](https://claude.ai/new#settings/usage)). This shows how much of your allocation is gone and when it resets. It covers Claude Web, Desktop and the VS Code extension on the same account.

**Claude Code `/cost` and `/context`.** Inside a Claude Code session, `/cost` reports what the current session has spent so far, and `/context` shows what is filling the context window: your files, the memory file, tool results, conversation. If most of it is tool results from three tasks ago, that is the trailer full of old groceries from the training slides.

**The Copilot context meter.** GitHub Copilot's chat panel in VS Code shows how full the current context window is. The Bootcamp version of the training suggested a reading of it at the end of a task: under 5% full and you probably used a bigger model than you needed; over 95% and details were probably lost along the way.

## 3. The half-hour review

Do this at the end of each month, on a day you are not in a hurry.

**Step 1. Write down three numbers (5 minutes).** Credits used this month, credits left, and the date of the reset. If you have Copilot premium requests as well, note how many are left. Keep the numbers in a plain text file in your home folder, one line per month. After three months you will have a trend, which is the only thing that makes any single month's number meaningful.

**Step 2. Name your five most common tasks (5 minutes).** Not "coding". Things like: fix a Stata error, write a cleaning script from a codebook, draft a results memo, proofread a Quarto slide, explain a package's syntax. Be honest about which of them you did most.

**Step 3. Assign each task a model (10 minutes).** For each of the five, write the model you have been using and the one you think would be enough. The test from the training: proofreading a paragraph does not need the largest model, and neither does explaining syntax or renaming variables. Reading a 40-file project to find a merge bug probably does. Pick one task where you are going to try the smaller model next month, and write it down so you remember to.

**Step 4. Check the memory file (5 minutes).** Open the project `AGENTS.md` or `CLAUDE.md` for the project you spent the most tokens on. Is the stack listed? The folder layout? The thing the agent always gets wrong? If the agent has had to rediscover any of this in the last month, add it now. Ask yourself the opposite question too: is there anything in the memory file the agent no longer needs, because that part of the project is finished? Every line is loaded on every request.

**Step 5. Count your sessions (5 minutes).** Scroll your Claude Code or Copilot history. How many sessions did you start this month, and how many tasks did you do? If the second number is a lot bigger than the first, you have been reusing sessions. The training slides put it plainly: on the tenth task in one session, you pay again for the previous nine. Resolve to use the plus button.

That is the review. The output is a dated text file with three numbers, five tasks, one experiment for next month, and a memory file that is a bit more accurate than it was.

## 4. What a good month looks like

It is tempting to measure success as "spent less". That is the wrong target. A good month is one where the expensive tokens went to the hard tasks and the routine tasks ran on cheap ones.

Some things that count as good:

- Enterprise credits were spent on work that touched confidential data or needed a big context, not on proofreading.
- The experiment from last month gave a verdict. Either the smaller model handled the task, and it is now the default, or it did not, and you know why.
- The memory file got shorter in one place and longer in another.
- You started more sessions than last month and finished the same amount of work.

And some things that are warning signs:

- Credits ran out mid-month and you did not know until the tool told you.
- The same correction appears in several sessions. ("No, we use `reghdfe`, not `areg`." Put it in the memory file.)
- A session hit the context limit and the agent started forgetting earlier instructions. That is the over-95% case: a task too big for one session, which should have been split.

## 5. For teams

If you run a team, do the same review together once a quarter, with each person's five tasks on one page. Two things usually fall out of it. First, people are using different models for the same task, which means at least one of them is over-paying or under-serving. Second, the "things it always gets wrong" lists overlap, and the overlap belongs in the shared memory file, not in five personal ones.

This is also the moment to decide whether something has become a skill. If three people have independently written a prompt for the same recurring job, that prompt is a skill waiting to be written down. Impact Analytics' December 3 training, Making Your Workflows AI-Enabled, is about exactly that.

## 6. Requesting more credits

If after a review you still need more, you are in a good position to ask. Talk to your manager, agree a spending limit, and submit the [eServices request](https://worldbankgroup.service-now.com/wbg/en/productivity-software-license-request?id=wbg_sc_catalog&sys_id=ebfd4d6693065210a2f6fd647aba10d7). Bring the text file. "I used 80% of the allocation on two projects with confidential survey data, moved proofreading to Copilot, and still ran out in week three" is a request that gets approved.

## What this article doesn't cover

It does not cover prices per token, which change too often to print, or the Bank's allocation policy, which is set by ITS. It covers one habit: look at your own numbers once a month, and change one thing.
