# Commands Cheat Sheet

All commands for the 4 days on one page. Windows PowerShell commands are shown first; macOS / Linux differences are noted.

## Virtual environment (run in the main course folder)

| Task | Command |
|---|---|
| Create | `python -m venv .venv` |
| Activate (Windows PowerShell) | `.venv\Scripts\Activate.ps1` |
| Activate (Windows Command Prompt) | `.venv\Scripts\activate.bat` |
| Activate (macOS / Linux) | `source .venv/bin/activate` |
| Install the course packages | `pip install -r requirements.txt` |
| List installed packages | `pip list` |
| Leave the environment | `deactivate` |

## Moving around the terminal

| Task | Windows PowerShell | macOS / Linux |
|---|---|---|
| Where am I? | `pwd` | `pwd` |
| List files | `ls` | `ls -la` |
| Go into a folder | `cd folder_name` | `cd folder_name` |
| Go up one folder | `cd ..` | `cd ..` |
| Make a folder | `mkdir name` | `mkdir -p name` |
| Copy a file | `Copy-Item source destination` | `cp source destination` |
| Copy a folder | `Copy-Item source -Recurse destination` | `cp -r source destination` |

## Notebooks (VS Code)

| Task | How |
|---|---|
| Run one cell | **Shift + Enter** |
| Run all cells | **Run All** button at the top |
| Restart (clear everything) | **Restart** button, then **Run All** |
| Choose the Python | **Select Kernel** (top right) -> **Python Environments** -> `.venv` |

## Day 2

| Task | Command |
|---|---|
| Create `.env` from the template (Windows) | `Copy-Item .env.example .env` |
| Create `.env` (macOS / Linux) | `cp .env.example .env` |
| Test your Gemini key | `python Day-02-Modern-AI-Domains/check_ai_key.py` |

## Day 3 (run in `my_study_buddy`)

| Task | Command |
|---|---|
| Start the app (auto-reload) | `uvicorn app.main:app --reload` |
| Start on another port | `uvicorn app.main:app --reload --port 8001` |
| Stop the app | **Ctrl + C** |
| Open the app | http://127.0.0.1:8000 |
| Open the API docs | http://127.0.0.1:8000/docs |
| Run all tests | `pytest -v` |
| Run tests whose name contains a word | `pytest -v -k ask` |

## Git

| Task | Command |
|---|---|
| Set your name and email (once) | `git config --global user.name "Your Name"` and `git config --global user.email "you@example.com"` |
| Start a repository | `git init -b main` |
| What changed? | `git status` and `git diff` |
| Stage files | `git add .` or `git add file_name` |
| Commit | `git commit -m "Clear message"` |
| Stage and commit changed tracked files | `git commit -am "Message"` |
| History | `git log --oneline` |
| Undo changes to a file | `git restore file_name` |
| Is a file ignored? | `git check-ignore -v .env` |
| Connect to GitHub | `git remote add origin https://github.com/USER/REPO.git` |
| First push | `git push -u origin main` |
| Later pushes | `git push` |
| Get new commits | `git pull` |
| New branch | `git switch -c branch-name` |
| Change branch | `git switch main` |
| Delete a local branch | `git branch -D branch-name` |
| Download a repository | `git clone https://github.com/USER/REPO.git` |

## Docker (run in `my_study_buddy`)

| Task | Command |
|---|---|
| Check Docker | `docker --version` and `docker run hello-world` |
| Build the image | `docker build -t study-buddy .` |
| Run (foreground) | `docker run --name buddy -p 8000:8000 --env-file .env study-buddy` |
| Run (background) | `docker run -d --name buddy -p 8000:8000 --env-file .env study-buddy` |
| Pass one setting | `-e MOCK_MODE=true` |
| Running containers | `docker ps` (add `-a` to include stopped ones) |
| Logs | `docker logs buddy` (add `-f` to follow) |
| Stop and remove | `docker rm -f buddy` |
| List images | `docker images` |
| Compose: start | `docker compose up --build` (add `-d` for background) |
| Compose: logs | `docker compose logs -f` |
| Compose: stop and remove | `docker compose down` |

## Checking a live app

| Task | Windows PowerShell | macOS / Linux |
|---|---|---|
| Health check | `Invoke-RestMethod https://YOUR-APP.onrender.com/health` | `curl https://YOUR-APP.onrender.com/health` |
