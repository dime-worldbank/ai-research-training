param(
    [string]$SourceRoot = "sessions"
)

$ErrorActionPreference = "Stop"
$projectRoot = $PSScriptRoot
$allowlistFileName = "push-to-teams.yml"
$sharePointConfigPath = Join-Path $projectRoot "sharepoint-path.local.txt"

function New-DirectoryIfMissing {
    param([Parameter(Mandatory)][string]$Path)

    if (Test-Path -LiteralPath $Path) {
        if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
            throw "Directory path '$Path' exists but is not a directory."
        }
        return
    }

    New-Item -ItemType Directory -Path $Path -Force -ErrorAction Stop | Out-Null
}

$sourceRootPath = Join-Path $projectRoot $SourceRoot
if (-not (Test-Path -LiteralPath $sourceRootPath -PathType Container)) {
    throw "Session source folder was not found: $sourceRootPath"
}
$sourceRootPath = (Resolve-Path -LiteralPath $sourceRootPath).Path
$allowlistPath = Join-Path $sourceRootPath $allowlistFileName

function Get-PresentationName {
    param([Parameter(Mandatory)][System.IO.FileInfo]$SourceFile)

    $name = $SourceFile.BaseName
    $metadataPath = Join-Path $SourceFile.DirectoryName "render-meta.yml"
    if (Test-Path -LiteralPath $metadataPath -PathType Leaf) {
        $metadataNames = @(
            Get-Content -LiteralPath $metadataPath | Where-Object { $_ -match '^\s*name\s*:\s*(.+)$' }
        )
        if ($metadataNames.Count -gt 1) {
            throw "More than one 'name' property found in '$metadataPath'."
        }
        if ($metadataNames.Count -eq 1 -and $metadataNames[0] -match '^\s*name\s*:\s*(.+)$') {
            $name = $Matches[1].Trim().Trim("'`"")
        }
    }

    if ($name -notmatch '^[A-Za-z0-9][A-Za-z0-9._ -]*$' -or $name -match '[. ]$' -or $name -in @('.', '..')) {
        throw "Invalid Teams name '$name' for '$($SourceFile.FullName)'. Use letters, numbers, spaces, periods, underscores, or hyphens."
    }

    return $name
}

function Get-AllowlistedPresentations {
    param(
        [Parameter(Mandatory)][string]$AllowlistPath,
        [Parameter(Mandatory)][string]$SourceRootPath
    )

    if (-not (Test-Path -LiteralPath $AllowlistPath -PathType Leaf)) {
        throw "Publication allowlist was not found: $AllowlistPath"
    }

    $presentations = @()
    $seenDays = @{}
    $seenPaths = @{}
    $seenDestinations = @{}
    $currentDay = $null
    $lineNumber = 0

    foreach ($line in Get-Content -LiteralPath $AllowlistPath) {
        $lineNumber++
        if ($line -match '^\s*$' -or $line -match '^\s*#') {
            continue
        }

        if ($line -match '^(day-\d+):$') {
            $currentDay = $Matches[1]
            if ($seenDays.ContainsKey($currentDay)) {
                throw "Duplicate day '$currentDay' in '$AllowlistPath' at line $lineNumber."
            }
            $seenDays[$currentDay] = $true
            continue
        }

        if ($line -match '^  - (.+)$') {
            if (-not $currentDay) {
                throw "A presentation entry appears before a day heading in '$AllowlistPath' at line $lineNumber."
            }

            $relativePath = $Matches[1]
            if ($relativePath -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]*(/[A-Za-z0-9][A-Za-z0-9._-]*)*\.qmd$') {
                throw "Invalid QMD path '$relativePath' in '$AllowlistPath' at line $lineNumber. Use a relative path with forward slashes and a .qmd extension."
            }

            $allowlistEntry = "$currentDay/$relativePath"
            if ($seenPaths.ContainsKey($allowlistEntry)) {
                throw "Duplicate presentation '$allowlistEntry' in '$AllowlistPath'."
            }
            $seenPaths[$allowlistEntry] = $true

            $sourcePath = Join-Path $SourceRootPath $allowlistEntry
            if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) {
                throw "Listed presentation was not found: $sourcePath"
            }

            $sourceFile = Get-Item -LiteralPath $sourcePath
            if ($sourceFile.Name.StartsWith('_')) {
                throw "Underscore-prefixed QMD files cannot be published: $sourcePath"
            }

            $name = Get-PresentationName -SourceFile $sourceFile
            $destinationKey = "$currentDay/$name"
            if ($seenDestinations.ContainsKey($destinationKey)) {
                throw "Multiple presentations resolve to the same Teams destination '$destinationKey'."
            }
            $seenDestinations[$destinationKey] = $true

            $presentations += [pscustomobject]@{
                Day = $currentDay
                Name = $name
                RelativePath = $allowlistEntry
                SourcePath = $sourceFile.FullName
                HtmlPath = Join-Path $sourceFile.DirectoryName ($sourceFile.BaseName + ".html")
            }
            continue
        }

        throw "Unsupported allowlist syntax in '$AllowlistPath' at line $lineNumber. Use day headings and two-space-indented '- path/to/file.qmd' entries."
    }

    if ($presentations.Count -eq 0) {
        throw "No presentations are listed in '$AllowlistPath'."
    }

    return $presentations
}

$documents = @(Get-AllowlistedPresentations -AllowlistPath $allowlistPath -SourceRootPath $sourceRootPath)

Write-Host "Allowlisted $($documents.Count) presentation(s) to render:"
foreach ($document in $documents) {
    Write-Host "  $($document.RelativePath)"
}

foreach ($document in $documents) {
    Write-Host "Rendering $($document.RelativePath) to HTML"
    Push-Location $projectRoot
    try {
        & quarto render $document.SourcePath
        if ($LASTEXITCODE -ne 0) {
            throw "Quarto failed to render '$($document.RelativePath)'."
        }
    }
    finally {
        Pop-Location
    }

    if (-not (Test-Path -LiteralPath $document.HtmlPath -PathType Leaf)) {
        throw "Quarto did not create the expected HTML file '$($document.HtmlPath)'."
    }
}

Write-Host "Rendered $($documents.Count) allowlisted HTML file(s). No PDFs were created."

if (Test-Path $sharePointConfigPath) {
    $sharePointPath = Get-Content $sharePointConfigPath | Where-Object { $_.Trim() } | Select-Object -First 1
}
else {
    $sharePointPath = $null
}

if (-not $sharePointPath) {
    Write-Warning "No Teams folder path configured. Create bootcamp/sharepoint-path.local.txt with the destination folder path to enable publishing. See bootcamp/pdfs/README.md for more details."
}
else {
    $sharePointPath = $sharePointPath.Trim()
    $answer = Read-Host "Copy $($documents.Count) allowlisted HTML file(s) into '$sharePointPath'? (Y/N)"
    while ($answer -notmatch '^[YyNn]$') {
        $answer = Read-Host "Please answer Y or N"
    }

    if ($answer -match '^[Yy]$') {
        foreach ($document in $documents) {
            $destinationFolder = Join-Path (Join-Path $sharePointPath $document.Day) $document.Name
            New-DirectoryIfMissing $destinationFolder
            $destinationHtml = Join-Path $destinationFolder ($document.Name + ".html")
            Copy-Item -LiteralPath $document.HtmlPath -Destination $destinationHtml -Force
        }
        Write-Host "Copied $($documents.Count) HTML file(s) to '$sharePointPath'."
    }
    else {
        Write-Host "Skipped Teams copy."
    }
}