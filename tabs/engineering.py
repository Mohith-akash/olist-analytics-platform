"""
Data Engineering tab component
"""

import streamlit as st

from app.components import render_hero_header, render_section_title


def render():
    """Render the Data Engineering tab with architecture and SQL examples."""
    render_hero_header(
        "🔧 Data Engineering",
        "SQL transformations, Delta Lake, and dimensional modeling",
        "135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%",
    )

    eng_tab1, eng_tab2, eng_tab3 = st.tabs(
        ["📐 Architecture", "📝 fct_orders.sql", "📝 dim_customers.sql"]
    )

    with eng_tab1:
        render_section_title("📐 Data Model Architecture")

        st.markdown(
            """
        <div class="chart-card">
        <p>This project uses <strong>Kimball dimensional modeling</strong> with a 3-layer Lakehouse architecture:</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        arch_tiers = [
            ("📥 Sources", "Raw CSV data from Olist", ["9 tables"]),
            ("🔄 Silver", "Cleaned & typed data", ["orders", "customers"]),
            ("📊 Gold", "Business-ready analytics", ["fct_orders", "dim_customers"]),
        ]
        for col, (title, desc, tags) in zip(st.columns(3), arch_tiers):
            with col:
                tags_html = "".join(f'<span class="skill-tag">{t}</span>' for t in tags)
                st.markdown(
                    f'<div class="skill-card"><h4>{title}</h4>'
                    f'<p style="color: #888;">{desc}</p>'
                    f'<div class="skill-tags">{tags_html}</div></div>',
                    unsafe_allow_html=True,
                )

        st.markdown("### 🛠️ SQL Skills Demonstrated")
        st.markdown(
            """
        <div class="skill-tags">
            <span class="skill-tag">CTEs</span>
            <span class="skill-tag">LEFT JOINs</span>
            <span class="skill-tag">Aggregations</span>
            <span class="skill-tag">CASE statements</span>
            <span class="skill-tag">Window functions</span>
            <span class="skill-tag">DATEDIFF</span>
            <span class="skill-tag">COALESCE</span>
            <span class="skill-tag">Delta Lake</span>
            <span class="skill-tag">Medallion Architecture</span>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with eng_tab2:
        render_section_title("📝 fct_orders.sql - Fact Table")
        st.markdown("*CTE + multi-table JOIN + window function for order sequencing*")

        st.code(
            """-- fct_orders.sql (Gold Layer - Databricks SQL)
CREATE OR REPLACE TABLE olist_gold.fct_orders AS
WITH order_details AS (
    SELECT
        oi.order_id,
        o.customer_id,
        oi.product_id,
        oi.seller_id,
        o.order_purchase_date AS order_purchase_timestamp,
        p.product_category AS product_category_name,
        oi.price,
        oi.freight_value,
        (oi.price + oi.freight_value) AS total_order_value,
        DATEDIFF(o.delivered_customer_date, o.order_purchase_date) AS delivery_days,
        DATEDIFF(o.estimated_delivery_date, o.delivered_customer_date) AS delivery_delta_days
    FROM olist_silver.order_items oi
    LEFT JOIN olist_silver.orders o ON oi.order_id = o.order_id
    LEFT JOIN olist_silver.products p ON oi.product_id = p.product_id
)
SELECT
    *,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id ORDER BY order_purchase_timestamp
    ) AS customer_order_seq
FROM order_details;""",
            language="sql",
        )

    with eng_tab3:
        render_section_title("📝 dim_customers.sql - Customer Dimension")
        st.markdown(
            "*CTE for lifetime metrics, DATEDIFF for lifespan, CASE segmentation*"
        )

        st.code(
            """-- dim_customers.sql (Gold Layer - Databricks SQL)
CREATE OR REPLACE TABLE olist_gold.dim_customers AS
WITH customer_metrics AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(price) AS lifetime_value,
        MIN(order_purchase_timestamp) AS first_purchase,
        MAX(order_purchase_timestamp) AS last_purchase,
        DATEDIFF(
            MAX(order_purchase_timestamp),
            MIN(order_purchase_timestamp)
        ) AS customer_lifespan_days,
        AVG(delivery_days) AS avg_delivery_days
    FROM olist_gold.fct_orders
    GROUP BY customer_id
)
SELECT
    c.customer_id,
    c.customer_unique_id,
    c.customer_zip_code_prefix AS zip_code,
    c.customer_city AS city,
    c.customer_state AS state,
    COALESCE(m.total_orders, 0) AS total_orders,
    COALESCE(m.lifetime_value, 0) AS lifetime_value,
    m.first_purchase,
    m.last_purchase,
    COALESCE(m.customer_lifespan_days, 0) AS customer_lifespan_days,
    ROUND(m.avg_delivery_days, 1) AS avg_delivery_days,
    CASE
        WHEN m.total_orders > 1 THEN 'Returning'
        WHEN m.total_orders = 1 THEN 'One-time'
        ELSE 'No Orders'
    END AS customer_type
FROM olist_silver.customers c
LEFT JOIN customer_metrics m ON c.customer_id = m.customer_id;""",
            language="sql",
        )
