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

# --- Step 1: Reproject the two new years (1994 and 2025 already reprojected earlier) ---
reproject_raster('data/raw/StolenStrata_NDVI_2005.tif', 'data/interim/NDVI_2005_UTM43N.tif')
reproject_raster('data/raw/StolenStrata_NDVI_2015.tif', 'data/interim/NDVI_2015_UTM43N.tif')

# --- Step 2: Load terrace polygons ---
gdf = gpd.read_file('data/processed/karewa_bare_earth_change.gpkg')
print(f"Loaded {len(gdf)} karewa terrace polygons")

# --- Step 3: Zonal bare-earth fraction for each of 4 years ---
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

gdf['bare_frac_2005'] = gdf.geometry.apply(lambda g: zonal_bare_fraction(g, 'data/interim/NDVI_2005_UTM43N.tif'))
gdf['bare_frac_2015'] = gdf.geometry.apply(lambda g: zonal_bare_fraction(g, 'data/interim/NDVI_2015_UTM43N.tif'))

# --- Step 4: Build the 4-point trend summary (mean across all 201 polygons, per year) ---
years = [1994, 2005, 2015, 2025]
cols = ['bare_frac_1994', 'bare_frac_2005', 'bare_frac_2015', 'bare_frac_2025']

print("\n--- Mean bare-earth fraction across all 201 terraces, by year ---")
for year, col in zip(years, cols):
    mean_val = gdf[col].mean() * 100
    print(f"{year}: {mean_val:.2f}%")

# --- Step 5: Save enriched dataset ---
gdf.to_file('data/processed/karewa_multitemporal_trend.gpkg', driver='GPKG')
print("\nSaved to data/processed/karewa_multitemporal_trend.gpkg")