import pandas as pd
from pathlib import Path


RAW_DATA_DIR = Path("data/raw")


def extract_customers() -> pd.DataFrame:
    return pd.read_csv(RAW_DATA_DIR / "customers.csv")


def extract_products() -> pd.DataFrame:
    return pd.read_csv(RAW_DATA_DIR / "products.csv")


def extract_orders() -> pd.DataFrame:
    return pd.read_csv(RAW_DATA_DIR / "orders.csv")


def extract_all() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    customers_df = extract_customers()
    products_df = extract_products()
    orders_df = extract_orders()
    return customers_df, products_df, orders_df