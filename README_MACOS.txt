yt-dlp UI - macOS Version
==========================

QUICK START
-----------
Method 1: Double-Click (if .app bundle exists)
   1. Double-click "yt-dlp-ui.app" in Finder
   2. If macOS shows security warning, right-click → Open → confirm

Method 2: Terminal
   1. Open Terminal (Applications → Utilities → Terminal)
   2. Navigate to this folder:
      cd ~/Downloads/yt-dlp-ui-macos
   3. Make executable:
      chmod +x yt-dlp-ui
   4. Run:
      ./yt-dlp-ui

USING THE APP
-------------
1. Paste a video URL in the URL field
2. Click "DEST..." to choose where to save downloads
3. Click "DOWNLOAD" to start

FEATURES
--------
- Download videos from 1800+ websites (YouTube, Vimeo, etc.)
- Download playlists with flexible options
- Extract audio to MP3, M4A, Opus, or WAV
- Download subtitles in any language
- Bypass age restrictions with cookies
- Live download progress monitoring

FFMPEG
------
FFmpeg is included in the "ffmpeg" folder and will be
automatically detected. No additional configuration needed!

TROUBLESHOOTING
---------------
Security Warning:
   - macOS may block the app because it's not from the App Store
   - Right-click the app → Open → Click "Open" to bypass

FFmpeg Not Detected:
   1. The app will show a warning
   2. Use "BROWSE" to locate: ffmpeg/bin/ffmpeg
   3. Click "AUTO-DETECT" to search again

Age-Restricted Videos:
   1. Export cookies from your browser
   2. Use "BROWSE" in "Network / Behavior" section
   3. Select your cookies.txt file

SYSTEM REQUIREMENTS
-------------------
- macOS 10.13 (High Sierra) or newer
- Internet connection

SUPPORT & DOCUMENTATION
-----------------------
Full documentation and updates:
https://github.com/wiirdoproductions/yt-dlp-ui

Report bugs or request features:
https://github.com/wiirdoproductions/yt-dlp-ui/issues

LEGAL
-----
This software uses FFmpeg under LGPL 2.1 license.
See FFMPEG_LICENSE.txt for details.

This software uses yt-dlp (Unlicense license).
See LICENSE.txt for the yt-dlp UI wrapper license.

DISCLAIMER
----------
This tool is for personal use only. Respect copyright laws
and the terms of service of websites you download from.

---
Made with ❤️ for the community
