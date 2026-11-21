# Lesson 08 - CI/CD with GitHub Actions

**Time:** 30 minutes  |  **Folder:** `Day-03-AI-App-Vibe-Coding/my_study_buddy`

---

## Goal

By the end of this lesson:

- you can explain **Continuous Integration** and **Continuous Delivery / Deployment**,
- GitHub automatically runs your tests and builds your Docker image on every push,
- you have seen a failing check stop a bad change,
- you understand how code changes flow to the live app.

---

## Understand

### CI - Continuous Integration

Every time someone pushes code, a robot **automatically** installs the project and **runs the tests**. If something is broken, everyone knows within minutes, with a red cross next to the commit.

### CD - Continuous Delivery and Continuous Deployment

- **Continuous Delivery:** every change that passes CI is **ready** to deploy; a person clicks "deploy".
- **Continuous Deployment:** every change that passes CI is deployed **automatically**.

Render's auto-deploy (Lesson 07) is continuous deployment. Today we connect it with CI so that **only tested code** reaches the live app:

```text
git push --> GitHub Actions: install -> pytest -> docker build --> all green? --> Render deploys
                                                                  any red?    --> nothing deployed, you get an email
```

### GitHub Actions words

| Word | Meaning |
|---|---|
| **Workflow** | An automated process, written in a YAML file in `.github/workflows/` |
| **Trigger** (`on:`) | What starts it, for example `push` or `pull_request` |
| **Job** | A group of steps that run on one fresh virtual computer (a **runner**) |
| **Step** | One command (`run:`) or a ready-made action (`uses:`) |

GitHub Actions is free for public repositories, and private repositories get a free monthly allowance of minutes.

---

## Do it now

### Step 1 - Add the workflow file

In `my_study_buddy`:

**Windows (PowerShell):**

```powershell
Copy-Item ..\study_buddy_lab\.github -Recurse .
```

**macOS / Linux:**

```bash
cp -r ../study_buddy_lab/.github .
```

The file is `.github/workflows/ci.yml`. Read it:

```yaml
# GitHub Actions workflow (Day 4, Lesson 08)
# Runs automatically on every push and pull request:
#   1. installs the packages and runs the tests (in mock mode, so no API key is needed)
#   2. if the tests pass, checks that the Docker image still builds
name: CI

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Get the code
        uses: actions/checkout@v4

      - name: Install Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install packages
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest -v
        env:
          MOCK_MODE: "true"

  docker-build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Get the code
        uses: actions/checkout@v4

      - name: Build the Docker image
        run: docker build -t study-buddy .
```

Notice:

- Tests run with `MOCK_MODE: "true"`, so **no API key is needed in CI** and nothing secret is involved.
- The `docker-build` job has `needs: test` - it runs only if the tests pass.

### Step 2 - Push and watch

```powershell
git add .github
```

```powershell
git commit -m "Add CI workflow"
```

```powershell
git push
```

On GitHub, open your repository -> **Actions** tab. You see the workflow running (yellow circle). Click it to watch each step and its output. After 1 to 3 minutes both jobs show a **green tick**.

Go to the **Code** tab: your latest commit now has a green tick next to it.

### Step 3 - See CI catch a bug

Let us push a bug on a **branch**, like a real team would:

```powershell
git switch -c broken-search
```

Open `app/store.py` and in `search` change `scores[i] > 0` to `scores[i] > 1` (the bug from Day 3 Lesson 10). Then:

```powershell
git commit -am "Try a change to search"
```

```powershell
git push -u origin broken-search
```

Open a **pull request** for `broken-search` on GitHub. After a minute the PR shows **Some checks were not successful** with a red cross. Click **Details** to see exactly which test failed and why - the same output as `pytest` on your laptop.

This is CI protecting `main`: a reviewer would never merge this PR.

Close the PR without merging (**Close pull request**), then go back:

```powershell
git switch main
```

```powershell
git branch -D broken-search
```

### Step 4 - Deploy only after CI passes (CD)

In your Render service: **Settings -> Build & Deploy -> Auto-Deploy**, choose **After CI Checks Pass** (if your plan shows this option). Now Render waits for the green tick before deploying.

### Step 5 - The full loop

Make a small visible change (for example the subtitle in `index.html`), commit and push to `main`. Watch:

1. GitHub Actions runs tests -> green.
2. Render starts a deploy automatically.
3. A few minutes later, the change is live at your `onrender.com` link.

You changed code, and **robots tested and deployed it**.

---

## Check

- [ ] The **Actions** tab shows a successful run with two jobs: `test` and `docker-build`.
- [ ] The broken branch showed a red cross in its pull request.
- [ ] A push to `main` was deployed automatically to Render.

---

## What just happened?

You built a real **CI/CD pipeline**. This is how professional teams ship software many times a day without breaking it: every change is tested automatically, and only passing changes go live.

---

## Try it yourself

1. Add a **status badge** to your README. On GitHub: **Actions -> CI -> ... (top right) -> Create status badge -> Copy status badge Markdown**, and paste it at the top of `README.md`.
2. Add a step that checks code style: add `ruff` to `requirements.txt` and a step `run: ruff check app` (ask your AI assistant what ruff does first).

---

## If it does not work

| Problem | Fix |
|---|---|
| No workflow appears in **Actions** | The file must be exactly at `.github/workflows/ci.yml` in the **root** of the repository (next to `README.md`). |
| `ERROR: Could not open requirements file` | Same: the workflow runs at the repository root, so `requirements.txt` must be there. |
| Tests pass locally but fail in CI | Often a missing file in Git (for example `sample_files/` not committed - check `git ls-files sample_files`), or a test that depends on your `.env`. |
| YAML error | Indentation must use **spaces**, exactly as in the file. Compare with the lab file. |

Next: **[Lesson 09 - Logs, monitoring and troubleshooting](09_LOGS_MONITORING_AND_TROUBLESHOOTING.md)**
