@echo off
REM CSV Processor Startup Script for Windows

echo 🚀 Starting CSV Processor...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    echo Visit: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not installed. Please install pip first.
    pause
    exit /b 1
)

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Check if installation was successful
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies. Please check your Python setup.
    pause
    exit /b 1
)

REM Start the server
echo 🌐 Starting server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
