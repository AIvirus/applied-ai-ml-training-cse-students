# Lesson 01 - The Project and the Plan

**Time:** 25 minutes  |  **You need:** nothing, just read and think

Good engineers **plan before they code**. With AI assistants this matters even more: a clear plan gives clear prompts, and clear prompts give good code.

---

## Goal

By the end of this lesson you can explain:

- the **problem** Study Buddy solves,
- what a **Minimum Viable Product (MVP)** is and what is in ours,
- the **architecture**: which parts the app has and how they talk to each other,
- the **API endpoints** we will build.

---

## Understand

### 1. The problem statement

> Students have many notes, PDFs and data files. Finding one fact, revising quickly and testing themselves takes a long time. General chatbots do not know the student's own notes and may invent answers.

**Our solution:** a web app where a student uploads **their own** material and gets answers **grounded in that material**, with sources, plus summaries, practice questions and simple data insights.

### 2. Minimum Viable Product (MVP)

An **MVP** is the **smallest version** of a product that is still useful. You build it first, test it with real users, then improve it. It stops you from spending weeks on features nobody needs.

| Priority | Feature | Why |
|---|---|---|
| **Must have (MVP)** | Upload notes (.txt, .md, .pdf) | Nothing works without documents |
| **Must have (MVP)** | Ask questions with answers from the notes + sources | The main value |
| **Must have (MVP)** | Summary and practice questions | Revision |
| **Must have (MVP)** | CSV insights and a chart | Data analysis (Day 1 skills) |
| **Must have (MVP)** | Mock mode when there is no API key | The app must always work in class |
| **Should have** | A simple web page | Normal users do not use API docs |
| **Could have (extension)** | OCR for photos of notes | Useful, but needs extra software |
| **Could have (extension)** | Research agent | Shows agentic AI |
| **Will not have (today)** | User accounts, database, saving forever | Too big for one day |

### 3. The architecture

```text
   BROWSER (the student)
   index.html + style.css + app.js
           |
           |  HTTP requests with JSON or files   (fetch)
           v
   +-------------------------------------------------------------+
   |  FASTAPI BACKEND  (app/main.py)                             |
   |  checks inputs, sends each request to the right module      |
   |                                                             |
   |   documents.py  -> read .txt/.md/.pdf, cut into chunks      |
   |   store.py      -> keep chunks in memory, search (TF-IDF)   |
   |   study.py      -> answer questions (RAG), summary,         |
   |                    practice questions (JSON + validation)   |
   |   csv_tools.py  -> pandas insights + matplotlib chart       |
   |   ocr.py        -> (optional) text from images              |
   |   agent.py      -> (optional) tool-using research agent     |
   |   llm.py        -> talks to Gemini, or MOCK MODE            |
   |   config.py     -> settings from .env                       |
   +-------------------------------------------------------------+
           |
           |  HTTPS (only from llm.py)
           v
   GOOGLE GEMINI API  (the LLM)
```

**Why this design?**

- **One job per file.** Easy to understand, test and change. If PDF reading breaks, you look in `documents.py`.
- **Only `llm.py` talks to the AI.** Changing the AI provider later means changing one file.
- **Mock mode in one place.** If the API fails, `llm.py` returns a prepared answer, so every feature still works.
- **The browser never sees the API key.** The key stays on the server.

### 4. The API endpoints

An **endpoint** is one address of the API that does one job.

| Method | Address | What it does |
|---|---|---|
| GET | `/` | The web page |
| GET | `/health` | "Are you alive?" check (for monitoring on Day 4) |
| POST | `/api/documents` | Upload a document |
| GET | `/api/documents` | List uploaded documents |
| DELETE | `/api/documents` | Remove all documents |
| POST | `/api/ask` | Ask a question about the documents |
| POST | `/api/summary` | Summarise the documents |
| POST | `/api/practice-questions` | Make practice questions |
| POST | `/api/csv` | Analyse a CSV file and draw a chart |
| POST | `/api/ocr` | (optional) Read text from an image |
| POST | `/api/agent` | (optional) Run the research agent |

### 5. Technology choices

| Part | Choice | Why |
|---|---|---|
| Backend | **FastAPI** (Python) | Simple, fast, builds API documentation for free at `/docs` |
| Server | **uvicorn** | Runs FastAPI apps |
| AI model | **Google Gemini** via `google-genai` | Free tier, good quality; mock mode as backup |
| Search | **TF-IDF** (scikit-learn) | Free, offline, simple. Can be upgraded to embeddings later (Day 2 Lesson 08). |
| Data | **pandas** + **matplotlib** | From Day 1 |
| Validation | **Pydantic** | Checks requests and AI JSON output |
| Frontend | Plain **HTML, CSS, JavaScript** | No extra tools to install |
| Tests | **pytest** | Standard Python testing tool |

---

## Do it now

On paper or in a text file, answer these planning questions **for Study Buddy** (5 minutes):

1. Who is the user?
2. What is the single most important feature?
3. What could go wrong? (Think: no internet, wrong file type, huge file, AI gives a wrong answer, someone uploads a file with hidden instructions.)
4. How will we know each feature works?

---

## Check

Compare with these sample answers:

1. A student revising for exams.
2. Asking questions about their own notes and getting correct answers with sources.
3. No internet or no key -> mock mode. Wrong type or too big -> clear error message (400 or 413). Wrong AI answer -> show sources so the student can check. Hidden instructions -> treat documents as data, not instructions (Day 2 Lesson 10).
4. Try it in the browser and in `/docs`, and write automated tests (Lesson 10).

---

## What just happened?

You did what a **software architect** does: defined the problem, cut it down to an MVP, split the system into parts with clear jobs, and planned how to test it. In the next lesson you will hand this plan to an AI coding assistant - and you will understand everything it produces, because you designed it.

---

## Try it yourself

1. Add one more "could have" feature you would like (for example "flashcards"). Which file would it go in?
2. Why is it a bad idea to call the Gemini API directly from `app.js` in the browser? (Hint: what would every visitor be able to see?)

---

## If it does not work

| Problem | Fix |
|---|---|
| "The diagram is confusing" | Follow one request: the student types a question -> `app.js` sends it to `/api/ask` -> `main.py` checks it -> `study.py` asks `store.py` for matching chunks -> `llm.py` asks Gemini -> the answer goes back the same way. |

Next: **[Lesson 02 - Vibe coding the right way](02_VIBE_CODING_THE_RIGHT_WAY.md)**
