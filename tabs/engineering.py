"""
Data Engineering tab component
"""

import streamlit as st


def render():
    """Render the Data Engineering tab with architecture and SQL examples."""
    st.markdown(
        """
    <div class="hero-header" style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);">
        <h1>🔧 Data Engineering</h1>
        <p>SQL transformations, Delta Lake, and dimensional modeling</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    eng_tab1, eng_tab2, eng_tab3 = st.tabs(
        ["📐 Architecture", "📝 fct_orders.sql", "📝 dim_customers.sql"]
    )

    with eng_tab1:
        st.markdown(
            '<div class="section-title">📐 Data Model Architecture</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <div class="chart-card">
        <p>This project uses <strong>Kimball dimensional modeling</strong> with a 3-layer Lakehouse architecture:</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                """
            <div class="skill-card">
                <h4>📥 Sources</h4>
                <p style="color: #888;">Raw CSV data from Olist</p>
                <div class="skill-tags">
                    <span class="skill-tag">9 tables</span>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                """
            <div class="skill-card">
                <h4>🔄 Silver</h4>
                <p style="color: #888;">Cleaned & typed data</p>
                <div class="skill-tags">
                    <span class="skill-tag">orders</span>
                    <span class="skill-tag">customers</span>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        with col3:
            st.markdown(
                """
            <div class="skill-card">
                <h4>📊 Gold</h4>
                <p style="color: #888;">Business-ready analytics</p>
                <div class="skill-tags">
                    <span class="skill-tag">fct_orders</span>
                    <span class="skill-tag">dim_customers</span>
                </div>
            </div>
            """,
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
            <span class="skill-tag">COALESCE</span>
            <span class="skill-tag">Delta Lake</span>
            <span class="skill-tag">Medallion Architecture</span>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with eng_tab2:
        st.markdown(
            '<div class="section-title">📝 fct_orders.sql - Fact Table</div>',
            unsafe_allow_html=True,
        )
        st.markdown("*Multi-table JOIN with calculated `total_order_value`*")

        st.code(
            """-- fct_orders.sql (Gold Layer - Databricks SQL)
CREATE OR REPLACE TABLE olist_gold.fct_orders AS
SELECT
    oi.order_id,
    o.customer_id,
    oi.product_id,
    o.order_purchase_date AS order_purchase_timestamp,
    p.product_category AS product_category_name,
    oi.price,
    oi.freight_value,
    (oi.price + oi.freight_value) AS total_order_value
FROM olist_silver.order_items oi
LEFT JOIN olist_silver.orders o ON oi.order_id = o.order_id
LEFT JOIN olist_silver.products p ON oi.product_id = p.product_id;""",
            language="sql",
        )

    with eng_tab3:
        st.markdown(
            '<div class="section-title">📝 dim_customers.sql - Customer Dimension</div>',
            unsafe_allow_html=True,
        )
        st.markdown("*LTV calculation, aggregations, and CASE-based segmentation*")

        st.code(
            """-- dim_customers.sql (Gold Layer - Databricks SQL)
CREATE OR REPLACE TABLE olist_gold.dim_customers AS
SELECT
    c.customer_id,
    c.customer_unique_id,
    c.customer_zip_code_prefix AS zip_code,
    c.customer_city AS city,
    c.customer_state AS state,
    COALESCE(agg.total_orders, 0) AS total_orders,
    COALESCE(agg.lifetime_value, 0) AS lifetime_value,
    CASE
        WHEN agg.total_orders > 1 THEN 'Returning'
        WHEN agg.total_orders = 1 THEN 'One-time'
        ELSE 'No Orders'
    END AS customer_type
FROM olist_silver.customers c
LEFT JOIN (
    SELECT customer_id,
           COUNT(DISTINCT order_id) AS total_orders,
           SUM(price) AS lifetime_value
    FROM olist_gold.fct_orders
    GROUP BY customer_id
) agg ON c.customer_id = agg.customer_id;""",
            language="sql",
        )
