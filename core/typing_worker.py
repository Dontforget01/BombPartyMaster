# core/typing_worker.py
from PySide6.QtCore import QThread
from core.typer import human_type


class TypingWorker(QThread):
    def __init__(self, text: str):
        super().__init__()
        self.text = text
        self._stop = False

    def request_stop(self):
        self._stop = True

    def run(self):
        human_type(self.text, lambda: self._stop)