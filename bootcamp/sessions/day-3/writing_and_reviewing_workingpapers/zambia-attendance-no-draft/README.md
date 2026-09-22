# Zambia School Meals — NO draft (setup + write-flow demo)

Fictional project for the bootcamp. Same study as the `with-draft` version,
but **no paper exists yet** — only the analysis outputs, a concept note, and
materials in `wb-paper/references/`. There is **no `wb-paper/profile.md`**:
the point is to run the full pipeline from scratch.

Unlike the with-draft version, this project is "healthy": clean tables with
self-contained captions, a complete bibliography. The exercise is production,
not defect-hunting.

## Suggested test script

```
1. git init && git add -A && git commit -m "baseline"
2. Invoke wb-paper-setup (standard route).
   - Part R should ask about the exemplar excerpt (positive/), the
     overwrought excerpt (negative/), the PRWP guidelines (guidelines/),
     and the referee report (feedback/).
   - Part 2: answer the positioning block from concept-note.md § "What we
     found" — in your own words; that's the point.
   - Check the playback gate offers two rosters and flags inferences.
3. Invoke wb-paper-write → Outline mode (expect two variants + writing order).
4. Draft mode: Results section first (outputs are rich there).
   - Expect clarifying questions, then outline → bullets → prose,
     numbers only from outputs/, [AUTHOR:] markers elsewhere.
5. Optionally run wb-paper-review on the AI draft — it should warn that the
   section is unedited AI text (human-touched: no).
6. Check wb-paper/log.md and git log after each step.
```

Everything here is fictional training material.
