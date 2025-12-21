"""
ingest.py - Load Olist CSVs to MotherDuck
Run once to populate the raw_olist schema
"""
import duckdb
import os

print("Connecting to MotherDuck...")
con = duckdb.connect('md:') 

print("Creating database...")
con.sql("CREATE DATABASE IF NOT EXISTS olist_analytics;")
con.sql("USE olist_analytics;")

# CSV to table name mapping
files_to_tables = {
    "olist_customers_dataset.csv": "customers",
    "olist_geolocation_dataset.csv": "geolocation",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_orders_dataset.csv": "orders",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "product_category_name_translation.csv": "category_translation"
}

print("Creating raw_olist schema...")
con.sql("CREATE SCHEMA IF NOT EXISTS raw_olist;")

data_folder = "data"
print("Loading data...")

for csv_file, table_name in files_to_tables.items():
    file_path = os.path.join(data_folder, csv_file)
    
    if os.path.exists(file_path):
        print(f"  {table_name}...")
        con.sql(f"""
            CREATE OR REPLACE TABLE raw_olist.{table_name} AS 
            SELECT * FROM read_csv_auto('{file_path}', normalize_names=True);
        """)
    else:
        print(f"  Missing: {csv_file}")

# Quick check
count = con.sql("SELECT count(*) FROM raw_olist.orders").fetchall()[0][0]
print(f"\nDone! Loaded {count} orders.")