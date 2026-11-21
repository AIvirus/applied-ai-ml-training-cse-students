# Lesson 02 - Vibe Coding the Right Way

**Time:** 30 minutes  |  **You need:** VS Code, internet, an AI coding assistant (options below)

---

## Goal

By the end of this lesson you will:

- know what **vibe coding** (AI-assisted development) is - and its dangers,
- have an **AI coding assistant** ready to use,
- know the **safe workflow** we use for every feature today,
- have **prompt templates** for building, explaining, debugging, testing and reviewing code.

---

## Understand

### 1. What is vibe coding?

**Vibe coding** means building software by **describing what you want in normal language** and letting an AI write the code. The term became popular in 2025. Today almost every professional developer uses AI assistants every day.

**The good:** much faster, great for learning, removes boring work, explains unfamiliar code.

**The danger:** if you accept code you do not understand, you get apps that look fine but have hidden bugs, security holes, made-up packages, leaked API keys and code nobody can fix.

> **In this course, vibe coding is an engineering workflow, not a replacement for understanding.**
> You are the engineer. The AI is a fast but sometimes careless assistant. You must **read, run, test and explain** every piece of code before you keep it.

### 2. AI coding assistants you can use

Pick **one**. Free plans and student offers change over time, so check each website for current terms.

| Tool | Type | Notes |
|---|---|---|
| **GitHub Copilot** (in VS Code) | Chat + edits inside the editor | Has a free plan; free Pro access for verified students through GitHub Education |
| **Gemini Code Assist** (in VS Code) | Chat + edits inside the editor | Free for individuals with a Google account |
| **Claude Code**, **Cursor**, **Windsurf** and similar | Agent-style tools that can edit many files and run commands | Powerful; free tiers vary |
| **Gemini, ChatGPT or Claude in the browser** | Chat only | Works anywhere. You copy code into VS Code yourself. |
| **No assistant at all** | - | Every lesson shows the **reference code**. Type it yourself - you will still learn everything. |

**Quick setup for GitHub Copilot in VS Code:**

1. Create a free account at https://github.com (you need it on Day 4 anyway).
2. In VS Code, open the **Extensions** panel, search **GitHub Copilot**, install it (it also installs **GitHub Copilot Chat**).
3. Click the **Accounts** icon (bottom left) and **sign in with GitHub**. Choose the free plan if asked.
4. Open the chat with **Ctrl + Alt + I** (or click the chat icon at the top). You can type questions or ask it to edit files.

### 3. The safe workflow (use it for every feature)

```text
 1. PLAN      Decide ONE small feature. Write what "done" means.
 2. PROMPT    Ask for that feature only. Give context: files, rules, examples.
 3. READ      Read every line. Ask the AI to explain anything you do not understand.
 4. CHECK     Packages real? Secrets safe? Inputs checked? Errors handled?
 5. RUN       Run it. Try a normal input AND bad inputs.
 6. DEBUG     If it fails, give the AI the EXACT error message and the code. Verify the fix.
 7. TEST      Add or run automated tests.
 8. SAVE      Commit it (Day 4) before starting the next feature.
```

**Small steps are the secret.** One big prompt like "build me a full AI study app" gives you 1,000 lines you cannot understand or fix. Seven small prompts give you seven pieces you understand and have tested.

### 4. Rules for responsible vibe coding

1. **Never paste secrets** (API keys, passwords, `.env` contents) into an AI chat.
2. **Check that packages really exist.** AI sometimes invents package names. Attackers publish fake packages with those names ("slopsquatting"). Only install packages you have checked on https://pypi.org.
3. **Do not trust, verify.** AI can produce code that runs but is wrong. Test with real and bad inputs.
4. **Use real error messages.** "It doesn't work" gives bad fixes. Copy the full red error text.
5. **Keep it simple.** If the AI adds complex things you did not ask for (databases, logins, extra libraries), ask it to remove them.
6. **You must be able to explain it.** If you cannot explain a function to a friend, you do not own it yet. Ask the AI: "Explain this function line by line for a beginner."
7. **Respect licences and rules.** Follow your college's rules about AI use, and say honestly that you used an AI assistant.

### 5. Prompt templates

Copy these and fill in the brackets.

**A. Build a feature**

```text
I am building "Study Buddy", a FastAPI app in Python 3.12. Project structure:
<paste the folder tree or describe the files>

Task: <ONE feature, for example "create app/documents.py with a function extract_text(filename, data)
that returns the text of .txt, .md and .pdf files">

Rules:
- Use only these packages: <list>
- Keep it simple and beginner-friendly, with short comments.
- Handle bad input with a clear error message.
- Do not add features I did not ask for.
Show the complete file.
```

**B. Explain code**

```text
Explain this code line by line for a beginner. Then tell me what could go wrong with it.
<paste code>
```

**C. Debug an error**

```text
When I run <the exact command>, I get this error:
<paste the FULL error, including the traceback>

Here is the code of the file mentioned in the error:
<paste the code>

Explain the cause in simple words, then give the smallest fix.
```

**D. Write tests**

```text
Write pytest tests for this FastAPI endpoint using fastapi.testclient.TestClient.
Test one normal case and at least two bad inputs (wrong type, empty, too large).
<paste the endpoint code>
```

**E. Review**

```text
Review this code like a senior engineer. Check: security (secrets, input validation),
error handling, edge cases and simplicity. List problems by importance, with fixes.
<paste code>
```

### 6. How each step lesson works today

Each "Step" lesson (04 to 12) gives you:

1. A **prompt for your AI assistant** - paste it, then compare the result with...
2. ...the **reference code**, which is tested and known to work. If the AI's version is different, that is fine **if it passes the Check**. If the AI's code fails, or you have no assistant, use the reference code.
3. A **review list** - what to look for in the code.
4. A **Check** to prove the feature works.

---

## Do it now

1. Set up one AI assistant from the table above (or decide to work without one).
2. Test it with prompt B on this small function:

```python
def average(numbers):
    return sum(numbers) / len(numbers)
```

3. Ask a follow-up: "What happens if the list is empty? Fix it with a clear error message."

---

## Check

- [ ] Your assistant explained the function.
- [ ] It found the problem: an empty list causes `ZeroDivisionError`.
- [ ] It suggested a fix such as `if not numbers: raise ValueError("The list is empty")`.

---

## What just happened?

You used the AI to **explain** and **review** code, not only to write it. That habit - asking "what could go wrong?" - is what makes AI-assisted development safe.

---

## Try it yourself

1. Ask your assistant: "Which Python package reads PDF files? Give me the exact pip name and its PyPI link." Then open the link and check it is real and popular.
2. Ask it for a function with a bug on purpose, then find the bug yourself before asking it.

---

## If it does not work

| Problem | Fix |
|---|---|
| Copilot says you have no access | Sign in again (Accounts icon). Check that the free plan is active on github.com -> Settings -> Copilot. |
| The assistant writes very long code | Add "Keep it under 40 lines. Do not add extra features." |
| The assistant uses a package we did not install | Ask: "Rewrite this using only <our packages>." |
| You reached the free limit | Use a browser chat (Gemini, ChatGPT, Claude), or continue with the reference code. |

Next: **[Lesson 03 - Set up the project](03_SET_UP_THE_PROJECT.md)**
