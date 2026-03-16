import pandas as pd
from pathlib import Path


PROCESSED_DATA_DIR = Path("data/processed")


def clean_customers(customers_df: pd.DataFrame) -> pd.DataFrame:
    df = customers_df.copy()

    df = df.drop_duplicates(subset=["customer_id"])
    df["first_name"] = df["first_name"].astype(str).str.strip().str.title()
    df["last_name"] = df["last_name"].astype(str).str.strip().str.title()
    df["city"] = df["city"].astype(str).str.strip().str.title()
    df["province"] = df["province"].astype(str).str.strip().str.upper()
    df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")

    df["full_name"] = df["first_name"] + " " + df["last_name"]

    dim_customers = df[[
        "customer_id",
        "full_name",
        "city",
        "province",
        "signup_date"
    ]].copy()

    return dim_customers


def clean_products(products_df: pd.DataFrame) -> pd.DataFrame:
    df = products_df.copy()

    df = df.drop_duplicates(subset=["product_id"])
    df["product_name"] = df["product_name"].astype(str).str.strip()
    df["category"] = df["category"].astype(str).str.strip().str.title()
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    dim_products = df[[
        "product_id",
        "product_name",
        "category",
        "price"
    ]].copy()

    return dim_products


def build_date_dimension(order_dates: pd.Series) -> pd.DataFrame:
    unique_dates = pd.Series(order_dates.dropna().unique())
    unique_dates = pd.to_datetime(unique_dates)

    dim_date = pd.DataFrame({
        "full_date": unique_dates
    }).sort_values("full_date").reset_index(drop=True)

    dim_date["date_id"] = dim_date["full_date"].dt.strftime("%Y%m%d").astype(int)
    dim_date["day"] = dim_date["full_date"].dt.day
    dim_date["month"] = dim_date["full_date"].dt.month
    dim_date["month_name"] = dim_date["full_date"].dt.month_name()
    dim_date["quarter"] = dim_date["full_date"].dt.quarter
    dim_date["year"] = dim_date["full_date"].dt.year

    return dim_date[[
        "date_id",
        "full_date",
        "day",
        "month",
        "month_name",
        "quarter",
        "year"
    ]]


def clean_orders(orders_df: pd.DataFrame, products_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    orders = orders_df.copy()
    products = products_df.copy()

    orders = orders.drop_duplicates(subset=["order_id"])
    orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")
    orders["quantity"] = pd.to_numeric(orders["quantity"], errors="coerce")
    orders["payment_method"] = orders["payment_method"].astype(str).str.strip().str.title()

    products["price"] = pd.to_numeric(products["price"], errors="coerce")

    merged = orders.merge(
        products[["product_id", "price"]],
        on="product_id",
        how="left"
    )

    merged["unit_price"] = merged["price"]
    merged["revenue"] = merged["quantity"] * merged["unit_price"]
    merged["date_id"] = merged["order_date"].dt.strftime("%Y%m%d")

    merged["date_id"] = pd.to_numeric(merged["date_id"], errors="coerce").astype("Int64")

    dim_date = build_date_dimension(merged["order_date"])

    fact_sales = merged[[
        "order_id",
        "customer_id",
        "product_id",
        "date_id",
        "quantity",
        "unit_price",
        "revenue",
        "payment_method"
    ]].copy()

    fact_sales.insert(0, "sale_id", range(1, len(fact_sales) + 1))

    return fact_sales, dim_date


def save_processed_data(
    dim_customers: pd.DataFrame,
    dim_products: pd.DataFrame,
    dim_date: pd.DataFrame,
    fact_sales: pd.DataFrame
) -> None:
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    dim_customers.to_csv(PROCESSED_DATA_DIR / "dim_customers.csv", index=False)
    dim_products.to_csv(PROCESSED_DATA_DIR / "dim_products.csv", index=False)
    dim_date.to_csv(PROCESSED_DATA_DIR / "dim_date.csv", index=False)
    fact_sales.to_csv(PROCESSED_DATA_DIR / "fact_sales.csv", index=False)