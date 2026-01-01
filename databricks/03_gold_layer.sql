-- ============================================
-- GOLD LAYER: Business-Ready Analytics Tables
-- ============================================

CREATE SCHEMA IF NOT EXISTS olist_gold;

-- Fact: Orders (at order item level)
CREATE OR REPLACE TABLE olist_gold.fct_orders AS
SELECT
    oi.order_id,
    o.customer_id,
    oi.product_id,
    o.order_purchase_date AS order_purchase_timestamp,
    p.product_category AS product_category_name,
    oi.price,
    oi.freight_value,
    (oi.price + oi.freight_value) AS total_order_value
FROM olist_silver.order_items oi
LEFT JOIN olist_silver.orders o ON oi.order_id = o.order_id
LEFT JOIN olist_silver.products p ON oi.product_id = p.product_id;

-- Dimension: Customers
CREATE OR REPLACE TABLE olist_gold.dim_customers AS
SELECT
    c.customer_id,
    c.customer_unique_id,
    c.customer_zip_code_prefix AS zip_code,
    c.customer_city AS city,
    c.customer_state AS state,
    COALESCE(agg.total_orders, 0) AS total_orders,
    COALESCE(agg.lifetime_value, 0) AS lifetime_value,
    CASE
        WHEN agg.total_orders > 1 THEN 'Returning'
        WHEN agg.total_orders = 1 THEN 'One-time'
        ELSE 'No Orders'
    END AS customer_type
FROM olist_silver.customers c
LEFT JOIN (
    SELECT customer_id, COUNT(DISTINCT order_id) AS total_orders, SUM(price) AS lifetime_value
    FROM olist_gold.fct_orders GROUP BY customer_id
) agg ON c.customer_id = agg.customer_id;

-- Dimension: Products
CREATE OR REPLACE TABLE olist_gold.dim_products AS
SELECT
    p.product_id,
    p.product_category AS product_category_name,
    COALESCE(ps.times_sold, 0) AS times_sold,
    COALESCE(ps.total_revenue, 0) AS total_revenue,
    CASE
        WHEN ps.times_sold >= 50 THEN 'High Seller'
        WHEN ps.times_sold >= 10 THEN 'Medium Seller'
        WHEN ps.times_sold >= 1 THEN 'Low Seller'
        ELSE 'Never Sold'
    END AS sales_tier
FROM olist_silver.products p
LEFT JOIN (
    SELECT product_id, COUNT(*) AS times_sold, SUM(price) AS total_revenue
    FROM olist_silver.order_items GROUP BY product_id
) ps ON p.product_id = ps.product_id;

-- Dimension: Sellers
CREATE OR REPLACE TABLE olist_gold.dim_sellers AS
SELECT
    s.seller_id,
    s.seller_city AS city,
    s.seller_state AS state,
    COALESCE(agg.total_orders, 0) AS total_orders,
    COALESCE(agg.total_revenue, 0) AS total_revenue,
    agg.avg_review_score,
    CASE
        WHEN agg.avg_review_score >= 4.5 THEN 'Platinum'
        WHEN agg.avg_review_score >= 4.0 THEN 'Gold'
        WHEN agg.avg_review_score >= 3.0 THEN 'Silver'
        ELSE 'Bronze'
    END AS seller_tier
FROM olist_silver.sellers s
LEFT JOIN (
    SELECT oi.seller_id, COUNT(DISTINCT oi.order_id) AS total_orders,
           SUM(oi.price) AS total_revenue, AVG(r.review_score) AS avg_review_score
    FROM olist_silver.order_items oi
    LEFT JOIN olist_silver.reviews r ON oi.order_id = r.order_id
    GROUP BY oi.seller_id
) agg ON s.seller_id = agg.seller_id;
