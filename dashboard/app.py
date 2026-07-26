import streamlit as st
from style import inject_css, card, GOLD, MAROON
import data as d

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

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Terraces Delineated", f"{d.TOTAL_TERRACES}", help="After area + elevation filtering of TPI/slope candidates")
col2.metric("Terrace Area Mapped", f"{d.TOTAL_AREA_KM2} km²")
col3.metric("Net Bare-Earth Conversion", f"{d.NET_CONVERSION_HA} ha", f"{d.NET_CONVERSION_PCT}% of mapped area")
col4.metric("Terraces Flagged Degraded", f"{d.DEGRADED_COUNT}", f"{d.DEGRADED_PCT_OF_TERRACES}% of total")

st.markdown("<br>", unsafe_allow_html=True)

c1, c2 = st.columns([1.3, 1])
with c1:
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
with c2:
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
        Use the sidebar to navigate — Study Design → Geomorphological Delineation → Degradation Analysis
        → Saffron Vulnerability → Governance &amp; Infrastructure → Explore Trends → Interactive Maps →
        Methodology &amp; Data → About &amp; GitHub.
    </p>
    """,
    unsafe_allow_html=True,
)
