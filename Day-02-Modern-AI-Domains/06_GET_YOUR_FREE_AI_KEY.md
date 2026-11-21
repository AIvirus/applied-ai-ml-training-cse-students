# Lesson 06 - Get Your Free AI API Key

**Time:** 15 minutes  |  **You need:** a Google account, internet

---

## Goal

By the end of this lesson:

- you have a free **Gemini API key**,
- it is saved safely in a private `.env` file,
- a small test script confirms that Python can talk to the AI.

---

## Understand

### What is an API?

An **API** (Application Programming Interface) is a way for **one program to ask another program for something**.

Think of a restaurant: you (your Python code) do not walk into the kitchen (Google's servers). You give your order to the **waiter** (the API). The waiter brings back your food (the AI's answer).

### What is an API key?

An **API key** is a long secret password for programs, like `AIzaSyB...`. It tells Google **who** is calling, so it can apply your free limits.

**Treat it like your ATM PIN:**

- Never share it in chat groups, screenshots or emails.
- Never type it directly inside a notebook or `.py` file.
- Never upload it to GitHub (bots scan GitHub for keys within minutes).
- If it leaks, delete it in Google AI Studio and create a new one.

### What is a `.env` file?

A small text file named exactly **`.env`** that holds secrets, one per line:

```text
GEMINI_API_KEY=AIzaSy...your key...
```

Our code reads it with the `python-dotenv` package. The course's `.gitignore` file already makes Git **ignore** `.env`, so it is never uploaded.

### About the free tier

- Google gives a free tier with **limits** (a number of requests per minute and per day). If you hit the limit you get an error like `429 RESOURCE_EXHAUSTED`. Wait a minute and try again. Our notebooks fall back to MOCK MODE automatically.
- On the free tier, Google may use what you send to improve its products. **Do not send private or personal data** (yours or anyone else's).
- Google's terms require API users to be **18 or older**. If you are younger, use **MOCK MODE** or ask your trainer to run the live demos.

---

## Do it now

### Step 1 - Create the key

1. Open https://aistudio.google.com/apikey in your browser.
2. Sign in with your Google account. Accept the terms if asked (read them first).
3. Click **Create API key**. If it asks for a project, choose **Create API key in new project** (or pick the default project).
4. Copy the key (it starts with `AIza`). Keep this page open for a minute.

### Step 2 - Create your `.env` file

In VS Code, make sure the terminal is in the **main course folder** (the line ends with `Applied_AI_ML_Training_Proposal_CSE_Students>`). Then copy the template:

**Windows (PowerShell):**

```powershell
Copy-Item .env.example .env
```

**macOS / Linux:**

```bash
cp .env.example .env
```

Open the new `.env` file in VS Code (it is in the Explorer on the left, at the top level). Paste your key after the `=` sign, with no spaces and no quotes:

```text
GEMINI_API_KEY=AIzaSyYourKeyGoesHere
GEMINI_MODEL=gemini-3.5-flash-lite
GEMINI_EMBEDDING_MODEL=gemini-embedding-001
```

Save the file (**Ctrl + S**).

### Step 3 - Test it

With `(.venv)` active, from the main course folder, run:

```powershell
python Day-02-Modern-AI-Domains/check_ai_key.py
```

---

## Check

You should see something like:

```text
Found .env file: D:\Applied_AI_ML_Training_Proposal_CSE_Students\.env
Key found: AIza...Xy12 (39 characters)
Model: gemini-3.5-flash-lite
Asking the AI a test question...
AI answered: Hello! Your key works.
SUCCESS - your API key works.
```

If you see `SUCCESS`, you are done. If not, read the error and the table below.

---

## What just happened?

- The script found your `.env` file and read the key (it prints only the first and last 4 characters, never the full key).
- It sent one small prompt to Google's Gemini API.
- Gemini sent back an answer.

---

## Try it yourself

1. Open `check_ai_key.py` and read it. Find the line that sends the question.
2. Change the test question to "Say hello in Hindi" and run it again.
3. Check that `.env` is listed in the `.gitignore` file in the main folder.

---

## If it does not work

| Problem | Fix |
|---|---|
| `No .env file found` | The file must be named exactly `.env` (not `.env.txt`, not `env`) and be in the **main course folder**. On Windows, turn on **View -> File name extensions** in File Explorer to see the real name. |
| `GEMINI_API_KEY is empty` | Paste the key after `=` and **save** the file. |
| `400 API key not valid` | The key was copied wrongly (a missing letter, or extra space). Copy it again. |
| `404 ... model ... is not found` | Model names change over time. Open https://ai.google.dev/gemini-api/docs/models, copy the name of a current **Flash** or **Flash-Lite** model, and put it in `GEMINI_MODEL` in `.env`. |
| `429 RESOURCE_EXHAUSTED` | Free limit reached. Wait one minute (or until tomorrow for the daily limit). Mock mode still works. |
| `403 PERMISSION_DENIED` or "not available in your region" | The free API may not be available for your account or country. Use MOCK MODE, or ask your trainer. |
| Network or SSL error | Check the internet. College networks sometimes block APIs - try a mobile hotspot. |

Next: **[Lesson 07 - Prompts and model APIs](07_PROMPTS_AND_MODEL_APIS.md)**
