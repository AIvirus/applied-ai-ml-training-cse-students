# Lesson 02 - Git Basics

**Time:** 35 minutes  |  **Folder:** `Day-03-AI-App-Vibe-Coding/my_study_buddy`

---

## Goal

By the end of this lesson you can:

- explain **version control**, **repository**, **working tree**, **staging area** and **commit**,
- install and configure Git,
- make your project a Git repository with a first commit,
- keep secrets (`.env`) out of Git.

---

## Understand

### 1. Version control

Have you ever saved files like `project_final.py`, `project_final2.py`, `project_REALLY_final.py`? **Version control** solves this properly. It records **every saved version** of your project, who changed what and why, and lets you go back in time.

**Git** is the most used version control system in the world. **GitHub** (next lesson) is a website that stores Git projects online.

### 2. The words

| Word | Meaning | School example |
|---|---|---|
| **Repository (repo)** | A project folder whose history is tracked by Git (the history lives in a hidden `.git` folder) | Your notebook with all past versions kept |
| **Working tree** | The files as they are right now on your disk | The page you are writing on |
| **Staging area** | The changes you have **chosen** to save in the next commit | Pages you put in the "to submit" tray |
| **Commit** | A saved snapshot of the staged changes, with a message | Submitting the tray with a note "Finished chapter 3" |
| **Log / history** | The list of all commits | The list of all submissions |

### 3. The three steps

```text
 working tree  --git add-->  staging area  --git commit-->  repository history
 (edit files)                (choose)                      (save forever)
```

### 4. Secrets and `.gitignore`

Once a secret is committed, it is in the history **forever**, even if you delete the file later. If you push it to GitHub, bots can find it within minutes.

The `.gitignore` file lists files Git must **ignore**. Ours contains `.env`, `.venv/` and `__pycache__/`. Check it **before** your first commit.

---

## Do it now

### Step 1 - Install Git

- **Windows:** download from https://git-scm.com/downloads and install with default options. Close and reopen VS Code.
- **macOS:** open Terminal and run `git --version`. If Git is missing, macOS offers to install the developer tools - click **Install**.
- **Linux (Ubuntu):** `sudo apt install git`

Check:

```powershell
git --version
```

You should see something like `git version 2.47.0`.

### Step 2 - Tell Git who you are (once per computer)

Use your name and the email you will use for GitHub:

```powershell
git config --global user.name "Your Name"
```

```powershell
git config --global user.email "you@example.com"
```

### Step 3 - Turn your project into a repository

In the terminal, go to your project:

```powershell
cd Day-03-AI-App-Vibe-Coding\my_study_buddy
```

```powershell
git init -b main
```

`-b main` names the main branch `main`. You see `Initialized empty Git repository in .../my_study_buddy/.git/`.

### Step 4 - Check that secrets are ignored

```powershell
git status
```

Read the list of **untracked files**. You must see `app/`, `tests/`, `README.md`, `requirements.txt`, `.env.example`, `.gitignore`... and you must **not** see `.env` or `.venv`.

Double-check with:

```powershell
git check-ignore -v .env
```

It should print `.gitignore:2:.env  .env` (Git is ignoring `.env` because of line 2 of `.gitignore`). If it prints nothing, **stop** and fix `.gitignore` first.

### Step 5 - Stage and commit

```powershell
git add .
```

```powershell
git status
```

Now the files are listed under **Changes to be committed** (staged). Commit them:

```powershell
git commit -m "First version of Study Buddy"
```

### Step 6 - See the history

```powershell
git log --oneline
```

You see one line: a short ID (like `a1b2c3d`) and your message.

### Step 7 - Make a second commit

1. Open `README.md` and add a line at the end: `Made by <your name> during the Applied AI course.`
2. Run these commands one by one and read the output of each:

```powershell
git status
```

```powershell
git diff
```

```powershell
git add README.md
```

```powershell
git commit -m "Add author line to README"
```

```powershell
git log --oneline
```

`git diff` showed exactly what changed (green `+` = added line, red `-` = removed line). Now the log has 2 commits.

---

## Check

- [ ] `git log --oneline` shows 2 commits.
- [ ] `git status` says `nothing to commit, working tree clean`.
- [ ] `git ls-files` lists your code files and does **not** list `.env`.

---

## What just happened?

Your project now has a **history**. Each commit is a safe point you can return to. If an AI assistant breaks your code tomorrow, you can see exactly what changed (`git diff`) and undo it.

---

## Try it yourself

1. Change something in `style.css`, then undo it with `git restore app/static/style.css`. The file goes back to the last commit.
2. Write good commit messages. Which is better: `"update"` or `"Show sources under each answer"`? Why?
3. Commit after every working feature from now on. Small commits with clear messages are a professional habit.

---

## If it does not work

| Problem | Fix |
|---|---|
| `git` is not recognized | Install Git, then **close and reopen VS Code** so the terminal sees it. |
| `Author identity unknown` | Run the two `git config` commands in Step 2. |
| `.env` appears in `git status` | `.gitignore` is missing or wrong. Copy it again from `study_buddy_lab` and check line `.env` exists. If you already committed `.env`, run `git rm --cached .env`, commit, and **create a new API key** (the old one is in the history). |
| `fatal: not a git repository` | You are in the wrong folder, or you skipped `git init`. |
| Git opens a strange editor (Vim) when you commit | You forgot `-m "message"`. Type `:q!` and press Enter to leave, then commit again with `-m`. |

Next: **[Lesson 03 - GitHub: push and collaborate](03_GITHUB_PUSH_AND_COLLABORATE.md)**
