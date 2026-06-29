@echo off
title Glyph Converter — Libraries Installer
color 0A

echo ============================================================
echo  📦 GLYPH CONVERTER — LIBRARIES INSTALLER
echo  Installs: mutagen, pydub, colorama
echo ============================================================
echo.
echo This will install Python libraries:
echo   ✅ mutagen (for audio metadata)
echo   ✅ pydub (for audio processing)
echo   ✅ colorama (for colored console output)
echo.
echo ============================================================
echo.

:: ============================================================
:: CHECK PYTHON
:: ============================================================

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found!
    echo Please run install_dependencies.bat first
    echo.
    pause
    exit /b 1
)

echo ✅ Python found
python --version
echo.

:: ============================================================
:: INSTALL LIBRARIES
:: ============================================================

echo [1/3] Installing mutagen...
pip install mutagen --quiet
if %errorlevel% neq 0 (
    echo ⚠️ Failed to install mutagen
) else (
    echo ✅ mutagen installed
)

echo.
echo [2/3] Installing pydub...
pip install pydub --quiet
if %errorlevel% neq 0 (
    echo ⚠️ Failed to install pydub
) else (
    echo ✅ pydub installed
)

echo.
echo [3/3] Installing colorama...
pip install colorama --quiet
if %errorlevel% neq 0 (
    echo ⚠️ Failed to install colorama
) else (
    echo ✅ colorama installed
)

:: ============================================================
:: FINAL MESSAGE
:: ============================================================

echo.
echo ============================================================
echo  ✅ LIBRARIES INSTALLED SUCCESSFULLY!
echo ============================================================
echo.
echo Installed:
echo   ✅ mutagen
echo   ✅ pydub
echo   ✅ colorama
echo.
echo 📁 Now you can run: glyph my_song.ogg
echo.
echo ============================================================
echo.

pause