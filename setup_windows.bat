@echo off
REM Webcam Streaming Service Setup Script for Windows

echo Setting up Webcam Streaming Service...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is required but not installed.
    echo Please download and install Python from https://python.org
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating Python virtual environment...
python -m venv .venv

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install Python dependencies
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install opencv-python numpy

echo Setup complete!
echo.
echo To start streaming:
echo 1. Run: .venv\Scripts\activate.bat
echo 2. Run: python webcam_http_stream.py
echo.
echo Or run directly: .venv\Scripts\python.exe webcam_http_stream.py
pause
