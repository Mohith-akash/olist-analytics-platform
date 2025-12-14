-- ============================================
-- SILVER LAYER: Cleaned & Typed Data
-- ============================================

CREATE SCHEMA IF NOT EXISTS olist_silver;

-- Orders with proper timestamps
CREATE OR REPLACE TABLE olist_silver.orders AS
SELECT
    order_id,
    customer_id,
    order_status,
    CAST(order_purchase_timestamp AS TIMESTAMP) AS order_purchase_date,
    CAST(order_approved_at AS TIMESTAMP) AS order_approved_date,
    CAST(order_delivered_carrier_date AS TIMESTAMP) AS delivered_carrier_date,
    CAST(order_delivered_customer_date AS TIMESTAMP) AS delivered_customer_date,
    CAST(order_estimated_delivery_date AS TIMESTAMP) AS estimated_delivery_date
FROM olist_bronze.orders
WHERE order_id IS NOT NULL;

-- Customers
CREATE OR REPLACE TABLE olist_silver.customers AS
SELECT
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix,
    customer_city,
    customer_state
FROM olist_bronze.customers
WHERE customer_id IS NOT NULL;

-- Products with English category names
CREATE OR REPLACE TABLE olist_silver.products AS
SELECT
    p.product_id,
    COALESCE(t.product_category_name_english, p.product_category_name) AS product_category,
    p.product_weight_g,
    p.product_length_cm,
    p.product_height_cm,
    p.product_width_cm
FROM olist_bronze.products p
LEFT JOIN olist_bronze.category_translation t
    ON p.product_category_name = t.product_category_name
WHERE p.product_id IS NOT NULL;

-- Sellers
CREATE OR REPLACE TABLE olist_silver.sellers AS
SELECT seller_id, seller_zip_code_prefix, seller_city, seller_state
FROM olist_bronze.sellers WHERE seller_id IS NOT NULL;

-- Order Items
CREATE OR REPLACE TABLE olist_silver.order_items AS
SELECT
    order_id, order_item_id, product_id, seller_id,
    CAST(price AS DOUBLE) AS price,
    CAST(freight_value AS DOUBLE) AS freight_value
FROM olist_bronze.order_items WHERE order_id IS NOT NULL;

-- Payments
CREATE OR REPLACE TABLE olist_silver.payments AS
SELECT
    order_id, payment_type, payment_installments,
    CAST(payment_value AS DOUBLE) AS payment_value
FROM olist_bronze.order_payments WHERE order_id IS NOT NULL;

-- Reviews
CREATE OR REPLACE TABLE olist_silver.reviews AS
SELECT
    order_id,
    CAST(review_score AS INT) AS review_score
FROM olist_bronze.order_reviews WHERE order_id IS NOT NULL;
