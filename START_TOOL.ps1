# Power BI Field Router - Startup Script (PowerShell)
# This script starts the Flask web server

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host " Power BI Field Router Startup" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Set location to script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Kill any existing Python processes on port 5000
Write-Host "Cleaning up any previous instances..." -ForegroundColor Yellow
Get-Process python3.14 -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "Starting Flask server..." -ForegroundColor Green
Write-Host "Access the tool at: http://127.0.0.1:5000/" -ForegroundColor Cyan
Write-Host ""

# Start the Flask app
python3.14 app.py
