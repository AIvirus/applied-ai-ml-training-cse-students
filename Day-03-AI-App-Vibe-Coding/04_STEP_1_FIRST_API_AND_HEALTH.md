# Lesson 04 - Step 1: First API and Health Check

**Time:** 30 minutes  |  **Files:** `app/config.py`, `app/llm.py`, `app/main.py`

---

## Goal

By the end of this lesson:

- the app reads its settings from `.env`,
- one file (`llm.py`) talks to Gemini, with mock mode as a backup,
- the API runs, and `/health` answers,
- you have seen the automatic API documentation at `/docs`.

---

## Understand

### FastAPI in 30 seconds

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")          # when someone visits GET /health ...
def health():                # ... run this function ...
    return {"status": "ok"}  # ... and send this back as JSON
```

**uvicorn** is the server program that receives requests from the browser and passes them to `app`.

### What is a health check?

`/health` is a tiny endpoint that answers "I am alive". Monitoring tools and cloud hosts call it every few seconds (Day 4). If it stops answering, someone gets an alert.

### Middleware

**Middleware** is code that runs for **every** request. Ours writes one **log line** per request: method, address, status code and time taken. On Day 4 you will read these logs on the cloud server.

---

## Do it now

### Part A - `app/config.py` (settings)

**Prompt for your AI assistant:**

```text
Create app/config.py for my FastAPI project. Use python-dotenv's load_dotenv() to read a .env file.
Read these settings from environment variables: GEMINI_API_KEY (default empty), GEMINI_MODEL
(default "gemini-3.5-flash-lite"), MOCK_MODE (true/false; mock is also on when there is no key),
MAX_UPLOAD_MB (default 2, also give MAX_UPLOAD_BYTES), LOG_LEVEL (default INFO).
Also define ALLOWED_DOCUMENT_TYPES = {".txt", ".md", ".pdf"} and ALLOWED_IMAGE_TYPES = {".png", ".jpg", ".jpeg"}.
Keep it short with beginner-friendly comments.
```

**Reference code** - create the file `app/config.py`:

```python
"""
config.py - all settings in one place.

Settings come from environment variables. On your computer they are read from a .env file
(this folder, or any parent folder). On a cloud server you type them in the host's dashboard.
"""

import os

from dotenv import load_dotenv

load_dotenv()  # looks for a .env file in this folder and the folders above it

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite").strip()

# MOCK_MODE=true forces the pretend AI even if a key exists (useful in class or when the API is down)
MOCK_MODE = os.getenv("MOCK_MODE", "false").strip().lower() == "true" or not GEMINI_API_KEY

MAX_UPLOAD_MB = float(os.getenv("MAX_UPLOAD_MB", "2"))
MAX_UPLOAD_BYTES = int(MAX_UPLOAD_MB * 1024 * 1024)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

ALLOWED_DOCUMENT_TYPES = {".txt", ".md", ".pdf"}
ALLOWED_IMAGE_TYPES = {".png", ".jpg", ".jpeg"}
```

### Part B - `app/llm.py` (the only file that talks to the AI)

**Prompt for your AI assistant:**

```text
Create app/llm.py. It has:
- current_mode() returning "mock" or "real" based on config.MOCK_MODE
- ask_llm(prompt, system=None, temperature=0.3, json_output=False, mock_answer="")
  that calls Gemini with the google-genai package (genai.Client, client.models.generate_content,
  types.GenerateContentConfig with system_instruction, temperature and
  response_mime_type="application/json" when json_output is True).
  It returns a tuple (text, mode). If MOCK_MODE is on, or the API call raises ANY exception,
  log a warning with only the error type (never the key) and return (mock_answer, "mock").
Create the client only once.
```

**Reference code** - create `app/llm.py`:

```python
"""
llm.py - talks to the AI model (Google Gemini).

If MOCK_MODE is on, or the API call fails, it returns the "mock" answer that the caller
prepared, so the app keeps working without internet or without an API key.
"""

import logging

from app import config

logger = logging.getLogger("study_buddy.llm")
_client = None


def _get_client():
    global _client
    if _client is None:
        from google import genai

        _client = genai.Client(api_key=config.GEMINI_API_KEY)
    return _client


def current_mode():
    return "mock" if config.MOCK_MODE else "real"


def ask_llm(prompt, system=None, temperature=0.3, json_output=False, mock_answer=""):
    """
    Send a prompt to Gemini and return (answer_text, mode).
    mode is "real" when Gemini answered, "mock" when the pretend answer was used.
    """
    if not config.MOCK_MODE:
        try:
            from google.genai import types

            settings = types.GenerateContentConfig(
                system_instruction=system,
                temperature=temperature,
                response_mime_type="application/json" if json_output else None,
            )
            response = _get_client().models.generate_content(
                model=config.GEMINI_MODEL, contents=prompt, config=settings
            )
            return (response.text or "").strip(), "real"
        except Exception as error:  # network problem, bad key, rate limit, model name changed...
            # Log the type of error only. Never log the API key.
            logger.warning("Gemini call failed (%s). Using mock answer.", type(error).__name__)

    return mock_answer, "mock"
```

### Part C - `app/main.py` (the API)

**Prompt for your AI assistant:**

```text
Create app/main.py with a FastAPI app titled "Study Buddy API". Configure logging with
config.LOG_LEVEL. Add an HTTP middleware that logs method, path, status code and duration in ms
for every request. Add GET /health that returns {"status": "ok", "ai_mode": current_mode()}.
```

**Reference code** - create `app/main.py`:

```python
"""
main.py - the web application (FastAPI).

Run it from the project folder with:
    uvicorn app.main:app --reload
Then open http://127.0.0.1:8000  (the app)  or  http://127.0.0.1:8000/docs  (the API documentation)
"""

import logging
import time

from fastapi import FastAPI, Request

from app import config
from app.llm import current_mode

# ---------------------------------------------------------------------------
# Logging: one line per request, so we can see what happens (Day 4 monitoring)
# ---------------------------------------------------------------------------
logging.basicConfig(level=config.LOG_LEVEL, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("study_buddy")

app = FastAPI(
    title="Study Buddy API",
    description="An AI learning and research assistant: upload notes, ask questions, get summaries, "
    "practice questions and CSV insights.",
    version="1.0.0",
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info("%s %s -> %s (%.0f ms)", request.method, request.url.path, response.status_code, duration_ms)
    return response


# ---------------------------------------------------------------------------
# Pages and health check
# ---------------------------------------------------------------------------
@app.get("/health")
def health():
    """Used by people and by monitoring tools to check that the app is alive."""
    return {"status": "ok", "ai_mode": current_mode()}
```

### Part D - Run it

In the terminal (in `my_study_buddy`, with `(.venv)` active):

```powershell
uvicorn app.main:app --reload
```

`app.main:app` means: "in the folder `app`, file `main.py`, use the variable `app`". `--reload` restarts the server automatically when you save a file.

You should see:

```text
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

Leave this terminal running. Open a browser:

1. http://127.0.0.1:8000/health - you see `{"status":"ok","ai_mode":"real"}` (or `"mock"`).
2. http://127.0.0.1:8000/docs - the **automatic API documentation** (Swagger UI). Click **GET /health -> Try it out -> Execute**.

Look at the terminal: there is a log line like
`INFO study_buddy: GET /health -> 200 (1 ms)`.

### Part E - Test the AI connection

Open a **second terminal** (click **+** in the terminal panel), activate `.venv`, go to `my_study_buddy`, and run:

```powershell
python -c "from app.llm import ask_llm; print(ask_llm('Say hello to a student in one short sentence.', mock_answer='Hello from mock mode!'))"
```

You see a tuple like `('Hello! Ready to learn something new today?', 'real')`, or `('Hello from mock mode!', 'mock')`.

---

## Check

- [ ] `/health` returns `"status": "ok"`.
- [ ] `/docs` shows the Study Buddy API with the `/health` endpoint.
- [ ] Each request prints a log line in the uvicorn terminal.
- [ ] The AI test prints an answer with `'real'` or `'mock'`.

---

## Review the code (do this every step)

- [ ] Is the API key read from the environment and **never written** in the code or printed in logs?
- [ ] If the AI call fails, does the app **keep working**? (Yes - `except Exception` returns the mock answer.)
- [ ] Do you understand every line? Ask your assistant to explain the middleware if not.

---

## What just happened?

- `config.py` loads `.env`, so secrets live outside the code.
- `llm.py` hides all AI details behind one function. Every feature will call `ask_llm(...)` and pass a sensible `mock_answer`.
- `main.py` created the API, logging and the health check. FastAPI generated `/docs` for free.

---

## Try it yourself

1. Add a new endpoint `GET /api/hello` that returns `{"message": "Hello from Study Buddy"}`. Save, and see it appear in `/docs` (no restart needed thanks to `--reload`).
2. Set `MOCK_MODE=true` in `.env`, stop the server (**Ctrl + C**) and start it again. What does `/health` show now? Set it back afterwards.

---

## If it does not work

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'app'` | You are not in `my_study_buddy`. Run `cd` to the right folder. Also check that `app/__init__.py` exists. |
| `Error loading ASGI app. Could not import module "app.main"` | Same as above, or a typing error in `main.py`. Read the lines above the error for the exact problem. |
| `[Errno 10048] ... address already in use` | Another server is running on port 8000. Stop it with **Ctrl + C** in its terminal, or run `uvicorn app.main:app --reload --port 8001` and use port 8001. |
| `uvicorn` is not recognized | `.venv` is not active. Activate it, or run `python -m uvicorn app.main:app --reload`. |
| AI test shows `'mock'` although you have a key | Check `.env` is in `my_study_buddy` and `MOCK_MODE=false`. Look at the warning line: it shows the error type (for example `ClientError` for a wrong key or model name). |

Next: **[Lesson 05 - Step 2: upload and chunk documents](05_STEP_2_UPLOAD_DOCUMENTS.md)**
