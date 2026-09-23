# Bootcamp PDFs

This folder is a build artifact of `../render-pdfs.ps1` — nothing here except this
README is version controlled - everything else is ignored.

The rendered content of this folder is then copied to the [Bootcamp Teams folder](https://worldbankgroup.sharepoint.com/teams/AI-EnabledResearchBootcamp-WBGroup/Shared%20Documents/Forms/AllItems.aspx?id=%2Fteams%2FAI%2DEnabledResearchBootcamp%2DWBGroup%2FShared%20Documents%2FAnnouncements%2FSession%20Materials&viewid=13a40481%2D0baa%2D426f%2D9199%2Dca0bea98ebac&FolderCTID=0x0120004A43097145FB58439F12F8848B758978)

See the respective instructions for "Creating a Presentation" and "Syncing the PDFs" depending on what you want to do. 

## What is needed for someone creating and including a presentation?

The script will include all `.qmd` files under `sessions/` that do not start with an underscore (`_`, e.g. `_template.qmd`). 

So if you do not want to include your presentation in theis workflow, give it a name starting with an underscore (`_`, e.g. `_my-topic.qmd`), and it will not be included. You can then add it to the teams folder manually. See the "Other content" section below.

### Name of PDF

It will use the same name and path for the generated PDF as the source `.qmd` file. So `sessions/day-1/my-topic/my-topic.qmd` will result in `pdfs/day-1/my-topic/my-topic.pdf`.

However, you can override the default name by adding a `render-meta.yml` file next to the `.qmd` with a custom name. Then the pdf path will be `pdfs/day-1/<name>/<name>.pdf` regardless of what the `.qmd` file is called. See example below

```yaml
name: 1-my-topic-long-name
```

This will allow you to have a longer name for the render file than the folder name in the repo. That also allows you to re-number the pdf files if the order in the agenda changes, without having to rename the folders and files tracked in the GitHub repository.

### Other content

This workflow does not delete anything in the Bootcamp Teams folder. It only adds or updates the files it generates from this repository.

If you have additional content (e.g., zipfiles or other session material) that should be added to the Teams folder manually.

If you have named your `.qmd` file with a leading underscore (`_`), you can add it to the Teams folder manually this way as well.


## What is needed for someone wanting to render and sync to Bootcamp Teams folder?

First test that the PDFs render properly. Nothing will be copied to the Bootcamp Teams folder until you have done more configuration. 

There is a risk we will get sync errors in the Bootcamp Teams folder if all of us runs this script all the time. Kristoffer can be the main person to run this file, but these instructions exists if anyone needs to step in as backup.

### Rendering PDFs
You first need to have the necessary tools installed to render the `.qmd` files into PDFs. This means having Quarto installed, plus either Google Chrome or Microsoft Edge (the script uses one of these, headlessly, to turn each slide deck into a PDF — no LaTeX installation is needed). 

Try running the `bootcamp/render-pdfs.ps1` file and work with GitHub Copilot to resolve any errors. This script will ask for a Y/N confirmation before anything is copied to the Bootcamp Teams folder, so it is safe to run the script for testing purposes, before you are ready to use it to sync files. 

Once the script runs, confirm that the PDFs have been correctly generated in the `bootcamp/pdfs` folder. If all files have been correctly rendered, you should see the expected PDF files organized by day and topic.

### Syncing to Bootcamp Teams Folder

You first need to sync the Bootcamp Teams folder linked above to your computer. Once you have done that, you need to create `bootcamp/sharepoint-path.local.txt` (git-ignored) in this repo containing the destination path, e.g.:

```text
C:\Users\WB123456\WBG\AI-Enabled Research Bootcamp - WB Group - Announcements\Session Materials
```

Without this file you will get a warning saying that the destination path for the Bootcamp Teams folder is not specified, and the sync step will be skipped.

Even after this file is created, you will still be prompted for a Y/N confirmation before any files are copied to the Bootcamp Teams folder. Once everything seems fine, feel free to run this script and confirm that the files may be copied to the Bootcamp Teams folder.


