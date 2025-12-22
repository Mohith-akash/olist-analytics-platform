"""
Query Data tab component
"""

import streamlit as st
from utils import fmt_curr


def render(fct_orders, dim_products, dim_customers):
    """Render the Query Data tab with filter and download options."""
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
        
        st.dataframe(month_data.head(100), width='stretch', hide_index=True)
        
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
        
        st.dataframe(cat_data.sort_values('total_revenue', ascending=False), width='stretch', hide_index=True)
        
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
        
        st.dataframe(state_data.nlargest(100, 'lifetime_value'), width='stretch', hide_index=True)
        
        csv = state_data.to_csv(index=False)
        st.download_button(f"📥 Download {len(state_data):,} customers", csv, f"customers_{sel_state}.csv", "text/csv")
