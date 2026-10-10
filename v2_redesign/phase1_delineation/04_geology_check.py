"""v2 Phase 1 — independent check of the flat-top delineation against a published Karewa Group map.

Reference: Dar & Zeeden (2020, Front. Earth Sci. 8:113), Fig. 2, "after Bhatt (1982)" — see
geology/SOURCE.md for how the crop was captured and georeferenced. The map is schematic
(about 100 m pixels, roughly 1 km positional error), so this is a coarse check.

Outputs (in v2_redesign/phase1_delineation/):
  geology_polygon_table.csv   share of each prototype polygon on Karewa formations / reworked / alluvium
  geology_summary.csv         the same per layer, plus wall-to-wall agreement for the v2 terraces
  geology_threshold_table.csv precision/recall of the scarp-share cut-off against the map

I run it from the repo root:  python v2_redesign/phase1_delineation/04_geology_check.py
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from PIL import Image
from rasterio.transform import Affine
from rasterio.features import rasterize
from rasterio.warp import reproject, Resampling
from scipy import ndimage as ndi
from scipy.stats import spearmanr
from shapely.geometry import box

OUT = "v2_redesign/phase1_delineation"
TILE = os.path.join(OUT, "geology", "karewa_group_map_tile.jpg")
DEM = "data/interim/DEM_buffered_UTM43N.tif"
AOI_LONLAT = (74.75, 33.85, 75.15, 34.15)
ELEV_MAX = 2000.0
MIN_PX_FOR_POLYGON_STATS = 60        # ~0.5 km2 on the map grid; smaller polygons are below the map's resolution

# legend colours as they appear in the crop (k-means centres)
REFS = {"alluvium": [(110, 105, 51), (128, 122, 70)], "dilpur_fm": [(85, 48, 25)], "reworked_karewa": [(75, 104, 23)],
        "pampur_mb": [(26, 86, 106)], "hirpur_fm": [(147, 46, 46), (173, 83, 83)],
        "nagum_other": [(126, 79, 116), (90, 30, 80)], "water": [(20, 93, 205)]}
KAREWA_UNITS = ["dilpur_fm", "pampur_mb", "hirpur_fm", "nagum_other"]     # in-situ Karewa Group

im = np.asarray(Image.open(TILE).convert("RGB")).astype(float)
names = list(REFS)
best = np.full(im.shape[:2], -1); bd = np.full(im.shape[:2], 1e9)
for k, n in enumerate(names):
    for c in REFS[n]:
        d = np.sqrt(((im - np.array(c)) ** 2).sum(2)); m = d < bd; bd[m] = d[m]; best[m] = k
grey = (im.max(2) - im.min(2)) < 25                      # hillshaded mountains, text
cls = np.where(grey | (bd > 45), -1, best)

S = 1 / 0.78125                                           # figure px per crop px
T = Affine(S / 1419.0, 0, 75 + (1100 - 1587) / 1419.0, 0, -S / 1417.0, 34 - (800 - 1065) / 1417.0)
cell_km2 = (S / 1419.0 * 92.5) * (S / 1417.0 * 111.0)     # km per degree at 34N: ~92.5 (lon), ~111 (lat)

kar = np.isin(cls, [names.index(n) for n in KAREWA_UNITS])
rew = cls == names.index("reworked_karewa")
allu = cls == names.index("alluvium")
valid = (cls >= 0) & (cls != names.index("water"))

def ras(geoms):
    return rasterize([(x, 1) for x in geoms], out_shape=cls.shape, transform=T, fill=0).astype(bool)

with rasterio.open(DEM) as src:
    z = src.read(1).astype(float); z[z == src.nodata] = np.nan
    zf = np.where(np.isnan(z), np.nanmean(z), z)
    dy, dx = np.gradient(ndi.gaussian_filter(zf, 1.0), src.transform.a)
    slope = np.degrees(np.arctan(np.hypot(dx, dy)))
    def warp(a):
        o = np.full(cls.shape, np.nan, "float32")
        reproject(a.astype("float32"), o, src_transform=src.transform, src_crs=src.crs,
                  dst_transform=T, dst_crs="EPSG:4326", resampling=Resampling.average)
        return o
    elev_w, slope_w = warp(zf), warp(slope)

aoi = ras([box(*AOI_LONLAT)])
domain = aoi & valid & (elev_w < ELEV_MAX)

proto = gpd.read_file(os.path.join(OUT, "karewa_flat_tops_prototype.gpkg"))
v2 = gpd.read_file(os.path.join(OUT, "karewa_terraces_v2.gpkg"))
pw, vw = proto.to_crs(4326), v2.to_crs(4326)

# ---- per polygon ----
rows = []
for tid, geom in zip(pw.terrace_id, pw.geometry):
    m = ras([geom]) & valid
    n = int(m.sum())
    rows.append(dict(terrace_id=tid, map_px=n,
                     karewa_fm=(m & kar).sum() / n if n else np.nan,
                     reworked=(m & rew).sum() / n if n else np.nan,
                     alluvium=(m & allu).sum() / n if n else np.nan))
poly = pd.DataFrame(rows).merge(proto[["terrace_id", "cls", "scarp_frac", "area_km2", "share_in_aoi", "mean_elev"]], on="terrace_id")
poly.round(3).to_csv(os.path.join(OUT, "geology_polygon_table.csv"), index=False)

big = poly[(poly.map_px >= MIN_PX_FOR_POLYGON_STATS) & (poly.share_in_aoi > 0.5)].copy()
rho, p = spearmanr(big.scarp_frac, big.karewa_fm)
print(f"Polygons >= ~0.5 km2 inside the box: {len(big)}; Spearman(scarp share, share on Karewa formations) = {rho:.2f} (p = {p:.1e})")
big["on_karewa"] = big.karewa_fm >= 0.6
thr = []
for t in [0.15, 0.20, 0.25, 0.30, 0.35, 0.45, 0.50]:
    pred = big.scarp_frac >= t; tp = int((pred & big.on_karewa).sum())
    thr.append(dict(scarp_min=t, polygons_kept=int(pred.sum()), precision=round(tp / max(pred.sum(), 1), 2),
                    recall=round(tp / big.on_karewa.sum(), 2),
                    area_weighted_share_on_karewa=round((big.area_km2 * big.karewa_fm)[pred].sum() / big.area_km2[pred].sum(), 2)))
thr = pd.DataFrame(thr); thr.to_csv(os.path.join(OUT, "geology_threshold_table.csv"), index=False)
print(thr.to_string(index=False))

# ---- per layer, wall to wall ----
def layer_row(name, mask):
    m = mask & domain; n = m.sum()
    return dict(layer=name, area_km2=round(n * cell_km2, 1), on_karewa_fm=round((m & kar).sum() / n, 2),
                on_reworked=round((m & rew).sum() / n, 2), on_alluvium=round((m & allu).sum() / n, 2))
kept = ras(vw.geometry)
layers = [layer_row("v2 terraces (scarp share >= 0.25)", kept)]
for c in ["scarp_bounded", "ambiguous", "rejected"]:
    layers.append(layer_row(f"prototype: {c}", ras(pw[pw.cls == c].geometry)))
layers.append(layer_row("whole study box below 2000 m", np.ones_like(kept)))
summ = pd.DataFrame(layers)

flat_kar = kar & domain & (slope_w < 4)
agree = dict(
    users_accuracy=round((kept & kar & domain).sum() / (kept & domain).sum(), 3),
    producers_accuracy_all_karewa_fm=round((kept & kar & domain).sum() / (kar & domain).sum(), 3),
    producers_accuracy_flat_karewa_fm=round((kept & flat_kar).sum() / flat_kar.sum(), 3),
    mapped_karewa_fm_km2=round((kar & domain).sum() * cell_km2, 1),
    flat_mapped_karewa_fm_km2=round(flat_kar.sum() * cell_km2, 1))
# sensitivity of user's accuracy to map misregistration (shift the map by up to ~0.6 km)
ua = []
for dy_ in range(-6, 7, 2):
    for dx_ in range(-6, 7, 2):
        k2 = np.roll(np.roll(kar, dy_, 0), dx_, 1); d2 = np.roll(np.roll(domain, dy_, 0), dx_, 1)
        ua.append((kept & k2 & d2).sum() / (kept & d2).sum())
agree["users_accuracy_range_under_0.6km_shift"] = f"{min(ua):.2f}-{max(ua):.2f}"
summ.to_csv(os.path.join(OUT, "geology_summary.csv"), index=False)
pd.Series(agree).to_csv(os.path.join(OUT, "geology_agreement.csv"), header=["value"])
print(summ.to_string(index=False)); print(pd.Series(agree).to_string())
