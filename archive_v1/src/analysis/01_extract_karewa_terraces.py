import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import numpy as np
from scipy.ndimage import uniform_filter, distance_transform_edt
import geopandas as gpd
from rasterio.features import shapes

def fill_nan_nearest(arr):
    mask = np.isnan(arr)
    if not mask.any():
        return arr
    idx = distance_transform_edt(mask, return_distances=False, return_indices=True)
    return arr[tuple(idx)]

# --- Step 1: Reproject DEM to UTM 43N (already validated working) ---
src_path = 'data/raw/StolenStrata_DEM_GLO30.tif'
utm_path = 'data/interim/DEM_UTM43N.tif'
dst_crs = config.DST_CRS

with rasterio.open(src_path) as src:
    src_nodata = src.nodata if src.nodata is not None else -9999.0
    transform, width, height = calculate_default_transform(
        src.crs, dst_crs, src.width, src.height, *src.bounds)
    kwargs = src.meta.copy()
    kwargs.update({'crs': dst_crs, 'transform': transform,
                    'width': width, 'height': height, 'nodata': src_nodata})

    with rasterio.open(utm_path, 'w', **kwargs) as dst:
        reproject(
            source=rasterio.band(src, 1), destination=rasterio.band(dst, 1),
            src_transform=src.transform, src_crs=src.crs,
            dst_transform=transform, dst_crs=dst_crs,
            src_nodata=src_nodata, dst_nodata=src_nodata,
            resampling=Resampling.bilinear)

# --- Step 2: Load, mask nodata, trim thin edge border, fill residual gaps ---
with rasterio.open(utm_path) as src:
    dem = src.read(1).astype(float)
    transform = src.transform
    crs = src.crs
    profile = src.profile
    pixel_size = transform[0]
    nodata_val = src.nodata

if nodata_val is not None:
    dem[dem == nodata_val] = np.nan

# Trim 10-pixel border where reprojection edge artifacts concentrate
trim = config.DEM_EDGE_TRIM_PX
dem = dem[trim:-trim, trim:-trim]
transform = rasterio.transform.from_origin(
    transform.c + trim * transform.a, transform.f + trim * transform.e,
    transform.a, -transform.e)

dem = fill_nan_nearest(dem)  # patch any remaining tiny gaps
print(f"DEM valid range after cleanup: {dem.min():.1f} / {dem.max():.1f}")

# --- Step 3: Slope + TPI ---
dy, dx = np.gradient(dem, pixel_size)
slope = np.degrees(np.arctan(np.sqrt(dx**2 + dy**2)))

window_size = config.TPI_WINDOW_SIZE
tpi = dem - uniform_filter(dem, size=window_size)

print(f"Slope range: {slope.min():.1f} / {slope.max():.1f}")
print(f"TPI range: {tpi.min():.2f} / {tpi.max():.2f} / mean {tpi.mean():.2f}")

# Calibrated thresholds (SS_Development_Log.md "Day 1") — TPI>5/slope<5 gave only
# 115 sliver candidates; TPI>3/slope<8 recovered 201 proper blob-shaped ones.
tpi_threshold = config.TPI_THRESHOLD
slope_threshold = config.SLOPE_THRESHOLD_DEG
karewa_mask = (tpi > tpi_threshold) & (slope < slope_threshold)
print(f"Karewa candidate pixels: {karewa_mask.sum()} out of {karewa_mask.size}")

if karewa_mask.sum() == 0:
    print("WARNING: still empty — thresholds need loosening.")
    exit()

# --- Step 4: Save + vectorize ---
profile.update(dtype=rasterio.uint8, count=1, height=dem.shape[0], width=dem.shape[1],
               transform=transform, crs=crs, nodata=None)
with rasterio.open('data/interim/karewa_candidate_mask.tif', 'w', **profile) as dst:
    dst.write(karewa_mask.astype(rasterio.uint8), 1)

mask = karewa_mask.astype(np.uint8)
results = (
    {'properties': {'terrace_candidate': int(v)}, 'geometry': s}
    for s, v in shapes(mask, mask=mask.astype(bool), transform=transform)
)
gdf = gpd.GeoDataFrame.from_features(list(results), crs=crs)
gdf.to_file('data/interim/karewa_candidates.gpkg', driver='GPKG')
print(f"Found {len(gdf)} candidate terrace polygons")