import streamlit as st
import os
from style import inject_css, card, GOLD, MAROON, BG_CARD, BG_PANEL, CREAM
import data as d
from doc_viewer import render_doc_viewer

st.set_page_config(
    page_title="Stolen Strata | Kashmir Karewa Terraces",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

st.markdown(
    f"""
    <div style="text-align:center; padding: 1.2rem 0 0.4rem 0;">
        <div class="ss-badge" style="font-size:0.85rem;">GEOMORPHOLOGY · REMOTE SENSING &amp; GIS · ENVIRONMENTAL POLICY</div>
        <div class="ss-hero-title">STOLEN STRATA</div>
        <p style="color:{GOLD}; font-family:'Montserrat',sans-serif; font-weight:700; font-size:1.15rem; margin-top:0.2rem;">
            Quantifying the Anthropogenic Erasure of Kashmir's Karewa Terraces<br>and Its Threat to the Saffron Economy
        </p>
        <p style="color:#9AA5B8; font-size:0.95rem;">Sakshi D. Maske &nbsp;·&nbsp; Kashmir Valley, Jammu &amp; Kashmir, India</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <style>
        .doi-badge-link {{ text-decoration:none; }}
        .doi-badge-card {{ transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease; cursor: pointer; }}
        .doi-badge-link:hover .doi-badge-card {{ transform: translateY(-3px) scale(1.02); box-shadow: 0 10px 32px rgba(139, 30, 63, 0.6); filter: brightness(1.08); }}
    </style>
    <div style="display:flex; justify-content:center; margin: 6px 0 18px 0;">
        <a href="https://doi.org/10.5281/zenodo.21766464" target="_blank" class="doi-badge-link" style="text-decoration:none;">
            <div class="doi-badge-card" style="
                display:flex; align-items:center; gap:18px;
                background: linear-gradient(145deg, {BG_CARD}, {BG_PANEL});
                border: 2px solid {MAROON};
                border-radius: 14px;
                padding: 16px 32px;
                box-shadow: 0 4px 20px rgba(139, 30, 63, 0.35);
            ">
                <div style="text-align:left;">
                    <div style="color:{GOLD}; font-family:'Montserrat',sans-serif; font-weight:800; font-size:1.05rem; letter-spacing:0.4px; display:flex; align-items:center; gap:8px;">
                        <span>ARCHIVED &amp; CITABLE ON ZENODO</span>
                        <span style="opacity:0.8; font-size:0.95rem;">↗</span>
                    </div>
                    <div style="color:{CREAM}; font-family:'Montserrat',sans-serif; font-weight:900; font-size:1.35rem; margin-top:2px;">
                        DOI: 10.5281/zenodo.21766464
                    </div>
                </div>
            </div>
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Terraces Delineated", f"{d.TOTAL_TERRACES}", help="After area + elevation filtering of TPI/slope candidates")
col2.metric("Terrace Area Mapped", f"{d.TOTAL_AREA_KM2} km²")
col3.metric("Net Bare-Earth Conversion", f"{d.NET_CONVERSION_HA} ha", f"{d.NET_CONVERSION_PCT}% of mapped area")
col4.metric("Terraces Flagged Degraded", f"{d.DEGRADED_COUNT}", f"{d.DEGRADED_PCT_OF_TERRACES}% of total")

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# WHY THIS MATTERS — real-world stakes callout
# ============================================================
card(
    "Why This Matters",
    f"""
    <p>This isn't just a landform story. The karewas' loess cap is the only reason Kashmir's
    Geographical Indication-tagged saffron (<i>Crocus sativus</i>) grows here at all — a crop the FAO's
    own baseline ties to roughly {d.FAO_FARM_FAMILIES:,} farming families. Every hectare mined for
    construction aggregate is permanently unavailable to that economy: unlike a fallow field, a
    flattened terrace cannot be replanted. The finding that degradation tracks road proximity
    (p = {d.ROAD_PROXIMITY_MANNWHITNEY_P}) turns an abstract land-cover statistic into an actionable
    lever — unregulated mining is not randomly distributed, it is access-driven, meaning targeted
    permitting and monitoring along road corridors near saffron-adjacent terraces could measurably slow
    it before the post-2015 acceleration reaches deeper into the Geographical Indication belt.</p>
    """,
    badge="Real-World Stakes",
)

# ============================================================
# THREE CARDS — stacked vertically, full width, one after another
# ============================================================
card(
    "The Question",
    """
    <p>The Kashmir Valley's <b>karewas</b> — flat-topped Plio-Pleistocene terraces left behind by an
    ancient intermontane lake — are being quietly flattened by unregulated soil mining and urban
    sprawl. The loess capping these terraces is exactly what makes them suitable for saffron
    (<i>Crocus sativus</i>) cultivation, a Geographical Indication-tagged crop central to the Pampore
    belt's economy. Journalistic accounts document the loss anecdotally. No systematic,
    multi-decadal, satellite-based quantification has previously connected the physical erasure
    of this landform to the economic fate of the industry it sustains — until now.</p>
    """,
    badge="Research Gap",
)

card(
    "The Approach",
    """
    <p>A fully scripted, reproducible Python pipeline — DEM-derived Topographic Position Index (TPI)
    and slope thresholding to algorithmically delineate terrace boundaries, Landsat/Sentinel-2
    time-series via Google Earth Engine to detect bare-earth land-cover change across a 1994–2025
    window, zonal saffron-signature detection, and proximity/statistical testing against road
    infrastructure. QGIS is used only for visual quality assurance — never for manual digitization.</p>
    """,
    badge="Methodology",
)

card(
    "Headline Finding",
    f"""
    <p style="font-size:1.4rem; color:{GOLD}; font-weight:800; margin-bottom:0.2rem;">
        {d.NET_CONVERSION_HA} ha lost
    </p>
    <p style="color:#9AA5B8; margin-top:0;">of karewa terrace converted to bare earth, 1994–2025</p>
    <hr>
    <p style="font-size:1.4rem; color:{GOLD}; font-weight:800; margin-bottom:0.2rem;">
        {d.DEGRADED_POLY_LOSS_SHARE_OF_TOTAL_LOSS_PCT}% of that loss
    </p>
    <p style="color:#9AA5B8; margin-top:0;">is concentrated within just {d.DEGRADED_COUNT} of {d.TOTAL_TERRACES} terraces ({d.DEGRADED_PCT_OF_TERRACES}%)</p>
    <hr>
    <p style="font-size:1.4rem; color:{GOLD}; font-weight:800; margin-bottom:0.2rem;">
        p = {d.ROAD_PROXIMITY_MANNWHITNEY_P}
    </p>
    <p style="color:#9AA5B8; margin-top:0;">degradation is statistically linked to road proximity</p>
    """,
    badge="At A Glance",
)

st.markdown("---")
st.markdown(
    f"""
    <p style="text-align:center; color:#9AA5B8; font-size:0.9rem;">
        Use the sidebar to navigate — Study Design → Theoretical Foundations → Geomorphological Delineation
        → Degradation Analysis → Saffron Vulnerability → Governance &amp; Infrastructure → Ground Verification
        → Explore Trends → Interactive Maps → Methodology &amp; Data. (Author and GitHub link are at the bottom of this page.)
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# FULL PROJECT DOCUMENTATION
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # .../dashboard
ROOT_DIR = os.path.dirname(BASE_DIR)                     # repo root

st.markdown(
    f"""
    <p style="text-align: center; color:{GOLD}; font-weight:700; font-size:1.1rem; margin-bottom:0.5rem;">
        Full Project Documentation
    </p>
    """,
    unsafe_allow_html=True,
)

_all_docs = [
    {"label": "Executive Summary", "filename": "SS_Executive_Summary.pdf"},
    {"label": "Research Paper", "filename": "SS_Research_Paper.pdf"},
    {"label": "Development Log", "filename": "SS_Development_Log.pdf"},
]
_docs = [d for d in _all_docs if os.path.exists(os.path.join(BASE_DIR, "static", d["filename"]))]
_missing = [d for d in _all_docs if d not in _docs]

if _docs:
    render_doc_viewer(
        docs=_docs,
        colors={
            "navy_dark": BG_PANEL,
            "navy_med": BG_CARD,
            "magenta": MAROON,
            "teal": GOLD,
            "text_light": CREAM,
        },
    )
for d in _missing:
    st.warning(f"{d['filename']} not found.")

# ============================================================
# FOOTER — name, role, and GitHub link, in a styled card
# ============================================================
st.markdown(
    f"""
    <div style='
        background-color:rgba(139, 0, 0, 0.08);
        border: 2px solid {MAROON};
        border-radius: 14px;
        padding: 28px 32px;
        margin-top: 2.5rem;
        text-align: center;
    '>
        <p style='font-size:2rem; font-weight:800; color:{GOLD}; margin-bottom:4px;'>
            Sakshi D. Maske
        </p>
        <p style='font-size:1.05rem; color:#9AA5B8; margin-top:0; margin-bottom:18px;'>
            Independent Geospatial Researcher
        </p>
        <a href='https://github.com/sakshimaske303-commits/STOLEN_STRATA' target='_blank' style='
            display:inline-block;
            background-color:{MAROON};
            padding:12px 26px;
            border-radius:8px;
            text-decoration:none;
        '>
            <span style='color:{GOLD} !important; font-weight:700; font-size:1rem;'>
                View Full Project on GitHub
            </span>
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)