$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot/..

if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host 'Created .env from .env.example' -ForegroundColor Green
}

Write-Host 'Pulling latest images...' -ForegroundColor Cyan
docker compose pull

Write-Host 'Starting services...' -ForegroundColor Cyan
docker compose up -d

Write-Host 'Waiting for services...' -ForegroundColor Cyan
Start-Sleep -Seconds 10

docker compose ps
