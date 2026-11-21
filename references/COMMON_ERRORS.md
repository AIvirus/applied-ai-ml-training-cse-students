# Common Errors and How to Fix Them

Read the error from the **bottom line up**: the last line says **what** went wrong, the lines above say **where**.

## Setup and Python

| Error | Cause | Fix |
|---|---|---|
| `'python' is not recognized` | Python not installed or not on PATH | Reinstall Python 3.12 and tick **Add python.exe to PATH**; reopen VS Code. Or use `py -3.12`. |
| `running scripts is disabled on this system` | PowerShell blocks the activate script | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, then activate again. |
| `ModuleNotFoundError: No module named 'pandas'` (or any package) | Wrong Python / `.venv` not active / wrong notebook kernel | Activate `.venv`; in notebooks choose the `.venv` kernel; run `pip install -r requirements.txt`. |
| `pip install` fails building a package | Python version too new for some packages | Use Python 3.12. Delete `.venv` and create it again with `py -3.12 -m venv .venv`. |
| `OSError ... long path` while installing | Windows path length limit | Put the course folder near the top of a drive (for example `D:\ai_course`), or enable long paths in Windows. |
| `FileNotFoundError: ... .csv` | Wrong current folder | Open notebooks from their `notebooks` folder; run Day 3 commands from `my_study_buddy`. |
| `NameError: name 'df' is not defined` | A notebook cell was skipped | **Restart** then **Run All**. |
| `IndentationError` | Mixed or wrong spaces | Use 4 spaces per level; let VS Code format the file. |

## Notebooks and Day 1 / Day 2 libraries

| Error | Cause | Fix |
|---|---|---|
| `ValueError: could not convert string to float: 'urban'` | Text column passed to a model | Encode categories first (one-hot) or drop the column. |
| `KeyError: 'final score'` | Column name typed wrongly | Check `df.columns`; names use underscores. |
| `ConvergenceWarning` | Model needs more iterations | Only a warning. Scale features or raise `max_iter`. |
| `LookupError: Resource punkt_tab not found` | NLTK data not downloaded | Run the NLTK download cell with internet. |
| `TesseractNotFoundError` | Tesseract program not installed | Install Tesseract (Day 2 Lesson 03) or skip OCR. |

## AI API (Gemini)

| Error | Cause | Fix |
|---|---|---|
| Always `[MOCK MODE]` | No key found | Create `.env` in the main course folder (or in `my_study_buddy`); restart the notebook kernel or server. |
| `400 API key not valid` | Key copied wrongly | Copy it again, no spaces or quotes. |
| `404 ... model ... not found` | Model name changed | Pick a current model at https://ai.google.dev/gemini-api/docs/models and set `GEMINI_MODEL`. |
| `429 RESOURCE_EXHAUSTED` | Free limit reached | Wait a minute (or until tomorrow); use mock mode meanwhile. |
| `403 PERMISSION_DENIED` / region not supported | Account or country not allowed | Use mock mode; ask your trainer. |
| `JSONDecodeError` / `ValidationError` on AI output | The model returned bad JSON | Ask for JSON only (`json_output=True`), validate, retry, fall back. |

## Day 3 app (FastAPI)

| Error | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'app'` | Wrong folder, or missing `app/__init__.py` | `cd` into `my_study_buddy`; create `app/__init__.py`. |
| `address already in use` / `[Errno 10048]` | Port 8000 is busy | Stop the other server (Ctrl + C) or use `--port 8001`. |
| `Form data requires "python-multipart"` | Package missing | `pip install -r requirements.txt` (`fastapi[standard]` includes it). |
| `422 Unprocessable Entity` | Request data failed validation | Read the `detail` field: it names the wrong field. |
| "Please upload a document first" after uploading | Server reloaded, memory cleared | Upload again. |
| `RuntimeError: Directory '.../static' does not exist` | Missing folder | Create `app/static` with the three files. |
| Page has no styles | `style.css` not served | Check `app.mount("/static", ...)` and the file location; press Ctrl + F5. |

## Git and GitHub

| Error | Cause | Fix |
|---|---|---|
| `Author identity unknown` | Git name/email not set | `git config --global user.name "..."` and `user.email`. |
| `.env` shows in `git status` | `.gitignore` missing or wrong | Fix `.gitignore`. If already committed: `git rm --cached .env`, commit, **create a new API key**. |
| `Support for password authentication was removed` | GitHub needs browser login or a token | Use Git Credential Manager (Windows) or `gh auth login`. |
| `failed to push some refs (fetch first)` | GitHub has commits you do not | `git pull --rebase origin main`, then push. |
| A strange editor opens on commit | `-m` missing | Type `:q!` and Enter, then commit with `-m "message"`. |

## Docker

| Error | Cause | Fix |
|---|---|---|
| `failed to connect to the docker API` / `Cannot connect to the Docker daemon` | Docker Desktop not running | Start Docker Desktop; wait for **Engine running**. |
| `port is already allocated` | Port in use | Stop the other process or container, or use `-p 8001:8000`. |
| `The container name "/buddy" is already in use` | Old container exists | `docker rm -f buddy` |
| `open .env: no such file` | Wrong folder or no `.env` | Run in `my_study_buddy`; create `.env`; or use `-e MOCK_MODE=true`. |
| App runs but browser cannot connect | Wrong host or port mapping | CMD must use `--host 0.0.0.0`; check `-p`. |

## Deployment (Render) and CI (GitHub Actions)

| Error | Cause | Fix |
|---|---|---|
| `Dockerfile not found` | Not at the repository root or not committed | Check the files on GitHub. |
| `No open ports detected` | App not listening on `$PORT` / `0.0.0.0` | Check the Dockerfile CMD. |
| Health check failed | Wrong path or app crashed | Path `/health`; read **Logs**. |
| Always mock answers online | Key missing or wrong in Render | Check **Environment**; read `Gemini call failed` in **Logs**. |
| No workflow in **Actions** | File in the wrong place | It must be `.github/workflows/ci.yml` at the repository root. |
| Tests fail only in CI | A file not committed, or a test depends on your `.env` | `git ls-files`; make tests use mock mode. |
