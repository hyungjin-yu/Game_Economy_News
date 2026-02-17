@echo off
cd /d "%~dp0"

echo ========================================================
echo   Game Dev News Notifier - Task Scheduler Setup
echo ========================================================
echo.

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    echo Installing dependencies...
    call venv\Scripts\activate
    pip install -r requirements.txt
)

set VENV_PYTHON="%~dp0venv\Scripts\pythonw.exe"
set SCRIPT="%~dp0src\main.py"
set TASK_NAME="GameDevNewsNotifier_Daily"
set TIME=09:50

echo.
echo Registering task to run daily at %TIME%...
echo Python Path: %VENV_PYTHON%
echo Script Path: %SCRIPT%
echo.

schtasks /create /tn %TASK_NAME% /tr "%VENV_PYTHON% %SCRIPT% --run-now" /sc daily /st %TIME% /f

if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Task registered successfully!
    echo The program will run silently in the background every day at %TIME%.
    echo You can close all windows now.
    echo Check 'activity.log' if you want to see the execution history.
) else (
    echo.
    echo [ERROR] Failed to register task. Please run as Administrator.
)

echo.
pause
