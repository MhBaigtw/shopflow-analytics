import pandas as pd
from src.db import get_engine


def load_table(df: pd.DataFrame, table_name: str) -> None:
    engine = get_engine()
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"Loaded {table_name} with {len(df)} rows.")


def load_all(
    dim_customers: pd.DataFrame,
    dim_products: pd.DataFrame,
    dim_date: pd.DataFrame,
    fact_sales: pd.DataFrame
) -> None:
    load_table(dim_customers, "dim_customers")
    load_table(dim_products, "dim_products")
    load_table(dim_date, "dim_date")
    load_table(fact_sales, "fact_sales")