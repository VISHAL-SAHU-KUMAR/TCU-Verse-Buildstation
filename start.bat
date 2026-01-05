@echo off
echo ======================================
echo   SkillLens AI - Career Intelligence
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [INFO] Python found
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created
    echo.
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install dependencies
echo [INFO] Installing dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [SUCCESS] Dependencies installed
echo.

REM Create necessary directories
if not exist "database" mkdir database
if not exist "uploads" mkdir uploads
if not exist "models" mkdir models

echo [INFO] Starting SkillLens AI server...
echo.
echo ======================================
echo   Server running at:
echo   http://127.0.0.1:5000
echo ======================================
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the Flask server
cd backend
python app.py

REM Deactivate virtual environment on exit
cd ..
call venv\Scripts\deactivate.bat
