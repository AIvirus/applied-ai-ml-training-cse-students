# Lesson 07 - Common Machine Learning Algorithms

**Time:** 50 minutes  |  **Notebook:** `notebooks/05_ML_Algorithms.ipynb`

An **algorithm** is a recipe - a set of steps. An ML algorithm is a recipe for **learning a pattern from data**. The result of running it on data is a **model**.

---

## Goal

By the end of this lesson you can explain in simple words, and run in Python:

- **regression** and **classification**,
- **linear regression** and **logistic regression**,
- **decision trees** and **random forests**,
- **K-Nearest Neighbours (KNN)**,
- **Support Vector Machines (SVM)**,
- **clustering** with **K-means**.

---

## Understand

### Reminder: regression vs classification

- **Regression** predicts a **number** (marks = 72.5).
- **Classification** predicts a **category** (pass or fail).

### 1. Linear regression (regression)

Draws the **best straight line** through the data.

```text
final_score = (a x hours_studied) + b
```

- `a` is the **slope** (how much marks go up for each extra hour).
- `b` is the **intercept** (starting point).

The algorithm picks `a` and `b` so the line is as close as possible to all points. With many features it becomes:
`score = a1*hours + a2*attendance + a3*sleep + ... + b`.

**Good for:** simple number predictions, and **explaining** how much each feature matters.
**Weak when:** the real pattern is curved or complex.

### 2. Logistic regression (classification - despite the name)

Gives the **probability** that something belongs to a class, a number between 0 and 1. Then it uses a cut-off, usually 0.5:

```text
probability of pass = 0.83  ->  0.83 >= 0.5  ->  predict "pass"
```

It squeezes a straight-line score into 0 to 1 using an S-shaped curve called the **sigmoid**.

**Good for:** yes/no problems (spam or not, pass or fail, fraud or not). Fast and easy to explain.

### 3. Decision tree (both)

Asks a series of **yes/no questions**, like the game "20 questions":

```text
                 hours_studied <= 3.5 ?
                 /                    \
               yes                     no
               /                        \
   previous_score <= 70 ?             PASS
       /          \
     yes           no
     /              \
   FAIL            PASS
```

The algorithm chooses the questions that split the data best.

**Good for:** easy to understand and draw; handles numbers and categories.
**Weak when:** a very deep tree **memorises** the training data (overfitting - next lesson).

### 4. Random forest (both)

Many decision trees (for example 100), each trained on a slightly different random part of the data. Then they **vote**. The majority answer wins.

Like asking 100 friends for advice instead of 1 - the group is usually wiser than any single person.

**Good for:** strong accuracy on table data with little tuning. Very popular in industry.
**Weak when:** harder to explain than one tree; slower.

### 5. K-Nearest Neighbours, KNN (both)

"Tell me who your neighbours are, and I will tell you who you are."

To classify a new student, KNN finds the **K most similar students** (closest in distance) in the training data and takes a **vote**. With K = 5, if 4 of the 5 nearest neighbours passed, it predicts pass.

**Good for:** very simple idea, no real "training" step.
**Weak when:** features are not **scaled** (Lesson 06) - big-number columns dominate the distance. Slow for very large data.

### 6. Support Vector Machine, SVM (mostly classification)

Finds the **widest possible road** that separates two classes. The road's middle line is the decision boundary. The points touching the edges of the road are the **support vectors**.

```text
   fail  x   x                 o   o  pass
       x    x   |  <- road ->  |   o    o
     x    x     |              |  o   o
```

With a trick called the **kernel**, SVM can also draw curved boundaries.

**Good for:** small and medium datasets with clear separation.
**Weak when:** very large data (slow); needs scaled features.

### 7. Clustering and K-means (unsupervised)

There are **no labels**. We want the computer to find **groups** by itself.

K-means steps (K = number of groups you want):

1. Put K centre points at random.
2. Give every data point to its nearest centre.
3. Move each centre to the middle (mean) of its points.
4. Repeat steps 2 and 3 until the centres stop moving.

**Real examples:** grouping customers into "budget", "regular" and "premium" shoppers; grouping students into study-habit types so teachers can plan support.

### Which algorithm should I choose?

| Situation | Try first |
|---|---|
| Predict a number, want a simple explanation | Linear regression |
| Yes/no answer, want probabilities and explanation | Logistic regression |
| Table data, want strong accuracy fast | Random forest |
| Want rules you can draw and show to people | Decision tree |
| Small data, few features | KNN or SVM (scale first) |
| No labels, want groups | K-means |

In practice, data scientists **try several algorithms and compare** them on test data. The notebook does exactly that.

### The scikit-learn pattern (same for every algorithm)

```python
model = SomeAlgorithm()          # 1. choose the recipe
model.fit(X_train, y_train)      # 2. learn from examples
predictions = model.predict(X_test)   # 3. predict for new data
```

Because every scikit-learn model uses the same `fit` and `predict`, switching algorithms is just changing one line.

---

## Do it now

Open `notebooks/05_ML_Algorithms.ipynb`, select the `.venv` kernel and run every cell. You will train all seven algorithms on the student data, draw a decision tree, and make a comparison table.

---

## Check

- [ ] Linear regression prints how many marks one extra study hour adds (around 4).
- [ ] You see a drawing of a decision tree.
- [ ] A table compares the accuracy of logistic regression, decision tree, random forest, KNN and SVM. All are 0.80 or higher.
- [ ] K-means prints the average habits of 3 groups of students.

---

## What just happened?

- Every algorithm followed the same `fit` -> `predict` pattern.
- Linear regression's **coefficients** (`model.coef_`) told us how much each feature adds to the marks - the model is **explainable**.
- Random forest's **feature importances** showed which columns the forest relied on most.
- K-means found groups **without** any labels.

---

## Try it yourself

1. Change `n_neighbors` in KNN from 5 to 1 and to 25. What happens to accuracy?
2. Change `max_depth` of the decision tree from 3 to 10. Does test accuracy go up or down? (Keep the answer for the next lesson.)
3. Run K-means with `n_clusters=2` and `n_clusters=4`. Can you describe the groups in words?

---

## If it does not work

| Problem | Fix |
|---|---|
| `ValueError: could not convert string to float: 'urban'` | You passed a text column to the model. Encode it first (Lesson 06), or drop it. |
| `ConvergenceWarning` for logistic regression | Only a warning. Scale the features, or use `LogisticRegression(max_iter=1000)`. |
| The tree drawing is too small to read | Make the figure bigger: `plt.figure(figsize=(16, 8))`. |
| Your accuracy numbers differ slightly | Normal. We use `random_state=42` so most numbers repeat exactly, but versions can differ. |

Next: **[Lesson 08 - Train, test and evaluate](08_TRAIN_TEST_AND_EVALUATE.md)**
