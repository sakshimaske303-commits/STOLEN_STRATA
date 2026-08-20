import streamlit as st
import streamlit.components.v1 as components
from style import inject_css, card, map_placeholder, page_title, map_image, GOLD
import data as d

st.set_page_config(page_title="STUDY DESIGN | Stolen Strata", page_icon="📖", layout="wide")
inject_css()

page_title("📖 STUDY DESIGN", "Region, rationale, and the questions this project set out to answer")

card(
    "Study Area",
    """
    <p>The primary study area is the central Kashmir Valley, encompassing the karewa belts of
    <b>Pampore, Pulwama, and Budgam districts</b>, together with the type-locality exposures near
    <b>Srinagar (Zewan section)</b>. This area holds the highest concentration of saffron-bearing
    karewas in the valley and has been repeatedly flagged in secondary literature as a hotspot of
    unregulated soil mining.</p>
    <p><b>Approximate bounding coordinates:</b> 33.85°N–34.15°N, 74.75°E–75.15°E</p>
    """,
    badge="Where",
)

components.iframe(
    src="https://sakshimaske303-commits.github.io/STOLEN_STRATA/outputs/interactive_maps/01_study_area_overview/index.html",
    height=560,
    scrolling=True,
)
st.markdown(
    "<p style='text-align:center; font-size:0.85rem; color:#999;'>The three-district study area boundary, waterways, and settlements — pan, zoom, and click features to inspect them.</p>",
    unsafe_allow_html=True,
)

c1, c2 = st.columns(2)
with c1:
    card(
        "Geomorphological Background",
        """
        <p>The Karewa Group represents a fluvio-lacustrine and glacio-fluvial infill sequence tied to
        the tectonic uplift of the Pir Panjal Range. A <b>Lower Karewa</b> (lacustrine clays, silts,
        lignite bands) records a standing-water phase; an <b>Upper Karewa</b> (coarser fluvial gravels
        and sands) records the basin's gradual infilling. Sediments span the Plio-Pleistocene.
        Subsequent incision by the Jhelum River and its tributaries dissected the infill, isolating the
        flat-topped terraces seen today. A Pleistocene aeolian loess cap gives the surface its
        agronomic value — well-drained, calcareous, silt-rich soil ideal for saffron corms.</p>
        """,
        badge="Theory",
    )
with c2:
    card(
        "Research Gap",
        """
        <ol>
        <li>No systematic, multi-decadal, satellite-derived quantification of karewa areal loss exists
        — only site-specific or anecdotal accounts.</li>
        <li>No spatially explicit overlay of karewa loss against saffron cultivation extent has been
        published, so it is unknown how much <i>productive</i> (versus marginal) terrace land is being
        consumed.</li>
        <li>Whether policy instruments such as the National Saffron Mission are targeting
        geomorphologically secure land, or land already under active erosion pressure, has not been
        assessed.</li>
        </ol>
        """,
        badge="Why This Matters",
    )

st.markdown("### Research Questions")
rq_cols = st.columns(4)
rqs = [
    ("RQ1", "What is the net areal change in karewa terrace extent between the earliest usable Landsat archive and the present day?"),
    ("RQ2", "Where is this loss concentrated, and does it correlate with proximity to roads / urban centres / mining activity?"),
    ("RQ3", "What proportion of lost terrace area overlapped with saffron cultivation, and what does this imply for the industry's viability?"),
    ("RQ4", "Are current policy investments (e.g. National Saffron Mission) spatially aligned with terrace land that remains intact?"),
]
for col, (tag, text) in zip(rq_cols, rqs):
    with col:
        card(tag, f"<p style='font-size:0.92rem;'>{text}</p>")

st.markdown("### Data Sources")
st.table(
    {
        "Data": [
            "Landsat 5/7/8/9 archive (1990s–2026)",
            "Sentinel-2 (2015–2026)",
            "DEM (SRTM/Copernicus)",
            "Saffron cultivation extent",
            "National Saffron Mission documentation",
            "OpenStreetMap road network",
        ],
        "Source": [
            "USGS / Google Earth Engine",
            "Copernicus / GEE",
            "Copernicus DEM via GEE",
            "Literature + ground-truthed via imagery",
            "Government of India / J&K publications",
            "osmnx",
        ],
        "Purpose": [
            "Multi-decadal land-cover change detection",
            "High-resolution recent-period mapping",
            "Terrace delineation via slope-break / TPI",
            "Economic overlay layer",
            "Policy evaluation layer",
            "Infrastructure-proximity analysis",
        ],
    }
)
