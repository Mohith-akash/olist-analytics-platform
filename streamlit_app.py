"""
🛒 Olist E-commerce Analytics Dashboard
Single page with horizontal tab navigation
"""

import streamlit as st
import duckdb
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

st.set_page_config(
    page_title="Olist Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS with horizontal tab nav
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    :root {
        --bg: #0f0f12;
        --card: #1a1a1f;
        --border: #2a2a30;
        --text: #ffffff;
        --text-dim: #9898a0;
        --purple: #a855f7;
        --pink: #ec4899;
        --green: #22c55e;
    }
    
    * { font-family: 'Inter', sans-serif; }
    .stApp { background: var(--bg); }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 0.5rem 2rem 2rem 2rem; max-width: 100%; }
    
    /* Hide default sidebar */
    section[data-testid="stSidebar"] { display: none; }
    
    /* Top Nav Bar */
    .top-nav {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 0.5rem;
        margin-bottom: 1.5rem;
        display: flex;
        gap: 0.5rem;
    }
    
    /* Style the Streamlit tabs to look like nav */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--card);
        border-radius: 12px;
        padding: 0.5rem;
        gap: 0.5rem;
        border: 1px solid var(--border);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        color: var(--text-dim);
        font-weight: 500;
        border: none;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(168, 85, 247, 0.1);
        color: var(--purple);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--purple) !important;
        color: white !important;
    }
    
    .stTabs [data-baseweb="tab-border"] { display: none; }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }
    
    /* KPI Cards */
    .kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
    .kpi-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        transition: all 0.2s;
    }
    .kpi-card:hover { border-color: var(--purple); transform: translateY(-2px); }
    .kpi-icon { font-size: 1.5rem; margin-bottom: 0.5rem; }
    .kpi-label { font-size: 0.7rem; color: var(--text-dim); text-transform: uppercase; }
    .kpi-value { font-size: 1.4rem; font-weight: 700; color: var(--text); margin: 0.25rem 0; }
    .kpi-desc { font-size: 0.7rem; color: var(--green); }
    
    /* Section */
    .section-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text);
        margin: 1.5rem 0 1rem 0;
        padding-left: 0.75rem;
        border-left: 4px solid var(--purple);
    }
    
    /* Chart Card */
    .chart-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .chart-header { font-size: 0.9rem; font-weight: 600; color: var(--text); }
    .chart-desc { font-size: 0.75rem; color: var(--text-dim); margin-top: 0.25rem; }
    
    /* Skills */
    .skill-tags { display: flex; gap: 0.5rem; flex-wrap: wrap; margin: 0.5rem 0; }
    .skill-tag {
        background: rgba(168, 85, 247, 0.15);
        border: 1px solid var(--purple);
        padding: 0.3rem 0.6rem;
        border-radius: 999px;
        font-size: 0.7rem;
        color: var(--purple);
    }
    
    /* Footer */
    .footer-box {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin-top: 2rem;
    }
    .github-btn {
        display: inline-block;
        background: var(--purple);
        padding: 0.5rem 1.5rem;
        border-radius: 8px;
        color: white;
        text-decoration: none;
        font-size: 0.85rem;
        font-weight: 500;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_connection():
    token = os.getenv("MOTHERDUCK_TOKEN") or st.secrets.get("MOTHERDUCK_TOKEN", "")
    if token:
        return duckdb.connect(f"md:olist_analytics?motherduck_token={token}")
    return duckdb.connect("md:olist_analytics")


@st.cache_data(ttl=600)
def load_data():
    conn = get_connection()
    fct_orders = conn.execute("SELECT * FROM dbt_main.fct_orders").df()
    dim_customers = conn.execute("SELECT * FROM dbt_main.dim_customers").df()
    dim_products = conn.execute("SELECT * FROM dbt_main.dim_products").df()
    dim_sellers = conn.execute("SELECT * FROM dbt_main.dim_sellers").df()
    return fct_orders, dim_customers, dim_products, dim_sellers


def fmt_curr(v):
    if v >= 1e6: return f"R$ {v/1e6:.2f}M"
    if v >= 1e3: return f"R$ {v/1e3:.1f}K"
    return f"R$ {v:,.2f}"


def fmt_num(v):
    if v >= 1e6: return f"{v/1e6:.1f}M"
    if v >= 1e3: return f"{v/1e3:.1f}K"
    return f"{v:,.0f}"


try:
    fct_orders, dim_customers, dim_products, dim_sellers = load_data()
    fct_orders['order_purchase_timestamp'] = pd.to_datetime(fct_orders['order_purchase_timestamp'])
except Exception as e:
    st.error(f"Connection Error: {e}")
    st.stop()


# ===== HORIZONTAL TAB NAVIGATION =====
tab_home, tab_engineering, tab_analytics, tab_query = st.tabs([
    "🏠 HOME", 
    "🔧 DATA ENGINEERING", 
    "📊 ANALYTICS", 
    "🔍 QUERY DATA"
])


# ============================================
# TAB 1: HOME
# ============================================
with tab_home:
    st.markdown("## 🛒 Olist E-commerce Analytics Platform")
    st.markdown("*End-to-end data pipeline: CSV → MotherDuck → dbt → Dashboard*")
    
    # KPIs
    total_rev = fct_orders['total_order_value'].sum()
    total_ord = fct_orders['order_id'].nunique()
    total_cust = dim_customers['customer_id'].nunique()
    avg_order = total_rev / total_ord if total_ord > 0 else 0
    
    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi-card">
            <div class="kpi-icon">💰</div>
            <div class="kpi-label">Total Revenue</div>
            <div class="kpi-value">{fmt_curr(total_rev)}</div>
            <div class="kpi-desc">Sum of all orders</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">📦</div>
            <div class="kpi-label">Total Orders</div>
            <div class="kpi-value">{fmt_num(total_ord)}</div>
            <div class="kpi-desc">Unique orders</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">👥</div>
            <div class="kpi-label">Customers</div>
            <div class="kpi-value">{fmt_num(total_cust)}</div>
            <div class="kpi-desc">Unique buyers</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">🛍️</div>
            <div class="kpi-label">Avg Order Value</div>
            <div class="kpi-value">{fmt_curr(avg_order)}</div>
            <div class="kpi-desc">Revenue ÷ Orders</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-header">Monthly Revenue</div>
            <div class="chart-desc">X: Month | Y: Revenue (R$)</div>
        </div>
        """, unsafe_allow_html=True)
        
        monthly = fct_orders.copy()
        monthly['month'] = monthly['order_purchase_timestamp'].dt.to_period('M').astype(str)
        m_agg = monthly.groupby('month')['total_order_value'].sum().reset_index()
        
        fig = go.Figure(go.Bar(x=m_agg['month'], y=m_agg['total_order_value'], marker_color='#a855f7'))
        fig.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickfont=dict(color='#9898a0', size=9)),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#9898a0', size=9)),
            margin=dict(t=10, b=40, l=50, r=10))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-header">Top 5 Categories</div>
            <div class="chart-desc">X: Revenue (R$) | Y: Category</div>
        </div>
        """, unsafe_allow_html=True)
        
        cat_data = fct_orders.groupby('product_category_name')['total_order_value'].sum().nlargest(5).reset_index()
        cat_data = cat_data.sort_values('total_order_value')
        
        fig = go.Figure(go.Bar(x=cat_data['total_order_value'], y=cat_data['product_category_name'],
            orientation='h', marker_color=['#6366f1', '#8b5cf6', '#a855f7', '#c084fc', '#ec4899']))
        fig.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#9898a0', size=9)),
            yaxis=dict(tickfont=dict(color='#fff', size=9)),
            margin=dict(t=10, b=40, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Skills
    st.markdown('<div class="section-title">🎯 Skills Demonstrated</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 🔧 Data Engineering")
        st.markdown("- dbt dimensional modeling\n- SQL transformations\n- Data quality testing")
    with col2:
        st.markdown("#### 📊 Analytics")
        st.markdown("- KPI calculations\n- Time-series analysis\n- Customer segmentation")
    with col3:
        st.markdown("#### 💻 Tech Stack")
        st.markdown("- MotherDuck (DuckDB)\n- dbt Core\n- Python / Streamlit")
    
    st.markdown("""
    <div class="footer-box">
        <h3 style="color: white; margin: 0;">Olist E-commerce Analytics Platform</h3>
        <p style="color: #9898a0; margin: 0.5rem 0;">Built to demonstrate data engineering skills</p>
        <a href="https://github.com/Mohith-Akash/olist-analytics-platform" target="_blank" class="github-btn">📂 View Source Code</a>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# TAB 2: DATA ENGINEERING
# ============================================
with tab_engineering:
    st.markdown("## 🔧 Data Engineering")
    st.markdown("*SQL transformations, dbt models, and data architecture*")
    
    eng_tab1, eng_tab2, eng_tab3 = st.tabs(["📐 Architecture", "📝 fct_orders.sql", "📝 dim_customers.sql"])
    
    with eng_tab1:
        st.markdown('<div class="section-title">📐 Data Model Architecture</div>', unsafe_allow_html=True)
        
        st.markdown("""
        This project uses **Kimball dimensional modeling** with a 3-layer dbt architecture:
        
        | Layer | Description | Models |
        |-------|-------------|--------|
        | **Sources** | Raw CSV data | 9 source tables |
        | **Staging** | Cleaned & typed | `stg_orders`, `stg_customers`, etc. |
        | **Marts** | Business-ready | `fct_orders`, `dim_customers`, `dim_sellers` |
        
        ### Key Design Decisions
        - **Fact Table**: One row per order line item
        - **Dimensions**: Customer, Product, Seller with calculated metrics
        - **Tests**: `not_null`, `unique`, `accepted_values`
        """)
        
        st.markdown("### Skills Demonstrated")
        st.markdown("""
        <div class="skill-tags">
            <span class="skill-tag">CTEs</span>
            <span class="skill-tag">JOINs</span>
            <span class="skill-tag">Aggregations</span>
            <span class="skill-tag">CASE statements</span>
            <span class="skill-tag">Window functions</span>
            <span class="skill-tag">dbt ref()</span>
        </div>
        """, unsafe_allow_html=True)
    
    with eng_tab2:
        st.markdown('<div class="section-title">📝 fct_orders.sql</div>', unsafe_allow_html=True)
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

select * from final''', language='sql')
    
    with eng_tab3:
        st.markdown('<div class="section-title">📝 dim_customers.sql</div>', unsafe_allow_html=True)
        st.code('''-- dim_customers.sql (dbt model)
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

select * from final''', language='sql')


# ============================================
# TAB 3: ANALYTICS
# ============================================
with tab_analytics:
    st.markdown("## 📊 Analytics Dashboard")
    st.markdown("*Interactive charts with filters*")
    
    # Filters
    col1, col2 = st.columns([1, 3])
    with col1:
        cats = ['All Categories'] + sorted(fct_orders['product_category_name'].dropna().unique().tolist())
        sel_cat = st.selectbox("Filter by Category", cats)
    
    df = fct_orders.copy()
    if sel_cat != 'All Categories':
        df = df[df['product_category_name'] == sel_cat]
    
    # Charts
    st.markdown('<div class="section-title">📈 Revenue Over Time</div>', unsafe_allow_html=True)
    
    monthly = df.copy()
    monthly['month'] = monthly['order_purchase_timestamp'].dt.to_period('M').astype(str)
    m_agg = monthly.groupby('month').agg({'total_order_value': 'sum', 'order_id': 'nunique'}).reset_index()
    m_agg.columns = ['Month', 'Revenue', 'Orders']
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=m_agg['Month'], y=m_agg['Revenue'], name='Revenue', marker_color='#a855f7'), secondary_y=False)
    fig.add_trace(go.Scatter(x=m_agg['Month'], y=m_agg['Orders'], name='Orders', line=dict(color='#22c55e', width=3)), secondary_y=True)
    
    fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickfont=dict(color='#9898a0')),
        yaxis=dict(title='Revenue (R$)', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#9898a0')),
        yaxis2=dict(title='Orders', tickfont=dict(color='#9898a0')),
        legend=dict(orientation='h', y=1.1, font=dict(color='#fff')),
        margin=dict(t=40, b=60))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Two charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-title">📍 Customers by State</div>', unsafe_allow_html=True)
        state_data = dim_customers.groupby('state').size().nlargest(10).reset_index(name='Count')
        
        fig = go.Figure(go.Bar(x=state_data['state'], y=state_data['Count'],
            marker=dict(color=state_data['Count'], colorscale=[[0, '#a855f7'], [1, '#ec4899']])))
        fig.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickfont=dict(color='#fff')),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#9898a0')),
            margin=dict(t=10, b=40))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        st.markdown('<div class="section-title">⭐ Seller Tiers</div>', unsafe_allow_html=True)
        tier_data = dim_sellers.groupby('seller_tier').size().reset_index(name='Count')
        tier_order = ['Platinum', 'Gold', 'Silver', 'Bronze']
        tier_data['seller_tier'] = pd.Categorical(tier_data['seller_tier'], categories=tier_order, ordered=True)
        tier_data = tier_data.sort_values('seller_tier')
        
        fig = go.Figure(go.Bar(x=tier_data['seller_tier'], y=tier_data['Count'],
            marker_color=['#e5e4e2', '#fbbf24', '#71717a', '#d97706']))
        fig.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickfont=dict(color='#fff')),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#9898a0')),
            margin=dict(t=10, b=40), bargap=0.4)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# ============================================
# TAB 4: QUERY DATA
# ============================================
with tab_query:
    st.markdown("## 🔍 Query Data")
    st.markdown("*Select filters and download as CSV*")
    
    query_tab1, query_tab2, query_tab3 = st.tabs(["📅 Orders", "🏷️ Products", "👥 Customers"])
    
    with query_tab1:
        st.markdown('<div class="section-title">📅 Orders by Month</div>', unsafe_allow_html=True)
        
        fct_orders['month'] = fct_orders['order_purchase_timestamp'].dt.to_period('M').astype(str)
        months = sorted(fct_orders['month'].unique().tolist())
        sel_month = st.selectbox("Select Month", months, index=len(months)-1)
        
        month_data = fct_orders[fct_orders['month'] == sel_month][
            ['order_id', 'customer_id', 'product_category_name', 'price', 'freight_value', 'total_order_value']
        ].copy()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Orders", f"{month_data['order_id'].nunique():,}")
        col2.metric("Revenue", fmt_curr(month_data['total_order_value'].sum()))
        col3.metric("Avg Order", fmt_curr(month_data['total_order_value'].mean()))
        
        st.dataframe(month_data.head(100), use_container_width=True, hide_index=True)
        
        csv = month_data.to_csv(index=False)
        st.download_button(f"📥 Download {len(month_data):,} orders", csv, f"orders_{sel_month}.csv", "text/csv")
    
    with query_tab2:
        st.markdown('<div class="section-title">🏷️ Products by Category</div>', unsafe_allow_html=True)
        
        categories = sorted(dim_products['product_category_name'].dropna().unique().tolist())
        sel_cat_q = st.selectbox("Select Category", categories, key="cat_query")
        
        cat_data = dim_products[dim_products['product_category_name'] == sel_cat_q][
            ['product_id', 'product_category_name', 'times_sold', 'total_revenue', 'sales_tier']
        ].copy()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Products", f"{len(cat_data):,}")
        col2.metric("Revenue", fmt_curr(cat_data['total_revenue'].sum()))
        col3.metric("Units Sold", f"{cat_data['times_sold'].sum():,}")
        
        st.dataframe(cat_data.sort_values('total_revenue', ascending=False), use_container_width=True, hide_index=True)
        
        csv = cat_data.to_csv(index=False)
        st.download_button(f"📥 Download {len(cat_data):,} products", csv, f"products.csv", "text/csv")
    
    with query_tab3:
        st.markdown('<div class="section-title">👥 Customers by State</div>', unsafe_allow_html=True)
        
        states = sorted(dim_customers['state'].dropna().unique().tolist())
        sel_state = st.selectbox("Select State", states)
        
        state_data = dim_customers[dim_customers['state'] == sel_state][
            ['customer_unique_id', 'city', 'state', 'total_orders', 'lifetime_value', 'customer_type']
        ].copy()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Customers", f"{len(state_data):,}")
        col2.metric("Total LTV", fmt_curr(state_data['lifetime_value'].sum()))
        col3.metric("Avg Orders", f"{state_data['total_orders'].mean():.2f}")
        
        st.dataframe(state_data.nlargest(100, 'lifetime_value'), use_container_width=True, hide_index=True)
        
        csv = state_data.to_csv(index=False)
        st.download_button(f"📥 Download {len(state_data):,} customers", csv, f"customers_{sel_state}.csv", "text/csv")
