# Lesson 04 - The Maths You Need (Only the Idea)

**Time:** 45 minutes  |  **Notebook:** `notebooks/02_Maths_for_ML.ipynb`

Do not worry. You do **not** need to solve hard equations. Python does all the calculating. You only need to understand **what** each idea means.

---

## Goal

By the end of this lesson you understand, at a simple level:

- variables and functions,
- vectors and matrices,
- mean, median, mode, variance and standard deviation,
- probability and correlation,
- the idea of **optimisation** - how a model gets better step by step.

---

## Understand

### 1. Variables

A **variable** is a name for a value that can change. In `marks = 72`, `marks` is a variable. In ML, every **feature** (hours studied, attendance) is a variable.

### 2. Functions

A **function** takes an input and gives an output.

```text
f(x) = 2x + 1
input x = 3   ->   output = 2*3 + 1 = 7
```

**A machine learning model is just a function** that the computer found by itself:

```text
predicted_marks = f(hours_studied, attendance, sleep, ...)
```

### 3. Vectors

A **vector** is an ordered list of numbers. One student can be written as a vector:

```text
student = [6.3, 46, 7.7, 61]
           hours, attendance, sleep, previous_score
```

Every row of a dataset is a vector. Words and images also become vectors on Day 2 (this is how AI "reads").

### 4. Matrices

A **matrix** is a table of numbers - many vectors stacked together. A whole dataset is a matrix: **rows = examples, columns = features**.

```text
        hours  attendance  sleep
S001  [  6.3       46       7.7 ]
S002  [  1.3       72       4.2 ]
S003  [  5.6       90       7.2 ]
```

This matrix has **shape 3 x 3** (3 rows, 3 columns). Our full data has shape 300 x 10. The `numpy` package is built for fast maths on vectors and matrices.

### 5. Describing data with a few numbers (statistics)

Take the marks of 7 students: `40, 55, 55, 60, 70, 80, 100`

| Measure | Meaning | Value here |
|---|---|---|
| **Mean** (average) | Add all, divide by how many | (40+55+55+60+70+80+100) / 7 = **65.7** |
| **Median** | The middle value after sorting | **60** |
| **Mode** | The value that appears most often | **55** |
| **Range** | Biggest minus smallest | 100 - 40 = **60** |
| **Variance** | Average of the **squared** distances from the mean. Big = values are spread out | about **331.6** |
| **Standard deviation (std)** | Square root of variance. "Typical distance from the mean", in the same unit as the data | about **18.2** marks |

**Why both mean and median?** If one student scores 100 and the rest are low, the mean jumps up but the median stays in the middle. The median is safer when there are a few extreme values (called **outliers**).

**Why standard deviation?** Two classes can have the same mean of 60:
- Class A: 58, 60, 62 (std small - everyone is similar)
- Class B: 20, 60, 100 (std large - very different students)

### 6. Probability

**Probability** is how likely something is, from **0** (impossible) to **1** (certain).

- A coin landing heads: 0.5 (50 percent).
- If 194 of 300 students passed, the probability that a random student passed is 194 / 300 = **0.65**.

Classification models often give a probability, for example "this email is spam with probability 0.93".

### 7. Correlation

**Correlation** tells how two things move together. It is a number from **-1 to +1**.

| Value | Meaning | Example |
|---|---|---|
| close to **+1** | When one goes up, the other goes up | Hours studied and marks |
| close to **0** | No clear relationship | Shoe size and marks |
| close to **-1** | When one goes up, the other goes down | Hours on phone games and marks |

**Important:** correlation is **not** causation. Ice cream sales and swimming accidents both go up in summer. Ice cream does not cause accidents - hot weather causes both.

### 8. Optimisation - how a model gets better

How does the computer "find" the best function? By **guessing, measuring the error, and improving step by step**.

Imagine you are on a dark hill and want to reach the lowest point of the valley. You cannot see, but you can feel the slope under your feet. So you take a small step **downhill**, feel again, take another step... until the ground is flat. That is the lowest point.

In ML:

1. The model starts with a random guess (for example `marks = 0 * hours + 0`).
2. It measures how wrong it is. This "wrongness" number is called the **loss** (or error).
3. It changes its numbers a little in the direction that makes the loss smaller.
4. It repeats steps 2 and 3 many times.

This method is called **gradient descent**. "Gradient" = the slope. "Descent" = going down. The size of each step is the **learning rate**. Almost all of modern AI, including ChatGPT and Gemini, is trained with this idea.

---

## Do it now

Open `notebooks/02_Maths_for_ML.ipynb`, select the `.venv` kernel and run every cell. You will:

- make vectors and matrices with `numpy`,
- calculate mean, median, mode and standard deviation for the real student data,
- calculate a probability,
- see correlations between columns,
- watch gradient descent learn a straight line, step by step, with the loss going down.

---

## Check

- [ ] The notebook prints the matrix shape `(3, 3)`.
- [ ] You see the mean, median and standard deviation of `final_score`.
- [ ] The correlation table shows that `hours_studied` has the **strongest positive** correlation with `final_score`.
- [ ] The gradient descent chart shows the loss going **down** and flattening.

---

## What just happened?

- `numpy` arrays are vectors and matrices. `.shape` tells their size.
- `pandas` can describe a column with `.mean()`, `.median()`, `.mode()` and `.std()`.
- `.corr()` gave correlations. Bigger positive number = stronger "go up together".
- Gradient descent started with a bad line and, by repeating small corrections, found a good line. The computer **learned** the numbers.

---

## Try it yourself

1. In the gradient descent cell, change `learning_rate` from `0.01` to `0.1`. What happens to the loss? Now try `0.0001`. (Too big jumps around or explodes; too small learns very slowly.)
2. Calculate by hand the mean and median of `10, 20, 30, 40, 1000`. Which one describes the "typical" value better?
3. Guess if these have positive, negative or near-zero correlation: temperature and AC sales; speed of a car and time to reach a city; your roll number and your marks.

---

## If it does not work

| Problem | Fix |
|---|---|
| The chart does not appear | Run the cell again. Make sure the cell has `plt.show()` at the end. |
| `ValueError: could not convert string to float` in `.corr()` | Use `df.corr(numeric_only=True)` so text columns are skipped. |
| The loss becomes `nan` or `inf` | Your learning rate is too big. Make it smaller. This is a real lesson: too big steps "jump out of the valley". |

Next: **[Lesson 05 - Data analysis and data science](05_DATA_ANALYSIS_AND_DATA_SCIENCE.md)**
