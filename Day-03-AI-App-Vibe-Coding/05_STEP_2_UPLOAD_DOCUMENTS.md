# Lesson 05 - Step 2: Upload and Chunk Documents

**Time:** 35 minutes  |  **Files:** `app/documents.py`, `app/store.py`, `app/main.py`

---

## Goal

By the end of this lesson the app can:

- receive an uploaded `.txt`, `.md` or `.pdf` file,
- refuse wrong, empty or too-large files with clear messages,
- read the text and cut it into **chunks** (Day 2 Lesson 08),
- keep the chunks in memory and **search** them with TF-IDF (Day 2 Lesson 02).

---

## Understand

### Validate every input

Never trust what users send. Before reading a file we check:

| Check | Status code if it fails |
|---|---|
| The file type is allowed (`.txt`, `.md`, `.pdf`) | **400** Bad Request |
| The file is not too big (2 MB) | **413** Payload Too Large |
| The file is not empty | **400** |
| The file contains readable text | **400** |

### Chunking and searching (from Day 2)

- `chunk_text` cuts the text into pieces of about 500 characters, keeping whole lines and repeating one line as **overlap**.
- `store.py` turns every chunk into a **TF-IDF vector**. A question is also turned into a vector, and the chunks with the highest similarity are returned.
- We also use a tiny **stemmer** so "fees" matches "fee" and "books" matches "book".

**Limitation:** the store lives **in memory**. If the server restarts, the documents are gone. That is fine for an MVP. A real product would save them in a database or vector database.

---

## Do it now

### Part A - `app/documents.py`

**Prompt for your AI assistant:**

```text
Create app/documents.py with:
1. class DocumentError(ValueError) for problems the user can fix.
2. extract_text(filename, data: bytes) -> str. For .txt/.md decode UTF-8 (fallback latin-1).
   For .pdf use pypdf.PdfReader on io.BytesIO and join the text of all pages.
   Raise DocumentError for other types, unreadable PDFs, or files with no text.
3. chunk_text(text, chunk_size=500) -> list of strings. Split into non-empty lines, add ":" to short
   lines that look like headings, then join lines into chunks of at most chunk_size characters,
   repeating the last line of a chunk at the start of the next one (overlap). Split very long lines.
```

**Reference code** - create `app/documents.py`:

```python
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
```

### Part B - `app/store.py`

**Prompt for your AI assistant:**

```text
Create app/store.py with a DocumentStore class that keeps chunks in memory as a list of
{"source": filename, "text": chunk}. Methods: add(filename, chunks) (replaces an older upload with
the same name), clear(), list_documents() (filename + number of chunks), get_text(filename=None),
get_chunks(filename=None), and search(question, top_k=3) using scikit-learn TfidfVectorizer
(rebuild it when documents change; return chunks with a "score" and skip score 0).
Add a small tokens() function (lowercase words, remove stop words, strip plural s/es) used as the
TF-IDF tokenizer, and keywords(text) returning a set of tokens. Create one shared store = DocumentStore().
```

**Reference code** - create `app/store.py`:

```python
"""
store.py - keeps the uploaded documents in memory and finds the chunks that match a question.

We use TF-IDF vectors (Day 2, Lesson 02) for retrieval: free, fast, offline and easy to understand.
The same class could later use embeddings and a real vector database (Day 2, Lesson 08).

Note: everything is kept in memory, so it is lost when the server restarts. That is fine for a demo.
"""

import re

from sklearn.feature_extraction.text import TfidfVectorizer

STOP_WORDS = {
    "the", "a", "an", "is", "are", "of", "to", "for", "and", "or", "what", "how", "in", "on", "if",
    "i", "my", "do", "does", "can", "it", "much", "many", "who", "when", "which", "why", "with", "be",
}


def simple_stem(word):
    """Very small stemmer: 'fees' -> 'fee', 'books' -> 'book', 'classes' -> 'class'."""
    if len(word) > 4 and word.endswith("es") and word[-3] in "sxz":
        return word[:-2]
    if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def tokens(text):
    """Split text into lowercase, stemmed words without stop words."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [simple_stem(w) for w in words if w not in STOP_WORDS and len(w) > 1]


def keywords(text):
    """The set of important words in a text."""
    return set(tokens(text))


class DocumentStore:
    def __init__(self):
        self.chunks = []  # list of {"source": filename, "text": chunk}
        self._vectorizer = None
        self._matrix = None

    # ---- adding and removing -------------------------------------------------
    def add(self, filename, chunks):
        self.chunks = [c for c in self.chunks if c["source"] != filename]  # replace an older upload
        self.chunks += [{"source": filename, "text": text} for text in chunks]
        self._rebuild()

    def clear(self):
        self.chunks = []
        self._rebuild()

    def list_documents(self):
        counts = {}
        for c in self.chunks:
            counts[c["source"]] = counts.get(c["source"], 0) + 1
        return [{"filename": name, "chunks": n} for name, n in counts.items()]

    def get_text(self, filename=None):
        selected = [c["text"] for c in self.chunks if filename is None or c["source"] == filename]
        return "\n".join(selected)

    def get_chunks(self, filename=None):
        return [c for c in self.chunks if filename is None or c["source"] == filename]

    # ---- searching -----------------------------------------------------------
    def _rebuild(self):
        if self.chunks:
            self._vectorizer = TfidfVectorizer(tokenizer=tokens, token_pattern=None, lowercase=False)
            self._matrix = self._vectorizer.fit_transform([c["text"] for c in self.chunks])
        else:
            self._vectorizer, self._matrix = None, None

    def search(self, question, top_k=3):
        """Return the top_k chunks most similar to the question, each with a score from 0 to 1."""
        if not self.chunks:
            return []
        question_vector = self._vectorizer.transform([question])
        scores = (self._matrix @ question_vector.T).toarray().ravel()
        best = scores.argsort()[::-1][:top_k]
        return [{**self.chunks[i], "score": round(float(scores[i]), 3)} for i in best if scores[i] > 0]


# One shared store for the whole app
store = DocumentStore()
```

### Part C - Add the upload endpoints to `app/main.py`

**Prompt for your AI assistant:**

```text
In app/main.py add:
- an async helper read_upload(upload, allowed_types) that checks the extension (400), size against
  config.MAX_UPLOAD_BYTES (413) and empty files (400), and returns the bytes;
- POST /api/documents: read the upload, extract_text (DocumentError -> 400), chunk_text, store.add,
  log it, return filename, characters and chunks;
- GET /api/documents (list) and DELETE /api/documents (clear);
- add "documents": number of documents to the /health response.
```

**Reference code.** Make these three changes in `app/main.py`:

**1. Add these import lines** at the top (with the other imports; replace the old `from fastapi import ...` line):

```python
from pathlib import Path
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from app.documents import DocumentError, chunk_text, extract_text
from app.store import store
```

**2. Replace the `health` function** with this version (it now also counts documents):

```python
@app.get("/health")
def health():
    """Used by people and by monitoring tools to check that the app is alive."""
    return {"status": "ok", "ai_mode": current_mode(), "documents": len(store.list_documents())}
```

**3. Add the helper and the endpoints.** Put `read_upload` just after the middleware, and the three endpoints at the end of the file:

```python
async def read_upload(upload: UploadFile, allowed_types):
    extension = Path(upload.filename or "").suffix.lower()
    if extension not in allowed_types:
        raise HTTPException(400, f"File type '{extension or 'none'}' is not allowed. Use: {', '.join(sorted(allowed_types))}")
    data = await upload.read()
    if len(data) > config.MAX_UPLOAD_BYTES:
        raise HTTPException(413, f"File is too large. The limit is {config.MAX_UPLOAD_MB:g} MB.")
    if not data:
        raise HTTPException(400, "The file is empty.")
    return data
```

```python
# ---------------------------------------------------------------------------
# Feature 1: documents
# ---------------------------------------------------------------------------
@app.post("/api/documents")
async def upload_document(file: UploadFile = File(...)):
    data = await read_upload(file, config.ALLOWED_DOCUMENT_TYPES)
    try:
        text = extract_text(file.filename, data)
    except DocumentError as error:
        raise HTTPException(400, str(error))
    chunks = chunk_text(text)
    store.add(file.filename, chunks)
    logger.info("Document added: %s (%d chunks)", file.filename, len(chunks))
    return {"filename": file.filename, "characters": len(text), "chunks": len(chunks)}


@app.get("/api/documents")
def list_documents():
    return {"documents": store.list_documents()}


@app.delete("/api/documents")
def delete_documents():
    store.clear()
    return {"message": "All documents removed."}
```

Not sure where things go? Open the full file below and compare.

<details>
<summary>Click to see the complete <code>app/main.py</code> after this step</summary>

```python
"""
main.py - the web application (FastAPI).

Run it from the project folder with:
    uvicorn app.main:app --reload
Then open http://127.0.0.1:8000  (the app)  or  http://127.0.0.1:8000/docs  (the API documentation)
"""

import logging
import time
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, Request, UploadFile

from app import config
from app.documents import DocumentError, chunk_text, extract_text
from app.llm import current_mode
from app.store import store

# ---------------------------------------------------------------------------
# Logging: one line per request, so we can see what happens (Day 4 monitoring)
# ---------------------------------------------------------------------------
logging.basicConfig(level=config.LOG_LEVEL, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("study_buddy")

app = FastAPI(
    title="Study Buddy API",
    description="An AI learning and research assistant: upload notes, ask questions, get summaries, "
    "practice questions and CSV insights.",
    version="1.0.0",
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info("%s %s -> %s (%.0f ms)", request.method, request.url.path, response.status_code, duration_ms)
    return response


async def read_upload(upload: UploadFile, allowed_types):
    extension = Path(upload.filename or "").suffix.lower()
    if extension not in allowed_types:
        raise HTTPException(400, f"File type '{extension or 'none'}' is not allowed. Use: {', '.join(sorted(allowed_types))}")
    data = await upload.read()
    if len(data) > config.MAX_UPLOAD_BYTES:
        raise HTTPException(413, f"File is too large. The limit is {config.MAX_UPLOAD_MB:g} MB.")
    if not data:
        raise HTTPException(400, "The file is empty.")
    return data


# ---------------------------------------------------------------------------
# Pages and health check
# ---------------------------------------------------------------------------
@app.get("/health")
def health():
    """Used by people and by monitoring tools to check that the app is alive."""
    return {"status": "ok", "ai_mode": current_mode(), "documents": len(store.list_documents())}


# ---------------------------------------------------------------------------
# Feature 1: documents
# ---------------------------------------------------------------------------
@app.post("/api/documents")
async def upload_document(file: UploadFile = File(...)):
    data = await read_upload(file, config.ALLOWED_DOCUMENT_TYPES)
    try:
        text = extract_text(file.filename, data)
    except DocumentError as error:
        raise HTTPException(400, str(error))
    chunks = chunk_text(text)
    store.add(file.filename, chunks)
    logger.info("Document added: %s (%d chunks)", file.filename, len(chunks))
    return {"filename": file.filename, "characters": len(text), "chunks": len(chunks)}


@app.get("/api/documents")
def list_documents():
    return {"documents": store.list_documents()}


@app.delete("/api/documents")
def delete_documents():
    store.clear()
    return {"message": "All documents removed."}
```

</details>

### Part D - Try it

The server reloads by itself when you save. Open http://127.0.0.1:8000/docs:

1. Click **POST /api/documents -> Try it out**.
2. Click **Choose File** and pick `sample_files/college_library_rules.txt`.
3. Click **Execute**.

---

## Check

- [ ] The response is `{"filename": "college_library_rules.txt", "characters": 1463, "chunks": 5}`.
- [ ] **GET /api/documents** lists the file with 5 chunks.
- [ ] Uploading a wrong type (for example a `.png` or `.docx`) gives **400** with "is not allowed".
- [ ] `/health` now shows `"documents": 1`.

Test the search directly in the second terminal:

```powershell
python -c "from app.store import store; from app.documents import chunk_text; store.add('t.txt', chunk_text(open('sample_files/college_library_rules.txt').read())); print(store.search('late fee', top_k=1))"
```

The first result should be the chunk that starts with `Late fees:`.

---

## Review the code

- [ ] Are **all** inputs checked before use (type, size, empty)?
- [ ] Are error messages helpful to a normal user, without showing internal details?
- [ ] Does `extract_text` handle a PDF that has no text (a scanned image)?

---

## What just happened?

Uploads go through `read_upload` (validation) -> `extract_text` (bytes to text) -> `chunk_text` (text to chunks) -> `store.add` (chunks to TF-IDF vectors in memory). This is the **indexing** half of RAG from Day 2.

---

## Try it yourself

1. Upload all three files in `sample_files/`. How many chunks in total?
2. Change `MAX_UPLOAD_MB=0.001` in `.env`, restart the server, and upload a file. You should get **413**. Change it back.
3. Upload a PDF of your own notes.

---

## If it does not work

| Problem | Fix |
|---|---|
| `Form data requires "python-multipart" to be installed` | Run `pip install -r requirements.txt` again (`fastapi[standard]` includes it). |
| `ImportError: cannot import name 'store' from 'app.store'` | `store = DocumentStore()` is missing at the end of `store.py`. |
| `NameError: name 'Path' is not defined` | Add `from pathlib import Path` to the imports of `main.py`. |
| The PDF says "no readable text" | It is a scanned image. Use the OCR feature (Lesson 11) or a PDF with real text. |

Next: **[Lesson 06 - Step 3: ask questions with RAG](06_STEP_3_ASK_QUESTIONS_RAG.md)**
