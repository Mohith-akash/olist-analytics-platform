"""
🛒 Olist E-commerce Analytics Dashboard
All charts have CLEAR LABELS, axis titles, and data context
"""

import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import os

st.set_page_config(
    page_title="Olist Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean Premium Theme
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
        --blue: #3b82f6;
        --orange: #f97316;
    }
    
    * { font-family: 'Inter', sans-serif; }
    .stApp { background: var(--bg); }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 1.5rem 2rem; max-width: 100%; }
    
    /* Header */
    .header-box {
        background: linear-gradient(135deg, var(--purple), var(--pink));
        padding: 1.75rem 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
    }
    .header-box h1 { font-size: 1.75rem; font-weight: 700; color: white; margin: 0; }
    .header-box p { color: rgba(255,255,255,0.9); margin: 0.25rem 0 0 0; font-size: 0.95rem; }
    
    /* KPI Cards */
    .kpi-row { display: grid; grid-template-columns: repeat(6, 1fr); gap: 1rem; margin-bottom: 2rem; }
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
    
    /* Section Headers */
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text);
        margin: 2rem 0 1rem 0;
        padding-left: 0.75rem;
        border-left: 4px solid var(--purple);
    }
    
    /* Chart Cards */
    .chart-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    .chart-header { font-size: 1rem; font-weight: 600; color: var(--text); margin-bottom: 0.25rem; }
    .chart-desc { font-size: 0.8rem; color: var(--text-dim); margin-bottom: 1rem; line-height: 1.4; }
    
    /* Sidebar */
    section[data-testid="stSidebar"] { background: #0a0a0d; }
    section[data-testid="stSidebar"] > div { background: transparent; }
    .sidebar-title { font-size: 1rem; font-weight: 600; color: var(--text); margin-bottom: 1rem; }
    .filter-label { font-size: 0.75rem; color: var(--purple); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem; font-weight: 600; }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { background: var(--card); border-radius: 10px; padding: 4px; border: 1px solid var(--border); }
    .stTabs [data-baseweb="tab"] { border-radius: 6px; color: var(--text-dim); }
    .stTabs [aria-selected="true"] { background: var(--purple) !important; color: white !important; }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 2rem;
        border-top: 1px solid var(--border);
        background: var(--card);
        border-radius: 12px 12px 0 0;
    }
    .footer h3 { font-size: 1rem; color: var(--text); margin: 0 0 0.5rem 0; }
    .footer p { color: var(--text-dim); font-size: 0.85rem; margin: 0; }
    .tech-row { display: flex; justify-content: center; gap: 0.5rem; margin: 1rem 0; flex-wrap: wrap; }
    .tech-pill { background: var(--border); padding: 0.4rem 0.75rem; border-radius: 999px; font-size: 0.75rem; color: var(--text); }
    .github-btn { display: inline-block; background: var(--purple); padding: 0.6rem 1.5rem; border-radius: 8px; color: white; text-decoration: none; font-weight: 500; font-size: 0.85rem; }
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
    data_loaded = True
except Exception as e:
    data_loaded = False
    error_msg = str(e)


# ===== SIDEBAR WITH FILTERS =====
with st.sidebar:
    st.markdown('<div class="sidebar-title">🎛️ Filters & Controls</div>', unsafe_allow_html=True)
    
    if data_loaded:
        fct_orders['order_purchase_timestamp'] = pd.to_datetime(fct_orders['order_purchase_timestamp'])
        
        st.markdown('<div class="filter-label">📅 Select Date Range</div>', unsafe_allow_html=True)
        min_d = fct_orders['order_purchase_timestamp'].min().date()
        max_d = fct_orders['order_purchase_timestamp'].max().date()
        date_range = st.date_input("Date Range", (min_d, max_d), min_value=min_d, max_value=max_d, label_visibility="collapsed")
        st.caption(f"Data from {min_d} to {max_d}")
        
        st.markdown("---")
        
        st.markdown('<div class="filter-label">🏷️ Product Category</div>', unsafe_allow_html=True)
        cats = ['All Categories'] + sorted(fct_orders['product_category_name'].dropna().unique().tolist())
        sel_cat = st.selectbox("Category", cats, label_visibility="collapsed")
        st.caption(f"{len(cats)-1} categories available")
        
        st.markdown("---")
        
        st.markdown('<div class="filter-label">📍 Customer State</div>', unsafe_allow_html=True)
        states = ['All States'] + sorted(dim_customers['state'].dropna().unique().tolist())
        sel_state = st.selectbox("State", states, label_visibility="collapsed")
        
        st.markdown("---")
        
        st.markdown("### 📊 Quick Stats")
        st.metric("Total Products", f"{len(dim_products):,}")
        st.metric("Total Sellers", f"{len(dim_sellers):,}")
        st.metric("Avg Seller Rating", f"{dim_sellers['avg_review_score'].mean():.2f} / 5.0")


if not data_loaded:
    st.error(f"Connection Error: {error_msg}")
    st.stop()


# Apply filters
df = fct_orders.copy()
if len(date_range) == 2:
    df = df[(df['order_purchase_timestamp'].dt.date >= date_range[0]) & (df['order_purchase_timestamp'].dt.date <= date_range[1])]
if sel_cat != 'All Categories':
    df = df[df['product_category_name'] == sel_cat]


# ===== HEADER =====
st.markdown("""
<div class="header-box">
    <h1>🛒 Olist E-commerce Analytics Dashboard</h1>
    <p>Brazilian marketplace data • 100K+ orders • 2016-2018</p>
</div>
""", unsafe_allow_html=True)


# ===== KPI METRICS =====
total_rev = df['total_order_value'].sum()
total_ord = df['order_id'].nunique()
total_cust = dim_customers['customer_id'].nunique()
avg_order = total_rev / total_ord if total_ord > 0 else 0
avg_rating = dim_sellers['avg_review_score'].mean()
repeat_pct = (dim_customers['customer_type'] == 'Returning').mean() * 100

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
        <div class="kpi-desc">Unique order count</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">👥</div>
        <div class="kpi-label">Total Customers</div>
        <div class="kpi-value">{fmt_num(total_cust)}</div>
        <div class="kpi-desc">Unique customer IDs</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">🛍️</div>
        <div class="kpi-label">Avg Order Value</div>
        <div class="kpi-value">{fmt_curr(avg_order)}</div>
        <div class="kpi-desc">Revenue ÷ Orders</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">⭐</div>
        <div class="kpi-label">Avg Seller Rating</div>
        <div class="kpi-value">{avg_rating:.2f}</div>
        <div class="kpi-desc">Scale: 1-5 stars</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">🔄</div>
        <div class="kpi-label">Repeat Customers</div>
        <div class="kpi-value">{repeat_pct:.1f}%</div>
        <div class="kpi-desc">Customers with 2+ orders</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ===== CHART 1: MONTHLY REVENUE =====
st.markdown('<div class="section-title">📈 Revenue Over Time</div>', unsafe_allow_html=True)

st.markdown("""
<div class="chart-card">
    <div class="chart-header">Monthly Revenue Trend (BRL)</div>
    <div class="chart-desc">
        <strong>X-axis:</strong> Month (Year-Month format) | 
        <strong>Y-axis:</strong> Total Revenue in Brazilian Reais (R$) | 
        <strong>What it shows:</strong> How revenue changed month-over-month from 2016 to 2018
    </div>
</div>
""", unsafe_allow_html=True)

monthly = df.copy()
monthly['month'] = monthly['order_purchase_timestamp'].dt.to_period('M').astype(str)
m_agg = monthly.groupby('month').agg({'total_order_value': 'sum', 'order_id': 'nunique'}).reset_index()
m_agg.columns = ['Month', 'Revenue (R$)', 'Order Count']

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Bar(
    x=m_agg['Month'], 
    y=m_agg['Revenue (R$)'],
    name='Revenue (R$)',
    marker_color='#a855f7',
    text=[fmt_curr(x) for x in m_agg['Revenue (R$)']],
    textposition='outside',
    textfont=dict(size=9, color='#c4b5fd'),
    hovertemplate='<b>%{x}</b><br>Revenue: R$ %{y:,.0f}<extra></extra>'
), secondary_y=False)

fig.add_trace(go.Scatter(
    x=m_agg['Month'], 
    y=m_agg['Order Count'],
    name='Order Count',
    line=dict(color='#22c55e', width=3),
    mode='lines+markers',
    marker=dict(size=8),
    hovertemplate='<b>%{x}</b><br>Orders: %{y:,}<extra></extra>'
), secondary_y=True)

fig.update_layout(
    height=380,
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(title='Month', tickfont=dict(color='#9898a0'), title_font=dict(color='#9898a0')),
    yaxis=dict(title='Revenue (R$ Brazilian Reais)', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#9898a0'), title_font=dict(color='#9898a0')),
    yaxis2=dict(title='Number of Orders', tickfont=dict(color='#9898a0'), title_font=dict(color='#9898a0')),
    legend=dict(orientation='h', y=1.1, font=dict(color='#fff')),
    margin=dict(t=40, b=60),
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# ===== CHART 2: TOP CATEGORIES =====
st.markdown('<div class="section-title">🏆 Top Product Categories by Revenue</div>', unsafe_allow_html=True)

st.markdown("""
<div class="chart-card">
    <div class="chart-header">Top 10 Product Categories</div>
    <div class="chart-desc">
        <strong>X-axis:</strong> Revenue in R$ (Brazilian Reais) | 
        <strong>Y-axis:</strong> Product Category Name | 
        <strong>What it shows:</strong> Which product categories generate the most revenue
    </div>
</div>
""", unsafe_allow_html=True)

cat_data = df.groupby('product_category_name')['total_order_value'].sum().reset_index()
cat_data.columns = ['Category', 'Revenue']
cat_data = cat_data.nlargest(10, 'Revenue').sort_values('Revenue')

fig = go.Figure(go.Bar(
    x=cat_data['Revenue'],
    y=cat_data['Category'],
    orientation='h',
    marker=dict(color=cat_data['Revenue'], colorscale=[[0, '#6366f1'], [1, '#ec4899']]),
    text=[fmt_curr(x) for x in cat_data['Revenue']],
    textposition='outside',
    textfont=dict(color='#c4b5fd', size=11),
    hovertemplate='<b>%{y}</b><br>Revenue: R$ %{x:,.0f}<extra></extra>'
))

fig.update_layout(
    height=400,
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(title='Revenue (R$ Brazilian Reais)', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#9898a0'), title_font=dict(color='#9898a0')),
    yaxis=dict(title='Product Category', tickfont=dict(color='#fff', size=10), title_font=dict(color='#9898a0')),
    margin=dict(l=10, r=100, t=20, b=60)
)

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# ===== CHART 3: CUSTOMER SEGMENTS =====
st.markdown('<div class="section-title">👥 Customer Segmentation</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-header">Revenue by Customer Type</div>
        <div class="chart-desc">
            <strong>Segments:</strong> One-time (1 order), Returning (2+ orders), No Orders | 
            <strong>Values:</strong> Total lifetime revenue (R$) per segment | 
            <strong>What it shows:</strong> Which customer types contribute most to revenue
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    cust_seg = dim_customers.groupby('customer_type')['lifetime_value'].sum().reset_index()
    cust_seg.columns = ['Customer Type', 'Lifetime Revenue']
    
    fig = go.Figure(go.Pie(
        labels=cust_seg['Customer Type'],
        values=cust_seg['Lifetime Revenue'],
        hole=0.5,
        marker=dict(colors=['#a855f7', '#22c55e', '#3f3f46'], line=dict(color='#0f0f12', width=2)),
        textinfo='label+percent',
        textfont=dict(color='#fff', size=12),
        hovertemplate='<b>%{label}</b><br>Revenue: R$ %{value:,.0f}<br>Share: %{percent}<extra></extra>'
    ))
    
    fig.update_layout(
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(t=20, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col2:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-header">Customers by State (Top 10)</div>
        <div class="chart-desc">
            <strong>X-axis:</strong> Brazilian State Code (e.g., SP = São Paulo) | 
            <strong>Y-axis:</strong> Number of Customers | 
            <strong>What it shows:</strong> Geographic distribution of customers across Brazil
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    state_data = dim_customers.groupby('state').size().reset_index(name='Customer Count')
    state_data = state_data.nlargest(10, 'Customer Count')
    
    fig = go.Figure(go.Bar(
        x=state_data['state'],
        y=state_data['Customer Count'],
        marker=dict(color=state_data['Customer Count'], colorscale=[[0, '#3b82f6'], [1, '#06b6d4']]),
        text=state_data['Customer Count'],
        textposition='outside',
        textfont=dict(color='#93c5fd', size=11),
        hovertemplate='<b>State: %{x}</b><br>Customers: %{y:,}<extra></extra>'
    ))
    
    fig.update_layout(
        height=350,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title='State', tickfont=dict(color='#fff'), title_font=dict(color='#9898a0')),
        yaxis=dict(title='Number of Customers', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#9898a0'), title_font=dict(color='#9898a0')),
        margin=dict(t=20, b=60)
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# ===== CHART 4: SELLER ANALYSIS =====
st.markdown('<div class="section-title">🏪 Seller Performance Analysis</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-header">Sellers by Performance Tier</div>
        <div class="chart-desc">
            <strong>X-axis:</strong> Seller Tier (Platinum, Gold, Silver, Bronze) | 
            <strong>Y-axis:</strong> Number of Sellers | 
            <strong>Tier Logic:</strong> Based on total revenue - Platinum = top sellers, Bronze = lowest
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    tier_data = dim_sellers.groupby('seller_tier').size().reset_index(name='Seller Count')
    tier_order = ['Platinum', 'Gold', 'Silver', 'Bronze']
    tier_data['seller_tier'] = pd.Categorical(tier_data['seller_tier'], categories=tier_order, ordered=True)
    tier_data = tier_data.sort_values('seller_tier')
    colors = ['#e5e4e2', '#fbbf24', '#71717a', '#d97706']
    
    fig = go.Figure(go.Bar(
        x=tier_data['seller_tier'],
        y=tier_data['Seller Count'],
        marker_color=colors,
        text=tier_data['Seller Count'],
        textposition='outside',
        textfont=dict(color='#fff', size=12),
        hovertemplate='<b>%{x} Tier</b><br>Sellers: %{y:,}<extra></extra>'
    ))
    
    fig.update_layout(
        height=350,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title='Performance Tier', tickfont=dict(color='#fff'), title_font=dict(color='#9898a0')),
        yaxis=dict(title='Number of Sellers', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#9898a0'), title_font=dict(color='#9898a0')),
        margin=dict(t=20, b=60),
        bargap=0.4
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col2:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-header">Sellers by State (Top 10)</div>
        <div class="chart-desc">
            <strong>X-axis:</strong> Brazilian State Code | 
            <strong>Y-axis:</strong> Number of Active Sellers | 
            <strong>What it shows:</strong> Where sellers are concentrated geographically
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    seller_state = dim_sellers.groupby('state').size().reset_index(name='Seller Count')
    seller_state = seller_state.nlargest(10, 'Seller Count')
    
    fig = go.Figure(go.Bar(
        x=seller_state['state'],
        y=seller_state['Seller Count'],
        marker=dict(color=seller_state['Seller Count'], colorscale=[[0, '#22c55e'], [1, '#86efac']]),
        text=seller_state['Seller Count'],
        textposition='outside',
        textfont=dict(color='#86efac', size=11),
        hovertemplate='<b>State: %{x}</b><br>Sellers: %{y:,}<extra></extra>'
    ))
    
    fig.update_layout(
        height=350,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title='State', tickfont=dict(color='#fff'), title_font=dict(color='#9898a0')),
        yaxis=dict(title='Number of Sellers', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#9898a0'), title_font=dict(color='#9898a0')),
        margin=dict(t=20, b=60)
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# ===== DATA EXPLORER =====
st.markdown('<div class="section-title">📋 Data Explorer - Drill Down Into Details</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🏆 Top Products by Revenue", "👥 Top Customers by Lifetime Value", "🏪 Top Sellers by Revenue"])

with tab1:
    st.markdown("**Showing top 15 products ranked by total revenue generated**")
    prods = dim_products.nlargest(15, 'total_revenue')[['product_id', 'product_category_name', 'times_sold', 'total_revenue', 'sales_tier']].copy()
    prods.columns = ['Product ID', 'Category', 'Times Sold', 'Total Revenue (R$)', 'Sales Tier']
    prods['Total Revenue (R$)'] = prods['Total Revenue (R$)'].apply(lambda x: f"R$ {x:,.2f}")
    st.dataframe(prods, use_container_width=True, hide_index=True)

with tab2:
    st.markdown("**Showing top 15 customers ranked by total lifetime spending**")
    custs = dim_customers.nlargest(15, 'lifetime_value')[['customer_unique_id', 'city', 'state', 'total_orders', 'lifetime_value', 'customer_type']].copy()
    custs.columns = ['Customer ID', 'City', 'State', 'Total Orders', 'Lifetime Value (R$)', 'Customer Type']
    custs['Lifetime Value (R$)'] = custs['Lifetime Value (R$)'].apply(lambda x: f"R$ {x:,.2f}")
    st.dataframe(custs, use_container_width=True, hide_index=True)

with tab3:
    st.markdown("**Showing top 15 sellers ranked by total revenue generated**")
    sells = dim_sellers.nlargest(15, 'total_revenue')[['seller_id', 'state', 'total_orders', 'total_revenue', 'avg_review_score', 'seller_tier']].copy()
    sells.columns = ['Seller ID', 'State', 'Orders Fulfilled', 'Total Revenue (R$)', 'Avg Rating (1-5)', 'Performance Tier']
    sells['Total Revenue (R$)'] = sells['Total Revenue (R$)'].apply(lambda x: f"R$ {x:,.2f}")
    sells['Avg Rating (1-5)'] = sells['Avg Rating (1-5)'].apply(lambda x: f"{x:.2f} ⭐")
    st.dataframe(sells, use_container_width=True, hide_index=True)


# ===== FOOTER =====
st.markdown("""
<div class="footer">
    <h3>Olist E-commerce Analytics Platform</h3>
    <p>Data Pipeline: Python → MotherDuck → dbt → Streamlit</p>
    <div class="tech-row">
        <span class="tech-pill">🦆 MotherDuck</span>
        <span class="tech-pill">📊 dbt Core</span>
        <span class="tech-pill">🐍 Python</span>
        <span class="tech-pill">🎨 Streamlit</span>
        <span class="tech-pill">📈 Plotly</span>
    </div>
    <a href="https://github.com/Mohith-Akash/olist-analytics-platform" target="_blank" class="github-btn">📂 View Source on GitHub</a>
</div>
""", unsafe_allow_html=True)
