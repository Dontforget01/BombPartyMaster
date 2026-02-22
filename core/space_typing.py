from pynput import keyboard


class SpaceTyper:
    def __init__(self):
        self.word = ""
        self.index = 0
        self.active = False
        self.synced = False  # 🔑 synchronisation mot/espace
        self.controller = keyboard.Controller()
        self.listener = None

    def set_word(self, word: str):
        """
        Appelé à CHAQUE nouveau mot détecté
        """
        self.word = word
        self.index = 0
        self.synced = True  # prêt à consommer le prochain ESPACE

    def start(self):
        if self.listener:
            return

        self.active = True
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            suppress=False
        )
        self.listener.start()

    def stop(self):
        self.active = False
        self.synced = False
        if self.listener:
            self.listener.stop()
            self.listener = None

    def on_press(self, key):
        if not self.active or not self.synced:
            return

        try:
            if key == keyboard.Key.space:
                self.type_next_letter()
                return False  # bloque l'espace
        except Exception:
            pass

    def type_next_letter(self):
        if self.index < len(self.word):
            self.controller.type(self.word[self.index])
            self.index += 1
        else:
            # mot fini → ENTER
            self.controller.press(keyboard.Key.enter)
            self.controller.release(keyboard.Key.enter)
            self.synced = False  # attendre un NOUVEAU mot