@echo off
REM Power BI Field Router - Startup Script
REM This script starts the Flask web server and opens the tool in your browser

echo Starting Power BI Field Router...
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Kill any existing Python processes on port 5000
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5000" ^| find "LISTENING"') do (
    taskkill /PID %%a /F 2>nul
)

echo Starting Flask server...
timeout /t 1 /nobreak

REM Start the Flask app
python3.14 app.py

pause
