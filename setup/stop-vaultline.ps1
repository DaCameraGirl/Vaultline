# Stop background Vaultline server.
$ErrorActionPreference = "SilentlyContinue"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$PidFile = Join-Path $ProjectRoot "catalog\vaultline-server.pid"

if (Test-Path $PidFile) {
    $serverPid = Get-Content $PidFile | Select-Object -First 1
    Stop-Process -Id ([int]$serverPid) -Force
    Remove-Item $PidFile -Force
    Write-Host "Vaultline stopped (pid $serverPid)" -ForegroundColor Yellow
}

Get-NetTCPConnection -LocalPort 8470 -ErrorAction SilentlyContinue |
    ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }

Write-Host "Port 8470 cleared." -ForegroundColor Green