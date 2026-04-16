"""
Analytics tab component
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from app.components import render_hero_header, render_section_title


def render(fct_orders, dim_customers, dim_sellers):
    """Render the Analytics tab with interactive charts."""
    render_hero_header(
        "📊 Analytics Dashboard",
        "Interactive charts with filters for deep analysis",
        "135deg, #10b981 0%, #06b6d4 50%, #3b82f6 100%",
    )

    # Filter
    col1, col2 = st.columns([1, 3])
    with col1:
        cats = ["All Categories"] + sorted(
            fct_orders["product_category_name"].dropna().unique().tolist()
        )
        sel_cat = st.selectbox("🏷️ Filter Category", cats)

    df = fct_orders.copy()
    if sel_cat != "All Categories":
        df = df[df["product_category_name"] == sel_cat]

    # Revenue Chart
    render_section_title("📈 Revenue & Orders Over Time")

    monthly = df.copy()
    monthly["month"] = (
        monthly["order_purchase_timestamp"]
        .dt.tz_localize(None)
        .dt.to_period("M")
        .astype(str)
    )
    m_agg = (
        monthly.groupby("month")
        .agg({"total_order_value": "sum", "order_id": "nunique"})
        .reset_index()
    )
    m_agg.columns = ["Month", "Revenue", "Orders"]

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            x=m_agg["Month"],
            y=m_agg["Revenue"],
            name="Revenue",
            marker=dict(
                color=m_agg["Revenue"],
                colorscale=[[0, "#6366f1"], [0.5, "#a855f7"], [1, "#8b5cf6"]],
            ),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=m_agg["Month"],
            y=m_agg["Orders"],
            name="Orders",
            line=dict(color="#22c55e", width=3),
            mode="lines+markers",
        ),
        secondary_y=True,
    )
    fig.update_layout(
        height=350,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(tickfont=dict(color="#888"), gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(
            title="Revenue (R$)",
            gridcolor="rgba(255,255,255,0.05)",
            tickfont=dict(color="#888"),
        ),
        yaxis2=dict(title="Orders", tickfont=dict(color="#888")),
        legend=dict(orientation="h", y=1.1, font=dict(color="#fff")),
        margin=dict(t=40, b=60),
    )
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    # Two charts row
    col1, col2 = st.columns(2)

    with col1:
        render_section_title("📍 Customers by State")
        filtered_customer_ids = df["customer_id"].unique()
        filtered_customers = dim_customers[
            dim_customers["customer_id"].isin(filtered_customer_ids)
        ]
        state_data = (
            filtered_customers.groupby("state")
            .size()
            .nlargest(10)
            .reset_index(name="Count")
        )

        fig = go.Figure(
            go.Bar(
                x=state_data["state"],
                y=state_data["Count"],
                marker=dict(
                    color=state_data["Count"],
                    colorscale=[[0, "#6366f1"], [1, "#8b5cf6"]],
                ),
            )
        )
        fig.update_layout(
            height=280,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(tickfont=dict(color="#fff")),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#888")),
            margin=dict(t=10, b=40),
        )
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    with col2:
        render_section_title("⭐ Seller Performance Tiers")
        # Note: Seller data shown for all categories (seller_id not in fct_orders)
        tier_data = dim_sellers.groupby("seller_tier").size().reset_index(name="Count")
        tier_order = ["Platinum", "Gold", "Silver", "Bronze"]
        tier_data["seller_tier"] = pd.Categorical(
            tier_data["seller_tier"], categories=tier_order, ordered=True
        )
        tier_data = tier_data.sort_values("seller_tier")

        fig = go.Figure(
            go.Bar(
                x=tier_data["seller_tier"],
                y=tier_data["Count"],
                marker_color=["#e5e4e2", "#fbbf24", "#71717a", "#d97706"],
            )
        )
        fig.update_layout(
            height=280,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(tickfont=dict(color="#fff")),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#888")),
            margin=dict(t=10, b=40),
            bargap=0.4,
        )
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
