import streamlit as st
import plotly.graph_objects as go
from style import inject_css, card, map_placeholder, page_title, map_image, MAROON, GOLD, TEAL, BG_CARD, CREAM
import data as d

st.set_page_config(page_title="DEGRADATION ANALYSIS | Stolen Strata", page_icon="🛰️", layout="wide")
inject_css()

page_title("🛰️ DEGRADATION ANALYSIS", "Multi-temporal bare-earth change detection, 1994–2025")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Bare-Earth Area, 1994", f"{d.BARE_1994_HA} ha")
c2.metric("Bare-Earth Area, 2025", f"{d.BARE_2025_HA} ha")
c3.metric("Net Conversion", f"{d.NET_CONVERSION_HA} ha", f"{d.NET_CONVERSION_PCT}%")
c4.metric("Terraces Flagged Degraded", f"{d.DEGRADED_COUNT} / {d.TOTAL_TERRACES}")

st.image(map_image("02_terrace_degradation_status.png"), use_container_width=True)

card(
    "Method",
    """
    <p>Rather than comparing mean NDVI (which dilutes a localized mining scar within a large terrace
    polygon), each terrace's <b>bare-earth fraction</b> — the percentage of pixels with NDVI below 0.15
    — is computed per polygon via zonal statistics (<code>rasterio.mask.mask</code>) for
    season-matched Landsat/Sentinel-2 composites. Season-matching (June–September in both years) was
    essential: an initial comparison using an all-season 1994 composite against a summer-only 2025
    composite produced a counter-intuitive <i>increase</i> in mean NDVI, traced entirely to seasonal
    mismatch rather than genuine land-cover recovery. A terrace is classified <b>likely_degraded</b>
    when its bare-earth fraction increases by ≥ 0.15 between the two dates.</p>
    """,
    badge="Pipeline Stage 2",
)

card(
    "Result",
    f"""
    <p>Of {d.TOTAL_TERRACES} delineated terraces, <b>{d.DEGRADED_COUNT} ({d.DEGRADED_PCT_OF_TERRACES}%)</b>
    show a bare-earth increase consistent with mining or built-up conversion. In absolute terms, total
    bare-earth area within mapped terraces rose from {d.BARE_1994_HA} ha to {d.BARE_2025_HA} ha — a net
    conversion of <b>{d.NET_CONVERSION_HA} ha ({d.NET_CONVERSION_PCT}% of total mapped terrace area)</b>.
    Strikingly, <b>{d.DEGRADED_POLY_LOSS_SHARE_OF_TOTAL_LOSS_PCT}%</b> of that loss
    ({d.DEGRADED_POLY_LOSS_HA} ha) is concentrated within the {d.DEGRADED_COUNT} flagged terraces alone
    — degradation is not diffuse background noise across the landscape, it is spatially concentrated.</p>
    """,
    badge="Finding",
)

st.markdown("## Four-Point Multi-Temporal Trend")
st.markdown(
    "Extending the two-point (1994 → 2025) comparison to four time slices (1994, 2005, 2015, 2025) "
    "reveals *when* degradation accelerated, not just its net magnitude."
)

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=d.TREND_YEARS,
        y=d.TREND_BARE_FRAC_PCT,
        mode="lines+markers+text",
        text=[f"{v}%" for v in d.TREND_BARE_FRAC_PCT],
        textposition="top center",
        textfont=dict(color=GOLD, size=14, family="Montserrat"),
        line=dict(color=MAROON, width=4),
        marker=dict(size=12, color=GOLD, line=dict(color=MAROON, width=2)),
        fill="tozeroy",
        fillcolor="rgba(139,30,63,0.15)",
    )
)
fig.update_layout(
    plot_bgcolor=BG_CARD,
    paper_bgcolor=BG_CARD,
    font=dict(color=CREAM, family="Inter"),
    xaxis=dict(title="Year", gridcolor="#2A3550", tickmode="array", tickvals=d.TREND_YEARS),
    yaxis=dict(title="Mean Bare-Earth Fraction (%)", gridcolor="#2A3550"),
    margin=dict(l=10, r=10, t=30, b=10),
    height=420,
)
st.plotly_chart(fig, width='stretch')

card(
    "Reading the Curve",
    """
    <p>Bare-earth fraction is essentially flat between 1994 and 2015 (1.84% → 2.62% → 2.63%) — three
    decades of relative stability — before more than <b>tripling</b> between 2015 and 2025 (2.63% →
    8.43%). This is the strongest single piece of evidence in the whole project: karewa degradation in
    this belt is a recent, accelerating phenomenon rather than a slow multi-decadal process, consistent
    with reporting of intensified mining activity in the last decade.</p>
    """,
    badge="Interpretation",
)