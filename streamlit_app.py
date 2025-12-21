"""
🛒 Olist E-commerce Analytics Dashboard
A premium dark-themed analytics dashboard built with Streamlit + MotherDuck
Showcasing: dbt transformations, dimensional modeling, and interactive visualization
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
    page_title="Olist Analytics Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Dark Theme CSS
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Dark Theme Base */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Hero Header */
    .hero-container {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
        padding: 2.5rem 3rem;
        border-radius: 1.25rem;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(99, 102, 241, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        opacity: 0.3;
    }
    
    .hero-title {
        font-size: 2.75rem;
        font-weight: 700;
        color: white;
        margin: 0;
        text-shadow: 0 4px 12px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle {
        font-size: 1.15rem;
        color: rgba(255,255,255,0.9);
        margin-top: 0.75rem;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    .hero-badges {
        margin-top: 1.25rem;
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
        position: relative;
        z-index: 1;
    }
    
    .badge {
        background: rgba(255,255,255,0.15);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 2rem;
        font-size: 0.875rem;
        font-weight: 500;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.25);
        transition: all 0.3s ease;
    }
    
    .badge:hover {
        background: rgba(255,255,255,0.25);
        transform: translateY(-2px);
    }
    
    /* KPI Cards - Glassmorphism */
    .kpi-card {
        background: rgba(30, 41, 59, 0.8);
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(99, 102, 241, 0.3);
        border-color: rgba(99, 102, 241, 0.5);
    }
    
    .kpi-icon {
        font-size: 2.25rem;
        margin-bottom: 0.5rem;
    }
    
    .kpi-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #f1f5f9;
        margin: 0.5rem 0;
        background: linear-gradient(135deg, #fff 0%, #c7d2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .kpi-label {
        font-size: 0.85rem;
        color: #94a3b8;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.75px;
    }
    
    .kpi-trend {
        font-size: 0.8rem;
        color: #10b981;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #f1f5f9;
        margin: 2.5rem 0 1.25rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 3px solid;
        border-image: linear-gradient(90deg, #6366f1, #a855f7) 1;
        display: inline-block;
    }
    
    /* Chart Containers */
    .chart-container {
        background: rgba(30, 41, 59, 0.6);
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 4px 24px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.05);
        margin-bottom: 1rem;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(30, 41, 59, 0.5);
        padding: 0.5rem;
        border-radius: 0.75rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #94a3b8;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background: rgba(30, 41, 59, 0.6);
        border-radius: 0.75rem;
        overflow: hidden;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2.5rem;
        color: #94a3b8;
        margin-top: 3rem;
        border-top: 1px solid rgba(255,255,255,0.1);
        background: rgba(15, 23, 42, 0.5);
        border-radius: 1rem;
    }
    
    .footer a {
        color: #a5b4fc;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    
    .footer a:hover {
        color: #c4b5fd;
    }
    
    .tech-stack {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-top: 1.25rem;
        flex-wrap: wrap;
    }
    
    .tech-item {
        background: rgba(99, 102, 241, 0.2);
        padding: 0.5rem 1.25rem;
        border-radius: 2rem;
        font-size: 0.875rem;
        color: #c7d2fe;
        font-weight: 500;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e293b;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #475569;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #64748b;
    }
    
    /* Input styling */
    .stSelectbox > div > div {
        background: rgba(30, 41, 59, 0.8) !important;
        border-color: rgba(255,255,255,0.1) !important;
    }
    
    .stDateInput > div > div {
        background: rgba(30, 41, 59, 0.8) !important;
    }
    
    /* Metric containers */
    [data-testid="stMetricValue"] {
        color: #f1f5f9 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }
</style>
""", unsafe_allow_html=True)


# Database Connection
@st.cache_resource
def get_connection():
    """Create MotherDuck connection."""
    token = os.getenv("MOTHERDUCK_TOKEN") or st.secrets.get("MOTHERDUCK_TOKEN", "")
    if token:
        return duckdb.connect(f"md:olist_analytics?motherduck_token={token}")
    return duckdb.connect("md:olist_analytics")


@st.cache_data(ttl=600)
def load_data():
    """Load data from MotherDuck dbt marts."""
    conn = get_connection()
    fct_orders = conn.execute("SELECT * FROM dbt_main.fct_orders").df()
    dim_customers = conn.execute("SELECT * FROM dbt_main.dim_customers").df()
    dim_products = conn.execute("SELECT * FROM dbt_main.dim_products").df()
    dim_sellers = conn.execute("SELECT * FROM dbt_main.dim_sellers").df()
    return fct_orders, dim_customers, dim_products, dim_sellers


def format_currency(value):
    """Format as Brazilian Real."""
    if value >= 1_000_000:
        return f"R$ {value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"R$ {value/1_000:.1f}K"
    return f"R$ {value:,.2f}"


def format_number(value):
    """Format number with K/M suffix."""
    if value >= 1_000_000:
        return f"{value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"{value/1_000:.1f}K"
    return f"{value:,.0f}"


# Plotly dark theme template
dark_template = {
    'layout': {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font': {'color': '#e2e8f0', 'family': 'Inter'},
        'xaxis': {
            'gridcolor': 'rgba(255,255,255,0.1)',
            'linecolor': 'rgba(255,255,255,0.1)',
            'tickfont': {'color': '#94a3b8'}
        },
        'yaxis': {
            'gridcolor': 'rgba(255,255,255,0.1)',
            'linecolor': 'rgba(255,255,255,0.1)',
            'tickfont': {'color': '#94a3b8'}
        },
        'colorway': ['#8b5cf6', '#6366f1', '#a855f7', '#c084fc', '#e879f9', '#f0abfc']
    }
}


# Load Data
try:
    fct_orders, dim_customers, dim_products, dim_sellers = load_data()
    data_loaded = True
except Exception as e:
    data_loaded = False
    error_message = str(e)


# Hero Header
st.markdown("""
<div class="hero-container">
    <h1 class="hero-title">🛒 Olist E-commerce Analytics</h1>
    <p class="hero-subtitle">Real-time insights from 100,000+ Brazilian e-commerce orders</p>
    <div class="hero-badges">
        <span class="badge">📊 dbt Transformations</span>
        <span class="badge">🦆 MotherDuck Cloud</span>
        <span class="badge">⚡ Real-time Data</span>
        <span class="badge">🏗️ Dimensional Model</span>
    </div>
</div>
""", unsafe_allow_html=True)


if not data_loaded:
    st.error(f"❌ Failed to connect to MotherDuck: {error_message}")
    st.info("💡 Ensure MOTHERDUCK_TOKEN is configured in your environment.")
    st.stop()


# Sidebar
with st.sidebar:
    st.markdown("## 🎛️ Dashboard Controls")
    st.markdown("---")
    
    # Date Filter
    if 'order_purchase_timestamp' in fct_orders.columns:
        fct_orders['order_purchase_timestamp'] = pd.to_datetime(fct_orders['order_purchase_timestamp'])
        min_date = fct_orders['order_purchase_timestamp'].min().date()
        max_date = fct_orders['order_purchase_timestamp'].max().date()
        
        st.markdown("### 📅 Date Range")
        date_range = st.date_input(
            "Select period",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            label_visibility="collapsed"
        )
        
        if len(date_range) == 2:
            mask = (fct_orders['order_purchase_timestamp'].dt.date >= date_range[0]) & \
                   (fct_orders['order_purchase_timestamp'].dt.date <= date_range[1])
            filtered_orders = fct_orders[mask]
        else:
            filtered_orders = fct_orders
    else:
        filtered_orders = fct_orders
    
    st.markdown("---")
    
    # Category Filter
    if 'product_category_name' in filtered_orders.columns:
        st.markdown("### 🏷️ Product Category")
        categories = ['All Categories'] + sorted(filtered_orders['product_category_name'].dropna().unique().tolist())
        selected_category = st.selectbox("Filter by category", categories, label_visibility="collapsed")
        
        if selected_category != 'All Categories':
            filtered_orders = filtered_orders[filtered_orders['product_category_name'] == selected_category]
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("### 📈 Quick Stats")
    st.markdown(f"**Orders in view:** {len(filtered_orders):,}")
    st.markdown(f"**Date range:** {(date_range[1] - date_range[0]).days if len(date_range) == 2 else 'N/A'} days")
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #64748b; font-size: 0.85rem; padding: 1rem;'>
        Built with ❤️ by<br/>
        <strong style='color: #a5b4fc;'>Analytics Engineer</strong>
    </div>
    """, unsafe_allow_html=True)


# Calculate KPIs
total_revenue = filtered_orders['total_order_value'].sum()
total_orders = filtered_orders['order_id'].nunique()
total_customers = dim_customers['customer_id'].nunique()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
total_products = dim_products['product_id'].nunique()
avg_review = dim_sellers['avg_review_score'].mean()


# KPI Cards Row
st.markdown('<p class="section-header">📊 Key Performance Indicators</p>', unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6 = st.columns(6)

kpi_data = [
    ("💰", "Total Revenue", format_currency(total_revenue), "All time", col1),
    ("📦", "Orders", format_number(total_orders), "Processed", col2),
    ("👥", "Customers", format_number(total_customers), "Unique", col3),
    ("🛍️", "Avg Order", format_currency(avg_order_value), "Per transaction", col4),
    ("📱", "Products", format_number(total_products), "In catalog", col5),
    ("⭐", "Avg Rating", f"{avg_review:.2f}/5", "Seller score", col6),
]

for icon, label, value, trend, col in kpi_data:
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-trend">{trend}</div>
        </div>
        """, unsafe_allow_html=True)


# Charts Row 1
st.markdown('<p class="section-header">📈 Revenue Analytics</p>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    # Monthly Revenue Trend
    monthly_data = filtered_orders.copy()
    monthly_data['month'] = monthly_data['order_purchase_timestamp'].dt.to_period('M').astype(str)
    monthly_agg = monthly_data.groupby('month').agg({
        'total_order_value': 'sum',
        'order_id': 'nunique'
    }).reset_index()
    monthly_agg.columns = ['month', 'revenue', 'orders']
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(
            x=monthly_agg['month'],
            y=monthly_agg['revenue'],
            name="Revenue",
            fill='tozeroy',
            fillcolor='rgba(139, 92, 246, 0.3)',
            line=dict(color='#a855f7', width=3),
            mode='lines+markers',
            marker=dict(size=8, color='#c084fc')
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Bar(
            x=monthly_agg['month'],
            y=monthly_agg['orders'],
            name="Orders",
            marker_color='rgba(99, 102, 241, 0.6)',
            opacity=0.8
        ),
        secondary_y=True
    )
    
    fig.update_layout(
        title=dict(text="Monthly Revenue & Order Volume", font=dict(size=18, color='#f1f5f9')),
        xaxis_title="",
        yaxis_title="Revenue (BRL)",
        yaxis2_title="Order Count",
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            font=dict(color='#94a3b8')
        ),
        height=420,
        hovermode="x unified",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#94a3b8')),
        yaxis2=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#94a3b8')),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#94a3b8')),
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Revenue by Customer Type
    customer_revenue = dim_customers.groupby('customer_type')['lifetime_value'].sum().reset_index()
    
    colors = {'Returning': '#10b981', 'One-time': '#8b5cf6', 'No Orders': '#475569'}
    
    fig = go.Figure(data=[go.Pie(
        labels=customer_revenue['customer_type'],
        values=customer_revenue['lifetime_value'],
        hole=0.65,
        marker_colors=[colors.get(x, '#8b5cf6') for x in customer_revenue['customer_type']],
        textposition='outside',
        textinfo='percent+label',
        textfont=dict(color='#e2e8f0', size=12)
    )])
    
    fig.update_layout(
        title=dict(text="Revenue by Customer Type", font=dict(size=18, color='#f1f5f9')),
        showlegend=False,
        height=420,
        annotations=[dict(
            text='<b>Customer</b><br>Mix', 
            x=0.5, y=0.5, 
            font=dict(size=14, color='#94a3b8'), 
            showarrow=False
        )],
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    st.plotly_chart(fig, use_container_width=True)


# Charts Row 2
st.markdown('<p class="section-header">🏆 Top Performers</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Top Categories
    category_revenue = filtered_orders.groupby('product_category_name')['total_order_value'].sum().reset_index()
    category_revenue = category_revenue.nlargest(10, 'total_order_value').sort_values('total_order_value')
    
    fig = go.Figure(go.Bar(
        x=category_revenue['total_order_value'],
        y=category_revenue['product_category_name'],
        orientation='h',
        marker=dict(
            color=category_revenue['total_order_value'],
            colorscale=[[0, '#6366f1'], [0.5, '#8b5cf6'], [1, '#a855f7']],
            line=dict(width=0)
        ),
        text=[format_currency(x) for x in category_revenue['total_order_value']],
        textposition='outside',
        textfont=dict(size=11, color='#c7d2fe')
    ))
    
    fig.update_layout(
        title=dict(text="Top 10 Product Categories", font=dict(size=18, color='#f1f5f9')),
        xaxis_title="Revenue (BRL)",
        yaxis_title="",
        height=450,
        margin=dict(l=10, r=120),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#94a3b8')),
        yaxis=dict(tickfont=dict(color='#e2e8f0')),
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Seller Tier Distribution
    seller_stats = dim_sellers.groupby('seller_tier').agg({
        'seller_id': 'count',
        'total_revenue': 'sum',
        'avg_review_score': 'mean'
    }).reset_index()
    seller_stats.columns = ['tier', 'count', 'revenue', 'avg_rating']
    
    tier_order = ['Platinum', 'Gold', 'Silver', 'Bronze']
    seller_stats['tier'] = pd.Categorical(seller_stats['tier'], categories=tier_order, ordered=True)
    seller_stats = seller_stats.sort_values('tier')
    
    tier_colors = {'Platinum': '#e5e4e2', 'Gold': '#fbbf24', 'Silver': '#94a3b8', 'Bronze': '#d97706'}
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=seller_stats['tier'],
        y=seller_stats['count'],
        name='Seller Count',
        marker_color=[tier_colors.get(t, '#8b5cf6') for t in seller_stats['tier']],
        text=seller_stats['count'],
        textposition='outside',
        textfont=dict(color='#e2e8f0'),
        marker_line=dict(color='rgba(255,255,255,0.2)', width=1)
    ))
    
    fig.update_layout(
        title=dict(text="Sellers by Performance Tier", font=dict(size=18, color='#f1f5f9')),
        xaxis_title="",
        yaxis_title="Number of Sellers",
        height=450,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickfont=dict(color='#e2e8f0')),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#94a3b8')),
    )
    
    st.plotly_chart(fig, use_container_width=True)


# Geographic Analysis
st.markdown('<p class="section-header">🗺️ Geographic Distribution</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Customer Distribution by State
    state_customers = dim_customers.groupby('state').agg({
        'customer_id': 'count',
        'lifetime_value': 'sum'
    }).reset_index()
    state_customers.columns = ['state', 'customers', 'revenue']
    state_customers = state_customers.nlargest(10, 'customers')
    
    fig = go.Figure(go.Bar(
        x=state_customers['state'],
        y=state_customers['customers'],
        marker=dict(
            color=state_customers['revenue'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Revenue", tickfont=dict(color='#94a3b8'), titlefont=dict(color='#94a3b8'))
        ),
        text=state_customers['customers'],
        textposition='outside',
        textfont=dict(color='#c7d2fe')
    ))
    
    fig.update_layout(
        title=dict(text="Top 10 States by Customer Count", font=dict(size=18, color='#f1f5f9')),
        xaxis_title="State",
        yaxis_title="Number of Customers",
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickfont=dict(color='#e2e8f0')),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#94a3b8')),
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Seller Distribution by State
    state_sellers = dim_sellers.groupby('state').agg({
        'seller_id': 'count',
        'total_revenue': 'sum',
        'avg_review_score': 'mean'
    }).reset_index()
    state_sellers.columns = ['state', 'sellers', 'revenue', 'rating']
    state_sellers = state_sellers.nlargest(10, 'sellers')
    
    fig = go.Figure(go.Bar(
        x=state_sellers['state'],
        y=state_sellers['sellers'],
        marker=dict(
            color=state_sellers['rating'],
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(title="Avg Rating", tickfont=dict(color='#94a3b8'), titlefont=dict(color='#94a3b8'))
        ),
        text=state_sellers['sellers'],
        textposition='outside',
        textfont=dict(color='#c7d2fe')
    ))
    
    fig.update_layout(
        title=dict(text="Top 10 States by Seller Count", font=dict(size=18, color='#f1f5f9')),
        xaxis_title="State",
        yaxis_title="Number of Sellers",
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickfont=dict(color='#e2e8f0')),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#94a3b8')),
    )
    
    st.plotly_chart(fig, use_container_width=True)


# Data Explorer Section
st.markdown('<p class="section-header">🔍 Data Explorer</p>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🏆 Top Products", "👥 Top Customers", "🏪 Top Sellers", "📊 Raw Data Sample"])

with tab1:
    top_products = dim_products.nlargest(15, 'total_revenue')[
        ['product_id', 'product_category_name', 'times_sold', 'total_revenue', 'sales_tier']
    ].copy()
    top_products['total_revenue'] = top_products['total_revenue'].apply(lambda x: f"R$ {x:,.2f}")
    st.dataframe(top_products, use_container_width=True, hide_index=True)

with tab2:
    top_customers = dim_customers.nlargest(15, 'lifetime_value')[
        ['customer_unique_id', 'city', 'state', 'total_orders', 'lifetime_value', 'customer_type']
    ].copy()
    top_customers['lifetime_value'] = top_customers['lifetime_value'].apply(lambda x: f"R$ {x:,.2f}")
    st.dataframe(top_customers, use_container_width=True, hide_index=True)

with tab3:
    top_sellers = dim_sellers.nlargest(15, 'total_revenue')[
        ['seller_id', 'state', 'total_orders', 'total_revenue', 'avg_review_score', 'seller_tier']
    ].copy()
    top_sellers['total_revenue'] = top_sellers['total_revenue'].apply(lambda x: f"R$ {x:,.2f}")
    top_sellers['avg_review_score'] = top_sellers['avg_review_score'].apply(lambda x: f"{x:.2f} ⭐")
    st.dataframe(top_sellers, use_container_width=True, hide_index=True)

with tab4:
    st.markdown("**Sample of Order Fact Table (first 100 rows)**")
    sample_orders = filtered_orders.head(100)[
        ['order_id', 'customer_id', 'product_category_name', 'price', 'freight_value', 'total_order_value']
    ].copy()
    sample_orders['total_order_value'] = sample_orders['total_order_value'].apply(lambda x: f"R$ {x:,.2f}")
    st.dataframe(sample_orders, use_container_width=True, hide_index=True)


# Footer
st.markdown("""
<div class="footer">
    <p style="font-size: 1.25rem; color: #f1f5f9; margin-bottom: 0.5rem;"><strong>Olist E-commerce Analytics Platform</strong></p>
    <p>Transforming raw data into actionable insights with Modern Data Stack</p>
    <div class="tech-stack">
        <span class="tech-item">🦆 DuckDB / MotherDuck</span>
        <span class="tech-item">📊 dbt Core</span>
        <span class="tech-item">🐍 Python</span>
        <span class="tech-item">🎨 Streamlit</span>
        <span class="tech-item">📈 Plotly</span>
    </div>
    <p style="margin-top: 1.5rem;">
        <a href="https://github.com/mohith-akash/olist-analytics-platform" target="_blank">📂 View Source on GitHub</a>
    </p>
</div>
""", unsafe_allow_html=True)
