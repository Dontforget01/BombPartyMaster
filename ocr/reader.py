import easyocr
import numpy as np
from PIL import Image

reader = easyocr.Reader(['fr', 'en'], gpu=False)


def read_syllable(image: Image.Image) -> str:
    """
    Lit le texte contenu dans l'image et retourne une syllabe nettoyée
    """
    img_np = np.array(image)

    results = reader.readtext(
        img_np,
        detail=0,
        paragraph=False
    )

    if not results:
        return ""

    text = results[0]

    text = text.lower()
    text = text.replace(" ", "")
    text = "".join(c for c in text if c.isalpha())

    return text