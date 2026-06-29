@echo off
title Glyph Converter

echo ============================================================
echo  🛠️  GLYPH CONVERTER
echo ============================================================
echo.

if "%~1"=="" (
    echo ❌ Usage: glyph song.ogg
    echo.
    echo Example: glyph my_song.ogg
    echo.
    pause
    exit /b 1
)

if not exist "%~1" (
    echo ❌ File "%~1" not found!
    pause
    exit /b 1
)

python "%~dp0converter.py" "%~1"

if errorlevel 1 (
    echo.
    echo ❌ Error
    pause
)

pause