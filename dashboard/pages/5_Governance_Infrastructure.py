import streamlit as st
from style import inject_css, card, map_placeholder, page_title, map_image, GOLD
import data as d

st.set_page_config(page_title="GOVERNANCE AND INFRASTRUCTURE | Stolen Strata", page_icon="🛣️", layout="wide")
inject_css()

page_title("🛣️ GOVERNANCE AND INFRASTRUCTURE", "Is degradation an accessibility story, and is policy targeting the right land?")

col1, col2 = st.columns(2)
col1.metric("Mann-Whitney U p-value", f"{d.ROAD_PROXIMITY_MANNWHITNEY_P}")
col2.metric("Test", "Degraded vs Non-Degraded Road Distance")

st.image(map_image("06_road_network_proximity.png"), use_container_width=True)

card(
    "Method",
    """
    <p>The OpenStreetMap road network within the study bounding box is extracted via
    <code>osmnx.graph_from_bbox(..., network_type='drive')</code>. Straight-line distance from each
    terrace centroid to the nearest road edge is computed, then compared between degraded and
    non-degraded terraces using a <b>Mann-Whitney U test</b> — a non-parametric test appropriate here
    because terrace-to-road distances are non-normally distributed and zero-inflated near dense
    settlement edges.</p>
    """,
    badge="Pipeline Stage 4",
)

card(
    "Result",
    f"""
    <p>{d.ROAD_PROXIMITY_FINDING}</p>
    <p>This is consistent with an accessibility-driven model of unregulated mining: extraction is
    economically viable where the marginal cost of transporting excavated material to a construction
    or brick-kiln market is lowest, i.e. near existing drivable roads — rather than being randomly
    distributed across the karewa landscape irrespective of infrastructure.</p>
    """,
    badge="Finding",
)

card(
    "Policy Framing (RQ4)",
    """
    <p>The project's fourth research question asks whether current agricultural policy investment
    (e.g. National Saffron Mission funding) is spatially aligned with karewa land that remains
    geomorphologically and agronomically intact — or is instead directed toward land already under
    active erosion pressure. Publicly available, spatially resolved land-lease and enforcement data for
    this comparison is limited; this page is framed honestly around that constraint rather than
    overstating what current open data permits. The road-proximity and degradation-hotspot layers
    developed here nonetheless provide a evidentiary basis that a future policy-alignment overlay
    (pending accessible scheme-level spatial data) could build on directly.</p>
    """,
    badge="Governance Question",
)