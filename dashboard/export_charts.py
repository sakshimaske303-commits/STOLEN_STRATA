"""export_charts.py — exports dashboard Plotly charts as PNGs. Run: python export_charts.py"""

import os
import plotly.graph_objects as go

from style import MAROON, MAROON_LIGHT, GOLD, TEAL, BG_CARD, BG_PRIMARY, CREAM
import data as d

OUT_DIR = os.path.join("..", "outputs", "figures", "dashboard_charts")
os.makedirs(OUT_DIR, exist_ok=True)

WIDTH, HEIGHT, SCALE = 1300, 800, 3  # high-res for print/paper use

COMMON_LAYOUT = dict(
    plot_bgcolor=BG_CARD,
    paper_bgcolor=BG_PRIMARY,
    font=dict(color=CREAM, family="Arial", size=16),  # web fonts don't render in static export; Arial is the safe fallback
    margin=dict(l=90, r=90, t=80, b=70),
)


def save(fig, filename, title=None):
    if title:
        fig.update_layout(title=dict(text=title, font=dict(size=22, color=GOLD), x=0.5, xanchor="center"))
    fig.update_layout(**COMMON_LAYOUT, width=WIDTH, height=HEIGHT)
    path = os.path.join(OUT_DIR, filename)
    fig.write_image(path, scale=SCALE)
    print(f"saved {path}")


# 1. Bare-earth fraction trend, 1994-2025 -----------------------------------
fig1 = go.Figure()
fig1.add_trace(go.Scatter(
    x=d.TREND_YEARS, y=d.TREND_BARE_FRAC_PCT,
    mode="lines+markers+text",
    text=[f"{v}%" for v in d.TREND_BARE_FRAC_PCT],
    textposition="top center",
    textfont=dict(color=GOLD, size=18),
    line=dict(color=MAROON, width=5, shape="spline"),
    marker=dict(size=16, color=GOLD, line=dict(color=MAROON, width=2)),
    fill="tozeroy", fillcolor="rgba(139,30,63,0.20)",
))
fig1.update_layout(
    xaxis=dict(title="Year", gridcolor="#2A3550", tickmode="array", tickvals=d.TREND_YEARS,
               range=[1990, 2029]),
    yaxis=dict(title="Mean Bare-Earth Fraction (%)", gridcolor="#2A3550", range=[0, 9.8]),
)
save(fig1, "01_bare_earth_trend_1994_2025.png", "Bare-Earth Fraction Trend, 1994–2025")

# 2. Bare-earth area comparison, 1994 vs 2025 --------------------------------
fig2 = go.Figure()
fig2.add_trace(go.Bar(
    x=["1994", "2025"], y=[d.BARE_1994_HA, d.BARE_2025_HA],
    marker_color=[TEAL, MAROON],
    text=[f"{d.BARE_1994_HA} ha", f"{d.BARE_2025_HA} ha"],
    textposition="outside", textfont=dict(color=CREAM, size=18),
))
fig2.update_layout(
    xaxis=dict(title=None, gridcolor="#2A3550"),
    yaxis=dict(title="Total Bare-Earth Area (ha)", gridcolor="#2A3550",
               range=[0, max(d.BARE_1994_HA, d.BARE_2025_HA) * 1.18]),
    showlegend=False,
)
save(fig2, "02_bare_earth_area_comparison.png", "Bare-Earth Area: 1994 vs 2025")

# 3. Loss concentration donut ------------------------------------------------
fig3 = go.Figure(data=[go.Pie(
    labels=[f"Within {d.DEGRADED_COUNT} degraded terraces", "Diffused across remaining terraces"],
    values=[d.DEGRADED_POLY_LOSS_HA, d.NET_CONVERSION_HA - d.DEGRADED_POLY_LOSS_HA],
    hole=0.55,
    marker=dict(colors=[MAROON, "#2A3550"]),
    textfont=dict(color=CREAM, size=16),
)])
fig3.update_layout(
    annotations=[dict(
        text=f"{d.DEGRADED_POLY_LOSS_SHARE_OF_TOTAL_LOSS_PCT}%<br>concentrated",
        x=0.5, y=0.5, font=dict(size=22, color=GOLD), showarrow=False,
    )],
)
save(fig3, "03_degradation_loss_concentration.png", "Where the Net Conversion Is Concentrated")

# 4. Saffron proximity-risk sensitivity --------------------------------------
labels = [f"{t} m" for t in d.SENSITIVITY_THRESHOLDS_M]
values = d.SENSITIVITY_AT_RISK_PCT
fig4 = go.Figure()
fig4.add_trace(go.Bar(
    x=labels, y=[v if v is not None else 0 for v in values],
    marker_color=GOLD,
    text=[f"{v}%" if v is not None else "n/a" for v in values],
    textposition="outside", textfont=dict(color=CREAM, size=16),
))
fig4.update_layout(
    xaxis=dict(title="Risk Radius", gridcolor="#2A3550"),
    yaxis=dict(title="% of Saffron Polygons 'At Risk'", gridcolor="#2A3550", range=[0, 115]),
    showlegend=False,
)
save(fig4, "04_saffron_proximity_sensitivity.png", "Saffron Proximity-Risk Sensitivity")

# 5. Degraded vs stable terrace count donut ----------------------------------
fig5 = go.Figure(data=[go.Pie(
    labels=["Degraded", "Stable"],
    values=[d.DEGRADED_COUNT, d.TOTAL_TERRACES - d.DEGRADED_COUNT],
    marker=dict(colors=[MAROON, TEAL]),
    hole=0.5,
    textfont=dict(color=CREAM, size=16),
)])
save(fig5, "05_degraded_vs_stable_terraces.png", f"Terrace Status ({d.TOTAL_TERRACES} Delineated Terraces)")

print(f"\nAll 5 charts exported to: {os.path.abspath(OUT_DIR)}")
