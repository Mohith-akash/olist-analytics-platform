"""Refresh snapshot/ from the Databricks Gold tables (the app's fallback when the warehouse is down).

DATABRICKS_HOST=... DATABRICKS_HTTP_PATH=... DATABRICKS_TOKEN=... python scripts/export_snapshot.py
"""

import os
from pathlib import Path

import pandas as pd
from databricks import sql

TABLES = ("fct_orders", "dim_customers", "dim_products", "dim_sellers")
OUT = Path(__file__).resolve().parent.parent / "snapshot"

with (
    sql.connect(
        server_hostname=os.environ["DATABRICKS_HOST"],
        http_path=os.environ["DATABRICKS_HTTP_PATH"],
        access_token=os.environ["DATABRICKS_TOKEN"],
    ) as conn,
    conn.cursor() as cur,
):
    for t in TABLES:
        cur.execute(f"SELECT * FROM olist_gold.{t}")
        df = pd.DataFrame(cur.fetchall(), columns=[d[0] for d in cur.description])
        df.to_parquet(OUT / f"{t}.parquet", index=False, compression="zstd")
        print(f"{t}: {len(df):,} rows")
