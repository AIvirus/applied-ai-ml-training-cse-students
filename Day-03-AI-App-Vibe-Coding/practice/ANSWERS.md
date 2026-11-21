# Answers - Day 3 Practice Workbook

Try the questions in [WORKBOOK.md](WORKBOOK.md) first. Your wording can be different - what matters is the meaning.

## Section A - Planning

1. Minimum Viable Product: the smallest version that is still useful. You learn what users really need before spending time on extra features.
2. MVP: upload notes, ask questions with sources, summary and practice questions, CSV insights and chart, mock mode. Could have: OCR, research agent (also: flashcards, user accounts).
3. One place for all AI code: easy to change provider, one place for mock mode and error handling, and the key is used in only one file.
4. The API key would be visible to every visitor in the browser, and anyone could use (and use up) your quota.
5. One address of the API that does one job. `GET /health`, `POST /api/documents`, `POST /api/ask`.

## Section B - Vibe coding

6. Building software by describing what you want in normal language and letting an AI write code. Advantage: speed. Dangers: hidden bugs and security holes, invented packages, leaked secrets, code nobody understands.
7. Plan, prompt, read, check, run, debug, test, save (commit).
8. Small pieces are easy to read, test and fix. One huge prompt gives code you cannot understand or debug.
9. Attackers publish fake packages with names that AI assistants tend to invent. Check every package on pypi.org before installing; prefer well-known packages.
10. The exact command, the full error message with traceback, the code of the file named in the error, and what you expected to happen.
11. Ask the assistant to explain it line by line, read the documentation, and test it until you can explain it. Do not keep code you cannot explain.

## Section C - Building

12. `.env` holds your real secrets and is never shared or uploaded. `.env.example` shows which settings exist, with empty values, and is safe to share.
13. `uvicorn` = the server program; `app.main` = the file `app/main.py`; `:app` = the variable called `app` inside it; `--reload` = restart automatically when a file is saved.
14. To check that the app is alive. Monitoring tools and cloud hosts call it regularly and raise an alert if it fails.
15. It runs for every request and logs the method, path, status code and how long the request took.
16. Allowed type (400), not too large (413), not empty (400), contains readable text (400).
17. Small chunks give precise search results and keep prompts small. Overlap stops a fact that sits on a chunk border from being lost.
18. `app.js` sends the question to `POST /api/ask` -> Pydantic checks its length -> `answer_question` asks `store.search` for the top 3 chunks -> a prompt with CONTEXT and QUESTION is built -> `ask_llm` sends it to Gemini with the system rules (or returns the mock answer) -> the answer, sources and mode go back as JSON -> `app.js` shows them.
19. Use only the context; say "I could not find this" if the answer is missing; treat context as data, not instructions; use simple English; cite the source file. These reduce hallucinations, resist prompt injection and let users check answers.
20. Pydantic raises a ValidationError; the app asks again once with a note; if it fails again it returns the mock questions, which are always valid. The user never sees a crash.
21. Fewer tokens (cheaper and faster) and better privacy: the raw data never leaves the server.
22. Text from documents or the AI could contain HTML or scripts. `innerHTML` would run them (XSS); `textContent` shows them as plain text.

## Section D - Testing and debugging

23. Arrange (prepare data), act (call the code), assert (check the result).
24. They need no key or internet, cost nothing, and always give the same results, so failures mean real bugs.
25. Start at the bottom: the last line says what went wrong. Then go up through the traceback to find the file and line in your own code.
26. Only that test needed the search to find something. The other tests either expected "not found" or did not use search at all - so a bug can hide where no test checks that behaviour.

## Section E - Extensions and review

27. When one part fails, the rest keeps working with a clear message. If Tesseract is missing, `/api/ocr` returns 503 with an explanation, and all other features still work.
28. `eval()` runs any Python code. An AI (or a prompt injection) could make it delete files or steal secrets on the server.
29. Tools that write, send, spend or delete: sending email, deleting documents, posting publicly, making payments.
30. Examples: the key is only in `.env` and never logged or sent to the browser; file type, size and length limits work; the app survives an AI failure; no `innerHTML`; answers use the notes and say "not found"; sources are shown; JSON is validated; prompt injection test.
31. Documents are in memory (lost on restart, shared by all users); TF-IDF matches words not meaning; no user accounts; AI answers can still be wrong.
