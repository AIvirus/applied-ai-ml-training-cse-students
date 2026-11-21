"""
ai_helper.py - a small helper that the Day 2 notebooks use to talk to an AI model.

You do NOT need to change this file. Just read it if you are curious.

What it does
------------
1. Reads your private settings from the ".env" file in the main course folder.
2. ask_llm(...)  sends a question (a "prompt") to Google Gemini and returns the answer text.
3. embed(...)    turns sentences into lists of numbers (embeddings / vectors).

MOCK MODE
---------
If there is no API key, or the internet or the API fails, the helper does not crash.
It prints "[MOCK MODE]" and returns a pretend answer, so your notebook keeps running.
"""

import os
from pathlib import Path

import numpy as np

try:
    from dotenv import load_dotenv
except ImportError:  # python-dotenv not installed
    load_dotenv = None


# ---------------------------------------------------------------------------
# 1. Read the settings from the .env file
# ---------------------------------------------------------------------------
def _find_env_file():
    """Look for a .env file in this folder and in every parent folder."""
    here = Path.cwd()
    for folder in [here, *here.parents]:
        candidate = folder / ".env"
        if candidate.exists():
            return candidate
    return None


ENV_FILE = _find_env_file()
if ENV_FILE and load_dotenv:
    load_dotenv(ENV_FILE)

API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite").strip()
EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001").strip()

_client = None
_embedding_mode = None  # becomes "gemini" or "mock" after the first embed() call


def _get_client():
    """Create the Gemini client one time and reuse it."""
    global _client
    if _client is None:
        from google import genai

        _client = genai.Client(api_key=API_KEY)
    return _client


def status():
    """Print whether we are using the real AI or MOCK MODE."""
    if API_KEY:
        print(f"REAL AI MODE - model: {MODEL}")
        print(f"Settings read from: {ENV_FILE}")
    else:
        print("[MOCK MODE] No GEMINI_API_KEY found.")
        print("The code will still run with pretend answers.")
        print("To use the real AI, follow Day 2 Lesson 06 and create the .env file.")


# ---------------------------------------------------------------------------
# 2. Ask the LLM a question
# ---------------------------------------------------------------------------
def ask_llm(prompt, system=None, temperature=0.7, json_output=False, mock_answer=None):
    """
    Send a prompt to the AI model and return its answer as text.

    prompt       the user message (your question or instruction)
    system       optional system instruction (the AI's role and rules)
    temperature  0.0 = focused and repeatable, 1.0+ = more creative and random
    json_output  True = ask the model to answer only with JSON
    mock_answer  the pretend answer to use in MOCK MODE (text, or a function that gets the prompt)
    """
    if API_KEY:
        try:
            from google.genai import types

            config = types.GenerateContentConfig(
                system_instruction=system,
                temperature=temperature,
                response_mime_type="application/json" if json_output else None,
            )
            response = _get_client().models.generate_content(model=MODEL, contents=prompt, config=config)
            return response.text or ""
        except Exception as error:  # network problem, wrong key, limit reached...
            print(f"[AI ERROR] {type(error).__name__}: {str(error)[:200]}")
            print("Switching to MOCK MODE for this answer so you can continue.")

    print("[MOCK MODE] pretend answer (no API key, or the API call failed)")
    if callable(mock_answer):
        return mock_answer(prompt)
    if mock_answer is not None:
        return mock_answer
    return (
        "This is a pretend answer from MOCK MODE. "
        "Add your GEMINI_API_KEY to the .env file to get a real AI answer."
    )


# ---------------------------------------------------------------------------
# 3. Embeddings: text -> vector of numbers
# ---------------------------------------------------------------------------
def _mock_embed(texts):
    """
    Offline stand-in for real embeddings.
    It counts words (with a trick called "hashing"), so sentences that share words get
    similar vectors. Real embeddings also understand meaning and synonyms; this one does not.
    """
    from sklearn.feature_extraction.text import HashingVectorizer

    vectorizer = HashingVectorizer(n_features=4096, alternate_sign=False, norm="l2", stop_words="english")
    return vectorizer.transform(texts).toarray()


def embed(texts):
    """Turn a list of texts into a 2D numpy array: one row (vector) per text."""
    global _embedding_mode
    if isinstance(texts, str):
        texts = [texts]

    if API_KEY and _embedding_mode != "mock":
        try:
            vectors = []
            for start in range(0, len(texts), 50):  # send at most 50 texts per request
                batch = texts[start : start + 50]
                result = _get_client().models.embed_content(model=EMBEDDING_MODEL, contents=batch)
                vectors.extend(e.values for e in result.embeddings)
            _embedding_mode = "gemini"
            array = np.array(vectors, dtype=float)
            return array / np.linalg.norm(array, axis=1, keepdims=True)
        except Exception as error:
            print(f"[AI ERROR] {type(error).__name__}: {str(error)[:200]}")
            if _embedding_mode == "gemini":
                print("Earlier vectors came from Gemini. Restart the notebook and run all cells again.")
            print("Switching to MOCK embeddings (word counting) from now on.")

    if _embedding_mode != "mock":
        print("[MOCK MODE] using offline word-count vectors instead of real embeddings")
    _embedding_mode = "mock"
    return _mock_embed(texts)


def cosine_similarity(a, b):
    """How similar two vectors are: 1 = same direction, 0 = unrelated."""
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))
