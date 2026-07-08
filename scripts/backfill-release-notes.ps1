# Backfill GitHub release notes for existing releases from CHANGELOG.md.
#
# Existing releases (v0.1.0 .. v0.2.2) were created before the release workflow
# started pulling notes from the changelog. Run this once to give them all the
# same descriptive notes. Future releases get their notes automatically.
#
# Prerequisites:
#   1. GitHub CLI installed  (winget install GitHub.cli)
#   2. Logged in             (gh auth login)
#
# Usage (from the repo root):
#   ./scripts/backfill-release-notes.ps1

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path $PSScriptRoot -Parent
# -Encoding UTF8 is required: PowerShell 5.1 otherwise reads the BOM-less
# UTF-8 changelog as ANSI and garbles em-dashes and other non-ASCII characters.
$changelog = Get-Content (Join-Path $repoRoot "CHANGELOG.md") -Raw -Encoding UTF8

$footer = @"

---
**Download** the binary for your OS below, or install in one line - see the [README](https://github.com/skate28/snipvault#install). Full history in the [changelog](https://github.com/skate28/snipvault/blob/main/CHANGELOG.md).
"@

# Match each "## vX.Y.Z" section up to the next "## " heading (or end of file).
$pattern = '(?ms)^##\s+(v\d+\.\d+\.\d+)\s*$\r?\n(.*?)(?=^##\s|\z)'
$matches = [regex]::Matches($changelog, $pattern)

if ($matches.Count -eq 0) {
    Write-Host "No version sections found in CHANGELOG.md" -ForegroundColor Red
    exit 1
}

foreach ($m in $matches) {
    $tag = $m.Groups[1].Value
    $body = $m.Groups[2].Value.Trim() + "`n" + $footer

    $tmp = New-TemporaryFile
    # UTF-8 without BOM so no stray character appears atop the notes.
    [System.IO.File]::WriteAllText($tmp, $body, (New-Object System.Text.UTF8Encoding($false)))

    Write-Host "Updating release $tag ..." -ForegroundColor Cyan
    gh release edit $tag --notes-file $tmp
    Remove-Item $tmp
}

Write-Host "`nDone. All existing releases now have descriptive notes." -ForegroundColor Green
