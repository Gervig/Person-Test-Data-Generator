@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\cov.ps1" %*
exit /b %ERRORLEVEL%