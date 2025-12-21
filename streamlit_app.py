"""
🛒 Olist Analytics - Home
Overview with KPIs and key metrics
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
    initial_sidebar_state="expanded"
)

# Theme CSS
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
    .block-container { padding: 1.5rem 2rem; max-width: 100%; }
    
    .header-box {
        background: linear-gradient(135deg, var(--purple), var(--pink));
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
    }
    .header-box h1 { font-size: 1.75rem; font-weight: 700; color: white; margin: 0; }
    .header-box p { color: rgba(255,255,255,0.9); margin: 0.25rem 0 0 0; font-size: 0.95rem; }
    
    .kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 2rem; }
    .kpi-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
    }
    .kpi-card:hover { border-color: var(--purple); transform: translateY(-2px); transition: all 0.2s; }
    .kpi-icon { font-size: 1.5rem; margin-bottom: 0.5rem; }
    .kpi-label { font-size: 0.7rem; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.5px; }
    .kpi-value { font-size: 1.5rem; font-weight: 700; color: var(--text); margin: 0.25rem 0; }
    .kpi-desc { font-size: 0.7rem; color: var(--green); }
    
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text);
        margin: 2rem 0 1rem 0;
        padding-left: 0.75rem;
        border-left: 4px solid var(--purple);
    }
    
    .chart-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    .chart-header { font-size: 1rem; font-weight: 600; color: var(--text); margin-bottom: 0.25rem; }
    .chart-desc { font-size: 0.8rem; color: var(--text-dim); margin-bottom: 1rem; }
    
    .nav-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.2s;
    }
    .nav-card:hover { border-color: var(--purple); transform: translateY(-2px); }
    .nav-icon { font-size: 2rem; margin-bottom: 0.5rem; }
    .nav-title { font-size: 1rem; font-weight: 600; color: var(--text); }
    .nav-desc { font-size: 0.8rem; color: var(--text-dim); margin-top: 0.25rem; }
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


# Header
st.markdown("""
<div class="header-box">
    <h1>🛒 Olist E-commerce Analytics</h1>
    <p>Brazilian marketplace data • 100K+ orders • 2016-2018 • Powered by dbt + MotherDuck</p>
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
        <div class="kpi-desc">Sum of all order values</div>
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
        <div class="kpi-desc">Unique customers</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">🛍️</div>
        <div class="kpi-label">Avg Order Value</div>
        <div class="kpi-value">{fmt_curr(avg_order)}</div>
        <div class="kpi-desc">Revenue ÷ Orders</div>
    </div>
</div>
""", unsafe_allow_html=True)


# Quick Stats
st.markdown('<div class="section-title">📈 Quick Overview</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-header">Monthly Revenue Trend</div>
        <div class="chart-desc">X: Month | Y: Revenue (R$) | Shows revenue growth over time</div>
    </div>
    """, unsafe_allow_html=True)
    
    monthly = fct_orders.copy()
    monthly['month'] = monthly['order_purchase_timestamp'].dt.to_period('M').astype(str)
    m_agg = monthly.groupby('month')['total_order_value'].sum().reset_index()
    
    fig = go.Figure(go.Bar(
        x=m_agg['month'], y=m_agg['total_order_value'],
        marker_color='#a855f7',
        hovertemplate='%{x}<br>R$%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        height=300,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title='Month', tickfont=dict(color='#9898a0'), title_font=dict(color='#9898a0')),
        yaxis=dict(title='Revenue (R$)', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#9898a0'), title_font=dict(color='#9898a0')),
        margin=dict(t=20, b=60)
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col2:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-header">Top 5 Categories</div>
        <div class="chart-desc">X: Revenue (R$) | Y: Category | Top performing categories</div>
    </div>
    """, unsafe_allow_html=True)
    
    cat_data = fct_orders.groupby('product_category_name')['total_order_value'].sum().nlargest(5).reset_index()
    cat_data = cat_data.sort_values('total_order_value')
    
    fig = go.Figure(go.Bar(
        x=cat_data['total_order_value'], y=cat_data['product_category_name'],
        orientation='h',
        marker=dict(color=['#6366f1', '#8b5cf6', '#a855f7', '#c084fc', '#ec4899']),
        hovertemplate='%{y}<br>R$%{x:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        height=300,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title='Revenue (R$)', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#9898a0'), title_font=dict(color='#9898a0')),
        yaxis=dict(tickfont=dict(color='#fff', size=10)),
        margin=dict(l=10, r=20, t=20, b=60)
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# Navigation Cards
st.markdown('<div class="section-title">🧭 Explore More</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="nav-card">
        <div class="nav-icon">📊</div>
        <div class="nav-title">Analytics</div>
        <div class="nav-desc">Detailed charts with filters</div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_Analytics.py", label="Go to Analytics →", use_container_width=True)

with col2:
    st.markdown("""
    <div class="nav-card">
        <div class="nav-icon">🔍</div>
        <div class="nav-title">Query Data</div>
        <div class="nav-desc">Search & download data</div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_Query_Data.py", label="Go to Query Data →", use_container_width=True)

with col3:
    st.markdown("""
    <div class="nav-card">
        <div class="nav-icon">🔧</div>
        <div class="nav-title">Data Engineering</div>
        <div class="nav-desc">SQL & dbt showcase</div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/3_Data_Engineering.py", label="Go to Data Engineering →", use_container_width=True)


# Quick Stats at bottom
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Products", f"{len(dim_products):,}")
col2.metric("Sellers", f"{len(dim_sellers):,}")
col3.metric("Avg Rating", f"{dim_sellers['avg_review_score'].mean():.2f} ⭐")
col4.metric("States", f"{dim_customers['state'].nunique()}")
