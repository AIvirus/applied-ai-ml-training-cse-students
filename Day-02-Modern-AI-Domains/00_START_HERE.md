# Day 2 - Deep Learning and Modern AI Domains

**Goal of the day:** understand the main areas of modern AI - neural networks, language (NLP), vision (Computer Vision), Generative AI and Large Language Models (LLMs), RAG and AI agents - and see each one working in Python. You will also call a real AI model from your own code.

**Before you start:** finish Day 1 Lesson 02 (setup). You use the same `.venv`.

---

## Your plan for today (do these in order)

| # | Lesson (read) | Notebook (do) | Time |
|---|---|---|---|
| 01 | [Deep Learning and neural networks](01_DEEP_LEARNING.md) | `01_Neural_Networks.ipynb` | 40 min |
| 02 | [Natural Language Processing (NLP)](02_NLP.md) | `02_NLP_Text_Processing.ipynb` | 40 min |
| 03 | [Computer Vision](03_COMPUTER_VISION.md) | `03_Computer_Vision.ipynb` | 35 min |
| 04 | [Other AI domains](04_OTHER_AI_DOMAINS.md) | `04_Other_AI_Domains.ipynb` | 25 min |
| 05 | [Generative AI and LLMs](05_GENERATIVE_AI_AND_LLMS.md) | `05_How_Generative_AI_Works.ipynb` | 40 min |
| -- | **Lunch break** | | 60 min |
| 06 | [Get your free AI API key](06_GET_YOUR_FREE_AI_KEY.md) | - | 15 min |
| 07 | [Prompts and model APIs](07_PROMPTS_AND_MODEL_APIS.md) | `06_Talk_to_an_LLM.ipynb` | 35 min |
| 08 | [Embeddings, semantic search and RAG](08_EMBEDDINGS_AND_RAG.md) | `07_Embeddings_and_RAG.ipynb` | 40 min |
| 09 | [Agentic AI](09_AGENTIC_AI.md) | `08_Build_a_Small_Agent.ipynb` | 30 min |
| 10 | [Responsible and secure AI](10_RESPONSIBLE_AND_SECURE_AI.md) | `09_Responsible_AI.ipynb` | 20 min |
| 11 | [Day 2 checklist and practice](11_DAY_2_CHECKLIST.md) | `practice/WORKBOOK.md` | 10 min |

Morning (10:00 AM to 1:20 PM): lessons 01 to 05. Afternoon (2:20 PM to 4:40 PM): lessons 06 to 11.

---

## What is in this folder?

```text
Day-02-Modern-AI-Domains/
|-- 00_START_HERE.md            you are here
|-- 01_ ... 11_ lessons         read these in order
|-- check_ai_key.py             tests your API key (Lesson 06)
|-- notebooks/
|   |-- ai_helper.py            small helper the notebooks use to talk to the AI (do not change)
|   |-- 01_Neural_Networks.ipynb
|   |-- 02_NLP_Text_Processing.ipynb
|   |-- 03_Computer_Vision.ipynb
|   |-- 04_Other_AI_Domains.ipynb
|   |-- 05_How_Generative_AI_Works.ipynb
|   |-- 06_Talk_to_an_LLM.ipynb
|   |-- 07_Embeddings_and_RAG.ipynb
|   |-- 08_Build_a_Small_Agent.ipynb
|   `-- 09_Responsible_AI.ipynb
|-- data/
|   |-- reviews.csv             60 short product reviews (positive / negative)
|   `-- documents/              3 small text documents for search and RAG
`-- practice/
    |-- WORKBOOK.md
    `-- ANSWERS.md
```

---

## About the internet and the API key

- Notebooks 01 to 05 need **no API key**. Notebook 02 downloads some small language files once (about 50 MB) the first time.
- Notebooks 06 to 09 use a real AI model (Google Gemini). Lesson 06 shows how to get a **free** key.
- **No key? No problem.** The notebooks switch to **MOCK MODE** and still run, with pretend answers. You will see `[MOCK MODE]` in the output.
- **Using Google Colab?** Upload the notebook, `ai_helper.py`, and the files it needs from `data/` (for example `reviews.csv` and the 3 `.txt` documents) into the same Colab folder. Notebooks 02 and 03 also need `pip install` lines in Colab only if a package is missing. Mock mode works in Colab too.

---

Start with **[Lesson 01 - Deep Learning and neural networks](01_DEEP_LEARNING.md)**
