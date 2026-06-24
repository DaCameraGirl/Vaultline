# Verify Vaultline install end-to-end.
$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "Vaultline verification" -ForegroundColor Cyan

$checks = @()

function Test-Cmd($name, $cmd) {
    try {
        & $cmd 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0 -or $null -eq $LASTEXITCODE) {
            Write-Host "[PASS] $name" -ForegroundColor Green
            return $true
        }
    }
    catch {}
    Write-Host "[FAIL] $name" -ForegroundColor Red
    return $false
}

$checks += Test-Cmd "python" { python --version }
$checks += Test-Cmd "ffmpeg" { ffmpeg -version }
$checks += (Test-Path ".venv\Scripts\python.exe")
if (-not (Test-Path ".venv\Scripts\python.exe")) { Write-Host "[FAIL] venv missing — run launch-vaultline.ps1 once" -ForegroundColor Red }

if (-not (Get-NetTCPConnection -LocalPort 8470 -ErrorAction SilentlyContinue)) {
    Write-Host "[WARN] Server not running — starting..." -ForegroundColor Yellow
    & "$ProjectRoot\setup\launch-vaultline.ps1"
    Start-Sleep 3
}

& .\.venv\Scripts\python.exe scripts\smoke_test.py
$smoke = $LASTEXITCODE -eq 0
if ($smoke) { Write-Host "`nVaultline is ready." -ForegroundColor Green }
else { Write-Host "`nFix failures above, then re-run setup/verify.ps1" -ForegroundColor Red; exit 1 }