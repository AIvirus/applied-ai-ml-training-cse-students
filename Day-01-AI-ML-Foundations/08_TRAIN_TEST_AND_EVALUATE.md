# Lesson 08 - Train, Test and Evaluate a Model

**Time:** 45 minutes  |  **Notebook:** `notebooks/06_Train_and_Evaluate.ipynb`

---

## Goal

By the end of this lesson you can explain and use:

- **training**, **validation** and **test** datasets,
- model **fitting**, **epochs** and **loss**,
- **overfitting** and **underfitting**,
- **bias** and **variance**,
- **accuracy**, **precision**, **recall**, **F1-score** and the **confusion matrix**.

---

## Understand

### 1. Why we split the data

Imagine a teacher gives students the **exact exam questions** to practise. Every student scores 100. Did they learn, or just memorise? You cannot tell.

To know if a model really learned, we must test it on examples it has **never seen**. So we split the data:

| Part | Usual size | Used for | School example |
|---|---|---|---|
| **Training set** | 60-80 percent | The model learns from it | Textbook exercises |
| **Validation set** | 10-20 percent | We tune settings and pick the best model | Mock tests |
| **Test set** | 10-20 percent | The **final, honest** score. Use it once at the end | The final board exam |

In scikit-learn: `train_test_split(X, y, test_size=0.2, random_state=42)`.
`random_state=42` makes the random split the same every time, so results can be repeated. (42 is just a habit; any number works.)

**Cross-validation:** instead of one validation set, split the training data into 5 parts, train 5 times, each time testing on a different part, and average the scores. More reliable when data is small.

### 2. Fitting, loss and epochs

- **Fitting** = training = `model.fit(...)`. The model adjusts its internal numbers to match the training data.
- **Loss** = a number that says **how wrong** the model is. Lower is better. Training tries to make the loss small (Lesson 04: gradient descent).
- **Epoch** = one full pass through **all** the training data. Many models (especially neural networks, Day 2) train for many epochs: epoch 1, epoch 2, ... and the loss usually goes down each epoch.

### 3. Underfitting and overfitting

| | Underfitting | Good fit | Overfitting |
|---|---|---|---|
| Meaning | Model is **too simple**, misses the pattern | Learns the real pattern | Model **memorises** training data, including noise |
| Training score | Low | High | Very high (often near 100 percent) |
| Test score | Low | High | Much **lower** than training |
| Student example | Did not study at all | Understood the concepts | Memorised the answers of last year's paper word by word |
| Fix | Use a more powerful model, better features | - | Simpler model, more data, limit depth, regularisation |

**How to spot overfitting:** compare training score and test score. A big gap = overfitting.

### 4. Bias and variance

Two kinds of errors, explained with darts:

- **High bias** = the darts all land **in the same wrong place**. The model has a wrong, too-simple idea. This causes **underfitting**.
- **High variance** = the darts land **all over the place**. The model changes a lot with small changes in data. This causes **overfitting**.

The **bias-variance trade-off**: making a model more complex lowers bias but raises variance. We look for the middle - complex enough to learn, simple enough to generalise.

### 5. Metrics for classification

Suppose a model checks 100 students to find who will **fail** (so teachers can help them). "Positive" here means "predicted fail".

#### The confusion matrix

A 2 x 2 table that shows **every kind of right and wrong answer**:

|                  | Model says: fail (positive) | Model says: pass (negative) |
|---|---|---|
| **Really failed** | **True Positive (TP)** - correctly caught | **False Negative (FN)** - missed a student who needed help |
| **Really passed** | **False Positive (FP)** - false alarm | **True Negative (TN)** - correctly left alone |

#### The four main metrics

| Metric | Formula | Question it answers |
|---|---|---|
| **Accuracy** | (TP + TN) / all | Out of everything, how often was the model right? |
| **Precision** | TP / (TP + FP) | When the model says "fail", how often is it really a fail? (Few false alarms) |
| **Recall** | TP / (TP + FN) | Out of all real fails, how many did the model catch? (Few misses) |
| **F1-score** | 2 x (P x R) / (P + R) | One number that balances precision and recall |

**Why accuracy is not enough:** if only 5 out of 100 people have a disease, a lazy model that always says "healthy" gets **95 percent accuracy** but catches **zero** sick people. Its recall is 0. Always look at precision and recall too.

**Which one matters more?**

- **Recall** matters most when **missing** is dangerous: disease detection, fraud detection, students at risk of failing.
- **Precision** matters most when **false alarms** are costly: marking a good email as spam, blocking a genuine customer's card.

### 6. Metrics for regression

| Metric | Meaning |
|---|---|
| **MAE** (Mean Absolute Error) | Average size of the mistakes. "On average we are off by 4 marks." Easy to explain. |
| **RMSE** (Root Mean Squared Error) | Like MAE but punishes big mistakes more. |
| **R squared (R2)** | How much of the variation the model explains. 1.0 = perfect, 0 = no better than guessing the average. |

---

## Do it now

Open `notebooks/06_Train_and_Evaluate.ipynb`, select the `.venv` kernel and run every cell. You will:

- split data into train, validation and test sets,
- see overfitting happen with a deep decision tree and fix it,
- draw a confusion matrix and calculate every metric by hand and with scikit-learn,
- watch the loss go down over epochs,
- evaluate a regression model with MAE and R2,
- use cross-validation.

---

## Check

- [ ] The overfitting chart shows training accuracy going to 1.0 while validation accuracy stops improving or drops.
- [ ] The confusion matrix picture shows 4 numbers that add up to the test set size.
- [ ] Your hand-calculated precision and recall match scikit-learn's numbers.
- [ ] The epochs chart shows loss going down.
- [ ] The final model's test accuracy is printed only once, at the end.

---

## What just happened?

You followed the professional evaluation process:

```text
split -> train on training set -> compare models on validation set -> pick the best -> test ONCE on the test set -> report precision, recall, F1, not just accuracy
```

---

## Try it yourself

1. A spam filter has TP = 40, FP = 10, FN = 20, TN = 130. Calculate accuracy, precision and recall by hand. (Answers in `practice/ANSWERS.md`.)
2. In the notebook, change `test_size` from 0.2 to 0.5. Does the test score change? Why might a too-small training set hurt?
3. A model scores 99 percent on training data and 70 percent on test data. What is the problem and how could you fix it?

---

## If it does not work

| Problem | Fix |
|---|---|
| `UndefinedMetricWarning: Precision is ill-defined` | The model never predicted the positive class. Check your labels and the `pos_label` setting. |
| Scores change every run | Add `random_state=42` to `train_test_split` and to the model. |
| `ValueError: pos_label=1 is not a valid label` | Our labels are text. Use `pos_label="fail"` (or whichever class you mean). |

Next: **[Lesson 09 - Day 1 checklist](09_DAY_1_CHECKLIST.md)**
