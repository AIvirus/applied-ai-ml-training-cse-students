# Lesson 03 - GitHub: Push and Collaborate

**Time:** 35 minutes  |  **Folder:** `Day-03-AI-App-Vibe-Coding/my_study_buddy`  |  **You need:** a GitHub account

---

## Goal

By the end of this lesson:

- your project is on GitHub with its README,
- you can **push** new commits,
- you know **clone**, **branch**, **pull request** and **merge** - the basics of working in a team,
- you know what to do if a secret ever leaks.

---

## Understand

| Word | Meaning |
|---|---|
| **Remote** | A copy of your repository on another computer, here on GitHub. Its usual name is `origin`. |
| **Push** | Send your new commits from your laptop to GitHub. |
| **Pull** | Get new commits from GitHub to your laptop. |
| **Clone** | Download a full copy of a repository from GitHub for the first time. |
| **Branch** | A separate line of work. You build a feature on a branch without disturbing `main`. |
| **Pull request (PR)** | A request to merge a branch into `main`. Teammates review the changes and comment before merging. |
| **Merge** | Combine the commits of one branch into another. |

```text
main:      A---B-----------E   (E = merge commit)
                \         /
feature:         C-------D
```

---

## Do it now

### Step 1 - Create an empty repository on GitHub

1. Sign in at https://github.com.
2. Click **+** (top right) -> **New repository**.
3. Repository name: `study-buddy`.
4. Description: `AI learning and research assistant (FastAPI + Gemini)`.
5. Choose **Public** (needed for free deployment and for your portfolio) or **Private**.
6. Do **not** tick "Add a README", ".gitignore" or "license" - you already have them.
7. Click **Create repository**. GitHub shows a page with commands. Keep it open.

### Step 2 - Connect your project and push

In the terminal, in `my_study_buddy`. Replace `YOUR-USERNAME` with your GitHub username:

```powershell
git remote add origin https://github.com/YOUR-USERNAME/study-buddy.git
```

```powershell
git push -u origin main
```

**Signing in the first time:**

- **Windows:** a browser window opens (Git Credential Manager). Click **Sign in with your browser** and authorise. This happens only once.
- **macOS / Linux:** the easiest way is the GitHub CLI. Install it from https://cli.github.com, run `gh auth login`, choose **GitHub.com -> HTTPS -> Login with a web browser**, then run the `git push` command again.

GitHub no longer accepts your account password for `git push`. Use the browser sign-in or the GitHub CLI.

### Step 3 - Look at your repository

Refresh the GitHub page. You see your files and your README shown nicely below them. Click `app/main.py` to read it on GitHub. Click **commits** to see your history.

Check: is `.env` there? It must **not** be.

### Step 4 - Work on a branch

Let us add a small feature in a professional way.

```powershell
git switch -c add-footer-version
```

You are now on a new branch. In `app/static/index.html`, change the footer to:

```html
<footer>Study Buddy v1.1 - AI answers can be wrong. Always check important facts in your own notes.</footer>
```

Commit and push the branch:

```powershell
git add app/static/index.html
```

```powershell
git commit -m "Show version number in the footer"
```

```powershell
git push -u origin add-footer-version
```

### Step 5 - Open and merge a pull request

1. On GitHub, a yellow bar says **add-footer-version had recent pushes**. Click **Compare & pull request**.
2. Write a short description: what changed and how you tested it.
3. Click **Create pull request**.
4. Click the **Files changed** tab - this is what a reviewer reads. In a team, a classmate would comment here.
5. Click **Merge pull request -> Confirm merge**. Then **Delete branch**.

### Step 6 - Update your laptop

```powershell
git switch main
```

```powershell
git pull
```

```powershell
git log --oneline
```

Your local `main` now contains the merged change.

### Step 7 - Clone (how a teammate gets your project)

In a different folder (for example your Desktop), a teammate would run:

```powershell
git clone https://github.com/YOUR-USERNAME/study-buddy.git
```

They get all the code and history - but **not** your `.env`. They create their own from `.env.example`. That is exactly how secrets should work.

---

## Check

- [ ] Your repository on GitHub shows your files and README, and **no** `.env`.
- [ ] You merged a pull request from a branch.
- [ ] `git log --oneline` on your laptop shows the merge.

---

## What just happened?

Your code is now backed up online and shareable. You used the **branch -> pull request -> review -> merge** workflow that almost every software team uses. On Lesson 08, GitHub will also **test** every pull request automatically.

---

## Collaboration basics

- **Pull before you start working** (`git pull`), so you have your teammates' latest changes.
- **One branch per feature.** Small pull requests are easier to review.
- **Review kindly and clearly.** Comment on the code, not the person.
- **Merge conflicts** happen when two people change the same lines. Git marks them with `<<<<<<<` and `>>>>>>>`. Edit the file to keep the right version, remove the markers, then `git add` and `git commit`. VS Code shows buttons to help.

---

## If a secret ever leaks

If you accidentally push an API key to GitHub:

1. **Immediately delete the key** at https://aistudio.google.com/apikey and create a new one. This is the only real fix - assume the old key is stolen.
2. Remove the file from Git (`git rm --cached .env`), make sure `.gitignore` lists it, commit and push.
3. Put the new key only in `.env` (local) and in the host's environment settings (Lesson 07).

GitHub also has **secret scanning**, which may warn you about leaked keys.

---

## Try it yourself

1. Create another branch, make a change, open a PR, and ask a classmate to review it.
2. On GitHub, add a **description** and **topics** (`fastapi`, `rag`, `gemini`) to your repository (gear icon next to "About").

---

## If it does not work

| Problem | Fix |
|---|---|
| `remote origin already exists` | Run `git remote set-url origin https://github.com/YOUR-USERNAME/study-buddy.git` |
| `Authentication failed` / `Support for password authentication was removed` | Use the browser sign-in (Windows) or `gh auth login` (macOS / Linux). |
| `failed to push some refs ... (fetch first)` | GitHub has commits you do not have (for example you created a README there). Run `git pull --rebase origin main`, then push again. |
| `src refspec main does not match any` | You have no commits yet, or your branch is called `master`. Run `git branch` to check. |
| `Repository not found` | Check the username and repository name in the URL, and that you are signed in to the right account. |

Next: **[Lesson 04 - Docker basics](04_DOCKER_BASICS.md)**
