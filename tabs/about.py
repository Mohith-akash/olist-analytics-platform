"""
About tab component
"""

import streamlit as st

from app.components import render_hero_header


def render(fct_orders):
    """Render the About tab with project info."""
    render_hero_header(
        "👤 About This Project",
        "Portfolio piece demonstrating modern data engineering skills",
        "135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%",
    )

    # Compact layout - everything in columns
    col1, col2 = st.columns(2)

    with col1:
        # Dataset info
        min_date = fct_orders["order_purchase_timestamp"].min().strftime("%b %Y")
        max_date = fct_orders["order_purchase_timestamp"].max().strftime("%b %Y")

        st.markdown(
            f"""
        <div class="chart-card">
            <div class="chart-header">📊 Olist E-commerce Dataset</div>
            <p style="color: #888; margin: 0.5rem 0; font-size: 0.9rem;">
                Public dataset from Brazilian marketplace Olist
                (<a href="https://www.kaggle.com/olistbr/brazilian-ecommerce" target="_blank" style="color: #a855f7;">Kaggle</a>)
            </p>
            <div style="display: flex; gap: 1.5rem; margin-top: 0.75rem;">
                <div><span style="color: #888;">📅</span> <strong style="color: white;">{min_date} - {max_date}</strong></div>
                <div><span style="color: #888;">📦</span> <strong style="color: white;">{fct_orders["order_id"].nunique():,}</strong> orders</div>
                <div><span style="color: #888;">🗂️</span> <strong style="color: white;">{len(fct_orders):,}</strong> records</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Tech Stack
        st.markdown(
            """
        <div class="chart-card" style="margin-top: 1rem;">
            <div class="chart-header">🛠️ Tech Stack</div>
            <div style="display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.5rem;">
                <span class="skill-tag">Databricks</span>
                <span class="skill-tag">Delta Lake</span>
                <span class="skill-tag">Python</span>
                <span class="skill-tag">SQL</span>
                <span class="skill-tag">Streamlit</span>
                <span class="skill-tag">GitHub Actions</span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        # Architecture
        st.markdown(
            """
        <div class="chart-card">
            <div class="chart-header">🏗️ Lakehouse Architecture</div>
            <p style="color: #888; margin: 0.5rem 0; font-size: 0.9rem;">
                Raw CSV → <strong style="color: #a855f7;">Databricks</strong> → Bronze → Silver → Gold → <strong style="color: #a855f7;">Streamlit</strong>
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Tech Evolution
        st.markdown(
            """
        <div class="chart-card" style="margin-top: 1rem;">
            <div class="chart-header">📈 Tech Evolution</div>
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-top: 0.5rem;">
                <div style="text-align: center; padding: 0.5rem 0.75rem; background: rgba(255,255,255,0.05); border-radius: 6px;">
                    <div style="color: #FFC107; font-weight: 600; font-size: 0.8rem;">v1.0</div>
                    <div style="color: #888; font-size: 0.7rem;">dbt + MotherDuck</div>
                </div>
                <div style="color: #a855f7;">→</div>
                <div style="text-align: center; padding: 0.5rem 0.75rem; background: rgba(168, 85, 247, 0.15); border-radius: 6px; border: 1px solid rgba(168, 85, 247, 0.3);">
                    <div style="color: #a855f7; font-weight: 600; font-size: 0.8rem;">v2.0</div>
                    <div style="color: #fff; font-size: 0.7rem;">Databricks + Delta Lake</div>
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Connect links
        st.markdown(
            """
        <div class="chart-card" style="margin-top: 1rem;">
            <div class="chart-header">🔗 Connect</div>
            <div style="display: flex; gap: 1rem; margin-top: 0.5rem;">
                <a href="https://github.com/Mohith-Akash" target="_blank" style="color: #a855f7; text-decoration: none;">📂 GitHub</a>
                <a href="https://www.linkedin.com/in/mohith-akash/" target="_blank" style="color: #a855f7; text-decoration: none;">💼 LinkedIn</a>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Skills section
    st.markdown("---")

    skill_data = [
        (
            "🔧 Data Engineering",
            ["Lakehouse architecture", "Medallion pattern", "Dimensional modeling"],
        ),
        ("📝 SQL", ["Complex JOINs & CTEs", "Window functions", "Databricks SQL"]),
        (
            "📊 Analytics",
            ["Interactive dashboards", "KPI design", "Plotly visualizations"],
        ),
    ]
    for col, (header, items) in zip(st.columns(3), skill_data):
        with col:
            items_html = "".join(f"<li>{i}</li>" for i in items)
            st.markdown(
                f'<div class="chart-card"><div class="chart-header">{header}</div>'
                f'<ul style="color: #888; margin: 0.5rem 0; padding-left: 1.2rem; font-size: 0.85rem;">'
                f"{items_html}</ul></div>",
                unsafe_allow_html=True,
            )
