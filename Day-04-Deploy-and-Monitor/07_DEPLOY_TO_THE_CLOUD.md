# Lesson 07 - Deploy to the Cloud

**Time:** 35 minutes  |  **You need:** your project on GitHub (Lesson 03) with the `Dockerfile` (Lesson 05)

---

## Goal

By the end of this lesson Study Buddy is **live on the internet** with a public link that anyone can open, and you can explain the main deployment ideas.

---

## Understand

### 1. Hosting concepts

| Word | Meaning |
|---|---|
| **Hosting** | Renting a computer in a data centre that runs your app all the time |
| **PaaS** (Platform as a Service) | A host that builds and runs your app for you from your code. You do not manage the server. Examples: **Render**, Railway, Fly.io, Google Cloud Run, Hugging Face Spaces |
| **IaaS** (Infrastructure as a Service) | You rent a raw virtual machine and set up everything yourself. Examples: AWS EC2, Azure VMs, Google Compute Engine |
| **Deployment** | Taking your code and making it run on the host |
| **Domain / URL** | The public address, like `study-buddy-asha.onrender.com` |
| **HTTPS** | Encrypted connection (the padlock). Render gives it for free. |

We use **Render** because it has a free plan, builds directly from GitHub, and understands our Dockerfile.

### 2. What every deployment needs

| Need | In Study Buddy |
|---|---|
| **Code** | Your GitHub repository |
| **Dependencies** | `requirements.txt`, installed by the Dockerfile |
| **Configuration** | Environment variables: `GEMINI_MODEL`, `MOCK_MODE`, `MAX_UPLOAD_MB`, `LOG_LEVEL` |
| **Secrets** | `GEMINI_API_KEY` - typed into the host's dashboard, **never** in the code or the image |
| **Build command** | `docker build` - done by Render using your `Dockerfile` |
| **Start command** | The `CMD` in the Dockerfile: `uvicorn app.main:app --host 0.0.0.0 --port ${PORT}` |
| **Port** | The host tells the app which port to use through the `PORT` variable; our CMD reads it |
| **Health check** | `/health` - the host checks it to know the app started correctly |

### 3. Free plan limits (be honest about them)

Free plans change over time - always read the host's current pricing page. On Render's free plan, at the time of writing:

- The service **goes to sleep** after about 15 minutes without visitors. The next visit wakes it up, which takes up to about a minute.
- Memory and CPU are small.
- The disk is **not permanent**: uploaded documents disappear on every restart or deploy (our app keeps them in memory anyway).

That is fine for a student demo, not for a real product.

---

## Do it now

### Step 1 - Make sure GitHub is up to date

In `my_study_buddy`:

```powershell
git status
```

If anything is not committed, commit and push it. Your GitHub repository must contain `Dockerfile`, `requirements.txt` and the `app/` folder **at the top level**.

### Step 2 - Create a Render account

1. Go to https://render.com and click **Get Started**.
2. Choose **GitHub** to sign up, and authorise Render.

### Step 3 - Create the web service

Render's screens change sometimes; the names below may be slightly different, but the ideas are the same.

1. In the Render dashboard click **New +** -> **Web Service**.
2. Connect your GitHub account if asked, and choose the `study-buddy` repository. (If it is not listed, click **Configure account** and give Render access to that repository.)
3. Fill in:

| Field | Value |
|---|---|
| Name | `study-buddy-yourname` (this becomes part of the URL) |
| Language / Runtime | **Docker** (Render detects the Dockerfile) |
| Branch | `main` |
| Region | The one closest to you (for India, Singapore is usually closest) |
| Instance type | **Free** |

4. Under **Environment Variables**, click **Add Environment Variable** for each:

| Key | Value |
|---|---|
| `GEMINI_API_KEY` | your key (or leave it out and set `MOCK_MODE` to `true`) |
| `GEMINI_MODEL` | `gemini-3.5-flash-lite` (or the model that worked for you) |
| `MOCK_MODE` | `false` (or `true` for a demo without a key) |
| `LOG_LEVEL` | `INFO` |

Do **not** add `PORT` - Render sets it.

5. Open **Advanced** and set **Health Check Path** to `/health`.
6. Click **Create Web Service** (or **Deploy Web Service**).

### Step 4 - Watch the deployment

Render shows the **deploy log** live:

1. `Cloning from https://github.com/...` - getting your code.
2. Docker build steps - the same lines you saw in Lesson 05.
3. `Deploying...` then uvicorn's startup lines.
4. `Your service is live`.

The first deploy takes 3 to 8 minutes.

### Step 5 - Verify the deployment

At the top of the page is your URL, like `https://study-buddy-yourname.onrender.com`.

Check, in this order:

1. `https://...onrender.com/health` -> `{"status":"ok","ai_mode":"real","documents":0}`
2. `https://...onrender.com/` -> the Study Buddy page with the padlock (HTTPS).
3. Upload `college_library_rules.txt` and ask a question.
4. `https://...onrender.com/docs` -> the API documentation.

Send the link to a friend and ask them to try it on their phone.

### Step 6 - Put the link in your README

Edit the "Live demo" line in `README.md`, then:

```powershell
git commit -am "Add live demo link"
```

```powershell
git push
```

Watch Render: it notices the push and **deploys automatically** (Auto-Deploy). This is continuous deployment, which Lesson 08 makes safer.

---

## Check

- [ ] Your app is live at a public `https://...onrender.com` address.
- [ ] `/health` returns `"status": "ok"`.
- [ ] Uploading and asking questions works on the live site.
- [ ] Your API key is only in Render's **Environment** settings - not in GitHub.

---

## What just happened?

Render **pulled** your code from GitHub, **built** the Docker image from your Dockerfile, **started** a container with your environment variables, checked `/health`, and connected it to a public HTTPS address. That is a full deployment.

---

## Other hosts you may meet

| Host | Notes |
|---|---|
| **Hugging Face Spaces** (Docker Space) | Popular for AI demos; free CPU spaces; uses port 7860 by default (set `PORT=7860`) |
| **Google Cloud Run** | Runs containers; generous free tier; needs a billing account |
| **Railway, Fly.io, Koyeb** | Similar PaaS; free offers change often |
| **A virtual machine (AWS EC2, Azure, Oracle Cloud)** | Full control; you install Docker and manage security yourself |

---

## Try it yourself

1. In Render, open **Environment**, change `MOCK_MODE` to `true` and save. Render redeploys. Check `/health`. Change it back.
2. Wait 20 minutes without visiting, then open the site and time how long it takes to wake up.

---

## If it does not work

| Problem | Fix |
|---|---|
| Deploy log: `failed to read dockerfile` / `Dockerfile not found` | The Dockerfile is not at the top of the repository, or not committed. Check on GitHub. |
| Deploy log: `ModuleNotFoundError` | A package is missing from `requirements.txt`. Add it, commit, push. |
| `No open ports detected` / timed out | The app must listen on `0.0.0.0` and `$PORT`. Check the `CMD` line in the Dockerfile. |
| Health check fails | Check the path is exactly `/health`. Open the **Logs** tab for errors. |
| The app works but answers are always mock | `GEMINI_API_KEY` missing or wrong, or `MOCK_MODE=true`. Check **Environment**, then look in **Logs** for `Gemini call failed`. |
| The page takes ~1 minute to open | Normal on the free plan: the service was asleep. |
| Out of memory | The free instance is small. Upload smaller files. |

Next: **[Lesson 08 - CI/CD with GitHub Actions](08_CI_CD_WITH_GITHUB_ACTIONS.md)**
