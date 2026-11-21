# Lesson 03 - How Machines Learn

**Time:** 35 minutes  |  **Notebook:** `notebooks/01_How_Machines_Learn.ipynb`

---

## Goal

By the end of this lesson you can explain:

- the difference between **traditional programming** and **machine learning**,
- what it means to "learn from examples",
- what a **dataset**, a **feature** and a **label** are,
- the four types of learning: **supervised**, **unsupervised**, **semi-supervised** and **reinforcement**.

---

## Understand

### 1. Traditional programming versus machine learning

**Traditional programming:** a person writes the **rules**. The computer uses the rules on the **data** and gives **answers**.

```text
   Rules  +  Data   --->  [ Computer ]  --->  Answers
```

Example: "If marks are 50 or more, print Pass, else print Fail." The teacher wrote the rule.

**Machine learning:** we give the computer **data** and the correct **answers** (examples). The computer **finds the rules by itself**.

```text
   Data  +  Answers --->  [ Computer ]  --->  Rules (called a MODEL)
```

Then we use that model on **new** data to get new answers. This is called **prediction**.

**Why is this useful?** Some rules are too hard for a person to write. Try writing exact if-else rules to recognise a cat in a photo: "if there are two pointed ears and whiskers and..." It never works for every photo. But if you show a computer 10,000 photos labelled "cat" and "not cat", it can learn the pattern.

### 2. Learning from examples - like a child

How does a small child learn what a dog is? Nobody gives the child a rulebook. Parents point and say "dog" many times. After enough examples, the child recognises a dog they have never seen. Machine learning works the same way: **many examples -> pattern -> recognise new cases**.

### 3. Dataset, features and labels

A **dataset** is a table of examples. Look at a small piece of our student data:

| hours_studied | attendance_percent | sleep_hours | result |
|---|---|---|---|
| 6.3 | 46 | 7.7 | pass |
| 1.3 | 72 | 4.2 | fail |
| 5.6 | 90 | 7.2 | pass |

- Each **row** is one **example** (also called a sample or record). Here, one student.
- **Features** are the **inputs** - the facts we know. Here: `hours_studied`, `attendance_percent`, `sleep_hours`. In code we call the features **X** (capital X).
- The **label** is the **answer** we want to predict. Here: `result`. In code we call it **y** (small y). Another name for label is **target**.

**Memory trick:** features are the **question**, the label is the **answer**.

### 4. The four types of machine learning

| Type | What data it gets | What it does | Real example |
|---|---|---|---|
| **Supervised learning** | Features **and** labels (questions with answers) | Learns to predict the label for new rows | Predict pass/fail from study hours. Detect spam emails. |
| **Unsupervised learning** | Features only (**no** labels) | Finds groups or patterns by itself | Group customers by shopping habits. Group news articles by topic. |
| **Semi-supervised learning** | A **few** labelled rows and **many** unlabelled rows | Uses the few labels to help label the rest | Labelling 100 photos by hand and letting the model label 10,000 more |
| **Reinforcement learning** | No dataset. An **agent** tries actions and gets **rewards** or **penalties** | Learns which actions give the most reward over time | A robot learning to walk. AlphaGo. A game player bot. |

**Simple way to remember:**

- Supervised = learning **with a teacher** who gives the answers.
- Unsupervised = learning **without a teacher**, by finding groups.
- Semi-supervised = a teacher who answers **only a few** questions.
- Reinforcement = learning by **trial and error**, like training a pet with treats.

### 5. Two kinds of supervised problems

| Problem type | The label is... | Example question |
|---|---|---|
| **Regression** | A **number** | "What **marks** will this student get?" (for example 72) |
| **Classification** | A **category** (a class) | "Will this student **pass or fail**?" |

You will train both kinds in the notebook.

---

## Do it now

1. Open `Day-01-AI-ML-Foundations/notebooks/01_How_Machines_Learn.ipynb`.
2. Make sure the kernel at the top right says `.venv`.
3. Run every cell from top to bottom with **Shift + Enter**. Read each text cell before you run the code under it.

In the notebook you will:

- write a pass/fail rule by hand (traditional programming),
- let the computer **learn** a rule from examples (machine learning),
- see features (X) and labels (y),
- try one tiny example of each learning type.

---

## Check

- [ ] The notebook loads the data and shows the first 5 rows.
- [ ] The "learned model" section prints an accuracy above **0.80** (80 percent).
- [ ] The model predicts a result for a new student that you typed.
- [ ] The clustering section prints 3 groups.

---

## What just happened?

- You saw that a hand-written rule is easy for simple problems but you had to **guess** the numbers.
- The machine learning model **found its own rule** from 240 example students and was then tested on 60 students it had never seen.
- `model.fit(X, y)` = "learn from these examples". `model.predict(new_X)` = "now give answers for new data". These two lines appear in almost every ML program.

---

## Try it yourself

1. In the notebook, change the new student's `hours_studied` from 2 to 8. Does the prediction change?
2. Classify these as supervised, unsupervised or reinforcement:
   a. A model groups songs into playlists by their sound, without any names given.
   b. A model learns to predict house prices from past sales.
   c. A program learns to play a racing game by getting points for speed and losing points for crashes.
3. For a "predict if it will rain tomorrow" model, write 3 good features and the label.

---

## If it does not work

| Problem | Fix |
|---|---|
| `FileNotFoundError: ... student_performance.csv` | Open the notebook from inside the `notebooks` folder, so `../data` points to the right folder. In Colab, upload the CSV file first. |
| `ModuleNotFoundError: No module named 'sklearn'` | Wrong kernel. Select the `.venv` kernel (Lesson 02, Step 9). Note: you install it as `scikit-learn` but import it as `sklearn`. |
| Accuracy is a little different from the text | Fine. Small differences are normal between computers and versions. |
| `NameError: name 'df' is not defined` | You skipped a cell. Click **Run All**, or run the cells again from the top. |

Next: **[Lesson 04 - The maths you need](04_MATHS_INTUITION.md)**
