# Lesson 09 - Day 1 Checklist and Practice

**Time:** 15 minutes (more if you do the full workbook)

---

## Tick what you can do

Be honest. If you cannot tick a line, go back to the lesson shown in brackets.

### Ideas (you can explain them to a friend)

- [ ] What AI is, and the difference between narrow AI and general AI (01)
- [ ] The difference between AI and automation (01)
- [ ] How AI, Machine Learning and Deep Learning fit inside each other (01)
- [ ] Traditional programming vs machine learning (03)
- [ ] Dataset, feature (X) and label (y) (03)
- [ ] Supervised, unsupervised, semi-supervised and reinforcement learning (03)
- [ ] Regression vs classification (03, 07)
- [ ] Vectors, matrices, mean, median, mode, standard deviation, probability, correlation (04)
- [ ] Gradient descent as "walking downhill to reduce the loss" (04)
- [ ] Data analysis vs analytics vs data science vs data engineering (05)
- [ ] Structured vs unstructured data, and the 3 Vs of big data (05)
- [ ] Missing values, duplicates, outliers, encoding, scaling, feature engineering, data leakage (06)
- [ ] How linear regression, logistic regression, decision tree, random forest, KNN, SVM and K-means work (07)
- [ ] Training, validation and test sets; epochs and loss (08)
- [ ] Overfitting vs underfitting; bias vs variance (08)
- [ ] Accuracy, precision, recall, F1 and the confusion matrix, and when accuracy is misleading (08)

### Skills (you did them in a notebook)

- [ ] Open a notebook in VS Code with the `.venv` kernel and run cells
- [ ] Load a CSV with pandas and do EDA (`shape`, `head`, `info`, `describe`, `groupby`)
- [ ] Draw a histogram, bar chart, scatter plot and box plot
- [ ] Clean a messy dataset and save the clean version
- [ ] Train a model with `fit` and use it with `predict`
- [ ] Split data with `train_test_split` and evaluate with a confusion matrix and classification report

---

## Practice

Open **[practice/WORKBOOK.md](practice/WORKBOOK.md)**. Answer the questions in your own words first, then check **[practice/ANSWERS.md](practice/ANSWERS.md)**.

---

## Mini project (optional, 30 to 60 minutes)

Use what you learned on a **new** dataset that comes inside scikit-learn (no download needed):

```python
from sklearn.datasets import load_breast_cancer
data = load_breast_cancer(as_frame=True)
df = data.frame          # 569 rows, 30 features + "target" (0 = malignant, 1 = benign)
```

1. Do EDA: shape, describe, how many of each target class.
2. Split into train and test sets.
3. Train logistic regression (with scaling) and a random forest.
4. Print the confusion matrix and classification report for both.
5. Write 3 lines: which model is better, and is **recall** for the malignant class (target 0) more important than precision here? Why?

---

## What is next?

Tomorrow (Day 2) you will go **deep**: neural networks, how computers read text (NLP) and see images (Computer Vision), and how today's Generative AI and chatbots really work - and you will call a real AI model from Python.

Go to **[Day 2 - Start here](../Day-02-Modern-AI-Domains/00_START_HERE.md)**
