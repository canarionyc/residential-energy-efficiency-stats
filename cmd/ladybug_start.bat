@echo off
echo =========================================
echo Starting Ladybug Tools Environment...
echo =========================================

:: 1. Set your custom variables
set RADIANCE_HOME=C:\Radiance-5-4
set RAYPATH=%RADIANCE_HOME%\lib

:: 2. SAFELY append to the existing Windows PATH
:: By adding %PATH%; at the beginning, we keep everything Windows needs
set PATH=%PATH%;%RHINO8_HOME%\System;%RADIANCE_HOME%\bin

:: 3. Launch Rhino
start "Rhino 8" "%RHINO8_HOME%\System\Rhino.exe" /scheme="LadybugToolsWorkflow"

exit