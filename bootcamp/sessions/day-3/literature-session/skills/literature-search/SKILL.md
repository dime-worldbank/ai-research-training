---
name: literature-search
description: Search the academic literature through the free OpenAlex and Semantic Scholar APIs, from the terminal, with a bundled script. Use whenever the user wants to find papers on a topic, map a literature, find the papers everyone in a field cites, check whether their research idea has already been done (nearest neighbours of a paper), list papers citing a paper, pull a paper's abstract and details, or verify that a reference or citation is real before it goes into a draft. Also use when an agent is writing a related-work section, a literature review, or a bibliography and needs real, checkable sources, even if the user does not mention OpenAlex or Semantic Scholar by name.
---

# Literature search (OpenAlex + Semantic Scholar)

`scripts/lit.py` queries two open scholarly databases and prints Markdown tables
with a DOI link for every paper. It needs only Python 3 (standard library), no
installs and no account. Free API keys are optional (see "API keys" below).

- **OpenAlex**: about 250 million works, good metadata, references and citations.
- **Semantic Scholar**: its own index plus embedding-based recommendations.

Results are leads for the user to open and read. A search engine cannot tell
whether a paper actually answers the user's question, so the job of this skill
is to find candidates quickly and honestly report what was found, not to
decide relevance on the user's behalf.

## Commands

Run from the skill folder (or give the full path to `scripts/lit.py`):

| The user wants to… | Command |
|---|---|
| find papers on a topic | `python3 scripts/lit.py search "QUERY" [--since 2018] [--sort relevance\|cited\|recent] [--n 15]` |
| know which papers everyone in the field cites | `python3 scripts/lit.py core "QUERY" [--pool 200] [--n 15]` |
| check whether their idea has been done | `python3 scripts/lit.py similar DOI` on the closest paper they know |
| see who built on a paper | `python3 scripts/lit.py citing DOI [--sort cited\|recent]` |
| read one paper's details and abstract | `python3 scripts/lit.py paper DOI` |
| check a reference is real | `python3 scripts/lit.py verify "full reference or title or DOI"` |

Useful flags: `--n` sets how many results are shown in total, `--abstracts` prints abstracts under the table (use it when you
must judge relevance), `--json` gives machine-readable output, `--oa-only`
restricts a search to open-access papers, `--source openalex|s2` queries one
database only. IDs can be DOIs, `doi.org` URLs, OpenAlex IDs (`W…`) or
Semantic Scholar paper IDs.

## How each command works (so you can explain the results)

- **search**: OpenAlex matches *all* query words in title and abstract;
  Semantic Scholar uses its own relevance ranking. Results are merged and
  deduplicated by DOI; the "Found in" column shows OA, S2 or both.
- **core**: takes the top `--pool` OpenAlex papers on the topic and counts which
  works they reference most. The "Cited by pool" column is the count: this
  surfaces the field's foundational papers, which are often older reviews.
- **similar**: two neighbour lists. *Shared refs* = papers whose reference
  lists overlap most with the seed paper, weighted so that sharing a niche
  study counts more than sharing a famous methods paper. *S2 recommended* =
  Semantic Scholar's embedding-based recommendations, which favour recent papers.
- **verify**: resolves a DOI, otherwise finds the title inside the reference
  text and matches it in both databases. It reports FOUND (title match ≥ 0.9),
  UNCERTAIN (≥ 0.7) or NOT FOUND, and for a found paper checks the year, the
  first author's surname and volume/pages against the record. Pass the full
  reference as one quoted string. FOUND means the paper exists; a ✗ in the
  details means the reference has an error to fix. Before calling a reference
  fabricated, look at the closest records it lists and try the DOI or the bare
  title once more: a NOT FOUND is strong evidence, not proof.

## Working well with it

**Write queries like a database, not like a chat.** OpenAlex requires every
word to appear, so a long natural-language question returns very few hits.
Use 3–6 key terms (`community health workers decision support`), then run
variants with synonyms (`lay health workers`, `mHealth`, `clinical decision
support`) and report how the hit counts change. The hit counts are part of the
answer: "39 hits for X, 1,200 for Y" tells the user how specific their framing is.

**Read before you recommend.** Rankings are by keyword match and citations, so
off-topic papers appear near the top. Before calling a paper relevant, run with
`--abstracts` or `paper DOI` and base the judgement on the abstract. Say which
papers you checked and which you are passing on unread.

**For "has someone done this?"**, combine three moves: a narrow `search` with
`--sort recent`, `similar` on the closest known paper, and `citing` on that
paper with `--sort recent`. Report the closest matches with how they differ
from the user's question (setting, population, method, outcome). Recent trial
protocols and registrations matter here: a protocol is exactly what a referee
will point to.

**Never cite something you have not seen in the output.** Every reference you
give the user must come with the DOI or link the script returned. If the user
or a draft contains references, run `verify` on each one and flag anything
UNCERTAIN or NOT FOUND instead of silently fixing it. Fabricated citations are
the most damaging failure in AI-assisted writing.

**Record what you did.** Searches change as databases update. When results feed
into a document, note the query, the database and the date (the script prints
the date) so the search can be rerun.

## API keys (tell the user about this)

Both databases work without keys, but the free tiers are shared and slow down
under load. The first time you use this skill in a session, and whenever the
script prints a rate-limit note (HTTP 429, "Semantic Scholar skipped"), tell the
user they can add free keys and how:

1. **Semantic Scholar**: request a free key at
   https://www.semanticscholar.org/product/api#api-key-form (arrives by email).
2. **OpenAlex**: create a free account and API key at https://openalex.org
   (raises the daily budget about 10×; see help.openalex.org, "Rate limits and
   authentication").
3. Make the keys available to the script as environment variables, e.g. in
   `~/.zshrc` or `~/.bashrc` on macOS/Linux:
   ```bash
   export S2_API_KEY="your-semantic-scholar-key"
   export OPENALEX_API_KEY="your-openalex-key"
   ```
   then open a new terminal (or `source ~/.zshrc`). On Windows:
   `setx S2_API_KEY "your-key"` and `setx OPENALEX_API_KEY "your-key"`, then
   restart the terminal. Keys are personal: never write them into project
   files, scripts or commits.

The script picks the keys up automatically; nothing else changes.

## Limits to tell the user about

- Coverage is broad but not complete: grey literature, working papers, some
  non-English and LMIC journals, and very recent preprints can be missing.
  For a systematic review / meta-analysis, this skill helps scope a search; it
  does not replace a documented database search.
- Without a key, Semantic Scholar often returns HTTP 429 (rate limited). The
  script retries, then continues with OpenAlex only and says so: report that
  the Semantic Scholar half is missing rather than presenting partial results
  as complete, and point the user to "API keys" above.
- `verify` cannot check full author lists, issue numbers or journal names in
  detail; a FOUND reference can still have small errors.
- Citation counts differ between the two databases; the table shows the higher.
