import streamlit as st
import pandas as pd
from sqlalchemy import create_engine


@st.cache_data
def load_data():
    engine = create_engine("sqlite:///shopflow.db")

    fact_sales = pd.read_sql("SELECT * FROM fact_sales", engine)
    dim_customers = pd.read_sql("SELECT * FROM dim_customers", engine)
    dim_products = pd.read_sql("SELECT * FROM dim_products", engine)
    dim_date = pd.read_sql("SELECT * FROM dim_date", engine)

    df = fact_sales.merge(dim_customers, on="customer_id", how="left")
    df = df.merge(dim_products, on="product_id", how="left")
    df = df.merge(dim_date, on="date_id", how="left")

    return df