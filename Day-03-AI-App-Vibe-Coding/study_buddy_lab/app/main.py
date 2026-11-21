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
from app.agent import run_agent
from app.csv_tools import CSVError, analyse_csv
from app.documents import DocumentError, chunk_text, extract_text
from app.llm import current_mode
from app.ocr import OCRUnavailable, image_to_text
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


class AgentRequest(BaseModel):
    goal: str = Field(min_length=3, max_length=500)


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


# ---------------------------------------------------------------------------
# Optional feature 5: OCR
# ---------------------------------------------------------------------------
@app.post("/api/ocr")
async def ocr(file: UploadFile = File(...), add_to_documents: bool = Form(default=False)):
    data = await read_upload(file, config.ALLOWED_IMAGE_TYPES)
    try:
        text = image_to_text(data)
    except OCRUnavailable as error:
        raise HTTPException(503, f"OCR is not available: {error}")
    if add_to_documents and text:
        store.add(f"{file.filename} (OCR)", chunk_text(text))
    return {"filename": file.filename, "text": text, "added_to_documents": bool(add_to_documents and text)}


# ---------------------------------------------------------------------------
# Optional feature 6: research agent
# ---------------------------------------------------------------------------
@app.post("/api/agent")
def agent(request: AgentRequest):
    if not store.chunks:
        raise HTTPException(400, "Please upload a document first.")
    return run_agent(request.goal.strip())
