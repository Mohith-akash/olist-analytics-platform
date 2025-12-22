"""
CSS styling for the Olist Analytics Dashboard
"""

import streamlit as st


def inject_css():
    """Inject custom CSS styling into the Streamlit app."""
    st.markdown(
        """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    :root {
        --bg-dark: #0a0a0f;
        --bg-card: #12121a;
        --bg-card-hover: #1a1a25;
        --border: #1f1f2e;
        --text: #ffffff;
        --text-dim: #8888a0;
        --purple: #a855f7;
        --pink: #8b5cf6;
        --blue: #3b82f6;
        --cyan: #06b6d4;
        --green: #10b981;
        --orange: #f97316;
        --glow-purple: rgba(168, 85, 247, 0.4);
    }

    * { font-family: 'Inter', sans-serif; }

    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #0d0d15 50%, #0a0a12 100%);
    }

    #MainMenu, footer, header { visibility: hidden; }
    section[data-testid="stSidebar"] { display: none; }
    .block-container { padding: 0.5rem 2rem 2rem 2rem; max-width: 100%; }

    /* Animated Background Particles */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background:
            radial-gradient(ellipse at 20% 20%, rgba(168, 85, 247, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 80%, rgba(236, 72, 153, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 50%, rgba(59, 130, 246, 0.05) 0%, transparent 60%);
        pointer-events: none;
        z-index: 0;
    }

    /* Premium Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(135deg, rgba(18, 18, 26, 0.9) 0%, rgba(20, 20, 30, 0.9) 100%);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 0.5rem;
        gap: 0.5rem;
        border: 1px solid rgba(168, 85, 247, 0.2);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), 0 0 40px rgba(168, 85, 247, 0.1);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        color: var(--text-dim);
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 0.5px;
        border: none;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.15) 0%, rgba(236, 72, 153, 0.15) 100%);
        color: var(--purple);
        transform: translateY(-2px);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #a855f7 0%, #8b5cf6 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4);
    }

    .stTabs [data-baseweb="tab-border"], .stTabs [data-baseweb="tab-highlight"] { display: none; }

    /* Hero Header */
    .hero-header {
        background: linear-gradient(135deg, #a855f7 0%, #8b5cf6 50%, #f97316 100%);
        padding: 2rem 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(168, 85, 247, 0.3);
    }

    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        animation: shimmer 3s infinite;
    }

    @keyframes shimmer {
        0% { transform: translateX(-100%) rotate(45deg); }
        100% { transform: translateX(100%) rotate(45deg); }
    }

    .hero-header h1 {
        font-size: 2rem;
        font-weight: 800;
        color: white;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }

    .hero-header p {
        color: rgba(255,255,255,0.9);
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }

    /* Glowing KPI Cards */
    .kpi-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.25rem;
        margin-bottom: 2rem;
    }

    .kpi-card {
        background: linear-gradient(135deg, rgba(18, 18, 26, 0.8) 0%, rgba(25, 25, 35, 0.8) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(168, 85, 247, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }

    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #a855f7, #8b5cf6, #f97316);
    }

    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: rgba(168, 85, 247, 0.5);
        box-shadow: 0 10px 30px rgba(168, 85, 247, 0.2), 0 0 20px rgba(168, 85, 247, 0.1);
    }

    .kpi-icon {
        font-size: 2rem;
        margin-bottom: 0.75rem;
        filter: drop-shadow(0 0 10px rgba(168, 85, 247, 0.5));
    }

    .kpi-label {
        font-size: 0.7rem;
        color: var(--text-dim);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }

    .kpi-value {
        font-size: 1.75rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff 0%, #c4b5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0;
    }

    .kpi-desc {
        font-size: 0.7rem;
        color: var(--green);
        font-weight: 500;
    }

    /* Section Titles */
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text);
        margin: 2rem 0 1rem 0;
        padding-left: 1rem;
        border-left: 4px solid;
        border-image: linear-gradient(180deg, #a855f7, #8b5cf6) 1;
        text-shadow: 0 0 20px rgba(168, 85, 247, 0.3);
    }

    /* Premium Chart Cards */
    .chart-card {
        background: linear-gradient(135deg, rgba(18, 18, 26, 0.9) 0%, rgba(22, 22, 32, 0.9) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(168, 85, 247, 0.15);
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }

    .chart-card:hover {
        border-color: rgba(168, 85, 247, 0.4);
        box-shadow: 0 5px 20px rgba(168, 85, 247, 0.15);
    }

    .chart-header {
        font-size: 1rem;
        font-weight: 700;
        background: linear-gradient(135deg, #fff 0%, #c4b5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .chart-desc {
        font-size: 0.75rem;
        color: var(--text-dim);
        margin-top: 0.25rem;
    }

    /* Skills Section */
    .skill-card {
        background: linear-gradient(135deg, rgba(18, 18, 26, 0.8) 0%, rgba(25, 25, 35, 0.8) 100%);
        border: 1px solid rgba(168, 85, 247, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        height: 100%;
    }

    .skill-card h4 {
        color: var(--purple);
        margin-bottom: 1rem;
    }

    .skill-tags {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin: 0.75rem 0;
    }

    .skill-tag {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.2) 0%, rgba(236, 72, 153, 0.2) 100%);
        border: 1px solid rgba(168, 85, 247, 0.4);
        padding: 0.4rem 0.8rem;
        border-radius: 999px;
        font-size: 0.75rem;
        color: #c4b5fd;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    .skill-tag:hover {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.4) 0%, rgba(236, 72, 153, 0.4) 100%);
        transform: scale(1.05);
    }

    /* Premium Footer */
    .footer-box {
        background: linear-gradient(135deg, rgba(18, 18, 26, 0.9) 0%, rgba(22, 22, 32, 0.9) 100%);
        border: 1px solid rgba(168, 85, 247, 0.2);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin-top: 3rem;
        position: relative;
        overflow: hidden;
    }

    .footer-box::before {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #a855f7, #8b5cf6, #f97316);
    }

    .github-btn {
        display: inline-block;
        background: linear-gradient(135deg, #a855f7 0%, #8b5cf6 100%);
        padding: 0.75rem 2rem;
        border-radius: 12px;
        color: white;
        text-decoration: none;
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.3);
    }

    .github-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(168, 85, 247, 0.5);
    }

    /* Data Tables */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Metrics styling */
    [data-testid="stMetricValue"] {
        background: linear-gradient(135deg, #fff 0%, #c4b5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* ==================== MOBILE RESPONSIVENESS ==================== */

    /* Tablet breakpoint */
    @media (max-width: 992px) {
        .kpi-row {
            grid-template-columns: repeat(3, 1fr);
        }

        .hero-header {
            padding: 1.5rem;
        }

        .hero-header h1 {
            font-size: 1.5rem;
        }

        .stTabs [data-baseweb="tab"] {
            padding: 0.6rem 1rem;
            font-size: 0.75rem;
        }
    }

    /* Mobile breakpoint */
    @media (max-width: 768px) {
        .block-container {
            padding: 0.5rem 1rem 2rem 1rem;
        }

        .kpi-row {
            grid-template-columns: repeat(2, 1fr);
            gap: 0.75rem;
        }

        .kpi-card {
            padding: 1rem;
        }

        .kpi-value {
            font-size: 1.4rem;
        }

        .kpi-label {
            font-size: 0.6rem;
        }

        .hero-header {
            padding: 1.25rem;
            border-radius: 12px;
            margin-bottom: 1rem;
        }

        .hero-header h1 {
            font-size: 1.25rem;
        }

        .hero-header p {
            font-size: 0.85rem;
        }

        .section-title {
            font-size: 0.95rem;
            margin: 1.5rem 0 0.75rem 0;
        }

        .stTabs [data-baseweb="tab-list"] {
            border-radius: 10px;
            padding: 0.25rem;
            overflow-x: auto;
            flex-wrap: nowrap;
        }

        .stTabs [data-baseweb="tab"] {
            padding: 0.5rem 0.75rem;
            font-size: 0.7rem;
            white-space: nowrap;
        }

        .skill-card {
            padding: 1rem;
        }

        .chart-card {
            padding: 1rem;
        }

        .footer-box {
            padding: 1.5rem 1rem;
        }
    }

    /* Small phone breakpoint */
    @media (max-width: 480px) {
        .kpi-row {
            grid-template-columns: 1fr;
        }

        .kpi-value {
            font-size: 1.5rem;
        }

        .hero-header h1 {
            font-size: 1.1rem;
        }
    }
</style>
""",
        unsafe_allow_html=True,
    )
