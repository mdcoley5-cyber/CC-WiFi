@echo off
title CC WiFi Radio Auto-Recovery Monitor
color 0A
cd /d "%~dp0\server"
echo =========================================================
echo       C.Crane CC WiFi Radio Auto-Recovery Tool
echo =========================================================
echo.
echo Make sure:
echo  1. The jumper wire is in place on the motherboard socket.
echo  2. The Barracuda daughtercard is reseated into the sockets.
echo  3. The Ethernet cable is plugged into your router / switch.
echo  4. The radio power cord is plugged in.
echo.
echo Starting network monitor...
echo.
python recover_radio.py
echo.
pause
