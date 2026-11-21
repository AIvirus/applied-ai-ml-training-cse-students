# Day 1 - AI, Machine Learning and Data Science Foundations

**Goal of the day:** understand what AI really is, how a machine "learns" from examples, why data is the most important ingredient, and train and test your first machine learning models with Python.

You do not need to know anything about AI before you start.

---

## Your plan for today (do these in order)

| # | Lesson (read) | Notebook (do) | Time |
|---|---|---|---|
| 01 | [What is AI?](01_WHAT_IS_AI.md) | - | 35 min |
| 02 | [Set up your computer](02_SET_UP_YOUR_COMPUTER.md) | `00_Check_Your_Setup.ipynb` | 40 min |
| 03 | [How machines learn](03_HOW_MACHINES_LEARN.md) | `01_How_Machines_Learn.ipynb` | 35 min |
| 04 | [The maths you need (only the idea)](04_MATHS_INTUITION.md) | `02_Maths_for_ML.ipynb` | 45 min |
| 05 | [Data analysis and data science](05_DATA_ANALYSIS_AND_DATA_SCIENCE.md) | `03_Explore_and_Visualise_Data.ipynb` | 45 min |
| -- | **Lunch break** | | 60 min |
| 06 | [Clean your data and build features](06_DATA_CLEANING_AND_FEATURES.md) | `04_Clean_Data_and_Features.ipynb` | 40 min |
| 07 | [Common ML algorithms](07_ML_ALGORITHMS.md) | `05_ML_Algorithms.ipynb` | 50 min |
| 08 | [Train, test and evaluate a model](08_TRAIN_TEST_AND_EVALUATE.md) | `06_Train_and_Evaluate.ipynb` | 45 min |
| 09 | [Day 1 checklist and practice](09_DAY_1_CHECKLIST.md) | `practice/WORKBOOK.md` | 15 min |

Morning (10:00 AM to 1:20 PM): lessons 01 to 05. Afternoon (2:20 PM to 4:40 PM): lessons 06 to 09.

---

## What is in this folder?

```text
Day-01-AI-ML-Foundations/
|-- 00_START_HERE.md                you are here
|-- 01_ ... 09_ lessons             read these in order
|-- notebooks/                      the practical part (Python code you run)
|   |-- 00_Check_Your_Setup.ipynb
|   |-- 01_How_Machines_Learn.ipynb
|   |-- 02_Maths_for_ML.ipynb
|   |-- 03_Explore_and_Visualise_Data.ipynb
|   |-- 04_Clean_Data_and_Features.ipynb
|   |-- 05_ML_Algorithms.ipynb
|   `-- 06_Train_and_Evaluate.ipynb
|-- data/
|   |-- student_performance.csv        300 students: study hours, attendance, marks...
|   `-- student_performance_messy.csv  the same kind of data, but with mistakes to clean
`-- practice/
    |-- WORKBOOK.md                 revision questions
    `-- ANSWERS.md                  answers (try first!)
```

### About our dataset

All of Day 1 uses one easy dataset: **300 students** and their study habits. Each row is one student.

| Column | Meaning |
|---|---|
| `student_id` | A name tag like S001 |
| `hours_studied` | Hours studied per day |
| `attendance_percent` | Class attendance in percent |
| `sleep_hours` | Hours of sleep per night |
| `previous_score` | Marks in the previous exam (out of 100) |
| `internet_access` | yes / no |
| `extra_classes` | yes / no |
| `city_type` | urban / semi-urban / rural |
| `final_score` | Marks in the final exam (out of 100) |
| `result` | pass (50 or more) / fail |

The data is **made up for learning** (no real student is in it), but it behaves like real data.

---

Start with **[Lesson 01 - What is AI?](01_WHAT_IS_AI.md)**
