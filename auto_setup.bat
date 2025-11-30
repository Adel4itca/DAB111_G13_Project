@echo off
title DAB111_G13_Project - Auto Install & Run

echo ===============================================
echo      Auto Install & Run Flask Application
echo ===============================================
echo.

:: --- Ask user where to install the project ---
set /p target_path=Enter the FULL path where you want to install the app: 

echo.
:: --- Ask user for the folder name they want ---
set /p folder_name=Enter a NAME for the project folder (no spaces): 

echo.
echo Installing into:
echo   %target_path%\%folder_name%
echo.

:: Create parent folder if not exists
if not exist "%target_path%" (
    echo Parent folder does NOT exist. Creating it...
    mkdir "%target_path%"
)

:: Go to the target directory
cd /d "%target_path%"

:: ---------------------------------------------
:: 1) Create chosen folder
:: ---------------------------------------------
if not exist "%folder_name%" (
    mkdir "%folder_name%"
) else (
    echo [WARNING] Folder already exists. Files may be overwritten.
)

cd "%folder_name%"

:: ---------------------------------------------
:: 2) Download ZIP from GitHub
:: ---------------------------------------------
echo Downloading project ZIP from GitHub...
powershell -Command "Invoke-WebRequest -Uri https://github.com/Adel4itca/DAB111_G13_Project/archive/refs/heads/main.zip -OutFile project.zip"

if not exist project.zip (
    echo [ERROR] Could not download the GitHub ZIP file.
    pause
    exit /b
)

echo Extracting ZIP...
powershell -Command "Expand-Archive project.zip -DestinationPath . -Force"
del project.zip

:: The downloaded folder is 'DAB111_G13_Project-main'
if exist DAB111_G13_Project-main (
    echo Renaming extracted folder...
    move DAB111_G13_Project-main src
) else (
    echo [ERROR] Extracted folder not found.
    pause
    exit /b
)

cd src

:: ---------------------------------------------
:: 3) Setup virtual environment
:: ---------------------------------------------
echo Checking for venv...

if not exist venv (
    echo Creating new virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists.
)

echo Activating virtual environment...
call venv\Scripts\activate

:: ---------------------------------------------
:: 4) Install dependencies
:: ---------------------------------------------
if exist requirements.txt (
    echo Installing dependencies...
    pip install --upgrade pip
    pip install -r requirements.txt
) else (
    echo [WARNING] No requirements.txt found.
)

:: ---------------------------------------------
:: 5) Run Flask application
:: ---------------------------------------------
echo Starting Flask app...
python app.py

echo.
echo Application is running at:
echo     http://127.0.0.1:5000
echo.
pause
