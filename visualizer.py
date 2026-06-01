<<<<<<< HEAD
import random
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QColor, QPen

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
=======
import random
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QColor, QPen

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
>>>>>>> b7b53d00ed6f75fe95d39350186ca96275e315b0
            painter.drawLine(x, y - bar_height, x, y + bar_height)