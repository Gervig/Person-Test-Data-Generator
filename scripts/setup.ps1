# Personal Test Data Generator - setup.ps1
# Run this script from the project root:
#   .\scripts\setup.ps1
#
# This script checks prerequisites, syncs Python dependencies, checks the
# backend .env file, and starts the database using Docker Compose.
# It does not install system software, create credentials, delete data,
# or make Git commits/pushes.

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host "`n==> $Message" -ForegroundColor Cyan
}

function Write-WarningMessage {
    param([string]$Message)
    Write-Host "WARNING: $Message" -ForegroundColor Yellow
}

function Test-Command {
    param([string]$Name)
    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

function Stop-Setup {
    param([string]$Message)
    Write-Host "`nSETUP STOPPED: $Message" -ForegroundColor Red
    exit 1
}

# Resolve the repository root from this script's location:
# <repo root>\scripts\setup.ps1
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$BackendPath = Join-Path $ProjectRoot "backend"
$EnvPath = Join-Path $BackendPath ".env"
$PyprojectPath = Join-Path $BackendPath "pyproject.toml"

Write-Host "Personal Test Data Generator - setup" -ForegroundColor Green
Write-Host "Project root: $ProjectRoot"

if (-not (Test-Path $BackendPath -PathType Container)) {
    Stop-Setup "Could not find the backend folder at '$BackendPath'. Save this script in <project root>\scripts\setup.ps1."
}

if (-not (Test-Path $PyprojectPath -PathType Leaf)) {
    Stop-Setup "Could not find backend\pyproject.toml. Check that you opened the correct project folder."
}

# Check Python
Write-Step "Checking Python"
if (Test-Command "python") {
    python --version
    if ($LASTEXITCODE -ne 0) {
        Write-WarningMessage "The 'python' command was found but did not run successfully."
    }
} else {
    Stop-Setup "Python was not found on PATH. Install Python 3.13.x, reopen PowerShell, and run this script again."
}

# Check and install uv if necessary
$uvInstallDir = Join-Path $HOME ".local\bin"
$uvExe = Join-Path $uvInstallDir "uv.exe"

# Check whether uv is already available
$uvCommand = Get-Command uv -ErrorAction SilentlyContinue

if (-not $uvCommand -and -not (Test-Path $uvExe)) {
    Write-Host "uv not found. Installing uv..."

    & powershell.exe -NoProfile -ExecutionPolicy Bypass -Command `
        "irm https://astral.sh/uv/install.ps1 | iex"

    if ($LASTEXITCODE -ne 0) {
        throw "uv installation failed."
    }
}

# Make the standard uv installation directory available
# for the rest of this PowerShell session.
if (Test-Path $uvExe) {
    if (($env:Path -split ';') -notcontains $uvInstallDir) {
        $env:Path = "$uvInstallDir;$env:Path"
    }
}

# Verify uv
$uvCommand = Get-Command uv -ErrorAction SilentlyContinue

if ($uvCommand) {
    uv --version
}
elseif (Test-Path $uvExe) {
    & $uvExe --version
}
else {
    throw "uv was not found after installation. Restart PowerShell and try again."
}

# Check Docker
Write-Step "Checking Docker"
if (-not (Test-Command "docker")) {
    Stop-Setup "Docker was not found on PATH. Install Docker Desktop, open it, and then rerun this script."
}
docker --version
if ($LASTEXITCODE -ne 0) {
    Stop-Setup "The Docker command did not run successfully."
}

try {
    docker info *> $null
    if ($LASTEXITCODE -ne 0) {
        Stop-Setup "Docker Desktop does not appear to be running. Start Docker Desktop, wait until it is ready, and rerun this script."
    }
} catch {
    Stop-Setup "Could not connect to Docker. Start Docker Desktop and rerun this script."
}

# Install/synchronize project dependencies
Write-Step "Installing Python dependencies with uv sync"
Push-Location $BackendPath
try {
    uv sync
    if ($LASTEXITCODE -ne 0) {
        Stop-Setup "uv sync failed. Read the error above, resolve it, and rerun this script."
    }
} finally {
    Pop-Location
}

# Check .env without overwriting it or printing its contents
Write-Step "Checking backend environment configuration"
if (Test-Path $EnvPath -PathType Leaf) {
    Write-Host "Found backend\.env. Its contents will not be displayed or changed."
} else {
    Write-WarningMessage "backend\.env was not found."
    Write-Host "Create backend\.env using the exact variable names expected by backend\app\database.py and the Docker Compose configuration."
    Write-Host "Do not put real credentials in Git. The setup script will not create a guessed .env file."
}

# Find a Compose file supported by Docker Compose
$ComposeCandidates = @(
    (Join-Path $BackendPath "compose.yaml"),
    (Join-Path $BackendPath "compose.yml"),
    (Join-Path $BackendPath "docker-compose.yaml"),
    (Join-Path $BackendPath "docker-compose.yml")
)
$ComposeFile = $ComposeCandidates | Where-Object { Test-Path $_ -PathType Leaf } | Select-Object -First 1

if (-not $ComposeFile) {
    Stop-Setup "No Docker Compose file was found in backend\. Expected compose.yaml, compose.yml, docker-compose.yaml, or docker-compose.yml."
}

Write-Step "Starting MariaDB services with Docker Compose"
Write-Host "Compose file: $ComposeFile"
Push-Location $BackendPath
try {
    docker compose -f $ComposeFile up -d
    if ($LASTEXITCODE -ne 0) {
        Stop-Setup "Docker Compose could not start the services. Check Docker Desktop, the Compose file, and your configuration."
    }

    Write-Step "Checking database container status"
    docker compose -f $ComposeFile ps
    if ($LASTEXITCODE -ne 0) {
        Write-WarningMessage "Could not display Compose service status. Check Docker Compose manually."
    }
} finally {
    Pop-Location
}

Write-Host "`nSetup steps completed." -ForegroundColor Green
Write-Host "Next steps:"
Write-Host "  1. Confirm backend\.env contains the required database settings."
Write-Host "  2. From the backend folder, start the API:"
Write-Host "     uv run uvicorn app.main:app --reload"
Write-Host "  3. Open http://127.0.0.1:8000/docs"
Write-Host "  4. In another terminal, run tests from backend:"
Write-Host "     uv run pytest -v"

if (-not (Test-Path $EnvPath -PathType Leaf)) {
    Write-WarningMessage "The API may not connect to the database until backend\.env is configured."
}
