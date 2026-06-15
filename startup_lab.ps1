param(
    [string]$VenvName = ".venv"
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $scriptDir

try {
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        throw "Python is not available on PATH. Install Python 3.10+ and reopen the terminal."
    }

    if (-not (Test-Path $VenvName)) {
        Write-Host "[Setup] Creating virtual environment '$VenvName'..."
        python -m venv $VenvName
    }
    else {
        Write-Host "[Setup] Virtual environment '$VenvName' already exists."
    }

    $venvPython = Join-Path $VenvName "Scripts\python.exe"
    if (-not (Test-Path $venvPython)) {
        throw "Virtual environment python executable not found at $venvPython"
    }

    $activateScript = Join-Path $VenvName "Scripts\Activate.ps1"
    if (-not (Test-Path $activateScript)) {
        throw "Virtual environment activation script not found at $activateScript"
    }

    Write-Host "[Setup] Activating virtual environment..."
    . $activateScript

    Write-Host "[Setup] Upgrading pip in virtual environment..."
    python -m pip install --upgrade pip

    Write-Host ""
    Write-Host "[Setup] Installing dependencies from requirements.txt..."
    Write-Host "[Setup] This may take 5-10 minutes on first run (caching speeds up future runs)."
    Write-Host "[Setup] Keep this terminal open and watch for package download/install messages."
    Write-Host ""
    python -m pip install -r requirements.txt

    Write-Host ""
    Write-Host "[Done] Lab environment is ready." -ForegroundColor Green
    if ($env:VIRTUAL_ENV) {
        Write-Host "[Done] Virtual environment active: $env:VIRTUAL_ENV" -ForegroundColor Green
        Write-Host "[Done] Next: Create .env file, then run any lab script (e.g., python 1_llmapiexample.py)" -ForegroundColor Green
    }
    else {
        Write-Host "[Info] VIRTUAL_ENV is not set. To keep .venv active in this terminal, run:" -ForegroundColor Yellow
        Write-Host "  . .\startup_lab.ps1"
    }
}
finally {
    Pop-Location
}
