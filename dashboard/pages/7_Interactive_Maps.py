import streamlit as st
import streamlit.components.v1 as components
from style import inject_css, card, page_title, GOLD

st.set_page_config(page_title="INTERACTIVE MAPS | Stolen Strata", page_icon="🗺️", layout="wide")
inject_css()

page_title("🗺️ INTERACTIVE MAPS", "Live, pannable/zoomable maps exported from QGIS")

card(
    "About These Maps",
    """
    <p>Each map below is a fully interactive, pannable/zoomable export — pan, zoom, and click features
    to inspect their attributes. Pick a map from the dropdown to explore it.</p>
    """,
    badge="Live",
)

# Change this to your GitHub Pages URL once maps are pushed live
MAP_SERVER_BASE = "https://sakshimaske303-commits.github.io/STOLEN_STRATA/outputs/interactive_maps"

MAPS = {
    "Road Network Proximity": "06_road_network_proximity",
    "Study Area Overview": "01_study_area_overview",
    "Terrace Degradation Status": "02_terrace_degradation_status",
    "Delineated Terrace Boundaries": "03_terrace_boundaries",
    "Validation at Saffron Fields, Lethpora": "04_validation_lethpora",
}

selected_label = st.selectbox("Choose a map to explore", list(MAPS.keys()), index=0)
selected_folder = MAPS[selected_label]

components.iframe(
    src=f"{MAP_SERVER_BASE}/{selected_folder}/index.html",
    height=650,
    scrolling=True,
)

st.markdown(
    f"""
    <p style="color:{GOLD}; font-size:0.9rem; margin-top:1rem;">
    Note: the Saffron Proximity-Risk map is temporarily excluded — its buffer-zone symbology didn't
    export cleanly. The static version on the Saffron Vulnerability page is correct.
    </p>
    """,
    unsafe_allow_html=True,
)