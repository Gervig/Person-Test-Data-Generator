[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

# Resolve paths from this script, so it can be launched from any working directory.
$repoRoot = Split-Path -Parent $PSScriptRoot
$backendPath = Join-Path $repoRoot "backend"
$pyprojectPath = Join-Path $backendPath "pyproject.toml"

if (-not (Test-Path $backendPath -PathType Container)) {
    throw "Could not find the backend folder at '$backendPath'. Make sure this script is in the repo's scripts folder."
}

if (-not (Test-Path $pyprojectPath -PathType Leaf)) {
    throw "Could not find '$pyprojectPath'. Make sure the backend project files are present."
}

# Find uv on PATH, or at its standard per-user Windows install location.
$uvCommand = Get-Command uv -ErrorAction SilentlyContinue
$uvExe = $null

if ($uvCommand) {
    $uvExe = $uvCommand.Source
}
else {
    $standardUvPath = Join-Path $HOME ".local\bin\uv.exe"
    if (Test-Path $standardUvPath -PathType Leaf) {
        $uvExe = $standardUvPath
        $uvInstallDir = Split-Path -Parent $standardUvPath
        if (($env:Path -split ';') -notcontains $uvInstallDir) {
            # This is only needed for this PowerShell session.
            $env:Path = "$uvInstallDir;$env:Path"
        }
    }
}

if (-not $uvExe) {
    throw "uv was not found. Run .\scripts\setup.ps1 first, or install uv from https://docs.astral.sh/uv/getting-started/installation/."
}

Write-Host "Using uv: $uvExe" -ForegroundColor DarkGray
& $uvExe --version
if ($LASTEXITCODE -ne 0) {
    throw "uv could not be run successfully."
}

$envFile = Join-Path $backendPath ".env"
if (-not (Test-Path $envFile -PathType Leaf)) {
    Write-Warning "backend\.env was not found. If the API needs local database settings, create this file before continuing."
}

Write-Host "Starting the API from backend..." -ForegroundColor Cyan
Write-Host "Stop the server with Ctrl+C.`n" -ForegroundColor DarkGray

# uv run uses the backend project's .venv and ensures the environment is up to date.
# --directory also makes app.main resolve from the backend directory.
& $uvExe run --directory $backendPath python -m uvicorn app.main:app --reload
$exitCode = $LASTEXITCODE

if ($exitCode -ne 0) {
    throw "The API process exited with code $exitCode. Check the error output above."
}
