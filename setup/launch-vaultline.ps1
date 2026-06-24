# One-click Vaultline launcher — starts server if needed, opens browser.
$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Port = 8470
$AppUrl = "http://localhost:$Port/site/index.html"
$LogDir = Join-Path $ProjectRoot "catalog"
$LogFile = Join-Path $LogDir "vaultline-server.log"
$PidFile = Join-Path $LogDir "vaultline-server.pid"

Set-Location $ProjectRoot
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

function Test-ServerUp {
    try {
        $r = Invoke-WebRequest -Uri "http://localhost:$Port/health" -UseBasicParsing -TimeoutSec 2
        return $r.StatusCode -eq 200
    }
    catch { return $false }
}

function Start-VaultlineServer {
    if (-not (Test-Path ".venv")) {
        python -m venv .venv
    }
    $python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
    if (-not (Test-Path $python)) { $python = "python" }

    & $python -m pip install -r requirements.txt -q 2>> $LogFile

    $proc = Start-Process -FilePath $python `
        -ArgumentList "-m", "api.server" `
        -WorkingDirectory $ProjectRoot `
        -WindowStyle Hidden `
        -PassThru

    $proc.Id | Out-File -FilePath $PidFile -Encoding ascii -Force
    return $proc
}

if (Test-ServerUp) {
    Start-Process $AppUrl
    exit 0
}

$proc = Start-VaultlineServer
$ready = $false
for ($i = 0; $i -lt 30; $i++) {
    Start-Sleep -Milliseconds 500
    if (Test-ServerUp) { $ready = $true; break }
}

if ($ready) {
    Start-Process $AppUrl
}
else {
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.MessageBox]::Show(
        "Vaultline server is starting but not ready yet.`n`nTry opening:`n$AppUrl`n`nin a few seconds.",
        "Vaultline",
        "OK",
        "Warning"
    ) | Out-Null
    Start-Process $AppUrl
}