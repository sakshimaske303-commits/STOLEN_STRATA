import os

import plotly.graph_objects as go
import streamlit as st

from lib import GREY, OCHRE, ORANGE, ROSE, TEAL, V2, caption, frame, mapfile, note, picture, show, style_fig, table
from style import page_title

page_title("Where and When", "Two brick-kiln belts in Budgam")
blk = mapfile("block_yearly.csv")
sm = mapfile("summary.json")
stock = table("west_extension/long_series_low_ndvi_stock.csv")
longd = table("west_extension/long_series_drop_test.csv")

# ------------------------------------------------------------------ Rangeen Kultreh
st.markdown("## Rangeen Kultreh")
st.markdown(
    f"""
Inside the Rangeen Kultreh site box (around 33.94° N, 74.85° E), about {sm['rangeen_block_ha']:.0f} ha of terrace passes the strict test (87.8 ha on the two whole terraces, 9 and 3). The chart follows those same pixels
back to 1993: their yearly peak NDVI in the Landsat record.
"""
)
u = blk[blk.usable]
fig = go.Figure()
fig.add_hrect(y0=0, y1=0.25, fillcolor=ORANGE, opacity=0.08, line_width=0)
fig.add_trace(go.Scatter(x=u.year, y=u.median_peak_ndvi_landsat, mode="lines+markers", name="Landsat 5/7/8/9, adjusted series", line=dict(color=TEAL, width=2), marker=dict(size=8),
                         hovertemplate="%{x}: %{y:.2f}<extra></extra>"))
o = blk[blk.median_peak_ndvi_landsat89.notna()]
fig.add_trace(go.Scatter(x=o.year, y=o.median_peak_ndvi_landsat89, mode="lines+markers", name="Landsat 8/9 only", line=dict(color=OCHRE, width=2, dash="dot"), marker=dict(size=7, symbol="diamond"),
                         hovertemplate="%{x}: %{y:.2f}<extra>Landsat 8/9</extra>"))
fig.add_vline(x=2017, line=dict(color=GREY, dash="dash"))
fig.add_annotation(x=2017, y=0.72, text="2017: kiln commissioned,<br>per the tribunal filing", showarrow=False, xanchor="right", xshift=-6, font=dict(color=GREY, size=12))
fig.add_annotation(x=1994, y=0.21, text="below 0.25 = bare all year", showarrow=False, xanchor="left", font=dict(color=ORANGE, size=12))
fig.update_layout(yaxis_title="Median yearly peak NDVI of the converted pixels", yaxis_range=[0, 0.78])
show(style_fig(fig, 430))
lo = u[(u.year <= 2016) & (u.year != 2001)].median_peak_ndvi_landsat
caption(f"Usable years only (at least 10 clear observations for the median terrace pixel). From 1993 to 2016 the median peak is between {lo.min():.2f} and {lo.max():.2f} "
        f"in every usable year except 2001 ({float(u[u.year == 2001].median_peak_ndvi_landsat.iloc[0]):.2f}), a year in which the whole series is anomalous. "
        f"It is {float(u[u.year == 2017].median_peak_ndvi_landsat.iloc[0]):.2f} in 2017 and {float(u[u.year == 2018].median_peak_ndvi_landsat.iloc[0]):.2f} in 2018.")

c1, c2 = st.columns([2, 3])
with c1:
    fig = go.Figure(go.Bar(x=o.year, y=o.bare_ha_landsat89, marker=dict(color=ORANGE, line=dict(color="#0A0E1A", width=2)), hovertemplate="%{x}: %{y:.0f} ha<extra></extra>"))
    fig.update_layout(yaxis_title="Peak NDVI below 0.25 (ha)", showlegend=False, xaxis=dict(dtick=2))
    show(style_fig(fig, 360, legend_top=False))
    caption("Bare land on the Rangeen Kultreh terraces by year, Landsat 8/9 only.")
with c2:
    picture(os.path.join(V2, "paper_figures", "Figure_3_rangeen_kultreh_onset.png"))
    caption("The year from which each strict-test pixel on terraces 9 and 3 stays bare. Most of the field opened in 2017–2018.")

st.markdown("#### What documents say about this place")
st.markdown(
    """
| Source | What it says | Against the satellite record |
|---|---|---|
| J&K Pollution Control Committee report to the National Green Tribunal, OA 364/2024 (1 July 2024) | A kiln at Rangeen Kultreh was commissioned in 2017 without consent; closure order in September 2018; 20 kilns within 1 km. | Agrees with the satellite onset |
| The Leaflet (2023); Greater Kashmir (2021) | Rangeen Kultreh is karewa land with about two dozen kilns; orchards felled for new ones. | Agrees on land use and place |
| Business Standard (2023) | Air Force Station letter: kilns around the station increased rapidly over the last decade. | Agrees on period |
| J&K Pollution Control Committee status report, OA 594/2022 (4 October 2023) | Six entries for the village among 226 kilns in the district: three kilns standing (one with consent, two under closure orders) and three with consent to establish, not yet built. | Agrees: no sign of two dozen older kilns under this village's name |
| The Leaflet (2023); Kashmir Despatch (2023) | About two dozen kilns were built 2003–2012 and none permitted 2013–2022. | **Does not agree:** the satellite record shows this block vegetated until 2016 |
"""
)
note("<b>One open point.</b> The contradiction with the 2003–2012 dates is not resolved: either the older kilns stand in another part of the village or the reported dates are wrong. "
     "The two official documents were read in full; the press reports were checked against extracts. The satellite onset was obtained before the tribunal filing was found.", "caution")

# ------------------------------------------------------------------ Bandagam-Batapora and the long view
st.markdown("---")
st.markdown("## Bandagam–Batapora, and the long view")
order = ["1993-1998", "1999-2002", "2003-2007", "2008-2012", "2013-2015", "2018-2020", "2023-2025"]
SITES = [("Bandagam-Batapora terraces", "Bandagam–Batapora terraces", ROSE, "circle"), ("Rangeen Kultreh terraces", "Rangeen Kultreh terraces", ORANGE, "square"),
         ("other terraces", "All other terraces", TEAL, "triangle-up"), ("other flat land", "Other flat, raised land", GREY, "diamond")]
fig = go.Figure()
for key, lab, colr, sym in SITES:
    d = stock[stock.site == key].set_index("period").loc[order]
    fig.add_trace(go.Scatter(x=order, y=d.below_035_pct, mode="lines+markers", name=lab, line=dict(color=colr, width=2), marker=dict(size=9, symbol=sym), customdata=d.below_035_ha,
                             hovertemplate=lab + "<br>%{x}: %{y:.1f}% (%{customdata:.0f} ha)<extra></extra>"))
fig.update_layout(yaxis_title="Land with yearly peak NDVI below 0.35 (%)", xaxis_title="Period (median of three usable years)", xaxis_type="category")
show(style_fig(fig, 430))
bb = stock[stock.site == "Bandagam-Batapora terraces"].set_index("period").loc[order]
caption("On the Bandagam–Batapora tablelands (about 74.60°–74.72° E, 33.99°–34.05° N) the low-vegetation land goes from "
        f"{bb.below_035_ha.iloc[0]:.0f} ha in 1993–1998 to {bb.below_035_ha.iloc[-1]:.0f} ha in 2023–2025, but not steadily: "
        + ", ".join(f"{v:.0f}" for v in bb.below_035_ha) + " ha across the seven periods. Inside the reliable Landsat 8/9 record (2013–2025) the drop test finds 142 ha of loss on these terraces (119 ha net), more than at Rangeen Kultreh (114 ha). Imagery shows kiln ground across several villages there. The Pollution Control Committee's list of October 2023 has registered kilns under most of those village names, without locations.")

l = longd[(longd.early == "1993-1998") & (longd.late == "2023-2025")].copy()
l["site"] = l.site.replace({"Bandagam-Batapora terraces": "Bandagam–Batapora terraces", "all terraces": "All terraces", "other terraces": "All other terraces", "other flat land": "Other flat, raised land"})
frame(l[["site", "drop_ha", "reverse_ha", "net_ha"]].round(0).rename(columns={"site": "Site", "drop_ha": "Vegetated → low (ha)", "reverse_ha": "Low → vegetated (ha)", "net_ha": "Net (ha)"}))
rk = float(l[l.site == "Rangeen Kultreh terraces"].net_ha.iloc[0]); b2 = float(l[l.site == "Bandagam–Batapora terraces"].net_ha.iloc[0]); al = l[l.site == "All terraces"].iloc[0]
ot = stock[stock.site == "other terraces"].set_index("period").loc[order[:4]].below_035_ha
note(
    f"<b>The three-decade figure is indicative only.</b> The drop test from 1993–1998 to 2023–2025 gives a net +{rk:.0f} ha at Rangeen Kultreh and +{b2:.0f} ha at Bandagam–Batapora, about {rk + b2:.0f} ha together. "
    "I do not put that on the same footing as the 2013–2025 figures, for three reasons. The two site boxes were drawn after the pattern had been seen. "
    f"Over all terraces the same test gives {al.drop_ha:.0f} ha of loss against {al.reverse_ha:.0f} ha in the opposite direction. "
    f"And before 2013 the low-vegetation land on the other terraces moves between {ot.min():.0f} and {ot.max():.0f} ha from one period to the next, which is as large as the signal. "
    "The Rangeen Kultreh part is firm because all of it happens after 2016. The Bandagam–Batapora part shows a direction and not a reliable amount. This long series also applied the Landsat 8/9 adjustment in the reverse direction and is being recomputed.",
    "caution",
)
