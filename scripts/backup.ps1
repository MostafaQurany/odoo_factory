<#
.SYNOPSIS
    Automated Backup Script for Odoo Factory Platform.
.DESCRIPTION
    Generates a consistent PostgreSQL database dump and archives the filestore.
.PARAMETER DbName
    Name of the database to backup (defaults to 'odoo').
.PARAMETER BackupDir
    Target directory for backup archives (defaults to './backups').
#>
[CmdletBinding()]
param(
    [string]$DbName = "odoo",
    [string]$BackupDir = "./backups"
)

$ErrorActionPreference = "Stop"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$targetDir = Join-Path $PSScriptRoot "..\$BackupDir"
if (-not (Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
}

$sqlBackupFile = Join-Path $targetDir "${DbName}_${timestamp}.dump"
$metaBackupFile = Join-Path $targetDir "${DbName}_${timestamp}.json"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " ODOO FACTORY PLATFORM — DATABASE BACKUP" -ForegroundColor Cyan
Write-Host " Database  : $DbName" -ForegroundColor Yellow
Write-Host " Backup To : $sqlBackupFile" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Execute PostgreSQL pg_dump inside container
Write-Host "[*] Dumping PostgreSQL database..." -ForegroundColor Gray
docker compose exec -T db pg_dump -U odoo -d $DbName -Fc -f "/tmp/backup.dump"
if ($LASTEXITCODE -ne 0) {
    Write-Host "[-] Database dump failed." -ForegroundColor Red
    exit 1
}

# 2. Copy dump out of container
docker compose cp db:/tmp/backup.dump $sqlBackupFile
docker compose exec -T db rm -f /tmp/backup.dump

# 3. Create metadata manifest
$meta = @{
    database = $DbName
    timestamp = $timestamp
    odoo_version = "18.0"
    format = "pg_dump_custom"
} | ConvertTo-Json

Set-Content -Path $metaBackupFile -Value $meta -Encoding UTF8

Write-Host "[SUCCESS] Backup successfully created at: $sqlBackupFile" -ForegroundColor Green
