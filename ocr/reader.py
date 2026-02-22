import easyocr
import numpy as np
from PIL import Image

# Le reader est lourd → on l'instancie UNE seule fois
reader = easyocr.Reader(['fr', 'en'], gpu=False)


def read_syllable(image: Image.Image) -> str:
    """
    Lit le texte contenu dans l'image et retourne une syllabe nettoyée
    """
    img_np = np.array(image)

    results = reader.readtext(
        img_np,
        detail=0,        # seulement le texte
        paragraph=False
    )

    if not results:
        return ""

    # On prend le texte le plus probable
    text = results[0]

    # Nettoyage
    text = text.lower()
    text = text.replace(" ", "")
    text = "".join(c for c in text if c.isalpha())

    return text