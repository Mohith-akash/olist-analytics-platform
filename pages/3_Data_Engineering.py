"""
🔧 Data Engineering - SQL & dbt Showcase
Demonstrating technical skills
"""

import streamlit as st

st.set_page_config(page_title="Data Engineering | Olist", page_icon="🔧", layout="wide")

# Theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    :root { --bg: #0f0f12; --card: #1a1a1f; --border: #2a2a30; --text: #ffffff; --text-dim: #9898a0; --purple: #a855f7; }
    * { font-family: 'Inter', sans-serif; }
    .stApp { background: var(--bg); }
    #MainMenu, footer, header { visibility: hidden; }
    .section-title { font-size: 1.1rem; font-weight: 600; color: var(--text); margin: 1.5rem 0 1rem 0; padding-left: 0.75rem; border-left: 4px solid var(--purple); }
    .info-box { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)


st.title("🔧 Data Engineering")
st.markdown("Explore the SQL transformations and dbt models powering this dashboard")

tab1, tab2, tab3, tab4 = st.tabs(["📐 Architecture", "📝 fct_orders SQL", "📝 dim_customers SQL", "🔗 Data Lineage"])


with tab1:
    st.markdown('<div class="section-title">📐 Data Model Architecture</div>', unsafe_allow_html=True)
    
    st.markdown("""
    This project uses **Kimball dimensional modeling** with a 3-layer dbt architecture:
    
    | Layer | Description | Models |
    |-------|-------------|--------|
    | **Sources** | Raw CSV data from Olist | 9 source tables |
    | **Staging** | Cleaned & typed data | `stg_orders`, `stg_customers`, `stg_products`, etc. |
    | **Marts** | Business-ready analytics | `fct_orders`, `dim_customers`, `dim_products`, `dim_sellers` |
    
    ### Key Design Decisions
    
    - **Fact Table (`fct_orders`)**: One row per order line item (product in order)
    - **Dimension Tables**: Customer, Product, Seller with calculated business metrics
    - **Materialization**: All mart models materialized as `table` for fast queries
    - **Data Quality**: dbt tests for `not_null`, `unique`, `accepted_values`
    
    ### Tech Stack
    - **Data Warehouse**: MotherDuck (cloud DuckDB)
    - **Transformation**: dbt Core
    - **Visualization**: Streamlit + Plotly
    - **Deployment**: Streamlit Cloud
    """)


with tab2:
    st.markdown('<div class="section-title">📝 fct_orders.sql - Fact Table</div>', unsafe_allow_html=True)
    
    st.markdown("Joins orders, order_items, and products to create the fact table with `total_order_value`:")
    
    st.code('''-- fct_orders.sql
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
        -- Key IDs
        order_items.order_id,
        orders.customer_id,
        order_items.product_id,
        
        -- Timestamp
        orders.order_purchase_timestamp,
        
        -- Product info
        products.product_category_name,
        
        -- Financials (calculated)
        order_items.price,
        order_items.freight_value,
        (order_items.price + order_items.freight_value) as total_order_value

    from order_items
    left join orders on order_items.order_id = orders.order_id
    left join products on order_items.product_id = products.product_id
)

select * from final''', language='sql')
    
    st.markdown("""
    **SQL Skills Demonstrated:**
    - CTEs (Common Table Expressions)
    - LEFT JOINs across multiple tables
    - Calculated columns
    - Clean, readable formatting
    """)


with tab3:
    st.markdown('<div class="section-title">📝 dim_customers.sql - Customer Dimension</div>', unsafe_allow_html=True)
    
    st.markdown("Calculates customer lifetime value, order counts, and segmentation:")
    
    st.code('''-- dim_customers.sql
{{ config(materialized='table') }}

with customers as (
    select * from {{ ref('stg_customers') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

-- Calculate LTV and metrics per customer
customer_orders as (
    select
        o.customer_id,
        count(distinct o.order_id) as total_orders,
        min(o.order_purchase_timestamp) as first_order_date,
        max(o.order_purchase_timestamp) as last_order_date,
        sum(oi.price) as total_revenue,
        avg(oi.price) as avg_order_value
    from orders o
    left join order_items oi on o.order_id = oi.order_id
    group by o.customer_id
),

final as (
    select
        c.customer_id,
        c.customer_unique_id,
        c.city,
        c.state,
        
        -- Calculated metrics
        coalesce(co.total_orders, 0) as total_orders,
        coalesce(co.total_revenue, 0) as lifetime_value,
        
        -- Segmentation logic
        case
            when co.total_orders > 1 then 'Returning'
            when co.total_orders = 1 then 'One-time'
            else 'No Orders'
        end as customer_type

    from customers c
    left join customer_orders co on c.customer_id = co.customer_id
)

select * from final''', language='sql')
    
    st.markdown("""
    **SQL Skills Demonstrated:**
    - dbt materializations (`table`)
    - Aggregate functions (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`)
    - `GROUP BY` for customer-level aggregation
    - `CASE` statements for business logic
    - `COALESCE` for null handling
    """)


with tab4:
    st.markdown('<div class="section-title">🔗 Data Lineage</div>', unsafe_allow_html=True)
    
    st.markdown("How data flows from raw sources to analytics:")
    
    st.code('''
┌──────────────────────────────────────────────────────────────────────┐
│                        DATA LINEAGE                                  │
└──────────────────────────────────────────────────────────────────────┘

RAW CSV FILES          STAGING (dbt)            MARTS (dbt)          DASHBOARD
─────────────          ─────────────            ───────────          ─────────

olist_orders     ──►   stg_orders      ──┐
                                        ├──►  fct_orders   ────►  📊 Charts
olist_order_items ──►  stg_order_items ──┤                        📈 KPIs
                                        │
olist_products   ──►   stg_products    ──┘

olist_customers  ──►   stg_customers   ────►  dim_customers ───►  👥 Segments

olist_sellers    ──►   stg_sellers     ──┬
olist_reviews    ──►   stg_reviews     ──┴─►  dim_sellers   ───►  🏪 Tiers
''')
    
    st.markdown("""
    ### dbt Tests Applied
    
    | Model | Tests |
    |-------|-------|
    | `fct_orders` | `not_null` on order_id, customer_id, product_id |
    | `dim_customers` | `unique` + `not_null` on customer_id, `accepted_values` on customer_type |
    | `dim_sellers` | `unique` + `not_null` on seller_id, `accepted_values` on seller_tier |
    | `dim_products` | `unique` + `not_null` on product_id |
    
    ### Key Transformations
    1. **Staging**: Data type casting, column standardization
    2. **Facts**: Multi-table joins, calculated metrics
    3. **Dimensions**: Aggregations, business logic (CASE), LTV calculation
    """)
    
    st.markdown("---")
    st.markdown("📂 **[View full dbt project on GitHub](https://github.com/Mohith-Akash/olist-analytics-platform/tree/main/olist_dbt)**")
