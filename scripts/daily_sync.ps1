<#
.SYNOPSIS
    GarminDB Daily Sync Wrapper Script for Windows.
.DESCRIPTION
    Runs GarminDB sync with HRV, sleep, and latest monitoring data.
    Designed for Windows Task Scheduler or manual execution.
#>

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir
Set-Location $ProjectDir

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

$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Output "[$Timestamp] Starting GarminDB Daily Sync..."

$ConfigPath = "C:\Users\Joel\.GarminDb\GarminConnectConfig.json"
$CliScript = Join-Path $ProjectDir "scripts\garmindb_cli.py"

& $PythonExe $CliScript -f $ConfigPath --sleep --all --hrv --download --import --analyze --latest

$ExitCode = $LASTEXITCODE
$EndTimestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
if ($ExitCode -eq 0) {
    Write-Output "[$EndTimestamp] GarminDB sync completed successfully."
} else {
    Write-Error "[$EndTimestamp] GarminDB sync failed with exit code $ExitCode."
}
exit $ExitCode
