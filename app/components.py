"""
Reusable UI component helpers.
"""

import streamlit as st


def render_hero_header(title: str, subtitle: str, gradient: str = "") -> None:
    """Render a full-width hero header banner."""
    style = f' style="background: linear-gradient({gradient});"' if gradient else ""
    st.markdown(
        f'<div class="hero-header"{style}><h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )


def render_section_title(text: str) -> None:
    """Render a styled section title."""
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


def render_chart_card(header: str, desc: str = "") -> None:
    """Render a chart card header with optional description above a chart."""
    desc_html = f'<div class="chart-desc">{desc}</div>' if desc else ""
    st.markdown(
        f'<div class="chart-card"><div class="chart-header">{header}</div>{desc_html}</div>',
        unsafe_allow_html=True,
    )
