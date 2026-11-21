# Lesson 04 - Other AI Domains

**Time:** 25 minutes  |  **Notebook:** `notebooks/04_Other_AI_Domains.ipynb`

AI is much bigger than chatbots. This lesson is a quick tour of other important areas. For each one: what it is, an everyday example, and how it works in one line.

---

## Goal

By the end of this lesson you can describe:

- speech recognition and speech synthesis,
- recommender systems,
- predictive analytics,
- robotics,
- reinforcement learning applications,
- explainable AI,
- edge AI,
- AI in cybersecurity.

---

## Understand

### 1. Speech recognition and speech synthesis

| | Speech recognition (speech-to-text) | Speech synthesis (text-to-speech) |
|---|---|---|
| Does | Turns **spoken words into text** | Turns **text into a spoken voice** |
| Examples | Voice typing, "Hey Google", YouTube auto-captions, call-centre transcripts | Google Maps directions, screen readers for blind users, audiobooks |
| How | Sound wave -> small time slices -> features -> deep learning model -> words | Text -> sounds (phonemes) -> deep learning model -> sound wave |
| Popular tools | OpenAI Whisper (free, open), Google Speech-to-Text | Google Text-to-Speech, ElevenLabs |

### 2. Recommender systems

Suggest things you might like: Netflix shows, Amazon products, YouTube videos, Spotify songs, Instagram reels.

Two main ideas:

- **Content-based:** "You liked an action movie, here is another **action movie**." Uses the item's features.
- **Collaborative filtering:** "People **similar to you** liked this." Uses the behaviour of many users. No need to know what the item is about.

Most real systems combine both. You will build a tiny collaborative filter in the notebook.

### 3. Predictive analytics

Using past data to **predict future events** - mostly the supervised ML from Day 1, used for business decisions.

Examples: predicting next month's sales, which customers may leave (churn), when a machine may break (predictive maintenance), crop yield, electricity demand.

### 4. Robotics

Robots that **sense, think and act** in the physical world. AI gives them vision (cameras + CV), planning (choosing a path) and control (moving arms and wheels).

Examples: warehouse robots (Amazon), robot vacuum cleaners, surgical robots, drones, factory arms, delivery robots.

### 5. Reinforcement learning applications

From Day 1: an **agent** learns by **trial and error** to get the most **reward**.

| Term | Meaning | Example (game) |
|---|---|---|
| Agent | The learner | The game player |
| Environment | The world it acts in | The game |
| State | The current situation | Position on the board |
| Action | What it can do | Move left / right |
| Reward | Score after the action | +10 for a coin, -100 for falling |
| Policy | Its learned strategy | "In this state, do this action" |

Uses: games (AlphaGo), robot walking, traffic signal control, data-centre cooling (Google saved energy this way), and **RLHF** - Reinforcement Learning from Human Feedback, which helps make chatbots more helpful and safe.

### 6. Explainable AI (XAI)

Many models (deep networks, random forests) are **black boxes**: they give an answer but not the reason. **Explainable AI** = methods that show **why** a model decided something.

Why it matters: if a bank AI rejects a loan, the customer deserves a reason; a doctor must know why an AI flags a scan; laws (like the EU AI Act) require explanations for high-risk uses.

Methods: **feature importance**, **permutation importance** (shuffle a column and see how much the model gets worse), **SHAP** and **LIME** (explain single predictions), and using simple models (decision trees) when explanation matters most.

### 7. Edge AI

Running AI **on the device itself** (phone, camera, car, watch) instead of sending data to a cloud server.

| Advantage | Why |
|---|---|
| Fast | No waiting for the internet |
| Private | Your data stays on your device (for example, face unlock) |
| Works offline | No network needed |
| Cheaper | No cloud server bills |

Challenge: devices have small memory and battery, so models are made smaller (**quantisation**, **pruning**). Examples: face unlock, Google keyboard predictions, smart cameras, Tesla driving computer. Tools: TensorFlow Lite, ONNX Runtime, Core ML.

### 8. AI in cybersecurity

AI helps **defend** systems:

- **Anomaly detection:** learn what "normal" looks like and flag anything unusual - a login from a new country at 3 AM, a sudden huge data download.
- **Spam and phishing detection** in email.
- **Malware detection** from file behaviour.
- **Fraud detection** in payments.

But attackers also use AI (fake voices, better phishing emails), and AI systems themselves can be attacked (prompt injection - Lesson 10).

---

## Do it now

Open `notebooks/04_Other_AI_Domains.ipynb`, select the `.venv` kernel and run every cell. You will build:

1. a tiny **movie recommender** (collaborative filtering),
2. a **Q-learning** agent (reinforcement learning) that learns to walk to a goal,
3. an **explanation** of a model with permutation importance (XAI),
4. a simple **sales forecast** (predictive analytics),
5. an **anomaly detector** for suspicious logins (cybersecurity).

---

## Check

- [ ] The recommender suggests a movie for "Asha" that she has not rated yet.
- [ ] The Q-learning agent's final path goes straight to the goal.
- [ ] The XAI chart shows which features matter most to the model.
- [ ] The anomaly detector flags the strange logins (like 3 AM with many failed attempts).

---

## What just happened?

You saw that the same building blocks (data, vectors, similarity, rewards, models) power very different AI products.

---

## Try it yourself

1. Add a new user to the ratings table and get recommendations for them.
2. In Q-learning, change the reward for each step from `-1` to `0`. Does the agent still find the shortest path?
3. List 3 apps on your phone and say which AI domain each one uses most.

---

## If it does not work

| Problem | Fix |
|---|---|
| Q-learning path is not the shortest | Learning has randomness. Increase `episodes` or run the cell again. |
| Anomaly detector flags a normal row | Anomaly detection is not perfect. Change `contamination` (expected share of unusual rows). |

Next: **[Lesson 05 - Generative AI and LLMs](05_GENERATIVE_AI_AND_LLMS.md)**
