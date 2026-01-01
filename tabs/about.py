"""
About tab component
"""

import streamlit as st


def render(fct_orders):
    """Render the About tab with project info."""
    st.markdown(
        """
    <div class="hero-header" style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);">
        <h1>👤 About This Project</h1>
        <p>Portfolio piece demonstrating modern data engineering skills</p>
    </div>
    """,
        unsafe_allow_html=True,
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
                <div><span style="color: #888;">📦</span> <strong style="color: white;">{fct_orders['order_id'].nunique():,}</strong> orders</div>
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

    # Skills section - more compact
    st.markdown("---")
    
    skill_col1, skill_col2, skill_col3 = st.columns(3)

    with skill_col1:
        st.markdown(
            """
        <div class="chart-card">
            <div class="chart-header">🔧 Data Engineering</div>
            <ul style="color: #888; margin: 0.5rem 0; padding-left: 1.2rem; font-size: 0.85rem;">
                <li>Lakehouse architecture</li>
                <li>Medallion pattern</li>
                <li>Dimensional modeling</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with skill_col2:
        st.markdown(
            """
        <div class="chart-card">
            <div class="chart-header">📝 SQL</div>
            <ul style="color: #888; margin: 0.5rem 0; padding-left: 1.2rem; font-size: 0.85rem;">
                <li>Complex JOINs & CTEs</li>
                <li>Window functions</li>
                <li>Databricks SQL</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with skill_col3:
        st.markdown(
            """
        <div class="chart-card">
            <div class="chart-header">📊 Analytics</div>
            <ul style="color: #888; margin: 0.5rem 0; padding-left: 1.2rem; font-size: 0.85rem;">
                <li>Interactive dashboards</li>
                <li>KPI design</li>
                <li>Plotly visualizations</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )
