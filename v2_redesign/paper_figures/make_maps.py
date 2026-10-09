"""Figures 1 and 3 of the revised paper.
Figure 1: study box, terraces and both conversion tests. Figure 3: Rangeen Kultreh, year from which each strict-test pixel stays bare.
Needs the rasters in data/raw (see DATA_ACCESS.md).
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
_me, _ml = np.median([OLI[y] for y in (2013, 2014, 2015)], 0), np.median([OLI[y] for y in (2023, 2024, 2025)], 0)
drop_only = (_me >= .45) & (_ml < .40) & (_me - _ml >= .20) & ~conv          # the drop test, minus what the strict test already flags
terr = gpd.read_file("v2_redesign/west_extension/karewa_terraces_wide.gpkg").to_crs(crs)
with rasterio.open("data/raw/StolenStrata_v2w_DEM_GLO30_buffered.tif") as d:   # raw export (EPSG:4326); reprojected below
    dem = np.full(shape, np.nan, "float32")
    reproject(rasterio.band(d, 1), dem, dst_transform=T, dst_crs=crs, resampling=Resampling.bilinear, dst_nodata=np.nan)
ext = (T.c, T.c + shape[1] * 30, T.f - shape[0] * 30, T.f)

fig, ax = plt.subplots(figsize=(11, 7.6))
ax.imshow(LightSource(315, 45).hillshade(np.nan_to_num(dem, nan=np.nanmean(dem)), vert_exag=2, dx=30, dy=30), cmap="gray", extent=ext, alpha=.9)
terr.boundary.plot(ax=ax, color="#0077bb", lw=.6)
ax.imshow(np.ma.masked_where(~ndi.binary_dilation(drop_only, iterations=2), np.ones(shape)), cmap=ListedColormap(["#fdae61"]), extent=ext, interpolation="nearest")
ax.imshow(np.ma.masked_where(~ndi.binary_dilation(conv, iterations=2), np.ones(shape)), cmap=ListedColormap(["#d7191c"]), extent=ext, interpolation="nearest")
old = gpd.GeoSeries([box(74.75, 33.85, 75.15, 34.15)], crs=4326).to_crs(crs)
old.boundary.plot(ax=ax, color="#222222", lw=1, ls="--")


def utm(lon, lat):
    x, y = warp_xy("EPSG:4326", crs, [lon], [lat]); return x[0], y[0]


for name, lon, lat, dx, dy in [("Rangeen Kultreh\nkiln field", 74.846, 33.944, -95, 18), ("Bandagam–Batapora\nkiln belt", 74.66, 34.02, -20, 62),
                               ("Pampore", 74.93, 34.016, 30, 20), ("Srinagar", 74.80, 34.085, -10, 28), ("Awantipora", 75.015, 33.92, 34, -10),
                               ("AIIMS campus works\n(not a kiln)", 75.02, 33.94, 55, 22), ("Dal Lake\n(water, not land)", 74.865, 34.115, 50, -12)]:
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
                   Patch(fc="#d7191c", label="Vegetated 2013–15, bare 2023–25 (strict test)"),
                   Patch(fc="#fdae61", label="Large fall in peak NDVI, drop test only"),
                   Line2D([], [], color="none", label="Flagged pixels drawn enlarged; all land covers"),
                   Line2D([], [], color="#222222", lw=1, ls="--", label="Original study box")],
          loc="lower right", fontsize=8.5, framealpha=.95)
plt.tight_layout(); plt.savefig(OUT + "Figure_1_study_box_terraces_conversion.png", dpi=220); plt.close()

# ---------------- Figure 3: Rangeen Kultreh, wide-box terraces 9 and 3, strict-test pixels by onset year ----------------
from rasterio.features import rasterize
from matplotlib.colors import BoundaryNorm
HA = 0.09
tid = rasterize([(g, int(i)) for g, i in zip(terr.geometry, terr.terrace_id)], out_shape=shape, transform=T)
yrs = list(range(2013, 2026))
stack = np.stack([OLI[y] < BARE for y in yrs])
stay = np.flip(np.cumprod(np.flip(stack, 0), 0), 0).astype(bool)          # bare from that year to 2025
first = np.where(stay.any(0), np.array(yrs)[stay.argmax(0)], 0)
k = conv & np.isin(tid, (9, 3))
GROUPS = [("2016", 2016, 2016, "#fee08b"), ("2017–2018", 2017, 2018, "#f46d43"), ("2019–2021", 2019, 2021, "#a50026"), ("2022–2023", 2022, 2023, "#542788")]
cls = np.zeros(shape, "uint8")
for n, (_, a0, a1, _) in enumerate(GROUPS, start=1):
    cls[k & (first >= a0) & (first <= a1)] = n
sub = terr[terr.terrace_id.isin([9, 3])]
x0, y0, x1, y1 = sub.total_bounds; pad = 400
fig, ax = plt.subplots(figsize=(8.5, 9.5))
ax.imshow(LightSource(315, 45).hillshade(np.nan_to_num(dem, nan=np.nanmean(dem)), vert_exag=3, dx=30, dy=30), cmap="gray", extent=ext, vmin=0, vmax=1)
ax.imshow(np.ma.masked_equal(cls, 0), cmap=ListedColormap([g[3] for g in GROUPS]), norm=BoundaryNorm(np.arange(.5, len(GROUPS) + 1), len(GROUPS)),
          extent=ext, interpolation="nearest")
sub.boundary.plot(ax=ax, color="#0077bb", lw=1.2)
for _, r in sub.iterrows():
    pt = r.geometry.representative_point(); ax.text(pt.x, pt.y, f"Terrace {r.terrace_id}", color="#0077bb", fontsize=10, ha="center", weight="bold")
ha_by = [(cls == n).sum() * HA for n in range(1, len(GROUPS) + 1)]
ax.legend(handles=[Patch(fc=g[3]) for g in GROUPS], labels=[f"Bare from {g[0]} ({h:.0f} ha)" for g, h in zip(GROUPS, ha_by)],
          title=f"Strict-test pixels on terraces 9 and 3 ({k.sum() * HA:.0f} ha)", loc="lower left", fontsize=8, title_fontsize=8, framealpha=.92)
ax.plot([x1 - 1200, x1 - 200], [y0 - 200, y0 - 200], color="k", lw=3); ax.text(x1 - 700, y0 - 140, "1 km", ha="center", fontsize=8)
ax.annotate("", (x1 + pad - 250, y1 + pad - 150), xytext=(x1 + pad - 250, y1 + pad - 900), arrowprops=dict(arrowstyle="-|>", lw=1.6, color="k"))
ax.text(x1 + pad - 250, y1 + pad - 1050, "N", ha="center", va="center", fontsize=10, fontweight="bold")
glon = np.arange(74.80, 74.91, 0.02); glat = np.arange(33.90, 33.97, 0.02)
ax.set_xticks([utm(l, 33.935)[0] for l in glon]); ax.set_xticklabels([f"{l:.2f}° E" for l in glon], fontsize=8)
ax.set_yticks([utm(74.85, l)[1] for l in glat]); ax.set_yticklabels([f"{l:.2f}° N" for l in glat], fontsize=8)
ax.set(xlim=(x0 - pad, x1 + pad), ylim=(y0 - pad, y1 + pad), xlabel="", ylabel="",
       title="Rangeen Kultreh: year from which each strict-test pixel stays bare (peak NDVI < 0.25) to 2025\nLandsat 8/9 only, 30 m; terrace numbers of the wide-box run; Copernicus DEM hillshade")
plt.tight_layout(); plt.savefig(OUT + "Figure_3_rangeen_kultreh_onset.png", dpi=200); plt.close()
print("ok")
