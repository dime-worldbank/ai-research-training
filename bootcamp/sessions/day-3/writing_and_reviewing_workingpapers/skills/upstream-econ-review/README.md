# Upstream extracts: econ-paper-review-skill

Curated, verbatim reference files from
[econ-paper-review-skill](https://github.com/hanlulong/econ-paper-review-skill)
by Lu Han, under the PolyForm Noncommercial License 1.0.0 (see [LICENSE](LICENSE);
educational and public-research use — including WBG training — is expressly
permitted).

These files are the standalone-valuable review protocols, vendored for use by
`wb-paper-review` (in development):

| File | What it gives us |
| --- | --- |
| `gates/did.md`, `gates/iv.md`, `gates/rdd.md` | Method-specific review lenses: required design facts + conditional checks per identification strategy |
| `design-audit.md` | Generic research-design audit (all paper types) |
| `inference-audit.md` | Standard errors, clustering, power, multiple testing |
| `table-audit.md`, `figure-audit.md` | Exhibit-level checks (caption/notes/consistency) |
| `reader-claim-audit.md` | Claim inventory: does each claim stay within its evidence |
| `argument-evidence-audit.md` | Argument-map checks: does the logic chain hold |
| `comment-style.md` | How to write referee comments an author can act on |
| `design-presets.md` | Design-family presets referenced by the design audit |
| `research-integrity-audit.md` | Governance/integrity checks (referenced by other audits) |

Not vendored: the full product's workflow, output contracts, PDF ingestion,
scripts, and managed Python runtime — those only function inside the upstream
installer. For full referee-grade reviews, install the upstream skill itself.

Some files reference upstream machinery (`run.json`, canonical ledgers,
`candidates.json`, `scripts/*.py`) and occasionally other reference files not
vendored here. `wb-paper-review` uses these files for their checks and
questions, not their bookkeeping: ignore ledger/schema instructions, skip
references to files that are not present (note the skip in the review round
file), and recompute numbers with your own tooling rather than upstream
scripts.

Vendored 2026-09-21 from the upstream `main` branch. Do not edit these files;
build on top in `wb-paper-review/`.
