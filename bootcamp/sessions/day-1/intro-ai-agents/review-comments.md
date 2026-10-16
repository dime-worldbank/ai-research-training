## Review: Day 1 · Introduction to AI Agents

Reviewed `intro-ai-agents.qmd` on `main`, and the revised version on `origin/day-1-mj-review` (commits `794d21c`, `8a6a5b5`), checked against Maria's comments.

### 1. Branch status (read first)

- **`main` still has the old deck.** The `day-1-mj-review` branch is not merged. Several of Maria's comments are already addressed on that branch but not on `main` or the live site.
- **Committed `index.html` on the branch is stale.** It has no "Do Not Panic" slide, so it was not re-rendered after the qmd edits. Re-render and re-copy `index.html` before merging, otherwise the site will not show the new content.

### 2. Broken image

- **`main`:** `./img/reasoning-models.svg` is referenced on two slides, but only the Mermaid source `reasoning-models.mmd` exists. The SVG was never generated or committed. This is also why "But What About Reasoning Models?" shows content only in the right column, which is what Maria saw. It is a missing image, not a rendering glitch.
- **Branch:** this is fixed by turning the diagram into a Quarto `{mermaid}` chunk (`img/reasoning-models.qmd`) included with `{{< include >}}`. Please confirm it renders in the final HTML.
- **Legend:** the diagram's colours (blue = embedding, green = generative, grey = tool) are never explained. The earlier slide's columns do not use those colours.
- **Agents slide:** the reasoning diagram is reused above the calculator JSON. They have nothing to do with each other there. I would drop it from this slide, or replace it with an agent-specific diagram (prompt → agent → tools → files → response).

### 3. Maria's comments: answered or missing?

| Maria's comment | Status | Notes |
|---|---|---|
| Slides don't follow the scope slide; flow and takeaways unclear | **Open** | Scope slide is unchanged (still promises "examples from coding work"). The new "Do Not Panic" slide is not in the scope. No takeaway or summary slide. |
| "How does AI work" slides may not be needed; reasoning slide has only a right column | **Partly** | The image fix explains the right-column problem. The slides are all still there, and there is no stated takeaway for the section. |
| Start with the "LLMs cannot do math" slides | **Open** | Still after the model-types and reasoning slides. |
| Bring back the "prediction" slide from the older version | **Open** | Not restored. I found nothing in this folder's history beyond the "predicting the next word" bullet, so it may live in another file. |
| Better name for the "Tools" section | **Done** | Now "The tools really aren't new, but giving an AI access to them is." It works, but it is long for a divider slide. |
| Two near-identical definitions of agent | **Partly** | Now "An agent is *also* software that combines LLMs and tools… *But*…", which signals the difference. The two definitions still overlap, so consider defining a platform and an agent once, side by side. |
| Agents can modify files directly (vs. browser) | **Done** | New bullet. Wording is heavy ("typically has been given access… and granted autonomy"). Something like "Unlike a browser chat, an agent can read **and edit** files on your computer" would be clearer. |
| "Claude Code is an agent…" bullet: how does it relate to privacy? | **Open** | Unchanged, and the grammar is still wrong ("exclusively use"). Either connect it to privacy or delete it. |
| Split the mAI bullet into two | **Done** | Now two bullets, as suggested. |
| Mention Copilot is approved for Official Use / Public data, not confidential, or point to the afternoon session | **Open** | Not added. Also add that WB data should not go through personal Claude/other accounts. The ethics session is at 4:00 on the agenda. Please confirm who "Mer" is (the agenda lists Maria Reyes Retana for that slot). |
| Context window section is disconnected; needs a clear flow | **Open** | Only the slide move was done (below). No connective thread between slides. |
| Move "What is a context window" into that section | **Done** | |
| Add an example of good and bad context | **Open** | Nothing added. |
| Retitle to "Prompt Engineering is Different with Agents"; explain agents see files directly and you control what they see | **Partly** | Retitled "Agents Do Prompt Engineering For You". It says agents do the pasting, but never says you control and direct what they see. |
| Sessions: lead with the context-window intuition | **Mostly done** | New title "Each Session Represents a New Context Window", bullets 1–2 set it up. Fine. |
| Planning mode: belongs in a "working with agents" section, not context windows | **Open** | Still inside the context window section. The new closing paragraph (agent plus domain expert) is good, and could open a short "Working with agents" section. |

### 4. Other issues not raised by Maria

- **New typos on the branch:** "enusre" and "tasl" in the Planning Mode slide.
- **Typos still present:** "how Agents fits" → "fit"; "LLMs that is" → "are"; "amazed… the last year" → "in the last year"; "provides" → "provide"; "exclusively use" → "uses"; "error code" → "error message" (twice).
- **Overclaim:** the "LLMs Cannot Do Math" title. "Are Unreliable at Exact Math" is safer.
- **Math slide payoff:** the "Bob, Alice and Tom each have 7 apples" word problem ends with no point. Say it shows the model turning words into a calculation, or cut it.
- **JSON snippet:** it repeats on three slides (math, Agents, context window) with no label. Mark it "simplified illustration".
- **"Which Agent is Best?":**
  - It says "I will not attempt one", then calls Claude "a market leader". That may read as an endorsement.
  - It says Copilot "is what we will use", while Day 0 says Copilot *or* Claude Code. Pick one framing.
- **Context window slide:** "the AI will summarize earlier content" is oversimplified (tools differ). No numbers are given. A rough tokens-to-pages example would help.
- **Embedding models:** "Finding relevant *tasks*" is probably "passages". "Identifying gaps in available information" is unclear.
- **Planning Mode:** it does not say how to turn it on in Copilot. Participants need that at 3:15.
- **Timing:** the slot is 35 minutes (9:10–9:45) for roughly 20 content slides plus a quiz. That is tight.
- **Closing slide:** the old "Set Up GitHub Copilot… after the coffee break" slide is gone on the branch. That is fine, since the agenda changed. Make sure the Day 0 and Memory Files decks cover the Copilot prerequisite.

### 5. Suggested priority

1. Merge the branch, with a re-rendered `index.html`.
2. Fix the privacy slide (drop or connect the Claude Code bullet, add Official Use / confidential wording, personal-account warning).
3. Reorder: lead with "LLMs cannot do math", cut or condense the model-types slides, and add a one-line takeaway per section.
4. Add a good-vs-bad context example, and move Planning Mode into a "Working with agents" section.
5. Fix the typos.
