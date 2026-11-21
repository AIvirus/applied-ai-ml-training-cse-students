"""
csv_tools.py - read a CSV file, find simple insights and draw a chart.
"""

import base64
import io

import matplotlib

matplotlib.use("Agg")  # draw charts into memory (a server has no screen)
import matplotlib.pyplot as plt
import pandas as pd

from app.llm import ask_llm


class CSVError(ValueError):
    """A problem with the CSV file that the user can fix."""


def read_csv(data):
    try:
        df = pd.read_csv(io.BytesIO(data))
    except Exception as error:
        raise CSVError(f"Could not read this CSV file ({type(error).__name__}).") from error
    if df.empty or len(df.columns) == 0:
        raise CSVError("The CSV file has no rows.")
    if len(df) > 100_000:
        raise CSVError("The CSV file is too big for this demo (more than 100,000 rows).")
    return df


def find_insights(df):
    """Simple, rule-based facts about the table (no AI needed)."""
    insights = [f"The table has {len(df)} rows and {len(df.columns)} columns."]

    missing = df.isna().sum()
    for column, count in missing[missing > 0].items():
        insights.append(f"Column '{column}' has {count} missing values.")

    numbers = df.select_dtypes("number")
    for column in numbers.columns[:5]:
        insights.append(
            f"'{column}': average {numbers[column].mean():.2f}, lowest {numbers[column].min()}, highest {numbers[column].max()}."
        )

    if numbers.shape[1] >= 2:
        corr = numbers.corr().abs()
        pairs = [(corr.iloc[i, j], corr.columns[i], corr.columns[j])
                 for i in range(len(corr)) for j in range(i + 1, len(corr))]
        pairs = [p for p in pairs if pd.notna(p[0])]
        if pairs:
            value, a, b = max(pairs)
            insights.append(f"The strongest relationship is between '{a}' and '{b}' (correlation {value:.2f}).")

    for column in df.select_dtypes(exclude="number").columns[:3]:
        top = df[column].value_counts()
        if not top.empty:
            insights.append(f"Most common value in '{column}' is '{top.index[0]}' ({top.iloc[0]} rows).")
    return insights


def make_chart(df, column=None):
    """Draw a histogram (number column) or bar chart (text column). Return it as base64 PNG text."""
    if column is None:
        numeric = df.select_dtypes("number").columns
        column = numeric[0] if len(numeric) else df.columns[0]
    if column not in df.columns:
        raise CSVError(f"Column '{column}' is not in the file. Columns: {', '.join(map(str, df.columns))}")

    fig, ax = plt.subplots(figsize=(7, 4))
    if pd.api.types.is_numeric_dtype(df[column]):
        ax.hist(df[column].dropna(), bins=15, edgecolor="black")
        ax.set_ylabel("Number of rows")
    else:
        df[column].value_counts().head(10).plot.bar(ax=ax)
        ax.set_ylabel("Count")
    ax.set_title(f"Distribution of '{column}'")
    ax.set_xlabel(str(column))
    fig.tight_layout()

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    plt.close(fig)
    return column, base64.b64encode(buffer.getvalue()).decode("ascii")


def analyse_csv(data, column=None):
    df = read_csv(data)
    insights = find_insights(df)
    chart_column, chart = make_chart(df, column)

    # Ask the AI to explain the facts in plain words (only the summary is sent, never the whole file)
    facts = "\n".join(insights)
    explanation, mode = ask_llm(
        f"Here are facts about a data table:\n{facts}\n\nExplain the 3 most interesting points for a student in simple English.",
        temperature=0.3,
        mock_answer="Key points: " + " ".join(insights[1:4]),
    )
    return {
        "rows": len(df),
        "columns": [str(c) for c in df.columns],
        "preview": df.head(5).astype(str).to_dict(orient="records"),
        "insights": insights,
        "explanation": explanation,
        "chart_column": str(chart_column),
        "chart_png_base64": chart,
        "mode": mode,
    }
