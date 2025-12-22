"""
Olist Analytics Dashboard
Streamlit app for e-commerce data visualization
"""

import streamlit as st
import pandas as pd

from app.styles import inject_css
from app.database import load_data
from tabs import home, engineering, analytics, query, about


# Page config must be first Streamlit command
st.set_page_config(
    page_title="Olist Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Inject custom CSS
inject_css()

# Load data from MotherDuck
try:
    fct_orders, dim_customers, dim_products, dim_sellers = load_data()
    fct_orders["order_purchase_timestamp"] = pd.to_datetime(
        fct_orders["order_purchase_timestamp"]
    )
except Exception as e:
    st.error(f"Connection Error: {e}")
    st.stop()


# Tab navigation
tab_home, tab_engineering, tab_analytics, tab_query, tab_about = st.tabs(
    ["🏠 HOME", "🔧 DATA ENGINEERING", "📊 ANALYTICS", "🔍 QUERY DATA", "👤 ABOUT"]
)

# Render each tab
with tab_home:
    home.render(fct_orders, dim_customers, dim_sellers)

with tab_engineering:
    engineering.render()

with tab_analytics:
    analytics.render(fct_orders, dim_customers, dim_sellers)

with tab_query:
    query.render(fct_orders, dim_products, dim_customers)

with tab_about:
    about.render(fct_orders)
