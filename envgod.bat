@echo off
REM EnvironmentGod Launcher for Windows

REM Change to script directory
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.6+ and try again
    pause
    exit /b 1
)

REM Run the application
if "%1"=="" (
    REM No arguments, run GUI
    python main.py
) else (
    REM Arguments provided, run CLI
    python main.py %*
)
