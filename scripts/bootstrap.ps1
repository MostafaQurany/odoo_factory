<#
.SYNOPSIS
    Idempotent Bootstrap & Profile Installer for Odoo Factory Platform.
.DESCRIPTION
    Runs headless Odoo container to initialize database and install or upgrade specified profiles/modules.
.PARAMETER Profile
    Name of the factory profile to install (core, operations, advanced, full). Default is 'core'.
.PARAMETER Demo
    Switch to include factory demo data.
.PARAMETER Modules
    Explicit comma-separated list of modules to install or upgrade.
.PARAMETER DbName
    Target database name. Defaults to ODOO_DB from .env or 'odoo'.
.PARAMETER Update
    If specified, runs upgrade (-u) instead of install (-i).
#>
[CmdletBinding()]
param(
    [string]$Profile = "core",
    [switch]$Demo,
    [string]$Modules = "",
    [string]$DbName = "",
    [switch]$Update
)

$ErrorActionPreference = "Stop"

if (-not $DbName) {
    if (Test-Path ".env") {
        $envMatch = Get-Content ".env" | Select-String "^ODOO_DB=(.*)$"
        if ($envMatch) {
            $DbName = $envMatch.Matches[0].Groups[1].Value.Trim()
        }
    }
    if (-not $DbName) {
        $DbName = "odoo"
    }
}

# Resolve modules to install
$targetModules = @()
if ($Modules) {
    $targetModules += $Modules.Split(",") | ForEach-Object { $_.Trim() }
} else {
    $profileMap = @{
        "core" = "factory_profile_core"
        "operations" = "factory_profile_operations"
        "advanced" = "factory_profile_advanced"
        "full" = "factory_profile_full"
        "legacy" = "odoo_factory_all"
    }
    if ($profileMap.ContainsKey($Profile.ToLower())) {
        $targetModules += $profileMap[$Profile.ToLower()]
    } else {
        Write-Error "Unknown profile: $Profile. Valid profiles: core, operations, advanced, full, legacy"
    }
}

if ($Demo) {
    $targetModules += "factory_demo"
}

$moduleArg = $targetModules -join ","
$flag = if ($Update) { "-u" } else { "-i" }

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " ODOO FACTORY PLATFORM — BOOTSTRAP RUNNER" -ForegroundColor Cyan
Write-Host " Database : $DbName" -ForegroundColor Yellow
Write-Host " Action   : $(if ($Update) {'Upgrade (-u)'} else {'Install (-i)'})" -ForegroundColor Yellow
Write-Host " Modules  : $moduleArg" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

$cmd = "docker compose run --rm web odoo -d $DbName $flag $moduleArg --stop-after-init"
Write-Host "Executing: $cmd" -ForegroundColor Gray
Invoke-Expression $cmd

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n[SUCCESS] Bootstrap operation completed successfully." -ForegroundColor Green
} else {
    Write-Error "[FAILURE] Bootstrap operation failed with exit code $LASTEXITCODE."
}
