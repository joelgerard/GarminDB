<#
.SYNOPSIS
    GarminDB + Centurion Daily Sync Wrapper Script for Windows.
.DESCRIPTION
    Runs GarminDB sync with HRV, sleep, and latest monitoring data, then generates
    and uploads the Centurion daily readiness JSON report when Centurion is installed.
    Designed for Windows Task Scheduler (including S4U headless sessions) or manual runs.
#>

$ErrorActionPreference = "Continue"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir
Set-Location $ProjectDir

# Ensure USERPROFILE is populated in headless Task Scheduler sessions
if (-not $env:USERPROFILE -and $env:LOCALAPPDATA) {
    $env:USERPROFILE = Split-Path -Parent (Split-Path -Parent $env:LOCALAPPDATA)
}

# Locate Python: Prefer project .venv, fallback to Python 3.12 system path
$PythonExe = Join-Path $ProjectDir ".venv\Scripts\python.exe"
if (-not (Test-Path $PythonExe)) {
    $PythonExe = "C:\Users\Joel\AppData\Local\Programs\Python\Python312\python.exe"
}

if (-not (Test-Path $PythonExe)) {
    $PythonCmd = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($PythonCmd) {
        $PythonExe = $PythonCmd.Source
    } else {
        Write-Error "Python executable not found!"
        exit 1
    }
}

$LogDir = "C:\Users\Joel\HealthData\logs"
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}
$LogFile = Join-Path $LogDir "daily_sync.log"

function Write-SyncLog {
    param([string]$Message)
    $Line = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $Message"
    Write-Output $Line
    Add-Content -Path $LogFile -Value $Line -Encoding UTF8
}

Write-SyncLog "Starting GarminDB Daily Sync..."

$ConfigDir = "C:\Users\Joel\.GarminDb"
$CliScript = Join-Path $ProjectDir "scripts\garmindb_cli.py"

& $PythonExe -u $CliScript -f $ConfigDir --sleep --all --hrv --download --import --analyze --latest 2>&1 |
    ForEach-Object { $_.ToString() } |
    Tee-Object -FilePath $LogFile -Append
$ExitCode = $LASTEXITCODE

if ($ExitCode -ne 0) {
    Write-SyncLog "ERROR: GarminDB sync failed with exit code $ExitCode."
    exit $ExitCode
}
Write-SyncLog "GarminDB sync completed successfully."

# Generate and upload Centurion daily readiness report
$CenturionDir = "C:\Users\Joel\dev\git\centurion"
$ExportScript = Join-Path $CenturionDir "export_daily_report.py"
if (Test-Path $ExportScript) {
    $CenturionPy = Join-Path $CenturionDir ".venv\Scripts\python.exe"
    if (-not (Test-Path $CenturionPy)) {
        $CenturionPy = $PythonExe
    }
    Write-SyncLog "Generating and uploading Centurion daily readiness report..."
    Push-Location $CenturionDir
    try {
        & $CenturionPy -u $ExportScript --upload 2>&1 |
            ForEach-Object { $_.ToString() } |
            Tee-Object -FilePath $LogFile -Append
        $ExportExit = $LASTEXITCODE
    } finally {
        Pop-Location
    }
    if ($ExportExit -ne 0) {
        Write-SyncLog "ERROR: Centurion export/upload failed with exit code $ExportExit."
        exit $ExportExit
    }
    Write-SyncLog "Centurion daily readiness report uploaded successfully."
}

exit 0

