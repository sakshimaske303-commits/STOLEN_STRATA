import streamlit as st
import streamlit.components.v1 as components
from style import inject_css, card, page_title, GOLD

st.set_page_config(page_title="INTERACTIVE MAPS | Stolen Strata", page_icon="🗺️", layout="wide")
inject_css()

page_title("🗺️ INTERACTIVE MAPS", "Live, pannable/zoomable maps built from the project's own geopackages")

card(
    "About These Maps",
    """
    <p>Each map below is a fully interactive, pannable/zoomable Leaflet export built directly from this
    project's geopackages — pan, zoom, and click features to inspect their attributes. Pick a map from
    the dropdown to explore it.</p>
    """,
    badge="Live",
)

MAP_SERVER_BASE = "https://sakshimaske303-commits.github.io/STOLEN_STRATA/outputs/interactive_maps"

MAPS = {
    "Study Area Overview": "01_study_area_overview",
    "Terrace Degradation Status": "02_terrace_degradation_status",
    "Delineated Terrace Boundaries": "03_terrace_boundaries",
    "Validation at Saffron Fields, Lethpora": "04_validation_lethpora",
    "Saffron Proximity Risk": "05_saffron_proximity_risk",
    "Road Network Proximity": "06_road_network_proximity",
    "Settlement Proximity": "07_settlement_proximity",
    "Saffron Economic Value-at-Risk": "08_economic_value_at_risk",
}

selected_label = st.selectbox("Choose a map to explore", list(MAPS.keys()), index=0)
selected_folder = MAPS[selected_label]

components.iframe(
    src=f"{MAP_SERVER_BASE}/{selected_folder}/index.html",
    height=650,
    scrolling=True,
)
