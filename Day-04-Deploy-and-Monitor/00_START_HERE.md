# Day 4 - GitHub, Docker, Deployment and Monitoring

**Goal of the day:** move Study Buddy from "it works on my laptop" to "it is on the internet, tested automatically on every change, and I can see what it is doing" - then present it.

**Before you start:** finish Day 3 up to Lesson 10. `pytest -v` must pass in `Day-03-AI-App-Vibe-Coding/my_study_buddy`.

---

## The big picture

```text
 your laptop                GitHub                       cloud host (Render)
 my_study_buddy  --push-->  repository  --webhook-->     builds the Docker image
   git commit               GitHub Actions:              runs the container
                            run tests, build Docker      https://your-app.onrender.com
                                    |                              |
                              green tick or red cross        logs, /health, uptime monitor
```

---

## Your plan for today (do these in order)

| # | Lesson | What you do | Time |
|---|---|---|---|
| 01 | [Finish and test your project](01_FINISH_AND_TEST_YOUR_PROJECT.md) | Final tests, failure handling, a README | 40 min |
| 02 | [Git basics](02_GIT_BASICS.md) | Version control, commits, keeping secrets out | 35 min |
| 03 | [GitHub: push and collaborate](03_GITHUB_PUSH_AND_COLLABORATE.md) | Put the code online, branches, pull requests | 35 min |
| 04 | [Docker basics](04_DOCKER_BASICS.md) | Containers, images, install Docker | 25 min |
| 05 | [Dockerfile: build and run](05_DOCKERFILE_BUILD_AND_RUN.md) | Pack Study Buddy into an image and run it | 35 min |
| 06 | [Docker Compose (awareness)](06_DOCKER_COMPOSE.md) | Start the app with one command | 10 min |
| -- | **Lunch break** | | 60 min |
| 07 | [Deploy to the cloud](07_DEPLOY_TO_THE_CLOUD.md) | Your app on the internet with a public link | 35 min |
| 08 | [CI/CD with GitHub Actions](08_CI_CD_WITH_GITHUB_ACTIONS.md) | Automatic tests on every push | 30 min |
| 09 | [Logs, monitoring and troubleshooting](09_LOGS_MONITORING_AND_TROUBLESHOOTING.md) | Read logs, health checks, uptime alerts | 30 min |
| 10 | [Final demonstration](10_FINAL_DEMO.md) | Present your project | 30 min |
| 11 | [Final checklist and what's next](11_FINAL_CHECKLIST_AND_WHATS_NEXT.md) | Check everything, plan your next steps | 10 min |

Morning (10:00 AM to 1:20 PM): lessons 01 to 06. Afternoon (2:20 PM to 4:40 PM): lessons 07 to 11.

---

## Accounts and tools you need today

| What | Lesson | Cost |
|---|---|---|
| Git | 02 | Free |
| GitHub account | 03 | Free |
| Docker Desktop (Windows / macOS) or Docker Engine (Linux) | 04 | Free for personal use, education and small businesses |
| Render account (sign in with GitHub) | 07 | Free plan |
| UptimeRobot account (optional) | 09 | Free plan |

No Docker on your computer (for example no admin rights)? You can still do Lessons 07 to 11: Render and GitHub Actions build the Docker image **for you** in the cloud.

---

## Where you work today

All commands run in **your project folder**: `Day-03-AI-App-Vibe-Coding/my_study_buddy`. The lessons are here in `Day-04-Deploy-and-Monitor`, but the code you deploy is the code you built on Day 3.

The finished reference files (`Dockerfile`, `compose.yaml`, `.github/workflows/ci.yml`) are in `Day-03-AI-App-Vibe-Coding/study_buddy_lab/`.

---

Start with **[Lesson 01 - Finish and test your project](01_FINISH_AND_TEST_YOUR_PROJECT.md)**
