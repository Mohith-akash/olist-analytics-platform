import duckdb
import os

# Connect to MotherDuck
print("🔌 Connecting to MotherDuck...")
con = duckdb.connect('md:') 

# Create DB if missing
print("🔨 Creating database 'olist_analytics'...")
con.sql("CREATE DATABASE IF NOT EXISTS olist_analytics;")
con.sql("USE olist_analytics;")

# Map raw CSVs to clean table names
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

# Create Schema
print("📂 Creating schema 'raw_olist'...")
con.sql("CREATE SCHEMA IF NOT EXISTS raw_olist;")

# Load Data
data_folder = "data" 
print("🚀 Starting Ingestion...")

for csv_file, table_name in files_to_tables.items():
    file_path = os.path.join(data_folder, csv_file)
    
    if os.path.exists(file_path):
        print(f"   ...Loading {table_name}")
        
        # Using DuckDB's read_csv_auto for automatic type inference
        query = f"""
        CREATE OR REPLACE TABLE raw_olist.{table_name} AS 
        SELECT * FROM read_csv_auto('{file_path}', normalize_names=True);
        """
        con.sql(query)
        print(f"   ✅ {table_name} Loaded.")
    else:
        print(f"   ⚠️ FILE MISSING: {csv_file}")

# Verify
count = con.sql("SELECT count(*) FROM raw_olist.orders").fetchall()[0][0]
print(f"\n🎉 Success! Loaded {count} orders into MotherDuck.")