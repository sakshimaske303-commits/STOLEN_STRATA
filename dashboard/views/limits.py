import streamlit as st

from lib import frame, note, table
from style import card, page_title

page_title("What It Cannot Show", "Tests that failed, questions left open, and what was dropped")
eg = table("phase4_elevation/elevation_gate_test.csv")

card(
    "How deep the ground was dug",
    """
    <p>The paper makes no depth or volume claim. Every free elevation model is older than the Rangeen Kultreh kiln field:
    SRTM (2000), ALOS World 3D (2006–2011) and Copernicus (2011–2015). Their differences over the converted block match the unconverted
    part of the same terraces to within noise. GEDI laser returns (2019–2025) are precise enough on these flat surfaces, but only nine usable
    shots fall on the converted block, all from 2019. The result says “vegetated to bare”, not “excavated”.</p>
    """,
    badge="Elevation test: failed",
)
g = eg[(eg.source == "GEDI minus TanDEM-X") & (eg.group != "whole_box") & (eg.n > 0)].copy()
g["group"] = g.group.replace({"converted": "Converted block", "terraces_5_3_unconverted": "Rest of the same two terraces", "other_terraces": "All other terraces"})
with st.expander("GEDI ground height minus the 2011–2015 surface, by year and group"):
    frame(g[["year", "group", "n", "median_m", "nmad_m"]].astype({"year": int}).rename(columns={"year": "Year", "group": "Group", "n": "Cells with shots", "median_m": "Median difference (m)", "nmad_m": "Spread, NMAD (m)"}))

card(
    "A link to the saffron land",
    """
    <p>The saffron-signature polygons of the earlier version lie around Pampore, 7 km or more from the Rangeen Kultreh kiln field. The terraces
    outside the two kiln belts, which include the Pampore and Lethpora tablelands, convert at 0.39% by the drop test, against 0.37% for other
    flat land. So there is no evidence in 2013–2025 that the saffron tablelands are being converted the way the Budgam tablelands are.
    This says nothing about saffron decline from other causes, or about earlier decades. The saffron value-at-risk figure of the earlier version is withdrawn.</p>
    """,
    badge="No evidence found",
)
card(
    "The whole karewa",
    """
    <p>The terrace map captures scarp-bounded tablelands: about a quarter of the Karewa formation area on the geological map of the original box.
    Karewa ground outside the terraces converts at the same rate as ordinary valley floor in that box (0.19% against 0.19%), so the omission does not
    hide a second area of loss there, but the unit of study is not the Karewa Group as a whole. The elevation model dates from 2011–2015: tableland
    removed before then may no longer register as a flat top at all.</p>
    """,
    badge="Scope",
)

st.markdown("### Limitations, in full")
st.markdown(
    """
- **Before-state of the sample.** The 85 flagged points were looked up in imagery of 2013–2014, knowing they were flagged and mostly on one image of September 2014. Vegetation is visible at 72 of them; 13 of the 60 drop-only points were not clearly vegetated in that image. One image shows one day, while the tests use the peak of the year.
- **One labeller, 120 points, one image date.** 25 points in the strict stratum, most of them in one kiln field.
- **No accuracy figure for the terrace map.** Its reference sample is drawn and not labelled. The geological check uses a schematic figure and covers the original box only.
- **Missed kiln land is not estimated.** The tests detect new loss. Kiln land already bare before 2013 enters only through the long series.
- **Low NDVI is not excavation.** Attribution to kilns comes from the sample, from imagery and from documents.
- **Before 2013 the Landsat record is thin.** Six years have too few scenes to use, 2001 is anomalous, and peak NDVI steps up when Landsat 8 arrives.
- **The cloud mask is not exhaustive.** It removes cloud, shadow and snow, but not the cirrus flag of Landsat 8/9 or saturated pixels. The yearly peak should limit the effect; it has not been tested.
- **Thresholds are choices.** The sensitivity runs bound their effect; they do not remove it.
- **Documents were not all read in the original.** The tribunal filing for Rangeen Kultreh and the district list of kilns were read in full. The press reports and the April 2023 district report were checked against extracts and summaries. For the Bandagam–Batapora belt the only document is a list of registered kilns by village, without locations or dates of establishment.
- **One contradiction is unresolved.** A press report dates the Rangeen Kultreh kilns to 2003–2012; the satellite record shows that block vegetated until 2016.
- **The 8.43% artefact is shown, not fully explained.** Which step of the earlier Sentinel-2 processing produced it has not been isolated.
- **No fieldwork** was done at either kiln belt.
"""
)

note("<b>Dropped from the earlier version.</b> The road and settlement proximity tests, the compactness and slope comparison, the 25 “degraded terraces”, the saffron proximity analysis and the rupee valuation "
     "all depended on the withdrawn degradation layer. They are not repeated here and should not be cited.", "withdrawn")
