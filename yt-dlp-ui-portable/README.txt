yt-dlp UI - Portable Version v1.0.2
====================================

WHAT'S NEW in v1.0.2
--------------------
CRITICAL BUG FIX: Download button no longer spawns multiple app instances.
Previous versions had a bug where clicking DOWNLOAD would open new windows
instead of downloading. This has been fixed. All users should update!


QUICK START
-----------
1. Double-click "yt-dlp-ui.exe" to launch the application
2. Paste a video URL in the URL field
3. Click "DEST..." to choose where to save your downloads
4. Click "DOWNLOAD" to start downloading

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

REQUIREMENTS
------------
- Windows 10/11 (64-bit)
- Internet connection

TROUBLESHOOTING
---------------
If FFmpeg is not detected:
1. The app will show a warning
2. Use the "BROWSE" button to locate: ffmpeg\bin\ffmpeg.exe
3. Click "AUTO-DETECT" to search again

For age-restricted videos:
1. Export cookies from your browser (see full README on GitHub)
2. Use the "BROWSE" button in "Network / Behavior" section
3. Select your cookies.txt file

SUPPORT & DOCUMENTATION
-----------------------
For detailed instructions, troubleshooting, and updates:
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
