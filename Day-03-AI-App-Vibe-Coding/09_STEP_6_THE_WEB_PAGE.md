# Lesson 09 - Step 6: The Web Page

**Time:** 25 minutes  |  **Files:** `app/static/index.html`, `app/static/style.css`, `app/static/app.js`, `app/main.py`

---

## Goal

By the end of this lesson students can use Study Buddy in a normal web page - no `/docs` needed.

---

## Understand

| File | Job |
|---|---|
| `index.html` | The **structure**: headings, forms, buttons, empty boxes for results |
| `style.css` | The **look**: colours, spacing, cards |
| `app.js` | The **behaviour**: when a button is clicked, call the API with `fetch()` and show the result |

FastAPI serves these files from the `app/static` folder, and `/` returns `index.html`.

### A security rule for the browser

Text from documents and from the AI is **untrusted**. If we put it into the page with `innerHTML`, a document containing `<script>...</script>` could run code in the user's browser (this attack is called **XSS**, cross-site scripting). So `app.js` always uses **`textContent`**, which shows text as plain text, never as code.

---

## Do it now

### Part A - Ask for the page

**Prompt for your AI assistant:**

```text
Create a simple, clean frontend for my FastAPI app in app/static: index.html, style.css and app.js.
No frameworks. Sections (cards): 1. upload a document (.txt/.md/.pdf) + list + "remove all" button,
2. ask a question + answer + collapsible sources, 3. buttons for summary and 5 practice questions,
4. CSV upload with optional column name, facts, explanation and chart image (base64 PNG),
5. optional OCR image upload with "add to my documents" checkbox, 6. optional research agent with steps.
Show the server status from GET /health at the top. API: POST /api/documents (file),
GET/DELETE /api/documents, POST /api/ask {question}, POST /api/summary {count},
POST /api/practice-questions {count}, POST /api/csv (file, column), POST /api/ocr (file,
add_to_documents), POST /api/agent {goal}. Show error messages from the "detail" field.
IMPORTANT: put all text into the page with textContent, never innerHTML. Disable buttons while waiting.
Show a note when the response has "mode": "mock".
```

### Part B - Reference code

Create the three files. (Sections 5 and 6 call optional endpoints; until you do Lessons 11 and 12 they show a "Not Found" message, which is fine.)

`app/static/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Study Buddy</title>
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>
  <header>
    <h1>Study Buddy</h1>
    <p>Your AI learning and research assistant</p>
    <p id="status" class="status">Checking the server...</p>
  </header>

  <main>
    <!-- 1. Documents -->
    <section class="card">
      <h2>1. Upload your notes</h2>
      <p class="hint">.txt, .md or .pdf, up to 2 MB</p>
      <form id="upload-form">
        <input type="file" id="doc-file" accept=".txt,.md,.pdf" required>
        <button type="submit">Upload</button>
      </form>
      <ul id="doc-list"></ul>
      <button id="clear-docs" class="secondary">Remove all documents</button>
      <p id="upload-result" class="result"></p>
    </section>

    <!-- 2. Ask -->
    <section class="card">
      <h2>2. Ask a question</h2>
      <form id="ask-form">
        <input type="text" id="question" placeholder="For example: What is the fine for a late book?" minlength="3" maxlength="500" required>
        <button type="submit">Ask</button>
      </form>
      <div id="answer" class="result"></div>
      <details>
        <summary>Sources used</summary>
        <ul id="sources"></ul>
      </details>
    </section>

    <!-- 3. Summary and practice -->
    <section class="card">
      <h2>3. Summary and practice questions</h2>
      <button id="summary-btn">Summarise all notes</button>
      <button id="practice-btn">Make 5 practice questions</button>
      <div id="study-result" class="result"></div>
    </section>

    <!-- 4. CSV -->
    <section class="card">
      <h2>4. CSV insights and chart</h2>
      <form id="csv-form">
        <input type="file" id="csv-file" accept=".csv" required>
        <input type="text" id="csv-column" placeholder="Column to chart (optional)">
        <button type="submit">Analyse</button>
      </form>
      <div id="csv-result" class="result"></div>
      <img id="csv-chart" alt="Chart of the selected column" hidden>
    </section>

    <!-- 5. Optional: OCR -->
    <section class="card optional">
      <h2>5. Optional: read text from an image (OCR)</h2>
      <form id="ocr-form">
        <input type="file" id="ocr-file" accept=".png,.jpg,.jpeg" required>
        <label><input type="checkbox" id="ocr-add"> Add the text to my documents</label>
        <button type="submit">Read text</button>
      </form>
      <pre id="ocr-result" class="result"></pre>
    </section>

    <!-- 6. Optional: agent -->
    <section class="card optional">
      <h2>6. Optional: research agent</h2>
      <form id="agent-form">
        <input type="text" id="goal" placeholder="For example: Find the late fee rule and calculate it for 3 books, 4 days late" minlength="3" maxlength="500" required>
        <button type="submit">Run agent</button>
      </form>
      <ol id="agent-steps"></ol>
      <div id="agent-result" class="result"></div>
    </section>
  </main>

  <footer>AI answers can be wrong. Always check important facts in your own notes.</footer>
  <script src="/static/app.js"></script>
</body>
</html>
```

`app/static/style.css`:

```css
:root {
  --bg: #f4f6fb;
  --card: #ffffff;
  --text: #1f2937;
  --muted: #6b7280;
  --accent: #2563eb;
  --error: #b91c1c;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.5;
}

header, footer { text-align: center; padding: 1.5rem 1rem; }
header h1 { margin: 0; color: var(--accent); }
header p { margin: 0.25rem 0; }
footer { color: var(--muted); font-size: 0.9rem; }

main {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 1rem;
  display: grid;
  gap: 1rem;
}

.card {
  background: var(--card);
  border-radius: 10px;
  padding: 1rem 1.25rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}
.card.optional { border-left: 4px solid #9ca3af; }
.card h2 { margin-top: 0; font-size: 1.2rem; }

form { display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center; }
input[type="text"] { flex: 1 1 280px; padding: 0.55rem; border: 1px solid #d1d5db; border-radius: 6px; }

button {
  background: var(--accent);
  color: white;
  border: none;
  border-radius: 6px;
  padding: 0.55rem 1rem;
  cursor: pointer;
  margin: 0.25rem 0.25rem 0.25rem 0;
}
button.secondary { background: #6b7280; }
button:disabled { opacity: 0.6; cursor: wait; }

.hint { color: var(--muted); margin-top: 0; font-size: 0.9rem; }
.status { font-size: 0.9rem; color: var(--muted); }
.result { white-space: pre-wrap; margin-top: 0.75rem; }
.error { color: var(--error); }
pre.result { background: #f3f4f6; padding: 0.5rem; border-radius: 6px; }
#csv-chart { max-width: 100%; margin-top: 0.75rem; }
```

`app/static/app.js`:

```javascript
// app.js - connects the web page to the Study Buddy API.
// Safety rule: we put text on the page with textContent (never innerHTML),
// so text from documents or from the AI cannot run as code in the browser.

const $ = (id) => document.getElementById(id);

// Small helper: call the API and return JSON, or throw an Error with the server's message
async function callApi(url, options = {}) {
  const response = await fetch(url, options);
  let body = {};
  try { body = await response.json(); } catch (e) { /* no JSON body */ }
  if (!response.ok) {
    const detail = Array.isArray(body.detail) ? body.detail.map((d) => d.msg).join("; ") : body.detail;
    throw new Error(detail || `Request failed with status ${response.status}`);
  }
  return body;
}

function postJson(url, data) {
  return callApi(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
}

function show(element, text, isError = false) {
  element.textContent = text;
  element.classList.toggle("error", isError);
}

// Disable a button while waiting, so users do not click twice
async function busy(button, work) {
  button.disabled = true;
  try { await work(); } finally { button.disabled = false; }
}

function modeNote(mode) {
  return mode === "mock" ? "\n\n[MOCK MODE: pretend AI answer. Add an API key for real answers.]" : "";
}

// ---- Status and document list ----------------------------------------------
async function refreshStatus() {
  try {
    const health = await callApi("/health");
    show($("status"), `Server OK. AI mode: ${health.ai_mode}. Documents: ${health.documents}.`);
  } catch (error) {
    show($("status"), "Cannot reach the server. Is uvicorn running?", true);
  }
}

async function refreshDocuments() {
  const data = await callApi("/api/documents");
  const list = $("doc-list");
  list.replaceChildren();
  for (const doc of data.documents) {
    const item = document.createElement("li");
    item.textContent = `${doc.filename} (${doc.chunks} chunks)`;
    list.appendChild(item);
  }
  refreshStatus();
}

// ---- 1. Upload ---------------------------------------------------------------
$("upload-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const button = event.submitter;
  busy(button, async () => {
    const form = new FormData();
    form.append("file", $("doc-file").files[0]);
    try {
      const result = await callApi("/api/documents", { method: "POST", body: form });
      show($("upload-result"), `Uploaded ${result.filename}: ${result.characters} characters, ${result.chunks} chunks.`);
      refreshDocuments();
    } catch (error) {
      show($("upload-result"), error.message, true);
    }
  });
});

$("clear-docs").addEventListener("click", async () => {
  await callApi("/api/documents", { method: "DELETE" });
  show($("upload-result"), "All documents removed.");
  refreshDocuments();
});

// ---- 2. Ask ------------------------------------------------------------------
$("ask-form").addEventListener("submit", (event) => {
  event.preventDefault();
  busy(event.submitter, async () => {
    show($("answer"), "Thinking...");
    $("sources").replaceChildren();
    try {
      const result = await postJson("/api/ask", { question: $("question").value });
      show($("answer"), result.answer + modeNote(result.mode));
      for (const source of result.sources) {
        const item = document.createElement("li");
        item.textContent = `${source.source} (score ${source.score}): ${source.text.slice(0, 200)}...`;
        $("sources").appendChild(item);
      }
    } catch (error) {
      show($("answer"), error.message, true);
    }
  });
});

// ---- 3. Summary and practice questions ---------------------------------------
$("summary-btn").addEventListener("click", (event) => {
  busy(event.target, async () => {
    show($("study-result"), "Summarising...");
    try {
      const result = await postJson("/api/summary", { count: 5 });
      show($("study-result"), result.summary + modeNote(result.mode));
    } catch (error) {
      show($("study-result"), error.message, true);
    }
  });
});

$("practice-btn").addEventListener("click", (event) => {
  busy(event.target, async () => {
    show($("study-result"), "Creating questions...");
    try {
      const result = await postJson("/api/practice-questions", { count: 5 });
      const text = result.questions.map((q, i) => `Q${i + 1}. ${q.question}\nAnswer: ${q.answer}`).join("\n\n");
      show($("study-result"), text + modeNote(result.mode));
    } catch (error) {
      show($("study-result"), error.message, true);
    }
  });
});

// ---- 4. CSV ------------------------------------------------------------------
$("csv-form").addEventListener("submit", (event) => {
  event.preventDefault();
  busy(event.submitter, async () => {
    const form = new FormData();
    form.append("file", $("csv-file").files[0]);
    if ($("csv-column").value.trim()) form.append("column", $("csv-column").value.trim());
    show($("csv-result"), "Analysing...");
    $("csv-chart").hidden = true;
    try {
      const result = await callApi("/api/csv", { method: "POST", body: form });
      const text = `Columns: ${result.columns.join(", ")}\n\nFacts:\n- ${result.insights.join("\n- ")}\n\nExplanation:\n${result.explanation}`;
      show($("csv-result"), text + modeNote(result.mode));
      $("csv-chart").src = `data:image/png;base64,${result.chart_png_base64}`;
      $("csv-chart").hidden = false;
    } catch (error) {
      show($("csv-result"), error.message, true);
    }
  });
});

// ---- 5. OCR ------------------------------------------------------------------
$("ocr-form").addEventListener("submit", (event) => {
  event.preventDefault();
  busy(event.submitter, async () => {
    const form = new FormData();
    form.append("file", $("ocr-file").files[0]);
    form.append("add_to_documents", $("ocr-add").checked);
    show($("ocr-result"), "Reading...");
    try {
      const result = await callApi("/api/ocr", { method: "POST", body: form });
      show($("ocr-result"), result.text || "(no text found)");
      if (result.added_to_documents) refreshDocuments();
    } catch (error) {
      show($("ocr-result"), error.message, true);
    }
  });
});

// ---- 6. Agent ----------------------------------------------------------------
$("agent-form").addEventListener("submit", (event) => {
  event.preventDefault();
  busy(event.submitter, async () => {
    $("agent-steps").replaceChildren();
    show($("agent-result"), "Working...");
    try {
      const result = await postJson("/api/agent", { goal: $("goal").value });
      for (const step of result.steps) {
        const item = document.createElement("li");
        item.textContent = `${step.tool}("${step.input}") -> ${step.observation.slice(0, 200)}`;
        $("agent-steps").appendChild(item);
      }
      show($("agent-result"), "Final answer: " + result.final_answer + modeNote(result.mode));
    } catch (error) {
      show($("agent-result"), error.message, true);
    }
  });
});

refreshDocuments();
```

### Part C - Serve the page from `app/main.py`

**1. Add these import lines:**

```python
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
```

**2. Add these lines** - `STATIC_DIR` just before `app = FastAPI(...)`, and `app.mount(...)` just after it:

```python
STATIC_DIR = Path(__file__).parent / "static"
```
```python
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
```

**3. Add the home page route** just before the `health` function:

```python
@app.get("/", include_in_schema=False)
def home():
    return FileResponse(STATIC_DIR / "index.html")
```

Your `main.py` is now complete for the core app. Compare it carefully:

<details>
<summary>Click to see the complete <code>app/main.py</code> after this step</summary>

```python
"""
main.py - the web application (FastAPI).

Run it from the project folder with:
    uvicorn app.main:app --reload
Then open http://127.0.0.1:8000  (the app)  or  http://127.0.0.1:8000/docs  (the API documentation)
"""

import logging
import time
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app import config
from app.csv_tools import CSVError, analyse_csv
from app.documents import DocumentError, chunk_text, extract_text
from app.llm import current_mode
from app.store import store
from app.study import answer_question, make_practice_questions, make_summary

# ---------------------------------------------------------------------------
# Logging: one line per request, so we can see what happens (Day 4 monitoring)
# ---------------------------------------------------------------------------
logging.basicConfig(level=config.LOG_LEVEL, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("study_buddy")

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(
    title="Study Buddy API",
    description="An AI learning and research assistant: upload notes, ask questions, get summaries, "
    "practice questions and CSV insights.",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info("%s %s -> %s (%.0f ms)", request.method, request.url.path, response.status_code, duration_ms)
    return response


# ---------------------------------------------------------------------------
# Request bodies (Pydantic checks the input for us)
# ---------------------------------------------------------------------------
class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=500)


class StudyRequest(BaseModel):
    filename: str | None = None
    count: int = Field(default=5, ge=1, le=10)


async def read_upload(upload: UploadFile, allowed_types):
    extension = Path(upload.filename or "").suffix.lower()
    if extension not in allowed_types:
        raise HTTPException(400, f"File type '{extension or 'none'}' is not allowed. Use: {', '.join(sorted(allowed_types))}")
    data = await upload.read()
    if len(data) > config.MAX_UPLOAD_BYTES:
        raise HTTPException(413, f"File is too large. The limit is {config.MAX_UPLOAD_MB:g} MB.")
    if not data:
        raise HTTPException(400, "The file is empty.")
    return data


# ---------------------------------------------------------------------------
# Pages and health check
# ---------------------------------------------------------------------------
@app.get("/", include_in_schema=False)
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health():
    """Used by people and by monitoring tools to check that the app is alive."""
    return {"status": "ok", "ai_mode": current_mode(), "documents": len(store.list_documents())}


# ---------------------------------------------------------------------------
# Feature 1: documents
# ---------------------------------------------------------------------------
@app.post("/api/documents")
async def upload_document(file: UploadFile = File(...)):
    data = await read_upload(file, config.ALLOWED_DOCUMENT_TYPES)
    try:
        text = extract_text(file.filename, data)
    except DocumentError as error:
        raise HTTPException(400, str(error))
    chunks = chunk_text(text)
    store.add(file.filename, chunks)
    logger.info("Document added: %s (%d chunks)", file.filename, len(chunks))
    return {"filename": file.filename, "characters": len(text), "chunks": len(chunks)}


@app.get("/api/documents")
def list_documents():
    return {"documents": store.list_documents()}


@app.delete("/api/documents")
def delete_documents():
    store.clear()
    return {"message": "All documents removed."}


# ---------------------------------------------------------------------------
# Feature 2: ask questions (RAG)
# ---------------------------------------------------------------------------
@app.post("/api/ask")
def ask(request: AskRequest):
    if not store.chunks:
        raise HTTPException(400, "Please upload a document first.")
    return answer_question(request.question.strip())


# ---------------------------------------------------------------------------
# Feature 3: summary and practice questions
# ---------------------------------------------------------------------------
def _check_filename(filename):
    if filename and filename not in {d["filename"] for d in store.list_documents()}:
        raise HTTPException(404, f"No document called '{filename}'.")
    if not store.chunks:
        raise HTTPException(400, "Please upload a document first.")


@app.post("/api/summary")
def summary(request: StudyRequest):
    _check_filename(request.filename)
    return make_summary(request.filename, points=request.count)


@app.post("/api/practice-questions")
def practice_questions(request: StudyRequest):
    _check_filename(request.filename)
    return make_practice_questions(request.filename, count=request.count)


# ---------------------------------------------------------------------------
# Feature 4: CSV insights and chart
# ---------------------------------------------------------------------------
@app.post("/api/csv")
async def csv_insights(file: UploadFile = File(...), column: str | None = Form(default=None)):
    data = await read_upload(file, {".csv"})
    try:
        return analyse_csv(data, column=column or None)
    except CSVError as error:
        raise HTTPException(400, str(error))
```

</details>

### Part D - Use the app

Open http://127.0.0.1:8000 and try every section with the files in `sample_files/`.

---

## Check

- [ ] The top line says "Server OK. AI mode: ...".
- [ ] Uploading a file shows it in the list.
- [ ] Asking "What is the fine for a late book?" shows the answer and, under **Sources used**, the chunks.
- [ ] Summary and practice questions appear.
- [ ] The CSV section shows facts, an explanation and a chart.
- [ ] Uploading a wrong file type shows the error in red, and the page keeps working.

---

## Review the code

- [ ] Search `app.js` for `innerHTML`. It must **not** be there.
- [ ] Is the API key anywhere in the HTML or JavaScript? It must **not** be. (Press **F12 -> Sources** in the browser to see what visitors can see.)
- [ ] Are buttons disabled while waiting, so users cannot send the same request 10 times?

---

## What just happened?

You built a complete **full-stack** app: a frontend (HTML, CSS, JS) that calls a backend API (FastAPI) that calls an AI model (Gemini). This is the same architecture as most AI products.

---

## Try it yourself

1. Ask your AI assistant to add a "Copy answer" button. Check that it still uses `textContent`.
2. Change the colours in `style.css` (`--accent`) to your favourite colour.
3. Open the browser's developer tools (**F12**) -> **Network** tab, ask a question, and look at the request and the JSON response.

---

## If it does not work

| Problem | Fix |
|---|---|
| The page is plain with no colours | `style.css` is not found. Check the file is in `app/static/` and `app.mount("/static", ...)` is in `main.py`. Press **Ctrl + F5** to reload without cache. |
| Buttons do nothing | Press **F12 -> Console** and read the red error. Often a typing mistake in `app.js` or a wrong element id. |
| `RuntimeError: Directory '.../app/static' does not exist` | Create the folder `app/static` (Lesson 03, Step 2). |
| "Cannot reach the server" | uvicorn is not running. Start it again. |

Next: **[Lesson 10 - Step 7: test and debug](10_STEP_7_TEST_AND_DEBUG.md)**
