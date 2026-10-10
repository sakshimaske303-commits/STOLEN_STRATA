"""Section 4.1 check: the earlier rule (June-September NDVI < 0.15) on the earlier 201 polygons,
computed with the SAME statistic the earlier version reported (unweighted mean of the per-polygon
shares) as well as the pooled pixel share, on Landsat only.

It also puts the earlier Sentinel-2 2025 raster on the Landsat 30 m grid, to show that pixel size
is not what produced the 2025 jump, and compares the NDVI levels of the two 2025 products.

I run it from the repo root:  python v2_redesign/phase2_timeseries/05_v1_rule_matched_statistic.py
Inputs : data/processed/karewa_multitemporal_trend.gpkg          (earlier polygons and their reported shares)
         data/raw/StolenStrata_v2_LS_summer_1990_2025.tif        (Landsat-only June-September median, per year)
         data/raw/StolenStrata_NDVI_2025.tif                      (earlier Sentinel-2 2025 composite)
Output : v2_redesign/phase2_timeseries/v1_rule_matched_statistic.csv
         v2_redesign/phase2_timeseries/v1_2025_product_comparison.csv
"""
import warnings
import numpy as np, pandas as pd, geopandas as gpd, rasterio
from rasterio.features import rasterize
from rasterio.warp import reproject, Resampling
warnings.filterwarnings("ignore")

OUT = "v2_redesign/phase2_timeseries/"
THR = 0.15
g = gpd.read_file("data/processed/karewa_multitemporal_trend.gpkg")

s = rasterio.open("data/raw/StolenStrata_v2_LS_summer_1990_2025.tif")
a = s.read().astype("float32"); a[a == -32768] = np.nan
SUM = {int(d[-4:]): a[i] / 1e4 for i, d in enumerate(s.descriptions)}
gg = g.to_crs(s.crs)
pid = rasterize([(geom, i + 1) for i, geom in enumerate(gg.geometry)], out_shape=s.shape, transform=s.transform)

def two_ways(img):
    """(pooled pixel share, unweighted mean of per-polygon shares), both in percent."""
    v = img[pid > 0]; pooled = (v[np.isfinite(v)] < THR).mean() * 100
    per = []
    for i in range(1, len(gg) + 1):
        w = img[pid == i]; w = w[np.isfinite(w)]
        if w.size: per.append((w < THR).mean())
    return round(float(pooled), 2), round(float(np.mean(per)) * 100, 2)

rows = []
for y in (1994, 2005, 2015, 2025):
    col = f"bare_frac_{y}"
    pooled, mean_poly = two_ways(SUM[y])
    rows.append(dict(year=y,
                     earlier_reported_mean_of_polygons_pct=round(g[col].mean() * 100, 2),
                     earlier_area_weighted_pct=round((g[col] * g.area_km2).sum() / g.area_km2.sum() * 100, 2),
                     landsat_only_mean_of_polygons_pct=mean_poly,
                     landsat_only_pooled_pct=pooled))
t = pd.DataFrame(rows); t.to_csv(OUT + "v1_rule_matched_statistic.csv", index=False); print(t.to_string(index=False))

# the earlier Sentinel-2 2025 raster, averaged onto the Landsat 30 m grid
src = rasterio.open("data/raw/StolenStrata_NDVI_2025.tif")
s2 = np.full(s.shape, np.nan, "float32")
reproject(rasterio.band(src, 1), s2, dst_transform=s.transform, dst_crs=s.crs, resampling=Resampling.average, dst_nodata=np.nan)
pooled_s2, mean_s2 = two_ways(s2)
m = (pid > 0) & np.isfinite(s2) & np.isfinite(SUM[2025])
c = pd.DataFrame([dict(
    product="earlier Sentinel-2 2025 composite, averaged to 30 m", below_015_mean_of_polygons_pct=mean_s2, below_015_pooled_pct=pooled_s2,
    median_ndvi_on_polygons=round(float(np.median(s2[m])), 3)),
    dict(product="Landsat-only June-September median 2025", below_015_mean_of_polygons_pct=two_ways(SUM[2025])[1],
         below_015_pooled_pct=two_ways(SUM[2025])[0], median_ndvi_on_polygons=round(float(np.median(SUM[2025][m])), 3))])
c.to_csv(OUT + "v1_2025_product_comparison.csv", index=False); print(c.to_string(index=False))
print("median pixel difference (Sentinel-2 product minus Landsat):", round(float(np.median(s2[m] - SUM[2025][m])), 3))
