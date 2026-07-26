import streamlit as st
from style import inject_css, card, page_title, GOLD, MAROON
import data as d

st.set_page_config(page_title="About & GitHub | Stolen Strata", page_icon="🔗", layout="wide")
inject_css()

page_title("🔗 About & Repository")
st.markdown("---")

c1, c2 = st.columns([1.3, 1])
with c1:
    card(
        "About This Project",
        """
        <p><b>Stolen Strata</b> quantifies the anthropogenic erasure of Kashmir's karewa terraces and
        its threat to the saffron economy, combining classical geomorphological theory with a fully
        scripted remote sensing and GIS pipeline. It is designed to demonstrate methodological range
        across physical and human geography — geomorphometrics and terrain analysis alongside
        multi-temporal satellite change detection and policy-relevant spatial statistics.</p>
        """,
    )
    card(
        "Author",
        """
        <p><b>Sakshi D. Maske</b><br>
        B.A. Economics, Political Science, History &amp; English Literature (2023)<br>
        GIS &amp; Remote Sensing Research Portfolio</p>
        <p>Prior portfolio work: <i>GPIE</i> (Ganga Plain Isostatic Equilibrium) and <i>ECOCIDE</i> —
        both built on the same principle followed here: QGIS reserved for visual quality assurance
        only, with every analytical step scripted and reproducible in Python.</p>
        """,
    )
with c2:
    st.markdown(
        f"""
        <div class="ss-card" style="text-align:center; padding:2.2rem 1.5rem;">
            <div class="ss-badge">Source Code</div>
            <h3 style="margin-top:0.4rem;">GitHub Repository</h3>
            <p style="color:#9AA5B8;">Fully documented, reproducible pipeline — scripts, data schema,
            and development log.</p>
            <a href="{d.GITHUB_URL_PLACEHOLDER}" target="_blank"
               style="display:inline-block; margin-top:0.8rem; background-color:{MAROON};
               color:#F5F1E8; font-family:'Montserrat',sans-serif; font-weight:800;
               padding:0.7rem 1.6rem; border-radius:8px; text-decoration:none; letter-spacing:0.4px;">
               ↗ View on GitHub
            </a>
            <p style="color:{GOLD}; font-size:0.8rem; margin-top:1rem;">
            (Replace the placeholder URL in <code>dashboard/data.py</code> →
            <code>GITHUB_URL_PLACEHOLDER</code> once the repo is public.)
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
st.markdown(
    """
    <p style="text-align:center; color:#9AA5B8; font-size:0.85rem;">
        Stolen Strata &nbsp;·&nbsp; Kashmir Valley, Jammu &amp; Kashmir &nbsp;·&nbsp; Geomorphology ·
        Remote Sensing &amp; GIS · Environmental Policy
    </p>
    """,
    unsafe_allow_html=True,
)
