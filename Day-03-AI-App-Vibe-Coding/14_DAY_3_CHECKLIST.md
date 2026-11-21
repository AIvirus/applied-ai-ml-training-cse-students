# Lesson 14 - Day 3 Checklist

**Time:** 10 minutes

---

## Tick what you can do

### The app works

- [ ] `uvicorn app.main:app --reload` starts without errors.
- [ ] The web page uploads notes, answers questions with sources, summarises, makes practice questions, and analyses a CSV with a chart.
- [ ] `/health` and `/docs` work.
- [ ] `pytest -v` passes.
- [ ] (Optional) OCR and the research agent work.

### You understand it

- [ ] You can draw the architecture and say what each file does (Lesson 01).
- [ ] You can explain the safe vibe coding workflow and its rules (Lesson 02).
- [ ] You can explain how a question becomes an answer: search -> context -> prompt -> LLM -> answer + sources (Lesson 06).
- [ ] You can explain why AI JSON is validated (Lesson 07).
- [ ] You can explain why `textContent` is used instead of `innerHTML` (Lesson 09).
- [ ] You can explain how tests run in mock mode and how you debugged a failure (Lesson 10).
- [ ] You can list the app's known limitations (Lesson 13).

---

## Practice

Open **[practice/WORKBOOK.md](practice/WORKBOOK.md)**, then check **[practice/ANSWERS.md](practice/ANSWERS.md)**.

---

## Prepare for Day 4

Tomorrow you put Study Buddy on **GitHub**, pack it into **Docker**, put it **on the internet**, add **automatic tests on every change**, and learn to **watch its logs**. Then you present it.

Before Day 4:

1. Make sure `pytest -v` passes in `my_study_buddy`.
2. Create a free GitHub account at https://github.com if you do not have one.
3. If possible, install **Docker Desktop** (Day 4 Lesson 04 shows how) - it is a large download.

Go to **[Day 4 - Start here](../Day-04-Deploy-and-Monitor/00_START_HERE.md)**
