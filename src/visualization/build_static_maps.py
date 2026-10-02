"""build_static_maps.py — matplotlib print-layout maps matching the QGIS export style (dark canvas, bold title, legend box, scale bar).

Maps 01 and 04 replace earlier QGIS exports: the QGIS map 01 title carried stray quotation
marks, and the QGIS map 04 filled every terrace in the "Detected Saffron Signature" colour
and was titled "Validation". Both are now built here from the project's own layers, with a
DEM hillshade backdrop (no web tiles needed, so the maps rebuild offline).
"""
import os
import numpy as np
import geopandas as gpd
import rasterio
from rasterio.windows import from_bounds
from shapely.geometry import Point, box
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrow
from matplotlib.lines import Line2D
from matplotlib_scalebar.scalebar import ScaleBar
import matplotlib.patheffects as pe

DATA_DIR = "data/processed"
OUT_DIR = "outputs/maps"
DEM_PATH = "data/interim/DEM_UTM43N.tif"
UTM = "EPSG:32643"

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

def legend_entry(ax, y, color, label, marker="s", x=0.02, edge="none", size=400, fontsize=17):
    ax.scatter([x], [y], s=size, color=color, marker=marker, edgecolors=edge, linewidths=1.5, transform=ax.transAxes, clip_on=False)
    ax.text(x + 0.04, y, label, transform=ax.transAxes, va="center", fontsize=fontsize, color="white")

def draw_hillshade(ax, bounds, azimuth=315, altitude=45, alpha=1.0):
    """Grey hillshade of the project DEM inside `bounds` (minx, miny, maxx, maxy in UTM 43N)."""
    with rasterio.open(DEM_PATH) as src:
        b = src.bounds
        minx, miny = max(bounds[0], b.left), max(bounds[1], b.bottom)
        maxx, maxy = min(bounds[2], b.right), min(bounds[3], b.top)
        if minx >= maxx or miny >= maxy:
            return
        win = from_bounds(minx, miny, maxx, maxy, src.transform).round_offsets().round_lengths()
        dem = src.read(1, window=win).astype(float)
        wt = src.window_transform(win)
        if src.nodata is not None:
            dem[dem == src.nodata] = np.nan
        px = src.transform.a
    dy, dx = np.gradient(dem, px)
    slope = np.pi / 2 - np.arctan(np.hypot(dx, dy))
    aspect = np.arctan2(dy, -dx)
    az, alt = np.radians(360 - azimuth + 90), np.radians(altitude)
    shade = np.sin(alt) * np.sin(slope) + np.cos(alt) * np.cos(slope) * np.cos(az - aspect)
    extent = (wt.c, wt.c + wt.a * dem.shape[1], wt.f + wt.e * dem.shape[0], wt.f)
    ax.imshow(shade, cmap="gray", extent=extent, vmin=-0.2, vmax=1.0, alpha=alpha, zorder=0, interpolation="bilinear")

def draw_backdrop(ax, view, kind):
    """Backdrop for maps 01/04. With internet + contextily installed, uses web tiles
    (kind='imagery' -> Esri World Imagery, kind='topo' -> Esri World Topo Map).
    Otherwise falls back to the DEM hillshade, which needs no network. Returns the source used."""
    ax.set_xlim(view[0], view[2]); ax.set_ylim(view[1], view[3])
    ax.set_aspect("equal")
    try:
        import contextily as cx
        src = cx.providers.Esri.WorldImagery if kind == "imagery" else cx.providers.Esri.WorldTopoMap
        cx.add_basemap(ax, crs=UTM, source=src, attribution_size=7, zorder=0)
        return "Esri World Imagery" if kind == "imagery" else "Esri World Topo Map"
    except Exception as e:  # no contextily, or no network
        print(f"  (web basemap unavailable: {type(e).__name__} — using DEM hillshade)")
        draw_hillshade(ax, view)
        return "DEM hillshade"

def clean_axes(ax, view):
    ax.set_xlim(view[0], view[2]); ax.set_ylim(view[1], view[3])
    ax.set_aspect("equal")
    ax.set_xlabel(""); ax.set_ylabel("")
    ax.set_xticks([]); ax.set_yticks([])

HALO = [pe.withStroke(linewidth=3, foreground="black")]

# Field-photo positions (3 Sep 2026), as stamped on the photos — see dashboard Ground Verification page.
FIELD_PHOTOS_LONLAT = [(74.951189, 33.97373), (74.951186, 33.973596), (74.951186, 33.973788), (74.950956, 33.973365)]

# ============================================================
# 01 — Study area overview
# ============================================================
def build_study_area_overview():
    districts = gp("kashmir_3districts.gpkg").to_crs(UTM)
    aoi = gp("aoi_bbox.gpkg").to_crs(UTM)
    terraces = gp("karewa_final_with_geomorphometrics.gpkg")
    settlements = gp("settlements.gpkg").to_crs(UTM)
    waterways = gp("waterway.gpkg").to_crs(UTM)

    fig, ax, axl = poster_frame()
    add_title(fig, "Study Area: Karewa Belt of the", "Central Kashmir Valley")

    minx, miny, maxx, maxy = districts.total_bounds
    padx, pady = (maxx - minx) * 0.04, (maxy - miny) * 0.04
    view = (minx - padx, miny - pady, maxx + padx, maxy + pady)
    backdrop = draw_backdrop(ax, view, "topo")
    if backdrop == "DEM hillshade":
        # the DEM only covers the study-area box; tint the districts so the rest isn't a void
        districts.plot(ax=ax, color="#1E3A3A", edgecolor="none", zorder=-1)
    waterways.clip(box(*view)).plot(ax=ax, color="#3A7BD5", linewidth=1.6, zorder=2)
    districts.boundary.plot(ax=ax, color=GOLD, linewidth=2.2, zorder=3)
    terraces.plot(ax=ax, color=CYAN, edgecolor="none", zorder=4)
    aoi.boundary.plot(ax=ax, color="#FFFF33", linewidth=3, zorder=5)
    settlements.plot(ax=ax, color="white", edgecolor="black", markersize=140, zorder=6)
    for _, r in settlements.iterrows():
        ax.annotate(r["name"], (r.geometry.x, r.geometry.y), xytext=(9, 7), textcoords="offset points",
                    fontsize=15, fontweight="bold", color="white", zorder=7,
                    bbox=dict(boxstyle="round,pad=0.15", fc="black", ec="none", alpha=0.6))
    for _, r in districts.iterrows():
        c = r.geometry.representative_point()
        outside = r.geometry.difference(aoi.geometry.iloc[0])
        if not outside.is_empty:
            c = max(getattr(outside, "geoms", [outside]), key=lambda g: g.area).representative_point()
        ax.text(c.x, c.y, str(r["DISTRICT"]).upper(), fontsize=15, color=GOLD, ha="center", va="center", zorder=6,
                fontweight="bold", path_effects=HALO)

    clean_axes(ax, view)
    add_scalebar(ax)
    add_north_arrow(fig)

    axl.text(0.02, 0.85, "Study Area (33.85–34.15°N, 74.75–75.15°E)", transform=axl.transAxes, fontsize=19, color="white")
    legend_entry(axl, 0.60, "none", "Study-area box", edge="#FFFF33")
    legend_entry(axl, 0.36, "none", "District boundaries (Badgam, Pulwama, Srinagar)", edge=GOLD)
    legend_entry(axl, 0.12, CYAN, f"Delineated terraces (n={len(terraces)})")
    legend_entry(axl, 0.60, "white", "Reference settlements", marker="o", x=0.62, edge="black")
    legend_entry(axl, 0.36, "#3A7BD5", "Waterways (OSM)", marker="s", x=0.62, size=160)
    axl.text(0.66, 0.12, f"Backdrop: {backdrop}", transform=axl.transAxes, va="center", fontsize=14, color="#BBBBBB")

    out = os.path.join(OUT_DIR, "01_study_area_overview.png")
    fig.savefig(out, dpi=250, facecolor=BG)
    plt.close(fig)
    print("saved", out)

# ============================================================
# 04 — Plausibility check at Saffron Fields, Lethpora (file name kept for existing links)
# ============================================================
def build_plausibility_lethpora():
    terraces = gp("karewa_saffron_overlay.gpkg")
    roads = gp("road_network.gpkg").to_crs(UTM)
    photos = gpd.GeoSeries([Point(xy) for xy in FIELD_PHOTOS_LONLAT], crs=4326).to_crs(UTM)

    saffron = terraces[terraces["likely_saffron"]]
    minx, miny, maxx, maxy = saffron.total_bounds
    padx, pady = (maxx - minx) * 0.12, (maxy - miny) * 0.12
    view = (minx - padx, miny - pady, maxx + padx, maxy + pady)
    in_view = terraces[terraces.intersects(box(*view))]
    saf_v = in_view[in_view["likely_saffron"]]
    deg_v = in_view[(in_view["status"] == "likely_degraded") & (~in_view["likely_saffron"])]
    oth_v = in_view[(~in_view["likely_saffron"]) & (in_view["status"] != "likely_degraded")]

    fig, ax, axl = poster_frame()
    add_title(fig, "Plausibility Check: Delineated Terraces", "at Saffron Fields, Lethpora")

    backdrop = draw_backdrop(ax, view, "imagery")
    road_col = "#5A5A5A" if backdrop == "DEM hillshade" else "#FFFFFF"
    roads.clip(box(*view)).plot(ax=ax, color=road_col, linewidth=0.7, alpha=0.7, zorder=1)
    oth_v.plot(ax=ax, color="#8FA3A3", edgecolor="black", linewidth=0.6, alpha=0.85, zorder=2)
    deg_v.plot(ax=ax, color=RED, edgecolor="black", linewidth=0.6, alpha=0.9, zorder=3)
    saf_v.plot(ax=ax, color=GOLD, edgecolor="black", linewidth=0.8, alpha=0.9, zorder=4)
    ax.scatter(photos.x, photos.y, s=260, marker="*", color="white", edgecolors="black", linewidths=1.2, zorder=6)
    p0 = photos.iloc[0]
    ax.annotate("Field photos\n(3 Sep 2026)", (p0.x, p0.y), xytext=(-16, 0), ha="right", va="center",
                textcoords="offset points", fontsize=13, color="white", fontweight="bold", zorder=7,
                bbox=dict(boxstyle="round,pad=0.25", fc="black", ec="none", alpha=0.65))

    clean_axes(ax, view)
    add_scalebar(ax)
    add_north_arrow(fig)

    axl.text(0.02, 0.85, "Polygons trace plateau rims and spurs, not the flat interior", transform=axl.transAxes, fontsize=19, color="white")
    legend_entry(axl, 0.60, GOLD, f"Terrace flagged likely saffron (n={len(saf_v)} in view, {len(saffron)} total)", edge="black")
    legend_entry(axl, 0.36, "#8FA3A3", f"Other delineated terrace (n={len(oth_v)} in view)", edge="black")
    legend_entry(axl, 0.12, RED, f"Likely degraded terrace (n={len(deg_v)} in view)", edge="black")
    legend_entry(axl, 0.60, "white", "Field photo points", marker="*", x=0.68, edge="black")
    legend_entry(axl, 0.36, road_col, "Roads (OSM)", marker="s", x=0.68, size=160)
    axl.text(0.72, 0.12, f"Backdrop: {backdrop}", transform=axl.transAxes, va="center", fontsize=14, color="#BBBBBB")

    out = os.path.join(OUT_DIR, "04_validation_lethpora.png")
    fig.savefig(out, dpi=250, facecolor=BG)
    plt.close(fig)
    print("saved", out)

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
    build_study_area_overview()
    build_plausibility_lethpora()
    build_settlement_proximity()
    build_economic_value_at_risk()
