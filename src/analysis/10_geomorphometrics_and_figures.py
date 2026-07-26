import geopandas as gpd
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu
from rasterio.mask import mask

# --- Step 1: Recompute and save slope from DEM (locally, reliable) ---
with rasterio.open('data/interim/DEM_UTM43N.tif') as src:
    dem = src.read(1).astype(float)
    transform = src.transform
    crs = src.crs
    profile = src.profile
    pixel_size = transform[0]

dy, dx = np.gradient(dem, pixel_size)
slope = np.degrees(np.arctan(np.sqrt(dx**2 + dy**2)))

profile.update(dtype=rasterio.float32, nodata=None)
with rasterio.open('data/interim/Slope_final_UTM43N.tif', 'w', **profile) as dst:
    dst.write(slope.astype(rasterio.float32), 1)
print("Slope raster saved.")

# --- Step 2: Load terrace data, compute geomorphic variables ---
gdf = gpd.read_file('data/processed/karewa_road_proximity.gpkg')

# Compactness index (4*pi*Area / Perimeter^2) — 1.0 = circular/compact, near 0 = elongated/dissected
gdf['compactness'] = (4 * np.pi * gdf.geometry.area) / (gdf.geometry.length ** 2)

def zonal_mean_slope(geom):
    with rasterio.open('data/interim/Slope_final_UTM43N.tif') as src:
        try:
            out_image, _ = mask(src, [geom], crop=True, nodata=np.nan)
            return float(np.nanmean(out_image))
        except Exception:
            return np.nan

gdf['mean_slope'] = gdf.geometry.apply(zonal_mean_slope)

# --- Step 3: Statistical comparison — degraded vs intact ---
print("\n--- Compactness (dissection degree) by status ---")
print(gdf.groupby('status')['compactness'].describe())
stat1, p1 = mannwhitneyu(gdf[gdf['status']=='likely_degraded']['compactness'],
                          gdf[gdf['status']=='intact']['compactness'])
print(f"Mann-Whitney U p-value (compactness): {p1:.4f}")

print("\n--- Mean internal slope by status ---")
print(gdf.groupby('status')['mean_slope'].describe())
stat2, p2 = mannwhitneyu(gdf[gdf['status']=='likely_degraded']['mean_slope'],
                          gdf[gdf['status']=='intact']['mean_slope'])
print(f"Mann-Whitney U p-value (slope): {p2:.4f}")

gdf.to_file('data/processed/karewa_final_with_geomorphometrics.gpkg', driver='GPKG')

# --- Step 4: FIRST static figures ---
import os
os.makedirs('outputs/figures', exist_ok=True)

# Figure 1: Terrace map colored by degradation status
fig, ax = plt.subplots(figsize=(10, 8))
gdf[gdf['status']=='intact'].plot(ax=ax, color='green', label='Intact', edgecolor='black', linewidth=0.3)
gdf[gdf['status']=='likely_degraded'].plot(ax=ax, color='red', label='Likely Degraded', edgecolor='black', linewidth=0.3)
ax.set_title('Stolen Strata: Karewa Terrace Degradation Status')
ax.legend()
ax.set_axis_off()
plt.savefig('outputs/figures/01_terrace_status_map.png', dpi=200, bbox_inches='tight')
plt.close()

# Figure 2: Four-point bare-earth trend
years = [1994, 2005, 2015, 2025]
means = [gdf['bare_frac_1994'].mean()*100, gdf['bare_frac_2005'].mean()*100,
         gdf['bare_frac_2015'].mean()*100, gdf['bare_frac_2025'].mean()*100]
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(years, means, marker='o', linewidth=2, color='darkred')
ax.set_xlabel('Year')
ax.set_ylabel('Mean Bare-Earth Fraction (%)')
ax.set_title('Karewa Degradation Trend (1994-2025)')
ax.grid(alpha=0.3)
plt.savefig('outputs/figures/02_degradation_trend.png', dpi=200, bbox_inches='tight')
plt.close()

# Figure 3: Compactness by status (boxplot)
fig, ax = plt.subplots(figsize=(6, 5))
gdf.boxplot(column='compactness', by='status', ax=ax)
ax.set_title('Terrace Compactness (Dissection Degree) by Status')
ax.set_ylabel('Compactness Index')
plt.suptitle('')
plt.savefig('outputs/figures/03_compactness_by_status.png', dpi=200, bbox_inches='tight')
plt.close()

# Figure 4: Distance to road by status (boxplot)
fig, ax = plt.subplots(figsize=(6, 5))
gdf.boxplot(column='dist_to_road_m', by='status', ax=ax)
ax.set_title('Distance to Nearest Road by Degradation Status')
ax.set_ylabel('Distance (m)')
plt.suptitle('')
plt.savefig('outputs/figures/04_road_distance_by_status.png', dpi=200, bbox_inches='tight')
plt.close()

print("\n4 static figures saved to outputs/figures/")