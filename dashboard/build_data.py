"""Builds the small map and series files the dashboard reads, from the v2 results and the rasters.

The dashboard itself needs no rasters: it reads the result tables in v2_redesign/ and the files written here.
Run from the repo root, after the v2_redesign scripts and with the rasters in data/raw (see DATA_ACCESS.md):
    python dashboard/build_data.py
Writes to dashboard/map_data/: terraces.geojson, flagged.geojson, accuracy_points.csv, site_yearly.csv, block_yearly.csv, summary.json
"""
import json
import numpy as np, pandas as pd, geopandas as gpd, rasterio
from rasterio.features import rasterize, shapes
from shapely.geometry import box, shape as shp
from shapely.ops import unary_union

RAW = "data/raw/StolenStrata_v2w_"
W = "v2_redesign/west_extension/"
OUT = "dashboard/map_data/"
HA = 0.09


def load(name, scale=1e4):
    with rasterio.open(RAW + name) as s:
        a = s.read().astype("float32"); a[a == -32768] = np.nan
        return s.transform, s.crs, s.shape, {int(d[-4:]): a[i] / scale for i, d in enumerate(s.descriptions)}


T, crs, shape, OLI = load("OLIonly_p90_2013_2025.tif")
LS = {**load("LS_p90_1990_2007.tif")[3], **load("LS_p90_2008_2025_fixed.tif")[3]}   # corrected Landsat 8/9 adjustment (gee_05_long_series_fixed.js)
CNT = load("LS_counts_1990_2025.tif", 1)[3]
t = gpd.read_file(W + "karewa_terraces_wide.gpkg").to_crs(crs)
tid = rasterize([(g, int(i)) for g, i in zip(t.geometry, t.terrace_id)], out_shape=shape, transform=T); mt = tid > 0

# the two tests of the paper (Section 3.4), Landsat 8/9 only
E, L = (2013, 2014, 2015), (2023, 2024, 2025)
strict = np.all([OLI[y] >= 0.35 for y in E], 0) & np.all([OLI[y] < 0.25 for y in L], 0)
a, b = np.median([OLI[y] for y in E], 0), np.median([OLI[y] for y in L], 0)
drop = (a >= 0.45) & (b < 0.40) & (a - b >= 0.20)
drop_only = drop & ~strict
print("strict on terraces %.1f ha | drop %.1f ha | drop only %.1f ha" % ((strict & mt).sum() * HA, (drop & mt).sum() * HA, (drop_only & mt).sum() * HA))

# ---- terraces -----------------------------------------------------------------------------------
per = pd.DataFrame({"terrace_id": t.terrace_id.astype(int)})
per["strict_ha"] = [round(float((strict & (tid == i)).sum() * HA), 2) for i in per.terrace_id]
per["drop_ha"] = [round(float((drop & (tid == i)).sum() * HA), 2) for i in per.terrace_id]
tt = t[["terrace_id", "area_km2", "scarp_frac", "geometry"]].merge(per, on="terrace_id")
tt["area_km2"] = tt.area_km2.round(3); tt["scarp_frac"] = tt.scarp_frac.round(2)
tt["geometry"] = tt.geometry.simplify(25)
tt.to_crs(4326).to_file(OUT + "terraces.geojson", driver="GeoJSON", COORDINATE_PRECISION=5)

# ---- flagged pixels on terraces, as polygons ------------------------------------------------------
feats = []
for name, m in (("strict", strict & mt), ("drop_only", drop_only & mt)):
    geoms = [shp(g) for g, v in shapes(m.astype("uint8"), mask=m, transform=T) if v == 1]
    feats.append(dict(test=name, ha=round(float(m.sum() * HA), 1), geometry=unary_union(geoms)))
gpd.GeoDataFrame(feats, crs=crs).to_crs(4326).to_file(OUT + "flagged.geojson", driver="GeoJSON", COORDINATE_PRECISION=5)

# ---- accuracy sample ------------------------------------------------------------------------------
# both samples (1-120 and 121-240), pooled by 15_pooled_accuracy.py, kiln-field edges under one rule (16_kiln_rule_result.py)
xy = pd.concat([pd.read_csv(W + "accuracy_sample_points.csv")[["point_id", "lat", "lon"]],
                pd.read_csv(W + "accuracy_sample2_points.csv")[["point_id", "lat", "lon"]]])
pts = xy.merge(pd.read_csv(W + "kiln_rule_points.csv")[["point_id", "draw", "stratum", "terrace_id", "p90_2013_15", "p90_2023_25", "final_rule", "before_label"]]
               .rename(columns={"final_rule": "final"}), on="point_id")
pts.to_csv(OUT + "accuracy_points.csv", index=False)

# ---- yearly series by site (adjusted Landsat series, usable years only) ---------------------------
def window(lon0, lat0, lon1, lat1):
    g = gpd.GeoSeries([box(lon0, lat0, lon1, lat1)], crs=4326).to_crs(crs).iloc[0]
    return rasterize([(g, 1)], out_shape=shape, transform=T) == 1


rk, bb = window(74.83, 33.925, 74.87, 33.958), window(74.60, 33.99, 74.72, 34.05)
SITES = {"Rangeen Kultreh terraces": mt & rk, "Bandagam-Batapora terraces": mt & bb, "All other terraces": mt & ~rk & ~bb}
rows = []
for y in range(1990, 2026):
    n = float(np.median(CNT[y][mt]))
    for k, m in SITES.items():
        v = LS[y][m]; v = v[np.isfinite(v)]
        rows.append(dict(year=y, site=k, median_clear_obs=n, usable=n >= 10, below_035_pct=round(float((v < 0.35).mean() * 100), 2),
                         below_035_ha=round(float((v < 0.35).sum() * HA), 1), median_peak_ndvi=round(float(np.median(v)), 3)))
pd.DataFrame(rows).to_csv(OUT + "site_yearly.csv", index=False)

# ---- the pixels that converted at Rangeen Kultreh: their yearly peak NDVI ---------------------------
blk = strict & mt & rk
rows = []
for y in range(1990, 2026):
    v = LS[y][blk]; v = v[np.isfinite(v)]
    o = OLI[y][blk] if y in OLI else None
    rows.append(dict(year=y, usable=float(np.median(CNT[y][mt])) >= 10, pixels=int(blk.sum()), median_peak_ndvi_landsat=round(float(np.median(v)), 3),
                     median_peak_ndvi_landsat89=None if o is None else round(float(np.nanmedian(o)), 3),
                     bare_ha_landsat89=None if o is None else round(float((OLI[y][mt & rk] < 0.25).sum() * HA), 1)))
pd.DataFrame(rows).to_csv(OUT + "block_yearly.csv", index=False)
print("block pixels", int(blk.sum()), "=", round(blk.sum() * HA, 1), "ha")

# ---- counts quoted on the pages ----------------------------------------------------------------------
ft = gpd.read_file(W + "karewa_flat_tops_wide.gpkg")
json.dump(dict(flat_tops=int(len(ft)), flat_tops_scarp_025=int((ft.scarp_frac >= 0.25).sum()), terraces=int(len(t)),
               terrace_km2=round(float(mt.sum() * HA / 100), 1), rangeen_block_ha=round(float(blk.sum() * HA), 1)),
          open(OUT + "summary.json", "w"), indent=1)
