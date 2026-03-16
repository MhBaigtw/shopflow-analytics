-- Total revenue
SELECT SUM(revenue) AS total_revenue
FROM fact_sales;

-- Revenue by product
SELECT p.product_name, SUM(f.revenue) AS revenue
FROM fact_sales f
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY p.product_name
ORDER BY revenue DESC;

-- Revenue by category
SELECT p.category, SUM(f.revenue) AS revenue
FROM fact_sales f
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC;

-- Monthly revenue
SELECT d.year, d.month, d.month_name, SUM(f.revenue) AS revenue
FROM fact_sales f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;

-- Top customers
-- Top customers
SELECT TOP 10 c.full_name, SUM(f.revenue) AS total_spend
FROM fact_sales f
JOIN dim_customers c ON f.customer_id = c.customer_id
GROUP BY c.customer_id, c.full_name
ORDER BY total_spend DESC;