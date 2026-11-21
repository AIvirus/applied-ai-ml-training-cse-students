# Lesson 04 - Docker Basics

**Time:** 25 minutes  |  **You need:** permission to install software (or skip to Lesson 07)

---

## Goal

By the end of this lesson you can explain:

- the "works on my machine" problem,
- **images** and **containers**,
- **containers vs virtual machines**,

and you have Docker installed and tested.

---

## Understand

### 1. The problem

Study Buddy works on your laptop because you installed Python 3.12, 15 packages, and (maybe) Tesseract. A cloud server, or a classmate's laptop, may have a different Python, different package versions, or a different operating system. Then it breaks: **"But it works on my machine!"**

### 2. Docker's solution

**Docker** packs your app **together with everything it needs** (the right Python, the packages, system programs like Tesseract, your code and the start command) into one box. That box runs the same way on any computer that has Docker.

| Word | Meaning | Kitchen example |
|---|---|---|
| **Dockerfile** | The step-by-step **recipe** to build the box | A recipe card |
| **Image** | The **built box**, ready to use, cannot change | A packed lunch box, sealed |
| **Container** | A **running** copy of an image | Someone eating the lunch |
| **Registry** | A place to store and share images (Docker Hub, GitHub Container Registry) | A shop shelf of lunch boxes |

One image can start many containers - like many identical lunch boxes from one recipe.

### 3. Container vs virtual machine

| | Virtual machine (VM) | Container |
|---|---|---|
| What it includes | A **whole operating system** with its own kernel | Only the app and its files; **shares** the host's kernel |
| Size | Gigabytes | Usually megabytes to a few hundred MB |
| Start time | Minutes | Seconds |
| Used for | Running a different OS, strong isolation | Packing and shipping apps, running many apps on one server |

```text
   Virtual machines                         Containers
 +-------+ +-------+                    +-------+ +-------+
 | App A | | App B |                    | App A | | App B |
 | Libs  | | Libs  |                    | Libs  | | Libs  |
 | OS    | | OS    |                    +-------+ +-------+
 +-------+ +-------+                    |  Docker engine     |
 |   Hypervisor    |                    |  Host OS (kernel)  |
 |   Host OS       |                    |  Hardware          |
 |   Hardware      |                    +--------------------+
 +-----------------+
```

---

## Do it now

### Step 1 - Install Docker

- **Windows 10/11 and macOS:** download **Docker Desktop** from https://www.docker.com/products/docker-desktop/ and install it with default options. On Windows it may ask to enable **WSL 2** - say yes and restart if asked. Then **start Docker Desktop** from the Start menu (or Applications) and wait until it says **Engine running**.
- **Linux (Ubuntu):** follow https://docs.docker.com/engine/install/ubuntu/ , then run `sudo usermod -aG docker $USER` and log out and in again.

Docker Desktop is free for personal use, education and small businesses. Large companies need a paid plan.

### Step 2 - Check it

Open a **new** terminal:

```powershell
docker --version
```

```powershell
docker run hello-world
```

The second command downloads a tiny test image and runs it. You should see `Hello from Docker!` and an explanation of what just happened.

### Step 3 - Look around

```powershell
docker images
```

```powershell
docker ps -a
```

`docker images` lists images on your computer (you see `hello-world`). `docker ps -a` lists containers, including stopped ones.

Clean up:

```powershell
docker rm $(docker ps -aq --filter ancestor=hello-world)
```

(If that line gives an error on your system, just skip it - it only removes the stopped test container.)

---

## Check

- [ ] `docker --version` prints a version.
- [ ] `docker run hello-world` prints `Hello from Docker!`.
- [ ] You can explain image vs container and container vs VM in your own words.

---

## What just happened?

`docker run hello-world` asked the Docker engine to run an image. It was not on your computer, so Docker **pulled** (downloaded) it from **Docker Hub**, created a **container** from it, ran it, and the container printed a message and stopped.

---

## Try it yourself

1. Run a real Python inside a container without installing anything: `docker run --rm -it python:3.12-slim python` - then type `print("Hello from a container")` and `exit()`.
2. Explain why a container starts much faster than a virtual machine.

---

## If it does not work

| Problem | Fix |
|---|---|
| `error during connect` / `failed to connect to the docker API ... dockerDesktopLinuxEngine` / `Cannot connect to the Docker daemon` | Docker Desktop is not running. Start it and wait for **Engine running**. |
| Docker Desktop says **WSL 2 installation is incomplete** | Open PowerShell **as Administrator**, run `wsl --install`, restart the computer. |
| **Virtualization must be enabled** | Turn on virtualization (Intel VT-x / AMD-V) in the BIOS settings. Ask your lab admin. |
| No admin rights / Docker cannot be installed | Skip to Lesson 07. Render and GitHub Actions build the Docker image in the cloud for you. |
| `permission denied ... docker.sock` (Linux) | Run `sudo usermod -aG docker $USER`, then log out and in. |

Next: **[Lesson 05 - Dockerfile: build and run](05_DOCKERFILE_BUILD_AND_RUN.md)**
