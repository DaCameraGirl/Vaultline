# Store IBM Quantum API key for Vaultline (session + user env).
param(
    [string]$ApiKey
)

$ErrorActionPreference = "Stop"

if (-not $ApiKey) {
    $secure = Read-Host "Paste IBM Quantum API key" -AsSecureString
    $ApiKey = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    )
}

if (-not $ApiKey -or $ApiKey.Length -lt 20) {
    throw "API key looks invalid."
}

[Environment]::SetEnvironmentVariable("IBM_QUANTUM_API_KEY", $ApiKey, "User")
$env:IBM_QUANTUM_API_KEY = $ApiKey

Write-Host "IBM_QUANTUM_API_KEY saved to your user environment." -ForegroundColor Green
Write-Host "Install quantum deps: pip install -r requirements-quantum.txt"
Write-Host "Test: python bench.py quantum status"
Write-Host "Generate seed: python bench.py quantum seed"