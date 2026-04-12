"""
Home tab component
"""

import plotly.graph_objects as go
import streamlit as st

from app.components import render_chart_card, render_hero_header, render_section_title
from app.utils import fmt_curr, fmt_num


def render(fct_orders, dim_customers, dim_sellers):
    """Render the Home tab with KPIs and overview charts."""
    render_hero_header(
        "🛒 Olist E-commerce Analytics Platform",
        "Brazilian marketplace data • 100K+ orders • 2016-2018 • Powered by Databricks + Delta Lake",
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
    <div class="kpi-grid">
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
    render_section_title("💡 Key Insights from the Data")

    top_category = (
        fct_orders.groupby("product_category_name")["total_order_value"].sum().idxmax()
    )
    top_category_rev = (
        fct_orders.groupby("product_category_name")["total_order_value"].sum().max()
    )
    top_state = dim_customers["state"].value_counts().idxmax()
    top_state_pct = dim_customers["state"].value_counts().max() / len(dim_customers) * 100
    platinum_sellers = (dim_sellers["seller_tier"] == "Platinum").sum()

    insights = [
        ("#10b981", "🏆", "Top Category", top_category, f"Generated {fmt_curr(top_category_rev)} in revenue"),
        ("#3b82f6", "📍", "Top Market", f"{top_state} (São Paulo)", f"{top_state_pct:.1f}% of all customers"),
        ("#a855f7", "⭐", "Platinum Sellers", f"{platinum_sellers} sellers", "Top-tier performers with 4.5+ rating"),
    ]
    for col, (color, emoji, header, value, sub) in zip(st.columns(3), insights):
        with col:
            st.markdown(
                f'<div class="chart-card" style="border-left: 4px solid {color};">'
                f'<div style="font-size: 2rem; margin-bottom: 0.5rem;">{emoji}</div>'
                f'<div class="chart-header">{header}</div>'
                f'<p style="color: {color}; font-size: 1.1rem; font-weight: 700; margin: 0.5rem 0;">{value}</p>'
                f'<p style="color: #888; font-size: 0.85rem; margin: 0;">{sub}</p></div>',
                unsafe_allow_html=True,
            )

    # Charts Row
    render_section_title("📈 Performance Overview")

    col1, col2 = st.columns(2)

    with col1:
        render_chart_card("📈 Monthly Revenue Growth", "Revenue trend showing marketplace growth")

        monthly = fct_orders.copy()
        monthly["month"] = (
            monthly["order_purchase_timestamp"]
            .dt.tz_localize(None)
            .dt.to_period("M")
            .astype(str)
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
            xaxis=dict(tickfont=dict(color="#888", size=9), gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#888", size=9)),
            margin=dict(t=10, b=40, l=50, r=10),
        )
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    with col2:
        render_chart_card("⭐ Seller Rating Distribution", "How sellers are rated by customers")

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
        render_chart_card("🏆 Top 5 Categories", "Highest revenue product categories")

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
        render_chart_card("📍 Customer Distribution", "Top 5 states by customer count")

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
    render_section_title("🎯 Technical Skills Demonstrated")

    skill_cards = [
        ("🔧", "Data Engineering", ["Databricks", "Delta Lake"]),
        ("📝", "SQL", ["CTEs", "JOINs"]),
        ("🐍", "Python", ["Pandas", "Plotly"]),
        ("☁️", "Cloud", ["Databricks", "Delta Lake"]),
    ]
    for col, (emoji, title, tags) in zip(st.columns(4), skill_cards):
        with col:
            tags_html = "".join(f'<span class="skill-tag">{t}</span>' for t in tags)
            st.markdown(
                f'<div class="skill-card" style="text-align: center;">'
                f'<div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{emoji}</div>'
                f'<h4 style="color: white; margin: 0;">{title}</h4>'
                f'<div class="skill-tags" style="justify-content: center; margin-top: 0.75rem;">{tags_html}</div>'
                f"</div>",
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
