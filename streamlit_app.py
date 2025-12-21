"""
🏠 Olist Analytics - Home
Portfolio piece for Data/Analytics Engineering roles
"""

import streamlit as st
import duckdb
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="Olist Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Shared CSS
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
    .block-container { padding: 1rem 2rem; max-width: 100%; }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a24 0%, #0f0f14 100%);
    }
    section[data-testid="stSidebar"] > div { padding-top: 1rem; }
    
    .sidebar-brand {
        text-align: center;
        padding: 1rem;
        border-bottom: 1px solid var(--border);
        margin-bottom: 1rem;
    }
    .sidebar-brand h2 { color: var(--text); font-size: 1.25rem; margin: 0; }
    .sidebar-brand p { color: var(--text-dim); font-size: 0.75rem; margin: 0.25rem 0 0 0; }
    
    /* Header */
    .header-box {
        background: linear-gradient(135deg, var(--purple), var(--pink));
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
    }
    .header-box h1 { font-size: 1.5rem; font-weight: 700; color: white; margin: 0; }
    .header-box p { color: rgba(255,255,255,0.9); margin: 0.25rem 0 0 0; font-size: 0.9rem; }
    
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
    
    /* Skills Tags */
    .skill-tags { display: flex; gap: 0.5rem; flex-wrap: wrap; margin: 1rem 0; }
    .skill-tag {
        background: rgba(168, 85, 247, 0.15);
        border: 1px solid var(--purple);
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        font-size: 0.75rem;
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
    .footer-box h3 { color: var(--text); font-size: 1rem; margin: 0 0 0.5rem 0; }
    .footer-box p { color: var(--text-dim); font-size: 0.85rem; margin: 0; }
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
    data_loaded = True
except Exception as e:
    data_loaded = False
    st.error(f"Connection Error: {e}")
    st.stop()


# ===== SIDEBAR =====
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
    
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    st.metric("Products", f"{len(dim_products):,}")
    st.metric("Sellers", f"{len(dim_sellers):,}")
    st.metric("Avg Rating", f"{dim_sellers['avg_review_score'].mean():.2f} ⭐")
    
    st.markdown("---")
    st.markdown("### 🛠️ Tech Stack")
    st.markdown("""
    <div class="skill-tags">
        <span class="skill-tag">dbt</span>
        <span class="skill-tag">SQL</span>
        <span class="skill-tag">Python</span>
        <span class="skill-tag">MotherDuck</span>
        <span class="skill-tag">Streamlit</span>
    </div>
    """, unsafe_allow_html=True)


# ===== MAIN CONTENT =====
st.markdown("""
<div class="header-box">
    <h1>🛒 Olist E-commerce Analytics Platform</h1>
    <p>End-to-end data pipeline: Raw CSV → MotherDuck → dbt transformations → Interactive Dashboard</p>
</div>
""", unsafe_allow_html=True)


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
st.markdown('<div class="section-title">📈 Overview</div>', unsafe_allow_html=True)

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
    fig.update_layout(
        height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickfont=dict(color='#9898a0', size=9)),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#9898a0', size=9)),
        margin=dict(t=10, b=40, l=50, r=10)
    )
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
    
    fig = go.Figure(go.Bar(
        x=cat_data['total_order_value'], y=cat_data['product_category_name'],
        orientation='h', marker_color=['#6366f1', '#8b5cf6', '#a855f7', '#c084fc', '#ec4899']
    ))
    fig.update_layout(
        height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#9898a0', size=9)),
        yaxis=dict(tickfont=dict(color='#fff', size=9)),
        margin=dict(t=10, b=40, l=10, r=10)
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# What This Project Demonstrates
st.markdown('<div class="section-title">🎯 Skills Demonstrated</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    #### 🔧 Data Engineering
    - dbt dimensional modeling (Kimball)
    - 3-layer architecture (staging → marts)
    - SQL transformations & CTEs
    - Data quality testing
    """)

with col2:
    st.markdown("""
    #### 📊 Analytics
    - KPI calculations
    - Time-series analysis
    - Customer segmentation
    - Geographic distribution
    """)

with col3:
    st.markdown("""
    #### 💻 Tech Stack
    - MotherDuck (Cloud DuckDB)
    - dbt Core
    - Python / Pandas
    - Streamlit / Plotly
    """)


# Footer
st.markdown("""
<div class="footer-box">
    <h3>Olist E-commerce Analytics Platform</h3>
    <p>Built to demonstrate data engineering skills • Brazilian marketplace dataset</p>
    <a href="https://github.com/Mohith-Akash/olist-analytics-platform" target="_blank" class="github-btn">
        📂 View Source Code
    </a>
</div>
""", unsafe_allow_html=True)
