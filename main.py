<<<<<<< HEAD
import sys
from PyQt5.QtWidgets import QApplication
from music_player import MusicPlayerUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MusicPlayerUI()
    player.show()
=======
import sys
from PyQt5.QtWidgets import QApplication
from music_player import MusicPlayerUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MusicPlayerUI()
    player.show()
>>>>>>> b7b53d00ed6f75fe95d39350186ca96275e315b0
    sys.exit(app.exec_())