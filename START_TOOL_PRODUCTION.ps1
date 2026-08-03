# Power BI Field Router - Production Startup Script
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Kill any existing Python processes
Get-Process python3.13 -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
python3.13 -m pip install -q --break-system-packages -r requirements.txt 2>$null

# Start Flask in production mode (no debug/reload)
Write-Host "Starting Flask server at http://127.0.0.1:5000/" -ForegroundColor Green
Write-Host "✓ pbixray is available - DAX extraction enabled" -ForegroundColor Green
$env:FLASK_ENV="production"
python3.13 -c "import sys; sys.argv[0]='app'; exec(open('app.py').read().replace('debug=True', 'debug=False').replace('use_reloader=True', 'use_reloader=False'))"
