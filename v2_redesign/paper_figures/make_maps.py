"""Figure 1 of the revised paper: study box, terraces and the strict conversion test.
Needs the rasters in data/raw and data/interim (see DATA_ACCESS.md).
Run from the repo root, after the west_extension scripts:  python v2_redesign/paper_figures/make_maps.py
"""
import numpy as np, geopandas as gpd, rasterio
from rasterio.warp import reproject, Resampling, transform as warp_xy
from scipy import ndimage as ndi
from shapely.geometry import box
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource, ListedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

OUT = "v2_redesign/paper_figures/"
BARE, VEG = 0.25, 0.35
with rasterio.open("data/raw/StolenStrata_v2w_OLIonly_p90_2013_2025.tif") as s:
    a = s.read().astype("float32"); a[a == -32768] = np.nan
    OLI = {int(d[-4:]): a[i] / 1e4 for i, d in enumerate(s.descriptions)}; T, crs, shape = s.transform, s.crs, s.shape
conv = np.all([OLI[y] >= VEG for y in (2013, 2014, 2015)], 0) & np.all([OLI[y] < BARE for y in (2023, 2024, 2025)], 0)
terr = gpd.read_file("v2_redesign/west_extension/karewa_terraces_wide.gpkg").to_crs(crs)
with rasterio.open("data/interim/DEM_wide_buffered_UTM43N.tif") as d:
    dem = np.full(shape, np.nan, "float32")
    reproject(rasterio.band(d, 1), dem, dst_transform=T, dst_crs=crs, resampling=Resampling.bilinear, dst_nodata=np.nan)
ext = (T.c, T.c + shape[1] * 30, T.f - shape[0] * 30, T.f)

fig, ax = plt.subplots(figsize=(11, 7.6))
ax.imshow(LightSource(315, 45).hillshade(np.nan_to_num(dem, nan=np.nanmean(dem)), vert_exag=2, dx=30, dy=30), cmap="gray", extent=ext, alpha=.9)
terr.boundary.plot(ax=ax, color="#0077bb", lw=.6)
ax.imshow(np.ma.masked_where(~ndi.binary_dilation(conv, iterations=2), np.ones(shape)), cmap=ListedColormap(["#d7191c"]), extent=ext, interpolation="nearest")
old = gpd.GeoSeries([box(74.75, 33.85, 75.15, 34.15)], crs=4326).to_crs(crs)
old.boundary.plot(ax=ax, color="#222222", lw=1, ls="--")


def utm(lon, lat):
    x, y = warp_xy("EPSG:4326", crs, [lon], [lat]); return x[0], y[0]


for name, lon, lat, dx, dy in [("Rangeen Kultreh\nkiln field", 74.846, 33.944, -95, 18), ("Bandagam–Batapora\nkiln belt", 74.66, 34.02, -20, 62),
                               ("Pampore", 74.93, 34.016, 30, 20), ("Srinagar", 74.80, 34.085, -10, 28), ("Awantipora", 75.015, 33.92, 34, -10)]:
    kiln = "kiln" in name
    ax.annotate(name, utm(lon, lat), xytext=(dx, dy), textcoords="offset points", fontsize=9, fontweight="bold" if kiln else "normal", ha="center",
                arrowprops=dict(arrowstyle="-", lw=.8, color="k"), bbox=dict(boxstyle="round,pad=.25", fc="w", ec="#888888" if kiln else "none", alpha=.92))
# axes in degrees
lons = np.arange(74.6, 75.11, 0.1); lats = np.arange(33.85, 34.11, 0.05)
ax.set_xticks([utm(l, 33.975)[0] for l in lons]); ax.set_xticklabels([f"{l:.1f}° E" for l in lons], fontsize=8.5)
ax.set_yticks([utm(74.85, l)[1] for l in lats]); ax.set_yticklabels([f"{l:.2f}° N" for l in lats], fontsize=8.5)
ax.set(xlim=ext[:2], ylim=ext[2:])
# scale bar and north arrow
x0, y0 = ext[0] + 2500, ext[2] + 2200
ax.plot([x0, x0 + 10000], [y0, y0], color="k", lw=3, solid_capstyle="butt"); ax.plot([x0, x0 + 5000], [y0, y0], color="w", lw=1.6, solid_capstyle="butt")
ax.text(x0 + 5000, y0 + 500, "10 km", ha="center", fontsize=9, bbox=dict(fc="w", ec="none", alpha=.8, pad=1.5))
ax.annotate("", (ext[1] - 2500, ext[3] - 1500), xytext=(ext[1] - 2500, ext[3] - 5000), arrowprops=dict(arrowstyle="-|>", lw=1.8, color="k"))
ax.text(ext[1] - 2500, ext[3] - 6000, "N", ha="center", va="center", fontsize=11, fontweight="bold", bbox=dict(boxstyle="circle,pad=.2", fc="w", ec="none", alpha=.85))
ax.set_xlabel(""); ax.set_ylabel("")
ax.legend(handles=[Line2D([], [], color="#0077bb", lw=1.2, label="Karewa terraces (180, 173 km²)"),
                   Patch(fc="#d7191c", label="Vegetated 2013–15, bare 2023–25 (strict test; drawn enlarged)"),
                   Line2D([], [], color="#222222", lw=1, ls="--", label="Original study box")],
          loc="lower right", fontsize=8.5, framealpha=.95)
plt.tight_layout(); plt.savefig(OUT + "Figure_1_study_box_terraces_conversion.png", dpi=220); plt.close()
print("ok")
