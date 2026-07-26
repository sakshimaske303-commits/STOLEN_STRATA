import geopandas as gpd
import rasterio
from rasterio.mask import mask
import numpy as np

gdf = gpd.read_file('data/interim/karewa_candidates.gpkg')
gdf['area_km2'] = gdf.geometry.area / 1e6

print(f"Total polygons: {len(gdf)}")
print(gdf['area_km2'].describe())

min_area_km2 = 0.05
filtered = gdf[gdf['area_km2'] >= min_area_km2].copy()
print(f"Polygons after area filter (>= {min_area_km2} km2): {len(filtered)}")

# --- Elevation filter: karewas are valley-floor-adjacent, not high-mountain ridges ---
def get_mean_elevation(geom, src):
    try:
        out_image, _ = mask(src, [geom], crop=True, nodata=np.nan)
        return np.nanmean(out_image)
    except Exception:
        return np.nan

with rasterio.open('data/interim/DEM_UTM43N.tif') as src:
    filtered['mean_elevation'] = filtered.geometry.apply(lambda g: get_mean_elevation(g, src))

elevation_min, elevation_max = 1550, 2000
filtered_elev = filtered[
    (filtered['mean_elevation'] >= elevation_min) & (filtered['mean_elevation'] <= elevation_max)
].copy()
print(f"Polygons after elevation filter ({elevation_min}-{elevation_max}m): {len(filtered_elev)}")

filtered_elev.to_file('data/interim/karewa_candidates_filtered.gpkg', driver='GPKG')