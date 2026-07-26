import streamlit as st
from style import inject_css, card, map_placeholder, page_title, GOLD
import data as d

st.set_page_config(page_title="GEOMORPHOLOGICAL DELINEATION | Stolen Strata", page_icon="⛰️", layout="wide")
inject_css()

page_title("⛰️ GEOMORPHOLOGICAL DELINEATION", "Turning a DEM into terrace boundaries — no manual digitization")

c1, c2, c3 = st.columns(3)
c1.metric("Raw TPI/Slope Candidates", f"{d.TOTAL_CANDIDATES_RAW:,}")
c2.metric("After Area + Elevation Filter", f"{d.TOTAL_TERRACES}")
c3.metric("Total Mapped Terrace Area", f"{d.TOTAL_AREA_KM2} km²")

st.image(map_image("03_terrace_boundaries.png"), use_container_width=True)
  st.image(map_image("04_validation_lethpora.png"), use_container_width=True)

card(
    "Method",
    """
    <p>Terrace delineation follows the <b>Topographic Position Index (TPI)</b> framework (Weiss, 2001),
    combined with a slope-magnitude threshold — a fully algorithmic alternative to manual polygon
    tracing in QGIS. The DEM is reprojected from EPSG:4326 to <b>EPSG:32643 (UTM Zone 43N)</b> so slope
    is computed in true metric units. Slope is derived via <code>np.gradient</code>; TPI via a moving
    <code>scipy.ndimage.uniform_filter</code> window (17-pixel). Pixels with TPI &gt; 3 and slope &lt; 8°
    are flagged as flat, locally-elevated terrace surface — the diagnostic signature of a karewa
    tread versus its bounding scarp.</p>
    <p>Raw candidate pixels are vectorized with <code>rasterio.features.shapes</code>, then filtered to
    polygons ≥ 0.05 km² in area and within the 1550–2000 m elevation band known to host karewa
    exposures, removing DEM noise and non-karewa flat surfaces (river floodplain, etc.).</p>
    """,
    badge="Pipeline Stage 1",
)

card(
    "Why Thresholds Were Revised",
    """
    <p>An initial stricter threshold (TPI &gt; 5, slope &lt; 5°) produced thin, sliver-shaped polygons —
    a geomorphologically implausible shape for a depositional terrace tread. Thresholds were loosened
    (TPI &gt; 3, slope &lt; 8°) to recover blob-shaped polygons consistent with real terrace
    morphology, and the result was cross-validated against the known <b>Saffron Fields, Lethpora</b>
    location, where mapped polygons correctly overlapped the documented cultivation area.</p>
    """,
    badge="Validation",
)

st.markdown(
    f"""
    <p style="color:{GOLD}; font-weight:700;">Geomorphometric characterisation (compactness index,
    per-terrace mean slope) is being finalised — see the Methodology &amp; Data page for status.</p>
    """,
    unsafe_allow_html=True,
)