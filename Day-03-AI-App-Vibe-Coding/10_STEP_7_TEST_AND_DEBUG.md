# Lesson 10 - Step 7: Test and Debug

**Time:** 30 minutes  |  **Files:** `tests/conftest.py`, `tests/test_app.py`

---

## Goal

By the end of this lesson you can:

- run **automated tests** that check every feature in about 3 seconds,
- test **normal** and **invalid** inputs,
- **debug** with real error messages and verify the fix.

---

## Understand

### Why automated tests?

Clicking through the web page after every change takes minutes, and you forget things. Tests are small programs that **check your program**. On Day 4, GitHub runs them automatically on every change (CI).

A test has three parts:

```python
def test_ask_finds_the_answer_with_source():
    upload("college_library_rules.txt")                                            # 1. ARRANGE
    response = client.post("/api/ask", json={"question": "What is the fine for a late book?"})   # 2. ACT
    assert "5 rupees" in response.json()["answer"]                                 # 3. ASSERT
```

`TestClient` sends requests to the app **without starting a server**.

### Tests run in mock mode

`conftest.py` turns on `MOCK_MODE` before the app loads. So tests:

- never use your API key or quota,
- work without internet,
- always give the same result (real AI answers vary, which would make tests flaky).

### How to debug like a professional

1. **Read the error from the bottom up.** The last line says **what** went wrong (`KeyError: 'answer'`). The lines above (the **traceback**) say **where**: file name and line number.
2. **Reproduce it** with the smallest possible input.
3. **Form a guess**, change **one** thing, run again.
4. With an AI assistant: give it the **full error**, the code of the file in the traceback, and what you expected (prompt C in Lesson 02).
5. **Verify** the fix: run the failing case again **and** all tests, to be sure nothing else broke.

---

## Do it now

### Part A - Create the tests

**Prompt for your AI assistant:**

```text
Write pytest tests for my FastAPI Study Buddy app using fastapi.testclient.TestClient.
In tests/conftest.py, set os.environ["MOCK_MODE"]="true" and GEMINI_API_KEY="" before the app
is imported, and add the project folder to sys.path.
In tests/test_app.py: use an autouse fixture that clears the store before and after each test.
Test: /health, the home page, chunk_text, uploading a .txt from sample_files, rejecting .exe,
empty and >2 MB files, asking a question (answer contains "5 rupees" and the source file),
a not-found question, asking with no documents (400), a too-short question (422),
summary bullets, practice-question shape, unknown filename (404), CSV insights + chart,
and an unknown CSV column (400).
```

**Reference code** - create `tests/conftest.py`:

```python
"""
conftest.py - pytest runs this file first.

We force MOCK MODE for tests, so tests never use your API key, never need the internet,
and always give the same results. This must happen BEFORE the app is imported.
"""

import os
import sys
from pathlib import Path

os.environ["MOCK_MODE"] = "true"
os.environ["GEMINI_API_KEY"] = ""

# Make "import app" work when pytest is started from the project folder
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
```

Create `tests/test_app.py`:

```python
"""
Automated tests for Study Buddy. Run from the project folder with:   pytest -v
Each test checks one behaviour: a normal input AND wrong inputs.
"""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.documents import chunk_text
from app.main import app
from app.store import store

client = TestClient(app)
SAMPLES = Path(__file__).resolve().parents[1] / "sample_files"


@pytest.fixture(autouse=True)
def empty_store():
    """Start every test with no documents."""
    store.clear()
    yield
    store.clear()


def upload(name):
    with open(SAMPLES / name, "rb") as f:
        return client.post("/api/documents", files={"file": (name, f, "text/plain")})


# ---- health and home page -----------------------------------------------------
def test_health_says_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["ai_mode"] == "mock"


def test_home_page_loads():
    response = client.get("/")
    assert response.status_code == 200
    assert "Study Buddy" in response.text


# ---- chunking -------------------------------------------------------------------
def test_chunk_text_keeps_pieces_small():
    text = "\n".join(f"Sentence number {i} is here." for i in range(100))
    chunks = chunk_text(text, chunk_size=200)
    assert len(chunks) > 5
    assert all(len(c) <= 260 for c in chunks)


# ---- documents ------------------------------------------------------------------
def test_upload_text_document():
    response = upload("college_library_rules.txt")
    assert response.status_code == 200
    assert response.json()["chunks"] >= 3
    assert client.get("/api/documents").json()["documents"][0]["filename"] == "college_library_rules.txt"


def test_upload_rejects_wrong_file_type():
    response = client.post("/api/documents", files={"file": ("virus.exe", b"MZ...", "application/octet-stream")})
    assert response.status_code == 400
    assert "not allowed" in response.json()["detail"]


def test_upload_rejects_empty_file():
    response = client.post("/api/documents", files={"file": ("empty.txt", b"", "text/plain")})
    assert response.status_code == 400


def test_upload_rejects_too_large_file():
    big = b"a" * (3 * 1024 * 1024)
    response = client.post("/api/documents", files={"file": ("big.txt", big, "text/plain")})
    assert response.status_code == 413


# ---- ask questions --------------------------------------------------------------
def test_ask_finds_the_answer_with_source():
    upload("college_library_rules.txt")
    response = client.post("/api/ask", json={"question": "What is the fine for a late book?"})
    data = response.json()
    assert response.status_code == 200
    assert "5 rupees" in data["answer"]
    assert data["sources"][0]["source"] == "college_library_rules.txt"


def test_ask_says_not_found_for_unrelated_question():
    upload("college_library_rules.txt")
    data = client.post("/api/ask", json={"question": "Who won the cricket world cup in 2011?"}).json()
    assert "could not find" in data["answer"].lower()


def test_ask_without_documents_gives_clear_error():
    response = client.post("/api/ask", json={"question": "What is the fine?"})
    assert response.status_code == 400
    assert "upload" in response.json()["detail"].lower()


def test_ask_rejects_too_short_question():
    upload("college_library_rules.txt")
    response = client.post("/api/ask", json={"question": "a"})
    assert response.status_code == 422


# ---- summary and practice questions ---------------------------------------------
def test_summary_returns_bullets():
    upload("healthy_study_habits.txt")
    data = client.post("/api/summary", json={"count": 3}).json()
    assert data["summary"].count("- ") >= 2


def test_practice_questions_have_valid_shape():
    upload("healthy_study_habits.txt")
    data = client.post("/api/practice-questions", json={"count": 3}).json()
    assert 1 <= len(data["questions"]) <= 3
    assert all(q["question"] and q["answer"] for q in data["questions"])


def test_practice_questions_unknown_file_gives_404():
    upload("healthy_study_habits.txt")
    response = client.post("/api/practice-questions", json={"filename": "missing.txt"})
    assert response.status_code == 404


# ---- CSV ------------------------------------------------------------------------
def test_csv_analysis_returns_insights_and_chart():
    with open(SAMPLES / "student_marks.csv", "rb") as f:
        response = client.post("/api/csv", files={"file": ("student_marks.csv", f, "text/csv")})
    data = response.json()
    assert response.status_code == 200
    assert data["rows"] > 0
    assert any("strongest relationship" in i for i in data["insights"])
    assert len(data["chart_png_base64"]) > 1000


def test_csv_with_unknown_column_gives_error():
    with open(SAMPLES / "student_marks.csv", "rb") as f:
        response = client.post("/api/csv", files={"file": ("m.csv", f, "text/csv")}, data={"column": "height"})
    assert response.status_code == 400
```

### Part B - Run the tests

Stop the server with **Ctrl + C** (or use your second terminal). In `my_study_buddy`:

```powershell
pytest -v
```

### Part C - A debugging exercise

Let us break something on purpose and fix it like a professional.

1. Open `app/store.py`. In the `search` function, find the last line and change `scores[i] > 0` to `scores[i] > 1`:

```python
        return [{**self.chunks[i], "score": round(float(scores[i]), 3)} for i in best if scores[i] > 1]
```

2. Save and run `pytest -v`. You see `1 failed, 15 passed`.
3. Read the **first** failure from the bottom up. You will see something like:

```text
>       assert "5 rupees" in data["answer"]
E       AssertionError: assert '5 rupees' in 'I could not find this in your documents.'
tests/test_app.py:85: AssertionError
```

4. Investigate like an engineer: **why did only one test fail?** Only `test_ask_finds_the_answer_with_source` needs the search to **find** something. The "not found" test still passes (nothing is found, which is what it expects), and the summary, CSV and upload tests do not search at all. This tells you the bug is in **searching**, so you look in `store.py`. It also shows a lesson about tests: a bug can hide if no test checks that exact behaviour.
5. Ask your AI assistant with prompt C from Lesson 02: paste the error and the code of `store.py` and `study.py`. Does it find the cause? (Similarity scores are between 0 and 1, so `> 1` removes every result.)
6. Fix it (change it back to `> 0`), then run `pytest -v` and check that **all** tests pass again.

---

## Check

- [ ] `pytest -v` ends with `16 passed` (the number may differ slightly if you added your own tests).
- [ ] You broke the code, saw failing tests, fixed it, and saw all tests pass again.
- [ ] You can explain what `assert`, `TestClient` and `conftest.py` do.

---

## Review the code

- [ ] Does every feature have at least one **normal** test and one **bad input** test?
- [ ] Do tests use mock mode, so they are free and repeatable?

---

## What just happened?

You built a **safety net**. From now on, after every change (yours or the AI's), run `pytest`. If all tests pass, you know the main features still work. Professional teams do not merge code without passing tests.

---

## Try it yourself

1. Write a test that uploads `solar_system_notes.txt` and asks "Which planet has rings?". What should the answer contain?
2. Ask your AI assistant to write a test for uploading a `.md` file. Read it before you run it. Does it really test what it says?
3. Run only one test: `pytest -v -k ask_finds`.

---

## If it does not work

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'app'` | Run `pytest` from the `my_study_buddy` folder, and check `tests/conftest.py` exists. |
| `FileNotFoundError: ... sample_files/...` | Copy `sample_files` into your project (Lesson 03, Step 3). |
| Tests pass on your computer but use your real key | `conftest.py` must set `MOCK_MODE` **before** importing the app. Check its content. |
| `fixture 'empty_store' not found` | The fixture must be in the same file (or in `conftest.py`) and have `@pytest.fixture(autouse=True)`. |

Next: **[Lesson 11 - Optional: OCR](11_OPTIONAL_OCR.md)** or skip to **[Lesson 13 - Review](13_REVIEW_SECURITY_AND_QUALITY.md)**
