# Start Vaultline enterprise stack locally.
$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot

Set-Location $ProjectRoot

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

& .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt -q

Write-Host ""
Write-Host "Vaultline Enterprise" -ForegroundColor Cyan
Write-Host "  Marketing:  http://localhost:8470/site/index.html"
Write-Host "  Console:    http://localhost:8470/console/index.html"
Write-Host "  API docs:   http://localhost:8470/docs"
Write-Host ""

python -m api.server