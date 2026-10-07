import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from lib import GREY, OCHRE, ORANGE, ROSE, TEAL, caption, frame, mapfile, note, numbers, show, style_fig, table
from style import page_title

page_title("Accuracy Sample", "What the flagged land is today, point by point")
n = numbers()
pts = mapfile("accuracy_points.csv")
res = table("west_extension/accuracy_result.csv")
bp = table("west_extension/accuracy_by_labelling_pass.csv")
bt = table("west_extension/accuracy_points_by_terrace.csv")

st.markdown(
    """
A satellite test says vegetation was lost. It does not say what replaced it. To find out I drew **120 random points** on the terraces:
25 from pixels flagged by the strict test, 60 from pixels flagged only by the drop test and 35 from pixels flagged by neither.
The points were shuffled, and I labelled each one against the 2026 satellite view in Google Maps without knowing which group it came from.
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
**The tests are right that the vegetation is gone.** All 25 strict points and {int(nv.hits['B_drop_only'])} of 60 drop-only points
({nv.share['B_drop_only'] * 100:.0f}%) are not vegetated today.

**They differ in what the land became.** {k.share['A_strict'] * 100:.0f}% of strict detections lie inside a kiln field
(95% interval {r(k.ci95_low['A_strict'])}–{r(k.ci95_high['A_strict'])}%). Drop-only detections are a mixture: about a quarter kiln field
({r(k.share['B_drop_only'])}%, interval {r(k.ci95_low['B_drop_only'])}–{r(k.ci95_high['B_drop_only'])}%), about as much again built-up land and roads, about as much other bare ground.

Scaled by stratum area that is about **{k.est_ha['A_strict']:.0f} ha + {k.est_ha['B_drop_only']:.0f} ha = {n['kiln_ha']:.0f} ha** inside brick-kiln fields,
with a 95% interval of roughly {n['kiln_lo']:.0f} to {n['kiln_hi']:.0f} ha.
"""
)

st.markdown("---")
st.markdown("### How much rests on the second look")
c1, c2 = st.columns([3, 2])
with c1:
    f = bp[bp.stratum != "C_not_flagged"]
    first = f[f.definition.str.startswith("first pass")].set_index("stratum"); second = f[f.definition.str.startswith("added by second")].set_index("stratum")
    xs = [NAME[s] for s in first.index] + ["Flagged land together"]
    y1 = list(first.est_ha) + [first.est_ha.sum()]; y2 = list(second.est_ha) + [second.est_ha.sum()]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=xs, y=y1, name="Point centre is a kiln, drying row or brick stack (first pass)", marker=dict(color=ORANGE, line=dict(color="#0A0E1A", width=2)),
                         text=[f"{v:.0f} ha" for v in y1], textposition="inside", hovertemplate="%{x}: %{y:.0f} ha<extra>first pass</extra>"))
    fig.add_trace(go.Bar(x=xs, y=y2, name="Bare or road point inside a kiln field (second pass)", marker=dict(color="#8A4A2A", line=dict(color="#0A0E1A", width=2)),
                         text=[f"{v:.0f} ha" for v in y2], textposition="inside", hovertemplate="%{x}: %{y:.0f} ha<extra>second pass</extra>"))
    fig.update_layout(barmode="stack", yaxis_title="Estimated area (ha)", legend=dict(orientation="h", y=1.02, yanchor="bottom", x=0))
    show(style_fig(fig, 400))
with c2:
    st.markdown(
        f"""
At close zoom, bare worked ground inside a kiln field cannot be told from any other bare ground. So the 68 points first labelled
bare or road were looked at a second time, one zoom level out, with one question: is this point inside a brick-kiln field?

Counting only the first pass, the estimate is about **{n['kiln_first_ha']:.0f} ha**. The second pass adds about **{n['kiln_second_ha']:.0f} ha**.

So the {n['kiln_ha']:.0f} ha is land *inside brick-kiln fields*. Roughly {n['kiln_first_ha']:.0f} ha of it is kilns and rows of bricks themselves;
the rest is the worked, bare ground between them.
"""
    )

note(
    "<b>Read these numbers with four cautions.</b><br>"
    "1. <b>The sample shows today, not 2013.</b> It cannot confirm that a point was vegetated before. That rests on the Landsat record. A check against older high-resolution imagery is prepared and not finished.<br>"
    f"2. <b>The strict stratum is mostly one place.</b> {int(bt[(bt.stratum == 'A_strict')].points.max())} of its 25 points fall on one terrace and 21 fall in the Rangeen Kultreh kiln field, because that is where most of the strict-test area lies.<br>"
    "3. <b>One labeller, one image date.</b> For roughly eight uncertain points I took a second opinion; the rest I labelled alone. There is no second labeller yet.<br>"
    f"4. <b>Missed kiln land is not estimated.</b> One of 35 unflagged points was inside a kiln field, which gives a range ({k.est_ha_low['C_not_flagged']:.0f} to {round(k.est_ha_high['C_not_flagged'], -1):,.0f} ha) too wide to mean anything.",
    "caution",
)
caption("13 of the 35 unflagged points also look non-vegetated in the 2026 image, because a dry-season picture of a karewa is largely brown. Present-day bareness on its own means little; the tests rest on change in the satellite record.")
