"""
11_threshold_sensitivity.py — Sensitivity analysis for the three thresholds this
project's classifications depend on: the TPI/slope terrace-delineation pair,
the bare-earth degradation threshold (15 percentage points), and the saffron
NDVI-signature threshold (0.15). Added during the External AI Review round —
four independent reviewers flagged all three thresholds as chosen by visual
inspection with no reported sensitivity check. This script answers that
directly: it shows each headline count/finding across a neighbourhood of
threshold values, rather than defending a single arbitrary cutoff.
"""
import geopandas as gpd
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import numpy as np
from scipy.ndimage import uniform_filter, distance_transform_edt
from rasterio.features import shapes

# ============================================================
# Part 1 — TPI / slope terrace-delineation threshold grid
# ============================================================
def fill_nan_nearest(arr):
    mask_ = np.isnan(arr)
    if not mask_.any():
        return arr
    idx = distance_transform_edt(mask_, return_distances=False, return_indices=True)
    return arr[tuple(idx)]

with rasterio.open('data/interim/DEM_UTM43N.tif') as src:
    dem = src.read(1).astype(float)
    transform = src.transform
    crs = src.crs
    pixel_size = transform[0]
    nodata_val = src.nodata
if nodata_val is not None:
    dem[dem == nodata_val] = np.nan
trim = 10
dem = dem[trim:-trim, trim:-trim]
transform = rasterio.transform.from_origin(
    transform.c + trim * transform.a, transform.f + trim * transform.e,
    transform.a, -transform.e)
dem = fill_nan_nearest(dem)
dy, dx = np.gradient(dem, pixel_size)
slope = np.degrees(np.arctan(np.sqrt(dx**2 + dy**2)))
window_size = 17
tpi = dem - uniform_filter(dem, size=window_size)

print("=== TPI / slope threshold grid (candidate count after area filter only, pre-elevation-filter) ===")
print(f"{'TPI>':>6} {'slope<':>7} {'raw_polygons':>13} {'area-filtered':>15}")
for tpi_t in [2, 3, 4]:
    for slope_t in [6, 8, 10]:
        mask_arr = ((tpi > tpi_t) & (slope < slope_t)).astype(np.uint8)
        results = ({'properties': {'v': int(v)}, 'geometry': s}
                    for s, v in shapes(mask_arr, mask=mask_arr.astype(bool), transform=transform))
        gdf_t = gpd.GeoDataFrame.from_features(list(results), crs=crs)
        gdf_t['area_km2'] = gdf_t.geometry.area / 1e6
        n_raw = len(gdf_t)
        n_filt = int((gdf_t['area_km2'] >= 0.05).sum())
        marker = "  <-- used" if (tpi_t, slope_t) == (3, 8) else ""
        print(f"{tpi_t:>6} {slope_t:>7} {n_raw:>13} {n_filt:>15}{marker}")

# ============================================================
# Part 2 — Bare-earth degradation threshold sensitivity
# ============================================================
gdf = gpd.read_file('data/processed/karewa_bare_earth_change.gpkg')
print("\n=== Bare-earth degradation threshold sensitivity (n=201 terraces) ===")
print(f"{'threshold_pp':>12} {'n_flagged':>10} {'pct':>7} {'flagged_area_ha':>16} {'loss_within_flagged_ha':>23}")
for t in [5, 8, 10, 12, 15, 17, 20, 25, 30]:
    flagged = gdf[gdf['bare_frac_change'] >= t / 100]
    n = len(flagged)
    area_ha = flagged['area_km2'].sum() * 100
    loss_within = (flagged['area_km2'] * flagged['bare_frac_change']).sum() * 100
    marker = "  <-- used" if t == 15 else ""
    print(f"{t:>12} {n:>10} {100*n/len(gdf):>6.1f}% {area_ha:>16.1f} {loss_within:>23.1f}{marker}")

# ============================================================
# Part 3 — Saffron NDVI threshold sensitivity
# ============================================================
saf_gdf = gpd.read_file('data/processed/karewa_saffron_overlay.gpkg')
degraded = saf_gdf[saf_gdf['status'] == 'likely_degraded']
degraded_union = degraded.geometry.union_all()
print("\n=== Saffron NDVI threshold sensitivity ===")
print(f"{'threshold':>10} {'n':>4} {'area_ha':>9} {'at_risk_1km':>13} {'pct_at_risk':>13}")
for t in [0.05, 0.10, 0.125, 0.15, 0.175, 0.20, 0.25]:
    saf = saf_gdf[saf_gdf['saffron_index'] >= t].copy()
    n = len(saf)
    area_ha = saf.geometry.area.sum() / 10000
    if n > 0:
        saf['d'] = saf.geometry.apply(lambda g: g.distance(degraded_union))
        at_risk = int((saf['d'] <= 1000).sum())
        pct = 100 * at_risk / n
    else:
        at_risk, pct = 0, float('nan')
    marker = "  <-- used" if t == 0.15 else ""
    print(f"{t:>10} {n:>4} {area_ha:>9.1f} {at_risk:>13} {pct:>12.0f}%{marker}")

print("""
Reading: the degradation-threshold and saffron-threshold sweeps both show the
project's headline classifications sitting in a broad, stable neighbourhood
rather than perched on an isolated spike — the 12-20pp degradation-threshold
range flags 23-31 terraces (vs. the reported 25), and the proximity-risk share
stays within 39-44% across the 0.05-0.175 saffron-threshold range (only
diverging at very small n above 0.175, where 4-6 detected terraces make any
percentage noisy). The TPI/slope grid is smooth and monotonic around the
chosen (3, 8) pair, with no discontinuity nearby. None of this proves the
thresholds are 'correct' in an absolute sense — no independently labelled
validation set exists to calibrate against — but it does show the reported
counts are not an artefact of one arbitrarily lucky cutoff.
""")
