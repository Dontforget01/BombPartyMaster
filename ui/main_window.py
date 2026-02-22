from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QDialog, QTextEdit
)
from PySide6.QtCore import Qt, QTimer
from pynput import keyboard
import os
import sys
from PySide6.QtGui import QIcon
from ocr.ocr_worker import OCRWorker
from core.dictionary import load_dictionary
from core.solver import LetterCoverageSolver, GAME_ALPHABET
from core.typing_worker import TypingWorker
from ui.selection_overlay import SelectionOverlay
# ======================
# App info
# ======================
APP_NAME = "Bomb Party Master"
APP_VERSION = "v0.1"


def resource_path(relative_path: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def panel(title: str) -> tuple[QFrame, QVBoxLayout]:
    frame = QFrame()
    frame.setStyleSheet("""
        QFrame {
            background-color:#111;
            border:1px solid #2a2a2a;
            padding:8px;
            border-radius:6px;
        }
        QLabel { color:#ddd; }
    """)
    layout = QVBoxLayout(frame)
    layout.setSpacing(4)

    lbl = QLabel(title)
    lbl.setStyleSheet("color:#777;font-size:10px;")
    layout.addWidget(lbl)

    return frame, layout


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"{APP_NAME} {APP_VERSION}")
        self.setFixedSize(980, 620)
        self.setStyleSheet("background-color:#0b0b0b;")
        self.setWindowIcon(QIcon(resource_path("assets/icon.ico")))
        self.last_syllable = ""
        self.current_word = ""
        self.waiting_for_enter = False
        self.waiting_to_type = False
        
        self.checked_letters = set()
        self.unchecked_letters = GAME_ALPHABET.copy()
        self.used_words = set()
        self.words_tried = []


        self.words = load_dictionary("liste_francais.txt")
        self.solver = LetterCoverageSolver(self.words)

        self.ocr_worker = None
        self.overlay = None
        self.overlay_enabled = False

        self.detecting = False
        self.auto_typing = False
        self.typing_worker = None

        keyboard.Listener(on_press=self.on_key_press).start()


        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(10)


        main = QVBoxLayout()
        main.setSpacing(8)

        self.syllable_label = QLabel("—")
        self.syllable_label.setAlignment(Qt.AlignCenter)
        self.syllable_label.setStyleSheet("""
            font-size:52px;
            font-weight:900;
            color:#f1c40f;
            letter-spacing:3px;
        """)

        self.word_label = QLabel("—")
        self.word_label.setAlignment(Qt.AlignCenter)
        self.word_label.setStyleSheet("""
            font-size:24px;
            font-weight:600;
            color:#4da3ff;
        """)

        frame_sw, lay_sw = panel("INPUT / OUTPUT")
        lay_sw.addWidget(self.syllable_label)
        lay_sw.addWidget(self.word_label)

        self.checked_label = QLabel()
        self.unchecked_label = QLabel()
        self.stats_label = QLabel()
        self.matches_label = QLabel("Matches: —")

        for lbl in (
            self.checked_label,
            self.unchecked_label,
            self.stats_label,
            self.matches_label,
        ):
            lbl.setStyleSheet("font-size:11px;color:#ccc;")

        frame_ls, lay_ls = panel("PROGRESSION")
        lay_ls.addWidget(self.checked_label)
        lay_ls.addWidget(self.unchecked_label)
        lay_ls.addWidget(self.stats_label)
        lay_ls.addWidget(self.matches_label)

        self.history_label = QLabel("History: —")
        self.history_label.setStyleSheet("font-size:11px;color:#999;")

        frame_hist, lay_hist = panel("HISTORY")
        lay_hist.addWidget(self.history_label)

        self.status_label = QLabel("[IDLE]")
        self.status_label.setStyleSheet("""
            font-size:11px;
            color:#888;
            padding:4px;
        """)


        footer = QLabel(f"{APP_NAME} {APP_VERSION}")
        footer.setAlignment(Qt.AlignLeft)
        footer.setStyleSheet("font-size:10px;color:#555;")

        main.addWidget(frame_sw)
        main.addWidget(frame_ls)
        main.addWidget(frame_hist)
        main.addWidget(self.status_label)
        main.addStretch()
        main.addWidget(footer)

        side = QVBoxLayout()
        side.setSpacing(8)

        def btn(txt):
            b = QPushButton(txt)
            b.setMinimumHeight(32)
            b.setStyleSheet("""
                QPushButton {
                    background:#151515;
                    color:#ddd;
                    border:1px solid #2f2f2f;
                    border-radius:6px;
                    font-size:11px;
                    padding:6px;
                }
                QPushButton:hover {
                    background:#1f1f1f;
                    border-color:#4da3ff;
                }
            """)
            return b

        self.btn_detect = btn("OCR [OFF]")
        self.btn_auto = btn("AUTO TYPE [OFF]")
        self.btn_overlay = btn("OCR ZONE")
        self.btn_reset = btn("RESET LETTERS")
        self.btn_reset_words = btn("RESET WORDS")
        self.btn_help = btn("HELP")

        for b in (
            self.btn_detect,
            self.btn_auto,
            self.btn_overlay,
            self.btn_reset,
            self.btn_reset_words,
            self.btn_help,
        ):
            side.addWidget(b)

        side.addStretch()

        root.addLayout(main, 3)
        root.addLayout(side, 1)


        self.ocr_timer = QTimer()
        self.ocr_timer.setInterval(700)
        self.ocr_timer.timeout.connect(self.run_ocr)


        self.btn_detect.clicked.connect(self.toggle_detection)
        self.btn_auto.clicked.connect(self.toggle_auto_typing)
        self.btn_overlay.clicked.connect(self.toggle_overlay)
        self.btn_reset.clicked.connect(self.reset_checked_letters)
        self.btn_reset_words.clicked.connect(self.reset_used_words)
        self.btn_help.clicked.connect(self.show_help)

        self.update_letters_ui()



    def start_runtime_services(self):
        QTimer.singleShot(500, self._start_keyboard_listener)

    def _start_keyboard_listener(self):
        from pynput import keyboard
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press
        )
        self.keyboard_listener.start()


    def on_key_press(self, key):
        from pynput import keyboard

        if key == keyboard.Key.esc:
            self.search_new_word()
        elif key == keyboard.Key.space:
            if self.auto_typing and self.waiting_to_type:
                self.waiting_to_type = False
                self.start_auto_typing()
        elif key == keyboard.Key.enter:
            if self.waiting_for_enter:
                self.validate_word()


    def run_ocr(self):
        if self.ocr_worker and self.ocr_worker.isRunning():
            return
        if not self.overlay_enabled or not self.overlay:
            return

        bbox = self.overlay.get_bbox()
        if not bbox:
            return

        self.ocr_worker = OCRWorker(bbox=bbox)
        self.ocr_worker.syllable_detected.connect(self.update_syllable)
        self.ocr_worker.finished.connect(lambda: setattr(self, "ocr_worker", None))
        self.ocr_worker.start()

    def update_syllable(self, syllable: str):
        if not syllable or syllable == self.last_syllable:
            return

        self.last_syllable = syllable
        self.words_tried.clear()
        self.syllable_label.setText(syllable)
        self.syllable_label.setStyleSheet("""
        font-size:52px;
        font-weight:900;
        color:#f1c40f;
        letter-spacing:3px;
    """)
        self.word_label.setStyleSheet("""
        font-size:24px;
        font-weight:600;
        color:#4da3ff;
    """)

        match_count = self.count_matching_words(syllable)
        self.matches_label.setText(f"Matches: {match_count}")

        self.search_new_word()

    def search_new_word(self):
        forbidden = self.used_words | set(self.words_tried)
        word = self.solver.find_word(
            self.last_syllable,
            forbidden,
            self.unchecked_letters
        )

        if not word:
            self.word_label.setText("NO MATCH")
            return

        self.current_word = word
        self.words_tried.append(word)
        self.word_label.setText(word)
        self.waiting_for_enter = True
        self.waiting_to_type = True
        self.history_label.setText("History: " + " | ".join(self.words_tried[-5:]))
        self.update_stats()

    def start_auto_typing(self):
        if self.typing_worker and self.typing_worker.isRunning():
            return
        self.typing_worker = TypingWorker(self.current_word)
        self.typing_worker.start()

    def validate_word(self):
        self.used_words.add(self.current_word)
        letters = set(self.current_word)
        self.checked_letters |= letters
        self.unchecked_letters -= letters
        self.current_word = ""
        self.update_letters_ui()


    def update_letters_ui(self):
        self.checked_label.setText("Checked: " + " ".join(sorted(self.checked_letters)))
        self.unchecked_label.setText("Remaining: " + " ".join(sorted(self.unchecked_letters)))
        self.update_stats()

    def update_stats(self):
        self.stats_label.setText(
            f"Stats: words={len(self.used_words)} letters={len(self.checked_letters)}/{len(GAME_ALPHABET)}"
        )

    def count_matching_words(self, syllable: str) -> int:
        return sum(1 for w in self.words if syllable in w)
    
    def toggle_detection(self):
        self.detecting = not self.detecting
        if self.detecting:
            self.ocr_timer.start()
            self.btn_detect.setText("OCR [ON]")
            self.status_label.setText("[RUNNING] OCR active")
        else:
            self.ocr_timer.stop()
            self.btn_detect.setText("OCR [OFF]")
            self.status_label.setText("[IDLE] OCR off")

    def toggle_auto_typing(self):
        self.auto_typing = not self.auto_typing
        self.btn_auto.setText(
            "AUTO TYPE [ON]" if self.auto_typing else "AUTO TYPE [OFF]"
        )

    def toggle_overlay(self):
        self.overlay_enabled = not self.overlay_enabled
        if self.overlay_enabled:
            self.overlay = SelectionOverlay()
            self.status_label.setText("[CONFIG] OCR zone")
        else:
            if self.overlay:
                self.overlay.close()
                self.overlay = None
            self.status_label.setText("[CONFIG] OCR zone off")

    def reset_checked_letters(self):
        self.checked_letters.clear()
        self.unchecked_letters = GAME_ALPHABET.copy()
        self.update_letters_ui()
        self.status_label.setText("[RESET] Letters")

    def reset_used_words(self):
        self.used_words.clear()
        self.status_label.setText("[RESET] Words")

    def show_help(self):
        d = QDialog(self)
        d.setWindowTitle("Help")
        d.setFixedSize(480, 420)
        d.setStyleSheet("background:#111;color:#ccc;")

        t = QTextEdit()
        t.setReadOnly(True)
        t.setStyleSheet("background:#0b0b0b;color:#ccc;font-size:11px;")
        t.setText("""
SPACE  → auto type
ENTER  → validate
ESC    → skip

OCR        → enable scan
AUTO TYPE → enable typing
OCR ZONE  → select screen
RESET     → reset state
        """)

        l = QVBoxLayout(d)
        l.addWidget(t)
        d.exec()