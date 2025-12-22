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
        <p>Portfolio piece demonstrating data engineering skills</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(
            """
        <div class="skill-card" style="text-align: center; padding: 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">👨‍💻</div>
            <h3 style="color: white; margin: 0;">Mohith Akash</h3>
            <p style="color: #a855f7; margin: 0.5rem 0;">Data Engineer</p>
            <div class="skill-tags" style="justify-content: center; margin-top: 1rem;">
                <span class="skill-tag">Python</span>
                <span class="skill-tag">SQL</span>
                <span class="skill-tag">dbt</span>
            </div>
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
            <div class="chart-header">End-to-End Data Pipeline</div>
            <p style="color: #888; margin: 0.5rem 0;">
                Raw CSV files → Python ingestion → MotherDuck (Cloud DuckDB) → dbt transformations → Streamlit dashboard
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Tech stack
        st.markdown("#### 🛠️ Technologies Used")

        tech_col1, tech_col2, tech_col3, tech_col4, tech_col5 = st.columns(5)

        with tech_col1:
            st.markdown(
                """
            <div class="skill-card" style="text-align: center;">
                <div style="font-size: 2rem;">🦆</div>
                <p style="color: white; font-weight: 600; margin: 0.5rem 0;">MotherDuck</p>
                <p style="color: #888; font-size: 0.75rem; margin: 0;">Cloud Data Warehouse</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with tech_col2:
            st.markdown(
                """
            <div class="skill-card" style="text-align: center;">
                <div style="font-size: 2rem;">📊</div>
                <p style="color: white; font-weight: 600; margin: 0.5rem 0;">dbt Core</p>
                <p style="color: #888; font-size: 0.75rem; margin: 0;">SQL Transformations</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with tech_col3:
            st.markdown(
                """
            <div class="skill-card" style="text-align: center;">
                <div style="font-size: 2rem;">🐍</div>
                <p style="color: white; font-weight: 600; margin: 0.5rem 0;">Python</p>
                <p style="color: #888; font-size: 0.75rem; margin: 0;">Data Processing</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with tech_col4:
            st.markdown(
                """
            <div class="skill-card" style="text-align: center;">
                <div style="font-size: 2rem;">🎨</div>
                <p style="color: white; font-weight: 600; margin: 0.5rem 0;">Streamlit</p>
                <p style="color: #888; font-size: 0.75rem; margin: 0;">Dashboard</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with tech_col5:
            st.markdown(
                """
            <div class="skill-card" style="text-align: center;">
                <div style="font-size: 2rem;">⚙️</div>
                <p style="color: white; font-weight: 600; margin: 0.5rem 0;">GitHub Actions</p>
                <p style="color: #888; font-size: 0.75rem; margin: 0;">CI/CD Pipeline</p>
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
                <li>ETL/ELT pipelines</li>
                <li>Dimensional modeling (Kimball)</li>
                <li>Data quality testing</li>
                <li>Cloud data warehousing</li>
                <li>CI/CD with GitHub Actions</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with skill_col2:
        st.markdown(
            """
        <div class="chart-card">
            <div class="chart-header">📝 SQL & dbt</div>
            <ul style="color: #888; margin: 1rem 0;">
                <li>Complex JOINs & CTEs</li>
                <li>Aggregate functions</li>
                <li>CASE statements</li>
                <li>dbt models & tests</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with skill_col3:
        st.markdown(
            """
        <div class="chart-card">
            <div class="chart-header">📊 Analytics & Viz</div>
            <ul style="color: #888; margin: 1rem 0;">
                <li>KPI design</li>
                <li>Interactive dashboards</li>
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
        <h3 style="color: white; margin: 0;">🚀 Ready to Collaborate?</h3>
        <p style="color: #888; margin: 0.75rem 0;">
            Open to Data Engineering, Analytics Engineering, and Data Analyst roles
        </p>
        <p style="color: #666; font-size: 0.85rem; margin: 0.5rem 0;">
            Check out my other projects featuring Dagster, RAG, Gemini AI, and more on GitHub
        </p>
        <a href="https://github.com/Mohith-Akash/olist-analytics-platform" target="_blank" class="github-btn">
            📂 View Full Source Code
        </a>
    </div>
    """,
        unsafe_allow_html=True,
    )
