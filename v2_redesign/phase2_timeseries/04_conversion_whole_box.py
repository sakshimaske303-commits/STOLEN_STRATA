"""v2 Phase 2 — where is the vegetated -> persistently bare conversion in the WHOLE study box, and on what geology?

Uses the same test as 02 (Landsat 8/9 only: p90 NDVI >= 0.35 in all of 2013-15, < 0.25 in all of 2023-25) and the
Dar & Zeeden (2020) Karewa Group map tile from Phase 1 (schematic, ~100 m pixels, ~1 km positional error).

I run it from the repo root:  python v2_redesign/phase2_timeseries/04_conversion_whole_box.py
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from PIL import Image
from rasterio.transform import Affine, xy
from rasterio.features import rasterize
from rasterio.warp import reproject, Resampling, transform as warp_xy
from scipy import ndimage as ndi
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource

RAW = "data/raw/StolenStrata_v2_"
P1 = "v2_redesign/phase1_delineation"
OUT = "v2_redesign/phase2_timeseries"
BARE, VEG, HA = 0.25, 0.35, 0.09
ELEV_MAX = 2000.0                 # valley part of the box; above this is mountain side, outside the geology map's units
GROUP_PX = 5                      # converted pixels closer than ~150 m are treated as one cluster
MIN_CLUSTER_HA = 2.0

with rasterio.open(RAW + "OLIonly_p90_2013_2025.tif") as s:
    a = s.read().astype("float32"); a[a == -32768] = np.nan
    OLI = {int(d[-4:]): a[i] / 1e4 for i, d in enumerate(s.descriptions)}
    T, crs, shape = s.transform, s.crs, s.shape

conv = np.all([OLI[y] >= VEG for y in (2013, 2014, 2015)], 0) & np.all([OLI[y] < BARE for y in (2023, 2024, 2025)], 0)
veg0 = np.all([OLI[y] >= VEG for y in (2013, 2014, 2015)], 0)       # what could have converted

# ---- geology tile -> Landsat grid (same legend colours and georeferencing as Phase 1 script 04) ----
REFS = {"alluvium": [(110, 105, 51), (128, 122, 70)], "dilpur_fm": [(85, 48, 25)], "reworked_karewa": [(75, 104, 23)],
        "pampur_mb": [(26, 86, 106)], "hirpur_fm": [(147, 46, 46), (173, 83, 83)],
        "nagum_other": [(126, 79, 116), (90, 30, 80)], "water": [(20, 93, 205)]}
names = list(REFS)
im = np.asarray(Image.open(os.path.join(P1, "geology", "karewa_group_map_tile.jpg")).convert("RGB")).astype(float)
best = np.full(im.shape[:2], -1); bd = np.full(im.shape[:2], 1e9)
for k, n in enumerate(names):
    for c in REFS[n]:
        d = np.sqrt(((im - np.array(c)) ** 2).sum(2)); m = d < bd; bd[m] = d[m]; best[m] = k
gcls = np.where(((im.max(2) - im.min(2)) < 25) | (bd > 45), -1, best).astype("int16")
S = 1 / 0.78125
GT = Affine(S / 1419.0, 0, 75 + (1100 - 1587) / 1419.0, 0, -S / 1417.0, 34 - (800 - 1065) / 1417.0)
geo = np.full(shape, -1, "int16")
reproject(gcls, geo, src_transform=GT, src_crs="EPSG:4326", dst_transform=T, dst_crs=crs,
          resampling=Resampling.nearest, src_nodata=-9999, dst_nodata=-1)
unit = np.full(shape, "unmapped", dtype=object)
unit[np.isin(geo, [names.index(n) for n in ("dilpur_fm", "pampur_mb", "hirpur_fm", "nagum_other")])] = "karewa_formation"
unit[geo == names.index("reworked_karewa")] = "reworked_karewa"
unit[geo == names.index("alluvium")] = "alluvium"
unit[geo == names.index("water")] = "water"

with rasterio.open("data/interim/DEM_buffered_UTM43N.tif") as d:
    dem = np.full(shape, np.nan, "float32")
    reproject(rasterio.band(d, 1), dem, dst_transform=T, dst_crs=crs, resampling=Resampling.bilinear, dst_nodata=np.nan)
gy, gx = np.gradient(ndi.gaussian_filter(np.nan_to_num(dem, nan=np.nanmean(dem)), 1.0), 30)
slope = np.degrees(np.arctan(np.hypot(gx, gy)))
valley = dem < ELEV_MAX

terr = gpd.read_file(os.path.join(P1, "karewa_terraces_v2.gpkg")).to_crs(crs)
proto = gpd.read_file(os.path.join(P1, "karewa_flat_tops_prototype.gpkg")).to_crs(crs)
m_terr = rasterize([(g, 1) for g in terr.geometry], out_shape=shape, transform=T) == 1
m_flat = (rasterize([(g, 1) for g in proto.geometry], out_shape=shape, transform=T) == 1) & ~m_terr

# ---- 1. rate by geology unit, inside and outside the v2 terraces ---------------------------
rows = []
for u in ("karewa_formation", "reworked_karewa", "alluvium", "unmapped"):
    for where, mk in (("inside_v2_terraces", m_terr), ("outside_v2_terraces", ~m_terr)):
        m = (unit == u) & mk & valley
        rows.append(dict(geology=u, where=where, area_km2=m.sum() * HA / 100, vegetated_2013_15_km2=(m & veg0).sum() * HA / 100,
                         converted_ha=(m & conv).sum() * HA,
                         converted_pct_of_vegetated=(m & conv).sum() / max((m & veg0).sum(), 1) * 100))
m = ~valley
rows.append(dict(geology="above_2000m", where="", area_km2=m.sum() * HA / 100, vegetated_2013_15_km2=(m & veg0).sum() * HA / 100,
                 converted_ha=(m & conv).sum() * HA, converted_pct_of_vegetated=(m & conv).sum() / max((m & veg0).sum(), 1) * 100))
by_geo = pd.DataFrame(rows)
by_geo.round(3).to_csv(os.path.join(OUT, "conversion_by_geology.csv"), index=False)

# ---- 2. clusters ------------------------------------------------------------------------------
grp, n = ndi.label(ndi.binary_dilation(conv, iterations=GROUP_PX // 2 + 1))
grp = np.where(conv, grp, 0)
idx = np.arange(1, n + 1)
ha = ndi.sum(conv, grp, idx) * HA
rows = []
for i in idx[ha >= MIN_CLUSTER_HA]:
    m = grp == i
    r, c = np.nonzero(m)
    x, y = xy(T, r.mean(), c.mean())
    lon, lat = warp_xy(crs, "EPSG:4326", [x], [y])
    u = pd.Series(unit[m]).value_counts(normalize=True)
    rows.append(dict(converted_ha=m.sum() * HA, lat=round(lat[0], 4), lon=round(lon[0], 4),
                     mean_elev_m=float(np.nanmean(dem[m])), mean_slope_deg=float(slope[m].mean()),
                     on_v2_terrace=float(m_terr[m].mean()), on_other_flat=float(m_flat[m].mean()),
                     karewa_formation=float(u.get("karewa_formation", 0)), reworked_karewa=float(u.get("reworked_karewa", 0)),
                     alluvium=float(u.get("alluvium", 0)), unmapped=float(u.get("unmapped", 0)),
                     km_from_west_edge=(x - (T.c)) / 1000,
                     google_maps=f"https://www.google.com/maps/@{lat[0]:.5f},{lon[0]:.5f},16z/data=!3m1!1e3"))
cl = pd.DataFrame(rows).sort_values("converted_ha", ascending=False).reset_index(drop=True)
cl.insert(0, "cluster", cl.index + 1)
cl.round(2).to_csv(os.path.join(OUT, "conversion_clusters_whole_box.csv"), index=False)

# ---- 3. map -------------------------------------------------------------------------------------
ext = (T.c, T.c + shape[1] * 30, T.f - shape[0] * 30, T.f)
fig, ax = plt.subplots(figsize=(11, 9.5))
ax.imshow(LightSource(315, 45).hillshade(np.nan_to_num(dem, nan=np.nanmean(dem)), vert_exag=2, dx=30, dy=30), cmap="gray", extent=ext)
kf = np.ma.masked_where(unit != "karewa_formation", np.ones(shape))
ax.imshow(kf, cmap="YlOrBr", vmin=0, vmax=2.5, alpha=.35, extent=ext)
terr.boundary.plot(ax=ax, color="#00b7ff", lw=.7)
big = ndi.binary_dilation(conv, iterations=2)
ax.imshow(np.ma.masked_where(~big, np.ones(shape)), cmap="autumn", vmin=1, vmax=3, extent=ext, interpolation="nearest")
for _, r in cl.head(12).iterrows():
    x, y = warp_xy("EPSG:4326", crs, [r.lon], [r.lat])
    ax.annotate(f"{int(r.cluster)}: {r.converted_ha:.0f} ha", (x[0], y[0]), xytext=(8, 8), textcoords="offset points", fontsize=8,
                color="k", bbox=dict(boxstyle="round,pad=.2", fc="w", ec="none", alpha=.85))
ax.set(xticks=[], yticks=[], title="Vegetated in 2013–15, persistently bare in 2023–25 (red; Landsat 8/9 only, drawn enlarged)\n"
       "Shaded tan = Karewa formations on the Dar & Zeeden (2020) map; blue outlines = v2 terraces")
plt.tight_layout(); plt.savefig(os.path.join(OUT, "conversion_whole_box_map.png"), dpi=170); plt.close()

pd.set_option("display.width", 250)
print(by_geo.round(2).to_string(index=False))
print("total converted ha:", conv.sum() * HA, "| in clusters >= %.0f ha: %.1f (%d clusters)" % (MIN_CLUSTER_HA, cl.converted_ha.sum(), len(cl)))
print(cl.drop(columns="google_maps").head(25).round(2).to_string(index=False))
