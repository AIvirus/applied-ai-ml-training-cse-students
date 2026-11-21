# Applied AI and Machine Learning - Self-Learning Course

A 4-day, step-by-step course for Computer Science and Engineering students.
You do **not** need any AI or Machine Learning knowledge to start. If you can switch on a computer and type, you can follow it.

Open **[00_START_HERE.md](00_START_HERE.md)** first.

---

## The 4 days

| Day | Folder | Theme | What you will be able to do |
|---|---|---|---|
| 1 | [Day-01-AI-ML-Foundations](Day-01-AI-ML-Foundations/00_START_HERE.md) | AI, Machine Learning and Data Science foundations | Explain AI, ML and Deep Learning. Explore, clean and chart data. Train and test your first ML models. |
| 2 | [Day-02-Modern-AI-Domains](Day-02-Modern-AI-Domains/00_START_HERE.md) | Deep Learning and modern AI domains | Understand neural networks, NLP, Computer Vision, Generative AI, LLMs, RAG and AI agents. Call a real LLM from Python. |
| 3 | [Day-03-AI-App-Vibe-Coding](Day-03-AI-App-Vibe-Coding/00_START_HERE.md) | Build an AI application with an AI coding assistant | Build "Study Buddy", an AI learning and research assistant, feature by feature, and test it. |
| 4 | [Day-04-Deploy-and-Monitor](Day-04-Deploy-and-Monitor/00_START_HERE.md) | GitHub, Docker, deployment and monitoring | Put your project on GitHub, pack it in Docker, put it on the internet, add automatic checks and watch its logs. |

---

## What is in this folder?

```text
Applied_AI_ML_Training_Proposal_CSE_Students/
|-- README.md                  you are here
|-- 00_START_HERE.md           read this first: how the course works + one-time setup
|-- requirements.txt           list of Python packages for all 4 days
|-- .env.example               template for your private API key
|-- .gitignore                 tells Git which files must never be uploaded
|-- Day-01-AI-ML-Foundations/  lessons + notebooks + data for Day 1
|-- Day-02-Modern-AI-Domains/  lessons + notebooks + data for Day 2
|-- Day-03-AI-App-Vibe-Coding/ lessons + finished project (answer key) for Day 3
|-- Day-04-Deploy-and-Monitor/ lessons for Day 4
|-- references/                glossary, commands cheat sheet, common errors
`-- docs/                      the original training proposal
```

## Quick setup (details in 00_START_HERE.md and Day 1 Lesson 02)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

On macOS or Linux use `source .venv/bin/activate` instead of the second line.
