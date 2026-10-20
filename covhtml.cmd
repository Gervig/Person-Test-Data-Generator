@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\covhtml.ps1" %*
exit /b %ERRORLEVEL%