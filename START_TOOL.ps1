# Power BI Field Router - Startup Script (PowerShell)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Kill any existing Python/Flask processes - AGGRESSIVE
Write-Host "Stopping any existing Flask processes..." -ForegroundColor Yellow

# Method 1: PowerShell Stop-Process
Get-Process python3.13 -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# Method 2: taskkill (more aggressive, multiple passes)
for ($attempt = 0; $attempt -lt 3; $attempt++) {
    taskkill /IM python3.13.exe /F /T 2>$null
    Start-Sleep -Milliseconds 300
}

# Method 3: WMI (ultimate force)
Get-WmiObject Win32_Process -Filter "Name='python3.13.exe'" -ErrorAction SilentlyContinue | ForEach-Object { $_.Terminate() }

Start-Sleep -Seconds 2

# Install dependencies (handle uv-managed environment)
Write-Host "Installing dependencies..." -ForegroundColor Yellow
python3.13 -m pip install -q --break-system-packages -r requirements.txt 2>$null

# Start Flask
Write-Host "Starting Flask server at http://127.0.0.1:5000/" -ForegroundColor Green
Write-Host "[OK] pbixray is available - DAX extraction enabled" -ForegroundColor Green
python3.13 app.py
