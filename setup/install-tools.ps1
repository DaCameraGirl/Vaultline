# Open official download pages for the media toolchain.
$pages = @{
    shotcut    = "https://www.shotcut.org/download/"
    openshot   = "https://www.openshot.org/download/"
    lightworks = "https://lwks.com/download"
    ardour     = "https://ardour.org/download.html"
    lmms       = "https://lmms.io/download/"
}

Write-Host "Opening download pages for the AI Research Media Workbench toolchain..." -ForegroundColor Cyan
foreach ($entry in $pages.GetEnumerator()) {
    Write-Host ("  {0,-10} {1}" -f $entry.Key, $entry.Value)
    Start-Process $entry.Value
    Start-Sleep -Milliseconds 400
}

Write-Host ""
Write-Host "After installing, run:" -ForegroundColor Green
Write-Host "  powershell -File setup/detect-tools.ps1"
Write-Host "  powershell -File setup/launch-tools.ps1 shotcut"