@echo off
echo ===============================================
echo Anti-Theft Alarm System - Setup Script
echo ===============================================
echo.

REM Check Python installation
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python 3.8 or higher.
    pause
    exit /b 1
)
python --version
echo.

REM Create virtual environment
echo [2/5] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo [4/5] Installing dependencies...
echo This may take several minutes...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.

REM Create storage directories
echo [5/5] Creating storage directories...
if not exist "storage" mkdir storage
if not exist "storage\intruders" mkdir storage\intruders
if not exist "storage\logs" mkdir storage\logs
if not exist "storage\authorized_faces" mkdir storage\authorized_faces
echo Storage directories created.
echo.

echo ===============================================
echo Setup Complete!
echo ===============================================
echo.
echo To run the system:
echo   1. Activate venv: venv\Scripts\activate.bat
echo   2. Run: python main.py
echo.
echo Optional: Add authorized face images to:
echo   storage\authorized_faces\person_name.jpg
echo.
pause
