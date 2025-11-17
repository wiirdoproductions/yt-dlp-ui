# yt-dlp UI v1.0.2 - Bug Fix Release

A modern, user-friendly graphical interface for yt-dlp, the powerful video downloader.

## 🎉 Features

### Core Functionality
- **Simple URL Download** - Paste any video URL and download
- **Batch Downloads** - Load a text file with multiple URLs
- **Format Selection** - Choose best quality, audio only, or custom formats
- **Real-time Logging** - Monitor download progress in built-in console
- **Live Command Preview** - See the exact yt-dlp command before downloading

### Playlist Support
- Download entire playlists or specific ranges
- Recent-only mode (download latest video)
- Episodes mode (download specific videos: 1,3,5 or 1-5)
- Flexible range selection (e.g., videos 10-20)

### Audio Extraction
- Convert to MP3, M4A, Opus, or WAV
- Custom bitrate configuration
- Re-encode option with ffmpeg

### Advanced Features
- **Subtitle Downloads** - Download and embed subtitles in multiple languages
- **Metadata & Thumbnails** - Automatically embed thumbnails and metadata
- **Authentication** - Bypass age restrictions with cookies or login credentials
- **Network Controls** - Rate limiting, proxy support, retry configuration
- **Custom Arguments** - Pass any yt-dlp command-line argument

## 📦 What's Included

### Portable Version (Recommended)
- Standalone executable (no Python required)
- Bundled ffmpeg binaries (~200 MB total)
- Complete documentation
- License files

### Source Code
- Full Python source code
- Build scripts for creating your own executable
- Detailed build instructions

## 🖥️ System Requirements

- **OS**: Windows 10/11 (64-bit)
- **RAM**: 2 GB minimum
- **Disk Space**: 500 MB for portable version
- **Internet**: Required for downloads

## 📥 Download

**Portable Version** (Recommended for most users):
- Download `yt-dlp-ui-portable-v1.0.2.zip` (198 MB)
- Extract and run `yt-dlp-ui.exe`
- No installation needed!

**Source Code**:
- Clone the repository or download source
- Requires Python 3.8+
- See README.md for setup instructions

## 🚀 Quick Start

1. Download and extract the portable ZIP
2. Run `yt-dlp-ui.exe`
3. Paste a video URL
4. Click "DEST..." to choose save location
5. Click "DOWNLOAD"

## 🐛 Bug Fixes in v1.0.2

### Critical Fix
- **FIXED**: Download button no longer spawns multiple application instances
  - Previous version had a critical bug where clicking DOWNLOAD in the .exe would open additional windows instead of downloading
  - This has been completely resolved by refactoring to use yt-dlp's Python API instead of subprocess
  - All users of v1.0.0 and v1.0.1 should update immediately

### Improvements
- Better download progress reporting with real-time updates
- Enhanced error handling and logging
- More reliable and maintainable codebase

## 🐛 Known Issues

None currently reported!

## 📝 Notes

- FFmpeg is included and automatically detected
- Supports 1800+ websites (YouTube, Vimeo, Twitch, etc.)
- For age-restricted content, use cookies.txt method
- See full documentation in README.md

## 🙏 Credits

- **yt-dlp**: https://github.com/yt-dlp/yt-dlp
- **FFmpeg**: https://ffmpeg.org/
- **Python & Tkinter**

## 📄 License

MIT License for the UI wrapper
LGPL 2.1 for bundled FFmpeg

---

**v1.0.2 Update**: Critical download bug fixed. All users should update to this version.

Report any issues at: https://github.com/wiirdoproductions/yt-dlp-ui/issues
