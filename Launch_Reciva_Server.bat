@echo off
cd /d "%~dp0reciva-patcher\files\RecivaServer"
powershell -Command "Start-Process '.\server.exe' -Verb RunAs"
