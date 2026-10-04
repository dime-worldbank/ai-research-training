# Contributing to the bootcamp materials

How to add or update a session: slides, materials, and the agenda on the [bootcamp site](https://dime-worldbank.github.io/ai-research-training/bootcamp/).

## Workflow

1. Pull `main`, then create a branch for your change (`git switch -c day3-my-session`).
2. Make your changes and check them locally (see [Check before you push](#check-before-you-push)).
3. Push the branch and open a pull request into `main`. Describe what changed and add a screenshot if you touched the site.
4. Once merged, GitHub Pages rebuilds the site from `main` within a few minutes.

Don't push directly to `main`.

## Add a session deck

1. Copy [`sessions/template/_presentation.qmd`](sessions/template/_presentation.qmd) to `sessions/<day>/<session-topic>/<session-topic>.qmd`. At that depth, the template's `../../../` paths to logos and the theme work without changes.
2. Keep `embed-resources: true` in the format block, so the deck renders to a single self-contained HTML file.
3. Put images in an `images/` folder next to the `.qmd`.
4. Put anything participants download in a `materials/` folder next to the `.qmd`.

## Publish a deck on the site

The site serves files committed to `main`; nothing is rendered automatically.

1. Render the deck to `index.html` in its session folder and commit that file:

   ```bash
   quarto render my-session.qmd --output index.html
   ```

2. In [`../_data/bootcamp.yml`](../_data/bootcamp.yml), give the session a `link` to its folder, and optionally a `materials` list (see below).
3. Don't add the session to a README schedule: the agenda lives only in `_data/bootcamp.yml`. `bootcamp/sessions/<day>/` redirects to the day page on the site.

**After any later edit to the `.qmd`, re-render `index.html` and commit it**, or the site keeps showing the old version.

### Session entries in `_data/bootcamp.yml`

```yaml
  - time: 11:30 – 12:15
    title: Use AI to draft and get feedback on working papers
    hands_on: true
    lead: Impact Analytics
    link: "/bootcamp/sessions/day-3/writing_and_reviewing_workingpapers/"
    materials:
    - label: "Skills"
      url: "https://github.com/dime-worldbank/ai-research-training/raw/refs/heads/main/bootcamp/sessions/day-3/writing_and_reviewing_workingpapers/materials/skills.zip"
    - label: "Companion deck"
      url: "/bootcamp/sessions/day-3/ai-skills-slides/"
```

- `link` and `materials` URLs can be full URLs or site paths starting with `/`; site paths get the site prefix automatically.
- `.zip` files are not published on the site, and `.md` files are served as raw text, so link those through GitHub (`github.com/.../raw/refs/heads/main/...` for downloads, `github.com/.../blob/main/...` to view).
- Materials show as small buttons, so keep each label to one or two short words (e.g. "Exercise", "Skill", "Demo"). Add 🔒 to the label for links that need a World Bank login (internal repos, mAI).

## Publish a deck to Teams

Add the `.qmd` to [`sessions/push-to-teams.yml`](sessions/push-to-teams.yml), then run [`render-and-push-html.ps1`](render-and-push-html.ps1) on a machine with the Bootcamp Teams folder synced. See [Publish session presentations to Teams](README.md#publish-session-presentations-to-teams).

## What gets committed

The repo's `.gitignore` ignores everything by default and lists the file types it allows. Watch out for:

| File | Committed? | What to do |
|---|---|---|
| `.qmd`, `.md`, `.py`, `.R`, `.do`, `.png`, `.zip` | Yes | Nothing |
| `index.html` in a session folder | Yes | Re-render after each edit |
| Any other `.html` | No | Rendered output, ignored on purpose |
| `.jpg`, `.svg`, `.pdf`, `.csv`, `.tex` | No | Convert images to `.png`, or `git add -f` the specific files |
| `.pptx`, source decks, drafts | No | Keep them out of the repo |

Before committing, run `git status` and check that nothing is missing (an image your deck needs) or extra (a draft, data, credentials).

Never commit data that is not public, personal data, or anything your data agreement does not allow. The Day 1 classification rules apply to the repo too.

## Check before you push

- **Deck:** `quarto preview my-session.qmd` and click through every slide at full screen. Check that nothing runs past the bottom of a slide.
- **Links:** open every link a slide or the agenda points to.
- **Site (optional, for changes to `_data/`, `_includes/`, `_layouts/` or `assets/`):** build the site locally with the same gem set GitHub uses. This needs Ruby 3.1 or older; newer Ruby needs extra gems (`csv`, `base64`, `bigdecimal`, `logger`) and a small compatibility patch.

  ```bash
  # in a folder outside the repo, with a Gemfile containing:
  #   gem "github-pages", group: :jekyll_plugins
  #   gem "webrick"
  bundle install
  PAGES_REPO_NWO=dime-worldbank/ai-research-training \
    bundle exec jekyll serve --source /path/to/ai-research-training
  ```

  Then open `http://localhost:4000/ai-research-training/bootcamp/`. Warnings about `{{< include >}}` in `.qmd` files are harmless: they are Quarto shortcodes, not Jekyll.
