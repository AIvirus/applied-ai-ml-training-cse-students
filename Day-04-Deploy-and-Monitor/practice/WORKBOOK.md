# Practice Workbook - Day 4

Use this **after** the lessons, for revision. Answer in your own words first, then check [ANSWERS.md](ANSWERS.md).

## Section A - Finishing and testing (Lesson 01)

1. What is a "definition of done"?
2. Name three kinds of testing you did, and what each one checks.
3. An AI answer is wrong but the sources are right. Where is the problem? And if the sources are wrong?
4. What should a good README contain?

## Section B - Git and GitHub (Lessons 02 and 03)

5. Explain working tree, staging area and commit with an example.
6. Write the commands to: start a repository, see what changed, stage everything, commit with a message, see the history.
7. Why must `.env` never be committed? What do you do if it was pushed by mistake?
8. What is the difference between push, pull and clone?
9. Describe the branch -> pull request -> merge workflow. Why do teams use it?
10. What is a merge conflict and how do you fix it?

## Section C - Docker (Lessons 04 to 06)

11. What problem does Docker solve?
12. Image vs container - explain with an example.
13. Container vs virtual machine - give two differences.
14. What does `-p 9000:8000` mean?
15. Why do we not copy `.env` into the image? How does the container get its settings?
16. Why do we copy `requirements.txt` and run `pip install` before copying the code?
17. Why does the container run as `appuser` instead of root?
18. What does the HEALTHCHECK line do?
19. When is Docker Compose useful?

## Section D - Deployment (Lesson 07)

20. PaaS vs IaaS - give an example of each.
21. List what every deployment needs (at least six items).
22. Why does our start command use `${PORT}` and `--host 0.0.0.0`?
23. Name three limits of a free hosting plan and how they affect Study Buddy.
24. How do you verify that a deployment worked?

## Section E - CI/CD (Lesson 08)

25. What is Continuous Integration?
26. Continuous Delivery vs Continuous Deployment?
27. Explain workflow, trigger, job and step in GitHub Actions.
28. Why do our CI tests not need an API key?
29. How did CI protect `main` from the broken search change?

## Section F - Monitoring (Lesson 09)

30. Application logs vs deployment logs - when do you read each?
31. Read this line and explain each part: `2026-11-22 10:15:03,412 INFO study_buddy: POST /api/ask -> 200 (1840 ms)`
32. What do 400, 422, 500 and 503 usually mean in our app?
33. What does an uptime monitor do?
34. Write the 7 steps of the troubleshooting process.
35. Name three operational limitations of our deployment and how a real product would solve them.

## Section G - Demo (Lesson 10)

36. What are the 6 parts of a good project demo?
37. Why should you prepare a local backup for a live demo?
