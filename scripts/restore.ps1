<#
.SYNOPSIS
    Automated Restore Script for Odoo Factory Platform.
.DESCRIPTION
    Restores a PostgreSQL database dump and validates system health.
.PARAMETER DumpFile
    Path to the .dump file to restore.
.PARAMETER TargetDb
    Target database name (defaults to 'odoo').
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$DumpFile,
    [string]$TargetDb = "odoo"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $DumpFile)) {
    Write-Host "[-] Dump file '$DumpFile' not found." -ForegroundColor Red
    exit 1
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " ODOO FACTORY PLATFORM — DATABASE RESTORE" -ForegroundColor Cyan
Write-Host " Source File : $DumpFile" -ForegroundColor Yellow
Write-Host " Target DB   : $TargetDb" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Terminate existing connections and drop target database if exists
Write-Host "[*] Resetting target database '$TargetDb'..." -ForegroundColor Gray
docker compose exec -T db dropdb -U odoo --if-exists $TargetDb 2>$null
docker compose exec -T db createdb -U odoo $TargetDb

# 2. Copy dump file into container and restore
Write-Host "[*] Restoring database via pg_restore..." -ForegroundColor Gray
docker compose cp $DumpFile db:/tmp/restore.dump
docker compose exec -T db pg_restore -U odoo -d $TargetDb --no-owner --role=odoo /tmp/restore.dump 2>$null
docker compose exec -T db rm -f /tmp/restore.dump

Write-Host "[SUCCESS] Database '$TargetDb' restored successfully." -ForegroundColor Green
