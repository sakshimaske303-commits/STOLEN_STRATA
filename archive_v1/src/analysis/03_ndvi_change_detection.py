import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

import geopandas as gpd
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.mask import mask
import numpy as np

DST_CRS = config.DST_CRS

def reproject_raster(src_path, dst_path, dst_crs=DST_CRS):
    with rasterio.open(src_path) as src:
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds)
        kwargs = src.meta.copy()
        kwargs.update({'crs': dst_crs, 'transform': transform, 'width': width, 'height': height})
        with rasterio.open(dst_path, 'w', **kwargs) as dst:
            reproject(
                source=rasterio.band(src, 1), destination=rasterio.band(dst, 1),
                src_transform=src.transform, src_crs=src.crs,
                dst_transform=transform, dst_crs=dst_crs,
                resampling=Resampling.bilinear)
    print(f"Reprojected {src_path} -> {dst_path}")

# --- Step 1: Reproject season-matched NDVI rasters ---
reproject_raster('data/raw/StolenStrata_NDVI_1994_v2.tif', 'data/interim/NDVI_1994_UTM43N.tif')
reproject_raster('data/raw/StolenStrata_NDVI_2025.tif', 'data/interim/NDVI_2025_UTM43N.tif')

# --- Step 2: Load karewa polygons ---
gdf = gpd.read_file('data/interim/karewa_candidates_filtered.gpkg')
print(f"Loaded {len(gdf)} karewa terrace polygons")

# --- Step 3: Zonal BARE-EARTH FRACTION per polygon (more sensitive than mean NDVI) ---
BARE_THRESHOLD = config.BARE_EARTH_NDVI_THRESHOLD  # pixels below this NDVI = bare earth / mining / built-up

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

gdf['bare_frac_1994'] = gdf.geometry.apply(lambda g: zonal_bare_fraction(g, 'data/interim/NDVI_1994_UTM43N.tif'))
gdf['bare_frac_2025'] = gdf.geometry.apply(lambda g: zonal_bare_fraction(g, 'data/interim/NDVI_2025_UTM43N.tif'))

# --- Step 4: Change in bare-earth fraction (positive = MORE bare earth now = degradation) ---
gdf['bare_frac_change'] = gdf['bare_frac_2025'] - gdf['bare_frac_1994']
print(gdf[['bare_frac_1994', 'bare_frac_2025', 'bare_frac_change']].describe())

# --- Step 5: Flag degrading terraces ---
loss_threshold = config.DEGRADATION_LOSS_THRESHOLD  # 15 percentage-point increase in bare-earth share — tune after seeing describe()
gdf['status'] = np.where(gdf['bare_frac_change'] >= loss_threshold, 'likely_degraded', 'intact')
print(gdf['status'].value_counts())

# --- Step 6: Save ---
gdf.to_file('data/processed/karewa_bare_earth_change.gpkg', driver='GPKG')
print("Saved to data/processed/karewa_bare_earth_change.gpkg")