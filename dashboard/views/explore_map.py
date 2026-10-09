import plotly.graph_objects as go
import streamlit as st

from lib import GREY, OCHRE, ORANGE, ROSE, TEAL, caption, mapfile, numbers, show
from style import CREAM, page_title

page_title("Interactive Map", "Terraces, flagged land and the 240 sample points")
n = numbers()
terr, flag, pts = mapfile("terraces.geojson"), mapfile("flagged.geojson"), mapfile("accuracy_points.csv")

VIEWS = {"Whole study box": (33.975, 74.85, 9.6), "Rangeen Kultreh kiln field": (33.942, 74.850, 13.2), "Bandagam–Batapora belt": (34.02, 74.665, 11.8), "Pampore tablelands": (33.985, 74.94, 11.8)}
c1, c2, c3 = st.columns([2, 2, 3])
view = c1.selectbox("Go to", list(VIEWS))
base = c2.radio("Background", ["Satellite", "Street map"], horizontal=True)
layers_on = c3.multiselect("Show", ["Terraces", "Strict test", "Drop test only", "Sample points"], default=["Terraces", "Strict test", "Drop test only", "Sample points"])

lat, lon, zoom = VIEWS[view]
fig = go.Figure()
if "Terraces" in layers_on:
    props = [f["properties"] for f in terr["features"]]
    fig.add_trace(go.Choroplethmapbox(
        geojson=terr, featureidkey="properties.terrace_id", locations=[p["terrace_id"] for p in props], z=[1] * len(props),
        colorscale=[[0, TEAL], [1, TEAL]], showscale=False, marker=dict(opacity=0.18, line=dict(color="#7FE3DA", width=1.2)), name="Terraces",
        customdata=[[p["area_km2"], p["scarp_frac"], p["strict_ha"], p["drop_ha"]] for p in props],
        hovertemplate="<b>Terrace %{location}</b><br>%{customdata[0]:.2f} km², scarp share %{customdata[1]:.2f}<br>strict test %{customdata[2]:.1f} ha · drop test %{customdata[3]:.1f} ha<extra></extra>"))
if "Sample points" in layers_on:
    CLS = [("kiln", "Sample: inside a kiln field", ORANGE), ("built_up", "Sample: built-up", ROSE), ("road", "Sample: road", "#B79CE0"), ("bare_other", "Sample: other bare ground", "#E6C65A"),
           ("vegetated", "Sample: still vegetated", "#5ED3C8"), ("unclear", "Sample: unclear", GREY)]
    STR = {"A_strict": "flagged by strict test", "B_drop_only": "flagged by drop test only", "C_not_flagged": "not flagged"}
    for key, lab, colr in CLS:
        d = pts[pts.final == key]
        fig.add_trace(go.Scattermapbox(lat=d.lat, lon=d.lon, mode="markers", name=lab, marker=dict(size=11, color=colr, opacity=0.95),
                                       customdata=list(zip(d.point_id, d.stratum.map(STR), d.before_label.fillna("not checked"), d.p90_2013_15, d.p90_2023_25)),
                                       hovertemplate="<b>Point %{customdata[0]}</b> · " + lab[8:] + "<br>%{customdata[1]}<br>2013–15 image: %{customdata[2]}<br>peak NDVI %{customdata[3]:.2f} → %{customdata[4]:.2f}<extra></extra>"))
layers = []
if base == "Satellite":
    layers.append(dict(sourcetype="raster", below="traces", sourceattribution="Imagery: Esri, Maxar, Earthstar Geographics",
                       source=["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"]))
for f in flag["features"]:
    name = "Strict test" if f["properties"]["test"] == "strict" else "Drop test only"
    if name in layers_on:
        layers.append(dict(sourcetype="geojson", source=f, type="fill", color=ORANGE if name == "Strict test" else "#F2D24B", opacity=0.75, below="traces"))
fig.update_layout(mapbox=dict(style="white-bg" if base == "Satellite" else "open-street-map", center=dict(lat=lat, lon=lon), zoom=zoom, layers=layers),
                  height=680, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="rgba(0,0,0,0)", uirevision=view + base,
                  legend=dict(bgcolor="rgba(10,14,26,0.85)", font=dict(color=CREAM, size=12), x=0.01, y=0.99, yanchor="top"))
show(fig)

sq = lambda c: f'<span style="display:inline-block; width:0.8em; height:0.8em; background:{c}; border-radius:2px; margin-right:0.3em;"></span>'
st.markdown(
    f"""
<p>{sq(ORANGE)}<b>Strict test</b> ({flag['features'][0]['properties']['ha']:.0f} ha on terraces): vegetated in each of 2013–2015, bare in each of 2023–2025. &nbsp;
{sq('#F2D24B')}<b>Drop test only</b> ({flag['features'][1]['properties']['ha']:.0f} ha): a large fall in peak NDVI that the strict test does not catch. &nbsp;
{sq('#7FE3DA')}<b>Terraces</b> ({n['terraces']}, {n['terrace_km2']:.1f} km²).</p>
""",
    unsafe_allow_html=True,
)
caption("Flagged land is shown on terraces only, Landsat 8/9, 30 m pixels. The satellite background is recent imagery and is there for orientation: it is not the imagery the tests were run on. "
        "Hover a terrace or a sample point for its values. Zoom in on Rangeen Kultreh to see the kiln field under the orange pixels.")
