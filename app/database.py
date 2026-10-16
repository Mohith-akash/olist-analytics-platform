"""
Database connection and data loading for Olist Analytics
Connects to Databricks SQL Warehouse (Free Edition). When the warehouse
won't start, falls back to a saved copy of the same Gold tables in snapshot/.
"""

import streamlit as st
from databricks import sql
import os
from pathlib import Path
import pandas as pd

TABLES = ("fct_orders", "dim_customers", "dim_products", "dim_sellers")
SNAPSHOT_DIR = Path(__file__).resolve().parent.parent / "snapshot"


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
def _load_live():
    """Load all dimension and fact tables from Databricks Gold layer."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        return tuple(_fetch_table(cursor, t) for t in TABLES)
    finally:
        cursor.close()


@st.cache_data(ttl=3600, show_spinner=False)
def _live_or_none():
    """Free Edition warehouses sometimes refuse to start ("Cannot create the
    resource"). Remember a failure for an hour so every rerun doesn't wait on it."""
    try:
        return _load_live()
    except Exception:
        return None


@st.cache_data(ttl=None)
def load_snapshot():
    """Saved copy of the Gold tables (refresh with scripts/export_snapshot.py)."""
    return tuple(pd.read_parquet(SNAPSHOT_DIR / f"{t}.parquet") for t in TABLES)


def load_data():
    """Gold tables from Databricks, or the saved snapshot if the warehouse is down.

    Returns fct_orders, dim_customers, dim_products, dim_sellers and a flag that
    is True when the tables came from the snapshot.
    """
    live = _live_or_none()
    if live is not None:
        return (*live, False)
    return (*load_snapshot(), True)
