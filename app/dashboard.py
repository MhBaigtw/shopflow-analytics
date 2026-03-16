import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "shopflow.db"


@st.cache_data
def load_data():
    engine = create_engine(f"sqlite:///{DB_PATH}")

    fact_sales = pd.read_sql("SELECT * FROM fact_sales", engine)
    dim_customers = pd.read_sql("SELECT * FROM dim_customers", engine)
    dim_products = pd.read_sql("SELECT * FROM dim_products", engine)
    dim_date = pd.read_sql("SELECT * FROM dim_date", engine)

    df = fact_sales.merge(dim_customers, on="customer_id", how="left")
    df = df.merge(dim_products, on="product_id", how="left")
    df = df.merge(dim_date, on="date_id", how="left")

    return df


st.set_page_config(page_title="ShopFlow Analytics", layout="wide")
st.title("ShopFlow Analytics Dashboard")

try:
    df = load_data()
    st.write("Database path:", DB_PATH)
    st.write("Rows loaded:", len(df))
    st.dataframe(df.head())
except Exception as e:
    st.error(f"Error loading dashboard data: {e}")
    st.stop()

if df.empty:
    st.warning("The dashboard loaded, but no data was found.")
    st.stop()

st.sidebar.header("Filters")

selected_category = st.sidebar.multiselect(
    "Category",
    options=sorted(df["category"].dropna().unique()),
    default=sorted(df["category"].dropna().unique())
)

selected_payment = st.sidebar.multiselect(
    "Payment Method",
    options=sorted(df["payment_method"].dropna().unique()),
    default=sorted(df["payment_method"].dropna().unique())
)

filtered_df = df[
    (df["category"].isin(selected_category)) &
    (df["payment_method"].isin(selected_payment))
]

total_revenue = filtered_df["revenue"].sum()
total_orders = filtered_df["order_id"].nunique()
total_customers = filtered_df["customer_id"].nunique()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Total Customers", f"{total_customers:,}")
col4.metric("Avg Order Value", f"${avg_order_value:,.2f}")

st.subheader("Revenue by Category")
category_revenue = (
    filtered_df.groupby("category", as_index=False)["revenue"]
    .sum()
    .sort_values("revenue", ascending=False)
)
st.bar_chart(category_revenue.set_index("category"))

st.subheader("Top Products by Revenue")
top_products = (
    filtered_df.groupby("product_name", as_index=False)["revenue"]
    .sum()
    .sort_values("revenue", ascending=False)
    .head(10)
)
st.dataframe(top_products, use_container_width=True)

st.subheader("Top Customers by Spend")
top_customers = (
    filtered_df.groupby("full_name", as_index=False)["revenue"]
    .sum()
    .sort_values("revenue", ascending=False)
    .head(10)
)
st.dataframe(top_customers, use_container_width=True)