# 🎵 Music Player Application

A feature-rich desktop music player built with **Python**, **PyQt5**, and **VLC**, backed by a **MySQL** database for persistent playlist and song management.

---

## 1. 📖 Introduction

The **Music Player Application** is a fully-featured desktop media player developed in Python using the PyQt5 GUI framework. It provides users with an intuitive interface to manage and play their local music library. The application supports playlist creation, song liking, play history tracking, real-time audio visualization, and a switchable dark/light theme — all powered by a MySQL relational database for persistent data storage.

Whether you want to add individual tracks, import entire folders, or organize your music into custom playlists, this app delivers a clean, modern experience similar to popular music streaming clients — but entirely offline and locally hosted.

---

## 2. 🏗️ Architecture

The project follows a **modular MVC-inspired architecture**, separating UI, data, and utility concerns into distinct files:

```
Music Player/
│
├── main.py                     # Entry point — launches the PyQt5 app
├── music_player.py             # Core UI class (MusicPlayerUI) — all logic & layout
├── database.py                 # MySQL connection handler
├── dialogs.py                  # Popup dialog windows (Playlists, History)
├── visualizer.py               # Animated wave visualizer widget
├── Musicdb.sql                 # Database schema (DDL)
└── .vscode/
    └── c_cpp_properties.json   # VSCode config (not used at runtime)
```

### Component Overview

| Module | Responsibility |
|---|---|
| `main.py` | Initializes `QApplication` and launches `MusicPlayerUI` |
| `music_player.py` | Main window — sidebar, song list, controls, playback logic |
| `database.py` | `connect_db()` — returns a MySQL connection object |
| `dialogs.py` | `PlaylistDialog` and `HistoryDialog` popup windows |
| `visualizer.py` | `WaveVisualizer` — animated real-time audio bar widget |
| `Musicdb.sql` | Creates `Music_playerDB` with 4 normalized tables |

### Database Schema

```
Music_playerDB
├── songs           (song_id, title, file_path)
├── playlists       (playlist_id, name)
├── playlist_songs  (id, playlist_id → playlists, song_id → songs)
└── liked_songs     (id, song_id → songs, liked_at)
```

---

## 3. 🏷️ Tech Tags

| Category | Technology |
|---|---|
| **Language** | Python 3.13 |
| **GUI Framework** | PyQt5 |
| **Audio Engine** | python-vlc (libVLC) |
| **Database** | MySQL via `mysql-connector-python` |
| **Visualization** | QPainter (custom wave widget) |
| **IDE Support** | VSCode |
| **Platform** | Windows / Linux / macOS |

---

## 4. 🚀 Steps to Run

### Prerequisites

Make sure the following are installed on your system:

- Python 3.10+
- MySQL Server (running locally)
- VLC Media Player (required by `python-vlc`)

### Step 1 — Clone / Extract the Project

```bash
unzip Music_player.zip
cd "Music player"
```

### Step 2 — Install Python Dependencies

```bash
pip install PyQt5 python-vlc mysql-connector-python
```

### Step 3 — Set Up the Database

Open MySQL and run the schema file:

```bash
mysql -u root -p < Musicdb.sql
```

Or manually paste the contents of `Musicdb.sql` into your MySQL client. This creates the `Music_playerDB` database and all required tables.

### Step 4 — Configure Database Credentials

Open `database.py` and update the credentials to match your MySQL setup:

```python
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",   # ← update this
    database="Music_playerDB"
)
```

> ⚠️ **Security Note:** It is strongly recommended to use environment variables instead of hardcoding credentials. Example:
> ```python
> import os
> password=os.environ.get("DB_PASSWORD")
> ```

### Step 5 — Run the Application

```bash
python main.py
```

The music player window will open. Use the sidebar to add songs, create playlists, and start playing your music.

---

## 5. 📝 Summary

### Key Features

- **Add Music** — Import individual `.mp3`/`.wav` files via file dialog
- **Add Folder** — Bulk-import all audio files from a selected directory
- **Playlists** — Create named playlists and assign songs to them; view all in a popup
- **Liked Songs** — Like/unlike any song; liked songs are persisted in the database
- **Play History** — Automatically tracks all played songs; viewable via popup dialog
- **Wave Visualizer** — Animated real-time vertical bar visualizer rendered with QPainter
- **Keyboard Shortcuts** — `Space` (play/pause), `→` (next), `←` (previous)
- **Dark / Light Theme** — One-click toggle between dark (`#121212`) and light (`#FFFFFF`) themes
- **Progress Slider** — Seek through a song by dragging the progress bar
- **Now Playing Label** — Displays the current song name at the top of the player

### Limitations / Known Issues

- Database credentials are currently hardcoded in `database.py` — use environment variables in production
- The wave visualizer uses random amplitudes (not actual audio FFT data)
- No support for streaming or online music sources
- Tested on Windows; cross-platform behavior may vary with VLC paths

---

# Music Player Application

## Screenshots

![Home Screen](Screenshort/Screenshot%202025-03-31%20185102.png)


![Music Library](Screenshort/Screenshot%202025-04-01%20131919.png)


![Player Interface](Screenshort/Screenshot%202025-04-01%20131940.png)

![Visualizer](Screenshort/Screenshot%202025-04-01%20131955.png)


![Database Management](Screenshort/Screenshot%202025-04-01%20132046.png)

---

