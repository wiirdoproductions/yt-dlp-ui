# Build Instructions for yt-dlp UI

This guide explains how to build the standalone executable and create distribution packages.

## Prerequisites

1. **Python 3.8+** installed
2. **Git** (optional, for cloning)
3. **yt-dlp** installed: `pip install yt-dlp`
4. **PyInstaller** installed: `pip install pyinstaller`

## Step 1: Download FFmpeg

1. Go to https://www.gyan.dev/ffmpeg/builds/
2. Download **ffmpeg-release-essentials.zip** (smaller) or **ffmpeg-release-full.zip**
3. Extract the ZIP file
4. Copy the following structure to your project directory:

```
yt-dlp/
├── ffmpeg/
│   └── bin/
│       ├── ffmpeg.exe
│       ├── ffprobe.exe
│       └── (other DLL files)
├── yt_dlp_ui.py
├── yt_dlp_ui.spec
└── build_executable.bat
```

**Note:** The `ffmpeg/bin/` folder should contain at minimum `ffmpeg.exe` and `ffprobe.exe`.

## Step 2: Build the Executable

### Method 1: Using the Build Script (Easy)

Simply run:
```bash
build_executable.bat
```

The script will:
- Check if PyInstaller is installed
- Verify ffmpeg binaries exist
- Clean previous builds
- Build the executable
- Report success/failure

### Method 2: Manual Build

```bash
# Clean previous builds
rmdir /s /q build
rmdir /s /q dist

# Build using spec file
pyinstaller yt_dlp_ui.spec
```

The executable will be created at: `dist\yt-dlp-ui.exe`

## Step 3: Test the Executable

1. Navigate to `dist` folder
2. Run `yt-dlp-ui.exe`
3. Test basic functionality:
   - Check if FFmpeg is auto-detected
   - Try downloading a public YouTube video
   - Verify audio extraction works
   - Test playlist options

## Step 4: Create Distribution Package

### For Portable ZIP Distribution:

1. Create a new folder named `yt-dlp-ui-portable`
2. Copy the following files:
   ```
   yt-dlp-ui-portable/
   ├── yt-dlp-ui.exe          (from dist folder)
   ├── README.txt              (simplified usage instructions)
   ├── FFMPEG_LICENSE.txt      (FFmpeg attribution)
   └── LICENSE.txt             (your MIT license)
   ```

3. Create a simple `README.txt` for non-technical users:

```txt
yt-dlp UI - Portable Version
============================

QUICK START:
1. Double-click yt-dlp-ui.exe to launch
2. Paste a video URL
3. Click DEST... to choose where to save
4. Click DOWNLOAD

FFmpeg is included and will be auto-detected.

For detailed instructions and troubleshooting:
Visit: https://github.com/YOUR_USERNAME/yt-dlp-ui

LEGAL:
This software uses FFmpeg under LGPL 2.1 license.
See FFMPEG_LICENSE.txt for details.
```

4. Compress the folder to `yt-dlp-ui-portable-v1.0.0.zip`

### File Size Expectations:

- **Without FFmpeg bundled**: ~20-30 MB
- **With FFmpeg bundled**: ~100-150 MB

## Step 5: Create GitHub Release

1. Go to your GitHub repository
2. Click "Releases" → "Create a new release"
3. Tag version: `v1.0.0`
4. Release title: `yt-dlp UI v1.0.0`
5. Description: Copy the feature list from README.md
6. Upload the ZIP file as a release asset
7. Mark as "Latest release"
8. Publish

## Troubleshooting Build Issues

### "ffmpeg.exe not found" during build

**Solution:** Verify that `ffmpeg/bin/ffmpeg.exe` exists in your project directory before building.

### Build succeeds but executable crashes

**Solution:**
1. Build without `--onefile` for testing:
   ```bash
   pyinstaller --noconsole yt_dlp_ui.py
   ```
2. Check the console output in `dist/yt_dlp_ui/` folder
3. Look for missing modules in PyInstaller's warnings

### Executable is too large

**Solution:**
1. Enable UPX compression (already enabled in spec file)
2. Install UPX: Download from https://upx.github.io/
3. Add UPX to your PATH
4. Rebuild

### Antivirus flags the executable

**Solution:**
1. This is normal with PyInstaller (false positive)
2. Upload to VirusTotal.com for analysis
3. Submit to antivirus vendors as false positive
4. Add instructions to README for adding exceptions

## Advanced: Automated Builds with GitHub Actions

You can automate builds for every release using GitHub Actions.

Create `.github/workflows/build-release.yml`:

```yaml
name: Build Release

on:
  release:
    types: [created]

jobs:
  build-windows:
    runs-on: windows-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install pyinstaller yt-dlp

    - name: Download FFmpeg
      run: |
        curl -L https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip -o ffmpeg.zip
        7z x ffmpeg.zip
        mkdir ffmpeg\bin
        move ffmpeg-*\bin\*.exe ffmpeg\bin\
        move ffmpeg-*\bin\*.dll ffmpeg\bin\

    - name: Build with PyInstaller
      run: pyinstaller yt_dlp_ui.spec

    - name: Create portable package
      run: |
        mkdir portable
        copy dist\yt-dlp-ui.exe portable\
        copy FFMPEG_LICENSE.txt portable\
        copy LICENSE portable\LICENSE.txt
        echo Quick Start: Run yt-dlp-ui.exe > portable\README.txt

    - name: Upload to Release
      uses: softprops/action-gh-release@v1
      with:
        files: portable/*
```

## Version Numbering

Follow semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

Example: v1.0.0 → v1.1.0 (added playlist support) → v1.1.1 (fixed bug)

## Maintenance

### For updates:
1. Make changes to `yt_dlp_ui.py`
2. Test thoroughly
3. Update version number in `APP_TITLE` or add version variable
4. Rebuild executable
5. Create new GitHub release with changelog

### For yt-dlp updates:
Users running the source version will automatically get updates via:
```bash
pip install --upgrade yt-dlp
```

Portable version users will need to download new releases.

---

**Questions or issues?** Open an issue on GitHub!
