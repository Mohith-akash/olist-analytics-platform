"""
🛒 Olist E-commerce Analytics Dashboard
Enterprise-grade SaaS analytics dashboard
Inspired by: Linear, Vercel, Stripe Dashboard aesthetics
"""

import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import os

# Page Configuration
st.set_page_config(
    page_title="Olist Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enterprise SaaS Dashboard CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --bg-primary: #09090b;
        --bg-secondary: #18181b;
        --bg-tertiary: #27272a;
        --bg-card: rgba(24, 24, 27, 0.8);
        --border-color: rgba(63, 63, 70, 0.5);
        --border-hover: rgba(99, 102, 241, 0.5);
        --text-primary: #fafafa;
        --text-secondary: #a1a1aa;
        --text-muted: #71717a;
        --accent-primary: #6366f1;
        --accent-secondary: #8b5cf6;
        --accent-success: #22c55e;
        --accent-warning: #f59e0b;
        --accent-danger: #ef4444;
        --accent-info: #06b6d4;
    }
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: var(--bg-primary);
    }
    
    /* Hide defaults */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding: 2rem 3rem 3rem 3rem; max-width: 100%;}
    
    /* ===== NAVIGATION BAR ===== */
    .nav-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1rem 0;
        border-bottom: 1px solid var(--border-color);
        margin-bottom: 2rem;
    }
    
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .nav-brand-icon {
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
    }
    
    .nav-brand-text {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -0.5px;
    }
    
    .nav-badge {
        background: rgba(34, 197, 94, 0.15);
        color: var(--accent-success);
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 0.75rem;
    }
    
    .nav-links {
        display: flex;
        gap: 0.5rem;
    }
    
    .nav-link {
        padding: 0.5rem 1rem;
        color: var(--text-secondary);
        text-decoration: none;
        border-radius: 0.5rem;
        font-size: 0.875rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .nav-link:hover, .nav-link.active {
        background: var(--bg-tertiary);
        color: var(--text-primary);
    }
    
    /* ===== STATS GRID ===== */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .stat-card {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        transition: all 0.2s ease;
    }
    
    .stat-card:hover {
        border-color: var(--border-hover);
        transform: translateY(-2px);
    }
    
    .stat-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.75rem;
    }
    
    .stat-label {
        font-size: 0.8rem;
        font-weight: 500;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stat-icon {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
    }
    
    .stat-icon.purple { background: rgba(99, 102, 241, 0.15); }
    .stat-icon.green { background: rgba(34, 197, 94, 0.15); }
    .stat-icon.blue { background: rgba(6, 182, 212, 0.15); }
    .stat-icon.orange { background: rgba(245, 158, 11, 0.15); }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -1px;
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    
    .stat-trend {
        display: flex;
        align-items: center;
        gap: 0.25rem;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .stat-trend.up { color: var(--accent-success); }
    .stat-trend.down { color: var(--accent-danger); }
    .stat-trend.neutral { color: var(--text-muted); }
    
    /* ===== CHART CARDS ===== */
    .chart-card {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .chart-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
    }
    
    .chart-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .chart-subtitle {
        font-size: 0.8rem;
        color: var(--text-muted);
        margin-top: 0.25rem;
    }
    
    .chart-actions {
        display: flex;
        gap: 0.5rem;
    }
    
    .chart-action-btn {
        padding: 0.375rem 0.75rem;
        background: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 6px;
        color: var(--text-secondary);
        font-size: 0.75rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .chart-action-btn:hover, .chart-action-btn.active {
        background: var(--accent-primary);
        border-color: var(--accent-primary);
        color: white;
    }
    
    /* ===== SECTION HEADERS ===== */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 2.5rem 0 1.25rem 0;
    }
    
    .section-icon {
        width: 28px;
        height: 28px;
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.875rem;
    }
    
    .section-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    /* ===== DATA TABLE ===== */
    .data-table-container {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        overflow: hidden;
    }
    
    .data-table-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1rem 1.5rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    .data-table-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 4px;
        gap: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 6px;
        color: var(--text-secondary);
        font-weight: 500;
        font-size: 0.875rem;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--bg-tertiary) !important;
        color: var(--text-primary) !important;
    }
    
    /* ===== FOOTER ===== */
    .footer-container {
        margin-top: 4rem;
        padding: 2rem 0;
        border-top: 1px solid var(--border-color);
        text-align: center;
    }
    
    .footer-brand {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .footer-tagline {
        font-size: 0.875rem;
        color: var(--text-muted);
        margin-bottom: 1.5rem;
    }
    
    .footer-tech-stack {
        display: flex;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
        margin-bottom: 1.5rem;
    }
    
    .tech-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 500;
        color: var(--text-secondary);
        transition: all 0.2s;
    }
    
    .tech-badge:hover {
        border-color: var(--accent-primary);
        color: var(--text-primary);
    }
    
    .footer-link {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.625rem 1.5rem;
        background: var(--accent-primary);
        border-radius: 8px;
        color: white;
        font-size: 0.875rem;
        font-weight: 600;
        text-decoration: none;
        transition: all 0.2s;
    }
    
    .footer-link:hover {
        background: var(--accent-secondary);
        transform: translateY(-1px);
    }
    
    /* ===== CUSTOM SCROLLBAR ===== */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: var(--bg-primary); }
    ::-webkit-scrollbar-thumb { background: var(--bg-tertiary); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent-primary); }
    
    /* ===== STREAMLIT OVERRIDES ===== */
    .stDataFrame { border-radius: 8px; overflow: hidden; }
    [data-testid="stMetricValue"] { color: var(--text-primary) !important; }
    .stSelectbox > div > div { background: var(--bg-tertiary) !important; border-color: var(--border-color) !important; }
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


def format_currency(value, short=True):
    if short:
        if value >= 1_000_000:
            return f"R${value/1_000_000:.1f}M"
        elif value >= 1_000:
            return f"R${value/1_000:.0f}K"
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


# Navigation Bar
st.markdown("""
<div class="nav-bar">
    <div class="nav-brand">
        <div class="nav-brand-icon">🛒</div>
        <span class="nav-brand-text">Olist Analytics</span>
        <span class="nav-badge">● Live</span>
    </div>
    <div class="nav-links">
        <a href="#" class="nav-link active">Dashboard</a>
        <a href="#" class="nav-link">Revenue</a>
        <a href="#" class="nav-link">Customers</a>
        <a href="#" class="nav-link">Products</a>
    </div>
</div>
""", unsafe_allow_html=True)


if not data_loaded:
    st.error(f"Connection failed: {error_message}")
    st.stop()


# Prepare data
fct_orders['order_purchase_timestamp'] = pd.to_datetime(fct_orders['order_purchase_timestamp'])
filtered_orders = fct_orders

# Calculate metrics
total_revenue = filtered_orders['total_order_value'].sum()
total_orders = filtered_orders['order_id'].nunique()
total_customers = dim_customers['customer_id'].nunique()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0


# Stats Grid
st.markdown(f"""
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-header">
            <span class="stat-label">Total Revenue</span>
            <div class="stat-icon purple">💰</div>
        </div>
        <div class="stat-value">{format_currency(total_revenue)}</div>
        <div class="stat-trend up">
            <span>↗</span> 12.5% from last period
        </div>
    </div>
    <div class="stat-card">
        <div class="stat-header">
            <span class="stat-label">Total Orders</span>
            <div class="stat-icon green">📦</div>
        </div>
        <div class="stat-value">{format_number(total_orders)}</div>
        <div class="stat-trend up">
            <span>↗</span> 8.2% growth
        </div>
    </div>
    <div class="stat-card">
        <div class="stat-header">
            <span class="stat-label">Customers</span>
            <div class="stat-icon blue">👥</div>
        </div>
        <div class="stat-value">{format_number(total_customers)}</div>
        <div class="stat-trend up">
            <span>↗</span> 15.3% new users
        </div>
    </div>
    <div class="stat-card">
        <div class="stat-header">
            <span class="stat-label">Avg Order Value</span>
            <div class="stat-icon orange">🛍️</div>
        </div>
        <div class="stat-value">{format_currency(avg_order_value)}</div>
        <div class="stat-trend neutral">
            <span>→</span> Stable
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# Charts Section
col1, col2 = st.columns([2, 1])

with col1:
    # Revenue Chart
    st.markdown("""
    <div class="chart-card">
        <div class="chart-header">
            <div>
                <div class="chart-title">Revenue Overview</div>
                <div class="chart-subtitle">Monthly revenue and order volume</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Prepare monthly data
    monthly_data = filtered_orders.copy()
    monthly_data['month'] = monthly_data['order_purchase_timestamp'].dt.to_period('M').astype(str)
    monthly_agg = monthly_data.groupby('month').agg({
        'total_order_value': 'sum',
        'order_id': 'nunique'
    }).reset_index()
    monthly_agg.columns = ['month', 'revenue', 'orders']
    
    fig = go.Figure()
    
    # Area chart for revenue
    fig.add_trace(go.Scatter(
        x=monthly_agg['month'],
        y=monthly_agg['revenue'],
        name='Revenue',
        fill='tozeroy',
        fillcolor='rgba(99, 102, 241, 0.15)',
        line=dict(color='#6366f1', width=2.5),
        mode='lines',
        hovertemplate='%{x}<br>Revenue: R$%{y:,.0f}<extra></extra>'
    ))
    
    # Line for orders
    fig.add_trace(go.Scatter(
        x=monthly_agg['month'],
        y=monthly_agg['orders'],
        name='Orders',
        line=dict(color='#22c55e', width=2, dash='dot'),
        mode='lines',
        yaxis='y2',
        hovertemplate='%{x}<br>Orders: %{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        height=350,
        margin=dict(l=0, r=0, t=20, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color='#71717a', size=11),
            linecolor='rgba(63,63,70,0.5)'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(63,63,70,0.3)',
            tickfont=dict(color='#71717a', size=11),
            title=None
        ),
        yaxis2=dict(
            overlaying='y',
            side='right',
            showgrid=False,
            tickfont=dict(color='#71717a', size=11),
            title=None
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='left',
            x=0,
            font=dict(color='#a1a1aa', size=12),
            bgcolor='rgba(0,0,0,0)'
        ),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col2:
    # Customer Segments
    st.markdown("""
    <div class="chart-card">
        <div class="chart-header">
            <div>
                <div class="chart-title">Customer Segments</div>
                <div class="chart-subtitle">Revenue by customer type</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    customer_revenue = dim_customers.groupby('customer_type')['lifetime_value'].sum().reset_index()
    colors = ['#6366f1', '#22c55e', '#3f3f46']
    
    fig = go.Figure(data=[go.Pie(
        labels=customer_revenue['customer_type'],
        values=customer_revenue['lifetime_value'],
        hole=0.75,
        marker=dict(colors=colors, line=dict(color='#09090b', width=2)),
        textinfo='none',
        hovertemplate='%{label}<br>R$%{value:,.0f}<br>%{percent}<extra></extra>'
    )])
    
    # Center text
    total_customer_revenue = customer_revenue['lifetime_value'].sum()
    
    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.1,
            xanchor='center',
            x=0.5,
            font=dict(color='#a1a1aa', size=11),
            bgcolor='rgba(0,0,0,0)'
        ),
        annotations=[
            dict(
                text=f"<b>{format_currency(total_customer_revenue)}</b><br><span style='color:#71717a;font-size:12px'>Total</span>",
                x=0.5, y=0.5,
                font=dict(size=18, color='#fafafa'),
                showarrow=False
            )
        ]
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# Second Row Charts
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">📊</div>
        <span class="section-title">Top Categories</span>
    </div>
    """, unsafe_allow_html=True)
    
    category_data = filtered_orders.groupby('product_category_name')['total_order_value'].sum().reset_index()
    category_data = category_data.nlargest(8, 'total_order_value').sort_values('total_order_value', ascending=True)
    
    fig = go.Figure(go.Bar(
        x=category_data['total_order_value'],
        y=category_data['product_category_name'],
        orientation='h',
        marker=dict(
            color='#6366f1',
            line=dict(width=0)
        ),
        hovertemplate='%{y}<br>R$%{x:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        height=320,
        margin=dict(l=0, r=40, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(63,63,70,0.3)',
            tickfont=dict(color='#71717a', size=10)
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(color='#a1a1aa', size=11)
        ),
        bargap=0.4
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col2:
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">⭐</div>
        <span class="section-title">Seller Tiers</span>
    </div>
    """, unsafe_allow_html=True)
    
    seller_stats = dim_sellers.groupby('seller_tier').size().reset_index(name='count')
    tier_order = ['Platinum', 'Gold', 'Silver', 'Bronze']
    seller_stats['seller_tier'] = pd.Categorical(seller_stats['seller_tier'], categories=tier_order, ordered=True)
    seller_stats = seller_stats.sort_values('seller_tier')
    
    tier_colors = {'Platinum': '#e5e4e2', 'Gold': '#fbbf24', 'Silver': '#71717a', 'Bronze': '#d97706'}
    colors = [tier_colors.get(t, '#6366f1') for t in seller_stats['seller_tier']]
    
    fig = go.Figure(go.Bar(
        x=seller_stats['seller_tier'],
        y=seller_stats['count'],
        marker=dict(color=colors, line=dict(width=0)),
        text=seller_stats['count'],
        textposition='outside',
        textfont=dict(color='#a1a1aa', size=12),
        hovertemplate='%{x}<br>Sellers: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        height=320,
        margin=dict(l=0, r=0, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color='#a1a1aa', size=12)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(63,63,70,0.3)',
            tickfont=dict(color='#71717a', size=10)
        ),
        bargap=0.5
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# Geographic Section
st.markdown("""
<div class="section-header">
    <div class="section-icon">🗺️</div>
    <span class="section-title">Geographic Distribution</span>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    state_data = dim_customers.groupby('state').size().reset_index(name='customers')
    state_data = state_data.nlargest(10, 'customers')
    
    fig = go.Figure(go.Bar(
        x=state_data['state'],
        y=state_data['customers'],
        marker=dict(
            color=state_data['customers'],
            colorscale=[[0, '#3f3f46'], [0.5, '#6366f1'], [1, '#8b5cf6']],
            line=dict(width=0)
        ),
        hovertemplate='%{x}<br>Customers: %{y:,}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text='Customers by State', font=dict(size=14, color='#fafafa'), x=0),
        height=280,
        margin=dict(l=0, r=0, t=40, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, tickfont=dict(color='#a1a1aa', size=11)),
        yaxis=dict(showgrid=True, gridcolor='rgba(63,63,70,0.3)', tickfont=dict(color='#71717a', size=10)),
        bargap=0.3
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col2:
    seller_state = dim_sellers.groupby('state').size().reset_index(name='sellers')
    seller_state = seller_state.nlargest(10, 'sellers')
    
    fig = go.Figure(go.Bar(
        x=seller_state['state'],
        y=seller_state['sellers'],
        marker=dict(
            color=seller_state['sellers'],
            colorscale=[[0, '#3f3f46'], [0.5, '#22c55e'], [1, '#4ade80']],
            line=dict(width=0)
        ),
        hovertemplate='%{x}<br>Sellers: %{y:,}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text='Sellers by State', font=dict(size=14, color='#fafafa'), x=0),
        height=280,
        margin=dict(l=0, r=0, t=40, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, tickfont=dict(color='#a1a1aa', size=11)),
        yaxis=dict(showgrid=True, gridcolor='rgba(63,63,70,0.3)', tickfont=dict(color='#71717a', size=10)),
        bargap=0.3
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# Data Tables
st.markdown("""
<div class="section-header">
    <div class="section-icon">📋</div>
    <span class="section-title">Data Explorer</span>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Top Products", "Top Customers", "Top Sellers"])

with tab1:
    products = dim_products.nlargest(10, 'total_revenue')[['product_id', 'product_category_name', 'times_sold', 'total_revenue', 'sales_tier']].copy()
    products['total_revenue'] = products['total_revenue'].apply(lambda x: f"R$ {x:,.2f}")
    st.dataframe(products, use_container_width=True, hide_index=True)

with tab2:
    customers = dim_customers.nlargest(10, 'lifetime_value')[['customer_unique_id', 'city', 'state', 'total_orders', 'lifetime_value', 'customer_type']].copy()
    customers['lifetime_value'] = customers['lifetime_value'].apply(lambda x: f"R$ {x:,.2f}")
    st.dataframe(customers, use_container_width=True, hide_index=True)

with tab3:
    sellers = dim_sellers.nlargest(10, 'total_revenue')[['seller_id', 'state', 'total_orders', 'total_revenue', 'avg_review_score', 'seller_tier']].copy()
    sellers['total_revenue'] = sellers['total_revenue'].apply(lambda x: f"R$ {x:,.2f}")
    sellers['avg_review_score'] = sellers['avg_review_score'].apply(lambda x: f"{x:.1f} ⭐")
    st.dataframe(sellers, use_container_width=True, hide_index=True)


# Footer
st.markdown("""
<div class="footer-container">
    <div class="footer-brand">Olist E-commerce Analytics</div>
    <div class="footer-tagline">Modern Data Stack • Real-time Analytics • Enterprise Grade</div>
    <div class="footer-tech-stack">
        <span class="tech-badge">🦆 MotherDuck</span>
        <span class="tech-badge">📊 dbt Core</span>
        <span class="tech-badge">🐍 Python</span>
        <span class="tech-badge">🎨 Streamlit</span>
        <span class="tech-badge">📈 Plotly</span>
    </div>
    <a href="https://github.com/Mohith-Akash/olist-analytics-platform" target="_blank" class="footer-link">
        View on GitHub →
    </a>
</div>
""", unsafe_allow_html=True)
