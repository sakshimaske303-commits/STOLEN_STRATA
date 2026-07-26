import streamlit as st
from style import inject_css, card, page_title, GOLD
import data as d

st.set_page_config(page_title="METHODOLOGY AND DATA | Stolen Strata", page_icon="🧪", layout="wide")
inject_css()

page_title("🧪 METHODOLOGY AND DATA", "Full pipeline, script-by-script")

steps = [
    ("01", "Extract Karewa Terraces", "DEM reprojected to UTM43N; slope via np.gradient; TPI via uniform_filter (window=17); threshold TPI>3 & slope<8°; vectorised via rasterio.features.shapes.", f"{d.TOTAL_CANDIDATES_RAW:,} raw candidate polygons"),
    ("02", "Filter Terrace Candidates", "Area filter (≥0.05 km²) + elevation filter (1550–2000 m) via zonal stats.", f"{d.TOTAL_TERRACES} filtered polygons"),
    ("03", "NDVI Change Detection", "Season-matched (Jun–Sep) NDVI composites, 1994 vs 2025; bare-earth fraction (% pixels < NDVI 0.15) per polygon.", f"{d.DEGRADED_COUNT}/{d.TOTAL_TERRACES} classified likely_degraded"),
    ("04", "Saffron Overlay", "Saffron Index = March NDVI − summer NDVI (inverse phenology); threshold 0.15.", f"{d.SAFFRON_POLYGONS} polygons flagged likely_saffron"),
    ("05", "Saffron Proximity Risk", "Distance from saffron polygons to union of degraded terrace geometries; sensitivity loop across 500–2500 m.", f"mean {d.PROXIMITY_MEAN_M} m, min {d.PROXIMITY_MIN_M} m"),
    ("06", "Saffron Area Benchmark", "Detected saffron area vs FAO GIAHS baseline (3,200 ha).", f"{d.SAFFRON_AREA_HA} ha detected — reported as a recall limitation, not a loss statistic"),
    ("07", "Absolute Area Loss", "Total terrace area, 1994 vs 2025 bare-earth area, net conversion, concentration within degraded subset.", f"{d.NET_CONVERSION_HA} ha net loss ({d.NET_CONVERSION_PCT}%)"),
    ("08", "Multi-Temporal Trend", "Adds 2005 and 2015 NDVI (Landsat 5 / Landsat 8) for a 4-point trend.", "1.84% → 2.62% → 2.63% → 8.43%"),
    ("09", "Road Proximity", "osmnx road network extraction; distance to nearest road per terrace; Mann-Whitney U test.", f"p = {d.ROAD_PROXIMITY_MANNWHITNEY_P}"),
    ("10", "Geomorphometrics & Figures", "Compactness Index (4π·Area/Perimeter²) and mean slope per terrace, tested against degradation status; first static figure set.", "pending confirmed run" if not d.GEOMORPHOMETRICS_CONFIRMED else "confirmed"),
]

for num, title, method, result in steps:
    card(
        f"{num} — {title}",
        f"<p>{method}</p><p style='color:{GOLD}; font-weight:700; margin-bottom:0;'>Result: {result}</p>",
    )

st.markdown("---")
st.markdown("### Repository Structure")
st.code(
    """
Stolen_Strata/
├── data/
│   ├── raw/          # GEE exports (DEM, NDVI composites, Saffron Index)
│   ├── interim/       # intermediate candidates, reprojected rasters
│   └── processed/     # final geopackages used by the dashboard
├── src/
│   ├── acquisition/   # GEE Code Editor scripts (JS)
│   ├── preprocessing/
│   ├── analysis/      # 01–10, the scripts described above
│   └── visualization/
├── notebooks/
├── outputs/
│   ├── maps/
│   ├── figures/
│   └── tables/
├── dashboard/          # this Streamlit app
├── docs/
│   ├── research_paper/
│   ├── project_journal/
│   └── development_log/
└── tests/
    """,
    language="text",
)

card(
    "Tools",
    """
    <p>Google Earth Engine (JavaScript, Code Editor) for Landsat 5/7/8 and Sentinel-2 acquisition ·
    Python (rasterio, geopandas, numpy, scipy, osmnx, matplotlib) for the entire analytical pipeline ·
    QGIS used exclusively for visual quality-assurance, never for production digitization · Streamlit
    + Plotly for this dashboard.</p>
    """,
    badge="Stack",
)

st.markdown("---")
st.markdown(
    f"""
    <div style="text-align:center; padding-top:1rem; padding-bottom:1rem;">
        <p style="color:{GOLD}; font-size:1.1rem; margin-bottom:0.3rem;">
            📦 Full code, data, and reproducible pipeline
        </p>
        <p style="margin-bottom:1.8rem;">
            <a href="https://github.com/sakshimaske303-commits/STOLEN_STRATA" target="_blank"
               style="color:{GOLD}; font-weight:700; font-size:1.05rem; text-decoration:none;">
                github.com/sakshimaske303-commits/STOLEN_STRATA
            </a>
        </p>
        <p style="color:#8A94AD; font-size:0.9rem; letter-spacing:0.15em; margin-bottom:0.3rem;">
            PROJECT AUTHOR
        </p>
        <p style="font-weight:800; font-size:1.4rem; letter-spacing:0.05em;">
            SAKSHI D. MASKE
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)