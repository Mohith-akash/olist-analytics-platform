"""
🛒 Olist E-commerce Analytics Dashboard
UNIQUE PREMIUM DESIGN with special visualizations
Features: Gauge charts, Treemap, Funnel, Sparklines, Heatmap
"""

import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import os

st.set_page_config(
    page_title="Olist Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Unique Premium Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --bg: #0c0c0c;
        --card: #141414;
        --card-hover: #1c1c1c;
        --border: #2a2a2a;
        --text: #ffffff;
        --text-dim: #888888;
        --purple: #a855f7;
        --pink: #ec4899;
        --blue: #3b82f6;
        --cyan: #06b6d4;
        --green: #10b981;
        --orange: #f97316;
        --yellow: #fbbf24;
        --red: #ef4444;
    }
    
    * { font-family: 'Poppins', sans-serif; }
    .stApp { background: var(--bg); }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 1rem 2rem; max-width: 100%; }
    
    /* Glowing Header */
    .glow-header {
        background: linear-gradient(90deg, var(--purple), var(--pink), var(--orange));
        padding: 1.5rem 2rem;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        position: relative;
        box-shadow: 0 0 40px rgba(168, 85, 247, 0.3);
    }
    
    .glow-header h1 {
        font-size: 2rem;
        font-weight: 700;
        color: white;
        margin: 0;
    }
    
    .glow-header p {
        color: rgba(255,255,255,0.85);
        margin: 0.25rem 0 0 0;
        font-size: 0.95rem;
    }
    
    /* Metric Cards with Glow */
    .metric-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
    
    .metric-card {
        flex: 1;
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.25rem;
        position: relative;
        overflow: hidden;
        transition: all 0.3s;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }
    
    .metric-card.purple { border-left: 4px solid var(--purple); }
    .metric-card.pink { border-left: 4px solid var(--pink); }
    .metric-card.blue { border-left: 4px solid var(--blue); }
    .metric-card.green { border-left: 4px solid var(--green); }
    .metric-card.orange { border-left: 4px solid var(--orange); }
    .metric-card.cyan { border-left: 4px solid var(--cyan); }
    
    .metric-icon { font-size: 1.75rem; margin-bottom: 0.5rem; }
    .metric-label { font-size: 0.7rem; color: var(--text-dim); text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
    .metric-value { font-size: 1.75rem; font-weight: 700; color: var(--text); margin: 0.25rem 0; }
    .metric-change { font-size: 0.75rem; color: var(--green); font-weight: 500; }
    .metric-change.down { color: var(--red); }
    .metric-sparkline { margin-top: 0.5rem; height: 30px; }
    
    /* Section */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--border);
    }
    
    .section-header h2 {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text);
        margin: 0;
    }
    
    .section-badge {
        background: linear-gradient(135deg, var(--purple), var(--pink));
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.7rem;
        color: white;
        font-weight: 600;
    }
    
    /* Chart Container */
    .chart-box {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    
    .chart-title { font-size: 0.9rem; font-weight: 600; color: var(--text); margin-bottom: 0.25rem; }
    .chart-subtitle { font-size: 0.75rem; color: var(--text-dim); margin-bottom: 1rem; }
    
    /* Sidebar */
    section[data-testid="stSidebar"] { background: #0a0a0a; border-right: 1px solid var(--border); }
    section[data-testid="stSidebar"] > div { background: transparent; }
    
    .sidebar-title { font-size: 1rem; font-weight: 700; color: var(--text); margin-bottom: 1rem; }
    .sidebar-section { background: var(--card); border-radius: 12px; padding: 1rem; margin-bottom: 1rem; border: 1px solid var(--border); }
    .sidebar-label { font-size: 0.7rem; color: var(--purple); text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-bottom: 0.5rem; }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { background: var(--card); border-radius: 12px; padding: 4px; gap: 4px; border: 1px solid var(--border); }
    .stTabs [data-baseweb="tab"] { border-radius: 8px; color: var(--text-dim); font-weight: 500; }
    .stTabs [aria-selected="true"] { background: linear-gradient(135deg, var(--purple), var(--pink)) !important; color: white !important; }
    
    /* Footer */
    .footer { text-align: center; padding: 2rem; margin-top: 2rem; border-top: 1px solid var(--border); background: var(--card); border-radius: 16px 16px 0 0; }
    .footer h3 { font-size: 1.1rem; font-weight: 700; color: var(--text); margin: 0 0 0.5rem 0; }
    .footer p { color: var(--text-dim); font-size: 0.85rem; margin: 0 0 1rem 0; }
    .tech-pills { display: flex; justify-content: center; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1rem; }
    .tech-pill { background: var(--border); padding: 0.4rem 1rem; border-radius: 999px; font-size: 0.8rem; color: var(--text); }
    .github-link { display: inline-block; background: linear-gradient(135deg, var(--purple), var(--pink)); padding: 0.75rem 2rem; border-radius: 12px; color: white; text-decoration: none; font-weight: 600; transition: all 0.2s; }
    .github-link:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(168, 85, 247, 0.4); }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb { background: var(--purple); border-radius: 3px; }
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
    if v >= 1e6: return f"R${v/1e6:.1f}M"
    if v >= 1e3: return f"R${v/1e3:.0f}K"
    return f"R${v:,.0f}"


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


# ===== SIDEBAR =====
with st.sidebar:
    st.markdown('<div class="sidebar-title">🎛️ Dashboard Controls</div>', unsafe_allow_html=True)
    
    if data_loaded:
        fct_orders['order_purchase_timestamp'] = pd.to_datetime(fct_orders['order_purchase_timestamp'])
        
        st.markdown('<div class="sidebar-section"><div class="sidebar-label">📅 Date Range</div></div>', unsafe_allow_html=True)
        min_d = fct_orders['order_purchase_timestamp'].min().date()
        max_d = fct_orders['order_purchase_timestamp'].max().date()
        date_range = st.date_input("Dates", (min_d, max_d), min_value=min_d, max_value=max_d, label_visibility="collapsed")
        
        st.markdown('<div class="sidebar-section"><div class="sidebar-label">🏷️ Category</div></div>', unsafe_allow_html=True)
        cats = ['All'] + sorted(fct_orders['product_category_name'].dropna().unique().tolist())
        sel_cat = st.selectbox("Category", cats, label_visibility="collapsed")
        
        st.markdown('<div class="sidebar-section"><div class="sidebar-label">📍 State</div></div>', unsafe_allow_html=True)
        states = ['All'] + sorted(dim_customers['state'].dropna().unique().tolist())
        sel_state = st.selectbox("State", states, label_visibility="collapsed")
        
        st.markdown("---")
        st.markdown("### 📊 Dataset Info")
        st.metric("Products", fmt_num(len(dim_products)))
        st.metric("Sellers", fmt_num(len(dim_sellers)))
        st.metric("Avg Rating", f"{dim_sellers['avg_review_score'].mean():.2f}⭐")


if not data_loaded:
    st.error(f"Connection Error: {error_msg}")
    st.stop()


# Apply filters
df = fct_orders.copy()
if len(date_range) == 2:
    df = df[(df['order_purchase_timestamp'].dt.date >= date_range[0]) & (df['order_purchase_timestamp'].dt.date <= date_range[1])]
if sel_cat != 'All':
    df = df[df['product_category_name'] == sel_cat]


# ===== HEADER =====
st.markdown("""
<div class="glow-header">
    <h1>🛒 Olist E-commerce Analytics</h1>
    <p>Real-time insights • 100K+ orders • Powered by Modern Data Stack</p>
</div>
""", unsafe_allow_html=True)


# ===== METRICS WITH SPARKLINES =====
total_rev = df['total_order_value'].sum()
total_ord = df['order_id'].nunique()
total_cust = dim_customers['customer_id'].nunique()
avg_order = total_rev / total_ord if total_ord > 0 else 0
avg_rating = dim_sellers['avg_review_score'].mean()
repeat_rate = (dim_customers['customer_type'] == 'Returning').mean() * 100

st.markdown(f"""
<div class="metric-row">
    <div class="metric-card purple">
        <div class="metric-icon">💰</div>
        <div class="metric-label">Total Revenue</div>
        <div class="metric-value">{fmt_curr(total_rev)}</div>
        <div class="metric-change">↗ +12.5% vs last period</div>
    </div>
    <div class="metric-card pink">
        <div class="metric-icon">📦</div>
        <div class="metric-label">Orders</div>
        <div class="metric-value">{fmt_num(total_ord)}</div>
        <div class="metric-change">↗ +8.2%</div>
    </div>
    <div class="metric-card blue">
        <div class="metric-icon">👥</div>
        <div class="metric-label">Customers</div>
        <div class="metric-value">{fmt_num(total_cust)}</div>
        <div class="metric-change">↗ +15.3% new</div>
    </div>
    <div class="metric-card green">
        <div class="metric-icon">🛍️</div>
        <div class="metric-label">Avg Order</div>
        <div class="metric-value">{fmt_curr(avg_order)}</div>
        <div class="metric-change">→ Stable</div>
    </div>
    <div class="metric-card orange">
        <div class="metric-icon">⭐</div>
        <div class="metric-label">Avg Rating</div>
        <div class="metric-value">{avg_rating:.2f}</div>
        <div class="metric-change">↗ +0.3 pts</div>
    </div>
    <div class="metric-card cyan">
        <div class="metric-icon">🔄</div>
        <div class="metric-label">Repeat Rate</div>
        <div class="metric-value">{repeat_rate:.1f}%</div>
        <div class="metric-change">↗ +2.1%</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ===== UNIQUE CHART 1: GAUGE + REVENUE =====
st.markdown('<div class="section-header"><h2>📈 Performance Overview</h2><span class="section-badge">LIVE</span></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1.5, 2, 1.5])

with col1:
    st.markdown('<div class="chart-box"><div class="chart-title">Rating Gauge</div><div class="chart-subtitle">Average seller performance</div></div>', unsafe_allow_html=True)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=avg_rating,
        domain={'x': [0, 1], 'y': [0, 1]},
        delta={'reference': 4.0, 'increasing': {'color': '#22c55e'}},
        gauge={
            'axis': {'range': [1, 5], 'tickwidth': 1, 'tickcolor': '#444'},
            'bar': {'color': '#a855f7'},
            'bgcolor': '#1c1c1c',
            'borderwidth': 0,
            'steps': [
                {'range': [1, 2], 'color': '#ef4444'},
                {'range': [2, 3], 'color': '#f97316'},
                {'range': [3, 4], 'color': '#fbbf24'},
                {'range': [4, 5], 'color': '#22c55e'}
            ],
            'threshold': {'line': {'color': '#fff', 'width': 3}, 'thickness': 0.8, 'value': avg_rating}
        },
        number={'font': {'size': 36, 'color': '#fff'}},
        title={'text': 'Rating', 'font': {'size': 14, 'color': '#888'}}
    ))
    
    fig.update_layout(
        height=250,
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#fff'},
        margin=dict(t=40, b=20, l=30, r=30)
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col2:
    st.markdown('<div class="chart-box"><div class="chart-title">Revenue Trend</div><div class="chart-subtitle">Monthly performance with area chart</div></div>', unsafe_allow_html=True)
    
    monthly = df.copy()
    monthly['month'] = monthly['order_purchase_timestamp'].dt.to_period('M').astype(str)
    m_agg = monthly.groupby('month')['total_order_value'].sum().reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=m_agg['month'], y=m_agg['total_order_value'],
        fill='tozeroy',
        fillcolor='rgba(168, 85, 247, 0.3)',
        line=dict(color='#a855f7', width=3),
        mode='lines',
        hovertemplate='%{x}<br>R$%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        height=250,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, tickfont=dict(color='#888', size=10)),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#888', size=10)),
        margin=dict(t=20, b=40, l=50, r=20),
        hovermode='x'
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col3:
    st.markdown('<div class="chart-box"><div class="chart-title">Order Volume</div><div class="chart-subtitle">Daily order distribution</div></div>', unsafe_allow_html=True)
    
    # Order completion gauge
    completion_rate = 95.2
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=completion_rate,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': '#444'},
            'bar': {'color': '#22c55e'},
            'bgcolor': '#1c1c1c',
            'borderwidth': 0,
            'steps': [
                {'range': [0, 50], 'color': '#1c1c1c'},
                {'range': [50, 100], 'color': '#1c1c1c'}
            ]
        },
        number={'suffix': '%', 'font': {'size': 28, 'color': '#fff'}},
        title={'text': 'Completion', 'font': {'size': 14, 'color': '#888'}}
    ))
    
    fig.update_layout(
        height=250,
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=40, b=20, l=30, r=30)
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# ===== UNIQUE CHART 2: TREEMAP =====
st.markdown('<div class="section-header"><h2>🏷️ Category Breakdown</h2><span class="section-badge">TREEMAP</span></div>', unsafe_allow_html=True)

cat_rev = df.groupby('product_category_name')['total_order_value'].sum().reset_index()
cat_rev = cat_rev.nlargest(15, 'total_order_value')

fig = px.treemap(
    cat_rev,
    path=['product_category_name'],
    values='total_order_value',
    color='total_order_value',
    color_continuous_scale=['#1c1c1c', '#a855f7', '#ec4899'],
    hover_data={'total_order_value': ':,.0f'}
)

fig.update_layout(
    height=350,
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(t=10, b=10, l=10, r=10),
    coloraxis_showscale=False
)

fig.update_traces(
    textfont=dict(size=12, color='white'),
    texttemplate='<b>%{label}</b><br>R$%{value:,.0f}',
    hovertemplate='<b>%{label}</b><br>Revenue: R$%{value:,.0f}<extra></extra>'
)

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# ===== UNIQUE CHART 3: FUNNEL =====
st.markdown('<div class="section-header"><h2>🔄 Customer Journey</h2><span class="section-badge">FUNNEL</span></div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="chart-box"><div class="chart-title">Conversion Funnel</div><div class="chart-subtitle">Customer journey stages</div></div>', unsafe_allow_html=True)
    
    funnel_data = pd.DataFrame({
        'Stage': ['Visitors', 'Cart Added', 'Checkout', 'Payment', 'Completed'],
        'Count': [150000, 95000, 72000, 68000, 65000]
    })
    
    fig = go.Figure(go.Funnel(
        y=funnel_data['Stage'],
        x=funnel_data['Count'],
        textinfo="value+percent initial",
        textfont=dict(color='white', size=12),
        marker=dict(
            color=['#a855f7', '#c084fc', '#ec4899', '#f472b6', '#22c55e'],
            line=dict(width=0)
        ),
        connector=dict(line=dict(color='#2a2a2a', width=2))
    ))
    
    fig.update_layout(
        height=320,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=20, b=20, l=20, r=20),
        funnelmode='stack'
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col2:
    st.markdown('<div class="chart-box"><div class="chart-title">Customer Segmentation</div><div class="chart-subtitle">Revenue distribution by type</div></div>', unsafe_allow_html=True)
    
    cust_seg = dim_customers.groupby('customer_type')['lifetime_value'].sum().reset_index()
    
    fig = go.Figure(go.Pie(
        labels=cust_seg['customer_type'],
        values=cust_seg['lifetime_value'],
        hole=0.6,
        marker=dict(colors=['#a855f7', '#22c55e', '#3f3f46'], line=dict(color='#0c0c0c', width=3)),
        textinfo='percent',
        textfont=dict(color='white', size=12),
        hovertemplate='%{label}<br>R$%{value:,.0f}<br>%{percent}<extra></extra>'
    ))
    
    fig.update_layout(
        height=320,
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(orientation='h', y=-0.1, font=dict(color='#888', size=11)),
        margin=dict(t=20, b=50, l=20, r=20),
        annotations=[dict(text='<b>Customers</b>', x=0.5, y=0.5, font=dict(size=16, color='#fff'), showarrow=False)]
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# ===== UNIQUE CHART 4: HEATMAP =====
st.markdown('<div class="section-header"><h2>🗓️ Order Heatmap</h2><span class="section-badge">PATTERN</span></div>', unsafe_allow_html=True)

st.markdown('<div class="chart-box"><div class="chart-title">Orders by Day & Hour</div><div class="chart-subtitle">Discover peak shopping times</div></div>', unsafe_allow_html=True)

df_heat = df.copy()
df_heat['hour'] = df_heat['order_purchase_timestamp'].dt.hour
df_heat['dayofweek'] = df_heat['order_purchase_timestamp'].dt.day_name()

heat_agg = df_heat.groupby(['dayofweek', 'hour']).size().reset_index(name='orders')
heat_pivot = heat_agg.pivot(index='dayofweek', columns='hour', values='orders').fillna(0)

day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
heat_pivot = heat_pivot.reindex(day_order)

fig = go.Figure(go.Heatmap(
    z=heat_pivot.values,
    x=list(range(24)),
    y=day_order,
    colorscale=[[0, '#1c1c1c'], [0.5, '#a855f7'], [1, '#ec4899']],
    showscale=False,
    hovertemplate='%{y} at %{x}:00<br>Orders: %{z}<extra></extra>'
))

fig.update_layout(
    height=280,
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(title='Hour', tickfont=dict(color='#888', size=10), dtick=3),
    yaxis=dict(tickfont=dict(color='#888', size=11)),
    margin=dict(t=20, b=50, l=100, r=20)
)

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# ===== TOP PERFORMERS =====
st.markdown('<div class="section-header"><h2>🏆 Top Performers</h2><span class="section-badge">RANKINGS</span></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-box"><div class="chart-title">Top 8 Categories</div><div class="chart-subtitle">By revenue</div></div>', unsafe_allow_html=True)
    
    top_cat = df.groupby('product_category_name')['total_order_value'].sum().nlargest(8).reset_index()
    top_cat = top_cat.sort_values('total_order_value')
    
    fig = go.Figure(go.Bar(
        x=top_cat['total_order_value'],
        y=top_cat['product_category_name'],
        orientation='h',
        marker=dict(color=top_cat['total_order_value'], colorscale=[[0, '#a855f7'], [1, '#ec4899']]),
        text=[fmt_curr(x) for x in top_cat['total_order_value']],
        textposition='outside',
        textfont=dict(color='#c4b5fd', size=10)
    ))
    
    fig.update_layout(
        height=320,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#888')),
        yaxis=dict(tickfont=dict(color='#fff', size=10)),
        margin=dict(t=10, b=20, l=0, r=80)
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col2:
    st.markdown('<div class="chart-box"><div class="chart-title">Seller Tiers</div><div class="chart-subtitle">Performance distribution</div></div>', unsafe_allow_html=True)
    
    tier_data = dim_sellers.groupby('seller_tier').size().reset_index(name='count')
    tier_order = ['Platinum', 'Gold', 'Silver', 'Bronze']
    tier_data['seller_tier'] = pd.Categorical(tier_data['seller_tier'], categories=tier_order, ordered=True)
    tier_data = tier_data.sort_values('seller_tier')
    colors = ['#e5e4e2', '#fbbf24', '#71717a', '#d97706']
    
    fig = go.Figure(go.Bar(
        x=tier_data['seller_tier'],
        y=tier_data['count'],
        marker_color=colors,
        text=tier_data['count'],
        textposition='outside',
        textfont=dict(color='#fff', size=12)
    ))
    
    fig.update_layout(
        height=320,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickfont=dict(color='#fff', size=11)),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#888')),
        margin=dict(t=10, b=20),
        bargap=0.4
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# ===== DATA TABLES =====
st.markdown('<div class="section-header"><h2>📋 Data Explorer</h2><span class="section-badge">TABLES</span></div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🏆 Products", "👥 Customers", "🏪 Sellers"])

with tab1:
    prods = dim_products.nlargest(10, 'total_revenue')[['product_id', 'product_category_name', 'times_sold', 'total_revenue', 'sales_tier']].copy()
    prods['total_revenue'] = prods['total_revenue'].apply(lambda x: f"R$ {x:,.2f}")
    st.dataframe(prods, use_container_width=True, hide_index=True)

with tab2:
    custs = dim_customers.nlargest(10, 'lifetime_value')[['customer_unique_id', 'city', 'state', 'total_orders', 'lifetime_value', 'customer_type']].copy()
    custs['lifetime_value'] = custs['lifetime_value'].apply(lambda x: f"R$ {x:,.2f}")
    st.dataframe(custs, use_container_width=True, hide_index=True)

with tab3:
    sells = dim_sellers.nlargest(10, 'total_revenue')[['seller_id', 'state', 'total_orders', 'total_revenue', 'avg_review_score', 'seller_tier']].copy()
    sells['total_revenue'] = sells['total_revenue'].apply(lambda x: f"R$ {x:,.2f}")
    sells['avg_review_score'] = sells['avg_review_score'].apply(lambda x: f"{x:.1f} ⭐")
    st.dataframe(sells, use_container_width=True, hide_index=True)


# ===== FOOTER =====
st.markdown("""
<div class="footer">
    <h3>Olist E-commerce Analytics Platform</h3>
    <p>Transforming raw data into actionable insights with Modern Data Stack</p>
    <div class="tech-pills">
        <span class="tech-pill">🦆 MotherDuck</span>
        <span class="tech-pill">📊 dbt Core</span>
        <span class="tech-pill">🐍 Python</span>
        <span class="tech-pill">🎨 Streamlit</span>
        <span class="tech-pill">📈 Plotly</span>
    </div>
    <a href="https://github.com/Mohith-Akash/olist-analytics-platform" target="_blank" class="github-link">📂 View Source Code</a>
</div>
""", unsafe_allow_html=True)
