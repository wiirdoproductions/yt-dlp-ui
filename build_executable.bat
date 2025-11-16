@echo off
REM Build script for yt-dlp UI executable
REM This script will create a standalone executable with bundled ffmpeg

echo ========================================
echo  yt-dlp UI - Build Executable
echo ========================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    echo.
)

REM Check if ffmpeg directory exists
if not exist "ffmpeg\bin\ffmpeg.exe" (
    echo WARNING: ffmpeg not found in ffmpeg\bin\ffmpeg.exe
    echo Please download ffmpeg binaries and extract to ffmpeg\bin\ directory
    echo Download from: https://www.gyan.dev/ffmpeg/builds/
    echo.
    pause
    exit /b 1
)

echo Building executable with PyInstaller...
echo.

REM Clean previous build
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

REM Build the executable
pyinstaller yt_dlp_ui.spec

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Build completed successfully!
echo ========================================
echo.
echo Executable location: dist\yt-dlp-ui.exe
echo.
echo To test: Run dist\yt-dlp-ui.exe
echo.
pause
