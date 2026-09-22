"""
main.py
--------
One command to run the FULL pipeline end-to-end:
    Raw data --> Clean --> Report (Excel + PNG dashboard)

Run:
    python main.py

To use YOUR OWN data instead of the sample data:
    python main.py --input path/to/your_file.csv
"""

import argparse
import os
import pandas as pd

from data_cleaning import clean_data
from report_generator import generate_report


def main(input_path: str):
    os.makedirs("output", exist_ok=True)

    print(f"Reading data from: {input_path}")
    df_raw = pd.read_csv(input_path)
    print(f"  -> {len(df_raw)} rows loaded")

    print("Cleaning data...")
    df_clean, log = clean_data(df_raw)
    df_clean.to_csv("output/cleaned_sales_data.csv", index=False)
    print("  -> Cleaning summary:")
    for k, v in log.items():
        print(f"     {k}: {v}")

    print("Generating report...")
    generate_report(df_clean, log)

    print("\nDone! Check the 'output/' folder for:")
    print("   - cleaned_sales_data.csv")
    print("   - Sales_Report.xlsx")
    print("   - summary_dashboard.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data Cleaning & Reporting Automation")
    parser.add_argument(
        "--input",
        default="data/raw_sales_data.csv",
        help="Path to input CSV file (default: sample dataset)",
    )
    args = parser.parse_args()
    main(args.input)
