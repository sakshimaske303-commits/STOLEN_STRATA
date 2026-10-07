"""12_robustness_and_effect_sizes.py — resolution-mismatch check (resample 2025 to 30m) + effect sizes/Holm-Bonferroni across the 4 Mann-Whitney tests."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

import geopandas as gpd
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.mask import mask
import numpy as np
from scipy.stats import mannwhitneyu

# ============================================================
# Part 1 — Resample 2025 Sentinel-2 to 30m, recompute bare-earth fraction
# ============================================================
DST_CRS = config.DST_CRS
src_path = 'data/raw/StolenStrata_NDVI_2025.tif'
dst_path = 'data/interim/NDVI_2025_UTM43N_30m.tif'

with rasterio.open(src_path) as src:
    transform, width, height = calculate_default_transform(
        src.crs, DST_CRS, src.width, src.height, *src.bounds, resolution=30)
    kwargs = src.meta.copy()
    kwargs.update({'crs': DST_CRS, 'transform': transform, 'width': width, 'height': height})
    with rasterio.open(dst_path, 'w', **kwargs) as dst:
        reproject(
            source=rasterio.band(src, 1), destination=rasterio.band(dst, 1),
            src_transform=src.transform, src_crs=src.crs,
            dst_transform=transform, dst_crs=DST_CRS,
            resampling=Resampling.average)  # area-average downsample, not nearest/bilinear
print(f"Resampled 2025 Sentinel-2 NDVI to 30m: {width}x{height} px")

gdf = gpd.read_file('data/processed/karewa_bare_earth_change.gpkg')

BARE_THRESHOLD = config.BARE_EARTH_NDVI_THRESHOLD
def zonal_bare_fraction(geom, raster_path, threshold=BARE_THRESHOLD):
    with rasterio.open(raster_path) as src:
        try:
            out_image, _ = mask(src, [geom], crop=True, nodata=np.nan)
            valid = out_image[~np.isnan(out_image)]
            if valid.size == 0:
                return np.nan
            return float(np.mean(valid < threshold))
        except Exception:
            return np.nan

gdf['bare_frac_2025_30m'] = gdf.geometry.apply(lambda g: zonal_bare_fraction(g, dst_path))

mean_10m = gdf['bare_frac_2025'].mean() * 100
mean_30m = gdf['bare_frac_2025_30m'].mean() * 100
bare_1994_ha = (gdf['area_km2'] * gdf['bare_frac_1994']).sum() * 100
bare_2025_10m_ha = (gdf['area_km2'] * gdf['bare_frac_2025']).sum() * 100
bare_2025_30m_ha = (gdf['area_km2'] * gdf['bare_frac_2025_30m']).sum() * 100
degraded_10m = int((gdf['bare_frac_2025'] - gdf['bare_frac_1994'] >= config.DEGRADATION_LOSS_THRESHOLD).sum())
degraded_30m = int((gdf['bare_frac_2025_30m'] - gdf['bare_frac_1994'] >= config.DEGRADATION_LOSS_THRESHOLD).sum())

print("\n=== Resolution-mismatch robustness check ===")
print(f"Mean bare-earth fraction, 2025 @ native ~10m Sentinel-2: {mean_10m:.2f}%")
print(f"Mean bare-earth fraction, 2025 @ resampled 30m:          {mean_30m:.2f}%  ({mean_30m-mean_10m:+.2f}pp)")
print(f"Net conversion (1994->2025) @ 10m: {bare_2025_10m_ha-bare_1994_ha:.1f} ha")
print(f"Net conversion (1994->2025) @ 30m: {bare_2025_30m_ha-bare_1994_ha:.1f} ha")
print(f"Degraded terrace count @ 10m: {degraded_10m}   @ 30m: {degraded_30m}")
trend = gpd.read_file('data/processed/karewa_multitemporal_trend.gpkg')
mean_2005 = trend['bare_frac_2005'].mean() * 100
mean_2015 = trend['bare_frac_2015'].mean() * 100
jump_10m = mean_10m - mean_2015
jump_30m = mean_30m - mean_2015
net_10m = bare_2025_10m_ha - bare_1994_ha
net_30m = bare_2025_30m_ha - bare_1994_ha
print(f"Reduction in net 1994->2025 conversion from resolution matching: {100*(net_10m-net_30m)/net_10m:.1f}%")
print(f"Post-2015 jump (2015->2025): {jump_10m:.2f}pp @10m vs {jump_30m:.2f}pp @30m "
      f"({100*(jump_10m-jump_30m)/jump_10m:.1f}% smaller)")
print(f"For reference, the 2005/2015 levels were {mean_2005:.2f}%/{mean_2015:.2f}% — even at 30m,")
print(f"2025's {mean_30m:.2f}% remains ~{mean_30m/mean_2015:.1f}x the 2015 level. This tests pixel size only;")
print(f"Landsat vs Sentinel-2 spectral/processing differences are not isolated by this check.")

gdf.to_file('data/processed/karewa_resolution_robustness_check.gpkg', driver='GPKG')

# ============================================================
# Part 2 — Effect sizes + Holm-Bonferroni across the 4 Mann-Whitney tests
# ============================================================
def rank_biserial(x, y, alternative='two-sided'):
    n1, n2 = len(x), len(y)
    U, p = mannwhitneyu(x, y, alternative=alternative)
    r = 1 - (2 * U) / (n1 * n2)
    return U, p, r

final = gpd.read_file('data/processed/karewa_final_with_geomorphometrics.gpkg')

# karewa_final_with_geomorphometrics.gpkg (written by script 10) never gets a
# dist_to_settlement_m column of its own — that column is only ever computed and
# written by script 14b, into a separate file (karewa_settlement_proximity.gpkg).
# Pull it in here explicitly by terrace id instead of assuming script 10 carries it,
# so this script is reproducible on a clean re-run regardless of what order 10/14a/14b
# happen to have left on disk. Run 09 -> 10 -> 14a -> 14b before this script.
# NOTE: 'terrace_candidate' is the raster value written by rasterio.features.shapes
# in script 01 and is 1 for EVERY polygon, so it cannot be used as a join key —
# merging on it produces a 201 x 201 = 40,401-row cross join and silently breaks
# every test below. Both files carry the same 201 polygons in the same row order
# (both descend from karewa_road_proximity.gpkg), so join by row position after
# asserting the geometries really are identical.
settlement = gpd.read_file('data/processed/karewa_settlement_proximity.gpkg')
assert len(settlement) == len(final), "settlement and final layers have different row counts"
assert settlement.geometry.geom_equals(final.geometry).all(), "row order differs between layers"
final = final.drop(columns=['dist_to_settlement_m'], errors='ignore')
final['dist_to_settlement_m'] = settlement['dist_to_settlement_m'].values

deg = final[final['status'] == 'likely_degraded']
intact = final[final['status'] == 'intact']

tests = {}
tests['road_proximity'] = rank_biserial(deg['dist_to_road_m'], intact['dist_to_road_m'], alternative='less') + ('degraded < intact, one-sided',)
tests['settlement_proximity'] = rank_biserial(deg['dist_to_settlement_m'], intact['dist_to_settlement_m'], alternative='less') + ('degraded < intact, one-sided',)
tests['compactness'] = rank_biserial(deg['compactness'], intact['compactness'], alternative='two-sided') + ('two-sided',)
tests['slope'] = rank_biserial(deg['mean_slope'].dropna(), intact['mean_slope'].dropna(), alternative='two-sided') + ('two-sided',)

print("\n=== Effect sizes (rank-biserial correlation r) for all 4 Mann-Whitney tests ===")
print(f"{'test':<20} {'U':>10} {'p_raw':>10} {'effect_r':>10}   note")
for k, (U, p, r, note) in tests.items():
    print(f"{k:<20} {U:>10.1f} {p:>10.4f} {r:>10.3f}   {note}")

pvals_sorted = sorted([(k, v[1]) for k, v in tests.items()], key=lambda x: x[1])
m = len(pvals_sorted)
print("\n--- Holm-Bonferroni correction across the 4 tests (family-wise alpha=0.05) ---")
stopped = False
survivors = []
for i, (k, p) in enumerate(pvals_sorted):
    adj_alpha = 0.05 / (m - i)
    # Holm is step-down: once one test fails, every later (larger-p) test also fails.
    if stopped or p >= adj_alpha:
        stopped = True
        sig = "not significant"
    else:
        sig = "SIGNIFICANT"
        survivors.append(k)
    print(f"rank {i+1}: {k}: p={p:.4f}, Holm-adjusted alpha={adj_alpha:.4f} -> {sig}")

print(f"\nSurvive Holm-Bonferroni: {', '.join(survivors) if survivors else 'none'}")
print("Note: these are terrace-level tests; spatial autocorrelation between neighbouring")
print("terraces is not modelled, so p-values may overstate the evidence.")
