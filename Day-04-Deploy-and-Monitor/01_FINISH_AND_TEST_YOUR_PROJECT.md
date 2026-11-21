# Lesson 01 - Finish and Test Your Project

**Time:** 40 minutes  |  **Folder:** `Day-03-AI-App-Vibe-Coding/my_study_buddy`

---

## Goal

By the end of this lesson:

- your priority features are complete and tested,
- you have tested the web page **and** the API, with normal and bad inputs,
- you have checked the quality of the AI answers,
- your project has a clear `README.md`.

---

## Understand

### Why finish before deploying?

Deploying a broken app just puts a broken app on the internet. Professional teams have a **definition of done**: the feature works, has tests, handles errors, and is documented.

### Three kinds of testing you do today

| Kind | Who checks | Example |
|---|---|---|
| **Automated tests** | `pytest` | 16 tests in `tests/test_app.py` |
| **Manual UI testing** | You, in the browser | Click every button with good and bad files |
| **AI output checks** | You, with known answers | 5 questions whose correct answers you know |

### What a README is

`README.md` is the **front page** of your project on GitHub. A good README answers: What is it? How do I run it? How do I test it? What are its limits? Recruiters and teammates read it first.

---

## Do it now

### Step 1 - Run the automated tests

Open a terminal, activate `.venv`, and go to your project:

```powershell
cd Day-03-AI-App-Vibe-Coding\my_study_buddy
```

```powershell
pytest -v
```

All tests must pass. If not, fix them first (Day 3 Lesson 10).

### Step 2 - Test the web page by hand

Start the app:

```powershell
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000 and fill in this table (copy it into a file called `TESTING.md` in your project if you like):

| # | Action | Expected | Result |
|---|---|---|---|
| 1 | Upload `sample_files/college_library_rules.txt` | Shown in the list | |
| 2 | Upload a `.docx` or `.png` in section 1 | Red error "not allowed" | |
| 3 | Ask "How many books can I borrow?" | 4 books, with source | |
| 4 | Ask "What is the capital of France?" | "I could not find this..." | |
| 5 | Click "Summarise all notes" | Bullet points | |
| 6 | Click "Make 5 practice questions" | Questions with answers | |
| 7 | Upload `sample_files/student_marks.csv` | Facts, explanation, chart | |
| 8 | CSV with column `nothing` | Red error "not in the file" | |
| 9 | Stop the server, click Ask | "Failed to fetch" or "Cannot reach the server" | |

### Step 3 - Test the API directly

Open http://127.0.0.1:8000/docs and try **GET /health**, **POST /api/ask** with `{"question": ""}` (expect **422**) and **POST /api/summary** with `{"count": 99}` (expect **422**).

### Step 4 - Check the quality of AI answers

With a real API key, ask 5 questions whose answers you know from `sample_files`. For each one write: correct / partly correct / wrong, and whether the source was right. If an answer is wrong, look at the **sources**: was the right chunk retrieved? If not, the problem is **retrieval**, not the AI.

### Step 5 - Handle common failures

Check that these situations give a clear message and **no crash**:

- No API key or a wrong key -> mock answers, a warning in the log.
- The free AI limit is reached (`429`) -> mock answers, a warning in the log.
- Tesseract missing -> OCR returns 503 (if you did Lesson 11 of Day 3).

### Step 6 - Write your README

Ask your AI assistant:

```text
Write a README.md for my project "Study Buddy". Sections: what it does (6 features), a simple
architecture diagram in text, how to run it locally on Windows and macOS (venv, pip install -r
requirements.txt, copy .env.example to .env, uvicorn app.main:app --reload), how to run tests
(pytest -v, mock mode), settings table (GEMINI_API_KEY, GEMINI_MODEL, MOCK_MODE, MAX_UPLOAD_MB,
LOG_LEVEL), known limitations, and a "Live demo" placeholder link. Keep it short and clear.
```

Compare with `Day-03-AI-App-Vibe-Coding/study_buddy_lab/README.md`. Save yours as `README.md` in `my_study_buddy`. **Read it:** every command in it must really work.

---

## Check

- [ ] `pytest -v` passes.
- [ ] All 9 manual tests give the expected result.
- [ ] You checked 5 AI answers and know which (if any) were wrong and why.
- [ ] `my_study_buddy/README.md` exists and its commands work.

---

## What just happened?

You applied a **definition of done**: tested automatically, tested by hand, checked the AI, and documented. Now the project is ready to be shared and deployed.

---

## Try it yourself

1. Add one more automated test for a bug you found during manual testing.
2. Ask a classmate to follow your README on their computer. Fix anything they get stuck on.

---

## If it does not work

| Problem | Fix |
|---|---|
| Tests pass but the page fails | Tests do not cover the frontend. Press **F12 -> Console** in the browser to see JavaScript errors. |
| Real AI answers are wrong but sources are right | Improve the prompt in `QA_SYSTEM`, lower the temperature, or send more chunks (`top_k`). |
| Sources are wrong | Retrieval problem: try more specific questions, smaller chunks, or (advanced) embeddings. |

Next: **[Lesson 02 - Git basics](02_GIT_BASICS.md)**
