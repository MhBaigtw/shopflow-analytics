import streamlit as st
import pandas as pd
from sqlalchemy import create_engine


DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "shopflow"


@st.cache_data
def load_data():
    connection_string = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    engine = create_engine(connection_string)

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

df = load_data()

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

st.subheader("Monthly Revenue Trend")
monthly_revenue = (
    filtered_df.groupby(["year", "month_name"], as_index=False)["revenue"]
    .sum()
)
st.dataframe(monthly_revenue, use_container_width=True)

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