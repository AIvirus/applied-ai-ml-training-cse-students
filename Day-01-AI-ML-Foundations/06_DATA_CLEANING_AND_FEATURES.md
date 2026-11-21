# Lesson 06 - Clean Your Data and Build Features

**Time:** 40 minutes  |  **Notebook:** `notebooks/04_Clean_Data_and_Features.ipynb`

---

## Goal

By the end of this lesson you can:

- find and fix **missing values**, **duplicates** and **outliers**,
- fix messy text like `" YES"` and `"yes"`,
- tell **numerical** from **categorical** data,
- turn categories into numbers (**encoding**),
- put numbers on the same scale (**scaling**),
- explain **feature selection** and **feature engineering**.

---

## Understand

Real data is messy. People make typing mistakes, forms are left empty, the same row gets saved twice. Models cannot fix this for you. So before training, we **clean**.

### 1. Missing values

An empty cell. pandas shows it as `NaN` ("Not a Number").

| Way to handle it | When to use it |
|---|---|
| **Drop the row** | Only a few rows are missing, and you have lots of data |
| **Drop the column** | Most of the column is empty |
| **Fill with the median** (or mean) | Number columns. Median is safer if there are outliers |
| **Fill with the mode** (most common value) | Category columns |
| **Fill with a constant** like `"unknown"` | When "missing" itself means something |

### 2. Duplicates

The same row saved more than once. It makes the model think that example is more important than it is. Fix: `df.drop_duplicates()`.

### 3. Outliers

Values that are very far from the others. Two kinds:

- **Mistakes:** attendance of `450` percent, sleep of `-3` hours. These are impossible -> fix or remove.
- **Real but rare:** a student who really studied 9.5 hours. Keep these - they are true.

A common rule to find outliers is the **IQR rule**: a value is an outlier if it is far below the 25th percentile or far above the 75th percentile (more than 1.5 times the middle spread). But always also use **common sense rules**: attendance must be 0 to 100.

### 4. Messy text

`"yes"`, `"Yes"`, `" YES"` and `"yes "` all mean the same, but the computer sees 4 different values. Fix: remove spaces and make lower case: `df["col"].str.strip().str.lower()`.

### 5. Numerical and categorical data

| Type | Meaning | Examples in our data |
|---|---|---|
| **Numerical** | Numbers you can do maths on | `hours_studied`, `final_score` |
| **Categorical** | Names of groups | `city_type`, `internet_access` |

Categorical data has two kinds: **nominal** (no order: urban, rural) and **ordinal** (has an order: low < medium < high).

### 6. Encoding - turning categories into numbers

ML models only understand numbers. So we **encode** categories.

**Yes/No columns** -> 1 and 0:

| internet_access | internet_access (encoded) |
|---|---|
| yes | 1 |
| no | 0 |

**One-hot encoding** for columns with more than two groups - one new column per group:

| city_type | city_rural | city_semi-urban | city_urban |
|---|---|---|---|
| urban | 0 | 0 | 1 |
| rural | 1 | 0 | 0 |

Why not just urban = 1, semi-urban = 2, rural = 3? Because the model would think rural is "3 times" urban, which is meaningless. One-hot avoids fake order.

### 7. Scaling

`attendance_percent` goes from 45 to 100. `sleep_hours` goes from 4 to 9. Some algorithms (like KNN and SVM in the next lesson) measure distances, so the column with **bigger numbers** would wrongly look more important.

**Scaling** puts all columns on a similar range:

| Method | What it does | Result range |
|---|---|---|
| **Standardisation** (`StandardScaler`) | Subtract the mean, divide by the standard deviation | Mostly between -3 and +3, mean 0 |
| **Normalisation** (`MinMaxScaler`) | Squeeze into a fixed range | 0 to 1 |

### 8. Feature selection and feature engineering

- **Feature selection** = keeping only useful columns. `student_id` is just a name tag; it cannot help predict marks, so we remove it. Removing useless columns makes models simpler and often better.
- **Feature engineering** = **creating new, more useful columns** from existing ones, using your understanding of the problem. Examples:
  - `study_per_sleep = hours_studied / sleep_hours`
  - `well_rested = 1 if sleep_hours >= 7 else 0`
  - From a date: day of week, month, is_holiday.

Good feature engineering often improves a model more than choosing a fancier algorithm.

### 9. Data leakage (an important warning)

Never use a column that **contains the answer** as a feature. If we predict `result` (pass/fail) and also give the model `final_score`, it just learns "score >= 50 means pass". It looks perfect in testing but is useless in real life, because you will not know the final score in advance. This mistake is called **data leakage**.

---

## Do it now

Open `notebooks/04_Clean_Data_and_Features.ipynb`, select the `.venv` kernel and run every cell. You will clean `student_performance_messy.csv` step by step and save a clean, model-ready file.

---

## Check

- [ ] After cleaning, `df.isna().sum()` shows **0** for every column.
- [ ] `df.duplicated().sum()` shows **0**.
- [ ] `internet_access` contains only `yes` and `no`, and `city_type` only `urban`, `semi-urban` and `rural`.
- [ ] No attendance is above 100 and no sleep value is below 0.
- [ ] The final table has new columns like `city_rural`, `city_urban` and `well_rested`.

---

## What just happened?

You followed the standard cleaning recipe used in real projects:

```text
load -> look -> fix text -> remove duplicates -> fix impossible values -> fill missing -> encode -> engineer features -> scale -> save
```

Each step was small and checked. This is also how you should work with AI coding assistants on Day 3: small steps, check each one.

---

## Try it yourself

1. Instead of filling missing `hours_studied` with the median, drop those rows. How many rows are left?
2. Create a new feature `high_attendance` that is 1 when attendance is 85 or more.
3. Explain in one line why we should not one-hot encode `student_id`.

---

## If it does not work

| Problem | Fix |
|---|---|
| `AttributeError: Can only use .str accessor with string values` | That column is not text. Only use `.str` on text columns. |
| Your changes "disappear" | Many pandas commands return a **new** table. Save it: `df = df.drop_duplicates()`. |
| `SettingWithCopyWarning` | Only a warning. Add `.copy()` when you make a smaller table: `small = df[df.x > 1].copy()`. |
| Different row count from the notebook text | Check that you ran the cells in order from the top. Use **Restart** then **Run All**. |

Next: **[Lesson 07 - Common ML algorithms](07_ML_ALGORITHMS.md)**
