"""The saved Gold snapshot must cover every column the app reads, and match the live dashboard totals."""

from pathlib import Path

import pandas as pd
import pytest

SNAPSHOT = Path(__file__).resolve().parent.parent / "snapshot"
APP_COLUMNS = {
    "fct_orders": {
        "order_id",
        "customer_id",
        "product_id",
        "order_purchase_timestamp",
        "product_category_name",
        "price",
        "total_order_value",
    },
    "dim_customers": {
        "customer_id",
        "customer_unique_id",
        "city",
        "state",
        "total_orders",
        "lifetime_value",
        "customer_type",
    },
    "dim_products": {
        "product_id",
        "product_category_name",
        "times_sold",
        "total_revenue",
        "sales_tier",
    },
    "dim_sellers": {
        "city",
        "state",
        "total_orders",
        "total_revenue",
        "avg_review_score",
        "seller_tier",
    },
}


@pytest.mark.parametrize("table", APP_COLUMNS)
def test_snapshot_has_every_column_the_app_uses(table):
    df = pd.read_parquet(SNAPSHOT / f"{table}.parquet")
    assert len(df) > 0
    assert APP_COLUMNS[table] <= set(df.columns)


def test_snapshot_matches_dashboard_totals():
    orders = pd.read_parquet(SNAPSHOT / "fct_orders.parquet")
    assert orders["order_id"].nunique() == 98_666
    assert round(orders["total_order_value"].sum() / 1e6, 2) == 15.84
    assert len(pd.read_parquet(SNAPSHOT / "dim_sellers.parquet")) == 3_095
