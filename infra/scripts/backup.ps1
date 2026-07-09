$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot/..

$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$backupDir = Join-Path $PWD 'backup'

if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
}

Write-Host "Backing up data to $backupDir ..." -ForegroundColor Cyan

if (Test-Path (Join-Path $PWD 'data')) {
    Compress-Archive -Path (Join-Path $PWD 'data') -DestinationPath (Join-Path $backupDir "data_$stamp.zip") -Force
}

Write-Host 'Backup completed.' -ForegroundColor Green
