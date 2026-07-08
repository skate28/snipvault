# Snippet Vault installer for Windows.
# Usage:  irm https://raw.githubusercontent.com/skate28/snipvault/main/install.ps1 | iex

$ErrorActionPreference = "Stop"

$repo = "skate28/snipvault"
$asset = "snipvault-windows-x64.exe"
$installDir = Join-Path $env:LOCALAPPDATA "snipvault\bin"
$exePath = Join-Path $installDir "snipvault.exe"
$url = "https://github.com/$repo/releases/latest/download/$asset"

Write-Host "Installing Snippet Vault..." -ForegroundColor Cyan

New-Item -ItemType Directory -Force -Path $installDir | Out-Null

Write-Host "  downloading $url"
Invoke-WebRequest -Uri $url -OutFile $exePath -UseBasicParsing

# Add the install dir to the *user* PATH if it isn't there already.
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$installDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$installDir", "User")
    Write-Host "  added $installDir to your user PATH"
    $pathNote = $true
}

# Verify it runs.
& $exePath --help | Out-Null

Write-Host ""
Write-Host "Snippet Vault installed to $exePath" -ForegroundColor Green
if ($pathNote) {
    Write-Host "Open a NEW terminal, then try:  snipvault --help"
} else {
    Write-Host "Try:  snipvault --help"
}
