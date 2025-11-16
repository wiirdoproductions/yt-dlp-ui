import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import threading
import shutil
import os
import sys
import queue

# Retro style single-window yt-dlp + FFmpeg frontend for Windows
# - Compact, all controls visible in one window
# - FFmpeg auto-detection and manual browse
# - Command builder, live log, background process
# - Designed for Windows (but should run on other platforms with minor tweaks)

APP_TITLE = "yt-dlp UI"
WINDOW_WIDTH = 1150
WINDOW_HEIGHT = 800

# Helper: detect ffmpeg.exe in bundled location, PATH, or common locations
def detect_ffmpeg():
    exe_name = "ffmpeg.exe" if os.name == 'nt' else "ffmpeg"

    # 1. Check bundled location first (for packaged executable)
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        app_dir = os.path.dirname(sys.executable)
    else:
        # Running as Python script
        app_dir = os.path.dirname(os.path.abspath(__file__))

    bundled_locations = [
        os.path.join(app_dir, 'ffmpeg', 'bin', exe_name),
        os.path.join(app_dir, 'ffmpeg', exe_name),
        os.path.join(app_dir, exe_name)
    ]

    for bundled_path in bundled_locations:
        if os.path.isfile(bundled_path):
            return bundled_path

    # 2. Check PATH
    path = shutil.which(exe_name)
    if path:
        return path

    # 3. Check common Windows locations
    common = [
        os.path.join(os.environ.get('ProgramFiles', ''), 'ffmpeg', 'bin', 'ffmpeg.exe'),
        os.path.join(os.environ.get('ProgramFiles(x86)', ''), 'ffmpeg', 'bin', 'ffmpeg.exe'),
        os.path.join(os.environ.get('USERPROFILE', ''), 'ffmpeg', 'bin', 'ffmpeg.exe')
    ]
    for p in common:
        if p and os.path.isfile(p):
            return p

    return ""

# Thread-safe logger queue
log_q = queue.Queue()

class TrainerUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)
        self.configure(bg='#0b0b0b')  # very dark background

        # retro fonts/colors
        self.fg = '#b6f08a'  # greenish text
        self.input_bg = '#222222'
        self.button_bg = '#222222'
        self.highlight = '#0f9d58'

        self.create_variables()
        self.create_widgets()
        self.ffmpeg_path_var.set(detect_ffmpeg())
        self.process = None
        self.stop_requested = False
        self.after(100, self._poll_log_queue)

    def create_variables(self):
        self.url_var = tk.StringVar()
        self.batch_file_var = tk.StringVar()
        self.output_template_var = tk.StringVar(value='%(title)s.%(ext)s')
        self.dest_folder_var = tk.StringVar()

        # format selection
        self.format_choice = tk.StringVar(value='best')  # best, audio, custom
        self.custom_format_var = tk.StringVar()

        # audio options
        self.audio_extract_var = tk.BooleanVar(value=False)
        self.audio_format_var = tk.StringVar(value='mp3')
        self.audio_bitrate_var = tk.StringVar(value='192k')

        # playlist options
        self.playlist_var = tk.StringVar(value='off')  # off or on
        self.playlist_items_var = tk.StringVar(value='all')  # all or recent
        self.playlist_range_start_var = tk.StringVar()
        self.playlist_range_end_var = tk.StringVar()
        self.playlist_episodes_var = tk.StringVar()

        # subtitles and metadata
        self.subtitles_var = tk.BooleanVar(value=False)
        self.subtitle_lang_var = tk.StringVar(value='en')
        self.embed_thumbnail_var = tk.BooleanVar(value=False)
        self.add_metadata_var = tk.BooleanVar(value=False)

        # authentication
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # network/behavior
        self.rate_limit_var = tk.StringVar()
        self.retries_var = tk.StringVar(value='10')
        self.cookies_var = tk.StringVar()
        self.proxy_var = tk.StringVar()

        # ffmpeg
        self.ffmpeg_path_var = tk.StringVar()
        self.merge_method_var = tk.StringVar(value='ffmpeg')  # ffmpeg or native
        self.reencode_var = tk.BooleanVar(value=False)

        # misc
        self.extra_args_var = tk.StringVar()

    def create_widgets(self):
        # top title bar (retro)
        title = tk.Label(self, text=APP_TITLE, fg=self.fg, bg='#0b0b0b', font=('Consolas', 22, 'bold'))
        title.place(x=12, y=8)

        # Left column: Inputs & Options
        left = tk.Frame(self, bg='#0b0b0b')
        left.place(x=10, y=50, width=770, height=750)

        # URL
        self._label(left, "URL:", 0, 0)
        url_entry = self._entry(left, self.url_var, 0, 1, width=40)
        batch_btn = tk.Button(left, text="BATCH URL..", command=self.choose_batch_file, bg=self.button_bg, fg=self.fg,
                 width=12, font=('Consolas', 9))
        batch_btn.place(x=630, y=0)

        # Output template and destination
        self._label(left, "Output template:", 1, 0)
        self._entry(left, self.output_template_var, 1, 1, width=46)
        dest_btn = tk.Button(left, text="DEST...", command=self.choose_dest, bg=self.button_bg, fg=self.fg,
                 width=8, font=('Consolas', 9))
        dest_btn.place(x=630, y=35)

        self._label(left, "Destination folder:", 2, 0)
        self.dest_entry = self._entry(left, self.dest_folder_var, 2, 1, width=66)

        # Format selection (radio-style)
        box1 = self._group(left, "Format Selection", 3)
        rb_best = tk.Radiobutton(box1, text='Best (video+audio)', variable=self.format_choice, value='best',
                                 fg=self.fg, bg='#0b0b0b', selectcolor='#0b0b0b', activebackground='#0b0b0b',
                                 font=('Consolas', 11))
        rb_best.grid(row=0, column=0, sticky='w', pady=4)
        rb_audio = tk.Radiobutton(box1, text='Audio only', variable=self.format_choice, value='audio',
                                  fg=self.fg, bg='#0b0b0b', selectcolor='#0b0b0b', font=('Consolas', 11))
        rb_audio.grid(row=0, column=1, sticky='w', padx=12, pady=4)
        rb_custom = tk.Radiobutton(box1, text='Custom format (use entry field below)', variable=self.format_choice, value='custom',
                                   fg=self.fg, bg='#0b0b0b', selectcolor='#0b0b0b', font=('Consolas', 11))
        rb_custom.grid(row=0, column=2, sticky='w', padx=12, pady=4)
        self.custom_format_entry = self._entry(box1, self.custom_format_var, 1, 0, colspan=3, width=60)

        # Audio options - using a container frame for side-by-side layout
        audio_playlist_row = tk.Frame(left, bg='#0b0b0b')
        audio_playlist_row.grid(row=6, column=0, columnspan=3, sticky='ew', pady=(6,3), padx=4)

        # Audio / Post-processing box (left side)
        box2 = tk.LabelFrame(audio_playlist_row, text="Audio / Post-processing", fg=self.highlight, bg='#0b0b0b',
                              font=('Consolas', 11, 'bold'), bd=2, relief='groove',
                              highlightbackground=self.highlight, highlightcolor=self.highlight)
        box2.pack(side='left', fill='both', expand=True, padx=(0,3))

        tk.Checkbutton(box2, text="Extract audio", variable=self.audio_extract_var, fg=self.fg, bg='#0b0b0b',
                      selectcolor='#0b0b0b', font=('Consolas', 9)).grid(row=0, column=0, sticky='w', padx=6, pady=4)

        self._label(box2, "Format:", 1, 0)
        tk.Radiobutton(box2, text='mp3', variable=self.audio_format_var, value='mp3', fg=self.fg, bg='#0b0b0b',
                      selectcolor='#0b0b0b', font=('Consolas', 11)).grid(row=1, column=1, sticky='w', padx=4, pady=4)
        tk.Radiobutton(box2, text='m4a', variable=self.audio_format_var, value='m4a', fg=self.fg, bg='#0b0b0b',
                      selectcolor='#0b0b0b', font=('Consolas', 11)).grid(row=1, column=2, sticky='w', padx=4, pady=4)
        tk.Radiobutton(box2, text='opus', variable=self.audio_format_var, value='opus', fg=self.fg, bg='#0b0b0b',
                      selectcolor='#0b0b0b', font=('Consolas', 11)).grid(row=1, column=3, sticky='w', padx=4, pady=4)
        tk.Radiobutton(box2, text='wav', variable=self.audio_format_var, value='wav', fg=self.fg, bg='#0b0b0b',
                      selectcolor='#0b0b0b', font=('Consolas', 11)).grid(row=1, column=4, sticky='w', padx=4, pady=4)

        self._label(box2, "Bitrate:", 2, 0)
        self._entry(box2, self.audio_bitrate_var, 2, 1, width=8)
        tk.Checkbutton(box2, text="Re-encode (ffmpeg)", variable=self.reencode_var, fg=self.fg, bg='#0b0b0b',
                      selectcolor='#0b0b0b', font=('Consolas', 9)).grid(row=3, column=0, sticky='w', padx=6, pady=4)

        # Playlist options box (right side)
        box2b = tk.LabelFrame(audio_playlist_row, text="Playlist", fg=self.highlight, bg='#0b0b0b',
                              font=('Consolas', 11, 'bold'), bd=2, relief='groove',
                              highlightbackground=self.highlight, highlightcolor=self.highlight)
        box2b.pack(side='left', fill='both', expand=True, padx=(3,0))

        self._label(box2b, "Playlist:", 0, 0)
        tk.Radiobutton(box2b, text='Off', variable=self.playlist_var, value='off', fg=self.fg, bg='#0b0b0b',
                      selectcolor='#0b0b0b', font=('Consolas', 11)).grid(row=0, column=1, sticky='w', padx=4, pady=4)
        tk.Radiobutton(box2b, text='On', variable=self.playlist_var, value='on', fg=self.fg, bg='#0b0b0b',
                      selectcolor='#0b0b0b', font=('Consolas', 11)).grid(row=0, column=2, sticky='w', padx=4, pady=4)

        self._label(box2b, "Download:", 1, 0)
        tk.Radiobutton(box2b, text='Recent', variable=self.playlist_items_var, value='recent', fg=self.fg, bg='#0b0b0b',
                      selectcolor='#0b0b0b', font=('Consolas', 11)).grid(row=1, column=1, sticky='w', padx=4, pady=4)
        tk.Radiobutton(box2b, text='All', variable=self.playlist_items_var, value='all', fg=self.fg, bg='#0b0b0b',
                      selectcolor='#0b0b0b', font=('Consolas', 11)).grid(row=1, column=2, sticky='w', padx=4, pady=4)

        self._label(box2b, "Range:", 2, 0)
        self._entry(box2b, self.playlist_range_start_var, 2, 1, width=6)
        self._label(box2b, "to", 2, 2)
        self._entry(box2b, self.playlist_range_end_var, 2, 3, width=6)

        self._label(box2b, "Episodes:", 3, 0)
        self._entry(box2b, self.playlist_episodes_var, 3, 1, width=20, colspan=3)

        # Subtitles / Metadata and Authentication - using a container frame for side-by-side layout
        subtitles_auth_row = tk.Frame(left, bg='#0b0b0b')
        subtitles_auth_row.grid(row=10, column=0, columnspan=3, sticky='ew', pady=(6,3), padx=4)

        # Configure column weights to match Audio/Playlist proportions (50/50)
        subtitles_auth_row.columnconfigure(0, weight=1)
        subtitles_auth_row.columnconfigure(1, weight=1)

        # Subtitles / Metadata box (left side)
        box3 = tk.LabelFrame(subtitles_auth_row, text="Subtitles & Metadata", fg=self.highlight, bg='#0b0b0b',
                              font=('Consolas', 11, 'bold'), bd=2, relief='groove',
                              highlightbackground=self.highlight, highlightcolor=self.highlight)
        box3.grid(row=0, column=0, sticky='nsew', padx=(0,3))

        tk.Checkbutton(box3, text="Download subtitles", variable=self.subtitles_var, fg=self.fg, bg='#0b0b0b',
                      selectcolor='#0b0b0b', font=('Consolas', 9)).grid(row=0, column=0, sticky='w', padx=6, pady=4)
        self._label(box3, "Lang:", 0, 1)
        self._entry(box3, self.subtitle_lang_var, 0, 2, width=8)
        tk.Checkbutton(box3, text="Embed thumbnail", variable=self.embed_thumbnail_var, fg=self.fg, bg='#0b0b0b',
                      selectcolor='#0b0b0b', font=('Consolas', 9)).grid(row=1, column=0, sticky='w', padx=6, pady=4)
        tk.Checkbutton(box3, text="Add metadata", variable=self.add_metadata_var, fg=self.fg, bg='#0b0b0b',
                      selectcolor='#0b0b0b', font=('Consolas', 9)).grid(row=1, column=1, sticky='w', padx=6, pady=4)

        # Authentication box (right side)
        box3b = tk.LabelFrame(subtitles_auth_row, text="Authentication", fg=self.highlight, bg='#0b0b0b',
                              font=('Consolas', 11, 'bold'), bd=2, relief='groove',
                              highlightbackground=self.highlight, highlightcolor=self.highlight)
        box3b.grid(row=0, column=1, sticky='nsew', padx=(3,0))

        self._label(box3b, "Username:", 0, 0)
        self._entry(box3b, self.username_var, 0, 1, width=20)
        self._label(box3b, "Password:", 1, 0)
        password_entry = self._entry(box3b, self.password_var, 1, 1, width=20)
        password_entry.configure(show='*')  # Hide password characters

        # Network / Behavior
        box4 = self._group(left, "Network / Behavior (optional)", 13)
        self._label(box4, "Rate limit (e.g. 500K):", 0, 0)
        self._entry(box4, self.rate_limit_var, 0, 1, width=12)
        self._label(box4, "Retries:", 1, 0)
        self._entry(box4, self.retries_var, 1, 1, width=8)
        self._label(box4, "Cookies file:", 2, 0)
        self._entry(box4, self.cookies_var, 2, 1, width=36)
        tk.Button(box4, text='BROWSE', command=self.browse_cookies, bg=self.button_bg, fg=self.fg,
                 width=10, font=('Consolas', 9)).grid(row=2, column=2, padx=6)
        self._label(box4, "Proxy:", 3, 0)
        self._entry(box4, self.proxy_var, 3, 1, width=36)

        # FFmpeg & Merge options
        box5 = self._group(left, "FFmpeg & Merging", 19)
        self._label(box5, "ffmpeg.exe path:", 0, 0)
        self._entry(box5, self.ffmpeg_path_var, 0, 1, width=36)
        tk.Button(box5, text='AUTO-DETECT', command=self.autodetect_ffmpeg, bg=self.button_bg, fg=self.fg,
                 width=12, font=('Consolas', 9)).grid(row=0, column=2, padx=6)
        tk.Button(box5, text='BROWSE', command=self.browse_ffmpeg, bg=self.button_bg, fg=self.fg,
                 width=10, font=('Consolas', 9)).grid(row=0, column=3, padx=6)

        tk.Radiobutton(box5, text='Use ffmpeg to merge', variable=self.merge_method_var, value='ffmpeg', fg=self.fg,
                      bg='#0b0b0b', selectcolor='#0b0b0b', font=('Consolas', 9)).grid(row=1, column=0, sticky='w', padx=6, pady=4)
        tk.Radiobutton(box5, text='Ask yt-dlp/native', variable=self.merge_method_var, value='native', fg=self.fg,
                      bg='#0b0b0b', selectcolor='#0b0b0b', font=('Consolas', 9)).grid(row=1, column=1, sticky='w', padx=6, pady=4)

        # Buttons: Download / Stop / Clear Log
        btn_frame = tk.Frame(left, bg='#0b0b0b')
        btn_frame.grid(row=22, column=0, columnspan=3, pady=(5,10))
        dl_btn = tk.Button(btn_frame, text='DOWNLOAD', command=self.start_download, bg=self.button_bg, fg=self.fg,
                          width=12, font=('Consolas', 9, 'bold'))
        dl_btn.grid(row=0, column=0, padx=6)
        stop_btn = tk.Button(btn_frame, text='STOP', command=self.stop_download, bg=self.button_bg, fg=self.fg,
                            width=8, font=('Consolas', 9, 'bold'))
        stop_btn.grid(row=0, column=1, padx=6)
        clear_btn = tk.Button(btn_frame, text='CLEAR LOG', command=self.clear_log, bg=self.button_bg, fg=self.fg,
                             width=10, font=('Consolas', 9, 'bold'))
        clear_btn.grid(row=0, column=2, padx=6)

        # Right column: Log console & command preview
        right = tk.Frame(self, bg='#0b0b0b')
        right.place(x=790, y=50, width=350, height=650)

        # Extra yt-dlp arguments
        extra_label = tk.Label(right, text='Extra yt-dlp arguments:', fg=self.fg, bg='#0b0b0b',
                              font=('Consolas', 10))
        extra_label.pack(anchor='nw', padx=6, pady=(6,2))
        extra_entry = tk.Entry(right, textvariable=self.extra_args_var, bg=self.input_bg, fg=self.fg,
                              insertbackground=self.fg, bd=0, font=('Consolas', 11))
        extra_entry.pack(fill='x', padx=6, pady=(0,6))

        # Command Preview
        preview_frame = tk.LabelFrame(right, text='COMMAND PREVIEW', fg=self.highlight, bg='#0b0b0b',
                                      font=('Consolas', 11, 'bold'), bd=2, relief='ridge',
                                      highlightbackground=self.highlight, highlightcolor=self.highlight)
        preview_frame.pack(fill='x', padx=6, pady=6)

        self.cmd_preview = tk.Text(preview_frame, height=8, bg='#060606', fg=self.highlight,
                                   bd=0, wrap='word', font=('Consolas', 9))
        self.cmd_preview.pack(fill='x', padx=6, pady=6)
        self.cmd_preview.configure(state='disabled')

        lbl_log = tk.Label(right, text='Log / Output', fg=self.fg, bg='#0b0b0b')
        lbl_log.pack(anchor='nw', padx=6, pady=(8,0))
        self.log_text = tk.Text(right, height=22, bg='#060606', fg=self.fg, bd=0)
        self.log_text.pack(fill='both', expand=True, padx=6, pady=(0,6))
        self.log_text.configure(state='disabled')

        # Initial update of preview
        self.update_command_preview()

        # Bind changes to update preview
        for var in [self.url_var, self.batch_file_var, self.output_template_var, self.dest_folder_var, self.format_choice,
                    self.custom_format_var, self.audio_extract_var, self.audio_format_var, self.audio_bitrate_var,
                    self.playlist_var, self.playlist_items_var, self.playlist_range_start_var, self.playlist_range_end_var,
                    self.playlist_episodes_var,
                    self.subtitles_var, self.subtitle_lang_var, self.embed_thumbnail_var, self.add_metadata_var,
                    self.username_var, self.password_var,
                    self.rate_limit_var, self.retries_var, self.cookies_var, self.proxy_var, self.ffmpeg_path_var,
                    self.merge_method_var, self.reencode_var, self.extra_args_var]:
            try:
                var.trace_add('write', lambda *a: self.update_command_preview())
            except Exception:
                pass

    # --- UI helpers
    def _label(self, parent, text, row, col):
        lbl = tk.Label(parent, text=text, fg=self.fg, bg='#0b0b0b', anchor='w', font=('Consolas', 11))
        lbl.grid(row=row, column=col, sticky='w', padx=4, pady=4)
        return lbl

    def _entry(self, parent, var, row, col, width=40, colspan=1):
        ent = tk.Entry(parent, textvariable=var, bg=self.input_bg, fg=self.fg, insertbackground=self.fg,
                      bd=0, width=width, font=('Consolas', 12))
        ent.grid(row=row, column=col, columnspan=colspan, sticky='w', padx=6, pady=4)
        return ent

    def _group(self, parent, title, grid_row):
        frame = tk.LabelFrame(parent, text=title, fg=self.highlight, bg='#0b0b0b',
                              font=('Consolas', 11, 'bold'), bd=2, relief='groove',
                              highlightbackground=self.highlight, highlightcolor=self.highlight)
        frame.grid(row=grid_row, column=0, columnspan=3, sticky='ew', pady=(6,3), padx=4)
        return frame


    # --- callbacks
    def choose_dest(self):
        initial = self.dest_folder_var.get()
        if not initial:
            initial = os.path.expanduser('~')
        folder = filedialog.askdirectory(initialdir=initial)
        if folder:
            self.dest_folder_var.set(folder)

    def choose_batch_file(self):
        path = filedialog.askopenfilename(title='Select batch file (URLs list)',
                                         filetypes=[('Text files', '*.txt'), ('All files', '*.*')])
        if path:
            self.batch_file_var.set(path)

    def browse_ffmpeg(self):
        path = filedialog.askopenfilename(title='Select ffmpeg.exe', filetypes=[('Executables','*.exe')])
        if path:
            self.ffmpeg_path_var.set(path)

    def autodetect_ffmpeg(self):
        p = detect_ffmpeg()
        if p:
            self.ffmpeg_path_var.set(p)
            messagebox.showinfo('FFmpeg', f'Auto-detected: {p}')
        else:
            messagebox.showwarning('FFmpeg', 'ffmpeg not found in PATH or common locations.')

    def browse_cookies(self):
        path = filedialog.askopenfilename(title='Select cookies.txt', filetypes=[('Cookies','*.*')])
        if path:
            self.cookies_var.set(path)

    def clear_log(self):
        self.log_text.configure(state='normal')
        self.log_text.delete('1.0', tk.END)
        self.log_text.configure(state='disabled')

    def _poll_log_queue(self):
        try:
            while True:
                line = log_q.get_nowait()
                self._append_log(line)
        except queue.Empty:
            pass
        self.after(100, self._poll_log_queue)

    def _append_log(self, text):
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, text)
        self.log_text.see(tk.END)
        self.log_text.configure(state='disabled')

    def update_command_preview(self):
        cmd = self.build_command(dry_run=True)
        self.cmd_preview.configure(state='normal')
        self.cmd_preview.delete('1.0', tk.END)
        self.cmd_preview.insert(tk.END, ' '.join(cmd))
        self.cmd_preview.configure(state='disabled')

    def build_command(self, dry_run=False):
        url = self.url_var.get().strip()
        batch_file = self.batch_file_var.get().strip()

        if not url and not batch_file and not dry_run:
            messagebox.showwarning('No URL or Batch File', 'Please enter a URL or select a batch file.')
            return []

        cmd = [sys.executable, '-m', 'yt_dlp']

        # output template and folder
        dest = self.dest_folder_var.get()
        if not dest:
            dest = os.path.expanduser('~')
        out = os.path.join(dest, self.output_template_var.get())
        cmd += ['-o', out]

        # format handling
        fmt_choice = self.format_choice.get()
        if fmt_choice == 'best':
            cmd += ['-f', 'bestvideo+bestaudio/best']
        elif fmt_choice == 'audio':
            cmd += ['-f', 'bestaudio']
        elif fmt_choice == 'custom':
            custom_fmt = self.custom_format_var.get().strip()
            if custom_fmt:
                cmd += ['-f', custom_fmt]

        # audio extraction
        if self.audio_extract_var.get():
            cmd += ['-x', '--audio-format', self.audio_format_var.get()]
            if self.audio_bitrate_var.get():
                cmd += ['--audio-quality', self.audio_bitrate_var.get()]

        # playlist options
        if self.playlist_var.get() == 'off':
            cmd += ['--no-playlist']
        else:
            # playlist is on
            episodes = self.playlist_episodes_var.get().strip()
            range_start = self.playlist_range_start_var.get().strip()
            range_end = self.playlist_range_end_var.get().strip()

            if episodes:
                # Specific episodes specified (e.g., "1,3,5" or "1,3-5,7")
                cmd += ['--playlist-items', episodes]
            elif range_start and range_end:
                # Range specified - use range values
                cmd += ['--playlist-items', f'{range_start}-{range_end}']
            elif range_start:
                # Only start specified - from start to end of playlist
                cmd += ['--playlist-items', f'{range_start}-']
            elif self.playlist_items_var.get() == 'recent':
                # Recent option selected
                cmd += ['--playlist-items', '1']
            # if 'all' and no range, no additional flag needed (default behavior)

        # subtitles
        if self.subtitles_var.get():
            cmd += ['--write-sub', '--sub-lang', self.subtitle_lang_var.get()]

        # embedding and metadata
        if self.embed_thumbnail_var.get():
            cmd += ['--embed-thumbnail']
        if self.add_metadata_var.get():
            cmd += ['--add-metadata']

        # authentication
        if self.username_var.get().strip():
            cmd += ['--username', self.username_var.get().strip()]
        if self.password_var.get().strip():
            cmd += ['--password', self.password_var.get().strip()]

        # network
        if self.rate_limit_var.get().strip():
            cmd += ['--limit-rate', self.rate_limit_var.get().strip()]
        if self.retries_var.get().strip():
            cmd += ['--retries', self.retries_var.get().strip()]
        if self.cookies_var.get().strip():
            cmd += ['--cookies', self.cookies_var.get().strip()]
        if self.proxy_var.get().strip():
            cmd += ['--proxy', self.proxy_var.get().strip()]

        # merging preferences
        if self.merge_method_var.get() == 'ffmpeg':
            # prefer ffmpeg merging
            # if user wants reencode, set args accordingly (handled by ffmpeg during postprocessing)
            cmd += ['--merge-output-format', 'mp4']

        # extra args (free text)
        extra = self.extra_args_var.get().strip()
        if extra:
            cmd += extra.split()

        # batch file or URL
        if batch_file:
            cmd += ['-a', batch_file]
        elif url:
            cmd += [url]

        return cmd

    def start_download(self):
        if self.process and self.process.poll() is None:
            messagebox.showinfo('Download running', 'A download is already running.')
            return
        cmd = self.build_command()
        if not cmd:
            return
        # Launch in background thread
        t = threading.Thread(target=self._run_process, args=(cmd,), daemon=True)
        t.start()

    def stop_download(self):
        self.stop_requested = True
        if self.process and self.process.poll() is None:
            try:
                self.process.terminate()
                log_q.put('\n[USER] Terminate requested.\n')
            except Exception as e:
                log_q.put(f'Failed to terminate process: {e}\n')

    def _run_process(self, cmd):
        # Build environment: ensure ffmpeg is in PATH if provided
        env = os.environ.copy()
        ffmpeg_path = self.ffmpeg_path_var.get().strip()
        if ffmpeg_path and os.path.isfile(ffmpeg_path):
            ff_dir = os.path.dirname(ffmpeg_path)
            env['PATH'] = ff_dir + os.pathsep + env.get('PATH', '')
            log_q.put(f'[INFO] Using ffmpeg at: {ffmpeg_path}\n')
        else:
            log_q.put('[WARN] ffmpeg not found or not set; yt-dlp may use internal merging if available.\n')

        log_q.put('[CMD] ' + ' '.join(cmd) + '\n')

        try:
            # Use universal_newlines/text mode for easier reading
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env, bufsize=1, text=True)

            for line in self.process.stdout:
                if self.stop_requested:
                    break
                log_q.put(line)

            self.process.wait()
            code = self.process.returncode
            if code == 0 and not self.stop_requested:
                log_q.put('\n[INFO] yt-dlp finished successfully.\n')
            elif self.stop_requested:
                log_q.put('\n[INFO] Process stopped by user.\n')
            else:
                log_q.put(f'\n[ERROR] yt-dlp exited with code {code}.\n')

        except FileNotFoundError as e:
            log_q.put(f'[ERROR] yt-dlp executable not found: {e}\n')
        except Exception as e:
            log_q.put(f'[ERROR] Exception while running yt-dlp: {e}\n')
        finally:
            self.stop_requested = False
            self.process = None


if __name__ == '__main__':
    app = TrainerUI()
    app.mainloop()
