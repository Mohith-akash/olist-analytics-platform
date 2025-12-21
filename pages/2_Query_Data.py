"""
🔍 Query Data - Interactive Data Query
Search and download specific data
"""

import streamlit as st
import duckdb
import pandas as pd
import os

st.set_page_config(page_title="Query Data | Olist", page_icon="🔍", layout="wide")

# Theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    :root { --bg: #0f0f12; --card: #1a1a1f; --border: #2a2a30; --text: #ffffff; --text-dim: #9898a0; --purple: #a855f7; }
    * { font-family: 'Inter', sans-serif; }
    .stApp { background: var(--bg); }
    #MainMenu, footer, header { visibility: hidden; }
    .section-title { font-size: 1.1rem; font-weight: 600; color: var(--text); margin: 1.5rem 0 1rem 0; padding-left: 0.75rem; border-left: 4px solid var(--purple); }
    .info-box { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem; }
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


try:
    fct_orders, dim_customers, dim_products, dim_sellers = load_data()
    fct_orders['order_purchase_timestamp'] = pd.to_datetime(fct_orders['order_purchase_timestamp'])
except Exception as e:
    st.error(f"Connection Error: {e}")
    st.stop()


st.title("🔍 Query Data")
st.markdown("Select filters to get specific data and download as CSV")

tab1, tab2, tab3, tab4 = st.tabs(["📅 Orders by Month", "🏷️ Products by Category", "📍 Customers by State", "🏪 Top Sellers"])


# Tab 1: Orders by Month
with tab1:
    st.markdown('<div class="section-title">📅 Get Orders for a Specific Month</div>', unsafe_allow_html=True)
    
    fct_orders['month'] = fct_orders['order_purchase_timestamp'].dt.to_period('M').astype(str)
    available_months = sorted(fct_orders['month'].unique().tolist())
    
    selected_month = st.selectbox("Select Month", available_months, index=len(available_months)-1)
    
    month_data = fct_orders[fct_orders['month'] == selected_month][
        ['order_id', 'customer_id', 'product_category_name', 'price', 'freight_value', 'total_order_value', 'order_purchase_timestamp']
    ].copy()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Orders", f"{month_data['order_id'].nunique():,}")
    col2.metric("Revenue", fmt_curr(month_data['total_order_value'].sum()))
    col3.metric("Avg Order", fmt_curr(month_data['total_order_value'].mean()))
    
    st.markdown(f"**First 100 orders from {selected_month}:**")
    display = month_data.head(100).copy()
    display['total_order_value'] = display['total_order_value'].apply(lambda x: f"R$ {x:.2f}")
    st.dataframe(display, use_container_width=True, hide_index=True)
    
    csv = month_data.to_csv(index=False)
    st.download_button(f"📥 Download {len(month_data):,} orders as CSV", csv, f"orders_{selected_month}.csv", "text/csv")


# Tab 2: Products by Category
with tab2:
    st.markdown('<div class="section-title">🏷️ Get Products by Category</div>', unsafe_allow_html=True)
    
    categories = sorted(dim_products['product_category_name'].dropna().unique().tolist())
    selected_cat = st.selectbox("Select Category", categories)
    
    cat_products = dim_products[dim_products['product_category_name'] == selected_cat][
        ['product_id', 'product_category_name', 'times_sold', 'total_revenue', 'sales_tier']
    ].copy()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Products", f"{len(cat_products):,}")
    col2.metric("Total Revenue", fmt_curr(cat_products['total_revenue'].sum()))
    col3.metric("Units Sold", f"{cat_products['times_sold'].sum():,}")
    
    st.markdown(f"**All products in '{selected_cat}':**")
    display = cat_products.copy()
    display['total_revenue'] = display['total_revenue'].apply(lambda x: f"R$ {x:.2f}")
    st.dataframe(display.sort_values('total_revenue', ascending=False), use_container_width=True, hide_index=True)
    
    csv = cat_products.to_csv(index=False)
    st.download_button(f"📥 Download {len(cat_products):,} products as CSV", csv, f"products_{selected_cat.replace(' ', '_')}.csv", "text/csv")


# Tab 3: Customers by State
with tab3:
    st.markdown('<div class="section-title">📍 Get Customers by State</div>', unsafe_allow_html=True)
    
    states = sorted(dim_customers['state'].dropna().unique().tolist())
    selected_state = st.selectbox("Select State", states)
    
    state_customers = dim_customers[dim_customers['state'] == selected_state][
        ['customer_unique_id', 'city', 'state', 'total_orders', 'lifetime_value', 'customer_type']
    ].copy()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Customers", f"{len(state_customers):,}")
    col2.metric("Total LTV", fmt_curr(state_customers['lifetime_value'].sum()))
    col3.metric("Avg Orders", f"{state_customers['total_orders'].mean():.2f}")
    
    st.markdown(f"**Top 100 customers in {selected_state}:**")
    display = state_customers.nlargest(100, 'lifetime_value').copy()
    display['lifetime_value'] = display['lifetime_value'].apply(lambda x: f"R$ {x:.2f}")
    st.dataframe(display, use_container_width=True, hide_index=True)
    
    csv = state_customers.to_csv(index=False)
    st.download_button(f"📥 Download {len(state_customers):,} customers as CSV", csv, f"customers_{selected_state}.csv", "text/csv")


# Tab 4: Top Sellers
with tab4:
    st.markdown('<div class="section-title">🏪 Top Sellers</div>', unsafe_allow_html=True)
    
    top_n = st.slider("Number of sellers to show", 10, 100, 25)
    
    sellers = dim_sellers.nlargest(top_n, 'total_revenue')[
        ['seller_id', 'state', 'total_orders', 'total_revenue', 'avg_review_score', 'seller_tier']
    ].copy()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Sellers Shown", f"{len(sellers):,}")
    col2.metric("Combined Revenue", fmt_curr(sellers['total_revenue'].sum()))
    col3.metric("Avg Rating", f"{sellers['avg_review_score'].mean():.2f} ⭐")
    
    display = sellers.copy()
    display['total_revenue'] = display['total_revenue'].apply(lambda x: f"R$ {x:.2f}")
    display['avg_review_score'] = display['avg_review_score'].apply(lambda x: f"{x:.2f} ⭐")
    st.dataframe(display, use_container_width=True, hide_index=True)
    
    csv = sellers.to_csv(index=False)
    st.download_button(f"📥 Download top {len(sellers)} sellers as CSV", csv, "top_sellers.csv", "text/csv")
