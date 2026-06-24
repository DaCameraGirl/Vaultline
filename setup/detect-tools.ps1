# Auto-detect installed media tools and update config/tool-paths.yaml.
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$ConfigPath = Join-Path $ProjectRoot "config\tool-paths.yaml"

$candidates = @{
    shotcut   = @(
        "${env:ProgramFiles}\Shotcut\shotcut.exe",
        "${env:ProgramFiles(x86)}\Shotcut\shotcut.exe",
        "${env:LOCALAPPDATA}\Programs\Shotcut\shotcut.exe"
    )
    openshot  = @(
        "${env:ProgramFiles}\OpenShot Video Editor\openshot-qt.exe",
        "${env:ProgramFiles(x86)}\OpenShot Video Editor\openshot-qt.exe",
        "${env:LOCALAPPDATA}\Programs\OpenShot Video Editor\openshot-qt.exe"
    )
    lightworks = @(
        "${env:ProgramFiles}\Lightworks\lightworks.exe",
        "${env:ProgramFiles(x86)}\Lightworks\lightworks.exe"
    )
    lmms      = @(
        "${env:ProgramFiles}\LMMS\lmms.exe",
        "${env:ProgramFiles(x86)}\LMMS\lmms.exe"
    )
    ardour    = @(
        "${env:ProgramFiles}\Ardour\bin\ardour.exe",
        "${env:ProgramFiles(x86)}\Ardour\bin\ardour.exe"
    )
}

function Resolve-InstalledPath {
    param([string[]]$Paths)
    foreach ($path in $Paths) {
        if ($path -and (Test-Path $path)) {
            return $path
        }
    }
    return ""
}

if (-not (Test-Path $ConfigPath)) {
    throw "Missing config file: $ConfigPath"
}

$lines = Get-Content $ConfigPath
$currentTool = $null
$updated = @{}

foreach ($line in $lines) {
    if ($line -match '^\s{2}(\w+):\s*$') {
        $currentTool = $Matches[1]
        continue
    }

    if ($currentTool -and $line -match '^\s+executable:\s*"(.*)"\s*$') {
        $found = Resolve-InstalledPath -Paths $candidates[$currentTool]
        if ($found) {
            $updated[$currentTool] = $found
            $lines[$lines.IndexOf($line)] = "    executable: `"$found`""
        }
    }
}

Set-Content -Path $ConfigPath -Value $lines -Encoding UTF8

Write-Host "Tool detection complete." -ForegroundColor Cyan
foreach ($tool in @("shotcut", "openshot", "lightworks", "ardour", "lmms")) {
    if ($updated.ContainsKey($tool)) {
        Write-Host ("  [found]   {0,-10} {1}" -f $tool, $updated[$tool]) -ForegroundColor Green
    }
    else {
        Write-Host ("  [missing] {0,-10} install manually and re-run" -f $tool) -ForegroundColor Yellow
    }
}