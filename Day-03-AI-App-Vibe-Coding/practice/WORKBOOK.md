# Practice Workbook - Day 3

Use this **after** the lessons, for revision. Answer in your own words first, then check [ANSWERS.md](ANSWERS.md).

## Section A - Planning (Lesson 01)

1. What is an MVP? Why build one first?
2. List the MVP features of Study Buddy and two "could have" features.
3. Why does only `llm.py` talk to the AI model?
4. Why must the browser never call the Gemini API directly?
5. What is an API endpoint? Give three from Study Buddy with their methods.

## Section B - Vibe coding (Lesson 02)

6. What is vibe coding? Give one advantage and two dangers.
7. Write the 8 steps of the safe workflow.
8. Why should you ask for one small feature per prompt?
9. What is "slopsquatting" and how do you protect yourself?
10. What should a good debugging prompt contain?
11. You cannot explain a function the AI wrote. What do you do?

## Section C - Building (Lessons 03 to 09)

12. What is the difference between `.env` and `.env.example`?
13. What does `uvicorn app.main:app --reload` mean, word by word?
14. What is a health check used for?
15. What does the middleware in `main.py` do?
16. Name four checks we do on uploaded files, and the status code for each.
17. Why do we cut documents into chunks with overlap?
18. Describe what happens, step by step, when the user asks a question.
19. What rules are in the system instruction for answering questions, and why?
20. What happens if the AI returns invalid JSON for practice questions?
21. Why do we send only the CSV facts, not the whole file, to the AI?
22. Why does `app.js` use `textContent` and never `innerHTML`?

## Section D - Testing and debugging (Lesson 10)

23. What are the three parts of a test?
24. Why do tests run in mock mode?
25. How do you read a Python error message?
26. In the debugging exercise, why did only one test fail?

## Section E - Extensions and review (Lessons 11 to 13)

27. What is graceful degradation? How does the OCR feature use it?
28. Why must the agent's calculator never use `eval()`?
29. Which agent tools would need human approval?
30. List four things you checked in the security and quality review.
31. Name three known limitations of Study Buddy.
