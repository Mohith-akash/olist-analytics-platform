"""
📊 Analytics - Detailed Charts
Interactive charts with filters
"""

import streamlit as st
import duckdb
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

st.set_page_config(page_title="Analytics | Olist", page_icon="📊", layout="wide")

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
    .chart-card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 1rem; margin-bottom: 1rem; }
    .chart-header { font-size: 0.9rem; font-weight: 600; color: var(--text); }
    .chart-desc { font-size: 0.75rem; color: var(--text-dim); margin-top: 0.25rem; }
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
    dim_sellers = conn.execute("SELECT * FROM dbt_main.dim_sellers").df()
    return fct_orders, dim_customers, dim_sellers


def fmt_curr(v):
    if v >= 1e6: return f"R$ {v/1e6:.2f}M"
    if v >= 1e3: return f"R$ {v/1e3:.1f}K"
    return f"R$ {v:,.2f}"


try:
    fct_orders, dim_customers, dim_sellers = load_data()
    fct_orders['order_purchase_timestamp'] = pd.to_datetime(fct_orders['order_purchase_timestamp'])
except Exception as e:
    st.error(f"Connection Error: {e}")
    st.stop()


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
    
    st.markdown("---")
    st.markdown("### 🎛️ Filters")
    
    min_d = fct_orders['order_purchase_timestamp'].min().date()
    max_d = fct_orders['order_purchase_timestamp'].max().date()
    date_range = st.date_input("Date Range", (min_d, max_d), min_value=min_d, max_value=max_d)
    
    cats = ['All Categories'] + sorted(fct_orders['product_category_name'].dropna().unique().tolist())
    sel_cat = st.selectbox("Category", cats)


# Apply filters
df = fct_orders.copy()
if len(date_range) == 2:
    df = df[(df['order_purchase_timestamp'].dt.date >= date_range[0]) & (df['order_purchase_timestamp'].dt.date <= date_range[1])]
if sel_cat != 'All Categories':
    df = df[df['product_category_name'] == sel_cat]


st.title("📊 Analytics Dashboard")
st.markdown("Detailed charts with filters — use sidebar to filter data")


# Chart 1: Monthly Revenue
st.markdown('<div class="section-title">📈 Revenue Over Time</div>', unsafe_allow_html=True)

st.markdown("""
<div class="chart-card">
    <div class="chart-header">Monthly Revenue & Orders</div>
    <div class="chart-desc">X: Month | Y-left: Revenue (R$) | Y-right: Order Count</div>
</div>
""", unsafe_allow_html=True)

monthly = df.copy()
monthly['month'] = monthly['order_purchase_timestamp'].dt.to_period('M').astype(str)
m_agg = monthly.groupby('month').agg({'total_order_value': 'sum', 'order_id': 'nunique'}).reset_index()
m_agg.columns = ['Month', 'Revenue', 'Orders']

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Bar(x=m_agg['Month'], y=m_agg['Revenue'], name='Revenue', marker_color='#a855f7'), secondary_y=False)
fig.add_trace(go.Scatter(x=m_agg['Month'], y=m_agg['Orders'], name='Orders', line=dict(color='#22c55e', width=3), mode='lines+markers'), secondary_y=True)

fig.update_layout(
    height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(title='Month', tickfont=dict(color='#9898a0')),
    yaxis=dict(title='Revenue (R$)', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#9898a0')),
    yaxis2=dict(title='Orders', tickfont=dict(color='#9898a0')),
    legend=dict(orientation='h', y=1.1, font=dict(color='#fff')),
    margin=dict(t=40, b=60)
)
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# Chart 2: Top Categories
st.markdown('<div class="section-title">🏆 Top Categories</div>', unsafe_allow_html=True)

st.markdown("""
<div class="chart-card">
    <div class="chart-header">Top 10 Categories by Revenue</div>
    <div class="chart-desc">X: Revenue (R$) | Y: Category Name</div>
</div>
""", unsafe_allow_html=True)

cat_data = df.groupby('product_category_name')['total_order_value'].sum().nlargest(10).reset_index()
cat_data = cat_data.sort_values('total_order_value')

fig = go.Figure(go.Bar(
    x=cat_data['total_order_value'], y=cat_data['product_category_name'],
    orientation='h',
    marker=dict(color=cat_data['total_order_value'], colorscale=[[0, '#6366f1'], [1, '#ec4899']]),
    text=[fmt_curr(x) for x in cat_data['total_order_value']],
    textposition='outside', textfont=dict(color='#c4b5fd', size=10)
))

fig.update_layout(
    height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(title='Revenue (R$)', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#9898a0')),
    yaxis=dict(tickfont=dict(color='#fff', size=9)),
    margin=dict(l=10, r=80, t=10, b=60)
)
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# Charts Row
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-title">📍 Customers by State</div>', unsafe_allow_html=True)
    
    state_data = dim_customers.groupby('state').size().nlargest(10).reset_index(name='Count')
    
    fig = go.Figure(go.Bar(
        x=state_data['state'], y=state_data['Count'],
        marker=dict(color=state_data['Count'], colorscale=[[0, '#a855f7'], [1, '#ec4899']]),
        text=state_data['Count'], textposition='outside', textfont=dict(color='#c4b5fd')
    ))
    fig.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title='State', tickfont=dict(color='#fff')),
        yaxis=dict(title='Customers', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#9898a0')),
        margin=dict(t=10, b=60))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col2:
    st.markdown('<div class="section-title">⭐ Seller Tiers</div>', unsafe_allow_html=True)
    
    tier_data = dim_sellers.groupby('seller_tier').size().reset_index(name='Count')
    tier_order = ['Platinum', 'Gold', 'Silver', 'Bronze']
    tier_data['seller_tier'] = pd.Categorical(tier_data['seller_tier'], categories=tier_order, ordered=True)
    tier_data = tier_data.sort_values('seller_tier')
    colors = ['#e5e4e2', '#fbbf24', '#71717a', '#d97706']
    
    fig = go.Figure(go.Bar(
        x=tier_data['seller_tier'], y=tier_data['Count'],
        marker_color=colors, text=tier_data['Count'], textposition='outside', textfont=dict(color='#fff')
    ))
    fig.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title='Tier', tickfont=dict(color='#fff')),
        yaxis=dict(title='Sellers', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#9898a0')),
        margin=dict(t=10, b=60), bargap=0.4)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
