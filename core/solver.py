# core/solver.py
import random
import string

# ✅ Alphabet COMPLET
GAME_ALPHABET = set(string.ascii_lowercase)


class LetterCoverageSolver:
    """
    Solver intelligent :
    - accepte TOUT l'alphabet
    - priorise les lettres NON checkées
    - maximise ensuite la couverture totale
    - ne retourne JAMAIS "" s'il existe un match
    """

    def __init__(self, words: list[str]):
        self.words = words

    # -----------------------
    # Scores
    # -----------------------
    def unchecked_score(self, word: str, unchecked_letters: set[str]) -> int:
        """Nombre de lettres NON encore checkées utilisées"""
        return len(set(word) & unchecked_letters)

    def coverage_score(self, word: str) -> int:
        """Couverture totale unique"""
        return len(set(word))

    # -----------------------
    # Solver principal
    # -----------------------
    def find_word(
        self,
        syllable: str,
        forbidden_words: set[str],
        unchecked_letters: set[str],
    ) -> str:
        if not syllable:
            return ""

        # 1️⃣ Tous les mots valides contenant la syllabe
        candidates = [
            w for w in self.words
            if (
                syllable in w
                and w not in forbidden_words
                and set(w) <= GAME_ALPHABET
            )
        ]

        # ❌ Aucun mot possible → vrai no match
        if not candidates:
            return ""

        # 2️⃣ Score PRIORITAIRE : lettres non checkées
        max_unchecked = max(
            self.unchecked_score(w, unchecked_letters) for w in candidates
        )
        best_unchecked = [
            w for w in candidates
            if self.unchecked_score(w, unchecked_letters) == max_unchecked
        ]

        # 3️⃣ Score secondaire : couverture globale
        max_coverage = max(
            self.coverage_score(w) for w in best_unchecked
        )
        best_final = [
            w for w in best_unchecked
            if self.coverage_score(w) == max_coverage
        ]

        # 4️⃣ Choix final stable
        return random.choice(best_final)