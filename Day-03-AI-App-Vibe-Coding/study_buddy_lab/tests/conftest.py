"""
conftest.py - pytest runs this file first.

We force MOCK MODE for tests, so tests never use your API key, never need the internet,
and always give the same results. This must happen BEFORE the app is imported.
"""

import os
import sys
from pathlib import Path

os.environ["MOCK_MODE"] = "true"
os.environ["GEMINI_API_KEY"] = ""

# Make "import app" work when pytest is started from the project folder
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
