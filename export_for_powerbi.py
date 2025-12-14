"""
Export dbt mart tables to Parquet files for Power BI
"""
import duckdb
import os

# Create exports folder
export_folder = "powerbi_exports"
os.makedirs(export_folder, exist_ok=True)

print("🔌 Connecting to MotherDuck...")
con = duckdb.connect('md:olist_analytics')

# Tables to export
tables = [
    "dbt_main.fct_orders",
    "dbt_main.dim_customers", 
    "dbt_main.dim_products",
    "dbt_main.dim_sellers"
]

print("📦 Exporting tables to Parquet...")

for table in tables:
    table_name = table.split('.')[-1]  # Get just the table name
    output_file = os.path.join(export_folder, f"{table_name}.parquet")
    
    query = f"COPY {table} TO '{output_file}' (FORMAT PARQUET)"
    con.sql(query)
    
    # Get row count
    count = con.sql(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"   ✅ {table_name}.parquet ({count:,} rows)")

print(f"\n🎉 Done! Files exported to: {os.path.abspath(export_folder)}")
print("\nNow open Power BI and import these Parquet files!")
