param(
    [string]$SourceRoot = "sessions"
)

$ErrorActionPreference = "Stop"
$projectRoot = $PSScriptRoot
$pdfsRoot = Join-Path $projectRoot "pdfs"
$sharePointConfigPath = Join-Path $projectRoot "sharepoint-path.local.txt"

$chromeCandidates = @(
    "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
    "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe",
    "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
)
$browser = $chromeCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1

if (-not $browser) {
    throw "Chrome or Edge was not found. Install one of these browsers to create PDFs."
}

$sourceRootPath = Join-Path $projectRoot $SourceRoot

# Any .qmd whose name starts with "_" is a template/partial, not a presentation to render.
$documents = Get-ChildItem $sourceRootPath -Recurse -Filter "*.qmd" |
    Where-Object { $_.Name -notlike "_*" } |
    Sort-Object FullName

if (-not $documents) {
    throw "No .qmd files found under '$SourceRoot'."
}

Write-Host "Discovered $($documents.Count) presentation(s) to render:"
foreach ($document in $documents) {
    Push-Location $projectRoot
    $relativeDocument = Resolve-Path -Relative $document.FullName
    Pop-Location
    Write-Host "  $relativeDocument"
}

$browserProfile = Join-Path $env:TEMP ("quarto-pdf-" + [Guid]::NewGuid())
New-Item -ItemType Directory -Path $browserProfile | Out-Null

try {
    foreach ($document in $documents) {
        Push-Location $projectRoot
        $relativeDocument = Resolve-Path -Relative $document.FullName
        Pop-Location
        Write-Host "Rendering $relativeDocument"
        & quarto render $relativeDocument
        if ($LASTEXITCODE -ne 0) {
            throw "Quarto failed to render $relativeDocument."
        }

        $htmlPath = [IO.Path]::ChangeExtension($document.FullName, ".html")
        $pdfPath = [IO.Path]::ChangeExtension($document.FullName, ".pdf")
        $htmlUrl = ([Uri]$htmlPath).AbsoluteUri + "?print-pdf"

        & $browser `
            --headless `
            --disable-gpu `
            --no-pdf-header-footer `
            --run-all-compositor-stages-before-draw `
            --virtual-time-budget=3000 `
            "--user-data-dir=$browserProfile" `
            "--print-to-pdf=$pdfPath" `
            $htmlUrl
        if ($LASTEXITCODE -ne 0) {
            throw "Browser failed to create $pdfPath."
        }

        # Mirror into bootcamp/pdfs/<day>/<session>/, honoring a sibling render-meta.yml name override
        $sessionFolder = $document.Directory
        $relativeToSourceRoot = $sessionFolder.FullName.Substring($sourceRootPath.Length).TrimStart('\', '/')
        $day = ($relativeToSourceRoot -split '[\\/]')[0]
        $sessionFolderName = $sessionFolder.Name

        $pdfName = [IO.Path]::GetFileNameWithoutExtension($document.Name)
        $metaPath = Join-Path $sessionFolder.FullName "render-meta.yml"
        if (Test-Path $metaPath) {
            $nameLine = Get-Content $metaPath | Where-Object { $_ -match '^\s*name\s*:\s*(.+)$' } | Select-Object -First 1
            if ($nameLine -match '^\s*name\s*:\s*(.+)$') {
                $pdfName = $Matches[1].Trim().Trim("'`"")
            }
        }

        $destinationDir = Join-Path (Join-Path $pdfsRoot $day) $sessionFolderName
        New-Item -ItemType Directory -Path $destinationDir -Force | Out-Null
        $destinationPdf = Join-Path $destinationDir "$pdfName.pdf"
        Copy-Item -Path $pdfPath -Destination $destinationPdf -Force
    }
}
finally {
    if (Test-Path $browserProfile) {
        Remove-Item $browserProfile -Recurse -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "Created $($documents.Count) PDF files."

if (Test-Path $sharePointConfigPath) {
    $sharePointPath = Get-Content $sharePointConfigPath | Where-Object { $_.Trim() } | Select-Object -First 1
}
else {
    $sharePointPath = $null
}

if (-not $sharePointPath) {
    Write-Warning "No SharePoint path configured. Create bootcamp/sharepoint-path.local.txt with the destination folder path to enable syncing. See bootcamp/pdfs/README.md for more details."
}
else {
    $sharePointPath = $sharePointPath.Trim()
    $answer = Read-Host "Copy bootcamp/pdfs into '$sharePointPath'? That folder may also hold files from other teams. (Y/N)"
    while ($answer -notmatch '^[YyNn]$') {
        $answer = Read-Host "Please answer Y or N"
    }

    if ($answer -match '^[Yy]$') {
        # File-by-file copy so unrelated content already in the SharePoint folder is never touched.
        $pdfFiles = Get-ChildItem $pdfsRoot -Recurse -File | Where-Object { $_.Name -ne "README.md" }
        foreach ($file in $pdfFiles) {
            $relativePath = $file.FullName.Substring($pdfsRoot.Length).TrimStart('\', '/')
            $destinationPath = Join-Path $sharePointPath $relativePath
            $destinationFolder = Split-Path $destinationPath -Parent
            if (-not (Test-Path $destinationFolder)) {
                New-Item -ItemType Directory -Path $destinationFolder -Force | Out-Null
            }
            Copy-Item -Path $file.FullName -Destination $destinationPath -Force
        }
        Write-Host "Copied $($pdfFiles.Count) file(s) to '$sharePointPath'."
    }
    else {
        Write-Host "Skipped SharePoint copy."
    }
}