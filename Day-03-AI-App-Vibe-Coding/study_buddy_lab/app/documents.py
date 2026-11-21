"""
documents.py - read text out of uploaded files and cut it into chunks.
"""

import io
from pathlib import Path


class DocumentError(ValueError):
    """A problem with an uploaded file that the user can fix (wrong type, empty, unreadable)."""


def extract_text(filename, data):
    """Return the plain text inside a .txt, .md or .pdf file given as bytes."""
    extension = Path(filename).suffix.lower()

    if extension in {".txt", ".md"}:
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            text = data.decode("latin-1")  # fallback for files saved in older encodings
    elif extension == ".pdf":
        from pypdf import PdfReader

        try:
            reader = PdfReader(io.BytesIO(data))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as error:
            raise DocumentError(f"Could not read this PDF ({type(error).__name__}).") from error
    else:
        raise DocumentError(f"File type '{extension}' is not supported. Use .txt, .md or .pdf.")

    text = text.replace("\r\n", "\n").strip()
    if not text:
        raise DocumentError("The file has no readable text. (A scanned PDF is an image - try the OCR feature.)")
    return text


def chunk_text(text, chunk_size=500):
    """
    Cut text into pieces of about chunk_size characters, keeping whole lines together.
    The last line of each chunk is repeated at the start of the next one (overlap),
    so a fact that sits on a border is not lost.
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    # A short line without a full stop is usually a heading: add ":" so it reads well when joined.
    lines = [line if line[-1] in ".!?:;" or len(line) > 80 else line + ":" for line in lines]

    chunks, current = [], []
    for line in lines:
        # Very long lines (common in PDFs) are split into smaller pieces first.
        while len(line) > chunk_size:
            cut = line.rfind(" ", 0, chunk_size)
            cut = cut if cut > 0 else chunk_size
            if current:
                chunks.append(" ".join(current))
                current = []
            chunks.append(line[:cut].strip())
            line = line[cut:].strip()
        if current and len(" ".join(current + [line])) > chunk_size:
            chunks.append(" ".join(current))
            current = current[-1:]  # overlap
        current.append(line)
    if current:
        chunks.append(" ".join(current))
    return [c for c in chunks if c]
