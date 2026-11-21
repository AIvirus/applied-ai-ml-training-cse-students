# Lesson 07 - Step 4: Summary and Practice Questions

**Time:** 25 minutes  |  **Files:** `app/study.py` (part 2), `app/main.py`

---

## Goal

By the end of this lesson the app can:

- summarise the notes in bullet points,
- create practice questions with answers as **JSON**, and **validate** them with Pydantic (Day 2 Lesson 07),
- retry once if the AI returns invalid JSON, and fall back to safe mock questions.

---

## Understand

### Keeping prompts small

We send at most 12,000 characters of notes to the AI (`text[:12000]`). Long prompts cost more tokens, take longer, and can go over the context window.

### Structured output you can trust

Practice questions must have a fixed shape so the web page can show them:

```json
{"questions": [{"question": "What is active recall?", "answer": "Testing yourself instead of re-reading."}]}
```

We describe that shape with Pydantic models (`PracticeQuestion`, `PracticeSet`). If the AI's JSON is broken or has the wrong shape, `model_validate_json` raises `ValidationError`, and we **ask again**. After two failures we use the mock questions, which are always valid. The user never sees a crash.

---

## Do it now

### Part A - Add part 2 to `app/study.py`

**Prompt for your AI assistant:**

```text
Add to app/study.py:
1. _mock_summary(text, points): pick `points` real sentences spread evenly through the text,
   without headings or repeats, as "- " bullet lines.
2. make_summary(filename=None, points=5): get the text from the store (first 12000 characters),
   ask the LLM for `points` short bullet points in simple English, return {"summary", "mode"}.
3. Pydantic models PracticeQuestion(question: str min 5 chars, answer: str min 1 char) and
   PracticeSet(questions: list[PracticeQuestion], at least 1).
4. _mock_questions(filename, count) returning valid JSON built from chunk headings.
5. make_practice_questions(filename=None, count=5): ask for JSON only, validate with
   PracticeSet.model_validate_json, retry once with a "your last reply was not valid" note,
   and fall back to the mock questions. Return {"questions": [...], "mode"}.
```

**Reference code** - add this to the **end** of `app/study.py`:

```python
# ---------------------------------------------------------------------------
# 2. Summary
# ---------------------------------------------------------------------------
def _mock_summary(text, points):
    """Offline stand-in summary: evenly spread real sentences, without headings or repeats."""
    sentences = []
    for sentence in _sentences(text.replace("\n", " ")):
        sentence = re.sub(r"^([A-Z][\w ,'-]{1,40}:\s+)+", "", sentence)  # drop "Heading:" at the start
        if len(sentence) > 25 and sentence not in sentences:
            sentences.append(sentence)
    step = max(1, len(sentences) // points)
    chosen = sentences[::step][:points]
    return "\n".join(f"- {s}" for s in chosen)


def make_summary(filename=None, points=5):
    text = store.get_text(filename)
    if not text:
        return {"summary": "Please upload a document first.", "mode": "none"}
    text = text[:12000]  # keep the prompt small (tokens cost money and time)
    prompt = f"Summarise this study material in {points} short bullet points, in simple English:\n\n{text}"
    summary, mode = ask_llm(prompt, temperature=0.3, mock_answer=_mock_summary(text, points))
    return {"summary": summary, "mode": mode}


# ---------------------------------------------------------------------------
# 3. Practice questions (structured JSON output + validation)
# ---------------------------------------------------------------------------
class PracticeQuestion(BaseModel):
    question: str = Field(min_length=5)
    answer: str = Field(min_length=1)


class PracticeSet(BaseModel):
    questions: list[PracticeQuestion] = Field(min_length=1)


def _mock_questions(filename, count):
    questions = []
    for chunk in store.get_chunks(filename):
        heading, _, rest = chunk["text"].partition(":")
        first = _sentences(rest)[:1]
        if first and 2 < len(heading) < 60:
            questions.append({"question": f"What do your notes say about '{heading.strip()}'?", "answer": first[0]})
        if len(questions) == count:
            break
    if not questions:
        questions = [{"question": "What is the main idea of this document?", "answer": _sentences(store.get_text(filename))[0]}]
    return json.dumps({"questions": questions})


def make_practice_questions(filename=None, count=5):
    text = store.get_text(filename)
    if not text:
        return {"questions": [], "mode": "none"}
    prompt = (
        f"Create {count} practice questions with short answers from this study material. "
        'Return ONLY JSON in this shape: {"questions": [{"question": "...", "answer": "..."}]}\n\n'
        + text[:12000]
    )
    mock = _mock_questions(filename, count)
    for _ in range(2):  # try twice, because AI output is sometimes invalid
        raw, mode = ask_llm(prompt, temperature=0.4, json_output=True, mock_answer=mock)
        try:
            practice = PracticeSet.model_validate_json(raw)
            return {"questions": [q.model_dump() for q in practice.questions[:count]], "mode": mode}
        except ValidationError:
            prompt += "\n\nYour last reply was not valid JSON in the required shape. Return ONLY that JSON."
    practice = PracticeSet.model_validate_json(mock)  # last fallback: the mock questions are always valid
    return {"questions": [q.model_dump() for q in practice.questions], "mode": "mock"}
```

### Part B - Add the endpoints to `app/main.py`

**1. Change the study import line** so it imports all three functions:

```python
from app.study import answer_question, make_practice_questions, make_summary
```

(This replaces the old `from app.study import answer_question` line.)

**2. Add the request model** after `AskRequest`:

```python
class StudyRequest(BaseModel):
    filename: str | None = None
    count: int = Field(default=5, ge=1, le=10)
```

**3. Add the endpoints** at the end of the file:

```python
# ---------------------------------------------------------------------------
# Feature 3: summary and practice questions
# ---------------------------------------------------------------------------
def _check_filename(filename):
    if filename and filename not in {d["filename"] for d in store.list_documents()}:
        raise HTTPException(404, f"No document called '{filename}'.")
    if not store.chunks:
        raise HTTPException(400, "Please upload a document first.")


@app.post("/api/summary")
def summary(request: StudyRequest):
    _check_filename(request.filename)
    return make_summary(request.filename, points=request.count)


@app.post("/api/practice-questions")
def practice_questions(request: StudyRequest):
    _check_filename(request.filename)
    return make_practice_questions(request.filename, count=request.count)
```

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
from pydantic import BaseModel, Field

from app import config
from app.documents import DocumentError, chunk_text, extract_text
from app.llm import current_mode
from app.store import store
from app.study import answer_question, make_practice_questions, make_summary

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


# ---------------------------------------------------------------------------
# Request bodies (Pydantic checks the input for us)
# ---------------------------------------------------------------------------
class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=500)


class StudyRequest(BaseModel):
    filename: str | None = None
    count: int = Field(default=5, ge=1, le=10)


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


# ---------------------------------------------------------------------------
# Feature 2: ask questions (RAG)
# ---------------------------------------------------------------------------
@app.post("/api/ask")
def ask(request: AskRequest):
    if not store.chunks:
        raise HTTPException(400, "Please upload a document first.")
    return answer_question(request.question.strip())


# ---------------------------------------------------------------------------
# Feature 3: summary and practice questions
# ---------------------------------------------------------------------------
def _check_filename(filename):
    if filename and filename not in {d["filename"] for d in store.list_documents()}:
        raise HTTPException(404, f"No document called '{filename}'.")
    if not store.chunks:
        raise HTTPException(400, "Please upload a document first.")


@app.post("/api/summary")
def summary(request: StudyRequest):
    _check_filename(request.filename)
    return make_summary(request.filename, points=request.count)


@app.post("/api/practice-questions")
def practice_questions(request: StudyRequest):
    _check_filename(request.filename)
    return make_practice_questions(request.filename, count=request.count)
```

</details>

### Part C - Try it

In `/docs`: upload `sample_files/healthy_study_habits.txt`, then:

- **POST /api/summary** with body `{"count": 5}`
- **POST /api/practice-questions** with body `{"count": 3}`

---

## Check

- [ ] The summary has about 5 bullet points (lines starting with `- `).
- [ ] Practice questions come back as a list of `{"question": ..., "answer": ...}`.
- [ ] `{"filename": "missing.txt"}` gives **404** "No document called 'missing.txt'."
- [ ] `{"count": 50}` gives **422** (the limit is 10).

---

## Review the code

- [ ] Is the AI's JSON **validated** before it is returned?
- [ ] Is there a limit on how much text is sent to the AI?
- [ ] Is there a limit on `count`, so nobody can ask for 10,000 questions and use up your quota?

---

## What just happened?

You used two kinds of AI output: **free text** (summary) and **structured JSON** (questions). Structured output plus validation is how professional apps use LLMs safely inside code.

---

## Try it yourself

1. Add a `difficulty` field (`"easy"`, `"medium"` or `"hard"`) to `PracticeQuestion` using `Literal`, and update the prompt.
2. Ask your assistant to review `make_practice_questions` with prompt E from Lesson 02.

---

## If it does not work

| Problem | Fix |
|---|---|
| Questions are always the mock ones although you have a key | The AI JSON may fail validation. Add `print(raw)` inside the loop for a moment to see what the AI returned, then remove the print. |
| `pydantic_core._pydantic_core.ValidationError` crashes the server | Make sure `model_validate_json` is inside `try` / `except ValidationError`. |

Next: **[Lesson 08 - Step 5: CSV insights and charts](08_STEP_5_CSV_INSIGHTS.md)**
