from multiprocessing import connection
import os
from sqlite3 import Cursor
import sys
import vlc
import random
import mysql.connector 

from pathlib import Path
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl,Qt 
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,QShortcut,QListWidget,QListWidgetItem,
    QFileDialog, QSlider, QMenuBar, QAction, QMessageBox, QInputDialog, QDialog, QFrame,QSizePolicy
)
from PyQt5.QtGui import QFont,QKeySequence,QPainter,QColor,QPen,QPixmap
from PyQt5.QtCore import QTimer

def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sushant@458",  # Consider using environment variables for security
            database="Music_playerDB"
        )
        if conn.is_connected():
            print("Connection is successfully")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    
class WaveVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.amplitude = [random.randint(30, 80) for _ in range(100)]  # Initial wave heights
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_wave)
        self.timer.start(100)  # Update every 100ms

    def update_wave(self):
        """Randomly change wave heights for animation effect"""
        self.amplitude = [random.randint(30, 80) for _ in range(100)]
        self.update()  # Redraw the widget

    def paintEvent(self, event):
        """Draw the animated sound waves"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()
        num_lines = len(self.amplitude)
        spacing = width // (num_lines + 1)

        # Draw wave bars
        for i in range(num_lines):
            x = (i + 1) * spacing
            y = height // 2
            bar_height = self.amplitude[i]

            pen = QPen(QColor(0, 255, 0))  # Green color for waves
            pen.setWidth(6)  # Thickness of wave lines
            painter.setPen(pen)
            painter.drawLine(x, y - bar_height, x, y + bar_height)

class PlaylistDialog(QDialog):
    """Popup to display all playlists and songs."""
    def __init__(self, playlists, play_song_callback):
        super().__init__()
        self.setWindowTitle("All Playlists and Songs")
        self.setGeometry(150, 150, 600, 400)
        self.play_song_callback = play_song_callback

        layout = QVBoxLayout()
        self.song_list_widget = QListWidget()

        for playlist, songs in playlists.items():
            self.song_list_widget.addItem(f"--- {playlist} ---")
            for song in songs:
                self.song_list_widget.addItem(song.split("/")[-1])

        self.song_list_widget.itemDoubleClicked.connect(self.song_selected)
        layout.addWidget(self.song_list_widget)
        self.setLayout(layout)
       

        self.setLayout(layout)
        self.play_history = []

    def song_selected(self, item):
        song_name = item.text()
        self.play_song_callback(song_name)
        self.close()

class HistoryDialog(QDialog):
    """Popup to show play history and allow replaying songs."""
    def __init__(self, history, play_song_callback):
        super().__init__()
        self.setWindowTitle("Play History")
        self.setGeometry(200, 200, 500, 400)
        self.play_song_callback = play_song_callback

        layout = QVBoxLayout()
        self.history_list_widget = QListWidget()

        for song in reversed(history):  # Show latest songs first
            self.history_list_widget.addItem(song.split("/")[-1])

        self.history_list_widget.itemDoubleClicked.connect(self.song_selected)
        layout.addWidget(self.history_list_widget)
        self.setLayout(layout)

    def song_selected(self, item):
        song_name = item.text()
        self.play_song_callback(song_name)
        self.close()

class MusicPlayerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Player")
        self.setGeometry(150, 130, 1000, 900)
        self.dark_mode = True
        self.set_dark_theme()

        self.vlc_instance = vlc.Instance()
        self.player = self.vlc_instance.media_player_new()
        self.is_playing = False
        self.current_song = None
        self.playlists = {"Liked Songs": []}
        self.current_playlist = []
        self.current_index = -1
        self.play_history = []  # ✅ Initialize play history list

        self.init_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)

    def set_dark_theme(self):
        self.setStyleSheet("background-color: #121212; color: white;")

    def set_light_theme(self):
        self.setStyleSheet("background-color: #FFFFFF; color: black;")

    def toggle_theme(self):
        if self.dark_mode:
            self.set_light_theme()
        else:
            self.set_dark_theme()
        self.dark_mode = not self.dark_mode

    def show_play_history(self):
        self.play_history = []  # Stores played song paths

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(50)
    
    # Create a horizontal layout to contain sidebar and content
        content_layout = QHBoxLayout()
    
    # Create the sidebar
        sidebar_frame = QFrame()
        sidebar_frame.setStyleSheet(
            "background-color: #1e1e1e; border-radius: 10px; margin: 5px;"
        )
        sidebar_frame.setFixedWidth(300)  # Width of sidebar
    
        sidebar_layout = QVBoxLayout(sidebar_frame)
        sidebar_layout.setSpacing(40)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
    
    # Define sidebar button style
        sidebar_btn_style = (
            "QPushButton { background-color: #2e2e2e; border-radius: 5px; "
            "color: white; font-size: 25px; padding: 10px; text-align: left; }"
            "QPushButton:hover { background-color: #3e3e3e; }"
        )
    
    # Create sidebar buttons
    
        add_music_btn = QPushButton("➕ Add Music")
        add_music_btn.setStyleSheet(sidebar_btn_style)
        add_music_btn.clicked.connect(self.add_song)
    
        add_folder_btn = QPushButton("📁 Add Folder")
        add_folder_btn.setStyleSheet(sidebar_btn_style)
        add_folder_btn.clicked.connect(self.add_folder)
    
        add_show_btn = QPushButton("📋 Show Songs")
        add_show_btn.setStyleSheet(sidebar_btn_style)
        add_show_btn.clicked.connect(self.show_all_songs)

        playlists_btn = QPushButton("📀 Playlists")
        playlists_btn.setStyleSheet(sidebar_btn_style)
        playlists_btn.clicked.connect(self.show_playlists_popup)
    
        create_playlist_btn = QPushButton("✏️ Create Playlist")
        create_playlist_btn.setStyleSheet(sidebar_btn_style)
        create_playlist_btn.clicked.connect(self.create_playlist)

        history_btn = QPushButton("⏱️ History")
        history_btn.setStyleSheet(sidebar_btn_style)
        history_btn.clicked.connect(self.show_play_history)

        theme_btn = QPushButton("🎨 Toggle Theme")
        theme_btn.setStyleSheet(sidebar_btn_style)
        theme_btn.clicked.connect(self.toggle_theme)

        # Add buttons to sidebar
        sidebar_layout.addWidget(add_music_btn)
        sidebar_layout.addWidget(add_folder_btn)
        sidebar_layout.addWidget(add_show_btn)
        sidebar_layout.addWidget(playlists_btn)
        sidebar_layout.addWidget(create_playlist_btn)
        sidebar_layout.addWidget(history_btn)
        sidebar_layout.addWidget(theme_btn)
        sidebar_layout.addStretch()

        # Create right content area
        content_frame = QFrame()
        content_layout_inner = QVBoxLayout(content_frame)

        # Add keyboard shortcuts
        self.play_shortcut = QShortcut(QKeySequence("Space"), self)
        self.play_shortcut.activated.connect(self.toggle_play_pause)
    
        self.next_shortcut = QShortcut(QKeySequence("Right"), self)
        self.next_shortcut.activated.connect(self.next_song)
    
        self.prev_shortcut = QShortcut(QKeySequence("Left"), self)
        self.prev_shortcut.activated.connect(self.previous_song)
    
    # Add center layout content to content area
        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)
    
        self.song_title_label = QLabel("Now Playing: ")
        self.song_title_label.setFont(QFont(self.font().family(), 18))
        self.song_title_label.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(self.song_title_label)
    
        self.songs = {}
        self.song_list = QListWidget()
        self.song_list.setFixedHeight(800)
        self.song_list.itemDoubleClicked.connect(self.play_selected_song)
        center_layout.addWidget(self.song_list)
    
        content_layout_inner.addLayout(center_layout)
        content_layout_inner.addStretch(1)
    
        # Bottom layout (wave visualizer, slider, and controls)
        bottom_layout = QVBoxLayout()
        bottom_layout.setSpacing(10)
    
        self.wave_visualizer = WaveVisualizer(self)
        self.wave_visualizer.setFixedHeight(500)
        bottom_layout.addWidget(self.wave_visualizer)
    
        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setFixedHeight(10)
        self.progress_slider.sliderMoved.connect(self.seek_position)
        bottom_layout.addWidget(self.progress_slider)
    
        self.duration_label = QLabel("00:00 / 00:00")
        self.duration_label.setFont(QFont(self.font().family(), 14))
        self.duration_label.setAlignment(Qt.AlignCenter)
        bottom_layout.addWidget(self.duration_label)
    
    # Playback controls
        playback_controls = QHBoxLayout()
        playback_controls.setSpacing(40)
        playback_controls.setAlignment(Qt.AlignCenter)
    
        button_style = (
            "QPushButton { background-color: #1e1e1e; border-radius: 10px; "
            "color: white; font-size: 36px; width: 70px; height: 70px; }"
            "QPushButton:hover { background-color: #333333; }"
            )
    
        self.like_song_btn = QPushButton("♡")
        self.like_song_btn.setStyleSheet(button_style)
        self.like_song_btn.clicked.connect(self.toggle_like_current_song)
    
        self.prev_btn = QPushButton("⏮")
        self.prev_btn.setStyleSheet(button_style)
        self.prev_btn.clicked.connect(self.previous_song)
    
        self.play_pause_btn = QPushButton("▶️")
        self.play_pause_btn.setStyleSheet(button_style)
        self.play_pause_btn.clicked.connect(self.toggle_play_pause)
    
        self.next_btn = QPushButton("⏭")
        self.next_btn.setStyleSheet(button_style)
        self.next_btn.clicked.connect(self.next_song)
    
        self.shuffle_btn = QPushButton("🔀")
        self.shuffle_btn.setStyleSheet(button_style)
    
        self.add_playlist_btn = QPushButton("➕")
        self.add_playlist_btn.setStyleSheet(button_style)
        self.add_playlist_btn.clicked.connect(self.add_to_playlist)
    
        playback_controls.addWidget(self.like_song_btn)
        playback_controls.addWidget(self.prev_btn)
        playback_controls.addWidget(self.play_pause_btn)
        playback_controls.addWidget(self.next_btn)
        playback_controls.addWidget(self.add_playlist_btn)
    
        bottom_layout.addLayout(playback_controls)
        content_layout_inner.addLayout(bottom_layout)
    
    # Add sidebar and content to horizontal layout
        content_layout.addWidget(sidebar_frame)
        content_layout.addWidget(content_frame, 1)  # Content takes remaining space
    
    # Add menu bar and content layout to main layout
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def add_folder(self):
        """Opens a folder selection dialog, loads music files, and adds them to the database."""
        folder_path = QFileDialog.getExistingDirectory(self, "Select Music Folder")
        
        if not folder_path:
            return  # No folder selected
        
        if not hasattr(self, 'songs'):
            self.songs = {}
        
        if not hasattr(self, 'song_list'):
            self.song_list = QListWidget()
            center_layout = self.layout().itemAt(1).layout()
            center_layout.addWidget(self.song_list)
            self.song_list.itemDoubleClicked.connect(self.play_selected_song)
        else:
            self.song_list.clear()  # Clear previous entries
        
        folder = Path(folder_path)
        music_files = list(folder.glob("*.mp3")) + list(folder.glob("*.wav")) + list(folder.glob("*.ogg"))
        
        if not music_files:
            QMessageBox.warning(self, "No Songs Found", "No audio files found in the selected folder.")
            return
        
        # Establish database connection
        connection = connect_db()
        if not connection:
            QMessageBox.critical(self, "Database Error", "Failed to connect to the database.")
            return
        
        try:
            cursor = connection.cursor()
            
            # Fetch existing songs from the database
            cursor.execute("SELECT file_path FROM songs")
            existing_songs = {row[0] for row in cursor.fetchall()}  # Store existing file paths
            
            query = "INSERT INTO songs (title, file_path) VALUES (%s, %s) ON DUPLICATE KEY UPDATE file_path = VALUES(file_path)"
            
            new_songs = 0
            for file in music_files:
                file_name = file.stem  # Extract only the song name
                file_path = str(file)  # Store the full file path
                
                if file_path in existing_songs:
                    print(f"Skipping (Already in DB): {file_name}")
                    continue  # Skip if the song already exists
                
                self.songs[file_name] = file_path  # Store path internally
                self.song_list.addItem(file_name)  # Display only the song name in UI
                
                # Insert into database
                cursor.execute(query, (file_name, file_path))
                print(f"Inserted: {file_name} - {file_path}")
                new_songs += 1
            
            connection.commit()  # Commit all inserts at once
            print(f"{new_songs} new songs added to the database.")
        
        except mysql.connector.Error as e:
            print(f"Database insertion error: {e.errno}, {e.msg}")
        
        finally:
            cursor.close()
            connection.close()
        
        self.current_playlist = [str(file) for file in music_files]
        self.current_index = -1  # Reset current index
        
        QMessageBox.information(self, "Songs Added", f"{new_songs} new songs added successfully!")

    def show_all_songs(self):
        connection = connect_db()
        if not connection:
            QMessageBox.critical(None, "Database Error", "Failed to connect to the database.")
            return

        try:
            cursor = connection.cursor()
            cursor.execute("SELECT title, file_path FROM songs")  # Get song title and path
            songs = cursor.fetchall()

            if not songs:
                QMessageBox.information(None, "No Songs", "No songs found in the database.")
                return

        # Clear the current song list
            self.song_list.clear()
            self.current_playlist = []  # Reset playlist

            font = QFont()
            font.setPointSize(14)  # You can adjust this value as needed
            self.song_list.setFont(font)

            for title, path in songs:
                item = QListWidgetItem(title)  # Show only title
                item.setData(Qt.UserRole, path)  # Store file path
                self.song_list.addItem(item)
                self.current_playlist.append(path)

            self.song_title_label.setText("All Songs")  # Update the title label

        except mysql.connector.Error as e:
            print(f"Database Fetch Error: {e}")
            QMessageBox.warning(self, "Error", f"Database error: {str(e)}")

        finally:
            cursor.close()
            connection.close()

    def play_selected_song(self, item=None):
        """Plays the selected song from either the main list or the popup list."""
        selected_item = item if item else self.song_list_popup.currentItem() or self.song_list.currentItem()
    
        if selected_item:
            song_path = selected_item.data(Qt.UserRole) if selected_item.data(Qt.UserRole) else self.songs.get(selected_item.text())

        if song_path:
            self.play_song(song_path)
   
    def create_playlist(self):
        playlist_name, ok = QInputDialog.getText(self, "Create Playlist", "Enter playlist name:")
    
        if ok and playlist_name:
            # Establish database connection
            connection = connect_db()
        
            try:
                cursor = connection.cursor()
                query = "INSERT INTO playlists (name) VALUES (%s)"
                cursor.execute(query, (playlist_name,))
                connection.commit()  # Commit the transaction
            
                # Store locally in the app
                if not hasattr(self, 'playlists'):
                    self.playlists = {}
            
                self.playlists[playlist_name] = []
                QMessageBox.information(self, "Playlist Created", f"Playlist '{playlist_name}' created successfully.")

            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to create playlist: {str(e)}")

            finally:
                cursor.close()
                connection.close()

    def add_to_playlist(self): 
        """Add the currently playing song to a selected playlist."""
        if not self.current_song:
            QMessageBox.warning(self, "No Song Playing", "No song is currently playing.")
            return

    # Select a playlist
        playlist_name, ok = QInputDialog.getItem(
            self, "Add to Playlist", "Select a playlist:", list(self.playlists.keys()), 0, False
    )

        if not ok or not playlist_name:
            return  # User canceled

    # Connect to database
        connection = connect_db()
        if not connection:
            QMessageBox.critical(self, "Database Error", "Failed to connect to the database.")
            return

        try:
            cursor = connection.cursor()

            # Get playlist_id
            cursor.execute("SELECT playlist_id FROM playlists WHERE name = %s", (playlist_name,))
            playlist_id = cursor.fetchone()
    
            if not playlist_id:
                print("Playlist not found:", playlist_name)  # Debugging
                QMessageBox.warning(self, "Error", "Playlist not found in database.")
                return
    
            playlist_id = playlist_id[0]  # Extract ID

        # Get song_id
            cursor.execute("SELECT song_id FROM songs WHERE file_path = %s", (self.current_song,))
            song_id = cursor.fetchone()

            if not song_id:
                print("Song not found:", self.current_song)  # Debugging
                QMessageBox.warning(self, "Error", "Song not found in database.")
                return
    
            song_id = song_id[0]  # Extract ID

            # Check if song is already in the playlist
            cursor.execute("SELECT * FROM playlist_songs WHERE playlist_id = %s AND song_id = %s", 
                        (playlist_id, song_id))
            exists = cursor.fetchone()

            if exists:
                QMessageBox.information(self, "Info", "Song already exists in this playlist.")
                return
    
        # Insert song into the playlist
            query = "INSERT INTO playlist_songs (playlist_id, song_id) VALUES (%s, %s)"
            cursor.execute(query, (playlist_id, song_id))
        
            connection.commit()  # Ensure commit happens even if an error occurs

        # Update local playlist storage
            if playlist_name in self.playlists:
                self.playlists[playlist_name].append(self.current_song)

            QMessageBox.information(self, "Song Added", f"Song added to '{playlist_name}' playlist.")

        except mysql.connector.Error as e:
            QMessageBox.warning(self, "Error", f"Database error: {str(e)}")

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.commit()  # Ensures changes are saved
                connection.close()

    def show_playlists_popup(self):
        """Fetch playlists and liked songs from the database and show the playlist popup."""
    # Connect to database
        connection = connect_db()
        if not connection:
            QMessageBox.critical(self, "Database Error", "Failed to connect to the database.")
            return

        try:
            cursor = connection.cursor()

        # Fetch playlist names from the database
            cursor.execute("SELECT playlist_id, name FROM playlists")
            playlists_data = cursor.fetchall()

        # Reset local playlists storage
            self.playlists = {}

            for playlist_id, playlist_name in playlists_data:
            # Fetch songs for each playlist
                cursor.execute("""
                    SELECT s.file_path FROM songs s
                    JOIN playlist_songs ps ON s.song_id = ps.song_id
                    WHERE ps.playlist_id = %s
                """, (playlist_id,))
            
                song_paths = [row[0] for row in cursor.fetchall()]
                self.playlists[playlist_name] = song_paths

        # Fetch liked songs from the database
            cursor.execute("""
                SELECT s.file_path FROM songs s
                JOIN liked_songs ls ON s.song_id = ls.song_id
            """)
            liked_songs = [row[0] for row in cursor.fetchall()]

        # Add liked songs to the playlists dictionary
            if liked_songs:
                self.playlists["Liked Songs"] = liked_songs

            cursor.close()
            connection.close()

        # Show the updated playlist dialog
            dialog = PlaylistDialog(self.playlists, self.play_song_by_name)
            dialog.exec_()

        except mysql.connector.Error as e:
            QMessageBox.warning(self, "Error", f"Database error: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def play_song_by_name(self, song_name):
        """Plays a song by searching in playlists, liked songs, or history."""
    
    # Search in playlists
        for playlist, songs in self.playlists.items():
            for index, song_path in enumerate(songs):
                if song_path.split("/")[-1] == song_name:
                    self.current_playlist = songs
                    self.current_index = index
                    self.play_song(song_path)
                    return

    # Search in liked songs
        if "Liked Songs" in self.playlists:
            for index, song_path in enumerate(self.playlists["Liked Songs"]):
                if song_path.split("/")[-1] == song_name:
                    self.current_playlist = self.playlists["Liked Songs"]
                    self.current_index = index
                    self.play_song(song_path)
                return

    # Search in history if not found in playlists or liked songs
        for song_path in self.play_history:
            if song_path.split("/")[-1] == song_name:
                self.play_song(song_path)
                return

        QMessageBox.warning(self, "Not Found", f"'{song_name}' not found in playlists, liked songs, or history.")

    def play_song(self, song_path):
        self.current_song = song_path
        self.song_title_label.setText(f"Now Playing: {Path(song_path).name}")
        media = self.vlc_instance.media_new(song_path)
        self.player.set_media(media)
        self.player.play()
        self.timer.start(1000)
        self.play_pause_btn.setText("⏸")
        self.is_playing = True

    #  Ensure play_history is updated correctly
        if song_path not in self.play_history:
            self.play_history.append(song_path)

    # Ensure play_history is a list before appending
        if isinstance(self.show_play_history, list):
            if not self.play_history or self.play_history[-1] != song_path:
                self.play_history.append(song_path)

    def show_play_history(self):
        if not self.play_history:
            QMessageBox.information(self, "No History", "No songs have been played yet.")
            return

        dialog = HistoryDialog(self.play_history, self.play_song_by_name)
        dialog.exec_()

    def toggle_like_current_song(self):
        if self.current_song:
            connection = connect_db()
        
        try:
            cursor = connection.cursor()

            # Get song_id from the database
            cursor.execute("SELECT song_id FROM songs WHERE file_path = %s", (self.current_song,))
            song_id = cursor.fetchone()

            if song_id:
                song_id = song_id[0]  # Extract song ID

                # Check if the song is already liked
                cursor.execute("SELECT * FROM liked_songs WHERE song_id = %s", (song_id,))
                liked = cursor.fetchone()

                if liked:
                    # Unlike the song (Remove from liked_songs table)
                    cursor.execute("DELETE FROM liked_songs WHERE song_id = %s", (song_id,))
                    connection.commit()

                    self.playlists["Liked Songs"].remove(self.current_song)  # Update local storage
                    self.like_song_btn.setText("♡")  # Unlike state
                    QMessageBox.information(self, "Unliked", "Song removed from Liked Songs playlist.")
                else:
                    # Like the song (Insert into liked_songs table)
                    cursor.execute("INSERT INTO liked_songs (song_id) VALUES (%s)", (song_id,))
                    connection.commit()

                    self.playlists["Liked Songs"].append(self.current_song)  # Update local storage
                    self.like_song_btn.setText("❤️")  # Liked state
                    QMessageBox.information(self, "Liked", "Song added to Liked Songs playlist.")
            else:
                QMessageBox.warning(self, "Error", "Song not found in database.")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to update liked songs: {str(e)}")

        finally:
            cursor.close()
            connection.close()

    def toggle_play_pause(self):
        if self.is_playing:
            self.player.pause()
            self.play_pause_btn.setText("▶️")
            self.is_playing = False
            self.wave_visualizer.timer.stop()  # Stop animation
        else:
            if self.current_song:
                self.player.play()
                self.timer.start(1000)
                self.play_pause_btn.setText("⏸")
                self.is_playing = True
                self.wave_visualizer.timer.start()  # Resume animation
            else:
                self.add_song()

    def add_song(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Audio Files (*.mp3 *.wav *.ogg)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            title = file_path.split("/")[-1]  # Extract filename as title

            connection = connect_db()

        try:
            connection = connect_db()
            cursor = connection.cursor()

            # Check if song title already exists
            query_check = "SELECT song_id FROM songs WHERE title = %s"
            cursor.execute(query_check, (title,))
            exists = cursor.fetchone()

            if exists:
                print(f"Song '{title}' already exists in the database. Skipping insertion.")
                QMessageBox.warning(self, "Duplicate Song", f"The song '{title}' is already in the database.")
            else:
                # Insert new song if not already in the database
                query_insert = "INSERT INTO songs (title, file_path) VALUES (%s, %s)"
                cursor.execute(query_insert, (title, file_path))
                connection.commit()
                print("Song inserted successfully with ID:", cursor.lastrowid)
                QMessageBox.information(self, "Song Added", f"'{title}' added successfully!")

            # Fetch all results to clear any unread results issue
            cursor.fetchall()  

        except mysql.connector.Error as error:
            print("Failed to insert song:", error)
            QMessageBox.critical(self, "Database Error", "Failed to insert song. Check console for details.")


        finally:
            cursor.close()
            connection.close()

        # Update the playlist and play the song
        self.current_playlist = [file_path]
        self.current_index = 0
        self.play_song(file_path)

    def previous_song(self):
        if self.current_playlist and self.current_index > 0:
            self.current_index -= 1
            self.play_song(self.current_playlist[self.current_index])

    def next_song(self):
        if self.current_playlist and self.current_index < len(self.current_playlist) - 1:
            self.current_index += 1
            self.play_song(self.current_playlist[self.current_index])

    def seek_position(self, position):
        total_duration = self.player.get_length()
        if total_duration > 0:
            new_position = int((position / 100) * total_duration)
            self.player.set_time(new_position)

    def update_progress(self):
        total_duration = self.player.get_length()
        if total_duration > 0:
            current_position = self.player.get_time()
            progress = int((current_position / total_duration) * 100)
            self.progress_slider.setValue(progress)
            self.update_duration_label(current_position, total_duration)

            if current_position >= total_duration - 1000:
                self.next_song()

    def update_duration_label(self, current, total):
        current_minutes, current_seconds = divmod(current // 1000, 60)
        total_minutes, total_seconds = divmod(total // 1000, 60)
        current_time = f"{current_minutes:02}:{current_seconds:02}"
        total_time = f"{total_minutes:02}:{total_seconds:02}"
        self.duration_label.setText(f"{current_time} / {total_time}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MusicPlayerUI()
    player.show()
    sys.exit(app.exec_())