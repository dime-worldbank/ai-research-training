# Publish Session HTML

The `render-pdfs.ps1` script keeps its legacy filename, but now renders and publishes standalone HTML presentations only. It does not create PDFs or require Chrome or Edge.

## Choose presentations

The day-grouped [`sessions/push-to-teams.yml`](../sessions/push-to-teams.yml) file is the complete publication allowlist. It contains paths to `.qmd` files relative to their day folder. Only listed files are rendered and copied; adding a presentation elsewhere does not publish it.

Each listed presentation must embed its resources so the HTML works as a single file in Teams. Set:

```yaml
format:
	bootcamp-revealjs:
		embed-resources: true
```

## Choose the Teams name

The script uses the `name` property in a `render-meta.yml` next to the `.qmd`, when present, for both the Teams session folder and HTML filename. For example, `name: 1-my-topic` publishes to `<day>/1-my-topic/1-my-topic.html`. Without a `name` property, it uses the `.qmd` basename for both.

## Render and publish

Install Quarto, then run `bootcamp/render-pdfs.ps1`. The script renders each allowlisted `.qmd` to its sibling `.html`, verifies the outputs, and then asks whether to copy the listed HTML files to Teams.

To enable copying, sync the Bootcamp Teams folder to your computer and create the git-ignored `bootcamp/sharepoint-path.local.txt` file with its local path, for example:

```text
C:\Users\WB123456\WBG\AI-Enabled Research Bootcamp - WB Group - Announcements\Session Materials
```

The script copies only the allowlisted HTML files to `<Teams>/<day>/<name>/<name>.html`. It updates matching files but does not delete or alter other content in the Teams folder. Without the local path file, the script renders the HTML and skips copying.


