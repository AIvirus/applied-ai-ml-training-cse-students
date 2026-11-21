# Lesson 06 - Docker Compose (Awareness)

**Time:** 10 minutes  |  **Folder:** `Day-03-AI-App-Vibe-Coding/my_study_buddy`

---

## Goal

You know what **Docker Compose** is, when it is useful, and you can start Study Buddy with one command.

---

## Understand

Real applications often have **several parts**: the app, a database, a cache, a background worker. Starting each with a long `docker run ...` command is slow and error-prone.

**Docker Compose** describes all the parts in **one file**, `compose.yaml`, and starts them together with **one command**. It also creates a private network so the parts can talk to each other by name (for example the app reaches the database at `db:5432`).

A typical bigger example (just to read - you do not need it today):

```yaml
services:
  app:
    build: .
    ports: ["8000:8000"]
    env_file: [.env]
    depends_on: [db]
  db:
    image: postgres:17
    environment:
      POSTGRES_PASSWORD: example
    volumes: [db-data:/var/lib/postgresql/data]
volumes:
  db-data:
```

Study Buddy has only one part, so our file is small - but the idea is the same.

---

## Do it now

### Step 1 - Copy and read `compose.yaml`

**Windows:** `Copy-Item ..\study_buddy_lab\compose.yaml .`   **macOS / Linux:** `cp ../study_buddy_lab/compose.yaml .`

```yaml
# compose.yaml - start Study Buddy with one command:  docker compose up --build
# (Day 4, Lesson 06). Compose is most useful when an app has several parts,
# for example an app + a database. Here we have one part, to learn the idea.
services:
  study-buddy:
    build: .
    ports:
      - "8000:8000"        # your computer's port 8000 -> the container's port 8000
    env_file:
      - .env               # GEMINI_API_KEY and other settings (never copied into the image)
    restart: unless-stopped
```

### Step 2 - Start, check, stop

```powershell
docker compose up --build
```

Open http://127.0.0.1:8000. Then press **Ctrl + C**, and remove everything Compose created:

```powershell
docker compose down
```

Useful commands:

| Command | What it does |
|---|---|
| `docker compose up -d` | Start in the background |
| `docker compose ps` | Show running services |
| `docker compose logs -f` | Follow the logs of all services |
| `docker compose down` | Stop and remove the containers |

Commit it:

```powershell
git add compose.yaml
```

```powershell
git commit -m "Add Docker Compose file"
```

---

## Check

- [ ] `docker compose up --build` started the app.
- [ ] You can explain when Compose is useful (apps with several parts).

---

## What just happened?

You described how to run the app in a file instead of remembering a long command. This is "configuration as code": anyone can start the app the same way.

---

## If it does not work

| Problem | Fix |
|---|---|
| `env file .env not found` | Create `.env` (copy `.env.example`). |
| `docker compose` is not a command | Old Docker versions use `docker-compose` (with a dash). Update Docker Desktop. |

Next: lunch break, then **[Lesson 07 - Deploy to the cloud](07_DEPLOY_TO_THE_CLOUD.md)**
