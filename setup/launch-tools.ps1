# Launch editor tools with project folders pre-selected.
param(
    [Parameter(Position = 0)]
    [ValidateSet("shotcut", "openshot", "lightworks", "ardour", "lmms", "all")]
    [string]$Tool = "all"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$ConfigPath = Join-Path $ProjectRoot "config\tool-paths.yaml"

function Read-SimpleYamlMap {
    param([string]$Path)

    $map = @{}
    $current = $null
    foreach ($line in Get-Content $Path) {
        if ($line -match '^\s{2}(\w+):\s*$') {
            $current = $Matches[1]
            $map[$current] = @{}
            continue
        }
        if ($current -and $line -match '^\s+(\w+):\s*"?([^"#]+?)"?\s*$') {
            $map[$current][$Matches[1]] = $Matches[2].Trim()
        }
    }
    return $map
}

function Launch-Tool {
    param([string]$Name, [hashtable]$Config)

    $exe = $Config.executable
    if (-not $exe -or -not (Test-Path $exe)) {
        Write-Host "[$Name] not configured. Run setup/detect-tools.ps1 or edit config/tool-paths.yaml." -ForegroundColor Yellow
        return
    }

    $inbox = Join-Path $ProjectRoot ($Config.inbox -replace "/", "\")
    $projects = Join-Path $ProjectRoot ($Config.projects -replace "/", "\")
    New-Item -ItemType Directory -Force -Path $inbox, $projects | Out-Null

    Write-Host "SignalForge → Launching $Name" -ForegroundColor Cyan
    Write-Host "  inbox:    $inbox"
    Write-Host "  projects: $projects"
    Start-Process -FilePath $exe -WorkingDirectory $projects
}

$toolMap = Read-SimpleYamlMap -Path $ConfigPath

if ($Tool -eq "all") {
    foreach ($name in @("shotcut", "openshot", "lightworks", "ardour", "lmms")) {
        Launch-Tool -Name $name -Config $toolMap[$name]
    }
}
else {
    Launch-Tool -Name $Tool -Config $toolMap[$Tool]
}