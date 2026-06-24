# Kill anything on port 8470 and start fresh Vaultline server.
$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Get-NetTCPConnection -LocalPort 8470 -ErrorAction SilentlyContinue |
    ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }

Start-Sleep -Seconds 1

if (-not (Test-Path ".venv")) { python -m venv .venv }
& .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt -q

Write-Host "Starting Vaultline on http://localhost:8470" -ForegroundColor Cyan
Write-Host "  App:      http://localhost:8470/site/index.html"
Write-Host "  Quantum:  http://localhost:8470/v1/quantum/status"
Write-Host ""

python -m api.server