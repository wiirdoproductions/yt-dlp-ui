# Changelog

All notable changes to yt-dlp UI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2025-11-16

### Fixed
- Fixed critical bug where clicking the DOWNLOAD button in compiled .exe spawns multiple instances of the application instead of executing the download
- Added `multiprocessing.freeze_support()` to properly handle subprocess spawning in PyInstaller frozen executables on Windows

### Technical Details
- The issue occurred because Windows was attempting to spawn the entire GUI application when subprocess.Popen() was called in the frozen executable
- Solution: Added freeze_support() call in main block to properly initialize multiprocessing support for PyInstaller

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
