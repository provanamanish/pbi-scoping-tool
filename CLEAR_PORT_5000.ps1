#!/bin/powershell
# Aggressively kill ALL processes on port 5000 and start Flask fresh

Write-Host "Clearing port 5000..." -ForegroundColor Yellow

# Loop until port is truly free
for ($i = 0; $i -lt 10; $i++) {
    $processes = (netstat -ano | Select-String ":5000.*LISTENING" | ForEach-Object { 
        $parts = $_ -split '\s+'
        $parts[-1]
    }) | Where-Object {$_ -ne ''}
    
    if ($processes -eq $null -or $processes.Count -eq 0) {
        Write-Host "Port 5000 is now free!" -ForegroundColor Green
        break
    }
    
    Write-Host "Found processes on :5000: $($processes -join ', ')"
    
    foreach ($pid in @($processes)) {
        if ($pid) {
            Write-Host "Killing PID $pid..." -ForegroundColor Cyan
            taskkill /PID $pid /F /T 2>$null | Out-Null
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue 2>$null
            wmic process where processid=$pid delete 2>$null | Out-Null
        }
    }
    
    Start-Sleep -Milliseconds 500
}

# Verify final state
$remaining = netstat -ano | Select-String ":5000.*LISTENING" | Measure-Object | % Count
Write-Host "`nFinal port check: $remaining processes on :5000"

if ($remaining -eq 0) {
    Write-Host "`n[OK] Port 5000 is completely free. Starting Flask..." -ForegroundColor Green
    python3.13 app.py
} else {
    Write-Host "`n[ERROR] Could not clear port 5000! Stubborn zombie process(es) remain." -ForegroundColor Red
    Write-Host "Try rebooting the machine." -ForegroundColor Yellow
}
