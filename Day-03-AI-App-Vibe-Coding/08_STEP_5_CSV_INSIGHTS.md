# Lesson 08 - Step 5: CSV Insights and Charts

**Time:** 25 minutes  |  **Files:** `app/csv_tools.py`, `app/main.py`

---

## Goal

By the end of this lesson the app can take a CSV file and return:

- basic facts (rows, columns, missing values, averages, the strongest relationship, the most common values),
- an AI explanation of those facts in simple words,
- a chart (histogram or bar chart) as an image.

---

## Understand

This is Day 1 (pandas and matplotlib) inside a web app.

- **Rule-based insights** come from pandas: always correct, always free.
- The **AI explanation** turns those facts into friendly sentences. We send only the **summary facts** to the AI, never the whole file - cheaper and better for privacy.
- A server has no screen, so matplotlib draws into memory (`matplotlib.use("Agg")`). We save the chart as PNG bytes and send it as **base64 text**, which the browser can show directly as an image.

---

## Do it now

### Part A - `app/csv_tools.py`

**Prompt for your AI assistant:**

```text
Create app/csv_tools.py with:
- class CSVError(ValueError)
- read_csv(data: bytes) -> DataFrame (pandas, io.BytesIO); raise CSVError if unreadable, empty,
  or more than 100,000 rows
- find_insights(df) -> list of plain-English facts: rows and columns, missing values per column,
  average/lowest/highest of up to 5 number columns, the strongest correlation pair,
  the most common value of up to 3 text columns
- make_chart(df, column=None) -> (column, base64 PNG). Use matplotlib with the "Agg" backend.
  Histogram for a number column, bar chart of the top 10 values for a text column.
  Default: the first number column. Raise CSVError for an unknown column.
- analyse_csv(data, column=None): run the above, ask the LLM to explain the facts for a student
  (mock answer = the first facts), return rows, columns, a 5-row preview, insights, explanation,
  chart_column, chart_png_base64 and mode.
```

**Reference code** - create `app/csv_tools.py`:

```python
"""
csv_tools.py - read a CSV file, find simple insights and draw a chart.
"""

import base64
import io

import matplotlib

matplotlib.use("Agg")  # draw charts into memory (a server has no screen)
import matplotlib.pyplot as plt
import pandas as pd

from app.llm import ask_llm


class CSVError(ValueError):
    """A problem with the CSV file that the user can fix."""


def read_csv(data):
    try:
        df = pd.read_csv(io.BytesIO(data))
    except Exception as error:
        raise CSVError(f"Could not read this CSV file ({type(error).__name__}).") from error
    if df.empty or len(df.columns) == 0:
        raise CSVError("The CSV file has no rows.")
    if len(df) > 100_000:
        raise CSVError("The CSV file is too big for this demo (more than 100,000 rows).")
    return df


def find_insights(df):
    """Simple, rule-based facts about the table (no AI needed)."""
    insights = [f"The table has {len(df)} rows and {len(df.columns)} columns."]

    missing = df.isna().sum()
    for column, count in missing[missing > 0].items():
        insights.append(f"Column '{column}' has {count} missing values.")

    numbers = df.select_dtypes("number")
    for column in numbers.columns[:5]:
        insights.append(
            f"'{column}': average {numbers[column].mean():.2f}, lowest {numbers[column].min()}, highest {numbers[column].max()}."
        )

    if numbers.shape[1] >= 2:
        corr = numbers.corr().abs()
        pairs = [(corr.iloc[i, j], corr.columns[i], corr.columns[j])
                 for i in range(len(corr)) for j in range(i + 1, len(corr))]
        pairs = [p for p in pairs if pd.notna(p[0])]
        if pairs:
            value, a, b = max(pairs)
            insights.append(f"The strongest relationship is between '{a}' and '{b}' (correlation {value:.2f}).")

    for column in df.select_dtypes(exclude="number").columns[:3]:
        top = df[column].value_counts()
        if not top.empty:
            insights.append(f"Most common value in '{column}' is '{top.index[0]}' ({top.iloc[0]} rows).")
    return insights


def make_chart(df, column=None):
    """Draw a histogram (number column) or bar chart (text column). Return it as base64 PNG text."""
    if column is None:
        numeric = df.select_dtypes("number").columns
        column = numeric[0] if len(numeric) else df.columns[0]
    if column not in df.columns:
        raise CSVError(f"Column '{column}' is not in the file. Columns: {', '.join(map(str, df.columns))}")

    fig, ax = plt.subplots(figsize=(7, 4))
    if pd.api.types.is_numeric_dtype(df[column]):
        ax.hist(df[column].dropna(), bins=15, edgecolor="black")
        ax.set_ylabel("Number of rows")
    else:
        df[column].value_counts().head(10).plot.bar(ax=ax)
        ax.set_ylabel("Count")
    ax.set_title(f"Distribution of '{column}'")
    ax.set_xlabel(str(column))
    fig.tight_layout()

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    plt.close(fig)
    return column, base64.b64encode(buffer.getvalue()).decode("ascii")


def analyse_csv(data, column=None):
    df = read_csv(data)
    insights = find_insights(df)
    chart_column, chart = make_chart(df, column)

    # Ask the AI to explain the facts in plain words (only the summary is sent, never the whole file)
    facts = "\n".join(insights)
    explanation, mode = ask_llm(
        f"Here are facts about a data table:\n{facts}\n\nExplain the 3 most interesting points for a student in simple English.",
        temperature=0.3,
        mock_answer="Key points: " + " ".join(insights[1:4]),
    )
    return {
        "rows": len(df),
        "columns": [str(c) for c in df.columns],
        "preview": df.head(5).astype(str).to_dict(orient="records"),
        "insights": insights,
        "explanation": explanation,
        "chart_column": str(chart_column),
        "chart_png_base64": chart,
        "mode": mode,
    }
```

### Part B - Add the endpoint to `app/main.py`

**1. Add / change these import lines** (`Form` is new in the fastapi line):

```python
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from app.csv_tools import CSVError, analyse_csv
```

**2. Add the endpoint** at the end of the file:

```python
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

### Part C - Try it

In `/docs`: **POST /api/csv -> Try it out**, choose `sample_files/student_marks.csv`, leave `column` empty, **Execute**.

---

## Check

- [ ] The response has `"rows": 80` and a list of `insights`.
- [ ] One insight says the strongest relationship is between `hours_studied` and `final_score`.
- [ ] `chart_png_base64` is a very long text (that is the picture).
- [ ] With `column` = `height`, you get **400** "Column 'height' is not in the file."

To see the chart now, copy the long `chart_png_base64` text and paste it into your browser's address bar after `data:image/png;base64,` - or just wait for Lesson 09, where the web page shows it.

---

## Review the code

- [ ] Is there a row limit so a huge file cannot freeze the server?
- [ ] Is only a summary (not the raw data) sent to the AI?
- [ ] Is the figure closed after saving (`plt.close(fig)`) so memory does not grow?

---

## What just happened?

You connected **data analysis** (Day 1) with **generative AI** (Day 2): exact numbers from pandas, plus a human-friendly explanation from the LLM.

---

## Try it yourself

1. Upload `Day-01-AI-ML-Foundations/data/student_performance.csv` (300 rows) with column `city_type`. You get a bar chart.
2. Add a new insight: the percentage of rows where `result` is `pass` (only if that column exists).

---

## If it does not work

| Problem | Fix |
|---|---|
| `RuntimeError: main thread is not in main loop` or a window tries to open | `matplotlib.use("Agg")` must come **before** `import matplotlib.pyplot`. |
| `UnicodeDecodeError` on a CSV | The file is not UTF-8. Open it in Excel and "Save As -> CSV UTF-8". |
| `400 File type '.xlsx' is not allowed` | Save the Excel file as CSV first. |

Next: **[Lesson 09 - Step 6: the web page](09_STEP_6_THE_WEB_PAGE.md)**
