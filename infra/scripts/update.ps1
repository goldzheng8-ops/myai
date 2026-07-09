$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot/..

Write-Host 'Pulling latest images...' -ForegroundColor Cyan
docker compose pull

Write-Host 'Recreating containers...' -ForegroundColor Cyan
docker compose up -d --remove-orphans

Write-Host 'Checking status...' -ForegroundColor Cyan
docker compose ps
