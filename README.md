# Sales & Profit Analytics Dashboard

A beginner-friendly data analytics project built with **Python, Pandas, Streamlit and Plotly**. Upload a shop sales CSV/Excel file and explore revenue, cost, profit, profit margin, product performance and sales trends.

## Features
- Upload CSV or Excel sales data
- KPI cards for revenue, cost, profit and profit margin
- Date-range and category filters
- Daily revenue/profit trend chart
- Revenue breakdown by category
- Top products by revenue and profit
- Product performance table
- Download filtered results as CSV
- Included sample dataset so the app runs immediately

## Preview
Run the app locally to see the interactive dashboard.

## 1. Requirements
- Python 3.9 or newer
- VS Code (recommended)

## 2. Install and run

Open a terminal inside this project folder and run:

```bash
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt**
```cmd
.venv\Scripts\activate
```

Install packages and start the dashboard:

```bash
pip install -r requirements.txt
streamlit run app.py
```

The dashboard opens in your browser, usually at `http://localhost:8501`.

## 3. Upload your own data

CSV or Excel files must contain these exact columns:

| Column | Meaning | Example |
|---|---|---|
| Date | Sale date | 2026-01-05 |
| Product | Product name | LED Bulb |
| Category | Product category | Electrical |
| Quantity | Units sold | 5 |
| Unit Price | Selling price per unit | 120 |
| Unit Cost | Cost per unit | 80 |

Revenue, cost and profit are calculated automatically:
- Revenue = Quantity × Unit Price
- Cost = Quantity × Unit Cost
- Profit = Revenue − Cost
- Profit Margin = Profit ÷ Revenue × 100

## Project structure

```text
sales-profit-analytics/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── data/
    └── sample_sales.csv
```

## 4. Push to GitHub

1. Create a new empty repository on GitHub named `sales-profit-analytics`.
2. Extract this ZIP file.
3. Open the extracted folder in VS Code.
4. Open the VS Code terminal and run:

```bash
git init
git add .
git commit -m "Add sales and profit analytics dashboard"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/sales-profit-analytics.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username.

## 5. Suggested future improvements
- Add login and user roles
- Add inventory and low-stock alerts
- Add sales forecasting
- Add PDF report export
- Deploy the dashboard online

## Learning outcomes
This project demonstrates data cleaning, feature engineering, aggregation, exploratory data analysis, interactive visualization, file handling and Git/GitHub workflow.
