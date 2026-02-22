from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtGui import QPainter, QPen, QColor
from pynput import keyboard
import pyautogui


class SelectionOverlay(QWidget):
    """
    Overlay transparent :
    - '*' 1ère fois  -> coin haut-gauche (position souris)
    - '*' 2ème fois  -> coin bas-droit (position souris)
    - affiche la zone sélectionnée
    """

    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.start_point: QPoint | None = None
        self.end_point: QPoint | None = None
        self.rect: QRect | None = None

        # Listener clavier global pour '*'
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()

        self.showFullScreen()

    def on_key_press(self, key):
        try:
            if key.char == "*":
                x, y = pyautogui.position()
                pos = QPoint(x, y)

                if self.start_point is None:
                    self.start_point = pos
                    self.end_point = None
                    self.rect = None
                else:
                    self.end_point = pos
                    self.create_rect()

                self.update()
        except Exception:
            pass


    def create_rect(self):
        if not self.start_point or not self.end_point:
            return

        left = min(self.start_point.x(), self.end_point.x())
        top = min(self.start_point.y(), self.end_point.y())
        right = max(self.start_point.x(), self.end_point.x())
        bottom = max(self.start_point.y(), self.end_point.y())

        self.rect = QRect(
            left,
            top,
            right - left,
            bottom - top
        )

    def get_bbox(self):
        if not self.rect:
            return None

        return {
            "left": self.rect.left(),
            "top": self.rect.top(),
            "width": self.rect.width(),
            "height": self.rect.height(),
        }

    def paintEvent(self, event):
        if not self.rect:
            return

        painter = QPainter(self)
        pen = QPen(QColor(255, 0, 0), 3)
        painter.setPen(pen)
        painter.drawRect(self.rect)


    def closeEvent(self, event):
        if self.listener:
            self.listener.stop()
        event.accept()