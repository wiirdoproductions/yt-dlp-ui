# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for yt-dlp UI
# Build with: pyinstaller yt_dlp_ui.spec

block_cipher = None

a = Analysis(
    ['yt_dlp_ui.py'],
    pathex=[],
    binaries=[
        # Bundle ffmpeg binaries (update path after downloading ffmpeg)
        ('ffmpeg/bin/ffmpeg.exe', 'ffmpeg/bin'),
        ('ffmpeg/bin/ffprobe.exe', 'ffmpeg/bin'),
    ],
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
