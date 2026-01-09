param(
    [string]$Python = "python",
    [switch]$Clean,
    [switch]$NoVenv
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Fail([string]$Message) {
    Write-Host "Error: $Message" -ForegroundColor Red
    exit 1
}

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repoRoot

Write-Host "Repo root: $repoRoot"

if ($Clean) {
    Write-Host "Cleaning build artifacts..."
    Remove-Item -Recurse -Force "build", "dist", "*.spec" -ErrorAction SilentlyContinue
}

$pythonExe = $Python
if (-not $NoVenv) {
    if (-not (Test-Path ".venv")) {
        Write-Host "Creating virtual environment..."
        & $Python -m venv .venv
        if ($LASTEXITCODE -ne 0) { Fail "Failed to create virtual environment." }
    }

    $pythonExe = Join-Path $repoRoot ".venv\Scripts\python.exe"
    if (-not (Test-Path $pythonExe)) {
        Fail "Virtual environment python not found at $pythonExe"
    }
}

Write-Host "Installing dependencies..."
& $pythonExe -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { Fail "pip upgrade failed." }

& $pythonExe -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { Fail "Dependency install failed." }

Write-Host "Running build..."
& $pythonExe build.py
if ($LASTEXITCODE -ne 0) { Fail "Build failed." }

Write-Host "Build finished. Check the dist folder for the executable."
