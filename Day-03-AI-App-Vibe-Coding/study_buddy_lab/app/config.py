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
