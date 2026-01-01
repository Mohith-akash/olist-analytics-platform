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
                <h4>🔄 Staging</h4>
                <p style="color: #888;">Cleaned & typed data</p>
                <div class="skill-tags">
                    <span class="skill-tag">stg_orders</span>
                    <span class="skill-tag">stg_customers</span>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        with col3:
            st.markdown(
                """
            <div class="skill-card">
                <h4>📊 Marts</h4>
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
            <span class="skill-tag">Materializations</span>
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
            """-- fct_orders.sql (Databricks SQL)
with orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

products as (
    select * from {{ ref('stg_products') }}
),

final as (
    select
        order_items.order_id,
        orders.customer_id,
        order_items.product_id,
        orders.order_purchase_timestamp,
        products.product_category_name,
        order_items.price,
        order_items.freight_value,
        (order_items.price + order_items.freight_value) as total_order_value
    from order_items
    left join orders on order_items.order_id = orders.order_id
    left join products on order_items.product_id = products.product_id
)

select * from final""",
            language="sql",
        )

    with eng_tab3:
        st.markdown(
            '<div class="section-title">📝 dim_customers.sql - Customer Dimension</div>',
            unsafe_allow_html=True,
        )
        st.markdown("*LTV calculation, aggregations, and CASE-based segmentation*")

        st.code(
            """-- dim_customers.sql (Databricks SQL)
{{ config(materialized='table') }}

with customers as (
    select * from {{ ref('stg_customers') }}
),

customer_orders as (
    select
        o.customer_id,
        count(distinct o.order_id) as total_orders,
        sum(oi.price) as total_revenue
    from {{ ref('stg_orders') }} o
    left join {{ ref('stg_order_items') }} oi on o.order_id = oi.order_id
    group by o.customer_id
),

final as (
    select
        c.customer_id,
        c.city,
        c.state,
        coalesce(co.total_orders, 0) as total_orders,
        coalesce(co.total_revenue, 0) as lifetime_value,
        case
            when co.total_orders > 1 then 'Returning'
            when co.total_orders = 1 then 'One-time'
            else 'No Orders'
        end as customer_type
    from customers c
    left join customer_orders co on c.customer_id = co.customer_id
)

select * from final""",
            language="sql",
        )
