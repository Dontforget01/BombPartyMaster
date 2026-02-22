# core/dictionary.py
import os
import sys


def resource_path(relative_path: str) -> str:
    """
    Retourne le bon chemin que l'on soit :
    - en mode script Python
    - en mode exe PyInstaller
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def load_dictionary(path: str) -> list[str]:
    words = []

    full_path = resource_path(path)

    encodings = ["utf-8", "latin-1", "cp1252"]

    for encoding in encodings:
        try:
            with open(full_path, "r", encoding=encoding) as f:
                for line in f:
                    word = line.strip().lower()
                    if word.isalpha():
                        words.append(word)

            print(f"[INFO] Dictionnaire chargé : {full_path} ({encoding})")
            return words

        except UnicodeDecodeError:
            continue

    raise RuntimeError(
        f"Impossible de lire le fichier dictionnaire : {full_path}"
    )