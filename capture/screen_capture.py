import mss
from PIL import Image


def capture_custom(bbox) -> Image.Image:
    with mss.mss() as sct:
        screenshot = sct.grab(bbox)
        return Image.frombytes("RGB", screenshot.size, screenshot.rgb)