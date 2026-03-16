# ShopFlow Analytics

ShopFlow Analytics is an end-to-end data engineering project that processes raw e-commerce data and turns it into business-ready analytics through an ETL pipeline and a Streamlit dashboard.

## Tech Stack
- Python
- Pandas
- PostgreSQL
- SQLAlchemy
- Streamlit

## Features
- Extract raw CSV files
- Transform and clean customer, product, and order data
- Build a star schema warehouse
- Load dimensional and fact tables into PostgreSQL
- Visualize KPIs and trends in a dashboard UI

## Project Structure
See the folder layout in the repository.

## How to Run
1. Create the PostgreSQL database:
   - database name: `shopflow`
2. Install dependencies:
   ```bash
   pip install -r requirements.txt