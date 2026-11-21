# Day 3 - Build an AI Application with Vibe Coding

**Goal of the day:** build **Study Buddy**, a working AI learning and research assistant, feature by feature, with the help of an AI coding assistant - and understand, run and test every part of it.

**Before you start:** finish Day 1 Lesson 02 (setup) and Day 2 Lessons 06 to 08 (API key, prompts, RAG). No API key? The app has a **mock mode** and works without one.

---

## What you will build

**Study Buddy** is a website where a student can:

1. **Upload notes** (.txt, .md or .pdf).
2. **Ask questions** and get answers **from their own notes**, with sources (RAG).
3. Get a **summary** and **practice questions** with answers.
4. Upload a **CSV** file and get **insights and a chart**.
5. *(Optional)* Read text from a **photo** of notes (OCR).
6. *(Optional)* Ask a small **research agent** to do a multi-step task.

---

## Your plan for today (do these in order)

| # | Lesson | What you build | Time |
|---|---|---|---|
| 01 | [The project and the plan](01_THE_PROJECT_AND_THE_PLAN.md) | Problem, MVP, architecture | 25 min |
| 02 | [Vibe coding the right way](02_VIBE_CODING_THE_RIGHT_WAY.md) | Set up an AI assistant, learn the safe workflow | 30 min |
| 03 | [Set up the project](03_SET_UP_THE_PROJECT.md) | Folders, settings, `.env` | 20 min |
| 04 | [Step 1 - First API and health check](04_STEP_1_FIRST_API_AND_HEALTH.md) | `config.py`, `llm.py`, `main.py`, `/health` | 30 min |
| 05 | [Step 2 - Upload and chunk documents](05_STEP_2_UPLOAD_DOCUMENTS.md) | `documents.py`, `store.py`, upload API | 35 min |
| 06 | [Step 3 - Ask questions with RAG](06_STEP_3_ASK_QUESTIONS_RAG.md) | `study.py` part 1, `/api/ask` | 30 min |
| -- | **Lunch break** | | 60 min |
| 07 | [Step 4 - Summary and practice questions](07_STEP_4_SUMMARY_AND_PRACTICE.md) | `study.py` part 2, JSON validation | 25 min |
| 08 | [Step 5 - CSV insights and charts](08_STEP_5_CSV_INSIGHTS.md) | `csv_tools.py`, `/api/csv` | 25 min |
| 09 | [Step 6 - The web page](09_STEP_6_THE_WEB_PAGE.md) | HTML, CSS, JavaScript | 25 min |
| 10 | [Step 7 - Test and debug](10_STEP_7_TEST_AND_DEBUG.md) | Automated tests, debugging real errors | 30 min |
| 11 | [Optional - OCR](11_OPTIONAL_OCR.md) | Read text from images | 15 min |
| 12 | [Optional - Research agent](12_OPTIONAL_RESEARCH_AGENT.md) | A tool-using agent | 15 min |
| 13 | [Review: keys, inputs, errors and AI quality](13_REVIEW_SECURITY_AND_QUALITY.md) | A professional review | 15 min |
| 14 | [Day 3 checklist](14_DAY_3_CHECKLIST.md) | Check everything | 10 min |

Morning (10:00 AM to 1:20 PM): lessons 01 to 06. Afternoon (2:20 PM to 4:40 PM): lessons 07 to 14. Lessons 11 and 12 are extensions - do them if you have time.

---

## What is in this folder?

```text
Day-03-AI-App-Vibe-Coding/
|-- 00_START_HERE.md            you are here
|-- 01_ ... 14_ lessons         read and do these in order
|-- my_study_buddy/             YOU create this in Lesson 03 - your own project
|-- study_buddy_lab/            the FINISHED project (answer key) - compare when stuck
|   |-- app/                    the Python code and the web page
|   |-- tests/                  automated tests
|   |-- sample_files/           notes and a CSV to try the app with
|   |-- requirements.txt, .env.example, Dockerfile, compose.yaml, .github/   (used on Day 4)
|   `-- README.md
`-- practice/
    |-- WORKBOOK.md
    `-- ANSWERS.md
```

### `my_study_buddy/` and `study_buddy_lab/` - important

- **`my_study_buddy/`** is **your** project. You build it step by step with your AI assistant.
- **`study_buddy_lab/`** is the **finished answer key**. Every lesson also shows the reference code, so you can compare the AI's code with it, or type it yourself if you have no AI assistant.
- Do not just copy the whole lab folder. The skill you learn today is **building, reading, testing and fixing** software with AI help.

Want to see the finished app first? Follow [study_buddy_lab/README.md](study_buddy_lab/README.md) (5 minutes).

---

Start with **[Lesson 01 - The project and the plan](01_THE_PROJECT_AND_THE_PLAN.md)**
