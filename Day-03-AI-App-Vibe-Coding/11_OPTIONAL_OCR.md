# Lesson 11 - Optional: Read Text from Images (OCR)

**Time:** 15 minutes  |  **Files:** `app/ocr.py`, `app/main.py`  |  **Extension feature**

Do this lesson if you have time. The app works without it.

---

## Goal

Students can upload a **photo of printed notes**, read the text with **OCR** (Day 2 Lesson 03), and optionally add it to their documents so they can ask questions about it.

---

## Understand

- `pytesseract` (a Python package) calls **Tesseract**, a separate free OCR **program**. You must install the program too.
- If Tesseract is missing, the endpoint returns **503 Service Unavailable** with a clear message. The rest of the app keeps working. This is called **graceful degradation**.
- Converting the image to grayscale first helps OCR.

---

## Do it now

### Part A - Install Tesseract (once)

- **Windows:** download the installer from https://github.com/UB-Mannheim/tesseract/wiki and install with default options (to `C:\Program Files\Tesseract-OCR`). Close and reopen VS Code.
- **macOS:** `brew install tesseract` (needs Homebrew from https://brew.sh)
- **Linux (Ubuntu):** `sudo apt install tesseract-ocr`

Check it in a new terminal:

```powershell
tesseract --version
```

On Windows, if this says "not recognized", that is OK - our code also looks in the default install folder.

### Part B - `app/ocr.py`

**Prompt for your AI assistant:**

```text
Create app/ocr.py with class OCRUnavailable(RuntimeError) and image_to_text(data: bytes) -> str.
Open the image with Pillow, convert to grayscale, and run pytesseract.image_to_string.
On Windows, if "tesseract" is not on PATH but C:\Program Files\Tesseract-OCR\tesseract.exe exists,
use that path. Raise OCRUnavailable if the packages or the Tesseract program are missing.
```

**Reference code** - create `app/ocr.py`:

```python
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
```

### Part C - Add the endpoint to `app/main.py`

**1. Add this import line:**

```python
from app.ocr import OCRUnavailable, image_to_text
```

**2. Add the endpoint** at the end of the file:

```python
# ---------------------------------------------------------------------------
# Optional feature 5: OCR
# ---------------------------------------------------------------------------
@app.post("/api/ocr")
async def ocr(file: UploadFile = File(...), add_to_documents: bool = Form(default=False)):
    data = await read_upload(file, config.ALLOWED_IMAGE_TYPES)
    try:
        text = image_to_text(data)
    except OCRUnavailable as error:
        raise HTTPException(503, f"OCR is not available: {error}")
    if add_to_documents and text:
        store.add(f"{file.filename} (OCR)", chunk_text(text))
    return {"filename": file.filename, "text": text, "added_to_documents": bool(add_to_documents and text)}
```

### Part D - Try it

Take a clear photo of a printed page (or a screenshot of text), save it as `.png` or `.jpg`, and upload it in section 5 of the web page. Tick "Add the text to my documents" and then ask a question about it.

---

## Check

- [ ] With Tesseract installed: the text from the image appears.
- [ ] With "Add the text to my documents" ticked, the image appears in the document list as `name.png (OCR)`.
- [ ] Without Tesseract: you get a clear 503 message, and the other features still work.

---

## What just happened?

You added a Computer Vision feature to the app and made it **fail safely** when a dependency is missing.

---

## If it does not work

| Problem | Fix |
|---|---|
| 503 "Tesseract program is not installed" | Install it (Part A), then restart VS Code and the server. |
| The text is full of mistakes | Use a sharper, well-lit, straight photo of **printed** text. Handwriting is hard for Tesseract. |

Next: **[Lesson 12 - Optional: research agent](12_OPTIONAL_RESEARCH_AGENT.md)**
