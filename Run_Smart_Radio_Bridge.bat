@echo off
title CC WiFi Smart Radio Bridge
cd /d "%~dp0server"

echo ========================================================
echo        Starting CC WiFi Smart Radio Bridge...
echo ========================================================
echo.
echo Opening browser to http://localhost:5000 in 2 seconds...
start "" http://localhost:5000
python app.py
pause
