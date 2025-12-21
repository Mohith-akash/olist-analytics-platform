"""
Olist Analytics Dashboard
Streamlit app for e-commerce data visualization
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

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --bg-dark: #0a0a0f;
        --bg-card: #12121a;
        --bg-card-hover: #1a1a25;
        --border: #1f1f2e;
        --text: #ffffff;
        --text-dim: #8888a0;
        --purple: #a855f7;
        --pink: #8b5cf6;
        --blue: #3b82f6;
        --cyan: #06b6d4;
        --green: #10b981;
        --orange: #f97316;
        --glow-purple: rgba(168, 85, 247, 0.4);
    }
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp { 
        background: linear-gradient(135deg, #0a0a0f 0%, #0d0d15 50%, #0a0a12 100%);
    }
    
    #MainMenu, footer, header { visibility: hidden; }
    section[data-testid="stSidebar"] { display: none; }
    .block-container { padding: 0.5rem 2rem 2rem 2rem; max-width: 100%; }
    
    /* Animated Background Particles */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(ellipse at 20% 20%, rgba(168, 85, 247, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 80%, rgba(236, 72, 153, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 50%, rgba(59, 130, 246, 0.05) 0%, transparent 60%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* Premium Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(135deg, rgba(18, 18, 26, 0.9) 0%, rgba(20, 20, 30, 0.9) 100%);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 0.5rem;
        gap: 0.5rem;
        border: 1px solid rgba(168, 85, 247, 0.2);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), 0 0 40px rgba(168, 85, 247, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        color: var(--text-dim);
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 0.5px;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.15) 0%, rgba(236, 72, 153, 0.15) 100%);
        color: var(--purple);
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #a855f7 0%, #8b5cf6 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4);
    }
    
    .stTabs [data-baseweb="tab-border"], .stTabs [data-baseweb="tab-highlight"] { display: none; }
    
    /* Hero Header */
    .hero-header {
        background: linear-gradient(135deg, #a855f7 0%, #8b5cf6 50%, #f97316 100%);
        padding: 2rem 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(168, 85, 247, 0.3);
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) rotate(45deg); }
        100% { transform: translateX(100%) rotate(45deg); }
    }
    
    .hero-header h1 {
        font-size: 2rem;
        font-weight: 800;
        color: white;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }
    
    .hero-header p {
        color: rgba(255,255,255,0.9);
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    /* Glowing KPI Cards */
    .kpi-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.25rem;
        margin-bottom: 2rem;
    }
    
    .kpi-card {
        background: linear-gradient(135deg, rgba(18, 18, 26, 0.8) 0%, rgba(25, 25, 35, 0.8) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(168, 85, 247, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #a855f7, #8b5cf6, #f97316);
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: rgba(168, 85, 247, 0.5);
        box-shadow: 0 10px 30px rgba(168, 85, 247, 0.2), 0 0 20px rgba(168, 85, 247, 0.1);
    }
    
    .kpi-icon {
        font-size: 2rem;
        margin-bottom: 0.75rem;
        filter: drop-shadow(0 0 10px rgba(168, 85, 247, 0.5));
    }
    
    .kpi-label {
        font-size: 0.7rem;
        color: var(--text-dim);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    .kpi-value {
        font-size: 1.75rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff 0%, #c4b5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0;
    }
    
    .kpi-desc {
        font-size: 0.7rem;
        color: var(--green);
        font-weight: 500;
    }
    
    /* Section Titles */
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text);
        margin: 2rem 0 1rem 0;
        padding-left: 1rem;
        border-left: 4px solid;
        border-image: linear-gradient(180deg, #a855f7, #8b5cf6) 1;
        text-shadow: 0 0 20px rgba(168, 85, 247, 0.3);
    }
    
    /* Premium Chart Cards */
    .chart-card {
        background: linear-gradient(135deg, rgba(18, 18, 26, 0.9) 0%, rgba(22, 22, 32, 0.9) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(168, 85, 247, 0.15);
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .chart-card:hover {
        border-color: rgba(168, 85, 247, 0.4);
        box-shadow: 0 5px 20px rgba(168, 85, 247, 0.15);
    }
    
    .chart-header {
        font-size: 1rem;
        font-weight: 700;
        background: linear-gradient(135deg, #fff 0%, #c4b5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .chart-desc {
        font-size: 0.75rem;
        color: var(--text-dim);
        margin-top: 0.25rem;
    }
    
    /* Skills Section */
    .skill-card {
        background: linear-gradient(135deg, rgba(18, 18, 26, 0.8) 0%, rgba(25, 25, 35, 0.8) 100%);
        border: 1px solid rgba(168, 85, 247, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        height: 100%;
    }
    
    .skill-card h4 {
        color: var(--purple);
        margin-bottom: 1rem;
    }
    
    .skill-tags {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin: 0.75rem 0;
    }
    
    .skill-tag {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.2) 0%, rgba(236, 72, 153, 0.2) 100%);
        border: 1px solid rgba(168, 85, 247, 0.4);
        padding: 0.4rem 0.8rem;
        border-radius: 999px;
        font-size: 0.75rem;
        color: #c4b5fd;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .skill-tag:hover {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.4) 0%, rgba(236, 72, 153, 0.4) 100%);
        transform: scale(1.05);
    }
    
    /* Premium Footer */
    .footer-box {
        background: linear-gradient(135deg, rgba(18, 18, 26, 0.9) 0%, rgba(22, 22, 32, 0.9) 100%);
        border: 1px solid rgba(168, 85, 247, 0.2);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin-top: 3rem;
        position: relative;
        overflow: hidden;
    }
    
    .footer-box::before {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #a855f7, #8b5cf6, #f97316);
    }
    
    .github-btn {
        display: inline-block;
        background: linear-gradient(135deg, #a855f7 0%, #8b5cf6 100%);
        padding: 0.75rem 2rem;
        border-radius: 12px;
        color: white;
        text-decoration: none;
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.3);
    }
    
    .github-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(168, 85, 247, 0.5);
    }
    
    /* Data Tables */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Metrics styling */
    [data-testid="stMetricValue"] {
        background: linear-gradient(135deg, #fff 0%, #c4b5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
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
tab_home, tab_engineering, tab_analytics, tab_query, tab_about = st.tabs([
    "🏠 HOME", 
    "🔧 DATA ENGINEERING", 
    "📊 ANALYTICS", 
    "🔍 QUERY DATA",
    "👤 ABOUT"
])


# ============================================
# TAB 1: HOME
# ============================================
with tab_home:
    st.markdown("""
    <div class="hero-header">
        <h1>🛒 Olist E-commerce Analytics Platform</h1>
        <p>Brazilian marketplace data • 100K+ orders • 2016-2018 • Powered by dbt + MotherDuck</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate all metrics
    total_rev = fct_orders['total_order_value'].sum()
    total_ord = fct_orders['order_id'].nunique()
    total_cust = dim_customers['customer_id'].nunique()
    avg_order = total_rev / total_ord if total_ord > 0 else 0
    avg_rating = dim_sellers['avg_review_score'].mean()
    total_sellers = len(dim_sellers)
    
    # 6 KPI Cards
    st.markdown(f"""
    <div style="display: grid; grid-template-columns: repeat(6, 1fr); gap: 1rem; margin-bottom: 2rem;">
        <div class="kpi-card">
            <div class="kpi-icon">💰</div>
            <div class="kpi-label">Total Revenue</div>
            <div class="kpi-value">{fmt_curr(total_rev)}</div>
            <div class="kpi-desc">2 years of sales</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">📦</div>
            <div class="kpi-label">Orders</div>
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
            <div class="kpi-label">Avg Order</div>
            <div class="kpi-value">{fmt_curr(avg_order)}</div>
            <div class="kpi-desc">Per transaction</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">⭐</div>
            <div class="kpi-label">Avg Rating</div>
            <div class="kpi-value">{avg_rating:.1f}/5</div>
            <div class="kpi-desc">Seller reviews</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">🏪</div>
            <div class="kpi-label">Sellers</div>
            <div class="kpi-value">{fmt_num(total_sellers)}</div>
            <div class="kpi-desc">Active sellers</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Insights Section
    st.markdown('<div class="section-title">💡 Key Insights from the Data</div>', unsafe_allow_html=True)
    
    # Calculate insights
    top_category = fct_orders.groupby('product_category_name')['total_order_value'].sum().idxmax()
    top_category_rev = fct_orders.groupby('product_category_name')['total_order_value'].sum().max()
    top_state = dim_customers['state'].value_counts().idxmax()
    top_state_pct = (dim_customers['state'].value_counts().max() / len(dim_customers) * 100)
    platinum_sellers = (dim_sellers['seller_tier'] == 'Platinum').sum()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="chart-card" style="border-left: 4px solid #10b981;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🏆</div>
            <div class="chart-header">Top Category</div>
            <p style="color: #10b981; font-size: 1.1rem; font-weight: 700; margin: 0.5rem 0;">{top_category}</p>
            <p style="color: #888; font-size: 0.85rem; margin: 0;">Generated {fmt_curr(top_category_rev)} in revenue</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="chart-card" style="border-left: 4px solid #3b82f6;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📍</div>
            <div class="chart-header">Top Market</div>
            <p style="color: #3b82f6; font-size: 1.1rem; font-weight: 700; margin: 0.5rem 0;">{top_state} (São Paulo)</p>
            <p style="color: #888; font-size: 0.85rem; margin: 0;">{top_state_pct:.1f}% of all customers</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="chart-card" style="border-left: 4px solid #a855f7;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">⭐</div>
            <div class="chart-header">Platinum Sellers</div>
            <p style="color: #a855f7; font-size: 1.1rem; font-weight: 700; margin: 0.5rem 0;">{platinum_sellers} sellers</p>
            <p style="color: #888; font-size: 0.85rem; margin: 0;">Top-tier performers with 4.5+ rating</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts Row
    st.markdown('<div class="section-title">📈 Performance Overview</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-header">📈 Monthly Revenue Growth</div>
            <div class="chart-desc">Revenue trend showing marketplace growth</div>
        </div>
        """, unsafe_allow_html=True)
        
        monthly = fct_orders.copy()
        monthly['month'] = monthly['order_purchase_timestamp'].dt.to_period('M').astype(str)
        m_agg = monthly.groupby('month')['total_order_value'].sum().reset_index()
        
        fig = go.Figure(go.Scatter(
            x=m_agg['month'], y=m_agg['total_order_value'],
            mode='lines+markers',
            fill='tozeroy',
            line=dict(color='#a855f7', width=3),
            fillcolor='rgba(168, 85, 247, 0.2)',
            marker=dict(size=6, color='#a855f7')
        ))
        fig.update_layout(
            height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickfont=dict(color='#888', size=9), gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#888', size=9)),
            margin=dict(t=10, b=40, l=50, r=10)
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-header">⭐ Seller Rating Distribution</div>
            <div class="chart-desc">How sellers are rated by customers</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Gauge chart for average rating
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_rating,
            number={'suffix': '/5', 'font': {'size': 40, 'color': '#fff'}},
            gauge={
                'axis': {'range': [0, 5], 'tickcolor': '#888', 'tickfont': {'color': '#888'}},
                'bar': {'color': '#a855f7'},
                'bgcolor': '#1a1a24',
                'bordercolor': '#2a2a34',
                'steps': [
                    {'range': [0, 2], 'color': 'rgba(239, 68, 68, 0.3)'},
                    {'range': [2, 3.5], 'color': 'rgba(245, 158, 11, 0.3)'},
                    {'range': [3.5, 5], 'color': 'rgba(16, 185, 129, 0.3)'}
                ],
                'threshold': {
                    'line': {'color': '#10b981', 'width': 4},
                    'thickness': 0.8,
                    'value': avg_rating
                }
            }
        ))
        fig.update_layout(
            height=300, paper_bgcolor='rgba(0,0,0,0)',
            font={'color': '#fff'},
            margin=dict(t=30, b=20, l=30, r=30)
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Second row of charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-header">🏆 Top 5 Categories</div>
            <div class="chart-desc">Highest revenue product categories</div>
        </div>
        """, unsafe_allow_html=True)
        
        cat_data = fct_orders.groupby('product_category_name')['total_order_value'].sum().nlargest(5).reset_index()
        cat_data = cat_data.sort_values('total_order_value')
        
        fig = go.Figure(go.Bar(
            x=cat_data['total_order_value'], y=cat_data['product_category_name'],
            orientation='h',
            marker=dict(
                color=['#3b82f6', '#6366f1', '#8b5cf6', '#a855f7', '#c084fc'],
                line=dict(width=0)
            ),
            text=[fmt_curr(x) for x in cat_data['total_order_value']],
            textposition='outside',
            textfont=dict(color='#c4b5fd', size=10)
        ))
        fig.update_layout(
            height=250, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(tickfont=dict(color='#fff', size=9)),
            margin=dict(t=10, b=10, l=10, r=80)
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-header">📍 Customer Distribution</div>
            <div class="chart-desc">Top 5 states by customer count</div>
        </div>
        """, unsafe_allow_html=True)
        
        state_data = dim_customers['state'].value_counts().head(5).reset_index()
        state_data.columns = ['State', 'Count']
        
        fig = go.Figure(go.Pie(
            labels=state_data['State'],
            values=state_data['Count'],
            hole=0.6,
            marker=dict(
                colors=['#a855f7', '#8b5cf6', '#6366f1', '#4f46e5', '#4338ca'],
                line=dict(color='#0a0a0f', width=2)
            ),
            textinfo='label+percent',
            textfont=dict(color='#fff', size=11)
        ))
        fig.update_layout(
            height=250, paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            margin=dict(t=10, b=10, l=10, r=10)
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Skills Section
    st.markdown('<div class="section-title">🎯 Technical Skills Demonstrated</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="skill-card" style="text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔧</div>
            <h4 style="color: white; margin: 0;">Data Engineering</h4>
            <div class="skill-tags" style="justify-content: center; margin-top: 0.75rem;">
                <span class="skill-tag">dbt</span>
                <span class="skill-tag">ETL</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="skill-card" style="text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📝</div>
            <h4 style="color: white; margin: 0;">SQL</h4>
            <div class="skill-tags" style="justify-content: center; margin-top: 0.75rem;">
                <span class="skill-tag">CTEs</span>
                <span class="skill-tag">JOINs</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="skill-card" style="text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🐍</div>
            <h4 style="color: white; margin: 0;">Python</h4>
            <div class="skill-tags" style="justify-content: center; margin-top: 0.75rem;">
                <span class="skill-tag">Pandas</span>
                <span class="skill-tag">Plotly</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="skill-card" style="text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">☁️</div>
            <h4 style="color: white; margin: 0;">Cloud</h4>
            <div class="skill-tags" style="justify-content: center; margin-top: 0.75rem;">
                <span class="skill-tag">MotherDuck</span>
                <span class="skill-tag">DuckDB</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer-box">
        <h3 style="color: white; margin: 0; font-size: 1.25rem;">🚀 Explore the Full Project</h3>
        <p style="color: #888; margin: 0.75rem 0;">Check out the Data Engineering tab to see the SQL code, or Query Data to explore the dataset</p>
        <a href="https://github.com/Mohith-Akash/olist-analytics-platform" target="_blank" class="github-btn">
            📂 View Source Code on GitHub
        </a>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# TAB 2: DATA ENGINEERING
# ============================================
with tab_engineering:
    st.markdown("""
    <div class="hero-header" style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);">
        <h1>🔧 Data Engineering</h1>
        <p>SQL transformations, dbt models, and dimensional modeling</p>
    </div>
    """, unsafe_allow_html=True)
    
    eng_tab1, eng_tab2, eng_tab3 = st.tabs(["📐 Architecture", "📝 fct_orders.sql", "📝 dim_customers.sql"])
    
    with eng_tab1:
        st.markdown('<div class="section-title">📐 Data Model Architecture</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="chart-card">
        <p>This project uses <strong>Kimball dimensional modeling</strong> with a 3-layer dbt architecture:</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="skill-card">
                <h4>📥 Sources</h4>
                <p style="color: #888;">Raw CSV data from Olist</p>
                <div class="skill-tags">
                    <span class="skill-tag">9 tables</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="skill-card">
                <h4>🔄 Staging</h4>
                <p style="color: #888;">Cleaned & typed data</p>
                <div class="skill-tags">
                    <span class="skill-tag">stg_orders</span>
                    <span class="skill-tag">stg_customers</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="skill-card">
                <h4>📊 Marts</h4>
                <p style="color: #888;">Business-ready analytics</p>
                <div class="skill-tags">
                    <span class="skill-tag">fct_orders</span>
                    <span class="skill-tag">dim_customers</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### 🛠️ SQL Skills Demonstrated")
        st.markdown("""
        <div class="skill-tags">
            <span class="skill-tag">CTEs</span>
            <span class="skill-tag">LEFT JOINs</span>
            <span class="skill-tag">Aggregations</span>
            <span class="skill-tag">CASE statements</span>
            <span class="skill-tag">Window functions</span>
            <span class="skill-tag">COALESCE</span>
            <span class="skill-tag">dbt ref()</span>
            <span class="skill-tag">Materializations</span>
        </div>
        """, unsafe_allow_html=True)
    
    with eng_tab2:
        st.markdown('<div class="section-title">📝 fct_orders.sql - Fact Table</div>', unsafe_allow_html=True)
        st.markdown("*Multi-table JOIN with calculated `total_order_value`*")
        
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
        st.markdown('<div class="section-title">📝 dim_customers.sql - Customer Dimension</div>', unsafe_allow_html=True)
        st.markdown("*LTV calculation, aggregations, and CASE-based segmentation*")
        
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
    st.markdown("""
    <div class="hero-header" style="background: linear-gradient(135deg, #10b981 0%, #06b6d4 50%, #3b82f6 100%);">
        <h1>📊 Analytics Dashboard</h1>
        <p>Interactive charts with filters for deep analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter
    col1, col2 = st.columns([1, 3])
    with col1:
        cats = ['All Categories'] + sorted(fct_orders['product_category_name'].dropna().unique().tolist())
        sel_cat = st.selectbox("🏷️ Filter Category", cats)
    
    df = fct_orders.copy()
    if sel_cat != 'All Categories':
        df = df[df['product_category_name'] == sel_cat]
    
    # Revenue Chart
    st.markdown('<div class="section-title">📈 Revenue & Orders Over Time</div>', unsafe_allow_html=True)
    
    monthly = df.copy()
    monthly['month'] = monthly['order_purchase_timestamp'].dt.to_period('M').astype(str)
    m_agg = monthly.groupby('month').agg({'total_order_value': 'sum', 'order_id': 'nunique'}).reset_index()
    m_agg.columns = ['Month', 'Revenue', 'Orders']
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=m_agg['Month'], y=m_agg['Revenue'], name='Revenue',
        marker=dict(color=m_agg['Revenue'], colorscale=[[0, '#6366f1'], [0.5, '#a855f7'], [1, '#8b5cf6']])
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=m_agg['Month'], y=m_agg['Orders'], name='Orders',
        line=dict(color='#22c55e', width=3), mode='lines+markers'
    ), secondary_y=True)
    
    fig.update_layout(
        height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickfont=dict(color='#888'), gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(title='Revenue (R$)', gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#888')),
        yaxis2=dict(title='Orders', tickfont=dict(color='#888')),
        legend=dict(orientation='h', y=1.1, font=dict(color='#fff')),
        margin=dict(t=40, b=60)
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Two charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-title">📍 Customers by State</div>', unsafe_allow_html=True)
        state_data = dim_customers.groupby('state').size().nlargest(10).reset_index(name='Count')
        
        fig = go.Figure(go.Bar(
            x=state_data['state'], y=state_data['Count'],
            marker=dict(color=state_data['Count'], colorscale=[[0, '#6366f1'], [1, '#8b5cf6']])
        ))
        fig.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickfont=dict(color='#fff')),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#888')),
            margin=dict(t=10, b=40))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        st.markdown('<div class="section-title">⭐ Seller Performance Tiers</div>', unsafe_allow_html=True)
        tier_data = dim_sellers.groupby('seller_tier').size().reset_index(name='Count')
        tier_order = ['Platinum', 'Gold', 'Silver', 'Bronze']
        tier_data['seller_tier'] = pd.Categorical(tier_data['seller_tier'], categories=tier_order, ordered=True)
        tier_data = tier_data.sort_values('seller_tier')
        
        fig = go.Figure(go.Bar(
            x=tier_data['seller_tier'], y=tier_data['Count'],
            marker_color=['#e5e4e2', '#fbbf24', '#71717a', '#d97706']
        ))
        fig.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickfont=dict(color='#fff')),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#888')),
            margin=dict(t=10, b=40), bargap=0.4)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# ============================================
# TAB 4: QUERY DATA
# ============================================
with tab_query:
    st.markdown("""
    <div class="hero-header" style="background: linear-gradient(135deg, #f97316 0%, #f59e0b 50%, #eab308 100%);">
        <h1>🔍 Query Data</h1>
        <p>Filter specific data and download as CSV</p>
    </div>
    """, unsafe_allow_html=True)
    
    query_tab1, query_tab2, query_tab3 = st.tabs(["📅 Orders", "🏷️ Products", "👥 Customers"])
    
    with query_tab1:
        st.markdown('<div class="section-title">📅 Orders by Month</div>', unsafe_allow_html=True)
        
        fct_orders['month'] = fct_orders['order_purchase_timestamp'].dt.to_period('M').astype(str)
        months = sorted(fct_orders['month'].unique().tolist())
        sel_month = st.selectbox("Select Month", months, index=len(months)-1)
        
        month_data = fct_orders[fct_orders['month'] == sel_month][
            ['order_id', 'customer_id', 'product_category_name', 'price', 'total_order_value']
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
        st.download_button(f"📥 Download {len(cat_data):,} products", csv, "products.csv", "text/csv")
    
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


# ============================================
# TAB 5: ABOUT
# ============================================
with tab_about:
    st.markdown("""
    <div class="hero-header" style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);">
        <h1>👤 About This Project</h1>
        <p>Portfolio piece demonstrating data engineering skills</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div class="skill-card" style="text-align: center; padding: 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">👨‍💻</div>
            <h3 style="color: white; margin: 0;">Mohith Akash</h3>
            <p style="color: #a855f7; margin: 0.5rem 0;">Data Engineer</p>
            <div class="skill-tags" style="justify-content: center; margin-top: 1rem;">
                <span class="skill-tag">Python</span>
                <span class="skill-tag">SQL</span>
                <span class="skill-tag">dbt</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("#### 🔗 Connect")
        st.markdown("📂 [GitHub](https://github.com/Mohith-Akash)")
        st.markdown("💼 [LinkedIn](https://www.linkedin.com/in/mohith-akash/)")
    
    with col2:
        st.markdown('<div class="section-title">📊 About the Dataset</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="chart-card">
            <div class="chart-header">Olist E-commerce Dataset</div>
            <p style="color: #888; margin: 1rem 0;">
                This is a <strong>public dataset</strong> from the Brazilian e-commerce platform Olist, 
                available on <a href="https://www.kaggle.com/olistbr/brazilian-ecommerce" target="_blank" style="color: #a855f7;">Kaggle</a>.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Dataset stats
        min_date = fct_orders['order_purchase_timestamp'].min().strftime('%b %Y')
        max_date = fct_orders['order_purchase_timestamp'].max().strftime('%b %Y')
        
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("📅 Date Range", f"{min_date} - {max_date}")
        col_b.metric("📦 Total Orders", f"{fct_orders['order_id'].nunique():,}")
        col_c.metric("🗂️ Total Records", f"{len(fct_orders):,}")
        
        st.markdown('<div class="section-title">🏗️ Architecture</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="chart-card">
            <div class="chart-header">End-to-End Data Pipeline</div>
            <p style="color: #888; margin: 0.5rem 0;">
                Raw CSV files → Python ingestion → MotherDuck (Cloud DuckDB) → dbt transformations → Streamlit dashboard
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tech stack
        st.markdown("#### 🛠️ Technologies Used")
        
        tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4)
        
        with tech_col1:
            st.markdown("""
            <div class="skill-card" style="text-align: center;">
                <div style="font-size: 2rem;">🦆</div>
                <p style="color: white; font-weight: 600; margin: 0.5rem 0;">MotherDuck</p>
                <p style="color: #888; font-size: 0.75rem; margin: 0;">Cloud Data Warehouse</p>
            </div>
            """, unsafe_allow_html=True)
        
        with tech_col2:
            st.markdown("""
            <div class="skill-card" style="text-align: center;">
                <div style="font-size: 2rem;">📊</div>
                <p style="color: white; font-weight: 600; margin: 0.5rem 0;">dbt Core</p>
                <p style="color: #888; font-size: 0.75rem; margin: 0;">SQL Transformations</p>
            </div>
            """, unsafe_allow_html=True)
        
        with tech_col3:
            st.markdown("""
            <div class="skill-card" style="text-align: center;">
                <div style="font-size: 2rem;">🐍</div>
                <p style="color: white; font-weight: 600; margin: 0.5rem 0;">Python</p>
                <p style="color: #888; font-size: 0.75rem; margin: 0;">Data Processing</p>
            </div>
            """, unsafe_allow_html=True)
        
        with tech_col4:
            st.markdown("""
            <div class="skill-card" style="text-align: center;">
                <div style="font-size: 2rem;">🎨</div>
                <p style="color: white; font-weight: 600; margin: 0.5rem 0;">Streamlit</p>
                <p style="color: #888; font-size: 0.75rem; margin: 0;">Dashboard</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<div class="section-title">🎯 Skills Demonstrated</div>', unsafe_allow_html=True)
    
    skill_col1, skill_col2, skill_col3 = st.columns(3)
    
    with skill_col1:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-header">🔧 Data Engineering</div>
            <ul style="color: #888; margin: 1rem 0;">
                <li>ETL/ELT pipelines</li>
                <li>Dimensional modeling (Kimball)</li>
                <li>Data quality testing</li>
                <li>Cloud data warehousing</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with skill_col2:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-header">📝 SQL & dbt</div>
            <ul style="color: #888; margin: 1rem 0;">
                <li>Complex JOINs & CTEs</li>
                <li>Aggregate functions</li>
                <li>CASE statements</li>
                <li>dbt models & tests</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with skill_col3:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-header">📊 Analytics & Viz</div>
            <ul style="color: #888; margin: 1rem 0;">
                <li>KPI design</li>
                <li>Interactive dashboards</li>
                <li>Data storytelling</li>
                <li>Plotly visualizations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer-box">
        <h3 style="color: white; margin: 0;">🚀 Ready to Collaborate?</h3>
        <p style="color: #888; margin: 0.75rem 0;">
            Open to Data Engineering, Analytics Engineering, and Data Analyst roles
        </p>
        <a href="https://github.com/Mohith-Akash/olist-analytics-platform" target="_blank" class="github-btn">
            📂 View Full Source Code
        </a>
    </div>
    """, unsafe_allow_html=True)
