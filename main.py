
import sys
from PyQt5.QtWidgets import QApplication
from music_player import MusicPlayerUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MusicPlayerUI()
    player.show()
    sys.exit(app.exec_())