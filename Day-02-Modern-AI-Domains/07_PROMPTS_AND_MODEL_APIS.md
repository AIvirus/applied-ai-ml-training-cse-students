# Lesson 07 - Prompts and Model APIs

**Time:** 35 minutes  |  **Notebook:** `notebooks/06_Talk_to_an_LLM.ipynb`

---

## Goal

By the end of this lesson you can:

- call an LLM from Python through its **API**,
- use **system instructions** and **user prompts**,
- write better prompts with **prompt engineering** techniques,
- control randomness with **temperature**,
- get **structured output** (JSON) and **validate** it,
- handle API errors without crashing.

---

## Understand

### 1. Model APIs

You can use an LLM in two ways:

- **Chat app** (gemini.google.com, ChatGPT): for people.
- **API**: for **programs**. Your code sends text, the model sends text back. This is how you build AI **into your own apps**.

Every API call has the same shape:

```text
your code  --->  [ model name + system instruction + user prompt + settings ]  --->  LLM
your code  <---  [ answer text (+ token counts) ]                              <---  LLM
```

In our notebooks this is one line: `ask_llm("your prompt", system="...")`. The helper file `ai_helper.py` does the API call with Google's official `google-genai` package.

### 2. System instruction vs user prompt

| | System instruction | User prompt |
|---|---|---|
| Who writes it | The **developer** (you) | The **user** of your app |
| What it says | The AI's **role, rules, tone and format** - for the whole conversation | The **actual question or task** |
| Example | "You are a patient tutor for school students. Use simple words. Answer in at most 5 lines." | "What is photosynthesis?" |

The system instruction is like the **job description**; the user prompt is the **daily task**.

### 3. Prompt engineering - how to ask well

**Prompt engineering** = writing instructions that get good, reliable results. The model cannot read your mind - be clear.

| Technique | Bad prompt | Better prompt |
|---|---|---|
| **Be specific** | "Tell me about Python." | "Explain in 3 bullet points why Python is popular for AI, for a first-year student." |
| **Give a role** | "Check my code." | "You are a senior Python reviewer. Find bugs in this code and explain each in one line." |
| **Give context** | "Write an email." | "Write a polite email to my professor asking for a 2-day extension on my ML assignment because I was ill." |
| **Set the format** | "List some fruits." | "List 5 fruits as a JSON array of strings, nothing else." |
| **Give examples (few-shot)** | "Classify: 'The app crashed.'" | "Classify the sentiment. 'Love it' -> positive. 'Waste of money' -> negative. 'The app crashed' ->" |
| **Ask for steps** | "What is 15% of 240 plus 18?" | "Solve step by step, then give the final answer on the last line." |
| **Set limits** | "Summarise this." | "Summarise this in under 50 words. If the text does not say, write 'not mentioned'." |

**Zero-shot** = no examples. **Few-shot** = a few examples in the prompt. Few-shot often makes the output much more consistent.

**A simple prompt template you can reuse:**

```text
ROLE:    You are a ...
TASK:    Do ...
CONTEXT: Here is the information you need: ...
FORMAT:  Answer as ... (bullets / JSON / max N words)
RULES:   If you do not know, say "I don't know". Do not invent facts.
```

### 4. Temperature

From Lesson 05: low (0 to 0.3) = focused and repeatable; high (0.8 or more) = creative and varied. Use low for facts, extraction and code; higher for stories and brainstorming.

### 5. Structured outputs and validation

Apps need answers they can **use in code**, not just read. So we ask for **JSON**:

```json
{"name": "Asha", "skills": ["Python", "SQL"], "years_experience": 2}
```

Then we **validate** it - check it has the right fields and types - before trusting it. LLMs sometimes return broken JSON, missing fields or wrong types. We use **Pydantic**, a Python package that checks data against a model (a schema):

```python
from pydantic import BaseModel

class Candidate(BaseModel):
    name: str
    skills: list[str]
    years_experience: int
```

If the AI's JSON does not match, Pydantic raises a clear error and our code can **retry** or show a friendly message. **Never trust AI output blindly** - validate it like user input.

### 6. Handling errors

API calls can fail: no internet, wrong key, limit reached (429), server busy (503), model name changed (404). Good code:

- catches the error (`try` / `except`),
- shows a helpful message,
- retries after a short wait for temporary errors,
- has a **fallback** (our MOCK MODE).

---

## Do it now

1. Make sure you finished Lesson 06 (or accept MOCK MODE).
2. Open `notebooks/06_Talk_to_an_LLM.ipynb`, select the `.venv` kernel, and run every cell.

You will compare bad vs good prompts, use system instructions, try temperatures, do few-shot classification and get validated JSON.

---

## Check

- [ ] The first cell prints `REAL AI MODE` (or `[MOCK MODE]` if you have no key - that is OK).
- [ ] The same question gives a different style with two different system instructions.
- [ ] The JSON cell prints a validated Python object, and the "broken JSON" cell shows a clean validation error instead of a crash.

---

## What just happened?

You called an LLM from code - the core skill for building AI applications. You saw that the **prompt is the program**: small changes in wording change the result. And you made AI output **safe to use in code** by asking for JSON and validating it.

---

## Try it yourself

1. Write a system instruction that makes the AI answer like a cricket commentator. Ask it to explain overfitting.
2. Ask the same factual question with temperature 0 three times, then with temperature 1.5 three times. Compare.
3. Create a Pydantic model `Recipe` (name, ingredients list, minutes) and ask the AI for a recipe in that JSON shape.

---

## If it does not work

| Problem | Fix |
|---|---|
| Always `[MOCK MODE]` even with a key | The `.env` must be in the main course folder. Restart the notebook kernel (**Restart** button) after creating `.env`, then run all cells again. |
| `json.decoder.JSONDecodeError` | The model did not return pure JSON. Use `json_output=True` and say "Return only JSON" in the prompt. The notebook shows how to handle this. |
| `429 RESOURCE_EXHAUSTED` | Free limit reached. Wait a minute. |
| Answers differ from the notebook text | Normal - LLM answers vary. Check the **idea**, not the exact words. |

Next: **[Lesson 08 - Embeddings, semantic search and RAG](08_EMBEDDINGS_AND_RAG.md)**
