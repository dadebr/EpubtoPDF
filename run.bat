@echo off
REM Windows batch script to update, install dependencies, and run the EpubtoPDF application
REM Usage: run.bat [arguments to pass to the Python application]

REM 1) Change to the repo root (where this batch file is located)
cd /d "%~dp0"

REM 2) Run git pull to update the repository
echo Updating repository...
git pull
if %errorlevel% neq 0 (
    echo Warning: Git pull failed. Continuing anyway...
)

REM 3) Install/update dependencies from requirements.txt
echo Installing/updating dependencies...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies.
    pause
    exit /b 1
)

REM 4) Set PYTHONPATH to include the src directory
set PYTHONPATH=%~dp0src

REM 5) Change to the src directory
cd /d "%~dp0src"
if %errorlevel% neq 0 (
    echo Error: Could not change to src directory.
    pause
    exit /b 1
)

REM 6) Run the Python application with all passed arguments
echo Starting EpubtoPDF...
python -m epubtopdf.main %*
