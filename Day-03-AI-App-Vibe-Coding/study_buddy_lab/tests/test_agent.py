"""
Tests for the optional research agent (Day 3, Lesson 12). Run with:   pytest -v
"""

from fastapi.testclient import TestClient

from app.main import app
from app.store import store

client = TestClient(app)


def test_agent_returns_steps_and_answer():
    store.clear()
    store.add("rules.txt", ["Late fees: If a book is returned late, the fine is 5 rupees per day for each book."])
    data = client.post("/api/agent", json={"goal": "What is the late fee for books?"}).json()
    assert data["steps"][0]["tool"] == "search_documents"
    assert "5 rupees" in data["final_answer"]
    store.clear()


def test_agent_needs_a_document_first():
    store.clear()
    response = client.post("/api/agent", json={"goal": "What is the late fee?"})
    assert response.status_code == 400
