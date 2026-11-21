# Dockerfile - the recipe to build a container image of Study Buddy (Day 4, Lesson 05)

# 1. Start from a small official image that already has Python 3.12
FROM python:3.12-slim

# 2. Install the Tesseract program for the optional OCR feature
RUN apt-get update \
    && apt-get install -y --no-install-recommends tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# 3. All next commands run inside the /app folder of the container
WORKDIR /app

# 4. Install Python packages first (Docker caches this step, so rebuilds are faster)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy our application code
COPY app ./app

# 6. Do not run as the all-powerful root user (safer)
RUN useradd --create-home appuser
USER appuser

# 7. Settings. Cloud hosts set PORT themselves; 8000 is the default.
ENV PORT=8000 \
    PYTHONUNBUFFERED=1
EXPOSE 8000

# 8. Docker checks every 30 seconds that the app answers on /health
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s \
    CMD python -c "import os, urllib.request; urllib.request.urlopen(f'http://127.0.0.1:{os.environ.get(\"PORT\", \"8000\")}/health')" || exit 1

# 9. The command that starts the app when the container starts
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
