@echo off
title DAB111_G13_Project - Auto Install & Run

echo ===============================================
echo      Auto Install & Run Flask Application
echo ===============================================
echo.

:: ---------------------------------------------
:: 0) CHECK PYTHON
:: ---------------------------------------------
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.11+ or newer, then run this file again.
    pause
    exit /b
)

echo Python detected.
echo.

:: ---------------------------------------------
:: 1) ASK FOR PROJECT LOCATION
:: ---------------------------------------------
set /p target_path=Enter FULL path where you want the project (e.g. D:\ST Clair\DA Courses\DBA 111): 
set /p folder_name=Enter project folder name (e.g. DAB111_G13_Project): 

set "full_path=%target_path%\%folder_name%"

if not exist "%full_path%" (
    echo Creating folder: "%full_path%"
    mkdir "%full_path%"
)

:: ---------------------------------------------
:: 2) CHECK IF PROJECT ALREADY INSTALLED
:: ---------------------------------------------
if exist "%full_path%\src\app.py" (
    echo Existing installation found.
    cd /d "%full_path%\src"
) else (
    echo No existing install found. Downloading project from GitHub...
    cd /d "%full_path%"

    :: Download ZIP
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/Adel4itca/DAB111_G13_Project/archive/refs/heads/main.zip' -OutFile 'project.zip'"

    if not exist "project.zip" (
        echo [ERROR] Failed to download project.zip from GitHub.
        pause
        exit /b
    )

    echo Extracting project...
    powershell -Command "Expand-Archive -Path 'project.zip' -DestinationPath '.' -Force"
    del project.zip

    :: Rename extracted folder to src
    if exist "DAB111_G13_Project-main" (
        ren "DAB111_G13_Project-main" "src"
    )

    if not exist "src\app.py" (
        echo [ERROR] Could not find src\app.py after extraction.
        echo Please check the GitHub repository structure.
        pause
        exit /b
    )

    cd src

    :: -----------------------------------------
    :: 3) CREATE AND SETUP VENV
    :: -----------------------------------------
    echo Creating virtual environment...
    python -m venv venv

    if not exist "venv\Scripts\activate.bat" (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b
    )

    echo Activating virtual environment...
    call venv\Scripts\activate.bat

    echo Upgrading pip and installing requirements...
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
)

:: ---------------------------------------------
:: 4) CREATE DESKTOP SHORTCUT (FIRST TIME ONLY)
:: ---------------------------------------------
set "SHORTCUT=%USERPROFILE%\Desktop\DAB111_G13_Project.url"
if not exist "%SHORTCUT%" (
    echo Creating desktop shortcut to http://127.0.0.1:5000 ...
    echo [InternetShortcut] > "%SHORTCUT%"
    echo URL=http://127.0.0.1:5000 >> "%SHORTCUT%"
    echo IconIndex=0 >> "%SHORTCUT%"
    echo IconFile=%SystemRoot%\system32\shell32.dll >> "%SHORTCUT%"
    echo Shortcut created!
)

:: ---------------------------------------------
:: 5) RUN FLASK APP
:: ---------------------------------------------
echo.
echo Starting Flask app...
call venv\Scripts\activate.bat
start "" python app.py

echo Opening browser...
start "" http://127.0.0.1:5000

echo.
echo Done. Close this window when finished.
pause
