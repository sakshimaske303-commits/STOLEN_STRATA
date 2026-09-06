import streamlit as st
import os
from style import inject_css, card, page_title, GOLD
import data as d

st.set_page_config(page_title="METHODOLOGY AND DATA | Stolen Strata", page_icon="🧪", layout="wide")
inject_css()

page_title("🧪 METHODOLOGY AND DATA", "Full pipeline, script-by-script")

# Proof-of-work popovers — pulsing buttons, click to reveal screenshot
st.markdown(f"""
<style>
    div[data-testid="stPopover"] button {{
        animation: proof-blink 1.8s ease-in-out infinite;
        border: 3px solid {GOLD} !important;
        width: 32px !important;
        height: 32px !important;
        border-radius: 50% !important;
        padding: 0 !important;
        min-height: unset !important;
        min-width: unset !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    div[data-testid="stPopover"] button p {{
        margin: 0 !important;
        font-size: 0.95rem !important;
        line-height: 1 !important;
    }}
    @keyframes proof-blink {{
        0%, 100% {{ box-shadow: 0 0 0px rgba(212, 175, 55, 0); }}
        50% {{ box-shadow: 0 0 12px rgba(212, 175, 55, 0.85); }}
    }}
</style>
""", unsafe_allow_html=True)

PROOF_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "outputs", "proof_screenshots")

def proof_popover(filename, caption):
    path = os.path.join(PROOF_DIR, filename)
    with st.popover("Proof"):
        if os.path.exists(path):
            st.image(path, caption=caption, use_container_width=True)
        else:
            st.caption(f"Screenshot not added yet — save it as `outputs/proof_screenshots/{filename}`.")

PROOF_MAP = {
    "01": ("01_extract_karewa_terraces_vscode.png", "01_extract_karewa_terraces.py open in VS Code — the DEM-based TPI/slope extraction that generates the raw terrace candidate polygons."),
    "03": ("06_terrace_degradation_qgis.png", "Terrace degradation status (stable vs. likely-degraded, from the NDVI bare-earth-fraction classification) across the Budgam–Pampore–Pulwama karewa belt, in QGIS."),
    "04": ("02_saffron_terraces_qgis.png", "Degraded terraces and the saffron overlay loaded together in QGIS over a satellite basemap — the terrace-vs-saffron-cultivation view at the heart of this project's thesis."),
    "09": ("05_road_proximity_qgis.png", "The road network loaded alongside terrace degradation status in QGIS — the layer behind the road-proximity Mann-Whitney test."),
    "11": ("03_threshold_sensitivity_vscode.png", "11_threshold_sensitivity.py open in VS Code — sweeps all three thresholds (TPI/slope, degradation, saffron signature) across a neighbourhood of plausible values, since all three were originally chosen by visual inspection with no reported sensitivity check."),
    "12": ("04_robustness_effect_sizes_vscode.png", "12_robustness_and_effect_sizes.py open in VS Code — the resolution-mismatch quantification and Holm-Bonferroni correction across the four Mann-Whitney tests."),
}

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
    ("10", "Geomorphometrics & Figures", "Compactness Index (4π·Area/Perimeter²) and mean slope per terrace, tested against degradation status; first static figure set.", f"compactness p={d.COMPACTNESS_MWU_P} (significant), slope p={d.SLOPE_MWU_P} (n.s.) — confirmed" if d.GEOMORPHOMETRICS_CONFIRMED else "pending confirmed run"),
    ("11", "Threshold Sensitivity", "Sweeps the TPI/slope, degradation, and saffron thresholds across a neighbourhood of plausible values, since all three were originally chosen by visual inspection with no reported sensitivity check.", "degradation: 23-31 terraces across 12-20pp; saffron proximity-risk: 39-44% across 0.05-0.175"),
    ("12", "Robustness & Effect Sizes", "Resamples 2025 Sentinel-2 to 30m (matching earlier years' Landsat) to quantify the resolution-mismatch effect; adds rank-biserial effect sizes and a Holm-Bonferroni correction across the Mann-Whitney tests.", f"resolution: 8.43%→7.48% (real, modest); settlement proximity, road proximity + compactness survive correction"),
    ("14b", "Settlement Proximity", "osmnx building-footprint extraction (3,266 features); distance to nearest building per terrace; Mann-Whitney U test — a second, independent infrastructure signal alongside roads.", f"p = {d.SETTLEMENT_PROXIMITY_MANNWHITNEY_P} (strongest effect in the study, r={d.EFFECT_SIZE_SETTLEMENT_R})"),
    ("15", "Economic Valuation", "Detected saffron area converted to annual production value using official 2024-25 state yield and price figures.", f"Rs {d.SAFFRON_TOTAL_VALUE_CR} cr/yr total, Rs {d.SAFFRON_AT_RISK_VALUE_CR} cr/yr within 1km risk radius"),
]

for num, title, method, result in steps:
    card(
        f"{num} — {title}",
        f"<p>{method}</p><p style='color:{GOLD}; font-weight:700; margin-bottom:0;'>Result: {result}</p>",
    )
    if num in PROOF_MAP:
        filename, caption = PROOF_MAP[num]
        pc1, pc2 = st.columns([0.92, 0.08])
        with pc2:
            proof_popover(filename, caption)

st.markdown("---")
st.markdown("### Repository Structure")
st.code(
    """
STOLEN_STRATA/
├── data/
│   ├── raw/          # GEE exports (DEM, NDVI composites, Saffron Index) — gitignored
│   ├── interim/       # intermediate candidates, reprojected rasters
│   └── processed/     # final geopackages used by the dashboard
├── src/
│   ├── acquisition/   # reserved for scripted GEE acquisition (currently empty —
│   │                   #   acquisition was run interactively in the GEE Code Editor)
│   ├── preprocessing/  # reserved, currently empty
│   ├── analysis/      # 01–15, the scripts described above
│   └── visualization/
├── notebooks/
├── outputs/
│   ├── maps/
│   ├── interactive_maps/
│   ├── ground_truth_sample_points.gpkg
│   └── figures/
├── dashboard/          # this Streamlit app
├── tests/
├── SS_Executive_Summary.md
├── SS_Research_Paper.md
├── SS_Development_Log.md
└── requirements.txt
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
    "<p style='text-align:center; color:#8A94AD; font-size:0.9rem;'>STOLEN STRATA — Quantifying the Anthropogenic Erasure of Kashmir's Karewa Terraces</p>",
    unsafe_allow_html=True,
)