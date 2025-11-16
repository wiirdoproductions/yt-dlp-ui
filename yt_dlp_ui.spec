# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for yt-dlp UI
# Build with: pyinstaller yt_dlp_ui.spec
# Cross-platform: Works on Windows, macOS, and Linux

import sys
import os

block_cipher = None

# Platform-specific ffmpeg binaries
binaries = []
if sys.platform == 'win32':
    # Windows: ffmpeg.exe and ffprobe.exe
    if os.path.exists('ffmpeg/bin/ffmpeg.exe'):
        binaries.extend([
            ('ffmpeg/bin/ffmpeg.exe', 'ffmpeg/bin'),
            ('ffmpeg/bin/ffprobe.exe', 'ffmpeg/bin'),
        ])
elif sys.platform == 'darwin':
    # macOS: ffmpeg and ffprobe binaries
    if os.path.exists('ffmpeg/bin/ffmpeg'):
        binaries.extend([
            ('ffmpeg/bin/ffmpeg', 'ffmpeg/bin'),
            ('ffmpeg/bin/ffprobe', 'ffmpeg/bin'),
        ])
else:
    # Linux: ffmpeg and ffprobe binaries
    if os.path.exists('ffmpeg/bin/ffmpeg'):
        binaries.extend([
            ('ffmpeg/bin/ffmpeg', 'ffmpeg/bin'),
            ('ffmpeg/bin/ffprobe', 'ffmpeg/bin'),
        ])

a = Analysis(
    ['yt_dlp_ui.py'],
    pathex=[],
    binaries=binaries,
    datas=[],
    hiddenimports=['yt_dlp'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='yt-dlp-ui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Compress executable with UPX if available
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Hide console window (GUI app)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Set to 'icon.ico' if you add an icon file
)
