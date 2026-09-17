param(
    [string]$SourceRoot = "sessions"
)

$ErrorActionPreference = "Stop"
$projectRoot = $PSScriptRoot
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

$documents = Get-ChildItem (Join-Path $projectRoot $SourceRoot) -Recurse -Filter "*.qmd" |
    Where-Object {
        $relativePath = $_.FullName.Substring($projectRoot.Length + 1)
        ($relativePath -notmatch '(^|[\\/])template[\\/]') -and ($_.Name -ne 'presentation.qmd')
    } |
    Sort-Object FullName

if (-not $documents) {
    throw "No .qmd files found under '$SourceRoot' after excluding the template presentation."
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
    }
}
finally {
    if (Test-Path $browserProfile) {
        Remove-Item $browserProfile -Recurse -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "Created $($documents.Count) PDF files."