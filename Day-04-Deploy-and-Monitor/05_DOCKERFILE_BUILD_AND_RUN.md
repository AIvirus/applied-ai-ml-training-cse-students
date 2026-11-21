# Lesson 05 - Dockerfile: Build and Run

**Time:** 35 minutes  |  **Folder:** `Day-03-AI-App-Vibe-Coding/my_study_buddy`  |  **You need:** Docker running (Lesson 04)

---

## Goal

By the end of this lesson you can:

- read every line of a **Dockerfile**,
- **build** an image of Study Buddy,
- **run** it as a container with **port mapping** and **environment variables**,
- see its logs, stop it and remove it.

---

## Understand

### Port mapping

Inside the container, the app listens on port 8000. The container is like a separate small computer, so your browser cannot reach that port until you **map** it:

```text
-p 8000:8000
   |     |
   |     `-- port INSIDE the container
   `-------- port on YOUR computer
```

`-p 9000:8000` would make the app available at http://127.0.0.1:9000.

### Environment variables in containers

We **never** copy `.env` into the image (it is listed in `.dockerignore`). An image might be shared or uploaded; secrets inside it would leak. Instead we give the settings **when the container starts**:

- one by one: `-e MOCK_MODE=true`
- from a file: `--env-file .env`

Cloud hosts do the same: you type the variables in their dashboard (Lesson 07).

### Layers and caching

Each line of a Dockerfile creates a **layer**. Docker re-uses (caches) layers that did not change. That is why we copy `requirements.txt` and install packages **before** copying our code: when you change only your code, the slow `pip install` step is not repeated.

---

## Do it now

### Step 1 - Copy the Dockerfile and .dockerignore

In `my_study_buddy`:

**Windows (PowerShell):**

```powershell
Copy-Item ..\study_buddy_lab\Dockerfile .
```

```powershell
Copy-Item ..\study_buddy_lab\.dockerignore .
```

**macOS / Linux:**

```bash
cp ../study_buddy_lab/Dockerfile ../study_buddy_lab/.dockerignore .
```

### Step 2 - Read the Dockerfile line by line

```dockerfile
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
```

| Line | What it does |
|---|---|
| `FROM python:3.12-slim` | Start from an official small Linux image with Python 3.12 |
| `RUN apt-get ... tesseract-ocr` | Install the Tesseract program for OCR, then delete the download lists to keep the image small |
| `WORKDIR /app` | Work in the folder `/app` inside the image |
| `COPY requirements.txt .` then `RUN pip install ...` | Install packages first, so this slow layer is cached |
| `COPY app ./app` | Copy only our code (not tests, not `.env`) |
| `useradd` + `USER appuser` | Run as a normal user, not the all-powerful root - safer if the app is attacked |
| `ENV PORT=8000` | Default port. Cloud hosts like Render set their own `PORT`, and our start command uses it |
| `HEALTHCHECK` | Docker calls `/health` every 30 seconds and marks the container healthy or unhealthy |
| `CMD [...]` | The command that runs when a container starts: uvicorn on `0.0.0.0` (all network interfaces), so it can be reached from outside the container |

And the `.dockerignore` file (what Docker must **not** copy):

```text
# Files Docker must NOT copy into the image
.env
.venv/
venv/
__pycache__/
*.pyc
.pytest_cache/
.git/
.github/
tests/
sample_files/
```

### Step 3 - Build the image

```powershell
docker build -t study-buddy .
```

- `-t study-buddy` gives the image a name (a **tag**).
- `.` means "use the Dockerfile in this folder".

The first build takes 2 to 6 minutes (it downloads Python and installs packages). At the end you see `naming to docker.io/library/study-buddy`.

```powershell
docker images study-buddy
```

### Step 4 - Run a container

Make sure your local uvicorn server is **stopped** (Ctrl + C), because it also uses port 8000.

```powershell
docker run --name buddy -p 8000:8000 --env-file .env study-buddy
```

You see uvicorn's startup lines. Open http://127.0.0.1:8000 - it is Study Buddy, running **inside a container**. Try uploading a file and asking a question.

Press **Ctrl + C** to stop it.

### Step 5 - Run it in the background and read the logs

```powershell
docker rm buddy
```

```powershell
docker run -d --name buddy -p 8000:8000 --env-file .env study-buddy
```

`-d` = detached (runs in the background). Now:

```powershell
docker ps
```

After about 30 seconds the STATUS column shows `(healthy)` - that is the HEALTHCHECK calling `/health`.

```powershell
docker logs buddy
```

Use the app in the browser, then run `docker logs buddy` again: you see one log line per request, from our middleware.

To follow the logs live (press Ctrl + C to stop following):

```powershell
docker logs -f buddy
```

### Step 6 - Pass a single environment variable

```powershell
docker rm -f buddy
```

```powershell
docker run -d --name buddy -p 8000:8000 -e MOCK_MODE=true study-buddy
```

Open http://127.0.0.1:8000/health - it says `"ai_mode": "mock"`.

### Step 7 - Clean up

```powershell
docker rm -f buddy
```

Commit the new files:

```powershell
git add Dockerfile .dockerignore
```

```powershell
git commit -m "Add Dockerfile"
```

```powershell
git push
```

---

## Check

- [ ] `docker build` finished without errors.
- [ ] Study Buddy worked at http://127.0.0.1:8000 while running in a container.
- [ ] `docker ps` showed `(healthy)`.
- [ ] `docker logs buddy` showed request log lines.
- [ ] `-e MOCK_MODE=true` changed `/health` to mock mode.

---

## What just happened?

You turned your project into a **portable image**. Any computer or cloud server with Docker can now run Study Buddy exactly the same way. Secrets stayed outside the image and were given at start time.

---

## Try it yourself

1. Run two containers at once from the same image, on ports 8000 and 8001 (`-p 8001:8000`, different `--name`). Open both. Upload a file in one - does the other see it? (No - each container has its own memory.)
2. Change a word in `index.html`, rebuild, and notice that the `pip install` step says `CACHED`.

---

## If it does not work

| Problem | Fix |
|---|---|
| `failed to connect to the docker API` | Start Docker Desktop and wait for **Engine running**. |
| `Bind for 0.0.0.0:8000 failed: port is already allocated` | Something else uses port 8000 (your uvicorn, or an old container). Stop it, or use `-p 8001:8000`. Run `docker ps` to see running containers. |
| `Conflict. The container name "/buddy" is already in use` | Remove the old one: `docker rm -f buddy` |
| `open .env: The system cannot find the file specified` | Run the command in `my_study_buddy`, where `.env` is. Or use `-e MOCK_MODE=true` instead. |
| The page does not load but the container runs | Check the `-p` mapping, and that the CMD uses `--host 0.0.0.0` (not 127.0.0.1). |
| Build fails at `pip install` | Read the error. Often a network problem - run the build again. |

Next: **[Lesson 06 - Docker Compose](06_DOCKER_COMPOSE.md)**
