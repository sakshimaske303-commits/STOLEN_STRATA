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
            for band in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, band), destination=rasterio.band(dst, band),
                    src_transform=src.transform, src_crs=src.crs,
                    dst_transform=transform, dst_crs=dst_crs,
                    resampling=Resampling.bilinear)
    print(f"Reprojected {src_path} -> {dst_path}")

# --- Step 1: Reproject the 3-band saffron index raster (v2 — March window) ---
reproject_raster('data/raw/StolenStrata_SaffronIndex_2025_v2.tif', 'data/interim/SaffronIndex_UTM43N.tif')

# --- Step 2: Load terrace polygons (already carrying bare-earth degradation status) ---
gdf = gpd.read_file('data/processed/karewa_bare_earth_change.gpkg')
print(f"Loaded {len(gdf)} karewa terrace polygons")

# --- Step 3: Zonal mean Saffron Index per polygon (band 1 = Saffron_Index) ---
def zonal_mean_band(geom, raster_path, band=1):
    with rasterio.open(raster_path) as src:
        try:
            out_image, _ = mask(src, [geom], crop=True, nodata=np.nan, indexes=band)
            return float(np.nanmean(out_image))
        except Exception:
            return np.nan

gdf['saffron_index'] = gdf.geometry.apply(lambda g: zonal_mean_band(g, 'data/interim/SaffronIndex_UTM43N.tif', band=1))

print(gdf['saffron_index'].describe())

# --- Step 4: Classify likely-saffron terraces (tune threshold after seeing describe() above) ---
saffron_threshold = config.SAFFRON_INDEX_THRESHOLD
gdf['likely_saffron'] = gdf['saffron_index'] >= saffron_threshold
print(gdf['likely_saffron'].value_counts())

# --- Step 5: The key policy-relevant cross-tab — saffron land that is ALSO degraded ---
crosstab = gdf.groupby(['likely_saffron', 'status']).size()
print(crosstab)

# --- Step 6: Save ---
gdf.to_file('data/processed/karewa_saffron_overlay.gpkg', driver='GPKG')
print("Saved to data/processed/karewa_saffron_overlay.gpkg")