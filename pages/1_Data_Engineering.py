"""
🔧 Data Engineering - SQL & dbt Skills
FIRST PAGE: Recruiters see this first to understand technical skills
"""

import streamlit as st

st.set_page_config(page_title="Data Engineering | Olist", page_icon="🔧", layout="wide")

# Shared CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    :root { --bg: #0f0f12; --card: #1a1a1f; --border: #2a2a30; --text: #ffffff; --text-dim: #9898a0; --purple: #a855f7; --pink: #ec4899; }
    * { font-family: 'Inter', sans-serif; }
    .stApp { background: var(--bg); }
    #MainMenu, footer, header { visibility: hidden; }
    section[data-testid="stSidebar"] { background: linear-gradient(180deg, #1a1a24 0%, #0f0f14 100%); }
    .sidebar-brand { text-align: center; padding: 1rem; border-bottom: 1px solid var(--border); margin-bottom: 1rem; }
    .sidebar-brand h2 { color: var(--text); font-size: 1.25rem; margin: 0; }
    .sidebar-brand p { color: var(--text-dim); font-size: 0.75rem; margin: 0.25rem 0 0 0; }
    .section-title { font-size: 1rem; font-weight: 600; color: var(--text); margin: 1.5rem 0 1rem 0; padding-left: 0.75rem; border-left: 4px solid var(--purple); }
    .info-box { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem; }
    .skill-tags { display: flex; gap: 0.5rem; flex-wrap: wrap; margin: 0.5rem 0; }
    .skill-tag { background: rgba(168, 85, 247, 0.15); border: 1px solid var(--purple); padding: 0.3rem 0.6rem; border-radius: 999px; font-size: 0.7rem; color: var(--purple); }
</style>
""", unsafe_allow_html=True)


# Sidebar Navigation
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <h2>🛒 Olist Analytics</h2>
        <p>Data Engineering Portfolio</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🧭 Navigation")
    st.page_link("streamlit_app.py", label="🏠 Home", use_container_width=True)
    st.page_link("pages/1_Data_Engineering.py", label="🔧 Data Engineering", use_container_width=True)
    st.page_link("pages/2_Analytics.py", label="📊 Analytics", use_container_width=True)
    st.page_link("pages/3_Query_Data.py", label="🔍 Query Data", use_container_width=True)


st.title("🔧 Data Engineering")
st.markdown("SQL transformations, dbt models, and data architecture")

tab1, tab2, tab3, tab4 = st.tabs(["📐 Architecture", "📝 fct_orders.sql", "📝 dim_customers.sql", "🔗 Lineage"])


with tab1:
    st.markdown('<div class="section-title">📐 Data Model Architecture</div>', unsafe_allow_html=True)
    
    st.markdown("""
    This project uses **Kimball dimensional modeling** with a 3-layer dbt architecture:
    
    | Layer | Description | Models |
    |-------|-------------|--------|
    | **Sources** | Raw CSV data from Olist | 9 source tables |
    | **Staging** | Cleaned & typed data | `stg_orders`, `stg_customers`, `stg_products`, etc. |
    | **Marts** | Business-ready analytics | `fct_orders`, `dim_customers`, `dim_products`, `dim_sellers` |
    """)
    
    st.markdown("### Key Design Decisions")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Fact Table (`fct_orders`)**
        - Grain: One row per order line item
        - Joins: orders + order_items + products
        - Calculated: `total_order_value = price + freight`
        """)
    with col2:
        st.markdown("""
        **Dimension Tables**
        - `dim_customers`: LTV, segmentation
        - `dim_sellers`: Tier classification
        - `dim_products`: Sales metrics
        """)
    
    st.markdown("### dbt Skills Demonstrated")
    st.markdown("""
    <div class="skill-tags">
        <span class="skill-tag">CTEs</span>
        <span class="skill-tag">JOINs</span>
        <span class="skill-tag">Aggregations</span>
        <span class="skill-tag">CASE statements</span>
        <span class="skill-tag">Window functions</span>
        <span class="skill-tag">Materializations</span>
        <span class="skill-tag">ref() function</span>
        <span class="skill-tag">Data tests</span>
    </div>
    """, unsafe_allow_html=True)


with tab2:
    st.markdown('<div class="section-title">📝 fct_orders.sql - Fact Table</div>', unsafe_allow_html=True)
    st.markdown("*Multi-table JOIN with calculated `total_order_value`*")
    
    st.code('''-- fct_orders.sql (dbt model)
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


with tab3:
    st.markdown('<div class="section-title">📝 dim_customers.sql - Customer Dimension</div>', unsafe_allow_html=True)
    st.markdown("*LTV calculation, aggregations, and CASE-based segmentation*")
    
    st.code('''-- dim_customers.sql (dbt model)
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

-- Aggregate metrics per customer
customer_orders as (
    select
        o.customer_id,
        count(distinct o.order_id) as total_orders,
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


with tab4:
    st.markdown('<div class="section-title">🔗 Data Lineage</div>', unsafe_allow_html=True)
    
    st.code('''
┌────────────────────────────────────────────────────────────────────┐
│                        DATA LINEAGE                                │
└────────────────────────────────────────────────────────────────────┘

CSV FILES              STAGING              MARTS              DASHBOARD
─────────              ───────              ─────              ─────────

olist_orders     ──►  stg_orders     ──┐
                                      ├──►  fct_orders  ────►  📊 Charts
olist_order_items ──► stg_order_items ──┤                      📈 KPIs
                                      │
olist_products   ──►  stg_products   ──┘

olist_customers  ──►  stg_customers  ────►  dim_customers ──►  👥 Segments

olist_sellers    ──►  stg_sellers    ──┬
olist_reviews    ──►  stg_reviews    ──┴─►  dim_sellers  ───►  🏪 Tiers
''')
    
    st.markdown("""
    ### dbt Tests Applied
    | Model | Tests |
    |-------|-------|
    | `fct_orders` | `not_null` on order_id, customer_id, product_id |
    | `dim_customers` | `unique` + `not_null` on customer_id, `accepted_values` on customer_type |
    | `dim_sellers` | `unique` + `not_null` on seller_id, `accepted_values` on seller_tier |
    """)
    
    st.markdown("📂 **[View full dbt project on GitHub](https://github.com/Mohith-Akash/olist-analytics-platform/tree/main/olist_dbt)**")
