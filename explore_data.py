import duckdb
import pandas as pd

# 1. Connect to MotherDuck (your cloud data warehouse)
print("🔌 Connecting to MotherDuck...")
con = duckdb.connect('md:olist_analytics')

# 2. Function to quickly peek at a table
def check_table(table_name):
    print(f"\n🔎 Previewing top 5 rows of: {table_name}")
    # We query the 'dbt_main' schema where dbt built your tables
    con.sql(f"SELECT * FROM dbt_main.{table_name} LIMIT 5").show()

# 3. Check your Marts (The clean, business-ready tables)
check_table("fct_orders")
check_table("dim_customers")
check_table("dim_products")

# 4. Run a Custom Business Query
print("\n📊 Running Custom Query: Top 3 Product Categories by Revenue")
con.sql("""
    SELECT 
        product_category_name, 
        sum(total_revenue) as revenue
    FROM dbt_main.dim_products
    GROUP BY 1
    ORDER BY 2 DESC
    LIMIT 3
""").show()
