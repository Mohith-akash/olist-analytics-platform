"""
🛒 Olist E-commerce Analytics Dashboard
Ultimate premium design with animated gradients, glassmorphism, and modern UI
Built with Streamlit + MotherDuck (DuckDB Cloud)
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

# Ultimate Premium Dark Theme CSS with Animations
st.markdown("""
<style>
    /* Import Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* CSS Variables for easy theming */
    :root {
        --bg-primary: #0a0a0f;
        --bg-secondary: #12121a;
        --bg-card: rgba(20, 20, 30, 0.8);
        --accent-purple: #8b5cf6;
        --accent-violet: #a855f7;
        --accent-pink: #ec4899;
        --accent-blue: #3b82f6;
        --accent-cyan: #06b6d4;
        --accent-green: #10b981;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --border-subtle: rgba(255, 255, 255, 0.08);
        --glow-purple: rgba(139, 92, 246, 0.5);
    }
    
    /* Animated Gradient Background */
    .stApp {
        font-family: 'Space Grotesk', 'Inter', sans-serif;
        background: var(--bg-primary);
        background-image: 
            radial-gradient(ellipse at 10% 20%, rgba(139, 92, 246, 0.15) 0%, transparent 50%),
            radial-gradient(ellipse at 90% 80%, rgba(236, 72, 153, 0.1) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 50%, rgba(6, 182, 212, 0.05) 0%, transparent 70%);
        min-height: 100vh;
    }
    
    /* Animated mesh gradient overlay */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            linear-gradient(135deg, transparent 0%, rgba(139, 92, 246, 0.03) 50%, transparent 100%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* Ultra Premium Hero Header */
    .hero-container {
        position: relative;
        background: linear-gradient(135deg, 
            rgba(139, 92, 246, 0.9) 0%, 
            rgba(168, 85, 247, 0.9) 25%,
            rgba(236, 72, 153, 0.85) 50%,
            rgba(59, 130, 246, 0.9) 75%,
            rgba(6, 182, 212, 0.9) 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        padding: 3rem 3.5rem;
        border-radius: 1.5rem;
        margin-bottom: 2.5rem;
        box-shadow: 
            0 0 60px rgba(139, 92, 246, 0.4),
            0 0 120px rgba(236, 72, 153, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Animated particles/dots overlay */
    .hero-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(255,255,255,0.15) 1px, transparent 1px),
            radial-gradient(circle at 80% 70%, rgba(255,255,255,0.1) 1px, transparent 1px),
            radial-gradient(circle at 40% 80%, rgba(255,255,255,0.12) 1px, transparent 1px),
            radial-gradient(circle at 60% 20%, rgba(255,255,255,0.08) 1px, transparent 1px);
        background-size: 100px 100px, 150px 150px, 200px 200px, 250px 250px;
        animation: floatParticles 20s linear infinite;
        opacity: 0.6;
    }
    
    @keyframes floatParticles {
        0% { transform: translateY(0) translateX(0); }
        50% { transform: translateY(-20px) translateX(10px); }
        100% { transform: translateY(0) translateX(0); }
    }
    
    /* Glowing line accent */
    .hero-container::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 10%;
        right: 10%;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.8), transparent);
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 1; }
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        color: white;
        margin: 0;
        text-shadow: 0 4px 20px rgba(0,0,0,0.4);
        position: relative;
        z-index: 1;
        letter-spacing: -0.5px;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: rgba(255,255,255,0.95);
        margin-top: 0.75rem;
        font-weight: 400;
        position: relative;
        z-index: 1;
        letter-spacing: 0.3px;
    }
    
    .hero-badges {
        margin-top: 1.5rem;
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
        position: relative;
        z-index: 1;
    }
    
    .badge {
        background: rgba(255,255,255,0.2);
        color: white;
        padding: 0.6rem 1.2rem;
        border-radius: 3rem;
        font-size: 0.9rem;
        font-weight: 500;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: default;
    }
    
    .badge:hover {
        background: rgba(255,255,255,0.35);
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    /* Ultra Premium KPI Cards with Glow */
    .kpi-card {
        background: linear-gradient(135deg, rgba(20, 20, 35, 0.9) 0%, rgba(30, 30, 50, 0.85) 100%);
        border-radius: 1.25rem;
        padding: 1.75rem 1.5rem;
        box-shadow: 
            0 8px 32px rgba(0,0,0,0.4),
            0 0 0 1px rgba(255,255,255,0.05),
            inset 0 1px 0 rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.08);
        backdrop-filter: blur(20px);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-purple), var(--accent-pink), var(--accent-cyan));
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 20px 60px rgba(139, 92, 246, 0.3),
            0 0 40px rgba(139, 92, 246, 0.15),
            0 0 0 1px rgba(139, 92, 246, 0.3),
            inset 0 1px 0 rgba(255,255,255,0.15);
        border-color: rgba(139, 92, 246, 0.5);
    }
    
    .kpi-card:hover::before {
        opacity: 1;
    }
    
    .kpi-icon {
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
    }
    
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
        background: linear-gradient(135deg, #fff 0%, #c4b5fd 50%, #f0abfc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: none;
    }
    
    .kpi-label {
        font-size: 0.8rem;
        color: var(--text-secondary);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    .kpi-trend {
        font-size: 0.75rem;
        color: var(--accent-green);
        font-weight: 600;
        margin-top: 0.75rem;
        padding: 0.3rem 0.8rem;
        background: rgba(16, 185, 129, 0.15);
        border-radius: 1rem;
        display: inline-block;
    }
    
    /* Premium Section Headers */
    .section-header {
        font-size: 1.6rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 3rem 0 1.5rem 0;
        padding-bottom: 1rem;
        position: relative;
        display: inline-block;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-purple), var(--accent-pink), transparent);
        border-radius: 2px;
    }
    
    /* Sidebar Premium Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f18 0%, #0a0a12 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown h2 {
        color: var(--text-primary);
        font-weight: 600;
    }
    
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: var(--accent-purple);
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    /* Premium Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(15, 15, 25, 0.8);
        padding: 0.5rem;
        border-radius: 1rem;
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: var(--text-secondary);
        border-radius: 0.75rem;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(139, 92, 246, 0.1);
        color: var(--text-primary);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--accent-purple), var(--accent-pink)) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
    }
    
    /* Premium Dataframe */
    .stDataFrame {
        background: rgba(15, 15, 25, 0.8);
        border-radius: 1rem;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Ultra Premium Footer */
    .footer {
        text-align: center;
        padding: 3rem;
        margin-top: 4rem;
        background: linear-gradient(180deg, rgba(15, 15, 25, 0.9) 0%, rgba(10, 10, 15, 0.95) 100%);
        border-top: 1px solid rgba(255,255,255,0.08);
        border-radius: 1.5rem 1.5rem 0 0;
        position: relative;
        overflow: hidden;
    }
    
    .footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 25%;
        right: 25%;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--accent-purple), var(--accent-pink), transparent);
    }
    
    .footer-title {
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--text-primary) 0%, var(--accent-purple) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .footer-subtitle {
        color: var(--text-secondary);
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .tech-stack {
        display: flex;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
        margin: 1.5rem 0;
    }
    
    .tech-item {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(236, 72, 153, 0.15) 100%);
        padding: 0.6rem 1.5rem;
        border-radius: 3rem;
        font-size: 0.9rem;
        color: var(--text-primary);
        font-weight: 500;
        border: 1px solid rgba(139, 92, 246, 0.3);
        transition: all 0.3s ease;
    }
    
    .tech-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.25);
    }
    
    .footer a {
        color: var(--accent-purple);
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
        padding: 0.75rem 2rem;
        border: 2px solid var(--accent-purple);
        border-radius: 3rem;
        display: inline-block;
        margin-top: 1rem;
    }
    
    .footer a:hover {
        background: var(--accent-purple);
        color: white;
        box-shadow: 0 8px 30px rgba(139, 92, 246, 0.4);
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Premium Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-primary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--accent-purple), var(--accent-pink));
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, var(--accent-pink), var(--accent-purple));
    }
    
    /* Premium Form Elements */
    .stSelectbox > div > div,
    .stMultiSelect > div > div,
    .stDateInput > div > div {
        background: rgba(15, 15, 25, 0.9) !important;
        border-color: rgba(255,255,255,0.1) !important;
        border-radius: 0.75rem !important;
    }
    
    .stSelectbox > div > div:hover,
    .stDateInput > div > div:hover {
        border-color: var(--accent-purple) !important;
    }
    
    /* Metrics override */
    [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
    }
    
    /* Loading animation */
    .stSpinner > div {
        border-top-color: var(--accent-purple) !important;
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
    """Format as Brazilian Real with smart abbreviation."""
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


# Premium color palettes
COLORS = {
    'primary': ['#8b5cf6', '#a855f7', '#c084fc', '#d8b4fe', '#ede9fe'],
    'accent': ['#ec4899', '#f472b6', '#f9a8d4', '#fbcfe8', '#fce7f3'],
    'success': ['#10b981', '#34d399', '#6ee7b7', '#a7f3d0', '#d1fae5'],
    'chart': ['#8b5cf6', '#ec4899', '#06b6d4', '#10b981', '#f59e0b', '#6366f1'],
    'gradient': ['#8b5cf6', '#a855f7', '#c026d3', '#db2777', '#ec4899']
}


# Load Data
try:
    fct_orders, dim_customers, dim_products, dim_sellers = load_data()
    data_loaded = True
except Exception as e:
    data_loaded = False
    error_message = str(e)


# Ultra Premium Hero Header
st.markdown("""
<div class="hero-container">
    <h1 class="hero-title">🛒 Olist E-commerce Analytics</h1>
    <p class="hero-subtitle">Real-time insights from 100K+ Brazilian e-commerce orders • Powered by Modern Data Stack</p>
    <div class="hero-badges">
        <span class="badge">📊 dbt Transformations</span>
        <span class="badge">🦆 MotherDuck Cloud</span>
        <span class="badge">⚡ Real-time Analytics</span>
        <span class="badge">🏗️ Dimensional Model</span>
        <span class="badge">✨ Premium Insights</span>
    </div>
</div>
""", unsafe_allow_html=True)


if not data_loaded:
    st.error(f"❌ Failed to connect to MotherDuck: {error_message}")
    st.info("💡 Ensure MOTHERDUCK_TOKEN is configured in your environment.")
    st.stop()


# Premium Sidebar
with st.sidebar:
    st.markdown("## 🎛️ Control Center")
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
        st.markdown("### 🏷️ Category Filter")
        categories = ['All Categories'] + sorted(filtered_orders['product_category_name'].dropna().unique().tolist())
        selected_category = st.selectbox("Filter by category", categories, label_visibility="collapsed")
        
        if selected_category != 'All Categories':
            filtered_orders = filtered_orders[filtered_orders['product_category_name'] == selected_category]
    
    st.markdown("---")
    
    # Live Stats Panel
    st.markdown("### 📈 Live Stats")
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(236, 72, 153, 0.15)); 
                padding: 1rem; border-radius: 0.75rem; border: 1px solid rgba(139, 92, 246, 0.3);'>
        <p style='color: #f8fafc; margin: 0.5rem 0;'><strong>📦 Orders:</strong> {len(filtered_orders):,}</p>
        <p style='color: #f8fafc; margin: 0.5rem 0;'><strong>📅 Days:</strong> {(date_range[1] - date_range[0]).days if len(date_range) == 2 else 'N/A'}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <p style='color: #64748b; font-size: 0.8rem; margin: 0;'>Crafted with ❤️ by</p>
        <p style='color: #a855f7; font-weight: 600; font-size: 0.9rem; margin: 0.25rem 0;'>Analytics Engineer</p>
    </div>
    """, unsafe_allow_html=True)


# Calculate KPIs
total_revenue = filtered_orders['total_order_value'].sum()
total_orders = filtered_orders['order_id'].nunique()
total_customers = dim_customers['customer_id'].nunique()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
total_products = dim_products['product_id'].nunique()
avg_review = dim_sellers['avg_review_score'].mean()


# Premium KPI Cards
st.markdown('<p class="section-header">📊 Key Performance Indicators</p>', unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6 = st.columns(6)

kpi_data = [
    ("💰", "Revenue", format_currency(total_revenue), "Total Sales", col1),
    ("📦", "Orders", format_number(total_orders), "Completed", col2),
    ("👥", "Customers", format_number(total_customers), "Active Users", col3),
    ("🛍️", "Avg Order", format_currency(avg_order_value), "Per Transaction", col4),
    ("📱", "Products", format_number(total_products), "In Catalog", col5),
    ("⭐", "Rating", f"{avg_review:.2f}", "Avg Score", col6),
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


# Charts Row 1 - Revenue Analytics
st.markdown('<p class="section-header">📈 Revenue Analytics</p>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    # Monthly Revenue with gradient area
    monthly_data = filtered_orders.copy()
    monthly_data['month'] = monthly_data['order_purchase_timestamp'].dt.to_period('M').astype(str)
    monthly_agg = monthly_data.groupby('month').agg({
        'total_order_value': 'sum',
        'order_id': 'nunique'
    }).reset_index()
    monthly_agg.columns = ['month', 'revenue', 'orders']
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Revenue area with gradient
    fig.add_trace(
        go.Scatter(
            x=monthly_agg['month'],
            y=monthly_agg['revenue'],
            name="Revenue",
            fill='tozeroy',
            fillcolor='rgba(139, 92, 246, 0.25)',
            line=dict(color='#a855f7', width=3, shape='spline'),
            mode='lines+markers',
            marker=dict(size=10, color='#c084fc', line=dict(width=2, color='#8b5cf6'))
        ),
        secondary_y=False
    )
    
    # Orders bars
    fig.add_trace(
        go.Bar(
            x=monthly_agg['month'],
            y=monthly_agg['orders'],
            name="Orders",
            marker=dict(
                color='rgba(236, 72, 153, 0.6)',
                line=dict(width=0)
            ),
            opacity=0.8
        ),
        secondary_y=True
    )
    
    fig.update_layout(
        title=dict(text="<b>Monthly Revenue & Order Trend</b>", font=dict(size=20, color='#f8fafc', family='Space Grotesk')),
        xaxis_title="",
        yaxis=dict(
            title="Revenue (BRL)", 
            gridcolor='rgba(255,255,255,0.08)', 
            tickfont=dict(color='#94a3b8'),
            title_font=dict(color='#94a3b8')
        ),
        yaxis2=dict(
            title="Order Count", 
            gridcolor='rgba(255,255,255,0.08)', 
            tickfont=dict(color='#94a3b8'),
            title_font=dict(color='#94a3b8')
        ),
        xaxis=dict(gridcolor='rgba(255,255,255,0.08)', tickfont=dict(color='#94a3b8')),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            font=dict(color='#f8fafc'), bgcolor='rgba(0,0,0,0)'
        ),
        height=450,
        hovermode="x unified",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=80, b=40),
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Customer Type Donut
    customer_revenue = dim_customers.groupby('customer_type')['lifetime_value'].sum().reset_index()
    
    colors_map = {'Returning': '#10b981', 'One-time': '#8b5cf6', 'No Orders': '#475569'}
    
    fig = go.Figure(data=[go.Pie(
        labels=customer_revenue['customer_type'],
        values=customer_revenue['lifetime_value'],
        hole=0.7,
        marker=dict(
            colors=[colors_map.get(x, '#8b5cf6') for x in customer_revenue['customer_type']],
            line=dict(color='#0a0a0f', width=3)
        ),
        textposition='outside',
        textinfo='percent+label',
        textfont=dict(color='#f8fafc', size=12),
        pull=[0.02, 0.02, 0.02]
    )])
    
    fig.update_layout(
        title=dict(text="<b>Customer Segments</b>", font=dict(size=20, color='#f8fafc', family='Space Grotesk')),
        showlegend=False,
        height=450,
        annotations=[dict(
            text='<b>Revenue</b><br><span style="color:#94a3b8">by Type</span>', 
            x=0.5, y=0.5, 
            font=dict(size=16, color='#f8fafc'), 
            showarrow=False
        )],
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=80, b=40),
    )
    
    st.plotly_chart(fig, use_container_width=True)


# Charts Row 2 - Top Performers
st.markdown('<p class="section-header">🏆 Top Performers</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Top Categories with gradient bars
    category_revenue = filtered_orders.groupby('product_category_name')['total_order_value'].sum().reset_index()
    category_revenue = category_revenue.nlargest(8, 'total_order_value').sort_values('total_order_value')
    
    # Create gradient colors
    n_bars = len(category_revenue)
    bar_colors = [f'rgba({139 + i*10}, {92 + i*15}, {246 - i*10}, 0.9)' for i in range(n_bars)]
    
    fig = go.Figure(go.Bar(
        x=category_revenue['total_order_value'],
        y=category_revenue['product_category_name'],
        orientation='h',
        marker=dict(
            color=bar_colors,
            line=dict(width=0),
            cornerradius=8
        ),
        text=[format_currency(x) for x in category_revenue['total_order_value']],
        textposition='outside',
        textfont=dict(size=12, color='#c7d2fe', family='Space Grotesk')
    ))
    
    fig.update_layout(
        title=dict(text="<b>Top Product Categories</b>", font=dict(size=20, color='#f8fafc', family='Space Grotesk')),
        xaxis=dict(
            title="Revenue (BRL)",
            gridcolor='rgba(255,255,255,0.08)', 
            tickfont=dict(color='#94a3b8'),
            title_font=dict(color='#94a3b8')
        ),
        yaxis=dict(tickfont=dict(color='#f8fafc', size=11)),
        height=450,
        margin=dict(l=10, r=120, t=80, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Seller Tier Chart
    seller_stats = dim_sellers.groupby('seller_tier').agg({
        'seller_id': 'count',
        'total_revenue': 'sum'
    }).reset_index()
    seller_stats.columns = ['tier', 'count', 'revenue']
    
    tier_order = ['Platinum', 'Gold', 'Silver', 'Bronze']
    seller_stats['tier'] = pd.Categorical(seller_stats['tier'], categories=tier_order, ordered=True)
    seller_stats = seller_stats.sort_values('tier')
    
    tier_colors = {
        'Platinum': 'linear-gradient(135deg, #e5e4e2, #c0c0c0)', 
        'Gold': '#fbbf24', 
        'Silver': '#94a3b8', 
        'Bronze': '#d97706'
    }
    bar_colors = [tier_colors.get(t, '#8b5cf6') for t in seller_stats['tier']]
    
    fig = go.Figure(go.Bar(
        x=seller_stats['tier'],
        y=seller_stats['count'],
        marker=dict(
            color=bar_colors,
            line=dict(color='rgba(255,255,255,0.2)', width=2),
            cornerradius=10
        ),
        text=seller_stats['count'],
        textposition='outside',
        textfont=dict(color='#f8fafc', size=14, family='Space Grotesk')
    ))
    
    fig.update_layout(
        title=dict(text="<b>Seller Performance Tiers</b>", font=dict(size=20, color='#f8fafc', family='Space Grotesk')),
        xaxis=dict(tickfont=dict(color='#f8fafc', size=12)),
        yaxis=dict(
            title="Number of Sellers",
            gridcolor='rgba(255,255,255,0.08)', 
            tickfont=dict(color='#94a3b8'),
            title_font=dict(color='#94a3b8')
        ),
        height=450,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=80, b=40),
    )
    
    st.plotly_chart(fig, use_container_width=True)


# Geographic Section
st.markdown('<p class="section-header">🗺️ Geographic Insights</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
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
            colorscale=[[0, '#6366f1'], [0.5, '#8b5cf6'], [1, '#c084fc']],
            showscale=True,
            colorbar=dict(
                title=dict(text="Revenue", font=dict(color='#94a3b8')), 
                tickfont=dict(color='#94a3b8')
            ),
            cornerradius=6
        ),
        text=state_customers['customers'],
        textposition='outside',
        textfont=dict(color='#c7d2fe', size=12)
    ))
    
    fig.update_layout(
        title=dict(text="<b>Customer Distribution by State</b>", font=dict(size=20, color='#f8fafc', family='Space Grotesk')),
        xaxis=dict(title="State", tickfont=dict(color='#f8fafc'), title_font=dict(color='#94a3b8')),
        yaxis=dict(
            title="Customers",
            gridcolor='rgba(255,255,255,0.08)', 
            tickfont=dict(color='#94a3b8'),
            title_font=dict(color='#94a3b8')
        ),
        height=420,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=80, b=40),
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    state_sellers = dim_sellers.groupby('state').agg({
        'seller_id': 'count',
        'avg_review_score': 'mean'
    }).reset_index()
    state_sellers.columns = ['state', 'sellers', 'rating']
    state_sellers = state_sellers.nlargest(10, 'sellers')
    
    fig = go.Figure(go.Bar(
        x=state_sellers['state'],
        y=state_sellers['sellers'],
        marker=dict(
            color=state_sellers['rating'],
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(
                title=dict(text="Avg Rating", font=dict(color='#94a3b8')), 
                tickfont=dict(color='#94a3b8')
            ),
            cornerradius=6
        ),
        text=state_sellers['sellers'],
        textposition='outside',
        textfont=dict(color='#c7d2fe', size=12)
    ))
    
    fig.update_layout(
        title=dict(text="<b>Seller Distribution by State</b>", font=dict(size=20, color='#f8fafc', family='Space Grotesk')),
        xaxis=dict(title="State", tickfont=dict(color='#f8fafc'), title_font=dict(color='#94a3b8')),
        yaxis=dict(
            title="Sellers",
            gridcolor='rgba(255,255,255,0.08)', 
            tickfont=dict(color='#94a3b8'),
            title_font=dict(color='#94a3b8')
        ),
        height=420,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=80, b=40),
    )
    
    st.plotly_chart(fig, use_container_width=True)


# Data Explorer
st.markdown('<p class="section-header">🔍 Data Explorer</p>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🏆 Top Products", "👥 Top Customers", "🏪 Top Sellers", "📊 Sample Data"])

with tab1:
    top_products = dim_products.nlargest(12, 'total_revenue')[
        ['product_id', 'product_category_name', 'times_sold', 'total_revenue', 'sales_tier']
    ].copy()
    top_products['total_revenue'] = top_products['total_revenue'].apply(lambda x: f"R$ {x:,.2f}")
    st.dataframe(top_products, use_container_width=True, hide_index=True)

with tab2:
    top_customers = dim_customers.nlargest(12, 'lifetime_value')[
        ['customer_unique_id', 'city', 'state', 'total_orders', 'lifetime_value', 'customer_type']
    ].copy()
    top_customers['lifetime_value'] = top_customers['lifetime_value'].apply(lambda x: f"R$ {x:,.2f}")
    st.dataframe(top_customers, use_container_width=True, hide_index=True)

with tab3:
    top_sellers = dim_sellers.nlargest(12, 'total_revenue')[
        ['seller_id', 'state', 'total_orders', 'total_revenue', 'avg_review_score', 'seller_tier']
    ].copy()
    top_sellers['total_revenue'] = top_sellers['total_revenue'].apply(lambda x: f"R$ {x:,.2f}")
    top_sellers['avg_review_score'] = top_sellers['avg_review_score'].apply(lambda x: f"{x:.2f} ⭐")
    st.dataframe(top_sellers, use_container_width=True, hide_index=True)

with tab4:
    sample = filtered_orders.head(50)[
        ['order_id', 'customer_id', 'product_category_name', 'price', 'freight_value', 'total_order_value']
    ].copy()
    sample['total_order_value'] = sample['total_order_value'].apply(lambda x: f"R$ {x:,.2f}")
    st.dataframe(sample, use_container_width=True, hide_index=True)


# Ultra Premium Footer
st.markdown("""
<div class="footer">
    <p class="footer-title">Olist E-commerce Analytics Platform</p>
    <p class="footer-subtitle">Transforming raw data into actionable insights with Modern Data Stack</p>
    <div class="tech-stack">
        <span class="tech-item">🦆 DuckDB / MotherDuck</span>
        <span class="tech-item">📊 dbt Core</span>
        <span class="tech-item">🐍 Python</span>
        <span class="tech-item">🎨 Streamlit</span>
        <span class="tech-item">📈 Plotly</span>
    </div>
    <a href="https://github.com/mohith-akash/olist-analytics-platform" target="_blank">📂 View Source Code</a>
</div>
""", unsafe_allow_html=True)
