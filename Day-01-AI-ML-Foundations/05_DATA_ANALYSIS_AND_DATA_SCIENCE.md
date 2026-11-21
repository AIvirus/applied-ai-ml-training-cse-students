# Lesson 05 - Data Analysis and Data Science

**Time:** 45 minutes  |  **Notebook:** `notebooks/03_Explore_and_Visualise_Data.ipynb`

---

## Goal

By the end of this lesson you can:

- explain the difference between data analytics, data analysis, data science and data engineering,
- tell **structured** from **unstructured** data,
- describe how data is **collected**,
- do **Exploratory Data Analysis (EDA)** with pandas,
- draw basic charts with matplotlib,
- explain what **big data** means.

---

## Understand

### 1. Why data matters so much

A machine learning model can only be as good as the data it learns from. People say: **"Garbage in, garbage out."** If the examples are wrong, missing or unfair, the model will be wrong or unfair too. That is why data work takes most of the time in real AI projects (often 60 to 80 percent).

### 2. Four job words that sound the same

| Word | Simple meaning | Main question it answers | Example |
|---|---|---|---|
| **Data analysis** | Looking closely at data to find facts | "What is in this data?" | "Average marks are 55. Rural students study 1 hour less." |
| **Data analytics** | Using analysis regularly to help business decisions, often with dashboards | "What happened and what should we do?" | A weekly sales dashboard for a shop owner |
| **Data science** | Analysis + statistics + machine learning to **predict** and build data products | "What will happen next?" | A model that predicts which students may fail, so teachers can help early |
| **Data engineering** | Building the **pipes** that collect, clean, store and move data reliably | "How does the data get here, every day, correctly?" | A system that copies attendance from 50 colleges into one database every night |

A simple picture of how they work together:

```text
 Data sources  -->  DATA ENGINEERING  -->  clean stored data  -->  ANALYSIS / ANALYTICS  -->  reports, dashboards
 (apps, forms,      (collect, clean,                          \
  sensors, web)      store, move)                              -->  DATA SCIENCE / ML  -->  predictions, AI features
```

### 3. Structured and unstructured data

| | Structured data | Unstructured data |
|---|---|---|
| What it looks like | Neat **tables** with rows and columns | No fixed table shape |
| Examples | Marks sheet, bank transactions, train timetable | Emails, chat messages, photos, videos, voice recordings, PDFs |
| Stored in | Spreadsheets, SQL databases | Files, object storage, document databases |
| Easy for classic ML? | Yes | Needs extra steps (NLP for text, Computer Vision for images - Day 2) |

There is also **semi-structured** data like JSON, which has labels but not a fixed table:
`{"name": "Asha", "skills": ["Python", "SQL"]}`

Most data in the world (about 80 percent) is unstructured.

### 4. How is data collected?

- **Forms and surveys** (Google Forms, admission forms)
- **Apps and websites** (every click, purchase and login)
- **Sensors and devices** (temperature sensors, smart watches, CCTV)
- **Public datasets** (government open data like data.gov.in, Kaggle, UCI repository)
- **Web scraping** (collecting from websites - only where it is allowed)
- **Buying or partnering** (data from other companies)

Always ask: **Do we have permission to use this data? Does it contain private information?** (More on privacy on Day 2.)

### 5. Exploratory Data Analysis (EDA)

**EDA** means "getting to know your data" **before** building any model. It is like reading the whole question paper before you start answering.

The EDA checklist:

| Step | Question | pandas command |
|---|---|---|
| 1 | How big is it? | `df.shape` |
| 2 | What do the first rows look like? | `df.head()` |
| 3 | What are the column types? Any missing values? | `df.info()` |
| 4 | What are the basic statistics? | `df.describe()` |
| 5 | How many of each category? | `df["city_type"].value_counts()` |
| 6 | How do groups compare? | `df.groupby("extra_classes")["final_score"].mean()` |
| 7 | Which columns move together? | `df.corr(numeric_only=True)` |
| 8 | What does it look like? | charts |

### 6. Data visualisation - which chart when?

| Chart | Use it to show | Example |
|---|---|---|
| **Histogram** | How values are spread (the distribution) | How many students got 0-10, 10-20, ... marks |
| **Bar chart** | Compare categories | Average marks for urban, semi-urban, rural |
| **Scatter plot** | Relationship between two numbers | Hours studied vs final marks |
| **Line chart** | Change over time | Marks across 6 monthly tests |
| **Box plot** | Spread and outliers | Marks by city type, with unusual values marked as dots |
| **Pie chart** | Parts of a whole (use rarely, max 4-5 parts) | Pass vs fail share |

A good chart has a **title**, **axis labels** and shows **one clear message**.

### 7. Big data

**Big data** is data so big, fast or varied that one normal computer cannot handle it. It is described with the **3 Vs** (sometimes 5):

- **Volume** - huge amounts (YouTube gets hundreds of hours of video every minute).
- **Velocity** - arrives very fast (UPI processes thousands of payments every second).
- **Variety** - many types (text, images, numbers, video).
- Extra Vs: **Veracity** (is it trustworthy?) and **Value** (is it useful?).

Big data needs special tools that split the work over many computers, such as **Apache Spark**, **Hadoop** and cloud data warehouses like **BigQuery** and **Snowflake**. Today our data is small, so pandas on one laptop is perfect.

---

## Do it now

Open `notebooks/03_Explore_and_Visualise_Data.ipynb`, select the `.venv` kernel and run every cell. You will do the full EDA checklist and draw a histogram, a bar chart, a scatter plot, a box plot and a correlation heatmap.

---

## Check

- [ ] `df.shape` shows `(300, 10)`.
- [ ] `df.info()` shows no missing values in this clean file.
- [ ] You see 5 charts, each with a title.
- [ ] You can answer from the output: "Do students with extra classes score more on average?"

---

## What just happened?

- `pd.read_csv()` loaded the CSV file into a **DataFrame** (pandas' word for a table).
- `describe()` gave count, mean, std, min, max and quartiles for every number column in one go.
- `groupby()` compared groups. This is how analysts find facts like "students with extra classes score about 3 marks more".
- matplotlib drew the charts. The scatter plot showed the clear upward pattern between hours and marks - the pattern our model will learn later.

---

## Try it yourself

1. Find the average `final_score` for each `city_type`. Which group is highest?
2. Draw a histogram of `sleep_hours`. Is it spread evenly?
3. Draw a scatter plot of `attendance_percent` against `final_score`. Is the pattern as strong as for hours studied?
4. Write 3 "facts" you discovered about this data, in plain sentences, like a data analyst's report.

---

## If it does not work

| Problem | Fix |
|---|---|
| `KeyError: 'final score'` | Column names must match exactly, with underscores: `final_score`. Use `df.columns` to see all names. |
| Charts overlap or look squashed | Add `plt.figure(figsize=(8, 4))` before the chart. |
| Text labels on a bar chart overlap | Add `plt.xticks(rotation=45)`. |
| `TypeError: Could not convert ... to numeric` in `groupby().mean()` | Select a number column before `.mean()`, like `df.groupby("city_type")["final_score"].mean()`. |

Next: lunch break, then **[Lesson 06 - Clean your data and build features](06_DATA_CLEANING_AND_FEATURES.md)**
