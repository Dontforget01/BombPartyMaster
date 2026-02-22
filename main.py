import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

from ui.main_window import MainWindow
from ui.splash_screen import SplashScreen


def main():
    app = QApplication(sys.argv)

    splash = SplashScreen()
    splash.show()

    window = MainWindow()

    def finish_loading():
        splash.close()
        window.show()

    QTimer.singleShot(1600, finish_loading)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()