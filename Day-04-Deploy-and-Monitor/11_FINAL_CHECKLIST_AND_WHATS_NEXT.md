# Lesson 11 - Final Checklist and What's Next

**Time:** 10 minutes

Congratulations. In four days you went from "what is AI?" to a tested, deployed, monitored AI application.

---

## Final checklist

### Day 4 skills

- [ ] Finished and tested the project: automated, manual and AI-quality checks (01)
- [ ] Wrote a README whose commands really work (01)
- [ ] Git: init, status, add, commit, log, diff, restore; `.env` never committed (02)
- [ ] GitHub: push, branch, pull request, review, merge, pull, clone (03)
- [ ] Docker: image vs container vs VM; build, run, port mapping, env vars, logs (04, 05)
- [ ] Docker Compose: what it is for; up and down (06)
- [ ] Deployed to Render with environment variables and a health check (07)
- [ ] CI with GitHub Actions; a failing check blocked a bad change; deploy after CI (08)
- [ ] Read app and deploy logs, used `/health`, set up uptime monitoring, fixed an AI API error (09)
- [ ] Presented the project and answered questions (10)

### The whole course

- [ ] Day 1 - AI, ML and data science foundations: [checklist](../Day-01-AI-ML-Foundations/09_DAY_1_CHECKLIST.md)
- [ ] Day 2 - Deep learning and modern AI domains: [checklist](../Day-02-Modern-AI-Domains/11_DAY_2_CHECKLIST.md)
- [ ] Day 3 - Building an AI app with vibe coding: [checklist](../Day-03-AI-App-Vibe-Coding/14_DAY_3_CHECKLIST.md)
- [ ] Day 4 - this page

---

## Practice

Open **[practice/WORKBOOK.md](practice/WORKBOOK.md)**, then check **[practice/ANSWERS.md](practice/ANSWERS.md)**.

---

## What's next? Ideas to keep growing

### Improve Study Buddy

| Idea | You will learn |
|---|---|
| Replace TF-IDF with **Gemini embeddings** and a vector database (Chroma, or PostgreSQL with pgvector) | Real semantic search (Day 2 Lesson 08) |
| Save documents in a **database** | Persistence, SQL |
| Add **user accounts** so each student has private documents | Authentication, security |
| **Stream** the AI answer word by word | Streaming APIs, better user experience |
| Add an **evaluation suite** of 20 questions with expected answers, run in CI | AI evaluation (Day 2 Lesson 10) |
| **Flashcards** with spaced repetition | Product thinking |
| Support **Hindi or your regional language** | Multilingual AI |

### Learn more

| Area | Next steps |
|---|---|
| Machine learning | Kaggle "Intro to Machine Learning" and competitions; the scikit-learn user guide |
| Deep learning | PyTorch tutorials; fast.ai "Practical Deep Learning for Coders" |
| LLM apps | The Gemini API docs (ai.google.dev); build a RAG app on your college syllabus |
| Agents | Build an MCP server for one tool; try an agent framework (LangGraph, Google ADK, OpenAI Agents SDK) |
| MLOps and deployment | Docker deeper, Kubernetes basics, model monitoring |
| Responsible AI | India's DPDP Act basics; the EU AI Act overview; bias and fairness toolkits |

### Build your portfolio

- Keep `study-buddy` public on GitHub with a good README, a CI badge and the live link.
- Write a short post (LinkedIn or a blog) about what you built and **one thing you learned from a bug**.
- Build one more small project on your own idea, using the same workflow: plan -> small prompts -> read -> test -> commit -> CI -> deploy -> monitor.

---

Thank you for learning with this course. Keep building - and keep checking what the AI writes.
