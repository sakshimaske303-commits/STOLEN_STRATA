import plotly.graph_objects as go
import streamlit as st

from lib import GREY, OCHRE, ORANGE, TEAL, caption, frame, mapfile, note, numbers, show, stats, style_fig, table
from style import page_title

page_title("Terrace Map", "Finding the tablelands from an elevation model")
n, sm = numbers(), mapfile("summary.json")
gs = table("phase1_delineation/geology_summary.csv")
ga = table("phase1_delineation/geology_agreement.csv").set_index("Unnamed: 0").value
th = table("phase1_delineation/geology_threshold_table.csv")
ds = table("west_extension/delineation_sensitivity.csv")

stats([("Flat tops found", sm["flat_tops"], f"{sm['flat_tops_scarp_025']} pass the scarp rule"),
       ("Kept as terraces", n["terraces"], "scarp share of 0.25 or more"),
       ("Terrace area", f"{n['terrace_km2']:.1f} km²", f"other flat, raised land: {n['flat_km2']:.1f} km²"),
       ("On Karewa formations", f"{float(ga['users_accuracy']) * 100:.0f}%", "67–89% if the geological map is shifted by up to 600 m")])
st.markdown(
    """
### The rule

The earlier version selected cells with a high topographic position index. That picks out rims and spurs and leaves the flat
plateau interior out; my own field photographs at Lethpora fell outside every polygon it produced. The new rule looks for the
flat top itself and then asks whether it is bounded by scarps.

1. **Flat and raised.** From the Copernicus 30 m elevation model: slope under 4°, more than 15 m above the nearest drainage line, below 1,950 m.
2. **Connected.** Cells are cleaned and grouped into flat tops of at least 0.05 km².
3. **Bounded by scarps.** For each flat top, the share of a ring just outside it that is steeper than 6°. A tableland drops away on most sides; an alluvial fan or a valley-side apron slopes gently into its surroundings.
4. **Cut-off.** A flat top is a terrace if its scarp share is 0.25 or more.
"""
)

st.markdown("### Checked against a geological map")
c1, c2 = st.columns([3, 2])
with c1:
    g = gs.copy()
    g["layer"] = g.layer.replace({"v2 terraces (scarp share >= 0.25)": "Terraces (scarp share ≥ 0.25)", "prototype: scarp_bounded": "Flat tops: clearly scarp-bounded",
                                  "prototype: ambiguous": "Flat tops: in between", "prototype: rejected": "Flat tops: rejected", "whole study box below 2000 m": "Whole box below 2,000 m"})
    fig = go.Figure()
    for col, name, colr in (("on_karewa_fm", "Karewa formations", TEAL), ("on_reworked", "Reworked karewa sediments", OCHRE), ("on_alluvium", "Alluvium", GREY)):
        fig.add_trace(go.Bar(y=g.layer, x=g[col] * 100, name=name, orientation="h", marker=dict(color=colr, line=dict(color="#0A0E1A", width=2)),
                             hovertemplate="%{y}<br>" + name + ": %{x:.0f}%<extra></extra>"))
    fig.update_layout(barmode="stack", xaxis_title="Share of area (%)", yaxis=dict(autorange="reversed"), xaxis_range=[0, 100])
    show(style_fig(fig, 360))
    caption("Original study box only. Geology from Dar and Zeeden (2020, Figure 2), georeferenced by hand.")
with c2:
    st.markdown(
        f"""
**{float(ga['users_accuracy']) * 100:.0f}%** of the terrace area lies on Karewa formations and the rest on alluvium. The flat tops
the rule rejects are a mixture, which is what a fan is.

**The weak direction is coverage.** The terraces include only **{float(ga['producers_accuracy_all_karewa_fm']) * 100:.0f}%** of the
Karewa formation area on that map, and {float(ga['producers_accuracy_flat_karewa_fm']) * 100:.0f}% of the flat part of it.
Karewa ground without a bounding scarp is not in the map. The unit of study is scarp-bounded tableland, not the Karewa Group as a whole.
"""
    )

note(
    "<b>How far this check goes.</b> The geological map is a schematic figure from a journal article with a positional error of roughly a kilometre. "
    "It covers the original box only: the strip west of about 74.66° E, which includes the Bandagam–Batapora belt, has no geological check. "
    "The same map was used to choose the 0.25 cut-off, from a table of a few dozen flat tops, so the agreement above is not a fully independent test. "
    "Of the flat tops that pass the scarp rule, four are dropped because they match flat tops removed in the original box after a first-pass review of terrain and imagery (foothill aprons and valley floors, 1.2 km², of which 0.5 km² inside the box; I have not yet confirmed those labels myself, but they hold 0.09 ha of strict-test conversion and none by the drop test, so no figure depends on them), and three fall below the minimum size at the edge of the box. "
    "A 460-point reference sample was drawn for the terrace map and has not been labelled, so the map has no accuracy figure of its own.",
    "caution",
)

c1, c2 = st.columns(2)
with c1:
    st.markdown("#### Choosing the cut-off")
    frame(th.rename(columns={"scarp_min": "Scarp share at least", "polygons_kept": "Flat tops kept", "precision": "Share of kept on Karewa fm.", "recall": "Share of Karewa flat tops kept",
                             "area_weighted_share_on_karewa": "Area share on Karewa fm."}))
    caption("Only flat tops large enough for the geological map to resolve are compared.")
with c2:
    st.markdown("#### Does the result depend on the cut-offs?")
    d = ds[["slope_max_deg", "hand_min_m", "terraces", "terrace_km2", "strict_ha", "drop_ha", "strict_ratio_vs_other_flat", "drop_ratio_vs_other_flat"]].round(1)
    frame(d.rename(columns={"slope_max_deg": "Slope under (°)", "hand_min_m": "Height above drainage over (m)", "terraces": "Terraces", "terrace_km2": "Area (km²)", "strict_ha": "Strict test (ha)",
                            "drop_ha": "Drop test (ha)", "strict_ratio_vs_other_flat": "Strict: terraces ÷ other flat", "drop_ratio_vs_other_flat": "Drop: terraces ÷ other flat"}))
    caption(f"Nine versions of the rule. Terrace area runs from {ds.terrace_km2.min():.0f} to {ds.terrace_km2.max():.0f} km²; the strict conversion stays between "
            f"{ds.strict_ha.min():.0f} and {ds.strict_ha.max():.0f} ha and terraces convert faster than other flat land in every version, a contrast that comes from the same two kiln belts. "
            "This run works on the raster and does not apply the review removals or the size filter after clipping to the box, so its base row has 186 terraces (173.9 km²) against 180 (173.3 km²) elsewhere.")
