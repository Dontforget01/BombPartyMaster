from PySide6.QtCore import QThread, Signal

from capture.screen_capture import capture_custom
from ocr.reader import read_syllable


class OCRWorker(QThread):
    syllable_detected = Signal(str)

    def __init__(self, bbox=None):
        super().__init__()
        self.bbox = bbox

    def run(self):
        if not self.bbox:
            return

        image = capture_custom(self.bbox)
        syllable = read_syllable(image)
        self.syllable_detected.emit(syllable)