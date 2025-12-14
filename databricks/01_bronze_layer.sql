-- ============================================
-- BRONZE LAYER: Raw Data Ingestion
-- ============================================
-- Run in Databricks SQL Editor after uploading CSVs

CREATE SCHEMA IF NOT EXISTS olist_bronze;

-- Create Delta tables from uploaded CSVs
-- Tables: customers, orders, products, sellers, order_items,
--         order_payments, order_reviews, geolocation, category_translation
