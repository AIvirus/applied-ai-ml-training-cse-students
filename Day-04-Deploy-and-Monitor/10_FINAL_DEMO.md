# Lesson 10 - Final Demonstration

**Time:** 30 minutes to prepare, 5 to 7 minutes to present

---

## Goal

You present your project clearly: the **problem**, the **architecture**, the **AI concepts** used, a **live demo** of the workflow, your **testing approach**, the **deployed result**, and honest **limitations**.

---

## Understand

A good technical demo is not "look at all my code". It is a **story**:

> "Here is a real problem. Here is how my app solves it. Here is how it works inside. Here is proof that it works and is tested. Here is what I would improve."

Evaluators usually look at four things (from the course plan):

| Area | Weight | What they look for |
|---|---|---|
| AI and domain understanding | 30% | Correct use of words: RAG, embeddings/TF-IDF, LLM, prompt, validation, agent |
| Practical participation | 20% | You did the exercises and notebooks |
| Project implementation | 30% | Working features, integration, testing, deployment |
| Explanation and presentation | 20% | You can explain design choices, limitations and results |

---

## Do it now

### Step 1 - Prepare 6 slides (or one page of notes)

Use any tool (Google Slides, PowerPoint, or just a Markdown file). Keep text short.

| Slide | Content | Time |
|---|---|---|
| 1. Problem | Who is the user, what problem, why it matters | 30 s |
| 2. Solution | Study Buddy's 4 core features (+ extensions you built) | 30 s |
| 3. Architecture | The diagram from Day 3 Lesson 01: browser -> FastAPI -> modules -> Gemini | 1 min |
| 4. AI concepts | RAG (chunking, retrieval, grounded prompt, sources), structured output with Pydantic, mock mode, (agent / OCR) | 1 min |
| 5. Live demo | (switch to the browser) | 2 min |
| 6. Quality and delivery | Tests (how many, what they cover), CI on GitHub, Docker, Render, logs and `/health`, limitations, next steps | 1 min |

### Step 2 - Plan the live demo (2 minutes)

Practise this exact path on your **live** URL:

1. Open the site - show the status line and `/health`.
2. Upload `college_library_rules.txt`.
3. Ask "What is the fine for returning a book late?" - open **Sources used** and point to the source.
4. Ask something not in the notes - show "I could not find this".
5. Click **Make 5 practice questions**.
6. Upload `student_marks.csv` - show the facts and chart.
7. Show the GitHub **Actions** tab with green ticks, and Render's **Logs** with your requests.

**Have a backup.** Free services sleep and networks fail. Open the site 2 minutes before you present (to wake it), and have the app running locally too (`uvicorn app.main:app`) in case the internet fails. Set `MOCK_MODE=true` locally if the AI quota is a risk.

### Step 3 - Prepare for questions

Be ready to answer:

1. Why did you use RAG instead of just asking the LLM?
2. How do you stop the AI from inventing answers?
3. Why is the API key not in your GitHub repository? Where is it?
4. What happens if the AI service is down?
5. What do your tests check? Why do they run in mock mode?
6. Which part did the AI assistant write, and how did you check it?
7. What would you change to support 1,000 students?
8. What is one bug you found and how did you fix it?

Sample short answers:

1. The LLM does not know my documents. RAG retrieves the right chunks and the prompt tells the model to answer only from them, with sources.
2. The system instruction says "only from the context, otherwise say not found", low temperature, and sources so the user can check.
3. In `.env` locally (ignored by Git) and in Render's environment settings. Never in code or the image.
4. `llm.py` catches the error, logs a warning and returns a mock answer. The app keeps working.
5. 16 tests: uploads (normal and bad), questions (found and not found), validation errors, summary, practice questions, CSV. Mock mode makes them free, offline and repeatable.
6. Be honest: for example "the assistant drafted `csv_tools.py`; I read it, compared it with the reference, tested bad columns, and fixed X."
7. User accounts and per-user storage in a database, a vector database with embeddings, more instances behind a load balancer, rate limits, caching, a paid AI plan, monitoring with alerts.
8. Your own story.

### Step 4 - Rehearse once with a timer

Present to a friend or record yourself. Stay within 7 minutes.

---

## Check

- [ ] 6 slides or notes are ready.
- [ ] You practised the demo path on the live URL.
- [ ] You have a local backup ready.
- [ ] You can answer the 8 questions in your own words.

---

## What just happened?

You turned a project into a **presentation**: problem -> solution -> architecture -> proof -> limits. This is the same structure used in job interviews, hackathons and project reviews.

---

## If it does not work (on demo day)

| Problem | Fix |
|---|---|
| The live site takes a minute to load | It was asleep. Talk about the architecture slide while it wakes up - or open it 2 minutes early. |
| AI answers are mock on the live site | Quota or key problem. Say so honestly, show the log line, and explain the fallback design - that is a strength. |
| No internet | Use your local backup in mock mode. |

Next: **[Lesson 11 - Final checklist and what's next](11_FINAL_CHECKLIST_AND_WHATS_NEXT.md)**
