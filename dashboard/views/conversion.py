import plotly.graph_objects as go
import streamlit as st

from lib import GREY, OCHRE, ORANGE, TEAL, bars, caption, frame, note, numbers, show, style_fig, table
from style import page_title

page_title("Conversion 2013–2025", "Land that was vegetated and is not any more, inside one sensor")
n = numbers()
cs = table("west_extension/conversion_by_stratum_wide.csv")
dt = table("west_extension/drop_test_by_stratum_wide.csv")
ct = table("west_extension/conversion_by_terrace_wide.csv")
dtt = table("west_extension/drop_test_by_terrace_wide.csv")
sens_d = table("west_extension/drop_test_sensitivity.csv")
sens_s = table("phase2_timeseries/conversion_sensitivity.csv")

st.markdown(
    """
Both tests compare two three-year windows, 2013–2015 and 2023–2025, in the Landsat 8/9 series alone, using each pixel's
**yearly peak NDVI**. A field that is bare in winter or at harvest still has a high peak; ground that has been stripped stays low all year.

- **Strict test.** Peak at least 0.35 in each of 2013, 2014, 2015 and below 0.25 in each of 2023, 2024, 2025.
- **Drop test.** Median peak at least 0.45 early, below 0.40 late, and a fall of at least 0.20. Added because a kiln field at 30 m is a mixture of kilns, drying rows, tracks and weeds, and the strict test misses most of it.

Each test is also run backwards (low to high) as a measure of noise, and on two kinds of comparison land.
"""
)

a = cs[(cs.series == "Landsat 8/9 only") & (cs.early == "2013-2014-2015") & (cs.late == "2023-2024-2025") & (cs.part == "whole box")].set_index("stratum")
d = dt[dt.test == "OLI 13-15>23-25"].groupby("stratum")[["drop_ha", "reverse_ha"]].sum()
order = ["terraces", "other_flat", "rest"]
label = {"terraces": "Terraces", "other_flat": "Other flat, raised land", "rest": "Rest of the box"}
km2 = a.stratum_km2
t1 = [dict(Stratum=label[k], **{"Area (km²)": round(km2[k], 1), "Strict test (ha)": round(a.veg_to_bare_ha[k], 1), "Strict, reverse (ha)": round(a.bare_to_veg_ha[k], 1),
                               "Strict (% of area)": round(a.veg_to_bare_pct[k], 2), "Drop test (ha)": round(d.drop_ha[k], 1), "Drop, reverse (ha)": round(d.reverse_ha[k], 1),
                               "Drop (% of area)": round(d.drop_ha[k] / km2[k], 2)}) for k in order]
import pandas as pd
t1 = pd.DataFrame(t1)

c1, c2 = st.columns(2)
for col, key, title, colr in ((c1, "Strict (% of area)", "Strict test", ORANGE), (c2, "Drop (% of area)", "Drop test", OCHRE)):
    with col:
        st.markdown(f"#### {title}: share of each kind of land converted")
        fig = go.Figure(bars(t1.Stratum, t1[key], [colr, GREY, GREY], [f"{v:.2f}%" for v in t1[key]]))
        fig.update_layout(showlegend=False, yaxis_title="Converted, % of area", yaxis_range=[0, t1[key].max() * 1.25])
        show(style_fig(fig, 340, legend_top=False))
frame(t1)
caption(f"By the strict test terraces convert about {a.veg_to_bare_pct['terraces'] / a.veg_to_bare_pct['other_flat']:.0f} times faster than other flat, raised land, "
        f"and by the drop test about {(d.drop_ha['terraces'] / km2['terraces']) / (d.drop_ha['other_flat'] / km2['other_flat']):.0f} times faster. "
        "These rates divide by the whole area of each kind of land, not by the part that was vegetated in 2013–2015. Off the terraces the drop test picks up a great deal of change in both directions, which is what fields, building and road works produce; those rows are not interpreted further.")

st.markdown("---")
st.markdown("### It is concentrated")
top = dtt.sort_values("ha", ascending=False).head(15).merge(ct[["terrace_id", "veg_to_bare_ha"]], on="terrace_id")
top["name"] = "Terrace " + top.terrace_id.astype(str)
fig = go.Figure()
fig.add_trace(go.Bar(y=top.name, x=top.veg_to_bare_ha, orientation="h", name="Strict test", marker=dict(color=ORANGE, line=dict(color="#0A0E1A", width=2)), hovertemplate="%{y}: %{x:.1f} ha<extra>strict</extra>"))
fig.add_trace(go.Bar(y=top.name, x=top.ha, orientation="h", name="Drop test", marker=dict(color=OCHRE, line=dict(color="#0A0E1A", width=2)), hovertemplate="%{y}: %{x:.1f} ha<extra>drop</extra>"))
fig.update_layout(barmode="group", yaxis=dict(autorange="reversed"), xaxis_title="Converted land (ha)")
show(style_fig(fig, 520))
s1, d1, d5 = int((ct.veg_to_bare_ha >= 1).sum()), int((dtt.ha >= 1).sum()), int((dtt.ha >= 5).sum())
two = ct.sort_values("veg_to_bare_ha", ascending=False).head(2).veg_to_bare_ha.sum()
caption(f"The 15 terraces with most drop-test conversion, of {n['terraces']}. By the strict test {s1} terraces have a hectare or more, and two adjoining terraces at Rangeen Kultreh "
        f"(9 and 3) hold {two:.1f} ha, {two / n['strict_ha'] * 100:.0f}% of the total. By the drop test {d1} terraces lose a hectare or more and {d5} lose five or more. "
        "Terrace numbers are those of the wide-box run; locations are on the Interactive Map page.")

st.markdown("---")
st.markdown("### Does it depend on the thresholds?")
c1, c2 = st.columns(2)
with c1:
    st.markdown("#### Drop test: 27 variants")
    fig = go.Figure(go.Scatter(x=sens_d.terraces_net_ha, y=sens_d.ratio_vs_other_flat, mode="markers", marker=dict(size=11, color=OCHRE, line=dict(color="#0A0E1A", width=2)),
                               customdata=sens_d[["early_min", "late_max", "fall_min"]],
                               hovertemplate="early ≥ %{customdata[0]}, late < %{customdata[1]}, fall ≥ %{customdata[2]}<br>net %{x:.0f} ha, %{y:.1f}× other flat land<extra></extra>"))
    fig.add_hline(y=1, line=dict(color=GREY, dash="dot"), annotation_text="same rate as other flat land", annotation_font_color=GREY)
    fig.update_layout(showlegend=False, xaxis_title="Net conversion on terraces (ha)", yaxis_title="Terraces ÷ other flat land", yaxis_range=[0, sens_d.ratio_vs_other_flat.max() * 1.15])
    show(style_fig(fig, 360, legend_top=False))
    caption(f"Net of reverse change, {sens_d.terraces_net_ha.min():.0f} to {sens_d.terraces_net_ha.max():.0f} ha; terraces convert {sens_d.ratio_vs_other_flat.min():.1f} to {sens_d.ratio_vs_other_flat.max():.1f} times faster than other flat land in every variant.")
with c2:
    st.markdown("#### Strict test: 24 variants (original box)")
    fig = go.Figure(go.Scatter(x=sens_s.terraces_ha, y=sens_s.share_on_terraces_5_and_3 * 100, mode="markers", marker=dict(size=11, color=ORANGE, line=dict(color="#0A0E1A", width=2)),
                               customdata=sens_s[["bare_below", "veg_at_least", "years_required"]],
                               hovertemplate="bare < %{customdata[0]}, vegetated ≥ %{customdata[1]}, %{customdata[2]} years<br>%{x:.0f} ha, %{y:.0f}% at Rangeen Kultreh<extra></extra>"))
    fig.update_layout(showlegend=False, xaxis_title="Conversion on terraces (ha)", yaxis_title="Share on the Rangeen Kultreh terraces (%)", yaxis_range=[0, 105])
    show(style_fig(fig, 360, legend_top=False))
    caption(f"{sens_s.terraces_ha.min():.0f} to {sens_s.terraces_ha.max():.0f} ha; in every variant {sens_s.share_on_terraces_5_and_3.min() * 100:.0f}% to {sens_s.share_on_terraces_5_and_3.max() * 100:.0f}% of it is on the Rangeen Kultreh terraces.")

note("<b>Do the instruments agree?</b> For the window Landsat 7 can cover (2013–2015 to 2019–2021), Landsat 7 alone gives 70.8 ha by the strict test on terraces and Landsat 8 gives 68.6 ha; "
     "Landsat 7 confirms 86% of the Landsat 8 drop-test pixels. Sentinel-2 puts 97% of the strict-test terrace pixels below 0.25 in each of 2023, 2024 and 2025.", "note")
note("<b>What the tests cannot tell apart.</b> They detect loss of vegetation from any cause. Off the terraces the largest clusters are a hospital campus under construction at Awantipora, "
     "open water replacing floating vegetation in Dal Lake, road works and shifts of the Jhelum channel. That is why the kiln figure comes from the labelled sample and not from the tests alone.", "caution")
