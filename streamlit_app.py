"""
Olist E-commerce Analytics Dashboard
Built with Streamlit + MotherDuck (DuckDB Cloud)
"""

import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Page config
st.set_page_config(
    page_title="Olist Analytics Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium look
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
    }
    .stMetric {
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 0.75rem;
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_connection():
    """Create MotherDuck connection using token from secrets or env."""
    token = os.getenv("MOTHERDUCK_TOKEN") or st.secrets.get("MOTHERDUCK_TOKEN", "")
    if token:
        return duckdb.connect(f"md:olist_analytics?motherduck_token={token}")
    else:
        # Fallback for local development with MotherDuck CLI auth
        return duckdb.connect("md:olist_analytics")


@st.cache_data(ttl=600)
def load_data():
    """Load data from MotherDuck dbt marts."""
    conn = get_connection()
    
    # Load fact and dimension tables
    fct_orders = conn.execute("SELECT * FROM dbt_main.fct_orders").df()
    dim_customers = conn.execute("SELECT * FROM dbt_main.dim_customers").df()
    dim_products = conn.execute("SELECT * FROM dbt_main.dim_products").df()
    dim_sellers = conn.execute("SELECT * FROM dbt_main.dim_sellers").df()
    
    return fct_orders, dim_customers, dim_products, dim_sellers


def format_currency(value):
    """Format value as Brazilian Real."""
    return f"R$ {value:,.2f}"


def format_number(value):
    """Format number with thousand separators."""
    return f"{value:,.0f}"


# Load data
try:
    fct_orders, dim_customers, dim_products, dim_sellers = load_data()
    data_loaded = True
except Exception as e:
    data_loaded = False
    error_message = str(e)

# Header
st.markdown('<p class="main-header">🛒 Olist E-commerce Analytics</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Brazilian E-commerce Data Warehouse • Built with dbt + MotherDuck</p>', unsafe_allow_html=True)

if not data_loaded:
    st.error(f"❌ Failed to connect to MotherDuck: {error_message}")
    st.info("Make sure MOTHERDUCK_TOKEN is set in your environment or Streamlit secrets.")
    st.stop()

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Date filter
if 'order_purchase_timestamp' in fct_orders.columns:
    fct_orders['order_purchase_timestamp'] = pd.to_datetime(fct_orders['order_purchase_timestamp'])
    min_date = fct_orders['order_purchase_timestamp'].min().date()
    max_date = fct_orders['order_purchase_timestamp'].max().date()
    
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        mask = (fct_orders['order_purchase_timestamp'].dt.date >= date_range[0]) & \
               (fct_orders['order_purchase_timestamp'].dt.date <= date_range[1])
        filtered_orders = fct_orders[mask]
    else:
        filtered_orders = fct_orders
else:
    filtered_orders = fct_orders

# Category filter
if 'product_category_name' in filtered_orders.columns:
    categories = ['All'] + sorted(filtered_orders['product_category_name'].dropna().unique().tolist())
    selected_category = st.sidebar.selectbox("Product Category", categories)
    
    if selected_category != 'All':
        filtered_orders = filtered_orders[filtered_orders['product_category_name'] == selected_category]

# KPI Metrics
st.markdown("### 📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

total_revenue = filtered_orders['total_order_value'].sum()
total_orders = filtered_orders['order_id'].nunique()
total_customers = dim_customers['customer_id'].nunique()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

with col1:
    st.metric(
        label="💰 Total Revenue",
        value=format_currency(total_revenue),
        delta="BRL"
    )

with col2:
    st.metric(
        label="📦 Total Orders",
        value=format_number(total_orders),
        delta=f"{total_orders} orders"
    )

with col3:
    st.metric(
        label="👥 Unique Customers",
        value=format_number(total_customers),
        delta="customers"
    )

with col4:
    st.metric(
        label="🛍️ Avg Order Value",
        value=format_currency(avg_order_value),
        delta="per order"
    )

st.markdown("---")

# Charts row 1
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Monthly Revenue Trend")
    
    monthly_revenue = filtered_orders.copy()
    monthly_revenue['month'] = monthly_revenue['order_purchase_timestamp'].dt.to_period('M').astype(str)
    monthly_agg = monthly_revenue.groupby('month')['total_order_value'].sum().reset_index()
    
    fig = px.line(
        monthly_agg,
        x='month',
        y='total_order_value',
        markers=True,
        color_discrete_sequence=['#667eea']
    )
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue (BRL)",
        showlegend=False,
        height=350
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 🏆 Top 10 Categories by Revenue")
    
    category_revenue = filtered_orders.groupby('product_category_name')['total_order_value'].sum().reset_index()
    category_revenue = category_revenue.nlargest(10, 'total_order_value')
    
    fig = px.bar(
        category_revenue,
        x='total_order_value',
        y='product_category_name',
        orientation='h',
        color='total_order_value',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(
        xaxis_title="Revenue (BRL)",
        yaxis_title="",
        showlegend=False,
        height=350,
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig, use_container_width=True)

# Charts row 2
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 👤 Customer Segmentation")
    
    customer_seg = dim_customers['customer_type'].value_counts().reset_index()
    customer_seg.columns = ['customer_type', 'count']
    
    fig = px.pie(
        customer_seg,
        values='count',
        names='customer_type',
        color_discrete_sequence=px.colors.qualitative.Set2,
        hole=0.4
    )
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### ⭐ Seller Tier Distribution")
    
    seller_tier = dim_sellers['seller_tier'].value_counts().reset_index()
    seller_tier.columns = ['seller_tier', 'count']
    
    # Custom colors for tiers
    tier_colors = {'Platinum': '#E5E4E2', 'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32'}
    
    fig = px.bar(
        seller_tier,
        x='seller_tier',
        y='count',
        color='seller_tier',
        color_discrete_map=tier_colors
    )
    fig.update_layout(
        xaxis_title="Seller Tier",
        yaxis_title="Count",
        showlegend=False,
        height=350
    )
    st.plotly_chart(fig, use_container_width=True)

# Data Tables
st.markdown("---")
st.markdown("### 📋 Data Explorer")

tab1, tab2, tab3 = st.tabs(["🛍️ Top Products", "👥 Top Customers", "🏪 Top Sellers"])

with tab1:
    top_products = dim_products.nlargest(10, 'total_revenue')[
        ['product_id', 'product_category_name', 'times_sold', 'total_revenue', 'sales_tier']
    ]
    st.dataframe(top_products, use_container_width=True, hide_index=True)

with tab2:
    top_customers = dim_customers.nlargest(10, 'lifetime_value')[
        ['customer_unique_id', 'city', 'state', 'total_orders', 'lifetime_value', 'customer_type']
    ]
    st.dataframe(top_customers, use_container_width=True, hide_index=True)

with tab3:
    top_sellers = dim_sellers.nlargest(10, 'total_revenue')[
        ['seller_id', 'state', 'total_orders', 'total_revenue', 'avg_review_score', 'seller_tier']
    ]
    st.dataframe(top_sellers, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #6b7280; padding: 1rem;'>
        Built with ❤️ using <b>Streamlit</b> + <b>dbt</b> + <b>MotherDuck</b> | 
        <a href='https://github.com/mohith-akash/olist-analytics-platform' target='_blank'>View on GitHub</a>
    </div>
    """,
    unsafe_allow_html=True
)
