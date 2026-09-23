# Bootcamp PDFs

This folder is a build artifact of `../render-pdfs.ps1` — nothing here except this
README is version controlled.

## How it's populated

Running `render-pdfs.ps1` from `bootcamp/` recursively renders every `.qmd` under
`sessions/` (skipping files that start with `_`, e.g. the template) and mirrors each
PDF here as `pdfs/<day>/<session>/<name>.pdf`.

By default `<name>` is the `.qmd` file's base name. To override it, add a
`render-meta.yml` file next to the `.qmd` with:

```yaml
name: my-custom-pdf-name
```

## Syncing to SharePoint

To also copy this folder to a SharePoint-synced folder on your machine, create
`bootcamp/sharepoint-path.local.txt` (git-ignored) containing the destination path,
e.g.:

```
C:\Users\you\OneDrive - World Bank Group\Bootcamp Slides
```

That folder may also contain PPT/PDF files from external teams unrelated to this
repo, so the script always asks for Y/N confirmation before copying, and only
adds/overwrites the files it generates — it never deletes or wipes the destination.
If no `sharepoint-path.local.txt` is found, the sync step is skipped with a warning.
