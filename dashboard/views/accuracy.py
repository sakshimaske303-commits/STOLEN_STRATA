import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import os

from lib import GREY, OCHRE, ORANGE, ROSE, TEAL, V2, caption, frame, mapfile, note, numbers, picture, show, style_fig, table
from style import page_title

page_title("Accuracy Sample", "What the flagged land is today, point by point")
n = numbers()
pts = mapfile("accuracy_points.csv")
pa = table("west_extension/kiln_rule_accuracy.csv")
po = table("west_extension/pooled_accuracy_result.csv")
res = pa[pa["sample"] == "pooled"].rename(columns={"measure": "reference_class"})
bp = table("west_extension/accuracy_by_labelling_pass.csv")
bt = table("west_extension/accuracy_points_by_terrace.csv")
pb = table("west_extension/kiln_rule_before.csv")
br = pb[pb["sample"] == "pooled"]
bl = table("west_extension/accuracy_before_pass.csv").rename(columns={"image_date": "before_date"})
l2 = table("west_extension/accuracy_sample2_labels_in_progress.csv").rename(columns={"before_basis": "basis"})
bl = pd.concat([bl[["point_id", "before_label", "before_date", "basis"]], l2[["point_id", "before_label", "before_date", "basis"]]])

st.markdown(
    """
A satellite test says vegetation was lost. It does not say what replaced it. To find out I drew **two random samples of points** on the terraces,
240 in all: 60 from pixels flagged by the strict test, 120 from pixels flagged only by the drop test and 60 from pixels flagged by neither.
The points were shuffled, and I labelled each one against the most recent satellite imagery without knowing which group it came from.
In the first sample (points 1–120) the date of that imagery was not recorded; in the second (121–240) it was, and ranges from 2022 to 2026.
The figures below pool the two samples, with the edges of kiln fields judged under one written rule (see below).
"""
)

NAME = {"A_strict": "Flagged by strict test", "B_drop_only": "Flagged by drop test only", "C_not_flagged": "Not flagged"}
CLS = [("kiln", "Inside a brick-kiln field", ORANGE), ("built_up", "Built-up", ROSE), ("road", "Road", "#8E6BBF"), ("bare_other", "Other bare ground", OCHRE),
       ("vegetated", "Still vegetated", TEAL), ("unclear", "Unclear", GREY)]
tab = pd.crosstab(pts.stratum, pts.final).reindex(columns=[c[0] for c in CLS], fill_value=0)
fig = go.Figure()
for key, lab, colr in CLS:
    fig.add_trace(go.Bar(y=[NAME[s] for s in tab.index], x=tab[key] / tab.sum(axis=1) * 100, name=lab, orientation="h", customdata=tab[key],
                         marker=dict(color=colr, line=dict(color="#0A0E1A", width=2)), hovertemplate="%{y}<br>" + lab + ": %{customdata} points (%{x:.0f}%)<extra></extra>"))
fig.update_layout(barmode="stack", xaxis_title="Share of sample points (%)", yaxis=dict(autorange="reversed"), xaxis_range=[0, 100])
show(style_fig(fig, 330))

t2 = tab.copy(); t2.insert(0, "Points", tab.sum(axis=1))
ha = res.drop_duplicates("stratum").set_index("stratum").stratum_ha
t2.insert(1, "Stratum area (ha)", [round(ha[s]) for s in t2.index])
t2.index = [NAME[s] for s in t2.index]
frame(t2.rename(columns={k: l for k, l, _ in CLS}).reset_index(names="Stratum"))

r = lambda x: int(x * 100 + 0.5)
k = res[res.reference_class == "kiln"].set_index("stratum"); nv = res[res.reference_class == "not vegetated"].set_index("stratum")
st.markdown(
    f"""
**The tests are right that the vegetation is gone.** All {int(nv.hits['A_strict'])} strict points and {int(nv.hits['B_drop_only'])} of 120 drop-only points
({nv.share['B_drop_only'] * 100:.0f}%) are not vegetated today; one more could not be told and is not counted. Scaled by stratum area, about
**{n['notveg_ha']:.0f} ha** of the 331 ha flagged is not vegetated today (roughly {n['notveg_lo']:.0f}–{n['notveg_hi']:.0f} ha).

**They differ in what the land became.** {k.share['A_strict'] * 100:.0f}% of strict detections lie inside a kiln field
(95% interval {r(k.ci95_low['A_strict'])}–{r(k.ci95_high['A_strict'])}%). Drop-only detections are a mixture: about half kiln field
({r(k.share['B_drop_only'])}%, interval {r(k.ci95_low['B_drop_only'])}–{r(k.ci95_high['B_drop_only'])}%), about a quarter built-up land and roads, about an eighth other bare ground.

Scaled by stratum area that is about **{k.est_ha['A_strict']:.0f} ha + {k.est_ha['B_drop_only']:.0f} ha = {n['kiln_ha']:.0f} ha** inside brick-kiln fields,
with a 95% interval of roughly {n['kiln_lo']:.0f} to {n['kiln_hi']:.0f} ha.
"""
)

st.markdown("---")
st.markdown("### Where a kiln field ends: one rule for both samples")
c1, c2 = st.columns([3, 2])
with c1:
    f = bp[bp.stratum != "C_not_flagged"]
    first = f[f.definition.str.startswith("first pass")].est_ha.sum()
    xs = ["First sample", "Second sample", "Both samples pooled"]
    fig = go.Figure()
    for lab, src, colr in (("As first labelled", po, GREY), ("Under one rule", pa, ORANGE)):
        kd = src[(src.stratum == "A_and_B") & (src.measure == "kiln")].set_index("sample")
        ys = [kd.est_ha[s] for s in ("draw 1", "draw 2", "pooled")]
        lo = [kd.est_ha_low[s] for s in ("draw 1", "draw 2", "pooled")]; hi = [kd.est_ha_high[s] for s in ("draw 1", "draw 2", "pooled")]
        fig.add_trace(go.Bar(x=xs, y=ys, name=lab, marker=dict(color=colr, line=dict(color="#0A0E1A", width=2)),
                             error_y=dict(type="data", symmetric=False, array=[h - y for h, y in zip(hi, ys)], arrayminus=[y - l for l, y in zip(lo, ys)], color="#F4EBD9"),
                             text=[f"{v:.0f} ha" for v in ys], textposition="inside", hovertemplate="%{x}: %{y:.0f} ha<extra>" + lab + "</extra>"))
    fig.update_layout(barmode="group", yaxis_title="Flagged land inside a kiln field (ha)", legend=dict(orientation="h", y=1.02, yanchor="bottom", x=0))
    show(style_fig(fig, 400))
with c2:
    st.markdown(
        f"""
As first labelled, the two samples disagreed on how much of the flagged land is kiln land: about **{n['kiln_old1_ha']:.0f} ha** by the first
and **{n['kiln_old2_ha']:.0f} ha** by the second. They had placed bare worked ground, tracks and cleared plots at the edge of a kiln field differently.

So I wrote one rule down: a point is in a kiln field if it is on a kiln, pit, brick rows or kiln shed, or on worked ground, a track or a yard
inside the worked area with bricks, a pit or a kiln **within about 100 m** and no house, public road or crop field in between.
The 86 flagged points whose label depended on their setting were relabelled under it.

Under the one rule the samples agree: **{n['kiln_draw1_ha']:.0f} ha** and **{n['kiln_draw2_ha']:.0f} ha**, {n['kiln_ha']:.0f} ha pooled.
Most of it is recognised from its setting, not from what lies at the point; kiln-field outlines on dated imagery would be an independent check.
"""
    )

st.markdown("---")
st.markdown("### Were the flagged points vegetated before?")
c1, c2 = st.columns([3, 2])
B = lambda s, m: br[(br.stratum == s) & (br.measure == m)].iloc[0]
with c1:
    BCLS = [("vegetated before", "Vegetated in 2013–15 imagery", TEAL), ("not vegetated before", "Not vegetated", OCHRE), ("unclear before", "Unclear", GREY)]
    rows = [("A_strict", "Flagged by strict test"), ("B_drop_only", "Flagged by drop test only"), ("A_and_B", "Flagged land together")]
    fig = go.Figure()
    for m, lab, colr in BCLS:
        v = [B(s, m) for s, _ in rows]
        fig.add_trace(go.Bar(y=[l for _, l in rows], x=[x.hits / x.n * 100 for x in v], name=lab, orientation="h", customdata=[int(x.hits) for x in v],
                             marker=dict(color=colr, line=dict(color="#0A0E1A", width=2)), hovertemplate="%{y}<br>" + lab + ": %{customdata} points (%{x:.0f}%)<extra></extra>"))
    fig.update_layout(barmode="stack", xaxis_title="Share of flagged sample points (%)", yaxis=dict(autorange="reversed"), xaxis_range=[0, 100])
    show(style_fig(fig, 300))
    with st.expander("The flagged points that were not clearly vegetated in the older image"):
        x = bl[bl.before_label != "vegetated"].merge(pts[pts.stratum != "C_not_flagged"][["point_id", "final"]], on="point_id")
        frame(x.rename(columns={"point_id": "Point", "before_label": "Older image", "before_date": "Image date", "basis": "What is seen at the point", "final": "Present class"})
              [["Point", "Older image", "Image date", "What is seen at the point", "Present class"]])
with c2:
    va, vb, vt = B("A_strict", "vegetated before"), B("B_drop_only", "vegetated before"), B("A_and_B", "vegetated before")
    kt = B("A_and_B", "vegetated before and inside a kiln field today"); gt = B("A_and_B", "vegetated before and not vegetated today")
    st.markdown(
        f"""
The labels above describe the present state. For the earlier state, each of the 180 flagged points was looked up in Google Earth Pro imagery of
2013–2015, mostly one image of September 2014.

Vegetation is visible at **{int(vt.hits)} of 180** points: {int(va.hits)} of 60 strict points
and {int(vb.hits)} of 120 drop-only points ({vb.share * 100:.0f}%).

Seven of the points that were not vegetated then are counted as kiln field today. Restricted to points the older image also shows as
vegetated, the kiln-field estimate is about **{kt.est_ha:.0f} ha** (roughly {kt.est_ha_low:.0f}–{kt.est_ha_high:.0f} ha) instead of {n['kiln_ha']:.0f} ha.
Land vegetated then and not vegetated today, whatever it became, is about {gt.est_ha:.0f} ha.
"""
    )
caption("\"Vegetated\" in the older image is a low bar: crop fields and orchards, but also rough grass and scattered trees on dry ground. "
        "In the first sample the pass was not blind, since only flagged points were looked at; the second sample was labelled blind. One image shows one day while the tests use the peak of the year.")

note(
    "<b>Read these numbers with four cautions.</b><br>"
    "1. <b>The kiln figure rests on one written rule for where a kiln field ends,</b> written after the two samples were compared, and applied by one labeller (see above).<br>"
    "2. <b>The strict stratum is mostly one place.</b> 44 of its 60 points fall on one terrace and 52 on the two Rangeen Kultreh terraces (51 of them inside the kiln field), because that is where most of the strict-test area lies.<br>"
    "3. <b>One labeller.</b> For roughly eight uncertain points of the first sample I took a second opinion; the rest I labelled alone. There is no second, independent labeller yet.<br>"
    f"4. <b>Missed kiln land is not estimated.</b> One of 60 unflagged points was inside a kiln field, which gives a range ({k.est_ha_low['C_not_flagged']:.0f} to {round(k.est_ha_high['C_not_flagged'], -1):,.0f} ha) too wide to mean anything.",
    "caution",
)
caption("20 of the 60 unflagged points also look non-vegetated in the recent image, because a dry-season picture of a karewa is largely brown. Present-day bareness on its own means little; the tests rest on change in the satellite record.")

st.markdown("---")
st.markdown("### A ground check at Lethpora")
fp = table("phase1_delineation/field_photo_check.csv")
cols = st.columns(4)
for c, r_ in zip(cols, fp.itertuples()):
    with c:
        picture(os.path.join(V2, "phase1_delineation", "field_photos", r_.photo), f"{r_.lat:.5f} N, {r_.lon:.5f} E")
st.markdown(
    f"""
Four photographs I took on **3 September 2026** on the Lethpora tableland beside the national highway, with a GPS camera that prints the position
on each image. They show tilled saffron beds and scattered trees. The earlier terrace map left this spot out; it is the reason the terrace rule was rebuilt.

On the new map all four fall **inside terrace {int(fp.terrace_id.iloc[0])}** ({fp.terrace_km2.iloc[0]:.1f} km²), {fp.m_inside_terrace_edge.min():.0f}–{fp.m_inside_terrace_edge.max():.0f} m from its edge,
and **none is on flagged land**: the nearest drop-test pixels are about {round(fp.m_to_drop_only.min(), -1):.0f} m away, the nearest strict-test pixels about {fp.m_to_strict.min() / 1000:.1f} km.
The ground, the map and the tests agree on this spot: a cultivated tableland, not converted.
"""
)
caption("One place on one day, so this is a check on the map and not a validation of it. No fieldwork was done at either kiln belt.")

