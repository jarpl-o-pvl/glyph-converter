@echo off
title Auto Glyph Converter

echo ============================================================
echo  🚀 AUTO GLYPH CONVERTER
echo  Choose your Nothing Phone model manually!
echo  Just drop your .ogg file and wait 1 minute!
echo ============================================================
echo.

if "%~1"=="" (
    echo ❌ Usage: auto-glyph song.ogg
    echo.
    echo Example: auto-glyph my_song.ogg
    echo.
    pause
    exit /b 1
)

if "%~1"=="--help" (
    python "%~dp0auto_converter.py" --help
    pause
    exit /b 0
)

if not exist "%~1" (
    echo ❌ File "%~1" not found!
    pause
    exit /b 1
)

python "%~dp0auto_converter.py" "%~1"

if errorlevel 1 (
    echo.
    echo ❌ Error
    pause
)

pause