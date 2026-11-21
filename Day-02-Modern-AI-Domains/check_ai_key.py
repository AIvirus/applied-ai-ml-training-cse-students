"""
check_ai_key.py - checks that your Gemini API key works.

Run it from the main course folder, with (.venv) active:
    python Day-02-Modern-AI-Domains/check_ai_key.py
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# 1. Find the .env file (in the current folder or any parent folder)
env_file = None
for folder in [Path.cwd(), *Path.cwd().parents]:
    if (folder / ".env").exists():
        env_file = folder / ".env"
        break

if env_file is None:
    print("No .env file found. Create it in the main course folder (Lesson 06, Step 2).")
    sys.exit(1)

print("Found .env file:", env_file)
load_dotenv(env_file)

# 2. Read the key and the model name
key = os.getenv("GEMINI_API_KEY", "").strip()
model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite").strip()

if not key:
    print("GEMINI_API_KEY is empty. Paste your key after the = sign in .env and save the file.")
    sys.exit(1)

# Show only the start and the end of the key - never print a full secret
print(f"Key found: {key[:4]}...{key[-4:]} ({len(key)} characters)")
print("Model:", model)

# 3. Ask one small question
print("Asking the AI a test question...")
try:
    from google import genai

    client = genai.Client(api_key=key)
    response = client.models.generate_content(
        model=model,
        contents="Reply with exactly this sentence: Hello! Your key works.",
    )
    print("AI answered:", response.text.strip())
    print("SUCCESS - your API key works.")
except Exception as error:
    print("FAILED:", type(error).__name__)
    print(str(error)[:500])
    print("See the 'If it does not work' table in Lesson 06.")
    sys.exit(1)
