"""
data_cleaning.py
------------------
Reusable, automated data-cleaning pipeline.

Handles:
    1. Missing values      -> smart fill / drop
    2. Duplicate records    -> removed
    3. Inconsistent text    -> trimmed, case-normalized
    4. Invalid numeric data -> negative / absurd outliers fixed
    5. Invalid / missing dates -> parsed, bad rows flagged

Usage:
    from data_cleaning import clean_data
    df_clean, log = clean_data(df)
"""

import pandas as pd
import numpy as np


def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Cleans a raw sales-style DataFrame and returns the cleaned DataFrame
    plus a log (dict) summarizing what was fixed -- used later in the report.
    """
    log = {}
    df = df.copy()
    log["rows_before"] = len(df)

    # ---------------------------------------------------------------
    # 1. Remove exact duplicate rows
    # ---------------------------------------------------------------
    dup_count = df.duplicated().sum()
    df = df.drop_duplicates()
    log["duplicates_removed"] = int(dup_count)

    # ---------------------------------------------------------------
    # 2. Standardize text columns (trim spaces, fix casing)
    # ---------------------------------------------------------------
    text_cols = ["Region", "Product", "SalesRep"]
    for col in text_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.title()
                .replace({"None": np.nan, "Nan": np.nan, "": np.nan})
            )

    # ---------------------------------------------------------------
    # 3. Handle missing values
    # ---------------------------------------------------------------
    missing_before = df.isna().sum().sum()

    # Categorical -> fill with "Unknown"
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    # Quantity -> fill missing with median of valid values
    if "Quantity" in df.columns:
        df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
        valid_qty_median = df.loc[df["Quantity"] > 0, "Quantity"].median()
        df["Quantity"] = df["Quantity"].fillna(valid_qty_median)
        # Fix invalid quantities (negative or absurdly large -> treat as bad data)
        df.loc[df["Quantity"] <= 0, "Quantity"] = valid_qty_median
        df.loc[df["Quantity"] > 100, "Quantity"] = valid_qty_median
        df["Quantity"] = df["Quantity"].round().astype(int)

    # UnitPrice -> fill missing with median of valid values
    if "UnitPrice" in df.columns:
        df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
        valid_price_median = df.loc[df["UnitPrice"] > 0, "UnitPrice"].median()
        df["UnitPrice"] = df["UnitPrice"].fillna(valid_price_median)
        df.loc[df["UnitPrice"] <= 0, "UnitPrice"] = valid_price_median

    # OrderDate -> parse; drop rows where date is unparseable/missing
    if "OrderDate" in df.columns:
        df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")
        bad_dates = df["OrderDate"].isna().sum()
        df = df.dropna(subset=["OrderDate"])
        log["rows_dropped_bad_date"] = int(bad_dates)
    else:
        log["rows_dropped_bad_date"] = 0

    log["missing_values_fixed"] = int(missing_before)

    # ---------------------------------------------------------------
    # 4. Derived column: TotalSale
    # ---------------------------------------------------------------
    if {"Quantity", "UnitPrice"}.issubset(df.columns):
        df["TotalSale"] = df["Quantity"] * df["UnitPrice"]

    # ---------------------------------------------------------------
    # 5. Final tidy-up
    # ---------------------------------------------------------------
    df = df.reset_index(drop=True)
    log["rows_after"] = len(df)
    log["rows_removed_total"] = log["rows_before"] - log["rows_after"]

    return df, log


if __name__ == "__main__":
    raw = pd.read_csv("data/raw_sales_data.csv")
    cleaned, summary = clean_data(raw)
    cleaned.to_csv("output/cleaned_sales_data.csv", index=False)
    print("Cleaning complete.")
    for k, v in summary.items():
        print(f"  {k}: {v}")
