$backend = Join-Path $PSScriptRoot "..\backend"
$python  = Join-Path $backend ".venv\Scripts\python.exe"

if (-not (Test-Path $python)) {
    Write-Host "No .venv found in backend. Run: cd backend; uv sync"
    exit 1
}

Push-Location $backend
try {
    & $python -m pytest -v --cov=app --cov-branch --cov-report=term-missing @args
    $code = $LASTEXITCODE
}
finally {
    Pop-Location
}
exit $code