import streamlit as st
import plotly.graph_objects as go
from style import inject_css, card, page_title, MAROON, MAROON_LIGHT, GOLD, TEAL, BG_CARD, CREAM, CHART_SEQUENCE
import data as d

st.set_page_config(page_title="EXPLORE TRENDS | Stolen Strata", page_icon="📈", layout="wide")
inject_css()

page_title("📈 EXPLORE TRENDS", "Interactive views across the full analytical pipeline")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Bare-Earth Trend", "Area Loss Breakdown", "Saffron Proximity", "Degradation Concentration"]
)

# --- Tab 1: bare-earth trend (duplicated interactive control here for one-stop exploration)
with tab1:
    st.markdown("#### Mean Bare-Earth Fraction Across Four Time Slices")
    show_fill = st.checkbox("Show area fill", value=True, key="fill1")
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=d.TREND_YEARS,
            y=d.TREND_BARE_FRAC_PCT,
            mode="lines+markers+text",
            text=[f"{v}%" for v in d.TREND_BARE_FRAC_PCT],
            textposition="top center",
            textfont=dict(color=GOLD, size=13, family="Montserrat"),
            line=dict(color=MAROON, width=4, shape="spline"),
            marker=dict(size=13, color=GOLD, line=dict(color=MAROON, width=2)),
            fill="tozeroy" if show_fill else None,
            fillcolor="rgba(139,30,63,0.18)",
        )
    )
    fig.update_layout(
        plot_bgcolor=BG_CARD, paper_bgcolor=BG_CARD, font=dict(color=CREAM, family="Inter"),
        xaxis=dict(title="Year", gridcolor="#2A3550", tickmode="array", tickvals=d.TREND_YEARS),
        yaxis=dict(title="Bare-Earth Fraction (%)", gridcolor="#2A3550"),
        height=440, margin=dict(l=10, r=10, t=30, b=10),
    )
    st.plotly_chart(fig, width='stretch')
    st.caption("Flat 1994–2015, then more than tripling 2015–2025 — the clearest acceleration signal in the dataset.")

# --- Tab 2: area loss breakdown
with tab2:
    st.markdown("#### Where the 190.3 ha of Net Conversion Sits")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=["1994 Bare Earth", "2025 Bare Earth"],
        y=[d.BARE_1994_HA, d.BARE_2025_HA],
        marker_color=[TEAL, MAROON],
        text=[f"{d.BARE_1994_HA} ha", f"{d.BARE_2025_HA} ha"],
        textposition="outside",
        textfont=dict(color=CREAM),
        name="Total bare-earth area",
    ))
    fig2.update_layout(
        plot_bgcolor=BG_CARD, paper_bgcolor=BG_CARD, font=dict(color=CREAM, family="Inter"),
        yaxis=dict(title="Hectares", gridcolor="#2A3550"),
        height=400, margin=dict(l=10, r=10, t=30, b=10), showlegend=False,
    )
    st.plotly_chart(fig2, width='stretch')

    fig3 = go.Figure(data=[go.Pie(
        labels=["Loss within the 25 flagged 'degraded' terraces", "Loss diffused across remaining terraces"],
        values=[d.DEGRADED_POLY_LOSS_HA, d.NET_CONVERSION_HA - d.DEGRADED_POLY_LOSS_HA],
        hole=0.55,
        marker=dict(colors=[MAROON, "#2A3550"]),
        textfont=dict(color=CREAM, size=13),
    )])
    fig3.update_layout(
        plot_bgcolor=BG_CARD, paper_bgcolor=BG_CARD, font=dict(color=CREAM, family="Inter"),
        height=400, margin=dict(l=10, r=10, t=30, b=10),
        annotations=[dict(text=f"{d.DEGRADED_POLY_LOSS_SHARE_OF_TOTAL_LOSS_PCT}%<br>concentrated", x=0.5, y=0.5,
                           font=dict(size=16, color=GOLD, family="Montserrat"), showarrow=False)],
    )
    st.plotly_chart(fig3, width='stretch')
    st.caption(f"{d.DEGRADED_POLY_LOSS_HA} ha of the {d.NET_CONVERSION_HA} ha net loss sits inside just {d.DEGRADED_COUNT} terraces ({d.DEGRADED_PCT_OF_TERRACES}% of the 201 mapped) — degradation is spatially concentrated, not diffuse.")

# --- Tab 3: saffron proximity
with tab3:
    st.markdown("#### Saffron Parcel Proximity to Nearest Degraded Terrace")
    fig4 = go.Figure()
    labels = [f"{t} m" for t in d.SENSITIVITY_THRESHOLDS_M]
    values = d.SENSITIVITY_AT_RISK_PCT
    fig4.add_trace(go.Scatter(
        x=labels,
        y=[v for v in values if v is not None],
        mode="markers",
        marker=dict(size=0),
        showlegend=False,
    ))
    fig4.add_trace(go.Bar(
        x=labels,
        y=[v if v is not None else 0 for v in values],
        marker_color=GOLD,
        text=[f"{v}%" if v is not None else "n/a" for v in values],
        textposition="outside",
        textfont=dict(color=CREAM),
        name="% at risk",
    ))
    fig4.update_layout(
        plot_bgcolor=BG_CARD, paper_bgcolor=BG_CARD, font=dict(color=CREAM, family="Inter"),
        xaxis=dict(title="Risk Radius", gridcolor="#2A3550"),
        yaxis=dict(title="% of Saffron Polygons At Risk", gridcolor="#2A3550", range=[0, 100]),
        height=420, margin=dict(l=10, r=10, t=30, b=10), showlegend=False,
    )
    st.plotly_chart(fig4, width='stretch')
    m1, m2 = st.columns(2)
    m1.metric("Mean Distance to Degradation", f"{d.PROXIMITY_MEAN_M} m")
    m2.metric("Closest Saffron Parcel", f"{d.PROXIMITY_MIN_M} m")

# --- Tab 4: degradation concentration across terraces
with tab4:
    st.markdown("#### Degraded vs Stable Terrace Counts")
    fig5 = go.Figure(data=[go.Pie(
        labels=["Degraded", "Stable"],
        values=[d.DEGRADED_COUNT, d.TOTAL_TERRACES - d.DEGRADED_COUNT],
        marker=dict(colors=[MAROON, TEAL]),
        hole=0.5,
        textfont=dict(color=CREAM, size=13),
    )])
    fig5.update_layout(
        plot_bgcolor=BG_CARD, paper_bgcolor=BG_CARD, font=dict(color=CREAM, family="Inter"),
        height=420, margin=dict(l=10, r=10, t=30, b=10),
    )
    st.plotly_chart(fig5, width='stretch')
    st.caption(f"{d.DEGRADED_COUNT} of {d.TOTAL_TERRACES} delineated terraces ({d.DEGRADED_PCT_OF_TERRACES}%) show a bare-earth increase ≥ 0.15 between 1994 and 2025.")

st.markdown("---")
card(
    "A Note on Live Data",
    """
    <p>Charts on this page read from a small, version-controlled results table
    (<code>dashboard/data.py</code>) that mirrors the outputs of the analysis scripts in
    <code>src/analysis/</code>. Re-running any script and updating that file will refresh every chart
    across the whole dashboard automatically — there is deliberately only one place these numbers live.</p>
    """,
    badge="How This Works",
)
