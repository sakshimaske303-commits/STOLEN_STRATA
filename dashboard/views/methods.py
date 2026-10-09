import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from lib import GITHUB, GREY, TEAL, caption, frame, note, show, style_fig, table
from style import page_title

page_title("Methods and Data", "What was used, in what order, and how to rerun it")
obs = table("west_extension/landsat_observation_counts_wide.csv")

st.markdown("### Data")
frame(pd.DataFrame([
    ("Elevation", "Copernicus DEM GLO-30 (2011–2015)", "Terrace delineation: slope, height above drainage, scarp share"),
    ("Main time series", "Landsat 8 and 9, Collection 2 Level 2, 2013–2025", "Both conversion tests"),
    ("Long series", "Landsat 5, 7, 8, 9, with 8/9 adjusted to 7 (Roy et al., 2016), 1990–2025", "The view back to 1993"),
    ("Second opinion", "Landsat 7 alone, 2013–2021", "Independent check on Landsat 8"),
    ("Third instrument", "Sentinel-2, Cloud Score+ masked, 2019–2025", "Confirms the 2023–2025 state"),
    ("Geology", "Dar and Zeeden (2020), Figure 2, georeferenced", "Check of the terrace map, original box"),
    ("Elevation change", "SRTM (2000), ALOS World 3D (2006–2011), GEDI (2019–2025)", "Depth test, which failed"),
    ("Reference labels", "Google Maps / Google Earth Pro: newest imagery (2022–2026) and 2013–2015 historical imagery", "Two accuracy samples, 240 points, and their before-check"),
], columns=["Role", "Source", "Used for"]))
caption("Study box: 74.55°–75.15° E, 33.80°–34.15° N, about 2,160 km². All satellite composites were exported from Google Earth Engine at 30 m and analysed locally in Python.")

st.markdown("### Which years can be used")
fig = go.Figure(go.Bar(x=obs.year, y=obs.median_clear_obs_terraces, marker=dict(color=[TEAL if u else GREY for u in obs.usable], line=dict(color="#0A0E1A", width=1)),
                       hovertemplate="%{x}: %{y:.0f} clear observations<extra></extra>"))
fig.add_hline(y=10, line=dict(color=GREY, dash="dot"), annotation_text="minimum used: 10", annotation_font_color=GREY, annotation_position="top left")
fig.update_layout(showlegend=False, yaxis_title="Clear observations in the year")
show(style_fig(fig, 340, legend_top=False))
caption("A year is used only if the median terrace pixel has at least 10 clear observations. That removes " + ", ".join(str(y) for y in obs[~obs.usable].year) + " (grey).")

st.markdown("### Steps")
st.markdown(
    """
| Step | What it does | Script in `v2_redesign/` |
|---|---|---|
| 1 | Flat tops from the elevation model; scarp share of each | `west_extension/01_flat_top_delineation_wide.py` |
| 2 | Cut-off chosen and checked against geology (original box) | `phase1_delineation/04_geology_check.py` |
| 3 | Yearly peak NDVI and observation counts, by sensor | `west_extension/gee_04_extended_box.js` (Earth Engine) |
| 4 | Strict test, by stratum and terrace; cross-sensor checks | `west_extension/02_conversion_wide_box.py` |
| 5 | Drop test, with reverse change | `west_extension/03_drop_test_wide.py` |
| 6 | Sample drawn, labelled blind to stratum, area estimates | `west_extension/04_accuracy_sample.py`, `05_accuracy_result.py`, `09_accuracy_by_labelling_pass.py`, `12_accuracy_sample_supplement.py`, `15_pooled_accuracy.py` |
| 7 | Sensitivity to terrace cut-offs and to test thresholds | `west_extension/06_…`, `07_…`, `phase2_timeseries/03_…` |
| 8 | Long series by site and period | `west_extension/08_long_series_wide.py` |
| 8a | Terraces against other flat land, polygon by polygon; omitted karewa with both tests | `west_extension/13_polygon_level_comparison.py`, `14_omitted_karewa_both_tests.py` |
| 9 | The earlier rule rerun on Landsat only | `phase2_timeseries/02_…`, `05_v1_rule_matched_statistic.py` |
| 10 | Elevation test | `phase4_elevation/01_elevation_gate_test.py` |
"""
)

st.markdown("### Rerunning it")
st.markdown(
    f"""
The Python scripts and every result table are in the [repository]({GITHUB}) under `v2_redesign/`. The rasters are too large to store
there; the Earth Engine scripts regenerate them, and `DATA_ACCESS.md` lists each file. With the rasters in `data/raw`, the scripts
run from the repository root and write the tables this dashboard reads. This dashboard needs no rasters: the map layers are built once by
`dashboard/build_data.py`.
"""
)

note("<b>Status, October 2026.</b> The analysis and the paper are revised. Two accuracy samples (240 points) are labelled and pooled, the flagged points have been checked against imagery of 2013–2015, and the two official documents read in full. Still open: a rule or drawn outlines for the edge of a kiln field, a second labeller, "
     "an accuracy figure for the terrace map, recomputing the long series with the corrected Landsat 8/9 adjustment, and replacing the September preprint, which still carries the withdrawn numbers.", "caution")
