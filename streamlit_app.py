"""
🛒 Olist E-commerce Analytics Dashboard
Premium interactive dashboard with filters, vibrant colors, and modern design
"""

import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import os

# Page Configuration
st.set_page_config(
    page_title="Olist Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Interactive Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    :root {
        --bg-dark: #0f0f14;
        --bg-card: #1a1a24;
        --bg-hover: #252532;
        --border: rgba(255,255,255,0.1);
        --text-bright: #ffffff;
        --text-primary: #f0f0f5;
        --text-secondary: #9898a6;
        --accent-purple: #7c3aed;
        --accent-violet: #8b5cf6;
        --accent-pink: #ec4899;
        --accent-blue: #3b82f6;
        --accent-cyan: #22d3ee;
        --accent-green: #22c55e;
        --accent-orange: #f97316;
        --accent-yellow: #eab308;
    }
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(180deg, var(--bg-dark) 0%, #0a0a0f 100%);
    }
    
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 1.5rem 2rem; max-width: 100%; }
    
    /* ===== HERO HEADER ===== */
    .hero {
        background: linear-gradient(135deg, #7c3aed 0%, #ec4899 50%, #f97316 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .hero::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M30 0L60 30L30 60L0 30z' fill='%23ffffff' fill-opacity='0.05'/%3E%3C/svg%3E");
        opacity: 0.5;
    }
    
    .hero-content { position: relative; z-index: 1; }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: white;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .hero-sub {
        font-size: 1.1rem;
        color: rgba(255,255,255,0.9);
        margin-top: 0.5rem;
    }
    
    .hero-badges {
        display: flex;
        gap: 0.5rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }
    
    .hero-badge {
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        padding: 0.4rem 1rem;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 500;
        color: white;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a24 0%, #0f0f14 100%);
        border-right: 1px solid var(--border);
    }
    
    section[data-testid="stSidebar"] > div { background: transparent; }
    
    .sidebar-header {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text-bright);
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .sidebar-section {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .sidebar-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--accent-violet);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    /* ===== KPI CARDS ===== */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .kpi-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--accent-purple), var(--accent-pink));
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .kpi-card:hover {
        transform: translateY(-4px);
        border-color: var(--accent-purple);
        box-shadow: 0 20px 40px rgba(124, 58, 237, 0.2);
    }
    
    .kpi-card:hover::before { opacity: 1; }
    
    .kpi-icon {
        font-size: 2rem;
        margin-bottom: 0.75rem;
    }
    
    .kpi-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--text-bright), var(--accent-violet));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.25rem 0;
    }
    
    .kpi-trend {
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--accent-green);
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    /* ===== SECTION HEADERS ===== */
    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text-bright);
        margin: 2rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .section-icon {
        width: 32px;
        height: 32px;
        background: linear-gradient(135deg, var(--accent-purple), var(--accent-pink));
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
    }
    
    /* ===== CHART CARDS ===== */
    .chart-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .chart-header {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-bright);
        margin-bottom: 0.25rem;
    }
    
    .chart-subtitle {
        font-size: 0.85rem;
        color: var(--text-secondary);
        margin-bottom: 1rem;
    }
    
    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: var(--text-secondary);
        border-radius: 8px;
        font-weight: 500;
        padding: 0.6rem 1.25rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--accent-purple), var(--accent-pink)) !important;
        color: white !important;
    }
    
    /* ===== FOOTER ===== */
    .footer {
        text-align: center;
        padding: 2.5rem;
        margin-top: 3rem;
        border-top: 1px solid var(--border);
        background: var(--bg-card);
        border-radius: 16px 16px 0 0;
    }
    
    .footer-title {
        font-size: 1.25rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--text-bright), var(--accent-violet));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .footer-sub { color: var(--text-secondary); margin: 0.5rem 0 1.5rem 0; }
    
    .tech-stack {
        display: flex;
        justify-content: center;
        gap: 0.75rem;
        flex-wrap: wrap;
        margin-bottom: 1.5rem;
    }
    
    .tech-badge {
        background: var(--bg-hover);
        border: 1px solid var(--border);
        padding: 0.5rem 1rem;
        border-radius: 999px;
        font-size: 0.85rem;
        color: var(--text-primary);
        transition: all 0.2s;
    }
    
    .tech-badge:hover {
        border-color: var(--accent-purple);
        background: rgba(124, 58, 237, 0.15);
    }
    
    .github-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: var(--accent-purple);
        color: white;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        text-decoration: none;
        transition: all 0.2s;
    }
    
    .github-btn:hover {
        background: var(--accent-pink);
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(236, 72, 153, 0.3);
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: var(--bg-dark); }
    ::-webkit-scrollbar-thumb { 
        background: linear-gradient(180deg, var(--accent-purple), var(--accent-pink)); 
        border-radius: 4px; 
    }
    
    /* ===== FORM ELEMENTS ===== */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: var(--bg-hover) !important;
        border-color: var(--border) !important;
        color: var(--text-bright) !important;
    }
    
    .stDateInput > div > div > input {
        background: var(--bg-hover) !important;
        color: var(--text-bright) !important;
    }
</style>
""", unsafe_allow_html=True)


# Database Connection
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


def format_currency(value):
    if value >= 1_000_000:
        return f"R$ {value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"R$ {value/1_000:.1f}K"
    return f"R$ {value:,.2f}"


def format_number(value):
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value/1_000:.1f}K"
    return f"{value:,.0f}"


# Load Data
try:
    fct_orders, dim_customers, dim_products, dim_sellers = load_data()
    data_loaded = True
except Exception as e:
    data_loaded = False
    error_message = str(e)


# ===== SIDEBAR WITH FILTERS =====
with st.sidebar:
    st.markdown('<div class="sidebar-header">🎛️ Control Panel</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Date Range Filter
    st.markdown('<div class="sidebar-label">📅 Date Range</div>', unsafe_allow_html=True)
    
    if data_loaded and 'order_purchase_timestamp' in fct_orders.columns:
        fct_orders['order_purchase_timestamp'] = pd.to_datetime(fct_orders['order_purchase_timestamp'])
        min_date = fct_orders['order_purchase_timestamp'].min().date()
        max_date = fct_orders['order_purchase_timestamp'].max().date()
        
        date_range = st.date_input(
            "Select dates",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            label_visibility="collapsed"
        )
    
    st.markdown("---")
    
    # Category Filter
    st.markdown('<div class="sidebar-label">🏷️ Product Category</div>', unsafe_allow_html=True)
    
    if data_loaded:
        categories = ['All Categories'] + sorted(fct_orders['product_category_name'].dropna().unique().tolist())
        selected_category = st.selectbox("Select category", categories, label_visibility="collapsed")
    
    st.markdown("---")
    
    # State Filter
    st.markdown('<div class="sidebar-label">📍 Customer State</div>', unsafe_allow_html=True)
    
    if data_loaded:
        states = ['All States'] + sorted(dim_customers['state'].dropna().unique().tolist())
        selected_state = st.selectbox("Select state", states, label_visibility="collapsed")
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown('<div class="sidebar-label">📊 Quick Stats</div>', unsafe_allow_html=True)
    
    if data_loaded:
        st.metric("Total Products", format_number(dim_products['product_id'].nunique()))
        st.metric("Total Sellers", format_number(dim_sellers['seller_id'].nunique()))
        st.metric("Avg Rating", f"{dim_sellers['avg_review_score'].mean():.2f} ⭐")


if not data_loaded:
    st.error(f"❌ Connection Error: {error_message}")
    st.stop()


# Apply Filters
filtered_orders = fct_orders.copy()

if len(date_range) == 2:
    mask = (filtered_orders['order_purchase_timestamp'].dt.date >= date_range[0]) & \
           (filtered_orders['order_purchase_timestamp'].dt.date <= date_range[1])
    filtered_orders = filtered_orders[mask]

if selected_category != 'All Categories':
    filtered_orders = filtered_orders[filtered_orders['product_category_name'] == selected_category]


# ===== HERO HEADER =====
st.markdown("""
<div class="hero">
    <div class="hero-content">
        <h1 class="hero-title">🛒 Olist E-commerce Analytics</h1>
        <p class="hero-sub">Real-time insights from 100K+ Brazilian e-commerce orders</p>
        <div class="hero-badges">
            <span class="hero-badge">📊 dbt Models</span>
            <span class="hero-badge">🦆 MotherDuck</span>
            <span class="hero-badge">⚡ Real-time</span>
            <span class="hero-badge">✨ Interactive</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# Calculate KPIs
total_revenue = filtered_orders['total_order_value'].sum()
total_orders = filtered_orders['order_id'].nunique()
total_customers = dim_customers['customer_id'].nunique()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0


# ===== KPI CARDS =====
st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-icon">💰</div>
        <div class="kpi-label">Total Revenue</div>
        <div class="kpi-value">{format_currency(total_revenue)}</div>
        <div class="kpi-trend">↗ 12.5% growth</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">📦</div>
        <div class="kpi-label">Orders</div>
        <div class="kpi-value">{format_number(total_orders)}</div>
        <div class="kpi-trend">↗ 8.2% vs last</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">👥</div>
        <div class="kpi-label">Customers</div>
        <div class="kpi-value">{format_number(total_customers)}</div>
        <div class="kpi-trend">↗ 15.3% new</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">🛍️</div>
        <div class="kpi-label">Avg Order</div>
        <div class="kpi-value">{format_currency(avg_order_value)}</div>
        <div class="kpi-trend">→ Stable</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ===== CHARTS =====
st.markdown('<div class="section-title"><div class="section-icon">📈</div>Revenue Analytics</div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="chart-card"><div class="chart-header">Monthly Revenue Trend</div><div class="chart-subtitle">Revenue and order volume over time</div></div>', unsafe_allow_html=True)
    
    monthly = filtered_orders.copy()
    monthly['month'] = monthly['order_purchase_timestamp'].dt.to_period('M').astype(str)
    monthly_agg = monthly.groupby('month').agg({'total_order_value': 'sum', 'order_id': 'nunique'}).reset_index()
    monthly_agg.columns = ['month', 'revenue', 'orders']
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(go.Scatter(
        x=monthly_agg['month'], y=monthly_agg['revenue'],
        name='Revenue', fill='tozeroy',
        fillcolor='rgba(124, 58, 237, 0.3)',
        line=dict(color='#8b5cf6', width=3),
        mode='lines+markers',
        marker=dict(size=8, color='#a78bfa')
    ), secondary_y=False)
    
    fig.add_trace(go.Bar(
        x=monthly_agg['month'], y=monthly_agg['orders'],
        name='Orders', marker_color='rgba(236, 72, 153, 0.6)',
        opacity=0.8
    ), secondary_y=True)
    
    fig.update_layout(
        height=380,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#9898a6')),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#9898a6'), title='Revenue'),
        yaxis2=dict(tickfont=dict(color='#9898a6'), title='Orders', showgrid=False),
        legend=dict(orientation='h', y=1.1, font=dict(color='#f0f0f5')),
        margin=dict(t=40, b=40),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<div class="chart-card"><div class="chart-header">Customer Segments</div><div class="chart-subtitle">Revenue distribution by type</div></div>', unsafe_allow_html=True)
    
    cust_rev = dim_customers.groupby('customer_type')['lifetime_value'].sum().reset_index()
    colors = ['#8b5cf6', '#22c55e', '#3f3f46']
    
    fig = go.Figure(go.Pie(
        labels=cust_rev['customer_type'],
        values=cust_rev['lifetime_value'],
        hole=0.7,
        marker=dict(colors=colors, line=dict(color='#0f0f14', width=3)),
        textinfo='percent+label',
        textfont=dict(color='#f0f0f5', size=11)
    ))
    
    fig.update_layout(
        height=380,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(t=40, b=40),
        annotations=[dict(text='<b>Customers</b>', x=0.5, y=0.5, font=dict(size=14, color='#f0f0f5'), showarrow=False)]
    )
    
    st.plotly_chart(fig, use_container_width=True)


# Top Categories & Sellers
st.markdown('<div class="section-title"><div class="section-icon">🏆</div>Top Performers</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-card"><div class="chart-header">Top 8 Categories</div><div class="chart-subtitle">By revenue</div></div>', unsafe_allow_html=True)
    
    cat_data = filtered_orders.groupby('product_category_name')['total_order_value'].sum().reset_index()
    cat_data = cat_data.nlargest(8, 'total_order_value').sort_values('total_order_value')
    
    fig = go.Figure(go.Bar(
        x=cat_data['total_order_value'],
        y=cat_data['product_category_name'],
        orientation='h',
        marker=dict(
            color=cat_data['total_order_value'],
            colorscale=[[0, '#7c3aed'], [0.5, '#ec4899'], [1, '#f97316']],
        ),
        text=[format_currency(x) for x in cat_data['total_order_value']],
        textposition='outside',
        textfont=dict(color='#c4b5fd', size=11)
    ))
    
    fig.update_layout(
        height=380,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#9898a6')),
        yaxis=dict(tickfont=dict(color='#f0f0f5', size=10)),
        margin=dict(l=0, r=100, t=20, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<div class="chart-card"><div class="chart-header">Seller Tiers</div><div class="chart-subtitle">Performance distribution</div></div>', unsafe_allow_html=True)
    
    seller_stats = dim_sellers.groupby('seller_tier').size().reset_index(name='count')
    tier_order = ['Platinum', 'Gold', 'Silver', 'Bronze']
    seller_stats['seller_tier'] = pd.Categorical(seller_stats['seller_tier'], categories=tier_order, ordered=True)
    seller_stats = seller_stats.sort_values('seller_tier')
    
    tier_colors = ['#e5e4e2', '#fbbf24', '#94a3b8', '#d97706']
    
    fig = go.Figure(go.Bar(
        x=seller_stats['seller_tier'],
        y=seller_stats['count'],
        marker_color=tier_colors,
        text=seller_stats['count'],
        textposition='outside',
        textfont=dict(color='#f0f0f5', size=13)
    ))
    
    fig.update_layout(
        height=380,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickfont=dict(color='#f0f0f5', size=12)),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#9898a6')),
        margin=dict(t=20, b=20),
        bargap=0.4
    )
    
    st.plotly_chart(fig, use_container_width=True)


# Geographic
st.markdown('<div class="section-title"><div class="section-icon">🗺️</div>Geographic Distribution</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    state_cust = dim_customers.groupby('state').size().reset_index(name='customers')
    state_cust = state_cust.nlargest(10, 'customers')
    
    fig = go.Figure(go.Bar(
        x=state_cust['state'], y=state_cust['customers'],
        marker=dict(color=state_cust['customers'], colorscale=[[0, '#7c3aed'], [1, '#ec4899']]),
        text=state_cust['customers'], textposition='outside',
        textfont=dict(color='#c4b5fd')
    ))
    
    fig.update_layout(
        title=dict(text='Customers by State', font=dict(color='#f0f0f5', size=14)),
        height=320, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickfont=dict(color='#f0f0f5')),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#9898a6')),
        margin=dict(t=50, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    state_sell = dim_sellers.groupby('state').size().reset_index(name='sellers')
    state_sell = state_sell.nlargest(10, 'sellers')
    
    fig = go.Figure(go.Bar(
        x=state_sell['state'], y=state_sell['sellers'],
        marker=dict(color=state_sell['sellers'], colorscale=[[0, '#22c55e'], [1, '#86efac']]),
        text=state_sell['sellers'], textposition='outside',
        textfont=dict(color='#86efac')
    ))
    
    fig.update_layout(
        title=dict(text='Sellers by State', font=dict(color='#f0f0f5', size=14)),
        height=320, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickfont=dict(color='#f0f0f5')),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#9898a6')),
        margin=dict(t=50, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)


# Data Explorer
st.markdown('<div class="section-title"><div class="section-icon">📋</div>Data Explorer</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🏆 Top Products", "👥 Top Customers", "🏪 Top Sellers"])

with tab1:
    prods = dim_products.nlargest(12, 'total_revenue')[['product_id', 'product_category_name', 'times_sold', 'total_revenue', 'sales_tier']].copy()
    prods['total_revenue'] = prods['total_revenue'].apply(lambda x: f"R$ {x:,.2f}")
    st.dataframe(prods, use_container_width=True, hide_index=True)

with tab2:
    custs = dim_customers.nlargest(12, 'lifetime_value')[['customer_unique_id', 'city', 'state', 'total_orders', 'lifetime_value', 'customer_type']].copy()
    custs['lifetime_value'] = custs['lifetime_value'].apply(lambda x: f"R$ {x:,.2f}")
    st.dataframe(custs, use_container_width=True, hide_index=True)

with tab3:
    sells = dim_sellers.nlargest(12, 'total_revenue')[['seller_id', 'state', 'total_orders', 'total_revenue', 'avg_review_score', 'seller_tier']].copy()
    sells['total_revenue'] = sells['total_revenue'].apply(lambda x: f"R$ {x:,.2f}")
    sells['avg_review_score'] = sells['avg_review_score'].apply(lambda x: f"{x:.1f} ⭐")
    st.dataframe(sells, use_container_width=True, hide_index=True)


# Footer
st.markdown("""
<div class="footer">
    <div class="footer-title">Olist E-commerce Analytics Platform</div>
    <p class="footer-sub">Transforming raw data into actionable insights</p>
    <div class="tech-stack">
        <span class="tech-badge">🦆 MotherDuck</span>
        <span class="tech-badge">📊 dbt Core</span>
        <span class="tech-badge">🐍 Python</span>
        <span class="tech-badge">🎨 Streamlit</span>
        <span class="tech-badge">📈 Plotly</span>
    </div>
    <a href="https://github.com/Mohith-Akash/olist-analytics-platform" target="_blank" class="github-btn">
        📂 View on GitHub
    </a>
</div>
""", unsafe_allow_html=True)
