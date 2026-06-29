@echo off
title Glyph Converter — Dependencies Installer
color 0A

echo ============================================================
echo  📦 GLYPH CONVERTER — DEPENDENCIES INSTALLER
echo  Installs: Python, Audacity, ffmpeg
echo ============================================================
echo.
echo This will install:
echo   ✅ Python 3.11 (if not installed)
echo   ✅ Audacity (latest)
echo   ✅ ffmpeg (latest)
echo.
echo ============================================================
echo.

:: ============================================================
:: CHECK ADMIN RIGHTS
:: ============================================================

net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Administrator rights required!
    echo Please right-click and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

:: ============================================================
:: 1. INSTALL PYTHON
:: ============================================================

echo.
echo [1/3] Checking Python...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Python not found. Downloading Python 3.11...
    
    set PYTHON_URL=https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe
    set PYTHON_INSTALLER=%TEMP%\python-installer.exe
    
    echo 📥 Downloading Python...
    powershell -Command "Invoke-WebRequest -Uri %PYTHON_URL% -OutFile %PYTHON_INSTALLER%"
    
    if %errorlevel% neq 0 (
        echo ❌ Failed to download Python
        echo Please download manually from python.org
        pause
        exit /b 1
    )
    
    echo 📦 Installing Python...
    %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    
    if %errorlevel% neq 0 (
        echo ❌ Python installation failed
        pause
        exit /b 1
    )
    
    echo ✅ Python installed successfully!
    echo.
    
    :: Refresh PATH
    set PATH=%PATH%;C:\Program Files\Python311;C:\Program Files\Python311\Scripts
) else (
    echo ✅ Python already installed
    python --version
    echo.
)

:: ============================================================
:: 2. INSTALL AUDACITY
:: ============================================================

echo [2/3] Checking Audacity...

if exist "C:\Program Files\Audacity\Audacity.exe" (
    echo ✅ Audacity already installed
) else (
    echo ⚠️ Audacity not found. Downloading...
    
    set AUDACITY_URL=https://github.com/audacity/audacity/releases/download/Audacity-3.4.2/audacity-win-3.4.2-x64.exe
    set AUDACITY_INSTALLER=%TEMP%\audacity-installer.exe
    
    echo 📥 Downloading Audacity...
    powershell -Command "Invoke-WebRequest -Uri %AUDACITY_URL% -OutFile %AUDACITY_INSTALLER%"
    
    if %errorlevel% neq 0 (
        echo ❌ Failed to download Audacity
        echo Please download manually from audacityteam.org
        pause
        exit /b 1
    )
    
    echo 📦 Installing Audacity...
    %AUDACITY_INSTALLER% /SILENT
    
    if %errorlevel% neq 0 (
        echo ❌ Audacity installation failed
        pause
        exit /b 1
    )
    
    echo ✅ Audacity installed successfully!
    echo.
)

:: ============================================================
:: 3. INSTALL FFMPEG
:: ============================================================

echo [3/3] Checking ffmpeg...

ffmpeg -version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ ffmpeg already installed
) else (
    echo ⚠️ ffmpeg not found. Downloading...
    
    set FFMPEG_URL=https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
    set FFMPEG_ZIP=%TEMP%\ffmpeg.zip
    set FFMPEG_DIR=C:\ffmpeg
    
    echo 📥 Downloading ffmpeg...
    powershell -Command "Invoke-WebRequest -Uri %FFMPEG_URL% -OutFile %FFMPEG_ZIP%"
    
    if %errorlevel% neq 0 (
        echo ❌ Failed to download ffmpeg
        echo Please download manually from ffmpeg.org
        pause
        exit /b 1
    )
    
    echo 📦 Extracting ffmpeg...
    powershell -Command "Expand-Archive -Path %FFMPEG_ZIP% -DestinationPath C:\ -Force"
    
    :: Rename extracted folder to ffmpeg
    for /d %%i in (C:\ffmpeg-*) do move "%%i" "C:\ffmpeg" >nul 2>&1
    
    :: Add ffmpeg to PATH
    setx PATH "%PATH%;C:\ffmpeg\bin" /M
    
    echo ✅ ffmpeg installed successfully!
    echo.
)

:: ============================================================
:: 4. FINAL MESSAGE
:: ============================================================

echo.
echo ============================================================
echo  ✅ DEPENDENCIES INSTALLED SUCCESSFULLY!
echo ============================================================
echo.
echo Installed:
echo   ✅ Python 3.11
echo   ✅ Audacity
echo   ✅ ffmpeg
echo.
echo 📁 Now run: install_libraries.bat to install Python libraries
echo.
echo ============================================================
echo.

pause