# Lesson 09 - Logs, Monitoring and Troubleshooting

**Time:** 30 minutes  |  **You need:** your app live on Render (Lesson 07)

---

## Goal

By the end of this lesson you can:

- read **application logs** and **deployment logs**,
- use a **health check** and an **uptime monitor**,
- recognise **request failures** and **AI API errors** in the logs,
- follow a simple troubleshooting process,
- explain the **operational limits** of your deployment.

---

## Understand

### 1. Why monitor?

Once your app is on the internet, you are not watching the terminal any more. Things go wrong while you sleep: the AI quota runs out, a user uploads a strange file, the server restarts. **Monitoring** tells you **what happened** and **that** something happened.

### 2. The main signals

| Signal | Question it answers | In Study Buddy |
|---|---|---|
| **Application logs** | What is the app doing right now? | One line per request from our middleware; warnings like `Gemini call failed` |
| **Deployment logs** | Did the build and start work? | Render's deploy log (Docker build + startup) |
| **Health check** | Is the app alive? | `/health` returns `{"status": "ok"}` |
| **Uptime** | Was it reachable all day? | An outside service calls `/health` every few minutes |
| **Error rate** | How many requests fail? | Count of status codes 4xx and 5xx in the logs |
| **Response time (latency)** | Is it fast enough? | The `(123 ms)` at the end of each log line |

### 3. Reading a log line

```text
2026-11-22 10:15:03,412 INFO study_buddy: POST /api/ask -> 200 (1840 ms)
|                       |    |            |    |           |    |
date and time           level  logger    method path      status  duration
```

**Log levels**, from least to most serious: `DEBUG` < `INFO` < `WARNING` < `ERROR` < `CRITICAL`. In production we usually log `INFO` and above. `LOG_LEVEL` in the environment controls this.

### 4. Status codes you will see

| Code | Meaning | Usually means |
|---|---|---|
| 200 | OK | Fine |
| 400 | Bad Request | The user sent a wrong file or no document yet - their problem, our clear message |
| 404 | Not Found | Wrong address or unknown filename |
| 413 | Payload Too Large | File over the limit |
| 422 | Unprocessable | Request data failed Pydantic validation |
| 500 | Internal Server Error | **A bug in our code** - investigate |
| 502 / 503 | Bad Gateway / Unavailable | The app is not running, is restarting, or (for OCR) a feature is unavailable |

### 5. AI API errors

Our `llm.py` catches AI errors and logs a warning such as:

```text
WARNING study_buddy.llm: Gemini call failed (ClientError). Using mock answer.
```

Common causes: wrong key or model name (400 / 404), **rate limit or quota reached (429)**, the AI service is busy (503), no network. The app keeps working in mock mode, but you should notice and fix the cause.

### 6. Troubleshooting process

```text
1. SEE      What is the symptom? (page error, slow, wrong answer)
2. CHECK    /health - is the app alive?
3. READ     Logs around the time of the problem - find the request and its status code
4. NARROW   Deploy problem (deploy log) or runtime problem (app log)? Our code or the AI API?
5. REPRODUCE  Make it happen again, locally if possible (same input, same settings)
6. FIX      Smallest fix, add a test for it, push - CI runs, Render deploys
7. VERIFY   Check /health and the original problem again
```

---

## Do it now

### Step 1 - Read the application logs

1. In Render, open your service -> **Logs**.
2. In another tab, use your live app: upload a file, ask a question, upload a wrong file type.
3. Back in **Logs**, find your requests. For each, note the path, status code and duration.

You should see lines like:

```text
INFO study_buddy: Document added: college_library_rules.txt (5 chunks)
INFO study_buddy: POST /api/documents -> 200 (35 ms)
INFO study_buddy: POST /api/ask -> 200 (1420 ms)
INFO study_buddy: POST /api/documents -> 400 (2 ms)
```

Notice: `/api/ask` is much slower than the others, because it waits for the AI. That is normal - and it is the first place to look if users say the app is slow.

### Step 2 - Read the deployment logs

In Render, open **Events** and click the latest deploy. Read it from top to bottom: clone, build steps, start, "live". If a deploy ever fails, this is where you look first.

### Step 3 - Make an AI error on purpose

1. In Render -> **Environment**, change `GEMINI_MODEL` to `model-that-does-not-exist` and save (Render redeploys).
2. Ask a question in the live app. You still get an answer (mock mode).
3. In **Logs**, find: `Gemini call failed (...). Using mock answer.`
4. Change `GEMINI_MODEL` back to the correct name and save.

You just practised the full loop: symptom (mock answers) -> logs -> cause (wrong setting) -> fix -> verify.

### Step 4 - Set up an uptime monitor (optional, free)

1. Create a free account at https://uptimerobot.com (or a similar service such as Better Stack).
2. **Add New Monitor**: type **HTTP(s)**, URL `https://YOUR-APP.onrender.com/health`, interval 5 minutes.
3. Add your email as the alert contact.

The monitor now checks your app from the outside and emails you if it goes down. (A side effect: regular checks also keep a free Render service awake. Respect your host's fair-use rules.)

### Step 5 - Check health from the terminal

**Windows (PowerShell):**

```powershell
Invoke-RestMethod https://YOUR-APP.onrender.com/health
```

**macOS / Linux:**

```bash
curl https://YOUR-APP.onrender.com/health
```

This is exactly what monitors and load balancers do.

---

## Check

- [ ] You found your own requests in Render's **Logs**, with status codes and durations.
- [ ] You found and read a deploy in **Events**.
- [ ] You caused, found and fixed an AI API error using the logs.
- [ ] (Optional) An uptime monitor checks `/health`.

---

## What just happened?

You learned to **observe** a running system. The logging middleware you added on Day 3 now pays off: every request leaves a trace you can read later.

---

## Operational limitations of our setup (know them, say them in your demo)

| Limitation | Why | A real product would... |
|---|---|---|
| Documents vanish on restart | Kept in memory; free disk is not permanent | Store them in a database or object storage |
| All users share the same documents | No accounts | Add login and per-user storage |
| Sleeps when idle; slow first request | Free plan | Use a paid instance |
| One small instance | Free plan | Scale to several instances behind a load balancer |
| Logs are kept only for a short time | Free plan | Send logs to a logging service |
| AI quota can run out | Free API tier | Paid API plan, rate limits per user, caching |
| No alerts on error rate | Only uptime is monitored | Use an APM / monitoring tool (for example Sentry, Grafana) |

---

## Try it yourself

1. Set `LOG_LEVEL` to `WARNING` in Render. Which log lines disappear? Set it back to `INFO`.
2. Ask your AI assistant: "Add a log line in answer_question that records how many chunks were found and the AI mode, without logging the question text." Why might we not want to log the user's question? (Privacy.)

---

## If it does not work

| Problem | Fix |
|---|---|
| Logs tab is empty | The service may be asleep. Open the site to wake it, then look again. |
| You see only uvicorn lines, no `study_buddy` lines | `LOG_LEVEL` is set higher than `INFO`, or the middleware is missing in `main.py`. |
| Many `429` warnings | The free AI quota is used up. Wait, reduce usage, or turn on `MOCK_MODE` for the demo. |

Next: **[Lesson 10 - Final demonstration](10_FINAL_DEMO.md)**
