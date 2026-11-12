import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Sales & Profit Analytics", page_icon="📊", layout="wide")

REQUIRED = {"Date", "Product", "Category", "Quantity", "Unit Price", "Unit Cost"}

@st.cache_data
def load_sample():
    return pd.read_csv(Path(__file__).parent / "data" / "sample_sales.csv", parse_dates=["Date"])

def prepare_data(df):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    for col in ["Quantity", "Unit Price", "Unit Cost"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=list(REQUIRED))
    df = df[(df["Quantity"] >= 0) & (df["Unit Price"] >= 0) & (df["Unit Cost"] >= 0)]
    df["Revenue"] = df["Quantity"] * df["Unit Price"]
    df["Cost"] = df["Quantity"] * df["Unit Cost"]
    df["Profit"] = df["Revenue"] - df["Cost"]
    return df

st.title("📊 Sales & Profit Analytics Dashboard")
st.caption("Explore revenue, costs, profit, product performance and sales trends.")

with st.sidebar:
    st.header("Data")
    uploaded = st.file_uploader("Upload your sales CSV or Excel file", type=["csv", "xlsx", "xls"])
    if uploaded:
        try:
            raw = pd.read_csv(uploaded) if uploaded.name.lower().endswith(".csv") else pd.read_excel(uploaded)
        except Exception as exc:
            st.error(f"Could not read the file: {exc}")
            st.stop()
    else:
        raw = load_sample()
        st.info("Showing the included sample dataset.")
    missing = REQUIRED - set(raw.columns)
    if missing:
        st.error("Missing required columns: " + ", ".join(sorted(missing)))
        st.markdown("Required columns: Date, Product, Category, Quantity, Unit Price, Unit Cost.")
        st.stop()
    data = prepare_data(raw)
    if data.empty:
        st.warning("No valid rows found. Check your uploaded data.")
        st.stop()
    min_date, max_date = data["Date"].min().date(), data["Date"].max().date()
    date_range = st.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    categories = sorted(data["Category"].dropna().unique())
    chosen_categories = st.multiselect("Categories", categories, default=categories)

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start, end = date_range
else:
    start, end = min_date, max_date

filtered = data[
    data["Date"].dt.date.between(start, end) &
    data["Category"].isin(chosen_categories)
].copy()

if filtered.empty:
    st.warning("No sales match the selected filters.")
    st.stop()

revenue = filtered["Revenue"].sum()
cost = filtered["Cost"].sum()
profit = filtered["Profit"].sum()
margin = (profit / revenue * 100) if revenue else 0

a, b, c, d = st.columns(4)
a.metric("Total Revenue", f"₹{revenue:,.2f}")
b.metric("Total Cost", f"₹{cost:,.2f}")
c.metric("Total Profit", f"₹{profit:,.2f}")
d.metric("Profit Margin", f"{margin:.1f}%")

st.divider()
left, right = st.columns(2)
daily = filtered.groupby(filtered["Date"].dt.date, as_index=False).agg(
    Revenue=("Revenue", "sum"), Profit=("Profit", "sum")
)
daily = daily.rename(columns={"Date": "Day"})
with left:
    st.subheader("Revenue and profit over time")
    long_daily = daily.melt(id_vars="Day", value_vars=["Revenue", "Profit"], var_name="Metric", value_name="Amount")
    st.plotly_chart(px.line(long_daily, x="Day", y="Amount", color="Metric", markers=True), use_container_width=True)
with right:
    st.subheader("Revenue by category")
    category_sales = filtered.groupby("Category", as_index=False)["Revenue"].sum()
    st.plotly_chart(px.pie(category_sales, names="Category", values="Revenue", hole=0.45), use_container_width=True)

left, right = st.columns(2)
product_summary = filtered.groupby("Product", as_index=False).agg(
    Quantity_Sold=("Quantity", "sum"), Revenue=("Revenue", "sum"), Profit=("Profit", "sum")
).sort_values("Revenue", ascending=False)
with left:
    st.subheader("Top products by revenue")
    st.plotly_chart(px.bar(product_summary.head(10), x="Revenue", y="Product", orientation="h"), use_container_width=True)
with right:
    st.subheader("Most profitable products")
    best_profit = product_summary.sort_values("Profit", ascending=False).head(10)
    st.plotly_chart(px.bar(best_profit, x="Product", y="Profit"), use_container_width=True)

st.subheader("Product performance")
st.dataframe(product_summary.sort_values("Revenue", ascending=False), use_container_width=True, hide_index=True)

st.subheader("Filtered sales records")
display_cols = ["Date", "Product", "Category", "Quantity", "Unit Price", "Unit Cost", "Revenue", "Cost", "Profit"]
st.dataframe(filtered[display_cols].sort_values("Date", ascending=False), use_container_width=True, hide_index=True)

csv = filtered[display_cols].to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download filtered report (CSV)", csv, "sales_profit_report.csv", "text/csv")
st.caption("Tip: Use the sample CSV as a template. Keep the column names exactly as shown in the sidebar.")
