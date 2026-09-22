# 🧹 Data Cleaning & Reporting Automation

Automated Python pipeline that cleans messy datasets and generates
professional Excel reports + a visual dashboard — with one command.

## ✨ Features

- **Handles missing values** — smart fill using median/mode, sensible defaults
- **Removes duplicates** — automatically detected and dropped
- **Fixes inconsistent data** — trims whitespace, normalizes text casing (`north`, `NORTH`, ` North ` → `North`)
- **Fixes invalid numbers** — negative/absurd outliers replaced with median
- **Parses & validates dates** — bad/unparseable dates flagged and removed
- **Generates automated reports**:
  - 📊 Excel workbook (`Sales_Report.xlsx`) with Summary, Cleaned Data, Region Summary (bar chart), and Product Summary (pie chart) — all built with native Excel charts
  - 🖼️ PNG visual dashboard (`summary_dashboard.png`) with 4 charts: sales by region, product share, monthly trend, sales by rep

## 📁 Project Structure

```
data-cleaning-reporting/
├── data/
│   └── raw_sales_data.csv        # sample dirty dataset (auto-generated)
├── output/                       # all generated files land here
│   ├── cleaned_sales_data.csv
│   ├── Sales_Report.xlsx
│   └── summary_dashboard.png
├── generate_sample_data.py       # creates a sample messy dataset
├── data_cleaning.py              # cleaning pipeline (reusable module)
├── report_generator.py           # Excel + PNG report builder
├── main.py                       # runs everything end-to-end
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

```bash
# 1. Clone this repo
git clone <your-repo-url>
cd data-cleaning-reporting

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) generate a sample dirty dataset to try it out
python generate_sample_data.py

# 4. Run the full pipeline
python main.py
```

That's it — check the `output/` folder for your cleaned data and reports.

## 🔧 Using Your Own Data

Replace the sample CSV with your own file and point `main.py` at it:

```bash
python main.py --input path/to/your_data.csv
```

Your CSV should ideally have columns similar to:
`OrderID, Region, Product, SalesRep, Quantity, UnitPrice, OrderDate`

> Don't have those exact columns? Open `data_cleaning.py` and
> `report_generator.py` — every section is commented so you can adapt the
> column names to your own dataset in a few minutes.

## 🧠 How the Cleaning Logic Works (`data_cleaning.py`)

| Issue | How it's handled |
|---|---|
| Duplicate rows | Detected with `.duplicated()` and dropped |
| Inconsistent text (`north`, `NORTH `) | `.str.strip().str.title()` |
| Missing categorical values | Filled with `"Unknown"` |
| Missing/invalid numeric values | Filled with median of valid values |
| Negative or absurd quantities/prices | Replaced with median |
| Missing/invalid dates | Row dropped, count logged |

Every run also produces a **cleaning log** (dict) showing exactly how many
rows were fixed/removed — this log is written straight into the Excel
report's Summary sheet, so you always have an audit trail.

## 📊 Extending This Project

- **Power BI**: Load `output/cleaned_sales_data.csv` directly into Power BI
  for interactive dashboards (Get Data → Text/CSV).
- **Excel only workflow**: Open `output/Sales_Report.xlsx` — it already has
  native Excel charts you can further customize.
- **Scheduling**: Wrap `python main.py` in a cron job (Linux/Mac) or Task
  Scheduler (Windows) to run this automatically on a schedule.

## 📚 Tech Stack

- **pandas** — data manipulation & cleaning
- **numpy** — numeric handling
- **openpyxl** — Excel report + native charts generation
- **matplotlib** — PNG dashboard visual summary

## 📝 License

Free to use and modify for learning, portfolio, or production purposes.
