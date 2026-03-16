from src.extract import extract_all
from src.transform import (
    clean_customers,
    clean_products,
    clean_orders,
    save_processed_data,
)
from src.load import load_all


def run_pipeline():
    print("Starting ETL pipeline...")

    customers_df, products_df, orders_df = extract_all()

    dim_customers = clean_customers(customers_df)
    dim_products = clean_products(products_df)
    fact_sales, dim_date = clean_orders(orders_df, dim_products)

    save_processed_data(
        dim_customers=dim_customers,
        dim_products=dim_products,
        dim_date=dim_date,
        fact_sales=fact_sales
    )

    load_all(
        dim_customers=dim_customers,
        dim_products=dim_products,
        dim_date=dim_date,
        fact_sales=fact_sales
    )

    print("ETL pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()