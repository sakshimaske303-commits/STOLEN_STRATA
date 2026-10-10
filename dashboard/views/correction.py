import plotly.graph_objects as go
import streamlit as st

from lib import GREY, ORANGE, ROSE, TEAL, bars, caption, frame, note, show, style_fig, table
from style import page_title

page_title("The Correction", "Why the first headline number was wrong")

m = table("phase2_timeseries/v1_rule_matched_statistic.csv")
pc = table("phase2_timeseries/v1_2025_product_comparison.csv")
y = table("phase2_timeseries/yearly_bare_share.csv")

st.markdown(
    f"""
The first version of this project classified a pixel as bare when its June–September NDVI was below 0.15 and reported, as the
mean over 201 terrace polygons, **{m.earlier_reported_mean_of_polygons_pct.iloc[0]}%** bare in 1994 and
**{m.earlier_reported_mean_of_polygons_pct.iloc[-1]}%** in 2025. The first three dates came from Landsat. The last came from Sentinel-2.

The test is simple: run the same polygons, the same threshold and the same statistic on Landsat alone.
"""
)

fig = go.Figure()
yrs = m.year.astype(str)
fig.add_trace(bars(yrs, m.earlier_reported_mean_of_polygons_pct, ROSE, [f"{v:.2f}%" for v in m.earlier_reported_mean_of_polygons_pct], "Earlier estimate (Landsat to 2015, Sentinel-2 in 2025)"))
fig.add_trace(bars(yrs, m.landsat_only_mean_of_polygons_pct, TEAL, [f"{v:.2f}%" for v in m.landsat_only_mean_of_polygons_pct], "Same polygons, rule and statistic, Landsat only"))
fig.update_layout(barmode="group", yaxis_title="Bare-earth share, mean of 201 polygons (%)", yaxis_range=[0, 9.8], bargap=0.3, xaxis_type="category")
show(style_fig(fig, 430))
caption(f"In 2025 the Landsat-only figure is {m.landsat_only_mean_of_polygons_pct.iloc[-1]}%, not {m.earlier_reported_mean_of_polygons_pct.iloc[-1]}%. "
        "The comparison is not exact in one respect: the Landsat-only values use a single year's June–September median, where the earlier version used composites of several years. "
        "The 2015 and 2025 Landsat values come from the original-box series, which still carries the reversed Landsat 8/9 adjustment of the first run and has not yet been recomputed.")

c1, c2 = st.columns(2)
with c1:
    st.markdown("#### The same numbers, two ways of averaging")
    t = m.rename(columns={"year": "Year", "earlier_reported_mean_of_polygons_pct": "Earlier, mean of polygons (%)", "earlier_area_weighted_pct": "Earlier, area-weighted (%)",
                          "landsat_only_mean_of_polygons_pct": "Landsat only, mean of polygons (%)", "landsat_only_pooled_pct": "Landsat only, all pixels pooled (%)"})
    frame(t)
    caption("Whichever way the share is averaged, the 2025 jump is absent on Landsat.")
with c2:
    st.markdown("#### It was not the pixel size")
    s2, ls = pc.iloc[0], pc.iloc[1]
    st.markdown(
        f"""
The earlier version checked itself by resampling the 10 m Sentinel-2 image to 30 m. That tests pixel size, not the product.
Averaged onto the Landsat grid, the earlier Sentinel-2 composite still gives **{s2.below_015_mean_of_polygons_pct}%**.

On the same polygons in 2025 the median NDVI is **{s2.median_ndvi_on_polygons:.2f}** in that Sentinel-2 composite and
**{ls.median_ndvi_on_polygons:.2f}** in the Landsat series. A gap that large is more than the two instruments' band differences
normally produce, so it points to how the composite was built. Which step is responsible (cloud masking, compositing or
reflectance level) has not been isolated.
"""
    )

st.markdown("---")
st.markdown("### Two things this check also showed")
c1, c2 = st.columns(2)
with c1:
    st.markdown("#### The summer median is not a usable measure here")
    u = y[y.usable & y.bare_summer_landsat_v1rule.notna()]
    fig = go.Figure(go.Scatter(x=u.year, y=u.bare_summer_landsat_v1rule, mode="lines+markers", line=dict(color=GREY, width=2), marker=dict(size=8),
                               hovertemplate="%{x}: %{y:.1f}%<extra></extra>"))
    fig.update_layout(yaxis_title="Summer NDVI < 0.15, share of terrace pixels (%)", showlegend=False)
    show(style_fig(fig, 340, legend_top=False))
    caption("Terraces of the original box, Landsat only, usable years. Before 2009 a pixel had between 0 and 8 clear summer observations a year because of monsoon cloud, and the share swings from under 1% to 16% and back.")
with c2:
    st.markdown("#### The level depends on the instrument")
    r = y[y.year == 2025].iloc[0]
    names = ["Landsat, adjusted series", "Landsat 8/9, unadjusted", "Sentinel-2"]
    vals = [r.bare_p90_landsat, r.bare_p90_OLIonly, r.bare_p90_S2]
    fig = go.Figure(bars(names, vals, [TEAL, TEAL, ORANGE], [f"{v:.1f}%" for v in vals]))
    fig.update_layout(yaxis_title="Yearly peak NDVI < 0.25 in 2025 (%)", showlegend=False, yaxis_range=[0, max(vals) * 1.25])
    show(style_fig(fig, 340, legend_top=False))
    caption("The adjusted series here is the first run, before the Landsat 8/9 adjustment was corrected. Same terraces, same year, same rule, three instruments. A statement of the form “x% of the karewas are bare” has no single answer. Only change measured inside one instrument is defensible.")

note("<b>What follows from it.</b> Every comparison through time in the rest of this dashboard is made inside one sensor family. "
     "The road and settlement proximity tests, the 25 “degraded terraces”, the saffron proximity analysis and the rupee valuation of the earlier version all depended on the withdrawn layer and are not repeated.", "note")
