"""build_static_maps.py — matplotlib print-layout maps matching the QGIS export style (dark canvas, bold title, legend box, scale bar)."""
import os
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrow
from matplotlib.lines import Line2D
from matplotlib_scalebar.scalebar import ScaleBar

DATA_DIR = "data/processed"
OUT_DIR = "outputs/maps"

BG = "#477271"
PANEL = "#040402"
GREEN = "#10DC04"
RED = "#EF0E00"
CYAN = "#3DEDE0"
GOLD = "#D4AF37"
LAVENDER = "#B39DDB"

def gp(name):
    return gpd.read_file(os.path.join(DATA_DIR, name))

def poster_frame(figsize=(14, 14.2)):
    fig = plt.figure(figsize=figsize, facecolor=BG)
    ax_map = fig.add_axes([0.06, 0.20, 0.88, 0.68], facecolor=PANEL)
    ax_legend = fig.add_axes([0.06, 0.02, 0.88, 0.15], facecolor=PANEL)
    ax_legend.set_xticks([]); ax_legend.set_yticks([])
    for spine in ax_legend.spines.values():
        spine.set_visible(False)
    ax_map.set_xticks([]); ax_map.set_yticks([])
    return fig, ax_map, ax_legend

def add_title(fig, line1, line2=""):
    fig.text(0.5, 0.965, line1, ha="center", va="top", fontsize=30, fontweight="bold", color="#1a1a1a")
    if line2:
        fig.text(0.5, 0.925, line2, ha="center", va="top", fontsize=26, fontweight="bold", color="#1a1a1a")

def add_scalebar(ax):
    ax.add_artist(ScaleBar(1, location="lower left", box_alpha=0, color="white", font_properties={"size": 13, "weight": "bold"}))

def add_north_arrow(fig):
    fig.text(0.955, 0.90, "▲\nN", ha="center", va="center", fontsize=16, color="#1a1a1a", fontweight="bold")

def legend_entry(ax, y, color, label, marker="s"):
    ax.scatter([0.02], [y], s=400, color=color, marker=marker, transform=ax.transAxes, clip_on=False)
    ax.text(0.06, y, label, transform=ax.transAxes, va="center", fontsize=17, color="white")

# ============================================================
# 07 — Settlement proximity
# ============================================================
def build_settlement_proximity():
    terraces = gp("karewa_settlement_proximity.gpkg")
    buildings = gp("settlement_footprints_osm.gpkg").to_crs(terraces.crs)

    fig, ax, axl = poster_frame()
    add_title(fig, "Degradation vs Settlement Proximity", "(Mann-Whitney p = 0.0001)")

    buildings_centroids = buildings.geometry.centroid
    ax.scatter(buildings_centroids.x, buildings_centroids.y, s=1.5, color=LAVENDER, alpha=0.5, linewidths=0, label="Buildings")

    stable = terraces[terraces["status"] != "likely_degraded"]
    degraded = terraces[terraces["status"] == "likely_degraded"]
    stable.plot(ax=ax, color=GREEN, edgecolor="none")
    degraded.plot(ax=ax, color=RED, edgecolor="none")

    minx, miny, maxx, maxy = terraces.total_bounds
    pad = (maxx - minx) * 0.05
    ax.set_xlim(minx - pad, maxx + pad)
    ax.set_ylim(miny - pad, maxy + pad)
    add_scalebar(ax)
    add_north_arrow(fig)

    axl.text(0.02, 0.85, "Terrace Status (201 Delineated Terraces)", transform=axl.transAxes, fontsize=19, color="white")
    legend_entry(axl, 0.55, GREEN, "Stable (n=176, 87.6%)")
    legend_entry(axl, 0.30, RED, "Likely Degraded (n=25, 12.4%)")
    legend_entry(axl, 0.05, LAVENDER, "Building Footprints (n=3,266, OSM)", marker="o")

    out = os.path.join(OUT_DIR, "07_settlement_proximity.png")
    fig.savefig(out, dpi=250, facecolor=BG)
    plt.close(fig)
    print("saved", out)

# ============================================================
# 08 — Economic value-at-risk
# ============================================================
def build_economic_value_at_risk():
    YIELD_KG_PER_HA = 5.27
    PRICE_PER_KG_RS = 272998
    saf = gp("saffron_proximity_risk.gpkg")
    degraded = gp("likely_degraded.gpkg")
    saf["area_ha"] = saf.geometry.area / 10000
    saf["annual_value_lakh"] = saf["area_ha"] * YIELD_KG_PER_HA * PRICE_PER_KG_RS / 1e5

    fig, ax, axl = poster_frame()
    add_title(fig, "Saffron Economic Value-at-Risk", "(₹32.4 cr/yr total, ₹17.8 cr/yr within 1km)")

    degraded.plot(ax=ax, color="#555555", edgecolor="none", alpha=0.6)
    at_risk = saf[saf["at_risk"]]
    not_at_risk = saf[~saf["at_risk"]]
    not_at_risk.plot(ax=ax, color=GOLD, edgecolor="#5c4508", linewidth=1.2)
    at_risk.plot(ax=ax, color="#B8860B", edgecolor=RED, linewidth=2)

    minx, miny, maxx, maxy = saf.total_bounds
    padx = (maxx - minx) * 0.25
    pady = (maxy - miny) * 0.25
    ax.set_xlim(minx - padx, maxx + padx)
    ax.set_ylim(miny - pady, maxy + pady)
    add_scalebar(ax)
    add_north_arrow(fig)

    axl.text(0.02, 0.85, "Saffron Terraces (14 Detected, 225.4 ha)", transform=axl.transAxes, fontsize=19, color="white")
    legend_entry(axl, 0.55, "#B8860B", "Within 1km risk radius (n=6, ₹17.8 cr/yr)")
    legend_entry(axl, 0.30, GOLD, "Beyond 1km risk radius (n=8)")
    legend_entry(axl, 0.05, "#555555", "Degraded terraces (n=25)")

    out = os.path.join(OUT_DIR, "08_economic_value_at_risk.png")
    fig.savefig(out, dpi=250, facecolor=BG)
    plt.close(fig)
    print("saved", out)

if __name__ == "__main__":
    build_settlement_proximity()
    build_economic_value_at_risk()
