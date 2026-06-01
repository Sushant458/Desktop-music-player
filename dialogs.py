<<<<<<< HEAD
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QListWidgetItem

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

    def song_selected(self, item):
        song_name = item.text()
        # Prevent clicking the headers
        if not song_name.startswith("---"):
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
=======
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QListWidgetItem

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

    def song_selected(self, item):
        song_name = item.text()
        # Prevent clicking the headers
        if not song_name.startswith("---"):
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
>>>>>>> b7b53d00ed6f75fe95d39350186ca96275e315b0
        self.close()