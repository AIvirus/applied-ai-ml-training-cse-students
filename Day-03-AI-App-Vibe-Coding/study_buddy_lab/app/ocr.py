"""
ocr.py - OPTIONAL feature: read text from an image with Tesseract OCR.

Needs the Tesseract program installed on the computer (see Day 3 Lesson 11).
If it is not installed, the app still runs; only this feature reports that it is unavailable.
"""

import io
import os
import shutil


class OCRUnavailable(RuntimeError):
    pass


def _find_tesseract():
    import pytesseract

    windows_default = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if not shutil.which("tesseract") and os.path.exists(windows_default):
        pytesseract.pytesseract.tesseract_cmd = windows_default
    return pytesseract


def image_to_text(data):
    try:
        from PIL import Image

        pytesseract = _find_tesseract()
        image = Image.open(io.BytesIO(data)).convert("L")  # "L" = grayscale, which helps OCR
        return pytesseract.image_to_string(image).strip()
    except ImportError as error:
        raise OCRUnavailable("OCR packages are not installed (pip install pytesseract pillow).") from error
    except Exception as error:
        if "tesseract" in type(error).__name__.lower() or "tesseract" in str(error).lower():
            raise OCRUnavailable("The Tesseract program is not installed on this computer.") from error
        raise
