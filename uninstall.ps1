# Snippet Vault uninstaller for Windows. Reverses install.ps1.
# Usage:  irm https://raw.githubusercontent.com/skate28/snipvault/main/uninstall.ps1 | iex

$ErrorActionPreference = "Stop"

$installDir = Join-Path $env:LOCALAPPDATA "snipvault\bin"
$vaultFile = Join-Path $env:USERPROFILE ".snipvault.json"

Write-Host "Uninstalling Snippet Vault..." -ForegroundColor Cyan

# Remove the installed binary directory.
if (Test-Path $installDir) {
    Remove-Item -Recurse -Force $installDir
    Write-Host "  removed $installDir"
} else {
    Write-Host "  nothing installed at $installDir"
}

# Remove the install dir from the user PATH if present.
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -and $userPath -like "*$installDir*") {
    $cleaned = ($userPath -split ';' | Where-Object { $_ -and $_ -ne $installDir }) -join ';'
    [Environment]::SetEnvironmentVariable("Path", $cleaned, "User")
    Write-Host "  removed $installDir from your user PATH"
}

Write-Host ""
Write-Host "Snippet Vault uninstalled." -ForegroundColor Green

# Leave the user's data in place; just tell them where it is.
if (Test-Path $vaultFile) {
    Write-Host "Your saved snippets are untouched at:" -ForegroundColor Yellow
    Write-Host "  $vaultFile"
    Write-Host "Delete that file too if you want to remove your snippets:"
    Write-Host "  Remove-Item `"$vaultFile`""
}
Write-Host "Open a new terminal for the PATH change to take effect."
