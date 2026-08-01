"""
style.py — Shared visual theme for the Stolen Strata dashboard.

Palette: "Loess Noir" — deep navy-black base, wine-maroon accent, antique gold
highlight, cream text. Chosen to echo the project's subject matter: a dark,
ancient sediment (the karewa loess) cut through with the maroon of exposed,
disturbed earth and the gold of saffron.

Import and call inject_css() at the top of every page (including app.py) so
styling stays consistent across the whole multi-page app.
"""

import streamlit as st
import os

# ---- Palette -----------------------------------------------------------
BG_PRIMARY   = "#0A0E1A"   # near-black navy — app background
BG_PANEL     = "#111827"   # panel / sidebar background
BG_CARD      = "#1A2236"   # card background
MAROON       = "#8B1E3F"   # primary accent — wine/maroon
MAROON_LIGHT = "#B33A5C"   # hover / lighter accent
GOLD         = "#D4AF37"   # secondary accent — antique gold (saffron nod)
TEAL         = "#2EC4B6"   # tertiary accent for charts
CREAM        = "#F5F1E8"   # primary text on dark background
MUTED        = "#9AA5B8"   # secondary / muted text

CHART_SEQUENCE = [MAROON, GOLD, TEAL, MAROON_LIGHT, "#5C6B8A", "#E8C468"]

def inject_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800;900&family=Inter:wght@400;500;600&display=swap');

        html, body, .stApp {{
            background-color: {BG_PRIMARY} !important;
            color: {CREAM} !important;
            font-family: 'Inter', sans-serif;
        }}

        .block-container,
        [data-testid="stAppViewBlockContainer"] {{
            padding-top: 1.5rem !important;
        }}

        /* ---- Sidebar collapse/expand button — safety net covering every
        naming variant Streamlit has used across versions. The button exists
        by default, but on a dark theme like this one it renders low-contrast
        (near-invisible) and can fail to show on mobile without this. ---- */
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapsedControl"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid="baseButton-header"],
        [data-testid="stHeader"] button,
        [data-testid*="ollapse" i],
        button[kind="header"] {{
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            z-index: 999999 !important;
        }}
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapsedControl"] {{
            position: fixed !important;
            top: 12px !important;
            left: 12px !important;
            background: {BG_PANEL} !important;
            border: 1.5px solid {MAROON} !important;
            border-radius: 8px !important;
            padding: 4px !important;
        }}
        [data-testid="collapsedControl"] svg,
        [data-testid="stSidebarCollapsedControl"] svg,
        [data-testid="stSidebarCollapseButton"] svg,
        [data-testid="baseButton-header"] svg,
        [data-testid="stHeader"] button svg,
        button[kind="header"] svg {{
            fill: {GOLD} !important;
            stroke: {GOLD} !important;
            opacity: 1 !important;
        }}

        h1, h2, h3, h4, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 800 !important;
            color: {CREAM} !important;
            letter-spacing: 0.3px;
        }}

        .ss-page-title-wrap {{
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
            padding: 0.5rem 0 0.8rem 0;
        }}
        .ss-page-title {{
            font-family: 'Montserrat', sans-serif;
            font-size: 3.2rem;
            font-weight: 900;
            color: {CREAM};
            border-bottom: 4px solid {MAROON};
            padding-bottom: 0.5rem;
            margin-bottom: 0.2rem;
            display: inline-block;
            text-align: center;
        }}

        .ss-hero-title {{
            font-family: 'Montserrat', sans-serif;
            font-size: 4.2rem;
            font-weight: 900;
            color: {CREAM};
            margin-bottom: 0;
            display: inline-block;
        }}

        .ss-page-subtitle {{
            font-family: 'Montserrat', sans-serif;
            color: {GOLD};
            font-weight: 700;
            font-size: 1.3rem;
            margin-top: 0.6rem;
            text-align: center;
        }}

        h2 {{ color: {GOLD} !important; }}

        p, li, span, label, .stMarkdown, div[data-testid="stMarkdownContainer"] {{
            color: {CREAM} !important;
            font-size: 1.02rem;
        }}

        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background-color: {BG_PANEL} !important;
            border-right: 2px solid {MAROON};
        }}
        section[data-testid="stSidebar"] * {{
            color: {CREAM} !important;
        }}
        section[data-testid="stSidebar"] *:not([data-testid="stIconMaterial"]):not(svg):not(path) {{
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
        }}

        /* Metrics */
        div[data-testid="stMetric"] {{
            background-color: {BG_CARD};
            border: 1px solid {MAROON};
            border-radius: 10px;
            padding: 1rem 1rem 0.6rem 1rem;
            box-shadow: 0 0 14px rgba(139, 30, 63, 0.25);
        }}
        div[data-testid="stMetricValue"] {{
            color: {GOLD} !important;
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 900 !important;
            font-size: 2rem !important;
        }}
        div[data-testid="stMetricLabel"] {{
            color: {MUTED} !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            font-size: 0.8rem !important;
        }}

        /* Cards / containers via horizontal rule + custom div class */
        .ss-card {{
            background: linear-gradient(145deg, {BG_CARD}, {BG_PANEL});
            border-left: 5px solid {MAROON};
            border-radius: 10px;
            padding: 1.2rem 1.5rem;
            margin-bottom: 1.2rem;
            box-shadow: 0 4px 18px rgba(0,0,0,0.35);
        }}
        .ss-card h3, .ss-card h4 {{ color: {GOLD} !important; margin-top: 0; }}

        .ss-badge {{
            display: inline-block;
            background-color: {MAROON};
            color: {CREAM} !important;
            font-family: 'Montserrat', sans-serif;
            font-weight: 800;
            font-size: 0.75rem;
            letter-spacing: 0.8px;
            text-transform: uppercase;
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            margin-bottom: 0.6rem;
        }}

        .ss-placeholder {{
            border: 2px dashed {GOLD};
            border-radius: 12px;
            background-color: {BG_PANEL};
            color: {GOLD} !important;
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            font-size: 1.1rem;
            text-align: center;
            padding: 3.5rem 1rem;
            margin: 1rem 0 1.6rem 0;
        }}

        /* Buttons / links */
        .stButton>button, .stDownloadButton>button {{
            background-color: {MAROON} !important;
            color: {CREAM} !important;
            font-weight: 700 !important;
            border-radius: 8px !important;
            border: none !important;
        }}
        .stButton>button:hover {{ background-color: {MAROON_LIGHT} !important; }}

        a, a:visited {{ color: {GOLD} !important; font-weight: 600; }}

        /* Divider */
        hr {{ border-top: 1px solid {MAROON} !important; }}

        /* Dataframe */
        div[data-testid="stDataFrame"] {{
            border: 1px solid {MAROON};
            border-radius: 8px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def page_title(title: str, subtitle: str = None):
    """Big, bold, centered page-title block — use at the top of every page
    instead of a raw st.markdown("# ...") so every page matches."""
    subtitle_html = f'<div class="ss-page-subtitle">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f"""
        <div class="ss-page-title-wrap">
            <div class="ss-page-title">{title}</div>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

def card(title: str, body_html: str, badge: str = None):
    """Render a styled content card."""
    badge_html = f'<span class="ss-badge">{badge}</span><br>' if badge else ""
    st.markdown(
        f'<div class="ss-card">{badge_html}<h3>{title}</h3>{body_html}</div>',
        unsafe_allow_html=True,
    )

def map_placeholder(caption: str = "Map will be uploaded here"):
    st.markdown(
        f'<div class="ss-placeholder">🗺️ &nbsp; {caption}</div>',
        unsafe_allow_html=True,
    )

def map_image(filename):
    """Resolve a static map PNG path relative to this file — works both
    locally and on Streamlit Cloud regardless of working directory."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "..", "outputs", "maps", filename)