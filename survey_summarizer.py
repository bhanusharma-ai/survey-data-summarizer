"""
Survey Data Summarizer (Multi-Format)
-------------------------------------
Generates an instant quality + summary report for survey data.
Supports CSV, Excel (.xlsx), and SPSS (.sav) files - so anyone in
market research can use it, whatever format their data is in.

Built from 8 years of market research data processing experience.
Author: Bhanu Sharma
Tech: Python, Pandas, pyreadstat
"""

import pandas as pd


def load_data(filepath):
    """
    Smart loader - detects file type and reads CSV, Excel, or SPSS.
    Returns the dataframe (and SPSS labels if available).
    """
    meta = None
    lower = filepath.lower()

    if lower.endswith(".csv"):
        df = pd.read_csv(filepath)
        print("Loaded CSV file.")

    elif lower.endswith((".xlsx", ".xls")):
        df = pd.read_excel(filepath)
        print("Loaded Excel file.")

    elif lower.endswith(".sav"):
        # SPSS file - use pyreadstat to also capture labels
        try:
            import pyreadstat
        except ImportError:
            raise ImportError(
                "Reading .sav needs pyreadstat. Install it first:\n"
                "   pip install pyreadstat"
            )
        df, meta = pyreadstat.read_sav(filepath)
        print("Loaded SPSS (.sav) file - with variable labels.")

    else:
        raise ValueError("Unsupported file type. Use .csv, .xlsx, or .sav")

    return df, meta


def summarize_survey(filepath, grid_cols=None):
    """
    Loads survey data (CSV / Excel / SPSS) and prints a full
    summary + quality report.

    Parameters:
        filepath (str): path or URL to a .csv, .xlsx, or .sav file
        grid_cols (list): optional grid question columns for
                          straightliner detection
    """

    # --- 1. Load data (any format) ---
    df, meta = load_data(filepath)

    print("=" * 45)
    print("SURVEY DATA SUMMARY REPORT")
    print("=" * 45)
    print("Base size (respondents):", df.shape[0])
    print("Variables (columns):", df.shape[1])
    print("\nColumns:", list(df.columns))

    # Show SPSS variable labels if present
    if meta is not None and meta.column_labels:
        print("\n--- VARIABLE LABELS (from SPSS) ---")
        for name, label in zip(meta.column_names, meta.column_labels):
            if label:
                print(f"  {name}: {label}")

    # --- 2. Preview ---
    print("\n--- PREVIEW (first 5 rows) ---")
    print(df.head())

    # --- 3. Descriptive statistics ---
    print("\n--- DESCRIPTIVE STATISTICS ---")
    print(df.describe())

    # --- 4. Frequencies for category columns ---
    print("\n--- FREQUENCIES ---")
    for col in df.select_dtypes(include="object").columns:
        print(f"\n{col}:")
        print(df[col].value_counts())

    # --- 5. Missing data check ---
    print("\n--- MISSING DATA CHECK ---")
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(missing[missing > 0])
    else:
        print("No missing data - clean!")

    # --- 6. Straightliner detection ---
    if grid_cols:
        print("\n--- STRAIGHTLINER CHECK ---")
        df["grid_sd"] = df[grid_cols].std(axis=1)
        df["straightliner"] = df["grid_sd"] < 0.5
        print("Flagged straightliners:", int(df["straightliner"].sum()))
        print("(low variation across grid = same answer repeated)")

    # --- 7. Save clean file ---
    df.to_csv("survey_summary.csv", index=False)
    print("\nSaved cleaned file: survey_summary.csv")

    return df


if __name__ == "__main__":
    # Demo with CSV. For your data, just point to a .csv, .xlsx, or .sav:
    #   summarize_survey("mydata.sav", grid_cols=["q1","q2","q3"])
    #   summarize_survey("mydata.xlsx", grid_cols=["q1","q2","q3"])
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"
    df = summarize_survey(url, grid_cols=["total_bill", "tip", "size"])
