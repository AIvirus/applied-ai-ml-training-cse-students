"""
Automated tests for Study Buddy. Run from the project folder with:   pytest -v
Each test checks one behaviour: a normal input AND wrong inputs.
"""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.documents import chunk_text
from app.main import app
from app.store import store

client = TestClient(app)
SAMPLES = Path(__file__).resolve().parents[1] / "sample_files"


@pytest.fixture(autouse=True)
def empty_store():
    """Start every test with no documents."""
    store.clear()
    yield
    store.clear()


def upload(name):
    with open(SAMPLES / name, "rb") as f:
        return client.post("/api/documents", files={"file": (name, f, "text/plain")})


# ---- health and home page -----------------------------------------------------
def test_health_says_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["ai_mode"] == "mock"


def test_home_page_loads():
    response = client.get("/")
    assert response.status_code == 200
    assert "Study Buddy" in response.text


# ---- chunking -------------------------------------------------------------------
def test_chunk_text_keeps_pieces_small():
    text = "\n".join(f"Sentence number {i} is here." for i in range(100))
    chunks = chunk_text(text, chunk_size=200)
    assert len(chunks) > 5
    assert all(len(c) <= 260 for c in chunks)


# ---- documents ------------------------------------------------------------------
def test_upload_text_document():
    response = upload("college_library_rules.txt")
    assert response.status_code == 200
    assert response.json()["chunks"] >= 3
    assert client.get("/api/documents").json()["documents"][0]["filename"] == "college_library_rules.txt"


def test_upload_rejects_wrong_file_type():
    response = client.post("/api/documents", files={"file": ("virus.exe", b"MZ...", "application/octet-stream")})
    assert response.status_code == 400
    assert "not allowed" in response.json()["detail"]


def test_upload_rejects_empty_file():
    response = client.post("/api/documents", files={"file": ("empty.txt", b"", "text/plain")})
    assert response.status_code == 400


def test_upload_rejects_too_large_file():
    big = b"a" * (3 * 1024 * 1024)
    response = client.post("/api/documents", files={"file": ("big.txt", big, "text/plain")})
    assert response.status_code == 413


# ---- ask questions --------------------------------------------------------------
def test_ask_finds_the_answer_with_source():
    upload("college_library_rules.txt")
    response = client.post("/api/ask", json={"question": "What is the fine for a late book?"})
    data = response.json()
    assert response.status_code == 200
    assert "5 rupees" in data["answer"]
    assert data["sources"][0]["source"] == "college_library_rules.txt"


def test_ask_says_not_found_for_unrelated_question():
    upload("college_library_rules.txt")
    data = client.post("/api/ask", json={"question": "Who won the cricket world cup in 2011?"}).json()
    assert "could not find" in data["answer"].lower()


def test_ask_without_documents_gives_clear_error():
    response = client.post("/api/ask", json={"question": "What is the fine?"})
    assert response.status_code == 400
    assert "upload" in response.json()["detail"].lower()


def test_ask_rejects_too_short_question():
    upload("college_library_rules.txt")
    response = client.post("/api/ask", json={"question": "a"})
    assert response.status_code == 422


# ---- summary and practice questions ---------------------------------------------
def test_summary_returns_bullets():
    upload("healthy_study_habits.txt")
    data = client.post("/api/summary", json={"count": 3}).json()
    assert data["summary"].count("- ") >= 2


def test_practice_questions_have_valid_shape():
    upload("healthy_study_habits.txt")
    data = client.post("/api/practice-questions", json={"count": 3}).json()
    assert 1 <= len(data["questions"]) <= 3
    assert all(q["question"] and q["answer"] for q in data["questions"])


def test_practice_questions_unknown_file_gives_404():
    upload("healthy_study_habits.txt")
    response = client.post("/api/practice-questions", json={"filename": "missing.txt"})
    assert response.status_code == 404


# ---- CSV ------------------------------------------------------------------------
def test_csv_analysis_returns_insights_and_chart():
    with open(SAMPLES / "student_marks.csv", "rb") as f:
        response = client.post("/api/csv", files={"file": ("student_marks.csv", f, "text/csv")})
    data = response.json()
    assert response.status_code == 200
    assert data["rows"] > 0
    assert any("strongest relationship" in i for i in data["insights"])
    assert len(data["chart_png_base64"]) > 1000


def test_csv_with_unknown_column_gives_error():
    with open(SAMPLES / "student_marks.csv", "rb") as f:
        response = client.post("/api/csv", files={"file": ("m.csv", f, "text/csv")}, data={"column": "height"})
    assert response.status_code == 400
