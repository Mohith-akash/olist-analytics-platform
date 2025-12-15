"""
Database connection and data loading for Olist Analytics
Connects to Databricks SQL Warehouse (Free Edition)
"""

import streamlit as st
from databricks import sql
import os
import pandas as pd


@st.cache_resource
def get_connection():
    """Get cached connection to Databricks SQL Warehouse."""
    return sql.connect(
        server_hostname=os.getenv("DATABRICKS_HOST")
        or st.secrets.get("DATABRICKS_HOST", ""),
        http_path=os.getenv("DATABRICKS_HTTP_PATH")
        or st.secrets.get("DATABRICKS_HTTP_PATH", ""),
        access_token=os.getenv("DATABRICKS_TOKEN")
        or st.secrets.get("DATABRICKS_TOKEN", ""),
    )


def _fetch_table(cursor, table_name: str) -> pd.DataFrame:
    """Helper to fetch a table as DataFrame."""
    cursor.execute(f"SELECT * FROM olist_gold.{table_name}")
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    return pd.DataFrame(rows, columns=columns)


@st.cache_data(ttl=None)  # Infinite cache - Olist data is static/historical
def load_data():
    """Load all dimension and fact tables from Databricks Gold layer."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        fct_orders = _fetch_table(cursor, "fct_orders")
        dim_customers = _fetch_table(cursor, "dim_customers")
        dim_products = _fetch_table(cursor, "dim_products")
        dim_sellers = _fetch_table(cursor, "dim_sellers")
    finally:
        cursor.close()

    return fct_orders, dim_customers, dim_products, dim_sellers
