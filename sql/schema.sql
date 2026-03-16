CREATE TABLE dim_customers (
    customer_id INT PRIMARY KEY,
    full_name VARCHAR(150),
    city VARCHAR(100),
    province VARCHAR(20),
    signup_date DATE
);

CREATE TABLE dim_products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(150),
    category VARCHAR(100),
    price NUMERIC(10, 2)
);

CREATE TABLE dim_date (
    date_id INT PRIMARY KEY,
    full_date DATE,
    day INT,
    month INT,
    month_name VARCHAR(20),
    quarter INT,
    year INT
);

CREATE TABLE fact_sales (
    sale_id INT PRIMARY KEY,
    order_id INT,
    customer_id INT,
    product_id INT,
    date_id INT,
    quantity INT,
    unit_price NUMERIC(10, 2),
    revenue NUMERIC(12, 2),
    payment_method VARCHAR(50),
    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES dim_products(product_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);