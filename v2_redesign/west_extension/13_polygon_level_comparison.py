"""v2 extended box: terraces against other flat, raised land, compared polygon by polygon.

The stratum rates in Table 1 count pixels. Converted pixels are not independent: they sit in a handful of clusters, and
82% of the strict-test area is on two terraces. This script therefore compares whole polygons: for each terrace and for
each other flat top (the flat tops that are not terraces, at least 0.05 km^2 inside the raster), the share of its area
converted by the strict and the drop test, with and without the two kiln-belt site boxes used in 08_long_series_wide.py.
A polygon counts as "in a belt" when more than half of its area lies inside one of the two boxes.

I run it from the repo root:  python v2_redesign/west_extension/13_polygon_level_comparison.py
Output: v2_redesign/west_extension/polygon_level_comparison.csv (one row per polygon)
        v2_redesign/west_extension/polygon_level_summary.csv
"""
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from scipy.stats import mannwhitneyu
from shapely.geometry import box

W = "v2_redesign/west_extension/"
HA = 0.09
with rasterio.open("data/raw/StolenStrata_v2w_OLIonly_p90_2013_2025.tif") as s:
    a = s.read().astype("float32"); a[a == -32768] = np.nan
    D = {int(d[-4:]): a[i] / 1e4 for i, d in enumerate(s.descriptions)}
    T, crs, shape = s.transform, s.crs, s.shape

E, L = (2013, 2014, 2015), (2023, 2024, 2025)
strict = np.all([D[y] >= .35 for y in E], 0) & np.all([D[y] < .25 for y in L], 0)
me, ml = np.median([D[y] for y in E], 0), np.median([D[y] for y in L], 0)
drop = (me >= .45) & (ml < .40) & (me - ml >= .20)

t = gpd.read_file(W + "karewa_terraces_wide.gpkg").to_crs(crs)
p = gpd.read_file(W + "karewa_flat_tops_wide.gpkg").to_crs(crs)
tid = rasterize([(g, int(i)) for g, i in zip(t.geometry, t.terrace_id)], out_shape=shape, transform=T)
pid = rasterize([(g, i + 1) for i, g in enumerate(p.geometry)], out_shape=shape, transform=T)
mt = tid > 0


def window(lon0, lat0, lon1, lat1):
    g = gpd.GeoSeries([box(lon0, lat0, lon1, lat1)], crs=4326).to_crs(crs).iloc[0]
    return rasterize([(g, 1)], out_shape=shape, transform=T) == 1


belt = window(74.83, 33.925, 74.87, 33.958) | window(74.60, 33.99, 74.72, 34.05)

rows = []
for i in t.terrace_id:
    m = tid == int(i)
    rows.append(dict(kind="terrace", id=int(i), px=int(m.sum()), strict_px=int(strict[m].sum()), drop_px=int(drop[m].sum()), belt_share=float(belt[m].mean())))
for i in range(1, len(p) + 1):
    m = (pid == i) & ~mt
    if m.sum() * HA / 100 < 0.05:
        continue
    rows.append(dict(kind="other_flat", id=i, px=int(m.sum()), strict_px=int(strict[m].sum()), drop_px=int(drop[m].sum()), belt_share=float(belt[m].mean())))
r = pd.DataFrame(rows)
r["strict_ha"], r["drop_ha"] = r.strict_px * HA, r.drop_px * HA
r["strict_pct"], r["drop_pct"] = r.strict_px / r.px * 100, r.drop_px / r.px * 100
r["in_belt"] = r.belt_share > 0.5
r.round(4).to_csv(W + "polygon_level_comparison.csv", index=False)

out = []
for label, q in (("all polygons", r), ("outside the two belts", r[~r.in_belt])):
    tt, ff = q[q.kind == "terrace"], q[q.kind == "other_flat"]
    row = dict(selection=label, n_terraces=len(tt), n_other_flat=len(ff))
    for col, thr in (("strict_ha", 1), ("drop_ha", 1), ("drop_ha", 5)):
        row[f"terraces_with_{col}_ge_{thr}_pct"] = (tt[col] >= thr).mean() * 100
        row[f"other_flat_with_{col}_ge_{thr}_pct"] = (ff[col] >= thr).mean() * 100
    for col in ("strict_pct", "drop_pct"):
        row[f"{col}_mean_terraces"], row[f"{col}_mean_other_flat"] = tt[col].mean(), ff[col].mean()
        row[f"{col}_mannwhitney_p_terraces_greater"] = mannwhitneyu(tt[col], ff[col], alternative="greater").pvalue
    out.append(row)
summ = pd.DataFrame(out)
summ.round(4).to_csv(W + "polygon_level_summary.csv", index=False)
pd.set_option("display.width", 250)
print(summ.round(3).T.to_string())
