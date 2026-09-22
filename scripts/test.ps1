<#
.SYNOPSIS
    Automated Test Runner with Disposable Databases for Odoo Factory Platform.
.DESCRIPTION
    Runs unit tests, module tests, or scenario checks inside isolated Odoo test databases.
.PARAMETER Module
    Module to test (e.g. factory_base, factory_mrp).
.PARAMETER Scenario
    Golden scenario code (e.g. GS-001, GX-001).
.PARAMETER KeepDb
    If set, does not drop the test database after the test run.
.PARAMETER DbName
    Explicit test database name. If not provided, generates disposable 'odoo_test_<timestamp>'.
#>
[CmdletBinding()]
param(
    [string]$Module = "",
    [string]$Scenario = "",
    [switch]$KeepDb,
    [string]$DbName = ""
)

$ErrorActionPreference = "Stop"

$runId = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
if (-not $DbName) {
    $DbName = "odoo_test_$runId"
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " ODOO FACTORY PLATFORM — TEST RUNNER" -ForegroundColor Cyan
Write-Host " Test Database : $DbName" -ForegroundColor Yellow
Write-Host " Target Module : $(if ($Module) {$Module} else {'All installed'})" -ForegroundColor Yellow
Write-Host " Scenario Code : $(if ($Scenario) {$Scenario} else {'N/A'})" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

$testArgs = @("-d", $DbName, "--test-enable", "--stop-after-init")
if ($Module) {
    $testArgs += @("-u", $Module)
}

$cmd = "docker compose run --rm web odoo $($testArgs -join ' ')"
Write-Host "Executing: $cmd" -ForegroundColor Gray

$testSuccess = $false
try {
    Invoke-Expression $cmd
    if ($LASTEXITCODE -eq 0) {
        $testSuccess = $true
        Write-Host "`n[TEST PASS] All tests passed." -ForegroundColor Green
    } else {
        Write-Host "`n[TEST FAIL] Tests failed with exit code $LASTEXITCODE." -ForegroundColor Red
    }
} finally {
    if (-not $KeepDb) {
        Write-Host "`nCleaning up disposable test database: $DbName..." -ForegroundColor Gray
        docker compose exec -T db dropdb -U odoo --if-exists $DbName 2>$null
        Write-Host "Database cleanup completed." -ForegroundColor Gray
    } else {
        Write-Host "Keeping test database '$DbName' as requested." -ForegroundColor Yellow
    }
}

if (-not $testSuccess) {
    exit 1
}
