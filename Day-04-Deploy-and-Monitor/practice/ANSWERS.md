# Answers - Day 4 Practice Workbook

Try the questions in [WORKBOOK.md](WORKBOOK.md) first. Your wording can be different - what matters is the meaning.

## Section A - Finishing and testing

1. An agreed list of what must be true before a feature counts as finished: it works, has tests, handles errors, and is documented.
2. Automated tests (pytest - features and bad inputs, repeatable), manual UI tests (the real page and user experience), AI output checks (are the AI answers correct and grounded).
3. Sources right but answer wrong: the generation step (prompt, temperature, model). Sources wrong: the retrieval step (search, chunking).
4. What it is, how to install and run it, how to test it, settings, known limitations, and (if any) a live link.

## Section B - Git and GitHub

5. You edit `README.md` (working tree), choose it with `git add` (staging area), and save a snapshot with `git commit -m "..."` (commit in the history).
6. `git init -b main`, `git status` (and `git diff`), `git add .`, `git commit -m "message"`, `git log --oneline`.
7. It contains secrets; once committed it stays in the history, and on GitHub bots find keys within minutes. If pushed: delete the key at the provider and create a new one, remove the file from Git (`git rm --cached .env`), make sure `.gitignore` lists it, commit and push.
8. Push sends your commits to GitHub; pull gets new commits from GitHub; clone downloads a whole repository the first time.
9. Create a branch for a feature, commit and push it, open a pull request, teammates review (and CI tests it), then merge into `main`. It keeps `main` working and lets others review changes.
10. Two people changed the same lines. Git marks both versions with `<<<<<<<` and `>>>>>>>`. Edit the file to keep the right code, remove the markers, `git add` and `git commit`.

## Section C - Docker

11. "It works on my machine": different Python versions, packages or operating systems. Docker packs the app with everything it needs so it runs the same everywhere.
12. The image is the built, read-only package (`study-buddy`); a container is a running copy of it (`buddy`). One image can run many containers.
13. A VM includes a full operating system and kernel; a container shares the host kernel. Containers are much smaller and start in seconds; VMs take minutes.
14. Port 9000 on your computer is connected to port 8000 inside the container. Open http://127.0.0.1:9000.
15. Images can be shared or uploaded, so secrets inside would leak. Settings are given at start time with `-e`, `--env-file`, or the host's environment settings.
16. Docker caches layers. Packages change rarely and are slow to install; code changes often. This order means a code change does not repeat `pip install`.
17. Safety: if an attacker breaks into the app, they get the limited rights of a normal user instead of full control of the container.
18. Docker calls `/health` every 30 seconds and marks the container healthy or unhealthy.
19. When an app has several parts (app, database, cache, worker) that must start together and talk to each other.

## Section D - Deployment

20. PaaS: the host builds and runs your app from code (Render, Cloud Run). IaaS: you rent a raw virtual machine and set it up yourself (AWS EC2).
21. Code, dependencies, configuration (environment variables), secrets, a build command, a start command, a port, a health check (also: a domain and HTTPS).
22. The host chooses the port and passes it in `PORT`. `0.0.0.0` makes uvicorn listen on all network interfaces, so traffic from outside the container can reach it (127.0.0.1 would only accept connections from inside).
23. The service sleeps when idle (slow first visit), small memory and CPU (large files may fail), no permanent disk (documents vanish on restart).
24. Read the deploy log until "live", open `/health`, open the page, try the main features, check the logs for your requests.

## Section E - CI/CD

25. Automatically building and testing the project on every push, so problems are found within minutes.
26. Delivery: every passing change is ready and a person clicks deploy. Deployment: every passing change is deployed automatically.
27. Workflow: the automated process in a YAML file. Trigger: the event that starts it (push, pull_request). Job: a group of steps on one fresh runner. Step: one command or action.
28. The workflow sets `MOCK_MODE=true`, so tests use the pretend AI - no key, no cost, repeatable results.
29. The pull request showed a red cross because a test failed, so it was not merged. With "deploy after CI checks pass", it could not reach the live site either.

## Section F - Monitoring

30. Deployment logs: when a deploy fails or the app does not start (build and startup). Application logs: when the running app behaves wrongly (requests, errors, warnings).
31. Date and time; level INFO; logger name `study_buddy`; method POST; path `/api/ask`; status 200 (success); it took 1840 ms (mostly waiting for the AI).
32. 400: the user sent something wrong (bad file, no document yet). 422: request data failed validation. 500: a bug in our code. 503: the app or a feature (OCR) is unavailable.
33. It calls a URL (our `/health`) from outside every few minutes and alerts you by email if it fails.
34. See the symptom, check `/health`, read the logs, narrow it down (deploy or runtime, our code or the AI API), reproduce, fix (with a test), verify.
35. Documents vanish on restart (use a database or storage); all users share documents (accounts and per-user storage); free instance sleeps and is small (paid instances, scaling); AI quota can run out (paid plan, rate limits, caching); no error alerts (monitoring tools).

## Section G - Demo

36. Problem, solution, architecture, AI concepts, live demo, quality and delivery (tests, CI, deployment, monitoring, limitations, next steps).
37. Free services sleep, networks fail and AI quotas run out. A local backup (in mock mode if needed) lets the demo continue.
