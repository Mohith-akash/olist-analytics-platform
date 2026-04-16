-- ============================================
-- GOLD LAYER: Business-Ready Analytics Tables
-- ============================================

CREATE SCHEMA IF NOT EXISTS olist_gold;

-- Fact: Orders (enriched with product + delivery metrics)
CREATE OR REPLACE TABLE olist_gold.fct_orders AS
WITH order_details AS (
    SELECT
        oi.order_id,
        o.customer_id,
        oi.product_id,
        oi.seller_id,
        o.order_purchase_date AS order_purchase_timestamp,
        p.product_category AS product_category_name,
        oi.price,
        oi.freight_value,
        (oi.price + oi.freight_value) AS total_order_value,
        DATEDIFF(o.delivered_customer_date, o.order_purchase_date) AS delivery_days,
        DATEDIFF(o.estimated_delivery_date, o.delivered_customer_date) AS delivery_delta_days
    FROM olist_silver.order_items oi
    LEFT JOIN olist_silver.orders o ON oi.order_id = o.order_id
    LEFT JOIN olist_silver.products p ON oi.product_id = p.product_id
)
SELECT
    *,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id ORDER BY order_purchase_timestamp
    ) AS customer_order_seq
FROM order_details;

-- Dimension: Customers (with lifetime metrics)
CREATE OR REPLACE TABLE olist_gold.dim_customers AS
WITH customer_metrics AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(price) AS lifetime_value,
        MIN(order_purchase_timestamp) AS first_purchase,
        MAX(order_purchase_timestamp) AS last_purchase,
        DATEDIFF(
            MAX(order_purchase_timestamp),
            MIN(order_purchase_timestamp)
        ) AS customer_lifespan_days,
        AVG(delivery_days) AS avg_delivery_days
    FROM olist_gold.fct_orders
    GROUP BY customer_id
)
SELECT
    c.customer_id,
    c.customer_unique_id,
    c.customer_zip_code_prefix AS zip_code,
    c.customer_city AS city,
    c.customer_state AS state,
    COALESCE(m.total_orders, 0) AS total_orders,
    COALESCE(m.lifetime_value, 0) AS lifetime_value,
    m.first_purchase,
    m.last_purchase,
    COALESCE(m.customer_lifespan_days, 0) AS customer_lifespan_days,
    ROUND(m.avg_delivery_days, 1) AS avg_delivery_days,
    CASE
        WHEN m.total_orders > 1 THEN 'Returning'
        WHEN m.total_orders = 1 THEN 'One-time'
        ELSE 'No Orders'
    END AS customer_type
FROM olist_silver.customers c
LEFT JOIN customer_metrics m ON c.customer_id = m.customer_id;

-- Dimension: Products (with revenue ranking)
CREATE OR REPLACE TABLE olist_gold.dim_products AS
WITH product_stats AS (
    SELECT
        product_id,
        COUNT(*) AS times_sold,
        SUM(price) AS total_revenue
    FROM olist_silver.order_items
    GROUP BY product_id
)
SELECT
    p.product_id,
    p.product_category AS product_category_name,
    COALESCE(ps.times_sold, 0) AS times_sold,
    COALESCE(ps.total_revenue, 0) AS total_revenue,
    RANK() OVER (
        PARTITION BY p.product_category ORDER BY COALESCE(ps.total_revenue, 0) DESC
    ) AS category_revenue_rank,
    CASE
        WHEN ps.times_sold >= 50 THEN 'High Seller'
        WHEN ps.times_sold >= 10 THEN 'Medium Seller'
        WHEN ps.times_sold >= 1 THEN 'Low Seller'
        ELSE 'Never Sold'
    END AS sales_tier
FROM olist_silver.products p
LEFT JOIN product_stats ps ON p.product_id = ps.product_id;

-- Dimension: Sellers (with performance tiers)
CREATE OR REPLACE TABLE olist_gold.dim_sellers AS
WITH seller_metrics AS (
    SELECT
        oi.seller_id,
        COUNT(DISTINCT oi.order_id) AS total_orders,
        SUM(oi.price) AS total_revenue,
        AVG(r.review_score) AS avg_review_score
    FROM olist_silver.order_items oi
    LEFT JOIN olist_silver.reviews r ON oi.order_id = r.order_id
    GROUP BY oi.seller_id
)
SELECT
    s.seller_id,
    s.seller_city AS city,
    s.seller_state AS state,
    COALESCE(m.total_orders, 0) AS total_orders,
    COALESCE(m.total_revenue, 0) AS total_revenue,
    m.avg_review_score,
    RANK() OVER (ORDER BY COALESCE(m.total_revenue, 0) DESC) AS revenue_rank,
    CASE
        WHEN m.avg_review_score >= 4.5 THEN 'Platinum'
        WHEN m.avg_review_score >= 4.0 THEN 'Gold'
        WHEN m.avg_review_score >= 3.0 THEN 'Silver'
        ELSE 'Bronze'
    END AS seller_tier
FROM olist_silver.sellers s
LEFT JOIN seller_metrics m ON s.seller_id = m.seller_id;
