# Changelog

All notable changes to yt-dlp UI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2025-11-16

### Fixed
- **Critical**: Fixed bug where clicking DOWNLOAD button in compiled .exe spawns multiple application instances instead of downloading
- Completely refactored to use yt-dlp Python API instead of subprocess calls
- This fix ensures the portable executable works correctly for all users

### Changed
- Replaced subprocess-based yt-dlp execution with direct Python API integration
- Improved download progress reporting with real-time updates
- Enhanced error handling and logging
- Better integration between GUI and yt-dlp functionality

### Technical Details
- Root cause: Using `subprocess.Popen([sys.executable, '-m', 'yt_dlp'])` in frozen executables caused `sys.executable` to point to the GUI .exe instead of Python
- Solution: Migrated to `yt_dlp.YoutubeDL()` Python API for direct module usage
- Added custom logger class to redirect yt-dlp output to GUI
- Implemented progress hooks for real-time download status
- This is the recommended approach for PyInstaller applications per PyInstaller documentation

## [1.0.1] - 2025-11-16

### Added
- GitHub Actions workflow for automated multi-platform builds

## [1.0.0] - 2025-11-16

### Added
- Initial release of yt-dlp UI
- Graphical user interface for yt-dlp video downloader
- Format selection (best quality, audio only, custom formats)
- Playlist support with range selection
- Audio extraction with multiple format options (MP3, M4A, Opus, WAV)
- Subtitle download and embedding
- Metadata and thumbnail embedding
- Authentication support (username/password, cookies)
- Network controls (rate limiting, proxy, retries)
- Live command preview
- Real-time download logging
- Batch download from text files
- FFmpeg integration and auto-detection
- Portable Windows executable with bundled FFmpeg

### Notes
- Supports 1800+ websites through yt-dlp
- No Python installation required for portable version
- Complete documentation included
