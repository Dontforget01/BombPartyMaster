from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt, QTimer

APP_NAME = "Bomb Party Master"
APP_VERSION = "v0.1"


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(420, 260)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color:#121212;")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)

        title = QLabel(APP_NAME)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size:24px;
            font-weight:800;
            color:#f1c40f;
        """)

        version = QLabel(APP_VERSION)
        version.setAlignment(Qt.AlignCenter)
        version.setStyleSheet("color:#666;font-size:11px;")

        subtitle = QLabel("Initialisation du programme…")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color:#aaaaaa;font-size:13px;")

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(10)
        self.progress.setStyleSheet("""
            QProgressBar {
                background:#1e1e1e;
                border-radius:5px;
            }
            QProgressBar::chunk {
                background:#4da3ff;
                border-radius:5px;
            }
        """)

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(version)
        layout.addWidget(subtitle)
        layout.addWidget(self.progress)
        layout.addStretch()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.advance)
        self.timer.start(25)

    def advance(self):
        value = self.progress.value() + 2
        self.progress.setValue(value)
        if value >= 100:
            self.timer.stop()