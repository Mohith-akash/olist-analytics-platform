-- ============================================
-- BRONZE LAYER: Raw Data Ingestion
-- ============================================
-- Ingest Olist CSV files into Delta tables (no transformations)
-- Run in Databricks SQL Editor after uploading CSVs to /FileStore/tables/

CREATE SCHEMA IF NOT EXISTS olist_bronze;

-- Customers
CREATE OR REPLACE TABLE olist_bronze.customers AS
SELECT * FROM read_files('/FileStore/tables/olist_customers_dataset.csv',
    format => 'csv', header => 'true', inferSchema => 'true');

-- Orders
CREATE OR REPLACE TABLE olist_bronze.orders AS
SELECT * FROM read_files('/FileStore/tables/olist_orders_dataset.csv',
    format => 'csv', header => 'true', inferSchema => 'true');

-- Order Items
CREATE OR REPLACE TABLE olist_bronze.order_items AS
SELECT * FROM read_files('/FileStore/tables/olist_order_items_dataset.csv',
    format => 'csv', header => 'true', inferSchema => 'true');

-- Order Payments
CREATE OR REPLACE TABLE olist_bronze.order_payments AS
SELECT * FROM read_files('/FileStore/tables/olist_order_payments_dataset.csv',
    format => 'csv', header => 'true', inferSchema => 'true');

-- Order Reviews
CREATE OR REPLACE TABLE olist_bronze.order_reviews AS
SELECT * FROM read_files('/FileStore/tables/olist_order_reviews_dataset.csv',
    format => 'csv', header => 'true', inferSchema => 'true');

-- Products
CREATE OR REPLACE TABLE olist_bronze.products AS
SELECT * FROM read_files('/FileStore/tables/olist_products_dataset.csv',
    format => 'csv', header => 'true', inferSchema => 'true');

-- Sellers
CREATE OR REPLACE TABLE olist_bronze.sellers AS
SELECT * FROM read_files('/FileStore/tables/olist_sellers_dataset.csv',
    format => 'csv', header => 'true', inferSchema => 'true');

-- Geolocation
CREATE OR REPLACE TABLE olist_bronze.geolocation AS
SELECT * FROM read_files('/FileStore/tables/olist_geolocation_dataset.csv',
    format => 'csv', header => 'true', inferSchema => 'true');

-- Category Name Translation (Portuguese → English)
CREATE OR REPLACE TABLE olist_bronze.category_translation AS
SELECT * FROM read_files('/FileStore/tables/product_category_name_translation.csv',
    format => 'csv', header => 'true', inferSchema => 'true');
