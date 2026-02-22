import random
import time
from pynput.keyboard import Controller

keyboard = Controller()

def human_type(text: str, should_stop):
    """
    Écrit le texte lettre par lettre.
    S'arrête immédiatement si should_stop() retourne True.
    """
    for char in text:
        if should_stop():
            return
        keyboard.type(char)
        time.sleep(random.uniform(0.05, 0.14))