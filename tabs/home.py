"""
Home tab component
"""

import streamlit as st
import plotly.graph_objects as go
from app.utils import fmt_curr, fmt_num


def render(fct_orders, dim_customers, dim_sellers):
    """Render the Home tab with KPIs and overview charts."""
    st.markdown(
        """
    <div class="hero-header">
        <h1>🛒 Olist E-commerce Analytics Platform</h1>
        <p>Brazilian marketplace data • 100K+ orders • 2016-2018 • Powered by dbt + MotherDuck</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Calculate metrics
    total_rev = fct_orders["total_order_value"].sum()
    total_ord = fct_orders["order_id"].nunique()
    total_cust = dim_customers["customer_id"].nunique()
    avg_order = total_rev / total_ord if total_ord > 0 else 0
    avg_rating = dim_sellers["avg_review_score"].mean()
    total_sellers = len(dim_sellers)

    # 6 KPI Cards
    st.markdown(
        f"""
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
    """,
        unsafe_allow_html=True,
    )

    # Key Insights Section
    st.markdown(
        '<div class="section-title">💡 Key Insights from the Data</div>',
        unsafe_allow_html=True,
    )

    top_category = (
        fct_orders.groupby("product_category_name")["total_order_value"].sum().idxmax()
    )
    top_category_rev = (
        fct_orders.groupby("product_category_name")["total_order_value"].sum().max()
    )
    top_state = dim_customers["state"].value_counts().idxmax()
    top_state_pct = (
        dim_customers["state"].value_counts().max() / len(dim_customers) * 100
    )
    platinum_sellers = (dim_sellers["seller_tier"] == "Platinum").sum()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
        <div class="chart-card" style="border-left: 4px solid #10b981;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🏆</div>
            <div class="chart-header">Top Category</div>
            <p style="color: #10b981; font-size: 1.1rem; font-weight: 700; margin: 0.5rem 0;">{top_category}</p>
            <p style="color: #888; font-size: 0.85rem; margin: 0;">Generated {fmt_curr(top_category_rev)} in revenue</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div class="chart-card" style="border-left: 4px solid #3b82f6;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📍</div>
            <div class="chart-header">Top Market</div>
            <p style="color: #3b82f6; font-size: 1.1rem; font-weight: 700; margin: 0.5rem 0;">{top_state} (São Paulo)</p>
            <p style="color: #888; font-size: 0.85rem; margin: 0;">{top_state_pct:.1f}% of all customers</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
        <div class="chart-card" style="border-left: 4px solid #a855f7;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">⭐</div>
            <div class="chart-header">Platinum Sellers</div>
            <p style="color: #a855f7; font-size: 1.1rem; font-weight: 700; margin: 0.5rem 0;">{platinum_sellers} sellers</p>
            <p style="color: #888; font-size: 0.85rem; margin: 0;">Top-tier performers with 4.5+ rating</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Charts Row
    st.markdown(
        '<div class="section-title">📈 Performance Overview</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        <div class="chart-card">
            <div class="chart-header">📈 Monthly Revenue Growth</div>
            <div class="chart-desc">Revenue trend showing marketplace growth</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        monthly = fct_orders.copy()
        monthly["month"] = (
            monthly["order_purchase_timestamp"].dt.to_period("M").astype(str)
        )
        m_agg = monthly.groupby("month")["total_order_value"].sum().reset_index()

        fig = go.Figure(
            go.Scatter(
                x=m_agg["month"],
                y=m_agg["total_order_value"],
                mode="lines+markers",
                fill="tozeroy",
                line=dict(color="#a855f7", width=3),
                fillcolor="rgba(168, 85, 247, 0.2)",
                marker=dict(size=6, color="#a855f7"),
            )
        )
        fig.update_layout(
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                tickfont=dict(color="#888", size=9), gridcolor="rgba(255,255,255,0.05)"
            ),
            yaxis=dict(
                gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#888", size=9)
            ),
            margin=dict(t=10, b=40, l=50, r=10),
        )
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    with col2:
        st.markdown(
            """
        <div class="chart-card">
            <div class="chart-header">⭐ Seller Rating Distribution</div>
            <div class="chart-desc">How sellers are rated by customers</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=avg_rating,
                number={"suffix": "/5", "font": {"size": 40, "color": "#fff"}},
                gauge={
                    "axis": {
                        "range": [0, 5],
                        "tickcolor": "#888",
                        "tickfont": {"color": "#888"},
                    },
                    "bar": {"color": "#a855f7"},
                    "bgcolor": "#1a1a24",
                    "bordercolor": "#2a2a34",
                    "steps": [
                        {"range": [0, 2], "color": "rgba(239, 68, 68, 0.3)"},
                        {"range": [2, 3.5], "color": "rgba(245, 158, 11, 0.3)"},
                        {"range": [3.5, 5], "color": "rgba(16, 185, 129, 0.3)"},
                    ],
                    "threshold": {
                        "line": {"color": "#10b981", "width": 4},
                        "thickness": 0.8,
                        "value": avg_rating,
                    },
                },
            )
        )
        fig.update_layout(
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
            font={"color": "#fff"},
            margin=dict(t=30, b=20, l=30, r=30),
        )
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    # Second row of charts
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        <div class="chart-card">
            <div class="chart-header">🏆 Top 5 Categories</div>
            <div class="chart-desc">Highest revenue product categories</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        cat_data = (
            fct_orders.groupby("product_category_name")["total_order_value"]
            .sum()
            .nlargest(5)
            .reset_index()
        )
        cat_data = cat_data.sort_values("total_order_value")

        fig = go.Figure(
            go.Bar(
                x=cat_data["total_order_value"],
                y=cat_data["product_category_name"],
                orientation="h",
                marker=dict(
                    color=["#3b82f6", "#6366f1", "#8b5cf6", "#a855f7", "#c084fc"],
                    line=dict(width=0),
                ),
                text=[fmt_curr(x) for x in cat_data["total_order_value"]],
                textposition="outside",
                textfont=dict(color="#c4b5fd", size=10),
            )
        )
        fig.update_layout(
            height=250,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(tickfont=dict(color="#fff", size=9)),
            margin=dict(t=10, b=10, l=10, r=80),
        )
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    with col2:
        st.markdown(
            """
        <div class="chart-card">
            <div class="chart-header">📍 Customer Distribution</div>
            <div class="chart-desc">Top 5 states by customer count</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        state_data = dim_customers["state"].value_counts().head(5).reset_index()
        state_data.columns = ["State", "Count"]

        fig = go.Figure(
            go.Pie(
                labels=state_data["State"],
                values=state_data["Count"],
                hole=0.6,
                marker=dict(
                    colors=["#a855f7", "#8b5cf6", "#6366f1", "#4f46e5", "#4338ca"],
                    line=dict(color="#0a0a0f", width=2),
                ),
                textinfo="label+percent",
                textfont=dict(color="#fff", size=11),
            )
        )
        fig.update_layout(
            height=250,
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            margin=dict(t=10, b=10, l=10, r=10),
        )
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    # Skills Section
    st.markdown(
        '<div class="section-title">🎯 Technical Skills Demonstrated</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            """
        <div class="skill-card" style="text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔧</div>
            <h4 style="color: white; margin: 0;">Data Engineering</h4>
            <div class="skill-tags" style="justify-content: center; margin-top: 0.75rem;">
                <span class="skill-tag">dbt</span>
                <span class="skill-tag">ETL</span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="skill-card" style="text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📝</div>
            <h4 style="color: white; margin: 0;">SQL</h4>
            <div class="skill-tags" style="justify-content: center; margin-top: 0.75rem;">
                <span class="skill-tag">CTEs</span>
                <span class="skill-tag">JOINs</span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
        <div class="skill-card" style="text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🐍</div>
            <h4 style="color: white; margin: 0;">Python</h4>
            <div class="skill-tags" style="justify-content: center; margin-top: 0.75rem;">
                <span class="skill-tag">Pandas</span>
                <span class="skill-tag">Plotly</span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            """
        <div class="skill-card" style="text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">☁️</div>
            <h4 style="color: white; margin: 0;">Cloud</h4>
            <div class="skill-tags" style="justify-content: center; margin-top: 0.75rem;">
                <span class="skill-tag">MotherDuck</span>
                <span class="skill-tag">DuckDB</span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Footer
    st.markdown(
        """
    <div class="footer-box">
        <h3 style="color: white; margin: 0; font-size: 1.25rem;">🚀 Explore the Full Project</h3>
        <p style="color: #888; margin: 0.75rem 0;">Check out the Data Engineering tab to see the SQL code, or Query Data to explore the dataset</p>
        <a href="https://github.com/Mohith-Akash/olist-analytics-platform" target="_blank" class="github-btn">
            📂 View Source Code on GitHub
        </a>
    </div>
    """,
        unsafe_allow_html=True,
    )
