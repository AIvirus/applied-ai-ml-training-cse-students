# Study Buddy - AI Learning and Research Assistant

A small web app for students: upload your notes, ask questions answered **only from your notes** (with sources), get summaries and practice questions, and turn a CSV file into insights and a chart. Optional: read text from images (OCR) and a small research agent.

This folder is the **finished answer key** for Day 3 of the Applied AI and Machine Learning course.

## Features

| Feature | Endpoint |
|---|---|
| Web page | `GET /` |
| Health check | `GET /health` |
| Upload / list / remove documents (.txt, .md, .pdf) | `POST`, `GET`, `DELETE /api/documents` |
| Ask a question (RAG with sources) | `POST /api/ask` |
| Summary | `POST /api/summary` |
| Practice questions (validated JSON) | `POST /api/practice-questions` |
| CSV insights and chart | `POST /api/csv` |
| Optional: OCR | `POST /api/ocr` |
| Optional: research agent | `POST /api/agent` |

Interactive API documentation: `/docs`.

## Architecture

```text
Browser (index.html, style.css, app.js)
   |  fetch() JSON / files
   v
FastAPI (app/main.py) -> documents.py, store.py (TF-IDF search), study.py (RAG, summary, questions),
                         csv_tools.py (pandas, matplotlib), ocr.py, agent.py
                         llm.py -> Google Gemini (or MOCK MODE)
```

## Run it on your computer (5 minutes)

From this folder, with the course virtual environment active:

```powershell
pip install -r requirements.txt
```

```powershell
Copy-Item .env.example .env
```

(macOS / Linux: `cp .env.example .env`.) Put your Gemini key in `.env`, or leave it empty to use mock mode.

```powershell
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000 and try the files in `sample_files/`.

## Run the tests

```powershell
pytest -v
```

Tests always run in mock mode, so they need no API key and no internet.

## Run with Docker

```powershell
docker build -t study-buddy .
```

```powershell
docker run --rm -p 8000:8000 --env-file .env study-buddy
```

Or: `docker compose up --build`.

## Settings (environment variables)

| Name | Default | Meaning |
|---|---|---|
| `GEMINI_API_KEY` | empty | Your Gemini API key. Empty = mock mode. |
| `GEMINI_MODEL` | `gemini-3.5-flash-lite` | Model name. Check current names at https://ai.google.dev/gemini-api/docs/models |
| `MOCK_MODE` | `false` | `true` forces the pretend AI |
| `MAX_UPLOAD_MB` | `2` | Largest allowed upload |
| `LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING` or `ERROR` |

## Known limitations

- Documents are stored in memory: they are lost when the server restarts, and all users share them.
- TF-IDF search matches words, not meaning.
- No user accounts.
- AI answers can be wrong; always check the sources.
