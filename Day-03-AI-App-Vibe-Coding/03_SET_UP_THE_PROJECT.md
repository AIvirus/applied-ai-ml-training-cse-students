# Lesson 03 - Set Up the Project

**Time:** 20 minutes  |  **You need:** the `.venv` from Day 1 Lesson 02

---

## Goal

By the end of this lesson you have:

- your own project folder `my_study_buddy` with the right structure,
- the package list, sample files and settings files in place,
- a private `.env` file with your API key (or mock mode),
- an architecture plan from your AI assistant, compared with Lesson 01.

---

## Understand

### The folder structure

```text
my_study_buddy/
|-- app/                 the Python package with all our code
|   |-- __init__.py      an empty file that tells Python "app is a package"
|   |-- config.py        (Lesson 04)
|   |-- llm.py           (Lesson 04)
|   |-- main.py          (Lesson 04, grows in every lesson)
|   |-- documents.py     (Lesson 05)
|   |-- store.py         (Lesson 05)
|   |-- study.py         (Lessons 06 and 07)
|   |-- csv_tools.py     (Lesson 08)
|   `-- static/          the web page (Lesson 09)
|-- tests/               automated tests (Lesson 10)
|-- sample_files/        notes and a CSV to try the app
|-- requirements.txt     the packages this project needs
|-- .env.example         a template for settings (safe to share)
|-- .env                 YOUR settings and API key (secret, never shared)
`-- .gitignore           tells Git to never upload .env (Day 4)
```

### Why a separate `requirements.txt` for the project?

The course's main `requirements.txt` has everything for all 4 days. On Day 4 we put **only this project** on GitHub, in Docker and on a cloud server. Those places need their own, smaller list. You already installed all these packages on Day 1, so nothing new is downloaded today.

---

## Do it now

### Step 1 - Open a terminal in the right place

1. In VS Code (with the main course folder open), open **Terminal -> New Terminal**.
2. Check that the line starts with `(.venv)`. If not, activate it (Day 1 Lesson 02, Step 7):

```powershell
.venv\Scripts\Activate.ps1
```

3. Go into the Day 3 folder:

```powershell
cd Day-03-AI-App-Vibe-Coding
```

### Step 2 - Create the project folders

**Windows (PowerShell):**

```powershell
mkdir my_study_buddy
```

```powershell
cd my_study_buddy
```

```powershell
mkdir app, app\static, tests
```

```powershell
New-Item app\__init__.py
```

**macOS / Linux:**

```bash
mkdir -p my_study_buddy/app/static my_study_buddy/tests && cd my_study_buddy && touch app/__init__.py
```

The terminal line should now end with `my_study_buddy>`. **From now on, run every Day 3 command from this folder.**

### Step 3 - Copy the starter files from the answer key

These files are not "code to learn", so we copy them. Run each line:

**Windows (PowerShell):**

```powershell
Copy-Item ..\study_buddy_lab\requirements.txt .
```

```powershell
Copy-Item ..\study_buddy_lab\.env.example .
```

```powershell
Copy-Item ..\study_buddy_lab\.gitignore .
```

```powershell
Copy-Item ..\study_buddy_lab\sample_files -Recurse .
```

**macOS / Linux:**

```bash
cp ../study_buddy_lab/requirements.txt ../study_buddy_lab/.env.example ../study_buddy_lab/.gitignore . && cp -r ../study_buddy_lab/sample_files .
```

Open `requirements.txt` in VS Code and read it: every line says what the package is for.

### Step 4 - Install (or confirm) the packages

```powershell
pip install -r requirements.txt
```

You should see many lines saying `Requirement already satisfied`. That is good.

### Step 5 - Create your private `.env` file

**Windows (PowerShell):**

```powershell
Copy-Item .env.example .env
```

**macOS / Linux:**

```bash
cp .env.example .env
```

Open `.env` in VS Code:

- If you have a Gemini key (Day 2 Lesson 06): paste it after `GEMINI_API_KEY=`.
- If you do not: leave the key empty. The app will run in mock mode.
- Want mock mode even with a key (to save your free quota while testing)? Set `MOCK_MODE=true`.

Save the file.

### Step 6 - Ask your AI assistant for an architecture plan

Open your AI assistant chat and send:

```text
I want to build "Study Buddy", a FastAPI web app (Python 3.12) for students:
upload notes (.txt, .md, .pdf), ask questions answered only from the notes with sources (RAG),
get summaries and practice questions, and upload a CSV to get insights and a chart.
It uses Google Gemini through the google-genai package, with a mock mode when there is no API key.
Search uses TF-IDF from scikit-learn. The frontend is plain HTML, CSS and JavaScript.

Propose: the folder structure, one sentence for what each file does, the API endpoints
(method + path + purpose), and the order in which to build the features in small steps.
Do not write code yet.
```

Compare its answer with Lesson 01. Different names are fine. Ask yourself: does each file have **one clear job**? Is the key kept on the server?

---

## Check

- [ ] The terminal line ends with `my_study_buddy>` and starts with `(.venv)`.
- [ ] `my_study_buddy` contains `app/__init__.py`, `app/static/`, `tests/`, `sample_files/`, `requirements.txt`, `.env.example`, `.env` and `.gitignore`.
- [ ] `.env` is listed inside `.gitignore`.
- [ ] Your AI assistant proposed a plan, and you compared it with Lesson 01.

---

## What just happened?

You created a clean, professional project layout, separated **shareable settings** (`.env.example`) from **secret settings** (`.env`), and used the AI as a **planning partner** before writing any code.

---

## Try it yourself

1. Ask your assistant: "Why should `.env` be in `.gitignore` but `.env.example` should not?" Check that its answer matches Day 2 Lesson 06.

---

## If it does not work

| Problem | Fix |
|---|---|
| `Copy-Item : Cannot find path` | You are in the wrong folder. The line must end with `my_study_buddy>`. Use `cd` to move, or `pwd` to see where you are. |
| `mkdir : An item with the specified name already exists` | You already created it. Continue with the next command. |
| `.env` does not appear in the Explorer | Files starting with a dot are sometimes hidden. It is still there; open it with **File -> Open File**. |

Next: **[Lesson 04 - Step 1: first API and health check](04_STEP_1_FIRST_API_AND_HEALTH.md)**
