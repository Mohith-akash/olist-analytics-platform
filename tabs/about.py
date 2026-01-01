"""
About tab component
"""

import streamlit as st


def render(fct_orders):
    """Render the About tab with project info and contact details."""
    st.markdown(
        """
    <div class="hero-header" style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);">
        <h1>👤 About This Project</h1>
        <p>Portfolio piece demonstrating modern data engineering skills</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Full-width tech stack at the top
    st.markdown(
        '<div class="section-title">🛠️ Tech Stack</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class="chart-card" style="padding: 1.5rem;">
        <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; justify-content: center;">
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

    # Tech Evolution box
    st.markdown(
        """
    <div class="chart-card" style="margin-top: 1rem; border-left: 3px solid #a855f7;">
        <div class="chart-header">📈 Tech Evolution</div>
        <p style="color: #888; margin: 0.5rem 0; font-size: 0.9rem;">
            <strong>v1.0</strong> → dbt + MotherDuck (DuckDB) &nbsp;→&nbsp; 
            <strong>v2.0</strong> → Databricks + Delta Lake (Lakehouse)
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("")  # Spacer

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(
            """
        <div class="skill-card" style="text-align: center; padding: 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">👨‍💻</div>
            <h3 style="color: white; margin: 0;">Mohith Akash</h3>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown("#### 🔗 Connect")
        st.markdown("📂 [GitHub](https://github.com/Mohith-Akash)")
        st.markdown("💼 [LinkedIn](https://www.linkedin.com/in/mohith-akash/)")

    with col2:
        st.markdown(
            '<div class="section-title">📊 About the Dataset</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <div class="chart-card">
            <div class="chart-header">Olist E-commerce Dataset</div>
            <p style="color: #888; margin: 1rem 0;">
                This is a <strong>public dataset</strong> from the Brazilian e-commerce platform Olist,
                available on <a href="https://www.kaggle.com/olistbr/brazilian-ecommerce" target="_blank" style="color: #a855f7;">Kaggle</a>.
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Dataset stats
        min_date = fct_orders["order_purchase_timestamp"].min().strftime("%b %Y")
        max_date = fct_orders["order_purchase_timestamp"].max().strftime("%b %Y")

        col_a, col_b, col_c = st.columns(3)
        col_a.metric("📅 Date Range", f"{min_date} - {max_date}")
        col_b.metric("📦 Total Orders", f"{fct_orders['order_id'].nunique():,}")
        col_c.metric("🗂️ Total Records", f"{len(fct_orders):,}")

        st.markdown(
            '<div class="section-title">🏗️ Architecture</div>', unsafe_allow_html=True
        )

        st.markdown(
            """
        <div class="chart-card">
            <div class="chart-header">Lakehouse with Medallion Architecture</div>
            <p style="color: #888; margin: 0.5rem 0;">
                Raw CSV → <strong>Databricks</strong> → Bronze (raw) → Silver (clean) → Gold (analytics) → <strong>Streamlit</strong>
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    st.markdown(
        '<div class="section-title">🎯 Skills Demonstrated</div>',
        unsafe_allow_html=True,
    )

    skill_col1, skill_col2, skill_col3 = st.columns(3)

    with skill_col1:
        st.markdown(
            """
        <div class="chart-card">
            <div class="chart-header">🔧 Data Engineering</div>
            <ul style="color: #888; margin: 1rem 0;">
                <li>Lakehouse architecture</li>
                <li>Medallion pattern (Bronze/Silver/Gold)</li>
                <li>Dimensional modeling</li>
                <li>Data quality & testing</li>
                <li>CI/CD pipelines</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with skill_col2:
        st.markdown(
            """
        <div class="chart-card">
            <div class="chart-header">📝 SQL & Transformations</div>
            <ul style="color: #888; margin: 1rem 0;">
                <li>Complex JOINs & CTEs</li>
                <li>Window functions</li>
                <li>Databricks SQL</li>
                <li>Delta Lake operations</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with skill_col3:
        st.markdown(
            """
        <div class="chart-card">
            <div class="chart-header">📊 Analytics & AI</div>
            <ul style="color: #888; margin: 1rem 0;">
                <li>Interactive dashboards</li>
                <li>KPI design</li>
                <li>Data storytelling</li>
                <li>Plotly visualizations</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Footer
    st.markdown(
        """
    <div class="footer-box">
        <h3 style="color: white; margin: 0;">🚀 Check Out My Other Projects</h3>
        <p style="color: #888; margin: 0.75rem 0;">
            GDELT News Analytics with Polars, RAG, and Gemini AI
        </p>
        <a href="https://github.com/Mohith-Akash" target="_blank" class="github-btn">
            📂 View All Projects on GitHub
        </a>
    </div>
    """,
        unsafe_allow_html=True,
    )
